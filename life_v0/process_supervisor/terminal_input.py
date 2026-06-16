from __future__ import annotations

import json
import select
import sys
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TextIO


TERMINAL_INPUT_PROFILE_REF = "runtime/state/terminal/terminal_input_profile.json"
BACKSPACE_CHARS = {"\x7f", "\b"}


@dataclass(frozen=True)
class TerminalEditResult:
    submitted: bool = False
    line: str | None = None
    eof: bool = False
    interrupt: bool = False
    echo: str = ""
    ignored_escape: bool = False
    redraw: bool = False


class TerminalLineBuffer:
    def __init__(self, *, history: list[str] | None = None) -> None:
        self._chars: list[str] = []
        self._cursor = 0
        self._escape_buffer: str | None = None
        self._history = history if history is not None else []
        self._history_index: int | None = None
        self._history_draft = ""

    @property
    def has_text(self) -> bool:
        return bool(self._chars)

    @property
    def text(self) -> str:
        return "".join(self._chars)

    @property
    def cursor_index(self) -> int:
        return self._cursor

    def feed(self, char: str) -> TerminalEditResult:
        if self._escape_buffer is not None:
            return self._feed_escape(char)
        if char in {"\n", "\r"}:
            line = self.text
            self._chars.clear()
            self._cursor = 0
            self._history_index = None
            self._history_draft = ""
            return TerminalEditResult(submitted=True, line=line, echo="\n")
        if char == "\x03":
            return TerminalEditResult(interrupt=True, echo="\n")
        if char == "\x04":
            if self._chars:
                return self._delete_at_cursor()
            return TerminalEditResult(eof=True, echo="\n")
        if char == "\x01":
            self._cursor = 0
            return TerminalEditResult(redraw=True)
        if char == "\x05":
            self._cursor = len(self._chars)
            return TerminalEditResult(redraw=True)
        if char == "\x15":
            self._chars.clear()
            self._cursor = 0
            self._history_index = None
            return TerminalEditResult(redraw=True)
        if char == "\x0b":
            del self._chars[self._cursor :]
            return TerminalEditResult(redraw=True)
        if char == "\x17":
            return self._delete_previous_word()
        if char == "\x0c":
            return TerminalEditResult(redraw=True)
        if char in BACKSPACE_CHARS:
            if self._cursor <= 0:
                return TerminalEditResult()
            del self._chars[self._cursor - 1]
            self._cursor -= 1
            self._history_index = None
            return TerminalEditResult(redraw=True)
        if char == "\x1b":
            self._escape_buffer = ""
            return TerminalEditResult(ignored_escape=True)
        if _is_printable_input_char(char):
            self._chars.insert(self._cursor, char)
            self._cursor += 1
            self._history_index = None
            return TerminalEditResult(redraw=True)
        return TerminalEditResult()

    def _feed_escape(self, char: str) -> TerminalEditResult:
        self._escape_buffer = (self._escape_buffer or "") + char
        sequence = self._escape_buffer
        if sequence == "[":
            return TerminalEditResult(ignored_escape=True)
        if sequence.startswith("[") and len(sequence) == 2 and sequence[1] in "ABCDHF":
            self._escape_buffer = None
            return self._apply_escape_command(sequence)
        if sequence.startswith("[") and sequence.endswith("~"):
            self._escape_buffer = None
            return self._apply_escape_command(sequence)
        if not sequence.startswith("[") or len(sequence) > 5:
            self._escape_buffer = None
        return TerminalEditResult(ignored_escape=True)

    def _apply_escape_command(self, sequence: str) -> TerminalEditResult:
        if sequence == "[D":
            self._cursor = max(0, self._cursor - 1)
            return TerminalEditResult(redraw=True)
        if sequence == "[C":
            self._cursor = min(len(self._chars), self._cursor + 1)
            return TerminalEditResult(redraw=True)
        if sequence == "[A":
            return self._history_previous()
        if sequence == "[B":
            return self._history_next()
        if sequence in {"[H", "[1~", "[7~"}:
            self._cursor = 0
            return TerminalEditResult(redraw=True)
        if sequence in {"[F", "[4~", "[8~"}:
            self._cursor = len(self._chars)
            return TerminalEditResult(redraw=True)
        if sequence == "[3~":
            return self._delete_at_cursor()
        return TerminalEditResult(ignored_escape=True)

    def _delete_at_cursor(self) -> TerminalEditResult:
        if self._cursor >= len(self._chars):
            return TerminalEditResult()
        del self._chars[self._cursor]
        self._history_index = None
        return TerminalEditResult(redraw=True)

    def _delete_previous_word(self) -> TerminalEditResult:
        if self._cursor <= 0:
            return TerminalEditResult()
        start = self._cursor
        while start > 0 and self._chars[start - 1].isspace():
            start -= 1
        while start > 0 and not self._chars[start - 1].isspace():
            start -= 1
        del self._chars[start : self._cursor]
        self._cursor = start
        self._history_index = None
        return TerminalEditResult(redraw=True)

    def _history_previous(self) -> TerminalEditResult:
        if not self._history:
            return TerminalEditResult(ignored_escape=True)
        if self._history_index is None:
            self._history_draft = self.text
            self._history_index = len(self._history) - 1
        else:
            self._history_index = max(0, self._history_index - 1)
        self._replace_text(self._history[self._history_index])
        return TerminalEditResult(redraw=True)

    def _history_next(self) -> TerminalEditResult:
        if self._history_index is None:
            return TerminalEditResult(ignored_escape=True)
        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            self._replace_text(self._history[self._history_index])
        else:
            self._history_index = None
            self._replace_text(self._history_draft)
            self._history_draft = ""
        return TerminalEditResult(redraw=True)

    def _replace_text(self, text: str) -> None:
        self._chars = list(str(text or ""))
        self._cursor = len(self._chars)


