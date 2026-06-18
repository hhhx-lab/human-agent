from __future__ import annotations

import shutil
import threading
import time
from pathlib import Path
from typing import Callable

from .prompt_toolkit_terminal_app import (
    TerminalIdleVoicePolicy,
    _TerminalCompleter,
    _confirm_selected_completion_or_submit,
    _move_completion_selection_or_history,
)
from .terminal_layout import (
    MessageRenderSpec,
    TerminalLayoutState,
    format_auxiliary_fragments,
    format_footer_fragments,
    format_sidebar_pane_fragments,
    format_top_bar_fragments,
    load_resident_status,
    load_sidebar_snapshot,
    resolve_release_badge,
    resolve_sidebar_pane_width,
    resolve_terminal_layout_state,
)
from .terminal_session_tabs import (
    create_terminal_session_tab,
    cycle_terminal_session_tab,
    format_session_tab_bar_fragments,
    list_terminal_session_tabs,
    switch_terminal_session,
)
from .terminal_session_transcript import (
    append_terminal_session_event,
    resolve_attach_terminal_session,
)
from .terminal_command_palette import (
    apply_palette_list_scroll_policy,
    build_palette_items,
    filter_palette_items,
    format_palette_detail_fragments,
    format_palette_footer_fragments,
    format_palette_list_fragments,
    resolve_palette_action,
    resolve_palette_visible_items,
)
from .terminal_scroll import (
    apply_conversation_scroll_policy,
    scroll_conversation_by_lines,
)
from .terminal_stream_bridge import stream_session
from .terminal_theme import build_terminal_style, cycle_terminal_theme
from .terminal_tui_runtime import ConversationModel, resolve_streaming_life_spec
from .terminal_ui_state import TerminalUIState
from .terminal_welcome import build_welcome_entries
from .terminal_welcome_pixel import format_pixel_welcome_screen


