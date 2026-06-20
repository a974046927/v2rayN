from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


@dataclass
class PetState:
    persona: str = "girl"
    affection: int = 5
    mood: str = "happy"
    mood_intensity: int = 3
    last_interaction: datetime | None = None
    last_rest_prompt: datetime | None = None
    last_move_prompt: datetime | None = None
    last_night_prompt: datetime | None = None
    last_weather_prompt: datetime | None = None

    @classmethod
    def load(cls, path: str | Path) -> "PetState":
        path = Path(path)
        if not path.exists():
            return cls()
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls(
            persona=data.get("persona", "girl"),
            affection=int(data.get("affection", 5)),
            mood=data.get("mood", "happy"),
            mood_intensity=int(data.get("mood_intensity", 3)),
            last_interaction=_parse_datetime(data.get("last_interaction")),
            last_rest_prompt=_parse_datetime(data.get("last_rest_prompt")),
            last_move_prompt=_parse_datetime(data.get("last_move_prompt")),
            last_night_prompt=_parse_datetime(data.get("last_night_prompt")),
            last_weather_prompt=_parse_datetime(data.get("last_weather_prompt")),
        )

    def to_json(self) -> dict[str, Any]:
        data = asdict(self)
        for key, value in list(data.items()):
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_json(), handle, ensure_ascii=False, indent=2)

    def mark_interaction(self, now: datetime) -> None:
        self.last_interaction = now
        self.affection = min(10, self.affection + 1)

    def set_emotion(self, mood: str, intensity: int) -> None:
        self.mood = mood
        self.mood_intensity = max(1, min(10, intensity))

    def switch_persona(self) -> str:
        self.persona = "mature" if self.persona == "girl" else "girl"
        return self.persona

    def initialize_prompt_baseline(self, now: datetime) -> None:
        if self.last_rest_prompt is None:
            self.last_rest_prompt = now
        if self.last_move_prompt is None:
            self.last_move_prompt = now
        if self.last_night_prompt is None:
            self.last_night_prompt = now
        if self.last_weather_prompt is None:
            self.last_weather_prompt = now
