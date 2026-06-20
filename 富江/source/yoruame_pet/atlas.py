from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from .config import default_config


STATE_ROWS = {
    "idle": (0, 6),
    "running-right": (1, 8),
    "running-left": (2, 8),
    "waving": (3, 4),
    "jumping": (4, 5),
    "failed": (5, 8),
    "waiting": (6, 6),
    "running": (7, 6),
    "review": (8, 6),
}


@dataclass
class SpriteAtlas:
    path: Path
    image: Image.Image
    cell_size: tuple[int, int] = (192, 208)

    @classmethod
    def from_default_pet(cls) -> "SpriteAtlas":
        config = default_config()
        path = Path(config["pet"]["atlas_path"])
        return cls.load(path, (config["pet"]["cell_width"], config["pet"]["cell_height"]))

    @classmethod
    def load(cls, path: str | Path, cell_size: tuple[int, int] = (192, 208)) -> "SpriteAtlas":
        path = Path(path)
        image = Image.open(path).convert("RGBA")
        return cls(path=path, image=image, cell_size=cell_size)

    @property
    def states(self) -> list[str]:
        return list(STATE_ROWS)

    def frame_count(self, state: str) -> int:
        return STATE_ROWS[state][1]

    def frame(self, state: str, index: int) -> Image.Image:
        row, count = STATE_ROWS[state]
        if index < 0 or index >= count:
            raise IndexError(f"{state} frame index out of range: {index}")
        width, height = self.cell_size
        left = index * width
        top = row * height
        return self.image.crop((left, top, left + width, top + height)).convert("RGBA")

    def frames(self, state: str) -> list[Image.Image]:
        return [self.frame(state, index) for index in range(self.frame_count(state))]


@dataclass
class DesktopFrameSource:
    fallback: SpriteAtlas
    source_dir: Path | None
    frame_size: tuple[int, int]
    chroma_key: tuple[int, int, int] = (0, 255, 255)
    chroma_threshold: int = 100

    @classmethod
    def from_config(cls, config: dict) -> "DesktopFrameSource":
        fallback = SpriteAtlas.load(
            config["pet"]["atlas_path"],
            (
                int(config["pet"]["cell_width"]),
                int(config["pet"]["cell_height"]),
            ),
        )
        height = int(config["pet"].get("desktop_sprite_height", 360))
        width = round(height * fallback.cell_size[0] / fallback.cell_size[1])
        source_dir = Path(config["pet"].get("decoded_source_dir", ""))
        if not source_dir.exists():
            source_dir = None
        return cls(fallback=fallback, source_dir=source_dir, frame_size=(width, height))

    @property
    def states(self) -> list[str]:
        return self.fallback.states

    def frame_count(self, state: str) -> int:
        return self.fallback.frame_count(state)

    def frame(self, state: str, index: int) -> Image.Image:
        high_res = self._high_res_frame(state, index)
        if high_res is not None:
            return high_res
        return self.fallback.frame(state, index).resize(self.frame_size, Image.Resampling.NEAREST)

    def frames(self, state: str) -> list[Image.Image]:
        return [self.frame(state, index) for index in range(self.frame_count(state))]

    def _high_res_frame(self, state: str, index: int) -> Image.Image | None:
        if self.source_dir is None:
            return None
        source_path = self.source_dir / f"{state}.png"
        if not source_path.exists():
            return None
        strip = Image.open(source_path).convert("RGBA")
        count = self.frame_count(state)
        if index < 0 or index >= count:
            raise IndexError(f"{state} frame index out of range: {index}")
        left = round(strip.width * index / count)
        right = round(strip.width * (index + 1) / count)
        slot = strip.crop((left, 0, right, strip.height))
        cleaned = self._remove_chroma(slot)
        bbox = cleaned.getbbox()
        if bbox is None:
            return Image.new("RGBA", self.frame_size, (0, 0, 0, 0))
        sprite = cleaned.crop(bbox)
        canvas_w, canvas_h = self.frame_size
        ratio = min(canvas_w / sprite.width, canvas_h / sprite.height)
        size = (max(1, round(sprite.width * ratio)), max(1, round(sprite.height * ratio)))
        sprite = sprite.resize(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", self.frame_size, (0, 0, 0, 0))
        x = (canvas_w - size[0]) // 2
        y = canvas_h - size[1]
        canvas.alpha_composite(sprite, (x, y))
        return canvas

    def _remove_chroma(self, image: Image.Image) -> Image.Image:
        key_r, key_g, key_b = self.chroma_key
        output = Image.new("RGBA", image.size, (0, 0, 0, 0))
        source_pixels = image.load()
        output_pixels = output.load()
        width, height = image.size
        threshold_sq = self.chroma_threshold * self.chroma_threshold
        for y in range(height):
            for x in range(width):
                red, green, blue, alpha = source_pixels[x, y]
                distance_sq = (
                    (red - key_r) * (red - key_r)
                    + (green - key_g) * (green - key_g)
                    + (blue - key_b) * (blue - key_b)
                )
                is_cyan_edge = red < 120 and green > 150 and blue > 150
                if alpha == 0 or distance_sq <= threshold_sq or is_cyan_edge:
                    continue
                output_pixels[x, y] = (red, green, blue, 255)
        return output
