from __future__ import annotations

import logging
import random
import threading
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from PIL import Image, ImageTk

from .atlas import DesktopFrameSource
from .assistant_mode import AssistantAnswer, PetAssistant
from .brain import PetAction, PetBrain
from .config import load_config
from .codex_status import CodexTaskStatusWatcher
from .hit_regions import classify_region
from .local_search import LocalSearch
from .reminders import due_reminders, mark_reminder
from .state import PetState
from .voice import VoiceRecognizer, VoiceResult, VoiceSpeaker
from .weather import fetch_weather_summary


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def prepare_window_frame(
    frame: Image.Image,
    size: tuple[int, int],
    transparent_color: str,
    alpha_threshold: int = 24,
) -> Image.Image:
    resized = frame.convert("RGBA").resize(size, Image.Resampling.NEAREST)
    key = _hex_to_rgb(transparent_color)
    output = Image.new("RGB", size, key)
    source_pixels = resized.load()
    output_pixels = output.load()
    width, height = size
    for y in range(height):
        for x in range(width):
            red, green, blue, alpha = source_pixels[x, y]
            if alpha > alpha_threshold:
                output_pixels[x, y] = (red, green, blue)
    return output


def comic_bubble_style(
    config: dict[str, Any],
    mood: str = "happy",
    intensity: int = 3,
) -> dict[str, Any]:
    defaults = {
        "fill": "#fffafc",
        "outline": "#111111",
        "outline_width": 2,
        "shadow": "#ffd2e4",
        "accent": "#ff6fae",
        "text": "#28151f",
        "decorations": ["♡", "♪"],
        "font_candidates": [
            "YouYuan",
            "幼圆",
            "Comic Sans MS",
            "FZYaoti",
            "Microsoft YaHei UI",
            "Microsoft JhengHei UI",
        ],
        "font_size": 11,
        "tail": True,
        "themes": {
            "happy": {
                "fill": "#fffafc",
                "shadow": "#ffd2e4",
                "accent": "#ff6fae",
                "text": "#28151f",
                "decorations": ["♡", "♪"],
            },
            "shy": {
                "fill": "#fff1f5",
                "shadow": "#ffd6df",
                "accent": "#ff7f9f",
                "text": "#43202b",
                "decorations": ["ฅ", "♡"],
            },
            "annoyed": {
                "fill": "#fff0ee",
                "shadow": "#ffc6c4",
                "accent": "#ff5365",
                "text": "#331111",
                "decorations": ["!!", "💢"],
            },
            "calm": {
                "fill": "#f7fbff",
                "shadow": "#d4e7ff",
                "accent": "#6f9cff",
                "text": "#172033",
                "decorations": ["…", "✧"],
            },
            "scare": {
                "fill": "#f3f2f4",
                "shadow": "#c9c9cf",
                "accent": "#111111",
                "text": "#050505",
                "decorations": ["?!", "●"],
            },
            "work": {
                "fill": "#f8fff8",
                "shadow": "#d4f1dd",
                "accent": "#40a970",
                "text": "#15251b",
                "decorations": ["✦", "✓"],
            },
            "review": {
                "fill": "#f8fff8",
                "shadow": "#d4f1dd",
                "accent": "#40a970",
                "text": "#15251b",
                "decorations": ["✦", "✓"],
            },
            "rest": {
                "fill": "#f7fbff",
                "shadow": "#d4e7ff",
                "accent": "#6f9cff",
                "text": "#172033",
                "decorations": ["☾", "✨"],
            },
            "move": {
                "fill": "#fffaf0",
                "shadow": "#ffe2bd",
                "accent": "#f18a2a",
                "text": "#33200d",
                "decorations": ["♪", "→"],
            },
            "late_night": {
                "fill": "#f3f2f4",
                "shadow": "#c9c9cf",
                "accent": "#111111",
                "text": "#050505",
                "decorations": ["☾", "!!"],
            },
            "weather": {
                "fill": "#f7fbff",
                "shadow": "#d4e7ff",
                "accent": "#5f93ed",
                "text": "#172033",
                "decorations": ["☂", "☀"],
            },
            "rain": {
                "fill": "#eef7ff",
                "shadow": "#c8def5",
                "accent": "#4f8fd8",
                "text": "#122234",
                "decorations": ["☂", "…"],
            },
            "sunny": {
                "fill": "#fff9eb",
                "shadow": "#ffe2b0",
                "accent": "#f59b26",
                "text": "#31200b",
                "decorations": ["☀", "♪"],
            },
        },
    }
    configured = config.get("window", {}).get("bubble", {})
    configured_base = {key: value for key, value in configured.items() if key != "themes"}
    themes = {**defaults["themes"], **configured.get("themes", {})}
    style = {**defaults, **configured_base}
    theme = themes.get(mood, themes["happy"])
    style.update(theme)
    if intensity >= 7:
        style["outline_width"] = int(style["outline_width"]) + 1
    style["themes"] = themes
    return style


