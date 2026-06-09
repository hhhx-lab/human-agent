from __future__ import annotations

from pathlib import Path
from typing import Any, Callable


def detect_and_normalize_interrupted_previous_state(
    *,
    run_id: str,
    generated_at: str,
    reports_dir: Path,
    previous_safe_terminal_loop: dict[str, Any],
    previous_terminal_life_loop_state: dict[str, Any],
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> dict[str, Any] | None:
    previous_safe_mode = previous_safe_terminal_loop.get("current_mode")
    previous_terminal_mode = previous_terminal_life_loop_state.get("current_mode")
    previous_turn_status = previous_terminal_life_loop_state.get("last_turn_status")

    interrupted = (
        previous_safe_mode not in (None, "restored_waiting_for_external_turn", "blocked")
        or previous_terminal_mode not in (None, "restored_waiting_for_external_turn", "blocked")
        or previous_turn_status == "open"
    )
    if not interrupted:
        return None

    recovery_report = {
        "report_kind": "relaunch_recovery_report",
        "run_id": run_id,
        "generated_at": generated_at,
        "relaunch_recovery_kind": "interrupted_previous_process_state",
        "previous_safe_terminal_mode": previous_safe_mode,
        "previous_terminal_loop_mode": previous_terminal_mode,
        "previous_turn_status": previous_turn_status,
        "normalized_mode": "restored_waiting_for_external_turn",
        "normalized_terminal_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "normalized_safe_terminal_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
    }

    safe_terminal_loop["current_mode"] = "restored_waiting_for_external_turn"
    safe_terminal_loop["last_relaunch_recovery_status"] = "normalized_from_interrupted_previous_process_state"

    terminal_life_loop_state["current_mode"] = "restored_waiting_for_external_turn"
    terminal_life_loop_state["last_turn_status"] = "relaunch_recovered"
    terminal_life_loop_state["last_turn_mode"] = "relaunch_recovery_return"
    terminal_life_loop_state["next_required_action"] = "await_next_external_relation_turn"

    reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(reports_dir / "digital_life_process_relaunch_recovery_report.json", recovery_report)
    return recovery_report
