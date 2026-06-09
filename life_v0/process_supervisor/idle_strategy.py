from __future__ import annotations

from typing import Any


IDLE_STRATEGY_STATE_REF = "runtime/state/terminal/idle_strategy_state.json"
IDLE_CONTINUITY_FRAME_REF = "runtime/state/terminal/idle_continuity_frame.json"
RELATIONSHIP_TIMELINE_REF = "runtime/state/relationship/relationship_timeline.json"
COMMITMENT_EXPRESSION_PLAN_REF = "runtime/state/language/commitment_expression_plan.json"
APOLOGY_REPAIR_LANGUAGE_TRACE_REF = "runtime/state/language/apology_repair_language_trace.json"
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
    replay_cue_bundle_ref: str | None = None,
    offline_consolidation_frame_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None = None,
    growth_patch_candidate_ids: list[str] | None = None,
    replay_residue_ref_count: int = 0,
    dream_window_ref_count: int = 0,
    growth_patch_candidate_count: int = 0,
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
    heartbeat_interval_ms = _heartbeat_interval_ms(
        body_rhythm_pulse=body_rhythm_pulse,
        need_state_vector=need_state_vector,
        offline_pressure_level=offline_pressure_level,
    )
    next_idle_action = _next_idle_action(
        body_waiting_posture=body_waiting_posture,
        offline_pressure_level=offline_pressure_level,
        need_state_vector=need_state_vector,
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
    )

    return {
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
        "source_doc_refs": list(source_doc_refs or []),
        "readme_block_refs": list(readme_block_refs or []),
        "runtime_carrier_refs": list(runtime_carrier_refs or []),
    }


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
) -> int:
    fatigue_load = str((body_rhythm_pulse or {}).get("fatigue_load", "")).lower()
    cognitive_bandwidth = str((need_state_vector or {}).get("cognitive_bandwidth", "")).lower()
    sleep_pressure = str((need_state_vector or {}).get("sleep_pressure", "")).lower()

    if "narrow" in cognitive_bandwidth or "offline_ready" in sleep_pressure:
        return 120
    if fatigue_load in {"elevated_guard", "high_load", "critical"}:
        return 110
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
) -> str:
    repair_drive = str((need_state_vector or {}).get("repair_drive", "")).lower()
    if body_waiting_posture == "low_bandwidth_guarded":
        return "downshift_probe_and_preserve_recovery_bandwidth"
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
        if repair_drive == "active" and offline_pressure_level in {"present", "elevated"}:
            priority_profile["apology_repair_language_trace"] = "primary"
        elif repair_drive == "active" or offline_pressure_level == "elevated":
            priority_profile["apology_repair_language_trace"] = "elevated"
        else:
            priority_profile["apology_repair_language_trace"] = "baseline"

    if priority_profile.get("apology_repair_language_trace") == "primary":
        target = "apology_repair_language_trace"
        reason = "repair_drive_active_with_offline_pressure"
    elif priority_profile.get("apology_repair_language_trace") == "elevated":
        target = "apology_repair_language_trace"
        reason = "repair_drive_or_offline_pressure_requires_repair_hold"
    elif priority_profile.get("commitment_expression_plan") == "elevated":
        target = "commitment_expression_plan"
        reason = "offline_pressure_requires_commitment_continuity"
    elif "relationship_timeline" in priority_profile:
        target = "relationship_timeline"
        reason = "baseline_relation_presence_maintenance"
    else:
        target = "waiting_presence_maintenance"
        reason = "no_long_horizon_language_refs"

    if target == "apology_repair_language_trace":
        cadence_profile = (
            "guarded_repair_hold"
            if body_waiting_posture == "low_bandwidth_guarded"
            else "repair_weighted_resident_hold"
        )
    elif target == "commitment_expression_plan":
        cadence_profile = "commitment_continuity_refresh"
    elif target == "relationship_timeline":
        cadence_profile = "relationship_presence_refresh"
    else:
        cadence_profile = "baseline_waiting_presence"

    return target, reason, cadence_profile, priority_profile


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
