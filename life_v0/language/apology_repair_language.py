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


def build_apology_repair_language_trace(
    *,
    run_id: str,
    generated_at: str,
    responsibility_loop_state: dict[str, Any],
    relationship_timeline: dict[str, Any],
    commitment_expression_plan: dict[str, Any],
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    regret_refs = [
        item.get("regret_pressure_id")
        for item in responsibility_loop_state.get("regret_pressure_candidates", [])
        if isinstance(item, dict) and item.get("regret_pressure_id")
    ]
    responsibility_event_refs = [
        item.get("responsibility_event_id")
        for item in responsibility_loop_state.get("responsibility_attribution_events", [])
        if isinstance(item, dict) and item.get("responsibility_event_id")
    ]
    relationship_injury_refs = [
        f"runtime/state/relationship/relationship_timeline.json#{item.get('relationship_injury_id')}"
        for item in relationship_timeline.get("relationship_injury_traces", [])
        if isinstance(item, dict) and item.get("relationship_injury_id")
    ]
    repair_obligation_refs = list(responsibility_loop_state.get("repair_obligation_refs", []))
    move_type_order = [
        "acknowledge_harm",
        "take_responsibility",
        "apology",
        "boundary_repair",
        "followup_commitment",
    ]

    repair_language_moves = [
        {
            "move_id": f"repair-move-{run_id}-0001",
            "move_type": "acknowledge_harm",
            "goal_code": "acknowledge_relationship_harm_and_open_pressure",
            "trigger_refs": relationship_injury_refs or repair_obligation_refs,
        },
        {
            "move_id": f"repair-move-{run_id}-0002",
            "move_type": "take_responsibility",
            "goal_code": "take_responsibility_without_deflecting_into_explanation",
            "trigger_refs": responsibility_event_refs,
        },
        {
            "move_id": f"repair-move-{run_id}-0003",
            "move_type": "apology",
            "goal_code": "emit_apology_after_responsibility",
            "trigger_refs": regret_refs or repair_obligation_refs,
        },
        {
            "move_id": f"repair-move-{run_id}-0004",
            "move_type": "followup_commitment",
            "goal_code": "followup_probe_for_repair_and_relationship_repair",
            "trigger_refs": list(commitment_expression_plan.get("responsibility_event_refs", [])) or responsibility_event_refs,
        },
    ]

    trace = {
        "schema_version": "apology_repair_language_trace_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "move_type_order": move_type_order,
        "repair_language_moves": repair_language_moves,
        "trigger_regret_refs": regret_refs,
        "responsibility_event_refs": responsibility_event_refs,
        "relationship_injury_refs": relationship_injury_refs,
        "repair_obligation_refs": repair_obligation_refs,
        "commitment_expression_ref": "runtime/state/language/commitment_expression_plan.json",
        "relationship_timeline_ref": "runtime/state/relationship/relationship_timeline.json",
        "source_doc_refs": source_doc_refs,
    }
    trace = project_apology_repair_language_trace_with_queue_e_repair_modulation(
        apology_repair_language_trace=trace,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    return project_apology_repair_language_trace_with_offline_learning(
        apology_repair_language_trace=trace,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
    )


def project_apology_repair_language_trace_with_queue_e_repair_modulation(
    *,
    apology_repair_language_trace: dict[str, Any],
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not apology_repair_language_trace:
        return {}
    repair_profile = build_queue_e_repair_modulation_profile(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    if repair_profile["pressure_level"] == "quiet" and not repair_profile["ref_set"]:
        return apology_repair_language_trace

    updated = json.loads(json.dumps(apology_repair_language_trace))
    ref_set = list(repair_profile.get("ref_set", []))
    pressure_level = str(repair_profile.get("pressure_level") or "quiet")

    moves = list(updated.get("repair_language_moves", []))
    if pressure_level in {"urgent", "elevated"} and not _has_move_type(
        moves,
        "responsibility_repair_modulation",
    ):
        moves.append(
            {
                "move_id": f"repair-move-{updated.get('run_id', 'queue-e')}-repair-modulation",
                "move_type": "responsibility_repair_modulation",
                "goal_code": "modulate_repair_language_with_responsibility_regret_pain_pressure",
                "trigger_refs": ref_set,
            }
        )
    updated["repair_language_moves"] = moves

    move_type_order = list(updated.get("move_type_order", []))
    if (
        pressure_level in {"urgent", "elevated"}
        and "responsibility_repair_modulation" not in move_type_order
    ):
        try:
            followup_index = move_type_order.index("followup_commitment")
        except ValueError:
            move_type_order.append("responsibility_repair_modulation")
        else:
            move_type_order.insert(followup_index, "responsibility_repair_modulation")
    updated["move_type_order"] = _dedupe(move_type_order)

    if pressure_level == "urgent":
        updated["queue_e_repair_window_mode"] = "responsibility_lock_first"
        updated["delay_or_release_decision"] = "hold_for_responsibility_repair_lock"
    elif pressure_level == "elevated":
        updated["queue_e_repair_window_mode"] = "responsibility_repair_guarded"
    elif pressure_level == "present":
        updated["queue_e_repair_window_mode"] = "responsibility_pressure_present"

    updated["queue_e_repair_modulation_profile"] = repair_profile
    updated["queue_e_repair_pressure_level"] = pressure_level
    updated["queue_e_repair_attention_target"] = repair_profile["attention_target"]
    updated["queue_e_repair_ref_set"] = ref_set
    return updated


def project_apology_repair_language_trace_with_offline_learning(
    *,
    apology_repair_language_trace: dict[str, Any],
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not apology_repair_language_trace:
        return {}

    updated = json.loads(json.dumps(apology_repair_language_trace))
    offline_profile = derive_offline_learning_profile(
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    ref_set = list(offline_profile.get("offline_learning_ref_set", []))
    if not ref_set:
        return project_apology_repair_language_trace_with_cumulative_offline_learning(
            apology_repair_language_trace=updated,
            offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        )

    relationship_targets = list((relationship_learning_plan or {}).get("relationship_targets", []))
    language_targets = list((language_learning_plan or {}).get("language_targets", []))
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

    moves = list(updated.get("repair_language_moves", []))
    if boundary_hold_required and not _has_move_type(moves, "boundary_repair"):
        moves.append(
            {
                "move_id": f"repair-move-{updated.get('run_id', 'offline')}-offline-boundary",
                "move_type": "boundary_repair",
                "goal_code": "confirm_boundary_and_release_conditions_before_recontact",
                "trigger_refs": ref_set,
            }
        )
    if paced_reentry_required and not _has_move_type(moves, "paced_reentry"):
        moves.append(
            {
                "move_id": f"repair-move-{updated.get('run_id', 'offline')}-offline-paced-reentry",
                "move_type": "paced_reentry",
                "goal_code": "place_repair_actions_into_slower_reentry_window",
                "trigger_refs": ref_set,
            }
        )
    updated["repair_language_moves"] = moves

    move_type_order = list(updated.get("move_type_order", []))
    if paced_reentry_required and "paced_reentry" not in move_type_order:
        try:
            followup_index = move_type_order.index("followup_commitment")
        except ValueError:
            move_type_order.append("paced_reentry")
        else:
            move_type_order.insert(followup_index, "paced_reentry")
    updated["move_type_order"] = _dedupe(move_type_order)

    if rewrite_required:
        repair_window_mode = "nightmare_rewrite_first"
    elif paced_reentry_required:
        repair_window_mode = "paced_reentry_guarded"
    elif boundary_hold_required:
        repair_window_mode = "boundary_confirmation_first"
    else:
        repair_window_mode = "baseline"

    updated["repair_window_mode"] = repair_window_mode
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
    updated["offline_learning_targets"] = _dedupe(relationship_targets + language_targets)
    return project_apology_repair_language_trace_with_cumulative_offline_learning(
        apology_repair_language_trace=updated,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
    )


def project_apology_repair_language_trace_with_cumulative_offline_learning(
    *,
    apology_repair_language_trace: dict[str, Any],
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not apology_repair_language_trace:
        return {}
    cumulative_profile = normalize_offline_learning_cumulative_profile(
        offline_learning_cumulative_profile
    )
    if not cumulative_profile:
        return apology_repair_language_trace

    updated = json.loads(json.dumps(apology_repair_language_trace))
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

    moves = list(updated.get("repair_language_moves", []))
    if pressure_level in {"urgent", "elevated"} and not _has_move_type(
        moves,
        "cumulative_offline_learning_repair",
    ):
        moves.append(
            {
                "move_id": f"repair-move-{updated.get('run_id', 'offline')}-cumulative-offline",
                "move_type": "cumulative_offline_learning_repair",
                "goal_code": "acknowledge_cross_wake_unintegrated_experience_in_repair_window",
                "trigger_refs": ref_set,
            }
        )
    if relationship_reconsolidation_required and not _has_move_type(
        moves,
        "relationship_offline_reconsolidation_repair",
    ):
        moves.append(
            {
                "move_id": f"repair-move-{updated.get('run_id', 'offline')}-relationship-reconsolidation",
                "move_type": "relationship_offline_reconsolidation_repair",
                "goal_code": "acknowledge_cross_wake_relationship_reconsolidation_before_commitment",
                "trigger_refs": ref_set,
            }
        )
    updated["repair_language_moves"] = moves

    move_type_order = list(updated.get("move_type_order", []))
    if (
        pressure_level in {"urgent", "elevated"}
        and "cumulative_offline_learning_repair" not in move_type_order
    ):
        try:
            followup_index = move_type_order.index("followup_commitment")
        except ValueError:
            move_type_order.append("cumulative_offline_learning_repair")
        else:
            move_type_order.insert(followup_index, "cumulative_offline_learning_repair")
    if relationship_reconsolidation_required:
        move_type_order = _insert_before_any(
            move_type_order,
            "relationship_offline_reconsolidation_repair",
            [
                "cumulative_offline_learning_repair",
                "followup_commitment",
            ],
        )
    updated["move_type_order"] = _dedupe(move_type_order)

    if relationship_reconsolidation_required:
        updated["cumulative_repair_window_mode"] = (
            "relationship_offline_reconsolidation_first"
        )
        if _can_replace_delay_decision(updated.get("delay_or_release_decision")):
            updated["delay_or_release_decision"] = (
                "hold_for_relationship_offline_reconsolidation"
            )
    elif pressure_level in {"urgent", "elevated"}:
        updated["cumulative_repair_window_mode"] = (
            "cumulative_offline_learning_first"
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


def _has_move_type(items: list[dict[str, Any]], expected: str) -> bool:
    return any(isinstance(item, dict) and item.get("move_type") == expected for item in items)


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
