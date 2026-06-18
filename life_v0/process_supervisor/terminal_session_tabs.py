from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .terminal_session_transcript import (
    read_terminal_session_index,
    render_terminal_session_lines,
    start_terminal_session_transcript,
)


@dataclass(frozen=True)
class TerminalSessionTab:
    session_id: str
    label: str
    is_current: bool


def list_terminal_session_tabs(
    *,
    terminal_dir: Path,
    limit: int = 5,
) -> list[TerminalSessionTab]:
    index = read_terminal_session_index(terminal_dir=terminal_dir)
    current = str(index.get("current_session_id") or "").strip()
    session_ids = [
        str(value).strip()
        for value in index.get("session_ids", [])
        if str(value or "").strip()
    ]
    if not session_ids and current:
        session_ids = [current]
    selected = session_ids[-max(1, limit) :]
    tabs: list[TerminalSessionTab] = []
    for position, session_id in enumerate(selected, start=1):
        tabs.append(
            TerminalSessionTab(
                session_id=session_id,
                label=_tab_label(session_id, position=position),
                is_current=session_id == current,
            )
        )
    return tabs


def format_session_tab_bar_fragments(
    *,
    terminal_dir: Path,
    width: int,
    limit: int = 5,
) -> list[tuple[str, str]]:
    tabs = list_terminal_session_tabs(terminal_dir=terminal_dir, limit=limit)
    if not tabs:
        return [
            ("class:tab-bar", " sessions "),
            ("class:hint", " Ctrl-T 新建"),
            ("", "\n"),
        ]
    fragments: list[tuple[str, str]] = [("class:tab-bar", " ")]
    for index, tab in enumerate(tabs):
        if index > 0:
            fragments.append(("class:tab-idle", "  "))
        if tab.is_current:
            fragments.append(("class:tab-active", f" {tab.label} "))
            underline = "─" * max(3, min(len(tab.label) + 2, 12))
            fragments.append(("class:tab-active-underline", underline))
        else:
            fragments.append(("class:tab-idle", f" {tab.label} "))
    fragments.append(("class:hint", "   +Ctrl-T"))
    fragments.append(("", "\n"))
    return fragments


def switch_terminal_session(*, terminal_dir: Path, session_id: str) -> str:
    normalized = str(session_id or "").strip()
    if not normalized:
        return read_terminal_session_index(terminal_dir=terminal_dir).get(
            "current_session_id", ""
        )
    index = read_terminal_session_index(terminal_dir=terminal_dir)
    session_ids = [
        str(value).strip()
        for value in index.get("session_ids", [])
        if str(value or "").strip()
    ]
    if normalized not in session_ids:
        session_ids.append(normalized)
    payload = {
        **index,
        "schema_version": "terminal_session_index_v0",
        "current_session_id": normalized,
        "session_ids": session_ids[-200:],
    }
    terminal_dir.mkdir(parents=True, exist_ok=True)
    path = terminal_dir / "terminal_session_index.json"
    import json

    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return normalized


def create_terminal_session_tab(
    *,
    terminal_dir: Path,
    life_name: str | None,
) -> str:
    event = start_terminal_session_transcript(
        terminal_dir=terminal_dir,
        life_name=life_name,
    )
    return str(event.get("session_id") or "")


def cycle_terminal_session_tab(
    *,
    terminal_dir: Path,
    direction: str = "next",
) -> str:
    tabs = list_terminal_session_tabs(terminal_dir=terminal_dir, limit=200)
    if not tabs:
        return ""
    current_index = next(
        (index for index, tab in enumerate(tabs) if tab.is_current),
        len(tabs) - 1,
    )
    if direction == "prev":
        next_index = (current_index - 1) % len(tabs)
    else:
        next_index = (current_index + 1) % len(tabs)
    return switch_terminal_session(
        terminal_dir=terminal_dir,
        session_id=tabs[next_index].session_id,
    )


def load_session_conversation_lines(
    *,
    terminal_dir: Path,
    session_id: str,
    limit: int = 400,
) -> list[str]:
    from .terminal_session_transcript import load_terminal_session_events

    events = load_terminal_session_events(
        terminal_dir=terminal_dir,
        session_id=session_id,
    )
    return render_terminal_session_lines(events=events, limit=limit)


def _tab_label(session_id: str, *, position: int) -> str:
    compact = str(session_id or "").replace("terminal-session-", "s")
    if len(compact) > 14:
        compact = compact[:6] + "…" + compact[-5:]
    return f"{position}:{compact}"