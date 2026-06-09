from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .idle_strategy import extract_idle_governance_fields


PERSISTENT_PROCESS_STATE_REF = "runtime/state/terminal/persistent_process_state.json"
PERSISTENT_PROCESS_REPORT_REF = "runtime/reports/latest/digital_life_persistent_process_report.json"
RESIDENT_GOVERNANCE_SNAPSHOT_REF = "runtime/state/terminal/resident_governance_snapshot.json"
RESIDENT_GOVERNANCE_REPORT_REF = "runtime/reports/latest/digital_life_resident_governance_report.json"


@dataclass(frozen=True)
class PersistentProcessArtifactsResult:
    state: dict[str, Any]
    report: dict[str, Any]
    resident_governance_snapshot: dict[str, Any]
    resident_governance_report: dict[str, Any]


def write_persistent_process_artifacts(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    heartbeat_counter: int,
    completed_turns: int,
    incident_count: int,
    relaunch_recovery_count: int,
    waiting_mode: str,
    idle_strategy_ref: str | None,
    idle_strategy_state: dict[str, Any] | None,
    last_heartbeat_packet_ref: str | None,
    last_dialogue_packet_ref: str | None,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    relationship_timeline_ref: str | None,
    commitment_expression_plan_ref: str | None,
    apology_repair_language_trace_ref: str | None,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> PersistentProcessArtifactsResult:
    terminal_dir = state_dir / "terminal"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    idle_governance = extract_idle_governance_fields(idle_strategy_state)

    resident_governance_snapshot = {
        "schema_version": "resident_governance_snapshot_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "foreground_terminal_residency",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "next_required_action": "await_process_relaunch_or_new_terminal_wake",
    }
    resident_governance_snapshot.update(idle_governance)
    state = {
        "schema_version": "persistent_process_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "foreground_terminal_residency",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "next_required_action": "await_process_relaunch_or_new_terminal_wake",
    }
    state.update(idle_governance)
    report = {
        "schema_version": "digital_life_persistent_process_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "foreground_terminal_residency",
        "persistent_process_state_ref": PERSISTENT_PROCESS_STATE_REF,
        "resident_governance_report_ref": RESIDENT_GOVERNANCE_REPORT_REF,
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }
    report.update(idle_governance)
    resident_governance_report = {
        "schema_version": "digital_life_resident_governance_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "foreground_terminal_residency",
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "persistent_process_state_ref": PERSISTENT_PROCESS_STATE_REF,
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }
    resident_governance_report.update(idle_governance)

    write_json(terminal_dir / "resident_governance_snapshot.json", resident_governance_snapshot)
    write_json(terminal_dir / "persistent_process_state.json", state)
    write_json(reports_dir / "digital_life_resident_governance_report.json", resident_governance_report)
    write_json(reports_dir / "digital_life_persistent_process_report.json", report)
    return PersistentProcessArtifactsResult(
        state=state,
        report=report,
        resident_governance_snapshot=resident_governance_snapshot,
        resident_governance_report=resident_governance_report,
    )
