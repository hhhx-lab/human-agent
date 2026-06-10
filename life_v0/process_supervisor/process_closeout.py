from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .persistent_process import (
    BACKGROUND_CONVERGENCE_HISTORY_REF,
    BACKGROUND_CONVERGENCE_SUMMARY_REF,
    PERSISTENT_PROCESS_REPORT_REF,
    RESIDENT_GOVERNANCE_REPORT_REF,
    RESIDENT_GOVERNANCE_STATE_REF,
    RESIDENT_GOVERNANCE_SNAPSHOT_REF,
    TRAIT_DRIFT_MONITOR_REF,
    PersistentProcessArtifactsResult,
    write_persistent_process_artifacts,
)
from .process_report import ProcessReportBundleResult, write_process_report_bundle


LIFE_CONTEXT_FRAME_REF = "runtime/state/terminal/life_context_frame.json"
RELATION_TURN_FRAME_REF = "runtime/state/terminal/relation_turn_frame.json"
EXPRESSION_PLAN_REF = "runtime/state/language/expression_plan.json"
RELATIONSHIP_TIMELINE_REF = "runtime/state/relationship/relationship_timeline.json"
COMMITMENT_EXPRESSION_PLAN_REF = "runtime/state/language/commitment_expression_plan.json"
APOLOGY_REPAIR_LANGUAGE_TRACE_REF = "runtime/state/language/apology_repair_language_trace.json"
DIALOGUE_WRITEBACK_BUNDLE_REF = "runtime/reports/latest/dialogue_writeback_bundle.json"


@dataclass(frozen=True)
class ProcessCloseoutResult:
    persistent_process_artifacts: PersistentProcessArtifactsResult
    report_bundle: ProcessReportBundleResult


