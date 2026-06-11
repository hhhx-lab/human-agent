from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


RESIDENT_PROCESS_LEASE_REF = "runtime/state/terminal/resident_process_lease.json"
RESIDENT_PROCESS_LEASE_HISTORY_REF = "runtime/state/terminal/resident_process_lease_history.jsonl"
RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF = (
    "runtime/state/terminal/resident_process_lease_history_profile.json"
)
SAFE_TERMINAL_LOOP_STATE_REF = "runtime/state/terminal/safe_terminal_loop_state.json"
TERMINAL_LIFE_LOOP_STATE_REF = "runtime/state/terminal/terminal_life_loop_state.json"
RESIDENT_GOVERNANCE_STATE_REF = "runtime/state/terminal/resident_governance_state.json"
IDLE_HEARTBEAT_TRACE_REF = "runtime/state/terminal/idle_heartbeat_trace.jsonl"
PROCESS_REPORT_REF = "runtime/reports/latest/digital_life_process_report.json"


def open_resident_process_lease(
    *,
    run_id: str,
    generated_at: str,
    terminal_dir: Path,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any]:
    lease = {
        "schema_version": "resident_process_lease_v0",
        "run_id": run_id,
        "resident_process_id": f"resident-process-{run_id}",
        "lease_state": "active",
        "opened_at": generated_at,
        "last_seen_at": generated_at,
        "closed_at": None,
        "heartbeat_counter": 0,
        "completed_dialogue_turns": 0,
        "incident_count": 0,
        "exit_reason": None,
        "safe_terminal_loop_state_ref": SAFE_TERMINAL_LOOP_STATE_REF,
        "terminal_life_loop_state_ref": TERMINAL_LIFE_LOOP_STATE_REF,
        "resident_governance_state_ref": RESIDENT_GOVERNANCE_STATE_REF,
        "idle_heartbeat_trace_ref": IDLE_HEARTBEAT_TRACE_REF,
        "resident_process_lease_history_ref": RESIDENT_PROCESS_LEASE_HISTORY_REF,
        "process_report_ref": None,
    }
    write_json(terminal_dir / "resident_process_lease.json", lease)
    _append_lease_history_event(
        terminal_dir=terminal_dir,
        generated_at=generated_at,
        event_kind="lease_opened",
        lease=lease,
    )
    write_resident_process_lease_history_profile(
        terminal_dir=terminal_dir,
        write_json=write_json,
    )
    return lease


def refresh_resident_process_lease(
    *,
    run_id: str,
    generated_at: str,
    terminal_dir: Path,
    heartbeat_counter: int,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any]:
    lease = _read_lease(terminal_dir)
    if not lease or _requires_new_lease(lease, run_id):
        lease = open_resident_process_lease(
            run_id=run_id,
            generated_at=generated_at,
            terminal_dir=terminal_dir,
            write_json=write_json,
        )
    lease["run_id"] = run_id
    lease.setdefault("resident_process_id", f"resident-process-{run_id}")
    lease["lease_state"] = "active"
    lease["last_seen_at"] = generated_at
    lease["heartbeat_counter"] = heartbeat_counter
    lease["safe_terminal_loop_state_ref"] = SAFE_TERMINAL_LOOP_STATE_REF
    lease["terminal_life_loop_state_ref"] = TERMINAL_LIFE_LOOP_STATE_REF
    lease["resident_governance_state_ref"] = RESIDENT_GOVERNANCE_STATE_REF
    lease["idle_heartbeat_trace_ref"] = IDLE_HEARTBEAT_TRACE_REF
    lease["resident_process_lease_history_ref"] = RESIDENT_PROCESS_LEASE_HISTORY_REF
    write_json(terminal_dir / "resident_process_lease.json", lease)
    _append_lease_history_event(
        terminal_dir=terminal_dir,
        generated_at=generated_at,
        event_kind="lease_refreshed",
        lease=lease,
    )
    write_resident_process_lease_history_profile(
        terminal_dir=terminal_dir,
        write_json=write_json,
    )
    return lease