def run_prompt_toolkit_split_terminal_app(
    *,
    terminal_dir: Path,
    life_name: str | None,
    handle_utterance: Callable[[str], tuple[int | None, str]],
    slash_commands: tuple[tuple[str, str], ...],
    idle_voice_fn: Callable[[], str | None] | None = None,
    repo_root: Path | None = None,
    idle_voice_interval_seconds: float = 90.0,
) -> int:
    from prompt_toolkit.application import Application
    from prompt_toolkit.buffer import Buffer
    from prompt_toolkit.cursor_shapes import CursorShape
    from prompt_toolkit.filters import Condition
    from prompt_toolkit.formatted_text import FormattedText
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import (
        ConditionalContainer,
        Dimension,
        HSplit,
        Layout,
        ScrollablePane,
        VSplit,
        Window,
    )
    from prompt_toolkit.layout.containers import Float, FloatContainer, ScrollOffsets
    from prompt_toolkit.layout.margins import ScrollbarMargin
    from prompt_toolkit.eventloop.utils import call_soon_threadsafe
    from prompt_toolkit.keys import Keys
    from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
    from prompt_toolkit.layout.menus import CompletionsMenu
    from prompt_toolkit.mouse_events import MouseEventType

    class _ScrollableConversationControl(FormattedTextControl):
        def __init__(
            self,
            *,
            text_func: Callable[[], object],
            on_scroll: Callable[[int], None],
        ) -> None:
            super().__init__(text_func)
            self._on_scroll = on_scroll

        def mouse_handler(self, mouse_event):
            if mouse_event.event_type == MouseEventType.SCROLL_UP:
                self._on_scroll(-3)
                return None
            if mouse_event.event_type == MouseEventType.SCROLL_DOWN:
                self._on_scroll(3)
                return None
            return super().mouse_handler(mouse_event)

    name = life_name or "Digital Life"
    opened_session = resolve_attach_terminal_session(
        terminal_dir=terminal_dir,
        life_name=name,
    )
    session_id = str(opened_session.get("session_id") or "")
    repo_root = repo_root or Path.cwd()
    layout_state = resolve_terminal_layout_state()
    completer = _TerminalCompleter(
        slash_commands=slash_commands,
        repo_root=repo_root,
    )
    history = InMemoryHistory()
    idle_policy = TerminalIdleVoicePolicy(
        interval_seconds=idle_voice_interval_seconds,
    )
    stop_idle_thread = threading.Event()
    conversation = ConversationModel(use_markdown=True)
    conversation.load_startup(
        terminal_dir=terminal_dir,
        life_name=name,
        width=layout_state.terminal_width,
    )
    ui_state = TerminalUIState()
    ui_state.enter_welcome()
    palette_items = build_palette_items(slash_commands=slash_commands)
    exit_code_holder: list[int | None] = [None]
    app_ref: list[Application | None] = [None]
    turn_inflight = threading.Event()
    stream_started = {"value": False}

    def _refresh_terminal_geometry() -> None:
        size = shutil.get_terminal_size(
            (layout_state.terminal_width, layout_state.terminal_height)
        )
        layout_state.terminal_width = max(56, int(size.columns))
        layout_state.terminal_height = max(20, int(size.lines))

    def _schedule_ui(callback: Callable[[], None]) -> None:
        app = app_ref[0]
        if app is None:
            callback()
            _invalidate_ui()
            return
        loop = getattr(app, "loop", None)
        if loop is None or loop.is_closed():
            callback()
            _invalidate_ui()
            return

        def _run_and_refresh() -> None:
            callback()
            _invalidate_ui()

        call_soon_threadsafe(_run_and_refresh, loop=loop)

    conversation_pane_holder: list = []

    def _auxiliary_line_count() -> int:
        fragments = _aux_fragments()
        if not fragments:
            return 0
        return max(1, sum(fragment.count("\n") for _, fragment in fragments))

    def _conversation_scroll_width() -> int:
        _refresh_terminal_geometry()
        width = layout_state.terminal_width
        if layout_state.sidebar_visible:
            width -= resolve_sidebar_pane_width(layout_state)
        return max(24, width - 2)

    def _scroll_conversation(delta: int) -> None:
        if not conversation_pane_holder:
            return
        scroll_conversation_by_lines(
            pane=conversation_pane_holder[0],
            conversation=conversation,
            delta=delta,
            terminal_height=layout_state.terminal_height,
            auxiliary_lines=_auxiliary_line_count(),
            width=_conversation_scroll_width(),
        )
        _invalidate_ui(sync_scroll=False)

    def _follow_conversation_end() -> None:
        conversation.scroll_to_end = True
        _sync_conversation_scroll()

    def _sync_conversation_scroll() -> None:
        if not conversation_pane_holder:
            return
        apply_conversation_scroll_policy(
            pane=conversation_pane_holder[0],
            conversation=conversation,
            terminal_height=layout_state.terminal_height,
            auxiliary_lines=_auxiliary_line_count(),
            width=_conversation_scroll_width(),
        )

    def _invalidate_ui(*, sync_scroll: bool = True) -> None:
        if sync_scroll:
            _sync_conversation_scroll()
        app = app_ref[0]
        if app is not None:
            app.invalidate()

    def _completion_hint(buffer) -> str:
        if buffer is None or not getattr(buffer, "complete_state", None):
            return ""
        hint = "  ↑↓ 选择  Enter 确认"
        completions = getattr(buffer.complete_state, "completions", None) or []
        remaining = max(0, len(completions) - 14)
        if remaining > 0:
            hint = f"{hint}  还有 {remaining} 个，继续输入筛选"
        return hint

    def _top_bar_fragments() -> list[tuple[str, str]]:
        _refresh_terminal_geometry()
        snapshot = load_sidebar_snapshot(terminal_dir=terminal_dir)
        from .terminal_theme import resolve_terminal_theme

        theme = resolve_terminal_theme(layout_state.theme_id)
        return format_top_bar_fragments(
            life_name=name,
            resident_status=load_resident_status(terminal_dir=terminal_dir),
            itr_flags=snapshot.itr_flags,
            width=layout_state.terminal_width,
            theme_label=theme.label,
        )

    def _sidebar_fragments() -> list[tuple[str, str]]:
        snapshot = load_sidebar_snapshot(terminal_dir=terminal_dir)
        return format_sidebar_pane_fragments(
            snapshot=snapshot,
            width=resolve_sidebar_pane_width(layout_state),
            collapsed=not layout_state.sidebar_visible,
        )

    def _aux_fragments() -> list[tuple[str, str]]:
        return format_auxiliary_fragments(
            active_text=str(getattr(input_buffer, "text", "") or ""),
            slash_commands=slash_commands,
            repo_root=repo_root,
            width=layout_state.terminal_width,
        )

    def _footer_fragments() -> list[tuple[str, str]]:
        pending = "  回合进行中…" if turn_inflight.is_set() else ""
        extra = ""
        if ui_state.overlay == "palette":
            extra = "  Ctrl+P面板"
        elif ui_state.overlay == "viewer":
            extra = "  块查看"
        elif ui_state.scrollback_focused:
            extra = "  j/k选块 h折叠 l展开 e切换 Enter全屏 Ctrl+O回输入"
        return format_footer_fragments(
            life_name=name,
            buffer=input_buffer,
            completion_hint=_completion_hint(input_buffer) + pending + extra,
        )

    def _conversation_fragments() -> list[tuple[str, str]]:
        if any(record.running for record in conversation.blocks):
            ui_state.animation_tick += 1
        return conversation.render_fragments(animation_tick=ui_state.animation_tick)

    def _tab_bar_fragments() -> list[tuple[str, str]]:
        _refresh_terminal_geometry()
        return format_session_tab_bar_fragments(
            terminal_dir=terminal_dir,
            width=layout_state.terminal_width,
        )

    def _welcome_fragments() -> list[tuple[str, str]]:
        _refresh_terminal_geometry()
        ui_state.welcome_animation_tick += 1
        return format_pixel_welcome_screen(
            terminal_dir=terminal_dir,
            life_name=name,
            selection=ui_state.welcome_selection,
            width=layout_state.terminal_width,
            height=layout_state.terminal_height,
            animation_tick=ui_state.welcome_animation_tick,
        )

    def _enter_from_welcome(*, force_new: bool = False) -> None:
        entries = build_welcome_entries(terminal_dir=terminal_dir, life_name=name)
        if not entries:
            entries = [("new", "新建会话")]
        if force_new:
            target_id = create_terminal_session_tab(
                terminal_dir=terminal_dir,
                life_name=name,
            )
        else:
            selected = max(0, min(ui_state.welcome_selection, len(entries) - 1))
            session_key, _label = entries[selected]
            if session_key == "new":
                target_id = create_terminal_session_tab(
                    terminal_dir=terminal_dir,
                    life_name=name,
                )
            else:
                target_id = session_key
        _reload_session_view(target_id)
        ui_state.enter_session()

    def _visible_palette_items():
        return resolve_palette_visible_items(
            palette_items,
            query=ui_state.palette_query,
        )

    palette_list_pane_holder: list = []

    def _sync_palette_list_scroll() -> None:
        if not palette_list_pane_holder:
            return
        apply_palette_list_scroll_policy(
            pane=palette_list_pane_holder[0],
            items=palette_items,
            query=ui_state.palette_query,
            selection=ui_state.palette_selection,
            visible_height=max(6, layout_state.terminal_height - 18),
        )

    def _palette_list_fragments() -> list[tuple[str, str]]:
        _refresh_terminal_geometry()
        return format_palette_list_fragments(
            items=palette_items,
            selection=ui_state.palette_selection,
            query=ui_state.palette_query,
            width=layout_state.terminal_width - 6,
        )

    def _palette_detail_fragments() -> list[tuple[str, str]]:
        _refresh_terminal_geometry()
        return format_palette_detail_fragments(
            items=palette_items,
            selection=ui_state.palette_selection,
            query=ui_state.palette_query,
            width=layout_state.terminal_width - 6,
        )

    def _viewer_fragments() -> list[tuple[str, str]]:
        _refresh_terminal_geometry()
        block_id = str(ui_state.viewer_block_id or "")
        if not block_id:
            return [("class:hint", " 无选中块\n")]
        return conversation.viewer_fragments(
            block_id,
            animation_tick=ui_state.animation_tick,
        )



    def _append_message(
        *,
        event_kind: str,
        speaker: str,
        text: str,
        active_session_id: str | None = None,
    ) -> None:
        active_id = active_session_id or session_id
        release_badge = resolve_release_badge(
            terminal_dir=terminal_dir,
            speaker=speaker,
            text=text,
        )
        append_terminal_session_event(
            terminal_dir=terminal_dir,
            session_id=active_id,
            event_kind=event_kind,
            speaker=speaker,
            text=text,
            life_name=name,
            metadata={"release_badge": release_badge} if release_badge else None,
        )
        conversation.append_message(
            MessageRenderSpec(
                speaker=speaker,
                text=text,
                life_name=name,
                release_badge=release_badge,
                event_kind=event_kind,
            )
        )

    def _persist_response_event(
        *,
        event_kind: str,
        speaker: str,
        text: str,
        release_badge: str | None = None,
    ) -> None:
        append_terminal_session_event(
            terminal_dir=terminal_dir,
            session_id=session_id,
            event_kind=event_kind,
            speaker=speaker,
            text=text,
            life_name=name,
            metadata={"release_badge": release_badge} if release_badge else None,
        )

    def _simulate_streaming_response(
        *,
        response: str,
        is_command: bool,
    ) -> None:
        text = str(response or "")
        if not text:
            return
        conversation.scroll_to_end = True

        def _stream_worker() -> None:
            spec = resolve_streaming_life_spec(
                terminal_dir=terminal_dir,
                life_name=name,
                text="",
                speaker="command_result" if is_command else "life",
                event_kind="command_result" if is_command else "life_response",
            )

            def _start_stream() -> None:
                conversation.start_stream_message(spec)

            _schedule_ui(_start_stream)
            chunk_size = 2 if len(text) < 240 else 3
            delay_seconds = 0.018
            for index in range(0, len(text), chunk_size):
                chunk = text[index : index + chunk_size]
                time.sleep(delay_seconds)

                def _apply_chunk(value: str = chunk) -> None:
                    conversation.append_stream_delta(value)
                    _sync_conversation_scroll()

                _schedule_ui(_apply_chunk)

            final_spec = resolve_streaming_life_spec(
                terminal_dir=terminal_dir,
                life_name=name,
                text=text,
                speaker=spec.speaker,
                event_kind=spec.event_kind,
            )

            def _finalize() -> None:
                conversation.finalize_stream_message(final_spec)
                _persist_response_event(
                    event_kind=final_spec.event_kind,
                    speaker=final_spec.speaker,
                    text=text,
                    release_badge=final_spec.release_badge,
                )
                _sync_conversation_scroll()

            _schedule_ui(_finalize)

        threading.Thread(target=_stream_worker, daemon=True).start()

    def _finish_turn(
        *,
        stripped: str,
        is_command: bool,
        exit_code: int | None,
        response: str,
        saw_live_stream: bool,
    ) -> None:
        turn_inflight.clear()
        if response:
            if saw_live_stream:
                final_spec = resolve_streaming_life_spec(
                    terminal_dir=terminal_dir,
                    life_name=name,
                    text=response,
                    speaker="command_result" if is_command else "life",
                    event_kind="command_result" if is_command else "life_response",
                )
                conversation.finalize_stream_message(final_spec)
                _persist_response_event(
                    event_kind=final_spec.event_kind,
                    speaker=final_spec.speaker,
                    text=response,
                    release_badge=final_spec.release_badge,
                )
            else:
                _simulate_streaming_response(
                    response=response,
                    is_command=is_command,
                )
        else:
            conversation.clear_typing()
            conversation.clear_stream()
        if exit_code is not None:
            exit_code_holder[0] = exit_code
            stop_idle_thread.set()
            app = app_ref[0]
            if app is not None:
                app.exit()
        _invalidate_ui()

    def _run_turn_async(stripped: str, *, is_command: bool) -> None:
        if turn_inflight.is_set():
            return
        turn_inflight.set()
        stream_started["value"] = False

        def on_start() -> None:
            _schedule_ui(lambda: conversation.show_typing(life_name=name))

        def on_delta(chunk: str) -> None:
            if not chunk:
                return

            def apply_delta() -> None:
                if not stream_started["value"]:
                    stream_started["value"] = True
                    conversation.start_stream_message(
                        resolve_streaming_life_spec(
                            terminal_dir=terminal_dir,
                            life_name=name,
                            text="",
                        )
                    )
                conversation.append_stream_delta(chunk)
                _sync_conversation_scroll()

            _schedule_ui(apply_delta)

        def worker() -> None:
            try:
                with stream_session(on_start=on_start, on_delta=on_delta):
                    exit_code, response = handle_utterance(stripped)
            except Exception as exc:
                exit_code = 1
                response = f"回合失败: {exc}"
            saw_live = stream_started["value"]
            _schedule_ui(
                lambda: _finish_turn(
                    stripped=stripped,
                    is_command=is_command,
                    exit_code=exit_code,
                    response=str(response or ""),
                    saw_live_stream=saw_live,
                )
            )

        threading.Thread(target=worker, daemon=True).start()
        _invalidate_ui()

    def _process_utterance(text: str) -> None:
        stripped = str(text or "").strip()
        idle_policy.mark_activity(active_text=stripped)
        if not stripped:
            if idle_voice_fn and not turn_inflight.is_set():
                voice = idle_voice_fn()
                if voice:
                    _append_message(
                        event_kind="proactive_voice",
                        speaker="proactive",
                        text=voice,
                    )
                    _invalidate_ui()
            return
        is_command = stripped.lstrip().startswith("/")
        conversation.scroll_to_end = True
        _append_message(
            event_kind="command" if is_command else "relation_utterance",
            speaker="command" if is_command else "relation",
            text=stripped,
        )
        _invalidate_ui()
        _run_turn_async(stripped, is_command=is_command)

    def _reload_session_view(target_session_id: str) -> None:
        nonlocal session_id
        session_id = switch_terminal_session(
            terminal_dir=terminal_dir,
            session_id=target_session_id,
        )
        conversation.load_session(
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=name,
            width=layout_state.terminal_width,
        )
        _invalidate_ui()

    def _execute_palette_selection() -> None:
        visible = _visible_palette_items()
        if not visible:
            ui_state.close_overlay()
            _invalidate_ui()
            return
        item = visible[ui_state.palette_selection % len(visible)]
        kind, payload = resolve_palette_action(item)
        ui_state.close_overlay()
        if kind == "slash":
            input_buffer.text = payload
            _process_utterance(payload)
        _invalidate_ui()

    def _accept_input(buffer: Buffer) -> bool:
        if turn_inflight.is_set():
            return True
        text = str(buffer.text or "")
        buffer.reset(append_to_history=bool(text.strip()))
        _process_utterance(text)
        return True

    input_buffer = Buffer(
        completer=completer,
        complete_while_typing=True,
        history=history,
        accept_handler=_accept_input,
        multiline=False,
        read_only=Condition(
            lambda: turn_inflight.is_set() or ui_state.screen == "welcome"
        ),
    )

    def _on_palette_buffer_changed(_buffer: Buffer) -> None:
        ui_state.palette_query = str(_buffer.text or "")
        ui_state.palette_selection = 0
        _sync_palette_list_scroll()
        _invalidate_ui()

    palette_buffer = Buffer(
        multiline=False,
        on_text_changed=_on_palette_buffer_changed,
    )

    palette_open = Condition(lambda: ui_state.overlay == "palette")
    viewer_open = Condition(lambda: ui_state.overlay == "viewer")
    scrollback_mode = Condition(
        lambda: ui_state.overlay == "none" and ui_state.scrollback_focused
    )
    sidebar_visible = Condition(lambda: layout_state.sidebar_visible)
    auxiliary_visible = Condition(lambda: bool(_aux_fragments()))

    conversation_pane = ScrollablePane(
        Window(
            _ScrollableConversationControl(
                text_func=lambda: FormattedText(_conversation_fragments()),
                on_scroll=_scroll_conversation,
            ),
            wrap_lines=True,
        ),
        height=Dimension(weight=1),
        show_scrollbar=True,
        display_arrows=False,
        keep_cursor_visible=False,
        keep_focused_window_visible=False,
    )
    conversation_pane_holder.append(conversation_pane)

    input_separator = Window(
        FormattedTextControl(
            lambda: FormattedText(
                [("class:input-separator", " " + "─" * max(10, layout_state.terminal_width - 2))]
            )
        ),
        height=Dimension.exact(1),
        dont_extend_height=True,
    )

    input_window = Window(
        BufferControl(
            buffer=input_buffer,
            focusable=True,
            input_processors=[],
        ),
        height=Dimension.exact(1),
        style="class:input-composer",
        get_line_prefix=lambda _line_number, _wrap_count: [
            ("class:input-box", "  "),
            ("class:speaker", "› "),
        ],
    )

    palette_input_window = Window(
        BufferControl(buffer=palette_buffer, focusable=True),
        height=Dimension.exact(1),
        style="class:palette-search",
        get_line_prefix=lambda _line_number, _wrap_count: [
            ("class:palette-title", " 搜索 › "),
        ],
    )

    palette_list_window = Window(
        FormattedTextControl(
            lambda: FormattedText(_palette_list_fragments())
        ),
        wrap_lines=False,
        height=Dimension(weight=1),
        style="class:overlay-panel",
        always_hide_cursor=True,
        right_margins=[ScrollbarMargin(display_arrows=False)],
        scroll_offsets=ScrollOffsets(top=0, bottom=0),
    )
    palette_list_pane_holder.append(palette_list_window)

    palette_panel = HSplit(
        [
            Window(
                FormattedTextControl(
                    lambda: FormattedText([("class:palette-title", " 命令面板\n")])
                ),
                height=Dimension.exact(1),
                dont_extend_height=True,
                style="class:overlay-panel",
            ),
            palette_input_window,
            palette_list_window,
            Window(
                FormattedTextControl(
                    lambda: FormattedText(_palette_detail_fragments())
                ),
                height=Dimension.exact(5),
                wrap_lines=True,
                dont_extend_height=True,
                style="class:overlay-panel",
            ),
            Window(
                FormattedTextControl(
                    lambda: FormattedText(format_palette_footer_fragments())
                ),
                height=Dimension.exact(1),
                dont_extend_height=True,
                style="class:overlay-panel",
            ),
        ],
        style="class:overlay-panel",
    )

    welcome_window = Window(
        FormattedTextControl(lambda: FormattedText(_welcome_fragments())),
        wrap_lines=False,
        style="class:welcome-screen",
    )

    session_container = HSplit(
        [
            Window(
                FormattedTextControl(lambda: FormattedText(_top_bar_fragments())),
                height=Dimension.exact(2),
                dont_extend_height=True,
            ),
            Window(
                FormattedTextControl(lambda: FormattedText(_tab_bar_fragments())),
                height=Dimension.exact(1),
                dont_extend_height=True,
            ),
            VSplit(
                [
                    conversation_pane,
                    ConditionalContainer(
                        Window(
                            FormattedTextControl(
                                lambda: FormattedText(_sidebar_fragments())
                            ),
                            width=Dimension.exact(resolve_sidebar_pane_width(layout_state)),
                            wrap_lines=True,
                        ),
                        filter=sidebar_visible,
                    ),
                ],
                height=Dimension(weight=1),
            ),
            ConditionalContainer(
                Window(
                    FormattedTextControl(lambda: FormattedText(_aux_fragments())),
                    height=Dimension(max=14),
                    wrap_lines=True,
                    dont_extend_height=True,
                    style="class:overlay-panel",
                ),
                filter=auxiliary_visible,
            ),
            input_separator,
            input_window,
            Window(
                FormattedTextControl(lambda: FormattedText(_footer_fragments())),
                height=Dimension.exact(1),
                dont_extend_height=True,
            ),
            CompletionsMenu(max_height=14),
        ]
    )

    session_with_overlays = FloatContainer(
        content=session_container,
        floats=[
            Float(
                ConditionalContainer(
                    welcome_window,
                    filter=Condition(lambda: ui_state.screen == "welcome"),
                ),
                top=0,
                left=0,
                right=0,
                bottom=0,
            ),
            Float(
                ConditionalContainer(
                    Window(style="class:overlay-backdrop"),
                    filter=palette_open,
                ),
                top=0,
                left=0,
                right=0,
                bottom=0,
                z_index=5,
            ),
            Float(
                ConditionalContainer(
                    palette_panel,
                    filter=palette_open,
                ),
                top=1,
                left=2,
                right=2,
                bottom=3,
                z_index=6,
            ),
            Float(
                ConditionalContainer(
                    Window(
                        FormattedTextControl(
                            lambda: FormattedText(_viewer_fragments())
                        ),
                        wrap_lines=True,
                        style="class:overlay-panel",
                    ),
                    filter=viewer_open,
                ),
                top=2,
                left=2,
                right=2,
                bottom=2,
            ),
        ],
    )

    root_container = session_with_overlays

    overlay_open = Condition(lambda: ui_state.overlay != "none")
    input_mode = Condition(
        lambda: ui_state.screen == "session"
        and ui_state.overlay == "none"
        and not ui_state.scrollback_focused
    )
    session_scroll_mode = Condition(
        lambda: ui_state.screen == "session" and ui_state.overlay == "none"
    )
    conversation_scroll_mode = Condition(
        lambda: ui_state.screen == "session"
        and ui_state.overlay == "none"
        and not ui_state.scrollback_focused
    )
    welcome_mode = Condition(lambda: ui_state.screen == "welcome")

    bindings = KeyBindings()

    @bindings.add("c-q")
    def _(event):
        stop_idle_thread.set()
        event.app.exit(exception=EOFError)

    @bindings.add("enter", filter=welcome_mode, eager=True)
    def _(event):
        _enter_from_welcome()
        event.app.layout.focus(input_window)
        event.app.invalidate()

    @bindings.add("escape", filter=welcome_mode)
    def _(event):
        _enter_from_welcome()
        event.app.layout.focus(input_window)
        event.app.invalidate()

    @bindings.add("up", filter=welcome_mode)
    def _(event):
        entries = build_welcome_entries(terminal_dir=terminal_dir, life_name=name)
        if entries:
            ui_state.welcome_selection = (ui_state.welcome_selection - 1) % len(entries)
        event.app.invalidate()

    @bindings.add("down", filter=welcome_mode)
    def _(event):
        entries = build_welcome_entries(terminal_dir=terminal_dir, life_name=name)
        if entries:
            ui_state.welcome_selection = (ui_state.welcome_selection + 1) % len(entries)
        event.app.invalidate()

    @bindings.add("c-n", filter=welcome_mode)
    def _(event):
        _enter_from_welcome(force_new=True)
        event.app.layout.focus(input_window)
        event.app.invalidate()

    @bindings.add("c-s", filter=welcome_mode)
    def _(event):
        _enter_from_welcome()
        event.app.layout.focus(input_window)
        event.app.invalidate()

    @bindings.add("c-p")
    def _(event):
        ui_state.open_palette()
        palette_buffer.text = ""
        _sync_palette_list_scroll()
        event.app.layout.focus(palette_input_window)
        event.app.invalidate()

    @bindings.add("c-b")
    def _(event):
        layout_state.sidebar_visible = not layout_state.sidebar_visible
        event.app.invalidate()

    @bindings.add("c-t")
    def _(event):
        new_session = create_terminal_session_tab(
            terminal_dir=terminal_dir,
            life_name=name,
        )
        _reload_session_view(new_session)

    @bindings.add("c-]")
    def _(event):
        target = cycle_terminal_session_tab(
            terminal_dir=terminal_dir,
            direction="next",
        )
        if target:
            _reload_session_view(target)

    @bindings.add("s-tab")
    def _(event):
        target = cycle_terminal_session_tab(
            terminal_dir=terminal_dir,
            direction="prev",
        )
        if target:
            _reload_session_view(target)

    for digit in range(1, 10):

        @bindings.add(f"c-{digit}")
        def _(event, tab_index=digit):
            tabs = list_terminal_session_tabs(terminal_dir=terminal_dir, limit=9)
            if tab_index - 1 < len(tabs):
                _reload_session_view(tabs[tab_index - 1].session_id)

    @bindings.add("c-y")
    def _(event):
        layout_state.theme_id = cycle_terminal_theme(layout_state.theme_id)
        event.app.style = build_terminal_style(layout_state.theme_id)
        event.app.invalidate()

    @bindings.add("escape", filter=overlay_open)
    def _(event):
        ui_state.close_overlay()
        event.app.layout.focus(input_window)
        event.app.invalidate()

    @bindings.add("escape", filter=scrollback_mode)
    def _(event):
        ui_state.scrollback_focused = False
        event.app.layout.focus(input_window)
        event.app.invalidate()

    @bindings.add("escape", "enter", filter=input_mode)
    def _(event):
        event.current_buffer.insert_text("\n")

    @bindings.add("c-o", filter=~overlay_open)
    def _(event):
        ui_state.scrollback_focused = not ui_state.scrollback_focused
        if ui_state.scrollback_focused:
            if conversation.selected_index is None and conversation.blocks:
                conversation.select_block(len(conversation.blocks) - 1)
            event.app.layout.focus(conversation_pane)
        else:
            event.app.layout.focus(input_window)
        event.app.invalidate()

    @bindings.add("j", filter=scrollback_mode)
    def _(event):
        conversation.move_selection(1)
        event.app.invalidate()

    @bindings.add("k", filter=scrollback_mode)
    def _(event):
        conversation.move_selection(-1)
        event.app.invalidate()

    @bindings.add("h", filter=scrollback_mode)
    def _(event):
        conversation.collapse_selected()
        event.app.invalidate()

    @bindings.add("l", filter=scrollback_mode)
    def _(event):
        conversation.expand_selected()
        event.app.invalidate()

    @bindings.add("e", filter=scrollback_mode)
    def _(event):
        conversation.toggle_selected_fold()
        event.app.invalidate()

    @bindings.add("enter", filter=scrollback_mode, eager=True)
    def _(event):
        block_id = conversation.selected_block_id()
        if block_id:
            ui_state.open_viewer(block_id)
            event.app.invalidate()

    @bindings.add("down", filter=palette_open)
    def _(event):
        visible = _visible_palette_items()
        if visible:
            ui_state.palette_selection = (ui_state.palette_selection + 1) % len(visible)
            _sync_palette_list_scroll()
        event.app.invalidate()

    @bindings.add("up", filter=palette_open)
    def _(event):
        visible = _visible_palette_items()
        if visible:
            ui_state.palette_selection = (ui_state.palette_selection - 1) % len(visible)
            _sync_palette_list_scroll()
        event.app.invalidate()

    @bindings.add("enter", filter=palette_open, eager=True)
    def _(event):
        _execute_palette_selection()
        event.app.layout.focus(input_window)

    @bindings.add("down", filter=input_mode)
    def _(event):
        if not _move_completion_selection_or_history(
            event.current_buffer,
            direction="down",
            completer=completer,
        ):
            event.current_buffer.auto_down()

    @bindings.add("up", filter=input_mode)
    def _(event):
        if not _move_completion_selection_or_history(
            event.current_buffer,
            direction="up",
            completer=completer,
        ):
            event.current_buffer.auto_up()

    @bindings.add("enter", filter=input_mode, eager=True)
    def _(event):
        _confirm_selected_completion_or_submit(event.current_buffer)

    def _bind_conversation_scroll(keys: str, *, delta: int) -> None:
        @bindings.add(keys, filter=session_scroll_mode, eager=True)
        def _(event):
            if ui_state.scrollback_focused:
                return
            _scroll_conversation(delta)

    # Mac-first: trackpad/wheel, then Control+Arrow while typing.
    _bind_conversation_scroll(Keys.ScrollUp, delta=-3)
    _bind_conversation_scroll(Keys.ScrollDown, delta=3)
    _bind_conversation_scroll(Keys.ControlUp, delta=-3)
    _bind_conversation_scroll(Keys.ControlDown, delta=3)
    _bind_conversation_scroll(Keys.ControlShiftUp, delta=-12)
    _bind_conversation_scroll(Keys.ControlShiftDown, delta=12)

    @bindings.add("c-g", filter=session_scroll_mode, eager=True)
    def _(event):
        if ui_state.scrollback_focused:
            return
        _follow_conversation_end()
        event.app.invalidate()

    def _idle_voice_loop() -> None:
        while not stop_idle_thread.wait(1.0):
            if idle_voice_fn is None or turn_inflight.is_set():
                continue
            try:
                active_text = str(input_buffer.text or "")
            except Exception:
                active_text = ""
            if not idle_policy.should_release(active_text=active_text):
                continue
            voice = idle_voice_fn()
            if not voice:
                continue
            _schedule_ui(
                lambda: _append_message(
                    event_kind="proactive_voice",
                    speaker="proactive",
                    text=voice,
                )
            )
            _invalidate_ui()

    if idle_voice_fn is not None:
        threading.Thread(target=_idle_voice_loop, daemon=True).start()

    app = Application(
        layout=Layout(root_container, focused_element=input_window),
        key_bindings=bindings,
        style=build_terminal_style(layout_state.theme_id),
        full_screen=True,
        mouse_support=True,
        refresh_interval=0.08,
        cursor=CursorShape.BLINKING_BEAM,
    )
    app_ref[0] = app
    _sync_conversation_scroll()

    try:
        app.run()
    except (EOFError, KeyboardInterrupt):
        stop_idle_thread.set()
        return 0
    finally:
        stop_idle_thread.set()

    return int(exit_code_holder[0] or 0)


