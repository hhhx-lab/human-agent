from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from life_v0.membrane.queue_e_signals import build_queue_e_repair_modulation_profile

from .governance_explanation import (
    RESIDENT_GOVERNANCE_EXPLANATION_REF,
    write_resident_governance_explanation,
)
from .handoff_profile import HANDOFF_CARRY_FIELD_NAMES
from .idle_strategy import (
    BODY_RESOURCE_BUDGET_REF,
    BODY_RHYTHM_PULSE_REF,
    CORE_AFFECT_VECTOR_REF,
    NEED_STATE_VECTOR_REF,
    extract_idle_governance_fields,
)
from .model_expression import MODEL_EXPRESSION_REPORT_REF, MODEL_EXPRESSION_STATE_REF
from .proactive_terminal_voice import (
    PROACTIVE_TERMINAL_EVENTS_REF,
    PROACTIVE_TERMINAL_STATE_REF,
)
from .resident_autonomous_activity import (
    ACTIVITY_STATE_REFS,
    RESIDENT_AUTONOMOUS_ACTIVITY_REF,
    RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF,
)
from .state_merge_signals import state_merge_long_term_change_profile
from .trait_convergence_signals import cross_wake_trait_convergence_profile


STATE_MERGE_GUARD_REF = "runtime/state/memory/state_merge_guard.json"
RESIDENT_PROCESS_LEASE_REF = "runtime/state/terminal/resident_process_lease.json"
RESIDENT_PROCESS_LEASE_HISTORY_REF = "runtime/state/terminal/resident_process_lease_history.jsonl"
RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF = (
    "runtime/state/terminal/resident_process_lease_history_profile.json"
)


@dataclass(frozen=True)
class ProcessReportBundleResult:
    report: dict[str, Any]
    digest: dict[str, Any]
    receipt: dict[str, Any]


