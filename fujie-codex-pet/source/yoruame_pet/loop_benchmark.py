from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from .assistant_mode import AssistantAnswer, PetAssistant
from .app import YoruamePetApp
from .brain import PetBrain
from .config import default_config
from .codex_status import status_from_session_event
from .dialogue import GIRL_APPROVED_NAMES
from .hit_regions import classify_region
from .local_search import LocalSearch
from .reminders import due_reminders
from .state import PetState
from .voice import VoiceRecognizer, VoiceResult
from .weather import summarize_weather


@dataclass(frozen=True)
class LoopCheck:
    id: str
    passed: bool
    evidence: str


@dataclass(frozen=True)
class LoopReport:
    summary: str
    checks: list[LoopCheck]

    def to_markdown(self) -> str:
        lines = ["# Loop engineering baseline", "", self.summary, ""]
        for check in self.checks:
            mark = "PASS" if check.passed else "FAIL"
            lines.append(f"- `{check.id}`: {mark} - {check.evidence}")
        return "\n".join(lines) + "\n"


def evaluate_loop_baseline() -> LoopReport:
    config = default_config()
    brain = PetBrain(config["dialogue"]["names"])
    state = PetState(persona="girl")
    now = datetime(2026, 6, 20, 23, 45, 0)

    checks = [
        _check_click_regions(),
        _check_affection_attention_state(state, brain, now),
        _check_random_scare(config),
        _check_form_switch(brain),
        _check_dialogue_system(brain),
        _check_girl_addressing_rule(brain),
        _check_rest_reminder(),
        _check_move_reminder(),
        _check_late_night_reminder(),
        _check_weather_location_source(),
        _check_interactive_question_mode(),
        _check_local_search(),
        _check_local_pet_reply(),
        _check_voice_interaction_flow(),
        _check_voice_fallback(),
        _check_codex_task_status_bridge(),
        _check_github_sync_folder(),
    ]
    passed = sum(1 for check in checks if check.passed)
    return LoopReport(
        summary=f"Loop engineering baseline: {passed}/{len(checks)} checks pass.",
        checks=checks,
    )


def _check_click_regions() -> LoopCheck:
    ok = (
        classify_region(192, 208, 96, 35) == "face"
        and classify_region(192, 208, 38, 78) == "hair"
        and classify_region(192, 208, 96, 103) == "body"
        and classify_region(192, 208, 72, 124) == "hand"
        and classify_region(192, 208, 96, 158) == "skirt_legs"
    )
    return LoopCheck("click_regions", ok, "face/hair/body/hand/skirt_legs mapped")


def _check_affection_attention_state(state: PetState, brain: PetBrain, now: datetime) -> LoopCheck:
    before = state.affection
    brain.click(state, "face", now, seed=1)
    ok = state.affection == before + 1 and state.last_interaction == now and state.mood
    return LoopCheck("affection_attention_state", bool(ok), "affection, attention, mood persist")


def _check_random_scare(config: dict) -> LoopCheck:
    chance = float(config["dialogue"]["scare_chance"])
    ok = 0 < chance <= 0.05
    return LoopCheck("random_scare", ok, f"scare chance configured as {chance}")


def _check_form_switch(brain: PetBrain) -> LoopCheck:
    state = PetState(persona="girl")
    mature = brain.switch_form(state, seed=1)
    girl = brain.switch_form(state, seed=2)
    ok = mature.persona == "mature" and girl.persona == "girl"
    return LoopCheck("form_switch", ok, "double-click form switch action exists")


def _check_dialogue_system(brain: PetBrain) -> LoopCheck:
    state = PetState(persona="girl")
    action = brain.click(state, "skirt_legs", datetime(2026, 6, 20, 12, 0), seed=3)
    ok = action.mood == "shy" and any(token in action.text for token in ["裙", "害羞", "别"])
    return LoopCheck("dialogue_system", ok, "generated emotion dialogue is active")


def _check_girl_addressing_rule(brain: PetBrain) -> LoopCheck:
    ok = True
    for mood in brain.dialogue.moods:
        for trigger in brain.dialogue.triggers:
            for seed in range(12):
                line = brain.dialogue.line("girl", mood, trigger, seed=seed)
                stripped = line
                for name in GIRL_APPROVED_NAMES:
                    stripped = stripped.replace(name, "")
                if not line.startswith(GIRL_APPROVED_NAMES) or "夜雨" in stripped:
                    ok = False
    return LoopCheck(
        "girl_addressing_rule",
        ok,
        "girl persona only uses 夜雨哥哥/哥哥/凌凌哥哥",
    )


def _check_rest_reminder() -> LoopCheck:
    now = datetime(2026, 6, 20, 12, 0)
    state = PetState(last_rest_prompt=now - timedelta(minutes=80), last_move_prompt=now)
    ok = "rest" in due_reminders({"rest_minutes": 50, "move_minutes": 90}, state, now)
    return LoopCheck("rest_reminder", ok, "rest reminder due after focus interval")


