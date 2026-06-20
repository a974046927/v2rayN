import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class AtlasAndAppTests(unittest.TestCase):
    def test_atlas_reports_expected_states_and_frame_counts(self):
        from yoruame_pet.atlas import SpriteAtlas

        atlas = SpriteAtlas.from_default_pet()

        self.assertEqual(atlas.cell_size, (192, 208))
        self.assertEqual(atlas.frame_count("idle"), 6)
        self.assertEqual(atlas.frame_count("failed"), 8)
        self.assertEqual(atlas.frame_count("review"), 6)
        self.assertIn("running-left", atlas.states)

    def test_atlas_can_extract_a_transparent_frame(self):
        from yoruame_pet.atlas import SpriteAtlas

        atlas = SpriteAtlas.from_default_pet()
        frame = atlas.frame("idle", 0)

        self.assertEqual(frame.size, (192, 208))
        self.assertEqual(frame.mode, "RGBA")
        self.assertGreater(sum(1 for pixel in frame.getdata() if pixel[3]), 1000)

    def test_desktop_frame_source_prefers_high_resolution_decoded_rows(self):
        from yoruame_pet.atlas import DesktopFrameSource
        from yoruame_pet.config import default_config

        config = default_config()
        source = DesktopFrameSource.from_config(config)
        frame = source.frame("idle", 0)

        self.assertEqual(source.frame_count("idle"), 6)
        self.assertGreater(frame.size[0], 192)
        self.assertGreater(frame.size[1], 208)
        self.assertGreater(sum(1 for pixel in frame.getdata() if pixel[3]), 5000)

    def test_app_module_imports_without_starting_window(self):
        import yoruame_pet.app as app

        self.assertTrue(hasattr(app, "YoruamePetApp"))

    def test_app_can_prepare_headless_runtime_state(self):
        from yoruame_pet.app import YoruamePetApp

        app = YoruamePetApp(headless=True)

        self.assertEqual(app.current_animation, "idle")
        self.assertIn("idle", app.frames.states)
        self.assertEqual(app.dialogue_names[0], "夜雨")
        self.assertGreater(app.sprite_size[0], 192)

    def test_idle_animation_uses_slower_state_specific_delay(self):
        from yoruame_pet.app import YoruamePetApp

        app = YoruamePetApp(headless=True)
        idle_delay = app.animation_delay_ms()
        app.current_animation = "waving"

        self.assertGreaterEqual(idle_delay, 450)
        self.assertLess(app.animation_delay_ms(), idle_delay)

    def test_window_frame_uses_key_background_without_purple_visible_halo(self):
        from yoruame_pet.app import prepare_window_frame
        from yoruame_pet.atlas import SpriteAtlas

        atlas = SpriteAtlas.from_default_pet()
        prepared = prepare_window_frame(atlas.frame("idle", 0), (288, 312), "#ff00ff")
        pixels = prepared.getdata()
        purple_like_visible = [
            pixel
            for pixel in pixels
            if pixel != (255, 0, 255) and pixel[0] > 180 and pixel[1] < 80 and pixel[2] > 180
        ]

        self.assertEqual(prepared.mode, "RGB")
        self.assertEqual(prepared.getpixel((0, 0)), (255, 0, 255))
        self.assertLess(len(purple_like_visible), 5)

    def test_comic_bubble_style_uses_cute_fonts_and_tail(self):
        from yoruame_pet.app import comic_bubble_style
        from yoruame_pet.config import default_config

        style = comic_bubble_style(default_config(), "happy")
        shy_style = comic_bubble_style(default_config(), "shy")
        scare_style = comic_bubble_style(default_config(), "scare")
        intense_scare_style = comic_bubble_style(default_config(), "scare", intensity=8)

        self.assertEqual(style["fill"], "#fffafc")
        self.assertEqual(style["outline"], "#111111")
        self.assertGreaterEqual(style["outline_width"], 2)
        self.assertTrue(style["tail"])
        self.assertIn("YouYuan", style["font_candidates"])
        self.assertIn("幼圆", style["font_candidates"])
        self.assertIn("♡", style["decorations"])
        self.assertNotEqual(style["fill"], shy_style["fill"])
        self.assertNotEqual(shy_style["accent"], scare_style["accent"])
        self.assertEqual(scare_style["accent"], "#111111")
        self.assertGreater(intense_scare_style["outline_width"], scare_style["outline_width"])
        self.assertIn("shadow", style)

    def test_pet_say_tracks_dialogue_mood_for_bubble_theme(self):
        from yoruame_pet.app import YoruamePetApp

        app = YoruamePetApp(headless=True)
        app.say("哥哥，别点裙子啦♡", mood="shy", intensity=6)

        self.assertEqual(app.bubble_text, "哥哥，别点裙子啦♡")
        self.assertEqual(app.bubble_mood, "shy")
        self.assertEqual(app.bubble_intensity, 6)

    def test_headless_app_can_answer_typed_question(self):
        from yoruame_pet.app import YoruamePetApp

        app = YoruamePetApp(headless=True)
        answer = app.answer_question("少女模式怎么称呼我")

        self.assertIn(answer.source, {"local", "local_pet"})
        self.assertTrue(app.bubble_text)
        self.assertEqual(app.bubble_mood, "review")

    def test_headless_app_voice_entry_degrades_without_recognizer(self):
        from yoruame_pet.app import YoruamePetApp
        from yoruame_pet.voice import VoiceRecognizer

        app = YoruamePetApp(headless=True)
        app.voice_recognizer = VoiceRecognizer(enabled=False)
        result = app.listen_for_question()

        self.assertFalse(result.available)
        self.assertIn("听不清", app.bubble_text)


if __name__ == "__main__":
    unittest.main()
