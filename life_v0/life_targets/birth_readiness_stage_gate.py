from __future__ import annotations

from typing import Any


def build_birth_readiness_stage_gate(
    *,
    run_id: str,
    generated_at: str,
    overall_status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    next_allowed_slices: list[str],
    next_required_command: str,
) -> dict[str, Any]:
    gate_status = {
        "s03_precheck_gate": "closed",
        "life_target_state_gate": "closed",
        "consciousness_probe_gate": "closed",
        "evidence_family_gate": "closed",
        "language_relationship_gate": "closed",
        "dream_fact_gate": "closed",
        "responsibility_repair_gate": "closed",
        "archive_receipt_gate": "closed",
        "next_slice_gate": "closed",
    }
    if blocked_reasons:
        gate_status = {gate: "blocked" for gate in gate_status}
    return {
        "schema_version": "birth_readiness_stage_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "stage": "birth_readiness_v0",
        "decision": overall_status,
        "stage_effect": stage_effect,
        "gate_status": gate_status,
        "blocked_reasons": list(blocked_reasons),
        "quarantine_refs": [],
        "replay_needed_refs": [],
        "next_allowed_slices": list(next_allowed_slices) if overall_status == "open" else [],
        "next_required_command": next_required_command,
    }