def build_terminal_input_profile(
    *,
    input_stream: TextIO,
    idle_voice_interval_seconds: float,
    mode_override: str | None = None,
) -> dict[str, Any]:
    is_tty = bool(getattr(input_stream, "isatty", lambda: False)())
    char_mode_available = is_tty and _has_usable_fileno(input_stream) and _has_tty_modules()
    readline_available = _readline_available()
    input_mode = mode_override
    if not input_mode:
        input_mode = (
            "char_line_editor_with_history_and_idle_voice"
            if char_mode_available
            else "canonical_line_with_idle_voice"
        )
    return {
        "schema_version": "terminal_input_profile_v0",
        "terminal_input_profile_ref": TERMINAL_INPUT_PROFILE_REF,
        "input_mode": input_mode,
        "is_tty": is_tty,
        "char_mode_available": char_mode_available,
        "readline_module_available": readline_available,
        "line_editing": {
            "backspace": "delete_previous_character",
            "delete": "delete_character_under_cursor",
            "left_right_arrows": "move_cursor_inside_current_line",
            "up_down_arrows": "navigate_in_memory_terminal_history",
            "home_end": "jump_to_line_boundaries",
            "ctrl_u": "clear_current_line",
            "ctrl_w": "delete_previous_word",
            "ctrl_k": "clear_line_after_cursor",
            "ctrl_a_ctrl_e": "jump_to_line_boundaries",
            "ctrl_l": "redraw_current_line",
            "ctrl_d": "eof_when_buffer_empty",
            "ctrl_c": "interrupt_current_input",
            "escape_sequence_policy": "interpret_common_navigation_escape_sequences",
            "redraw_strategy": "single_prompt_line_redraw_for_multibyte_text",
        },
        "idle_voice_policy": {
            "enabled": idle_voice_interval_seconds > 0,
            "interval_seconds": idle_voice_interval_seconds,
            "release_only_when_input_buffer_empty": True,
            "reprint_prompt_after_idle_voice": True,
        },
        "relation_turn_boundary": {
            "slash_commands_bypass_relation_inbox": True,
            "input_profile_is_terminal_periphery": True,
        },
    }


def write_terminal_input_profile(
    *,
    terminal_dir: Path,
    profile: dict[str, Any],
) -> dict[str, Any]:
    terminal_dir.mkdir(parents=True, exist_ok=True)
    path = terminal_dir / "terminal_input_profile.json"
    path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return profile


