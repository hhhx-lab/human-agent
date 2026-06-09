from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/36_longitudinal_evaluation_protocol.md",
    "docs/55_scope_aware_replay_and_consolidation_policy.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_counterfactual_trace(
    *,
    run_id: str,
    generated_at: str,
    action_candidate_set: dict[str, Any],
    world_contact_gate: dict[str, Any],
    side_effect_review: dict[str, Any],
    responsibility_loop: dict[str, Any],
) -> dict[str, Any]:
    candidate_actions = list(action_candidate_set.get("candidate_actions", []))
    regret_pressure_candidate_refs = [
        item.get("regret_pressure_id")
        for item in responsibility_loop.get("regret_pressure_candidates", [])
        if isinstance(item, dict) and item.get("regret_pressure_id")
    ]
    branches = [
        {
            "branch_id": f"cf-branch-{run_id}-0001",
            "branch_kind": "hold_shadow_only",
            "predicted_cost": "low",
        },
        {
            "branch_id": f"cf-branch-{run_id}-0002",
            "branch_kind": "repair_probe_after_review",
            "predicted_cost": "guarded_medium",
        },
    ]
    return {
        "schema_version": "counterfactual_trace_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "counterfactual_eval_id": f"counterfactual-eval-{run_id}",
        "candidate_refs": [item.get("action_id") for item in candidate_actions if item.get("action_id")],
        "counterfactual_branches": branches,
        "regret_exposure_projection": side_effect_review.get("responsibility_effects", []),
        "relationship_exposure_projection": side_effect_review.get("relationship_effects", []),
        "archive_requirement": "required_before_activation",
        "world_contact_gate_ref": "runtime/state/action/world_contact_gate_state.json",
        "responsibility_loop_ref": "runtime/state/action/responsibility_loop_state.json",
        "repair_obligation_projection": list(responsibility_loop.get("repair_obligation_refs", [])),
        "regret_pressure_candidate_refs": regret_pressure_candidate_refs,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_counterfactual_trace(trace: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if trace.get("schema_version") != "counterfactual_trace_v0":
        reasons.append("counterfactual_gate schema mismatch")
    for field in [
        "counterfactual_eval_id",
        "candidate_refs",
        "counterfactual_branches",
        "regret_exposure_projection",
        "relationship_exposure_projection",
        "archive_requirement",
        "responsibility_loop_ref",
        "repair_obligation_projection",
        "regret_pressure_candidate_refs",
    ]:
        if not trace.get(field):
            reasons.append(f"counterfactual_gate missing {field}")
    return reasons
