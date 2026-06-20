from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceResult:
    text: str | None
    available: bool
    message: str


class VoiceRecognizer:
    def __init__(self, enabled: bool = True, timeout_seconds: int = 5) -> None:
        self.enabled = enabled
        self.timeout_seconds = timeout_seconds

    def listen(self) -> VoiceResult:
        if not self.enabled:
            return VoiceResult(
                text=None,
                available=False,
                message="我现在还听不清，哥哥先打字给我嘛。",
            )
        try:
            import speech_recognition as sr  # type: ignore[import-not-found]
        except Exception:
            return VoiceResult(
                text=None,
                available=False,
                message="我现在还听不清，哥哥先打字给我嘛。",
            )

        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=self.timeout_seconds)
            text = recognizer.recognize_google(audio, language="zh-CN")
        except Exception:
            return VoiceResult(
                text=None,
                available=False,
                message="我刚刚没听清，哥哥先打字给我嘛。",
            )
        return VoiceResult(text=text, available=True, message="我听到了。")
