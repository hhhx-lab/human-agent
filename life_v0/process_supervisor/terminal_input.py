from __future__ import annotations

import json
import select
import sys
import time
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


class TerminalLineBuffer:
    def __init__(self) -> None:
        self._chars: list[str] = []
        self._escape_sequence_remaining = 0

    @property
    def has_text(self) -> bool:
        return bool(self._chars)

    @property
    def text(self) -> str:
        return "".join(self._chars)

    def feed(self, char: str) -> TerminalEditResult:
        if self._escape_sequence_remaining > 0:
            self._escape_sequence_remaining -= 1
            return TerminalEditResult(ignored_escape=True)
        if char in {"\n", "\r"}:
            line = self.text
            self._chars.clear()
            return TerminalEditResult(submitted=True, line=line, echo="\n")
        if char == "\x03":
            return TerminalEditResult(interrupt=True, echo="\n")
        if char == "\x04":
            if self._chars:
                return TerminalEditResult()
            return TerminalEditResult(eof=True, echo="\n")
        if char == "\x15":
            count = len(self._chars)
            self._chars.clear()
            return TerminalEditResult(echo="\b \b" * count)
        if char in BACKSPACE_CHARS:
            if not self._chars:
                return TerminalEditResult()
            self._chars.pop()
            return TerminalEditResult(echo="\b \b")
        if char == "\x1b":
            self._escape_sequence_remaining = 2
            return TerminalEditResult(ignored_escape=True)
        if _is_printable_input_char(char):
            self._chars.append(char)
            return TerminalEditResult(echo=char)
        return TerminalEditResult()


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
            "char_line_editor_with_idle_voice"
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
            "ctrl_u": "clear_current_line",
            "ctrl_d": "eof_when_buffer_empty",
            "ctrl_c": "interrupt_current_input",
            "escape_sequence_policy": "ignore_navigation_escape_sequences",
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
) -> str:
    import termios
    import tty

    fd = input_stream.fileno()
    previous_settings = termios.tcgetattr(fd)
    editor = TerminalLineBuffer()
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
                if result.echo:
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
            if idle_voice_fn():
                output_stream.write(prompt)
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
