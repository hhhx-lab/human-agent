from __future__ import annotations

from typing import Any


def build_terminal_life_loop_state(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    next_required_action: str,
) -> dict[str, Any]:
    return {
        "schema_version": "terminal_life_loop_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_mode": "restored_waiting_for_external_turn" if status == "closed" else "blocked",
        "last_turn_status": status,
        "last_turn_mode": "resumed_external_dialogue_loop" if status == "closed" else "blocked",
        "last_dialogue_packet_ref": "runtime/reports/latest/resumed_external_dialogue_packet.json",
        "dialogue_writeback_bundle_ref": "runtime/reports/latest/dialogue_writeback_bundle.json",
        "context_accumulation_ref": "runtime/state/terminal/context_accumulation_window.json",
        "turn_transition_ref": "runtime/state/terminal/turn_transition_trace.json",
        "next_required_action": next_required_action,
    }
