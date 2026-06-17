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
    del status
    title = life_name or "Digital Life"
    return _box(
        title=f"{title} / live terminal",
        body=[
            "直接输入文字开始交谈。",
            "/ 查看状态命令，@ 引用当前项目里的文件或文件夹。",
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
    body = [
        resolved_name,
        "/state /memory /dream /emotion /relationship",
        "@docs @life_v0",
    ]
    return _box(title="conversation", body=body, width=width)


def render_dialogue_box(
    speaker: str,
    text: str,
    *,
    width: int | None = None,
) -> str:
    lines = str(text or "").splitlines() or [""]
    body = [("  " + line) if line else "" for line in lines]
    return "\n".join([speaker.strip() or "Digital Life", *body])


def render_input_prompt(*, life_name: str | None = None) -> str:
    prefix = life_name or "关系"
    return f"╭─ {prefix} " + "─" * 42 + "\n╰─> "


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
    transcript_body = _extract_transcript_body(stripped)
    if transcript_body:
        return transcript_body
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


def _extract_transcript_body(emitted_output: str) -> str:
    lines = str(emitted_output or "").splitlines()
    if len(lines) < 2:
        return ""
    speaker = lines[0].strip()
    if not speaker or speaker.startswith(("{", "[")):
        return ""
    body_lines = lines[1:]
    if not all((not line) or line.startswith("  ") for line in body_lines):
        return ""
    return "\n".join(line[2:] if line.startswith("  ") else "" for line in body_lines).strip()


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""
