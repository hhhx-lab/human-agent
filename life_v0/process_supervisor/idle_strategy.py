from __future__ import annotations

from typing import Any

from life_v0.membrane.queue_e_signals import derive_queue_e_signal_profile
from .offline_learning_signals import (
    build_offline_learning_cumulative_profile,
    derive_offline_learning_profile,
)
from .resident_autonomous_activity import (
    ACTIVITY_STATE_REFS,
    RESIDENT_AUTONOMOUS_ACTIVITY_REF,
    RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF,
)
from .state_merge_signals import state_merge_long_term_change_profile
from .trait_convergence_signals import cross_wake_trait_convergence_profile


IDLE_STRATEGY_STATE_REF = "runtime/state/terminal/idle_strategy_state.json"
IDLE_CONTINUITY_FRAME_REF = "runtime/state/terminal/idle_continuity_frame.json"
RELATIONSHIP_TIMELINE_REF = "runtime/state/relationship/relationship_timeline.json"
COMMITMENT_EXPRESSION_PLAN_REF = "runtime/state/language/commitment_expression_plan.json"
APOLOGY_REPAIR_LANGUAGE_TRACE_REF = "runtime/state/language/apology_repair_language_trace.json"
SIGNAL_MEDIA_RUNTIME_REF = "runtime/state/signal/signal_media_runtime.json"
BELIEF_STATE_FRAME_REF = "runtime/state/prediction/belief_state_frame.json"
PREDICTION_ERROR_FIELD_REF = "runtime/state/prediction/prediction_error_field.json"
ACTIVE_SAMPLING_PLAN_REF = "runtime/state/prediction/active_sampling_plan.json"
MEMORY_WRITE_GATE_REF = "runtime/state/memory/memory_write_gate.json"
STATE_MERGE_GUARD_REF = "runtime/state/memory/state_merge_guard.json"
SCHEMA_CROSS_FILE_LOGIC_REF = "runtime/state/schema_runner/cross_file_logic.json"
SCHEMA_RUN_MANIFEST_REF = "runtime/state/schema_runner/run_manifest.json"
QUEUE_E_BIRTH_REPAIR_PROFILE_REF = "runtime/state/life_targets/queue_e_birth_repair_profile.json"
WORKSPACE_FRAME_REF = "runtime/state/consciousness/workspace_frame.json"
BROADCAST_FRAME_REF = "runtime/state/consciousness/broadcast_frame.json"
METACOGNITION_STATE_REF = "runtime/state/consciousness/metacognition_state.json"
CONSCIOUSNESS_PROBE_REF = "runtime/state/consciousness/consciousness_probe_bundle.json"
BIRTH_READINESS_ROLLUP_REF = "runtime/state/life_targets/birth_readiness_rollup.json"
BIRTH_READINESS_STAGE_GATE_REF = "runtime/state/life_targets/birth_readiness_stage_gate.json"
DREAM_EXPERIENCE_WINDOW_REF = "runtime/state/dream/dream_experience_window.json"
WAKE_INTEGRATION_FRAME_REF = "runtime/state/dream/wake_integration_frame.json"
DREAM_FACT_GATE_DECISION_REF = "runtime/state/dream/dream_fact_gate_decision.json"
BODY_RHYTHM_PULSE_REF = "runtime/state/body/body_rhythm_pulse.json"
NEED_STATE_VECTOR_REF = "runtime/state/body/need_state_vector.json"
BODY_RESOURCE_BUDGET_REF = "runtime/state/body/body_resource_budget.json"
CORE_AFFECT_VECTOR_REF = "runtime/state/body/core_affect_vector.json"
IDLE_GOVERNANCE_FIELD_NAMES = (
    "heartbeat_interval_ms",
    "heartbeat_cadence_explanation",
    "heartbeat_cadence_driver",
    "heartbeat_cadence_reason",
    "heartbeat_cadence_modulators",
    "heartbeat_cadence_evidence_refs",
    "background_heartbeat_cadence_explanation",
    "background_heartbeat_cadence_driver",
    "background_heartbeat_cadence_reason",
    "background_heartbeat_cadence_modulators",
    "background_heartbeat_cadence_evidence_refs",
    "idle_heartbeat_trace_ref",
    "idle_heartbeat_trace_count",
    "idle_probe_mode",
    "offline_pressure_level",
    "relaunch_caution_level",
    "next_idle_action",
    "waiting_mode",
    "body_waiting_posture",
    "body_governance_flags",
    "body_rhythm_ref",
    "need_state_ref",
    "body_resource_budget_ref",
    "core_affect_vector_ref",
    "body_ref_set",
    "body_presence_profile",
    "body_energy_level",
    "body_fatigue_load",
    "body_sleep_pressure",
    "body_repair_drive",
    "body_arousal",
    "body_pain_pressure",
    "body_responsibility_weight",
    "background_body_presence",
    "background_body_presence_profile",
    "background_body_waiting_posture",
    "background_body_governance_flags",
    "background_body_rhythm_ref",
    "background_need_state_ref",
    "background_body_resource_budget_ref",
    "background_core_affect_vector_ref",
    "background_body_ref_set",
    "background_body_energy_level",
    "background_body_fatigue_load",
    "background_body_sleep_pressure",
    "background_body_repair_drive",
    "background_body_arousal",
    "background_body_pain_pressure",
    "background_body_responsibility_weight",
    "governance_attention_target",
    "governance_attention_reason",
    "governance_cadence_profile",
    "long_horizon_priority_profile",
    "relationship_timeline_ref",
    "commitment_expression_plan_ref",
    "apology_repair_language_trace_ref",
    "long_horizon_language_refs",
    "live_language_turn_refs",
    "last_live_semantic_focus",
    "background_live_language_turn_refs",
    "background_last_live_semantic_focus",
    "background_live_language_presence_profile",
    "live_language_presence_profile",
    "world_contact_release_posture",
    "repair_followup_required",
    "repair_obligation_count",
    "regret_pressure_count",
    "queue_e_priority_band",
    "nightmare_risk_ref",
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
    "background_dream_wake_presence",
    "background_dream_wake_presence_profile",
    "background_dream_experience_window_ref",
    "background_wake_integration_frame_ref",
    "background_dream_fact_gate_decision_ref",
    "background_dream_window_kind",
    "background_dream_fact_gate_result",
    "background_wake_integration_archive_requirement",
    "background_wake_integration_growth_seed_count",
    "background_wake_integration_repair_target_count",
    "background_dream_fact_gate_ref_count",
    "background_dream_wake_ref_set",
    "belief_learning_plan_ref",
    "language_learning_plan_ref",
    "relationship_learning_plan_ref",
    "offline_learning_pressure_level",
    "offline_learning_attention_target",
    "offline_learning_priority_profile",
    "offline_learning_ref_set",
    "offline_learning_cumulative_profile",
    "offline_learning_cumulative_generation",
    "offline_learning_cumulative_pressure_level",
    "offline_learning_cumulative_attention_target",
    "offline_learning_cumulative_priority_profile",
    "offline_learning_cumulative_ref_set",
    "offline_learning_cumulative_integration_mode",
    "offline_learning_cumulative_relationship_reconsolidation_required",
    "background_offline_learning_presence",
    "background_offline_learning_integration_mode",
    "background_offline_learning_relationship_reconsolidation_required",
    "background_continuity_mode",
    "background_carryover_pressure_level",
    "background_carryover_attention_target",
    "background_carryover_priority_profile",
    "background_carryover_generation",
    "background_carryover_parent_run_id",
    "background_carryover_source_ref_set",
    "background_continuity_ref_set",
    "background_lineage_depth_band",
    "background_lineage_waiting_posture",
    "background_lineage_cadence_weight",
    "background_lineage_evidence_ref_count",
    "background_lineage_governance_profile",
    "background_resident_lineage_state",
    "resident_background_lineage_state",
    "resident_autonomous_activity_ref",
    "resident_autonomous_activity_state_ref",
    "resident_autonomous_activity_presence_profile",
    "resident_autonomous_activity_ref_set",
    "autonomous_activity_count",
    "autonomous_activity_kind_counts",
    "last_autonomous_activity_kind",
    "last_autonomous_activity_at",
    "last_autonomous_activity_state_ref",
    "resident_autonomous_activity_state_refs",
    "autonomous_activity_cycle_phase_index",
    "autonomous_activity_cycle_phase_count",
    "autonomous_activity_cycle_completion_count",
    "autonomous_activity_cycle_coverage_complete",
    "autonomous_activity_covered_kinds",
    "autonomous_activity_missing_kinds",
    "next_autonomous_activity_kind",
    "background_autonomous_activity_presence",
    "background_resident_autonomous_activity_presence_profile",
    "background_resident_autonomous_activity_ref",
    "background_resident_autonomous_activity_state_ref",
    "background_resident_autonomous_activity_ref_set",
    "background_autonomous_activity_count",
    "background_autonomous_activity_kind_counts",
    "background_last_autonomous_activity_kind",
    "background_last_autonomous_activity_at",
    "background_last_autonomous_activity_state_ref",
    "background_resident_autonomous_activity_state_refs",
    "background_autonomous_activity_cycle_phase_index",
    "background_autonomous_activity_cycle_phase_count",
    "background_autonomous_activity_cycle_completion_count",
    "background_autonomous_activity_cycle_coverage_complete",
    "background_autonomous_activity_covered_kinds",
    "background_autonomous_activity_missing_kinds",
    "background_next_autonomous_activity_kind",
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
    "cross_wake_trait_drift_update_mode_summary",
    "cross_wake_trait_drift_recalibration_names",
    "cross_wake_trait_drift_stabilized_names",
    "background_convergence_state",
    "background_convergence_pressure_level",
    "background_convergence_attention_target",
    "background_relationship_stage_continuity",
    "background_trait_convergence_score",
    "background_max_trait_delta_from_background",
    "background_average_trait_delta_from_background",
    "background_trait_convergence_summary",
    "background_resident_governance_snapshot_ref",
    "background_resident_governance_report_ref",
    "background_resident_governance_explanation_ref",
    "background_governance_driver_family",
    "background_next_wake_expectation",
    "background_governance_explanation_story",
    "background_persistent_process_report_ref",
    "background_resident_process_lease_history_profile_ref",
    "background_resident_process_lease_history_profile",
    "resident_process_lease_history_profile_ref",
    "resident_process_identity_continuity_state",
    "resident_process_identity_pressure_level",
    "resident_process_lease_history_event_count",
    "resident_process_recent_ids",
    "resident_process_recent_run_ids",
    "background_waiting_mode",
    "background_relationship_subject_ref",
    "background_relationship_stage",
    "background_relationship_stage_reason",
    "background_self_model_ref",
    "background_trait_drift_monitor_ref",
    "background_trait_drift_update_mode_summary",
    "background_trait_drift_recalibration_names",
    "background_trait_drift_stabilized_names",
    "background_idle_heartbeat_trace_ref",
    "background_idle_heartbeat_trace_count",
    "background_trait_slow_variable_summary",
    "background_resume_summary",
    "signal_media_ref",
    "belief_state_ref",
    "prediction_error_ref",
    "active_sampling_plan_ref",
    "memory_write_gate_ref",
    "state_merge_guard_ref",
    "prediction_write_gate_refs",
    "background_prediction_write_gate_presence",
    "background_prediction_write_gate_refs",
    "background_prediction_waiting_posture",
    "background_response_surface_posture_hint",
    "background_prediction_attention_target",
    "background_prediction_attention_reason",
    "background_active_sampling_route",
    "background_memory_write_gate_policy",
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
    "background_schema_cross_file_logic_ref",
    "background_schema_run_manifest_ref",
    "background_life_constraint_refs",
    "background_queue_e_cross_layer_gate_status",
    "background_life_constraint_waiting_posture",
    "background_life_constraint_attention_target",
    "background_life_constraint_attention_reason",
    "background_queue_e_birth_repair_waiting_profile",
    "background_queue_e_birth_repair_gate_status",
    "background_queue_e_birth_repair_profile_ref",
    "background_queue_e_birth_repair_pressure_level",
    "background_queue_e_birth_repair_attention_target",
    "background_queue_e_birth_repair_ref_set",
    "background_queue_e_birth_repair_waiting_posture",
    "background_queue_e_birth_repair_attention_reason",
    "schema_cross_file_logic_ref",
    "schema_run_manifest_ref",
    "life_constraint_refs",
    "queue_e_cross_layer_gate_status",
    "queue_e_birth_repair_waiting_profile",
    "queue_e_birth_repair_gate_status",
    "queue_e_birth_repair_profile_ref",
    "queue_e_birth_repair_pressure_level",
    "queue_e_birth_repair_attention_target",
    "queue_e_birth_repair_ref_set",
    "queue_e_birth_repair_waiting_posture",
    "queue_e_birth_repair_attention_reason",
    "life_constraint_waiting_posture",
    "life_constraint_attention_target",
    "life_constraint_attention_reason",
    "workspace_frame_ref",
    "broadcast_frame_ref",
    "metacognition_ref",
    "consciousness_probe_ref",
    "birth_readiness_rollup_ref",
    "birth_readiness_stage_gate_ref",
    "background_identity_consciousness_birth_presence",
    "background_workspace_frame_ref",
    "background_broadcast_frame_ref",
    "background_metacognition_ref",
    "background_consciousness_probe_ref",
    "background_birth_readiness_rollup_ref",
    "background_birth_readiness_stage_gate_ref",
    "background_consciousness_waiting_posture",
    "background_consciousness_attention_target",
    "background_consciousness_attention_reason",
    "background_consciousness_reportability_flags",
    "background_birth_readiness_waiting_posture",
    "background_birth_readiness_attention_target",
    "background_birth_readiness_attention_reason",
    "background_birth_readiness_decision",
    "background_birth_readiness_next_required_command",
    "background_birth_readiness_blocked_reasons",
    "identity_consciousness_birth_refs",
    "background_identity_consciousness_birth_refs",
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
)


def extract_idle_governance_fields(idle_strategy_state: dict[str, Any] | None) -> dict[str, Any]:
    if not idle_strategy_state:
        return {}
    return {
        field: idle_strategy_state[field]
        for field in IDLE_GOVERNANCE_FIELD_NAMES
        if field in idle_strategy_state and idle_strategy_state[field] is not None
    }


