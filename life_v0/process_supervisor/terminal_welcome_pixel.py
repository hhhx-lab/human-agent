from __future__ import annotations

from pathlib import Path

from .terminal_welcome import build_welcome_entries
from .welcome_reference_cells import REFERENCE_CELLS

_CANVAS_W = 80
_CANVAS_H = 26
_LOAD_FRAMES = 64
_CYCLE_FRAMES = 80

_BINARY_WORDS: tuple[str, ...] = (
    "01001001",
    "10110100",
    "01011010",
    "10100101",
    "01101001",
)

_STYLE_PREFIX = "class:"


def _style(name: str) -> str:
    return f"{_STYLE_PREFIX}{name}"


def _progress_percent(frame: int) -> float:
    tick = max(0, int(frame))
    if tick >= _LOAD_FRAMES:
        return 100.0
    return min(100.0, tick * (100.0 / _LOAD_FRAMES))


def _paint_text(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    x: int,
    y: int,
    text: str,
    style: str,
) -> None:
    for offset, char in enumerate(text):
        px = x + offset
        if 0 <= px < _CANVAS_W and 0 <= y < _CANVAS_H:
            canvas[(px, y)] = (char, style)


def _paint_left_binary(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
) -> None:
    if progress < 4:
        return
    for index, word in enumerate(_BINARY_WORDS):
        y = 4 + index * 2
        if y > 14:
            break
        threshold = 6 + index * 5
        if progress < threshold:
            continue
        style = (
            _style("welcome-binary-bright")
            if (index + int(progress)) % 3 == 0
            else _style("welcome-binary")
        )
        _paint_text(canvas, x=1, y=y, text=word, style=style)
    if progress >= 28:
        dots = "." * (1 + int(progress) % 3)
        _paint_text(
            canvas,
            x=1,
            y=15,
            text=f"{dots}STREAMING{dots}",
            style=_style("welcome-binary-dim"),
        )


def _paint_top_hud(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
    frame: int,
) -> None:
    if progress < 2:
        return
    _paint_text(
        canvas,
        x=2,
        y=0,
        text="> INITIATE: SOUL_GEN.EXE",
        style=_style("welcome-hud"),
    )
    dots = "." * (1 + frame % 3)
    _paint_text(
        canvas,
        x=2,
        y=1,
        text=f"> STATUS: ASSEMBLING{dots}",
        style=_style("welcome-hud"),
    )
    phase = "BIRTH" if progress < 88 else "SYMBIOSIS"
    _paint_text(
        canvas,
        x=2,
        y=2,
        text=f"> PHASE: {phase}",
        style=_style("welcome-hud-bright"),
    )


