from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_config() -> dict[str, Any]:
    pet_dir = Path.home() / ".codex" / "pets" / "yoruame-kagehime"
    root = project_root()
    return {
        "pet": {
            "id": "yoruame-kagehime",
            "display_name": "夜雨影姬",
            "atlas_path": str(pet_dir / "spritesheet.webp"),
            "decoded_source_dir": str(root.parent / "pet-runs" / "yoruame-kagehime" / "decoded"),
            "desktop_sprite_height": 360,
            "cell_width": 192,
            "cell_height": 208,
        },
        "window": {
            "scale": 1.0,
            "start_x": 1120,
            "start_y": 560,
            "transparent_color": "#ff00ff",
            "always_on_top": True,
            "animation_ms": 260,
            "animation_ms_by_state": {
                "idle": 520,
                "waiting": 380,
                "review": 360,
                "failed": 340,
                "running": 420,
                "jumping": 420,
            },
            "bubble": {
                "fill": "#fffafc",
                "outline": "#111111",
                "outline_width": 2,
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
            },
        },
        "dialogue": {
            "names": ["夜雨", "哥哥", "凌凌哥哥"],
            "ignored_seconds": 240,
            "idle_loop_ms": 24000,
            "idle_first_delay_ms": 12000,
            "scare_chance": 0.04,
            "idle_talk_chance": 0.12,
            "idle_motion_chance": 0.35,
            "ignored_chance": 0.22,
        },
        "voice": {
            "enabled": False,
            "reply_enabled": True,
            "timeout_seconds": 5,
            "tts_rate": 0,
            "tts_volume": 90,
        },
        "codex_status": {
            "enabled": True,
            "sessions_root": str(Path.home() / ".codex" / "sessions"),
            "poll_ms": 2500,
            "show_seconds": 5,
        },
        "codex_dialogue": {
            "enabled": False,
            "thread_id": "",
            "thread_name": "宠物对话",
            "cwd": str(root.parent),
            "model": "gpt-5.4-mini",
            "timeout_seconds": 120,
            "startup_service_tier": "fast",
            "codex_exe": str(
                Path.home() / "AppData" / "Local" / "OpenAI" / "Codex" / "bin" / "codex.exe"
            ),
            "node_exe": str(
                Path.home()
                / ".cache"
                / "codex-runtimes"
                / "codex-primary-runtime"
                / "dependencies"
                / "node"
                / "bin"
                / "node.exe"
            ),
            "developer_instructions": (
                "你是桌宠富江，只和夜雨/哥哥对话。回复要像真人短句，"
                "可以可爱、傲娇、冷艳，但不要自称 AI。少女状态只能称呼"
                "哥哥、夜雨哥哥、凌凌哥哥。回答问题时先给有用信息，再用桌宠语气收尾。"
            ),
        },
        "reminders": {
            "rest_minutes": 50,
            "move_minutes": 90,
            "late_night_hour": 23,
            "cooldown_minutes": 30,
        },
        "weather": {
            "enabled": True,
            "weather_city": "",
            "startup_delay_seconds": 10,
            "cooldown_minutes": 180,
            "request_timeout_seconds": 6,
        },
        "paths": {
            "state_path": str(root / "data" / "state.json"),
            "log_path": str(root / "logs" / "pet.log"),
            "search_root": str(root),
            "transfer_root": str(root / "transfer"),
        },
    }


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    config = default_config()
    if path is None:
        path = project_root() / "config" / "settings.json"
    path = Path(path)
    if not path.exists():
        return config
    with path.open("r", encoding="utf-8") as handle:
        user_config = json.load(handle)
    if not isinstance(user_config, dict):
        raise ValueError(f"Config root must be an object: {path}")
    return deep_merge(config, user_config)
