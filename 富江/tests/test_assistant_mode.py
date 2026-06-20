import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class AssistantModeTests(unittest.TestCase):
    def test_local_search_finds_relevant_design_snippet(self):
        from yoruame_pet.local_search import LocalSearch

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = root / "FUJIE_DESIGN_SPEC.md"
            doc.write_text(
                "少女模式只使用夜雨哥哥、哥哥、凌凌哥哥。分裂脸用于惊吓状态。",
                encoding="utf-8",
            )

            result = LocalSearch([root]).answer("少女模式怎么称呼我")

        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.source, "local")
        self.assertIn("夜雨哥哥", result.text)
        self.assertIn("FUJIE_DESIGN_SPEC.md", result.citations[0])

    def test_assistant_answers_from_local_search_before_ai(self):
        from yoruame_pet.ai_provider import UnavailableAIProvider
        from yoruame_pet.assistant_mode import PetAssistant
        from yoruame_pet.local_search import LocalSearch

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes.md").write_text("待机动画使用 520ms，避免动作太快。", encoding="utf-8")
            assistant = PetAssistant(LocalSearch([root]), UnavailableAIProvider())

            answer = assistant.ask("待机动作速度是多少")

        self.assertEqual(answer.source, "local")
        self.assertIn("520ms", answer.text)
        self.assertIn("哥哥", answer.pet_line)

    def test_assistant_falls_back_to_local_pet_reply_without_external_ai(self):
        from yoruame_pet.assistant_mode import PetAssistant
        from yoruame_pet.local_search import LocalSearch

        with tempfile.TemporaryDirectory() as temp:
            assistant = PetAssistant(LocalSearch([Path(temp)]))

            answer = assistant.ask("帮我查一个不存在的问题")

        self.assertEqual(answer.source, "local_pet")
        self.assertIn("哥哥", answer.pet_line)
        self.assertNotIn("外部 AI", answer.pet_line)
        self.assertNotIn("没接上", answer.pet_line)

    def test_voice_recognizer_reports_unavailable_without_crashing(self):
        from yoruame_pet.voice import VoiceRecognizer

        result = VoiceRecognizer(enabled=False).listen()

        self.assertFalse(result.available)
        self.assertIsNone(result.text)
        self.assertIn("听不清", result.message)


if __name__ == "__main__":
    unittest.main()
