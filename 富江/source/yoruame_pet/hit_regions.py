from __future__ import annotations


def classify_region(width: int, height: int, x: int, y: int) -> str:
    nx = x / max(width, 1)
    ny = y / max(height, 1)

    if ny < 0.28 and 0.34 <= nx <= 0.66:
        return "face"
    if ny < 0.55 and (nx < 0.34 or nx > 0.66):
        return "hair"
    if 0.45 <= ny < 0.67 and (nx < 0.43 or nx > 0.57):
        return "hand"
    if ny >= 0.67:
        return "skirt_legs"
    if 0.28 <= ny < 0.67:
        return "body"
    return "body"

