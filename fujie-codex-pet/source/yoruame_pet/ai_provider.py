from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AIResult:
    text: str
    available: bool


class AIProvider(Protocol):
    def answer(self, question: str) -> AIResult:
        ...


class UnavailableAIProvider:
    def answer(self, question: str) -> AIResult:
        return AIResult(
            text="我现在还没有接上外部 AI，先把能在本地查到的告诉你。",
            available=False,
        )
