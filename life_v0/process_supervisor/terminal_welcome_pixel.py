from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .terminal_welcome import build_welcome_entries

_CANVAS_W = 72
_CANVAS_H = 34
_CYCLE_FRAMES = 64
_HUD_TOP_Y = 2
_FIGURE_Y = 7
_ART_W = 44
_ART_H = 21
_ORIGIN_X = 18
_ORIGIN_Y = _FIGURE_Y
_SPLIT_COL = 22
_CORE = (_ORIGIN_X + 23, _ORIGIN_Y + 10)
_HUD_BOTTOM_Y = 29

_BINARY_WORDS: tuple[str, ...] = (
    "01001001",
    "10110100",
    "01011010",
    "10100101",
    "01101001",
    "11010010",
    "00101101",
)

_STYLE = {
    ".": (" ", "class:welcome-void"),
    "·": ("·", "class:welcome-particle-cyan"),
    "∙": ("∙", "class:welcome-particle-magenta"),
    "░": ("░", "class:welcome-pixel-cyan"),
    "▒": ("▒", "class:welcome-pixel-cyan"),
    "▓": ("▓", "class:welcome-pixel-magenta"),
    "█": ("█", "class:welcome-pixel-magenta"),
    "▄": ("▄", "class:welcome-pixel-cyan"),
    "▀": ("▀", "class:welcome-pixel-magenta"),
    "║": ("║", "class:welcome-circuit-green"),
    "═": ("═", "class:welcome-circuit-green"),
    "╱": ("╱", "class:welcome-circuit-green"),
    "╲": ("╲", "class:welcome-circuit-green"),
    "─": ("─", "class:welcome-circuit-green"),
    "│": ("│", "class:welcome-circuit-green"),
    "┌": ("┌", "class:welcome-circuit-green"),
    "┐": ("┐", "class:welcome-circuit-green"),
    "└": ("└", "class:welcome-circuit-green"),
    "┘": ("┘", "class:welcome-circuit-green"),
    "├": ("├", "class:welcome-circuit-green"),
    "┤": ("┤", "class:welcome-circuit-green"),
    "┬": ("┬", "class:welcome-circuit-green"),
    "┴": ("┴", "class:welcome-circuit-green"),
    "╔": ("╔", "class:welcome-circuit-green"),
    "╗": ("╗", "class:welcome-circuit-green"),
    "╚": ("╚", "class:welcome-circuit-green"),
    "╝": ("╝", "class:welcome-circuit-green"),
    "╟": ("╟", "class:welcome-circuit-green"),
    "╢": ("╢", "class:welcome-circuit-green"),
    "╤": ("╤", "class:welcome-circuit-green"),
    "╧": ("╧", "class:welcome-circuit-green"),
    "╪": ("╪", "class:welcome-fusion"),
    "╫": ("╫", "class:welcome-fusion"),
    "╳": ("╳", "class:welcome-node"),
    "╬": ("╬", "class:welcome-fusion"),
    "╮": ("╮", "class:welcome-circuit-green"),
    "╯": ("╯", "class:welcome-circuit-green"),
    "╭": ("╭", "class:welcome-circuit-green"),
    "╰": ("╰", "class:welcome-circuit-green"),
}


def _pad_art_row(row: str, *, width: int = _ART_W) -> str:
    if len(row) > width:
        return row[:width]
    return row + ("." * (width - len(row)))


def _lean_offset(row_index: int) -> int:
    if row_index < 8:
        return 0
    if row_index < 15:
        return 1
    return 2


