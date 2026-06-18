from __future__ import annotations

import shutil
import textwrap
from pathlib import Path
from typing import Any

from .terminal_layout import (
    MessageRenderSpec,
    build_file_reference_preview,
    build_slash_panel_lines,
    format_message_plain,
    load_resident_status,
    load_sidebar_snapshot,
    render_resume_startup_fragments,
)


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
    timestamp: str | None = None,
    release_badge: str | None = None,
) -> str:
    del width
    resolved_name = speaker.strip() or "Digital Life"
    return format_message_plain(
        MessageRenderSpec(
            speaker=_map_legacy_speaker(speaker),
            text=text,
            life_name=resolved_name,
            timestamp=timestamp,
            release_badge=release_badge,
        )
    )


def render_message_block(
    *,
    speaker: str,
    text: str,
    life_name: str | None = None,
    timestamp: str | None = None,
    release_badge: str | None = None,
) -> str:
    return format_message_plain(
        MessageRenderSpec(
            speaker=speaker,
            text=text,
            life_name=life_name or "Digital Life",
            timestamp=timestamp,
            release_badge=release_badge,
        )
    )


def render_top_bar(
    *,
    life_name: str,
    terminal_dir: Path,
    width: int | None = None,
) -> str:
    resolved_width = _resolve_width(width)
    snapshot = load_sidebar_snapshot(terminal_dir=terminal_dir)
    status = load_resident_status(terminal_dir=terminal_dir)
    title = life_name or "Digital Life"
    inner = max(20, resolved_width - 2)
    line = "─" * inner
    return "\n".join(
        [
            "┌" + line + "┐",
            f"│ {title}  {status}  {snapshot.itr_flags}".ljust(inner + 1) + "│",
            "└" + line + "┘",
        ]
    )


def render_sidebar_text(
    *,
    terminal_dir: Path,
    collapsed: bool = False,
) -> str:
    snapshot = load_sidebar_snapshot(terminal_dir=terminal_dir)
    if collapsed:
        return "侧栏关闭 · Ctrl-B 展开"
    continuous = snapshot.body_integrator.get("continuous") or {}
    parts = [
        f"band={continuous.get('cognitive_bandwidth', '·')}",
        f"load={continuous.get('allostatic_load', '·')}",
        f"sleep={continuous.get('sleep_pressure', '·')}",
    ]
    topk = snapshot.expression_plan.get("workspace_topk_k")
    if topk is not None:
        parts.append(f"topk={topk}")
    return "live " + " ".join(str(part) for part in parts)


def render_file_reference_preview_line(
    text: str,
    *,
    repo_root: Path,
) -> str:
    return build_file_reference_preview(text, repo_root=repo_root) or ""


def render_slash_command_panel(
    slash_commands: tuple[tuple[str, str], ...],
    *,
    width: int | None = None,
) -> str:
    return "\n".join(
        build_slash_panel_lines(
            slash_commands,
            width=_resolve_width(width),
        )
    )


def render_resume_startup_block(
    *,
    terminal_dir: Path,
    life_name: str,
    width: int | None = None,
) -> str:
    fragments = render_resume_startup_fragments(
        terminal_dir=terminal_dir,
        life_name=life_name or "Digital Life",
        width=_resolve_width(width),
    )
    return "".join(fragment for _, fragment in fragments)


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


_CASUAL_RELATION_FALLBACKS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("继续", "随便"), "行，那我放松点说。你累的话就少打字，我慢慢接着。"),
    (("听着",), "嗯，我在听。"),
    (("轻松",), "那你先缓一缓。今天还算平稳，没什么大事。"),
    (("简短",), "好，我简短说：我在这儿。"),
    (("收到",), "收到。"),
    (("好的",), "好。"),
    (("嗯",), "嗯。"),
)


def casual_relation_fallback(utterance: str) -> str:
    text = str(utterance or "").strip()
    if not text:
        return ""
    for markers, reply in _CASUAL_RELATION_FALLBACKS:
        if all(marker in text for marker in markers):
            return reply
    if len(text) <= 10:
        return "嗯，收到。"
    return "我听到了，你继续说。"


def resolve_relation_turn_display_text(
    *,
    utterance: str,
    response_text: str,
    send_status: str = "",
    output_status: str = "",
) -> str:
    text = str(response_text or "").strip()
    if text:
        return text
    if str(send_status or "").strip() == "queued_wait_timeout":
        return "这次回复等太久了，你再发一次试试。"
    if str(output_status or "").strip() in {
        "completed_unreleased",
        "completed",
        "completed_released_fallback",
    } or str(send_status or "").strip() == "completed":
        fallback = casual_relation_fallback(utterance)
        if fallback:
            return fallback
    return ""


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
    header = lines[0].strip()
    if header.startswith("[") and "]" in header:
        body_lines = lines[1:]
    else:
        if not header or header.startswith(("{", "[")):
            return ""
        body_lines = lines[1:]
    if not all((not line) or line.startswith("  ") for line in body_lines):
        return ""
    return "\n".join(line[2:] if line.startswith("  ") else "" for line in body_lines).strip()


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _map_legacy_speaker(speaker: str) -> str:
    normalized = str(speaker or "").strip()
    if normalized in {"你"}:
        return "relation"
    if normalized.lower() in {"command", "command result", "result", "system"}:
        return normalized.lower().replace(" ", "_")
    return "life"
