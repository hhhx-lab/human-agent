from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from .background_continuity import load_background_continuity_profile
from .background_lineage_state import build_resident_background_lineage_state
from .continuity_writeback import build_idle_continuity_frame, record_idle_continuity
from .idle_strategy import (
    IDLE_STRATEGY_STATE_REF,
    decide_idle_strategy,
    extract_idle_governance_fields,
)
from .persistent_process import (
    RESIDENT_GOVERNANCE_REPORT_REF,
    RESIDENT_GOVERNANCE_SNAPSHOT_REF,
    RESIDENT_GOVERNANCE_STATE_REF,
)


IDLE_HEARTBEAT_TRACE_REF = "runtime/state/terminal/idle_heartbeat_trace.jsonl"


def write_waiting_heartbeat(
    *,
    run_id: str,
    generated_at: str,
    terminal_dir: Path,
    reports_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    relationship_timeline: dict[str, Any] | None = None,
    commitment_expression_plan: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
    body_rhythm_pulse: dict[str, Any] | None = None,
    need_state_vector: dict[str, Any] | None = None,
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    dream_experience_window: dict[str, Any] | None = None,
    wake_integration_frame: dict[str, Any] | None = None,
    dream_fact_gate_decision: dict[str, Any] | None = None,
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
    schema_cross_file_logic: dict[str, Any] | None = None,
    schema_run_manifest: dict[str, Any] | None = None,
    workspace_frame: dict[str, Any] | None = None,
    broadcast_frame: dict[str, Any] | None = None,
    metacognition_state: dict[str, Any] | None = None,
    consciousness_probe: dict[str, Any] | None = None,
    birth_readiness_rollup: dict[str, Any] | None = None,
    birth_readiness_stage_gate: dict[str, Any] | None = None,
    replay_cue_bundle_ref: str | None = None,
    offline_consolidation_frame_ref: str | None = None,
    dream_experience_window_ref: str | None = None,
    wake_integration_frame_ref: str | None = None,
    dream_fact_gate_decision_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None = None,
    nightmare_risk_ref: str | None = None,
    belief_learning_plan_ref: str | None = None,
    language_learning_plan_ref: str | None = None,
    relationship_learning_plan_ref: str | None = None,
    signal_media_runtime_ref: str | None = None,
    belief_state_ref: str | None = None,
    prediction_error_field_ref: str | None = None,
    active_sampling_plan_ref: str | None = None,
    memory_write_gate_ref: str | None = None,
    state_merge_guard_ref: str | None = None,
    schema_cross_file_logic_ref: str | None = None,
    schema_run_manifest_ref: str | None = None,
    workspace_frame_ref: str | None = None,
    broadcast_frame_ref: str | None = None,
    metacognition_state_ref: str | None = None,
    consciousness_probe_ref: str | None = None,
    birth_readiness_rollup_ref: str | None = None,
    birth_readiness_stage_gate_ref: str | None = None,
    growth_patch_candidate_ids: list[str] | None = None,
    replay_residue_ref_count: int = 0,
    dream_window_ref_count: int = 0,
    growth_patch_candidate_count: int = 0,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> int:
    heartbeat_counter = int(safe_terminal_loop.get("heartbeat_counter", 0)) + 1
    heartbeat_report_ref = "runtime/reports/latest/digital_life_waiting_heartbeat.json"
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    background_continuity_profile = load_background_continuity_profile(
        terminal_dir=terminal_dir,
        reports_dir=reports_dir,
    )
    idle_strategy = decide_idle_strategy(
        run_id=run_id,
        generated_at=generated_at,
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
        idle_continuity_frame=None,
        relationship_timeline=relationship_timeline,
        commitment_expression_plan=commitment_expression_plan,
        apology_repair_language_trace=apology_repair_language_trace,
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        dream_experience_window=dream_experience_window,
        wake_integration_frame=wake_integration_frame,
        dream_fact_gate_decision=dream_fact_gate_decision,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        memory_write_gate=memory_write_gate,
        state_merge_guard=state_merge_guard,
        schema_cross_file_logic=schema_cross_file_logic,
        schema_run_manifest=schema_run_manifest,
        workspace_frame=workspace_frame,
        broadcast_frame=broadcast_frame,
        metacognition_state=metacognition_state,
        consciousness_probe=consciousness_probe,
        birth_readiness_rollup=birth_readiness_rollup,
        birth_readiness_stage_gate=birth_readiness_stage_gate,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        dream_experience_window_ref=dream_experience_window_ref,
        wake_integration_frame_ref=wake_integration_frame_ref,
        dream_fact_gate_decision_ref=dream_fact_gate_decision_ref,
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
        signal_media_runtime_ref=signal_media_runtime_ref,
        belief_state_ref=belief_state_ref,
        prediction_error_field_ref=prediction_error_field_ref,
        active_sampling_plan_ref=active_sampling_plan_ref,
        memory_write_gate_ref=memory_write_gate_ref,
        state_merge_guard_ref=state_merge_guard_ref,
        schema_cross_file_logic_ref=schema_cross_file_logic_ref,
        schema_run_manifest_ref=schema_run_manifest_ref,
        workspace_frame_ref=workspace_frame_ref,
        broadcast_frame_ref=broadcast_frame_ref,
        metacognition_state_ref=metacognition_state_ref,
        consciousness_probe_ref=consciousness_probe_ref,
        birth_readiness_rollup_ref=birth_readiness_rollup_ref,
        birth_readiness_stage_gate_ref=birth_readiness_stage_gate_ref,
        growth_patch_candidate_ids=growth_patch_candidate_ids,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
        background_continuity_profile=background_continuity_profile,
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
    )
    world_contact_release_posture = str(
        idle_strategy.get("world_contact_release_posture")
        or (world_contact_summary or {}).get("release_posture", "shadow_only_guarded")
    )
    repair_followup_required = bool(
        idle_strategy.get("repair_followup_required")
        or (pain_regret_repair_report or {}).get("repair_followup_required")
        or (responsibility_loop_state or {}).get("repair_followup_required")
    )
    waiting_mode = str(
        idle_strategy.get("waiting_mode", "restored_waiting_for_external_turn")
    )
    heartbeat_packet = {
        "schema_version": "digital_life_waiting_heartbeat_v0",
        "run_id": run_id,
        "generated_at": now_iso(),
        "status": "closed",
        "heartbeat_counter": heartbeat_counter,
        "waiting_mode": waiting_mode,
        "idle_strategy_ref": IDLE_STRATEGY_STATE_REF,
        "resident_governance_state_ref": RESIDENT_GOVERNANCE_STATE_REF,
        "safe_terminal_loop_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "next_required_action": "await_next_external_relation_turn",
    }
    if responsibility_loop_state_ref:
        heartbeat_packet["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        heartbeat_packet["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        heartbeat_packet["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        heartbeat_packet["membrane_guard_refs"] = membrane_guard_refs
    if world_contact_release_posture:
        heartbeat_packet["world_contact_release_posture"] = world_contact_release_posture
    if repair_followup_required:
        heartbeat_packet["repair_followup_required"] = True
    heartbeat_packet.update(extract_idle_governance_fields(idle_strategy))

    safe_terminal_loop["current_mode"] = waiting_mode
    safe_terminal_loop["last_heartbeat_mode"] = waiting_mode
    safe_terminal_loop["heartbeat_counter"] = heartbeat_counter
    safe_terminal_loop["last_heartbeat_packet_ref"] = heartbeat_report_ref
    safe_terminal_loop["idle_strategy_ref"] = IDLE_STRATEGY_STATE_REF
    safe_terminal_loop["resident_governance_state_ref"] = RESIDENT_GOVERNANCE_STATE_REF
    safe_terminal_loop["idle_heartbeat_trace_ref"] = IDLE_HEARTBEAT_TRACE_REF
    safe_terminal_loop["idle_heartbeat_trace_count"] = heartbeat_counter
    write_json(terminal_dir / "safe_terminal_loop_state.json", safe_terminal_loop)

    terminal_life_loop_state["current_mode"] = waiting_mode
    terminal_life_loop_state["heartbeat_counter"] = heartbeat_counter
    terminal_life_loop_state["last_heartbeat_packet_ref"] = heartbeat_report_ref
    terminal_life_loop_state["next_required_action"] = "await_next_external_relation_turn"
    terminal_life_loop_state["idle_strategy_ref"] = IDLE_STRATEGY_STATE_REF
    terminal_life_loop_state["resident_governance_state_ref"] = RESIDENT_GOVERNANCE_STATE_REF
    terminal_life_loop_state["idle_heartbeat_trace_ref"] = IDLE_HEARTBEAT_TRACE_REF
    terminal_life_loop_state["idle_heartbeat_trace_count"] = heartbeat_counter
    for field in (
        "relationship_timeline_ref",
        "commitment_expression_plan_ref",
        "apology_repair_language_trace_ref",
        "background_resident_governance_state_ref",
        "background_convergence_summary_ref",
        "background_convergence_history_ref",
        "background_convergence_history_trend_state",
        "background_convergence_history_window_size",
        "background_dominant_convergence_pressure_level",
        "background_dominant_convergence_state",
        "background_trait_convergence_history_profile",
        "background_trait_convergence_unstable_names",
        "background_trait_convergence_stable_names",
        "background_trait_convergence_history_focus",
        "cross_wake_trait_convergence_profile",
        "cross_wake_trait_convergence_focus",
        "cross_wake_trait_convergence_pressure",
        "cross_wake_trait_convergence_unstable_names",
        "cross_wake_trait_convergence_stable_names",
        "cross_wake_trait_convergence_score",
        "cross_wake_trait_convergence_refs",
        "background_convergence_state",
        "background_convergence_pressure_level",
        "background_convergence_attention_target",
        "background_relationship_stage_continuity",
        "background_trait_convergence_score",
        "background_max_trait_delta_from_background",
        "background_average_trait_delta_from_background",
        "background_trait_convergence_summary",
        "background_resident_governance_explanation_ref",
        "background_governance_driver_family",
        "background_next_wake_expectation",
        "background_governance_explanation_story",
        "background_trait_drift_monitor_ref",
        "background_trait_drift_update_mode_summary",
        "background_trait_drift_recalibration_names",
        "background_trait_drift_stabilized_names",
        "background_lineage_governance_profile",
        "background_lineage_depth_band",
        "background_lineage_waiting_posture",
        "background_lineage_cadence_weight",
        "background_lineage_evidence_ref_count",
        "background_resident_lineage_state",
        "resident_background_lineage_state",
        "dream_experience_window_ref",
        "wake_integration_frame_ref",
        "dream_fact_gate_decision_ref",
        "dream_wake_presence_profile",
        "dream_window_id",
        "dream_window_kind",
        "dream_affective_themes",
        "dream_reportability",
        "dream_fact_gate_result",
        "dream_fact_gate_ref_count",
        "wake_integration_id",
        "wake_integration_archive_requirement",
        "wake_integration_growth_seed_count",
        "wake_integration_repair_target_count",
        "dream_wake_ref_set",
        "background_idle_heartbeat_trace_ref",
        "background_idle_heartbeat_trace_count",
        "long_horizon_language_refs",
        "live_language_turn_refs",
        "last_live_semantic_focus",
        "background_live_language_turn_refs",
        "background_last_live_semantic_focus",
        "background_live_language_presence_profile",
        "live_language_presence_profile",
        "offline_learning_cumulative_profile",
        "offline_learning_cumulative_generation",
        "offline_learning_cumulative_pressure_level",
        "offline_learning_cumulative_attention_target",
        "offline_learning_cumulative_priority_profile",
        "offline_learning_cumulative_ref_set",
        "signal_media_ref",
        "belief_state_ref",
        "prediction_error_ref",
        "active_sampling_plan_ref",
        "memory_write_gate_ref",
        "state_merge_guard_ref",
        "prediction_write_gate_refs",
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
        "background_state_merge_guard_ref",
        "background_state_merge_policy",
        "background_state_merge_long_term_change_count",
        "background_state_merge_long_term_change_families",
        "background_state_merge_long_term_change_refs",
        "schema_cross_file_logic_ref",
        "schema_run_manifest_ref",
        "life_constraint_refs",
        "queue_e_cross_layer_gate_status",
        "life_constraint_waiting_posture",
        "life_constraint_attention_target",
        "life_constraint_attention_reason",
        "workspace_frame_ref",
        "broadcast_frame_ref",
        "metacognition_ref",
        "consciousness_probe_ref",
        "birth_readiness_rollup_ref",
        "birth_readiness_stage_gate_ref",
        "consciousness_waiting_posture",
        "consciousness_attention_target",
        "consciousness_attention_reason",
        "consciousness_reportability_flags",
        "birth_readiness_waiting_posture",
        "birth_readiness_attention_target",
        "birth_readiness_attention_reason",
        "birth_readiness_decision",
        "birth_readiness_next_required_command",
        "birth_readiness_blocked_reasons",
    ):
        if field in idle_strategy:
            terminal_life_loop_state[field] = idle_strategy[field]
    if responsibility_loop_state_ref:
        terminal_life_loop_state["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        terminal_life_loop_state["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        terminal_life_loop_state["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        terminal_life_loop_state["membrane_guard_refs"] = membrane_guard_refs
    write_json(terminal_dir / "terminal_life_loop_state.json", terminal_life_loop_state)

    record_idle_continuity(
        self_narrative_trace=self_narrative_trace,
        commitment_index=commitment_index,
        relationship_graph=relationship_graph,
        heartbeat_counter=heartbeat_counter,
        heartbeat_report_ref=heartbeat_report_ref,
    )
    write_json(language_dir / "self_narrative_language_trace.json", self_narrative_trace)
    write_json(language_dir / "commitment_repair_language_index.json", commitment_index)
    write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)

    idle_continuity_frame = build_idle_continuity_frame(
        run_id=run_id,
        generated_at=generated_at,
        heartbeat_counter=heartbeat_counter,
        heartbeat_report_ref=heartbeat_report_ref,
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
        relationship_timeline_ref=idle_strategy.get("relationship_timeline_ref"),
        commitment_expression_plan_ref=idle_strategy.get("commitment_expression_plan_ref"),
        apology_repair_language_trace_ref=idle_strategy.get("apology_repair_language_trace_ref"),
        live_language_turn_refs=idle_strategy.get("live_language_turn_refs"),
        last_live_semantic_focus=idle_strategy.get("last_live_semantic_focus"),
        background_live_language_turn_refs=idle_strategy.get(
            "background_live_language_turn_refs"
        ),
        background_last_live_semantic_focus=idle_strategy.get(
            "background_last_live_semantic_focus"
        ),
        live_language_presence_profile=idle_strategy.get(
            "live_language_presence_profile"
        ),
        background_live_language_presence_profile=idle_strategy.get(
            "background_live_language_presence_profile"
        ),
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        dream_experience_window_ref=idle_strategy.get("dream_experience_window_ref"),
        wake_integration_frame_ref=idle_strategy.get("wake_integration_frame_ref"),
        dream_fact_gate_decision_ref=idle_strategy.get(
            "dream_fact_gate_decision_ref"
        ),
        dream_wake_presence_profile=idle_strategy.get("dream_wake_presence_profile"),
        growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
        nightmare_risk_ref=nightmare_risk_ref,
        belief_learning_plan_ref=belief_learning_plan_ref,
        language_learning_plan_ref=language_learning_plan_ref,
        relationship_learning_plan_ref=relationship_learning_plan_ref,
        growth_patch_candidate_ids=growth_patch_candidate_ids,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
        world_contact_release_posture=world_contact_release_posture,
        repair_followup_required=repair_followup_required,
        offline_learning_pressure_level=idle_strategy.get("offline_learning_pressure_level"),
        offline_learning_attention_target=idle_strategy.get("offline_learning_attention_target"),
        background_continuity_mode=idle_strategy.get("background_continuity_mode"),
        background_carryover_pressure_level=idle_strategy.get("background_carryover_pressure_level"),
        background_carryover_attention_target=idle_strategy.get("background_carryover_attention_target"),
        background_carryover_generation=idle_strategy.get("background_carryover_generation"),
        background_carryover_parent_run_id=idle_strategy.get("background_carryover_parent_run_id"),
        background_carryover_source_ref_set=idle_strategy.get("background_carryover_source_ref_set"),
        background_continuity_ref_set=idle_strategy.get("background_continuity_ref_set"),
        background_resident_governance_state_ref=idle_strategy.get(
            "background_resident_governance_state_ref"
        ),
        background_convergence_summary_ref=idle_strategy.get(
            "background_convergence_summary_ref"
        ),
        background_convergence_history_ref=idle_strategy.get(
            "background_convergence_history_ref"
        ),
        background_convergence_history_trend_state=idle_strategy.get(
            "background_convergence_history_trend_state"
        ),
        background_convergence_history_window_size=idle_strategy.get(
            "background_convergence_history_window_size"
        ),
        background_trait_convergence_history_profile=idle_strategy.get(
            "background_trait_convergence_history_profile"
        ),
        background_trait_convergence_unstable_names=idle_strategy.get(
            "background_trait_convergence_unstable_names"
        ),
        background_trait_convergence_stable_names=idle_strategy.get(
            "background_trait_convergence_stable_names"
        ),
        background_trait_convergence_history_focus=idle_strategy.get(
            "background_trait_convergence_history_focus"
        ),
        background_convergence_state=idle_strategy.get("background_convergence_state"),
        background_convergence_pressure_level=idle_strategy.get(
            "background_convergence_pressure_level"
        ),
        background_convergence_attention_target=idle_strategy.get(
            "background_convergence_attention_target"
        ),
        background_resident_governance_explanation_ref=idle_strategy.get(
            "background_resident_governance_explanation_ref"
        ),
        background_governance_driver_family=idle_strategy.get(
            "background_governance_driver_family"
        ),
        background_next_wake_expectation=idle_strategy.get(
            "background_next_wake_expectation"
        ),
        background_governance_explanation_story=idle_strategy.get(
            "background_governance_explanation_story"
        ),
        background_trait_drift_monitor_ref=idle_strategy.get(
            "background_trait_drift_monitor_ref"
        ),
        background_trait_drift_update_mode_summary=idle_strategy.get(
            "background_trait_drift_update_mode_summary"
        ),
        background_trait_drift_recalibration_names=idle_strategy.get(
            "background_trait_drift_recalibration_names"
        ),
        background_trait_drift_stabilized_names=idle_strategy.get(
            "background_trait_drift_stabilized_names"
        ),
        background_lineage_governance_profile=idle_strategy.get(
            "background_lineage_governance_profile"
        ),
        background_lineage_depth_band=idle_strategy.get(
            "background_lineage_depth_band"
        ),
        background_lineage_waiting_posture=idle_strategy.get(
            "background_lineage_waiting_posture"
        ),
        background_lineage_cadence_weight=idle_strategy.get(
            "background_lineage_cadence_weight"
        ),
        background_lineage_evidence_ref_count=idle_strategy.get(
            "background_lineage_evidence_ref_count"
        ),
        background_idle_heartbeat_trace_ref=idle_strategy.get(
            "background_idle_heartbeat_trace_ref"
        ),
        background_idle_heartbeat_trace_count=idle_strategy.get(
            "background_idle_heartbeat_trace_count"
        ),
        signal_media_ref=idle_strategy.get("signal_media_ref"),
        belief_state_ref=idle_strategy.get("belief_state_ref"),
        prediction_error_ref=idle_strategy.get("prediction_error_ref"),
        active_sampling_plan_ref=idle_strategy.get("active_sampling_plan_ref"),
        memory_write_gate_ref=idle_strategy.get("memory_write_gate_ref"),
        state_merge_guard_ref=idle_strategy.get("state_merge_guard_ref"),
        background_state_merge_guard_ref=idle_strategy.get(
            "background_state_merge_guard_ref"
        ),
        background_state_merge_policy=idle_strategy.get(
            "background_state_merge_policy"
        ),
        background_state_merge_long_term_change_count=idle_strategy.get(
            "background_state_merge_long_term_change_count"
        ),
        background_state_merge_long_term_change_families=idle_strategy.get(
            "background_state_merge_long_term_change_families"
        ),
        background_state_merge_long_term_change_refs=idle_strategy.get(
            "background_state_merge_long_term_change_refs"
        ),
        prediction_write_gate_refs=idle_strategy.get("prediction_write_gate_refs"),
        prediction_waiting_posture=idle_strategy.get("prediction_waiting_posture"),
        response_surface_posture_hint=idle_strategy.get("response_surface_posture_hint"),
    )
    write_json(terminal_dir / "idle_continuity_frame.json", idle_continuity_frame)
    _append_idle_heartbeat_trace(
        terminal_dir=terminal_dir,
        run_id=run_id,
        generated_at=heartbeat_packet["generated_at"],
        heartbeat_counter=heartbeat_counter,
        waiting_mode=waiting_mode,
        heartbeat_report_ref=heartbeat_report_ref,
        idle_strategy=idle_strategy,
        idle_continuity_frame=idle_continuity_frame,
        membrane_guard_refs=membrane_guard_refs,
    )
    resident_governance_state = {
        "schema_version": "resident_governance_state_v0",
        "run_id": run_id,
        "generated_at": now_iso(),
        "status": "active",
        "governance_mode": "foreground_terminal_residency",
        "governance_phase": "waiting_heartbeat_active",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "idle_strategy_ref": IDLE_STRATEGY_STATE_REF,
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "resident_governance_report_ref": RESIDENT_GOVERNANCE_REPORT_REF,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "last_heartbeat_packet_ref": heartbeat_report_ref,
        "idle_heartbeat_trace_ref": IDLE_HEARTBEAT_TRACE_REF,
        "idle_heartbeat_trace_count": heartbeat_counter,
        "relationship_timeline_ref": idle_strategy.get("relationship_timeline_ref"),
        "commitment_expression_plan_ref": idle_strategy.get("commitment_expression_plan_ref"),
        "apology_repair_language_trace_ref": idle_strategy.get("apology_repair_language_trace_ref"),
        "long_horizon_language_refs": list(idle_strategy.get("long_horizon_language_refs", [])),
        "next_required_action": "await_next_external_relation_turn",
    }
    idle_strategy["idle_continuity_ref"] = "runtime/state/terminal/idle_continuity_frame.json"
    idle_strategy["idle_heartbeat_trace_ref"] = IDLE_HEARTBEAT_TRACE_REF
    idle_strategy["idle_heartbeat_trace_count"] = heartbeat_counter
    if responsibility_loop_state_ref:
        resident_governance_state["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        resident_governance_state["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        resident_governance_state["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        resident_governance_state["membrane_guard_refs"] = membrane_guard_refs
    resident_governance_state.update(extract_idle_governance_fields(idle_strategy))
    resident_background_lineage_state = build_resident_background_lineage_state(
        resident_governance_state,
        governance_phase="waiting_heartbeat_active",
        status="active",
    )
    if resident_background_lineage_state:
        resident_governance_state["resident_background_lineage_state"] = (
            resident_background_lineage_state
        )
        terminal_life_loop_state["resident_background_lineage_state"] = (
            resident_background_lineage_state
        )
        write_json(terminal_dir / "terminal_life_loop_state.json", terminal_life_loop_state)
    write_json(terminal_dir / "resident_governance_state.json", resident_governance_state)
    write_json(terminal_dir / "idle_strategy_state.json", idle_strategy)
    write_json(reports_dir / "digital_life_waiting_heartbeat.json", heartbeat_packet)
    return heartbeat_counter


def _append_idle_heartbeat_trace(
    *,
    terminal_dir: Path,
    run_id: str,
    generated_at: str,
    heartbeat_counter: int,
    waiting_mode: str,
    heartbeat_report_ref: str,
    idle_strategy: dict[str, Any],
    idle_continuity_frame: dict[str, Any],
    membrane_guard_refs: list[str],
) -> None:
    trace_event = {
        "schema_version": "idle_heartbeat_trace_event_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "event_kind": "waiting_heartbeat_refresh",
        "heartbeat_counter": heartbeat_counter,
        "waiting_mode": waiting_mode,
        "heartbeat_ref": heartbeat_report_ref,
        "idle_strategy_ref": IDLE_STRATEGY_STATE_REF,
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "resident_governance_state_ref": RESIDENT_GOVERNANCE_STATE_REF,
        "heartbeat_interval_ms": idle_strategy.get("heartbeat_interval_ms"),
        "idle_probe_mode": idle_strategy.get("idle_probe_mode"),
        "next_idle_action": idle_strategy.get("next_idle_action"),
        "governance_attention_target": idle_strategy.get("governance_attention_target"),
        "governance_cadence_profile": idle_strategy.get("governance_cadence_profile"),
        "offline_pressure_level": idle_strategy.get("offline_pressure_level"),
        "body_waiting_posture": idle_strategy.get("body_waiting_posture"),
        "queue_e_priority_band": idle_strategy.get("queue_e_priority_band"),
        "background_convergence_history_trend_state": idle_strategy.get(
            "background_convergence_history_trend_state"
        ),
        "background_trait_convergence_history_focus": idle_strategy.get(
            "background_trait_convergence_history_focus"
        ),
        "background_trait_drift_update_mode_summary": idle_strategy.get(
            "background_trait_drift_update_mode_summary"
        ),
        "background_trait_drift_recalibration_names": list(
            idle_strategy.get("background_trait_drift_recalibration_names", [])
        ),
        "background_trait_drift_stabilized_names": list(
            idle_strategy.get("background_trait_drift_stabilized_names", [])
        ),
        "cross_wake_trait_convergence_focus": idle_strategy.get(
            "cross_wake_trait_convergence_focus"
        ),
        "cross_wake_trait_convergence_pressure": idle_strategy.get(
            "cross_wake_trait_convergence_pressure"
        ),
        "cross_wake_trait_convergence_refs": list(
            idle_strategy.get("cross_wake_trait_convergence_refs", [])
        ),
        "background_state_merge_guard_ref": idle_strategy.get(
            "background_state_merge_guard_ref"
        ),
        "background_state_merge_policy": idle_strategy.get(
            "background_state_merge_policy"
        ),
        "background_state_merge_long_term_change_count": idle_strategy.get(
            "background_state_merge_long_term_change_count"
        ),
        "background_state_merge_long_term_change_families": list(
            idle_strategy.get("background_state_merge_long_term_change_families", [])
        ),
        "background_state_merge_long_term_change_refs": list(
            idle_strategy.get("background_state_merge_long_term_change_refs", [])
        ),
        "long_horizon_language_refs": list(
            idle_strategy.get("long_horizon_language_refs", [])
        ),
        "live_language_turn_refs": list(
            idle_strategy.get("live_language_turn_refs", [])
        ),
        "last_live_semantic_focus": idle_strategy.get("last_live_semantic_focus"),
        "background_live_language_turn_refs": list(
            idle_strategy.get("background_live_language_turn_refs", [])
        ),
        "background_last_live_semantic_focus": idle_strategy.get(
            "background_last_live_semantic_focus"
        ),
        "live_language_presence_profile": idle_strategy.get(
            "live_language_presence_profile"
        ),
        "replay_seed_refs": list(idle_continuity_frame.get("replay_seed_refs", [])),
        "dream_wake_ref_set": list(idle_strategy.get("dream_wake_ref_set", [])),
        "membrane_guard_refs": list(membrane_guard_refs),
    }
    trace_path = terminal_dir / "idle_heartbeat_trace.jsonl"
    with trace_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(trace_event, ensure_ascii=False) + "\n")
