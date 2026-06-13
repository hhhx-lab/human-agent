from __future__ import annotations

import shutil
import textwrap
from typing import Any


DEFAULT_TERMINAL_WIDTH = 88
MIN_TERMINAL_WIDTH = 56
MAX_TERMINAL_WIDTH = 112


def render_digital_life_banner(
    *,
    life_name: str | None = None,
    status: str | None = None,
    width: int | None = None,
) -> str:
    resolved_width = _resolve_width(width)
    title = "Digital Life"
    subtitle_parts = []
    if life_name:
        subtitle_parts.append(f"name: {life_name}")
    if status:
        subtitle_parts.append(f"state: {status}")
    subtitle = " | ".join(subtitle_parts) or "resident relation terminal"
    return _box(
        title=title,
        body=[
            subtitle,
            "输入关系话语后按 Enter；/exit 只离开当前终端，/stop 会请求常驻进程停止。",
        ],
        width=resolved_width,
    )


def render_life_opening(
    state: dict[str, Any] | None = None,
    *,
    life_name: str | None = None,
    width: int | None = None,
) -> str:
    state = state or {}
    resolved_name = life_name or _text(state.get("life_name")) or "Digital Life"
    status = _text(state.get("status")) or "restored"
    next_kind = (
        _text(state.get("resident_autonomous_activity_next_kind"))
        or _text(state.get("autonomous_activity_next_kind"))
    )
    waiting_mode = (
        _text(state.get("resident_waiting_mode"))
        or _text(state.get("resident_terminal_current_mode"))
        or _text(state.get("residency_posture"))
    )
    activity_count = state.get("resident_autonomous_activity_count")

    body = [
        f"终端已连接：{resolved_name}",
        f"状态：{status}；会话模式：{waiting_mode or 'relation_waiting'}。",
    ]
    if activity_count is not None or next_kind:
        activity_line = "常驻进程已恢复"
        if activity_count is not None:
            activity_line += f"，活动计数 {activity_count}"
        if next_kind:
            activity_line += f"，下一状态 {next_kind}"
        body.append(activity_line + "。")
    body.append("输入关系话语后按 Enter；/exit 离开当前终端，/stop 请求停止常驻进程。")
    return _box(title=f"{resolved_name} / terminal", body=body, width=width)


def render_dialogue_box(
    speaker: str,
    text: str,
    *,
    width: int | None = None,
) -> str:
    return _box(title=speaker, body=str(text or "").splitlines() or [""], width=width)


def render_input_prompt(*, life_name: str | None = None) -> str:
    prefix = life_name or "关系"
    return f"{prefix} > "


def render_life_cycle_output(
    emitted_output: str,
    *,
    life_name: str | None = None,
    width: int | None = None,
) -> str:
    response_text = extract_life_response_text(emitted_output)
    if response_text:
        return render_dialogue_box(
            life_name or "Digital Life",
            response_text,
            width=width,
        )
    return render_dialogue_box("Digital Life", emitted_output, width=width)


def extract_life_response_text(emitted_output: str) -> str:
    stripped = str(emitted_output or "").strip()
    if not stripped:
        return ""
    boxed_body = _extract_box_body(stripped)
    if boxed_body:
        return boxed_body
    if stripped.startswith("{") or stripped.startswith("["):
        return ""
    return stripped


def _box(*, title: str, body: list[str], width: int | None = None) -> str:
    resolved_width = _resolve_width(width)
    inner_width = resolved_width - 4
    title_text = f" {title.strip() or 'Digital Life'} "
    if len(title_text) > inner_width:
        title_text = title_text[:inner_width]
    left = (inner_width - len(title_text)) // 2
    right = inner_width - len(title_text) - left
    top = "+" + "-" * left + title_text + "-" * right + "+"
    divider = "+" + "-" * inner_width + "+"
    lines = [top]
    for paragraph in body:
        wrapped = _wrap_line(str(paragraph), inner_width)
        if not wrapped:
            lines.append("| " + " " * inner_width + " |")
            continue
        for line in wrapped:
            lines.append("| " + line.ljust(inner_width) + " |")
    lines.append(divider)
    return "\n".join(lines)


def _wrap_line(text: str, width: int) -> list[str]:
    if text == "":
        return [""]
    return textwrap.wrap(
        text,
        width=max(width, 20),
        replace_whitespace=False,
        drop_whitespace=True,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [text]


def _resolve_width(width: int | None) -> int:
    if width is None:
        width = shutil.get_terminal_size((DEFAULT_TERMINAL_WIDTH, 24)).columns
    return max(MIN_TERMINAL_WIDTH, min(MAX_TERMINAL_WIDTH, int(width)))


def _extract_box_body(emitted_output: str) -> str:
    lines: list[str] = []
    for raw_line in str(emitted_output or "").splitlines():
        line = raw_line.rstrip()
        if not line.startswith("| ") or not line.endswith(" |"):
            continue
        content = line[2:-2].rstrip()
        if content:
            lines.append(content)
    return "\n".join(lines).strip()


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""