def split_terminal_experience_profile() -> dict[str, object]:
    return {
        "terminal_framework": "prompt_toolkit",
        "layout_profile": "product_split_pane_v4_grok_visual",
        "mouse_support": True,
        "scrollback_policy": "in_app_conversation_pane_mac_trackpad_and_ctrl_arrows",
        "session_replay_line_limit": 400,
        "enable_history_search": True,
        "show_frame": True,
        "complete_style": "COLUMN",
        "reserve_space_for_menu": 14,
        "cursor_shape": "BLINKING_BEAM",
        "input_box": "split_pane_bottom_composer",
        "conversation_pane": "scrollable_left_column",
        "sidebar_pane": "fixed_right_column_ctrl_b",
        "top_bar": "fixed_header_row",
        "session_tabs": "visible_tab_bar_row_ctrl_t_ctrl_bracket_ctrl_1_9",
        "sidebar_toggle": "ctrl_b",
        "theme_cycle": "ctrl_y",
        "slash_panel": "inline_on_empty_slash_query",
        "file_reference_preview": "inline_on_at_reference",
        "message_blocks": "timestamp_speaker_badge_body",
        "session_resume": "startup_carry_and_transcript",
        "welcome_screen": "pixel_birth_crt_animation_overlay",
        "markdown_rendering": "headings_lists_links_code_fences",
        "block_visual": "grok_style_accent_blocks_foldable",
        "streaming_output": "live_sse_with_simulated_fallback",
        "async_turns": "background_worker_with_typing_indicator",
        "resize_policy": "geometry_refresh_on_render",
        "command_palette": "ctrl_p_search_list_detail_overlay",
        "block_fold": "h_collapse_l_expand_e_toggle",
        "block_viewer": "enter_fullscreen_esc_close",
        "scrollback_focus": "ctrl_o_j_k_block_nav",
        "truecolor_themes": "groknight_grokday_tokyonight_rosepine_oscura",
        "overlay_container": "float_palette_and_viewer",
    }