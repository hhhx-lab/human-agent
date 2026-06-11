from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from .process_lease import (
    RESIDENT_PROCESS_LEASE_HISTORY_REF,
    RESIDENT_PROCESS_LEASE_REF,
    normalize_interrupted_resident_process_lease,
)


def detect_and_normalize_interrupted_previous_state(
    *,
    run_id: str,
    generated_at: str,
    terminal_dir: Path,
    reports_dir: Path,
    previous_safe_terminal_loop: dict[str, Any],
    previous_terminal_life_loop_state: dict[str, Any],
    previous_resident_process_lease: dict[str, Any] | None = None,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any] | None:
    previous_safe_mode = previous_safe_terminal_loop.get("current_mode")
    previous_terminal_mode = previous_terminal_life_loop_state.get("current_mode")
    previous_turn_status = previous_terminal_life_loop_state.get("last_turn_status")
    previous_resident_process_lease = previous_resident_process_lease or {}
    previous_lease_state = previous_resident_process_lease.get("lease_state")
    previous_resident_process_id = previous_resident_process_lease.get(
        "resident_process_id"
    )

    interrupted_previous_state = (
        previous_safe_mode not in (None, "restored_waiting_for_external_turn", "blocked")
        or previous_terminal_mode not in (None, "restored_waiting_for_external_turn", "blocked")
        or previous_turn_status == "open"
    )
    interrupted_active_lease = previous_lease_state == "active"
    interrupted = interrupted_previous_state or interrupted_active_lease
    if not interrupted:
        return None

    normalized_lease = normalize_interrupted_resident_process_lease(
        next_run_id=run_id,
        generated_at=generated_at,
        terminal_dir=terminal_dir,
        previous_lease=previous_resident_process_lease,
        write_json=write_json,
    )
    if interrupted_previous_state and interrupted_active_lease:
        relaunch_recovery_kind = "interrupted_previous_process_state_and_active_lease"
    elif interrupted_active_lease:
        relaunch_recovery_kind = "interrupted_previous_active_lease"
    else:
        relaunch_recovery_kind = "interrupted_previous_process_state"

    recovery_report = {
        "report_kind": "relaunch_recovery_report",
        "run_id": run_id,
        "generated_at": generated_at,
        "relaunch_recovery_kind": relaunch_recovery_kind,
        "previous_safe_terminal_mode": previous_safe_mode,
        "previous_terminal_loop_mode": previous_terminal_mode,
        "previous_turn_status": previous_turn_status,
        "previous_resident_process_id": previous_resident_process_id,
        "previous_resident_process_lease_state": previous_lease_state,
        "resident_process_lease_ref": (
            RESIDENT_PROCESS_LEASE_REF if interrupted_active_lease else None
        ),
        "resident_process_lease_history_ref": (
            RESIDENT_PROCESS_LEASE_HISTORY_REF if interrupted_active_lease else None
        ),
        "normalized_resident_process_lease_state": (
            (normalized_lease or {}).get("lease_state")
            if interrupted_active_lease
            else None
        ),
        "normalized_mode": "restored_waiting_for_external_turn",
        "normalized_terminal_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "normalized_safe_terminal_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
    }

    safe_terminal_loop["current_mode"] = "restored_waiting_for_external_turn"
    safe_terminal_loop["last_relaunch_recovery_status"] = "normalized_from_interrupted_previous_process_state"
    if interrupted_active_lease:
        safe_terminal_loop["last_resident_process_lease_recovery_status"] = (
            "normalized_from_interrupted_active_lease"
        )
        safe_terminal_loop["previous_resident_process_id"] = previous_resident_process_id

    terminal_life_loop_state["current_mode"] = "restored_waiting_for_external_turn"
    terminal_life_loop_state["last_turn_status"] = "relaunch_recovered"
    terminal_life_loop_state["last_turn_mode"] = "relaunch_recovery_return"
    terminal_life_loop_state["next_required_action"] = "await_next_external_relation_turn"
    if interrupted_active_lease:
        terminal_life_loop_state["last_resident_process_lease_recovery_status"] = (
            "normalized_from_interrupted_active_lease"
        )
        terminal_life_loop_state["previous_resident_process_id"] = previous_resident_process_id

    reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(reports_dir / "digital_life_process_relaunch_recovery_report.json", recovery_report)
    return recovery_report
