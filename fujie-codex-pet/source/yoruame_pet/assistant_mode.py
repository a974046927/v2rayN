from __future__ import annotations

from dataclasses import dataclass

from .ai_provider import AIProvider
from .local_search import LocalSearch


@dataclass(frozen=True)
class AssistantAnswer:
    text: str
    source: str
    pet_line: str
    citations: list[str]


class PetAssistant:
    def __init__(self, local_search: LocalSearch, ai_provider: AIProvider) -> None:
        self.local_search = local_search
        self.ai_provider = ai_provider

    def ask(self, question: str) -> AssistantAnswer:
        clean_question = question.strip()
        if not clean_question:
            return AssistantAnswer(
                text="问题是空的。",
                source="fallback",
                pet_line="哥哥，你还没问我呢。",
                citations=[],
            )

        local = self.local_search.answer(clean_question)
        if local is not None:
            return AssistantAnswer(
                text=local.text,
                source="local",
                pet_line=f"哥哥，我在本地翻到了：{local.text}",
                citations=local.citations,
            )

        ai_result = self.ai_provider.answer(clean_question)
        if ai_result.available:
            return AssistantAnswer(
                text=ai_result.text,
                source="ai",
                pet_line=f"我问到了，哥哥：{ai_result.text}",
                citations=[],
            )

        return AssistantAnswer(
            text=ai_result.text,
            source="fallback",
            pet_line="哥哥，我本地没查到，外部 AI 也还没接上。你先打字给我嘛。",
            citations=[],
        )
