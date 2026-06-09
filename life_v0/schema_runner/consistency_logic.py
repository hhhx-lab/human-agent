from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/22_state_transition_and_threshold_model.md",
    "docs/53_runner_integration_plan.md",
    "docs/65_schema_cross_ref_checker_design.md",
    "docs/153_life_reality_full_archive_cross_file_checker_rollup_plan.md",
    "docs/v0/code_framework/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_consistency_logic(
    *,
    run_id: str,
    generated_at: str,
    action_candidate_set: dict[str, Any],
    observation_truth_review: dict[str, Any],
    boundary_audit: dict[str, Any],
) -> dict[str, Any]:
    inconsistency_findings: list[str] = []
    if not action_candidate_set.get("candidate_actions"):
        inconsistency_findings.append("candidate_action_missing")
    if observation_truth_review.get("missing_fields"):
        inconsistency_findings.append("observation_truth_missing_fields")
    return {
        "schema_version": "consistency_logic_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "consistency_logic_id": f"consistency-logic-{run_id}",
        "state_refs": [
            "runtime/state/action/action_candidate_set.json",
            "runtime/state/validation/observation_truth_review.json",
            "runtime/state/validation/boundary_audit_state.json",
        ],
        "comparison_axes": [
            "observation_to_prediction",
            "prediction_to_action_candidate",
            "world_contact_to_boundary_audit",
        ],
        "inconsistency_findings": inconsistency_findings,
        "severity": "guarded_low" if not inconsistency_findings else "guarded_medium",
        "repair_route_refs": [
            "runtime/state/validation/boundary_audit_state.json",
            "runtime/state/action/world_contact_gate_state.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_consistency_logic(state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if state.get("schema_version") != "consistency_logic_v0":
        reasons.append("consistency_logic_gate schema mismatch")
    for field in ["consistency_logic_id", "state_refs", "comparison_axes", "severity", "repair_route_refs"]:
        if not state.get(field):
            reasons.append(f"consistency_logic_gate missing {field}")
    return reasons
