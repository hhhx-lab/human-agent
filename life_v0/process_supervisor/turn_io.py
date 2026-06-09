from __future__ import annotations

import io
import select
from typing import TextIO


def poll_input_line(input_stream: TextIO, *, timeout_seconds: float) -> str | None:
    poll_line = getattr(input_stream, "poll_line", None)
    if callable(poll_line):
        return poll_line(timeout_seconds)

    fileno = getattr(input_stream, "fileno", None)
    if not callable(fileno):
        return input_stream.readline()

    try:
        fileno()
    except (OSError, ValueError, AttributeError, io.UnsupportedOperation):
        return input_stream.readline()

    try:
        ready, _, _ = select.select([input_stream], [], [], timeout_seconds)
    except (OSError, ValueError):
        ready = []
    if not ready:
        return None

    return input_stream.readline()
