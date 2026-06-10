from __future__ import annotations

from typing import Any

from life_v0.membrane.queue_e_signals import derive_queue_e_signal_profile
from .offline_learning_signals import derive_offline_learning_profile


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
WORKSPACE_FRAME_REF = "runtime/state/consciousness/workspace_frame.json"
BROADCAST_FRAME_REF = "runtime/state/consciousness/broadcast_frame.json"
METACOGNITION_STATE_REF = "runtime/state/consciousness/metacognition_state.json"
CONSCIOUSNESS_PROBE_REF = "runtime/state/consciousness/consciousness_probe_bundle.json"
BIRTH_READINESS_ROLLUP_REF = "runtime/state/life_targets/birth_readiness_rollup.json"
BIRTH_READINESS_STAGE_GATE_REF = "runtime/state/life_targets/birth_readiness_stage_gate.json"
IDLE_GOVERNANCE_FIELD_NAMES = (
    "heartbeat_interval_ms",
    "idle_probe_mode",
    "offline_pressure_level",
    "relaunch_caution_level",
    "next_idle_action",
    "waiting_mode",
    "body_waiting_posture",
    "body_governance_flags",
    "body_rhythm_ref",
    "need_state_ref",
    "governance_attention_target",
    "governance_attention_reason",
    "governance_cadence_profile",
    "long_horizon_priority_profile",
    "relationship_timeline_ref",
    "commitment_expression_plan_ref",
    "apology_repair_language_trace_ref",
    "long_horizon_language_refs",
    "world_contact_release_posture",
    "repair_followup_required",
    "repair_obligation_count",
    "regret_pressure_count",
    "queue_e_priority_band",
    "nightmare_risk_ref",
    "belief_learning_plan_ref",
    "language_learning_plan_ref",
    "relationship_learning_plan_ref",
    "offline_learning_pressure_level",
    "offline_learning_attention_target",
    "offline_learning_priority_profile",
    "offline_learning_ref_set",
    "background_continuity_mode",
    "background_carryover_pressure_level",
    "background_carryover_attention_target",
    "background_carryover_priority_profile",
    "background_carryover_generation",
    "background_carryover_parent_run_id",
    "background_carryover_source_ref_set",
    "background_continuity_ref_set",
    "background_resident_governance_state_ref",
    "background_resident_governance_snapshot_ref",
    "background_resident_governance_report_ref",
    "background_persistent_process_report_ref",
    "background_waiting_mode",
    "background_relationship_subject_ref",
    "background_relationship_stage",
    "background_relationship_stage_reason",
    "background_self_model_ref",
    "background_trait_drift_monitor_ref",
    "background_trait_slow_variable_summary",
    "background_resume_summary",
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
    replay_cue_bundle: dict[str, Any] | None,
    offline_consolidation_frame: dict[str, Any] | None,
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
    replay_cue_bundle_ref: str | None = None,
    offline_consolidation_frame_ref: str | None = None,
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
    life_constraint_profile = _life_constraint_waiting_profile(
        schema_cross_file_logic=schema_cross_file_logic,
        schema_run_manifest=schema_run_manifest,
    )
    consciousness_profile = _consciousness_waiting_profile(
        workspace_frame=workspace_frame,
        broadcast_frame=broadcast_frame,
        metacognition_state=metacognition_state,
        consciousness_probe=consciousness_probe,
    )
    birth_readiness_profile = _birth_readiness_waiting_profile(
        birth_readiness_rollup=birth_readiness_rollup,
        birth_readiness_stage_gate=birth_readiness_stage_gate,
    )
    offline_learning_profile = derive_offline_learning_profile(
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    background_continuity_profile = dict(background_continuity_profile or {})
    heartbeat_interval_ms = _heartbeat_interval_ms(
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        offline_pressure_level=offline_pressure_level,
        queue_e_priority_band=queue_e_priority_band,
        offline_learning_pressure_level=offline_learning_profile["offline_learning_pressure_level"],
        prediction_waiting_posture=prediction_profile["prediction_waiting_posture"],
        consciousness_waiting_posture=consciousness_profile["consciousness_waiting_posture"],
        birth_readiness_waiting_posture=birth_readiness_profile[
            "birth_readiness_waiting_posture"
        ],
        background_carryover_pressure_level=background_continuity_profile.get(
            "background_carryover_pressure_level"
        ),
        background_carryover_generation=_int_or_zero(
            background_continuity_profile.get("background_carryover_generation")
        ),
    )
    next_idle_action = _next_idle_action(
        body_waiting_posture=body_waiting_posture,
        offline_pressure_level=offline_pressure_level,
        need_state_vector=need_state_vector,
        repair_followup_required=repair_followup_required,
        queue_e_priority_band=queue_e_priority_band,
        offline_learning_pressure_level=offline_learning_profile["offline_learning_pressure_level"],
        prediction_waiting_posture=prediction_profile["prediction_waiting_posture"],
        consciousness_waiting_posture=consciousness_profile["consciousness_waiting_posture"],
        birth_readiness_waiting_posture=birth_readiness_profile[
            "birth_readiness_waiting_posture"
        ],
        background_carryover_pressure_level=background_continuity_profile.get(
            "background_carryover_pressure_level"
        ),
        background_carryover_generation=_int_or_zero(
            background_continuity_profile.get("background_carryover_generation")
        ),
    )
    relaunch_caution_level = _relaunch_caution_level(
        safe_terminal_loop=safe_terminal_loop,
        terminal_life_loop_state=terminal_life_loop_state,
    )
    body_governance_flags = _body_governance_flags(
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
    )
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
    )
    schema_run_manifest_runtime_ref = _ref_if_present(
        payload=schema_run_manifest,
        ref=schema_run_manifest_ref or SCHEMA_RUN_MANIFEST_REF,
    )
    workspace_frame_runtime_ref = _ref_if_present(
        payload=workspace_frame,
        ref=workspace_frame_ref or WORKSPACE_FRAME_REF,
    )
    broadcast_frame_runtime_ref = _ref_if_present(
        payload=broadcast_frame,
        ref=broadcast_frame_ref or BROADCAST_FRAME_REF,
    )
    metacognition_runtime_ref = _ref_if_present(
        payload=metacognition_state,
        ref=metacognition_state_ref or METACOGNITION_STATE_REF,
    )
    consciousness_probe_runtime_ref = _ref_if_present(
        payload=consciousness_probe,
        ref=consciousness_probe_ref or CONSCIOUSNESS_PROBE_REF,
    )
    birth_readiness_rollup_runtime_ref = _ref_if_present(
        payload=birth_readiness_rollup,
        ref=birth_readiness_rollup_ref or BIRTH_READINESS_ROLLUP_REF,
    )
    birth_readiness_stage_gate_runtime_ref = _ref_if_present(
        payload=birth_readiness_stage_gate,
        ref=birth_readiness_stage_gate_ref or BIRTH_READINESS_STAGE_GATE_REF,
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
        background_carryover_attention_target=background_continuity_profile.get(
            "background_carryover_attention_target"
        ),
        background_carryover_generation=_int_or_zero(
            background_continuity_profile.get("background_carryover_generation")
        ),
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

    payload = {
        "schema_version": "idle_strategy_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "strategy_id": f"idle-strategy-{run_id}-{heartbeat_counter:04d}",
        "heartbeat_counter": heartbeat_counter,
        "heartbeat_interval_ms": heartbeat_interval_ms,
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
        "body_rhythm_ref": (
            "runtime/state/body/body_rhythm_pulse.json" if body_rhythm_pulse else None
        ),
        "need_state_ref": (
            "runtime/state/body/need_state_vector.json" if need_state_vector else None
        ),
        "governance_attention_target": governance_attention_target,
        "governance_attention_reason": governance_attention_reason,
        "governance_cadence_profile": governance_cadence_profile,
        "long_horizon_priority_profile": long_horizon_priority_profile,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "long_horizon_language_refs": long_horizon_refs,
        "world_contact_release_posture": world_contact_release_posture,
        "repair_followup_required": repair_followup_required,
        "repair_obligation_count": repair_obligation_count,
        "regret_pressure_count": regret_pressure_count,
        "queue_e_priority_band": queue_e_priority_band,
        "nightmare_risk_ref": nightmare_risk_ref if nightmare_risk else None,
        "belief_learning_plan_ref": belief_learning_plan_ref if belief_learning_plan else None,
        "language_learning_plan_ref": language_learning_plan_ref if language_learning_plan else None,
        "relationship_learning_plan_ref": (
            relationship_learning_plan_ref if relationship_learning_plan else None
        ),
        "offline_learning_pressure_level": offline_learning_profile["offline_learning_pressure_level"],
        "offline_learning_attention_target": offline_learning_profile["offline_learning_attention_target"],
        "offline_learning_priority_profile": offline_learning_profile["offline_learning_priority_profile"],
        "offline_learning_ref_set": offline_learning_profile["offline_learning_ref_set"],
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
        "schema_cross_file_logic_ref": schema_cross_file_logic_runtime_ref,
        "schema_run_manifest_ref": schema_run_manifest_runtime_ref,
        "life_constraint_refs": life_constraint_profile["life_constraint_refs"],
        "queue_e_cross_layer_gate_status": life_constraint_profile[
            "queue_e_cross_layer_gate_status"
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
    return payload


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
) -> str:
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
    if offline_learning_pressure_level == "urgent":
        return 58
    if birth_readiness_waiting_posture == "birth_open_waiting":
        return 44
    if (
        background_carryover_generation >= 3
        and background_carryover_pressure_level in {"present", "elevated"}
        and offline_pressure_level == "quiet"
    ):
        return 52
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
    if offline_learning_pressure_level == "urgent":
        return "refresh_waiting_heartbeat_with_offline_learning_hold"
    if birth_readiness_waiting_posture == "birth_open_waiting":
        return "refresh_waiting_heartbeat_with_birth_ready_presence_hold"
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
    elif "relationship_timeline" in priority_profile:
        target = "relationship_timeline"
        reason = "baseline_relation_presence_maintenance"
    elif background_carryover_attention_target:
        target = background_carryover_attention_target
        if background_carryover_generation >= 2:
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
        if background_carryover_generation >= 2:
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


def _life_constraint_waiting_profile(
    *,
    schema_cross_file_logic: dict[str, Any] | None,
    schema_run_manifest: dict[str, Any] | None,
) -> dict[str, Any]:
    cross_file_logic = schema_cross_file_logic or {}
    run_manifest = schema_run_manifest or {}
    gate_status = dict(
        cross_file_logic.get("queue_e_cross_layer_gate_status")
        or run_manifest.get("queue_e_cross_layer_gate_status")
        or {}
    )
    refs = list(
        dict.fromkeys(
            [
                *list(cross_file_logic.get("life_constraint_refs", [])),
                *list(run_manifest.get("queue_e_cross_layer_refs", [])),
            ]
        )
    )
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


def _consciousness_waiting_profile(
    *,
    workspace_frame: dict[str, Any] | None,
    broadcast_frame: dict[str, Any] | None,
    metacognition_state: dict[str, Any] | None,
    consciousness_probe: dict[str, Any] | None,
) -> dict[str, Any]:
    has_objects = any([workspace_frame, broadcast_frame, metacognition_state, consciousness_probe])
    flags = list((consciousness_probe or {}).get("reportability_flags", []))
    blocking_flags = {
        flag
        for flag in flags
        if str(flag).endswith("_missing") or str(flag).endswith("_minimal")
    }
    if not has_objects:
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
) -> dict[str, Any]:
    rollup = birth_readiness_rollup or {}
    stage_gate = birth_readiness_stage_gate or {}
    overall_status = str(rollup.get("overall_status", ""))
    decision = str(stage_gate.get("decision", ""))
    blocked_reasons = list(rollup.get("blocked_reasons", [])) + list(
        stage_gate.get("blocked_reasons", [])
    )

    if not rollup and not stage_gate:
        posture = "birth_unobserved_waiting"
        target = "waiting_presence_maintenance"
        reason = "birth_readiness_objects_absent"
    elif decision == "open" and overall_status == "open":
        posture = "birth_open_waiting"
        target = "birth_readiness_stage_gate"
        reason = "birth_readiness_open_requires_resident_birth_presence"
    else:
        posture = "birth_blocked_waiting"
        target = "birth_readiness_repair"
        reason = "birth_readiness_gate_not_open"

    return {
        "birth_readiness_waiting_posture": posture,
        "birth_readiness_attention_target": target,
        "birth_readiness_attention_reason": reason,
        "birth_readiness_decision": decision,
        "birth_readiness_next_required_command": stage_gate.get("next_required_command", ""),
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
) -> list[str]:
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
