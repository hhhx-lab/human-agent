from __future__ import annotations

from pathlib import Path

from .terminal_welcome import build_welcome_entries

_CANVAS_W = 112
_CANVAS_H = 42
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
_FLOW_CHARS = ("·", "∙", "•", "✦")
_ASSEMBLY_TARGETS: tuple[tuple[int, int, str, float], ...] = (
    (51, 4, "welcome-particle-cyan", 8),
    (56, 4, "welcome-particle-magenta", 10),
    (60, 5, "welcome-circuit-green", 12),
    (50, 7, "welcome-particle-cyan", 14),
    (55, 7, "welcome-particle-magenta", 16),
    (61, 8, "welcome-circuit-green", 18),
    (52, 12, "welcome-particle-cyan", 20),
    (57, 12, "welcome-particle-magenta", 22),
    (60, 13, "welcome-circuit-green", 24),
    (52, 15, "welcome-particle-cyan", 26),
    (56, 15, "welcome-fusion", 28),
    (61, 15, "welcome-circuit-green", 30),
    (45, 17, "welcome-particle-cyan", 34),
    (52, 17, "welcome-particle-magenta", 36),
    (57, 17, "welcome-fusion", 38),
    (64, 17, "welcome-circuit-green", 40),
    (71, 17, "welcome-circuit-green", 42),
    (38, 20, "welcome-particle-cyan", 44),
    (47, 21, "welcome-particle-magenta", 46),
    (52, 21, "welcome-heart-red", 48),
    (59, 21, "welcome-fusion", 50),
    (66, 21, "welcome-circuit-green", 52),
    (76, 21, "welcome-circuit-green", 54),
    (37, 24, "welcome-particle-cyan", 52),
    (49, 24, "welcome-heart-red", 54),
    (53, 24, "welcome-heart-red", 56),
    (60, 24, "welcome-fusion", 58),
    (68, 24, "welcome-circuit-green", 60),
    (76, 24, "welcome-circuit-green", 62),
    (39, 29, "welcome-particle-magenta", 60),
    (51, 29, "welcome-heart-red", 62),
    (59, 29, "welcome-fusion", 64),
    (67, 29, "welcome-circuit-green", 66),
    (75, 29, "welcome-circuit-green", 68),
    (45, 33, "welcome-particle-cyan", 70),
    (53, 33, "welcome-particle-magenta", 72),
    (62, 33, "welcome-circuit-green", 74),
    (70, 33, "welcome-circuit-green", 76),
)


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


def _paint_revealed_text(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    x: int,
    y: int,
    text: str,
    style: str,
    progress: float,
    reveal: float,
) -> None:
    if progress < reveal:
        return
    fade = min(1.0, max(0.0, (progress - reveal) / 12.0))
    active_style = style if fade >= 0.45 else _style("welcome-circuit-fade")
    _paint_text(canvas, x=x, y=y, text=text, style=active_style)


