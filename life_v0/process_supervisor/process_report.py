from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

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
    write_json: Callable[[Path, dict[str, Any]], None],
) -> ProcessReportBundleResult:
    idle_governance = extract_idle_governance_fields(idle_strategy_state)
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
        "resident_governance_snapshot_ref": resident_governance_snapshot_ref,
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
        "next_required_action": "process_closed_waiting_relaunch",
        "blocked_reasons": [],
    }
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
        "exit_reason": exit_reason,
        "last_external_turn_utterance": None if last_external_turn is None else last_external_turn["utterance"],
        "dialogue_writeback_bundle_ref": dialogue_writeback_bundle_ref,
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
            ]
            if ref
        ],
    }
    receipt = build_process_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        idle_strategy_ref=idle_strategy_ref,
        resident_governance_snapshot_ref=resident_governance_snapshot_ref,
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
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        reports_dir / "digital_life_shell_report.json",
        state_dir / "terminal" / "session_envelope.json",
        state_dir / "terminal" / "safe_terminal_loop_state.json",
        state_dir / "terminal" / "terminal_life_loop_state.json",
        state_dir / "terminal" / "idle_strategy_state.json",
        state_dir / "terminal" / "life_context_frame.json",
        state_dir / "terminal" / "relation_turn_frame.json",
        state_dir / "language" / "dialogue_turn_log.jsonl",
        state_dir / "language" / "self_narrative_language_trace.json",
        state_dir / "language" / "commitment_repair_language_index.json",
        state_dir / "language" / "expression_plan.json",
        state_dir / "replay" / "replay_cue_bundle.json",
        state_dir / "dream" / "offline_consolidation_frame.json",
        state_dir / "growth" / "growth_patch_candidate_queue.json",
        state_dir / "relationship" / "relationship_subject_graph.json",
        reports_dir / "dialogue_writeback_bundle.json",
        reports_dir / "digital_life_process_relaunch_recovery_report.json",
        reports_dir / "digital_life_process_incident_report.json",
        reports_dir / "digital_life_process_recovery_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = sha256(path)

    output_paths = [
        reports_dir / "digital_life_process_report.json",
        reports_dir / "digital_life_process_digest.json",
        receipts_dir / f"digital_life_process_{run_id}.json",
    ]
    return {
        "schema_version": "digital_life_process_receipt_v0",
        "receipt_id": f"digital_life_process_{run_id}",
        "run_id": run_id,
        "command": "digital life",
        "report_refs": [
            "runtime/reports/latest/digital_life_process_report.json",
            "runtime/reports/latest/digital_life_process_digest.json",
        ],
        "shared_object_refs": [
            ref
            for ref in [
                idle_strategy_ref,
                resident_governance_snapshot_ref,
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
