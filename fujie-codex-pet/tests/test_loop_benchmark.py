import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class LoopBenchmarkTests(unittest.TestCase):
    def test_loop_benchmark_covers_updated_goal_requirements(self):
        from yoruame_pet.loop_benchmark import evaluate_loop_baseline

        report = evaluate_loop_baseline()
        required = {
            "click_regions",
            "affection_attention_state",
            "random_scare",
            "form_switch",
            "dialogue_system",
            "girl_addressing_rule",
            "rest_reminder",
            "move_reminder",
            "late_night_reminder",
            "weather_location_source",
            "interactive_question_mode",
            "local_search",
            "local_pet_reply",
            "voice_interaction_flow",
            "voice_fallback",
            "codex_task_status_bridge",
            "github_sync_folder",
        }
        by_id = {check.id: check for check in report.checks}

        self.assertTrue(required <= set(by_id))
        self.assertTrue(all(by_id[check_id].passed for check_id in required))
        self.assertIn("Loop engineering", report.summary)

    def test_loop_benchmark_markdown_is_human_readable(self):
        from yoruame_pet.loop_benchmark import evaluate_loop_baseline

        markdown = evaluate_loop_baseline().to_markdown()

        self.assertIn("# Loop engineering baseline", markdown)
        self.assertIn("click_regions", markdown)
        self.assertIn("weather_location_source", markdown)
        self.assertIn("github_sync_folder", markdown)


if __name__ == "__main__":
    unittest.main()