def _paint_binary_cells(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    x: int,
    y: int,
    width: int,
    progress: float,
    reveal: float,
    frame: int,
    salt: int,
) -> None:
    if progress < reveal:
        return
    for offset in range(width):
        bit = "1" if ((frame + salt + offset * 3) % 5) in {0, 2, 3} else "0"
        style_name = (
            "welcome-pixel-magenta"
            if ((frame // 2 + salt + offset) % 3 == 0)
            else "welcome-pixel-cyan"
        )
        canvas[(x + offset, y)] = (bit, _style(style_name))


def _paint_circuit_text(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    x: int,
    y: int,
    text: str,
    progress: float,
    reveal: float,
    frame: int,
    pulse_salt: int,
) -> None:
    if progress < reveal:
        return
    _paint_revealed_text(
        canvas,
        x=x,
        y=y,
        text=text,
        style=_style("welcome-circuit-green"),
        progress=progress,
        reveal=reveal,
    )
    active_positions = [i for i, char in enumerate(text) if char not in {" ", "╭", "╮", "╰", "╯"}]
    if not active_positions:
        return
    pulse = active_positions[(frame * 3 + pulse_salt) % len(active_positions)]
    canvas[(x + pulse, y)] = (
        "●" if frame % 2 == 0 else "∙",
        _style("welcome-particle-white" if frame % 3 == 0 else "welcome-particle-cyan"),
    )


def _clamp_cell(value: int, *, upper: int) -> int:
    return max(0, min(upper, value))


def _paint_assembly_particles(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
    frame: int,
) -> None:
    # Early frames are intentionally only moving particles. As progress rises,
    # each particle eases toward a target point on the final humanoid.
    for index, (target_x, target_y, style_name, lock_progress) in enumerate(_ASSEMBLY_TARGETS):
        orbit_x = 6 + ((index * 17 + frame * (2 + index % 3)) % 84)
        orbit_y = 4 + ((index * 11 + frame * (1 + index % 2)) % 21)
        convergence = min(1.0, max(0.0, progress / max(1.0, lock_progress)))
        if progress >= lock_progress + 10:
            convergence = 1.0
        ease = convergence * convergence * (3.0 - 2.0 * convergence)
        x = round(orbit_x + (target_x - orbit_x) * ease)
        y = round(orbit_y + (target_y - orbit_y) * ease)
        char = _FLOW_CHARS[(index + frame // 3) % len(_FLOW_CHARS)]
        if ease > 0.82:
            char = "●" if index % 4 == 0 else "∙"
        if ease > 0.96 and progress < 100:
            char = "✦" if index % 5 == 0 else "·"
        canvas[(_clamp_cell(x, upper=_CANVAS_W - 1), _clamp_cell(y, upper=_CANVAS_H - 1))] = (
            char,
            _style(style_name),
        )


def _paint_left_binary(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
) -> None:
    if progress < 4:
        return
    for index, word in enumerate(_BINARY_WORDS):
        y = 8 + index * 2
        if y > 16:
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
        _paint_text(
            canvas,
            x=1,
            y=18,
            text="...STREAMING...",
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
        text="INITIATE: SOUL_GEN.EXE",
        style=_style("welcome-hud"),
    )
    _paint_text(
        canvas,
        x=2,
        y=1,
        text="STATUS: ASSEMBLING...",
        style=_style("welcome-hud"),
    )
    _paint_text(
        canvas,
        x=2,
        y=2,
        text="PHASE: BIRTH",
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
        y=35,
        text=label,
        style=_style("welcome-hud-bright"),
    )

    bar_w = 48
    filled = int(round(bar_w * progress / 100.0))
    bar = "[" + ("█" * filled) + (" " * max(0, bar_w - filled)) + "]"
    bar_x = max(2, (_CANVAS_W - len(bar)) // 2)
    for offset, char in enumerate(bar):
        style = (
            _style("welcome-progress-fill")
            if char == "█"
            else _style("welcome-progress-empty")
        )
        canvas[(bar_x + offset, 36)] = (char, style)

    if progress >= 10:
        center_x = bar_x + len(bar) // 2
        for particle_index in range(18):
            side = -1 if particle_index % 2 == 0 else 1
            distance = 2 + ((frame * (2 + particle_index % 4) + particle_index * 5) % 24)
            x = _clamp_cell(center_x + side * distance, upper=_CANVAS_W - 1)
            y = 36 if particle_index % 3 else 37
            char = _FLOW_CHARS[(frame + particle_index) % len(_FLOW_CHARS)]
            style_name = (
                "welcome-particle-white"
                if particle_index % 4 == 0
                else "welcome-particle-cyan"
                if particle_index % 2 == 0
                else "welcome-particle-magenta"
            )
            canvas[(x, y)] = (char, _style(style_name))
        canvas[(center_x, 36)] = ("●", _style("welcome-hud-ok"))

    if progress >= 72:
        _paint_text(
            canvas,
            x=70,
            y=38,
            text="POST-HUMAN SYMBIOSIS",
            style=_style("welcome-hud"),
        )
        _paint_text(
            canvas,
            x=72,
            y=39,
            text="PROTOCOL: LINKED",
            style=_style("welcome-hud"),
        )
        ok_style = (
            _style("welcome-hud-ok")
            if frame % 16 < 10
            else _style("welcome-hud-bright")
        )
        _paint_text(canvas, x=82, y=40, text="[ OK ]", style=ok_style)


def _paint_particle_field(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
    frame: int,
) -> None:
    if progress < 10:
        return
    streams = (
        (27, 35, 5, 12, 1, 3),
        (60, 72, 5, 16, -1, 4),
        (15, 24, 18, 38, 1, 4),
        (66, 78, 18, 40, -1, 4),
        (15, 24, 23, 54, 1, 5),
        (67, 80, 23, 56, -1, 5),
    )
    for index, (start, end, y, reveal, direction, speed) in enumerate(streams):
        if progress < reveal:
            continue
        span = max(1, end - start + 1)
        for particle_index in range(2):
            offset = (frame * speed + particle_index * 7 + index * 5) % span
            if direction < 0:
                offset = span - 1 - offset
            x = start + offset
            char = _FLOW_CHARS[(particle_index + index + frame // 7) % len(_FLOW_CHARS)]
            style = (
                _style("welcome-particle-cyan")
                if (particle_index + index) % 2 == 0
                else _style("welcome-particle-magenta")
            )
            canvas[(x, y)] = (char, style)


def _paint_flowing_circuit_line(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    x1: int,
    x2: int,
    y: int,
    progress: float,
    reveal: float,
    frame: int,
    direction: int = 1,
    rail_char: str = "─",
) -> None:
    if progress < reveal:
        return
    left = max(0, min(x1, x2))
    right = min(_CANVAS_W - 1, max(x1, x2))
    if not (0 <= y < _CANVAS_H) or left > right:
        return
    base_style = (
        _style("welcome-link-active")
        if progress - reveal > 22
        else _style("welcome-link")
    )
    for x in range(left, right + 1):
        canvas[(x, y)] = (rail_char, base_style)
    span = max(1, right - left + 1)
    pulse_offset = (frame * 2) % span
    if direction < 0:
        pulse_offset = span - 1 - pulse_offset
    pulse_x = left + pulse_offset
    for dx, char in ((-1, "═"), (0, "●"), (1, "═")):
        x = pulse_x + dx
        if left <= x <= right:
            canvas[(x, y)] = (char, _style("welcome-circuit-green"))


def _paint_flowing_circuit_column(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    x: int,
    y1: int,
    y2: int,
    progress: float,
    reveal: float,
    frame: int,
    direction: int = 1,
) -> None:
    if progress < reveal:
        return
    top = max(0, min(y1, y2))
    bottom = min(_CANVAS_H - 1, max(y1, y2))
    if not (0 <= x < _CANVAS_W) or top > bottom:
        return
    base_style = (
        _style("welcome-link-active")
        if progress - reveal > 22
        else _style("welcome-link")
    )
    for y in range(top, bottom + 1):
        canvas[(x, y)] = ("│", base_style)
    span = max(1, bottom - top + 1)
    pulse_offset = frame % span
    if direction < 0:
        pulse_offset = span - 1 - pulse_offset
    pulse_y = top + pulse_offset
    canvas[(x, pulse_y)] = ("●", _style("welcome-circuit-green"))


def _paint_flowing_circuit_network(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
    frame: int,
) -> None:
    # Keep the live circuitry in the peripheral glass. The humanoid owns the
    # central nervous-system traces; crossing rails make the silhouette muddy.
    lines = (
        (17, 29, 7, 22, 1),
        (68, 89, 7, 24, -1),
        (7, 19, 24, 58, 1),
        (74, 90, 24, 60, -1),
    )
    for x1, x2, y, reveal, direction in lines:
        _paint_flowing_circuit_line(
            canvas,
            x1=x1,
            x2=x2,
            y=y,
            progress=progress,
            reveal=reveal,
            frame=frame,
            direction=direction,
        )
    columns = (
        (89, 11, 18, 46, -1),
        (80, 18, 23, 60, 1),
    )
    for x, y1, y2, reveal, direction in columns:
        _paint_flowing_circuit_column(
            canvas,
            x=x,
            y1=y1,
            y2=y2,
            progress=progress,
            reveal=reveal,
            frame=frame,
            direction=direction,
        )


def _paint_circuit_flow_particles(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
    frame: int,
) -> None:
    if progress < 20:
        return
    for index in range(136):
        band = index % 4
        if band == 0:
            x = 57 + ((frame * (3 + index % 5) + index * 4) % 16)
            y = 17 + ((frame * (2 + index % 3) + index * 5) % 17)
        elif band == 1:
            x = 64 + ((frame * (4 + index % 4) + index * 3) % 15)
            y = 17 + ((frame * (2 + index % 2) + index * 7) % 16)
        elif band == 2:
            x = 70 + ((frame * (3 + index % 4) + index * 5) % 13)
            y = 18 + ((frame * (2 + index % 3) + index * 6) % 15)
        else:
            x = 60 + ((frame * (5 + index % 3) + index * 2) % 20)
            y = 18 + ((frame * (3 + index % 2) + index * 4) % 9)
        canvas[(x, y)] = (
            "●" if index % 3 == 0 else "✦" if index % 11 == 0 else "∙",
            _style("welcome-particle-white" if index % 4 == 0 else "welcome-particle-cyan"),
        )


def _paint_heart_convergence_particles(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
    frame: int,
) -> None:
    if progress < 18:
        return
    heart_x = 50
    heart_y = 23
    for index in range(96):
        from_left = index % 2 == 0
        start_x = 16 + (index * 3) % 24 if from_left else 72 + (index * 5) % 28
        start_y = 14 + (index * 7) % 20
        phase = ((frame * (3 + index % 5) + index * 11) % 36) / 35.0
        x = round(start_x + (heart_x - start_x) * phase)
        y = round(start_y + (heart_y - start_y) * phase)
        style_name = (
            "welcome-heart-red"
            if abs(x - heart_x) + abs(y - heart_y) <= 4 and index % 4 == 0
            else "welcome-particle-white"
            if index % 5 == 0
            else "welcome-particle-cyan"
            if from_left
            else "welcome-particle-magenta"
        )
        canvas[(_clamp_cell(x, upper=_CANVAS_W - 1), _clamp_cell(y, upper=_CANVAS_H - 1))] = (
            _FLOW_CHARS[(frame + index) % len(_FLOW_CHARS)],
            _style(style_name),
        )


def _paint_beating_heart(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
    frame: int,
) -> None:
    if progress < 44:
        return
    pulse_style = _style("welcome-heart-red" if frame % 16 < 8 else "welcome-heart-dim")
    rows = (
        (47, 21, "██  ██"),
        (46, 22, "███████"),
        (46, 23, "███████"),
        (47, 24, " ████ "),
        (48, 25, " ██ "),
    )
    for x, y, text in rows:
        _paint_text(canvas, x=x, y=y, text=text, style=pulse_style)


def _paint_humanoid(
    canvas: dict[tuple[int, int], tuple[str, str]],
    *,
    progress: float,
    frame: int,
) -> None:
    head_binary_rows = (
        (52, 4, 4, 12),
        (50, 5, 6, 14),
        (49, 6, 7, 16),
        (49, 7, 7, 18),
        (49, 8, 7, 20),
        (50, 9, 6, 22),
        (51, 10, 5, 24),
        (52, 11, 4, 26),
        (53, 12, 3, 28),
        (53, 13, 3, 30),
        (54, 14, 2, 32),
    )
    for x, y, width, reveal in head_binary_rows:
        _paint_binary_cells(
            canvas,
            x=x,
            y=y,
            width=width,
            progress=progress,
            reveal=reveal,
            frame=frame,
            salt=y,
        )

    head_circuits = (
        (56, 4, "╭─●╮", 14),
        (56, 5, "├●┬┤", 16),
        (56, 6, "│╭┴┤", 18),
        (56, 7, "├┬●┤", 20),
        (56, 8, "│●╭┤", 22),
        (56, 9, "├╯││", 24),
        (56, 10, "╰●┴╯", 26),
        (57, 11, "││", 28),
        (57, 12, "●│", 30),
        (57, 13, "│●", 32),
        (57, 14, "╰╯", 34),
    )
    for x, y, text, reveal in head_circuits:
        _paint_circuit_text(
            canvas,
            x=x,
            y=y,
            text=text,
            progress=progress,
            reveal=reveal,
            frame=frame,
            pulse_salt=y,
        )

    neck_binary_rows = (
        (53, 15, 3, 34),
        (53, 16, 3, 36),
    )
    for x, y, width, reveal in neck_binary_rows:
        _paint_binary_cells(
            canvas,
            x=x,
            y=y,
            width=width,
            progress=progress,
            reveal=reveal,
            frame=frame,
            salt=20 + y,
        )
    for x, y, text, reveal in (
        (57, 15, "│●│", 34),
        (57, 16, "╰┬●", 36),
    ):
        _paint_circuit_text(
            canvas,
            x=x,
            y=y,
            text=text,
            progress=progress,
            reveal=reveal,
            frame=frame,
            pulse_salt=30 + y,
        )

    torso_binary_rows = (
        (41, 17, 14, 40),
        (40, 18, 15, 42),
        (40, 19, 15, 44),
        (40, 20, 15, 46),
        (40, 21, 15, 48),
        (40, 22, 15, 50),
        (41, 23, 14, 52),
        (41, 24, 14, 54),
        (42, 25, 13, 56),
        (43, 26, 12, 58),
        (44, 27, 11, 60),
        (45, 28, 10, 62),
        (46, 29, 9, 64),
        (47, 30, 8, 66),
        (48, 31, 7, 68),
        (49, 32, 6, 70),
    )
    for x, y, width, reveal in torso_binary_rows:
        _paint_binary_cells(
            canvas,
            x=x,
            y=y,
            width=width,
            progress=progress,
            reveal=reveal,
            frame=frame,
            salt=50 + y,
        )

    torso_circuit_rows = (
        (56, 17, "╭──●─┬──●╮", 40),
        (56, 18, "├┬●─┼─●┬┤", 42),
        (56, 19, "│├●┬┴─┬●│", 44),
        (56, 20, "││╭●─┴┬┤│", 46),
        (56, 21, "├●╯╭─●┼┴┤", 48),
        (56, 22, "│├─●╯│╭●┤", 50),
        (56, 23, "││╭─●┴┬─┤", 52),
        (56, 24, "├●┴─┬──●╯", 54),
        (56, 25, "│╰┬●┴╮│", 56),
        (56, 26, "│╭┼─●╯│", 58),
        (56, 27, "╰┬┴●╮╭╯", 60),
        (57, 28, "│●─┬┤", 62),
        (57, 29, "├──●╯", 64),
        (57, 30, "│╭●┤", 66),
        (57, 31, "╰┴╮●", 68),
        (58, 32, "╰●┴╯", 70),
    )
    for x, y, text, reveal in torso_circuit_rows:
        _paint_circuit_text(
            canvas,
            x=x,
            y=y,
            text=text,
            progress=progress,
            reveal=reveal,
            frame=frame,
            pulse_salt=70 + y,
        )

    right_chest_fill_rows = (
        (64, 17, "╭─●─┬──╮", 40),
        (65, 18, "├●┬─┼●┤", 42),
        (66, 19, "├┬●┼─┤", 44),
        (66, 20, "│├─●┬┤", 46),
        (66, 21, "├●┬─┴╯", 48),
        (66, 22, "│╰●┬╮", 50),
        (66, 23, "├─┬●┤", 52),
        (66, 24, "●╭┴┬┤", 54),
        (66, 25, "├●─┼╯", 56),
        (66, 26, "│╭●┤", 58),
        (65, 27, "╰●┼┤", 60),
        (65, 28, "╭─●┴╯", 62),
        (65, 29, "├●┬╮", 64),
        (65, 30, "││●┤", 66),
        (64, 31, "╰●┴╯", 68),
    )
    for x, y, text, reveal in right_chest_fill_rows:
        _paint_circuit_text(
            canvas,
            x=x,
            y=y,
            text=text,
            progress=progress,
            reveal=reveal,
            frame=frame,
            pulse_salt=150 + y,
        )

    left_arm_rows = (
        (33, 17, 9, 40),
        (31, 18, 10, 42),
        (30, 19, 10, 44),
        (30, 20, 10, 46),
        (30, 21, 10, 48),
        (31, 22, 9, 50),
        (32, 23, 9, 52),
        (32, 24, 9, 54),
        (33, 25, 8, 56),
        (34, 26, 8, 58),
        (35, 27, 7, 60),
        (35, 28, 7, 62),
        (36, 29, 7, 64),
        (36, 30, 6, 66),
        (37, 31, 6, 68),
        (37, 32, 6, 70),
    )
    for x, y, width, reveal in left_arm_rows:
        _paint_binary_cells(
            canvas,
            x=x,
            y=y,
            width=width,
            progress=progress,
            reveal=reveal,
            frame=frame,
            salt=90 + y,
        )

    right_arm_rows = (
        (70, 17, "╭●──┬──╮", 40),
        (71, 18, "├╮╭●┬─┤", 42),
        (72, 19, "│││╭●┤", 44),
        (72, 20, "●╯││││", 46),
        (72, 21, "│╭╯●┤│", 48),
        (72, 22, "│╭─┬●┤", 50),
        (71, 23, "├●╯│││", 52),
        (71, 24, "│╭─●┤│", 54),
        (71, 25, "●╮│╭┤│", 56),
        (70, 26, "├●┴─┼╯", 58),
        (70, 27, "│╭●┬╯", 60),
        (70, 28, "●┤╭╯", 62),
        (69, 29, "├╮●", 64),
        (69, 30, "│●┤", 66),
        (68, 31, "╰●╮", 68),
        (68, 32, "╰●╯", 70),
    )
    for x, y, text, reveal in right_arm_rows:
        _paint_circuit_text(
            canvas,
            x=x,
            y=y,
            text=text,
            progress=progress,
            reveal=reveal,
            frame=frame,
            pulse_salt=110 + y,
        )

    for x, y, text, reveal, style_name in (
        (54, 18, "1●", 42, "welcome-fusion"),
        (54, 19, "0◈", 44, "welcome-fusion"),
        (54, 20, "1●", 46, "welcome-fusion"),
        (54, 21, "0●", 48, "welcome-fusion"),
        (54, 22, "1◈", 50, "welcome-fusion"),
        (54, 23, "0●", 52, "welcome-fusion"),
        (54, 24, "1●", 54, "welcome-fusion"),
        (54, 25, "0◈", 56, "welcome-fusion"),
        (55, 26, "●", 58, "welcome-fusion"),
        (55, 27, "◈", 60, "welcome-fusion"),
        (55, 28, "●", 62, "welcome-fusion"),
    ):
        _paint_revealed_text(
            canvas,
            x=x,
            y=y,
            text=text,
            style=_style(style_name),
            progress=progress,
            reveal=reveal,
        )

    node_network = (
        (47, 5, "●─╮", 22, "welcome-particle-cyan"),
        (61, 5, "╭─●", 24, "welcome-particle-magenta"),
        (47, 10, "●─╯", 28, "welcome-particle-magenta"),
        (62, 11, "╰─●", 30, "welcome-particle-cyan"),
        (41, 17, "●─╮", 40, "welcome-particle-cyan"),
        (72, 17, "╭─●", 42, "welcome-particle-magenta"),
        (38, 24, "●──╮", 48, "welcome-particle-magenta"),
        (77, 24, "╭──●", 50, "welcome-particle-cyan"),
        (41, 31, "●─╯", 56, "welcome-particle-cyan"),
        (73, 31, "╰─●", 58, "welcome-particle-magenta"),
        (48, 34, "●──╯", 64, "welcome-particle-magenta"),
        (63, 34, "╰──●", 66, "welcome-particle-cyan"),
    )
    for x, y, text, reveal, style_name in node_network:
        _paint_revealed_text(
            canvas,
            x=x,
            y=y,
            text=text,
            style=_style(style_name),
            progress=progress,
            reveal=reveal,
        )

    _paint_heart_convergence_particles(canvas, progress=progress, frame=frame)
    _paint_circuit_flow_particles(canvas, progress=progress, frame=frame)
    for x, y, text, reveal in (
        (57, 31, "╰┴╮●", 68),
        (58, 32, "╰●╯ ", 70),
        (68, 32, "╰●╯ ", 70),
    ):
        _paint_revealed_text(
            canvas,
            x=x,
            y=y,
            text=text,
            style=_style("welcome-circuit-green"),
            progress=progress,
            reveal=reveal,
        )
    _paint_beating_heart(canvas, progress=progress, frame=frame)
    _paint_particle_field(canvas, progress=progress, frame=frame)


def _render_canvas(*, tick: int) -> list[list[tuple[str, str]]]:
    frame = int(tick) % _CYCLE_FRAMES
    progress = _progress_percent(tick)
    canvas: dict[tuple[int, int], tuple[str, str]] = {}

    for y in range(_CANVAS_H):
        for x in range(_CANVAS_W):
            if (x + y + frame) % 6 == 0:
                canvas[(x, y)] = (" ", _style("welcome-scanline"))
            else:
                canvas[(x, y)] = (" ", _style("welcome-void"))

    _paint_assembly_particles(canvas, progress=progress, frame=frame)
    _paint_top_hud(canvas, progress=progress, frame=frame)
    _paint_left_binary(canvas, progress=progress)
    _paint_flowing_circuit_network(canvas, progress=progress, frame=frame)
    _paint_humanoid(canvas, progress=progress, frame=frame)
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
    inner = min(max(72, width - 6), _CANVAS_W)
    entries = build_welcome_entries(terminal_dir=terminal_dir, life_name=life_name)
    if not entries:
        entries = [("new", "新建会话")]
    selected = max(0, min(selection, len(entries) - 1))
    canvas_rows = _render_canvas(tick=animation_tick)
    progress = _progress_percent(int(animation_tick))

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
        (_style("welcome-crt-border"), _center_pad(f"╭{bezel}╮", width) + "\n")
    )
    for row in canvas_rows:
        _append_canvas_row(fragments, row=row, inner=inner, width=width)
    fragments.append(
        (_style("welcome-crt-border"), _center_pad(f"╰{bezel}╯", width) + "\n")
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
                width=128,
                height=52,
                animation_tick=tick,
            )
        )
        frames.append(f"=== frame {tick} ===\n{rendered}")
    return frames
