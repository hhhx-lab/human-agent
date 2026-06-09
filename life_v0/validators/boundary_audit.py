from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/81_coexistence_event_review_and_responsibility_loop.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_boundary_audit_state(
    *,
    run_id: str,
    generated_at: str,
    life_membrane: dict[str, Any],
    world_contact_gate: dict[str, Any],
    quarantine_index: dict[str, Any],
    responsibility_boundary: dict[str, Any],
) -> dict[str, Any]:
    audit_findings: list[str] = []
    if life_membrane.get("stage_policy") != "pre_activation_shadow_only":
        audit_findings.append("membrane_stage_policy_mismatch")
    if world_contact_gate.get("contact_mode") == "blocked":
        audit_findings.append("world_contact_blocked")
    return {
        "schema_version": "boundary_audit_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "boundary_audit_id": f"boundary-audit-{run_id}",
        "life_membrane_ref": "runtime/state/membrane/life_membrane.json",
        "world_contact_gate_ref": "runtime/state/action/world_contact_gate_state.json",
        "quarantine_refs": list(quarantine_index.get("quarantine_refs", [])),
        "responsibility_boundary_refs": [
            "runtime/state/membrane/responsibility_repair_boundary.json",
            *list(responsibility_boundary.get("required_links", []))[:1],
        ],
        "audit_findings": audit_findings,
        "blocked_reasons": [] if not audit_findings else audit_findings,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_boundary_audit_state(audit: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if audit.get("schema_version") != "boundary_audit_state_v0":
        reasons.append("boundary_audit_gate schema mismatch")
    for field in ["boundary_audit_id", "life_membrane_ref", "world_contact_gate_ref", "responsibility_boundary_refs"]:
        if not audit.get(field):
            reasons.append(f"boundary_audit_gate missing {field}")
    return reasons
