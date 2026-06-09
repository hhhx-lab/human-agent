from __future__ import annotations

from typing import Any


LAST_DIALOGUE_PACKET_REF = "runtime/reports/latest/resumed_external_dialogue_packet.json"


def build_persistent_wait_bridge(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    safe_terminal_loop: dict[str, Any],
    last_dialogue_packet_ref: str = LAST_DIALOGUE_PACKET_REF,
) -> dict[str, Any]:
    return {
        **safe_terminal_loop,
        "schema_version": safe_terminal_loop.get(
            "schema_version", "safe_terminal_loop_state_v0"
        ),
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_mode": "restored_waiting_for_external_turn"
        if status == "closed"
        else "blocked",
        "last_completed_turn_mode": "resumed_external_dialogue_loop"
        if status == "closed"
        else "blocked",
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
    }