# Full-body silhouette: head -> shoulders/arms -> torso -> legs -> feet.
# Viewer-left = streaming cyan/magenta body, later overlaid with binary recall.
_FLESH_ART = tuple(
    _pad_art_row(row)
    for row in (
        "...............····∙····....................",
        "............░░▒▒▓▓██▓▒░░...................",
        "..........░░▓████████▓▓░░..................",
        ".........░▓███████████▓▓░░.................",
        "........░▓██████████▓▓▓░░..................",
        ".........░▓█████████▓░░....................",
        "...........░░▓████▓░░......................",
        "............░▓███▓░.........................",
        "..........▄██▓████▓██▄.....................",
        "........▄███▓██████▓██▄....................",
        ".......░███▓████████▓██░...................",
        "......░███▓████████▓██░....................",
        "......░██▓▓████████▓▓█░....................",
        ".......░█▓▓██████▓▓█░......................",
        ".......░█▓████████▓█░......................",
        "......░██▓██░░░░██▓██░.....................",
        ".....░██▓██░....░██▓██░....................",
        "....░██▓██░......░██▓██░...................",
        "...░██▓█░..........░█▓██░..................",
        "...▄██▄..............▄██▄..................",
        "..▄███▄..............▄███▄.................",
    )
)

# Viewer-right circuit traces follow the same body: head, chest, arm, pelvis, legs.
_CIRCUIT_ART = tuple(
    _pad_art_row(row)
    for row in (
        "............................∙....·.........",
        "..........................╱────╲..∙.......",
        "...........................╲╳╱─╮..........",
        "...........................╱╬╲ │..........",
        "...........................╲╳╱─╯..........",
        "............................││............",
        ".........................╔══╪══╗..........",
        "........................╔╬══╪══╬╗.........",
        "........................║╟────╢║──∙......",
        "........................║╟────╢║.........",
        "........................║╟────╢║╲........",
        "........................║╟────╢║│........",
        "........................╟╪────╪╢│........",
        "........................║╟────╢║│........",
        "........................║╟────╢║╲........",
        "........................║╟──╮.║╟╮........",
        "........................║╟╮.│.║║│........",
        "........................║║│.│.║║│........",
        "........................║║│.│.║║│........",
        "........................╳╧╯...╳╧╯........",
        "..........................................",
    )
)

_SCATTER_BINARY: tuple[tuple[int, int, int], ...] = (
    (_ORIGIN_X + 4, _ORIGIN_Y + 3, 10),
    (_ORIGIN_X + 6, _ORIGIN_Y + 6, 12),
    (_ORIGIN_X + 5, _ORIGIN_Y + 9, 16),
    (_ORIGIN_X + 7, _ORIGIN_Y + 11, 20),
    (_ORIGIN_X + 5, _ORIGIN_Y + 14, 24),
    (_ORIGIN_X + 7, _ORIGIN_Y + 17, 28),
)

_BODY_BINARY_ROWS: tuple[tuple[int, int, str, int], ...] = (
    (12, 3, "10", 18),
    (11, 4, "011", 18),
    (10, 5, "1111", 20),
    (10, 6, "0111", 20),
    (11, 7, "0011", 22),
    (12, 8, "1100", 22),
    (12, 9, "1011", 24),
    (12, 10, "011", 24),
    (11, 11, "101 1", 26),
    (10, 12, "01  01", 28),
    (8, 13, "001  0110", 28),
    (7, 14, "1011011011", 30),
    (6, 15, "011011101110", 30),
    (5, 16, "00011110011", 32),
    (5, 17, "011110011", 34),
    (4, 18, "1110 101", 36),
    (3, 19, "0101 010", 38),
)

_HEAD_HALO_NODES: tuple[tuple[int, int, int], ...] = (
    (_ORIGIN_X + 12, _ORIGIN_Y + 0, 5),
    (_ORIGIN_X + 29, _ORIGIN_Y + 0, 6),
    (_ORIGIN_X + 8, _ORIGIN_Y + 3, 9),
    (_ORIGIN_X + 34, _ORIGIN_Y + 3, 10),
    (_ORIGIN_X + 5, _ORIGIN_Y + 6, 12),
    (_ORIGIN_X + 38, _ORIGIN_Y + 6, 13),
    (_ORIGIN_X + 21, _ORIGIN_Y - 1, 7),
    (_ORIGIN_X + 3, _ORIGIN_Y + 11, 20),
    (_ORIGIN_X + 42, _ORIGIN_Y + 11, 21),
    (_ORIGIN_X + 11, _ORIGIN_Y + 18, 28),
    (_ORIGIN_X + 35, _ORIGIN_Y + 18, 29),
)

