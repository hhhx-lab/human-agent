from __future__ import annotations

from typing import Any


def build_resident_background_lineage_state(
    idle_governance: dict[str, Any] | None,
    *,
    governance_phase: str,
    status: str,
) -> dict[str, Any]:
    governance = idle_governance or {}
    identity_consciousness_birth_presence = _identity_consciousness_birth_presence(
        governance
    )
    resident_process_identity_presence = _resident_process_identity_presence(
        governance
    )
    profile = _dict_or_empty(governance.get("background_lineage_governance_profile"))
    explicit_depth_band = (
        governance.get("background_lineage_depth_band")
        or profile.get("depth_band")
    )
    generation = _int_or_zero(
        governance.get("background_carryover_generation")
        if governance.get("background_carryover_generation") is not None
        else profile.get("generation")
    )
    depth_band = _deeper_depth_band(
        str(explicit_depth_band or ""),
        _depth_band_for_generation(generation),
    )
    if not depth_band and identity_consciousness_birth_presence:
        depth_band = "no_background_lineage"
    if not depth_band and resident_process_identity_presence:
        depth_band = "no_background_lineage"
    if not depth_band:
        return {}

    lineage_state = {
        "schema_version": "resident_background_lineage_state_v0",
        "status": status,
        "governance_phase": governance_phase,
        "continuity_mode": governance.get("background_continuity_mode"),
        "generation": generation,
        "depth_band": str(depth_band),
        "waiting_posture": _waiting_posture_for_depth(
            depth_band,
            pressure_level=governance.get("background_carryover_pressure_level"),
        ),
        "cadence_weight": _cadence_weight_for_depth(depth_band),
        "evidence_ref_count": _int_or_zero(
            governance.get("background_lineage_evidence_ref_count")
            if governance.get("background_lineage_evidence_ref_count") is not None
            else profile.get("evidence_ref_count")
        ),
        "attention_target": governance.get("governance_attention_target")
        or profile.get("governance_attention_target"),
        "attention_reason": governance.get("governance_attention_reason")
        or profile.get("governance_attention_reason"),
        "cadence_profile": governance.get("governance_cadence_profile")
        or profile.get("governance_cadence_profile"),
        "next_idle_action": governance.get("next_idle_action")
        or profile.get("next_idle_action"),
        "heartbeat_interval_ms": _int_or_zero(
            governance.get("heartbeat_interval_ms")
            if governance.get("heartbeat_interval_ms") is not None
            else profile.get("heartbeat_interval_ms")
        ),
    }
    _copy_if_present(
        lineage_state,
        "parent_run_id",
        governance.get("background_carryover_parent_run_id")
        or profile.get("parent_run_id"),
    )
    evidence_refs = _string_list(
        profile.get("evidence_refs")
        or governance.get("background_continuity_ref_set")
    )
    if evidence_refs:
        lineage_state["evidence_refs"] = evidence_refs
    source_refs = _string_list(governance.get("background_carryover_source_ref_set"))
    if source_refs:
        lineage_state["source_refs"] = source_refs
    continuity_refs = _string_list(governance.get("background_continuity_ref_set"))
    if continuity_refs:
        lineage_state["continuity_refs"] = continuity_refs
    if profile:
        lineage_state["governance_profile_ref"] = (
            "background_lineage_governance_profile"
        )
    relationship_presence = _relationship_presence(governance)
    if relationship_presence:
        lineage_state["relationship_presence"] = relationship_presence
    trait_convergence_presence = _trait_convergence_presence(governance)
    if trait_convergence_presence:
        lineage_state["trait_convergence_presence"] = trait_convergence_presence
    heartbeat_presence = _heartbeat_presence(governance)
    if heartbeat_presence:
        lineage_state["heartbeat_presence"] = heartbeat_presence
    language_presence = _language_presence(governance)
    if language_presence:
        lineage_state["language_presence"] = language_presence
    state_merge_presence = _state_merge_presence(governance)
    if state_merge_presence:
        lineage_state["state_merge_presence"] = state_merge_presence
    if identity_consciousness_birth_presence:
        lineage_state["identity_consciousness_birth_presence"] = (
            identity_consciousness_birth_presence
        )
    if resident_process_identity_presence:
        lineage_state["resident_process_identity_presence"] = (
            resident_process_identity_presence
        )
    offline_learning_presence = _offline_learning_presence(governance)
    if offline_learning_presence:
        lineage_state["offline_learning_presence"] = offline_learning_presence
    dream_wake_presence = _dream_wake_presence(governance)
    if dream_wake_presence:
        lineage_state["dream_wake_presence"] = dream_wake_presence
    autonomous_activity_presence = _autonomous_activity_presence(governance)
    if autonomous_activity_presence:
        lineage_state["autonomous_activity_presence"] = autonomous_activity_presence
    return {
        key: value
        for key, value in lineage_state.items()
        if value is not None and value != ""
    }


