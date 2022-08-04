"""
This file hold utilities function for skia renderer
"""

from ...core import p5


def mode_adjust(a, b, c, d, mode):
    if mode == "CORNER":
        return {"x": a, "y": b, "w": c, "h": d}
    # TODO: Add documentation for CORNERS mode
    elif mode == "CORNERS":
        return {"x": a, "y": b, "w": c - a, "h": d - b}
    elif mode == "RADIUS":
        return {"x": a - c, "y": b - d, "w": c * 2, "h": d * 2}
    elif mode == "CENTER":
        return {"x": a - c * 0.5, "y": b - d * 0.5, "w": c, "h": d}
    else:
        raise ValueError(f"Unknown mode {mode}")


def should_draw():
    return p5.renderer.style.stroke_enabled or p5.renderer.style.fill_enabled
