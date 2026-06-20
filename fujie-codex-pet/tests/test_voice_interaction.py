import sys
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class VoiceInteractionTests(unittest.TestCase):
    def test_voice_question_answers_recognized_text_and_speaks_reply(self):
        from yoruame_pet.app import YoruamePetApp
        from yoruame_pet.assistant_mode import AssistantAnswer
        from yoruame_pet.voice import VoiceResult

        class FakeRecognizer:
            def listen(self):
                return VoiceResult(text="待机动作速度是多少", available=True, message="我听到了。")

        class FakeAssistant:
            def __init__(self):
                self.questions = []

            def ask(self, question: str) -> AssistantAnswer:
                self.questions.append(question)
                return AssistantAnswer(
                    text="待机现在慢一点。",
                    source="ai",
                    pet_line="哥哥，我查到了，待机现在慢一点。",
                    citations=[],
                )

        class FakeSpeaker:
            def __init__(self):
                self.spoken = []

            def speak(self, text: str):
                self.spoken.append(text)

        app = YoruamePetApp(headless=True)
        assistant = FakeAssistant()
        speaker = FakeSpeaker()
        app.voice_recognizer = FakeRecognizer()
        app.assistant = assistant
        app.voice_speaker = speaker

        result = app.listen_for_question()

        self.assertTrue(result.available)
        self.assertEqual(assistant.questions, ["待机动作速度是多少"])
        self.assertEqual(app.bubble_text, "哥哥，我查到了，待机现在慢一点。")
        self.assertEqual(app.bubble_mood, "review")
        self.assertEqual(speaker.spoken, ["哥哥，我查到了，待机现在慢一点。"])

    def test_start_voice_interaction_listens_in_background(self):
        from yoruame_pet.app import YoruamePetApp
        from yoruame_pet.assistant_mode import AssistantAnswer
        from yoruame_pet.voice import VoiceResult

        class FakeRoot:
            def after(self, _delay_ms, callback=None):
                if callback is not None:
                    callback()
                return "after-id"

        class BlockingRecognizer:
            def __init__(self):
                self.started = threading.Event()
                self.release = threading.Event()

            def listen(self):
                self.started.set()
                self.release.wait(timeout=2)
                return VoiceResult(text="你听得到吗", available=True, message="我听到了。")

        class FakeAssistant:
            def ask(self, question: str) -> AssistantAnswer:
                return AssistantAnswer(
                    text=f"听得到：{question}",
                    source="ai",
                    pet_line=f"听得到：{question}",
                    citations=[],
                )

        class FakeSpeaker:
            def speak(self, _text: str):
                return None

        app = YoruamePetApp(headless=True)
        recognizer = BlockingRecognizer()
        app.root = FakeRoot()
        app.voice_recognizer = recognizer
        app.assistant = FakeAssistant()
        app.voice_speaker = FakeSpeaker()

        start = time.monotonic()
        app.start_voice_interaction()
        elapsed = time.monotonic() - start

        self.assertLess(elapsed, 0.25)
        self.assertTrue(recognizer.started.wait(timeout=1))
        self.assertTrue(app.voice_listening)
        self.assertIn("我在听", app.bubble_text)

        recognizer.release.set()
        deadline = time.monotonic() + 2
        while app.voice_listening and time.monotonic() < deadline:
            time.sleep(0.01)

        self.assertFalse(app.voice_listening)
        self.assertEqual(app.bubble_text, "听得到：你听得到吗")

    def test_voice_speaker_disabled_reports_safe_fallback(self):
        from yoruame_pet.voice import VoiceSpeaker

        result = VoiceSpeaker(enabled=False).speak("哥哥，我在。")

        self.assertFalse(result.available)
        self.assertIn("出声", result.message)


if __name__ == "__main__":
    unittest.main()
