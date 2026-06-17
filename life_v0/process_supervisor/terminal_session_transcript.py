from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TERMINAL_SESSION_TRANSCRIPT_REF = "runtime/state/terminal/terminal_session_transcript.jsonl"
TERMINAL_SESSION_INDEX_REF = "runtime/state/terminal/terminal_session_index.json"


def start_terminal_session_transcript(
    *,
    terminal_dir: Path,
    life_name: str | None,
    now_iso=None,
) -> dict[str, Any]:
    generated_at = _call_now(now_iso)
    session_id = _allocate_session_id(
        terminal_dir=terminal_dir,
        generated_at=generated_at,
    )
    event = {
        "schema_version": "terminal_session_transcript_event_v0",
        "event_kind": "session_opened",
        "session_id": session_id,
        "speaker": "terminal",
        "text": "",
        "life_name": life_name or "Digital Life",
        "generated_at": generated_at,
        "terminal_session_transcript_ref": TERMINAL_SESSION_TRANSCRIPT_REF,
        "terminal_session_index_ref": TERMINAL_SESSION_INDEX_REF,
    }
    _append_jsonl(terminal_dir / "terminal_session_transcript.jsonl", event)
    _write_session_index(
        terminal_dir=terminal_dir,
        session_id=session_id,
        life_name=life_name,
        generated_at=generated_at,
        current_event=event,
    )
    return event