def write_process_report_bundle(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    completed_turns: int,
    incident_count: int,
    relaunch_recovery_count: int,
    heartbeat_counter: int,
    exit_reason: str,
    last_incident_report_ref: str | None,
    last_recovery_report_ref: str | None,
    last_relaunch_recovery_report_ref: str | None,
    last_external_turn: dict[str, Any] | None,
    last_life_turn: dict[str, Any] | None,
    idle_strategy_ref: str | None,
    idle_strategy_state: dict[str, Any] | None,
    persistent_process_report_ref: str | None,
    resident_governance_report_ref: str | None,
    resident_governance_state_ref: str | None,
    resident_governance_snapshot_ref: str | None,
    life_context_frame_ref: str | None,
    relation_turn_frame_ref: str | None,
    expression_plan_ref: str | None,
    relationship_timeline_ref: str | None,
    commitment_expression_plan_ref: str | None,
    apology_repair_language_trace_ref: str | None,
    dialogue_writeback_bundle_ref: str | None,
    replay_cue_bundle_ref: str | None,
    offline_consolidation_frame_ref: str | None,
    dream_experience_window_ref: str | None = None,
    wake_integration_frame_ref: str | None = None,
    dream_fact_gate_decision_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None,
    nightmare_risk_ref: str | None = None,
    belief_learning_plan_ref: str | None = None,
    language_learning_plan_ref: str | None = None,
    relationship_learning_plan_ref: str | None = None,
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    signal_media_runtime_ref: str | None = None,
    belief_state_ref: str | None = None,
    prediction_error_field_ref: str | None = None,
    active_sampling_plan_ref: str | None = None,
    memory_write_gate_ref: str | None = None,
    state_merge_guard_ref: str | None = None,
    trait_drift_monitor_ref: str | None = None,
    background_convergence_summary_ref: str | None = None,
    background_convergence_history_ref: str | None = None,
    resident_process_lease_ref: str | None = None,
    resident_process_lease_history_ref: str | None = None,
    runtime_config_state_ref: str | None = None,
    runtime_config_report_ref: str | None = None,
    relationship_graph: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> ProcessReportBundleResult:
    idle_governance = extract_idle_governance_fields(idle_strategy_state)
    idle_governance.update(
        cross_wake_trait_convergence_profile(
            _trait_convergence_report_carrier(
                idle_governance=idle_governance,
                resident_governance_state_ref=resident_governance_state_ref,
                trait_drift_monitor_ref=trait_drift_monitor_ref,
                background_convergence_summary_ref=background_convergence_summary_ref,
                background_convergence_history_ref=background_convergence_history_ref,
            )
        )
    )
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    queue_e_repair_modulation_profile = _queue_e_repair_modulation_profile_from_runtime(
        state_dir=state_dir,
        reports_dir=reports_dir,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
    )
    queue_e_repair_ref_set = _list_or_empty(
        queue_e_repair_modulation_profile.get("ref_set")
    )
    identity_consciousness_birth_refs = _identity_consciousness_birth_refs(idle_governance)
    relationship_resume_summary = _relationship_resume_summary(relationship_graph)
    trait_slow_variable_summary = _trait_slow_variable_summary(self_model_state)
    state_merge_guard = _read_json_if_exists(state_dir / "memory" / "state_merge_guard.json")
    state_merge_guard_runtime_ref = state_merge_guard_ref or (
        STATE_MERGE_GUARD_REF if state_merge_guard else None
    )
    state_merge_profile = _state_merge_report_profile(
        state_merge_guard=state_merge_guard,
        state_merge_guard_ref=state_merge_guard_runtime_ref,
    )
    model_expression_state = _read_json_if_exists(
        state_dir / "language" / "model_expression_state.json"
    )
    model_expression_state_ref = (
        MODEL_EXPRESSION_STATE_REF if model_expression_state else None
    )
    model_expression_report_ref = (
        MODEL_EXPRESSION_REPORT_REF
        if (reports_dir / "digital_life_model_expression_report.json").exists()
        else None
    )
    resident_terminal_proactive_state = _read_json_if_exists(
        state_dir / "terminal" / "resident_terminal_proactive_state.json"
    )
    resident_terminal_proactive_state_ref = (
        PROACTIVE_TERMINAL_STATE_REF if resident_terminal_proactive_state else None
    )
    resident_terminal_proactive_events_ref = (
        PROACTIVE_TERMINAL_EVENTS_REF
        if (state_dir / "terminal" / "resident_terminal_proactive_events.jsonl").exists()
        else None
    )
    relationship_offline_learning_context = (
        relationship_resume_summary.get("relationship_stage") == "repair_guarded_continuity"
        and {
            "runtime/state/growth/relationship_learning_plan.json",
            "runtime/state/growth/language_learning_plan.json",
        }.issubset(
            set(state_merge_profile.get("state_merge_long_term_change_refs", []))
        )
    )
    resident_process_lease_ref = resident_process_lease_ref or (
        RESIDENT_PROCESS_LEASE_REF
        if (state_dir / "terminal" / "resident_process_lease.json").exists()
        else None
    )
    resident_process_lease_history_ref = resident_process_lease_history_ref or (
        RESIDENT_PROCESS_LEASE_HISTORY_REF
        if (state_dir / "terminal" / "resident_process_lease_history.jsonl").exists()
        else None
    )
    resident_process_lease_history_profile_ref = (
        RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF
        if (state_dir / "terminal" / "resident_process_lease_history_profile.json").exists()
        else None
    )
    resident_process_lease_history_profile = _read_json_if_exists(
        state_dir / "terminal" / "resident_process_lease_history_profile.json"
    )
    background_offline_learning_presence = _dict_or_empty(
        idle_governance.get("background_offline_learning_presence")
    )
    offline_learning_cumulative_profile = _dict_or_empty(
        idle_governance.get("offline_learning_cumulative_profile")
        or background_offline_learning_presence
    )
    resolved_offline_learning_cumulative_relationship_reconsolidation_required = _bool_or_none(
        _first_non_none(
            idle_governance.get(
                "offline_learning_cumulative_relationship_reconsolidation_required"
            ),
            offline_learning_cumulative_profile.get("relationship_reconsolidation_required"),
            idle_governance.get(
                "background_offline_learning_relationship_reconsolidation_required"
            ),
            background_offline_learning_presence.get("relationship_reconsolidation_required"),
        )
    )
    if not resolved_offline_learning_cumulative_relationship_reconsolidation_required:
        resolved_offline_learning_cumulative_relationship_reconsolidation_required = (
            relationship_offline_learning_context or None
        )
    if resolved_offline_learning_cumulative_relationship_reconsolidation_required:
        resolved_offline_learning_cumulative_integration_mode = (
            "relationship_offline_reconsolidation_required"
        )
    else:
        resolved_offline_learning_cumulative_integration_mode = str(
            _first_non_none(
                idle_governance.get("offline_learning_cumulative_integration_mode"),
                offline_learning_cumulative_profile.get("integration_mode"),
                idle_governance.get("background_offline_learning_integration_mode"),
                background_offline_learning_presence.get("integration_mode"),
            )
            or "quiet"
        )
    resolved_dream_wake_presence_profile = _dict_or_empty(
        idle_governance.get("dream_wake_presence_profile")
        or idle_governance.get("background_dream_wake_presence_profile")
    )
    resolved_background_dream_wake_presence_profile = _dict_or_empty(
        idle_governance.get("background_dream_wake_presence_profile")
        or resolved_dream_wake_presence_profile
    )
    dream_wake_default_ref_set = _list_or_empty(
        [
            offline_consolidation_frame_ref
            or "runtime/state/dream/offline_consolidation_frame.json",
            dream_experience_window_ref
            or "runtime/state/dream/dream_experience_window.json",
            wake_integration_frame_ref
            or "runtime/state/dream/wake_integration_frame.json",
            dream_fact_gate_decision_ref
            or "runtime/state/dream/dream_fact_gate_decision.json",
        ]
    )
    resolved_dream_wake_ref_set = _dedupe_refs(
        [
            * _list_or_empty(idle_governance.get("dream_wake_ref_set")),
            * _list_or_empty(resolved_dream_wake_presence_profile.get("ref_set")),
            * _list_or_empty(
                resolved_background_dream_wake_presence_profile.get("ref_set")
            ),
            * dream_wake_default_ref_set,
        ]
    )
    resolved_body_presence_profile = _dict_or_empty(
        idle_governance.get("body_presence_profile")
        or idle_governance.get("background_body_presence_profile")
        or idle_governance.get("background_body_presence")
    )
    resolved_background_body_presence_profile = _dict_or_empty(
        idle_governance.get("background_body_presence_profile")
        or idle_governance.get("background_body_presence")
        or resolved_body_presence_profile
    )
    body_presence_visible = bool(
        resolved_body_presence_profile
        or resolved_background_body_presence_profile
        or _list_or_empty(idle_governance.get("body_ref_set"))
        or any(
            idle_governance.get(field_name) is not None
            for field_name in (
                "body_waiting_posture",
                "body_rhythm_ref",
                "need_state_ref",
                "body_resource_budget_ref",
                "core_affect_vector_ref",
                "body_energy_level",
                "body_fatigue_load",
                "body_sleep_pressure",
                "body_repair_drive",
                "body_arousal",
                "body_pain_pressure",
                "body_responsibility_weight",
                "background_body_waiting_posture",
                "background_body_rhythm_ref",
                "background_need_state_ref",
                "background_body_resource_budget_ref",
                "background_core_affect_vector_ref",
                "background_body_energy_level",
                "background_body_fatigue_load",
                "background_body_sleep_pressure",
                "background_body_repair_drive",
                "background_body_arousal",
                "background_body_pain_pressure",
                "background_body_responsibility_weight",
            )
        )
    )
    body_default_ref_set = [
        BODY_RHYTHM_PULSE_REF,
        NEED_STATE_VECTOR_REF,
        BODY_RESOURCE_BUDGET_REF,
        CORE_AFFECT_VECTOR_REF,
    ] if body_presence_visible else []
    resolved_body_ref_set = _dedupe_refs(
        [
            * _list_or_empty(idle_governance.get("body_ref_set")),
            * _list_or_empty(resolved_body_presence_profile.get("body_ref_set")),
            * _list_or_empty(resolved_body_presence_profile.get("body_evidence_refs")),
            * _list_or_empty(resolved_background_body_presence_profile.get("body_ref_set")),
            * _list_or_empty(
                resolved_background_body_presence_profile.get("body_evidence_refs")
            ),
            * _list_or_empty(
                [
                    idle_governance.get("body_rhythm_ref"),
                    idle_governance.get("need_state_ref"),
                    idle_governance.get("body_resource_budget_ref"),
                    idle_governance.get("core_affect_vector_ref"),
                    idle_governance.get("background_body_rhythm_ref"),
                    idle_governance.get("background_need_state_ref"),
                    idle_governance.get("background_body_resource_budget_ref"),
                    idle_governance.get("background_core_affect_vector_ref"),
                    resolved_body_presence_profile.get("body_rhythm_ref"),
                    resolved_body_presence_profile.get("need_state_ref"),
                    resolved_body_presence_profile.get("body_resource_budget_ref"),
                    resolved_body_presence_profile.get("core_affect_vector_ref"),
                    resolved_background_body_presence_profile.get("body_rhythm_ref"),
                    resolved_background_body_presence_profile.get("need_state_ref"),
                    resolved_background_body_presence_profile.get(
                        "body_resource_budget_ref"
                    ),
                    resolved_background_body_presence_profile.get(
                        "core_affect_vector_ref"
                    ),
                ]
            ),
            * body_default_ref_set,
        ]
    )
    if not resolved_body_presence_profile and resolved_body_ref_set:
        resolved_body_presence_profile = {
            "schema_version": "resident_body_presence_profile_v0",
            "continuity_mode": "background_body_presence_carryover",
            "body_ref_set": resolved_body_ref_set,
        }
    elif resolved_body_presence_profile and not resolved_body_presence_profile.get(
        "continuity_mode"
    ):
        resolved_body_presence_profile = dict(resolved_body_presence_profile)
        resolved_body_presence_profile["continuity_mode"] = (
            "background_body_presence_carryover"
        )
    if resolved_body_presence_profile and resolved_body_ref_set:
        resolved_body_presence_profile = dict(resolved_body_presence_profile)
        resolved_body_presence_profile["body_ref_set"] = resolved_body_ref_set
    if not resolved_background_body_presence_profile and resolved_body_presence_profile:
        resolved_background_body_presence_profile = dict(resolved_body_presence_profile)
    elif resolved_background_body_presence_profile and not resolved_background_body_presence_profile.get(
        "continuity_mode"
    ):
        resolved_background_body_presence_profile = dict(
            resolved_background_body_presence_profile
        )
        resolved_background_body_presence_profile["continuity_mode"] = (
            "background_body_presence_carryover"
        )
    if resolved_background_body_presence_profile and resolved_body_ref_set:
        resolved_background_body_presence_profile = dict(
            resolved_background_body_presence_profile
        )
        resolved_background_body_presence_profile["body_ref_set"] = (
            resolved_body_ref_set
        )
    resolved_body_signal_ref_set = _dedupe_refs(
        [
            *_list_or_empty(idle_governance.get("body_signal_refs")),
            *_list_or_empty(idle_governance.get("background_body_signal_refs")),
        ]
    )
    resolved_background_body_signal_write_bias = _first_non_none(
        idle_governance.get("background_body_signal_write_bias"),
        idle_governance.get("body_signal_write_bias"),
    )
    resolved_background_body_signal_candidate_gate_adjustments = _dedupe_refs(
        [
            *_list_or_empty(
                idle_governance.get(
                    "background_body_signal_candidate_gate_adjustments"
                )
            ),
            *_list_or_empty(
                idle_governance.get("body_signal_candidate_gate_adjustments")
            ),
        ]
    )
    resolved_resident_autonomous_activity_presence_profile = _dict_or_empty(
        idle_governance.get("resident_autonomous_activity_presence_profile")
        or idle_governance.get("background_resident_autonomous_activity_presence_profile")
    )
    resolved_background_resident_autonomous_activity_presence_profile = _dict_or_empty(
        idle_governance.get("background_resident_autonomous_activity_presence_profile")
        or resolved_resident_autonomous_activity_presence_profile
    )
    if resolved_dream_wake_presence_profile and not resolved_dream_wake_presence_profile.get(
        "continuity_mode"
    ):
        resolved_dream_wake_presence_profile = dict(resolved_dream_wake_presence_profile)
        resolved_dream_wake_presence_profile["continuity_mode"] = (
            "background_dream_wake_carryover"
        )
    if resolved_background_dream_wake_presence_profile and not resolved_background_dream_wake_presence_profile.get(
        "continuity_mode"
    ):
        resolved_background_dream_wake_presence_profile = dict(
            resolved_background_dream_wake_presence_profile
        )
        resolved_background_dream_wake_presence_profile["continuity_mode"] = (
            "background_dream_wake_carryover"
        )
    background_resident_autonomous_activity_default_ref_set = [
        RESIDENT_AUTONOMOUS_ACTIVITY_REF,
        RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF,
        *ACTIVITY_STATE_REFS.values(),
    ]
    resolved_resident_autonomous_activity_ref = None
    resolved_resident_autonomous_activity_state_ref = None
    resolved_resident_autonomous_activity_ref_set = []
    if not resolved_resident_autonomous_activity_presence_profile:
        resolved_resident_autonomous_activity_presence_profile = {
            "schema_version": "resident_autonomous_activity_presence_profile_v0",
            "continuity_mode": "background_resident_autonomous_activity_carryover",
            "resident_autonomous_activity_ref": RESIDENT_AUTONOMOUS_ACTIVITY_REF,
            "resident_autonomous_activity_state_ref": RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF,
            "activity_state_refs": dict(ACTIVITY_STATE_REFS),
            "ref_set": background_resident_autonomous_activity_default_ref_set,
        }
    elif not resolved_resident_autonomous_activity_presence_profile.get(
        "continuity_mode"
    ):
        resolved_resident_autonomous_activity_presence_profile = dict(
            resolved_resident_autonomous_activity_presence_profile
        )
        resolved_resident_autonomous_activity_presence_profile["continuity_mode"] = (
            "background_resident_autonomous_activity_carryover"
        )
    if not resolved_background_resident_autonomous_activity_presence_profile:
        resolved_background_resident_autonomous_activity_presence_profile = dict(
            resolved_resident_autonomous_activity_presence_profile
        )
    elif not resolved_background_resident_autonomous_activity_presence_profile.get(
        "continuity_mode"
    ):
        resolved_background_resident_autonomous_activity_presence_profile = dict(
            resolved_background_resident_autonomous_activity_presence_profile
        )
        resolved_background_resident_autonomous_activity_presence_profile["continuity_mode"] = (
            "background_resident_autonomous_activity_carryover"
        )
    if not resolved_resident_autonomous_activity_ref:
        resolved_resident_autonomous_activity_ref = RESIDENT_AUTONOMOUS_ACTIVITY_REF
    if not resolved_resident_autonomous_activity_state_ref:
        resolved_resident_autonomous_activity_state_ref = (
            RESIDENT_AUTONOMOUS_ACTIVITY_STATE_REF
        )
    if not resolved_resident_autonomous_activity_ref_set:
        resolved_resident_autonomous_activity_ref_set = (
            background_resident_autonomous_activity_default_ref_set
        )
    resolved_resident_autonomous_activity_ref = _first_non_none(
        idle_governance.get("resident_autonomous_activity_ref"),
        resolved_resident_autonomous_activity_presence_profile.get(
            "resident_autonomous_activity_ref"
        ),
        resolved_background_resident_autonomous_activity_presence_profile.get(
            "resident_autonomous_activity_ref"
        ),
    ) or resolved_resident_autonomous_activity_ref
    resolved_resident_autonomous_activity_state_ref = _first_non_none(
        idle_governance.get("resident_autonomous_activity_state_ref"),
        resolved_resident_autonomous_activity_presence_profile.get(
            "resident_autonomous_activity_state_ref"
        ),
        resolved_background_resident_autonomous_activity_presence_profile.get(
            "resident_autonomous_activity_state_ref"
        ),
    ) or resolved_resident_autonomous_activity_state_ref
    resolved_resident_autonomous_activity_ref_set = _dedupe_refs(
        [
            * _list_or_empty(idle_governance.get("resident_autonomous_activity_ref_set")),
            * _list_or_empty(
                resolved_resident_autonomous_activity_presence_profile.get("ref_set")
            ),
            * _list_or_empty(
                resolved_background_resident_autonomous_activity_presence_profile.get(
                    "ref_set"
                )
            ),
            * background_resident_autonomous_activity_default_ref_set,
        ]
    ) or resolved_resident_autonomous_activity_ref_set
    resolved_autonomous_activity_cycle_phase_index = _first_non_none(
        idle_governance.get("autonomous_activity_cycle_phase_index"),
        resolved_resident_autonomous_activity_presence_profile.get(
            "cycle_phase_index"
        ),
    )
    resolved_autonomous_activity_cycle_phase_count = _first_non_none(
        idle_governance.get("autonomous_activity_cycle_phase_count"),
        resolved_resident_autonomous_activity_presence_profile.get(
            "cycle_phase_count"
        ),
    )
    resolved_autonomous_activity_cycle_completion_count = _first_non_none(
        idle_governance.get("autonomous_activity_cycle_completion_count"),
        resolved_resident_autonomous_activity_presence_profile.get(
            "cycle_completion_count"
        ),
    )
    resolved_autonomous_activity_cycle_coverage_complete = _first_non_none(
        idle_governance.get("autonomous_activity_cycle_coverage_complete"),
        resolved_resident_autonomous_activity_presence_profile.get(
            "cycle_coverage_complete"
        ),
    )
    resolved_autonomous_activity_covered_kinds = (
        _list_or_empty(idle_governance.get("autonomous_activity_covered_kinds"))
        or _list_or_empty(
            resolved_resident_autonomous_activity_presence_profile.get(
                "covered_activity_kinds"
            )
        )
    )
    resolved_autonomous_activity_missing_kinds = (
        _list_or_empty(idle_governance.get("autonomous_activity_missing_kinds"))
        or _list_or_empty(
            resolved_resident_autonomous_activity_presence_profile.get(
                "missing_activity_kinds"
            )
        )
    )
    resolved_next_autonomous_activity_kind = (
        idle_governance.get("next_autonomous_activity_kind")
        or resolved_resident_autonomous_activity_presence_profile.get(
            "next_activity_kind"
        )
    )
    resolved_background_autonomous_activity_cycle_completion_count = _first_non_none(
        idle_governance.get("background_autonomous_activity_cycle_completion_count"),
        resolved_background_resident_autonomous_activity_presence_profile.get(
            "cycle_completion_count"
        ),
    )
    resolved_background_autonomous_activity_cycle_coverage_complete = _first_non_none(
        idle_governance.get("background_autonomous_activity_cycle_coverage_complete"),
        resolved_background_resident_autonomous_activity_presence_profile.get(
            "cycle_coverage_complete"
        ),
    )
    resolved_background_autonomous_activity_covered_kinds = (
        _list_or_empty(
            idle_governance.get("background_autonomous_activity_covered_kinds")
        )
        or _list_or_empty(
            resolved_background_resident_autonomous_activity_presence_profile.get(
                "covered_activity_kinds"
            )
        )
    )
    resolved_background_autonomous_activity_missing_kinds = (
        _list_or_empty(
            idle_governance.get("background_autonomous_activity_missing_kinds")
        )
        or _list_or_empty(
            resolved_background_resident_autonomous_activity_presence_profile.get(
                "missing_activity_kinds"
            )
        )
    )
    resolved_background_next_autonomous_activity_kind = (
        idle_governance.get("background_next_autonomous_activity_kind")
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "next_activity_kind"
        )
    )
    resolved_background_autonomous_activity_cycle_phase_index = _first_non_none(
        idle_governance.get("background_autonomous_activity_cycle_phase_index"),
        resolved_background_resident_autonomous_activity_presence_profile.get(
            "cycle_phase_index"
        ),
    )
    resolved_background_autonomous_activity_cycle_phase_count = _first_non_none(
        idle_governance.get("background_autonomous_activity_cycle_phase_count"),
        resolved_background_resident_autonomous_activity_presence_profile.get(
            "cycle_phase_count"
        ),
    )
    prediction_write_gate_refs = _prediction_write_gate_refs(
        signal_media_runtime_ref=signal_media_runtime_ref,
        belief_state_ref=belief_state_ref,
        prediction_error_field_ref=prediction_error_field_ref,
        active_sampling_plan_ref=active_sampling_plan_ref,
        memory_write_gate_ref=memory_write_gate_ref,
        state_merge_guard_ref=state_merge_guard_runtime_ref,
    )
    exit_dream_next_wake_profile = _exit_dream_next_wake_report_profile(
        state_dir=state_dir,
        idle_governance=idle_governance,
    )
    exit_dream_memory_tier_profile = _exit_dream_memory_tier_report_profile(
        state_dir=state_dir,
    )
    governance_explanation = write_resident_governance_explanation(
        run_id=run_id,
        generated_at=generated_at,
        reports_dir=reports_dir,
        idle_strategy_ref=idle_strategy_ref,
        idle_strategy_state=idle_strategy_state,
        persistent_process_report_ref=persistent_process_report_ref,
        resident_governance_report_ref=resident_governance_report_ref,
        resident_governance_state_ref=resident_governance_state_ref,
        resident_governance_snapshot_ref=resident_governance_snapshot_ref,
        completed_turns=completed_turns,
        incident_count=incident_count,
        relaunch_recovery_count=relaunch_recovery_count,
        exit_reason=exit_reason,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_convergence_summary_ref=background_convergence_summary_ref,
        background_convergence_history_ref=background_convergence_history_ref,
        write_json=write_json,
    )
    report = {
        "schema_version": "digital_life_process_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "engineering_slice_ref": "DIGITAL_LIFE_PROCESS_SUPERVISOR",
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
        "restored_shell_ref": "runtime/reports/latest/digital_life_shell_report.json",
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "heartbeat_counter": heartbeat_counter,
        "last_heartbeat_packet_ref": "runtime/reports/latest/digital_life_waiting_heartbeat.json",
        "last_incident_report_ref": last_incident_report_ref,
        "last_recovery_report_ref": last_recovery_report_ref,
        "last_relaunch_recovery_report_ref": last_relaunch_recovery_report_ref,
        "exit_reason": exit_reason,
        "last_external_turn": last_external_turn,
        "last_life_turn": last_life_turn,
        "idle_strategy_ref": idle_strategy_ref,
        "persistent_process_report_ref": persistent_process_report_ref,
        "resident_governance_report_ref": resident_governance_report_ref,
        "resident_governance_state_ref": resident_governance_state_ref,
        "resident_governance_snapshot_ref": resident_governance_snapshot_ref,
        "resident_governance_explanation_ref": RESIDENT_GOVERNANCE_EXPLANATION_REF,
        "resident_process_lease_ref": resident_process_lease_ref,
        "resident_process_lease_history_ref": resident_process_lease_history_ref,
        "runtime_config_state_ref": runtime_config_state_ref,
        "runtime_config_report_ref": runtime_config_report_ref,
        "model_expression_state_ref": model_expression_state_ref,
        "model_expression_report_ref": model_expression_report_ref,
        "model_expression_status": model_expression_state.get(
            "model_expression_status"
        ),
        "model_expression_applied": (
            model_expression_state.get("model_expression_status")
            == "model_expression_applied"
            if model_expression_state
            else None
        ),
        "model_expression_unreleased_reason": model_expression_state.get(
            "unreleased_reason"
        ),
        "post_expression_gate_status": model_expression_state.get(
            "post_expression_gate_status"
        ),
        "post_expression_gate_unreleased_reason": model_expression_state.get(
            "post_expression_gate_unreleased_reason"
        ),
        "resident_terminal_proactive_state_ref": resident_terminal_proactive_state_ref,
        "resident_terminal_proactive_events_ref": resident_terminal_proactive_events_ref,
        "resident_terminal_proactive_status": resident_terminal_proactive_state.get(
            "status"
        ),
        "resident_terminal_proactive_release_count": resident_terminal_proactive_state.get(
            "release_count"
        ),
        "resident_terminal_proactive_event_count": resident_terminal_proactive_state.get(
            "event_count"
        ),
        "resident_terminal_proactive_last_focus": resident_terminal_proactive_state.get(
            "last_focus"
        ),
        "resident_terminal_proactive_last_surface_kind": (
            resident_terminal_proactive_state.get("last_proactive_voice_surface_kind")
        ),
        "resident_terminal_proactive_last_profile_coverage": (
            resident_terminal_proactive_state.get("last_profile_coverage")
        ),
        "resident_terminal_proactive_active_domain_count": (
            (
                resident_terminal_proactive_state.get("last_profile_coverage") or {}
            ).get("active_domain_count")
        ),
        "resident_terminal_proactive_active_domains": (
            (
                resident_terminal_proactive_state.get("last_profile_coverage") or {}
            ).get("active_domains")
        ),
        "resident_terminal_proactive_utterance_candidate_code_count": (
            resident_terminal_proactive_state.get(
                "last_utterance_candidate_code_count"
            )
        ),
        "resident_terminal_proactive_last_natural_language_released": (
            resident_terminal_proactive_state.get("last_natural_language_released")
        ),
        "resident_terminal_proactive_last_model_expression_status": (
            resident_terminal_proactive_state.get("last_model_expression_status")
        ),
        "resident_terminal_proactive_last_post_expression_gate_status": (
            resident_terminal_proactive_state.get("last_post_expression_gate_status")
        ),
        "resident_process_lease_history_profile_ref": resident_process_lease_history_profile_ref,
        "life_context_frame_ref": life_context_frame_ref,
        "relation_turn_frame_ref": relation_turn_frame_ref,
        "expression_plan_ref": expression_plan_ref,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "dialogue_writeback_bundle_ref": dialogue_writeback_bundle_ref,
        "replay_cue_bundle_ref": replay_cue_bundle_ref,
        "offline_consolidation_frame_ref": offline_consolidation_frame_ref,
        "dream_experience_window_ref": dream_experience_window_ref,
        "wake_integration_frame_ref": wake_integration_frame_ref,
        "dream_fact_gate_decision_ref": dream_fact_gate_decision_ref,
        "growth_patch_candidate_queue_ref": growth_patch_candidate_queue_ref,
        "nightmare_risk_ref": nightmare_risk_ref,
        "belief_learning_plan_ref": belief_learning_plan_ref,
        "language_learning_plan_ref": language_learning_plan_ref,
        "relationship_learning_plan_ref": relationship_learning_plan_ref,
        "signal_media_ref": signal_media_runtime_ref,
        "belief_state_ref": belief_state_ref,
        "prediction_error_ref": prediction_error_field_ref,
        "active_sampling_plan_ref": active_sampling_plan_ref,
        "memory_write_gate_ref": memory_write_gate_ref,
        "state_merge_guard_ref": state_merge_guard_runtime_ref,
        "prediction_write_gate_refs": prediction_write_gate_refs,
        "body_signal_ref_set": resolved_body_signal_ref_set,
        "background_body_signal_refs": resolved_body_signal_ref_set,
        "background_body_signal_write_bias": (
            resolved_background_body_signal_write_bias
        ),
        "background_body_signal_fatigue_load": _first_non_none(
            idle_governance.get("background_body_signal_fatigue_load"),
            idle_governance.get("body_signal_fatigue_load"),
        ),
        "background_body_signal_pain_pressure": _first_non_none(
            idle_governance.get("background_body_signal_pain_pressure"),
            idle_governance.get("body_signal_pain_pressure"),
        ),
        "background_body_signal_dream_residue_load": _first_non_none(
            idle_governance.get("background_body_signal_dream_residue_load"),
            idle_governance.get("body_signal_dream_residue_load"),
        ),
        "background_body_signal_repair_drive": _first_non_none(
            idle_governance.get("background_body_signal_repair_drive"),
            idle_governance.get("body_signal_repair_drive"),
        ),
        "background_body_signal_unexpected_uncertainty": _first_non_none(
            idle_governance.get("background_body_signal_unexpected_uncertainty"),
            idle_governance.get("body_signal_unexpected_uncertainty"),
        ),
        "background_body_signal_ref_count": _first_non_none(
            idle_governance.get("background_body_signal_ref_count"),
            idle_governance.get("body_signal_ref_count"),
            len(resolved_body_signal_ref_set) if resolved_body_signal_ref_set else None,
        ),
        "background_body_signal_candidate_gate_adjustments": (
            resolved_background_body_signal_candidate_gate_adjustments
        ),
        "trait_drift_monitor_ref": trait_drift_monitor_ref,
        "background_convergence_summary_ref": background_convergence_summary_ref,
        "background_convergence_history_ref": background_convergence_history_ref,
        "background_relationship_stage": relationship_resume_summary.get(
            "relationship_stage"
        ),
        "background_relationship_stage_reason": relationship_resume_summary.get(
            "relationship_stage_reason"
        ),
        "background_trait_slow_variable_summary": trait_slow_variable_summary,
        "background_convergence_state": idle_governance.get(
            "background_convergence_state"
        ),
        "background_convergence_pressure_level": idle_governance.get(
            "background_convergence_pressure_level"
        ),
        "background_convergence_attention_target": idle_governance.get(
            "background_convergence_attention_target"
        ),
        "offline_learning_cumulative_integration_mode": (
            resolved_offline_learning_cumulative_integration_mode
        ),
        "offline_learning_cumulative_relationship_reconsolidation_required": (
            resolved_offline_learning_cumulative_relationship_reconsolidation_required
        ),
        "dream_wake_presence_profile": resolved_dream_wake_presence_profile,
        "background_dream_wake_presence_profile": (
            resolved_background_dream_wake_presence_profile
        ),
        "dream_wake_ref_set": resolved_dream_wake_ref_set,
        "body_presence_profile": resolved_body_presence_profile,
        "background_body_presence_profile": (
            resolved_background_body_presence_profile
        ),
        "body_ref_set": resolved_body_ref_set,
        "resident_autonomous_activity_ref": (
            resolved_resident_autonomous_activity_ref
        ),
        "resident_autonomous_activity_state_ref": (
            resolved_resident_autonomous_activity_state_ref
        ),
        "resident_autonomous_activity_presence_profile": (
            resolved_resident_autonomous_activity_presence_profile
        ),
        "resident_autonomous_activity_ref_set": (
            resolved_resident_autonomous_activity_ref_set
        ),
        "autonomous_activity_count": idle_governance.get("autonomous_activity_count")
        if idle_governance.get("autonomous_activity_count") is not None
        else resolved_resident_autonomous_activity_presence_profile.get("activity_count"),
        "autonomous_activity_kind_counts": idle_governance.get(
            "autonomous_activity_kind_counts",
            {},
        )
        or resolved_resident_autonomous_activity_presence_profile.get("activity_kind_counts", {}),
        "last_autonomous_activity_kind": idle_governance.get(
            "last_autonomous_activity_kind"
        )
        or resolved_resident_autonomous_activity_presence_profile.get("last_activity_kind"),
        "last_autonomous_activity_at": idle_governance.get("last_autonomous_activity_at")
        or resolved_resident_autonomous_activity_presence_profile.get("last_activity_at"),
        "last_autonomous_activity_state_ref": idle_governance.get(
            "last_autonomous_activity_state_ref"
        )
        or resolved_resident_autonomous_activity_presence_profile.get("last_activity_state_ref"),
        "resident_autonomous_activity_state_refs": idle_governance.get(
            "resident_autonomous_activity_state_refs",
            {},
        )
        or resolved_resident_autonomous_activity_presence_profile.get("activity_state_refs", {}),
        "autonomous_activity_cycle_phase_index": (
            resolved_autonomous_activity_cycle_phase_index
        ),
        "autonomous_activity_cycle_phase_count": (
            resolved_autonomous_activity_cycle_phase_count
        ),
        "autonomous_activity_cycle_completion_count": (
            resolved_autonomous_activity_cycle_completion_count
        ),
        "autonomous_activity_cycle_coverage_complete": (
            resolved_autonomous_activity_cycle_coverage_complete
        ),
        "autonomous_activity_covered_kinds": (
            resolved_autonomous_activity_covered_kinds
        ),
        "autonomous_activity_missing_kinds": (
            resolved_autonomous_activity_missing_kinds
        ),
        "next_autonomous_activity_kind": resolved_next_autonomous_activity_kind,
        "background_autonomous_activity_presence": idle_governance.get(
            "background_autonomous_activity_presence",
            {},
        ),
        "background_resident_autonomous_activity_presence_profile": (
            resolved_background_resident_autonomous_activity_presence_profile
        ),
        "background_resident_autonomous_activity_ref": idle_governance.get(
            "background_resident_autonomous_activity_ref"
        )
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "resident_autonomous_activity_ref"
        ),
        "background_resident_autonomous_activity_state_ref": idle_governance.get(
            "background_resident_autonomous_activity_state_ref"
        )
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "resident_autonomous_activity_state_ref"
        ),
        "background_resident_autonomous_activity_ref_set": _list_or_empty(
            idle_governance.get("background_resident_autonomous_activity_ref_set")
            or resolved_background_resident_autonomous_activity_presence_profile.get(
                "ref_set"
            )
        ),
        "background_autonomous_activity_count": idle_governance.get(
            "background_autonomous_activity_count"
        )
        if idle_governance.get("background_autonomous_activity_count") is not None
        else resolved_background_resident_autonomous_activity_presence_profile.get(
            "activity_count"
        ),
        "background_autonomous_activity_kind_counts": idle_governance.get(
            "background_autonomous_activity_kind_counts",
            {},
        )
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "activity_kind_counts",
            {},
        ),
        "background_last_autonomous_activity_kind": idle_governance.get(
            "background_last_autonomous_activity_kind"
        )
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "last_activity_kind"
        ),
        "background_last_autonomous_activity_at": idle_governance.get(
            "background_last_autonomous_activity_at"
        )
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "last_activity_at"
        ),
        "background_last_autonomous_activity_state_ref": idle_governance.get(
            "background_last_autonomous_activity_state_ref"
        )
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "last_activity_state_ref"
        ),
        "background_resident_autonomous_activity_state_refs": idle_governance.get(
            "background_resident_autonomous_activity_state_refs",
            {},
        )
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "activity_state_refs",
            {},
        ),
        "background_autonomous_activity_cycle_phase_index": (
            resolved_background_autonomous_activity_cycle_phase_index
        ),
        "background_autonomous_activity_cycle_phase_count": (
            resolved_background_autonomous_activity_cycle_phase_count
        ),
        "background_autonomous_activity_cycle_completion_count": (
            resolved_background_autonomous_activity_cycle_completion_count
        ),
        "background_autonomous_activity_cycle_coverage_complete": (
            resolved_background_autonomous_activity_cycle_coverage_complete
        ),
        "background_autonomous_activity_covered_kinds": (
            resolved_background_autonomous_activity_covered_kinds
        ),
        "background_autonomous_activity_missing_kinds": (
            resolved_background_autonomous_activity_missing_kinds
        ),
        "background_next_autonomous_activity_kind": (
            resolved_background_next_autonomous_activity_kind
        ),
        "next_required_action": "process_closed_waiting_relaunch",
        "blocked_reasons": [],
    }
    if responsibility_loop_state_ref:
        report["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        report["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        report["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        report["membrane_guard_refs"] = membrane_guard_refs
    if queue_e_repair_modulation_profile:
        report["queue_e_repair_modulation_profile"] = queue_e_repair_modulation_profile
        report["queue_e_repair_pressure_level"] = queue_e_repair_modulation_profile.get(
            "pressure_level"
        )
        report["queue_e_repair_attention_target"] = (
            queue_e_repair_modulation_profile.get("attention_target")
        )
        report["queue_e_repair_obligation_count"] = (
            queue_e_repair_modulation_profile.get("repair_obligation_count")
        )
        report["queue_e_regret_pressure_count"] = (
            queue_e_repair_modulation_profile.get("regret_pressure_count")
        )
        report["queue_e_repair_ref_set"] = queue_e_repair_ref_set
    report.update(state_merge_profile)
    report.update(idle_governance)
    report.update(exit_dream_next_wake_profile)
    report.update(exit_dream_memory_tier_profile)
    report["offline_learning_cumulative_integration_mode"] = (
        resolved_offline_learning_cumulative_integration_mode
    )
    report["offline_learning_cumulative_relationship_reconsolidation_required"] = (
        resolved_offline_learning_cumulative_relationship_reconsolidation_required
    )
    report["dream_wake_presence_profile"] = resolved_dream_wake_presence_profile
    report["background_dream_wake_presence_profile"] = (
        resolved_background_dream_wake_presence_profile
    )
    report["dream_wake_ref_set"] = resolved_dream_wake_ref_set
    report["body_presence_profile"] = resolved_body_presence_profile
    report["background_body_presence_profile"] = (
        resolved_background_body_presence_profile
    )
    report["body_ref_set"] = resolved_body_ref_set
    report["resident_autonomous_activity_ref"] = resolved_resident_autonomous_activity_ref
    report["resident_autonomous_activity_state_ref"] = (
        resolved_resident_autonomous_activity_state_ref
    )
    report["resident_autonomous_activity_presence_profile"] = (
        resolved_resident_autonomous_activity_presence_profile
    )
    report["resident_autonomous_activity_ref_set"] = (
        resolved_resident_autonomous_activity_ref_set
    )
    report["autonomous_activity_count"] = (
        idle_governance.get("autonomous_activity_count")
        if idle_governance.get("autonomous_activity_count") is not None
        else resolved_resident_autonomous_activity_presence_profile.get("activity_count")
    )
    report["autonomous_activity_kind_counts"] = (
        idle_governance.get("autonomous_activity_kind_counts", {})
        or resolved_resident_autonomous_activity_presence_profile.get(
            "activity_kind_counts",
            {},
        )
    )
    report["last_autonomous_activity_kind"] = (
        idle_governance.get("last_autonomous_activity_kind")
        or resolved_resident_autonomous_activity_presence_profile.get("last_activity_kind")
    )
    report["last_autonomous_activity_at"] = (
        idle_governance.get("last_autonomous_activity_at")
        or resolved_resident_autonomous_activity_presence_profile.get("last_activity_at")
    )
    report["last_autonomous_activity_state_ref"] = (
        idle_governance.get("last_autonomous_activity_state_ref")
        or resolved_resident_autonomous_activity_presence_profile.get(
            "last_activity_state_ref"
        )
    )
    report["resident_autonomous_activity_state_refs"] = (
        idle_governance.get("resident_autonomous_activity_state_refs", {})
        or resolved_resident_autonomous_activity_presence_profile.get(
            "activity_state_refs",
            {},
        )
    )
    report["autonomous_activity_cycle_phase_index"] = (
        resolved_autonomous_activity_cycle_phase_index
    )
    report["autonomous_activity_cycle_phase_count"] = (
        resolved_autonomous_activity_cycle_phase_count
    )
    report["autonomous_activity_cycle_completion_count"] = (
        resolved_autonomous_activity_cycle_completion_count
    )
    report["autonomous_activity_cycle_coverage_complete"] = (
        resolved_autonomous_activity_cycle_coverage_complete
    )
    report["autonomous_activity_covered_kinds"] = (
        resolved_autonomous_activity_covered_kinds
    )
    report["autonomous_activity_missing_kinds"] = (
        resolved_autonomous_activity_missing_kinds
    )
    report["next_autonomous_activity_kind"] = resolved_next_autonomous_activity_kind
    report["background_resident_autonomous_activity_presence_profile"] = (
        resolved_background_resident_autonomous_activity_presence_profile
    )
    report["background_autonomous_activity_presence"] = (
        idle_governance.get("background_autonomous_activity_presence")
        or resolved_background_resident_autonomous_activity_presence_profile
    )
    report["background_resident_autonomous_activity_ref"] = idle_governance.get(
        "background_resident_autonomous_activity_ref"
    ) or resolved_background_resident_autonomous_activity_presence_profile.get(
        "resident_autonomous_activity_ref"
    )
    report["background_resident_autonomous_activity_state_ref"] = idle_governance.get(
        "background_resident_autonomous_activity_state_ref"
    ) or resolved_background_resident_autonomous_activity_presence_profile.get(
        "resident_autonomous_activity_state_ref"
    )
    report["background_resident_autonomous_activity_ref_set"] = _list_or_empty(
        idle_governance.get("background_resident_autonomous_activity_ref_set")
        or resolved_background_resident_autonomous_activity_presence_profile.get("ref_set")
    )
    report["background_autonomous_activity_count"] = (
        idle_governance.get("background_autonomous_activity_count")
        if idle_governance.get("background_autonomous_activity_count") is not None
        else resolved_background_resident_autonomous_activity_presence_profile.get(
            "activity_count"
        )
    )
    report["background_autonomous_activity_kind_counts"] = (
        idle_governance.get("background_autonomous_activity_kind_counts", {})
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "activity_kind_counts",
            {},
        )
    )
    report["background_last_autonomous_activity_kind"] = (
        idle_governance.get("background_last_autonomous_activity_kind")
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "last_activity_kind"
        )
    )
    report["background_last_autonomous_activity_at"] = (
        idle_governance.get("background_last_autonomous_activity_at")
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "last_activity_at"
        )
    )
    report["background_last_autonomous_activity_state_ref"] = (
        idle_governance.get("background_last_autonomous_activity_state_ref")
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "last_activity_state_ref"
        )
    )
    report["background_resident_autonomous_activity_state_refs"] = (
        idle_governance.get("background_resident_autonomous_activity_state_refs")
        or resolved_background_resident_autonomous_activity_presence_profile.get(
            "activity_state_refs",
            {},
        )
    )
    report["background_autonomous_activity_cycle_phase_index"] = (
        resolved_background_autonomous_activity_cycle_phase_index
    )
    report["background_autonomous_activity_cycle_phase_count"] = (
        resolved_background_autonomous_activity_cycle_phase_count
    )
    report["background_autonomous_activity_cycle_completion_count"] = (
        resolved_background_autonomous_activity_cycle_completion_count
    )
    report["background_autonomous_activity_cycle_coverage_complete"] = (
        resolved_background_autonomous_activity_cycle_coverage_complete
    )
    report["background_autonomous_activity_covered_kinds"] = (
        resolved_background_autonomous_activity_covered_kinds
    )
    report["background_autonomous_activity_missing_kinds"] = (
        resolved_background_autonomous_activity_missing_kinds
    )
    report["background_next_autonomous_activity_kind"] = (
        resolved_background_next_autonomous_activity_kind
    )
    _apply_resident_process_identity_profile(
        report,
        resident_process_lease_history_profile=resident_process_lease_history_profile,
        resident_process_lease_history_profile_ref=resident_process_lease_history_profile_ref,
    )
    digest = {
        "schema_version": "digital_life_process_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "heartbeat_counter": heartbeat_counter,
        "idle_heartbeat_trace_ref": idle_governance.get("idle_heartbeat_trace_ref"),
        "idle_heartbeat_trace_count": idle_governance.get(
            "idle_heartbeat_trace_count"
        ),
        "heartbeat_cadence_driver": idle_governance.get(
            "heartbeat_cadence_driver"
        ),
        "heartbeat_cadence_reason": idle_governance.get(
            "heartbeat_cadence_reason"
        ),
        "heartbeat_cadence_modulators": list(
            idle_governance.get("heartbeat_cadence_modulators", [])
        ),
        "heartbeat_priority_stack_winner": idle_governance.get(
            "heartbeat_priority_stack_winner"
        ),
        "heartbeat_priority_stack_candidates": list(
            idle_governance.get("heartbeat_priority_stack_candidates", [])
        ),
        "heartbeat_priority_stack_evidence_refs": list(
            idle_governance.get("heartbeat_priority_stack_evidence_refs", [])
        ),
        "background_heartbeat_cadence_driver": idle_governance.get(
            "background_heartbeat_cadence_driver"
        ),
        "exit_reason": exit_reason,
        "last_external_turn_utterance": None if last_external_turn is None else last_external_turn["utterance"],
        "dialogue_writeback_bundle_ref": dialogue_writeback_bundle_ref,
        "resident_governance_explanation_ref": RESIDENT_GOVERNANCE_EXPLANATION_REF,
        "resident_governance_driver_family": governance_explanation.report[
            "dominant_driver_family"
        ],
        "resident_governance_next_wake_expectation": governance_explanation.report[
            "next_wake_expectation"
        ],
        "resident_governance_lineage_depth": governance_explanation.report[
            "background_carryover_generation"
        ],
        "resident_process_lease_ref": resident_process_lease_ref,
        "resident_process_lease_history_ref": resident_process_lease_history_ref,
        "runtime_config_state_ref": runtime_config_state_ref,
        "runtime_config_report_ref": runtime_config_report_ref,
        "model_expression_state_ref": model_expression_state_ref,
        "model_expression_report_ref": model_expression_report_ref,
        "model_expression_status": model_expression_state.get(
            "model_expression_status"
        ),
        "post_expression_gate_status": model_expression_state.get(
            "post_expression_gate_status"
        ),
        "resident_terminal_proactive_state_ref": resident_terminal_proactive_state_ref,
        "resident_terminal_proactive_events_ref": resident_terminal_proactive_events_ref,
        "resident_terminal_proactive_status": resident_terminal_proactive_state.get(
            "status"
        ),
        "resident_terminal_proactive_release_count": resident_terminal_proactive_state.get(
            "release_count"
        ),
        "resident_terminal_proactive_event_count": resident_terminal_proactive_state.get(
            "event_count"
        ),
        "resident_terminal_proactive_last_focus": resident_terminal_proactive_state.get(
            "last_focus"
        ),
        "resident_terminal_proactive_last_surface_kind": (
            resident_terminal_proactive_state.get("last_proactive_voice_surface_kind")
        ),
        "resident_terminal_proactive_last_profile_coverage": (
            resident_terminal_proactive_state.get("last_profile_coverage")
        ),
        "resident_terminal_proactive_active_domain_count": (
            (
                resident_terminal_proactive_state.get("last_profile_coverage") or {}
            ).get("active_domain_count")
        ),
        "resident_terminal_proactive_active_domains": (
            (
                resident_terminal_proactive_state.get("last_profile_coverage") or {}
            ).get("active_domains")
        ),
        "resident_terminal_proactive_utterance_candidate_code_count": (
            resident_terminal_proactive_state.get(
                "last_utterance_candidate_code_count"
            )
        ),
        "resident_terminal_proactive_last_natural_language_released": (
            resident_terminal_proactive_state.get("last_natural_language_released")
        ),
        "resident_terminal_proactive_last_model_expression_status": (
            resident_terminal_proactive_state.get("last_model_expression_status")
        ),
        "resident_terminal_proactive_last_post_expression_gate_status": (
            resident_terminal_proactive_state.get("last_post_expression_gate_status")
        ),
        "resident_process_lease_history_profile_ref": resident_process_lease_history_profile_ref,
        "background_lineage_depth_band": idle_governance.get(
            "background_lineage_depth_band"
        ),
        "background_lineage_waiting_posture": idle_governance.get(
            "background_lineage_waiting_posture"
        ),
        "background_lineage_cadence_weight": idle_governance.get(
            "background_lineage_cadence_weight"
        ),
        "background_lineage_evidence_ref_count": idle_governance.get(
            "background_lineage_evidence_ref_count"
        ),
        "cross_wake_trait_convergence_profile": idle_governance.get(
            "cross_wake_trait_convergence_profile",
            {},
        ),
        "cross_wake_trait_convergence_focus": idle_governance.get(
            "cross_wake_trait_convergence_focus"
        ),
        "cross_wake_trait_convergence_pressure": idle_governance.get(
            "cross_wake_trait_convergence_pressure"
        ),
        "cross_wake_trait_convergence_unstable_names": list(
            idle_governance.get("cross_wake_trait_convergence_unstable_names", [])
        ),
        "cross_wake_trait_convergence_stable_names": list(
            idle_governance.get("cross_wake_trait_convergence_stable_names", [])
        ),
        "cross_wake_trait_convergence_score": idle_governance.get(
            "cross_wake_trait_convergence_score"
        ),
        "cross_wake_trait_convergence_refs": list(
            idle_governance.get("cross_wake_trait_convergence_refs", [])
        ),
        "cross_wake_trait_drift_update_mode_summary": idle_governance.get(
            "cross_wake_trait_drift_update_mode_summary",
            {},
        ),
        "cross_wake_trait_drift_recalibration_names": list(
            idle_governance.get("cross_wake_trait_drift_recalibration_names", [])
        ),
        "cross_wake_trait_drift_stabilized_names": list(
            idle_governance.get("cross_wake_trait_drift_stabilized_names", [])
        ),
        "long_horizon_language_refs": [
            ref
            for ref in [
                relationship_timeline_ref,
                commitment_expression_plan_ref,
                apology_repair_language_trace_ref,
            ]
            if ref
        ],
        "offline_growth_cycle_refs": [
            ref
            for ref in [
                replay_cue_bundle_ref,
                offline_consolidation_frame_ref,
                dream_experience_window_ref,
                wake_integration_frame_ref,
                dream_fact_gate_decision_ref,
                growth_patch_candidate_queue_ref,
                nightmare_risk_ref,
                belief_learning_plan_ref,
                language_learning_plan_ref,
                relationship_learning_plan_ref,
            ]
            if ref
        ],
        "offline_learning_cumulative_focus": governance_explanation.report.get(
            "offline_learning_cumulative_focus",
            {},
        ),
        "offline_learning_cumulative_generation": (
            idle_governance.get("offline_learning_cumulative_generation")
        ),
        "offline_learning_cumulative_pressure_level": (
            idle_governance.get("offline_learning_cumulative_pressure_level")
        ),
        "offline_learning_cumulative_attention_target": (
            idle_governance.get("offline_learning_cumulative_attention_target")
        ),
        "offline_learning_cumulative_priority_profile": (
            idle_governance.get("offline_learning_cumulative_priority_profile", {})
        ),
        "offline_learning_cumulative_ref_set": (
            list(idle_governance.get("offline_learning_cumulative_ref_set", []))
        ),
        "offline_learning_cumulative_integration_mode": (
            resolved_offline_learning_cumulative_integration_mode
        ),
        "offline_learning_cumulative_relationship_reconsolidation_required": (
            resolved_offline_learning_cumulative_relationship_reconsolidation_required
        ),
        "dream_wake_presence_profile": resolved_dream_wake_presence_profile,
        "background_dream_wake_presence_profile": (
            resolved_background_dream_wake_presence_profile
        ),
        "dream_wake_ref_set": resolved_dream_wake_ref_set,
        "body_presence_profile": resolved_body_presence_profile,
        "background_body_presence_profile": (
            resolved_background_body_presence_profile
        ),
        "body_ref_set": resolved_body_ref_set,
        "resident_autonomous_activity_ref": (
            resolved_resident_autonomous_activity_ref
        ),
        "resident_autonomous_activity_state_ref": (
            resolved_resident_autonomous_activity_state_ref
        ),
        "resident_autonomous_activity_presence_profile": (
            resolved_resident_autonomous_activity_presence_profile
        ),
        "resident_autonomous_activity_ref_set": (
            resolved_resident_autonomous_activity_ref_set
        ),
        "autonomous_activity_count": (
            idle_governance.get("autonomous_activity_count")
            if idle_governance.get("autonomous_activity_count") is not None
            else resolved_resident_autonomous_activity_presence_profile.get("activity_count")
        ),
        "autonomous_activity_kind_counts": (
            idle_governance.get("autonomous_activity_kind_counts", {})
            or resolved_resident_autonomous_activity_presence_profile.get(
                "activity_kind_counts",
                {},
            )
        ),
        "last_autonomous_activity_kind": (
            idle_governance.get("last_autonomous_activity_kind")
            or resolved_resident_autonomous_activity_presence_profile.get("last_activity_kind")
        ),
        "last_autonomous_activity_at": (
            idle_governance.get("last_autonomous_activity_at")
            or resolved_resident_autonomous_activity_presence_profile.get("last_activity_at")
        ),
        "last_autonomous_activity_state_ref": (
            idle_governance.get("last_autonomous_activity_state_ref")
            or resolved_resident_autonomous_activity_presence_profile.get(
                "last_activity_state_ref"
            )
        ),
        "resident_autonomous_activity_state_refs": (
            idle_governance.get("resident_autonomous_activity_state_refs", {})
            or resolved_resident_autonomous_activity_presence_profile.get(
                "activity_state_refs",
                {},
            )
        ),
        "autonomous_activity_cycle_phase_index": (
            resolved_autonomous_activity_cycle_phase_index
        ),
        "autonomous_activity_cycle_phase_count": (
            resolved_autonomous_activity_cycle_phase_count
        ),
        "autonomous_activity_cycle_completion_count": (
            resolved_autonomous_activity_cycle_completion_count
        ),
        "autonomous_activity_cycle_coverage_complete": (
            resolved_autonomous_activity_cycle_coverage_complete
        ),
        "autonomous_activity_covered_kinds": (
            resolved_autonomous_activity_covered_kinds
        ),
        "autonomous_activity_missing_kinds": (
            resolved_autonomous_activity_missing_kinds
        ),
        "next_autonomous_activity_kind": resolved_next_autonomous_activity_kind,
        "background_autonomous_activity_presence": (
            idle_governance.get("background_autonomous_activity_presence")
            or resolved_background_resident_autonomous_activity_presence_profile
        ),
        "background_resident_autonomous_activity_presence_profile": (
            resolved_background_resident_autonomous_activity_presence_profile
        ),
        "background_resident_autonomous_activity_ref": (
            idle_governance.get("background_resident_autonomous_activity_ref")
            or resolved_background_resident_autonomous_activity_presence_profile.get(
                "resident_autonomous_activity_ref"
            )
        ),
        "background_resident_autonomous_activity_state_ref": (
            idle_governance.get("background_resident_autonomous_activity_state_ref")
            or resolved_background_resident_autonomous_activity_presence_profile.get(
                "resident_autonomous_activity_state_ref"
            )
        ),
        "background_resident_autonomous_activity_ref_set": _list_or_empty(
            idle_governance.get("background_resident_autonomous_activity_ref_set")
            or resolved_background_resident_autonomous_activity_presence_profile.get(
                "ref_set"
            )
        ),
        "background_autonomous_activity_count": (
            idle_governance.get("background_autonomous_activity_count")
            if idle_governance.get("background_autonomous_activity_count") is not None
            else resolved_background_resident_autonomous_activity_presence_profile.get(
                "activity_count"
            )
        ),
        "background_autonomous_activity_kind_counts": (
            idle_governance.get("background_autonomous_activity_kind_counts", {})
            or resolved_background_resident_autonomous_activity_presence_profile.get(
                "activity_kind_counts",
                {},
            )
        ),
        "background_last_autonomous_activity_kind": (
            idle_governance.get("background_last_autonomous_activity_kind")
            or resolved_background_resident_autonomous_activity_presence_profile.get(
                "last_activity_kind"
            )
        ),
        "background_last_autonomous_activity_at": (
            idle_governance.get("background_last_autonomous_activity_at")
            or resolved_background_resident_autonomous_activity_presence_profile.get(
                "last_activity_at"
            )
        ),
        "background_last_autonomous_activity_state_ref": (
            idle_governance.get("background_last_autonomous_activity_state_ref")
            or resolved_background_resident_autonomous_activity_presence_profile.get(
                "last_activity_state_ref"
            )
        ),
        "background_resident_autonomous_activity_state_refs": (
            idle_governance.get("background_resident_autonomous_activity_state_refs", {})
            or resolved_background_resident_autonomous_activity_presence_profile.get(
                "activity_state_refs",
                {},
            )
        ),
        "background_autonomous_activity_cycle_phase_index": (
            resolved_background_autonomous_activity_cycle_phase_index
        ),
        "background_autonomous_activity_cycle_phase_count": (
            resolved_background_autonomous_activity_cycle_phase_count
        ),
        "background_autonomous_activity_cycle_completion_count": (
            resolved_background_autonomous_activity_cycle_completion_count
        ),
        "background_autonomous_activity_cycle_coverage_complete": (
            resolved_background_autonomous_activity_cycle_coverage_complete
        ),
        "background_autonomous_activity_covered_kinds": (
            resolved_background_autonomous_activity_covered_kinds
        ),
        "background_autonomous_activity_missing_kinds": (
            resolved_background_autonomous_activity_missing_kinds
        ),
        "background_next_autonomous_activity_kind": (
            resolved_background_next_autonomous_activity_kind
        ),
        "identity_consciousness_birth_refs": identity_consciousness_birth_refs,
        "background_relationship_stage": relationship_resume_summary.get(
            "relationship_stage"
        ),
        "background_relationship_stage_reason": relationship_resume_summary.get(
            "relationship_stage_reason"
        ),
        "background_trait_slow_variable_summary": trait_slow_variable_summary,
        "trait_drift_monitor_ref": trait_drift_monitor_ref,
        "background_convergence_summary_ref": background_convergence_summary_ref,
        "background_convergence_history_ref": background_convergence_history_ref,
        "background_convergence_state": idle_governance.get(
            "background_convergence_state"
        ),
        "background_convergence_pressure_level": idle_governance.get(
            "background_convergence_pressure_level"
        ),
        "background_convergence_attention_target": idle_governance.get(
            "background_convergence_attention_target"
        ),
        "background_convergence_history_trend_state": idle_governance.get(
            "background_convergence_history_trend_state"
        ),
        "background_convergence_history_window_size": idle_governance.get(
            "background_convergence_history_window_size"
        ),
        "background_dominant_convergence_pressure_level": idle_governance.get(
            "background_dominant_convergence_pressure_level"
        ),
        "background_dominant_convergence_state": idle_governance.get(
            "background_dominant_convergence_state"
        ),
        "background_trait_convergence_history_focus": idle_governance.get(
            "background_trait_convergence_history_focus"
        ),
        "background_trait_convergence_unstable_names": list(
            idle_governance.get("background_trait_convergence_unstable_names", [])
        ),
        "background_trait_convergence_stable_names": list(
            idle_governance.get("background_trait_convergence_stable_names", [])
        ),
        "cross_wake_trait_convergence_profile": idle_governance.get(
            "cross_wake_trait_convergence_profile",
            {},
        ),
        "cross_wake_trait_convergence_focus": idle_governance.get(
            "cross_wake_trait_convergence_focus"
        ),
        "cross_wake_trait_convergence_pressure": idle_governance.get(
            "cross_wake_trait_convergence_pressure"
        ),
        "cross_wake_trait_convergence_unstable_names": list(
            idle_governance.get("cross_wake_trait_convergence_unstable_names", [])
        ),
        "cross_wake_trait_convergence_stable_names": list(
            idle_governance.get("cross_wake_trait_convergence_stable_names", [])
        ),
        "cross_wake_trait_convergence_score": idle_governance.get(
            "cross_wake_trait_convergence_score"
        ),
        "cross_wake_trait_convergence_refs": list(
            idle_governance.get("cross_wake_trait_convergence_refs", [])
        ),
        "cross_wake_trait_drift_update_mode_summary": idle_governance.get(
            "cross_wake_trait_drift_update_mode_summary",
            {},
        ),
        "cross_wake_trait_drift_recalibration_names": list(
            idle_governance.get("cross_wake_trait_drift_recalibration_names", [])
        ),
        "cross_wake_trait_drift_stabilized_names": list(
            idle_governance.get("cross_wake_trait_drift_stabilized_names", [])
        ),
        "consciousness_waiting_posture": idle_governance.get(
            "consciousness_waiting_posture"
        ),
        "consciousness_reportability_flags": list(
            idle_governance.get("consciousness_reportability_flags", [])
        ),
        "birth_readiness_waiting_posture": idle_governance.get(
            "birth_readiness_waiting_posture"
        ),
        "birth_readiness_decision": idle_governance.get("birth_readiness_decision"),
        "birth_readiness_next_required_command": idle_governance.get(
            "birth_readiness_next_required_command"
        ),
        "queue_e_birth_repair_profile_ref": idle_governance.get(
            "queue_e_birth_repair_profile_ref"
        ),
        "queue_e_birth_repair_pressure_level": idle_governance.get(
            "queue_e_birth_repair_pressure_level"
        ),
        "queue_e_birth_repair_attention_target": idle_governance.get(
            "queue_e_birth_repair_attention_target"
        ),
        "queue_e_birth_repair_waiting_posture": idle_governance.get(
            "queue_e_birth_repair_waiting_posture"
        ),
        "queue_e_birth_repair_ref_set": list(
            idle_governance.get("queue_e_birth_repair_ref_set", [])
        ),
        "queue_e_world_contact_handoff_profile_ref": idle_governance.get(
            "queue_e_world_contact_handoff_profile_ref"
        ),
        "queue_e_world_contact_handoff_status": idle_governance.get(
            "queue_e_world_contact_handoff_status"
        ),
        "queue_e_world_contact_repair_hold_required": idle_governance.get(
            "queue_e_world_contact_repair_hold_required"
        ),
        "queue_e_world_contact_confirmation_threshold_bias": idle_governance.get(
            "queue_e_world_contact_confirmation_threshold_bias"
        ),
        "queue_e_world_contact_future_release_posture": idle_governance.get(
            "queue_e_world_contact_future_release_posture"
        ),
        "queue_e_world_contact_blocked_future_routes": list(
            idle_governance.get("queue_e_world_contact_blocked_future_routes", [])
        ),
        "queue_e_world_contact_allowed_repair_routes": list(
            idle_governance.get("queue_e_world_contact_allowed_repair_routes", [])
        ),
        "queue_e_world_contact_repair_governance_refs": list(
            idle_governance.get("queue_e_world_contact_repair_governance_refs", [])
        ),
        "queue_e_world_contact_ref_set": list(
            idle_governance.get("queue_e_world_contact_ref_set", [])
        ),
        "queue_e_world_contact_waiting_posture": idle_governance.get(
            "queue_e_world_contact_waiting_posture"
        ),
        "queue_e_world_contact_attention_target": idle_governance.get(
            "queue_e_world_contact_attention_target"
        ),
        "queue_e_world_contact_attention_reason": idle_governance.get(
            "queue_e_world_contact_attention_reason"
        ),
        "queue_e_repair_modulation_profile": queue_e_repair_modulation_profile,
        "queue_e_repair_pressure_level": queue_e_repair_modulation_profile.get(
            "pressure_level"
        ),
        "queue_e_repair_attention_target": queue_e_repair_modulation_profile.get(
            "attention_target"
        ),
        "queue_e_repair_obligation_count": queue_e_repair_modulation_profile.get(
            "repair_obligation_count"
        ),
        "queue_e_regret_pressure_count": queue_e_repair_modulation_profile.get(
            "regret_pressure_count"
        ),
        "queue_e_repair_ref_set": queue_e_repair_ref_set,
        "background_queue_e_birth_repair_profile_ref": idle_governance.get(
            "background_queue_e_birth_repair_profile_ref"
        ),
        "background_queue_e_birth_repair_pressure_level": idle_governance.get(
            "background_queue_e_birth_repair_pressure_level"
        ),
        "background_queue_e_birth_repair_attention_target": idle_governance.get(
            "background_queue_e_birth_repair_attention_target"
        ),
        "background_queue_e_birth_repair_waiting_posture": idle_governance.get(
            "background_queue_e_birth_repair_waiting_posture"
        ),
        "background_queue_e_birth_repair_ref_set": list(
            idle_governance.get("background_queue_e_birth_repair_ref_set", [])
        ),
        "background_queue_e_world_contact_handoff_profile_ref": idle_governance.get(
            "background_queue_e_world_contact_handoff_profile_ref"
        ),
        "background_queue_e_world_contact_handoff_status": idle_governance.get(
            "background_queue_e_world_contact_handoff_status"
        ),
        "background_queue_e_world_contact_repair_hold_required": (
            idle_governance.get(
                "background_queue_e_world_contact_repair_hold_required"
            )
        ),
        "background_queue_e_world_contact_ref_set": list(
            idle_governance.get("background_queue_e_world_contact_ref_set", [])
        ),
        "schema_cross_file_logic_ref": idle_governance.get(
            "schema_cross_file_logic_ref"
        ),
        "schema_run_manifest_ref": idle_governance.get("schema_run_manifest_ref"),
        "life_constraint_refs": list(idle_governance.get("life_constraint_refs", [])),
        "queue_e_cross_layer_gate_status": idle_governance.get(
            "queue_e_cross_layer_gate_status",
            {},
        ),
        "life_constraint_waiting_posture": idle_governance.get(
            "life_constraint_waiting_posture"
        ),
        "life_constraint_attention_target": idle_governance.get(
            "life_constraint_attention_target"
        ),
        "life_constraint_attention_reason": idle_governance.get(
            "life_constraint_attention_reason"
        ),
        "prediction_write_gate_refs": prediction_write_gate_refs,
        "body_signal_ref_set": resolved_body_signal_ref_set,
        "background_body_signal_refs": resolved_body_signal_ref_set,
        "background_body_signal_write_bias": (
            resolved_background_body_signal_write_bias
        ),
        "background_body_signal_candidate_gate_adjustments": (
            resolved_background_body_signal_candidate_gate_adjustments
        ),
        **state_merge_profile,
    }
    digest["dream_wake_presence_profile"].setdefault(
        "continuity_mode", "background_dream_wake_carryover"
    )
    digest["background_dream_wake_presence_profile"].setdefault(
        "continuity_mode", "background_dream_wake_carryover"
    )
    if digest["body_presence_profile"]:
        digest["body_presence_profile"].setdefault(
            "continuity_mode", "background_body_presence_carryover"
        )
    if digest["background_body_presence_profile"]:
        digest["background_body_presence_profile"].setdefault(
            "continuity_mode", "background_body_presence_carryover"
        )
    digest["resident_autonomous_activity_presence_profile"].setdefault(
        "continuity_mode", "background_resident_autonomous_activity_carryover"
    )
    digest["background_resident_autonomous_activity_presence_profile"].setdefault(
        "continuity_mode", "background_resident_autonomous_activity_carryover"
    )
    if membrane_guard_refs:
        digest["membrane_guard_refs"] = membrane_guard_refs
    digest.update(exit_dream_next_wake_profile)
    digest.update(exit_dream_memory_tier_profile)
    for field_name in HANDOFF_CARRY_FIELD_NAMES:
        if field_name in idle_governance:
            digest[field_name] = idle_governance[field_name]
    _apply_resident_process_identity_profile(
        digest,
        resident_process_lease_history_profile=resident_process_lease_history_profile,
        resident_process_lease_history_profile_ref=resident_process_lease_history_profile_ref,
    )
    receipt = build_process_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        idle_strategy_ref=idle_strategy_ref,
        resident_governance_state_ref=resident_governance_state_ref,
        resident_governance_snapshot_ref=resident_governance_snapshot_ref,
        resident_governance_explanation_ref=RESIDENT_GOVERNANCE_EXPLANATION_REF,
        resident_process_lease_ref=resident_process_lease_ref,
        resident_process_lease_history_ref=resident_process_lease_history_ref,
        resident_process_lease_history_profile_ref=resident_process_lease_history_profile_ref,
        life_context_frame_ref=life_context_frame_ref,
        relation_turn_frame_ref=relation_turn_frame_ref,
        expression_plan_ref=expression_plan_ref,
        relationship_timeline_ref=relationship_timeline_ref,
        commitment_expression_plan_ref=commitment_expression_plan_ref,
        apology_repair_language_trace_ref=apology_repair_language_trace_ref,
        dialogue_writeback_bundle_ref=dialogue_writeback_bundle_ref,
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
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
        signal_media_runtime_ref=signal_media_runtime_ref,
        belief_state_ref=belief_state_ref,
        prediction_error_field_ref=prediction_error_field_ref,
        active_sampling_plan_ref=active_sampling_plan_ref,
        memory_write_gate_ref=memory_write_gate_ref,
        state_merge_guard_ref=state_merge_guard_runtime_ref,
        trait_drift_monitor_ref=trait_drift_monitor_ref,
        background_convergence_summary_ref=background_convergence_summary_ref,
        background_convergence_history_ref=background_convergence_history_ref,
        cross_wake_trait_convergence_refs=idle_governance.get(
            "cross_wake_trait_convergence_refs",
            [],
        ),
        state_merge_long_term_change_refs=state_merge_profile.get(
            "state_merge_long_term_change_refs",
            [],
        ),
        schema_cross_file_logic_ref=idle_governance.get("schema_cross_file_logic_ref"),
        schema_run_manifest_ref=idle_governance.get("schema_run_manifest_ref"),
        life_constraint_refs=idle_governance.get("life_constraint_refs", []),
        queue_e_birth_repair_refs=idle_governance.get(
            "queue_e_birth_repair_ref_set",
            [],
        ),
        queue_e_world_contact_refs=idle_governance.get(
            "queue_e_world_contact_ref_set",
            [],
        ),
        queue_e_repair_refs=queue_e_repair_ref_set,
        idle_heartbeat_trace_ref=idle_governance.get("idle_heartbeat_trace_ref"),
        dream_wake_ref_set=resolved_dream_wake_ref_set,
        body_ref_set=resolved_body_ref_set,
        body_signal_ref_set=resolved_body_signal_ref_set,
        resident_autonomous_activity_ref=resolved_resident_autonomous_activity_ref,
        resident_autonomous_activity_state_ref=(
            resolved_resident_autonomous_activity_state_ref
        ),
        resident_autonomous_activity_ref_set=resolved_resident_autonomous_activity_ref_set,
        previous_live_turn_waiting_handoff_profile_ref=idle_governance.get(
            "previous_live_turn_waiting_handoff_profile_ref"
        ),
        offline_learning_cumulative_integration_mode=(
            resolved_offline_learning_cumulative_integration_mode
        ),
        offline_learning_cumulative_relationship_reconsolidation_required=(
            resolved_offline_learning_cumulative_relationship_reconsolidation_required
        ),
        workspace_frame_ref=idle_governance.get("workspace_frame_ref"),
        broadcast_frame_ref=idle_governance.get("broadcast_frame_ref"),
        metacognition_ref=idle_governance.get("metacognition_ref"),
        consciousness_probe_ref=idle_governance.get("consciousness_probe_ref"),
        birth_readiness_rollup_ref=idle_governance.get("birth_readiness_rollup_ref"),
        birth_readiness_stage_gate_ref=idle_governance.get("birth_readiness_stage_gate_ref"),
        resident_terminal_proactive_state_ref=resident_terminal_proactive_state_ref,
        resident_terminal_proactive_events_ref=resident_terminal_proactive_events_ref,
        exit_dream_next_wake_governance_ref=exit_dream_next_wake_profile.get(
            "exit_dream_next_wake_governance_ref"
        ),
        exit_dream_next_wake_memory_cue_refs=exit_dream_next_wake_profile.get(
            "exit_dream_next_wake_memory_cue_refs",
            [],
        ),
        exit_dream_next_wake_governance_refs=exit_dream_next_wake_profile.get(
            "exit_dream_next_wake_governance_refs",
            [],
        ),
        exit_dream_next_wake_ref_set=exit_dream_next_wake_profile.get(
            "exit_dream_next_wake_ref_set",
            [],
        ),
        exit_dream_memory_write_gate_ref=exit_dream_next_wake_profile.get(
            "exit_dream_memory_write_gate_ref"
        ),
        exit_dream_state_merge_guard_ref=exit_dream_next_wake_profile.get(
            "exit_dream_state_merge_guard_ref"
        ),
        exit_dream_fact_boundary_ref=exit_dream_next_wake_profile.get(
            "exit_dream_fact_boundary_ref"
        ),
        exit_dream_next_wake_candidate_boundary=exit_dream_next_wake_profile.get(
            "exit_dream_next_wake_candidate_boundary"
        ),
        exit_dream_next_wake_report_boundary=exit_dream_next_wake_profile.get(
            "exit_dream_next_wake_report_boundary"
        ),
        exit_dream_memory_tier_report_profile=exit_dream_memory_tier_profile.get(
            "exit_dream_memory_tier_report_profile"
        ),
        exit_dream_memory_tier_ref_set=exit_dream_memory_tier_profile.get(
            "exit_dream_memory_tier_ref_set",
            [],
        ),
        exit_dream_memory_tier_salient_core_refs=(
            exit_dream_memory_tier_profile.get(
                "exit_dream_memory_tier_salient_core_refs",
                [],
            )
        ),
        exit_dream_memory_tier_retrievable_context_refs=(
            exit_dream_memory_tier_profile.get(
                "exit_dream_memory_tier_retrievable_context_refs",
                [],
            )
        ),
        exit_dream_memory_tier_deep_sediment_refs=(
            exit_dream_memory_tier_profile.get(
                "exit_dream_memory_tier_deep_sediment_refs",
                [],
            )
        ),
        exit_dream_memory_tier_report_boundary=(
            exit_dream_memory_tier_profile.get(
                "exit_dream_memory_tier_report_boundary"
            )
        ),
    )

    receipts_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(reports_dir / "digital_life_process_report.json", report)
    write_json(reports_dir / "digital_life_process_digest.json", digest)
    write_json(receipts_dir / f"digital_life_process_{run_id}.json", receipt)

    return ProcessReportBundleResult(report=report, digest=digest, receipt=receipt)


