import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def write_event(path: Path, event_type: str, payload: dict) -> None:
    event = {
        "timestamp": "2026-06-21T01:00:00.000Z",
        "type": event_type,
        "payload": payload,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


class CodexStatusTests(unittest.TestCase):
    def test_watcher_reads_codex_task_progress_from_latest_session(self):
        from yoruame_pet.codex_status import CodexTaskStatusWatcher

        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp) / "rollout-test.jsonl"
            watcher = CodexTaskStatusWatcher(Path(tmp))

            write_event(session, "event_msg", {"type": "task_started"})
            started = watcher.poll()

            write_event(
                session,
                "response_item",
                {"type": "function_call", "name": "shell_command"},
            )
            running = watcher.poll()

            write_event(session, "event_msg", {"type": "task_complete"})
            complete = watcher.poll()

        self.assertIsNotNone(started)
        self.assertEqual(started.state, "started")
        self.assertTrue(started.active)
        self.assertIsNotNone(running)
        self.assertEqual(running.state, "command")
        self.assertTrue(running.active)
        self.assertIsNotNone(complete)
        self.assertEqual(complete.state, "complete")
        self.assertFalse(complete.active)

    def test_app_can_show_codex_task_status_in_bubble(self):
        from yoruame_pet.app import YoruamePetApp
        from yoruame_pet.config import default_config

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session_dir = root / "sessions"
            session_dir.mkdir()
            session = session_dir / "rollout-test.jsonl"
            config = default_config()
            config["paths"]["state_path"] = str(root / "state.json")
            config["paths"]["log_path"] = str(root / "pet.log")
            config["codex_status"] = {
                "enabled": True,
                "sessions_root": str(session_dir),
                "poll_ms": 1000,
                "show_seconds": 4,
            }
            config_path = root / "settings.json"
            config_path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
            app = YoruamePetApp(config_path=config_path, headless=True)

            write_event(session, "event_msg", {"type": "task_started"})
            handled = app.check_codex_status_once()

        self.assertTrue(handled)
        self.assertEqual(app.current_animation, "running")
        self.assertEqual(app.bubble_mood, "work")
        self.assertIn("Codex", app.bubble_text)


if __name__ == "__main__":
    unittest.main()
