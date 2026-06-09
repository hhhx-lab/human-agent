from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/06_action_reward_inhibition.md",
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/81_coexistence_event_review_and_responsibility_loop.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_action_candidate_set(
    *,
    run_id: str,
    generated_at: str,
    prediction_workspace: dict[str, Any],
    expression_plan: dict[str, Any],
    relation_turn_frame: dict[str, Any],
    need_state: dict[str, Any],
    core_affect: dict[str, Any],
    value_orientation: dict[str, Any],
    consciousness_probe_bundle: dict[str, Any],
    life_state: dict[str, Any],
) -> dict[str, Any]:
    candidate_explanations = list(prediction_workspace.get("workspace_contents", {}).get("candidate_explanations", []))
    semantic_goal = expression_plan.get("semantic_goal") or "continuity_hold"
    repair_pressure = int(expression_plan.get("repair_pressure", 0))
    world_contact_needed = repair_pressure > 0 or bool(candidate_explanations)
    relationship_subjects = list(life_state.get("relationship_subjects", []))
    responsibility_bindings = list(life_state.get("responsibility_bindings", []))

    candidate_actions = [
        {
            "action_id": f"action-candidate-{run_id}-0001",
            "action_kind": "observe_and_clarify",
            "semantic_goal": semantic_goal,
            "world_contact_mode": "observation_only",
        },
        {
            "action_id": f"action-candidate-{run_id}-0002",
            "action_kind": "shadow_relationship_reply",
            "semantic_goal": "relationship_continuity",
            "world_contact_mode": "shadow_only",
        },
    ]
    if world_contact_needed:
        candidate_actions.append(
            {
                "action_id": f"action-candidate-{run_id}-0003",
                "action_kind": "repair_probe",
                "semantic_goal": "repair_review",
                "world_contact_mode": "review_before_release",
            }
        )

    return {
        "schema_version": "action_candidate_set_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "action_candidate_set_id": f"action-candidate-set-{run_id}",
        "candidate_actions": candidate_actions,
        "world_contact_needed": world_contact_needed,
        "go_nogo_state": "review_required" if world_contact_needed else "shadow_hold",
        "responsibility_projection": [
            "runtime/state/membrane/responsibility_repair_boundary.json",
            *responsibility_bindings[:1],
        ],
        "side_effect_projection": [
            "external_irreversible_action_blocked",
            "relationship_commitment_requires_review",
        ],
        "relationship_consequence_projection": [
            "relationship_subject_continuity" if relationship_subjects else "relation_scope_seed_only",
            "repair_trace_review_required" if repair_pressure else "no_repair_pressure",
        ],
        "action_state_refs": [
            "runtime/state/action/action_candidate_set.json",
            "runtime/state/action/go_nogo_state.json",
            "runtime/state/action/world_contact_gate_state.json",
            "runtime/state/action/side_effect_review.json",
        ],
        "input_refs": {
            "prediction_workspace_ref": "runtime/state/prediction/prediction_workspace_frame.json",
            "expression_plan_ref": (
                "runtime/state/language/expression_plan.json" if expression_plan else "runtime/state/language/expression_plan.json#unavailable"
            ),
            "relation_turn_frame_ref": (
                "runtime/state/terminal/relation_turn_frame.json"
                if relation_turn_frame
                else "runtime/state/terminal/relation_turn_frame.json#unavailable"
            ),
            "need_state_ref": (
                "runtime/state/body/need_state_vector.json" if need_state else "runtime/state/body/need_state_vector.json#unavailable"
            ),
            "core_affect_ref": (
                "runtime/state/body/core_affect_vector.json" if core_affect else "runtime/state/body/core_affect_vector.json#unavailable"
            ),
            "value_orientation_ref": "runtime/state/direction/value_orientation.json",
            "consciousness_probe_ref": (
                "runtime/state/consciousness/consciousness_probe_bundle.json"
                if consciousness_probe_bundle
                else "runtime/state/consciousness/consciousness_probe_bundle.json#unavailable"
            ),
        },
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_action_candidate_set(candidate_set: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if candidate_set.get("schema_version") != "action_candidate_set_v0":
        reasons.append("action_candidate_gate schema mismatch")
    for field in [
        "action_candidate_set_id",
        "candidate_actions",
        "responsibility_projection",
        "side_effect_projection",
        "relationship_consequence_projection",
        "action_state_refs",
    ]:
        if not candidate_set.get(field):
            reasons.append(f"action_candidate_gate missing {field}")
    return reasons
