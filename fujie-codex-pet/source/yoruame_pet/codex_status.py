from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CodexTaskStatus:
    state: str
    line: str
    mood: str
    active: bool
    intensity: int = 4


class CodexTaskStatusWatcher:
    """Read local Codex session events and turn them into pet status lines."""

    def __init__(self, sessions_root: str | Path, tail_bytes: int = 131_072) -> None:
        self.sessions_root = Path(sessions_root).expanduser()
        self.tail_bytes = tail_bytes
        self._active_path: Path | None = None
        self._offsets: dict[Path, int] = {}
        self._last_signature: tuple[str, str] | None = None

    def poll(self) -> CodexTaskStatus | None:
        path = self._latest_session_file()
        if path is None:
            return None
        latest: CodexTaskStatus | None = None
        for event in self._read_new_events(path):
            status = status_from_session_event(event)
            if status is not None:
                latest = status
        if latest is None:
            return None
        signature = (latest.state, latest.line)
        if signature == self._last_signature:
            return None
        self._last_signature = signature
        return latest

    def _latest_session_file(self) -> Path | None:
        if not self.sessions_root.exists():
            return None
        candidates = [path for path in self.sessions_root.rglob("*.jsonl") if path.is_file()]
        if not candidates:
            return None
        return max(candidates, key=lambda path: path.stat().st_mtime)

    def _read_new_events(self, path: Path) -> list[dict[str, Any]]:
        size = path.stat().st_size
        offset = self._offsets.get(path)
        skip_partial = False
        if path != self._active_path or offset is None or offset > size:
            offset = 0 if size <= self.tail_bytes else size - self.tail_bytes
            skip_partial = offset > 0
        events: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            handle.seek(offset)
            if skip_partial:
                handle.readline()
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict):
                    events.append(value)
            self._offsets[path] = handle.tell()
        self._active_path = path
        return events


def status_from_session_event(event: dict[str, Any]) -> CodexTaskStatus | None:
    event_type = event.get("type")
    payload = event.get("payload")
    if not isinstance(payload, dict):
        return None

    if event_type == "event_msg":
        inner_type = payload.get("type")
        if inner_type == "task_started":
            return CodexTaskStatus(
                state="started",
                line="Codex 开始做事啦，哥哥别偷懒。",
                mood="work",
                active=True,
                intensity=5,
            )
        if inner_type == "task_complete":
            return CodexTaskStatus(
                state="complete",
                line="Codex 做完啦，哥哥快看结果。",
                mood="happy",
                active=False,
                intensity=4,
            )
        if inner_type == "agent_message":
            return CodexTaskStatus(
                state="report",
                line="Codex 正在回话，哥哥看这里。",
                mood="review",
                active=True,
                intensity=4,
            )
        return None

    if event_type != "response_item":
        return None

    item_type = payload.get("type")
    if item_type == "function_call":
        return _status_for_tool_call(str(payload.get("name") or ""))
    if item_type == "function_call_output":
        return CodexTaskStatus(
            state="tool_result",
            line="工具结果回来啦，我在帮哥哥盯着。",
            mood="review",
            active=True,
            intensity=4,
        )
    return None


def _status_for_tool_call(name: str) -> CodexTaskStatus:
    normalized = name.lower()
    if "apply_patch" in normalized or "update_file" in normalized or "create_file" in normalized:
        return CodexTaskStatus(
            state="editing",
            line="Codex 在改文件，哥哥先别急。",
            mood="work",
            active=True,
            intensity=5,
        )
    if "shell" in normalized or "command" in normalized:
        return CodexTaskStatus(
            state="command",
            line="Codex 在跑命令，我替哥哥盯着。",
            mood="work",
            active=True,
            intensity=5,
        )
    if "github" in normalized:
        return CodexTaskStatus(
            state="github",
            line="Codex 在同步 GitHub，哥哥等我一下。",
            mood="review",
            active=True,
            intensity=4,
        )
    if "web" in normalized or "search" in normalized:
        return CodexTaskStatus(
            state="research",
            line="Codex 在查资料，哥哥别分心。",
            mood="review",
            active=True,
            intensity=4,
        )
    return CodexTaskStatus(
        state="tool",
        line="Codex 在调用工具，我看着呢。",
        mood="work",
        active=True,
        intensity=4,
    )
