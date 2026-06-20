import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class CodexDialogueTests(unittest.TestCase):
    def test_bridge_returns_codex_thread_answer(self):
        from yoruame_pet.codex_dialogue import CodexDialogueBridge, CodexDialogueResult

        class FakeClient:
            def __init__(self):
                self.questions = []

            def ask(self, question: str) -> CodexDialogueResult:
                self.questions.append(question)
                return CodexDialogueResult(
                    text="\u54e5\u54e5\uff0c\u6211\u4ece\u5ba0\u7269\u5bf9\u8bdd\u91cc\u542c\u5230\u4e86\u3002",
                    thread_id="thread-1",
                )

        client = FakeClient()
        bridge = CodexDialogueBridge(enabled=True, client=client)

        answer = bridge.ask("\u4f60\u542c\u5f97\u5230\u5417")

        self.assertIsNotNone(answer)
        assert answer is not None
        self.assertEqual(client.questions, ["\u4f60\u542c\u5f97\u5230\u5417"])
        self.assertEqual(answer.source, "codex_thread")
        self.assertEqual(answer.text, "\u54e5\u54e5\uff0c\u6211\u4ece\u5ba0\u7269\u5bf9\u8bdd\u91cc\u542c\u5230\u4e86\u3002")
        self.assertEqual(answer.pet_line, "\u54e5\u54e5\uff0c\u6211\u4ece\u5ba0\u7269\u5bf9\u8bdd\u91cc\u542c\u5230\u4e86\u3002")

    def test_node_client_sends_question_to_helper_as_utf8_json(self):
        from yoruame_pet.codex_dialogue import NodeCodexDialogueClient

        calls = []

        def fake_run(*args, **kwargs):
            calls.append((args, kwargs))
            payload = json.loads(kwargs["input"])
            self.assertEqual(payload["question"], "\u4eca\u5929\u8981\u4e0d\u8981\u4f11\u606f")
            self.assertEqual(payload["threadId"], "thread-1")
            self.assertEqual(payload["threadName"], "\u5ba0\u7269\u5bf9\u8bdd")
            return subprocess.CompletedProcess(
                args=args[0],
                returncode=0,
                stdout=json.dumps(
                    {
                        "ok": True,
                        "text": "\u54e5\u54e5\uff0c\u8d77\u6765\u8d70\u4e00\u4e0b\u3002",
                        "threadId": "thread-1",
                    },
                    ensure_ascii=False,
                ),
                stderr="",
            )

        client = NodeCodexDialogueClient(
            node_exe="node.exe",
            helper_script=Path("bridge.mjs"),
            codex_exe="codex.exe",
            cwd=Path("E:/Codex \u9879\u76ee/\u6742\u8c08"),
            thread_id="thread-1",
            thread_name="\u5ba0\u7269\u5bf9\u8bdd",
            model="gpt-5.4-mini",
            timeout_seconds=12,
            runner=fake_run,
        )

        result = client.ask("\u4eca\u5929\u8981\u4e0d\u8981\u4f11\u606f")

        self.assertEqual(result.text, "\u54e5\u54e5\uff0c\u8d77\u6765\u8d70\u4e00\u4e0b\u3002")
        self.assertEqual(result.thread_id, "thread-1")
        self.assertEqual(calls[0][0][0][:2], ["node.exe", "bridge.mjs"])
        self.assertTrue(calls[0][1]["text"])
        self.assertEqual(calls[0][1]["encoding"], "utf-8")
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            self.assertEqual(calls[0][1]["creationflags"], subprocess.CREATE_NO_WINDOW)

    def test_node_helper_hides_spawned_codex_window(self):
        helper = ROOT / "src" / "yoruame_pet" / "codex_app_bridge.mjs"

        text = helper.read_text(encoding="utf-8")

        self.assertIn("windowsHide: true", text)


if __name__ == "__main__":
    unittest.main()
