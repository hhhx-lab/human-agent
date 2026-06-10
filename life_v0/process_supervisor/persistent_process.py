from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .idle_strategy import extract_idle_governance_fields


PERSISTENT_PROCESS_STATE_REF = "runtime/state/terminal/persistent_process_state.json"
PERSISTENT_PROCESS_REPORT_REF = "runtime/reports/latest/digital_life_persistent_process_report.json"
RESIDENT_GOVERNANCE_STATE_REF = "runtime/state/terminal/resident_governance_state.json"
BACKGROUND_CONVERGENCE_SUMMARY_REF = (
    "runtime/state/terminal/background_convergence_summary.json"
)
RESIDENT_GOVERNANCE_SNAPSHOT_REF = "runtime/state/terminal/resident_governance_snapshot.json"
RESIDENT_GOVERNANCE_REPORT_REF = "runtime/reports/latest/digital_life_resident_governance_report.json"
RELATIONSHIP_SUBJECT_GRAPH_REF = "runtime/state/relationship/relationship_subject_graph.json"
SELF_MODEL_REF = "runtime/state/self/self_model.json"
TRAIT_DRIFT_MONITOR_REF = "runtime/state/body/trait_drift_monitor.json"


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
    trait_drift_monitor_ref: str | None = None,
    background_convergence_summary_ref: str | None = None,
    write_json: Callable[[Path, dict[str, Any]], None],
    relationship_graph: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
) -> PersistentProcessArtifactsResult:
    terminal_dir = state_dir / "terminal"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    idle_governance = extract_idle_governance_fields(idle_strategy_state)
    current_background_ref_set = [
        RESIDENT_GOVERNANCE_STATE_REF,
        RESIDENT_GOVERNANCE_SNAPSHOT_REF,
        RESIDENT_GOVERNANCE_REPORT_REF,
        PERSISTENT_PROCESS_REPORT_REF,
    ]
    if background_convergence_summary_ref:
        current_background_ref_set.insert(1, background_convergence_summary_ref)
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
    _apply_background_resume_fields(
        resident_governance_snapshot,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    resident_governance_snapshot.update(_idle_governance_without_background_lineage(idle_governance))
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
    _apply_background_resume_fields(
        resident_governance_state,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    resident_governance_state.update(_idle_governance_without_background_lineage(idle_governance))
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
    _apply_background_resume_fields(
        state,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    state.update(_idle_governance_without_background_lineage(idle_governance))
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
    _apply_background_resume_fields(
        report,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    report.update(_idle_governance_without_background_lineage(idle_governance))
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
    _apply_background_resume_fields(
        resident_governance_report,
        relationship_resume_summary=relationship_resume_summary,
        trait_slow_variable_summary=trait_slow_variable_summary,
        background_resume_summary=background_resume_summary,
    )
    resident_governance_report.update(_idle_governance_without_background_lineage(idle_governance))

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


def _int_or_default(value: Any, *, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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
