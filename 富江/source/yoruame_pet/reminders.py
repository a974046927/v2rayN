from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from .state import PetState


def _due(last: datetime | None, now: datetime, minutes: int) -> bool:
    if last is None:
        return True
    return now - last >= timedelta(minutes=minutes)


def due_reminders(config: dict[str, Any], state: PetState, now: datetime) -> list[str]:
    events: list[str] = []
    cooldown = int(config.get("cooldown_minutes", 30))
    if _due(state.last_rest_prompt, now, int(config.get("rest_minutes", 50))):
        events.append("rest")
    if _due(state.last_move_prompt, now, int(config.get("move_minutes", 90))):
        events.append("move")
    if now.hour >= int(config.get("late_night_hour", 23)) and _due(
        state.last_night_prompt, now, cooldown
    ):
        events.append("late_night")
    return events


def mark_reminder(state: PetState, event: str, now: datetime) -> None:
    if event == "rest":
        state.last_rest_prompt = now
    elif event == "move":
        state.last_move_prompt = now
    elif event == "late_night":
        state.last_night_prompt = now
    elif event == "weather":
        state.last_weather_prompt = now