_HEAD_HALO_LINKS: tuple[tuple[int, int, int, int, int], ...] = (
    (_ORIGIN_X + 12, _ORIGIN_Y + 1, _ORIGIN_X + 18, _ORIGIN_Y + 3, 10),
    (_ORIGIN_X + 25, _ORIGIN_Y + 1, _ORIGIN_X + 20, _ORIGIN_Y + 3, 11),
    (_ORIGIN_X + 9, _ORIGIN_Y + 3, _ORIGIN_X + 12, _ORIGIN_Y + 5, 13),
    (_ORIGIN_X + 28, _ORIGIN_Y + 3, _ORIGIN_X + 25, _ORIGIN_Y + 5, 14),
    (_ORIGIN_X + 18, _ORIGIN_Y + 0, _ORIGIN_X + 18, _ORIGIN_Y + 2, 8),
    (_ORIGIN_X + 7, _ORIGIN_Y + 5, _ORIGIN_X + 30, _ORIGIN_Y + 5, 16),
    (_ORIGIN_X + 8, _ORIGIN_Y + 10, _ORIGIN_X + 14, _ORIGIN_Y + 15, 24),
    (_ORIGIN_X + 31, _ORIGIN_Y + 10, _ORIGIN_X + 27, _ORIGIN_Y + 15, 25),
    (_ORIGIN_X + 10, _ORIGIN_Y + 11, _CORE[0] - 4, _CORE[1], 32),
    (_ORIGIN_X + _ART_W - 6, _ORIGIN_Y + 11, _CORE[0] + 4, _CORE[1], 33),
    (_CORE[0], _CORE[1] + 1, _CORE[0] + 2, _ORIGIN_Y + 17, 36),
    (_ORIGIN_X + 16, _ORIGIN_Y + 17, _ORIGIN_X + 22, _ORIGIN_Y + 17, 40),
)


@dataclass(frozen=True)
class _TimedPixel:
    x: int
    y: int
    char: str
    style: str
    appear: int
    layer: str


def _manhattan_to_core(x: int, y: int) -> int:
    return abs(x - _CORE[0]) + abs(y - _CORE[1])


def _is_fusion_char(symbol: str) -> bool:
    return symbol in {"╪", "╫", "╬", "╳"}


def _build_timed_pixels() -> tuple[_TimedPixel, ...]:
    pixels: list[_TimedPixel] = []
    for row_index, row in enumerate(_FLESH_ART):
        lean = _lean_offset(row_index)
        for col_index, symbol in enumerate(row):
            if symbol == ".":
                continue
            char, style = _STYLE[symbol]
            x = _ORIGIN_X + col_index + lean
            y = _ORIGIN_Y + row_index
            distance = _manhattan_to_core(x, y)
            appear = 8 + distance * 2 + (col_index % 3)
            if symbol in {"·", "∙"}:
                appear = 4 + (col_index + row_index) % 5
            if col_index >= _SPLIT_COL and symbol in {"▓", "█", "▀"}:
                appear = max(5, appear - 4)
            pixels.append(_TimedPixel(x, y, char, style, appear, "flesh"))
    for row_index, row in enumerate(_CIRCUIT_ART):
        lean = _lean_offset(row_index)
        for col_index, symbol in enumerate(row):
            if symbol in {".", "·", "∙"}:
                continue
            char, style = _STYLE.get(symbol, (symbol, "class:welcome-circuit-green"))
            x = _ORIGIN_X + col_index + lean
            y = _ORIGIN_Y + row_index
            appear = 8 + row_index + max(0, col_index - _SPLIT_COL)
            layer = "fusion" if _is_fusion_char(symbol) else "circuit"
            pixels.append(_TimedPixel(x, y, char, style, appear, layer))
    return tuple(sorted(pixels, key=lambda item: item.appear))