def append_terminal_session_event(
    *,
    terminal_dir: Path,
    session_id: str,
    event_kind: str,
    speaker: str,
    text: str,
    life_name: str | None = None,
    now_iso=None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    generated_at = _call_now(now_iso)
    event = {
        "schema_version": "terminal_session_transcript_event_v0",
        "event_kind": str(event_kind or "").strip() or "message",
        "session_id": str(session_id or "").strip(),
        "speaker": str(speaker or "").strip() or "terminal",
        "text": str(text or ""),
        "life_name": life_name or "Digital Life",
        "generated_at": generated_at,
        "terminal_session_transcript_ref": TERMINAL_SESSION_TRANSCRIPT_REF,
        "terminal_session_index_ref": TERMINAL_SESSION_INDEX_REF,
    }
    if metadata:
        event["metadata"] = dict(metadata)
    _append_jsonl(terminal_dir / "terminal_session_transcript.jsonl", event)
    _write_session_index(
        terminal_dir=terminal_dir,
        session_id=event["session_id"],
        life_name=life_name,
        generated_at=generated_at,
        current_event=event,
    )
    return event


def load_current_terminal_session_lines(
    *,
    terminal_dir: Path,
    limit: int = 200,
) -> list[str]:
    index = read_terminal_session_index(terminal_dir=terminal_dir)
    session_id = str(index.get("current_session_id") or "").strip()
    if not session_id:
        return []
    return render_terminal_session_lines(
        events=[
            event
            for event in _read_jsonl(terminal_dir / "terminal_session_transcript.jsonl")
            if event.get("session_id") == session_id
        ],
        limit=limit,
    )


def render_resume_transcript(
    *,
    terminal_dir: Path,
    session_count: int = 3,
    event_limit: int = 80,
) -> str:
    events = _read_jsonl(terminal_dir / "terminal_session_transcript.jsonl")
    if not events:
        return "还没有可恢复的终端会话记录。"
    session_order: list[str] = []
    for event in events:
        session_id = str(event.get("session_id") or "").strip()
        if session_id and session_id not in session_order:
            session_order.append(session_id)
    selected_sessions = session_order[-max(1, session_count) :]
    if not selected_sessions:
        return "还没有可恢复的终端会话记录。"
    lines: list[str] = ["最近会话："]
    for index, session_id in enumerate(selected_sessions, start=1):
        session_events = [
            event
            for event in events
            if str(event.get("session_id") or "").strip() == session_id
            and not _is_resume_command_result_event(event)
        ]
        if not session_events:
            continue
        first_event = session_events[0]
        last_event = session_events[-1]
        line_count = sum(1 for event in session_events if str(event.get("text") or "").strip())
        lines.append(
            f"{index}. {session_id} | {line_count} 条记录 | "
            f"{_resume_preview(first_event)} -> {_resume_preview(last_event)}"
        )
    lines.append("")
    lines.append("最近内容：")
    selected_events = [
        event
        for event in events
        if str(event.get("session_id") or "").strip() in set(selected_sessions)
        and not _is_resume_command_result_event(event)
    ][-max(1, event_limit) :]
    session_lines = render_terminal_session_lines(events=selected_events, limit=event_limit)
    lines.extend(session_lines or ["还没有可恢复的终端会话记录。"])
    return "\n".join(lines).strip() or "还没有可恢复的终端会话记录。"


def render_terminal_session_lines(
    *,
    events: list[dict[str, Any]],
    limit: int = 200,
) -> list[str]:
    lines: list[str] = []
    previous_session_id = ""
    for event in events[-max(1, limit) :]:
        kind = str(event.get("event_kind") or "")
        session_id = str(event.get("session_id") or "")
        if session_id and session_id != previous_session_id:
            previous_session_id = session_id
            if lines:
                lines.append("")
            lines.append(f"session {session_id}")
        if kind == "session_opened":
            continue
        speaker = str(event.get("speaker") or "").strip() or "terminal"
        text = str(event.get("text") or "").strip()
        if not text:
            continue
        prefix = _speaker_prefix(speaker, event.get("life_name"))
        text_lines = text.splitlines() or [""]
        lines.append(prefix + text_lines[0])
        for continuation in text_lines[1:]:
            lines.append("  " + continuation)
    return lines[-max(1, limit) :]


def read_terminal_session_index(*, terminal_dir: Path) -> dict[str, Any]:
    path = terminal_dir / "terminal_session_index.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_session_index(
    *,
    terminal_dir: Path,
    session_id: str,
    life_name: str | None,
    generated_at: str,
    current_event: dict[str, Any],
) -> None:
    terminal_dir.mkdir(parents=True, exist_ok=True)
    path = terminal_dir / "terminal_session_index.json"
    previous = read_terminal_session_index(terminal_dir=terminal_dir)
    session_ids = [
        str(value)
        for value in previous.get("session_ids", [])
        if str(value or "").strip()
    ]
    if session_id and session_id not in session_ids:
        session_ids.append(session_id)
    payload = {
        "schema_version": "terminal_session_index_v0",
        "current_session_id": session_id,
        "session_ids": session_ids[-200:],
        "life_name": life_name or "Digital Life",
        "last_event_kind": current_event.get("event_kind"),
        "last_event_at": generated_at,
        "terminal_session_transcript_ref": TERMINAL_SESSION_TRANSCRIPT_REF,
        "terminal_session_index_ref": TERMINAL_SESSION_INDEX_REF,
        "context_policy": "stored_for_resume_view_not_injected_into_current_model_context",
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _allocate_session_id(*, terminal_dir: Path, generated_at: str) -> str:
    base = "terminal-session-" + generated_at.replace(":", "").replace("+", "Z")
    index = read_terminal_session_index(terminal_dir=terminal_dir)
    existing = {
        str(value)
        for value in index.get("session_ids", [])
        if str(value or "").strip()
    }
    if base not in existing:
        return base
    counter = 2
    while True:
        candidate = f"{base}-{counter:02d}"
        if candidate not in existing:
            return candidate
        counter += 1


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    events: list[dict[str, Any]] = []
    for line in lines:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except ValueError:
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events


def _speaker_prefix(speaker: str, life_name: Any) -> str:
    normalized = str(speaker or "").strip().lower()
    if normalized in {"self", "life", "adam"}:
        return f"{str(life_name or 'Adam').strip() or 'Adam'}: "
    if normalized in {"relation", "human", "person"}:
        return "你: "
    if normalized == "command":
        return "command: "
    if normalized == "command_result":
        return "command result: "
    if normalized == "proactive":
        return f"{str(life_name or 'Adam').strip() or 'Adam'}: "
    return f"{speaker}: "


def _is_resume_command_result_event(event: dict[str, Any]) -> bool:
    metadata = event.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    return (
        event.get("event_kind") == "command_result"
        and str(metadata.get("title") or "") == "会话恢复"
    )


def _call_now(now_iso) -> str:
    if callable(now_iso):
        return str(now_iso())
    if now_iso:
        return str(now_iso)
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _resume_preview(event: dict[str, Any]) -> str:
    speaker = _speaker_prefix(str(event.get("speaker") or "").strip(), event.get("life_name"))
    text = str(event.get("text") or "").strip().replace("\n", " ")
    if len(text) > 24:
        text = text[:24] + "…"
    return speaker + text if text else speaker.rstrip()
