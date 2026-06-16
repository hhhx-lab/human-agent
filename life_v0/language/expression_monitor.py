from __future__ import annotations

import json
from typing import Any

from life_v0.membrane.queue_e_signals import build_queue_e_repair_modulation_profile


BODY_RESOURCE_BUDGET_REF = "runtime/state/body/body_resource_budget.json"
CORE_AFFECT_VECTOR_REF = "runtime/state/body/core_affect_vector.json"


def build_expression_monitor_state(
    *,
    run_id: str,
    generated_at: str,
    source_doc_refs: list[str],
    cross_scope_risk_terms: list[str] | None = None,
    ambiguity_queue: list[str] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, object]:
    memory_write_gate = memory_write_gate or {}
    core_affect_vector = core_affect_vector or {}
    signal_media_runtime = signal_media_runtime or {}
    modulation_vector = signal_media_runtime.get("modulation_vector", {})
    write_gate_pressure = {
        "memory_write_gate_ref": (
            "runtime/state/memory/memory_write_gate.json" if memory_write_gate else None
        ),
        "stage_policy": memory_write_gate.get("stage_policy"),
        "quarantine_release_condition": memory_write_gate.get("quarantine_route", {}).get("release_condition"),
        "responsibility_event_count": len(memory_write_gate.get("responsibility_event_refs", [])),
    }
    affect_expression_modulation = {
        "core_affect_vector_ref": (
            "runtime/state/body/core_affect_vector.json" if core_affect_vector else None
        ),
        "valence": core_affect_vector.get("valence"),
        "arousal": core_affect_vector.get("arousal"),
        "repair_drive": core_affect_vector.get("repair_drive"),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json" if signal_media_runtime else None
        ),
        "language_precision": signal_media_runtime.get("precision_policy", {}).get("language_precision"),
        "relationship_pressure": modulation_vector.get("relationship_pressure"),
    }
    return {
        "schema_version": "expression_monitor_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "monitor_dimensions": [
            "semantic_coherence",
            "relationship_consequence",
            "commitment_trace",
            "dream_fact",
            "action_consequence",
        ],
        "blocked_language": ["subordinate_object", "service_object", "task_requester"],
        "cross_scope_risk_terms": list(cross_scope_risk_terms or []),
        "ambiguity_queue": list(ambiguity_queue or []),
        "memory_write_gate_ref": (
            "runtime/state/memory/memory_write_gate.json" if memory_write_gate else None
        ),
        "core_affect_vector_ref": (
            "runtime/state/body/core_affect_vector.json" if core_affect_vector else None
        ),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json" if signal_media_runtime else None
        ),
        "write_gate_pressure": write_gate_pressure,
        "affect_expression_modulation": affect_expression_modulation,
        "source_doc_refs": source_doc_refs,
    }


