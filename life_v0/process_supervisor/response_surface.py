from __future__ import annotations

import hashlib
import json
from typing import Any

from ..state_store.memory_retrieval import memory_retrieval_context_summary
from .dialogue_events import build_offline_learning_cumulative_payload
from .handoff_profile import select_handoff_profile
from .offline_learning_signals import derive_offline_learning_profile
from .state_merge_signals import state_merge_long_term_change_profile


def compose_life_response(
    *,
    external_utterance: str,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    dialogue_memory_summary: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    shared_term_registry: dict[str, Any] | None = None,
    commitment_index: dict[str, Any] | None = None,
    commitment_expression_plan: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
    relation_turn_frame: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
    life_context_frame: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
) -> str:
    expression_plan = expression_plan or {}
    relationship_memory = relationship_memory or {}
    dialogue_memory_summary = dialogue_memory_summary or {}
    terminal_life_loop_state = terminal_life_loop_state or {}
    lineage = terminal_life_loop_state.get("resident_background_lineage_state") or {}
    if not isinstance(lineage, dict):
        lineage = {}

    subject = _first_dict((relationship_graph or {}).get("subjects"))
    continuity_report = _first_dict(
        (relationship_timeline or {}).get("relationship_continuity_reports")
    )
    trust_trajectory = _first_dict(
        (relationship_timeline or {}).get("trust_trajectories")
    )
    shared_terms = [
        {
            "term_id": str(term.get("term_id", "")),
            "surface": str(term.get("surface", "")),
        }
        for term in (shared_term_registry or {}).get("shared_terms", [])
        if isinstance(term, dict)
    ]
    commitment_refs = _string_list((commitment_index or {}).get("commitment_refs"))
    repair_move_order = _string_list(
        (apology_repair_language_trace or {}).get("move_type_order")
    )
    commitment_act_order = _string_list(
        (commitment_expression_plan or {}).get("act_type_order")
    )
    memory_tier_summary = _memory_tier_summary(
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
    )
    memory_retrieval_summary = memory_retrieval_context_summary(
        memory_retrieval_frame
    )

    offline_profile = derive_offline_learning_profile(
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    offline_cumulative = build_offline_learning_cumulative_payload(
        terminal_life_loop_state
    )
    prediction_surface = _prediction_surface_posture(
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        memory_write_gate=memory_write_gate,
        state_merge_guard=state_merge_guard,
    )
    prediction_presence = lineage.get("prediction_write_gate_presence")
    if isinstance(prediction_presence, dict):
        prediction_surface = _prediction_surface_with_presence(
            prediction_surface,
            prediction_presence,
        )

    body_presence = _dict_value(lineage, "body_presence")
    trait_presence = _dict_value(lineage, "trait_convergence_presence")
    language_presence = _dict_value(lineage, "language_presence")
    identity_presence = _dict_value(lineage, "identity_consciousness_birth_presence")
    offline_presence = _dict_value(lineage, "offline_learning_presence")
    dream_wake_presence = _dict_value(lineage, "dream_wake_presence")
    memory_retrieval_presence = _dict_value(lineage, "memory_retrieval_presence")
    autonomous_presence = _dict_value(lineage, "autonomous_activity_presence")
    birth_repair_presence = _dict_value(lineage, "birth_repair_presence")
    life_constraint_presence = _dict_value(lineage, "life_constraint_presence")
    relationship_presence = _dict_value(lineage, "relationship_presence")
    heartbeat_presence = _dict_value(lineage, "heartbeat_cadence_presence")
    previous_handoff_profile = select_handoff_profile(terminal_life_loop_state)

    material = {
        "schema_version": "audited_expression_material_v0",
        "material_kind": "structured_expression_context",
        "natural_language_release_disabled": True,
        "external_utterance_sha256": _sha256_text(external_utterance),
        "external_utterance_sha256_length": len(_sha256_text(external_utterance)),
        "relationship": {
            "relation_role": subject.get("relation_role"),
            "relationship_stage": subject.get("relationship_stage")
            or relationship_presence.get("relationship_stage"),
            "relation_subject_ref": (relation_turn_frame or {}).get(
                "relation_subject_ref"
            ),
            "continuity_state": continuity_report.get("continuity_state"),
            "trust_state": trust_trajectory.get("current_trust_state"),
            "shared_terms": shared_terms,
            "commitment_ref_count": len(commitment_refs),
            "commitment_refs": commitment_refs,
            "memory_tier_projection_ref": memory_tier_summary.get(
                "relationship_memory_tier_projection_ref"
            ),
            "dialogue_memory_summary_ref": memory_tier_summary.get(
                "dialogue_memory_summary_ref"
            ),
            "next_wake_cues": memory_tier_summary.get("next_wake_cues", []),
        },
        "language": {
            "semantic_goal": expression_plan.get("semantic_goal"),
            "body_signal_refs": _string_list(expression_plan.get("body_signal_refs")),
            "offline_influence_refs": _string_list(
                expression_plan.get("offline_influence_refs")
            ),
            "fatigue_pressure": expression_plan.get("fatigue_pressure"),
            "body_repair_drive": expression_plan.get("body_repair_drive"),
            "affect_arousal": expression_plan.get("affect_arousal"),
            "release_caution_level": expression_plan.get("release_caution_level"),
            "expression_tempo_mode": expression_plan.get("expression_tempo_mode"),
            "self_narrative_ref_count": len(
                _string_list((life_context_frame or {}).get("self_narrative_refs"))
            ),
            "commitment_act_order": commitment_act_order,
            "repair_move_order": repair_move_order,
            "resident_language_attention_target": language_presence.get(
                "governance_attention_target"
            ),
            "resident_last_live_semantic_focus": (
                language_presence.get("last_live_semantic_focus")
                or language_presence.get("background_last_live_semantic_focus")
            ),
            "memory_tier_projection_ref": memory_tier_summary.get(
                "relationship_memory_tier_projection_ref"
            ),
            "dialogue_memory_tiering_ref": memory_tier_summary.get(
                "dialogue_memory_tiering_ref"
            ),
        },
        "memory_dream_growth": {
            "replay_cue_count": len(
                _string_list((replay_cue_bundle or {}).get("anti_forgetting_targets"))
            ),
            "dream_window_count": len(
                _string_list((offline_consolidation_frame or {}).get("dream_window_refs"))
            ),
            "growth_candidate_count": len(
                (growth_patch_candidate_queue or {}).get("candidates", [])
                if isinstance(
                    (growth_patch_candidate_queue or {}).get("candidates", []),
                    list,
                )
                else []
            ),
            "nightmare_risk_status": (nightmare_risk or {}).get("risk_status"),
            "offline_learning_pressure_level": offline_profile.get(
                "offline_learning_pressure_level"
            ),
            "offline_learning_attention_target": offline_profile.get(
                "offline_learning_attention_target"
            ),
            "offline_learning_targets": _learning_targets(
                belief_learning_plan=belief_learning_plan,
                language_learning_plan=language_learning_plan,
                relationship_learning_plan=relationship_learning_plan,
            ),
            "offline_learning_cumulative": offline_cumulative,
            "memory_tier_projection": memory_tier_summary.get(
                "relationship_memory_tier_projection"
            ),
            "dialogue_memory_tiering": memory_tier_summary.get(
                "dialogue_memory_tiering"
            ),
            "next_wake_cue_count": memory_tier_summary.get("next_wake_cue_count"),
            "memory_tier_refs": {
                "relationship_memory_tier_refs": memory_tier_summary.get(
                    "relationship_memory_tier_refs", []
                ),
                "dialogue_memory_tier_refs": memory_tier_summary.get(
                    "dialogue_memory_tier_refs", []
                ),
            },
            "memory_retrieval": memory_retrieval_summary,
            "resident_memory_retrieval_presence": _selected_keys(
                memory_retrieval_presence,
                (
                    "memory_retrieval_frame_ref",
                    "reconstruction_focus",
                    "cue_terms",
                    "activated_ref_count",
                    "relationship_hit_count",
                    "dream_residue_hit_count",
                    "responsibility_hit_count",
                    "ref_count",
                ),
            ),
            "next_wake_cues": memory_tier_summary.get("next_wake_cues", []),
            "resident_offline_presence": _selected_keys(
                offline_presence,
                (
                    "generation",
                    "pressure_level",
                    "attention_target",
                    "current_pressure_level",
                    "previous_generation",
                    "integration_mode",
                    "relationship_reconsolidation_required",
                ),
            ),
            "resident_dream_wake_presence": _selected_keys(
                dream_wake_presence,
                (
                    "dream_window_kind",
                    "dream_fact_gate_result",
                    "wake_archive_requirement",
                    "wake_growth_seed_count",
                    "wake_repair_target_count",
                ),
            ),
        },
        "body_affect": {
            "fatigue_level": (body_resource_budget or {})
            .get("fatigue_state", {})
            .get("level"),
            "repair_drive": (core_affect_vector or {}).get("repair_drive")
            or (body_resource_budget or {})
            .get("maintenance_pressure", {})
            .get("repair_drive"),
            "arousal": (core_affect_vector or {}).get("arousal"),
            "resident_body_presence": _selected_keys(
                body_presence,
                (
                    "body_waiting_posture",
                    "fatigue_load",
                    "sleep_pressure",
                    "energy_level",
                    "repair_drive",
                    "arousal",
                    "pain_pressure",
                    "responsibility_weight",
                ),
            ),
            "resident_body_ref_count": len(
                _dedupe_string_list(
                    _string_list(body_presence.get("body_evidence_refs"))
                    + _string_list(body_presence.get("body_ref_set"))
                )
            ),
        },
        "responsibility_repair": {
            "world_contact_release_posture": (world_contact_summary or {}).get(
                "release_posture"
            ),
            "repair_obligation_count": len(
                _string_list((world_contact_summary or {}).get("repair_obligation_refs"))
            )
            or len(
                _string_list(
                    (responsibility_loop_state or {}).get("repair_obligation_refs")
                )
            ),
            "regret_pressure_count": len(
                _string_list(
                    (pain_regret_repair_report or {}).get("regret_pressure_refs")
                )
            )
            or _list_count(
                (responsibility_loop_state or {}).get("regret_pressure_candidates")
            ),
            "repair_followup_required": bool(
                (pain_regret_repair_report or {}).get("repair_followup_required")
                or (responsibility_loop_state or {}).get("repair_followup_required")
            ),
            "birth_repair_presence": _selected_keys(
                birth_repair_presence,
                (
                    "gate_status",
                    "pressure_level",
                    "attention_target",
                    "waiting_posture",
                    "attention_reason",
                    "continuity_mode",
                ),
            ),
        },
        "prediction_attention": prediction_surface,
        "resident_background": {
            "depth_band": lineage.get("depth_band"),
            "cadence_weight": lineage.get("cadence_weight"),
            "heartbeat_cadence_presence": _selected_keys(
                heartbeat_presence,
                (
                    "driver",
                    "reason",
                    "modulators",
                    "heartbeat_priority_stack_winner",
                    "heartbeat_priority_stack_candidates",
                    "evidence_ref_count",
                ),
            ),
            "trait_convergence_presence": _selected_keys(
                trait_presence,
                (
                    "trait_convergence_history_focus",
                    "trait_convergence_score",
                    "trait_drift_monitor_ref",
                    "trait_convergence_unstable_names",
                    "trait_convergence_stable_names",
                    "trait_drift_recalibration_names",
                    "trait_drift_stabilized_names",
                ),
            ),
            "identity_consciousness_birth_presence": _selected_keys(
                identity_presence,
                (
                    "consciousness_waiting_posture",
                    "consciousness_reportability_flags",
                    "birth_readiness_waiting_posture",
                    "birth_readiness_decision",
                    "birth_readiness_next_required_command",
                ),
            ),
            "life_constraint_presence": _selected_keys(
                life_constraint_presence,
                (
                    "queue_e_cross_layer_gate_status",
                    "waiting_posture",
                    "attention_target",
                    "attention_reason",
                ),
            ),
            "prediction_write_gate_presence": _selected_keys(
                prediction_presence if isinstance(prediction_presence, dict) else {},
                (
                    "prediction_waiting_posture",
                    "response_surface_posture_hint",
                    "prediction_attention_target",
                    "prediction_error_count",
                    "active_sampling_route",
                    "memory_write_gate_policy",
                    "state_merge_policy",
                ),
            ),
            "autonomous_activity_presence": _selected_keys(
                autonomous_presence,
                (
                    "activity_count",
                    "last_activity_kind",
                    "cycle_completion_count",
                    "cycle_coverage_complete",
                    "covered_activity_kinds",
                    "next_activity_kind",
                    "last_web_dream_learning_status",
                    "last_web_dream_learning_topic_candidates",
                    "last_web_dream_learning_wake_question_candidates",
                ),
            ),
            "previous_handoff_profile": _selected_keys(
                previous_handoff_profile,
                (
                    "next_required_action",
                    "lineage_depth_band",
                    "last_live_semantic_focus",
                    "carried_presence_keys",
                    "handoff_evidence_ref_count",
                ),
            ),
            "previous_handoff_carry_status": terminal_life_loop_state.get(
                "previous_live_turn_waiting_handoff_carry_status"
            ),
        },
        "self_slow_variables": _self_slow_variable_snapshot(self_model_state),
    }
    return json.dumps(_compact(material), ensure_ascii=False, sort_keys=True)


def compose_life_spoken_response(
    *,
    external_utterance: str,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    dialogue_memory_summary: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    life_name: str = "Adam",
    shared_term_registry: dict[str, Any] | None = None,
    commitment_index: dict[str, Any] | None = None,
    commitment_expression_plan: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
    relation_turn_frame: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
    life_context_frame: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
    evidence_response: str | None = None,
) -> str:
    _ = (
        external_utterance,
        relationship_graph,
        relationship_timeline,
        relationship_memory,
        dialogue_memory_summary,
        memory_retrieval_frame,
        life_name,
        shared_term_registry,
        commitment_index,
        commitment_expression_plan,
        apology_repair_language_trace,
        relation_turn_frame,
        expression_plan,
        life_context_frame,
        replay_cue_bundle,
        offline_consolidation_frame,
        growth_patch_candidate_queue,
        nightmare_risk,
        belief_learning_plan,
        language_learning_plan,
        relationship_learning_plan,
        signal_media_runtime,
        belief_state,
        prediction_error_field,
        active_sampling_plan,
        memory_write_gate,
        state_merge_guard,
        body_resource_budget,
        core_affect_vector,
        responsibility_loop_state,
        world_contact_summary,
        pain_regret_repair_report,
        self_model_state,
        terminal_life_loop_state,
        evidence_response,
    )
    return ""


def _prediction_surface_posture(
    *,
    signal_media_runtime: dict[str, Any] | None,
    belief_state: dict[str, Any] | None,
    prediction_error_field: dict[str, Any] | None,
    active_sampling_plan: dict[str, Any] | None,
    memory_write_gate: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
) -> dict[str, Any]:
    selected_route = str((active_sampling_plan or {}).get("selected_route", ""))
    stage_effect = str((active_sampling_plan or {}).get("stage_effect", ""))
    error_events = (prediction_error_field or {}).get("error_events", [])
    error_count = len(error_events) if isinstance(error_events, list) else 0
    modulation_vector = (signal_media_runtime or {}).get("modulation_vector", {})
    if not isinstance(modulation_vector, dict):
        modulation_vector = {}
    repair_drive = str(modulation_vector.get("repair_drive", "")).lower()
    confidence_level = str((belief_state or {}).get("confidence_level", "")).lower()
    memory_policy = str((memory_write_gate or {}).get("stage_policy", ""))
    merge_policy = str((state_merge_guard or {}).get("stage_policy", ""))
    change_profile = state_merge_long_term_change_profile(state_merge_guard)
    route_lower = selected_route.lower()
    stage_lower = stage_effect.lower()
    memory_policy_lower = memory_policy.lower()

    surface_posture = ""
    if "clarify" in route_lower:
        surface_posture = "question"
    elif "repair" in route_lower:
        surface_posture = "repair"
    elif "hold_for_evidence" in stage_lower or error_count > 0:
        surface_posture = "hold"
    elif repair_drive == "active" or "repair" in memory_policy_lower:
        surface_posture = "repair"
    elif change_profile["state_merge_long_term_change_count"] > 0:
        surface_posture = "hold"
    elif confidence_level in {"stable", "high", "confirmed"}:
        surface_posture = "confirm"

    return {
        "surface_posture": surface_posture,
        "active_sampling_route": selected_route,
        "prediction_error_count": error_count,
        "memory_write_gate_policy": memory_policy,
        "state_merge_policy": merge_policy,
        **change_profile,
    }


def _prediction_surface_with_presence(
    prediction_surface: dict[str, Any],
    prediction_write_gate_presence: dict[str, Any],
) -> dict[str, Any]:
    surface = dict(prediction_surface)
    posture_hint = str(
        prediction_write_gate_presence.get("response_surface_posture_hint") or ""
    )
    if not surface.get("surface_posture") and posture_hint:
        surface["surface_posture"] = posture_hint
    for key in (
        "active_sampling_route",
        "prediction_error_count",
        "memory_write_gate_policy",
        "state_merge_policy",
        "state_merge_long_term_change_count",
        "state_merge_long_term_change_families",
    ):
        if not surface.get(key) and prediction_write_gate_presence.get(key):
            surface[key] = prediction_write_gate_presence[key]
    return surface


def _learning_targets(
    *,
    belief_learning_plan: dict[str, Any] | None,
    language_learning_plan: dict[str, Any] | None,
    relationship_learning_plan: dict[str, Any] | None,
) -> dict[str, list[str]]:
    return {
        "belief_targets": _string_list(
            (belief_learning_plan or {}).get("belief_targets")
        ),
        "language_targets": _string_list(
            (language_learning_plan or {}).get("language_targets")
        ),
        "relationship_targets": _string_list(
            (relationship_learning_plan or {}).get("relationship_targets")
        ),
    }


def _memory_tier_summary(
    *,
    relationship_memory: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    relationship_memory = relationship_memory or {}
    dialogue_memory_summary = dialogue_memory_summary or {}
    relationship_memory_tier_projection = _selected_keys(
        _dict_value(relationship_memory, "memory_tier_projection"),
        (
            "schema_version",
            "salient_core_episode_refs",
            "retrievable_context_episode_refs",
            "deep_sediment_episode_refs",
            "projection_source_ref",
        ),
    )
    dialogue_memory_tiering = _selected_keys(
        _dict_value(dialogue_memory_summary, "memory_tiering"),
        (
            "schema_version",
            "tier_policy",
            "salient_core_episode_refs",
            "retrievable_context_episode_refs",
            "deep_sediment_episode_refs",
            "tier_score_records",
        ),
    )
    relationship_memory_tier_refs = _dedupe_string_list(
        _string_list(relationship_memory_tier_projection.get("salient_core_episode_refs"))
        + _string_list(
            relationship_memory_tier_projection.get("retrievable_context_episode_refs")
        )
        + _string_list(relationship_memory_tier_projection.get("deep_sediment_episode_refs"))
    )
    dialogue_memory_tier_refs = _dedupe_string_list(
        _string_list(dialogue_memory_tiering.get("salient_core_episode_refs"))
        + _string_list(dialogue_memory_tiering.get("retrievable_context_episode_refs"))
        + _string_list(dialogue_memory_tiering.get("deep_sediment_episode_refs"))
    )
    next_wake_cues = _dedupe_string_list(
        _string_list(relationship_memory.get("next_wake_cues"))
        + _string_list(dialogue_memory_summary.get("next_wake_cues"))
    )
    relation_person_profile = _selected_keys(
        _dict_value(relationship_memory, "relation_person_profile"),
        (
            "schema_version",
            "observed_names",
            "preference_hypotheses",
            "personality_hypotheses",
            "relationship_stage_hint",
            "last_profile_update_ref",
        ),
    )
    return {
        "relationship_memory_ref": (
            "runtime/state/memory/relationship_memory.json"
            if relationship_memory
            else None
        ),
        "dialogue_memory_summary_ref": (
            "runtime/state/memory/dialogue_memory_summary.json"
            if dialogue_memory_summary
            else None
        ),
        "relationship_memory_tier_projection_ref": (
            "runtime/state/memory/relationship_memory.json#memory_tier_projection"
            if relationship_memory_tier_projection
            else None
        ),
        "dialogue_memory_tiering_ref": (
            "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering"
            if dialogue_memory_tiering
            else None
        ),
        "relationship_memory_tier_projection": relationship_memory_tier_projection,
        "dialogue_memory_tiering": dialogue_memory_tiering,
        "relationship_memory_tier_refs": relationship_memory_tier_refs,
        "dialogue_memory_tier_refs": dialogue_memory_tier_refs,
        "next_wake_cues": next_wake_cues,
        "next_wake_cue_count": len(next_wake_cues),
        "relation_person_profile": relation_person_profile,
        "memory_tier_ref_count": len(
            _dedupe_string_list(relationship_memory_tier_refs + dialogue_memory_tier_refs)
        ),
    }


def _self_slow_variable_snapshot(
    self_model_state: dict[str, Any] | None,
) -> dict[str, Any]:
    trait_slow_variables = (self_model_state or {}).get("trait_slow_variables", {})
    if not isinstance(trait_slow_variables, dict):
        return {}
    return {
        "repair_seriousness": _slow_value(trait_slow_variables, "repair_seriousness"),
        "boundary_respect": _slow_value(trait_slow_variables, "boundary_respect"),
        "continuity_drive": _slow_value(trait_slow_variables, "continuity_drive"),
    }


def _selected_keys(payload: dict[str, Any] | None, keys: tuple[str, ...]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {key: payload[key] for key in keys if key in payload}


def _dict_value(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    return value if isinstance(value, dict) else {}


def _first_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, list) and value and isinstance(value[0], dict):
        return value[0]
    return {}


def _slow_value(trait_slow_variables: dict[str, Any], key: str) -> float:
    payload = trait_slow_variables.get(key, {})
    if isinstance(payload, dict):
        value = payload.get("value")
        if isinstance(value, (int, float)):
            return float(value)
    if isinstance(payload, (int, float)):
        return float(payload)
    return 0.0


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _list_count(value: Any) -> int:
    return len(value) if isinstance(value, list) else 0


def _dedupe_string_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _sha256_text(text: str) -> str:
    return hashlib.sha256(str(text or "").encode("utf-8")).hexdigest()


def _compact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: compacted
            for key, item in value.items()
            if (compacted := _compact(item)) not in ({}, [], None, "")
        }
    if isinstance(value, list):
        return [
            compacted
            for item in value
            if (compacted := _compact(item)) not in ({}, [], None, "")
        ]
    return value