_TIMED_PIXELS = _build_timed_pixels()


def _cycle_tick(tick: int) -> int:
    return int(tick) % _CYCLE_FRAMES


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


def _paint_left_binary_column(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    frame: int,
) -> None:
    start_y = _FIGURE_Y + 1
    for index, word in enumerate(_BINARY_WORDS):
        y = start_y + index * 2
        if y >= _FIGURE_Y + _ART_H - 2:
            break
        if frame < 6 + index * 2:
            continue
        style = (
            "class:welcome-binary-bright"
            if (frame + index) % 5 < 2
            else "class:welcome-binary"
        )
        _paint_text(canvas, x=1, y=y, text=word, style=style)
    stream_y = min(start_y + len(_BINARY_WORDS) * 2, _FIGURE_Y + _ART_H - 1)
    stream_y = max(_FIGURE_Y + 10, stream_y - 1)
    if frame >= 20:
        dots = "." * (1 + frame % 3)
        _paint_text(
            canvas,
            x=1,
            y=stream_y,
            text=f"{dots}STREAMING{dots}",
            style="class:welcome-binary-dim",
        )


def _paint_scatter_binary(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    frame: int,
) -> None:
    for x, y, appear in _SCATTER_BINARY:
        if frame < appear:
            continue
        bit = "1" if (x * 3 + y * 5 + frame) % 2 == 0 else "0"
        existing = canvas.get((x, y))
        if existing and existing[0] not in {" ", "0", "1"}:
            continue
        canvas[(x, y)] = (
            bit,
            "class:welcome-binary-dim" if frame % 4 else "class:welcome-binary",
        )


def _paint_body_binary_stream(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    frame: int,
) -> None:
    for start_col, row_index, bits, appear in _BODY_BINARY_ROWS:
        if frame < appear:
            continue
        lean = _lean_offset(row_index)
        y = _ORIGIN_Y + row_index
        for offset, char in enumerate(bits):
            if char == " ":
                continue
            x = _ORIGIN_X + start_col + lean + offset
            existing = canvas.get((x, y))
            if existing and existing[0] in {"█", "▓", "▒", "░", "▄", "▀"}:
                style = (
                    "class:welcome-binary-bright"
                    if (frame + offset + row_index) % 5 < 3
                    else "class:welcome-binary"
                )
                canvas[(x, y)] = (char, style)


def _integrity_percent(frame: int) -> float:
    if frame <= 0:
        return 0.0
    if frame < 12:
        return min(42.0, frame * 3.5)
    if frame < 48:
        return min(96.0, 42.0 + (frame - 12) * 1.5)
    return 100.0


def _paint_top_hud(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    frame: int,
) -> None:
    dots = "." * (1 + frame % 3)
    _paint_text(
        canvas,
        x=4,
        y=_HUD_TOP_Y,
        text="> INITIATE: SOUL_GEN.EXE",
        style="class:welcome-hud",
    )
    _paint_text(
        canvas,
        x=4,
        y=_HUD_TOP_Y + 1,
        text=f"> STATUS: ASSEMBLING{dots}",
        style="class:welcome-hud",
    )
    _paint_text(
        canvas,
        x=4,
        y=_HUD_TOP_Y + 2,
        text="> PHASE: BIRTH",
        style="class:welcome-hud-bright",
    )


