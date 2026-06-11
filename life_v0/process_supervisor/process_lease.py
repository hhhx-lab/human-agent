from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


RESIDENT_PROCESS_LEASE_REF = "runtime/state/terminal/resident_process_lease.json"
RESIDENT_PROCESS_LEASE_HISTORY_REF = "runtime/state/terminal/resident_process_lease_history.jsonl"
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
    return lease


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
