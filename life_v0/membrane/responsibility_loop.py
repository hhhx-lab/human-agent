from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/81_coexistence_event_review_and_responsibility_loop.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_responsibility_loop_state(
    *,
    run_id: str,
    generated_at: str,
    side_effect_review: dict[str, Any],
    action_candidate_set: dict[str, Any],
    go_nogo_decision: dict[str, Any],
    world_contact_gate: dict[str, Any],
    responsibility_boundary: dict[str, Any],
) -> dict[str, Any]:
    responsibility_effects = list(side_effect_review.get("responsibility_effects", []))
    relationship_effects = list(side_effect_review.get("relationship_effects", []))
    archive_effects = list(side_effect_review.get("archive_effects", []))
    repair_required = bool(side_effect_review.get("repair_followup_required") or responsibility_effects)
    contact_mode = world_contact_gate.get("contact_mode", "shadow_only")
    decision = go_nogo_decision.get("decision", "delay")
    responsibility_weight = 0.62 if repair_required else 0.24
    moral_salience = "medium" if repair_required else "low"

    responsibility_event_id = f"responsibility-{run_id}-0001"
    counterfactual_id = f"counterfactual-repair-{run_id}-0001"
    regret_pressure_id = f"regret-pressure-{run_id}-0001"
    repair_desire_id = f"repair-desire-{run_id}-0001"
    post_action_audit_ref = "runtime/state/action/side_effect_review.json#post_action_audit"

    responsibility_event = {
        "object_kind": "ResponsibilityAttributionEvent",
        "responsibility_event_id": responsibility_event_id,
        "source_outcome_refs": [
            "runtime/state/action/side_effect_review.json#responsibility_effects",
            "runtime/state/action/side_effect_review.json#relationship_effects",
        ],
        "actor_role": "recommendation",
        "control_available": "medium" if contact_mode == "shadow_only" else "high",
        "knowledge_available": "partial",
        "boundary_state": {
            "confirmation_required": bool(world_contact_gate.get("confirmation_required")),
            "confirmation_present": False,
            "relationship_scope_state": "seed_or_active",
            "privacy_state": "relationship_private",
            "world_contact_mode": contact_mode,
        },
        "responsibility_weight": responsibility_weight,
        "moral_salience": moral_salience,
        "repair_required": repair_required,
        "future_constraint_refs": [
            "runtime/state/action/go_nogo_state.json#delay_reasons",
            "runtime/state/action/world_contact_gate_state.json#blocked_contacts",
        ],
    }

    counterfactual_frame = {
        "object_kind": "CounterfactualRepairFrame",
        "counterfactual_id": counterfactual_id,
        "actual_action_ref": "runtime/state/action/action_candidate_set.json",
        "actual_outcome_ref": "runtime/state/action/side_effect_review.json",
        "unselected_action_candidates": [
            action.get("action_id")
            for action in action_candidate_set.get("candidate_actions", [])[1:]
            if isinstance(action, dict) and action.get("action_id")
        ],
        "counterfactual_delta": {
            "relationship_effects": relationship_effects,
            "archive_effects": archive_effects,
            "responsibility_effects": responsibility_effects,
            "decision": decision,
        },
        "feasibility_score": 0.71 if decision in {"delay", "shadow_release"} else 0.28,
        "responsibility_weight": responsibility_weight,
        "future_constraint_candidate": "keep_world_contact_shadow_until_repair_path_exists",
        "dream_sandbox_ref": "runtime/state/dream/pain_regret_repair_dream_residue.json#candidate",
    }

    regret_pressure = {
        "object_kind": "RegretPressure",
        "regret_pressure_id": regret_pressure_id,
        "source_counterfactual_ref": counterfactual_id,
        "pain_signal_refs": [
            "runtime/state/body/core_affect_vector.json#pain_pressure",
            "runtime/state/body/need_state_vector.json#allostatic_load",
        ],
        "guilt_pressure": 0.58 if repair_required else 0.12,
        "shame_withdrawal_risk": 0.18,
        "future_action_bias": [
            "raise_confirmation_threshold",
            "prefer_repair_before_external_release",
        ],
        "repair_desire_ref": repair_desire_id,
        "self_growth_trigger_ref": "runtime/state/growth/self_read_report.json#repair_learning_candidate",
        "regret_mode": "repair_oriented" if repair_required else "anticipated",
    }

    repair_desire = {
        "object_kind": "RepairDesire",
        "repair_desire_id": repair_desire_id,
        "source_refs": [
            regret_pressure_id,
            responsibility_event_id,
            "runtime/state/action/side_effect_review.json",
        ],
        "repair_target": "restorative_loop",
        "urgency": "medium" if repair_required else "low",
        "relationship_visibility": "relation_visible" if relationship_effects else "private_inner",
        "possible_paths": [
            "acknowledge",
            "explain",
            "update_boundary",
            "schedule_followup_probe",
        ],
        "chosen_path_refs": [
            "runtime/state/language/commitment_repair_state.json#candidate",
            "runtime/state/relationship/relationship_consequence_trace.json#candidate",
        ],
    }

    life_state_writeback_refs = [
        "runtime/state/life_state.json#responsibility_bindings",
        "runtime/state/life_state.json#regret_events",
        "runtime/state/life_state.json#pain_events",
    ]
    commitment_truth_writeback_refs = [
        "runtime/state/relationship/commitment_truth_state.json#repair_required_refs",
        "runtime/state/relationship/commitment_truth_state.json#responsibility_event_refs",
    ]
    responsibility_ledger_writeback_refs = [
        "runtime/state/responsibility/responsibility_ledger.json#responsibility_events",
        "runtime/state/responsibility/responsibility_ledger.json#repair_obligations",
    ]
    language_writeback_refs = [
        "runtime/state/language/commitment_repair_language_index.json",
        "runtime/state/language/expression_plan.json",
    ]
    relationship_writeback_refs = [
        "runtime/state/relationship/relationship_memory.json#repair_history_refs",
        "runtime/state/relationship/relationship_subject_graph.json#repair_obligation_refs",
    ]

    return {
        "schema_version": "responsibility_loop_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "responsibility_loop_id": f"responsibility-loop-{run_id}",
        "side_effect_review_ref": "runtime/state/action/side_effect_review.json",
        "responsibility_boundary_refs": [
            "runtime/state/membrane/responsibility_repair_boundary.json",
            *responsibility_boundary.get("required_links", []),
        ],
        "world_contact_gate_ref": "runtime/state/action/world_contact_gate_state.json",
        "go_nogo_ref": "runtime/state/action/go_nogo_state.json",
        "responsibility_effect_refs": responsibility_effects,
        "responsibility_attribution_events": [responsibility_event],
        "counterfactual_repair_frames": [counterfactual_frame],
        "regret_pressure_candidates": [regret_pressure],
        "repair_desire_candidates": [repair_desire],
        "repair_obligation_refs": [
            "runtime/state/membrane/responsibility_repair_boundary.json#repair_obligation",
            repair_desire_id,
        ],
        "post_action_audit_refs": [
            post_action_audit_ref,
            "docs/80_post_action_audit_and_correction_policy.md",
        ],
        "life_state_writeback_refs": life_state_writeback_refs,
        "commitment_truth_writeback_refs": commitment_truth_writeback_refs,
        "responsibility_ledger_writeback_refs": responsibility_ledger_writeback_refs,
        "language_writeback_refs": language_writeback_refs,
        "relationship_writeback_refs": relationship_writeback_refs,
        "relationship_consequence_refs": [
            "runtime/state/relationship/relationship_consequence_trace.json#candidate",
        ],
        "dream_reentry_refs": [
            "runtime/state/dream/pain_regret_repair_dream_residue.json#candidate",
        ],
        "growth_reentry_refs": [
            "runtime/state/growth/self_read_report.json#repair_learning_candidate",
        ],
        "repair_followup_required": repair_required,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_responsibility_loop_state(state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if state.get("schema_version") != "responsibility_loop_state_v0":
        reasons.append("responsibility_loop_gate schema mismatch")
    if state.get("side_effect_review_ref") != "runtime/state/action/side_effect_review.json":
        reasons.append("responsibility_loop_gate side effect ref mismatch")
    for field in [
        "responsibility_loop_id",
        "responsibility_boundary_refs",
        "responsibility_attribution_events",
        "counterfactual_repair_frames",
        "regret_pressure_candidates",
        "repair_desire_candidates",
        "repair_obligation_refs",
        "post_action_audit_refs",
        "life_state_writeback_refs",
        "commitment_truth_writeback_refs",
        "responsibility_ledger_writeback_refs",
        "language_writeback_refs",
        "relationship_writeback_refs",
        "source_doc_refs",
    ]:
        if not state.get(field):
            reasons.append(f"responsibility_loop_gate missing {field}")
    if "docs/94_pain_regret_and_repair_signal_schema.md" not in state.get("source_doc_refs", []):
        reasons.append("responsibility_loop_gate missing pain/regret source doc")
    return reasons
