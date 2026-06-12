from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .background_lineage_state import build_resident_background_lineage_state
from .governance_explanation import RESIDENT_GOVERNANCE_EXPLANATION_REF
from .handoff_profile import previous_handoff_profile_fields, select_handoff_profile
from .idle_strategy import extract_idle_governance_fields
from .state_merge_signals import state_merge_long_term_change_profile
from .trait_convergence_signals import cross_wake_trait_convergence_profile


PERSISTENT_PROCESS_STATE_REF = "runtime/state/terminal/persistent_process_state.json"
PERSISTENT_PROCESS_REPORT_REF = "runtime/reports/latest/digital_life_persistent_process_report.json"
RESIDENT_GOVERNANCE_STATE_REF = "runtime/state/terminal/resident_governance_state.json"
BACKGROUND_CONVERGENCE_SUMMARY_REF = (
    "runtime/state/terminal/background_convergence_summary.json"
)
BACKGROUND_CONVERGENCE_HISTORY_REF = (
    "runtime/state/terminal/background_convergence_history.json"
)
RESIDENT_GOVERNANCE_SNAPSHOT_REF = "runtime/state/terminal/resident_governance_snapshot.json"
RESIDENT_GOVERNANCE_REPORT_REF = "runtime/reports/latest/digital_life_resident_governance_report.json"
RELATIONSHIP_SUBJECT_GRAPH_REF = "runtime/state/relationship/relationship_subject_graph.json"
SELF_MODEL_REF = "runtime/state/self/self_model.json"
TRAIT_DRIFT_MONITOR_REF = "runtime/state/body/trait_drift_monitor.json"
STATE_MERGE_GUARD_REF = "runtime/state/memory/state_merge_guard.json"
RESIDENT_PROCESS_LEASE_REF = "runtime/state/terminal/resident_process_lease.json"
RESIDENT_PROCESS_LEASE_HISTORY_REF = "runtime/state/terminal/resident_process_lease_history.jsonl"
RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF = (
    "runtime/state/terminal/resident_process_lease_history_profile.json"
)


