from __future__ import annotations

from typing import Any

from .state_merge_signals import state_merge_long_term_change_profile
from .trait_convergence_signals import (
    BACKGROUND_TRAIT_CONVERGENCE_REF_KEYS,
    cross_wake_trait_convergence_profile,
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
    event.update(build_life_constraint_payload(terminal_life_loop_state))
    event.update(build_queue_e_birth_repair_payload(terminal_life_loop_state))
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
    payload.update(cross_wake_trait_convergence_profile(terminal_life_loop_state))
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
    for key in (
        "relationship_presence",
        "trait_convergence_presence",
        "heartbeat_presence",
        "language_presence",
        "state_merge_presence",
        "identity_consciousness_birth_presence",
        "resident_process_identity_presence",
        "offline_learning_presence",
        "dream_wake_presence",
    ):
        presence = lineage_state.get(key)
        if isinstance(presence, dict) and presence:
            payload[f"resident_background_lineage_{key}"] = dict(presence)
    trait_convergence_presence = lineage_state.get("trait_convergence_presence")
    if isinstance(trait_convergence_presence, dict):
        focus = trait_convergence_presence.get("trait_convergence_history_focus")
        unstable_names = _dedupe_string_list(
            _string_list(
                trait_convergence_presence.get("trait_convergence_unstable_names")
            )
        )
        stable_names = _dedupe_string_list(
            _string_list(
                trait_convergence_presence.get("trait_convergence_stable_names")
            )
        )
        trait_drift_update_mode_summary = trait_convergence_presence.get(
            "trait_drift_update_mode_summary"
        )
        if not isinstance(trait_drift_update_mode_summary, dict):
            trait_drift_update_mode_summary = {}
        trait_drift_recalibration_names = _dedupe_string_list(
            _string_list(
                trait_convergence_presence.get("trait_drift_recalibration_names")
            )
            or _string_list(
                trait_drift_update_mode_summary.get(
                    "background_history_recalibration"
                )
            )
        )
        trait_drift_stabilized_names = _dedupe_string_list(
            _string_list(
                trait_convergence_presence.get("trait_drift_stabilized_names")
            )
            or _string_list(
                trait_drift_update_mode_summary.get("background_history_stabilized")
            )
        )
        trait_refs = _dedupe_string_list(
            _string_list(
                trait_convergence_presence.get("trait_convergence_evidence_refs")
            )
        )
        trait_drift_monitor_ref = trait_convergence_presence.get(
            "trait_drift_monitor_ref"
        )
        if isinstance(trait_drift_monitor_ref, str) and trait_drift_monitor_ref:
            trait_refs = _dedupe_string_list([*trait_refs, trait_drift_monitor_ref])
            payload["resident_background_lineage_trait_drift_monitor_ref"] = (
                trait_drift_monitor_ref
            )
        if focus not in {None, ""}:
            payload["resident_background_lineage_trait_convergence_history_focus"] = (
                focus
            )
        if unstable_names:
            payload[
                "resident_background_lineage_trait_convergence_unstable_names"
            ] = unstable_names
        if stable_names:
            payload[
                "resident_background_lineage_trait_convergence_stable_names"
            ] = stable_names
        if trait_drift_update_mode_summary:
            payload[
                "resident_background_lineage_trait_drift_update_mode_summary"
            ] = dict(trait_drift_update_mode_summary)
        if trait_drift_recalibration_names:
            payload[
                "resident_background_lineage_trait_drift_recalibration_names"
            ] = trait_drift_recalibration_names
        if trait_drift_stabilized_names:
            payload[
                "resident_background_lineage_trait_drift_stabilized_names"
            ] = trait_drift_stabilized_names
        if trait_convergence_presence.get("trait_convergence_score") is not None:
            payload["resident_background_lineage_trait_convergence_score"] = (
                trait_convergence_presence.get("trait_convergence_score")
            )
        if isinstance(
            trait_convergence_presence.get("trait_convergence_history_profile"),
            dict,
        ) and trait_convergence_presence.get("trait_convergence_history_profile"):
            payload[
                "resident_background_lineage_trait_convergence_history_profile"
            ] = dict(
                trait_convergence_presence["trait_convergence_history_profile"]
            )
        if trait_refs:
            payload["resident_background_lineage_trait_convergence_refs"] = trait_refs
            lineage_refs.extend(trait_refs)
    language_presence = lineage_state.get("language_presence")
    if isinstance(language_presence, dict):
        live_language_refs = _dedupe_string_list(
            _string_list(language_presence.get("live_language_turn_refs"))
        )
        background_live_language_refs = _dedupe_string_list(
            _string_list(language_presence.get("background_live_language_turn_refs"))
        )
        long_horizon_language_refs = _dedupe_string_list(
            _string_list(language_presence.get("long_horizon_language_refs"))
        )
        live_language_presence_refs = _dedupe_string_list(
            [
                *long_horizon_language_refs,
                *live_language_refs,
                *background_live_language_refs,
            ]
        )
        semantic_focus = (
            language_presence.get("last_live_semantic_focus")
            or language_presence.get("background_last_live_semantic_focus")
        )
        if live_language_refs:
            payload["resident_background_lineage_live_language_refs"] = (
                live_language_refs
            )
            lineage_refs.extend(live_language_refs)
        if background_live_language_refs:
            payload["resident_background_lineage_background_live_language_refs"] = (
                background_live_language_refs
            )
            lineage_refs.extend(background_live_language_refs)
        if semantic_focus not in {None, ""}:
            payload["resident_background_lineage_last_live_semantic_focus"] = (
                semantic_focus
            )
        if live_language_presence_refs:
            payload["resident_background_lineage_language_evidence_refs"] = (
                live_language_presence_refs
            )
            lineage_refs.extend(live_language_presence_refs)
    state_merge_presence = lineage_state.get("state_merge_presence")
    if isinstance(state_merge_presence, dict):
        state_merge_guard_ref = state_merge_presence.get("state_merge_guard_ref")
        state_merge_policy = state_merge_presence.get("state_merge_policy")
        state_merge_refs = _dedupe_string_list(
            _string_list(state_merge_presence.get("state_merge_evidence_refs"))
            or (
                _string_list(state_merge_presence.get("long_term_change_refs"))
                + _string_list([state_merge_guard_ref])
            )
        )
        state_merge_families = _dedupe_string_list(
            _string_list(state_merge_presence.get("long_term_change_families"))
        )
        if isinstance(state_merge_guard_ref, str) and state_merge_guard_ref:
            payload["resident_background_lineage_state_merge_guard_ref"] = (
                state_merge_guard_ref
            )
        if isinstance(state_merge_policy, str) and state_merge_policy:
            payload["resident_background_lineage_state_merge_policy"] = (
                state_merge_policy
            )
        if state_merge_presence.get("long_term_change_count") is not None:
            payload[
                "resident_background_lineage_state_merge_long_term_change_count"
            ] = state_merge_presence.get("long_term_change_count")
        if state_merge_families:
            payload[
                "resident_background_lineage_state_merge_long_term_change_families"
            ] = state_merge_families
        if state_merge_refs:
            payload["resident_background_lineage_state_merge_refs"] = (
                state_merge_refs
            )
            lineage_refs.extend(state_merge_refs)
    identity_consciousness_birth_presence = lineage_state.get(
        "identity_consciousness_birth_presence"
    )
    if isinstance(identity_consciousness_birth_presence, dict):
        for source_key, target_key in (
            ("workspace_frame_ref", "resident_background_lineage_workspace_frame_ref"),
            ("broadcast_frame_ref", "resident_background_lineage_broadcast_frame_ref"),
            ("metacognition_ref", "resident_background_lineage_metacognition_ref"),
            (
                "consciousness_probe_ref",
                "resident_background_lineage_consciousness_probe_ref",
            ),
            (
                "birth_readiness_rollup_ref",
                "resident_background_lineage_birth_readiness_rollup_ref",
            ),
            (
                "birth_readiness_stage_gate_ref",
                "resident_background_lineage_birth_readiness_stage_gate_ref",
            ),
            (
                "consciousness_waiting_posture",
                "resident_background_lineage_consciousness_waiting_posture",
            ),
            (
                "consciousness_attention_target",
                "resident_background_lineage_consciousness_attention_target",
            ),
            (
                "consciousness_attention_reason",
                "resident_background_lineage_consciousness_attention_reason",
            ),
            (
                "birth_readiness_waiting_posture",
                "resident_background_lineage_birth_readiness_waiting_posture",
            ),
            (
                "birth_readiness_attention_target",
                "resident_background_lineage_birth_readiness_attention_target",
            ),
            (
                "birth_readiness_attention_reason",
                "resident_background_lineage_birth_readiness_attention_reason",
            ),
            (
                "birth_readiness_decision",
                "resident_background_lineage_birth_readiness_decision",
            ),
            (
                "birth_readiness_next_required_command",
                "resident_background_lineage_birth_readiness_next_required_command",
            ),
        ):
            value = identity_consciousness_birth_presence.get(source_key)
            if value not in {None, ""}:
                payload[target_key] = value
        consciousness_flags = _dedupe_string_list(
            _string_list(
                identity_consciousness_birth_presence.get(
                    "consciousness_reportability_flags"
                )
            )
        )
        blocked_reasons = _dedupe_string_list(
            _string_list(
                identity_consciousness_birth_presence.get(
                    "birth_readiness_blocked_reasons"
                )
            )
        )
        identity_consciousness_birth_refs = _dedupe_string_list(
            _string_list(
                identity_consciousness_birth_presence.get(
                    "identity_consciousness_birth_refs"
                )
            )
            or _string_list(
                [
                    identity_consciousness_birth_presence.get("workspace_frame_ref"),
                    identity_consciousness_birth_presence.get("broadcast_frame_ref"),
                    identity_consciousness_birth_presence.get("metacognition_ref"),
                    identity_consciousness_birth_presence.get(
                        "consciousness_probe_ref"
                    ),
                    identity_consciousness_birth_presence.get(
                        "birth_readiness_rollup_ref"
                    ),
                    identity_consciousness_birth_presence.get(
                        "birth_readiness_stage_gate_ref"
                    ),
                ]
            )
        )
        if consciousness_flags:
            payload[
                "resident_background_lineage_consciousness_reportability_flags"
            ] = consciousness_flags
        if blocked_reasons:
            payload[
                "resident_background_lineage_birth_readiness_blocked_reasons"
            ] = blocked_reasons
        if identity_consciousness_birth_refs:
            payload[
                "resident_background_lineage_identity_consciousness_birth_refs"
            ] = identity_consciousness_birth_refs
            lineage_refs.extend(identity_consciousness_birth_refs)
    resident_process_identity_presence = lineage_state.get(
        "resident_process_identity_presence"
    )
    if isinstance(resident_process_identity_presence, dict):
        for source_key, target_key in (
            (
                "resident_process_lease_ref",
                "resident_background_lineage_resident_process_lease_ref",
            ),
            (
                "resident_process_lease_history_ref",
                "resident_background_lineage_resident_process_lease_history_ref",
            ),
            (
                "resident_process_lease_history_profile_ref",
                "resident_background_lineage_resident_process_lease_history_profile_ref",
            ),
            (
                "resident_process_identity_continuity_state",
                "resident_background_lineage_resident_process_identity_continuity_state",
            ),
            (
                "resident_process_identity_pressure_level",
                "resident_background_lineage_resident_process_identity_pressure_level",
            ),
        ):
            value = resident_process_identity_presence.get(source_key)
            if value not in {None, ""}:
                payload[target_key] = value
        if (
            resident_process_identity_presence.get(
                "resident_process_lease_history_event_count"
            )
            is not None
        ):
            payload[
                "resident_background_lineage_resident_process_lease_history_event_count"
            ] = resident_process_identity_presence[
                "resident_process_lease_history_event_count"
            ]
        recent_process_ids = _dedupe_string_list(
            _string_list(
                resident_process_identity_presence.get("resident_process_recent_ids")
            )
        )
        recent_run_ids = _dedupe_string_list(
            _string_list(
                resident_process_identity_presence.get(
                    "resident_process_recent_run_ids"
                )
            )
        )
        resident_process_identity_refs = _dedupe_string_list(
            _string_list(
                resident_process_identity_presence.get(
                    "resident_process_identity_refs"
                )
            )
            or _string_list(
                [
                    resident_process_identity_presence.get(
                        "resident_process_lease_ref"
                    ),
                    resident_process_identity_presence.get(
                        "resident_process_lease_history_ref"
                    ),
                    resident_process_identity_presence.get(
                        "resident_process_lease_history_profile_ref"
                    ),
                ]
            )
        )
        if recent_process_ids:
            payload[
                "resident_background_lineage_resident_process_recent_ids"
            ] = recent_process_ids
        if recent_run_ids:
            payload[
                "resident_background_lineage_resident_process_recent_run_ids"
            ] = recent_run_ids
        if resident_process_identity_refs:
            payload[
                "resident_background_lineage_resident_process_identity_refs"
            ] = resident_process_identity_refs
            lineage_refs.extend(resident_process_identity_refs)
    offline_presence = lineage_state.get("offline_learning_presence")
    if isinstance(offline_presence, dict):
        for source_key, target_key in (
            ("generation", "resident_background_lineage_offline_learning_generation"),
            (
                "pressure_level",
                "resident_background_lineage_offline_learning_pressure_level",
            ),
            (
                "attention_target",
                "resident_background_lineage_offline_learning_attention_target",
            ),
        ):
            value = offline_presence.get(source_key)
            if value not in {None, ""}:
                payload[target_key] = value
        offline_refs = _dedupe_string_list(_string_list(offline_presence.get("ref_set")))
        if offline_refs:
            payload["resident_background_lineage_offline_learning_refs"] = offline_refs
            lineage_refs.extend(offline_refs)
    dream_wake_presence = lineage_state.get("dream_wake_presence")
    if isinstance(dream_wake_presence, dict):
        for source_key, target_key in (
            ("dream_window_kind", "resident_background_lineage_dream_window_kind"),
            ("dream_fact_gate_result", "resident_background_lineage_dream_fact_gate_result"),
            ("wake_archive_requirement", "resident_background_lineage_wake_archive_requirement"),
        ):
            value = dream_wake_presence.get(source_key)
            if value not in {None, ""}:
                payload[target_key] = value
        for source_key, target_key in (
            ("wake_growth_seed_count", "resident_background_lineage_wake_growth_seed_count"),
            ("wake_repair_target_count", "resident_background_lineage_wake_repair_target_count"),
            ("dream_fact_gate_ref_count", "resident_background_lineage_dream_fact_gate_ref_count"),
        ):
            value = dream_wake_presence.get(source_key)
            if value not in {None, ""}:
                payload[target_key] = value
        dream_wake_refs = _dedupe_string_list(
            _string_list(dream_wake_presence.get("ref_set"))
        )
        if dream_wake_refs:
            payload["resident_background_lineage_dream_wake_refs"] = (
                dream_wake_refs
            )
            lineage_refs.extend(dream_wake_refs)
    if lineage_refs:
        payload["resident_background_lineage_evidence_refs"] = _dedupe_string_list(
            lineage_refs
        )
    return payload


def build_offline_learning_cumulative_payload(
    terminal_life_loop_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not terminal_life_loop_state:
        return {}
    profile = terminal_life_loop_state.get("offline_learning_cumulative_profile")
    if not isinstance(profile, dict):
        profile = {}
    lineage_state = terminal_life_loop_state.get("resident_background_lineage_state")
    if not isinstance(lineage_state, dict):
        lineage_state = {}
    offline_learning_presence = lineage_state.get("offline_learning_presence")
    if not isinstance(offline_learning_presence, dict):
        offline_learning_presence = {}
    priority_profile = (
        terminal_life_loop_state.get("offline_learning_cumulative_priority_profile")
        or profile.get("priority_profile")
        or offline_learning_presence.get("priority_profile")
        or {}
    )
    if not isinstance(priority_profile, dict):
        priority_profile = {}
    ref_set = _dedupe_string_list(
        _string_list(
            terminal_life_loop_state.get("offline_learning_cumulative_ref_set")
            or profile.get("ref_set")
            or offline_learning_presence.get("ref_set")
        )
    )
    generation = (
        terminal_life_loop_state.get("offline_learning_cumulative_generation")
        or profile.get("generation")
        or offline_learning_presence.get("generation")
    )
    pressure_level = (
        terminal_life_loop_state.get("offline_learning_cumulative_pressure_level")
        or profile.get("pressure_level")
        or offline_learning_presence.get("pressure_level")
    )
    attention_target = (
        terminal_life_loop_state.get("offline_learning_cumulative_attention_target")
        or profile.get("attention_target")
        or offline_learning_presence.get("attention_target")
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


def build_queue_e_birth_repair_payload(
    terminal_life_loop_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not terminal_life_loop_state:
        return {}
    profile = terminal_life_loop_state.get("queue_e_birth_repair_waiting_profile")
    if not isinstance(profile, dict):
        profile = {}

    gate_status = (
        terminal_life_loop_state.get("queue_e_birth_repair_gate_status")
        or profile.get("gate_status")
    )
    profile_ref = (
        terminal_life_loop_state.get("queue_e_birth_repair_profile_ref")
        or profile.get("profile_ref")
    )
    pressure_level = (
        terminal_life_loop_state.get("queue_e_birth_repair_pressure_level")
        or profile.get("pressure_level")
    )
    attention_target = (
        terminal_life_loop_state.get("queue_e_birth_repair_attention_target")
        or profile.get("attention_target")
    )
    waiting_posture = (
        terminal_life_loop_state.get("queue_e_birth_repair_waiting_posture")
        or profile.get("waiting_posture")
    )
    attention_reason = (
        terminal_life_loop_state.get("queue_e_birth_repair_attention_reason")
        or profile.get("attention_reason")
    )
    ref_set = _dedupe_string_list(
        _string_list(terminal_life_loop_state.get("queue_e_birth_repair_ref_set"))
        + _string_list(profile.get("ref_set"))
    )
    if isinstance(profile_ref, str) and profile_ref:
        ref_set = _dedupe_string_list([*ref_set, profile_ref])

    if not any(
        [
            profile,
            gate_status,
            profile_ref,
            pressure_level,
            attention_target,
            waiting_posture,
            attention_reason,
            ref_set,
        ]
    ):
        return {}

    payload: dict[str, Any] = {}
    if profile:
        payload["queue_e_birth_repair_waiting_profile"] = dict(profile)
    if gate_status:
        payload["queue_e_birth_repair_gate_status"] = str(gate_status)
    if profile_ref:
        payload["queue_e_birth_repair_profile_ref"] = str(profile_ref)
    if pressure_level:
        payload["queue_e_birth_repair_pressure_level"] = str(pressure_level)
    if attention_target:
        payload["queue_e_birth_repair_attention_target"] = str(attention_target)
    if waiting_posture:
        payload["queue_e_birth_repair_waiting_posture"] = str(waiting_posture)
    if attention_reason:
        payload["queue_e_birth_repair_attention_reason"] = str(attention_reason)
    if ref_set:
        payload["queue_e_birth_repair_ref_set"] = ref_set
        payload["queue_e_birth_repair_refs"] = ref_set
        payload["queue_e_birth_repair_evidence_refs"] = ref_set
    return payload


def build_life_constraint_payload(
    terminal_life_loop_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not terminal_life_loop_state:
        return {}

    gate_status = terminal_life_loop_state.get("queue_e_cross_layer_gate_status")
    if not isinstance(gate_status, dict):
        gate_status = {}
    schema_cross_file_logic_ref = terminal_life_loop_state.get(
        "schema_cross_file_logic_ref"
    )
    schema_run_manifest_ref = terminal_life_loop_state.get("schema_run_manifest_ref")
    life_constraint_refs = _dedupe_string_list(
        _string_list(terminal_life_loop_state.get("life_constraint_refs"))
    )
    evidence_refs = _dedupe_string_list(
        [
            *[
                str(ref)
                for ref in [schema_cross_file_logic_ref, schema_run_manifest_ref]
                if ref
            ],
            *life_constraint_refs,
        ]
    )
    waiting_posture = terminal_life_loop_state.get("life_constraint_waiting_posture")
    attention_target = terminal_life_loop_state.get("life_constraint_attention_target")
    attention_reason = terminal_life_loop_state.get("life_constraint_attention_reason")

    if not any(
        [
            gate_status,
            schema_cross_file_logic_ref,
            schema_run_manifest_ref,
            life_constraint_refs,
            waiting_posture,
            attention_target,
            attention_reason,
        ]
    ):
        return {}

    payload: dict[str, Any] = {}
    if schema_cross_file_logic_ref:
        payload["schema_cross_file_logic_ref"] = str(schema_cross_file_logic_ref)
    if schema_run_manifest_ref:
        payload["schema_run_manifest_ref"] = str(schema_run_manifest_ref)
    if gate_status:
        payload["queue_e_cross_layer_gate_status"] = {
            str(key): str(value)
            for key, value in gate_status.items()
            if value is not None
        }
    if life_constraint_refs:
        payload["life_constraint_refs"] = life_constraint_refs
    if waiting_posture:
        payload["life_constraint_waiting_posture"] = str(waiting_posture)
    if attention_target:
        payload["life_constraint_attention_target"] = str(attention_target)
    if attention_reason:
        payload["life_constraint_attention_reason"] = str(attention_reason)
    if evidence_refs:
        payload["life_constraint_evidence_refs"] = evidence_refs
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
        "state_merge_long_term_change_count",
        "state_merge_long_term_change_families",
        "state_merge_long_term_change_refs",
    ):
        value = profile.get(key) if profile else terminal_life_loop_state.get(key)
        if not _present_value(value):
            value = terminal_life_loop_state.get(key)
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
    state_merge_change_profile = state_merge_long_term_change_profile(
        state_merge_guard
    )

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
            **state_merge_change_profile,
        }
    if "repair" in route_lower:
        return {
            "prediction_waiting_posture": "repair_write_guard",
            "response_surface_posture_hint": "repair",
            "prediction_attention_target": "active_sampling_plan",
            "prediction_attention_reason": "active_sampling_route_prioritizes_repair_pressure",
            "prediction_error_count": error_count,
            "active_sampling_route": selected_route,
            "memory_write_gate_policy": memory_policy,
            "state_merge_policy": merge_policy,
            **state_merge_change_profile,
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
            **state_merge_change_profile,
        }
    if repair_drive == "active" or "repair" in memory_policy_lower:
        return {
            "prediction_waiting_posture": "repair_write_guard",
            "response_surface_posture_hint": "repair",
            "prediction_attention_target": "memory_write_gate",
            "prediction_attention_reason": "repair_drive_or_write_gate_requires_repair_posture",
            "prediction_error_count": error_count,
            "active_sampling_route": selected_route,
            "memory_write_gate_policy": memory_policy,
            "state_merge_policy": merge_policy,
            **state_merge_change_profile,
        }
    if state_merge_change_profile["state_merge_long_term_change_count"] > 0:
        return {
            "prediction_waiting_posture": "state_merge_long_term_integration_hold",
            "response_surface_posture_hint": "hold",
            "prediction_attention_target": "state_merge_guard",
            "prediction_attention_reason": "state_merge_guard_has_long_term_change_sources",
            "prediction_error_count": error_count,
            "active_sampling_route": selected_route,
            "memory_write_gate_policy": memory_policy,
            "state_merge_policy": merge_policy,
            **state_merge_change_profile,
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
            **state_merge_change_profile,
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
        **state_merge_change_profile,
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