def _paint_bottom_hud(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
    frame: int,
) -> None:
    if progress < 8:
        return
    label = f"SOUL INTEGRITY: {progress:5.1f}%"
    _paint_text(
        canvas,
        x=max(2, (_CANVAS_W - len(label)) // 2),
        y=21,
        text=label,
        style=_style("welcome-hud-bright"),
    )

    bar_w = 28
    filled = int(round(bar_w * progress / 100.0))
    bar = "█" * filled + "░" * max(0, bar_w - filled)
    bar_x = max(2, (_CANVAS_W - len(bar)) // 2)
    for offset, char in enumerate(bar):
        style = (
            _style("welcome-progress-fill")
            if char == "█"
            else _style("welcome-progress-empty")
        )
        canvas[(bar_x + offset, 22)] = (char, style)

    if progress >= 72:
        _paint_text(
            canvas,
            x=55,
            y=23,
            text="POST-HUMAN SYMBIOSIS",
            style=_style("welcome-hud"),
        )
        _paint_text(
            canvas,
            x=57,
            y=24,
            text="PROTOCOL: LINKED",
            style=_style("welcome-hud"),
        )
        ok_style = (
            _style("welcome-hud-ok")
            if frame % 16 < 10
            else _style("welcome-hud-bright")
        )
        _paint_text(canvas, x=73, y=24, text="[ OK ]", style=ok_style)


def _render_canvas(*, tick: int) -> list[list[tuple[str, str]]]:
    frame = int(tick) % _CYCLE_FRAMES
    progress = _progress_percent(frame)
    canvas: dict[tuple[int, int], tuple[str, str]] = {}

    for y in range(_CANVAS_H):
        for x in range(_CANVAS_W):
            if (x + y + frame) % 6 == 0:
                canvas[(x, y)] = (" ", _style("welcome-scanline"))
            else:
                canvas[(x, y)] = (" ", _style("welcome-void"))

    for x, y, char, style_name, reveal in REFERENCE_CELLS:
        if progress < reveal:
            continue
        fade = min(1.0, max(0.0, (progress - reveal) / 8.0))
        style = _style(style_name)
        if fade < 0.55 and style_name.startswith("welcome-pixel"):
            style = _style("welcome-circuit-fade")
        canvas[(x, y)] = (char, style)

    _paint_top_hud(canvas, progress=progress, frame=frame)
    _paint_left_binary(canvas, progress=progress)
    _paint_bottom_hud(canvas, progress=progress, frame=frame)

    rows: list[list[tuple[str, str]]] = []
    for y in range(_CANVAS_H):
        rows.append([canvas.get((x, y), (" ", _style("welcome-void"))) for x in range(_CANVAS_W)])
    return rows


def _center_pad(line: str, width: int) -> str:
    if len(line) >= width:
        return line[:width]
    left = max(0, (width - len(line)) // 2)
    return (" " * left) + line


def _append_canvas_row(
    fragments: list[tuple[str, str]],
    *,
    row: list[tuple[str, str]],
    inner: int,
    width: int,
) -> None:
    left_margin = max(0, (width - inner - 2) // 2)
    fragments.append((_style("welcome-screen"), " " * left_margin))
    fragments.append((_style("welcome-crt-border"), "│ "))
    clipped = row[:inner]
    for char, style in clipped:
        fragments.append((style, char))
    if len(clipped) < inner:
        fragments.append((_style("welcome-void"), " " * (inner - len(clipped))))
    fragments.append((_style("welcome-crt-border"), " │\n"))


def _common_commands_line(inner: int) -> str:
    hints = "Enter 唤醒  ↑↓ 会话  Ctrl+N 新建  Ctrl+P 命令  Ctrl+Q 退出"
    if len(hints) > inner:
        hints = "Enter 唤醒  ↑↓ 会话  Ctrl+P 命令  Ctrl+Q 退出"
    return hints


def format_pixel_welcome_screen(
    *,
    terminal_dir: Path,
    life_name: str,
    selection: int,
    width: int,
    height: int,
    animation_tick: int,
) -> list[tuple[str, str]]:
    inner = min(max(56, width - 6), _CANVAS_W)
    entries = build_welcome_entries(terminal_dir=terminal_dir, life_name=life_name)
    if not entries:
        entries = [("new", "新建会话")]
    selected = max(0, min(selection, len(entries) - 1))
    canvas_rows = _render_canvas(tick=animation_tick)
    progress = _progress_percent(int(animation_tick) % _CYCLE_FRAMES)

    top_pad = max(0, int(height * 0.02))
    fragments: list[tuple[str, str]] = [(_style("welcome-screen"), "\n" * top_pad)]

    header_left = "Digital Life"
    header_right = life_name
    header_gap = max(2, inner - len(header_left) - len(header_right))
    fragments.append(
        (
            _style("welcome-title"),
            _center_pad(f"{header_left}{' ' * header_gap}{header_right}", width) + "\n",
        )
    )

    bezel = "─" * inner
    fragments.append(
        (_style("welcome-crt-border"), _center_pad(f"┌{bezel}┐", width) + "\n")
    )
    for row in canvas_rows:
        _append_canvas_row(fragments, row=row, inner=inner, width=width)
    fragments.append(
        (_style("welcome-crt-border"), _center_pad(f"└{bezel}┘", width) + "\n")
    )

    _, active_label = entries[selected]
    short_label = active_label
    if len(short_label) > inner - 8:
        short_label = short_label[: max(12, inner - 11)] + "…"
    fragments.append(
        (_style("welcome-line"), _center_pad(f"› {short_label}", width) + "\n")
    )
    fragments.append(
        (
            _style("welcome-phase"),
            _center_pad(f"加载 {progress:5.1f}%", width) + "\n",
        )
    )
    fragments.append(
        (
            _style("hint"),
            _center_pad(_common_commands_line(inner), width) + "\n",
        )
    )
    return fragments


def render_welcome_preview_frames(*, ticks: range | None = None) -> list[str]:
    selected_ticks = list(ticks or range(0, _CYCLE_FRAMES, 4))
    frames: list[str] = []
    terminal_dir = Path("runtime/state/terminal")
    for tick in selected_ticks:
        rendered = "".join(
            fragment
            for _, fragment in format_pixel_welcome_screen(
                terminal_dir=terminal_dir,
                life_name="Adam",
                selection=0,
                width=100,
                height=32,
                animation_tick=tick,
            )
        )
        frames.append(f"=== frame {tick} ===\n{rendered}")
    return frames