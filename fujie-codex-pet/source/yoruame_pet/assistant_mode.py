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
    def __init__(self, local_search: LocalSearch, ai_provider: AIProvider | None = None) -> None:
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

        local_reply = self._local_pet_reply(clean_question)
        return AssistantAnswer(
            text=local_reply,
            source="local_pet",
            pet_line=local_reply,
            citations=[],
        )

    def _local_pet_reply(self, question: str) -> str:
        lowered = question.lower()
        if any(word in question for word in ["休息", "累", "困", "头疼", "眼睛"]):
            return "哥哥，先停一下嘛。水喝一点，眼睛也放松一下，我在这里等你。"
        if any(word in question for word in ["喜欢", "爱", "想我", "陪我"]):
            return "凌凌哥哥当然要陪我呀。你看着我的时候，我就会乖一点点♡"
        if any(word in question for word in ["生气", "不理", "忙"]):
            return "哥哥又想把我晾在旁边？哼……那你现在多跟我说两句。"
        if any(word in question for word in ["天气", "下雨", "太阳", "晴"]):
            return "哥哥，天气这块我会按本地设置提醒你。你先告诉我城市，我就记得更准。"
        if any(word in lowered for word in ["hi", "hello"]) or any(
            word in question for word in ["你好", "在吗", "富江"]
        ):
            return "哥哥，我在。你刚刚叫我，我听到了。"
        return "哥哥，这个我本地资料里没翻到，不过我可以陪你慢慢聊。你再说细一点嘛。"
