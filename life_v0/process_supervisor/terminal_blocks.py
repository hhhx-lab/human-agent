from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import uuid4

from .terminal_markdown import format_markdown_body_fragments

if TYPE_CHECKING:
    from .terminal_layout import MessageRenderSpec

DIFF_HEADER_RE = re.compile(r"^(\+\+\+|---|@@)", re.MULTILINE)
SHELL_PREFIXES = ("!", "$ ", "bash ", "sh ", "uv run ", "python ", "npm ", "git ")


@dataclass(frozen=True)
class BlockRenderSpec:
    block_kind: str
    title: str
    body: str
    subtitle: str = ""
    collapsed: bool = False
    selected: bool = False
    running: bool = False
    animation_tick: int = 0
    foldable: bool = True


@dataclass
class BlockRecord:
    block_id: str
    spec: "MessageRenderSpec"
    block_kind: str
    collapsed: bool = False
    running: bool = False
    ephemeral: bool = False

    @staticmethod
    def create(spec: "MessageRenderSpec", *, ephemeral: bool = False) -> "BlockRecord":
        return BlockRecord(
            block_id=uuid4().hex[:10],
            spec=spec,
            block_kind=resolve_block_kind(
                speaker=spec.speaker,
                event_kind=spec.event_kind,
                text=spec.text,
            ),
            collapsed=default_collapsed_for_kind(
                resolve_block_kind(
                    speaker=spec.speaker,
                    event_kind=spec.event_kind,
                    text=spec.text,
                ),
                text=spec.text,
            ),
            ephemeral=ephemeral,
        )


def resolve_block_kind(*, speaker: str, event_kind: str = "", text: str = "") -> str:
    normalized = str(speaker or "").strip().lower()
    kind = str(event_kind or "").strip().lower()
    body = str(text or "")
    if _looks_like_diff(body):
        return "diff"
    if normalized == "relation":
        return "user_prompt"
    if normalized in {"life", "proactive"}:
        return "assistant"
    if normalized == "command" or kind == "command":
        if _looks_like_execute(body):
            return "execute"
        return "tool"
    if normalized in {"command_result", "result"} or kind == "command_result":
        if _looks_like_diff(body):
            return "diff"
        if _looks_like_execute(body):
            return "execute"
        return "tool_result"
    if kind == "proactive_voice":
        return "assistant"
    if kind == "thinking":
        return "thinking"
    return "system"


def default_collapsed_for_kind(block_kind: str, *, text: str) -> bool:
    if block_kind in {"user_prompt", "thinking"}:
        return False
    line_count = len(str(text or "").splitlines())
    if block_kind in {"diff", "tool_result", "execute"}:
        return line_count > 6
    if block_kind == "assistant":
        return line_count > 10
    return line_count > 8


def resolve_block_title(
    *,
    speaker: str,
    life_name: str,
    timestamp: str | None,
    release_badge: str | None,
    block_kind: str,
) -> str:
    normalized = str(speaker or "").strip().lower()
    stamp = str(timestamp or "").strip()
    badge = ""
    if release_badge == "released":
        badge = " released"
    elif release_badge == "unreleased":
        badge = " unreleased"
    if block_kind == "thinking":
        return f"{life_name} · thinking"
    if block_kind == "execute":
        label = "Run"
    elif block_kind == "diff":
        label = "Diff"
    elif block_kind == "tool":
        label = "Tool"
    elif block_kind == "tool_result":
        label = "Result"
    elif normalized == "relation":
        label = "你"
    elif normalized in {"life", "proactive"}:
        label = life_name
    elif normalized == "command":
        label = "command"
    else:
        label = "·"
    if stamp and stamp not in {"··", "..."}:
        stamp = f"[{stamp}]" if not stamp.startswith("[") else stamp
    parts = [part for part in (stamp, label + badge) if part]
    return " · ".join(parts)


