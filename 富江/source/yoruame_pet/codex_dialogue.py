from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol

from .assistant_mode import AssistantAnswer


class CodexDialogueError(RuntimeError):
    pass


@dataclass(frozen=True)
class CodexDialogueResult:
    text: str
    thread_id: str | None = None


class CodexDialogueClient(Protocol):
    def ask(self, question: str) -> CodexDialogueResult:
        ...


Runner = Callable[..., subprocess.CompletedProcess[str]]


class NodeCodexDialogueClient:
    def __init__(
        self,
        *,
        node_exe: str,
        helper_script: Path,
        codex_exe: str,
        cwd: Path,
        thread_id: str | None,
        thread_name: str,
        model: str | None,
        timeout_seconds: int,
        runner: Runner = subprocess.run,
        developer_instructions: str | None = None,
        startup_service_tier: str = "fast",
    ) -> None:
        self.node_exe = node_exe
        self.helper_script = helper_script
        self.codex_exe = codex_exe
        self.cwd = cwd
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.runner = runner
        self.developer_instructions = developer_instructions
        self.startup_service_tier = startup_service_tier

    def ask(self, question: str) -> CodexDialogueResult:
        payload = {
            "codexExe": self.codex_exe,
            "cwd": str(self.cwd),
            "threadId": self.thread_id,
            "threadName": self.thread_name,
            "question": question,
            "model": self.model,
            "timeoutMs": self.timeout_seconds * 1000,
            "developerInstructions": self.developer_instructions,
            "startupServiceTier": self.startup_service_tier,
            "allowCreateOnResumeFailure": True,
        }
        completed = self.runner(
            [self.node_exe, str(self.helper_script)],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=self.timeout_seconds + 20,
            check=False,
        )
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or "").strip()
            raise CodexDialogueError(detail or f"Codex bridge exited with {completed.returncode}")
        try:
            data = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise CodexDialogueError("Codex bridge returned invalid JSON") from exc
        if not data.get("ok"):
            raise CodexDialogueError(str(data.get("error") or "Codex bridge failed"))
        text = str(data.get("text") or "").strip()
        if not text:
            raise CodexDialogueError("Codex bridge returned an empty reply")
        thread_id = data.get("threadId")
        if isinstance(thread_id, str) and thread_id:
            self.thread_id = thread_id
        return CodexDialogueResult(text=text, thread_id=self.thread_id)


class CodexDialogueBridge:
    def __init__(self, *, enabled: bool, client: CodexDialogueClient | None) -> None:
        self.enabled = enabled
        self.client = client

    def ask(self, question: str) -> AssistantAnswer | None:
        clean_question = question.strip()
        if not self.enabled or self.client is None or not clean_question:
            return None
        try:
            result = self.client.ask(clean_question)
        except Exception:
            return None
        text = result.text.strip()
        if not text:
            return None
        return AssistantAnswer(text=text, source="codex_thread", pet_line=text, citations=[])


def default_codex_exe() -> str:
    configured = os.environ.get("CODEX_CLI_PATH")
    if configured:
        return configured
    return str(Path.home() / "AppData" / "Local" / "OpenAI" / "Codex" / "bin" / "codex.exe")


def default_node_exe() -> str:
    bundled = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "node"
        / "bin"
        / "node.exe"
    )
    return str(bundled) if bundled.exists() else "node"


def build_codex_dialogue_bridge(config: dict, fallback_cwd: Path) -> CodexDialogueBridge | None:
    if not bool(config.get("enabled", False)):
        return None
    helper_script = Path(__file__).with_name("codex_app_bridge.mjs")
    timeout_seconds = int(config.get("timeout_seconds", 120))
    client = NodeCodexDialogueClient(
        node_exe=str(config.get("node_exe") or default_node_exe()),
        helper_script=helper_script,
        codex_exe=str(config.get("codex_exe") or default_codex_exe()),
        cwd=Path(config.get("cwd") or fallback_cwd),
        thread_id=str(config.get("thread_id") or "") or None,
        thread_name=str(config.get("thread_name") or "\u5ba0\u7269\u5bf9\u8bdd"),
        model=str(config.get("model") or "") or None,
        timeout_seconds=timeout_seconds,
        developer_instructions=str(config.get("developer_instructions") or "") or None,
        startup_service_tier=str(config.get("startup_service_tier") or "fast"),
    )
    return CodexDialogueBridge(enabled=True, client=client)
