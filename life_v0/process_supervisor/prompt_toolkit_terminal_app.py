from __future__ import annotations

import shutil
import time
import threading
from pathlib import Path
from typing import Callable

from .terminal_input import TerminalCompletionState, build_terminal_completion_state
from .terminal_layout import (
    MessageRenderSpec,
    TerminalLayoutState,
    format_layout_toolbar_fragments,
    format_message_fragments,
    render_resume_startup_fragments,
    render_session_history_fragments,
    resolve_release_badge,
    resolve_terminal_layout_state,
)
from .terminal_session_transcript import (
    append_terminal_session_event,
    start_terminal_session_transcript,
)


def prompt_toolkit_available() -> bool:
    try:
        import prompt_toolkit  # noqa: F401
    except ImportError:
        return False
    return True


def run_prompt_toolkit_terminal_app(
    *,
    terminal_dir: Path,
    life_name: str | None,
    handle_utterance: Callable[[str], tuple[int | None, str]],
    slash_commands: tuple[tuple[str, str], ...],
    idle_voice_fn: Callable[[], str | None] | None = None,
    repo_root: Path | None = None,
    idle_voice_interval_seconds: float = 90.0,
) -> int:
    from .prompt_toolkit_split_terminal_app import run_prompt_toolkit_split_terminal_app

    return run_prompt_toolkit_split_terminal_app(
        terminal_dir=terminal_dir,
        life_name=life_name,
        handle_utterance=handle_utterance,
        slash_commands=slash_commands,
        idle_voice_fn=idle_voice_fn,
        repo_root=repo_root,
        idle_voice_interval_seconds=idle_voice_interval_seconds,
    )