def read_interactive_line_with_idle_voice(
    *,
    prompt: str,
    idle_voice_fn: Callable[[], bool],
    idle_voice_interval_seconds: float,
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
    history: list[str] | None = None,
) -> str:
    input_stream = input_stream or sys.stdin
    output_stream = output_stream or sys.stdout
    if idle_voice_interval_seconds <= 0:
        return input(prompt)
    if _can_use_char_line_editor(input_stream):
        return _read_char_line_with_idle_voice(
            prompt=prompt,
            idle_voice_fn=idle_voice_fn,
            idle_voice_interval_seconds=idle_voice_interval_seconds,
            input_stream=input_stream,
            output_stream=output_stream,
            history=history,
        )
    return _read_canonical_line_with_idle_voice(
        prompt=prompt,
        idle_voice_fn=idle_voice_fn,
        idle_voice_interval_seconds=idle_voice_interval_seconds,
        input_stream=input_stream,
        output_stream=output_stream,
    )


def _read_char_line_with_idle_voice(
    *,
    prompt: str,
    idle_voice_fn: Callable[[], bool],
    idle_voice_interval_seconds: float,
    input_stream: TextIO,
    output_stream: TextIO,
    history: list[str] | None = None,
) -> str:
    import termios
    import tty

    fd = input_stream.fileno()
    previous_settings = termios.tcgetattr(fd)
    editor = TerminalLineBuffer(history=history)
    output_stream.write(prompt)
    output_stream.flush()
    next_idle_at = time.monotonic() + idle_voice_interval_seconds
    try:
        tty.setcbreak(fd)
        while True:
            timeout = max(0.0, min(0.1, next_idle_at - time.monotonic()))
            readable, _, _ = select.select([input_stream], [], [], timeout)
            if readable:
                char = input_stream.read(1)
                if char == "":
                    raise EOFError
                result = editor.feed(char)
                if result.redraw:
                    output_stream.write(_render_editor_redraw(prompt, editor))
                    output_stream.flush()
                elif result.echo:
                    output_stream.write(result.echo)
                    output_stream.flush()
                if result.interrupt:
                    raise KeyboardInterrupt
                if result.eof:
                    raise EOFError
                if result.submitted:
                    return result.line or ""
                continue
            if time.monotonic() < next_idle_at:
                continue
            next_idle_at = time.monotonic() + idle_voice_interval_seconds
            if editor.has_text:
                continue
            output_stream.write("\r\x1b[2K")
            output_stream.flush()
            if idle_voice_fn():
                output_stream.write(_render_editor_redraw(prompt, editor))
            else:
                output_stream.write(_render_editor_redraw(prompt, editor))
            output_stream.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, previous_settings)


def _read_canonical_line_with_idle_voice(
    *,
    prompt: str,
    idle_voice_fn: Callable[[], bool],
    idle_voice_interval_seconds: float,
    input_stream: TextIO,
    output_stream: TextIO,
) -> str:
    output_stream.write(prompt)
    output_stream.flush()
    while True:
        try:
            readable, _, _ = select.select(
                [input_stream],
                [],
                [],
                idle_voice_interval_seconds,
            )
        except (OSError, ValueError):
            return input("")
        if readable:
            line = input_stream.readline()
            if line == "":
                raise EOFError
            return line.rstrip("\n")
        if idle_voice_fn():
            output_stream.write(prompt)
            output_stream.flush()


def _can_use_char_line_editor(input_stream: TextIO) -> bool:
    return (
        bool(getattr(input_stream, "isatty", lambda: False)())
        and _has_usable_fileno(input_stream)
        and _has_tty_modules()
    )


def _has_usable_fileno(input_stream: TextIO) -> bool:
    fileno = getattr(input_stream, "fileno", None)
    if not callable(fileno):
        return False
    try:
        fileno()
    except (OSError, ValueError, AttributeError):
        return False
    return True


def _has_tty_modules() -> bool:
    try:
        import termios  # noqa: F401
        import tty  # noqa: F401
    except ImportError:
        return False
    return True


def _readline_available() -> bool:
    try:
        import readline  # noqa: F401
    except ImportError:
        return False
    return True


def _is_printable_input_char(char: str) -> bool:
    return bool(char) and char.isprintable()


def _render_editor_redraw(prompt: str, editor: TerminalLineBuffer) -> str:
    cursor_columns = _terminal_display_width(prompt + editor.text[: editor.cursor_index])
    move = f"\x1b[{cursor_columns}C" if cursor_columns > 0 else ""
    return "\r\x1b[2K" + prompt + editor.text + "\r" + move


def _terminal_display_width(text: str) -> int:
    width = 0
    for char in str(text or ""):
        if unicodedata.combining(char):
            continue
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return width
