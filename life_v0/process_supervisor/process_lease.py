from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


RESIDENT_PROCESS_LEASE_REF = "runtime/state/terminal/resident_process_lease.json"
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
        "process_report_ref": None,
    }
    write_json(terminal_dir / "resident_process_lease.json", lease)
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
    if not lease:
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
    write_json(terminal_dir / "resident_process_lease.json", lease)
    return lease


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
    lease["process_report_ref"] = PROCESS_REPORT_REF
    write_json(terminal_dir / "resident_process_lease.json", lease)
    return lease


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