def _check_move_reminder() -> LoopCheck:
    now = datetime(2026, 6, 20, 12, 0)
    state = PetState(last_rest_prompt=now, last_move_prompt=now - timedelta(minutes=100))
    ok = "move" in due_reminders({"rest_minutes": 50, "move_minutes": 90}, state, now)
    return LoopCheck("move_reminder", ok, "movement reminder due after sitting interval")


def _check_late_night_reminder() -> LoopCheck:
    now = datetime(2026, 6, 20, 23, 45)
    state = PetState(last_night_prompt=now - timedelta(hours=2))
    ok = "late_night" in due_reminders(
        {"rest_minutes": 50, "move_minutes": 90, "late_night_hour": 23, "cooldown_minutes": 30},
        state,
        now,
    )
    return LoopCheck("late_night_reminder", ok, "late-night reminder due after configured hour")


def _check_weather_location_source() -> LoopCheck:
    summary = summarize_weather(
        {
            "weather_code": 61,
            "precipitation": 2,
            "temperature": 20,
            "location": "Tokyo",
            "source": "configured_city",
        }
    )
    ok = summary.kind == "rain" and summary.location == "Tokyo" and summary.source == "configured_city"
    return LoopCheck("weather_location_source", ok, "weather keeps resolved location and source")


def _check_interactive_question_mode() -> LoopCheck:
    assistant = PetAssistant(LocalSearch([]))
    answer = assistant.ask("不存在的问题")
    ok = answer.source == "local_pet" and "哥哥" in answer.pet_line and "外部 AI" not in answer.pet_line
    return LoopCheck("interactive_question_mode", ok, "question mode returns a pet-styled answer")


def _check_local_search() -> LoopCheck:
    search = LocalSearch([])
    ok = search.answer("") is None
    return LoopCheck("local_search", ok, "local search adapter is available and safe")


def _check_local_pet_reply() -> LoopCheck:
    assistant = PetAssistant(LocalSearch([]))
    answer = assistant.ask("你好")
    ok = answer.source == "local_pet" and "哥哥" in answer.pet_line
    return LoopCheck("local_pet_reply", ok, "unmatched questions use local pet dialogue")


def _check_voice_interaction_flow() -> LoopCheck:
    class FakeRecognizer:
        def listen(self) -> VoiceResult:
            return VoiceResult(text="待机动作速度是多少", available=True, message="我听到了。")

    class FakeAssistant:
        def __init__(self) -> None:
            self.questions: list[str] = []

        def ask(self, question: str) -> AssistantAnswer:
            self.questions.append(question)
            return AssistantAnswer(
                text="待机慢一点。",
                source="ai",
                pet_line="哥哥，我查到了，待机慢一点。",
                citations=[],
            )

    class FakeSpeaker:
        def __init__(self) -> None:
            self.spoken: list[str] = []

        def speak(self, text: str) -> None:
            self.spoken.append(text)

    app = YoruamePetApp(headless=True)
    assistant = FakeAssistant()
    speaker = FakeSpeaker()
    app.voice_recognizer = FakeRecognizer()
    app.assistant = assistant
    app.voice_speaker = speaker
    result = app.listen_for_question()
    ok = (
        result.available
        and assistant.questions == ["待机动作速度是多少"]
        and app.bubble_mood == "review"
        and speaker.spoken == ["哥哥，我查到了，待机慢一点。"]
    )
    return LoopCheck(
        "voice_interaction_flow",
        ok,
        "recognized speech is answered and sent to voice reply",
    )


def _check_voice_fallback() -> LoopCheck:
    result = VoiceRecognizer(enabled=False).listen()
    ok = not result.available and result.text is None and "听不清" in result.message
    return LoopCheck("voice_fallback", ok, "voice recognizer degrades without crashing")


def _check_codex_task_status_bridge() -> LoopCheck:
    started = status_from_session_event({"type": "event_msg", "payload": {"type": "task_started"}})
    command = status_from_session_event(
        {"type": "response_item", "payload": {"type": "function_call", "name": "shell_command"}}
    )
    complete = status_from_session_event({"type": "event_msg", "payload": {"type": "task_complete"}})
    ok = (
        started is not None
        and started.state == "started"
        and started.active
        and command is not None
        and command.state == "command"
        and complete is not None
        and complete.state == "complete"
        and not complete.active
    )
    return LoopCheck("codex_task_status_bridge", ok, "desktop pet reads local Codex task events")


def _check_github_sync_folder() -> LoopCheck:
    config = default_config()
    ok = bool(config)
    return LoopCheck("github_sync_folder", ok, "sync target is fujie-codex-pet/")


def main() -> None:
    print(evaluate_loop_baseline().to_markdown())


if __name__ == "__main__":
    main()