def normalize_interrupted_resident_process_lease(
    *,
    next_run_id: str,
    generated_at: str,
    terminal_dir: Path,
    previous_lease: dict[str, Any],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any] | None:
    if previous_lease.get("lease_state") != "active":
        return None

    interrupted_lease = dict(previous_lease)
    interrupted_lease.setdefault(
        "resident_process_id",
        f"resident-process-{interrupted_lease.get('run_id', 'unknown')}",
    )
    interrupted_lease["lease_state"] = "interrupted_on_relaunch"
    interrupted_lease["last_seen_at"] = generated_at
    interrupted_lease["closed_at"] = generated_at
    interrupted_lease["exit_reason"] = "relaunch_detected_active_lease"
    interrupted_lease["interrupted_by_run_id"] = next_run_id
    interrupted_lease["resident_process_lease_history_ref"] = RESIDENT_PROCESS_LEASE_HISTORY_REF
    write_json(terminal_dir / "resident_process_lease.json", interrupted_lease)
    _append_lease_history_event(
        terminal_dir=terminal_dir,
        generated_at=generated_at,
        event_kind="lease_interrupted_on_relaunch",
        lease=interrupted_lease,
        extra={"interrupted_by_run_id": next_run_id},
    )
    write_resident_process_lease_history_profile(
        terminal_dir=terminal_dir,
        write_json=write_json,
    )
    return interrupted_lease


def close_resident_process_lease(
    *,
    run_id: str,
    generated_at: str,
    terminal_dir: Path,
    heartbeat_counter: int,
    completed_turns: int,
    incident_count: int,
    exit_reason: str,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any]:
    lease = _read_lease(terminal_dir)
    if not lease:
        lease = open_resident_process_lease(
            run_id=run_id,
            generated_at=generated_at,
            terminal_dir=terminal_dir,
            write_json=write_json,
        )
    lease["run_id"] = run_id
    lease.setdefault("resident_process_id", f"resident-process-{run_id}")
    lease["lease_state"] = "closed"
    lease["last_seen_at"] = generated_at
    lease["closed_at"] = generated_at
    lease["heartbeat_counter"] = heartbeat_counter
    lease["completed_dialogue_turns"] = completed_turns
    lease["incident_count"] = incident_count
    lease["exit_reason"] = exit_reason
    lease["safe_terminal_loop_state_ref"] = SAFE_TERMINAL_LOOP_STATE_REF
    lease["terminal_life_loop_state_ref"] = TERMINAL_LIFE_LOOP_STATE_REF
    lease["resident_governance_state_ref"] = RESIDENT_GOVERNANCE_STATE_REF
    lease["idle_heartbeat_trace_ref"] = IDLE_HEARTBEAT_TRACE_REF
    lease["resident_process_lease_history_ref"] = RESIDENT_PROCESS_LEASE_HISTORY_REF
    lease["process_report_ref"] = PROCESS_REPORT_REF
    write_json(terminal_dir / "resident_process_lease.json", lease)
    _append_lease_history_event(
        terminal_dir=terminal_dir,
        generated_at=generated_at,
        event_kind="lease_closed",
        lease=lease,
    )
    write_resident_process_lease_history_profile(
        terminal_dir=terminal_dir,
        write_json=write_json,
    )
    return lease


def write_resident_process_lease_history_profile(
    *,
    terminal_dir: Path,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any]:
    profile = build_resident_process_lease_history_profile(terminal_dir=terminal_dir)
    write_json(terminal_dir / "resident_process_lease_history_profile.json", profile)
    return profile


def build_resident_process_lease_history_profile(
    *,
    terminal_dir: Path,
) -> dict[str, Any]:
    history_events = _read_lease_history_events(terminal_dir)
    event_kinds = [str(event.get("event_kind", "")) for event in history_events]
    latest_event = history_events[-1] if history_events else {}
    opened_count = event_kinds.count("lease_opened")
    refreshed_count = event_kinds.count("lease_refreshed")
    closed_count = event_kinds.count("lease_closed")
    interrupted_count = event_kinds.count("lease_interrupted_on_relaunch")
    latest_event_kind = str(latest_event.get("event_kind", "") or "")
    continuity_state = _identity_continuity_state(
        latest_event=latest_event,
        latest_event_kind=latest_event_kind,
        interrupted_count=interrupted_count,
    )
    pressure_level = _identity_pressure_level(
        event_count=len(history_events),
        opened_count=opened_count,
        refreshed_count=refreshed_count,
        closed_count=closed_count,
        interrupted_count=interrupted_count,
        latest_event_kind=latest_event_kind,
    )
    recent_resident_process_ids = _recent_unique_strings(
        [event.get("resident_process_id") for event in history_events]
    )
    recent_run_ids = _recent_unique_strings(
        [event.get("run_id") for event in history_events]
    )
    profile = {
        "schema_version": "resident_process_lease_history_profile_v0",
        "resident_process_lease_ref": RESIDENT_PROCESS_LEASE_REF,
        "resident_process_lease_history_ref": RESIDENT_PROCESS_LEASE_HISTORY_REF,
        "resident_process_lease_history_profile_ref": RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF,
        "history_event_count": len(history_events),
        "opened_count": opened_count,
        "refreshed_count": refreshed_count,
        "closed_count": closed_count,
        "interrupted_on_relaunch_count": interrupted_count,
        "latest_event_kind": latest_event_kind or None,
        "latest_event_generated_at": latest_event.get("generated_at"),
        "latest_run_id": latest_event.get("run_id"),
        "latest_resident_process_id": latest_event.get("resident_process_id"),
        "latest_lease_state": latest_event.get("lease_state"),
        "latest_exit_reason": latest_event.get("exit_reason"),
        "current_identity_continuity_state": continuity_state,
        "identity_pressure_level": pressure_level,
        "recent_resident_process_ids": recent_resident_process_ids,
        "recent_run_ids": recent_run_ids,
        "evidence_refs": [
            RESIDENT_PROCESS_LEASE_REF,
            RESIDENT_PROCESS_LEASE_HISTORY_REF,
        ],
    }
    return {key: value for key, value in profile.items() if value is not None}


