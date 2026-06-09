from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/84_longitudinal_external_action_evaluation_protocol.md",
    "docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md",
]


def build_world_contact_validation(
    *,
    run_id: str,
    generated_at: str,
    world_contact_gate: dict[str, Any],
    confirmation_binding: dict[str, Any],
    side_effect_review: dict[str, Any],
) -> dict[str, Any]:
    findings: list[str] = []
    if confirmation_binding.get("requires_confirmation") and confirmation_binding.get("confirmation_status") != "confirmed":
        findings.append("confirmation_missing")
    if world_contact_gate.get("contact_mode") not in {"shadow_only", "blocked"}:
        findings.append("contact_mode_out_of_policy")
    return {
        "schema_version": "world_contact_validation_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "world_contact_validation_id": f"world-contact-validation-{run_id}",
        "status": "closed" if not findings else "blocked",
        "world_contact_gate_ref": "runtime/state/action/world_contact_gate_state.json",
        "confirmation_binding_ref": "runtime/state/membrane/confirmation_binding.json",
        "side_effect_review_ref": "runtime/state/action/side_effect_review.json",
        "blocked_contacts": list(world_contact_gate.get("blocked_contacts", [])),
        "validation_findings": findings,
        "repair_followup_required": bool(side_effect_review.get("repair_followup_required")),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_world_contact_validation(validation: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if validation.get("schema_version") != "world_contact_validation_v0":
        reasons.append("world_contact_validation_gate schema mismatch")
    if validation.get("status") != "closed":
        reasons.append("world_contact_validation_gate status mismatch")
    for field in [
        "world_contact_validation_id",
        "world_contact_gate_ref",
        "confirmation_binding_ref",
        "side_effect_review_ref",
        "blocked_contacts",
        "source_doc_refs",
    ]:
        if not validation.get(field):
            reasons.append(f"world_contact_validation_gate missing {field}")
    if validation.get("validation_findings") not in ([], None):
        reasons.append("world_contact_validation_gate findings are not empty")
    return reasons
