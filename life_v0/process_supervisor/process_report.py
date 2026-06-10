from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .governance_explanation import (
    RESIDENT_GOVERNANCE_EXPLANATION_REF,
    write_resident_governance_explanation,
)
from .idle_strategy import extract_idle_governance_fields


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
    relationship_graph: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> ProcessReportBundleResult:
    idle_governance = extract_idle_governance_fields(idle_strategy_state)
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    identity_consciousness_birth_refs = _identity_consciousness_birth_refs(idle_governance)
    relationship_resume_summary = _relationship_resume_summary(relationship_graph)
    trait_slow_variable_summary = _trait_slow_variable_summary(self_model_state)
    prediction_write_gate_refs = _prediction_write_gate_refs(
        signal_media_runtime_ref=signal_media_runtime_ref,
        belief_state_ref=belief_state_ref,
        prediction_error_field_ref=prediction_error_field_ref,
        active_sampling_plan_ref=active_sampling_plan_ref,
        memory_write_gate_ref=memory_write_gate_ref,
        state_merge_guard_ref=state_merge_guard_ref,
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
        "life_context_frame_ref": life_context_frame_ref,
        "relation_turn_frame_ref": relation_turn_frame_ref,
        "expression_plan_ref": expression_plan_ref,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "dialogue_writeback_bundle_ref": dialogue_writeback_bundle_ref,
        "replay_cue_bundle_ref": replay_cue_bundle_ref,
        "offline_consolidation_frame_ref": offline_consolidation_frame_ref,
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
        "state_merge_guard_ref": state_merge_guard_ref,
        "prediction_write_gate_refs": prediction_write_gate_refs,
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
    report.update(idle_governance)
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
                growth_patch_candidate_queue_ref,
                nightmare_risk_ref,
                belief_learning_plan_ref,
                language_learning_plan_ref,
                relationship_learning_plan_ref,
            ]
            if ref
        ],
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
        "prediction_write_gate_refs": prediction_write_gate_refs,
    }
    if membrane_guard_refs:
        digest["membrane_guard_refs"] = membrane_guard_refs
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
        life_context_frame_ref=life_context_frame_ref,
        relation_turn_frame_ref=relation_turn_frame_ref,
        expression_plan_ref=expression_plan_ref,
        relationship_timeline_ref=relationship_timeline_ref,
        commitment_expression_plan_ref=commitment_expression_plan_ref,
        apology_repair_language_trace_ref=apology_repair_language_trace_ref,
        dialogue_writeback_bundle_ref=dialogue_writeback_bundle_ref,
        replay_cue_bundle_ref=replay_cue_bundle_ref,
        offline_consolidation_frame_ref=offline_consolidation_frame_ref,
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
        idle_heartbeat_trace_ref=idle_governance.get("idle_heartbeat_trace_ref"),
        workspace_frame_ref=idle_governance.get("workspace_frame_ref"),
        broadcast_frame_ref=idle_governance.get("broadcast_frame_ref"),
        metacognition_ref=idle_governance.get("metacognition_ref"),
        consciousness_probe_ref=idle_governance.get("consciousness_probe_ref"),
        birth_readiness_rollup_ref=idle_governance.get("birth_readiness_rollup_ref"),
        birth_readiness_stage_gate_ref=idle_governance.get("birth_readiness_stage_gate_ref"),
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
    life_context_frame_ref: str | None,
    relation_turn_frame_ref: str | None,
    expression_plan_ref: str | None,
    relationship_timeline_ref: str | None,
    commitment_expression_plan_ref: str | None,
    apology_repair_language_trace_ref: str | None,
    dialogue_writeback_bundle_ref: str | None,
    replay_cue_bundle_ref: str | None,
    offline_consolidation_frame_ref: str | None,
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
    idle_heartbeat_trace_ref: str | None = None,
    workspace_frame_ref: str | None = None,
    broadcast_frame_ref: str | None = None,
    metacognition_ref: str | None = None,
    consciousness_probe_ref: str | None = None,
    birth_readiness_rollup_ref: str | None = None,
    birth_readiness_stage_gate_ref: str | None = None,
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        reports_dir / "digital_life_shell_report.json",
        state_dir / "terminal" / "session_envelope.json",
        state_dir / "terminal" / "safe_terminal_loop_state.json",
        state_dir / "terminal" / "terminal_life_loop_state.json",
        state_dir / "terminal" / "idle_strategy_state.json",
        state_dir / "terminal" / "idle_heartbeat_trace.jsonl",
        state_dir / "terminal" / "resident_governance_state.json",
        state_dir / "terminal" / "life_context_frame.json",
        state_dir / "terminal" / "relation_turn_frame.json",
        state_dir / "language" / "dialogue_turn_log.jsonl",
        state_dir / "language" / "self_narrative_language_trace.json",
        state_dir / "language" / "commitment_repair_language_index.json",
        state_dir / "language" / "expression_plan.json",
        state_dir / "action" / "responsibility_loop_state.json",
        state_dir / "membrane" / "world_contact_summary.json",
        state_dir / "signal" / "signal_media_runtime.json",
        state_dir / "prediction" / "belief_state_frame.json",
        state_dir / "prediction" / "prediction_error_field.json",
        state_dir / "prediction" / "active_sampling_plan.json",
        state_dir / "consciousness" / "workspace_frame.json",
        state_dir / "consciousness" / "broadcast_frame.json",
        state_dir / "consciousness" / "metacognition_state.json",
        state_dir / "consciousness" / "consciousness_probe_bundle.json",
        state_dir / "life_targets" / "birth_readiness_rollup.json",
        state_dir / "life_targets" / "birth_readiness_stage_gate.json",
        state_dir / "memory" / "memory_write_gate.json",
        state_dir / "memory" / "state_merge_guard.json",
        state_dir / "body" / "trait_drift_monitor.json",
        state_dir / "terminal" / "background_convergence_summary.json",
        state_dir / "terminal" / "background_convergence_history.json",
        state_dir / "replay" / "replay_cue_bundle.json",
        state_dir / "dream" / "offline_consolidation_frame.json",
        state_dir / "dream" / "nightmare_loop_risk.json",
        state_dir / "growth" / "growth_patch_candidate_queue.json",
        state_dir / "growth" / "belief_learning_plan.json",
        state_dir / "growth" / "language_learning_plan.json",
        state_dir / "growth" / "relationship_learning_plan.json",
        state_dir / "relationship" / "relationship_subject_graph.json",
        state_dir / "self" / "self_model.json",
        reports_dir / "pain_regret_repair_report.json",
        reports_dir / "dialogue_writeback_bundle.json",
        reports_dir / "digital_life_process_relaunch_recovery_report.json",
        reports_dir / "digital_life_process_incident_report.json",
        reports_dir / "digital_life_process_recovery_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = sha256(path)

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
    return {
        "schema_version": "digital_life_process_receipt_v0",
        "receipt_id": f"digital_life_process_{run_id}",
        "run_id": run_id,
        "command": "digital life",
        "report_refs": [
            "runtime/reports/latest/digital_life_resident_governance_explanation.json",
            "runtime/reports/latest/digital_life_process_report.json",
            "runtime/reports/latest/digital_life_process_digest.json",
        ],
        "shared_object_refs": [
            ref
            for ref in [
                idle_strategy_ref,
                idle_heartbeat_trace_ref,
                resident_governance_state_ref,
                resident_governance_snapshot_ref,
                resident_governance_explanation_ref,
                life_context_frame_ref,
                relation_turn_frame_ref,
                expression_plan_ref,
                relationship_timeline_ref,
                commitment_expression_plan_ref,
                apology_repair_language_trace_ref,
                dialogue_writeback_bundle_ref,
                replay_cue_bundle_ref,
                offline_consolidation_frame_ref,
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
                workspace_frame_ref,
                broadcast_frame_ref,
                metacognition_ref,
                consciousness_probe_ref,
                birth_readiness_rollup_ref,
                birth_readiness_stage_gate_ref,
                relationship_graph_ref,
                self_model_ref,
            ]
            if ref
        ],
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