def format_message_block_fragments(
    spec: "MessageRenderSpec",
    *,
    width: int = 88,
    markdown: bool = True,
    collapsed: bool | None = None,
    selected: bool = False,
    running: bool = False,
    animation_tick: int = 0,
) -> list[tuple[str, str]]:
    block_kind = resolve_block_kind(
        speaker=spec.speaker,
        event_kind=spec.event_kind,
        text=spec.text,
    )
    title = resolve_block_title(
        speaker=spec.speaker,
        life_name=spec.life_name,
        timestamp=spec.timestamp,
        release_badge=spec.release_badge,
        block_kind=block_kind,
    )
    is_collapsed = (
        default_collapsed_for_kind(block_kind, text=spec.text)
        if collapsed is None
        else collapsed
    )
    return format_block_fragments(
        BlockRenderSpec(
            block_kind=block_kind,
            title=title,
            body=str(spec.text or ""),
            collapsed=is_collapsed,
            selected=selected,
            running=running,
            animation_tick=animation_tick,
        ),
        width=width,
        markdown=markdown,
    )


def format_thinking_block_fragments(
    *,
    life_name: str,
    text: str = "Thinking…",
    width: int = 88,
    running: bool = True,
    animation_tick: int = 0,
) -> list[tuple[str, str]]:
    return format_block_fragments(
        BlockRenderSpec(
            block_kind="thinking",
            title=f"{life_name} · thinking",
            body=text,
            running=running,
            animation_tick=animation_tick,
            foldable=False,
        ),
        width=width,
        markdown=False,
    )


def format_block_fragments(
    spec: BlockRenderSpec,
    *,
    width: int = 88,
    markdown: bool = True,
) -> list[tuple[str, str]]:
    accent_style, accent_char = _accent_for_kind(
        spec.block_kind,
        running=spec.running,
        animation_tick=spec.animation_tick,
    )
    header_style, body_style = _styles_for_kind(spec.block_kind)
    inner_width = max(24, width - 4)
    fragments: list[tuple[str, str]] = []
    if spec.selected:
        fragments.append(("class:block-selected", " " + "─" * max(10, width - 2) + "\n"))
    header = _truncate(spec.title, inner_width)
    if spec.subtitle:
        header = f"{header}  {spec.subtitle}"
    if header:
        fold_marker = ""
        if spec.foldable and str(spec.body or "").strip():
            fold_marker = " ▸" if spec.collapsed else " ▾"
        fragments.extend(
            _accent_line(
                accent_style,
                accent_char,
                f" {header}{fold_marker}\n",
                header_style,
            )
        )
    body_text = str(spec.body or "")
    if spec.collapsed and body_text.strip():
        preview = " ".join(body_text.split())
        preview = _truncate(preview, inner_width)
        fragments.extend(
            _accent_line(accent_style, accent_char, f" {preview}\n", "class:block-muted")
        )
        fragments.extend(
            _accent_line(accent_style, accent_char, " › expand\n", "class:block-muted")
        )
        if spec.selected:
            fragments.append(("class:block-selected", " " + "─" * max(10, width - 2) + "\n"))
        fragments.append(("", "\n"))
        return fragments
    if not body_text.strip():
        fragments.append(("", "\n"))
        return fragments
    if spec.block_kind == "diff":
        body_fragments = _format_diff_body(body_text)
    elif markdown:
        body_fragments = format_markdown_body_fragments(body_text)
    else:
        body_fragments = [
            ("class:block-body", f"  {line}\n" if line else "\n")
            for line in body_text.splitlines() or [""]
        ]
    for style, text in body_fragments:
        for line in str(text).splitlines(keepends=True):
            normalized = line.rstrip("\n")
            if not normalized and line.endswith("\n"):
                fragments.extend(_accent_line(accent_style, accent_char, "\n", body_style))
                continue
            content = normalized[2:] if normalized.startswith("  ") else normalized
            style_name = style or body_style
            if spec.block_kind == "diff" and content.startswith(("+", "-", "@@")):
                if content.startswith("+"):
                    style_name = "class:diff-insert"
                elif content.startswith("-"):
                    style_name = "class:diff-delete"
                elif content.startswith("@@"):
                    style_name = "class:diff-hunk"
            fragments.extend(
                _accent_line(accent_style, accent_char, f" {content}\n", style_name)
            )
    if spec.selected:
        fragments.append(("class:block-selected", " " + "─" * max(10, width - 2) + "\n"))
    fragments.append(("", "\n\n"))
    return fragments