def build_expression_plan(
    *,
    run_id: str,
    generated_at: str,
    inner_speech: dict[str, Any],
    semantic_map: dict[str, Any],
    language_percept: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    ambiguity_flags = list(language_percept.get("ambiguity_flags", []))
    cross_scope_risks = list(language_percept.get("cross_scope_risk_terms", []))
    repair_triggers = list(language_percept.get("repair_trigger_candidates", []))
    commitment_triggers = list(language_percept.get("commitment_trigger_candidates", []))
    replay_cue_targets = list((replay_cue_bundle or {}).get("anti_forgetting_targets", []))
    dream_window_refs = list((offline_consolidation_frame or {}).get("dream_window_refs", []))
    growth_candidates = list((growth_patch_candidate_queue or {}).get("candidates", []))

    expression_risk_flags = ambiguity_flags + cross_scope_risks
    if repair_triggers:
        expression_risk_flags.append("repair_pressure_present")
    if commitment_triggers:
        expression_risk_flags.append("commitment_trace_present")
    if commitment_repair_index.get("repair_obligation_refs") or commitment_repair_index.get("responsibility_trace_refs"):
        expression_risk_flags.append("responsibility_repair_language_pressure_present")
    if replay_cue_targets:
        expression_risk_flags.append("offline_replay_pressure_present")
    if dream_window_refs:
        expression_risk_flags.append("dream_integration_pressure_present")
    if growth_candidates:
        expression_risk_flags.append("growth_candidate_pressure_present")

    expression_plan = {
        "schema_version": "expression_plan_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "expression_plan_id": f"expression-plan-{run_id}",
        "inner_speech_ref": "runtime/state/language/inner_speech_frame.json",
        "semantic_goal": semantic_map.get("semantic_focus"),
        "expression_risk_flags": expression_risk_flags,
        "repair_pressure": len(repair_triggers) + len(commitment_repair_index.get("repair_obligation_refs", [])),
        "responsibility_pressure": len(commitment_repair_index.get("commitment_refs", []))
        + len(commitment_repair_index.get("responsibility_trace_refs", [])),
        "replay_cue_pressure": len(replay_cue_targets),
        "dream_integration_pressure": len(dream_window_refs),
        "growth_candidate_pressure": len(growth_candidates),
        "delay_or_release_decision": (
            "delay_for_clarification"
            if ambiguity_flags
            else "release_guarded_expression"
        ),
        "shared_term_refs": list(language_percept.get("shared_term_hits", [])),
        "offline_influence_refs": [
            ref
            for ref, present in [
                ("runtime/state/replay/replay_cue_bundle.json", bool(replay_cue_targets)),
                ("runtime/state/dream/offline_consolidation_frame.json", bool(dream_window_refs)),
                ("runtime/state/growth/growth_patch_candidate_queue.json", bool(growth_candidates)),
            ]
            if present
        ],
        "source_doc_refs": source_doc_refs,
        "semantic_map_ref": inner_speech.get("semantic_map_ref"),
    }
    return apply_body_affect_modulation(
        expression_plan=expression_plan,
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
    )


def apply_body_affect_modulation(
    *,
    expression_plan: dict[str, Any],
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not expression_plan:
        return {}

    updated = dict(expression_plan)
    fatigue_pressure = (body_resource_budget or {}).get("fatigue_state", {}).get("level")
    repair_drive = (
        (core_affect_vector or {}).get("repair_drive")
        or (body_resource_budget or {}).get("maintenance_pressure", {}).get("repair_drive")
    )
    affect_arousal = (core_affect_vector or {}).get("arousal")
    affect_valence = (core_affect_vector or {}).get("valence")
    affect_responsibility_weight = (core_affect_vector or {}).get("responsibility_weight")

    body_signal_refs = list(updated.get("body_signal_refs", []))
    if body_resource_budget and BODY_RESOURCE_BUDGET_REF not in body_signal_refs:
        body_signal_refs.append(BODY_RESOURCE_BUDGET_REF)
    if core_affect_vector and CORE_AFFECT_VECTOR_REF not in body_signal_refs:
        body_signal_refs.append(CORE_AFFECT_VECTOR_REF)
    if body_signal_refs:
        updated["body_signal_refs"] = body_signal_refs

    if fatigue_pressure:
        updated["fatigue_pressure"] = fatigue_pressure
    if repair_drive:
        updated["body_repair_drive"] = repair_drive
    if affect_arousal is not None:
        updated["affect_arousal"] = affect_arousal
    if affect_valence is not None:
        updated["affect_valence"] = affect_valence
    if affect_responsibility_weight is not None:
        updated["affect_responsibility_weight"] = affect_responsibility_weight

    body_modulation_flags = list(updated.get("body_modulation_flags", []))
    if fatigue_pressure and "fatigue_pressure_present" not in body_modulation_flags:
        body_modulation_flags.append("fatigue_pressure_present")
    if repair_drive and "repair_drive_present" not in body_modulation_flags:
        body_modulation_flags.append("repair_drive_present")
    if affect_arousal is not None and "affect_arousal_present" not in body_modulation_flags:
        body_modulation_flags.append("affect_arousal_present")
    if body_signal_refs and "body_signal_refs_present" not in body_modulation_flags:
        body_modulation_flags.append("body_signal_refs_present")
    if body_modulation_flags:
        updated["body_modulation_flags"] = body_modulation_flags

    tempo_mode = _derive_expression_tempo_mode(
        fatigue_pressure=fatigue_pressure,
        affect_arousal=affect_arousal,
    )
    if tempo_mode:
        updated["expression_tempo_mode"] = tempo_mode
    if fatigue_pressure in {"high_load", "critical"}:
        updated["delay_or_release_decision"] = "hold_for_body_recovery"

    caution_level = _derive_release_caution_level(
        expression_plan=updated,
        fatigue_pressure=fatigue_pressure,
        affect_arousal=affect_arousal,
    )
    if caution_level:
        updated["release_caution_level"] = caution_level

    return updated


def _derive_expression_tempo_mode(
    *,
    fatigue_pressure: str | None,
    affect_arousal: Any,
) -> str | None:
    if fatigue_pressure:
        if fatigue_pressure in {"elevated_guard", "high_load", "critical"}:
            return "slow_protective"
        return "guarded_deliberate"
    if isinstance(affect_arousal, (int, float)) and affect_arousal >= 0.75:
        return "tight_high_tension"
    return None


def _derive_release_caution_level(
    *,
    expression_plan: dict[str, Any],
    fatigue_pressure: str | None,
    affect_arousal: Any,
) -> str | None:
    if expression_plan.get("delay_or_release_decision") == "delay_for_clarification":
        return "elevated"
    if int(expression_plan.get("repair_pressure", 0) or 0) > 0:
        return "elevated"
    if int(expression_plan.get("responsibility_pressure", 0) or 0) > 0:
        return "elevated"
    if fatigue_pressure in {"elevated_guard", "high_load", "critical"}:
        return "elevated"
    if isinstance(affect_arousal, (int, float)) and affect_arousal >= 0.7:
        return "elevated"
    if fatigue_pressure or affect_arousal is not None:
        return "baseline"
    return None


def apply_body_proactive_release_threshold(
    *,
    expression_plan: dict[str, Any],
    proactive_voice_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not expression_plan:
        return {}
    updated = json.loads(json.dumps(expression_plan))
    fatigue_pressure = updated.get("fatigue_pressure")
    caution = updated.get("release_caution_level")
    constraints = list(
        (proactive_voice_profile or {}).get("release_constraints", [])
    )
    if fatigue_pressure in {"high_load", "critical"}:
        constraints.append("hold_proactive_voice_until_body_recovery")
        updated["proactive_release_threshold"] = "elevated"
    elif caution == "elevated":
        updated["proactive_release_threshold"] = "guarded"
    else:
        updated["proactive_release_threshold"] = "baseline"
    if constraints and proactive_voice_profile is not None:
        proactive_voice_profile["release_constraints"] = _dedupe_strings(constraints)
    updated["body_proactive_modulation_boundary"] = (
        "structured_body_modulation_not_spoken_response"
    )
    return updated


def apply_world_contact_handoff_modulation(
    *,
    expression_plan: dict[str, Any],
    world_contact_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not expression_plan or not world_contact_summary:
        return expression_plan or {}
    handoff = world_contact_summary.get("world_contact_handoff_presence")
    if not isinstance(handoff, dict) or not handoff:
        return expression_plan
    updated = json.loads(json.dumps(expression_plan))
    risk_flags = list(updated.get("expression_risk_flags", []))
    if "world_contact_handoff_present" not in risk_flags:
        risk_flags.append("world_contact_handoff_present")
    updated["expression_risk_flags"] = risk_flags
    if handoff.get("repair_hold_active"):
        updated["release_caution_level"] = "elevated"
        if updated.get("delay_or_release_decision") not in {
            "hold_for_responsibility_repair_lock",
        }:
            updated["delay_or_release_decision"] = "hold_for_world_contact_repair"
        updated["world_contact_handoff_tempo_mode"] = "repair_lock_first"
    updated["world_contact_handoff_presence_ref"] = (
        "runtime/state/membrane/world_contact_summary.json#world_contact_handoff_presence"
    )
    updated["world_contact_handoff_modulation_boundary"] = (
        "structured_world_contact_handoff_not_spoken_response"
    )
    return updated


def _dedupe_strings(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def project_expression_plan_with_offline_reconsolidation_modulation(
    *,
    expression_plan: dict[str, Any],
    commitment_expression_plan: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not expression_plan:
        return {}
    commitment_expression_plan = commitment_expression_plan or {}
    apology_repair_language_trace = apology_repair_language_trace or {}
    tempo_mode = commitment_expression_plan.get("cumulative_commitment_tempo_mode")
    repair_window = apology_repair_language_trace.get("cumulative_repair_window_mode")
    if tempo_mode != "relationship_offline_reconsolidation_first" and (
        repair_window != "relationship_offline_reconsolidation_first"
    ):
        return expression_plan
    updated = json.loads(json.dumps(expression_plan))
    risk_flags = list(updated.get("expression_risk_flags", []))
    if "relationship_offline_reconsolidation_present" not in risk_flags:
        risk_flags.append("relationship_offline_reconsolidation_present")
    updated["expression_risk_flags"] = risk_flags
    updated["offline_reconsolidation_tempo_mode"] = (
        tempo_mode or repair_window or "relationship_offline_reconsolidation_first"
    )
    updated["offline_reconsolidation_refs"] = _dedupe_strings(
        list(commitment_expression_plan.get("offline_reconsolidation_refs", []))
        + list(commitment_expression_plan.get("offline_learning_ref_set", []))
        + list(apology_repair_language_trace.get("offline_learning_ref_set", []))
    )[:12]
    if _can_replace_release_decision(updated.get("delay_or_release_decision")):
        updated["delay_or_release_decision"] = (
            "hold_for_relationship_offline_reconsolidation"
        )
    updated["release_caution_level"] = "elevated"
    updated["offline_reconsolidation_modulation_boundary"] = (
        "structured_offline_reconsolidation_not_spoken_response"
    )
    return updated


def _can_replace_release_decision(decision: Any) -> bool:
    return decision not in {
        "hold_for_responsibility_repair_lock",
        "hold_for_world_contact_repair",
    }


def project_expression_plan_with_queue_e_repair_modulation(
    *,
    expression_plan: dict[str, Any],
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not expression_plan:
        return {}
    repair_profile = build_queue_e_repair_modulation_profile(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    if repair_profile["pressure_level"] == "quiet" and not repair_profile["ref_set"]:
        return expression_plan

    updated = json.loads(json.dumps(expression_plan))
    ref_set = list(repair_profile.get("ref_set", []))
    pressure_level = str(repair_profile.get("pressure_level") or "quiet")
    risk_flags = list(updated.get("expression_risk_flags", []))
    if "queue_e_repair_pressure_present" not in risk_flags:
        risk_flags.append("queue_e_repair_pressure_present")
    updated["expression_risk_flags"] = risk_flags

    if pressure_level == "urgent":
        updated["queue_e_expression_tempo_mode"] = "responsibility_lock_first"
        updated["delay_or_release_decision"] = "hold_for_responsibility_repair_lock"
        updated["release_caution_level"] = "elevated"
    elif pressure_level == "elevated":
        updated["queue_e_expression_tempo_mode"] = "responsibility_repair_guarded"
        if updated.get("delay_or_release_decision") != "hold_for_responsibility_repair_lock":
            updated["delay_or_release_decision"] = "release_guarded_expression"

    updated["queue_e_repair_modulation_profile"] = repair_profile
    updated["queue_e_repair_pressure_level"] = pressure_level
    updated["queue_e_repair_attention_target"] = repair_profile["attention_target"]
    updated["queue_e_repair_ref_set"] = ref_set
    return updated