def run_prompt_toolkit_legacy_terminal_app(
    *,
    terminal_dir: Path,
    life_name: str | None,
    handle_utterance: Callable[[str], tuple[int | None, str]],
    slash_commands: tuple[tuple[str, str], ...],
    idle_voice_fn: Callable[[], str | None] | None = None,
    repo_root: Path | None = None,
    idle_voice_interval_seconds: float = 90.0,
) -> int:
    from prompt_toolkit import PromptSession, print_formatted_text
    from prompt_toolkit.cursor_shapes import CursorShape
    from prompt_toolkit.formatted_text import FormattedText, HTML
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.patch_stdout import patch_stdout
    from prompt_toolkit.shortcuts import clear
    from prompt_toolkit.shortcuts.prompt import CompleteStyle
    from prompt_toolkit.styles import Style

    name = life_name or "Digital Life"
    opened_session = start_terminal_session_transcript(
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
    bindings = KeyBindings()
    idle_policy = TerminalIdleVoicePolicy(
        interval_seconds=idle_voice_interval_seconds,
    )
    stop_idle_thread = threading.Event()

    @bindings.add("c-q")
    def _(event):
        event.app.exit(exception=EOFError, style="class:aborting")

    @bindings.add("c-b")
    def _(event):
        layout_state.sidebar_visible = not layout_state.sidebar_visible
        event.app.invalidate()

    @bindings.add("escape", "enter")
    def _(event):
        event.current_buffer.insert_text("\n")

    @bindings.add("down")
    def _(event):
        if not _move_completion_selection_or_history(
            event.current_buffer,
            direction="down",
            completer=completer,
        ):
            event.current_buffer.auto_down()

    @bindings.add("up")
    def _(event):
        if not _move_completion_selection_or_history(
            event.current_buffer,
            direction="up",
            completer=completer,
        ):
            event.current_buffer.auto_up()

    @bindings.add("enter", eager=True)
    def _(event):
        _confirm_selected_completion_or_submit(event.current_buffer)

    style = Style.from_dict(
        {
            "status": "ansicyan",
            "hint": "ansibrightblack",
            "speaker": "ansigreen bold",
            "relation": "ansiwhite",
            "input": "ansiblue",
            "error": "ansired",
            "input-box": "ansibrightblack",
            "cursor-index": "ansiyellow",
            "top-bar": "ansibrightblack",
            "sidebar": "ansimagenta",
            "sidebar-title": "ansimagenta bold",
            "timestamp": "ansibrightblack",
            "message-body": "ansiwhite",
            "badge": "ansibrightblack",
            "badge-released": "ansigreen",
            "badge-unreleased": "ansired",
            "slash-panel-title": "ansicyan bold",
            "slash-panel-group": "ansicyan",
            "slash-panel-item": "ansibrightblack",
            "file-preview": "ansiyellow",
            "resume-title": "ansicyan bold",
            "resume-section": "ansicyan",
            "resume-line": "ansibrightblack",
            "resume-carry": "ansigreen",
        }
    )
    session = PromptSession(
        history=history,
        completer=completer,
        complete_while_typing=True,
        complete_style=CompleteStyle.COLUMN,
        reserve_space_for_menu=14,
        enable_history_search=True,
        key_bindings=bindings,
        multiline=False,
        bottom_toolbar=lambda: _bottom_toolbar(
            terminal_dir=terminal_dir,
            life_name=name,
            layout_state=layout_state,
            slash_commands=slash_commands,
            repo_root=repo_root,
        ),
        mouse_support=False,
        cursor=CursorShape.BLINKING_BEAM,
        show_frame=True,
        placeholder=HTML(
            "<ansibrightblack>输入对话，/ 命令面板，@ 引用文件，Ctrl-B 侧栏</ansibrightblack>"
        ),
        style=style,
    )
    clear()
    _print_startup_layout(
        terminal_dir=terminal_dir,
        life_name=name,
        layout_state=layout_state,
        print_formatted_text=print_formatted_text,
    )
    with patch_stdout(raw=True):
        idle_thread = None
        if idle_voice_fn is not None:
            idle_thread = threading.Thread(
                target=_idle_voice_loop,
                kwargs={
                    "stop_event": stop_idle_thread,
                    "idle_policy": idle_policy,
                    "terminal_dir": terminal_dir,
                    "session_id": session_id,
                    "life_name": name,
                    "idle_voice_fn": idle_voice_fn,
                    "print_formatted_text": print_formatted_text,
                    "get_active_text": lambda: session.default_buffer.text,
                },
                daemon=True,
            )
            idle_thread.start()
        while True:
            try:
                layout_state.terminal_width = max(
                    56,
                    min(112, shutil.get_terminal_size((layout_state.terminal_width, 28)).columns),
                )
                utterance = session.prompt(
                    _prompt_prefix(name),
                    refresh_interval=0.5,
                )
            except (EOFError, KeyboardInterrupt):
                stop_idle_thread.set()
                print_formatted_text(HTML("<ansibrightblack>terminal detached</ansibrightblack>"))
                return 0
            text = str(utterance or "").strip()
            idle_policy.mark_activity(active_text=text)
            if not text:
                if idle_voice_fn:
                    voice = idle_voice_fn()
                    if voice:
                        _append_and_print(
                            terminal_dir=terminal_dir,
                            session_id=session_id,
                            event_kind="proactive_voice",
                            speaker="proactive",
                            text=voice,
                            life_name=name,
                            print_formatted_text=print_formatted_text,
                        )
                continue
            is_command = text.lstrip().startswith("/")
            _append_and_print(
                terminal_dir=terminal_dir,
                session_id=session_id,
                event_kind="command" if is_command else "relation_utterance",
                speaker="command" if is_command else "relation",
                text=text,
                life_name=name,
                print_formatted_text=print_formatted_text,
            )
            exit_code, response = handle_utterance(text)
            if response:
                _append_and_print(
                    terminal_dir=terminal_dir,
                    session_id=session_id,
                    event_kind="command_result" if is_command else "life_response",
                    speaker="command_result" if is_command else "life",
                    text=response,
                    life_name=name,
                    print_formatted_text=print_formatted_text,
                )
            if exit_code is not None:
                stop_idle_thread.set()
                return exit_code


class TerminalIdleVoicePolicy:
    def __init__(
        self,
        *,
        interval_seconds: float = 90.0,
        now_fn: Callable[[], float] | None = None,
    ) -> None:
        self.interval_seconds = max(5.0, float(interval_seconds))
        self.now_fn = now_fn or time.monotonic
        now = self.now_fn()
        self.last_activity_at = now
        self.last_voice_at = now

    def mark_activity(self, *, active_text: str = "") -> None:
        self.last_activity_at = self.now_fn()
        if str(active_text or "").strip():
            self.last_voice_at = self.last_activity_at

    def should_release(self, *, active_text: str = "") -> bool:
        if str(active_text or "").strip():
            self.mark_activity(active_text=active_text)
            return False
        now = self.now_fn()
        idle_for = now - self.last_activity_at
        since_voice = now - self.last_voice_at
        if idle_for < self.interval_seconds or since_voice < self.interval_seconds:
            return False
        self.last_voice_at = now
        return True


def _maybe_emit_idle_voice(
    *,
    idle_policy: TerminalIdleVoicePolicy,
    terminal_dir: Path,
    session_id: str,
    life_name: str,
    idle_voice_fn: Callable[[], str | None] | None,
    print_formatted_text,
    active_text: str,
) -> None:
    if idle_voice_fn is None:
        return
    if not idle_policy.should_release(active_text=active_text):
        return
    voice = idle_voice_fn()
    if not voice:
        return
    _append_and_print(
        terminal_dir=terminal_dir,
        session_id=session_id,
        event_kind="proactive_voice",
        speaker="proactive",
        text=voice,
        life_name=life_name,
        print_formatted_text=print_formatted_text,
    )


def _idle_voice_loop(
    *,
    stop_event,
    idle_policy: TerminalIdleVoicePolicy,
    terminal_dir: Path,
    session_id: str,
    life_name: str,
    idle_voice_fn: Callable[[], str | None],
    print_formatted_text,
    get_active_text: Callable[[], str],
) -> None:
    while not stop_event.wait(1.0):
        try:
            active_text = get_active_text()
        except Exception:
            active_text = ""
        _maybe_emit_idle_voice(
            idle_policy=idle_policy,
            terminal_dir=terminal_dir,
            session_id=session_id,
            life_name=life_name,
            idle_voice_fn=idle_voice_fn,
            print_formatted_text=print_formatted_text,
            active_text=active_text,
        )


class _TerminalCompleter:
    def __init__(
        self,
        *,
        slash_commands: tuple[tuple[str, str], ...],
        repo_root: Path,
    ) -> None:
        self.slash_commands = slash_commands
        self.repo_root = repo_root

    def get_completions(self, document, complete_event):
        from prompt_toolkit.completion import Completion

        del complete_event
        completion = build_terminal_completion_state(
            document.text,
            cursor_index=document.cursor_position,
            slash_commands=self.slash_commands,
            repo_root=self.repo_root,
            limit=200,
        )
        if not isinstance(completion, TerminalCompletionState):
            return
        for item in completion.items:
            replacement = item.label if completion.trigger == "/" else "@" + item.label
            display_meta = _completion_display_meta(item)
            yield Completion(
                replacement,
                start_position=completion.start_index - document.cursor_position,
                display=item.label,
                display_meta=display_meta,
            )

    async def get_completions_async(self, document, complete_event):
        for completion in self.get_completions(document, complete_event):
            yield completion


def _move_completion_selection_or_history(buffer, *, direction: str, completer=None) -> bool:
    if not getattr(buffer, "complete_state", None) and completer is not None:
        _open_completion_state_synchronously(buffer, completer=completer)
    if not getattr(buffer, "complete_state", None):
        return False
    if direction == "up":
        buffer.complete_previous()
        return True
    if direction == "down":
        buffer.complete_next()
        return True
    return False


def _confirm_selected_completion_or_submit(buffer) -> bool:
    complete_state = getattr(buffer, "complete_state", None)
    if complete_state:
        completion = getattr(complete_state, "current_completion", None)
        if completion is None and getattr(complete_state, "completions", None):
            buffer.complete_next(disable_wrap_around=True)
            complete_state = getattr(buffer, "complete_state", None)
            completion = getattr(complete_state, "current_completion", None)
        if completion is not None:
            buffer.apply_completion(completion)
            return True
    buffer.validate_and_handle()
    return False


def _open_completion_state_synchronously(buffer, *, completer) -> bool:
    from prompt_toolkit.buffer import CompletionState

    completions = list(completer.get_completions(buffer.document, complete_event=None))
    if not completions:
        return False
    buffer.complete_state = CompletionState(
        buffer.document,
        completions=completions,
    )
    return True


def _session_experience_profile() -> dict[str, object]:
    from .prompt_toolkit_split_terminal_app import split_terminal_experience_profile

    return split_terminal_experience_profile()


def _completion_display_meta(item) -> str:
    group = str(getattr(item, "group", "") or "").strip()
    detail = str(getattr(item, "detail", "") or "").strip()
    if group and detail:
        return f"{group}｜{detail}"
    return detail or group


def _prompt_prefix(life_name: str):
    fragments = [
        ("class:input-box", "╭─ "),
        ("class:speaker", life_name),
        ("class:input-box", "\n╰─› "),
    ]
    try:
        from prompt_toolkit.formatted_text import FormattedText

        return FormattedText(fragments)
    except ImportError:
        return fragments


def _format_right_prompt(*, buffer=None):
    cursor_index = 0
    text_length = 0
    if buffer is not None:
        cursor_index = int(getattr(buffer, "cursor_position", 0) or 0)
        text_length = len(str(getattr(buffer, "text", "") or ""))
    return _as_formatted_text(
        [
            ("class:cursor-index", f" pos {cursor_index}/{text_length} "),
        ]
    )


def _print_startup_layout(
    *,
    terminal_dir: Path,
    life_name: str,
    layout_state: TerminalLayoutState,
    print_formatted_text,
) -> None:
    from prompt_toolkit.formatted_text import FormattedText

    print_formatted_text(
        FormattedText(
            render_resume_startup_fragments(
                terminal_dir=terminal_dir,
                life_name=life_name,
                width=layout_state.terminal_width,
            )
        )
    )
    print_formatted_text("")
    print_formatted_text(
        FormattedText(
            render_session_history_fragments(
                terminal_dir=terminal_dir,
                life_name=life_name,
                width=layout_state.terminal_width,
            )
        )
    )


def _append_and_print(
    *,
    terminal_dir: Path,
    session_id: str,
    event_kind: str,
    speaker: str,
    text: str,
    life_name: str,
    print_formatted_text,
) -> None:
    from prompt_toolkit.formatted_text import FormattedText

    release_badge = resolve_release_badge(
        terminal_dir=terminal_dir,
        speaker=speaker,
        text=text,
    )
    append_terminal_session_event(
        terminal_dir=terminal_dir,
        session_id=session_id,
        event_kind=event_kind,
        speaker=speaker,
        text=text,
        life_name=life_name,
        metadata={"release_badge": release_badge} if release_badge else None,
    )
    print_formatted_text(
        FormattedText(
            format_message_fragments(
                MessageRenderSpec(
                    speaker=speaker,
                    text=text,
                    life_name=life_name,
                    release_badge=release_badge,
                    event_kind=event_kind,
                )
            )
        )
    )


def _bottom_toolbar(
    *,
    terminal_dir: Path,
    life_name: str,
    layout_state: TerminalLayoutState,
    slash_commands: tuple[tuple[str, str], ...],
    repo_root: Path,
):
    buffer = None
    try:
        from prompt_toolkit.application.current import get_app_or_none

        app = get_app_or_none()
        if app is not None:
            buffer = getattr(app, "current_buffer", None)
    except ImportError:
        buffer = None
    return _as_formatted_text(
        format_layout_toolbar_fragments(
            life_name=life_name,
            terminal_dir=terminal_dir,
            layout_state=layout_state,
            buffer=buffer,
            slash_commands=slash_commands,
            repo_root=repo_root,
        )
    )


def _format_bottom_toolbar(*, life_name: str, buffer=None, **kwargs):
    terminal_dir = kwargs.get("terminal_dir")
    layout_state = kwargs.get("layout_state") or resolve_terminal_layout_state()
    slash_commands = kwargs.get("slash_commands") or ()
    repo_root = kwargs.get("repo_root") or Path.cwd()
    if terminal_dir is None:
        return _as_formatted_text(
            [
                ("class:status", f" {life_name} "),
                ("class:input-box", " ┃ "),
                ("class:cursor-index", "pos 0/0"),
            ]
        )
    return _as_formatted_text(
        format_layout_toolbar_fragments(
            life_name=life_name,
            terminal_dir=terminal_dir,
            layout_state=layout_state,
            buffer=buffer,
            slash_commands=slash_commands,
            repo_root=repo_root,
        )
    )


def _as_formatted_text(fragments: list[tuple[str, str]]):
    try:
        from prompt_toolkit.formatted_text import FormattedText

        return FormattedText(fragments)
    except ImportError:
        return fragments