class YoruamePetApp:
    def __init__(
        self,
        config_path: str | Path | None = None,
        headless: bool = False,
    ) -> None:
        self.config = load_config(config_path)
        self.dialogue_names = list(self.config["dialogue"]["names"])
        self.frames = DesktopFrameSource.from_config(self.config)
        self.state_path = Path(self.config["paths"]["state_path"])
        self.log_path = Path(self.config["paths"]["log_path"])
        self.state = PetState.load(self.state_path)
        self.state.initialize_prompt_baseline(datetime.now())
        self.brain = PetBrain(self.dialogue_names)
        self.assistant = PetAssistant(
            LocalSearch(
                [
                    Path(self.config["paths"]["search_root"]),
                    Path(self.config["paths"]["transfer_root"]),
                ]
            )
        )
        self.voice_recognizer = VoiceRecognizer(
            enabled=bool(self.config["voice"]["enabled"]),
            timeout_seconds=int(self.config["voice"]["timeout_seconds"]),
        )
        self.voice_speaker = VoiceSpeaker(
            enabled=bool(self.config["voice"].get("reply_enabled", True)),
            rate=int(self.config["voice"].get("tts_rate", 0)),
            volume=int(self.config["voice"].get("tts_volume", 90)),
        )
        status_config = self.config.get("codex_status", {})
        self.codex_status_watcher = (
            CodexTaskStatusWatcher(Path(status_config["sessions_root"]))
            if bool(status_config.get("enabled", False))
            else None
        )
        self.voice_listening = False
        self.current_animation = "idle"
        self.frame_index = 0
        self.bubble_text = ""
        self.bubble_mood = "happy"
        self.bubble_intensity = 3
        self.bubble_until: datetime | None = None
        self.last_motion_at = datetime.now()
        self.started = False
        self.headless = headless
        self.root: tk.Tk | None = None
        self.canvas: tk.Canvas | None = None
        self.question_window: tk.Toplevel | None = None
        self.photo: ImageTk.PhotoImage | None = None
        self.drag_start: tuple[int, int, int, int] | None = None
        self.drag_moved = False
        self.weather_fetching = False
        self.rng = random.Random()

    @property
    def scale(self) -> float:
        return float(self.config["window"]["scale"])

    @property
    def sprite_size(self) -> tuple[int, int]:
        width, height = self.frames.frame_size
        return max(1, int(width * self.scale)), max(1, int(height * self.scale))

    @property
    def bubble_height(self) -> int:
        return 76

    def animation_delay_ms(self) -> int:
        overrides = self.config["window"].get("animation_ms_by_state", {})
        return int(overrides.get(self.current_animation, self.config["window"]["animation_ms"]))

    def run(self) -> None:
        self.started = True
        self._configure_logging()
        if self.headless:
            return
        self._build_window()
        self._schedule_loops()
        assert self.root is not None
        self.root.mainloop()

    def _configure_logging(self) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=self.log_path,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            encoding="utf-8",
        )

    def _build_window(self) -> None:
        transparent = self.config["window"]["transparent_color"]
        self.root = tk.Tk()
        self.root.title(self.config["pet"]["display_name"])
        self.root.overrideredirect(True)
        self.root.configure(bg=transparent)
        self.root.attributes("-topmost", bool(self.config["window"]["always_on_top"]))
        self.root.wm_attributes("-transparentcolor", transparent)

        width, height = self.sprite_size
        total_height = height + self.bubble_height
        start_x = int(self.config["window"]["start_x"])
        start_y = int(self.config["window"]["start_y"])
        self.root.geometry(f"{width}x{total_height}+{start_x}+{start_y}")

        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=total_height,
            bg=transparent,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Double-Button-1>", self._on_double_click)
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.canvas.bind("<Button-2>", self._on_middle_click)
        self.canvas.bind("<Control-Button-1>", self._on_middle_click)
        self.root.bind("<KeyPress-v>", self._on_voice_hotkey)
        self.root.bind("<KeyPress-V>", self._on_voice_hotkey)
        self._render()

    def _schedule_loops(self) -> None:
        assert self.root is not None
        self.root.after(1, self._animation_loop)
        self.root.after(int(self.config["dialogue"]["idle_first_delay_ms"]), self._idle_loop)
        self.root.after(15000, self._reminder_loop)
        self.root.after(int(self.config["weather"]["startup_delay_seconds"]) * 1000, self._weather_loop)
        self.root.after(int(self.config["codex_status"]["poll_ms"]), self._codex_status_loop)

    def _animation_loop(self) -> None:
        self.frame_index = (self.frame_index + 1) % self.frames.frame_count(self.current_animation)
        self._render()
        assert self.root is not None
        self.root.after(self.animation_delay_ms(), self._animation_loop)

    def _idle_loop(self) -> None:
        now = datetime.now()
        ignored_seconds = int(self.config["dialogue"]["ignored_seconds"])
        if now - self.last_motion_at > timedelta(seconds=ignored_seconds):
            self.show_action(self.brain.ignored(self.state, seed=self.rng.randint(0, 10000)))
        else:
            roll = self.rng.random()
            if roll < float(self.config["dialogue"]["scare_chance"]):
                self.show_action(self.brain.scare(self.state, seed=self.rng.randint(0, 10000)))
            elif roll < float(self.config["dialogue"]["idle_talk_chance"]):
                action = self.brain.click(
                    self.state,
                    "face",
                    now,
                    seed=self.rng.randint(0, 10000),
                )
                self.show_action(action)
        assert self.root is not None
        self.root.after(int(self.config["dialogue"]["idle_loop_ms"]), self._idle_loop)

    def _reminder_loop(self) -> None:
        now = datetime.now()
        events = due_reminders(self.config["reminders"], self.state, now)
        if events:
            event = events[0]
            self.show_action(self.brain.reminder(event, self.state, seed=self.rng.randint(0, 10000)))
            mark_reminder(self.state, event, now)
            self.state.save(self.state_path)
        assert self.root is not None
        self.root.after(60000, self._reminder_loop)

    def _codex_status_loop(self) -> None:
        self.check_codex_status_once()
        assert self.root is not None
        self.root.after(int(self.config["codex_status"]["poll_ms"]), self._codex_status_loop)

    def check_codex_status_once(self) -> bool:
        if self.codex_status_watcher is None:
            return False
        try:
            status = self.codex_status_watcher.poll()
        except Exception:
            logging.exception("Failed to read Codex task status")
            return False
        if status is None:
            return False
        self.current_animation = "running" if status.active else "waving"
        self.state.set_emotion(status.mood, status.intensity)
        self.say(
            status.line,
            seconds=int(self.config["codex_status"].get("show_seconds", 5)),
            mood=status.mood,
            intensity=status.intensity,
        )
        return True

    def _weather_loop(self) -> None:
        if not self.config["weather"]["enabled"] or self.weather_fetching:
            self._reschedule_weather()
            return
        now = datetime.now()
        cooldown = int(self.config["weather"]["cooldown_minutes"])
        if self.state.last_weather_prompt and now - self.state.last_weather_prompt < timedelta(
            minutes=cooldown
        ):
            self._reschedule_weather()
            return
        self.weather_fetching = True
        thread = threading.Thread(target=self._fetch_weather_worker, daemon=True)
        thread.start()

    def _fetch_weather_worker(self) -> None:
        summary = fetch_weather_summary(self.config["weather"])
        if self.root is None:
            self.weather_fetching = False
            return
        self.root.after(0, lambda: self._finish_weather(summary))

    def _finish_weather(self, summary: Any) -> None:
        self.weather_fetching = False
        if summary is not None:
            self.current_animation = "review" if summary.kind != "rain" else "waiting"
            self.state.set_emotion(summary.kind, 5)
            self.say(summary.pet_line, mood=summary.kind, intensity=self.state.mood_intensity)
            mark_reminder(self.state, "weather", datetime.now())
            self.state.save(self.state_path)
        self._reschedule_weather()

    def _reschedule_weather(self) -> None:
        if self.root is not None:
            self.root.after(15 * 60 * 1000, self._weather_loop)

    def show_action(self, action: PetAction) -> None:
        self.current_animation = action.animation
        self.frame_index = 0
        self.say(action.text, mood=action.mood, intensity=action.intensity)
        self.state.persona = action.persona
        self.state.save(self.state_path)

    def answer_question(self, question: str) -> AssistantAnswer:
        answer = self.assistant.ask(question)
        self.current_animation = "review"
        self.state.set_emotion("review", 5)
        self.say(answer.pet_line, seconds=8, mood="review", intensity=5)
        return answer

    def listen_for_question(self) -> VoiceResult:
        result = self.voice_recognizer.listen()
        if result.available and result.text:
            answer = self.answer_question(result.text)
            self.voice_speaker.speak(answer.pet_line)
        else:
            self.current_animation = "waiting"
            self.state.set_emotion("calm", 4)
            self.say(result.message, seconds=6, mood="calm", intensity=4)
        return result

    def start_voice_interaction(self) -> None:
        if self.voice_listening:
            self.say("我已经在听啦，哥哥慢慢说。", seconds=4, mood="calm", intensity=4)
            return
        self.voice_listening = True
        self.current_animation = "waiting"
        self.state.set_emotion("calm", 4)
        self.say("我在听，哥哥你说。", seconds=8, mood="calm", intensity=4)
        thread = threading.Thread(target=self._voice_worker, daemon=True)
        thread.start()

    def _voice_worker(self) -> None:
        result = self.voice_recognizer.listen()
        if self.root is not None:
            self.root.after(0, lambda: self._finish_voice_interaction(result))
        else:
            self._finish_voice_interaction(result)

    def _finish_voice_interaction(self, result: VoiceResult) -> None:
        self.voice_listening = False
        if result.available and result.text:
            question = result.text.strip()
            if not question:
                self.current_animation = "waiting"
                self.state.set_emotion("calm", 4)
                self.say("我没听到内容，哥哥再说一遍嘛。", seconds=6, mood="calm", intensity=4)
                return
            self.say(f"我听到：{question}", seconds=3, mood="review", intensity=4)
            if self.root is not None:
                self.root.after(700, lambda: self._answer_voice_question(question))
            else:
                self._answer_voice_question(question)
            return
        self.current_animation = "waiting"
        self.state.set_emotion("calm", 4)
        self.say(result.message, seconds=6, mood="calm", intensity=4)

    def _answer_voice_question(self, question: str) -> AssistantAnswer:
        answer = self.answer_question(question)
        self.voice_speaker.speak(answer.pet_line)
        return answer

    def say(
        self,
        text: str,
        seconds: int = 5,
        mood: str = "happy",
        intensity: int = 3,
    ) -> None:
        self.bubble_text = text
        self.bubble_mood = mood
        self.bubble_intensity = max(1, min(10, intensity))
        self.bubble_until = datetime.now() + timedelta(seconds=seconds)
        self._render()

    def _frame_image(self) -> Image.Image:
        frame = self.frames.frame(
            self.current_animation,
            self.frame_index % self.frames.frame_count(self.current_animation),
        )
        return prepare_window_frame(
            frame,
            self.sprite_size,
            self.config["window"]["transparent_color"],
        )

    def _render(self) -> None:
        if self.canvas is None:
            return
        width, height = self.sprite_size
        self.canvas.delete("all")
        if self.bubble_until and datetime.now() < self.bubble_until and self.bubble_text:
            self._draw_bubble(width)
        else:
            self.bubble_text = ""
            self.bubble_until = None
        self.photo = ImageTk.PhotoImage(self._frame_image())
        self.canvas.create_image(width // 2, self.bubble_height, image=self.photo, anchor="n")

    def _draw_bubble(self, width: int) -> None:
        assert self.canvas is not None
        style = comic_bubble_style(self.config, self.bubble_mood, self.bubble_intensity)
        x0, y0 = 8, 4
        x1, y1 = width - 8, self.bubble_height - 16
        radius = 16
        self._draw_rounded_rect(
            x0 + 3,
            y0 + 4,
            x1 + 3,
            y1 + 4,
            radius,
            fill=style["shadow"],
            outline=style["shadow"],
            width=1,
        )
        self._draw_rounded_rect(
            x0,
            y0,
            x1,
            y1,
            radius,
            fill=style["fill"],
            outline=style["outline"],
            width=int(style["outline_width"]),
        )
        if style["tail"]:
            tail_x = max(32, width // 3)
            self.canvas.create_polygon(
                tail_x + 3,
                y1 + 3,
                tail_x + 19,
                y1 + 3,
                tail_x + 10,
                y1 + 15,
                fill=style["shadow"],
                outline=style["shadow"],
                width=1,
            )
            self.canvas.create_polygon(
                tail_x,
                y1 - 1,
                tail_x + 16,
                y1 - 1,
                tail_x + 7,
                y1 + 12,
                fill=style["fill"],
                outline=style["outline"],
                width=int(style["outline_width"]),
            )
        font_name = self._font_name(style["font_candidates"])
        self._draw_bubble_decorations(
            x0,
            y0,
            x1,
            y1,
            font_name,
            style["accent"],
            list(style.get("decorations", [])),
        )
        self.canvas.create_text(
            width // 2,
            (y0 + y1) // 2,
            text=self._wrap_text(self.bubble_text, 17),
            fill=style["text"],
            font=(font_name, int(style["font_size"]), "bold"),
            width=width - 28,
            justify="center",
        )

    def _draw_bubble_decorations(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        font_name: str,
        accent: str,
        decorations: list[str],
    ) -> None:
        assert self.canvas is not None
        if not decorations:
            return
        self.canvas.create_line(
            x0 + 18,
            y0 + 9,
            x0 + 54,
            y0 + 9,
            fill=accent,
            width=2,
            capstyle="round",
        )
        self.canvas.create_line(
            x1 - 54,
            y1 - 9,
            x1 - 18,
            y1 - 9,
            fill=accent,
            width=2,
            capstyle="round",
        )
        self.canvas.create_text(
            x0 + 20,
            y0 + 19,
            text=decorations[0],
            fill=accent,
            font=(font_name, 10, "bold"),
        )
        if len(decorations) > 1:
            self.canvas.create_text(
                x1 - 20,
                y0 + 19,
                text=decorations[1],
                fill=accent,
                font=(font_name, 10, "bold"),
            )

    def _draw_rounded_rect(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        radius: int,
        fill: str,
        outline: str,
        width: int,
    ) -> None:
        assert self.canvas is not None
        points = [
            x0 + radius,
            y0,
            x1 - radius,
            y0,
            x1,
            y0,
            x1,
            y0 + radius,
            x1,
            y1 - radius,
            x1,
            y1,
            x1 - radius,
            y1,
            x0 + radius,
            y1,
            x0,
            y1,
            x0,
            y1 - radius,
            x0,
            y0 + radius,
            x0,
            y0,
        ]
        self.canvas.create_polygon(
            points,
            smooth=True,
            fill=fill,
            outline=outline,
            width=width,
        )

    def _font_name(self, candidates: list[str]) -> str:
        try:
            families = set(tkfont.families())
        except Exception:
            families = set()
        for candidate in candidates:
            if not families or candidate in families:
                return candidate
        return "Microsoft YaHei UI"

    def _wrap_text(self, text: str, limit: int) -> str:
        lines: list[str] = []
        current = ""
        for char in text:
            current += char
            if len(current) >= limit:
                lines.append(current)
                current = ""
        if current:
            lines.append(current)
        return "\n".join(lines[:2])

    def _on_press(self, event: tk.Event) -> None:
        assert self.root is not None
        self.drag_start = (event.x_root, event.y_root, self.root.winfo_x(), self.root.winfo_y())
        self.drag_moved = False

    def _on_drag(self, event: tk.Event) -> None:
        if self.root is None or self.drag_start is None:
            return
        start_x, start_y, window_x, window_y = self.drag_start
        dx = event.x_root - start_x
        dy = event.y_root - start_y
        if abs(dx) + abs(dy) > 4:
            self.drag_moved = True
        self.root.geometry(f"+{window_x + dx}+{window_y + dy}")

    def _on_release(self, event: tk.Event) -> None:
        if self.drag_moved:
            self.drag_start = None
            self.drag_moved = False
            return
        self.last_motion_at = datetime.now()
        width, height = self.sprite_size
        sprite_y = max(0, event.y - self.bubble_height)
        region = classify_region(width, height, int(event.x), int(sprite_y))
        self.show_action(
            self.brain.click(
                self.state,
                region,
                datetime.now(),
                seed=self.rng.randint(0, 10000),
            )
        )

    def _on_double_click(self, _event: tk.Event) -> None:
        self.last_motion_at = datetime.now()
        self.show_action(self.brain.switch_form(self.state, seed=self.rng.randint(0, 10000)))

    def _on_right_click(self, _event: tk.Event) -> None:
        self.last_motion_at = datetime.now()
        self.show_action(self.brain.scare(self.state, seed=self.rng.randint(0, 10000)))

    def _on_middle_click(self, _event: tk.Event) -> None:
        self.last_motion_at = datetime.now()
        self.open_question_window()

    def _on_voice_hotkey(self, _event: tk.Event) -> None:
        self.last_motion_at = datetime.now()
        self.start_voice_interaction()

    def open_question_window(self) -> None:
        if self.root is None:
            return
        if self.question_window is not None and self.question_window.winfo_exists():
            self.question_window.lift()
            return
        window = tk.Toplevel(self.root)
        self.question_window = window
        window.title("问富江")
        window.configure(bg="#fffafc")
        window.attributes("-topmost", True)
        window.resizable(False, False)
        frame = tk.Frame(window, bg="#fffafc", padx=10, pady=10)
        frame.pack(fill="both", expand=True)
        entry = tk.Entry(frame, width=28, font=(self._font_name(["YouYuan", "幼圆", "Microsoft YaHei UI"]), 11))
        entry.grid(row=0, column=0, columnspan=2, padx=4, pady=4)

        def submit() -> None:
            question = entry.get().strip()
            if question:
                self.answer_question(question)
                entry.delete(0, "end")

        def listen() -> None:
            self.start_voice_interaction()

        ask_button = tk.Button(frame, text="问她", command=submit, bg="#fff1f5", relief="groove")
        voice_button = tk.Button(frame, text="语音", command=listen, bg="#f7fbff", relief="groove")
        ask_button.grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        voice_button.grid(row=1, column=1, padx=4, pady=4, sticky="ew")
        entry.bind("<Return>", lambda _event: submit())
        entry.focus_set()