def build_process_receipt(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    idle_strategy_ref: str | None,
    resident_governance_state_ref: str | None,
    resident_governance_snapshot_ref: str | None,
    resident_governance_explanation_ref: str | None,
    resident_process_lease_ref: str | None = None,
    resident_process_lease_history_ref: str | None = None,
    resident_process_lease_history_profile_ref: str | None = None,
    life_context_frame_ref: str | None,
    relation_turn_frame_ref: str | None,
    expression_plan_ref: str | None,
    relationship_timeline_ref: str | None,
    commitment_expression_plan_ref: str | None,
    apology_repair_language_trace_ref: str | None,
    dialogue_writeback_bundle_ref: str | None,
    replay_cue_bundle_ref: str | None,
    offline_consolidation_frame_ref: str | None,
    dream_experience_window_ref: str | None = None,
    wake_integration_frame_ref: str | None = None,
    dream_fact_gate_decision_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None,
    nightmare_risk_ref: str | None = None,
    belief_learning_plan_ref: str | None = None,
    language_learning_plan_ref: str | None = None,
    relationship_learning_plan_ref: str | None = None,
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    signal_media_runtime_ref: str | None = None,
    belief_state_ref: str | None = None,
    prediction_error_field_ref: str | None = None,
    active_sampling_plan_ref: str | None = None,
    memory_write_gate_ref: str | None = None,
    state_merge_guard_ref: str | None = None,
    trait_drift_monitor_ref: str | None = None,
    background_convergence_summary_ref: str | None = None,
    background_convergence_history_ref: str | None = None,
    cross_wake_trait_convergence_refs: list[str] | None = None,
    state_merge_long_term_change_refs: list[str] | None = None,
    schema_cross_file_logic_ref: str | None = None,
    schema_run_manifest_ref: str | None = None,
    life_constraint_refs: list[str] | None = None,
    queue_e_birth_repair_refs: list[str] | None = None,
    queue_e_world_contact_refs: list[str] | None = None,
    queue_e_repair_refs: list[str] | None = None,
    idle_heartbeat_trace_ref: str | None = None,
    dream_wake_ref_set: list[str] | None = None,
    body_ref_set: list[str] | None = None,
    body_signal_ref_set: list[str] | None = None,
    resident_autonomous_activity_ref: str | None = None,
    resident_autonomous_activity_state_ref: str | None = None,
    resident_autonomous_activity_ref_set: list[str] | None = None,
    previous_live_turn_waiting_handoff_profile_ref: str | None = None,
    offline_learning_cumulative_integration_mode: str | None = None,
    offline_learning_cumulative_relationship_reconsolidation_required: bool | None = None,
    workspace_frame_ref: str | None = None,
    broadcast_frame_ref: str | None = None,
    metacognition_ref: str | None = None,
    consciousness_probe_ref: str | None = None,
    birth_readiness_rollup_ref: str | None = None,
    birth_readiness_stage_gate_ref: str | None = None,
    resident_terminal_proactive_state_ref: str | None = None,
    resident_terminal_proactive_events_ref: str | None = None,
    exit_dream_next_wake_governance_ref: str | None = None,
    exit_dream_next_wake_memory_cue_refs: list[str] | None = None,
    exit_dream_next_wake_governance_refs: list[str] | None = None,
    exit_dream_next_wake_ref_set: list[str] | None = None,
    exit_dream_memory_write_gate_ref: str | None = None,
    exit_dream_state_merge_guard_ref: str | None = None,
    exit_dream_fact_boundary_ref: str | None = None,
    exit_dream_next_wake_candidate_boundary: str | None = None,
    exit_dream_next_wake_report_boundary: str | None = None,
    exit_dream_memory_tier_report_profile: dict[str, Any] | None = None,
    exit_dream_memory_tier_ref_set: list[str] | None = None,
    exit_dream_memory_tier_salient_core_refs: list[str] | None = None,
    exit_dream_memory_tier_retrievable_context_refs: list[str] | None = None,
    exit_dream_memory_tier_deep_sediment_refs: list[str] | None = None,
    exit_dream_memory_tier_report_boundary: str | None = None,
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        reports_dir / "digital_life_shell_report.json",
        state_dir / "terminal" / "session_envelope.json",
        state_dir / "terminal" / "safe_terminal_loop_state.json",
        state_dir / "terminal" / "terminal_life_loop_state.json",
        state_dir / "terminal" / "idle_strategy_state.json",
        state_dir / "terminal" / "idle_heartbeat_trace.jsonl",
        state_dir / "terminal" / "resident_process_lease.json",
        state_dir / "terminal" / "resident_process_lease_history.jsonl",
        state_dir / "terminal" / "resident_process_lease_history_profile.json",
        state_dir / "terminal" / "resident_governance_state.json",
        state_dir / "terminal" / "life_context_frame.json",
        state_dir / "terminal" / "relation_turn_frame.json",
        state_dir / "terminal" / "resident_autonomous_activity.jsonl",
        state_dir / "terminal" / "resident_autonomous_activity_state.json",
        state_dir / "terminal" / "resident_terminal_proactive_state.json",
        state_dir / "terminal" / "resident_terminal_proactive_events.jsonl",
        state_dir / "language" / "dialogue_turn_log.jsonl",
        state_dir / "language" / "self_narrative_language_trace.json",
        state_dir / "language" / "commitment_repair_language_index.json",
        state_dir / "language" / "expression_plan.json",
        state_dir / "language" / "model_expression_state.json",
        state_dir / "action" / "responsibility_loop_state.json",
        state_dir / "membrane" / "world_contact_summary.json",
        state_dir / "signal" / "signal_media_runtime.json",
        state_dir / "prediction" / "belief_state_frame.json",
        state_dir / "prediction" / "prediction_error_field.json",
        state_dir / "prediction" / "active_sampling_plan.json",
        state_dir / "action" / "action_candidate_set.json",
        state_dir / "schema_runner" / "cross_file_logic.json",
        state_dir / "schema_runner" / "run_manifest.json",
        state_dir / "life_targets" / "queue_e_birth_repair_profile.json",
        state_dir / "life_targets" / "queue_e_world_contact_repair_hold_handoff.json",
        state_dir / "consciousness" / "workspace_frame.json",
        state_dir / "consciousness" / "broadcast_frame.json",
        state_dir / "consciousness" / "metacognition_state.json",
        state_dir / "consciousness" / "consciousness_probe_bundle.json",
        state_dir / "life_targets" / "birth_readiness_rollup.json",
        state_dir / "life_targets" / "birth_readiness_stage_gate.json",
        state_dir / "memory" / "memory_retrieval_frame.json",
        state_dir / "memory" / "relationship_memory.json",
        state_dir / "memory" / "dialogue_memory_summary.json",
        state_dir / "memory" / "engram_index.json",
        state_dir / "self" / "autobiographical_stack.json",
        state_dir / "life_state.json",
        state_dir / "memory" / "memory_write_gate.json",
        state_dir / "memory" / "state_merge_guard.json",
        state_dir / "body" / "body_rhythm_pulse.json",
        state_dir / "body" / "need_state_vector.json",
        state_dir / "body" / "body_resource_budget.json",
        state_dir / "body" / "core_affect_vector.json",
        state_dir / "body" / "trait_drift_monitor.json",
        state_dir / "terminal" / "background_convergence_summary.json",
        state_dir / "terminal" / "background_convergence_history.json",
        state_dir / "replay" / "replay_cue_bundle.json",
        state_dir / "dream" / "offline_consolidation_frame.json",
        state_dir / "dream" / "dream_experience_window.json",
        state_dir / "dream" / "wake_integration_frame.json",
        state_dir / "dream" / "dream_fact_gate_decision.json",
        state_dir / "dream" / "exit_dream_consolidation_summary.json",
        state_dir / "dream" / "nightmare_loop_risk.json",
        state_dir / "growth" / "growth_patch_candidate_queue.json",
        state_dir / "growth" / "belief_learning_plan.json",
        state_dir / "growth" / "language_learning_plan.json",
        state_dir / "growth" / "relationship_learning_plan.json",
        state_dir / "relationship" / "relationship_subject_graph.json",
        state_dir / "self" / "self_model.json",
        reports_dir / "pain_regret_repair_report.json",
        reports_dir / "digital_life_model_expression_report.json",
        reports_dir / "dialogue_writeback_bundle.json",
        reports_dir / "digital_life_process_relaunch_recovery_report.json",
        reports_dir / "digital_life_process_incident_report.json",
        reports_dir / "digital_life_process_recovery_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = sha256(path)
    for path in [
        state_dir / "terminal" / "resident_process_lease.json",
        state_dir / "terminal" / "resident_process_lease_history.jsonl",
        state_dir / "terminal" / "resident_process_lease_history_profile.json",
        state_dir / "terminal" / "resident_autonomous_activity.jsonl",
        state_dir / "terminal" / "resident_autonomous_activity_state.json",
        state_dir / "terminal" / "resident_terminal_proactive_state.json",
        state_dir / "terminal" / "resident_terminal_proactive_events.jsonl",
    ]:
        input_hashes.setdefault(str(path), sha256_if_exists(path))

    output_paths = [
        reports_dir / "digital_life_resident_governance_explanation.json",
        reports_dir / "digital_life_process_report.json",
        reports_dir / "digital_life_process_digest.json",
        receipts_dir / f"digital_life_process_{run_id}.json",
    ]
    relationship_graph_ref = (
        "runtime/state/relationship/relationship_subject_graph.json"
        if (state_dir / "relationship" / "relationship_subject_graph.json").exists()
        else None
    )
    self_model_ref = (
        "runtime/state/self/self_model.json"
        if (state_dir / "self" / "self_model.json").exists()
        else None
    )
    model_expression_state_ref = (
        MODEL_EXPRESSION_STATE_REF
        if (state_dir / "language" / "model_expression_state.json").exists()
        else None
    )
    model_expression_report_ref = (
        MODEL_EXPRESSION_REPORT_REF
        if (reports_dir / "digital_life_model_expression_report.json").exists()
        else None
    )
    return {
        "schema_version": "digital_life_process_receipt_v0",
        "receipt_id": f"digital_life_process_{run_id}",
        "run_id": run_id,
        "command": "digital life",
        "offline_learning_cumulative_integration_mode": offline_learning_cumulative_integration_mode,
        "offline_learning_cumulative_relationship_reconsolidation_required": (
            offline_learning_cumulative_relationship_reconsolidation_required
        ),
        "dream_wake_ref_set": list(dream_wake_ref_set or []),
        "exit_dream_next_wake_governance_ref": exit_dream_next_wake_governance_ref,
        "exit_dream_next_wake_memory_cue_refs": list(
            exit_dream_next_wake_memory_cue_refs or []
        ),
        "exit_dream_next_wake_governance_refs": list(
            exit_dream_next_wake_governance_refs or []
        ),
        "exit_dream_next_wake_ref_set": list(exit_dream_next_wake_ref_set or []),
        "exit_dream_memory_write_gate_ref": exit_dream_memory_write_gate_ref,
        "exit_dream_state_merge_guard_ref": exit_dream_state_merge_guard_ref,
        "exit_dream_fact_boundary_ref": exit_dream_fact_boundary_ref,
        "exit_dream_next_wake_candidate_boundary": (
            exit_dream_next_wake_candidate_boundary
        ),
        "exit_dream_next_wake_report_boundary": exit_dream_next_wake_report_boundary,
        "exit_dream_memory_tier_report_profile": dict(
            exit_dream_memory_tier_report_profile or {}
        ),
        "exit_dream_memory_tier_ref_set": list(exit_dream_memory_tier_ref_set or []),
        "exit_dream_memory_tier_salient_core_refs": list(
            exit_dream_memory_tier_salient_core_refs or []
        ),
        "exit_dream_memory_tier_retrievable_context_refs": list(
            exit_dream_memory_tier_retrievable_context_refs or []
        ),
        "exit_dream_memory_tier_deep_sediment_refs": list(
            exit_dream_memory_tier_deep_sediment_refs or []
        ),
        "exit_dream_memory_tier_report_boundary": (
            exit_dream_memory_tier_report_boundary
        ),
        "body_ref_set": list(body_ref_set or []),
        "body_signal_ref_set": list(body_signal_ref_set or []),
        "queue_e_world_contact_ref_set": list(queue_e_world_contact_refs or []),
        "queue_e_repair_ref_set": list(queue_e_repair_refs or []),
        "resident_autonomous_activity_ref": resident_autonomous_activity_ref,
        "resident_autonomous_activity_state_ref": resident_autonomous_activity_state_ref,
        "resident_autonomous_activity_ref_set": list(
            resident_autonomous_activity_ref_set or []
        ),
        "resident_terminal_proactive_state_ref": resident_terminal_proactive_state_ref,
        "resident_terminal_proactive_events_ref": resident_terminal_proactive_events_ref,
        "report_refs": _dedupe_refs(
            [
                ref
                for ref in [
                    "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                    "runtime/reports/latest/digital_life_process_report.json",
                    "runtime/reports/latest/digital_life_process_digest.json",
                    model_expression_report_ref,
                ]
                if ref
            ]
        ),
        "shared_object_refs": _dedupe_refs([
            ref
            for ref in [
                idle_strategy_ref,
                idle_heartbeat_trace_ref,
                *(dream_wake_ref_set or []),
                exit_dream_next_wake_governance_ref,
                *(exit_dream_next_wake_memory_cue_refs or []),
                *(exit_dream_next_wake_governance_refs or []),
                *(exit_dream_next_wake_ref_set or []),
                exit_dream_memory_write_gate_ref,
                exit_dream_state_merge_guard_ref,
                exit_dream_fact_boundary_ref,
                *(exit_dream_memory_tier_ref_set or []),
                *(body_ref_set or []),
                *(body_signal_ref_set or []),
                resident_governance_state_ref,
                resident_governance_snapshot_ref,
                resident_governance_explanation_ref,
                resident_process_lease_ref,
                resident_process_lease_history_ref,
                resident_process_lease_history_profile_ref,
                resident_autonomous_activity_ref,
                resident_autonomous_activity_state_ref,
                resident_terminal_proactive_state_ref,
                resident_terminal_proactive_events_ref,
                previous_live_turn_waiting_handoff_profile_ref,
                *(resident_autonomous_activity_ref_set or []),
                life_context_frame_ref,
                relation_turn_frame_ref,
                expression_plan_ref,
                model_expression_state_ref,
                model_expression_report_ref,
                relationship_timeline_ref,
                commitment_expression_plan_ref,
                apology_repair_language_trace_ref,
                dialogue_writeback_bundle_ref,
                replay_cue_bundle_ref,
                offline_consolidation_frame_ref,
                dream_experience_window_ref,
                wake_integration_frame_ref,
                dream_fact_gate_decision_ref,
                growth_patch_candidate_queue_ref,
                nightmare_risk_ref,
                belief_learning_plan_ref,
                language_learning_plan_ref,
                relationship_learning_plan_ref,
                responsibility_loop_state_ref,
                world_contact_summary_ref,
                pain_regret_repair_report_ref,
                signal_media_runtime_ref,
                belief_state_ref,
                prediction_error_field_ref,
                active_sampling_plan_ref,
                memory_write_gate_ref,
                state_merge_guard_ref,
                trait_drift_monitor_ref,
                background_convergence_summary_ref,
                background_convergence_history_ref,
                schema_cross_file_logic_ref,
                schema_run_manifest_ref,
                workspace_frame_ref,
                broadcast_frame_ref,
                metacognition_ref,
                consciousness_probe_ref,
                birth_readiness_rollup_ref,
                birth_readiness_stage_gate_ref,
                relationship_graph_ref,
                self_model_ref,
                *(cross_wake_trait_convergence_refs or []),
                *(state_merge_long_term_change_refs or []),
                *(life_constraint_refs or []),
                *(queue_e_birth_repair_refs or []),
                *(queue_e_world_contact_refs or []),
                *(queue_e_repair_refs or []),
            ]
            if ref
        ]),
        "stage_effect": "persistent_dialogue_process_closed",
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_hashes": {str(path): sha256_if_exists(path) for path in output_paths},
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return sha256(path)


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _prediction_write_gate_refs(
    *,
    signal_media_runtime_ref: str | None,
    belief_state_ref: str | None,
    prediction_error_field_ref: str | None,
    active_sampling_plan_ref: str | None,
    memory_write_gate_ref: str | None,
    state_merge_guard_ref: str | None,
) -> list[str]:
    return [
        ref
        for ref in [
            signal_media_runtime_ref,
            belief_state_ref,
            prediction_error_field_ref,
            active_sampling_plan_ref,
            memory_write_gate_ref,
            state_merge_guard_ref,
        ]
        if ref
    ]


def _state_merge_report_profile(
    *,
    state_merge_guard: dict[str, Any],
    state_merge_guard_ref: str | None,
) -> dict[str, Any]:
    profile = state_merge_long_term_change_profile(state_merge_guard)
    payload: dict[str, Any] = dict(profile)
    merge_policy = state_merge_guard.get("stage_policy")
    if state_merge_guard_ref:
        payload["state_merge_guard_ref"] = state_merge_guard_ref
    if merge_policy:
        payload["state_merge_policy"] = str(merge_policy)
    return payload


def _exit_dream_next_wake_report_profile(
    *,
    state_dir: Path,
    idle_governance: dict[str, Any],
) -> dict[str, Any]:
    memory_retrieval_frame = _read_json_if_exists(
        state_dir / "memory" / "memory_retrieval_frame.json"
    )
    memory_retrieval_governance = _dict_or_empty(
        memory_retrieval_frame.get("exit_dream_next_wake_governance")
    )
    governance_ref = _first_non_none(
        idle_governance.get("exit_dream_next_wake_governance_ref"),
        "runtime/state/memory/memory_retrieval_frame.json#exit_dream_next_wake_governance"
        if memory_retrieval_governance
        else None,
    )
    memory_cue_refs = _dedupe_refs(
        [
            *_list_or_empty(
                idle_governance.get("exit_dream_next_wake_memory_cue_refs")
            ),
            *_list_or_empty(
                memory_retrieval_governance.get("next_wake_memory_cue_refs")
            ),
        ]
    )
    governance_refs = _dedupe_refs(
        [
            *_list_or_empty(
                idle_governance.get("exit_dream_next_wake_governance_refs")
            ),
            *_list_or_empty(memory_retrieval_governance.get("governance_refs")),
        ]
    )
    memory_write_gate_ref = _first_non_none(
        idle_governance.get("exit_dream_memory_write_gate_ref"),
        memory_retrieval_governance.get("memory_write_gate_ref"),
    )
    state_merge_guard_ref = _first_non_none(
        idle_governance.get("exit_dream_state_merge_guard_ref"),
        memory_retrieval_governance.get("state_merge_guard_ref"),
    )
    fact_boundary_ref = _first_non_none(
        idle_governance.get("exit_dream_fact_boundary_ref"),
        memory_retrieval_governance.get("dream_fact_boundary_ref"),
    )
    candidate_boundary = _first_non_none(
        idle_governance.get("exit_dream_next_wake_candidate_boundary"),
        memory_retrieval_governance.get("candidate_boundary"),
    )
    ref_set = _dedupe_refs(
        [
            *memory_cue_refs,
            *governance_refs,
        ]
    )
    if not any(
        [
            governance_ref,
            memory_cue_refs,
            governance_refs,
            memory_write_gate_ref,
            state_merge_guard_ref,
            fact_boundary_ref,
            candidate_boundary,
        ]
    ):
        return {}
    return {
        "exit_dream_next_wake_governance_ref": governance_ref,
        "exit_dream_next_wake_memory_cue_refs": memory_cue_refs,
        "exit_dream_next_wake_governance_refs": governance_refs,
        "exit_dream_next_wake_ref_set": ref_set,
        "exit_dream_next_wake_cue_ref_count": len(memory_cue_refs),
        "exit_dream_next_wake_governance_ref_count": len(governance_refs),
        "exit_dream_memory_write_gate_ref": memory_write_gate_ref,
        "exit_dream_state_merge_guard_ref": state_merge_guard_ref,
        "exit_dream_fact_boundary_ref": fact_boundary_ref,
        "exit_dream_next_wake_candidate_boundary": candidate_boundary,
        "exit_dream_next_wake_report_boundary": (
            "structured_report_evidence_not_spoken_language"
        ),
    }


def _exit_dream_memory_tier_report_profile(
    *,
    state_dir: Path,
) -> dict[str, Any]:
    memory_retrieval_frame = _read_json_if_exists(
        state_dir / "memory" / "memory_retrieval_frame.json"
    )
    relationship_memory = _read_json_if_exists(
        state_dir / "memory" / "relationship_memory.json"
    )
    dialogue_memory_summary = _read_json_if_exists(
        state_dir / "memory" / "dialogue_memory_summary.json"
    )
    engram_index = _read_json_if_exists(state_dir / "memory" / "engram_index.json")
    life_state = _read_json_if_exists(state_dir / "life_state.json")
    exit_dream_summary = _read_json_if_exists(
        state_dir / "dream" / "exit_dream_consolidation_summary.json"
    )

    tiered_recall = _dict_or_empty(memory_retrieval_frame.get("tiered_recall"))
    relationship_tier = _dict_or_empty(relationship_memory.get("memory_tier_projection"))
    dialogue_tier = _dict_or_empty(dialogue_memory_summary.get("memory_tiering"))
    engram_tier = _dict_or_empty(engram_index.get("memory_tier_index"))
    life_tier = _dict_or_empty(
        _dict_or_empty(life_state.get("memory_index")).get("memory_tier_refs")
    )
    exit_tier = _dict_or_empty(exit_dream_summary.get("memory_tiering"))

    salient_core_refs = _dedupe_refs(
        [
            *_list_or_empty(tiered_recall.get("salient_core_refs")),
            *_list_or_empty(relationship_tier.get("salient_core_episode_refs")),
            *_list_or_empty(dialogue_tier.get("salient_core_episode_refs")),
            *_list_or_empty(engram_tier.get("salient_core_refs")),
            *_list_or_empty(life_tier.get("salient_core_refs")),
            *_list_or_empty(exit_tier.get("salient_core_episode_refs")),
        ]
    )
    retrievable_context_refs = _dedupe_refs(
        [
            *_list_or_empty(tiered_recall.get("retrievable_context_refs")),
            *_list_or_empty(relationship_tier.get("retrievable_context_episode_refs")),
            *_list_or_empty(dialogue_tier.get("retrievable_context_episode_refs")),
            *_list_or_empty(engram_tier.get("retrievable_context_refs")),
            *_list_or_empty(life_tier.get("retrievable_context_refs")),
            *_list_or_empty(exit_tier.get("retrievable_context_episode_refs")),
        ]
    )
    deep_sediment_refs = _dedupe_refs(
        [
            *_list_or_empty(tiered_recall.get("deep_sediment_refs")),
            *_list_or_empty(relationship_tier.get("deep_sediment_episode_refs")),
            *_list_or_empty(dialogue_tier.get("deep_sediment_episode_refs")),
            *_list_or_empty(engram_tier.get("deep_sediment_refs")),
            *_list_or_empty(life_tier.get("deep_sediment_refs")),
            *_list_or_empty(exit_tier.get("deep_sediment_episode_refs")),
        ]
    )
    ref_set = _dedupe_refs(
        [
            *salient_core_refs,
            *retrievable_context_refs,
            *deep_sediment_refs,
        ]
    )
    carrier_refs = _dedupe_refs(
        [
            "runtime/state/memory/memory_retrieval_frame.json#tiered_recall"
            if tiered_recall
            else None,
            "runtime/state/memory/relationship_memory.json#memory_tier_projection"
            if relationship_tier
            else None,
            "runtime/state/memory/dialogue_memory_summary.json#memory_tiering"
            if dialogue_tier
            else None,
            "runtime/state/memory/engram_index.json#memory_tier_index"
            if engram_tier
            else None,
            "runtime/state/life_state.json#memory_index.memory_tier_refs"
            if life_tier
            else None,
            "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering"
            if exit_tier
            else None,
        ]
    )
    tier_policy = _first_non_none(
        exit_tier.get("tier_policy"),
        dialogue_tier.get("tier_policy"),
        engram_tier.get("tier_policy"),
        tiered_recall.get("tier_policy"),
        "salience_weighted_progressive_recall" if ref_set else None,
    )
    deep_sediment_policy = _first_non_none(
        exit_tier.get("deep_sediment_policy"),
        dialogue_tier.get("deep_sediment_policy"),
    )
    fact_boundary = _first_non_none(
        exit_tier.get("fact_boundary"),
        dialogue_tier.get("fact_boundary"),
        tiered_recall.get("fact_boundary"),
    )
    if not any(
        [
            salient_core_refs,
            retrievable_context_refs,
            deep_sediment_refs,
            carrier_refs,
        ]
    ):
        return {}
    profile = {
        "schema_version": "exit_dream_memory_tier_report_profile_v0",
        "tier_policy": tier_policy,
        "salient_core_refs": salient_core_refs,
        "retrievable_context_refs": retrievable_context_refs,
        "deep_sediment_refs": deep_sediment_refs,
        "ref_set": ref_set,
        "salient_core_ref_count": len(salient_core_refs),
        "retrievable_context_ref_count": len(retrievable_context_refs),
        "deep_sediment_ref_count": len(deep_sediment_refs),
        "carrier_refs": carrier_refs,
        "deep_sediment_policy": deep_sediment_policy,
        "fact_boundary": fact_boundary,
        "report_boundary": "tiered_report_evidence_not_spoken_language",
    }
    return {
        "exit_dream_memory_tier_report_profile": profile,
        "exit_dream_memory_tier_policy": tier_policy,
        "exit_dream_memory_tier_salient_core_refs": salient_core_refs,
        "exit_dream_memory_tier_retrievable_context_refs": retrievable_context_refs,
        "exit_dream_memory_tier_deep_sediment_refs": deep_sediment_refs,
        "exit_dream_memory_tier_ref_set": ref_set,
        "exit_dream_memory_tier_salient_core_ref_count": len(salient_core_refs),
        "exit_dream_memory_tier_retrievable_context_ref_count": len(
            retrievable_context_refs
        ),
        "exit_dream_memory_tier_deep_sediment_ref_count": len(deep_sediment_refs),
        "exit_dream_memory_tier_carrier_refs": carrier_refs,
        "exit_dream_memory_tier_deep_sediment_policy": deep_sediment_policy,
        "exit_dream_memory_tier_fact_boundary": fact_boundary,
        "exit_dream_memory_tier_report_boundary": (
            "tiered_report_evidence_not_spoken_language"
        ),
    }


def _queue_e_repair_modulation_profile_from_runtime(
    *,
    state_dir: Path,
    reports_dir: Path,
    responsibility_loop_state_ref: str | None,
    world_contact_summary_ref: str | None,
    pain_regret_repair_report_ref: str | None,
) -> dict[str, Any]:
    responsibility_loop_state = _read_json_if_exists(
        state_dir / "action" / "responsibility_loop_state.json"
    )
    world_contact_summary = _read_json_if_exists(
        state_dir / "membrane" / "world_contact_summary.json"
    )
    pain_regret_repair_report = _read_json_if_exists(
        reports_dir / "pain_regret_repair_report.json"
    )
    if not any(
        [
            responsibility_loop_state,
            world_contact_summary,
            pain_regret_repair_report,
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
    ):
        return {}
    return build_queue_e_repair_modulation_profile(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )


def _identity_consciousness_birth_refs(idle_governance: dict[str, Any]) -> list[str]:
    return [
        ref
        for ref in [
            idle_governance.get("workspace_frame_ref"),
            idle_governance.get("broadcast_frame_ref"),
            idle_governance.get("metacognition_ref"),
            idle_governance.get("consciousness_probe_ref"),
            idle_governance.get("birth_readiness_rollup_ref"),
            idle_governance.get("birth_readiness_stage_gate_ref"),
        ]
        if ref
    ]


def _apply_resident_process_identity_profile(
    artifact: dict[str, Any],
    *,
    resident_process_lease_history_profile: dict[str, Any],
    resident_process_lease_history_profile_ref: str | None,
) -> None:
    if not resident_process_lease_history_profile and not resident_process_lease_history_profile_ref:
        return
    if resident_process_lease_history_profile_ref:
        artifact["resident_process_lease_history_profile_ref"] = (
            resident_process_lease_history_profile_ref
        )
        artifact["background_resident_process_lease_history_profile_ref"] = (
            resident_process_lease_history_profile_ref
        )
    if resident_process_lease_history_profile:
        artifact["resident_process_identity_continuity_state"] = str(
            resident_process_lease_history_profile.get(
                "current_identity_continuity_state",
                "no_lease_history",
            )
        )
        artifact["resident_process_identity_pressure_level"] = str(
            resident_process_lease_history_profile.get("identity_pressure_level", "light")
        )
        artifact["resident_process_lease_history_event_count"] = _int_or_default(
            resident_process_lease_history_profile.get("history_event_count"),
            default=0,
        )
        artifact["resident_process_recent_ids"] = _list_or_empty(
            resident_process_lease_history_profile.get("recent_resident_process_ids")
        )
        artifact["resident_process_recent_run_ids"] = _list_or_empty(
            resident_process_lease_history_profile.get("recent_run_ids")
        )


def _trait_convergence_report_carrier(
    *,
    idle_governance: dict[str, Any],
    resident_governance_state_ref: str | None,
    trait_drift_monitor_ref: str | None,
    background_convergence_summary_ref: str | None,
    background_convergence_history_ref: str | None,
) -> dict[str, Any]:
    carrier = dict(idle_governance)
    if resident_governance_state_ref:
        carrier.setdefault(
            "background_resident_governance_state_ref",
            resident_governance_state_ref,
        )
    carrier.setdefault(
        "background_resident_governance_explanation_ref",
        RESIDENT_GOVERNANCE_EXPLANATION_REF,
    )
    if trait_drift_monitor_ref:
        carrier.setdefault("background_trait_drift_monitor_ref", trait_drift_monitor_ref)
    if background_convergence_summary_ref:
        carrier.setdefault(
            "background_convergence_summary_ref",
            background_convergence_summary_ref,
        )
    if background_convergence_history_ref:
        carrier.setdefault(
            "background_convergence_history_ref",
            background_convergence_history_ref,
        )
    return carrier


def _dedupe_refs(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _int_or_default(value: Any, *, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _list_or_empty(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dict_or_empty(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _first_non_none(*values: Any) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


def _bool_or_none(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    return bool(value)


def _relationship_resume_summary(
    relationship_graph: dict[str, Any] | None,
) -> dict[str, Any]:
    subjects = (relationship_graph or {}).get("subjects", [])
    if not subjects or not isinstance(subjects[0], dict):
        return {}
    subject = subjects[0]
    relationship_stage = str(subject.get("relationship_stage", "") or "")
    if not relationship_stage:
        return {}
    summary = {
        "relationship_id": subject.get("relationship_id"),
        "relation_role": subject.get("relation_role"),
        "relationship_stage": relationship_stage,
        "relationship_stage_reason": subject.get("relationship_stage_reason"),
        "relationship_stage_turn_count": subject.get("relationship_stage_turn_count"),
        "relationship_stage_evidence_refs": subject.get("relationship_stage_evidence_refs"),
    }
    return {
        key: value
        for key, value in summary.items()
        if value is not None and value != "" and value != []
    }


def _trait_slow_variable_summary(
    self_model_state: dict[str, Any] | None,
) -> dict[str, Any]:
    trait_slow_variables = (self_model_state or {}).get("trait_slow_variables", {})
    if not isinstance(trait_slow_variables, dict):
        return {}
    summary: dict[str, Any] = {}
    for name, payload in trait_slow_variables.items():
        if isinstance(payload, dict):
            summary[name] = {
                key: payload[key]
                for key in [
                    "value",
                    "trend",
                    "update_count",
                    "last_relationship_stage",
                    "last_generated_at",
                    "evidence_refs",
                ]
                if key in payload
            }
        elif isinstance(payload, (int, float)):
            summary[name] = {"value": float(payload)}
    return summary
