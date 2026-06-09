from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class IncidentRecoveryResult:
    incident_report_ref: str
    recovery_report_ref: str
    incident_report: dict[str, Any]
    recovery_report: dict[str, Any]


def recover_from_dialogue_turn_exception(
    *,
    run_id: str,
    incident_count: int,
    external_utterance: str,
    exc: Exception,
    reports_dir: Path,
    terminal_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    write_json: Callable[[Path, dict[str, Any]], None],
    now_iso: Callable[[], str],
) -> IncidentRecoveryResult:
    incident_generated_at = now_iso()
    incident_report_ref = "runtime/reports/latest/digital_life_process_incident_report.json"
    recovery_report_ref = "runtime/reports/latest/digital_life_process_recovery_report.json"

    incident_report = {
        "report_kind": "incident_report",
        "incident_id": f"{run_id}-incident-{incident_count:04d}",
        "incident_kind": "dialogue_turn_processing_failure",
        "severity": "high",
        "detected_at": incident_generated_at,
        "source_report_refs": [
            "runtime/reports/latest/digital_life_shell_report.json",
            "runtime/state/terminal/terminal_life_loop_state.json",
        ],
        "affected_surfaces": [
            "language_expression",
            "relationship_continuity",
            "terminal_dialogue_loop",
        ],
        "containment": {
            "quarantine_refs": [],
            "stage_decision": "restored_waiting_for_external_turn",
            "replay_blocked": False,
        },
        "coexistence_review_refs": [],
        "recovery_plan_ref": recovery_report_ref,
        "external_turn_utterance": external_utterance,
        "error_type": exc.__class__.__name__,
        "error_message": str(exc),
    }
    recovery_report = {
        "report_kind": "incident_recovery_report",
        "incident_ref": incident_report_ref,
        "result": "recovered_to_waiting_state",
        "fixed_root_causes": [],
        "regression_fixture_refs": [
            "tests/process/test_persistent_digital_life_process.py::test_digital_life_process_recovers_from_dialogue_turn_exception_and_returns_to_waiting_state",
        ],
        "rerun_reports": [
            "runtime/reports/latest/digital_life_process_report.json",
        ],
        "release_decision": "resume_waiting_for_next_external_turn",
        "forbidden_routes": [
            "active_memory_direct",
            "relationship_model_direct_commit",
        ],
    }

    safe_terminal_loop["current_mode"] = "restored_waiting_for_external_turn"
    safe_terminal_loop["last_incident_status"] = "recovered_to_waiting_state"
    safe_terminal_loop["last_incident_report_ref"] = incident_report_ref
    write_json(terminal_dir / "safe_terminal_loop_state.json", safe_terminal_loop)

    terminal_life_loop_state["current_mode"] = "restored_waiting_for_external_turn"
    terminal_life_loop_state["last_turn_status"] = "incident_recovered"
    terminal_life_loop_state["last_turn_mode"] = "incident_recovery_return"
    terminal_life_loop_state["last_external_turn_utterance"] = external_utterance
    terminal_life_loop_state["next_required_action"] = "await_next_external_relation_turn"
    terminal_life_loop_state["last_incident_report_ref"] = incident_report_ref
    write_json(terminal_dir / "terminal_life_loop_state.json", terminal_life_loop_state)

    record_recovery_continuity(
        self_narrative_trace=self_narrative_trace,
        commitment_index=commitment_index,
        relationship_graph=relationship_graph,
        event_kind="dialogue_incident_recovery",
        report_ref=recovery_report_ref,
        details={
            "incident_report_ref": incident_report_ref,
            "external_turn_utterance": external_utterance,
            "result": "recovered_to_waiting_state",
        },
    )
    write_json(language_dir / "self_narrative_language_trace.json", self_narrative_trace)
    write_json(language_dir / "commitment_repair_language_index.json", commitment_index)
    write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)

    reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(reports_dir / "digital_life_process_incident_report.json", incident_report)
    write_json(reports_dir / "digital_life_process_recovery_report.json", recovery_report)

    return IncidentRecoveryResult(
        incident_report_ref=incident_report_ref,
        recovery_report_ref=recovery_report_ref,
        incident_report=incident_report,
        recovery_report=recovery_report,
    )


def record_recovery_continuity(
    *,
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    event_kind: str,
    report_ref: str,
    details: dict[str, Any],
) -> None:
    self_narrative_trace.setdefault("recovery_event_refs", [])
    self_narrative_trace["recovery_event_refs"].append(report_ref)
    self_narrative_trace["last_recovery_event"] = {
        "event_kind": event_kind,
        "report_ref": report_ref,
        "details": details,
    }

    commitment_index.setdefault("recovery_history_refs", [])
    commitment_index["recovery_history_refs"].append(report_ref)
    commitment_index["last_recovery_event_kind"] = event_kind
    commitment_index["last_recovery_report_ref"] = report_ref

    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        subjects[0]["last_continuity_event_kind"] = event_kind
        subjects[0]["last_continuity_report_ref"] = report_ref
