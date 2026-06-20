import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class CoreBehaviorTests(unittest.TestCase):
    def test_default_config_contains_required_local_pet_settings(self):
        from yoruame_pet.config import default_config

        config = default_config()

        self.assertEqual(config["pet"]["display_name"], "夜雨影姬")
        self.assertTrue(config["pet"]["atlas_path"].endswith("spritesheet.webp"))
        self.assertIn("夜雨", config["dialogue"]["names"])
        self.assertGreaterEqual(config["window"]["animation_ms"], 220)
        self.assertGreaterEqual(config["window"]["animation_ms_by_state"]["idle"], 450)
        self.assertGreaterEqual(config["dialogue"]["idle_loop_ms"], 20000)
        self.assertLessEqual(config["dialogue"]["scare_chance"], 0.05)
        self.assertGreaterEqual(config["reminders"]["rest_minutes"], 1)
        self.assertIn("weather_city", config["weather"])

    def test_load_config_merges_user_overrides_without_losing_defaults(self):
        from yoruame_pet.config import load_config

        with tempfile.TemporaryDirectory() as temp:
            config_path = Path(temp) / "settings.json"
            config_path.write_text(
                json.dumps(
                    {
                        "window": {"scale": 1.4},
                        "weather": {"weather_city": "Kyoto"},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            config = load_config(config_path)

        self.assertEqual(config["window"]["scale"], 1.4)
        self.assertEqual(config["weather"]["weather_city"], "Kyoto")
        self.assertEqual(config["pet"]["display_name"], "夜雨影姬")

    def test_click_regions_match_body_areas(self):
        from yoruame_pet.hit_regions import classify_region

        self.assertEqual(classify_region(192, 208, 96, 35), "face")
        self.assertEqual(classify_region(192, 208, 38, 78), "hair")
        self.assertEqual(classify_region(192, 208, 96, 103), "body")
        self.assertEqual(classify_region(192, 208, 72, 124), "hand")
        self.assertEqual(classify_region(192, 208, 96, 158), "skirt_legs")

    def test_dialogue_varies_by_persona_mood_and_region(self):
        from yoruame_pet.dialogue import DialogueBook

        book = DialogueBook(["夜雨", "哥哥", "凌凌哥哥"])

        girl_line = book.line("girl", "happy", "face", seed=1)
        mature_line = book.line("mature", "annoyed", "ignored", seed=2)
        shy_line = book.line("girl", "shy", "skirt_legs", seed=3)

        self.assertIn("夜雨", girl_line + mature_line + shy_line)
        self.assertNotEqual(girl_line, mature_line)
        self.assertTrue(any(word in shy_line for word in ["别", "害羞", "裙"]))

    def test_girl_persona_only_uses_approved_names(self):
        from yoruame_pet.dialogue import DialogueBook

        book = DialogueBook(["夜雨", "哥哥", "凌凌哥哥"])
        samples = [
            book.line("girl", "happy", "face", seed=seed)
            for seed in range(18)
        ]
        approved_names = ("夜雨哥哥", "哥哥", "凌凌哥哥")

        self.assertTrue(all(line.startswith(approved_names) for line in samples))
        self.assertTrue(all(not line.startswith("夜雨，") for line in samples))

    def test_girl_persona_never_uses_bare_yeyu_address(self):
        from yoruame_pet.dialogue import DialogueBook

        book = DialogueBook(["夜雨", "哥哥", "凌凌哥哥"])
        approved_names = ("夜雨哥哥", "哥哥", "凌凌哥哥")

        for mood in book.moods:
            for trigger in book.triggers:
                for seed in range(12):
                    line = book.line("girl", mood, trigger, seed=seed)
                    stripped = line
                    for name in approved_names:
                        stripped = stripped.replace(name, "")

                    self.assertTrue(line.startswith(approved_names), line)
                    self.assertNotIn("夜雨", stripped, line)

    def test_dialogue_is_generated_from_emotion_context_not_fixed_lines(self):
        from yoruame_pet.dialogue import DialogueBook

        book = DialogueBook(["夜雨", "哥哥", "凌凌哥哥"])
        samples = {
            book.line("girl", "happy", "face", seed=seed)
            for seed in range(18)
        }
        old_fixed_lines = {
            "夜雨，终于看我啦♡ 眼睛亮一下！",
            "嗯？夜雨，再靠近一点也可以哦♪",
        }

        self.assertGreaterEqual(len(samples), 8)
        self.assertTrue(all(any(name in line for name in ["夜雨哥哥", "哥哥", "凌凌哥哥"]) for line in samples))
        self.assertFalse(samples <= old_fixed_lines)

    def test_generated_dialogue_uses_distinct_emotional_language(self):
        from yoruame_pet.dialogue import DialogueBook

        book = DialogueBook(["夜雨", "哥哥", "凌凌哥哥"])
        shy = "".join(book.line("girl", "shy", "skirt_legs", seed=seed) for seed in range(6))
        annoyed = "".join(book.line("mature", "annoyed", "ignored", seed=seed) for seed in range(6))
        scare = "".join(book.line("mature", "scare", "failed", seed=seed) for seed in range(6))

        self.assertTrue(any(token in shy for token in ["害羞", "裙", "脸红", "躲"]))
        self.assertTrue(any(token in annoyed for token in ["不理", "生气", "吃醋", "哼"]))
        self.assertTrue(any(token in scare for token in ["吓", "心跳", "醒着", "别怕"]))

    def test_generated_dialogue_avoids_ai_flavored_words(self):
        from yoruame_pet.dialogue import DialogueBook

        book = DialogueBook(["夜雨", "哥哥", "凌凌哥哥"])
        samples = [
            book.line("girl", "happy", "face", seed=seed)
            for seed in range(16)
        ] + [
            book.line("mature", "work", "body", seed=seed)
            for seed in range(16)
        ]
        blocked = ["系统", "触发", "当前", "生成", "模板", "用户", "执行", "情绪强度", "进度条"]

        self.assertFalse(any(word in line for line in samples for word in blocked))

    def test_generated_dialogue_feels_like_short_human_turns(self):
        from yoruame_pet.dialogue import DialogueBook

        book = DialogueBook(["夜雨", "哥哥", "凌凌哥哥"])
        samples = [
            book.line("girl", "shy", "skirt_legs", seed=seed)
            for seed in range(12)
        ] + [
            book.line("mature", "annoyed", "ignored", seed=seed)
            for seed in range(12)
        ]
        conversational = ["啦", "嘛", "呢", "呀", "哦", "欸", "哼", "别", "先", "好了", "等下"]

        self.assertTrue(any(word in line for line in samples for word in conversational))
        self.assertTrue(all(len(line) <= 34 for line in samples))
        self.assertTrue(all(line.count("，") <= 2 for line in samples))

    def test_dialogue_has_cute_manga_symbols_without_being_plain_text(self):
        from yoruame_pet.dialogue import DialogueBook

        book = DialogueBook(["夜雨", "哥哥", "凌凌哥哥"])
        samples = [
            book.line("girl", "happy", "face", seed=1),
            book.line("girl", "shy", "skirt_legs", seed=3),
            book.event_line("rest", seed=4),
        ]
        joined = "".join(samples)

        self.assertTrue(any(symbol in joined for symbol in ["♡", "♪", "✨", "哼哼", "ฅ"]))

    def test_state_round_trips_and_updates_attention(self):
        from yoruame_pet.state import PetState

        with tempfile.TemporaryDirectory() as temp:
            state_path = Path(temp) / "state.json"
            state = PetState.load(state_path)
            state.persona = "mature"
            state.affection = 7
            state.mark_interaction(datetime(2026, 6, 20, 12, 0, 0))
            state.save(state_path)

            loaded = PetState.load(state_path)

        self.assertEqual(loaded.persona, "mature")
        self.assertEqual(loaded.affection, 8)
        self.assertEqual(loaded.last_interaction.isoformat(), "2026-06-20T12:00:00")

    def test_state_can_initialize_reminder_baseline_once(self):
        from yoruame_pet.state import PetState

        state = PetState()
        now = datetime(2026, 6, 20, 12, 0, 0)

        state.initialize_prompt_baseline(now)
        state.initialize_prompt_baseline(datetime(2026, 6, 20, 13, 0, 0))

        self.assertEqual(state.last_rest_prompt, now)
        self.assertEqual(state.last_move_prompt, now)
        self.assertEqual(state.last_weather_prompt, now)

    def test_reminders_trigger_rest_movement_and_late_night(self):
        from yoruame_pet.reminders import due_reminders
        from yoruame_pet.state import PetState

        now = datetime(2026, 6, 20, 23, 45, 0)
        state = PetState()
        state.last_rest_prompt = now - timedelta(minutes=80)
        state.last_move_prompt = now - timedelta(minutes=140)
        state.last_night_prompt = now - timedelta(hours=26)
        config = {
            "rest_minutes": 50,
            "move_minutes": 90,
            "late_night_hour": 23,
            "cooldown_minutes": 30,
        }

        self.assertEqual(due_reminders(config, state, now), ["rest", "move", "late_night"])

    def test_weather_summary_classifies_rain_and_sun(self):
        from yoruame_pet.weather import summarize_weather

        rain = summarize_weather(
            {
                "weather_code": 61,
                "precipitation": 2.5,
                "temperature": 20,
                "location": "Tokyo",
                "source": "ip",
            }
        )
        sun = summarize_weather({"weather_code": 0, "precipitation": 0, "temperature": 27})

        self.assertEqual(rain.kind, "rain")
        self.assertEqual(rain.location, "Tokyo")
        self.assertEqual(rain.source, "ip")
        self.assertIn("雨", rain.pet_line)
        stripped_rain_line = rain.pet_line
        for name in ("夜雨哥哥", "哥哥", "凌凌哥哥"):
            stripped_rain_line = stripped_rain_line.replace(name, "")
        self.assertNotIn("夜雨", stripped_rain_line)
        self.assertEqual(sun.kind, "sunny")
        self.assertTrue(any(word in sun.pet_line for word in ["太阳", "晴"]))

    def test_weather_fetch_prefers_configured_city_and_records_source(self):
        from yoruame_pet import weather

        responses = [
            {"results": [{"latitude": 35.0, "longitude": 139.0, "name": "Tokyo"}]},
            {
                "current": {
                    "temperature_2m": 24,
                    "precipitation": 0,
                    "weather_code": 0,
                }
            },
        ]

        def fake_read_json(_url, _timeout):
            return responses.pop(0)

        with patch("yoruame_pet.weather._read_json", side_effect=fake_read_json):
            summary = weather.fetch_weather_summary(
                {
                    "weather_city": "Tokyo",
                    "request_timeout_seconds": 1,
                }
            )

        self.assertIsNotNone(summary)
        assert summary is not None
        self.assertEqual(summary.location, "Tokyo")
        self.assertEqual(summary.source, "configured_city")

    def test_weather_fetch_failure_returns_none_instead_of_crashing(self):
        from yoruame_pet.weather import fetch_weather_summary

        config = {
            "weather_city": "",
            "request_timeout_seconds": 1,
        }

        with patch("yoruame_pet.weather.locate_by_ip", side_effect=OSError("offline")):
            self.assertIsNone(fetch_weather_summary(config))

    def test_brain_maps_clicks_to_dialogue_and_animation(self):
        from yoruame_pet.brain import PetBrain
        from yoruame_pet.state import PetState

        brain = PetBrain(["夜雨", "哥哥", "凌凌哥哥"])
        state = PetState(persona="girl")

        face = brain.click(state, "face", datetime(2026, 6, 20, 12, 0, 0), seed=1)
        shy = brain.click(state, "skirt_legs", datetime(2026, 6, 20, 12, 1, 0), seed=3)

        self.assertEqual(face.animation, "waving")
        self.assertIn(face.persona, {"girl", "mature"})
        self.assertIn("夜雨", face.text + shy.text)
        self.assertEqual(shy.animation, "waiting")
        self.assertEqual(shy.mood, "shy")
        self.assertEqual(state.mood, "shy")
        self.assertGreaterEqual(state.mood_intensity, 4)
        self.assertTrue(any(word in shy.text for word in ["别", "害羞", "裙"]))

    def test_brain_idle_action_pool_includes_running_and_jumping(self):
        from yoruame_pet.brain import PetBrain
        from yoruame_pet.state import PetState

        brain = PetBrain(["夜雨", "哥哥", "凌凌哥哥"])
        state = PetState(persona="girl")

        self.assertTrue(
            hasattr(brain, "idle_action"),
            "PetBrain should expose ambient idle actions for the standby loop",
        )
        animations = {brain.idle_action(state, seed=seed).animation for seed in range(24)}

        self.assertIn("running", animations)
        self.assertIn("jumping", animations)
        self.assertIn("waving", animations)

    def test_brain_ignored_and_reminder_events_are_distinct(self):
        from yoruame_pet.brain import PetBrain
        from yoruame_pet.state import PetState

        brain = PetBrain(["夜雨", "哥哥", "凌凌哥哥"])
        state = PetState(persona="girl")

        ignored = brain.ignored(state, seed=2)
        rest = brain.reminder("rest", state, seed=4)
        scare = brain.scare(state, seed=5)

        self.assertEqual(ignored.animation, "waiting")
        self.assertEqual(ignored.persona, "mature")
        self.assertEqual(ignored.mood, "annoyed")
        self.assertGreaterEqual(ignored.intensity, 5)
        self.assertEqual(state.mood, "scare")
        self.assertEqual(rest.animation, "review")
        self.assertEqual(rest.mood, "rest")
        self.assertEqual(scare.animation, "failed")
        self.assertEqual(scare.mood, "scare")
        self.assertNotEqual(ignored.text, rest.text)

    def test_brain_can_switch_between_girl_and_mature_forms(self):
        from yoruame_pet.brain import PetBrain
        from yoruame_pet.state import PetState

        brain = PetBrain(["夜雨", "哥哥", "凌凌哥哥"])
        state = PetState(persona="girl")

        mature = brain.switch_form(state, seed=1)
        girl = brain.switch_form(state, seed=2)

        self.assertEqual(mature.persona, "mature")
        self.assertEqual(mature.animation, "review")
        self.assertEqual(state.persona, "girl")
        self.assertEqual(girl.persona, "girl")
        self.assertEqual(girl.animation, "waving")


if __name__ == "__main__":
    unittest.main()