def format_block_viewer_fragments(
    record: BlockRecord,
    *,
    width: int,
    animation_tick: int = 0,
) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = [
        ("class:viewer-title", " 块全屏查看\n"),
        ("class:hint", " Esc 关闭\n\n"),
    ]
    fragments.extend(
        format_message_block_fragments(
            record.spec,
            width=width,
            collapsed=False,
            selected=False,
            running=record.running,
            animation_tick=animation_tick,
        )
    )
    return fragments


def _looks_like_diff(text: str) -> bool:
    normalized = str(text or "")
    if "diff --git" in normalized:
        return True
    return bool(DIFF_HEADER_RE.search(normalized))


def _looks_like_execute(text: str) -> bool:
    first = str(text or "").strip().splitlines()[0] if str(text or "").strip() else ""
    lowered = first.lower()
    return lowered.startswith(SHELL_PREFIXES)


def _format_diff_body(text: str) -> list[tuple[str, str]]:
    lines: list[tuple[str, str]] = []
    for line in str(text or "").splitlines() or [""]:
        if line.startswith("+"):
            lines.append(("class:diff-insert", f"  {line}\n"))
        elif line.startswith("-"):
            lines.append(("class:diff-delete", f"  {line}\n"))
        elif line.startswith("@@"):
            lines.append(("class:diff-hunk", f"  {line}\n"))
        else:
            lines.append(("class:block-body", f"  {line}\n" if line else "\n"))
    return lines


def _accent_line(
    accent_style: str,
    accent_char: str,
    text: str,
    body_style: str,
) -> list[tuple[str, str]]:
    if not text or text == "\n":
        return [(accent_style, f"{accent_char}\n")]
    return [(accent_style, accent_char), (body_style, text)]


def _accent_for_kind(
    block_kind: str,
    *,
    running: bool = False,
    animation_tick: int = 0,
) -> tuple[str, str]:
    mapping = {
        "user_prompt": ("class:block-accent-user", "›"),
        "assistant": ("class:block-accent-assistant", "▌"),
        "thinking": ("class:block-accent-thinking", "▌"),
        "tool": ("class:block-accent-tool", "◆"),
        "execute": ("class:block-accent-execute", "▌"),
        "diff": ("class:block-accent-diff", "▌"),
        "tool_result": ("class:block-accent-system", "▌"),
        "system": ("class:block-accent-system", "▌"),
    }
    style, char = mapping.get(block_kind, ("class:block-accent-system", "▌"))
    if running and block_kind in {"thinking", "execute", "tool"}:
        char = "│" if animation_tick % 2 else "▌"
        style = f"{style} bold"
    return style, char


def _styles_for_kind(block_kind: str) -> tuple[str, str]:
    mapping = {
        "user_prompt": ("class:block-title-user", "class:block-body"),
        "assistant": ("class:block-title-assistant", "class:block-body"),
        "thinking": ("class:block-title-thinking", "class:block-body-thinking"),
        "tool": ("class:block-title-tool", "class:block-body-tool"),
        "execute": ("class:block-title-execute", "class:block-body-execute"),
        "diff": ("class:block-title-diff", "class:block-body"),
        "tool_result": ("class:block-title-system", "class:block-body"),
        "system": ("class:block-title-system", "class:block-body-muted"),
    }
    return mapping.get(block_kind, ("class:block-title-system", "class:block-body"))


def _truncate(text: str, width: int) -> str:
    normalized = str(text or "")
    if len(normalized) <= width:
        return normalized
    return normalized[: max(0, width - 1)] + "…"