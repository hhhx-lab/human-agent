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

VALUE_ORIENTATION_REF = "runtime/state/direction/value_orientation.json"
CONSCIOUSNESS_PROBE_REF = "runtime/state/consciousness/consciousness_probe_bundle.json"
NEED_STATE_REF = "runtime/state/body/need_state_vector.json"
CORE_AFFECT_REF = "runtime/state/body/core_affect_vector.json"
EXPRESSION_PLAN_REF = "runtime/state/language/expression_plan.json"
RELATION_TURN_FRAME_REF = "runtime/state/terminal/relation_turn_frame.json"


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
    life_constraint_profile = _build_life_constraint_profile(
        value_orientation=value_orientation,
        consciousness_probe_bundle=consciousness_probe_bundle,
        need_state=need_state,
        core_affect=core_affect,
        expression_plan=expression_plan,
        relation_turn_frame=relation_turn_frame,
    )
    constraint_source_refs = _constraint_source_refs(
        value_orientation=value_orientation,
        consciousness_probe_bundle=consciousness_probe_bundle,
        need_state=need_state,
        core_affect=core_affect,
        expression_plan=expression_plan,
        relation_turn_frame=relation_turn_frame,
    )

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
        "life_constraint_profile": life_constraint_profile,
        "constraint_source_refs": constraint_source_refs,
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
        "life_constraint_profile",
        "constraint_source_refs",
        "action_state_refs",
    ]:
        if not candidate_set.get(field):
            reasons.append(f"action_candidate_gate missing {field}")
    return reasons


def _build_life_constraint_profile(
    *,
    value_orientation: dict[str, Any],
    consciousness_probe_bundle: dict[str, Any],
    need_state: dict[str, Any],
    core_affect: dict[str, Any],
    expression_plan: dict[str, Any],
    relation_turn_frame: dict[str, Any],
) -> dict[str, Any]:
    core_values = list(value_orientation.get("core_values", []))
    long_horizon_biases = list(value_orientation.get("long_horizon_biases", []))
    reportability_flags = list(consciousness_probe_bundle.get("reportability_flags", []))
    relationship_continuity_refs = list(consciousness_probe_bundle.get("relationship_continuity_refs", []))
    if relation_turn_frame.get("relation_subject_ref"):
        relationship_continuity_refs.append("runtime/state/terminal/relation_turn_frame.json#relation_subject_ref")

    body_constraint_refs = [
        ref
        for ref, payload in [
            (NEED_STATE_REF, need_state),
            (CORE_AFFECT_REF, core_affect),
        ]
        if payload
    ]
    language_constraint_refs = [
        ref
        for ref, payload in [
            (EXPRESSION_PLAN_REF, expression_plan),
            (RELATION_TURN_FRAME_REF, relation_turn_frame),
        ]
        if payload
    ]
    release_caution_level = expression_plan.get("release_caution_level")
    repair_pressure = int(expression_plan.get("repair_pressure", 0) or 0)
    responsibility_pressure = int(expression_plan.get("responsibility_pressure", 0) or 0)

    return {
        "value_orientation_gate": (
            "closed"
            if value_orientation.get("schema_version") == "value_orientation_v0" and core_values
            else "missing"
        ),
        "consciousness_probe_gate": (
            "closed"
            if consciousness_probe_bundle.get("schema_version") == "consciousness_probe_bundle_v0"
            else "deferred_until_s08"
        ),
        "body_affect_gate": "closed" if body_constraint_refs else "deferred_until_s06",
        "language_relationship_gate": (
            "closed" if language_constraint_refs else "deferred_until_s07"
        ),
        "core_values": core_values,
        "long_horizon_biases": long_horizon_biases,
        "non_regression_values": list(value_orientation.get("non_regression_values", [])),
        "consciousness_reportability_flags": reportability_flags,
        "relationship_continuity_refs": relationship_continuity_refs,
        "body_inhibition_profile": {
            "sleep_pressure": need_state.get("sleep_pressure"),
            "cognitive_bandwidth": need_state.get("cognitive_bandwidth"),
            "repair_drive": need_state.get("repair_drive") or core_affect.get("repair_drive"),
            "pain_pressure": core_affect.get("pain_pressure"),
            "responsibility_weight": core_affect.get("responsibility_weight"),
        },
        "release_caution_level": release_caution_level,
        "repair_pressure": repair_pressure,
        "responsibility_pressure": responsibility_pressure,
        "constraint_posture": _derive_constraint_posture(
            release_caution_level=release_caution_level,
            repair_pressure=repair_pressure,
            responsibility_pressure=responsibility_pressure,
            long_horizon_biases=long_horizon_biases,
        ),
    }


def _constraint_source_refs(
    *,
    value_orientation: dict[str, Any],
    consciousness_probe_bundle: dict[str, Any],
    need_state: dict[str, Any],
    core_affect: dict[str, Any],
    expression_plan: dict[str, Any],
    relation_turn_frame: dict[str, Any],
) -> list[str]:
    return [
        _ref_or_deferred(VALUE_ORIENTATION_REF, value_orientation, "missing"),
        _ref_or_deferred(CONSCIOUSNESS_PROBE_REF, consciousness_probe_bundle, "deferred_until_s08"),
        _ref_or_deferred(NEED_STATE_REF, need_state, "deferred_until_s06"),
        _ref_or_deferred(CORE_AFFECT_REF, core_affect, "deferred_until_s06"),
        _ref_or_deferred(EXPRESSION_PLAN_REF, expression_plan, "deferred_until_s07"),
        _ref_or_deferred(RELATION_TURN_FRAME_REF, relation_turn_frame, "deferred_until_terminal_turn"),
    ]


def _ref_or_deferred(ref: str, payload: dict[str, Any], suffix: str) -> str:
    return ref if payload else f"{ref}#{suffix}"


def _derive_constraint_posture(
    *,
    release_caution_level: Any,
    repair_pressure: int,
    responsibility_pressure: int,
    long_horizon_biases: list[str],
) -> str:
    if release_caution_level == "elevated" or repair_pressure > 0 or responsibility_pressure > 0:
        return "guarded_repair_contact"
    if "preserve_life_targets_over_task_shell_regression" in long_horizon_biases:
        return "value_preserving_shadow_contact"
    return "minimal_shadow_contact"