def close_digital_life_process(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    heartbeat_counter: int,
    completed_turns: int,
    incident_count: int,
    relaunch_recovery_count: int,
    exit_reason: str,
    last_incident_report_ref: str | None,
    last_recovery_report_ref: str | None,
    last_relaunch_recovery_report_ref: str | None,
    last_external_turn: dict[str, Any] | None,
    last_life_turn: dict[str, Any] | None,
    waiting_mode: str,
    idle_strategy_ref: str | None,
    idle_strategy_state: dict[str, Any] | None,
    last_heartbeat_packet_ref: str | None,
    last_dialogue_packet_ref: str | None,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    life_context_frame: dict[str, Any],
    relation_turn_frame: dict[str, Any],
    expression_plan: dict[str, Any],
    relationship_timeline: dict[str, Any],
    commitment_expression_plan: dict[str, Any],
    apology_repair_language_trace: dict[str, Any],
    replay_cue_bundle_ref: str | None,
    offline_consolidation_frame_ref: str | None,
    dream_experience_window_ref: str | None = None,
    wake_integration_frame_ref: str | None = None,
    dream_fact_gate_decision_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None = None,
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
    write_json: Callable[[Path, dict[str, Any]], None],
    relationship_graph: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
) -> ProcessCloseoutResult:
    if (
        trait_drift_monitor_ref is None
        and (state_dir / "body" / "trait_drift_monitor.json").exists()
    ):
        trait_drift_monitor_ref = TRAIT_DRIFT_MONITOR_REF
    if (
        background_convergence_summary_ref is None
        and (state_dir / "terminal" / "background_convergence_summary.json").exists()
    ):
        background_convergence_summary_ref = BACKGROUND_CONVERGENCE_SUMMARY_REF
    if (
        background_convergence_history_ref is None
        and (state_dir / "terminal" / "background_convergence_history.json").exists()
    ):
        background_convergence_history_ref = BACKGROUND_CONVERGENCE_HISTORY_REF
    persistent_process_artifacts = write_persistent_process_artifacts(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        heartbeat_counter=heartbeat_counter,
        completed_turns=completed_turns,
        incident_count=incident_count,
        relaunch_recovery_count=relaunch_recovery_count,
        waiting_mode=waiting_mode,
        idle_strategy_ref=idle_strategy_ref,
        idle_strategy_state=idle_strategy_state,
        last_heartbeat_packet_ref=last_heartbeat_packet_ref,
        last_dialogue_packet_ref=last_dialogue_packet_ref,
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
        relationship_timeline_ref=_ref_if_present(
            payload=relationship_timeline,
            ref=RELATIONSHIP_TIMELINE_REF,
        ),
        commitment_expression_plan_ref=_ref_if_present(
            payload=commitment_expression_plan,
            ref=COMMITMENT_EXPRESSION_PLAN_REF,
        ),
        apology_repair_language_trace_ref=_ref_if_present(
            payload=apology_repair_language_trace,
            ref=APOLOGY_REPAIR_LANGUAGE_TRACE_REF,
        ),
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
        trait_drift_monitor_ref=trait_drift_monitor_ref,
        background_convergence_summary_ref=background_convergence_summary_ref,
        background_convergence_history_ref=background_convergence_history_ref,
        relationship_graph=relationship_graph,
        self_model_state=self_model_state,
        write_json=write_json,
    )

    report_bundle = write_process_report_bundle(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
        completed_turns=completed_turns,
        incident_count=incident_count,
        relaunch_recovery_count=relaunch_recovery_count,
        heartbeat_counter=heartbeat_counter,
        exit_reason=exit_reason,
        last_incident_report_ref=last_incident_report_ref,
        last_recovery_report_ref=last_recovery_report_ref,
        last_relaunch_recovery_report_ref=last_relaunch_recovery_report_ref,
        last_external_turn=last_external_turn,
        last_life_turn=last_life_turn,
        idle_strategy_ref=idle_strategy_ref,
        idle_strategy_state=idle_strategy_state,
        persistent_process_report_ref=PERSISTENT_PROCESS_REPORT_REF,
        resident_governance_report_ref=RESIDENT_GOVERNANCE_REPORT_REF,
        resident_governance_state_ref=RESIDENT_GOVERNANCE_STATE_REF,
        resident_governance_snapshot_ref=RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        life_context_frame_ref=_ref_if_present(
            payload=life_context_frame,
            ref=LIFE_CONTEXT_FRAME_REF,
        ),
        relation_turn_frame_ref=_ref_if_present(
            payload=relation_turn_frame,
            ref=RELATION_TURN_FRAME_REF,
        ),
        expression_plan_ref=_ref_if_present(
            payload=expression_plan,
            ref=EXPRESSION_PLAN_REF,
        ),
        relationship_timeline_ref=_ref_if_present(
            payload=relationship_timeline,
            ref=RELATIONSHIP_TIMELINE_REF,
        ),
        commitment_expression_plan_ref=_ref_if_present(
            payload=commitment_expression_plan,
            ref=COMMITMENT_EXPRESSION_PLAN_REF,
        ),
        apology_repair_language_trace_ref=_ref_if_present(
            payload=apology_repair_language_trace,
            ref=APOLOGY_REPAIR_LANGUAGE_TRACE_REF,
        ),
        dialogue_writeback_bundle_ref=_report_ref_if_exists(
            path=reports_dir / "dialogue_writeback_bundle.json",
            ref=DIALOGUE_WRITEBACK_BUNDLE_REF,
        ),
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
        state_merge_guard_ref=state_merge_guard_ref,
        trait_drift_monitor_ref=trait_drift_monitor_ref,
        background_convergence_summary_ref=background_convergence_summary_ref,
        background_convergence_history_ref=background_convergence_history_ref,
        relationship_graph=relationship_graph,
        self_model_state=self_model_state,
        write_json=write_json,
    )
    return ProcessCloseoutResult(
        persistent_process_artifacts=persistent_process_artifacts,
        report_bundle=report_bundle,
    )


def _ref_if_present(*, payload: dict[str, Any], ref: str) -> str | None:
    if not payload:
        return None
    return ref


def _report_ref_if_exists(*, path: Path, ref: str) -> str | None:
    if not path.exists():
        return None
    return ref