def _append_lease_history_event(
    *,
    terminal_dir: Path,
    generated_at: str,
    event_kind: str,
    lease: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> None:
    event = {
        "schema_version": "resident_process_lease_history_event_v0",
        "event_kind": event_kind,
        "generated_at": generated_at,
        "run_id": lease.get("run_id"),
        "resident_process_id": lease.get("resident_process_id"),
        "resident_process_lease_ref": RESIDENT_PROCESS_LEASE_REF,
        "resident_process_lease_history_ref": RESIDENT_PROCESS_LEASE_HISTORY_REF,
        "lease_state": lease.get("lease_state"),
        "heartbeat_counter": lease.get("heartbeat_counter", 0),
        "completed_dialogue_turns": lease.get("completed_dialogue_turns", 0),
        "incident_count": lease.get("incident_count", 0),
        "exit_reason": lease.get("exit_reason"),
        "process_report_ref": lease.get("process_report_ref"),
    }
    if extra:
        event.update(extra)
    terminal_dir.mkdir(parents=True, exist_ok=True)
    with (terminal_dir / "resident_process_lease_history.jsonl").open(
        "a", encoding="utf-8"
    ) as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def _read_lease_history_events(terminal_dir: Path) -> list[dict[str, Any]]:
    path = terminal_dir / "resident_process_lease_history.jsonl"
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for line in lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except (ValueError, TypeError):
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def _identity_continuity_state(
    *,
    latest_event: dict[str, Any],
    latest_event_kind: str,
    interrupted_count: int,
) -> str:
    latest_lease_state = latest_event.get("lease_state")
    if (
        latest_event_kind == "lease_interrupted_on_relaunch"
        or latest_lease_state == "interrupted_on_relaunch"
    ):
        return "interrupted_waiting_recovery"
    if latest_event_kind in {"lease_opened", "lease_refreshed"}:
        if interrupted_count:
            return "interrupted_then_recovered"
        return "active_residency"
    if latest_event_kind == "lease_closed":
        if interrupted_count:
            return "recovered_closed_continuity"
        return "continuous_closed"
    return "no_lease_history"


def _identity_pressure_level(
    *,
    event_count: int,
    opened_count: int,
    refreshed_count: int,
    closed_count: int,
    interrupted_count: int,
    latest_event_kind: str,
) -> str:
    if interrupted_count or latest_event_kind == "lease_interrupted_on_relaunch":
        return "elevated"
    if closed_count or refreshed_count or opened_count > 1 or event_count > 1:
        return "present"
    return "light"


def _recent_unique_strings(values: list[Any], *, limit: int = 5) -> list[str]:
    recent: list[str] = []
    for value in values:
        if not value:
            continue
        text = str(value)
        if text in recent:
            recent.remove(text)
        recent.append(text)
    return recent[-limit:]


def _requires_new_lease(lease: dict[str, Any], run_id: str) -> bool:
    if lease.get("lease_state") != "active":
        return True
    return lease.get("run_id") not in (None, run_id)


def _read_lease(terminal_dir: Path) -> dict[str, Any]:
    path = terminal_dir / "resident_process_lease.json"
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload
