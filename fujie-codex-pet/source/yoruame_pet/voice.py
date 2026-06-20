from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceResult:
    text: str | None
    available: bool
    message: str


@dataclass(frozen=True)
class VoiceSpeakResult:
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
                message="我现在还听不清，缺少 speech_recognition 或麦克风依赖，哥哥先打字给我嘛。",
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


class VoiceSpeaker:
    def __init__(self, enabled: bool = True, rate: int = 0, volume: int = 90) -> None:
        self.enabled = enabled
        self.rate = max(-10, min(10, rate))
        self.volume = max(0, min(100, volume))

    def speak(self, text: str) -> VoiceSpeakResult:
        clean_text = text.strip()
        if not self.enabled:
            return VoiceSpeakResult(
                available=False,
                message="我现在还不能出声，哥哥先看气泡嘛。",
            )
        if not clean_text:
            return VoiceSpeakResult(
                available=False,
                message="没有要说的话。",
            )
        if os.name != "nt":
            return VoiceSpeakResult(
                available=False,
                message="这个系统暂时不能用 Windows 语音朗读。",
            )

        powershell = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        if not os.path.exists(powershell):
            powershell = "powershell.exe"
        script = (
            "Add-Type -AssemblyName System.Speech; "
            "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$speaker.Rate = {self.rate}; "
            f"$speaker.Volume = {self.volume}; "
            "$speaker.Speak($env:YORUAME_TTS_TEXT)"
        )
        env = os.environ.copy()
        env["YORUAME_TTS_TEXT"] = clean_text
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            subprocess.Popen(
                [
                    powershell,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    script,
                ],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creationflags,
            )
        except Exception:
            return VoiceSpeakResult(
                available=False,
                message="我现在还不能出声，哥哥先看气泡嘛。",
            )
        return VoiceSpeakResult(available=True, message="我说给你听了。")
