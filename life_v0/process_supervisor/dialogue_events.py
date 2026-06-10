from __future__ import annotations

from typing import Any


BACKGROUND_TRAIT_CONVERGENCE_REF_KEYS = (
    "background_resident_governance_state_ref",
    "background_resident_governance_explanation_ref",
    "background_trait_drift_monitor_ref",
    "background_convergence_summary_ref",
    "background_convergence_history_ref",
)


def build_external_turn_event(
    *,
    turn_id: str,
    generated_at: str,
    utterance: str,
    shared_term_registry: dict[str, Any],
    commitment_index: dict[str, Any],
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
) -> dict[str, Any]:
    event = {
        "schema_version": "dialogue_turn_event_v0",
        "turn_id": turn_id,
        "generated_at": generated_at,
        "event_role": "external_relation_turn",
        "relation_role": "friend",
        "utterance": utterance,
        "shared_term_refs": shared_term_refs(shared_term_registry),
        "commitment_refs": list(commitment_index.get("commitment_refs", [])),
        "expression_monitor_ref": "runtime/state/language/expression_monitor_state.json",
        "narrative_trace_ref": "runtime/state/language/self_narrative_language_trace.json",
    }
    _attach_queue_e_refs(
        event=event,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
    )
    return event


def build_life_turn_event(
    *,
    turn_id: str,
    generated_at: str,
    utterance: str,
    shared_term_registry: dict[str, Any],
    commitment_index: dict[str, Any],
    terminal_life_loop_state: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    signal_media_runtime_ref: str | None = None,
    belief_state_ref: str | None = None,
    prediction_error_field_ref: str | None = None,
    active_sampling_plan_ref: str | None = None,
    memory_write_gate_ref: str | None = None,
    state_merge_guard_ref: str | None = None,
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
) -> dict[str, Any]:
    event = {
        "schema_version": "dialogue_turn_event_v0",
        "turn_id": turn_id,
        "generated_at": generated_at,
        "event_role": "digital_life_turn",
        "relation_role": "friend",
        "utterance": utterance,
        "shared_term_refs": shared_term_refs(shared_term_registry),
        "commitment_refs": list(commitment_index.get("commitment_refs", [])),
        "expression_monitor_ref": "runtime/state/language/expression_monitor_state.json",
        "narrative_trace_ref": "runtime/state/language/self_narrative_language_trace.json",
    }
    _attach_queue_e_refs(
        event=event,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
    )
    event.update(build_background_trait_convergence_payload(terminal_life_loop_state))
    event.update(build_resident_background_lineage_payload(terminal_life_loop_state))
    event.update(build_offline_learning_cumulative_payload(terminal_life_loop_state))
    event.update(
        build_prediction_write_gate_payload(
            terminal_life_loop_state=terminal_life_loop_state,
            signal_media_runtime=signal_media_runtime,
            belief_state=belief_state,
            prediction_error_field=prediction_error_field,
            active_sampling_plan=active_sampling_plan,
            memory_write_gate=memory_write_gate,
            state_merge_guard=state_merge_guard,
            signal_media_runtime_ref=signal_media_runtime_ref,
            belief_state_ref=belief_state_ref,
            prediction_error_field_ref=prediction_error_field_ref,
            active_sampling_plan_ref=active_sampling_plan_ref,
            memory_write_gate_ref=memory_write_gate_ref,
            state_merge_guard_ref=state_merge_guard_ref,
        )
    )
    return event


