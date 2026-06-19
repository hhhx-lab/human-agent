from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .terminal_tui_runtime import ConversationModel

_CONVERSATION_CONTENT_HEIGHT_CACHE: dict[
    tuple[int, int, int, int, int],
    int,
] = {}


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
    return resolve_conversation_content_height(
        conversation,
        width=width,
    )


def conversation_layout_chrome_lines(*, auxiliary_lines: int = 0) -> int:
    # top bar (2) + tab bar (1) + separator (1) + input (1) + footer (1)
    return 6 + max(0, int(auxiliary_lines))


def conversation_visible_height(*, terminal_height: int, auxiliary_lines: int = 0) -> int:
    return resolve_conversation_viewport_height(
        terminal_height=terminal_height,
        auxiliary_lines=auxiliary_lines,
    )


def resolve_conversation_viewport_height(
    *,
    terminal_height: int,
    auxiliary_lines: int = 0,
) -> int:
    chrome = conversation_layout_chrome_lines(auxiliary_lines=auxiliary_lines)
    return max(8, int(terminal_height) - chrome)


def resolve_conversation_content_height(
    conversation: ConversationModel,
    *,
    width: int | None = None,
    animation_tick: int = 0,
) -> int:
    render_width = max(24, int(width or conversation.width or 88))
    running_blocks = sum(1 for record in conversation.blocks if record.running)
    cache_key = (
        id(conversation),
        len(conversation.blocks),
        render_width,
        len(conversation.stream_text),
        running_blocks,
        int(animation_tick),
    )
    cached = _CONVERSATION_CONTENT_HEIGHT_CACHE.get(cache_key)
    if cached is not None:
        return cached

    from prompt_toolkit.formatted_text import FormattedText
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl

    fragments = conversation.render_fragments(animation_tick=animation_tick)
    control = FormattedTextControl(lambda: FormattedText(fragments))
    window = Window(control, wrap_lines=True)
    preferred = int(window.preferred_height(render_width, 10000).preferred or 0)
    height = max(1, preferred)
    _CONVERSATION_CONTENT_HEIGHT_CACHE[cache_key] = height
    return height


def invalidate_conversation_scroll_cache(conversation: ConversationModel | None = None) -> None:
    if conversation is None:
        _CONVERSATION_CONTENT_HEIGHT_CACHE.clear()
        return
    conversation_id = id(conversation)
    stale_keys = [key for key in _CONVERSATION_CONTENT_HEIGHT_CACHE if key[0] == conversation_id]
    for key in stale_keys:
        _CONVERSATION_CONTENT_HEIGHT_CACHE.pop(key, None)


def resolve_conversation_max_scroll(
    *,
    pane,
    conversation: ConversationModel,
    terminal_height: int,
    auxiliary_lines: int = 0,
    width: int | None = None,
    animation_tick: int = 0,
) -> int:
    viewport = resolve_conversation_viewport_height(
        terminal_height=terminal_height,
        auxiliary_lines=auxiliary_lines,
    )
    content_height = resolve_conversation_content_height(
        conversation,
        width=width or conversation.width,
        animation_tick=animation_tick,
    )
    virtual_height = max(content_height, viewport)
    return max(0, virtual_height - viewport)


def clamp_conversation_scroll(
    *,
    pane,
    conversation: ConversationModel,
    terminal_height: int,
    auxiliary_lines: int = 0,
    width: int | None = None,
    animation_tick: int = 0,
) -> None:
    max_scroll = resolve_conversation_max_scroll(
        pane=pane,
        conversation=conversation,
        terminal_height=terminal_height,
        auxiliary_lines=auxiliary_lines,
        width=width,
        animation_tick=animation_tick,
    )
    pane.vertical_scroll = max(0, min(max_scroll, int(getattr(pane, "vertical_scroll", 0) or 0)))


def apply_conversation_scroll_policy(
    *,
    pane,
    conversation: ConversationModel,
    terminal_height: int,
    auxiliary_lines: int = 0,
    width: int | None = None,
    animation_tick: int = 0,
) -> None:
    if not conversation.scroll_to_end:
        clamp_conversation_scroll(
            pane=pane,
            conversation=conversation,
            terminal_height=terminal_height,
            auxiliary_lines=auxiliary_lines,
            width=width,
            animation_tick=animation_tick,
        )
        return
    pane.vertical_scroll = resolve_conversation_max_scroll(
        pane=pane,
        conversation=conversation,
        terminal_height=terminal_height,
        auxiliary_lines=auxiliary_lines,
        width=width,
        animation_tick=animation_tick,
    )


def scroll_conversation_by_lines(
    *,
    pane,
    conversation: ConversationModel,
    delta: int,
    terminal_height: int,
    auxiliary_lines: int = 0,
    width: int | None = None,
    animation_tick: int = 0,
) -> None:
    conversation.scroll_to_end = False
    max_scroll = resolve_conversation_max_scroll(
        pane=pane,
        conversation=conversation,
        terminal_height=terminal_height,
        auxiliary_lines=auxiliary_lines,
        width=width,
        animation_tick=animation_tick,
    )
    pane.vertical_scroll = max(0, min(max_scroll, pane.vertical_scroll + delta))