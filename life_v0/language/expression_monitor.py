from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

from life_v0.membrane.queue_e_signals import build_queue_e_repair_modulation_profile


BODY_RESOURCE_BUDGET_REF = "runtime/state/body/body_resource_budget.json"
CORE_AFFECT_VECTOR_REF = "runtime/state/body/core_affect_vector.json"
BODY_INTEGRATOR_STATE_REF = "runtime/state/body/body_integrator_state.json"
WORKSPACE_FRAME_REF = "runtime/state/consciousness/workspace_frame.json"
BROADCAST_FRAME_REF = "runtime/state/consciousness/broadcast_frame.json"
NETWORK_STATE_REF = "runtime/state/neural_life_core/network_state.json"
EPISODIC_SPEECH_MEMORY_REF = "runtime/state/language/episodic_speech_memory.jsonl"
EXPRESSION_SLOTS_SCHEMA = "expression_plan_slots_v1"


def is_expression_slots_enabled(environ: Mapping[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return _parse_bool(env.get("DIGITAL_LIFE_EXPRESSION_SLOTS"), False)


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
    proactive_drive = updated.get("proactive_drive_scalar")
    if proactive_drive is None and proactive_voice_profile:
        proactive_drive = proactive_voice_profile.get("proactive_drive_scalar")
    constraints = list(
        (proactive_voice_profile or {}).get("release_constraints", [])
    )
    if fatigue_pressure in {"high_load", "critical"}:
        constraints.append("hold_proactive_voice_until_body_recovery")
        updated["proactive_release_threshold"] = "elevated"
    elif isinstance(proactive_drive, (int, float)) and proactive_drive < 0.35:
        constraints.append("hold_proactive_voice_low_drive")
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


def maybe_apply_expression_slots_to_plan(
    *,
    expression_plan: dict[str, Any],
    workspace_frame: dict[str, Any] | None = None,
    broadcast_frame: dict[str, Any] | None = None,
    body_integrator: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    return apply_expression_slots_from_live_state(
        expression_plan=expression_plan,
        workspace_frame=workspace_frame,
        broadcast_frame=broadcast_frame,
        body_integrator=body_integrator,
        network_state=network_state,
        environ=environ,
    )


def apply_expression_slots_from_live_state(
    *,
    expression_plan: dict[str, Any],
    workspace_frame: dict[str, Any] | None = None,
    broadcast_frame: dict[str, Any] | None = None,
    body_integrator: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    if not expression_plan or not is_expression_slots_enabled(environ):
        return expression_plan or {}

    updated = json.loads(json.dumps(expression_plan))
    continuous = (body_integrator or {}).get("continuous") or {}
    topk_meta = (workspace_frame or {}).get("workspace_topk") or {}
    primary_broadcast = (broadcast_frame or {}).get("primary_broadcast") or {}
    secondary_broadcast = (broadcast_frame or {}).get("secondary_broadcast") or {}
    if not primary_broadcast:
        candidates = list((workspace_frame or {}).get("candidate_explanations") or [])
        if candidates and isinstance(candidates[0], dict):
            primary_broadcast = candidates[0]
        if len(candidates) >= 2 and isinstance(candidates[1], dict):
            secondary_broadcast = candidates[1]

    cognitive_bandwidth = float(continuous.get("cognitive_bandwidth", 0.82) or 0.82)
    allostatic_load = float(continuous.get("allostatic_load", 0.0) or 0.0)
    sleep_pressure = float(continuous.get("sleep_pressure", 0.0) or 0.0)
    workspace_k = topk_meta.get("k")
    if workspace_k is None:
        workspace_k = len((workspace_frame or {}).get("candidate_explanations") or [])

    slot_refs = list(updated.get("expression_slot_refs", []))
    for ref in (
        BODY_INTEGRATOR_STATE_REF,
        WORKSPACE_FRAME_REF,
        BROADCAST_FRAME_REF,
        NETWORK_STATE_REF,
    ):
        if ref not in slot_refs:
            slot_refs.append(ref)

    dmn_profile = _dmn_network_profile(network_state)
    proactive_drive = compute_proactive_drive_scalar(
        body_integrator=body_integrator,
        network_state=network_state,
        expression_plan=updated,
    )

    updated.update(
        {
            "expression_slots_applied": True,
            "expression_slots_schema_version": EXPRESSION_SLOTS_SCHEMA,
            "expression_slot_refs": slot_refs,
            "body_integrator_ref": BODY_INTEGRATOR_STATE_REF,
            "workspace_frame_ref": WORKSPACE_FRAME_REF,
            "broadcast_frame_ref": BROADCAST_FRAME_REF,
            "network_state_ref": NETWORK_STATE_REF,
            "cognitive_bandwidth_scalar": round(cognitive_bandwidth, 3),
            "allostatic_load_scalar": round(allostatic_load, 3),
            "sleep_pressure_scalar": round(sleep_pressure, 3),
            "workspace_topk_k": workspace_k,
            "workspace_primary_focus": (
                primary_broadcast.get("focus")
                or updated.get("semantic_goal")
            ),
            "workspace_broadcast_primary_ref": primary_broadcast.get("explanation_id"),
            "workspace_broadcast_secondary_ref": secondary_broadcast.get(
                "explanation_id"
            ),
            "broadcast_primary_focus": primary_broadcast.get("focus"),
            "broadcast_secondary_focus": secondary_broadcast.get("focus"),
            "dmn_network_mode": dmn_profile.get("mode"),
            "dmn_network_dominant": dmn_profile.get("dominant"),
            "proactive_drive_scalar": proactive_drive,
        }
    )
    modulation_flags = list(updated.get("body_modulation_flags", []))
    if "expression_slots_present" not in modulation_flags:
        modulation_flags.append("expression_slots_present")
    updated["body_modulation_flags"] = modulation_flags
    return updated


def compute_proactive_drive_scalar(
    *,
    body_integrator: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
) -> float:
    continuous = (body_integrator or {}).get("continuous") or {}
    bandwidth = max(0.0, min(1.0, float(continuous.get("cognitive_bandwidth", 0.5) or 0.5)))
    sleep_pressure = max(0.0, min(1.0, float(continuous.get("sleep_pressure", 0.0) or 0.0)))
    allostatic_load = max(
        0.0, min(1.0, float(continuous.get("allostatic_load", 0.0) or 0.0))
    )
    dmn_scalar = float(_dmn_network_profile(network_state).get("drive_weight", 0.2))

    drive = (
        bandwidth * 0.4
        + dmn_scalar * 0.35
        + (1.0 - sleep_pressure) * 0.15
        + (1.0 - allostatic_load) * 0.1
    )
    fatigue_pressure = (expression_plan or {}).get("fatigue_pressure")
    if fatigue_pressure in {"high_load", "critical"}:
        drive *= 0.45
    elif fatigue_pressure == "elevated_guard":
        drive *= 0.72
    caution = (expression_plan or {}).get("release_caution_level")
    if caution == "elevated":
        drive *= 0.85
    return round(max(0.0, min(1.0, drive)), 3)


def maybe_append_episodic_speech_ref(
    *,
    language_dir: Path,
    utterance_ref: str,
    expression_plan: dict[str, Any] | None = None,
    gate_status: str,
    generated_at: str,
    environ: Mapping[str, str] | None = None,
) -> bool:
    if not is_expression_slots_enabled(environ):
        return False
    if gate_status != "accepted" or not utterance_ref:
        return False

    entry = {
        "schema_version": "episodic_speech_ref_v1",
        "utterance_ref": utterance_ref,
        "gate_status": gate_status,
        "generated_at": generated_at,
        "semantic_goal": (expression_plan or {}).get("semantic_goal"),
        "workspace_primary_focus": (expression_plan or {}).get(
            "workspace_primary_focus"
        ),
        "expression_plan_ref": "runtime/state/language/expression_plan.json",
    }
    path = language_dir / "episodic_speech_memory.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return True


def expression_plan_slots_summary(expression_plan: dict[str, Any] | None) -> dict[str, Any]:
    plan = expression_plan or {}
    if not plan.get("expression_slots_applied"):
        return {}
    keys = (
        "expression_slots_schema_version",
        "semantic_goal",
        "fatigue_pressure",
        "body_repair_drive",
        "affect_arousal",
        "expression_tempo_mode",
        "release_caution_level",
        "delay_or_release_decision",
        "cognitive_bandwidth_scalar",
        "allostatic_load_scalar",
        "sleep_pressure_scalar",
        "workspace_topk_k",
        "workspace_primary_focus",
        "workspace_broadcast_primary_ref",
        "workspace_broadcast_secondary_ref",
        "broadcast_primary_focus",
        "broadcast_secondary_focus",
        "dmn_network_mode",
        "dmn_network_dominant",
        "proactive_drive_scalar",
        "memory_grounding_refs",
        "memory_reconstruction_focus",
        "dream_fact_boundary",
        "body_integrator_ref",
        "workspace_frame_ref",
        "broadcast_frame_ref",
        "network_state_ref",
    )
    return {
        key: plan.get(key)
        for key in keys
        if plan.get(key) is not None or key in {
            "workspace_broadcast_primary_ref",
            "workspace_broadcast_secondary_ref",
        }
    }


def _dmn_network_profile(network_state: dict[str, Any] | None) -> dict[str, Any]:
    state = network_state or {}
    dominant = str(state.get("dominant_network") or "")
    active_networks = [
        item
        for item in state.get("active_networks", [])
        if isinstance(item, dict)
    ]
    dmn_entry = next(
        (
            item
            for item in active_networks
            if item.get("network_id") == "default_mode_network"
        ),
        {},
    )
    mode = dmn_entry.get("mode")
    is_dominant = dominant == "default_mode_network"
    is_active = bool(dmn_entry)
    drive_weight = 0.85 if is_dominant else (0.55 if is_active else 0.2)
    return {
        "mode": mode,
        "dominant": is_dominant,
        "active": is_active,
        "drive_weight": drive_weight,
    }


def _parse_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


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