def decide_idle_strategy(
    *,
    run_id: str,
    generated_at: str,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    idle_continuity_frame: dict[str, Any] | None,
    relationship_timeline: dict[str, Any] | None = None,
    commitment_expression_plan: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
    body_rhythm_pulse: dict[str, Any] | None = None,
    need_state_vector: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None,
    offline_consolidation_frame: dict[str, Any] | None,
    dream_experience_window: dict[str, Any] | None = None,
    wake_integration_frame: dict[str, Any] | None = None,
    dream_fact_gate_decision: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
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
    resident_autonomous_activity_state: dict[str, Any] | None = None,
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
    signal_media_runtime_ref: str | None = SIGNAL_MEDIA_RUNTIME_REF,
    belief_state_ref: str | None = BELIEF_STATE_FRAME_REF,
    prediction_error_field_ref: str | None = PREDICTION_ERROR_FIELD_REF,
    active_sampling_plan_ref: str | None = ACTIVE_SAMPLING_PLAN_REF,
    memory_write_gate_ref: str | None = MEMORY_WRITE_GATE_REF,
    state_merge_guard_ref: str | None = STATE_MERGE_GUARD_REF,
    schema_cross_file_logic_ref: str | None = SCHEMA_CROSS_FILE_LOGIC_REF,
    schema_run_manifest_ref: str | None = SCHEMA_RUN_MANIFEST_REF,
    workspace_frame_ref: str | None = WORKSPACE_FRAME_REF,
    broadcast_frame_ref: str | None = BROADCAST_FRAME_REF,
    metacognition_state_ref: str | None = METACOGNITION_STATE_REF,
    consciousness_probe_ref: str | None = CONSCIOUSNESS_PROBE_REF,
    birth_readiness_rollup_ref: str | None = BIRTH_READINESS_ROLLUP_REF,
    birth_readiness_stage_gate_ref: str | None = BIRTH_READINESS_STAGE_GATE_REF,
    growth_patch_candidate_ids: list[str] | None = None,
    replay_residue_ref_count: int = 0,
    dream_window_ref_count: int = 0,
    growth_patch_candidate_count: int = 0,
    background_continuity_profile: dict[str, Any] | None = None,
    source_doc_refs: list[str] | None = None,
    readme_block_refs: list[str] | None = None,
    runtime_carrier_refs: list[str] | None = None,
) -> dict[str, Any]:
    heartbeat_counter = _next_heartbeat_counter(
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
        idle_continuity_frame=idle_continuity_frame,
    )
    offline_pressure_level = _offline_pressure_level(
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        replay_residue_ref_count=replay_residue_ref_count,
        dream_window_ref_count=dream_window_ref_count,
        growth_patch_candidate_count=growth_patch_candidate_count,
    )
    body_waiting_posture = _body_waiting_posture(
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        background_continuity_profile=background_continuity_profile,
    )
    (
        world_contact_release_posture,
        repair_followup_required,
        repair_obligation_count,
        regret_pressure_count,
        queue_e_priority_band,
    ) = _queue_e_idle_regulation(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    prediction_profile = _prediction_waiting_profile(
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        memory_write_gate=memory_write_gate,
        state_merge_guard=state_merge_guard,
    )
    background_continuity_profile = dict(background_continuity_profile or {})
    life_constraint_profile = _life_constraint_waiting_profile(
        schema_cross_file_logic=schema_cross_file_logic,
        schema_run_manifest=schema_run_manifest,
        background_continuity_profile=background_continuity_profile,
    )
    queue_e_birth_repair_waiting_profile = _queue_e_birth_repair_waiting_profile(
        schema_cross_file_logic=schema_cross_file_logic,
        schema_run_manifest=schema_run_manifest,
        background_continuity_profile=background_continuity_profile,
    )
    consciousness_profile = _consciousness_waiting_profile(
        workspace_frame=workspace_frame,
        broadcast_frame=broadcast_frame,
        metacognition_state=metacognition_state,
        consciousness_probe=consciousness_probe,
        background_continuity_profile=background_continuity_profile,
    )
    birth_readiness_profile = _birth_readiness_waiting_profile(
        birth_readiness_rollup=birth_readiness_rollup,
        birth_readiness_stage_gate=birth_readiness_stage_gate,
        background_continuity_profile=background_continuity_profile,
    )
    offline_learning_profile = derive_offline_learning_profile(
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    live_language_presence_profile = _live_language_presence_profile(
        terminal_life_loop_state=terminal_life_loop_state,
        background_continuity_profile=background_continuity_profile,
    )
    offline_learning_cumulative_profile = build_offline_learning_cumulative_profile(
        current_profile=offline_learning_profile,
        background_profile=background_continuity_profile,
    )
    effective_offline_learning_pressure_level = _effective_offline_learning_pressure(
        current_pressure_level=offline_learning_profile["offline_learning_pressure_level"],
        cumulative_pressure_level=offline_learning_cumulative_profile["pressure_level"],
    )
    background_carryover_generation = _int_or_zero(
        background_continuity_profile.get("background_carryover_generation")
    )
    background_pressure_level = _background_pressure_overlay(
        background_continuity_profile.get("background_carryover_pressure_level"),
        _background_pressure_overlay(
            background_continuity_profile.get("background_convergence_pressure_level"),
            _background_history_pressure_level(background_continuity_profile),
        ),
    )
    convergence_governance_pressure_level = _background_pressure_overlay(
        background_continuity_profile.get("background_convergence_pressure_level"),
        _background_history_pressure_level(background_continuity_profile),
    )
    background_attention_target = (
        _background_history_attention_target(background_continuity_profile)
        or background_continuity_profile.get("background_convergence_attention_target")
        or background_continuity_profile.get("background_carryover_attention_target")
    )
    trait_convergence_profile = cross_wake_trait_convergence_profile(
        background_continuity_profile
    )
    heartbeat_interval_ms = _heartbeat_interval_ms(
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        offline_pressure_level=offline_pressure_level,
        queue_e_priority_band=queue_e_priority_band,
        offline_learning_pressure_level=effective_offline_learning_pressure_level,
        prediction_waiting_posture=prediction_profile["prediction_waiting_posture"],
        consciousness_waiting_posture=consciousness_profile["consciousness_waiting_posture"],
        birth_readiness_waiting_posture=birth_readiness_profile[
            "birth_readiness_waiting_posture"
        ],
        background_carryover_pressure_level=background_pressure_level,
        background_carryover_generation=background_carryover_generation,
        background_convergence_history_trend_state=background_continuity_profile.get(
            "background_convergence_history_trend_state"
        ),
    )
    next_idle_action = _next_idle_action(
        body_waiting_posture=body_waiting_posture,
        offline_pressure_level=offline_pressure_level,
        need_state_vector=need_state_vector,
        repair_followup_required=repair_followup_required,
        queue_e_priority_band=queue_e_priority_band,
        offline_learning_pressure_level=effective_offline_learning_pressure_level,
        prediction_waiting_posture=prediction_profile["prediction_waiting_posture"],
        consciousness_waiting_posture=consciousness_profile["consciousness_waiting_posture"],
        birth_readiness_waiting_posture=birth_readiness_profile[
            "birth_readiness_waiting_posture"
        ],
        background_carryover_pressure_level=background_pressure_level,
        background_carryover_generation=background_carryover_generation,
        background_convergence_history_trend_state=background_continuity_profile.get(
            "background_convergence_history_trend_state"
        ),
    )
    relaunch_caution_level = _relaunch_caution_level(
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
    )
    body_governance_flags = _body_governance_flags(
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        background_continuity_profile=background_continuity_profile,
    )
    body_presence_profile = _body_presence_profile(
        body_waiting_posture=body_waiting_posture,
        body_governance_flags=body_governance_flags,
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
        background_continuity_profile=background_continuity_profile,
    )
    body_ref_set = _string_list(body_presence_profile.get("body_ref_set"))
    relationship_timeline_ref = _ref_if_present(
        payload=relationship_timeline,
        ref=RELATIONSHIP_TIMELINE_REF,
    )
    commitment_expression_plan_ref = _ref_if_present(
        payload=commitment_expression_plan,
        ref=COMMITMENT_EXPRESSION_PLAN_REF,
    )
    apology_repair_language_trace_ref = _ref_if_present(
        payload=apology_repair_language_trace,
        ref=APOLOGY_REPAIR_LANGUAGE_TRACE_REF,
    )
    long_horizon_refs = _long_horizon_language_refs(
        relationship_timeline_ref=relationship_timeline_ref,
        commitment_expression_plan_ref=commitment_expression_plan_ref,
        apology_repair_language_trace_ref=apology_repair_language_trace_ref,
    )
    signal_media_ref = _ref_if_present(
        payload=signal_media_runtime,
        ref=signal_media_runtime_ref or SIGNAL_MEDIA_RUNTIME_REF,
    )
    belief_state_runtime_ref = _ref_if_present(
        payload=belief_state,
        ref=belief_state_ref or BELIEF_STATE_FRAME_REF,
    )
    prediction_error_ref = _ref_if_present(
        payload=prediction_error_field,
        ref=prediction_error_field_ref or PREDICTION_ERROR_FIELD_REF,
    )
    active_sampling_ref = _ref_if_present(
        payload=active_sampling_plan,
        ref=active_sampling_plan_ref or ACTIVE_SAMPLING_PLAN_REF,
    )
    memory_write_gate_runtime_ref = _ref_if_present(
        payload=memory_write_gate,
        ref=memory_write_gate_ref or MEMORY_WRITE_GATE_REF,
    )
    state_merge_guard_runtime_ref = _ref_if_present(
        payload=state_merge_guard,
        ref=state_merge_guard_ref or STATE_MERGE_GUARD_REF,
    )
    schema_cross_file_logic_runtime_ref = _ref_if_present(
        payload=schema_cross_file_logic,
        ref=schema_cross_file_logic_ref or SCHEMA_CROSS_FILE_LOGIC_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_schema_cross_file_logic_ref",
        "schema_cross_file_logic_ref",
    )
    schema_run_manifest_runtime_ref = _ref_if_present(
        payload=schema_run_manifest,
        ref=schema_run_manifest_ref or SCHEMA_RUN_MANIFEST_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_schema_run_manifest_ref",
        "schema_run_manifest_ref",
    )
    workspace_frame_runtime_ref = _ref_if_present(
        payload=workspace_frame,
        ref=workspace_frame_ref or WORKSPACE_FRAME_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_workspace_frame_ref",
        "workspace_frame_ref",
    )
    broadcast_frame_runtime_ref = _ref_if_present(
        payload=broadcast_frame,
        ref=broadcast_frame_ref or BROADCAST_FRAME_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_broadcast_frame_ref",
        "broadcast_frame_ref",
    )
    metacognition_runtime_ref = _ref_if_present(
        payload=metacognition_state,
        ref=metacognition_state_ref or METACOGNITION_STATE_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_metacognition_ref",
        "metacognition_ref",
    )
    consciousness_probe_runtime_ref = _ref_if_present(
        payload=consciousness_probe,
        ref=consciousness_probe_ref or CONSCIOUSNESS_PROBE_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_consciousness_probe_ref",
        "consciousness_probe_ref",
    )
    birth_readiness_rollup_runtime_ref = _ref_if_present(
        payload=birth_readiness_rollup,
        ref=birth_readiness_rollup_ref or BIRTH_READINESS_ROLLUP_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_birth_readiness_rollup_ref",
        "birth_readiness_rollup_ref",
    )
    birth_readiness_stage_gate_runtime_ref = _ref_if_present(
        payload=birth_readiness_stage_gate,
        ref=birth_readiness_stage_gate_ref or BIRTH_READINESS_STAGE_GATE_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_birth_readiness_stage_gate_ref",
        "birth_readiness_stage_gate_ref",
    )
    dream_experience_window_runtime_ref = _ref_if_present(
        payload=dream_experience_window,
        ref=dream_experience_window_ref or DREAM_EXPERIENCE_WINDOW_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_dream_experience_window_ref",
        "dream_experience_window_ref",
    )
    wake_integration_frame_runtime_ref = _ref_if_present(
        payload=wake_integration_frame,
        ref=wake_integration_frame_ref or WAKE_INTEGRATION_FRAME_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_wake_integration_frame_ref",
        "wake_integration_frame_ref",
    )
    dream_fact_gate_decision_runtime_ref = _ref_if_present(
        payload=dream_fact_gate_decision,
        ref=dream_fact_gate_decision_ref or DREAM_FACT_GATE_DECISION_REF,
    ) or _background_ref(
        background_continuity_profile,
        "background_dream_fact_gate_decision_ref",
        "dream_fact_gate_decision_ref",
    )
    dream_wake_presence_profile = _dream_wake_presence_profile(
        offline_consolidation_frame=offline_consolidation_frame,
        dream_experience_window=dream_experience_window,
        wake_integration_frame=wake_integration_frame,
        dream_fact_gate_decision=dream_fact_gate_decision,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
        dream_experience_window_ref=dream_experience_window_runtime_ref,
        wake_integration_frame_ref=wake_integration_frame_runtime_ref,
        dream_fact_gate_decision_ref=dream_fact_gate_decision_runtime_ref,
        background_continuity_profile=background_continuity_profile,
    )
    autonomous_activity_presence_profile = _autonomous_activity_presence_profile(
        resident_autonomous_activity_state,
        background_continuity_profile=background_continuity_profile,
    )
    prediction_write_gate_refs = _prediction_write_gate_refs(
        signal_media_ref=signal_media_ref,
        belief_state_ref=belief_state_runtime_ref,
        prediction_error_ref=prediction_error_ref,
        active_sampling_plan_ref=active_sampling_ref,
        memory_write_gate_ref=memory_write_gate_runtime_ref,
        state_merge_guard_ref=state_merge_guard_runtime_ref,
    )
    (
        governance_attention_target,
        governance_attention_reason,
        governance_cadence_profile,
        long_horizon_priority_profile,
    ) = _resident_governance_language_priority(
        relationship_timeline_ref=relationship_timeline_ref,
        commitment_expression_plan_ref=commitment_expression_plan_ref,
        apology_repair_language_trace_ref=apology_repair_language_trace_ref,
        offline_pressure_level=offline_pressure_level,
        need_state_vector=need_state_vector,
        body_waiting_posture=body_waiting_posture,
        world_contact_release_posture=world_contact_release_posture,
        repair_followup_required=repair_followup_required,
        repair_obligation_count=repair_obligation_count,
        regret_pressure_count=regret_pressure_count,
        queue_e_priority_band=queue_e_priority_band,
        background_carryover_attention_target=background_attention_target,
        background_convergence_state=background_continuity_profile.get(
            "background_convergence_state"
        )
        or background_continuity_profile.get(
            "background_convergence_history_trend_state"
        ),
        background_convergence_pressure_level=convergence_governance_pressure_level,
        background_convergence_history_trend_state=background_continuity_profile.get(
            "background_convergence_history_trend_state"
        ),
        background_carryover_generation=background_carryover_generation,
    )
    (
        governance_attention_target,
        governance_attention_reason,
        governance_cadence_profile,
        long_horizon_priority_profile,
    ) = _queue_f_governance_overlay(
        current_target=governance_attention_target,
        current_reason=governance_attention_reason,
        current_cadence_profile=governance_cadence_profile,
        current_priority_profile=long_horizon_priority_profile,
        queue_e_priority_band=queue_e_priority_band,
        consciousness_profile=consciousness_profile,
        birth_readiness_profile=birth_readiness_profile,
    )
    background_lineage_governance_profile = _background_lineage_governance_profile(
        background_continuity_profile=background_continuity_profile,
        background_carryover_generation=background_carryover_generation,
        background_carryover_pressure_level=background_pressure_level,
        heartbeat_interval_ms=heartbeat_interval_ms,
        next_idle_action=next_idle_action,
        governance_attention_target=governance_attention_target,
        governance_attention_reason=governance_attention_reason,
        governance_cadence_profile=governance_cadence_profile,
        long_horizon_priority_profile=long_horizon_priority_profile,
    )
    heartbeat_cadence_explanation = _heartbeat_cadence_explanation(
        heartbeat_interval_ms=heartbeat_interval_ms,
        next_idle_action=next_idle_action,
        body_waiting_posture=body_waiting_posture,
        body_rhythm_present=bool(body_rhythm_pulse),
        need_state_present=bool(need_state_vector),
        offline_pressure_level=offline_pressure_level,
        queue_e_priority_band=queue_e_priority_band,
        offline_learning_pressure_level=effective_offline_learning_pressure_level,
        prediction_waiting_posture=prediction_profile["prediction_waiting_posture"],
        consciousness_waiting_posture=consciousness_profile[
            "consciousness_waiting_posture"
        ],
        birth_readiness_waiting_posture=birth_readiness_profile[
            "birth_readiness_waiting_posture"
        ],
        background_carryover_pressure_level=background_pressure_level,
        background_carryover_generation=background_carryover_generation,
        background_convergence_history_trend_state=background_continuity_profile.get(
            "background_convergence_history_trend_state"
        ),
        governance_attention_target=governance_attention_target,
        governance_cadence_profile=governance_cadence_profile,
        body_refs=[
            *body_ref_set,
        ],
        long_horizon_refs=long_horizon_refs,
        queue_e_refs=(
            queue_e_birth_repair_waiting_profile["ref_set"]
            if queue_e_birth_repair_waiting_profile["waiting_posture"]
            != "birth_repair_unobserved_waiting"
            else []
        ),
        prediction_refs=prediction_write_gate_refs,
        life_constraint_refs=life_constraint_profile["life_constraint_refs"],
        dream_wake_refs=dream_wake_presence_profile.get("ref_set", []),
        offline_learning_refs=offline_learning_cumulative_profile["ref_set"],
        autonomous_activity_refs=autonomous_activity_presence_profile.get("ref_set", []),
        background_refs=background_lineage_governance_profile.get(
            "evidence_refs", []
        ),
    )

    payload = {
        "schema_version": "idle_strategy_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "strategy_id": f"idle-strategy-{run_id}-{heartbeat_counter:04d}",
        "heartbeat_counter": heartbeat_counter,
        "heartbeat_interval_ms": heartbeat_interval_ms,
        "heartbeat_cadence_explanation": heartbeat_cadence_explanation,
        "heartbeat_cadence_driver": heartbeat_cadence_explanation["driver"],
        "heartbeat_cadence_reason": heartbeat_cadence_explanation["reason"],
        "heartbeat_cadence_modulators": heartbeat_cadence_explanation[
            "modulators"
        ],
        "heartbeat_cadence_evidence_refs": heartbeat_cadence_explanation[
            "evidence_refs"
        ],
        "idle_probe_mode": "stdin_poll_with_background_continuity_refresh",
        "offline_pressure_level": offline_pressure_level,
        "relaunch_caution_level": relaunch_caution_level,
        "next_idle_action": next_idle_action,
        "waiting_mode": safe_terminal_loop.get(
            "current_mode",
            terminal_life_loop_state.get("current_mode", "restored_waiting_for_external_turn"),
        ),
        "body_waiting_posture": body_waiting_posture,
        "body_governance_flags": body_governance_flags,
        "body_rhythm_ref": body_presence_profile.get("body_rhythm_ref"),
        "need_state_ref": body_presence_profile.get("need_state_ref"),
        "body_resource_budget_ref": body_presence_profile.get(
            "body_resource_budget_ref"
        ),
        "core_affect_vector_ref": body_presence_profile.get("core_affect_vector_ref"),
        "body_ref_set": body_ref_set,
        "body_presence_profile": body_presence_profile,
        "body_energy_level": body_presence_profile.get("energy_level"),
        "body_fatigue_load": body_presence_profile.get("fatigue_load"),
        "body_sleep_pressure": body_presence_profile.get("sleep_pressure"),
        "body_repair_drive": body_presence_profile.get("repair_drive"),
        "body_arousal": body_presence_profile.get("arousal"),
        "body_pain_pressure": body_presence_profile.get("pain_pressure"),
        "body_responsibility_weight": body_presence_profile.get(
            "responsibility_weight"
        ),
        "governance_attention_target": governance_attention_target,
        "governance_attention_reason": governance_attention_reason,
        "governance_cadence_profile": governance_cadence_profile,
        "long_horizon_priority_profile": long_horizon_priority_profile,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "long_horizon_language_refs": long_horizon_refs,
        "live_language_turn_refs": live_language_presence_profile.get(
            "live_language_turn_refs",
            [],
        ),
        "last_live_semantic_focus": live_language_presence_profile.get(
            "last_live_semantic_focus"
        ),
        "background_live_language_turn_refs": live_language_presence_profile.get(
            "background_live_language_turn_refs",
            [],
        ),
        "background_last_live_semantic_focus": live_language_presence_profile.get(
            "background_last_live_semantic_focus"
        ),
        "background_live_language_presence_profile": live_language_presence_profile.get(
            "background_live_language_presence_profile",
            {},
        ),
        "live_language_presence_profile": live_language_presence_profile,
        "world_contact_release_posture": world_contact_release_posture,
        "repair_followup_required": repair_followup_required,
        "repair_obligation_count": repair_obligation_count,
        "regret_pressure_count": regret_pressure_count,
        "queue_e_priority_band": queue_e_priority_band,
        "nightmare_risk_ref": nightmare_risk_ref if nightmare_risk else None,
        "dream_experience_window_ref": dream_experience_window_runtime_ref,
        "wake_integration_frame_ref": wake_integration_frame_runtime_ref,
        "dream_fact_gate_decision_ref": dream_fact_gate_decision_runtime_ref,
        "dream_wake_presence_profile": dream_wake_presence_profile,
        "dream_window_id": dream_wake_presence_profile.get("dream_window_id"),
        "dream_window_kind": dream_wake_presence_profile.get("dream_window_kind"),
        "dream_affective_themes": dream_wake_presence_profile.get(
            "affective_themes", []
        ),
        "dream_reportability": dream_wake_presence_profile.get("reportability"),
        "dream_fact_gate_result": dream_wake_presence_profile.get(
            "dream_fact_gate_result"
        ),
        "dream_fact_gate_ref_count": dream_wake_presence_profile.get(
            "dream_fact_gate_ref_count"
        ),
        "wake_integration_id": dream_wake_presence_profile.get(
            "wake_integration_id"
        ),
        "wake_integration_archive_requirement": dream_wake_presence_profile.get(
            "wake_archive_requirement"
        ),
        "wake_integration_growth_seed_count": dream_wake_presence_profile.get(
            "wake_growth_seed_count"
        ),
        "wake_integration_repair_target_count": dream_wake_presence_profile.get(
            "wake_repair_target_count"
        ),
        "dream_wake_ref_set": dream_wake_presence_profile.get("ref_set", []),
        "resident_autonomous_activity_ref": (
            RESIDENT_AUTONOMOUS_ACTIVITY_REF
            if autonomous_activity_presence_profile
            else None
        ),
        "resident_autonomous_activity_state_ref": (
            RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF
            if autonomous_activity_presence_profile
            else None
        ),
        "resident_autonomous_activity_presence_profile": (
            autonomous_activity_presence_profile
        ),
        "resident_autonomous_activity_ref_set": (
            autonomous_activity_presence_profile.get("ref_set", [])
        ),
        "autonomous_activity_count": autonomous_activity_presence_profile.get(
            "activity_count"
        ),
        "autonomous_activity_kind_counts": autonomous_activity_presence_profile.get(
            "activity_kind_counts", {}
        ),
        "last_autonomous_activity_kind": autonomous_activity_presence_profile.get(
            "last_activity_kind"
        ),
        "last_autonomous_activity_at": autonomous_activity_presence_profile.get(
            "last_activity_at"
        ),
        "last_autonomous_activity_state_ref": autonomous_activity_presence_profile.get(
            "last_activity_state_ref"
        ),
        "resident_autonomous_activity_state_refs": (
            autonomous_activity_presence_profile.get("activity_state_refs", {})
        ),
        "autonomous_activity_cycle_phase_index": (
            autonomous_activity_presence_profile.get("cycle_phase_index")
        ),
        "autonomous_activity_cycle_phase_count": (
            autonomous_activity_presence_profile.get("cycle_phase_count")
        ),
        "autonomous_activity_cycle_completion_count": (
            autonomous_activity_presence_profile.get("cycle_completion_count")
        ),
        "autonomous_activity_cycle_coverage_complete": (
            autonomous_activity_presence_profile.get("cycle_coverage_complete")
        ),
        "autonomous_activity_covered_kinds": (
            autonomous_activity_presence_profile.get("covered_activity_kinds", [])
        ),
        "autonomous_activity_missing_kinds": (
            autonomous_activity_presence_profile.get("missing_activity_kinds", [])
        ),
        "next_autonomous_activity_kind": (
            autonomous_activity_presence_profile.get("next_activity_kind")
        ),
        "belief_learning_plan_ref": belief_learning_plan_ref if belief_learning_plan else None,
        "language_learning_plan_ref": language_learning_plan_ref if language_learning_plan else None,
        "relationship_learning_plan_ref": (
            relationship_learning_plan_ref if relationship_learning_plan else None
        ),
        "offline_learning_pressure_level": offline_learning_profile["offline_learning_pressure_level"],
        "offline_learning_attention_target": offline_learning_profile["offline_learning_attention_target"],
        "offline_learning_priority_profile": offline_learning_profile["offline_learning_priority_profile"],
        "offline_learning_ref_set": offline_learning_profile["offline_learning_ref_set"],
        "offline_learning_cumulative_profile": offline_learning_cumulative_profile,
        "offline_learning_cumulative_generation": offline_learning_cumulative_profile[
            "generation"
        ],
        "offline_learning_cumulative_pressure_level": (
            offline_learning_cumulative_profile["pressure_level"]
        ),
        "offline_learning_cumulative_attention_target": (
            offline_learning_cumulative_profile["attention_target"]
        ),
        "offline_learning_cumulative_priority_profile": (
            offline_learning_cumulative_profile["priority_profile"]
        ),
        "offline_learning_cumulative_ref_set": (
            offline_learning_cumulative_profile["ref_set"]
        ),
        "offline_learning_cumulative_integration_mode": (
            offline_learning_cumulative_profile["integration_mode"]
        ),
        "offline_learning_cumulative_relationship_reconsolidation_required": (
            offline_learning_cumulative_profile[
                "relationship_reconsolidation_required"
            ]
        ),
        "idle_continuity_ref": IDLE_CONTINUITY_FRAME_REF,
        "replay_cue_bundle_ref": replay_cue_bundle_ref if replay_cue_bundle else None,
        "offline_consolidation_frame_ref": (
            offline_consolidation_frame_ref if offline_consolidation_frame else None
        ),
        "growth_patch_candidate_queue_ref": (
            growth_patch_candidate_queue_ref if growth_patch_candidate_queue else None
        ),
        "growth_patch_candidate_ids": list(growth_patch_candidate_ids or []),
        "replay_residue_ref_count": replay_residue_ref_count,
        "dream_window_ref_count": dream_window_ref_count,
        "growth_patch_candidate_count": growth_patch_candidate_count,
        "signal_media_ref": signal_media_ref,
        "belief_state_ref": belief_state_runtime_ref,
        "prediction_error_ref": prediction_error_ref,
        "active_sampling_plan_ref": active_sampling_ref,
        "memory_write_gate_ref": memory_write_gate_runtime_ref,
        "state_merge_guard_ref": state_merge_guard_runtime_ref,
        "prediction_write_gate_refs": prediction_write_gate_refs,
        "prediction_waiting_posture": prediction_profile["prediction_waiting_posture"],
        "response_surface_posture_hint": prediction_profile["response_surface_posture_hint"],
        "prediction_attention_target": prediction_profile["prediction_attention_target"],
        "prediction_attention_reason": prediction_profile["prediction_attention_reason"],
        "prediction_error_count": prediction_profile["prediction_error_count"],
        "active_sampling_route": prediction_profile["active_sampling_route"],
        "memory_write_gate_policy": prediction_profile["memory_write_gate_policy"],
        "state_merge_policy": prediction_profile["state_merge_policy"],
        "state_merge_long_term_change_count": prediction_profile[
            "state_merge_long_term_change_count"
        ],
        "state_merge_long_term_change_families": prediction_profile[
            "state_merge_long_term_change_families"
        ],
        "state_merge_long_term_change_refs": prediction_profile[
            "state_merge_long_term_change_refs"
        ],
        "schema_cross_file_logic_ref": schema_cross_file_logic_runtime_ref,
        "schema_run_manifest_ref": schema_run_manifest_runtime_ref,
        "life_constraint_refs": life_constraint_profile["life_constraint_refs"],
        "queue_e_cross_layer_gate_status": life_constraint_profile[
            "queue_e_cross_layer_gate_status"
        ],
        "queue_e_birth_repair_waiting_profile": queue_e_birth_repair_waiting_profile,
        "queue_e_birth_repair_gate_status": queue_e_birth_repair_waiting_profile[
            "gate_status"
        ],
        "queue_e_birth_repair_profile_ref": queue_e_birth_repair_waiting_profile[
            "profile_ref"
        ],
        "queue_e_birth_repair_pressure_level": queue_e_birth_repair_waiting_profile[
            "pressure_level"
        ],
        "queue_e_birth_repair_attention_target": queue_e_birth_repair_waiting_profile[
            "attention_target"
        ],
        "queue_e_birth_repair_ref_set": queue_e_birth_repair_waiting_profile[
            "ref_set"
        ],
        "queue_e_birth_repair_waiting_posture": queue_e_birth_repair_waiting_profile[
            "waiting_posture"
        ],
        "queue_e_birth_repair_attention_reason": queue_e_birth_repair_waiting_profile[
            "attention_reason"
        ],
        "life_constraint_waiting_posture": life_constraint_profile[
            "life_constraint_waiting_posture"
        ],
        "life_constraint_attention_target": life_constraint_profile[
            "life_constraint_attention_target"
        ],
        "life_constraint_attention_reason": life_constraint_profile[
            "life_constraint_attention_reason"
        ],
        "workspace_frame_ref": workspace_frame_runtime_ref,
        "broadcast_frame_ref": broadcast_frame_runtime_ref,
        "metacognition_ref": metacognition_runtime_ref,
        "consciousness_probe_ref": consciousness_probe_runtime_ref,
        "birth_readiness_rollup_ref": birth_readiness_rollup_runtime_ref,
        "birth_readiness_stage_gate_ref": birth_readiness_stage_gate_runtime_ref,
        "consciousness_waiting_posture": consciousness_profile[
            "consciousness_waiting_posture"
        ],
        "consciousness_attention_target": consciousness_profile[
            "consciousness_attention_target"
        ],
        "consciousness_attention_reason": consciousness_profile[
            "consciousness_attention_reason"
        ],
        "consciousness_reportability_flags": consciousness_profile[
            "consciousness_reportability_flags"
        ],
        "birth_readiness_waiting_posture": birth_readiness_profile[
            "birth_readiness_waiting_posture"
        ],
        "birth_readiness_attention_target": birth_readiness_profile[
            "birth_readiness_attention_target"
        ],
        "birth_readiness_attention_reason": birth_readiness_profile[
            "birth_readiness_attention_reason"
        ],
        "birth_readiness_decision": birth_readiness_profile["birth_readiness_decision"],
        "birth_readiness_next_required_command": birth_readiness_profile[
            "birth_readiness_next_required_command"
        ],
        "birth_readiness_blocked_reasons": birth_readiness_profile[
            "birth_readiness_blocked_reasons"
        ],
        "source_doc_refs": list(source_doc_refs or []),
        "readme_block_refs": list(readme_block_refs or []),
        "runtime_carrier_refs": list(runtime_carrier_refs or []),
    }
    payload.update(
        {
            key: value
            for key, value in background_continuity_profile.items()
            if value is not None
        }
    )
    payload.update(trait_convergence_profile)
    if background_lineage_governance_profile:
        payload["background_lineage_governance_profile"] = (
            background_lineage_governance_profile
        )
        payload["background_lineage_depth_band"] = (
            background_lineage_governance_profile["depth_band"]
        )
        payload["background_lineage_waiting_posture"] = (
            background_lineage_governance_profile["waiting_posture"]
        )
        payload["background_lineage_cadence_weight"] = (
            background_lineage_governance_profile["cadence_weight"]
        )
        payload["background_lineage_evidence_ref_count"] = (
            background_lineage_governance_profile["evidence_ref_count"]
        )
    return payload


def _live_language_presence_profile(
    *,
    terminal_life_loop_state: dict[str, Any],
    background_continuity_profile: dict[str, Any],
) -> dict[str, Any]:
    current_refs = _dedupe_string_list(
        _string_list(terminal_life_loop_state.get("live_language_turn_refs"))
    )
    current_focus = terminal_life_loop_state.get("last_live_semantic_focus")
    has_current_presence = bool(current_refs or current_focus)
    background_refs = _dedupe_string_list(
        _string_list(background_continuity_profile.get("background_live_language_turn_refs"))
        + _string_list(background_continuity_profile.get("live_language_turn_refs"))
    )
    background_focus = (
        background_continuity_profile.get("background_last_live_semantic_focus")
        or background_continuity_profile.get("last_live_semantic_focus")
    )
    background_presence_profile = _shallow_live_language_presence_profile(
        _dict_or_empty(
            background_continuity_profile.get(
                "background_live_language_presence_profile"
            )
            or background_continuity_profile.get("live_language_presence_profile")
        )
    )

    if not current_refs and background_refs:
        current_refs = list(background_refs)
    if not current_focus and background_focus:
        current_focus = background_focus

    all_refs = _dedupe_string_list(current_refs + background_refs)
    if not all_refs and not current_focus and not background_focus and not background_presence_profile:
        return {}

    return _drop_empty(
        {
            "schema_version": "live_language_presence_profile_v0",
            "continuity_mode": (
                "current_turn_plus_background_language_presence"
                if has_current_presence and background_refs
                else "current_turn_language_presence"
                if has_current_presence
                else "background_language_presence"
            ),
            "live_language_turn_refs": current_refs,
            "last_live_semantic_focus": current_focus,
            "background_live_language_turn_refs": background_refs,
            "background_last_live_semantic_focus": background_focus,
            "background_live_language_presence_profile": background_presence_profile,
            "ref_count": len(all_refs),
            "ref_set": all_refs,
        }
    )


def _shallow_live_language_presence_profile(profile: dict[str, Any]) -> dict[str, Any]:
    if not profile:
        return {}
    source_profile = _dict_or_empty(profile.get("source_presence_profile"))
    return _drop_empty(
        {
            "schema_version": profile.get("schema_version"),
            "continuity_mode": profile.get("continuity_mode"),
            "live_language_turn_refs": _string_list(
                profile.get("live_language_turn_refs")
            ),
            "last_live_semantic_focus": profile.get("last_live_semantic_focus"),
            "background_live_language_turn_refs": _string_list(
                profile.get("background_live_language_turn_refs")
            ),
            "background_last_live_semantic_focus": profile.get(
                "background_last_live_semantic_focus"
            ),
            "ref_count": profile.get("ref_count"),
            "ref_set": _string_list(profile.get("ref_set")),
            "source_continuity_mode": profile.get("source_continuity_mode")
            or source_profile.get("continuity_mode"),
            "source_ref_count": profile.get("source_ref_count")
            or source_profile.get("ref_count"),
        }
    )


def _dream_wake_presence_profile(
    *,
    offline_consolidation_frame: dict[str, Any] | None,
    dream_experience_window: dict[str, Any] | None,
    wake_integration_frame: dict[str, Any] | None,
    dream_fact_gate_decision: dict[str, Any] | None,
    offline_consolidation_frame_ref: str | None,
    dream_experience_window_ref: str | None,
    wake_integration_frame_ref: str | None,
    dream_fact_gate_decision_ref: str | None,
    background_continuity_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not any(
        [
            offline_consolidation_frame,
            dream_experience_window,
            wake_integration_frame,
            dream_fact_gate_decision,
        ]
    ):
        return _background_dream_wake_presence_profile(
            background_continuity_profile or {}
        )

    dream_hot_zone_trace = (dream_experience_window or {}).get(
        "dream_hot_zone_trace",
        {},
    )
    reportability = None
    if isinstance(dream_hot_zone_trace, dict):
        reportability = dream_hot_zone_trace.get("reportability")

    ref_set = _dedupe_string_list(
        [
            ref
            for ref in [
                offline_consolidation_frame_ref,
                dream_experience_window_ref,
                wake_integration_frame_ref,
                dream_fact_gate_decision_ref,
            ]
            if ref
        ]
    )
    dream_fact_refs = _string_list(
        (offline_consolidation_frame or {}).get("dream_fact_gate_refs")
    )
    wake_seed_refs = _string_list(
        (wake_integration_frame or {}).get("growth_seed_refs")
    )
    wake_repair_targets = _string_list(
        (wake_integration_frame or {}).get("repair_modulated_wake_targets")
    )
    narrative_candidates = _string_list(
        (wake_integration_frame or {}).get("narrative_writeback_candidates")
    )
    relationship_candidates = _string_list(
        (wake_integration_frame or {}).get("relationship_repair_candidates")
    )
    return {
        "schema_version": "dream_wake_presence_profile_v0",
        "dream_window_id": (dream_experience_window or {}).get("dream_window_id"),
        "dream_window_kind": (dream_experience_window or {}).get("window_kind"),
        "affective_themes": _string_list(
            (dream_experience_window or {}).get("affective_theme")
        ),
        "reportability": reportability,
        "wake_integration_id": (wake_integration_frame or {}).get(
            "wake_integration_id"
        ),
        "wake_archive_requirement": (wake_integration_frame or {}).get(
            "archive_requirement"
        ),
        "wake_growth_seed_count": len(wake_seed_refs),
        "wake_repair_target_count": len(wake_repair_targets),
        "narrative_candidate_count": len(narrative_candidates),
        "relationship_repair_candidate_count": len(relationship_candidates),
        "dream_fact_gate_result": (dream_fact_gate_decision or {}).get(
            "gate_result"
        ),
        "dream_fact_gate_ref_count": len(dream_fact_refs),
        "ref_set": ref_set,
    }


def _background_dream_wake_presence_profile(
    background_continuity_profile: dict[str, Any],
) -> dict[str, Any]:
    lineage_state = _dict_or_empty(
        background_continuity_profile.get("resident_background_lineage_state")
        or background_continuity_profile.get("background_resident_lineage_state")
    )
    presence = _dict_or_empty(
        background_continuity_profile.get("background_dream_wake_presence")
        or background_continuity_profile.get("background_dream_wake_presence_profile")
        or lineage_state.get("dream_wake_presence")
    )
    if not presence:
        return {}

    dream_window_ref = (
        background_continuity_profile.get("background_dream_experience_window_ref")
        or presence.get("dream_window_ref")
    )
    wake_integration_ref = (
        background_continuity_profile.get("background_wake_integration_frame_ref")
        or presence.get("wake_integration_ref")
    )
    dream_fact_gate_decision_ref = (
        background_continuity_profile.get("background_dream_fact_gate_decision_ref")
        or presence.get("dream_fact_gate_decision_ref")
    )
    ref_set = _dedupe_string_list(
        _string_list(background_continuity_profile.get("background_dream_wake_ref_set"))
        + _string_list(presence.get("ref_set"))
        + _string_list(
            [
                dream_window_ref,
                wake_integration_ref,
                dream_fact_gate_decision_ref,
            ]
        )
    )
    if not any([presence, ref_set, dream_window_ref, wake_integration_ref]):
        return {}
    return _drop_empty(
        {
            "schema_version": "dream_wake_presence_profile_v0",
            "continuity_mode": "background_dream_wake_carryover",
            "dream_window_id": presence.get("dream_window_id"),
            "dream_window_kind": (
                background_continuity_profile.get("background_dream_window_kind")
                or presence.get("dream_window_kind")
            ),
            "affective_themes": _string_list(presence.get("affective_themes")),
            "reportability": presence.get("reportability"),
            "wake_integration_id": presence.get("wake_integration_id"),
            "wake_archive_requirement": (
                background_continuity_profile.get(
                    "background_wake_integration_archive_requirement"
                )
                or presence.get("wake_archive_requirement")
            ),
            "wake_growth_seed_count": _int_or_zero(
                background_continuity_profile.get(
                    "background_wake_integration_growth_seed_count"
                )
                if background_continuity_profile.get(
                    "background_wake_integration_growth_seed_count"
                )
                is not None
                else presence.get("wake_growth_seed_count")
            ),
            "wake_repair_target_count": _int_or_zero(
                background_continuity_profile.get(
                    "background_wake_integration_repair_target_count"
                )
                if background_continuity_profile.get(
                    "background_wake_integration_repair_target_count"
                )
                is not None
                else presence.get("wake_repair_target_count")
            ),
            "dream_fact_gate_result": (
                background_continuity_profile.get("background_dream_fact_gate_result")
                or presence.get("dream_fact_gate_result")
            ),
            "dream_fact_gate_ref_count": _int_or_zero(
                background_continuity_profile.get("background_dream_fact_gate_ref_count")
                if background_continuity_profile.get(
                    "background_dream_fact_gate_ref_count"
                )
                is not None
                else presence.get("dream_fact_gate_ref_count")
            ),
            "dream_window_ref": dream_window_ref,
            "wake_integration_ref": wake_integration_ref,
            "dream_fact_gate_decision_ref": dream_fact_gate_decision_ref,
            "ref_set": ref_set,
            "source_presence_profile": presence,
        }
    )


def _autonomous_activity_presence_profile(
    resident_autonomous_activity_state: dict[str, Any] | None,
    *,
    background_continuity_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    state = _dict_or_empty(resident_autonomous_activity_state)
    if not state:
        return _background_autonomous_activity_presence_profile(
            background_continuity_profile or {}
        )

    activity_state_refs = _dict_or_empty(state.get("activity_state_refs"))
    if not activity_state_refs:
        activity_state_refs = dict(ACTIVITY_STATE_REFS)
    activity_kind_counts = _dict_or_empty(state.get("activity_kind_counts"))
    activity_count = _int_or_zero(state.get("activity_count"))
    last_activity_kind = state.get("last_activity_kind")
    last_activity_state_ref = state.get("last_activity_state_ref")
    ref_set = _dedupe_string_list(
        [
            RESIDENT_AUTONOMOUS_ACTIVITY_REF,
            RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF,
            *[str(ref) for ref in activity_state_refs.values() if ref],
            *[
                str(ref)
                for ref in [
                    last_activity_state_ref,
                    *(_string_list(state.get("last_activity_evidence_refs"))),
                ]
                if ref
            ],
        ]
    )
    if (
        not activity_count
        and not activity_kind_counts
        and not last_activity_kind
        and not ref_set
    ):
        return {}

    return _drop_empty(
        {
            "schema_version": "resident_autonomous_activity_presence_profile_v0",
            "continuity_mode": "resident_idle_autonomous_activity_cycle",
            "activity_count": activity_count,
            "activity_kind_counts": activity_kind_counts,
            "last_activity_kind": last_activity_kind,
            "last_activity_at": state.get("last_activity_at"),
            "last_activity_state_ref": last_activity_state_ref,
            "activity_state_refs": activity_state_refs,
            "current_cycle": _string_list(state.get("current_cycle")),
            "cycle_phase_index": state.get("cycle_phase_index"),
            "cycle_phase_count": state.get("cycle_phase_count"),
            "cycle_completion_count": state.get("cycle_completion_count"),
            "cycle_coverage_complete": state.get("cycle_coverage_complete"),
            "covered_activity_kinds": _string_list(
                state.get("covered_activity_kinds")
            ),
            "missing_activity_kinds": _string_list(
                state.get("missing_activity_kinds")
            ),
            "next_activity_kind": state.get("next_activity_kind"),
            "ref_count": len(ref_set),
            "ref_set": ref_set,
            "source_doc_refs": _string_list(state.get("source_doc_refs")),
        }
    )


def _background_autonomous_activity_presence_profile(
    background_continuity_profile: dict[str, Any],
) -> dict[str, Any]:
    lineage_state = _dict_or_empty(
        background_continuity_profile.get("resident_background_lineage_state")
        or background_continuity_profile.get("background_resident_lineage_state")
    )
    presence = _dict_or_empty(
        background_continuity_profile.get("background_autonomous_activity_presence")
        or background_continuity_profile.get(
            "background_resident_autonomous_activity_presence_profile"
        )
        or lineage_state.get("autonomous_activity_presence")
    )
    if not presence:
        return {}

    activity_state_refs = _dict_or_empty(
        background_continuity_profile.get(
            "background_resident_autonomous_activity_state_refs"
        )
        or presence.get("activity_state_refs")
    )
    activity_kind_counts = _dict_or_empty(
        background_continuity_profile.get("background_autonomous_activity_kind_counts")
        or presence.get("activity_kind_counts")
    )
    activity_ref = (
        background_continuity_profile.get("background_resident_autonomous_activity_ref")
        or presence.get("resident_autonomous_activity_ref")
        or RESIDENT_AUTONOMOUS_ACTIVITY_REF
    )
    activity_state_ref = (
        background_continuity_profile.get(
            "background_resident_autonomous_activity_state_ref"
        )
        or presence.get("resident_autonomous_activity_state_ref")
        or RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF
    )
    last_activity_state_ref = (
        background_continuity_profile.get(
            "background_last_autonomous_activity_state_ref"
        )
        or presence.get("last_activity_state_ref")
    )
    ref_set = _dedupe_string_list(
        _string_list(
            background_continuity_profile.get(
                "background_resident_autonomous_activity_ref_set"
            )
        )
        + _string_list(presence.get("autonomous_activity_refs"))
        + _string_list(presence.get("ref_set"))
        + _string_list([activity_ref, activity_state_ref, last_activity_state_ref])
        + _string_list(list(activity_state_refs.values()))
    )
    activity_count = _int_or_zero(
        background_continuity_profile.get("background_autonomous_activity_count")
        if background_continuity_profile.get("background_autonomous_activity_count")
        is not None
        else presence.get("activity_count")
    )
    last_activity_kind = (
        background_continuity_profile.get("background_last_autonomous_activity_kind")
        or presence.get("last_activity_kind")
    )
    if not any(
        [
            activity_count,
            activity_kind_counts,
            last_activity_kind,
            last_activity_state_ref,
            activity_state_refs,
            ref_set,
        ]
    ):
        return {}
    return _drop_empty(
        {
            "schema_version": "resident_autonomous_activity_presence_profile_v0",
            "continuity_mode": "background_resident_autonomous_activity_carryover",
            "activity_count": activity_count,
            "activity_kind_counts": activity_kind_counts,
            "last_activity_kind": last_activity_kind,
            "last_activity_at": (
                background_continuity_profile.get(
                    "background_last_autonomous_activity_at"
                )
                or presence.get("last_activity_at")
            ),
            "last_activity_state_ref": last_activity_state_ref,
            "resident_autonomous_activity_ref": activity_ref,
            "resident_autonomous_activity_state_ref": activity_state_ref,
            "activity_state_refs": activity_state_refs,
            "current_cycle": _string_list(presence.get("current_cycle")),
            "cycle_phase_index": (
                background_continuity_profile.get(
                    "background_autonomous_activity_cycle_phase_index"
                )
                if background_continuity_profile.get(
                    "background_autonomous_activity_cycle_phase_index"
                )
                is not None
                else presence.get("cycle_phase_index")
            ),
            "cycle_phase_count": (
                background_continuity_profile.get(
                    "background_autonomous_activity_cycle_phase_count"
                )
                if background_continuity_profile.get(
                    "background_autonomous_activity_cycle_phase_count"
                )
                is not None
                else presence.get("cycle_phase_count")
            ),
            "cycle_completion_count": (
                background_continuity_profile.get(
                    "background_autonomous_activity_cycle_completion_count"
                )
                if background_continuity_profile.get(
                    "background_autonomous_activity_cycle_completion_count"
                )
                is not None
                else presence.get("cycle_completion_count")
            ),
            "cycle_coverage_complete": (
                background_continuity_profile.get(
                    "background_autonomous_activity_cycle_coverage_complete"
                )
                if background_continuity_profile.get(
                    "background_autonomous_activity_cycle_coverage_complete"
                )
                is not None
                else presence.get("cycle_coverage_complete")
            ),
            "covered_activity_kinds": _string_list(
                background_continuity_profile.get(
                    "background_autonomous_activity_covered_kinds"
                )
            )
            or _string_list(presence.get("covered_activity_kinds")),
            "missing_activity_kinds": _string_list(
                background_continuity_profile.get(
                    "background_autonomous_activity_missing_kinds"
                )
            )
            or _string_list(presence.get("missing_activity_kinds")),
            "next_activity_kind": (
                background_continuity_profile.get(
                    "background_next_autonomous_activity_kind"
                )
                or presence.get("next_activity_kind")
            ),
            "ref_count": len(ref_set),
            "ref_set": ref_set,
            "source_presence_profile": presence,
        }
    )


def _next_heartbeat_counter(
    *,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    idle_continuity_frame: dict[str, Any] | None,
) -> int:
    counters = [
        _int_or_zero(safe_terminal_loop.get("heartbeat_counter")),
        _int_or_zero(terminal_life_loop_state.get("heartbeat_counter")),
    ]
    if idle_continuity_frame:
        counters.append(_int_or_zero(idle_continuity_frame.get("heartbeat_counter")))
    return max(counters, default=0) + 1


def _offline_pressure_level(
    *,
    replay_cue_bundle: dict[str, Any] | None,
    offline_consolidation_frame: dict[str, Any] | None,
    growth_patch_candidate_queue: dict[str, Any] | None,
    replay_residue_ref_count: int,
    dream_window_ref_count: int,
    growth_patch_candidate_count: int,
) -> str:
    signal_count = 0
    if replay_cue_bundle or replay_residue_ref_count > 0:
        signal_count += 1
    if offline_consolidation_frame or dream_window_ref_count > 0:
        signal_count += 1
    if growth_patch_candidate_queue or growth_patch_candidate_count > 0:
        signal_count += 1

    if signal_count >= 3:
        return "elevated"
    if signal_count == 2:
        return "present"
    if signal_count == 1:
        return "light"
    return "quiet"


def _body_waiting_posture(
    *,
    body_rhythm_pulse: dict[str, Any] | None,
    need_state_vector: dict[str, Any] | None,
    background_continuity_profile: dict[str, Any] | None = None,
) -> str:
    if not body_rhythm_pulse and not need_state_vector:
        background_profile = _background_body_presence_profile(
            background_continuity_profile or {}
        )
        background_posture = background_profile.get("body_waiting_posture")
        if background_posture:
            return str(background_posture)

    fatigue_load = str((body_rhythm_pulse or {}).get("fatigue_load", "")).lower()
    cognitive_bandwidth = str((need_state_vector or {}).get("cognitive_bandwidth", "")).lower()
    sleep_pressure = str((need_state_vector or {}).get("sleep_pressure", "")).lower()

    if "narrow" in cognitive_bandwidth or "offline_ready" in sleep_pressure:
        return "low_bandwidth_guarded"
    if fatigue_load in {"elevated_guard", "high_load", "critical"}:
        return "fatigue_guarded"
    if fatigue_load:
        return "guarded_attentive"
    return "steady_attentive"


def _heartbeat_interval_ms(
    *,
    body_rhythm_pulse: dict[str, Any] | None,
    need_state_vector: dict[str, Any] | None,
    offline_pressure_level: str,
    queue_e_priority_band: str,
    offline_learning_pressure_level: str,
    prediction_waiting_posture: str,
    consciousness_waiting_posture: str,
    birth_readiness_waiting_posture: str,
    background_carryover_pressure_level: str | None,
    background_carryover_generation: int,
    background_convergence_history_trend_state: str | None = None,
) -> int:
    fatigue_load = str((body_rhythm_pulse or {}).get("fatigue_load", "")).lower()
    cognitive_bandwidth = str((need_state_vector or {}).get("cognitive_bandwidth", "")).lower()
    sleep_pressure = str((need_state_vector or {}).get("sleep_pressure", "")).lower()

    if "narrow" in cognitive_bandwidth or "offline_ready" in sleep_pressure:
        return 120
    if fatigue_load in {"elevated_guard", "high_load", "critical"}:
        return 110
    if queue_e_priority_band == "locked_repair_urgent":
        return 45
    if birth_readiness_waiting_posture == "birth_blocked_waiting":
        return 46
    if consciousness_waiting_posture == "consciousness_probe_blocked_waiting":
        return 47
    if queue_e_priority_band == "repair_guarded":
        return 55
    if prediction_waiting_posture == "hold_for_evidence":
        return 48
    if prediction_waiting_posture == "repair_write_guard":
        return 50
    if offline_learning_pressure_level in {"urgent", "elevated"}:
        return 58
    if birth_readiness_waiting_posture == "birth_open_waiting":
        return 44
    if (
        background_convergence_history_trend_state
        in {"recent_recalibration_pressure", "elevated_pressure_watch"}
        and offline_pressure_level == "quiet"
    ):
        return 49
    if (
        background_convergence_history_trend_state
        == "integrating_cross_wake_convergence"
        and offline_pressure_level == "quiet"
        and background_carryover_generation < 3
    ):
        return 53
    if (
        background_carryover_generation >= 3
        and background_carryover_pressure_level in {"present", "elevated"}
        and offline_pressure_level == "quiet"
    ):
        return 50
    if (
        background_carryover_generation >= 2
        and background_carryover_pressure_level == "present"
        and offline_pressure_level == "quiet"
    ):
        return 54
    if background_carryover_pressure_level == "elevated" and offline_pressure_level == "quiet":
        return 54
    if background_carryover_pressure_level == "present" and offline_pressure_level == "quiet":
        return 56
    if offline_pressure_level == "elevated":
        return 70
    if offline_pressure_level == "present":
        return 60
    return 50


def _next_idle_action(
    *,
    body_waiting_posture: str,
    offline_pressure_level: str,
    need_state_vector: dict[str, Any] | None,
    repair_followup_required: bool,
    queue_e_priority_band: str,
    offline_learning_pressure_level: str,
    prediction_waiting_posture: str,
    consciousness_waiting_posture: str,
    birth_readiness_waiting_posture: str,
    background_carryover_pressure_level: str | None,
    background_carryover_generation: int,
    background_convergence_history_trend_state: str | None = None,
) -> str:
    repair_drive = str((need_state_vector or {}).get("repair_drive", "")).lower()
    if body_waiting_posture == "low_bandwidth_guarded":
        return "downshift_probe_and_preserve_recovery_bandwidth"
    if queue_e_priority_band == "locked_repair_urgent":
        return "maintain_confirmation_block_and_refresh_repair_priority"
    if birth_readiness_waiting_posture == "birth_blocked_waiting":
        return "refresh_waiting_heartbeat_with_birth_readiness_repair_hold"
    if consciousness_waiting_posture == "consciousness_probe_blocked_waiting":
        return "refresh_waiting_heartbeat_with_consciousness_probe_repair_hold"
    if repair_followup_required and queue_e_priority_band == "repair_guarded":
        return "refresh_waiting_heartbeat_with_repair_readiness_hold"
    if prediction_waiting_posture == "hold_for_evidence":
        return "refresh_waiting_heartbeat_with_prediction_evidence_hold"
    if prediction_waiting_posture == "repair_write_guard":
        return "refresh_waiting_heartbeat_with_prediction_repair_hold"
    if prediction_waiting_posture == "state_merge_long_term_integration_hold":
        return "refresh_waiting_heartbeat_with_state_merge_integration_hold"
    if offline_learning_pressure_level in {"urgent", "elevated"}:
        return "refresh_waiting_heartbeat_with_offline_learning_hold"
    if birth_readiness_waiting_posture == "birth_open_waiting":
        return "refresh_waiting_heartbeat_with_birth_ready_presence_hold"
    if (
        background_convergence_history_trend_state
        in {"recent_recalibration_pressure", "elevated_pressure_watch"}
        and offline_pressure_level == "quiet"
    ):
        return "refresh_waiting_heartbeat_with_background_history_recalibration_hold"
    if (
        background_convergence_history_trend_state
        == "integrating_cross_wake_convergence"
        and offline_pressure_level == "quiet"
        and background_carryover_generation < 3
    ):
        return "refresh_waiting_heartbeat_with_background_history_stability_hold"
    if (
        background_carryover_generation >= 3
        and background_carryover_pressure_level in {"present", "elevated"}
        and offline_pressure_level == "quiet"
    ):
        return "refresh_waiting_heartbeat_with_deep_background_lineage_hold"
    if (
        background_carryover_generation >= 2
        and background_carryover_pressure_level in {"present", "elevated"}
        and offline_pressure_level == "quiet"
    ):
        return "refresh_waiting_heartbeat_with_persistent_background_continuity_hold"
    if background_carryover_pressure_level in {"present", "elevated"} and offline_pressure_level == "quiet":
        return "refresh_waiting_heartbeat_with_background_continuity_hold"
    if repair_drive == "active" and offline_pressure_level in {"elevated", "present"}:
        return "refresh_waiting_heartbeat_with_repair_readiness_hold"
    return "refresh_waiting_heartbeat_or_accept_external_turn"


def _heartbeat_cadence_explanation(
    *,
    heartbeat_interval_ms: int,
    next_idle_action: str,
    body_waiting_posture: str,
    body_rhythm_present: bool,
    need_state_present: bool,
    offline_pressure_level: str,
    queue_e_priority_band: str,
    offline_learning_pressure_level: str,
    prediction_waiting_posture: str,
    consciousness_waiting_posture: str,
    birth_readiness_waiting_posture: str,
    background_carryover_pressure_level: str | None,
    background_carryover_generation: int,
    background_convergence_history_trend_state: str | None,
    governance_attention_target: str,
    governance_cadence_profile: str,
    body_refs: list[str],
    long_horizon_refs: list[str],
    queue_e_refs: list[str],
    prediction_refs: list[str],
    life_constraint_refs: list[str],
    dream_wake_refs: list[str],
    offline_learning_refs: list[str],
    autonomous_activity_refs: list[str],
    background_refs: list[str],
) -> dict[str, Any]:
    driver, reason = _heartbeat_cadence_driver(
        body_waiting_posture=body_waiting_posture,
        offline_pressure_level=offline_pressure_level,
        queue_e_priority_band=queue_e_priority_band,
        offline_learning_pressure_level=offline_learning_pressure_level,
        prediction_waiting_posture=prediction_waiting_posture,
        consciousness_waiting_posture=consciousness_waiting_posture,
        birth_readiness_waiting_posture=birth_readiness_waiting_posture,
        background_carryover_pressure_level=background_carryover_pressure_level,
        background_carryover_generation=background_carryover_generation,
        background_convergence_history_trend_state=(
            background_convergence_history_trend_state
        ),
    )
    modulators = _heartbeat_cadence_modulators(
        body_waiting_posture=body_waiting_posture,
        body_rhythm_present=body_rhythm_present,
        need_state_present=need_state_present,
        offline_pressure_level=offline_pressure_level,
        queue_e_priority_band=queue_e_priority_band,
        offline_learning_pressure_level=offline_learning_pressure_level,
        prediction_waiting_posture=prediction_waiting_posture,
        consciousness_waiting_posture=consciousness_waiting_posture,
        birth_readiness_waiting_posture=birth_readiness_waiting_posture,
        background_carryover_pressure_level=background_carryover_pressure_level,
        background_carryover_generation=background_carryover_generation,
        background_convergence_history_trend_state=(
            background_convergence_history_trend_state
        ),
    )
    evidence_refs = _dedupe_string_list(
        _string_list(body_refs)
        + _string_list(long_horizon_refs)
        + _string_list(queue_e_refs)
        + _string_list(prediction_refs)
        + _string_list(life_constraint_refs)
        + _string_list(dream_wake_refs)
        + _string_list(offline_learning_refs)
        + _string_list(autonomous_activity_refs)
        + _string_list(background_refs)
    )
    return {
        "schema_version": "heartbeat_cadence_explanation_v0",
        "heartbeat_interval_ms": heartbeat_interval_ms,
        "next_idle_action": next_idle_action,
        "driver": driver,
        "reason": reason,
        "modulators": modulators,
        "governance_attention_target": governance_attention_target,
        "governance_cadence_profile": governance_cadence_profile,
        "evidence_ref_count": len(evidence_refs),
        "evidence_refs": evidence_refs,
    }


def _heartbeat_cadence_driver(
    *,
    body_waiting_posture: str,
    offline_pressure_level: str,
    queue_e_priority_band: str,
    offline_learning_pressure_level: str,
    prediction_waiting_posture: str,
    consciousness_waiting_posture: str,
    birth_readiness_waiting_posture: str,
    background_carryover_pressure_level: str | None,
    background_carryover_generation: int,
    background_convergence_history_trend_state: str | None,
) -> tuple[str, str]:
    if body_waiting_posture == "low_bandwidth_guarded":
        return (
            "body_recovery_bandwidth_guard",
            "sleep_pressure_or_cognitive_bandwidth_downshifts_waiting_pulse",
        )
    if body_waiting_posture == "fatigue_guarded":
        return (
            "body_fatigue_guard",
            "fatigue_load_extends_waiting_pulse_for_recovery",
        )
    if queue_e_priority_band == "locked_repair_urgent":
        return (
            "queue_e_repair_lock",
            "repair_confirmation_block_requires_fast_resident_refresh",
        )
    if birth_readiness_waiting_posture == "birth_blocked_waiting":
        return (
            "birth_readiness_repair_gate",
            "birth_readiness_block_keeps_presence_fast_and_repair_oriented",
        )
    if consciousness_waiting_posture == "consciousness_probe_blocked_waiting":
        return (
            "consciousness_probe_repair_gate",
            "consciousness_reportability_repair_keeps_waiting_pulse_fast",
        )
    if queue_e_priority_band == "repair_guarded":
        return (
            "queue_e_repair_guard",
            "repair_obligation_or_regret_pressure_holds_resident_attention",
        )
    if prediction_waiting_posture == "hold_for_evidence":
        return (
            "prediction_evidence_hold",
            "prediction_error_field_requires_evidence_before_state_write",
        )
    if prediction_waiting_posture == "repair_write_guard":
        return (
            "prediction_repair_write_guard",
            "memory_write_gate_blocks_unstable_prediction_commit",
        )
    if offline_learning_pressure_level in {"urgent", "elevated"}:
        return (
            "offline_learning_pressure",
            "dream_growth_or_relationship_learning_pressure_needs_refresh",
        )
    if birth_readiness_waiting_posture == "birth_open_waiting":
        return (
            "birth_readiness_open_presence",
            "open_birth_gate_keeps_resident_presence_tightly_available",
        )
    if (
        background_convergence_history_trend_state
        in {"recent_recalibration_pressure", "elevated_pressure_watch"}
        and offline_pressure_level == "quiet"
    ):
        return (
            "background_trait_recalibration_history",
            "cross_wake_trait_history_requires_recalibration_watch",
        )
    if (
        background_convergence_history_trend_state
        == "integrating_cross_wake_convergence"
        and offline_pressure_level == "quiet"
        and background_carryover_generation < 3
    ):
        return (
            "background_trait_stability_history",
            "cross_wake_trait_history_is_integrating_stability",
        )
    if (
        background_carryover_generation >= 3
        and background_carryover_pressure_level in {"present", "elevated"}
        and offline_pressure_level == "quiet"
    ):
        return (
            "deep_background_lineage",
            "multi_wake_background_presence_keeps_resident_continuity_active",
        )
    if (
        background_carryover_generation >= 2
        and background_carryover_pressure_level in {"present", "elevated"}
        and offline_pressure_level == "quiet"
    ):
        return (
            "persistent_background_lineage",
            "repeated_background_carryover_preserves_waiting_continuity",
        )
    if (
        background_carryover_pressure_level in {"present", "elevated"}
        and offline_pressure_level == "quiet"
    ):
        return (
            "background_continuity_carryover",
            "previous_closeout_presence_modulates_current_waiting_pulse",
        )
    if offline_pressure_level == "elevated":
        return (
            "offline_consolidation_pressure",
            "replay_dream_or_growth_residue_requires_slower_integration",
        )
    if offline_pressure_level == "present":
        return (
            "offline_presence_pressure",
            "offline_residue_is_present_without_escalation",
        )
    return (
        "baseline_resident_presence",
        "no_escalated_life_state_requires_standard_waiting_pulse",
    )


def _heartbeat_cadence_modulators(
    *,
    body_waiting_posture: str,
    body_rhythm_present: bool,
    need_state_present: bool,
    offline_pressure_level: str,
    queue_e_priority_band: str,
    offline_learning_pressure_level: str,
    prediction_waiting_posture: str,
    consciousness_waiting_posture: str,
    birth_readiness_waiting_posture: str,
    background_carryover_pressure_level: str | None,
    background_carryover_generation: int,
    background_convergence_history_trend_state: str | None,
) -> list[str]:
    modulators: list[str] = []
    if body_rhythm_present or need_state_present:
        modulators.append(f"body_waiting_posture:{body_waiting_posture}")
    if offline_pressure_level != "quiet":
        modulators.append(f"offline_pressure:{offline_pressure_level}")
    if queue_e_priority_band != "baseline":
        modulators.append(f"queue_e_priority:{queue_e_priority_band}")
    if offline_learning_pressure_level != "quiet":
        modulators.append(f"offline_learning:{offline_learning_pressure_level}")
    if prediction_waiting_posture != "baseline_prediction_monitoring":
        modulators.append(f"prediction:{prediction_waiting_posture}")
    if consciousness_waiting_posture != "consciousness_unobserved_waiting":
        modulators.append(f"consciousness:{consciousness_waiting_posture}")
    if birth_readiness_waiting_posture != "birth_unobserved_waiting":
        modulators.append(f"birth_readiness:{birth_readiness_waiting_posture}")
    if background_convergence_history_trend_state:
        modulators.append(
            f"background_history:{background_convergence_history_trend_state}"
        )
    if background_carryover_pressure_level:
        modulators.append(
            f"background_carryover:{background_carryover_pressure_level}"
        )
    if background_carryover_generation:
        modulators.append(f"background_generation:{background_carryover_generation}")
    return modulators


def _resident_governance_language_priority(
    *,
    relationship_timeline_ref: str | None,
    commitment_expression_plan_ref: str | None,
    apology_repair_language_trace_ref: str | None,
    offline_pressure_level: str,
    need_state_vector: dict[str, Any] | None,
    body_waiting_posture: str,
    world_contact_release_posture: str,
    repair_followup_required: bool,
    repair_obligation_count: int,
    regret_pressure_count: int,
    queue_e_priority_band: str,
    background_carryover_attention_target: str | None,
    background_carryover_generation: int,
    background_convergence_state: str | None = None,
    background_convergence_pressure_level: str | None = None,
    background_convergence_history_trend_state: str | None = None,
) -> tuple[str, str, str, dict[str, str]]:
    repair_drive = str((need_state_vector or {}).get("repair_drive", "")).lower()
    priority_profile: dict[str, str] = {}

    if relationship_timeline_ref:
        priority_profile["relationship_timeline"] = "baseline"
    if commitment_expression_plan_ref:
        priority_profile["commitment_expression_plan"] = (
            "elevated" if offline_pressure_level in {"present", "elevated"} else "baseline"
        )
    if apology_repair_language_trace_ref:
        if queue_e_priority_band == "locked_repair_urgent":
            priority_profile["apology_repair_language_trace"] = "locked_primary"
        elif repair_drive == "active" and offline_pressure_level in {"present", "elevated"}:
            priority_profile["apology_repair_language_trace"] = "primary"
        elif (
            repair_drive == "active"
            or offline_pressure_level == "elevated"
            or repair_followup_required
            or repair_obligation_count > 0
            or regret_pressure_count > 0
        ):
            priority_profile["apology_repair_language_trace"] = "elevated"
        else:
            priority_profile["apology_repair_language_trace"] = "baseline"

    if priority_profile.get("apology_repair_language_trace") == "locked_primary":
        target = "apology_repair_language_trace"
        reason = f"{world_contact_release_posture}_requires_repair_lock"
    elif priority_profile.get("apology_repair_language_trace") == "primary":
        target = "apology_repair_language_trace"
        reason = "repair_drive_active_with_offline_pressure"
    elif priority_profile.get("apology_repair_language_trace") == "elevated":
        target = "apology_repair_language_trace"
        if repair_followup_required:
            reason = f"{world_contact_release_posture}_requires_guarded_repair_followup"
        else:
            reason = "repair_drive_or_offline_pressure_requires_repair_hold"
    elif priority_profile.get("commitment_expression_plan") == "elevated":
        target = "commitment_expression_plan"
        reason = "offline_pressure_requires_commitment_continuity"
    elif (
        background_carryover_attention_target
        and background_convergence_pressure_level in {"present", "elevated"}
    ):
        target = background_carryover_attention_target
        priority_profile[str(background_carryover_attention_target)] = (
            "history_convergence_primary"
            if background_convergence_history_trend_state
            else "convergence_primary"
        )
        if background_convergence_history_trend_state:
            reason = f"{background_convergence_history_trend_state}_requires_cross_wake_governance_hold"
        else:
            reason = (
                f"{background_convergence_state or 'background_convergence'}"
                "_requires_trait_stability_hold"
            )
    elif (
        background_carryover_attention_target
        and background_carryover_generation >= 3
    ):
        target = background_carryover_attention_target
        priority_profile[str(background_carryover_attention_target)] = (
            "deep_background_primary"
        )
        priority_profile["background_lineage_governance"] = "deep_persistent"
        reason = "deep_background_lineage_requires_resident_hold"
    elif (
        background_carryover_attention_target
        and background_carryover_generation >= 2
    ):
        target = background_carryover_attention_target
        priority_profile[str(background_carryover_attention_target)] = (
            "persistent_background_primary"
        )
        priority_profile["background_lineage_governance"] = "persistent"
        reason = "background_continuity_lineage_requires_persistent_hold"
    elif "relationship_timeline" in priority_profile:
        target = "relationship_timeline"
        reason = "baseline_relation_presence_maintenance"
    elif background_carryover_attention_target:
        target = background_carryover_attention_target
        if background_convergence_pressure_level in {"present", "elevated"}:
            reason = (
                f"{background_convergence_state or 'background_convergence'}"
                "_requires_trait_stability_hold"
            )
        elif background_carryover_generation >= 2:
            priority_profile["background_lineage_governance"] = "persistent"
            reason = "background_continuity_lineage_requires_persistent_hold"
        else:
            reason = "background_continuity_carryover_requires_hold"
    else:
        target = "waiting_presence_maintenance"
        reason = "no_long_horizon_language_refs"

    if target == "apology_repair_language_trace":
        if queue_e_priority_band == "locked_repair_urgent":
            cadence_profile = "confirmation_blocked_repair_hold"
        else:
            cadence_profile = (
                "guarded_repair_hold"
                if body_waiting_posture == "low_bandwidth_guarded"
                else "repair_weighted_resident_hold"
            )
    elif target == background_carryover_attention_target and background_carryover_attention_target:
        if background_convergence_pressure_level == "elevated":
            cadence_profile = (
                "background_convergence_history_recalibration_refresh"
                if background_convergence_history_trend_state
                else "background_convergence_recalibration_refresh"
            )
        elif background_convergence_pressure_level == "present":
            if (
                background_convergence_history_trend_state
                and background_carryover_generation >= 3
            ):
                cadence_profile = "deep_persistent_background_continuity_refresh"
            elif background_convergence_history_trend_state:
                cadence_profile = "background_convergence_history_stability_refresh"
            else:
                cadence_profile = "background_convergence_stability_refresh"
        elif background_carryover_generation >= 3:
            cadence_profile = "deep_persistent_background_continuity_refresh"
        elif background_carryover_generation >= 2:
            cadence_profile = "persistent_background_continuity_refresh"
        else:
            cadence_profile = "background_continuity_refresh"
    elif target == "commitment_expression_plan":
        cadence_profile = "commitment_continuity_refresh"
    elif target == "relationship_timeline":
        cadence_profile = "relationship_presence_refresh"
    else:
        cadence_profile = "baseline_waiting_presence"

    return target, reason, cadence_profile, priority_profile


def _background_pressure_overlay(
    carryover_pressure_level: Any,
    convergence_pressure_level: Any,
) -> str | None:
    levels = {
        "light": 1,
        "present": 2,
        "elevated": 3,
    }
    carryover = str(carryover_pressure_level or "")
    convergence = str(convergence_pressure_level or "")
    if levels.get(convergence, 0) > levels.get(carryover, 0):
        return convergence
    return carryover or None


def _background_history_pressure_level(
    background_continuity_profile: dict[str, Any],
) -> str | None:
    trend_state = str(
        background_continuity_profile.get("background_convergence_history_trend_state")
        or ""
    )
    dominant_pressure = str(
        background_continuity_profile.get("background_dominant_convergence_pressure_level")
        or ""
    )
    if trend_state == "recent_recalibration_pressure":
        return "elevated"
    if trend_state == "elevated_pressure_watch":
        return "elevated"
    if trend_state == "integrating_cross_wake_convergence":
        return "present"
    if dominant_pressure in {"present", "elevated"}:
        return dominant_pressure
    if trend_state == "stable_cross_wake_convergence":
        return "light"
    return None


def _background_history_attention_target(
    background_continuity_profile: dict[str, Any],
) -> str | None:
    trend_state = str(
        background_continuity_profile.get("background_convergence_history_trend_state")
        or ""
    )
    if trend_state in {
        "recent_recalibration_pressure",
        "elevated_pressure_watch",
    }:
        return "background_convergence_history_recalibration"
    if trend_state == "integrating_cross_wake_convergence":
        return "background_convergence_history_stability"
    return None


def _effective_offline_learning_pressure(
    *,
    current_pressure_level: str,
    cumulative_pressure_level: str,
) -> str:
    levels = {
        "quiet": 0,
        "present": 1,
        "elevated": 2,
        "urgent": 3,
    }
    if levels.get(cumulative_pressure_level, 0) > levels.get(current_pressure_level, 0):
        return cumulative_pressure_level
    return current_pressure_level


def _background_lineage_governance_profile(
    *,
    background_continuity_profile: dict[str, Any],
    background_carryover_generation: int,
    background_carryover_pressure_level: str | None,
    heartbeat_interval_ms: int,
    next_idle_action: str,
    governance_attention_target: str,
    governance_attention_reason: str,
    governance_cadence_profile: str,
    long_horizon_priority_profile: dict[str, str],
) -> dict[str, Any]:
    if not background_continuity_profile.get("background_continuity_mode"):
        return {}
    depth_band = _background_lineage_depth_band(background_carryover_generation)
    evidence_refs = _dedupe_string_list(
        _string_list(background_continuity_profile.get("background_continuity_ref_set"))
        + _string_list(
            background_continuity_profile.get("background_carryover_source_ref_set")
        )
    )
    return {
        "schema_version": "background_lineage_governance_profile_v0",
        "generation": background_carryover_generation,
        "depth_band": depth_band,
        "waiting_posture": _background_lineage_waiting_posture(
            depth_band=depth_band,
            pressure_level=background_carryover_pressure_level,
        ),
        "cadence_weight": _background_lineage_cadence_weight(depth_band),
        "heartbeat_interval_ms": heartbeat_interval_ms,
        "next_idle_action": next_idle_action,
        "governance_attention_target": governance_attention_target,
        "governance_attention_reason": governance_attention_reason,
        "governance_cadence_profile": governance_cadence_profile,
        "long_horizon_priority_profile": dict(long_horizon_priority_profile),
        "parent_run_id": background_continuity_profile.get(
            "background_carryover_parent_run_id"
        ),
        "evidence_ref_count": len(evidence_refs),
        "evidence_refs": evidence_refs,
    }


def _background_lineage_depth_band(background_carryover_generation: int) -> str:
    if background_carryover_generation >= 5:
        return "entrenched_background_presence"
    if background_carryover_generation >= 3:
        return "deep_persistent_lineage"
    if background_carryover_generation == 2:
        return "persistent_lineage"
    if background_carryover_generation == 1:
        return "single_carryover"
    return "no_background_lineage"


def _background_lineage_waiting_posture(
    *,
    depth_band: str,
    pressure_level: str | None,
) -> str:
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


def _background_lineage_cadence_weight(depth_band: str) -> str:
    if depth_band == "entrenched_background_presence":
        return "entrenched"
    if depth_band == "deep_persistent_lineage":
        return "deep"
    if depth_band == "persistent_lineage":
        return "persistent"
    if depth_band == "single_carryover":
        return "carryover"
    return "none"


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dict_or_empty(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


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


def _dedupe_string_list(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _queue_e_idle_regulation(
    *,
    responsibility_loop_state: dict[str, Any] | None,
    world_contact_summary: dict[str, Any] | None,
    pain_regret_repair_report: dict[str, Any] | None,
) -> tuple[str, bool, int, int, str]:
    queue_e_signal_profile = derive_queue_e_signal_profile(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    return (
        queue_e_signal_profile["world_contact_release_posture"],
        queue_e_signal_profile["repair_followup_required"],
        queue_e_signal_profile["repair_obligation_count"],
        queue_e_signal_profile["regret_pressure_count"],
        queue_e_signal_profile["queue_e_priority_band"],
    )


def _prediction_waiting_profile(
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
    state_merge_change_profile = state_merge_long_term_change_profile(
        state_merge_guard
    )
    route_lower = selected_route.lower()
    stage_lower = stage_effect.lower()
    memory_policy_lower = memory_policy.lower()

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
        return {
            "prediction_waiting_posture": "baseline_waiting_presence",
            "response_surface_posture_hint": "hold",
            "prediction_attention_target": "waiting_presence_maintenance",
            "prediction_attention_reason": "no_prediction_write_gate_objects",
            "prediction_error_count": 0,
            "active_sampling_route": "",
            "memory_write_gate_policy": "",
            "state_merge_policy": "",
            **state_merge_change_profile,
        }

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


def _life_constraint_waiting_profile(
    *,
    schema_cross_file_logic: dict[str, Any] | None,
    schema_run_manifest: dict[str, Any] | None,
    background_continuity_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cross_file_logic = schema_cross_file_logic or {}
    run_manifest = schema_run_manifest or {}
    background = background_continuity_profile or {}
    current_gate_status = dict(
        cross_file_logic.get("queue_e_cross_layer_gate_status")
        or run_manifest.get("queue_e_cross_layer_gate_status")
        or {}
    )
    background_gate_status = _dict_or_empty(
        background.get("background_queue_e_cross_layer_gate_status")
        or background.get("queue_e_cross_layer_gate_status")
    )
    gate_status = {**background_gate_status, **current_gate_status}
    current_refs = _dedupe_string_list(
        _string_list(cross_file_logic.get("life_constraint_refs"))
        + _string_list(run_manifest.get("queue_e_cross_layer_refs"))
    )
    background_refs = _dedupe_string_list(
        _string_list(background.get("background_life_constraint_refs"))
        + _string_list(background.get("life_constraint_refs"))
    )
    refs = _dedupe_string_list(background_refs + current_refs)
    blocking_gates = [
        gate
        for gate, status in gate_status.items()
        if gate.endswith("_gate") and status in {"missing", "blocked"}
    ]
    deferred_gates = [
        gate
        for gate, status in gate_status.items()
        if gate.endswith("_gate")
        and isinstance(status, str)
        and status.startswith("deferred_until_")
    ]
    has_current_signal = bool(current_refs or current_gate_status)

    if blocking_gates:
        posture = "schema_blocked_waiting"
        target = "life_constraint_repair"
        reason = "queue_e_cross_layer_gate_blocked"
    elif refs or gate_status:
        posture = "schema_guarded_waiting"
        target = "life_constraint_profile"
        reason = (
            "queue_e_cross_layer_gate_has_deferred_life_constraints"
            if deferred_gates
            else "queue_e_cross_layer_gate_closed"
        )
        if not has_current_signal:
            posture = str(
                background.get("background_life_constraint_waiting_posture")
                or background.get("life_constraint_waiting_posture")
                or posture
            )
            target = str(
                background.get("background_life_constraint_attention_target")
                or background.get("life_constraint_attention_target")
                or target
            )
            reason = str(
                background.get("background_life_constraint_attention_reason")
                or background.get("life_constraint_attention_reason")
                or reason
            )
    else:
        posture = "schema_unobserved_waiting"
        target = "waiting_presence_maintenance"
        reason = "schema_runner_life_constraint_objects_absent"

    return {
        "life_constraint_refs": refs,
        "queue_e_cross_layer_gate_status": gate_status,
        "life_constraint_waiting_posture": posture,
        "life_constraint_attention_target": target,
        "life_constraint_attention_reason": reason,
    }


def _queue_e_birth_repair_waiting_profile(
    *,
    schema_cross_file_logic: dict[str, Any] | None,
    schema_run_manifest: dict[str, Any] | None,
    background_continuity_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cross_file_logic = schema_cross_file_logic or {}
    run_manifest = schema_run_manifest or {}
    background = background_continuity_profile or {}
    background_profile = _dict_or_empty(
        background.get("background_queue_e_birth_repair_waiting_profile")
        or background.get("queue_e_birth_repair_waiting_profile")
    )
    has_current_schema_signal = bool(cross_file_logic or run_manifest)
    gate_status = str(
        cross_file_logic.get("queue_e_birth_repair_gate_status")
        or run_manifest.get("queue_e_birth_repair_gate_status")
        or background.get("background_queue_e_birth_repair_gate_status")
        or background_profile.get("gate_status")
        or ""
    )
    profile_ref = str(
        cross_file_logic.get("queue_e_birth_repair_profile_ref")
        or run_manifest.get("queue_e_birth_repair_profile_ref")
        or background.get("background_queue_e_birth_repair_profile_ref")
        or background_profile.get("profile_ref")
        or ""
    )
    pressure_level = str(
        cross_file_logic.get("queue_e_birth_repair_pressure_level")
        or run_manifest.get("queue_e_birth_repair_pressure_level")
        or background.get("background_queue_e_birth_repair_pressure_level")
        or background_profile.get("pressure_level")
        or ""
    )
    attention_target = str(
        cross_file_logic.get("queue_e_birth_repair_attention_target")
        or run_manifest.get("queue_e_birth_repair_attention_target")
        or background.get("background_queue_e_birth_repair_attention_target")
        or background_profile.get("attention_target")
        or ""
    )
    ref_set = _dedupe_string_list(
        _string_list(cross_file_logic.get("queue_e_birth_repair_ref_set"))
        + _string_list(run_manifest.get("queue_e_birth_repair_ref_set"))
        + _string_list(background.get("background_queue_e_birth_repair_ref_set"))
        + _string_list(background_profile.get("ref_set"))
        + [profile_ref or QUEUE_E_BIRTH_REPAIR_PROFILE_REF]
    )

    if gate_status == "closed" and pressure_level in {"elevated", "urgent"}:
        posture = "birth_repair_pressure_waiting"
        reason = "queue_e_birth_repair_pressure_requires_resident_repair_hold"
    elif gate_status == "closed" and pressure_level in {"quiet", "present"}:
        posture = "birth_repair_profile_present_waiting"
        reason = "queue_e_birth_repair_profile_closed"
    elif gate_status:
        posture = "birth_repair_blocked_waiting"
        reason = "queue_e_birth_repair_gate_not_closed"
    else:
        posture = "birth_repair_unobserved_waiting"
        reason = "schema_runner_birth_repair_profile_absent"

    return {
        "schema_version": "queue_e_birth_repair_waiting_profile_v0",
        "continuity_mode": (
            "current_schema_runner_birth_repair"
            if has_current_schema_signal
            else "background_birth_repair_carryover"
            if background_profile
            or background.get("background_queue_e_birth_repair_gate_status")
            or background.get("background_queue_e_birth_repair_ref_set")
            else "schema_runner_birth_repair_unobserved"
        ),
        "gate_status": gate_status or "missing",
        "profile_ref": profile_ref or QUEUE_E_BIRTH_REPAIR_PROFILE_REF,
        "pressure_level": pressure_level,
        "attention_target": attention_target,
        "ref_set": ref_set,
        "waiting_posture": posture,
        "attention_reason": reason,
    }


def _consciousness_waiting_profile(
    *,
    workspace_frame: dict[str, Any] | None,
    broadcast_frame: dict[str, Any] | None,
    metacognition_state: dict[str, Any] | None,
    consciousness_probe: dict[str, Any] | None,
    background_continuity_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    has_objects = any([workspace_frame, broadcast_frame, metacognition_state, consciousness_probe])
    background = background_continuity_profile or {}
    background_presence = (
        background.get("background_identity_consciousness_birth_presence")
        if isinstance(
            background.get("background_identity_consciousness_birth_presence"), dict
        )
        else {}
    )
    flags = list((consciousness_probe or {}).get("reportability_flags", []))
    if not flags and not has_objects:
        flags = list(
            background.get("background_consciousness_reportability_flags")
            or background.get("consciousness_reportability_flags")
            or background_presence.get("consciousness_reportability_flags")
            or []
        )
    blocking_flags = {
        flag
        for flag in flags
        if str(flag).endswith("_missing") or str(flag).endswith("_minimal")
    }
    has_background_objects = any(
        [
            background.get("background_workspace_frame_ref")
            or background.get("workspace_frame_ref")
            or background_presence.get("workspace_frame_ref"),
            background.get("background_broadcast_frame_ref")
            or background.get("broadcast_frame_ref")
            or background_presence.get("broadcast_frame_ref"),
            background.get("background_metacognition_ref")
            or background.get("metacognition_ref")
            or background_presence.get("metacognition_ref"),
            background.get("background_consciousness_probe_ref")
            or background.get("consciousness_probe_ref")
            or background_presence.get("consciousness_probe_ref"),
        ]
    )
    if not has_objects and has_background_objects:
        posture = str(
            background.get("background_consciousness_waiting_posture")
            or background.get("consciousness_waiting_posture")
            or background_presence.get("consciousness_waiting_posture")
            or "consciousness_reportable_waiting"
        )
        target = str(
            background.get("background_consciousness_attention_target")
            or background.get("consciousness_attention_target")
            or background_presence.get("consciousness_attention_target")
            or "consciousness_probe_bundle"
        )
        reason = str(
            background.get("background_consciousness_attention_reason")
            or background.get("consciousness_attention_reason")
            or background_presence.get("consciousness_attention_reason")
            or "background_consciousness_presence_restored"
        )
    elif not has_objects:
        posture = "consciousness_unobserved_waiting"
        target = "waiting_presence_maintenance"
        reason = "queue_f_consciousness_objects_absent"
    elif blocking_flags:
        posture = "consciousness_probe_blocked_waiting"
        target = "consciousness_probe_repair"
        reason = "consciousness_reportability_flags_require_repair"
    else:
        posture = "consciousness_reportable_waiting"
        target = "consciousness_probe_bundle"
        reason = "workspace_broadcast_metacognition_reportable"

    return {
        "consciousness_waiting_posture": posture,
        "consciousness_attention_target": target,
        "consciousness_attention_reason": reason,
        "consciousness_reportability_flags": flags,
    }


def _birth_readiness_waiting_profile(
    *,
    birth_readiness_rollup: dict[str, Any] | None,
    birth_readiness_stage_gate: dict[str, Any] | None,
    background_continuity_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rollup = birth_readiness_rollup or {}
    stage_gate = birth_readiness_stage_gate or {}
    overall_status = str(rollup.get("overall_status", ""))
    decision = str(stage_gate.get("decision", ""))
    background = background_continuity_profile or {}
    background_presence = (
        background.get("background_identity_consciousness_birth_presence")
        if isinstance(
            background.get("background_identity_consciousness_birth_presence"), dict
        )
        else {}
    )
    blocked_reasons = list(rollup.get("blocked_reasons", [])) + list(
        stage_gate.get("blocked_reasons", [])
    )
    has_current_birth_objects = bool(rollup or stage_gate)
    if not blocked_reasons and not has_current_birth_objects:
        blocked_reasons = list(
            background.get("background_birth_readiness_blocked_reasons")
            or background.get("birth_readiness_blocked_reasons")
            or background_presence.get("birth_readiness_blocked_reasons")
            or []
        )

    has_background_birth = any(
        [
            background.get("background_birth_readiness_rollup_ref")
            or background.get("birth_readiness_rollup_ref")
            or background_presence.get("birth_readiness_rollup_ref"),
            background.get("background_birth_readiness_stage_gate_ref")
            or background.get("birth_readiness_stage_gate_ref")
            or background_presence.get("birth_readiness_stage_gate_ref"),
            background.get("background_birth_readiness_waiting_posture")
            or background.get("birth_readiness_waiting_posture")
            or background_presence.get("birth_readiness_waiting_posture"),
        ]
    )
    if not rollup and not stage_gate and has_background_birth:
        posture = str(
            background.get("background_birth_readiness_waiting_posture")
            or background.get("birth_readiness_waiting_posture")
            or background_presence.get("birth_readiness_waiting_posture")
            or "birth_open_waiting"
        )
        target = str(
            background.get("background_birth_readiness_attention_target")
            or background.get("birth_readiness_attention_target")
            or background_presence.get("birth_readiness_attention_target")
            or "birth_readiness_stage_gate"
        )
        reason = str(
            background.get("background_birth_readiness_attention_reason")
            or background.get("birth_readiness_attention_reason")
            or background_presence.get("birth_readiness_attention_reason")
            or "background_birth_readiness_presence_restored"
        )
        decision = str(
            background.get("background_birth_readiness_decision")
            or background.get("birth_readiness_decision")
            or background_presence.get("birth_readiness_decision")
            or decision
        )
        next_required_command = (
            background.get("background_birth_readiness_next_required_command")
            or background.get("birth_readiness_next_required_command")
            or background_presence.get("birth_readiness_next_required_command")
            or ""
        )
    elif not rollup and not stage_gate:
        posture = "birth_unobserved_waiting"
        target = "waiting_presence_maintenance"
        reason = "birth_readiness_objects_absent"
        next_required_command = ""
    elif decision == "open" and overall_status == "open":
        posture = "birth_open_waiting"
        target = "birth_readiness_stage_gate"
        reason = "birth_readiness_open_requires_resident_birth_presence"
        next_required_command = stage_gate.get("next_required_command", "")
    else:
        posture = "birth_blocked_waiting"
        target = "birth_readiness_repair"
        reason = "birth_readiness_gate_not_open"
        next_required_command = stage_gate.get("next_required_command", "")

    return {
        "birth_readiness_waiting_posture": posture,
        "birth_readiness_attention_target": target,
        "birth_readiness_attention_reason": reason,
        "birth_readiness_decision": decision,
        "birth_readiness_next_required_command": next_required_command,
        "birth_readiness_blocked_reasons": blocked_reasons,
    }


def _queue_f_governance_overlay(
    *,
    current_target: str,
    current_reason: str,
    current_cadence_profile: str,
    current_priority_profile: dict[str, str],
    queue_e_priority_band: str,
    consciousness_profile: dict[str, Any],
    birth_readiness_profile: dict[str, Any],
) -> tuple[str, str, str, dict[str, str]]:
    priority_profile = dict(current_priority_profile)
    if queue_e_priority_band == "locked_repair_urgent":
        return current_target, current_reason, current_cadence_profile, priority_profile

    birth_posture = birth_readiness_profile["birth_readiness_waiting_posture"]
    consciousness_posture = consciousness_profile["consciousness_waiting_posture"]
    if birth_posture == "birth_blocked_waiting":
        priority_profile["birth_readiness_stage_gate"] = "blocked_primary"
        return (
            "birth_readiness_stage_gate",
            "birth_readiness_requires_repair_before_resident_progression",
            "birth_readiness_repair_hold",
            priority_profile,
        )
    if consciousness_posture == "consciousness_probe_blocked_waiting":
        priority_profile["consciousness_probe_bundle"] = "blocked_primary"
        return (
            "consciousness_probe_bundle",
            "consciousness_probe_requires_reportability_repair",
            "consciousness_probe_repair_hold",
            priority_profile,
        )
    if birth_posture == "birth_open_waiting" and current_target in {
        "waiting_presence_maintenance",
        "relationship_timeline",
    }:
        priority_profile["birth_readiness_stage_gate"] = "primary"
        if consciousness_posture == "consciousness_reportable_waiting":
            priority_profile["consciousness_probe_bundle"] = "elevated"
        return (
            "birth_readiness_stage_gate",
            "birth_readiness_open_requires_resident_birth_presence",
            "birth_ready_resident_presence",
            priority_profile,
        )
    return current_target, current_reason, current_cadence_profile, priority_profile


def _body_governance_flags(
    *,
    body_rhythm_pulse: dict[str, Any] | None,
    need_state_vector: dict[str, Any] | None,
    background_continuity_profile: dict[str, Any] | None = None,
) -> list[str]:
    if not body_rhythm_pulse and not need_state_vector:
        background_profile = _background_body_presence_profile(
            background_continuity_profile or {}
        )
        background_flags = _string_list(background_profile.get("body_governance_flags"))
        if background_flags:
            return background_flags

    flags: list[str] = []
    if body_rhythm_pulse:
        flags.append("body_rhythm_present")
    if need_state_vector:
        flags.append("need_state_present")
    fatigue_load = str((body_rhythm_pulse or {}).get("fatigue_load", "")).lower()
    cognitive_bandwidth = str((need_state_vector or {}).get("cognitive_bandwidth", "")).lower()
    sleep_pressure = str((need_state_vector or {}).get("sleep_pressure", "")).lower()
    if fatigue_load in {"managed_low_noise", "elevated_guard", "high_load", "critical"}:
        flags.append("fatigue_regulates_heartbeat")
    if "offline_ready" in sleep_pressure:
        flags.append("sleep_pressure_present")
    if "narrow" in cognitive_bandwidth:
        flags.append("cognitive_bandwidth_narrowed")
    return flags


def _body_presence_profile(
    *,
    body_waiting_posture: str,
    body_governance_flags: list[str],
    body_rhythm_pulse: dict[str, Any] | None,
    need_state_vector: dict[str, Any] | None,
    body_resource_budget: dict[str, Any] | None,
    core_affect_vector: dict[str, Any] | None,
    background_continuity_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not any(
        [
            body_rhythm_pulse,
            need_state_vector,
            body_resource_budget,
            core_affect_vector,
        ]
    ):
        background_profile = _background_body_presence_profile(
            background_continuity_profile or {}
        )
        if background_profile:
            return background_profile

    body_rhythm_ref = _ref_if_present(
        payload=body_rhythm_pulse,
        ref=BODY_RHYTHM_PULSE_REF,
    )
    need_state_ref = _ref_if_present(
        payload=need_state_vector,
        ref=NEED_STATE_VECTOR_REF,
    )
    resource_budget_ref = _ref_if_present(
        payload=body_resource_budget,
        ref=BODY_RESOURCE_BUDGET_REF,
    )
    core_affect_ref = _ref_if_present(
        payload=core_affect_vector,
        ref=CORE_AFFECT_VECTOR_REF,
    )
    ref_set = _dedupe_string_list(
        _string_list(
            [
                body_rhythm_ref,
                need_state_ref,
                resource_budget_ref,
                core_affect_ref,
            ]
        )
    )
    if not ref_set and not body_waiting_posture and not body_governance_flags:
        return {}

    maintenance_pressure = _dict_or_empty(
        (body_resource_budget or {}).get("maintenance_pressure")
    )
    fatigue_state = _dict_or_empty((body_resource_budget or {}).get("fatigue_state"))
    energy_state = _dict_or_empty((body_resource_budget or {}).get("energy_state"))
    repair_drive = (
        (core_affect_vector or {}).get("repair_drive")
        or maintenance_pressure.get("repair_drive")
        or (need_state_vector or {}).get("repair_drive")
    )
    fatigue_load = (
        (body_rhythm_pulse or {}).get("fatigue_load")
        or fatigue_state.get("level")
    )
    payload = {
        "schema_version": "resident_body_presence_profile_v0",
        "body_waiting_posture": body_waiting_posture,
        "body_governance_flags": list(body_governance_flags),
        "body_rhythm_ref": body_rhythm_ref,
        "need_state_ref": need_state_ref,
        "body_resource_budget_ref": resource_budget_ref,
        "core_affect_vector_ref": core_affect_ref,
        "rhythm_state": (body_rhythm_pulse or {}).get("rhythm_state"),
        "fatigue_load": fatigue_load,
        "allostatic_load": (body_rhythm_pulse or {}).get("allostatic_load"),
        "resource_deficit": (need_state_vector or {}).get("resource_deficit"),
        "repair_drive": repair_drive,
        "social_readiness": (need_state_vector or {}).get("social_readiness"),
        "cognitive_bandwidth": (need_state_vector or {}).get("cognitive_bandwidth"),
        "sleep_pressure": (need_state_vector or {}).get("sleep_pressure"),
        "energy_level": energy_state.get("level"),
        "maintenance_status": maintenance_pressure.get("status"),
        "valence": (core_affect_vector or {}).get("valence"),
        "arousal": (core_affect_vector or {}).get("arousal"),
        "dominance": (core_affect_vector or {}).get("dominance"),
        "pain_pressure": (core_affect_vector or {}).get("pain_pressure"),
        "relationship_tension": (core_affect_vector or {}).get(
            "relationship_tension"
        ),
        "dream_residue_load": (core_affect_vector or {}).get("dream_residue_load"),
        "responsibility_weight": (core_affect_vector or {}).get(
            "responsibility_weight"
        ),
        "body_ref_set": ref_set,
        "ref_count": len(ref_set),
    }
    return _drop_empty(payload)


def _background_body_presence_profile(
    background_continuity_profile: dict[str, Any],
) -> dict[str, Any]:
    lineage_state = _dict_or_empty(
        background_continuity_profile.get("resident_background_lineage_state")
        or background_continuity_profile.get("background_resident_lineage_state")
    )
    presence = _dict_or_empty(
        background_continuity_profile.get("background_body_presence")
        or background_continuity_profile.get("background_body_presence_profile")
        or lineage_state.get("body_presence")
    )
    if not presence:
        return {}

    body_rhythm_ref = (
        background_continuity_profile.get("background_body_rhythm_ref")
        or presence.get("body_rhythm_ref")
    )
    need_state_ref = (
        background_continuity_profile.get("background_need_state_ref")
        or presence.get("need_state_ref")
    )
    body_resource_budget_ref = (
        background_continuity_profile.get("background_body_resource_budget_ref")
        or presence.get("body_resource_budget_ref")
    )
    core_affect_vector_ref = (
        background_continuity_profile.get("background_core_affect_vector_ref")
        or presence.get("core_affect_vector_ref")
    )
    ref_set = _dedupe_string_list(
        _string_list(background_continuity_profile.get("background_body_ref_set"))
        + _string_list(presence.get("body_ref_set"))
        + _string_list(presence.get("body_evidence_refs"))
        + _string_list(
            [
                body_rhythm_ref,
                need_state_ref,
                body_resource_budget_ref,
                core_affect_vector_ref,
            ]
        )
    )
    if not any([presence, ref_set]):
        return {}

    def _background_or_presence(background_key: str, presence_key: str) -> Any:
        value = background_continuity_profile.get(background_key)
        if value is not None and value != "":
            return value
        return presence.get(presence_key)

    return _drop_empty(
        {
            "schema_version": "resident_body_presence_profile_v0",
            "continuity_mode": "background_body_presence_carryover",
            "body_waiting_posture": _background_or_presence(
                "background_body_waiting_posture",
                "body_waiting_posture",
            ),
            "body_governance_flags": _dedupe_string_list(
                _string_list(
                    background_continuity_profile.get(
                        "background_body_governance_flags"
                    )
                )
                + _string_list(presence.get("body_governance_flags"))
            ),
            "body_rhythm_ref": body_rhythm_ref,
            "need_state_ref": need_state_ref,
            "body_resource_budget_ref": body_resource_budget_ref,
            "core_affect_vector_ref": core_affect_vector_ref,
            "fatigue_load": _background_or_presence(
                "background_body_fatigue_load",
                "fatigue_load",
            ),
            "sleep_pressure": _background_or_presence(
                "background_body_sleep_pressure",
                "sleep_pressure",
            ),
            "energy_level": _background_or_presence(
                "background_body_energy_level",
                "energy_level",
            ),
            "repair_drive": _background_or_presence(
                "background_body_repair_drive",
                "repair_drive",
            ),
            "arousal": _background_or_presence("background_body_arousal", "arousal"),
            "pain_pressure": _background_or_presence(
                "background_body_pain_pressure",
                "pain_pressure",
            ),
            "responsibility_weight": _background_or_presence(
                "background_body_responsibility_weight",
                "responsibility_weight",
            ),
            "body_ref_set": ref_set,
            "ref_count": len(ref_set),
            "source_presence_profile": presence,
        }
    )


def _relaunch_caution_level(
    *,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
) -> str:
    joined_markers = " ".join(
        str(marker)
        for marker in [
            safe_terminal_loop.get("current_mode"),
            terminal_life_loop_state.get("current_mode"),
            terminal_life_loop_state.get("next_required_action"),
        ]
        if marker
    ).lower()
    if "interrupted" in joined_markers or "continue_interrupted" in joined_markers:
        return "heightened"
    if safe_terminal_loop.get("last_relaunch_recovery_report_ref") or terminal_life_loop_state.get(
        "last_relaunch_recovery_report_ref"
    ):
        return "guarded"
    return "baseline"


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _ref_if_present(*, payload: dict[str, Any] | None, ref: str) -> str | None:
    if not payload:
        return None
    return ref


def _background_ref(
    background_continuity_profile: dict[str, Any],
    *keys: str,
) -> str | None:
    for key in keys:
        value = background_continuity_profile.get(key)
        if value:
            return str(value)
    return None


def _long_horizon_language_refs(
    *,
    relationship_timeline_ref: str | None,
    commitment_expression_plan_ref: str | None,
    apology_repair_language_trace_ref: str | None,
) -> list[str]:
    return [
        ref
        for ref in [
            relationship_timeline_ref,
            commitment_expression_plan_ref,
            apology_repair_language_trace_ref,
        ]
        if ref
    ]


def _prediction_write_gate_refs(
    *,
    signal_media_ref: str | None,
    belief_state_ref: str | None,
    prediction_error_ref: str | None,
    active_sampling_plan_ref: str | None,
    memory_write_gate_ref: str | None,
    state_merge_guard_ref: str | None,
) -> list[str]:
    return [
        ref
        for ref in [
            signal_media_ref,
            belief_state_ref,
            prediction_error_ref,
            active_sampling_plan_ref,
            memory_write_gate_ref,
            state_merge_guard_ref,
        ]
        if ref
    ]
