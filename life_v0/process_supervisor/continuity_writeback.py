from __future__ import annotations

from typing import Any


def build_idle_continuity_frame(
    *,
    run_id: str,
    generated_at: str,
    heartbeat_counter: int,
    heartbeat_report_ref: str,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    relationship_timeline_ref: str | None = None,
    commitment_expression_plan_ref: str | None = None,
    apology_repair_language_trace_ref: str | None = None,
    replay_cue_bundle_ref: str | None = None,
    offline_consolidation_frame_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None = None,
    nightmare_risk_ref: str | None = None,
    belief_learning_plan_ref: str | None = None,
    language_learning_plan_ref: str | None = None,
    relationship_learning_plan_ref: str | None = None,
    growth_patch_candidate_ids: list[str] | None = None,
    replay_residue_ref_count: int = 0,
    dream_window_ref_count: int = 0,
    growth_patch_candidate_count: int = 0,
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    world_contact_release_posture: str | None = None,
    repair_followup_required: bool = False,
    offline_learning_pressure_level: str | None = None,
    offline_learning_attention_target: str | None = None,
    background_continuity_mode: str | None = None,
    background_carryover_pressure_level: str | None = None,
    background_carryover_attention_target: str | None = None,
    background_carryover_generation: int | None = None,
    background_carryover_parent_run_id: str | None = None,
    background_carryover_source_ref_set: list[str] | None = None,
    background_continuity_ref_set: list[str] | None = None,
    background_resident_governance_state_ref: str | None = None,
    background_convergence_summary_ref: str | None = None,
    background_convergence_history_ref: str | None = None,
    background_convergence_history_trend_state: str | None = None,
    background_convergence_history_window_size: int | None = None,
    background_trait_convergence_history_profile: dict[str, Any] | None = None,
    background_trait_convergence_unstable_names: list[str] | None = None,
    background_trait_convergence_stable_names: list[str] | None = None,
    background_trait_convergence_history_focus: str | None = None,
    background_convergence_state: str | None = None,
    background_convergence_pressure_level: str | None = None,
    background_convergence_attention_target: str | None = None,
    background_resident_governance_explanation_ref: str | None = None,
    background_governance_driver_family: str | None = None,
    background_next_wake_expectation: str | None = None,
    background_governance_explanation_story: list[str] | None = None,
    background_trait_drift_monitor_ref: str | None = None,
    background_lineage_governance_profile: dict[str, Any] | None = None,
    background_lineage_depth_band: str | None = None,
    background_lineage_waiting_posture: str | None = None,
    background_lineage_cadence_weight: str | None = None,
    background_lineage_evidence_ref_count: int | None = None,
    background_idle_heartbeat_trace_ref: str | None = None,
    background_idle_heartbeat_trace_count: int | None = None,
    signal_media_ref: str | None = None,
    belief_state_ref: str | None = None,
    prediction_error_ref: str | None = None,
    active_sampling_plan_ref: str | None = None,
    memory_write_gate_ref: str | None = None,
    state_merge_guard_ref: str | None = None,
    prediction_write_gate_refs: list[str] | None = None,
    prediction_waiting_posture: str | None = None,
    response_surface_posture_hint: str | None = None,
) -> dict[str, Any]:
    replay_seed_refs = ["runtime/state/life_state.json#memory_index.replay_cues"]
    if replay_cue_bundle_ref:
        replay_seed_refs.append(replay_cue_bundle_ref)
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    payload = {
        "schema_version": "idle_continuity_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "idle_continuity_id": f"idle-continuity-{run_id}-{heartbeat_counter:04d}",
        "event_kind": "waiting_heartbeat_refresh",
        "heartbeat_counter": heartbeat_counter,
        "heartbeat_ref": heartbeat_report_ref,
        "self_narrative_idle_refs": [heartbeat_report_ref],
        "commitment_idle_refs": [heartbeat_report_ref],
        "relationship_idle_refs": [heartbeat_report_ref],
        "replay_seed_refs": replay_seed_refs,
        "waiting_state": "restored_waiting_for_external_turn",
        "self_narrative_ref": "runtime/state/language/self_narrative_language_trace.json",
        "commitment_index_ref": "runtime/state/language/commitment_repair_language_index.json",
        "relationship_graph_ref": "runtime/state/relationship/relationship_subject_graph.json",
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "long_horizon_language_refs": [
            ref
            for ref in [
                relationship_timeline_ref,
                commitment_expression_plan_ref,
                apology_repair_language_trace_ref,
            ]
            if ref
        ],
        "replay_cue_bundle_ref": replay_cue_bundle_ref,
        "offline_consolidation_frame_ref": offline_consolidation_frame_ref,
        "growth_patch_candidate_queue_ref": growth_patch_candidate_queue_ref,
        "nightmare_risk_ref": nightmare_risk_ref,
        "belief_learning_plan_ref": belief_learning_plan_ref,
        "language_learning_plan_ref": language_learning_plan_ref,
        "relationship_learning_plan_ref": relationship_learning_plan_ref,
        "growth_patch_candidate_ids": list(growth_patch_candidate_ids or []),
        "replay_residue_ref_count": replay_residue_ref_count,
        "dream_window_ref_count": dream_window_ref_count,
        "growth_patch_candidate_count": growth_patch_candidate_count,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }
    if responsibility_loop_state_ref:
        payload["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        payload["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        payload["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        payload["membrane_guard_refs"] = membrane_guard_refs
    if world_contact_release_posture:
        payload["world_contact_release_posture"] = world_contact_release_posture
    if repair_followup_required:
        payload["repair_followup_required"] = True
    if offline_learning_pressure_level:
        payload["offline_learning_pressure_level"] = offline_learning_pressure_level
    if offline_learning_attention_target:
        payload["offline_learning_attention_target"] = offline_learning_attention_target
    if background_continuity_mode:
        payload["background_continuity_mode"] = background_continuity_mode
    if background_carryover_pressure_level:
        payload["background_carryover_pressure_level"] = background_carryover_pressure_level
    if background_carryover_attention_target:
        payload["background_carryover_attention_target"] = background_carryover_attention_target
    if background_carryover_generation is not None:
        payload["background_carryover_generation"] = int(background_carryover_generation)
    if background_carryover_parent_run_id:
        payload["background_carryover_parent_run_id"] = background_carryover_parent_run_id
    if background_carryover_source_ref_set:
        payload["background_carryover_source_ref_set"] = list(background_carryover_source_ref_set)
    if background_continuity_ref_set:
        payload["background_continuity_ref_set"] = list(background_continuity_ref_set)
    if background_resident_governance_state_ref:
        payload["background_resident_governance_state_ref"] = (
            background_resident_governance_state_ref
        )
    if background_convergence_summary_ref:
        payload["background_convergence_summary_ref"] = background_convergence_summary_ref
    if background_convergence_history_ref:
        payload["background_convergence_history_ref"] = background_convergence_history_ref
    if background_convergence_history_trend_state:
        payload["background_convergence_history_trend_state"] = (
            background_convergence_history_trend_state
        )
    if background_convergence_history_window_size is not None:
        payload["background_convergence_history_window_size"] = int(
            background_convergence_history_window_size
        )
    if background_trait_convergence_history_profile:
        payload["background_trait_convergence_history_profile"] = dict(
            background_trait_convergence_history_profile
        )
    if background_trait_convergence_unstable_names:
        payload["background_trait_convergence_unstable_names"] = list(
            background_trait_convergence_unstable_names
        )
    if background_trait_convergence_stable_names:
        payload["background_trait_convergence_stable_names"] = list(
            background_trait_convergence_stable_names
        )
    if background_trait_convergence_history_focus:
        payload["background_trait_convergence_history_focus"] = (
            background_trait_convergence_history_focus
        )
    if background_convergence_state:
        payload["background_convergence_state"] = background_convergence_state
    if background_convergence_pressure_level:
        payload["background_convergence_pressure_level"] = (
            background_convergence_pressure_level
        )
    if background_convergence_attention_target:
        payload["background_convergence_attention_target"] = (
            background_convergence_attention_target
        )
    if background_resident_governance_explanation_ref:
        payload["background_resident_governance_explanation_ref"] = (
            background_resident_governance_explanation_ref
        )
    if background_governance_driver_family:
        payload["background_governance_driver_family"] = (
            background_governance_driver_family
        )
    if background_next_wake_expectation:
        payload["background_next_wake_expectation"] = background_next_wake_expectation
    if background_governance_explanation_story:
        payload["background_governance_explanation_story"] = list(
            background_governance_explanation_story
        )
    if background_trait_drift_monitor_ref:
        payload["background_trait_drift_monitor_ref"] = background_trait_drift_monitor_ref
    if background_lineage_governance_profile:
        payload["background_lineage_governance_profile"] = dict(
            background_lineage_governance_profile
        )
    if background_lineage_depth_band:
        payload["background_lineage_depth_band"] = background_lineage_depth_band
    if background_lineage_waiting_posture:
        payload["background_lineage_waiting_posture"] = (
            background_lineage_waiting_posture
        )
    if background_lineage_cadence_weight:
        payload["background_lineage_cadence_weight"] = (
            background_lineage_cadence_weight
        )
    if background_lineage_evidence_ref_count is not None:
        payload["background_lineage_evidence_ref_count"] = int(
            background_lineage_evidence_ref_count
        )
    if background_idle_heartbeat_trace_ref:
        payload["background_idle_heartbeat_trace_ref"] = (
            background_idle_heartbeat_trace_ref
        )
    if background_idle_heartbeat_trace_count is not None:
        payload["background_idle_heartbeat_trace_count"] = int(
            background_idle_heartbeat_trace_count
        )
    if signal_media_ref:
        payload["signal_media_ref"] = signal_media_ref
    if belief_state_ref:
        payload["belief_state_ref"] = belief_state_ref
    if prediction_error_ref:
        payload["prediction_error_ref"] = prediction_error_ref
    if active_sampling_plan_ref:
        payload["active_sampling_plan_ref"] = active_sampling_plan_ref
    if memory_write_gate_ref:
        payload["memory_write_gate_ref"] = memory_write_gate_ref
    if state_merge_guard_ref:
        payload["state_merge_guard_ref"] = state_merge_guard_ref
    if prediction_write_gate_refs:
        payload["prediction_write_gate_refs"] = list(prediction_write_gate_refs)
    if prediction_waiting_posture:
        payload["prediction_waiting_posture"] = prediction_waiting_posture
    if response_surface_posture_hint:
        payload["response_surface_posture_hint"] = response_surface_posture_hint
    return payload


def record_idle_continuity(
    *,
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    heartbeat_counter: int,
    heartbeat_report_ref: str,
) -> None:
    self_narrative_trace.setdefault("idle_continuity_refs", [])
    self_narrative_trace["idle_continuity_refs"].append(heartbeat_report_ref)
    self_narrative_trace["idle_continuity_counter"] = heartbeat_counter
    self_narrative_trace["last_idle_continuity"] = {
        "event_kind": "waiting_heartbeat_refresh",
        "heartbeat_counter": heartbeat_counter,
        "heartbeat_ref": heartbeat_report_ref,
    }

    commitment_index.setdefault("idle_presence_refs", [])
    commitment_index["idle_presence_refs"].append(heartbeat_report_ref)
    commitment_index["idle_presence_counter"] = heartbeat_counter
    commitment_index["last_idle_presence"] = {
        "event_kind": "waiting_heartbeat_refresh",
        "heartbeat_counter": heartbeat_counter,
        "heartbeat_ref": heartbeat_report_ref,
    }

    relationship_graph.setdefault("idle_presence_refs", [])
    relationship_graph["idle_presence_refs"].append(heartbeat_report_ref)
    relationship_graph["idle_presence_counter"] = heartbeat_counter

    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        subjects[0]["idle_presence_counter"] = heartbeat_counter
        subjects[0]["last_idle_continuity_event_kind"] = "waiting_heartbeat_refresh"
        subjects[0]["last_idle_continuity_report_ref"] = heartbeat_report_ref