def shared_term_refs(shared_term_registry: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for term in shared_term_registry.get("shared_terms", []):
        if isinstance(term, dict) and term.get("term_id"):
            refs.append(f"runtime/state/language/shared_term_registry.json#{term['term_id']}")
    return refs


def _attach_queue_e_refs(
    *,
    event: dict[str, Any],
    responsibility_loop_state_ref: str | None,
    world_contact_summary_ref: str | None,
    pain_regret_repair_report_ref: str | None,
) -> None:
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    if responsibility_loop_state_ref:
        event["responsibility_loop_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        event["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        event["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        event["membrane_guard_refs"] = membrane_guard_refs


def build_background_trait_convergence_payload(
    terminal_life_loop_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not terminal_life_loop_state:
        return {}

    payload: dict[str, Any] = {}
    evidence_refs: list[str] = []
    for key in BACKGROUND_TRAIT_CONVERGENCE_REF_KEYS:
        value = terminal_life_loop_state.get(key)
        if isinstance(value, str) and value:
            payload[key] = value
            evidence_refs.append(value)

    focus = terminal_life_loop_state.get("background_trait_convergence_history_focus")
    if isinstance(focus, str) and focus:
        payload["background_trait_convergence_history_focus"] = focus

    for key in (
        "background_trait_convergence_unstable_names",
        "background_trait_convergence_stable_names",
    ):
        names = _string_list(terminal_life_loop_state.get(key))
        if names:
            payload[key] = names

    profile = terminal_life_loop_state.get("background_trait_convergence_history_profile")
    if isinstance(profile, dict) and profile:
        payload["background_trait_convergence_history_profile"] = dict(profile)

    if evidence_refs:
        payload["background_trait_convergence_evidence_refs"] = evidence_refs
    return payload


def build_resident_background_lineage_payload(
    terminal_life_loop_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not terminal_life_loop_state:
        return {}
    lineage_state = terminal_life_loop_state.get("resident_background_lineage_state")
    if not isinstance(lineage_state, dict) or not lineage_state:
        return {}

    payload: dict[str, Any] = {
        "resident_background_lineage_state": dict(lineage_state),
    }
    for key in (
        "schema_version",
        "governance_phase",
        "depth_band",
        "waiting_posture",
        "cadence_weight",
        "generation",
    ):
        value = lineage_state.get(key)
        if value not in {None, ""}:
            payload[f"resident_background_lineage_{key}"] = value
    lineage_refs: list[str] = []
    for key in (
        "evidence_refs",
        "continuity_refs",
        "source_refs",
    ):
        lineage_refs.extend(_string_list(lineage_state.get(key)))
    if lineage_refs:
        payload["resident_background_lineage_evidence_refs"] = _dedupe_string_list(
            lineage_refs
        )
    for key in (
        "relationship_presence",
        "trait_convergence_presence",
        "heartbeat_presence",
        "language_presence",
    ):
        presence = lineage_state.get(key)
        if isinstance(presence, dict) and presence:
            payload[f"resident_background_lineage_{key}"] = dict(presence)
    return payload


def build_offline_learning_cumulative_payload(
    terminal_life_loop_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not terminal_life_loop_state:
        return {}
    profile = terminal_life_loop_state.get("offline_learning_cumulative_profile")
    if not isinstance(profile, dict):
        profile = {}
    priority_profile = (
        terminal_life_loop_state.get("offline_learning_cumulative_priority_profile")
        or profile.get("priority_profile")
        or {}
    )
    if not isinstance(priority_profile, dict):
        priority_profile = {}
    ref_set = _dedupe_string_list(
        _string_list(
            terminal_life_loop_state.get("offline_learning_cumulative_ref_set")
            or profile.get("ref_set")
        )
    )
    generation = (
        terminal_life_loop_state.get("offline_learning_cumulative_generation")
        or profile.get("generation")
    )
    pressure_level = (
        terminal_life_loop_state.get("offline_learning_cumulative_pressure_level")
        or profile.get("pressure_level")
    )
    attention_target = (
        terminal_life_loop_state.get("offline_learning_cumulative_attention_target")
        or profile.get("attention_target")
    )
    if not any([profile, priority_profile, ref_set, generation, pressure_level, attention_target]):
        return {}

    payload: dict[str, Any] = {}
    if profile:
        payload["offline_learning_cumulative_profile"] = dict(profile)
    if generation is not None:
        payload["offline_learning_cumulative_generation"] = generation
    if pressure_level:
        payload["offline_learning_cumulative_pressure_level"] = str(pressure_level)
    if attention_target:
        payload["offline_learning_cumulative_attention_target"] = str(attention_target)
    if priority_profile:
        payload["offline_learning_cumulative_priority_profile"] = {
            str(key): str(value)
            for key, value in priority_profile.items()
            if value is not None
        }
    if ref_set:
        payload["offline_learning_cumulative_ref_set"] = ref_set
        payload["offline_learning_cumulative_evidence_refs"] = ref_set
    return payload


def build_prediction_write_gate_payload(
    *,
    terminal_life_loop_state: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    signal_media_runtime_ref: str | None = None,
    belief_state_ref: str | None = None,
    prediction_error_field_ref: str | None = None,
    active_sampling_plan_ref: str | None = None,
    memory_write_gate_ref: str | None = None,
    state_merge_guard_ref: str | None = None,
) -> dict[str, Any]:
    terminal_life_loop_state = terminal_life_loop_state or {}
    profile = _derive_prediction_write_gate_profile(
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        memory_write_gate=memory_write_gate,
        state_merge_guard=state_merge_guard,
    )
    payload: dict[str, Any] = {}

    for key in (
        "signal_media_ref",
        "belief_state_ref",
        "prediction_error_ref",
        "active_sampling_plan_ref",
        "memory_write_gate_ref",
        "state_merge_guard_ref",
    ):
        value = terminal_life_loop_state.get(key)
        if value:
            payload[key] = value
    explicit_ref_values = {
        "signal_media_ref": signal_media_runtime_ref,
        "belief_state_ref": belief_state_ref,
        "prediction_error_ref": prediction_error_field_ref,
        "active_sampling_plan_ref": active_sampling_plan_ref,
        "memory_write_gate_ref": memory_write_gate_ref,
        "state_merge_guard_ref": state_merge_guard_ref,
    }
    for key, value in explicit_ref_values.items():
        if value and key not in payload:
            payload[key] = value

    prediction_refs = [
        *_string_list(terminal_life_loop_state.get("prediction_write_gate_refs")),
        *[ref for ref in explicit_ref_values.values() if ref],
    ]
    if prediction_refs:
        payload["prediction_write_gate_refs"] = _dedupe_string_list(prediction_refs)

    for key in (
        "prediction_waiting_posture",
        "response_surface_posture_hint",
        "prediction_attention_target",
        "prediction_attention_reason",
        "prediction_error_count",
        "active_sampling_route",
        "memory_write_gate_policy",
        "state_merge_policy",
    ):
        value = terminal_life_loop_state.get(key, profile.get(key))
        if _present_value(value):
            payload[key] = value
    return payload


def _derive_prediction_write_gate_profile(
    *,
    signal_media_runtime: dict[str, Any] | None,
    belief_state: dict[str, Any] | None,
    prediction_error_field: dict[str, Any] | None,
    active_sampling_plan: dict[str, Any] | None,
    memory_write_gate: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
) -> dict[str, Any]:
    selected_route = str((active_sampling_plan or {}).get("selected_route", ""))
    route_lower = selected_route.lower()
    stage_effect = str((active_sampling_plan or {}).get("stage_effect", ""))
    stage_lower = stage_effect.lower()
    error_events = (prediction_error_field or {}).get("error_events", [])
    error_count = len(error_events) if isinstance(error_events, list) else 0
    modulation_vector = (signal_media_runtime or {}).get("modulation_vector", {})
    repair_drive = str(
        (modulation_vector if isinstance(modulation_vector, dict) else {}).get(
            "repair_drive", ""
        )
    ).lower()
    confidence_level = str((belief_state or {}).get("confidence_level", "")).lower()
    memory_policy = str((memory_write_gate or {}).get("stage_policy", ""))
    memory_policy_lower = memory_policy.lower()
    merge_policy = str((state_merge_guard or {}).get("stage_policy", ""))

    has_prediction_objects = any(
        [
            signal_media_runtime,
            belief_state,
            prediction_error_field,
            active_sampling_plan,
            memory_write_gate,
            state_merge_guard,
        ]
    )
    if not has_prediction_objects:
        return {}
    if "clarify" in route_lower:
        return {
            "prediction_waiting_posture": "hold_for_evidence",
            "response_surface_posture_hint": "question",
            "prediction_attention_target": "active_sampling_plan",
            "prediction_attention_reason": "selected_route_requires_relation_subject_clarification",
            "prediction_error_count": error_count,
            "active_sampling_route": selected_route,
            "memory_write_gate_policy": memory_policy,
            "state_merge_policy": merge_policy,
        }
    if "hold_for_evidence" in stage_lower or error_count > 0:
        return {
            "prediction_waiting_posture": "hold_for_evidence",
            "response_surface_posture_hint": "hold",
            "prediction_attention_target": "prediction_error_field",
            "prediction_attention_reason": "prediction_error_requires_evidence_hold",
            "prediction_error_count": error_count,
            "active_sampling_route": selected_route,
            "memory_write_gate_policy": memory_policy,
            "state_merge_policy": merge_policy,
        }
    if repair_drive == "active" or "repair" in route_lower or "repair" in memory_policy_lower:
        return {
            "prediction_waiting_posture": "repair_write_guard",
            "response_surface_posture_hint": "repair",
            "prediction_attention_target": "memory_write_gate",
            "prediction_attention_reason": "repair_drive_or_write_gate_requires_repair_posture",
            "prediction_error_count": error_count,
            "active_sampling_route": selected_route,
            "memory_write_gate_policy": memory_policy,
            "state_merge_policy": merge_policy,
        }
    if confidence_level in {"stable", "high", "confirmed"}:
        return {
            "prediction_waiting_posture": "confirm_when_stable",
            "response_surface_posture_hint": "confirm",
            "prediction_attention_target": "belief_state",
            "prediction_attention_reason": "stable_belief_frame_allows_confirmation",
            "prediction_error_count": error_count,
            "active_sampling_route": selected_route,
            "memory_write_gate_policy": memory_policy,
            "state_merge_policy": merge_policy,
        }
    return {
        "prediction_waiting_posture": "baseline_prediction_monitoring",
        "response_surface_posture_hint": "hold",
        "prediction_attention_target": "prediction_workspace",
        "prediction_attention_reason": "prediction_objects_present_without_escalation",
        "prediction_error_count": error_count,
        "active_sampling_route": selected_route,
        "memory_write_gate_policy": memory_policy,
        "state_merge_policy": merge_policy,
    }


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _present_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str) and not value:
        return False
    if isinstance(value, (list, tuple, dict, set)) and not value:
        return False
    return True


def _dedupe_string_list(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