def _paint_bottom_hud(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    frame: int,
) -> None:
    integrity = _integrity_percent(frame)
    label = f"SOUL INTEGRITY: {integrity:5.1f}%"
    label_x = max(2, (_CANVAS_W - len(label)) // 2)
    _paint_text(
        canvas,
        x=label_x,
        y=_HUD_BOTTOM_Y,
        text=label,
        style="class:welcome-hud-bright",
    )

    bar_w = 45
    filled = int(round(bar_w * integrity / 100.0))
    if frame >= 10:
        bar_x = max(2, (_CANVAS_W - bar_w - 2) // 2)
        canvas[(bar_x, _HUD_BOTTOM_Y + 1)] = ("[", "class:welcome-hud")
        canvas[(bar_x + bar_w + 1, _HUD_BOTTOM_Y + 1)] = ("]", "class:welcome-hud")
        for offset in range(bar_w):
            char = "█" if offset < filled else " "
            style = (
                "class:welcome-progress-fill"
                if char == "█"
                else "class:welcome-progress-empty"
            )
            canvas[(bar_x + 1 + offset, _HUD_BOTTOM_Y + 1)] = (char, style)

    if frame >= 48:
        _paint_text(
            canvas,
            x=47,
            y=_HUD_BOTTOM_Y + 2,
            text="POST-HUMAN SYMBIOSIS",
            style="class:welcome-hud",
        )
        _paint_text(
            canvas,
            x=49,
            y=_HUD_BOTTOM_Y + 3,
            text="PROTOCOL: LINKED",
            style="class:welcome-hud",
        )
        ok_style = (
            "class:welcome-hud-ok"
            if frame % 16 < 10
            else "class:welcome-hud-bright"
        )
        _paint_text(canvas, x=60, y=_HUD_BOTTOM_Y + 4, text="[ OK ]", style=ok_style)


def _plot_link(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    tick: int,
    appear: int,
) -> None:
    if tick < appear:
        return
    pulse = (tick + appear) % 10 < 5
    style = "class:welcome-link-active" if pulse else "class:welcome-link"
    steps = max(abs(x2 - x1), abs(y2 - y1), 1)
    for step in range(steps + 1):
        ratio = step / steps
        x = int(round(x1 + (x2 - x1) * ratio))
        y = int(round(y1 + (y2 - y1) * ratio))
        if y >= _HUD_BOTTOM_Y:
            continue
        existing = canvas.get((x, y))
        if existing and existing[1].startswith("class:welcome-hud"):
            continue
        if existing and existing[0] in {"█", "▓", "░", "▒", "▄", "▀"}:
            continue
        if step in {0, steps}:
            char = "·"
            style = (
                "class:welcome-particle-magenta"
                if step == steps and x >= _CORE[0]
                else "class:welcome-particle-cyan"
            )
        elif abs(x2 - x1) >= abs(y2 - y1):
            char = "─"
        else:
            char = "│"
        canvas[(x, y)] = (char, style)


def _apply_chromatic_glitch(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    frame: int,
) -> None:
    if frame < 24 or frame >= 44 or frame % 11 != 0:
        return
    shift = 1 if frame % 14 < 7 else -1
    ghosts: list[tuple[int, int, str, str]] = []
    for (x, y), (char, style) in list(canvas.items()):
        if y < _FIGURE_Y or y >= _HUD_BOTTOM_Y:
            continue
        if style not in {
            "class:welcome-pixel-cyan",
            "class:welcome-pixel-magenta",
            "class:welcome-fusion",
            "class:welcome-node",
        }:
            continue
        if char in {" ", "0", "1"}:
            continue
        ghosts.append((x + shift, y, "▒", "class:welcome-glitch-red"))
    for x, y, char, style in ghosts:
        if 0 <= x < _CANVAS_W and 0 <= y < _CANVAS_H:
            existing = canvas.get((x, y))
            if existing and existing[0] in {"█", "▓"}:
                continue
            canvas[(x, y)] = (char, style)


def _render_canvas(*, tick: int) -> list[list[tuple[str, str]]]:
    frame = _cycle_tick(tick)
    canvas: dict[tuple[int, int], tuple[str, str]] = {}

    for y in range(_CANVAS_H):
        for x in range(_CANVAS_W):
            if y >= _FIGURE_Y and y < _HUD_BOTTOM_Y and (x + y + frame) % 7 == 0:
                canvas[(x, y)] = (" ", "class:welcome-scanline")
            else:
                canvas[(x, y)] = (" ", "class:welcome-void")

    _paint_top_hud(canvas, frame=frame)
    _paint_left_binary_column(canvas, frame=frame)
    _paint_scatter_binary(canvas, frame=frame)

    for x, y, appear in _HEAD_HALO_NODES:
        if frame < appear:
            continue
        pulse = frame % 8 < 4
        style = (
            "class:welcome-particle-magenta"
            if x >= _CORE[0]
            else "class:welcome-particle-cyan"
        )
        char = "∙" if pulse else "·"
        canvas[(x, y)] = (char, style)

    for pixel in _TIMED_PIXELS:
        if frame < pixel.appear:
            continue
        if pixel.layer == "circuit" and frame < 14:
            continue
        if pixel.layer == "circuit":
            existing = canvas.get((pixel.x, pixel.y))
            if existing and existing[0] not in {" ", "0", "1", "·", "∙"}:
                if not _is_fusion_char(pixel.char):
                    continue
        style = pixel.style
        if pixel.layer == "circuit" and frame < pixel.appear + 4:
            style = "class:welcome-circuit-fade"
        if pixel.layer == "flesh" and pixel.x >= _CORE[0] and pixel.char in {"▓", "█"}:
            style = (
                "class:welcome-pixel-magenta"
                if frame % 10 < 6
                else "class:welcome-pixel-magenta-pulse"
            )
        canvas[(pixel.x, pixel.y)] = (pixel.char, style)

    _paint_body_binary_stream(canvas, frame=frame)

    for x1, y1, x2, y2, appear in _HEAD_HALO_LINKS:
        _plot_link(canvas, x1=x1, y1=y1, x2=x2, y2=y2, tick=frame, appear=appear)

    _apply_chromatic_glitch(canvas, frame=frame)
    _paint_bottom_hud(canvas, frame=frame)

    rows: list[list[tuple[str, str]]] = []
    for y in range(_CANVAS_H):
        row: list[tuple[str, str]] = []
        for x in range(_CANVAS_W):
            row.append(canvas.get((x, y), (" ", "class:welcome-void")))
        rows.append(row)
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
    fragments.append(("class:welcome-screen", " " * left_margin))
    fragments.append(("class:welcome-crt-border", "║ "))
    clipped = row[:inner]
    for char, style in clipped:
        fragments.append((style, char))
    if len(clipped) < inner:
        fragments.append(("class:welcome-void", " " * (inner - len(clipped))))
    fragments.append(("class:welcome-crt-border", " ║\n"))


def format_pixel_welcome_screen(
    *,
    terminal_dir: Path,
    life_name: str,
    selection: int,
    width: int,
    height: int,
    animation_tick: int,
) -> list[tuple[str, str]]:
    inner = min(max(60, width - 12), _CANVAS_W)
    entries = build_welcome_entries(terminal_dir=terminal_dir, life_name=life_name)
    if not entries:
        entries = [("new", "新建会话")]
    selected = max(0, min(selection, len(entries) - 1))
    canvas_rows = _render_canvas(tick=animation_tick)

    top_pad = max(0, int(height * 0.03))
    fragments: list[tuple[str, str]] = [("class:welcome-screen", "\n" * top_pad)]

    bezel = "═" * inner
    fragments.append(
        ("class:welcome-crt-bezel", _center_pad(f"╔{bezel}╗", width) + "\n")
    )
    for row in canvas_rows:
        _append_canvas_row(fragments, row=row, inner=inner, width=width)
    fragments.append(
        ("class:welcome-crt-bezel", _center_pad(f"╚{bezel}╝", width) + "\n")
    )

    _, active_label = entries[selected]
    short_label = active_label
    if len(short_label) > inner - 8:
        short_label = short_label[: max(12, inner - 11)] + "…"
    fragments.append(
        ("class:welcome-line", _center_pad(f"› {short_label}", width) + "\n")
    )
    fragments.append(
        (
            "class:hint",
            _center_pad("ENTER WAKE  ↑↓ SESSION  CTRL+N NEW  CTRL+Q EXIT", width) + "\n",
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