def _copy_if_present(target: dict[str, Any], key: str, value: Any) -> None:
    if value:
        target[key] = str(value)


def _dict_or_empty(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dedupe_string_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _depth_band_for_generation(generation: int) -> str:
    if generation >= 5:
        return "entrenched_background_presence"
    if generation >= 3:
        return "deep_persistent_lineage"
    if generation == 2:
        return "persistent_lineage"
    if generation == 1:
        return "single_carryover"
    return ""


def _deeper_depth_band(left: str, right: str) -> str:
    order = {
        "": 0,
        "no_background_lineage": 0,
        "single_carryover": 1,
        "persistent_lineage": 2,
        "deep_persistent_lineage": 3,
        "entrenched_background_presence": 4,
    }
    return left if order.get(left, 0) >= order.get(right, 0) else right


def _waiting_posture_for_depth(depth_band: str, *, pressure_level: Any) -> str:
    if depth_band == "entrenched_background_presence":
        return "entrenched_background_residency_hold"
    if depth_band == "deep_persistent_lineage":
        return "deep_background_residency_hold"
    if depth_band == "persistent_lineage":
        return "persistent_background_hold"
    if depth_band == "single_carryover":
        return (
            "background_carryover_pressure_hold"
            if pressure_level in {"present", "elevated"}
            else "background_carryover_hold"
        )
    return "no_background_lineage_hold"


def _cadence_weight_for_depth(depth_band: str) -> str:
    if depth_band == "entrenched_background_presence":
        return "entrenched"
    if depth_band == "deep_persistent_lineage":
        return "deep"
    if depth_band == "persistent_lineage":
        return "persistent"
    if depth_band == "single_carryover":
        return "carryover"
    return "none"


def _relationship_presence(governance: dict[str, Any]) -> dict[str, Any]:
    relationship = _dict_or_empty(
        _dict_or_empty(governance.get("background_resume_summary")).get(
            "relationship"
        )
    )
    stage = (
        governance.get("background_relationship_stage")
        or relationship.get("relationship_stage")
    )
    if not stage:
        return {}
    payload = {
        "relationship_stage": str(stage),
        "relationship_stage_reason": governance.get(
            "background_relationship_stage_reason"
        )
        or relationship.get("relationship_stage_reason"),
        "relationship_subject_ref": governance.get(
            "background_relationship_subject_ref"
        )
        or relationship.get("relationship_subject_ref"),
        "relationship_stage_continuity": governance.get(
            "background_relationship_stage_continuity"
        ),
        "relationship_stage_turn_count": governance.get(
            "background_relationship_stage_turn_count"
        )
        or relationship.get("relationship_stage_turn_count"),
    }
    evidence_refs = _string_list(
        governance.get("background_relationship_stage_evidence_refs")
        or relationship.get("relationship_stage_evidence_refs")
    )
    if evidence_refs:
        payload["relationship_stage_evidence_refs"] = evidence_refs
    return _drop_empty(payload)


def _trait_convergence_presence(governance: dict[str, Any]) -> dict[str, Any]:
    trait_summary = _dict_or_empty(
        governance.get("background_trait_slow_variable_summary")
        or _dict_or_empty(governance.get("background_resume_summary")).get(
            "trait_slow_variables"
        )
    )
    history_profile = _dict_or_empty(
        governance.get("background_trait_convergence_history_profile")
    )
    if not trait_summary and not history_profile:
        return {}
    payload = {
        "trait_slow_variable_summary": trait_summary,
        "trait_convergence_history_focus": governance.get(
            "background_trait_convergence_history_focus"
        ),
        "trait_convergence_history_profile": history_profile,
        "trait_convergence_unstable_names": _string_list(
            governance.get("background_trait_convergence_unstable_names")
        ),
        "trait_convergence_stable_names": _string_list(
            governance.get("background_trait_convergence_stable_names")
        ),
        "trait_convergence_score": governance.get(
            "background_trait_convergence_score"
        ),
        "trait_convergence_summary": _dict_or_empty(
            governance.get("background_trait_convergence_summary")
        ),
        "trait_drift_monitor_ref": governance.get(
            "background_trait_drift_monitor_ref"
        )
        or governance.get("trait_drift_monitor_ref"),
        "trait_drift_update_mode_summary": _dict_or_empty(
            governance.get("background_trait_drift_update_mode_summary")
        ),
        "trait_drift_recalibration_names": _string_list(
            governance.get("background_trait_drift_recalibration_names")
        ),
        "trait_drift_stabilized_names": _string_list(
            governance.get("background_trait_drift_stabilized_names")
        ),
        "trait_convergence_evidence_refs": _dedupe_string_list(
            _string_list(
                [
                    governance.get("background_resident_governance_state_ref"),
                    governance.get("background_resident_governance_explanation_ref"),
                    governance.get("background_trait_drift_monitor_ref")
                    or governance.get("trait_drift_monitor_ref"),
                    governance.get("background_convergence_summary_ref"),
                    governance.get("background_convergence_history_ref"),
                ]
            )
        ),
    }
    return _drop_empty(payload)


def _heartbeat_presence(governance: dict[str, Any]) -> dict[str, Any]:
    current_trace_ref = governance.get("idle_heartbeat_trace_ref")
    background_trace_ref = governance.get("background_idle_heartbeat_trace_ref")
    current_count = _int_or_zero(governance.get("idle_heartbeat_trace_count"))
    background_count = _int_or_zero(
        governance.get("background_idle_heartbeat_trace_count")
    )
    heartbeat_interval_ms = _int_or_zero(governance.get("heartbeat_interval_ms"))
    next_idle_action = governance.get("next_idle_action")
    if (
        not current_trace_ref
        and not background_trace_ref
        and not current_count
        and not background_count
        and not heartbeat_interval_ms
        and not next_idle_action
    ):
        return {}
    return _drop_empty(
        {
            "idle_heartbeat_trace_ref": current_trace_ref,
            "idle_heartbeat_trace_count": current_count,
            "background_idle_heartbeat_trace_ref": background_trace_ref,
            "background_idle_heartbeat_trace_count": background_count,
            "heartbeat_interval_ms": heartbeat_interval_ms,
            "next_idle_action": next_idle_action,
        }
    )


def _language_presence(governance: dict[str, Any]) -> dict[str, Any]:
    language_refs = _string_list(governance.get("long_horizon_language_refs"))
    priority_profile = _dict_or_empty(
        governance.get("long_horizon_priority_profile")
    )
    live_language_refs = _string_list(governance.get("live_language_turn_refs"))
    background_live_language_refs = _string_list(
        governance.get("background_live_language_turn_refs")
    )
    live_presence_profile = _dict_or_empty(
        governance.get("live_language_presence_profile")
    )
    background_live_presence_profile = _dict_or_empty(
        governance.get("background_live_language_presence_profile")
    )
    last_live_semantic_focus = (
        governance.get("last_live_semantic_focus")
        or governance.get("background_last_live_semantic_focus")
    )
    if (
        not language_refs
        and not priority_profile
        and not live_language_refs
        and not background_live_language_refs
        and not live_presence_profile
        and not background_live_presence_profile
        and not last_live_semantic_focus
    ):
        return {}
    return _drop_empty(
        {
            "long_horizon_language_refs": language_refs,
            "long_horizon_priority_profile": priority_profile,
            "live_language_turn_refs": live_language_refs,
            "last_live_semantic_focus": last_live_semantic_focus,
            "background_live_language_turn_refs": background_live_language_refs,
            "background_last_live_semantic_focus": governance.get(
                "background_last_live_semantic_focus"
            ),
            "live_language_presence_profile": live_presence_profile,
            "background_live_language_presence_profile": (
                background_live_presence_profile
            ),
            "governance_attention_target": governance.get(
                "governance_attention_target"
            ),
            "governance_attention_reason": governance.get(
                "governance_attention_reason"
            ),
            "governance_cadence_profile": governance.get(
                "governance_cadence_profile"
            ),
        }
    )


def _state_merge_presence(governance: dict[str, Any]) -> dict[str, Any]:
    state_merge_guard_ref = (
        governance.get("background_state_merge_guard_ref")
        or governance.get("state_merge_guard_ref")
    )
    state_merge_policy = (
        governance.get("background_state_merge_policy")
        or governance.get("state_merge_policy")
    )
    long_term_change_count = _int_or_zero(
        governance.get("background_state_merge_long_term_change_count")
        if governance.get("background_state_merge_long_term_change_count")
        is not None
        else governance.get("state_merge_long_term_change_count")
    )
    long_term_change_families = _string_list(
        governance.get("background_state_merge_long_term_change_families")
        or governance.get("state_merge_long_term_change_families")
    )
    long_term_change_refs = _string_list(
        governance.get("background_state_merge_long_term_change_refs")
        or governance.get("state_merge_long_term_change_refs")
    )
    if (
        not state_merge_guard_ref
        and not state_merge_policy
        and not long_term_change_count
        and not long_term_change_families
        and not long_term_change_refs
    ):
        return {}
    evidence_refs = _dedupe_string_list(
        [
            str(ref)
            for ref in [
                state_merge_guard_ref,
                *long_term_change_refs,
            ]
            if ref
        ]
    )
    return _drop_empty(
        {
            "state_merge_guard_ref": state_merge_guard_ref,
            "state_merge_policy": state_merge_policy,
            "long_term_change_count": long_term_change_count,
            "long_term_change_families": long_term_change_families,
            "long_term_change_refs": long_term_change_refs,
            "state_merge_evidence_refs": evidence_refs,
        }
    )


def _identity_consciousness_birth_presence(
    governance: dict[str, Any],
) -> dict[str, Any]:
    refs = _dedupe_string_list(
        _string_list(
            [
                governance.get("workspace_frame_ref"),
                governance.get("broadcast_frame_ref"),
                governance.get("metacognition_ref"),
                governance.get("consciousness_probe_ref"),
                governance.get("birth_readiness_rollup_ref"),
                governance.get("birth_readiness_stage_gate_ref"),
            ]
        )
    )
    reportability_flags = _string_list(
        governance.get("consciousness_reportability_flags")
    )
    blocked_reasons = _string_list(governance.get("birth_readiness_blocked_reasons"))
    has_presence = any(
        [
            refs,
            governance.get("consciousness_waiting_posture"),
            governance.get("consciousness_attention_target"),
            governance.get("consciousness_attention_reason"),
            reportability_flags,
            governance.get("birth_readiness_waiting_posture"),
            governance.get("birth_readiness_attention_target"),
            governance.get("birth_readiness_attention_reason"),
            governance.get("birth_readiness_decision"),
            governance.get("birth_readiness_next_required_command"),
            blocked_reasons,
        ]
    )
    if not has_presence:
        return {}
    return _drop_empty(
        {
            "workspace_frame_ref": governance.get("workspace_frame_ref"),
            "broadcast_frame_ref": governance.get("broadcast_frame_ref"),
            "metacognition_ref": governance.get("metacognition_ref"),
            "consciousness_probe_ref": governance.get("consciousness_probe_ref"),
            "birth_readiness_rollup_ref": governance.get("birth_readiness_rollup_ref"),
            "birth_readiness_stage_gate_ref": governance.get(
                "birth_readiness_stage_gate_ref"
            ),
            "consciousness_waiting_posture": governance.get(
                "consciousness_waiting_posture"
            ),
            "consciousness_attention_target": governance.get(
                "consciousness_attention_target"
            ),
            "consciousness_attention_reason": governance.get(
                "consciousness_attention_reason"
            ),
            "consciousness_reportability_flags": reportability_flags,
            "birth_readiness_waiting_posture": governance.get(
                "birth_readiness_waiting_posture"
            ),
            "birth_readiness_attention_target": governance.get(
                "birth_readiness_attention_target"
            ),
            "birth_readiness_attention_reason": governance.get(
                "birth_readiness_attention_reason"
            ),
            "birth_readiness_decision": governance.get("birth_readiness_decision"),
            "birth_readiness_next_required_command": governance.get(
                "birth_readiness_next_required_command"
            ),
            "birth_readiness_blocked_reasons": blocked_reasons,
            "identity_consciousness_birth_refs": refs,
        }
    )


def _resident_process_identity_presence(governance: dict[str, Any]) -> dict[str, Any]:
    profile = _dict_or_empty(
        governance.get("background_resident_process_lease_history_profile")
        or governance.get("resident_process_lease_history_profile")
    )
    profile_ref = (
        governance.get("resident_process_lease_history_profile_ref")
        or governance.get("background_resident_process_lease_history_profile_ref")
        or profile.get("resident_process_lease_history_profile_ref")
    )
    lease_ref = (
        governance.get("resident_process_lease_ref")
        or profile.get("resident_process_lease_ref")
    )
    history_ref = (
        governance.get("resident_process_lease_history_ref")
        or profile.get("resident_process_lease_history_ref")
    )
    continuity_state = (
        governance.get("resident_process_identity_continuity_state")
        or profile.get("current_identity_continuity_state")
    )
    pressure_level = (
        governance.get("resident_process_identity_pressure_level")
        or profile.get("identity_pressure_level")
    )
    history_event_count = _int_or_zero(
        governance.get("resident_process_lease_history_event_count")
        if governance.get("resident_process_lease_history_event_count") is not None
        else profile.get("history_event_count")
    )
    recent_process_ids = _dedupe_string_list(
        _string_list(governance.get("resident_process_recent_ids"))
        or _string_list(profile.get("recent_resident_process_ids"))
    )
    recent_run_ids = _dedupe_string_list(
        _string_list(governance.get("resident_process_recent_run_ids"))
        or _string_list(profile.get("recent_run_ids"))
    )
    evidence_refs = _dedupe_string_list(
        _string_list(profile.get("evidence_refs"))
        + _string_list([lease_ref, history_ref, profile_ref])
    )
    if not any(
        [
            profile,
            profile_ref,
            lease_ref,
            history_ref,
            continuity_state,
            pressure_level,
            history_event_count,
            recent_process_ids,
            recent_run_ids,
        ]
    ):
        return {}
    return _drop_empty(
        {
            "resident_process_lease_ref": lease_ref,
            "resident_process_lease_history_ref": history_ref,
            "resident_process_lease_history_profile_ref": profile_ref,
            "resident_process_identity_continuity_state": continuity_state,
            "resident_process_identity_pressure_level": pressure_level,
            "resident_process_lease_history_event_count": history_event_count,
            "resident_process_recent_ids": recent_process_ids,
            "resident_process_recent_run_ids": recent_run_ids,
            "resident_process_identity_refs": evidence_refs,
        }
    )


def _offline_learning_presence(governance: dict[str, Any]) -> dict[str, Any]:
    profile = _dict_or_empty(governance.get("offline_learning_cumulative_profile"))
    priority_profile = _dict_or_empty(
        governance.get("offline_learning_cumulative_priority_profile")
        or profile.get("priority_profile")
    )
    ref_set = _string_list(
        governance.get("offline_learning_cumulative_ref_set")
        or profile.get("ref_set")
    )
    generation = _int_or_zero(
        governance.get("offline_learning_cumulative_generation")
        if governance.get("offline_learning_cumulative_generation") is not None
        else profile.get("generation")
    )
    pressure_level = (
        governance.get("offline_learning_cumulative_pressure_level")
        or profile.get("pressure_level")
    )
    attention_target = (
        governance.get("offline_learning_cumulative_attention_target")
        or profile.get("attention_target")
    )
    current_pressure_level = profile.get("current_pressure_level")
    previous_generation = _int_or_zero(profile.get("previous_generation"))
    integration_mode = profile.get("integration_mode") or governance.get(
        "offline_learning_cumulative_integration_mode"
    )
    relationship_reconsolidation_required = profile.get(
        "relationship_reconsolidation_required"
    )
    if relationship_reconsolidation_required is None:
        relationship_reconsolidation_required = governance.get(
            "offline_learning_cumulative_relationship_reconsolidation_required"
        )
    if (
        not profile
        and not priority_profile
        and not ref_set
        and not generation
        and not pressure_level
        and not attention_target
        and not integration_mode
        and relationship_reconsolidation_required is None
    ):
        return {}
    return _drop_empty(
        {
            "generation": generation,
            "pressure_level": pressure_level,
            "attention_target": attention_target,
            "priority_profile": priority_profile,
            "ref_set": ref_set,
            "current_pressure_level": current_pressure_level,
            "previous_generation": previous_generation,
            "integration_mode": integration_mode,
            "relationship_reconsolidation_required": (
                relationship_reconsolidation_required
            ),
        }
    )


def _dream_wake_presence(governance: dict[str, Any]) -> dict[str, Any]:
    profile = _dict_or_empty(governance.get("dream_wake_presence_profile"))
    ref_set = _string_list(governance.get("dream_wake_ref_set") or profile.get("ref_set"))
    dream_affective_themes = _string_list(
        governance.get("dream_affective_themes")
        or profile.get("affective_themes")
    )
    dream_window_id = governance.get("dream_window_id") or profile.get(
        "dream_window_id"
    )
    dream_window_kind = governance.get("dream_window_kind") or profile.get(
        "dream_window_kind"
    )
    wake_integration_id = governance.get("wake_integration_id") or profile.get(
        "wake_integration_id"
    )
    dream_fact_gate_result = governance.get("dream_fact_gate_result") or profile.get(
        "dream_fact_gate_result"
    )
    if (
        not profile
        and not ref_set
        and not dream_affective_themes
        and not dream_window_id
        and not wake_integration_id
        and not dream_fact_gate_result
    ):
        return {}
    return _drop_empty(
        {
            "dream_window_ref": governance.get("dream_experience_window_ref"),
            "wake_integration_ref": governance.get("wake_integration_frame_ref"),
            "dream_fact_gate_decision_ref": governance.get(
                "dream_fact_gate_decision_ref"
            ),
            "dream_window_id": dream_window_id,
            "dream_window_kind": dream_window_kind,
            "affective_themes": dream_affective_themes,
            "reportability": governance.get("dream_reportability")
            if governance.get("dream_reportability") is not None
            else profile.get("reportability"),
            "wake_integration_id": wake_integration_id,
            "wake_archive_requirement": governance.get(
                "wake_integration_archive_requirement"
            )
            or profile.get("wake_archive_requirement"),
            "wake_growth_seed_count": _int_or_zero(
                governance.get("wake_integration_growth_seed_count")
                if governance.get("wake_integration_growth_seed_count") is not None
                else profile.get("wake_growth_seed_count")
            ),
            "wake_repair_target_count": _int_or_zero(
                governance.get("wake_integration_repair_target_count")
                if governance.get("wake_integration_repair_target_count") is not None
                else profile.get("wake_repair_target_count")
            ),
            "dream_fact_gate_result": dream_fact_gate_result,
            "dream_fact_gate_ref_count": _int_or_zero(
                governance.get("dream_fact_gate_ref_count")
                if governance.get("dream_fact_gate_ref_count") is not None
                else profile.get("dream_fact_gate_ref_count")
            ),
            "narrative_candidate_count": _int_or_zero(
                profile.get("narrative_candidate_count")
            ),
            "relationship_repair_candidate_count": _int_or_zero(
                profile.get("relationship_repair_candidate_count")
            ),
            "ref_set": ref_set,
        }
    )


def _autonomous_activity_presence(governance: dict[str, Any]) -> dict[str, Any]:
    profile = _dict_or_empty(
        governance.get("resident_autonomous_activity_presence_profile")
    )
    activity_state_refs = _dict_or_empty(
        governance.get("resident_autonomous_activity_state_refs")
        or profile.get("activity_state_refs")
    )
    activity_kind_counts = _dict_or_empty(
        governance.get("autonomous_activity_kind_counts")
        or profile.get("activity_kind_counts")
    )
    ref_set = _dedupe_string_list(
        _string_list(governance.get("resident_autonomous_activity_ref_set"))
        or _string_list(profile.get("ref_set"))
    )
    activity_count = _int_or_zero(
        governance.get("autonomous_activity_count")
        if governance.get("autonomous_activity_count") is not None
        else profile.get("activity_count")
    )
    last_activity_kind = (
        governance.get("last_autonomous_activity_kind")
        or profile.get("last_activity_kind")
    )
    last_activity_state_ref = (
        governance.get("last_autonomous_activity_state_ref")
        or profile.get("last_activity_state_ref")
    )
    if (
        not profile
        and not ref_set
        and not activity_count
        and not activity_kind_counts
        and not last_activity_kind
        and not activity_state_refs
    ):
        return {}
    return _drop_empty(
        {
            "resident_autonomous_activity_ref": governance.get(
                "resident_autonomous_activity_ref"
            )
            or profile.get("resident_autonomous_activity_ref")
            or "runtime/state/terminal/resident_autonomous_activity.jsonl",
            "resident_autonomous_activity_state_ref": governance.get(
                "resident_autonomous_activity_state_ref"
            )
            or profile.get("resident_autonomous_activity_state_ref")
            or "runtime/state/terminal/resident_autonomous_activity_state.json",
            "activity_count": activity_count,
            "activity_kind_counts": activity_kind_counts,
            "last_activity_kind": last_activity_kind,
            "last_activity_at": governance.get("last_autonomous_activity_at")
            or profile.get("last_activity_at"),
            "last_activity_state_ref": last_activity_state_ref,
            "activity_state_refs": activity_state_refs,
            "current_cycle": _string_list(profile.get("current_cycle")),
            "autonomous_activity_refs": ref_set,
            "autonomous_activity_evidence_ref_count": len(ref_set),
        }
    )


def _drop_empty(payload: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in payload.items():
        if value is None:
            continue
        if isinstance(value, str) and not value:
            continue
        if isinstance(value, (list, tuple, dict)) and not value:
            continue
        result[key] = value
    return result
