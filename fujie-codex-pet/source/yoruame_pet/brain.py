from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .dialogue import DialogueBook
from .state import PetState


@dataclass(frozen=True)
class PetAction:
    animation: str
    text: str
    persona: str
    mood: str = "happy"
    intensity: int = 3


class PetBrain:
    def __init__(self, names: Iterable[str]) -> None:
        self.dialogue = DialogueBook(names)

    def click(
        self,
        state: PetState,
        region: str,
        now: datetime,
        seed: int | None = None,
    ) -> PetAction:
        state.mark_interaction(now)
        persona = state.persona

        if region == "face":
            mood = "happy" if persona == "girl" else "calm"
            animation = "waving" if persona == "girl" else "review"
            intensity = 4
        elif region == "skirt_legs":
            mood = "shy"
            animation = "waiting"
            persona = "girl"
            intensity = 6
        elif region == "hand":
            mood = "happy"
            animation = "waving"
            intensity = 4
        elif region == "body":
            mood = "work" if persona == "mature" else "happy"
            animation = "running" if persona == "mature" else "idle"
            intensity = 5 if persona == "mature" else 3
        elif region == "hair":
            mood = "happy"
            animation = "idle"
            intensity = 3
        else:
            mood = "happy"
            animation = "idle"
            intensity = 3

        state.set_emotion(mood, intensity)
        text = self.dialogue.line(
            persona,
            mood,
            region,
            seed=seed,
            affection=state.affection,
            intensity=state.mood_intensity,
        )
        state.persona = persona
        return PetAction(
            animation=animation,
            text=text,
            persona=persona,
            mood=mood,
            intensity=state.mood_intensity,
        )

    def ignored(self, state: PetState, seed: int | None = None) -> PetAction:
        state.persona = "mature"
        intensity = min(10, state.mood_intensity + 2)
        state.set_emotion("annoyed", max(5, intensity))
        text = self.dialogue.line(
            "mature",
            "annoyed",
            "ignored",
            seed=seed,
            affection=state.affection,
            intensity=state.mood_intensity,
        )
        return PetAction(
            animation="waiting",
            text=text,
            persona="mature",
            mood="annoyed",
            intensity=state.mood_intensity,
        )

    def scare(self, state: PetState, seed: int | None = None) -> PetAction:
        state.persona = "mature"
        state.set_emotion("scare", 8)
        text = self.dialogue.line(
            "mature",
            "scare",
            "failed",
            seed=seed,
            affection=state.affection,
            intensity=state.mood_intensity,
        )
        return PetAction(
            animation="failed",
            text=text,
            persona="mature",
            mood="scare",
            intensity=state.mood_intensity,
        )

    def idle_action(self, state: PetState, seed: int | None = None) -> PetAction:
        persona = state.persona
        pool = [
            ("waving", "happy", "face", 4),
            ("running", "work", "running", 4),
            ("jumping", "move", "move", 4),
            ("waving", "happy", "hand", 3),
            ("idle", "calm" if persona == "mature" else "happy", "hair", 3),
        ]
        index = random.randrange(len(pool)) if seed is None else seed % len(pool)
        animation, mood, trigger, intensity = pool[index]
        state.set_emotion(mood, intensity)
        text = self.dialogue.line(
            persona,
            mood,
            trigger,
            seed=seed,
            affection=state.affection,
            intensity=state.mood_intensity,
        )
        return PetAction(
            animation=animation,
            text=text,
            persona=persona,
            mood=mood,
            intensity=state.mood_intensity,
        )

    def switch_form(self, state: PetState, seed: int | None = None) -> PetAction:
        persona = state.switch_persona()
        if persona == "mature":
            mood = "calm"
            animation = "review"
            intensity = 5
        else:
            mood = "happy"
            animation = "waving"
            intensity = 4
        state.set_emotion(mood, intensity)
        text = self.dialogue.line(
            persona,
            mood,
            "face",
            seed=seed,
            affection=state.affection,
            intensity=state.mood_intensity,
        )
        return PetAction(
            animation=animation,
            text=text,
            persona=persona,
            mood=mood,
            intensity=state.mood_intensity,
        )

    def reminder(self, event: str, state: PetState, seed: int | None = None) -> PetAction:
        state.persona = "mature"
        animation = "review" if event in {"rest", "late_night", "weather"} else "jumping"
        intensity = 7 if event == "late_night" else 5
        state.set_emotion(event, intensity)
        text = self.dialogue.event_line(
            event,
            seed=seed,
            affection=state.affection,
            intensity=state.mood_intensity,
        )
        return PetAction(
            animation=animation,
            text=text,
            persona="mature",
            mood=event,
            intensity=state.mood_intensity,
        )
