from __future__ import annotations

import json
from typing import Any

from life_v0.growth.offline_learning_profile import (
    derive_offline_learning_profile,
    normalize_offline_learning_cumulative_profile,
)
from life_v0.membrane.queue_e_signals import (
    build_queue_e_repair_modulation_profile,
)


def build_commitment_expression_plan(
    *,
    run_id: str,
    generated_at: str,
    expression_plan: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    commitment_truth_state: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    responsibility_loop_state: dict[str, Any],
    relationship_timeline: dict[str, Any],
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    repair_refs = list(commitment_repair_index.get("repair_obligation_refs", []))
    commitment_refs = list(commitment_repair_index.get("commitment_refs", []))
    responsibility_event_refs = list(responsibility_ledger.get("responsibility_event_refs", []))
    regret_refs = list(commitment_repair_index.get("regret_trace_refs", []))
    relationship_injury_refs = [
        f"runtime/state/relationship/relationship_timeline.json#{item.get('relationship_injury_id')}"
        for item in relationship_timeline.get("relationship_injury_traces", [])
        if isinstance(item, dict) and item.get("relationship_injury_id")
    ]
    act_type_order = [
        "clarify",
        "commitment",
        "boundary_statement",
        "apology",
        "followup_commitment",
    ]

    language_act_candidates = [
        {
            "act_id": f"commitment-act-{run_id}-0001",
            "act_type": "clarify",
            "goal_code": "clarify_shared_language_and_current_commitment",
            "trigger_refs": ["runtime/state/language/expression_plan.json#semantic_goal"],
        },
        {
            "act_id": f"commitment-act-{run_id}-0002",
            "act_type": "commitment",
            "goal_code": "restate_open_commitment_with_traceable_followup_window",
            "trigger_refs": commitment_refs or ["runtime/state/language/commitment_repair_language_index.json#commitment_refs"],
        },
    ]
    if repair_refs or regret_refs or relationship_injury_refs:
        language_act_candidates.append(
            {
                "act_id": f"commitment-act-{run_id}-0003",
                "act_type": "apology",
                "goal_code": "responsibility_first_apology_with_repair_intent",
                "trigger_refs": repair_refs + regret_refs + relationship_injury_refs,
            }
        )
        language_act_candidates.append(
            {
                "act_id": f"commitment-act-{run_id}-0004",
                "act_type": "followup_commitment",
                "goal_code": "next_turn_probe_for_repair_and_commitment_realization",
                "trigger_refs": responsibility_event_refs or ["runtime/state/responsibility/responsibility_ledger.json#responsibility_events"],
            }
        )

    plan = {
        "schema_version": "commitment_expression_plan_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "semantic_goal": expression_plan.get("semantic_goal", "repair_commitment_shared_language"),
        "delay_or_release_decision": expression_plan.get("delay_or_release_decision", "delay_for_clarification"),
        "repair_pressure": expression_plan.get("repair_pressure", 0),
        "responsibility_pressure": expression_plan.get("responsibility_pressure", 0),
        "act_type_order": act_type_order,
        "language_act_candidates": language_act_candidates,
        "repair_obligation_refs": repair_refs,
        "commitment_truth_refs": list(commitment_truth_state.get("open_commitment_refs", [])) or commitment_refs,
        "responsibility_event_refs": responsibility_event_refs,
        "regret_trace_refs": regret_refs,
        "relationship_injury_refs": relationship_injury_refs,
        "relationship_timeline_ref": "runtime/state/relationship/relationship_timeline.json",
        "responsibility_loop_ref": "runtime/state/action/responsibility_loop_state.json",
        "commitment_repair_index_ref": "runtime/state/language/commitment_repair_language_index.json",
        "source_doc_refs": source_doc_refs,
        "counterfactual_repair_refs": [
            item.get("counterfactual_id")
            for item in responsibility_loop_state.get("counterfactual_repair_frames", [])
            if isinstance(item, dict) and item.get("counterfactual_id")
        ],
    }
    plan = project_commitment_expression_plan_with_queue_e_repair_modulation(
        commitment_expression_plan=plan,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    return project_commitment_expression_plan_with_offline_learning(
        commitment_expression_plan=plan,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
    )


def project_commitment_expression_plan_with_queue_e_repair_modulation(
    *,
    commitment_expression_plan: dict[str, Any],
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not commitment_expression_plan:
        return {}
    repair_profile = build_queue_e_repair_modulation_profile(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    if repair_profile["pressure_level"] == "quiet" and not repair_profile["ref_set"]:
        return commitment_expression_plan

    updated = json.loads(json.dumps(commitment_expression_plan))
    ref_set = list(repair_profile.get("ref_set", []))
    pressure_level = str(repair_profile.get("pressure_level") or "quiet")

    candidates = list(updated.get("language_act_candidates", []))
    if pressure_level in {"urgent", "elevated"} and not _has_item_type(
        candidates,
        "responsibility_repair_modulation",
        "act_type",
    ):
        candidates.append(
            {
                "act_id": f"commitment-act-{updated.get('run_id', 'queue-e')}-repair-modulation",
                "act_type": "responsibility_repair_modulation",
                "goal_code": "modulate_commitment_expression_with_responsibility_pressure",
                "trigger_refs": ref_set,
            }
        )
    updated["language_act_candidates"] = candidates

    act_type_order = list(updated.get("act_type_order", []))
    if (
        pressure_level in {"urgent", "elevated"}
        and "responsibility_repair_modulation" not in act_type_order
    ):
        try:
            followup_index = act_type_order.index("followup_commitment")
        except ValueError:
            act_type_order.append("responsibility_repair_modulation")
        else:
            act_type_order.insert(followup_index, "responsibility_repair_modulation")
    updated["act_type_order"] = _dedupe(act_type_order)

    if pressure_level == "urgent":
        updated["queue_e_commitment_tempo_mode"] = "responsibility_lock_first"
        updated["delay_or_release_decision"] = "hold_for_responsibility_repair_lock"
    elif pressure_level == "elevated":
        updated["queue_e_commitment_tempo_mode"] = "responsibility_repair_guarded"

    updated["queue_e_repair_modulation_profile"] = repair_profile
    updated["queue_e_repair_pressure_level"] = pressure_level
    updated["queue_e_repair_attention_target"] = repair_profile["attention_target"]
    updated["queue_e_repair_ref_set"] = ref_set
    return updated


def project_commitment_expression_plan_with_offline_learning(
    *,
    commitment_expression_plan: dict[str, Any],
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not commitment_expression_plan:
        return {}

    updated = json.loads(json.dumps(commitment_expression_plan))
    offline_profile = derive_offline_learning_profile(
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    ref_set = list(offline_profile.get("offline_learning_ref_set", []))
    if not ref_set:
        return project_commitment_expression_plan_with_cumulative_offline_learning(
            commitment_expression_plan=updated,
            offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        )

    relationship_targets = list((relationship_learning_plan or {}).get("relationship_targets", []))
    language_targets = list((language_learning_plan or {}).get("language_targets", []))
    belief_targets = list((belief_learning_plan or {}).get("belief_targets", []))
    rewrite_required = bool((nightmare_risk or {}).get("rewrite_required"))
    boundary_hold_required = (
        (relationship_learning_plan or {}).get("world_contact_release_posture")
        == "confirmation_blocked"
        or "confirmation_locked_expression_restraint" in language_targets
    )
    paced_reentry_required = any(
        target in relationship_targets
        for target in [
            "repair_reentry_timing_adjustment",
            "relationship_pacing_adjustment",
            "repair_timing_adjustment",
        ]
    )

    candidates = list(updated.get("language_act_candidates", []))
    if boundary_hold_required and not _has_item_type(candidates, "boundary_statement", "act_type"):
        candidates.append(
            {
                "act_id": f"commitment-act-{updated.get('run_id', 'offline')}-offline-boundary",
                "act_type": "boundary_statement",
                "goal_code": "declare_boundary_and_release_conditions_before_reentry",
                "trigger_refs": ref_set,
            }
        )
    if paced_reentry_required and not _has_item_type(candidates, "paced_reentry", "act_type"):
        candidates.append(
            {
                "act_id": f"commitment-act-{updated.get('run_id', 'offline')}-offline-paced-reentry",
                "act_type": "paced_reentry",
                "goal_code": "slow_reentry_then_confirm_window_before_realization",
                "trigger_refs": ref_set,
            }
        )
    updated["language_act_candidates"] = candidates

    act_type_order = list(updated.get("act_type_order", []))
    if paced_reentry_required and "paced_reentry" not in act_type_order:
        try:
            followup_index = act_type_order.index("followup_commitment")
        except ValueError:
            act_type_order.append("paced_reentry")
        else:
            act_type_order.insert(followup_index, "paced_reentry")
    updated["act_type_order"] = _dedupe(act_type_order)

    if rewrite_required:
        updated["delay_or_release_decision"] = "hold_for_nightmare_rewrite_integration"
    elif boundary_hold_required:
        updated["delay_or_release_decision"] = "hold_for_boundary_confirmation"

    if boundary_hold_required:
        tempo_mode = "confirmation_locked_restraint"
    elif paced_reentry_required:
        tempo_mode = "paced_reentry_guarded"
    elif offline_profile["offline_learning_pressure_level"] in {"urgent", "elevated"}:
        tempo_mode = "offline_learning_guarded"
    else:
        tempo_mode = "baseline"

    updated["commitment_tempo_mode"] = tempo_mode
    updated["offline_learning_pressure_level"] = offline_profile[
        "offline_learning_pressure_level"
    ]
    updated["offline_learning_attention_target"] = offline_profile[
        "offline_learning_attention_target"
    ]
    updated["offline_learning_priority_profile"] = offline_profile[
        "offline_learning_priority_profile"
    ]
    updated["offline_learning_ref_set"] = ref_set
    updated["offline_learning_targets"] = _dedupe(
        relationship_targets + language_targets + belief_targets
    )
    return project_commitment_expression_plan_with_cumulative_offline_learning(
        commitment_expression_plan=updated,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
    )


def project_commitment_expression_plan_with_cumulative_offline_learning(
    *,
    commitment_expression_plan: dict[str, Any],
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not commitment_expression_plan:
        return {}
    cumulative_profile = normalize_offline_learning_cumulative_profile(
        offline_learning_cumulative_profile
    )
    if not cumulative_profile:
        return commitment_expression_plan

    updated = json.loads(json.dumps(commitment_expression_plan))
    ref_set = list(cumulative_profile.get("ref_set", []))
    pressure_level = str(cumulative_profile.get("pressure_level") or "quiet")
    attention_target = str(
        cumulative_profile.get("attention_target")
        or "baseline_offline_learning_maintenance"
    )
    generation = int(cumulative_profile.get("generation") or 0)
    relationship_reconsolidation_required = (
        generation >= 2
        and pressure_level in {"urgent", "elevated"}
        and attention_target == "relationship_learning_plan"
    )

    candidates = list(updated.get("language_act_candidates", []))
    if pressure_level in {"urgent", "elevated"} and not _has_item_type(
        candidates,
        "cumulative_offline_learning_integration",
        "act_type",
    ):
        candidates.append(
            {
                "act_id": f"commitment-act-{updated.get('run_id', 'offline')}-cumulative-offline",
                "act_type": "cumulative_offline_learning_integration",
                "goal_code": "integrate_cross_wake_dream_growth_pressure_into_commitment_expression",
                "trigger_refs": ref_set,
            }
        )
    if relationship_reconsolidation_required and not _has_item_type(
        candidates,
        "relationship_offline_reconsolidation",
        "act_type",
    ):
        candidates.append(
            {
                "act_id": f"commitment-act-{updated.get('run_id', 'offline')}-relationship-reconsolidation",
                "act_type": "relationship_offline_reconsolidation",
                "goal_code": "reconsolidate_relationship_learning_before_followup_realization",
                "trigger_refs": ref_set,
            }
        )
    updated["language_act_candidates"] = candidates

    act_type_order = list(updated.get("act_type_order", []))
    if (
        pressure_level in {"urgent", "elevated"}
        and "cumulative_offline_learning_integration" not in act_type_order
    ):
        try:
            followup_index = act_type_order.index("followup_commitment")
        except ValueError:
            act_type_order.append("cumulative_offline_learning_integration")
        else:
            act_type_order.insert(
                followup_index,
                "cumulative_offline_learning_integration",
            )
    if relationship_reconsolidation_required:
        act_type_order = _insert_before_any(
            act_type_order,
            "relationship_offline_reconsolidation",
            [
                "cumulative_offline_learning_integration",
                "followup_commitment",
            ],
        )
    updated["act_type_order"] = _dedupe(act_type_order)

    if relationship_reconsolidation_required:
        updated["cumulative_commitment_tempo_mode"] = (
            "relationship_offline_reconsolidation_first"
        )
        if _can_replace_delay_decision(updated.get("delay_or_release_decision")):
            updated["delay_or_release_decision"] = (
                "hold_for_relationship_offline_reconsolidation"
            )
    elif pressure_level in {"urgent", "elevated"}:
        updated["cumulative_commitment_tempo_mode"] = (
            "cumulative_offline_learning_guarded"
        )
        if _can_replace_delay_decision(updated.get("delay_or_release_decision")):
            updated["delay_or_release_decision"] = (
                "hold_for_cumulative_offline_learning_integration"
            )

    updated["offline_learning_cumulative_projection"] = {
        "schema_version": cumulative_profile["schema_version"],
        "generation": generation,
        "pressure_level": pressure_level,
        "attention_target": attention_target,
        "priority_profile": dict(cumulative_profile.get("priority_profile", {})),
        "ref_set": ref_set,
    }
    updated["offline_learning_cumulative_generation"] = generation
    updated["offline_learning_cumulative_pressure_level"] = pressure_level
    updated["offline_learning_cumulative_attention_target"] = attention_target
    updated["offline_learning_cumulative_ref_set"] = ref_set
    return updated


def _has_item_type(items: list[dict[str, Any]], expected: str, field: str) -> bool:
    return any(isinstance(item, dict) and item.get(field) == expected for item in items)


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def _insert_before_any(order: list[str], item: str, anchors: list[str]) -> list[str]:
    if item in order:
        return _dedupe(order)
    for anchor in anchors:
        if anchor in order:
            order.insert(order.index(anchor), item)
            return _dedupe(order)
    order.append(item)
    return _dedupe(order)


def _can_replace_delay_decision(value: Any) -> bool:
    return value in {
        None,
        "",
        "baseline",
        "release",
        "delay_for_clarification",
        "hold_for_cumulative_offline_learning_integration",
    }
