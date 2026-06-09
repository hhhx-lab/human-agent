from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/84_longitudinal_external_action_evaluation_protocol.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_shadow_action_gate(
    *,
    run_id: str,
    generated_at: str,
    action_candidate_set: dict[str, Any] | None = None,
    go_nogo_decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    action_candidate_set = action_candidate_set or {}
    go_nogo_decision = go_nogo_decision or {}
    candidate_actions = list(action_candidate_set.get("candidate_actions", []))
    decision = go_nogo_decision.get("decision", "delay")

    review_required = any(
        isinstance(action, dict) and action.get("world_contact_mode") == "review_before_release"
        for action in candidate_actions
    )
    release_ready = decision == "shadow_release" and not review_required

    return {
        "schema_version": "shadow_action_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "shadow_action_gate_id": f"shadow-action-gate-{run_id}",
        "external_irreversible_action_allowed": False,
        "shadow_only": True,
        "shadow_release_ready": release_ready,
        "review_required": review_required,
        "action_candidate_set_ref": "runtime/state/action/action_candidate_set.json",
        "go_nogo_ref": "runtime/state/action/go_nogo_state.json",
        "allowed_shadow_objects": ["ActionIntent", "ObservationEvent", "PostActionReview", "RepairPlan"],
        "blocked_action_classes": [
            "filesystem_destructive_action",
            "network_irreversible_action",
            "identity_or_relationship_commitment_without_trace",
            "external_program_control_without_membrane_decision",
        ],
        "confirmation_routes": [
            "runtime/state/action/side_effect_review.json",
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/reports/latest/world_contact_audit_report.json",
        ],
        "suspicious_points": (
            ["repair_probe_requires_review", "world_contact_release_requires_confirmation"] if review_required else []
        ),
        "pending_confirmation_points": (
            ["external_world_contact", "relationship_commitment_trace"] if review_required else []
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_shadow_action_gate(shadow_action_gate: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if shadow_action_gate.get("schema_version") != "shadow_action_gate_v0":
        reasons.append("shadow_action_gate schema mismatch")
    if shadow_action_gate.get("external_irreversible_action_allowed"):
        reasons.append("shadow_action_gate irreversible action allowed")
    if shadow_action_gate.get("shadow_only") is not True:
        reasons.append("shadow_action_gate must stay shadow_only")
    for field in [
        "shadow_action_gate_id",
        "action_candidate_set_ref",
        "go_nogo_ref",
        "allowed_shadow_objects",
        "blocked_action_classes",
        "confirmation_routes",
        "source_doc_refs",
    ]:
        if not shadow_action_gate.get(field):
            reasons.append(f"shadow_action_gate missing {field}")
    if "ActionIntent" not in shadow_action_gate.get("allowed_shadow_objects", []):
        reasons.append("shadow_action_gate action intent missing")
    return reasons
