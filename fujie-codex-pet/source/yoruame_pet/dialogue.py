from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable

GIRL_APPROVED_NAMES = ("夜雨哥哥", "哥哥", "凌凌哥哥")


@dataclass(frozen=True)
class DialogueContext:
    persona: str
    mood: str
    trigger: str
    name: str
    affection: int = 5
    intensity: int = 3


class DialogueBook:
    """Local emotion-driven dialogue generator with short, spoken lines."""

    def __init__(self, names: Iterable[str]) -> None:
        self.names = list(names) or ["夜雨"]
        self.names_by_persona = {
            "girl": list(GIRL_APPROVED_NAMES),
            "mature": self.names,
        }
        self.voice = {
            "girl": {
                "softeners": ["嘛", "呀", "哦", "啦", "呢"],
                "suffix": ["♡", "♪", "ฅ", "✨", ""],
            },
            "mature": {
                "softeners": ["嗯", "听话", "先这样", "别乱来", "过来"],
                "suffix": ["。", "…", "♡", ""],
            },
        }
        self.moods = {
            "happy": {
                "react": ["你终于看我了", "我刚还在等你", "嗯？看到我啦", "这下舒服了"],
                "nudge": ["再陪我一下嘛", "别马上跑掉", "看这边", "靠近一点也行"],
                "after": ["我会乖", "就一小会儿", "算你有良心", "今天先不闹你"],
            },
            "shy": {
                "react": ["等下", "别点那里", "裙子会乱", "我脸有点热"],
                "nudge": ["手先拿开啦", "别一直看", "真的会害羞", "装作没发生也行"],
                "after": ["哥哥坏", "我躲一下", "只许这一次", "哼，不许笑"],
            },
            "annoyed": {
                "react": ["你刚刚是不是忘了我", "我等得要吃醋了", "我有点生气", "哼，终于想起我了"],
                "nudge": ["看我", "说句话", "别不理我", "现在理我一下"],
                "after": ["这次先记着", "我要吃醋了", "别再这样", "补偿我"],
            },
            "calm": {
                "react": ["眼睛别硬撑", "肩放松", "停一下", "你太紧了"],
                "nudge": ["先休息半分钟", "看我，不看屏幕", "呼吸慢一点", "别逞强"],
                "after": ["听话", "我数着", "就现在", "别让我催第二遍"],
            },
            "scare": {
                "react": ["吓到了？", "醒了吗", "刚才很近吧", "心跳快了没"],
                "nudge": ["别怕，我在", "谁让你不理我", "我只是贴近一点", "吐舌头给你看"],
                "after": ["下次还敢吗", "摸摸头就原谅你", "醒了就好", "我没走"],
            },
            "work": {
                "react": ["先别分心", "这一段快了", "我看着呢", "手别停"],
                "nudge": ["先做完这点", "别急着切走", "继续写", "把这一小段收掉"],
                "after": ["做完再陪我", "我等你", "乖一点", "别偷懒"],
            },
            "review": {
                "react": ["这里再看一眼", "慢一点", "别跳太快", "这处别糊弄"],
                "nudge": ["确认完再走", "我陪你看", "先别急", "把这儿收干净"],
                "after": ["过了再继续", "我盯着", "别偷懒", "嗯，就这样"],
            },
            "rest": {
                "react": ["眼睛该休息了", "你又撑太久", "停一下", "喝口水吧"],
                "nudge": ["离开屏幕三分钟", "眨眨眼", "肩膀放松", "先别工作"],
                "after": ["回来我还在", "我等你", "别让我担心", "乖"],
            },
            "move": {
                "react": ["坐太久了", "腿该动一下", "起来一下", "别窝着啦"],
                "nudge": ["走两步", "伸个懒腰", "站起来", "去门口转一圈"],
                "after": ["我等你回来", "别偷偷坐回去", "回来再说", "听话嘛"],
            },
            "late_night": {
                "react": ["都这么晚了", "还不睡呀", "该收了", "你真的不困吗"],
                "nudge": ["先停在这里", "去洗漱", "别继续熬", "把最后一段收尾"],
                "after": ["我会生气的", "哥哥听话", "明天再继续", "陪你关屏幕"],
            },
            "weather": {
                "react": ["外面天气变了", "出门前看一下", "我刚看过天气", "今天别乱出门"],
                "nudge": ["带好东西", "慢一点", "按天气来", "先看窗外"],
                "after": ["别让我操心", "回来告诉我", "乖", "我会提醒你"],
            },
            "rain": {
                "react": ["外面有雨", "雨天来了", "路上会湿", "空气都潮了"],
                "nudge": ["带伞", "别踩水", "外套拿上", "出门慢点"],
                "after": ["别淋湿", "我等你回来", "哥哥最懂雨天", "听我的"],
            },
            "sunny": {
                "react": ["太阳不错", "外面挺亮", "今天光线很好", "适合出去走一下"],
                "nudge": ["眼睛休息一下", "起来走走", "晒一点光", "别一直盯屏幕"],
                "after": ["回来我还在", "我等你", "听到了吗", "这次很温柔吧"],
            },
        }
        self.triggers = {
            "face": ["脸靠这么近", "你看过来了", "欸，对上眼了", "终于看我了"],
            "hair": ["头发乱了", "别拨我刘海", "发尾被你碰到了", "轻一点呀"],
            "hand": ["手碰到了", "只牵一下", "指尖别乱跑", "嗯，手给你"],
            "body": ["我就在这儿", "衣服被你点到了", "站这么乖还不看我", "你碰到我了"],
            "skirt_legs": ["裙摆会乱", "别点裙子", "下半身不许乱点", "腿边有点痒"],
            "ignored": ["你刚刚不理我", "我等好久了", "屏幕这边很安静", "你把我晾着了"],
            "failed": ["刚才贴太近了", "吓你一下", "我从旁边探出来了", "醒醒"],
            "running": ["工作还没完", "这一段在动", "我看着进度", "别分神"],
            "review": ["这里要看", "细节在这", "先别翻过去", "再确认一下"],
            "rest": ["休息点到了", "我拦你一下", "眼睛在抗议", "停一下"],
            "move": ["久坐提醒", "该起来了", "身体要动", "椅子先放开你"],
            "late_night": ["夜深了", "屏幕还亮着", "你还没睡", "时间不早了"],
            "weather": ["天气提醒", "外面的事", "出门前", "窗外那边"],
            "rain": ["雨声来了", "外面下雨", "路上有水", "伞该出场"],
            "sunny": ["太阳出来了", "外面挺亮", "晴天到了", "光线不错"],
        }

    def name(self, seed: int | None = None) -> str:
        if seed is None:
            return random.choice(self.names)
        return self.names[seed % len(self.names)]

    def persona_name(self, persona: str, seed: int | None = None) -> str:
        names = self.names_by_persona.get(persona, self.names)
        if not names:
            names = ["夜雨哥哥"]
        if seed is None:
            return random.choice(names)
        return names[seed % len(names)]

    def line(
        self,
        persona: str,
        mood: str,
        region: str,
        seed: int | None = None,
        affection: int = 5,
        intensity: int = 3,
    ) -> str:
        return self._compose(
            DialogueContext(
                persona=persona,
                mood=mood,
                trigger=region,
                name=self.persona_name(persona, seed),
                affection=affection,
                intensity=intensity,
            ),
            seed,
        )

    def event_line(
        self,
        event: str,
        seed: int | None = None,
        affection: int = 5,
        intensity: int = 3,
    ) -> str:
        return self._compose(
            DialogueContext(
                persona="mature",
                mood=event,
                trigger=event,
                name=self.persona_name("mature", seed),
                affection=affection,
                intensity=intensity,
            ),
            seed,
        )

    def _compose(self, context: DialogueContext, seed: int | None) -> str:
        rng = random.Random(seed)
        mood = self.moods.get(context.mood, self.moods["happy"])
        voice = self.voice.get(context.persona, self.voice["girl"])
        trigger = rng.choice(self.triggers.get(context.trigger, self.triggers["body"]))
        react = rng.choice(mood["react"])
        nudge = rng.choice(mood["nudge"])
        after = rng.choice(mood["after"])
        suffix = rng.choice(voice["suffix"])
        softer = rng.choice(voice["softeners"])

        mark = "！" if context.intensity >= 7 else "。"
        warm = "乖" if context.affection >= 7 else softer
        patterns = [
            "{name}，{react}。{nudge}{suffix}",
            "{name}。{trigger}，{after}{suffix}",
            "{name}，{nudge}。{after}{suffix}",
            "{name}，{trigger}。{react}{suffix}",
            "{name}，{react}{mark}{after}{suffix}",
            "{name}，{nudge}{suffix}",
            "{name}，{trigger}。{nudge}，{warm}{suffix}",
        ]
        line = rng.choice(patterns).format(
            name=context.name,
            trigger=trigger,
            react=react,
            nudge=nudge,
            after=after,
            mark=mark,
            suffix=suffix,
            warm=warm,
        )
        return self._ensure_required_cue(line, context, suffix)

    def _ensure_required_cue(
        self,
        line: str,
        context: DialogueContext,
        suffix: str,
    ) -> str:
        line = self._normalize_persona_addressing(line, context)
        if (
            context.mood == "shy"
            and context.trigger == "skirt_legs"
            and not any(token in line for token in ["别", "害羞", "裙"])
        ):
            line = line.removesuffix(suffix) + "。裙子会乱啦" + suffix
            return self._normalize_persona_addressing(line, context)
        return line

    def _normalize_persona_addressing(self, line: str, context: DialogueContext) -> str:
        if context.persona != "girl":
            return line
        protected = "\0GIRL_YEYU_NAME\0"
        normalized = line.replace("夜雨哥哥", protected)
        normalized = normalized.replace("夜雨，", "")
        normalized = normalized.replace("夜雨、", "")
        normalized = normalized.replace("夜雨", "哥哥")
        return normalized.replace(protected, "夜雨哥哥")
