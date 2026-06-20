from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class LocalAnswer:
    text: str
    source: str
    citations: list[str]


class LocalSearch:
    def __init__(self, roots: Iterable[str | Path]) -> None:
        self.roots = [Path(root) for root in roots]
        self.extensions = {".md", ".txt", ".json"}

    def answer(self, question: str) -> LocalAnswer | None:
        query = question.strip()
        if not query:
            return None
        best: tuple[int, str, Path] | None = None
        for path in self._iter_files():
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            snippet = self._best_snippet(text, query)
            if snippet is None:
                continue
            score, line = snippet
            if best is None or score > best[0]:
                best = (score, line, path)
        if best is None:
            return None
        _score, line, path = best
        return LocalAnswer(text=line, source="local", citations=[path.name])

    def _iter_files(self) -> Iterable[Path]:
        for root in self.roots:
            if root.is_file() and root.suffix.lower() in self.extensions:
                yield root
            elif root.exists():
                for path in root.rglob("*"):
                    if path.is_file() and path.suffix.lower() in self.extensions:
                        yield path

    def _best_snippet(self, text: str, query: str) -> tuple[int, str] | None:
        best: tuple[int, str] | None = None
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            score = self._score(line, query)
            if score > 0 and (best is None or score > best[0]):
                best = (score, line[:180])
        if best is None or best[0] < 2:
            return None
        return best

    def _score(self, line: str, query: str) -> int:
        line_lower = line.lower()
        query_lower = query.lower()
        score = 0
        for token in query_lower.split():
            if token and token in line_lower:
                score += len(token) * 2
        for char in set(query_lower):
            if char.isspace() or char in "，。！？!?、：:；;的了是我你他她它吗么怎什么":
                continue
            if char in line_lower:
                score += 1
        return score
