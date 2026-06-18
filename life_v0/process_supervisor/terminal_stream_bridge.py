from __future__ import annotations

import contextvars
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class TerminalStreamSink:
    on_delta: Callable[[str], None] | None = None
    on_start: Callable[[], None] | None = None
    on_complete: Callable[[str], None] | None = None
    deltas: list[str] = field(default_factory=list)

    def emit_start(self) -> None:
        if self.on_start is not None:
            self.on_start()

    def emit_delta(self, chunk: str) -> None:
        if not chunk:
            return
        self.deltas.append(chunk)
        if self.on_delta is not None:
            self.on_delta(chunk)

    def emit_complete(self, full_text: str) -> None:
        if self.on_complete is not None:
            self.on_complete(full_text)

    @property
    def saw_live_deltas(self) -> bool:
        return bool(self.deltas)


_active_sink: contextvars.ContextVar[TerminalStreamSink | None] = contextvars.ContextVar(
    "terminal_stream_sink",
    default=None,
)


def get_stream_sink() -> TerminalStreamSink | None:
    return _active_sink.get()


@contextmanager
def stream_session(
    *,
    on_delta: Callable[[str], None] | None = None,
    on_start: Callable[[], None] | None = None,
    on_complete: Callable[[str], None] | None = None,
) -> Iterator[TerminalStreamSink]:
    sink = TerminalStreamSink(
        on_delta=on_delta,
        on_start=on_start,
        on_complete=on_complete,
    )
    token = _active_sink.set(sink)
    try:
        yield sink
    finally:
        _active_sink.reset(token)


def emit_stream_delta(chunk: str) -> None:
    sink = get_stream_sink()
    if sink is not None:
        sink.emit_delta(chunk)