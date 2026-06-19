#!/usr/bin/env python3
"""Render welcome screen at 100% and compare with 参考图.png."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PIL import Image

from life_v0.process_supervisor.terminal_welcome_pixel import _render_canvas


def _canvas_to_image(rows: list[list[tuple[str, str]]]) -> Image.Image:
    palette = {
        "welcome-void": (0, 0, 0),
        "welcome-scanline": (5, 5, 5),
        "welcome-pixel-cyan": (0, 255, 255),
        "welcome-pixel-magenta": (255, 0, 255),
        "welcome-circuit-green": (0, 255, 159),
        "welcome-circuit-fade": (26, 92, 58),
        "welcome-binary": (57, 255, 20),
        "welcome-binary-bright": (127, 255, 127),
        "welcome-binary-dim": (26, 77, 46),
        "welcome-hud": (57, 255, 20),
        "welcome-hud-bright": (127, 255, 127),
        "welcome-hud-ok": (0, 255, 159),
        "welcome-progress-fill": (57, 255, 20),
        "welcome-progress-empty": (26, 77, 46),
    }
    height = len(rows)
    width = len(rows[0]) if rows else 0
    img = Image.new("RGB", (width, height), (0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        for x, (char, style) in enumerate(row):
            if char == " ":
                continue
            key = style.replace("class:", "")
            px[x, y] = palette.get(key, (180, 180, 180))
    return img.resize((width * 8, height * 16), Image.Resampling.NEAREST)


def main() -> int:
    ref_path = ROOT / "参考图.png"
    if not ref_path.exists():
        print(f"missing reference: {ref_path}")
        return 1

    rows = _render_canvas(tick=64)
    rendered = _canvas_to_image(rows)

    ref = Image.open(ref_path).convert("RGB")
    rw, rh = ref.size
    crop = ref.crop((int(rw * 0.095), int(rh * 0.075), int(rw * 0.905), int(rh * 0.93)))
    target = crop.resize(rendered.size, Image.Resampling.NEAREST)

    out_dir = ROOT / "runtime"
    out_dir.mkdir(exist_ok=True)
    rendered_path = out_dir / "welcome_render_100.png"
    diff_path = out_dir / "welcome_render_diff.png"
    rendered.save(rendered_path)

    diff = Image.new("RGB", rendered.size)
    dpx = diff.load()
    rpx = rendered.load()
    tpx = target.load()
    total = 0
    mismatch = 0
    for y in range(rendered.size[1]):
        for x in range(rendered.size[0]):
            total += 1
            a = rpx[x, y]
            b = tpx[x, y]
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) > 80:
                mismatch += 1
                dpx[x, y] = (255, 0, 0)
            else:
                dpx[x, y] = (0, 40, 0)
    diff.save(diff_path)
    score = 100.0 * (1.0 - mismatch / max(total, 1))
    print(f"similarity: {score:.1f}%")
    print(f"rendered: {rendered_path}")
    print(f"diff: {diff_path}")
    return 0 if score >= 35 else 1


if __name__ == "__main__":
    raise SystemExit(main())