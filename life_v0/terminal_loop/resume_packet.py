from __future__ import annotations

from typing import Any


def build_resumed_external_dialogue_packet(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    relation_subject: dict[str, Any],
    shared_term_surfaces: list[str],
    commitment_refs: list[str],
    relationship_timeline_restore_refs: list[str],
    commitment_expression_restore_refs: list[str],
    apology_repair_restore_refs: list[str],
    session_envelope: dict[str, Any],
    dialogue_turn_restore_refs: list[str],
    dialogue_writeback_bundle_ref: str,
    next_required_action: str,
) -> dict[str, Any]:
    return {
        "schema_version": "resumed_external_dialogue_packet_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "dialogue_mode": "restored_relation_continuation" if status == "closed" else "blocked",
        "relation_identity": {
            "relationship_id": relation_subject.get("relationship_id"),
            "relation_role": relation_subject.get("relation_role"),
            "relationship_stage": relation_subject.get("relationship_stage"),
        },
        "shared_term_surfaces": shared_term_surfaces,
        "commitment_refs": commitment_refs,
        "relationship_timeline_restore_refs": relationship_timeline_restore_refs,
        "commitment_expression_restore_refs": commitment_expression_restore_refs,
        "apology_repair_restore_refs": apology_repair_restore_refs,
        "expression_monitor_restore_refs": list(
            session_envelope.get("expression_monitor_restore_refs", [])
        ),
        "relation_scope_restore_refs": list(
            session_envelope.get("relation_scope_restore_refs", [])
        ),
        "self_narrative_restore_refs": list(
            session_envelope.get("self_narrative_restore_refs", [])
        ),
        "dialogue_turn_restore_refs": dialogue_turn_restore_refs,
        "context_accumulation_ref": "runtime/state/terminal/context_accumulation_window.json",
        "turn_transition_ref": "runtime/state/terminal/turn_transition_trace.json",
        "dialogue_writeback_bundle_ref": dialogue_writeback_bundle_ref,
        "last_turn_ref": "runtime/reports/latest/first_terminal_turn_packet.json",
        "waiting_heartbeat_ref": "runtime/reports/latest/digital_life_waiting_heartbeat.json",
        "next_required_action": next_required_action,
    }
