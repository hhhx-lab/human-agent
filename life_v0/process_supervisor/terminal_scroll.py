from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .terminal_tui_runtime import ConversationModel


def estimate_conversation_visual_lines(conversation: ConversationModel) -> int:
    total = 0
    for record in conversation.blocks:
        body = str(record.spec.text or "")
        line_count = len(body.splitlines()) if body.strip() else 1
        if record.collapsed and body.strip():
            line_count = min(line_count, 2)
        total += 3 + line_count
    return max(total, 1)


def count_conversation_display_lines(
    conversation: ConversationModel,
    *,
    width: int | None = None,
) -> int:
    from prompt_toolkit.utils import get_cwidth

    render_width = max(24, int(width or conversation.width or 88))
    total = 0
    for _style, text in conversation.render_fragments():
        normalized = str(text or "")
        if not normalized:
            continue
        for line in normalized.split("\n"):
            if not line:
                total += 1
                continue
            line_width = sum(get_cwidth(char) for char in line)
            total += max(1, (line_width + render_width - 1) // render_width)
    return max(total, 1)


def conversation_visible_height(*, terminal_height: int, auxiliary_lines: int = 0) -> int:
    reserved = 10 + max(0, auxiliary_lines)
    return max(8, int(terminal_height) - reserved)


def resolve_conversation_max_scroll(
    *,
    pane,
    conversation: ConversationModel,
    terminal_height: int,
    auxiliary_lines: int = 0,
    width: int | None = None,
) -> int:
    visible = conversation_visible_height(
        terminal_height=terminal_height,
        auxiliary_lines=auxiliary_lines,
    )
    render_info = getattr(pane, "render_info", None)
    if render_info is not None:
        return max(0, int(render_info.content_height) - int(render_info.window_height))
    content_lines = count_conversation_display_lines(conversation, width=width)
    return max(0, content_lines - visible)


def apply_conversation_scroll_policy(
    *,
    pane,
    conversation: ConversationModel,
    terminal_height: int,
    auxiliary_lines: int = 0,
    width: int | None = None,
) -> None:
    if not conversation.scroll_to_end:
        return
    pane.vertical_scroll = resolve_conversation_max_scroll(
        pane=pane,
        conversation=conversation,
        terminal_height=terminal_height,
        auxiliary_lines=auxiliary_lines,
        width=width,
    )


def scroll_conversation_by_lines(
    *,
    pane,
    conversation: ConversationModel,
    delta: int,
    terminal_height: int,
    auxiliary_lines: int = 0,
    width: int | None = None,
) -> None:
    conversation.scroll_to_end = False
    max_scroll = resolve_conversation_max_scroll(
        pane=pane,
        conversation=conversation,
        terminal_height=terminal_height,
        auxiliary_lines=auxiliary_lines,
        width=width,
    )
    pane.vertical_scroll = max(0, min(max_scroll, pane.vertical_scroll + delta))