@dataclass(frozen=True)
class PersistentProcessArtifactsResult:
    state: dict[str, Any]
    report: dict[str, Any]
    resident_governance_state: dict[str, Any]
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
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
    state_merge_guard_ref: str | None = None,
    trait_drift_monitor_ref: str | None = None,
    background_convergence_summary_ref: str | None = None,
    background_convergence_history_ref: str | None = None,
    resident_process_lease_ref: str | None = None,
    resident_process_lease_history_ref: str | None = None,
    write_json: Callable[[Path, dict[str, Any]], None],
    relationship_graph: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
) -> PersistentProcessArtifactsResult:
    terminal_dir = state_dir / "terminal"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    terminal_life_loop_state = _read_json_if_exists(
        terminal_dir / "terminal_life_loop_state.json"
    )
    previous_resident_governance_state = _read_json_if_exists(
        terminal_dir / "resident_governance_state.json"
    )
    handoff_carry_fields = previous_handoff_profile_fields(
        select_handoff_profile(
            idle_strategy_state,
            terminal_life_loop_state,
            previous_resident_governance_state,
        ),
        carry_status="carried_into_process_closeout",
    )
    if handoff_carry_fields:
        idle_strategy_state = dict(idle_strategy_state or {})
        idle_strategy_state.update(handoff_carry_fields)
    if resident_process_lease_ref is None and (
        terminal_dir / "resident_process_lease.json"
    ).exists():
        resident_process_lease_ref = RESIDENT_PROCESS_LEASE_REF
    if resident_process_lease_history_ref is None and (
        terminal_dir / "resident_process_lease_history.jsonl"
    ).exists():
        resident_process_lease_history_ref = RESIDENT_PROCESS_LEASE_HISTORY_REF
    resident_process_lease_history_profile_ref = (
        RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF
        if (terminal_dir / "resident_process_lease_history_profile.json").exists()
        else None
    )
    resident_process_lease = _read_json_if_exists(terminal_dir / "resident_process_lease.json")
    resident_process_lease_history_profile = _read_json_if_exists(
        terminal_dir / "resident_process_lease_history_profile.json"
    )
    resident_process_id = resident_process_lease.get("resident_process_id")
    if not isinstance(resident_process_id, str) or not resident_process_id:
        resident_process_id = None
    idle_governance = extract_idle_governance_fields(idle_strategy_state)
    idle_governance.update(
        cross_wake_trait_convergence_profile(
            _trait_convergence_closeout_carrier(
                idle_governance=idle_governance,
                trait_drift_monitor_ref=trait_drift_monitor_ref,
                background_convergence_summary_ref=background_convergence_summary_ref,
                background_convergence_history_ref=background_convergence_history_ref,
            )
        )
    )
    current_background_ref_set = [
        RESIDENT_GOVERNANCE_STATE_REF,
        RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        RESIDENT_GOVERNANCE_REPORT_REF,
        PERSISTENT_PROCESS_REPORT_REF,
    ]
    if background_convergence_summary_ref:
        current_background_ref_set.insert(1, background_convergence_summary_ref)
    if background_convergence_history_ref:
        current_background_ref_set.insert(2, background_convergence_history_ref)
    if resident_process_lease_history_profile_ref:
        current_background_ref_set.append(resident_process_lease_history_profile_ref)
    background_source_ref_set = [
        str(ref)
        for ref in idle_governance.get("background_continuity_ref_set", [])
        if ref
    ]
    background_parent_run_id = idle_governance.get("background_carryover_parent_run_id")
    background_carryover_generation = _next_background_carryover_generation(idle_governance)
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    relationship_resume_summary = _relationship_resume_summary(relationship_graph)
    trait_slow_variable_summary = _trait_slow_variable_summary(self_model_state)
    background_resume_summary = _background_resume_summary(
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        current_background_ref_set=current_background_ref_set,
        background_source_ref_set=background_source_ref_set,
    )
    state_merge_guard = _read_json_if_exists(state_dir / "memory" / "state_merge_guard.json")
    state_merge_profile = _state_merge_closeout_profile(
        state_merge_guard=state_merge_guard,
        state_merge_guard_ref=state_merge_guard_ref
        or (STATE_MERGE_GUARD_REF if state_merge_guard else None),
    )

    resident_governance_snapshot = {
        "schema_version": "resident_governance_snapshot_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "background_resident_continuity",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "resident_process_lease_ref": resident_process_lease_ref,
        "resident_process_lease_history_ref": resident_process_lease_history_ref,
        "resident_process_id": resident_process_id,
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "next_required_action": "await_process_relaunch_or_new_terminal_wake",
        "background_continuity_mode": "closed_process_carryover",
        "background_continuity_ref_set": list(current_background_ref_set),
        "background_carryover_generation": background_carryover_generation,
    }
    if background_source_ref_set:
        resident_governance_snapshot["background_carryover_source_ref_set"] = list(
            background_source_ref_set
        )
    if background_parent_run_id:
        resident_governance_snapshot["background_carryover_parent_run_id"] = str(
            background_parent_run_id
        )
    if membrane_guard_refs:
        resident_governance_snapshot["membrane_guard_refs"] = membrane_guard_refs
    if trait_drift_monitor_ref:
        resident_governance_snapshot["trait_drift_monitor_ref"] = trait_drift_monitor_ref
    if background_convergence_summary_ref:
        resident_governance_snapshot["background_convergence_summary_ref"] = (
            background_convergence_summary_ref
        )
    if background_convergence_history_ref:
        resident_governance_snapshot["background_convergence_history_ref"] = (
            background_convergence_history_ref
        )
    _apply_background_resume_fields(
        resident_governance_snapshot,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    resident_governance_snapshot.update(state_merge_profile)
    resident_governance_snapshot.update(_idle_governance_without_background_lineage(idle_governance))
    _apply_resident_process_identity_profile(
        resident_governance_snapshot,
        resident_process_lease_history_profile=resident_process_lease_history_profile,
        resident_process_lease_history_profile_ref=resident_process_lease_history_profile_ref,
    )
    _attach_resident_background_lineage_state(
        resident_governance_snapshot,
        governance_phase="process_closed_waiting_relaunch",
        status="closed",
    )
    resident_governance_state = {
        "schema_version": "resident_governance_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "background_resident_continuity",
        "governance_phase": "process_closed_waiting_relaunch",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "resident_governance_report_ref": RESIDENT_GOVERNANCE_REPORT_REF,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "resident_process_lease_ref": resident_process_lease_ref,
        "resident_process_lease_history_ref": resident_process_lease_history_ref,
        "resident_process_id": resident_process_id,
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
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
        "next_required_action": "await_process_relaunch_or_new_terminal_wake",
        "background_continuity_mode": "closed_process_carryover",
        "background_continuity_ref_set": list(current_background_ref_set),
        "background_carryover_generation": background_carryover_generation,
    }
    if background_source_ref_set:
        resident_governance_state["background_carryover_source_ref_set"] = list(
            background_source_ref_set
        )
    if background_parent_run_id:
        resident_governance_state["background_carryover_parent_run_id"] = str(
            background_parent_run_id
        )
    if responsibility_loop_state_ref:
        resident_governance_state["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        resident_governance_state["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        resident_governance_state["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        resident_governance_state["membrane_guard_refs"] = membrane_guard_refs
    if trait_drift_monitor_ref:
        resident_governance_state["trait_drift_monitor_ref"] = trait_drift_monitor_ref
    if background_convergence_summary_ref:
        resident_governance_state["background_convergence_summary_ref"] = (
            background_convergence_summary_ref
        )
    if background_convergence_history_ref:
        resident_governance_state["background_convergence_history_ref"] = (
            background_convergence_history_ref
        )
    _apply_background_resume_fields(
        resident_governance_state,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    resident_governance_state.update(state_merge_profile)
    resident_governance_state.update(_idle_governance_without_background_lineage(idle_governance))
    _apply_resident_process_identity_profile(
        resident_governance_state,
        resident_process_lease_history_profile=resident_process_lease_history_profile,
        resident_process_lease_history_profile_ref=resident_process_lease_history_profile_ref,
    )
    _attach_resident_background_lineage_state(
        resident_governance_state,
        governance_phase="process_closed_waiting_relaunch",
        status="closed",
    )
    state = {
        "schema_version": "persistent_process_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "background_resident_continuity",
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "resident_governance_state_ref": RESIDENT_GOVERNANCE_STATE_REF,
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "resident_process_lease_ref": resident_process_lease_ref,
        "resident_process_lease_history_ref": resident_process_lease_history_ref,
        "resident_process_id": resident_process_id,
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "next_required_action": "await_process_relaunch_or_new_terminal_wake",
        "background_continuity_mode": "closed_process_carryover",
        "background_continuity_ref_set": list(current_background_ref_set),
        "background_carryover_generation": background_carryover_generation,
    }
    if background_source_ref_set:
        state["background_carryover_source_ref_set"] = list(background_source_ref_set)
    if background_parent_run_id:
        state["background_carryover_parent_run_id"] = str(background_parent_run_id)
    if responsibility_loop_state_ref:
        state["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        state["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        state["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        state["membrane_guard_refs"] = membrane_guard_refs
    if trait_drift_monitor_ref:
        state["trait_drift_monitor_ref"] = trait_drift_monitor_ref
    if background_convergence_summary_ref:
        state["background_convergence_summary_ref"] = background_convergence_summary_ref
    if background_convergence_history_ref:
        state["background_convergence_history_ref"] = background_convergence_history_ref
    _apply_background_resume_fields(
        state,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    state.update(state_merge_profile)
    state.update(_idle_governance_without_background_lineage(idle_governance))
    _apply_resident_process_identity_profile(
        state,
        resident_process_lease_history_profile=resident_process_lease_history_profile,
        resident_process_lease_history_profile_ref=resident_process_lease_history_profile_ref,
    )
    _attach_resident_background_lineage_state(
        state,
        governance_phase="process_closed_waiting_relaunch",
        status="closed",
    )
    report = {
        "schema_version": "digital_life_persistent_process_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "background_resident_continuity",
        "persistent_process_state_ref": PERSISTENT_PROCESS_STATE_REF,
        "resident_governance_state_ref": RESIDENT_GOVERNANCE_STATE_REF,
        "resident_governance_report_ref": RESIDENT_GOVERNANCE_REPORT_REF,
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "safe_terminal_loop_state_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "terminal_life_loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "resident_process_lease_ref": resident_process_lease_ref,
        "resident_process_lease_history_ref": resident_process_lease_history_ref,
        "resident_process_id": resident_process_id,
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
        "background_continuity_mode": "closed_process_carryover",
        "background_continuity_ref_set": list(current_background_ref_set),
        "background_carryover_generation": background_carryover_generation,
    }
    if background_source_ref_set:
        report["background_carryover_source_ref_set"] = list(background_source_ref_set)
    if background_parent_run_id:
        report["background_carryover_parent_run_id"] = str(background_parent_run_id)
    if responsibility_loop_state_ref:
        report["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        report["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        report["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        report["membrane_guard_refs"] = membrane_guard_refs
    if trait_drift_monitor_ref:
        report["trait_drift_monitor_ref"] = trait_drift_monitor_ref
    if background_convergence_summary_ref:
        report["background_convergence_summary_ref"] = background_convergence_summary_ref
    if background_convergence_history_ref:
        report["background_convergence_history_ref"] = background_convergence_history_ref
    _apply_background_resume_fields(
        report,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    report.update(state_merge_profile)
    report.update(_idle_governance_without_background_lineage(idle_governance))
    _apply_resident_process_identity_profile(
        report,
        resident_process_lease_history_profile=resident_process_lease_history_profile,
        resident_process_lease_history_profile_ref=resident_process_lease_history_profile_ref,
    )
    _attach_resident_background_lineage_state(
        report,
        governance_phase="process_closed_waiting_relaunch",
        status="closed",
    )
    resident_governance_report = {
        "schema_version": "digital_life_resident_governance_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "governance_mode": "background_resident_continuity",
        "resident_governance_state_ref": RESIDENT_GOVERNANCE_STATE_REF,
        "resident_governance_snapshot_ref": RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        "persistent_process_state_ref": PERSISTENT_PROCESS_STATE_REF,
        "waiting_mode": waiting_mode,
        "heartbeat_counter": heartbeat_counter,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "idle_strategy_ref": idle_strategy_ref,
        "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
        "resident_process_lease_ref": resident_process_lease_ref,
        "resident_process_lease_history_ref": resident_process_lease_history_ref,
        "resident_process_id": resident_process_id,
        "last_heartbeat_packet_ref": last_heartbeat_packet_ref,
        "last_dialogue_packet_ref": last_dialogue_packet_ref,
        "relationship_timeline_ref": relationship_timeline_ref,
        "commitment_expression_plan_ref": commitment_expression_plan_ref,
        "apology_repair_language_trace_ref": apology_repair_language_trace_ref,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
        "background_continuity_mode": "closed_process_carryover",
        "background_continuity_ref_set": list(current_background_ref_set),
        "background_carryover_generation": background_carryover_generation,
    }
    if background_source_ref_set:
        resident_governance_report["background_carryover_source_ref_set"] = list(
            background_source_ref_set
        )
    if background_parent_run_id:
        resident_governance_report["background_carryover_parent_run_id"] = str(
            background_parent_run_id
        )
    if responsibility_loop_state_ref:
        resident_governance_report["responsibility_loop_state_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        resident_governance_report["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        resident_governance_report["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        resident_governance_report["membrane_guard_refs"] = membrane_guard_refs
    if trait_drift_monitor_ref:
        resident_governance_report["trait_drift_monitor_ref"] = trait_drift_monitor_ref
    if background_convergence_summary_ref:
        resident_governance_report["background_convergence_summary_ref"] = (
            background_convergence_summary_ref
        )
    if background_convergence_history_ref:
        resident_governance_report["background_convergence_history_ref"] = (
            background_convergence_history_ref
        )
    _apply_background_resume_fields(
        resident_governance_report,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    resident_governance_report.update(state_merge_profile)
    resident_governance_report.update(_idle_governance_without_background_lineage(idle_governance))
    _apply_resident_process_identity_profile(
        resident_governance_report,
        resident_process_lease_history_profile=resident_process_lease_history_profile,
        resident_process_lease_history_profile_ref=resident_process_lease_history_profile_ref,
    )
    _attach_resident_background_lineage_state(
        resident_governance_report,
        governance_phase="process_closed_waiting_relaunch",
        status="closed",
    )

    write_json(terminal_dir / "resident_governance_state.json", resident_governance_state)
    write_json(terminal_dir / "resident_governance_snapshot.json", resident_governance_snapshot)
    write_json(terminal_dir / "persistent_process_state.json", state)
    write_json(reports_dir / "digital_life_resident_governance_report.json", resident_governance_report)
    write_json(reports_dir / "digital_life_persistent_process_report.json", report)
    return PersistentProcessArtifactsResult(
        state=state,
        report=report,
        resident_governance_state=resident_governance_state,
        resident_governance_snapshot=resident_governance_snapshot,
        resident_governance_report=resident_governance_report,
    )


def _next_background_carryover_generation(idle_governance: dict[str, Any]) -> int:
    if idle_governance.get("background_continuity_mode"):
        current_generation = _int_or_default(
            idle_governance.get("background_carryover_generation"),
            default=1,
        )
        return max(current_generation + 1, 2)
    return 1


def _idle_governance_without_background_lineage(
    idle_governance: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: value
        for key, value in idle_governance.items()
        if key
        not in {
            "background_continuity_ref_set",
            "background_carryover_generation",
            "background_carryover_source_ref_set",
            "background_carryover_parent_run_id",
        }
    }


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _state_merge_closeout_profile(
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


def _trait_convergence_closeout_carrier(
    *,
    idle_governance: dict[str, Any],
    trait_drift_monitor_ref: str | None,
    background_convergence_summary_ref: str | None,
    background_convergence_history_ref: str | None,
) -> dict[str, Any]:
    carrier = dict(idle_governance)
    carrier.setdefault(
        "background_resident_governance_state_ref",
        RESIDENT_GOVERNANCE_STATE_REF,
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


def _attach_resident_background_lineage_state(
    artifact: dict[str, Any],
    *,
    governance_phase: str,
    status: str,
) -> None:
    lineage_state = build_resident_background_lineage_state(
        artifact,
        governance_phase=governance_phase,
        status=status,
    )
    if lineage_state:
        artifact["resident_background_lineage_state"] = lineage_state


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


def _int_or_default(value: Any, *, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _list_or_empty(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _relationship_resume_summary(
    relationship_graph: dict[str, Any] | None,
) -> dict[str, Any]:
    subjects = (relationship_graph or {}).get("subjects", [])
    if not subjects or not isinstance(subjects[0], dict):
        return {}
    subject = subjects[0]
    stage = str(subject.get("relationship_stage", "") or "")
    if not stage:
        return {}
    summary = {
        "relationship_subject_ref": RELATIONSHIP_SUBJECT_GRAPH_REF + "#subjects[0]",
        "relationship_stage": stage,
    }
    for source_key, target_key in [
        ("relationship_id", "relationship_id"),
        ("relation_role", "relation_role"),
        ("relationship_stage_reason", "relationship_stage_reason"),
        ("relationship_stage_turn_count", "relationship_stage_turn_count"),
        ("relationship_stage_evidence_refs", "relationship_stage_evidence_refs"),
    ]:
        if source_key in subject:
            summary[target_key] = subject[source_key]
    return summary


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


def _background_resume_summary(
    *,
    relationship_resume_summary: dict[str, Any],
    trait_slow_variable_summary: dict[str, Any],
    current_background_ref_set: list[str],
    background_source_ref_set: list[str],
) -> dict[str, Any]:
    if not relationship_resume_summary and not trait_slow_variable_summary:
        return {}
    return {
        "relationship": relationship_resume_summary,
        "trait_slow_variables": trait_slow_variable_summary,
        "source_ref_set": list(current_background_ref_set) + list(background_source_ref_set),
    }


def _apply_background_resume_fields(
    payload: dict[str, Any],
    *,
    relationship_resume_summary: dict[str, Any],
    trait_slow_variable_summary: dict[str, Any],
    background_resume_summary: dict[str, Any],
) -> None:
    if relationship_resume_summary:
        payload["background_relationship_subject_ref"] = relationship_resume_summary[
            "relationship_subject_ref"
        ]
        payload["background_relationship_stage"] = relationship_resume_summary[
            "relationship_stage"
        ]
        if relationship_resume_summary.get("relationship_stage_reason"):
            payload["background_relationship_stage_reason"] = relationship_resume_summary[
                "relationship_stage_reason"
            ]
        if relationship_resume_summary.get("relationship_stage_turn_count") is not None:
            payload["background_relationship_stage_turn_count"] = relationship_resume_summary[
                "relationship_stage_turn_count"
            ]
        if relationship_resume_summary.get("relationship_stage_evidence_refs"):
            payload["background_relationship_stage_evidence_refs"] = list(
                relationship_resume_summary["relationship_stage_evidence_refs"]
            )
    if trait_slow_variable_summary:
        payload["background_self_model_ref"] = SELF_MODEL_REF
        payload["background_trait_slow_variable_summary"] = trait_slow_variable_summary
    if background_resume_summary:
        payload["background_resume_summary"] = background_resume_summary
