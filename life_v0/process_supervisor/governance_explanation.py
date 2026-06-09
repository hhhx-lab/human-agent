from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .idle_strategy import extract_idle_governance_fields


RESIDENT_GOVERNANCE_EXPLANATION_REF = (
    "runtime/reports/latest/digital_life_resident_governance_explanation.json"
)


@dataclass(frozen=True)
class ResidentGovernanceExplanationResult:
    report: dict[str, Any]


def write_resident_governance_explanation(
    *,
    run_id: str,
    generated_at: str,
    reports_dir: Path,
    idle_strategy_ref: str | None,
    idle_strategy_state: dict[str, Any] | None,
    persistent_process_report_ref: str | None,
    resident_governance_report_ref: str | None,
    resident_governance_state_ref: str | None,
    resident_governance_snapshot_ref: str | None,
    completed_turns: int,
    incident_count: int,
    relaunch_recovery_count: int,
    exit_reason: str,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> ResidentGovernanceExplanationResult:
    idle_governance = extract_idle_governance_fields(idle_strategy_state)
    background_carryover_generation = _int_or_zero(
        idle_governance.get("background_carryover_generation")
    )
    dominant_driver_family = _dominant_driver_family(idle_governance)
    next_wake_expectation = _next_wake_expectation(
        dominant_driver_family=dominant_driver_family
    )
    report = {
        "schema_version": "digital_life_resident_governance_explanation_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "explanation_id": f"resident-governance-explanation-{run_id}",
        "idle_strategy_ref": idle_strategy_ref,
        "persistent_process_report_ref": persistent_process_report_ref,
        "resident_governance_report_ref": resident_governance_report_ref,
        "resident_governance_state_ref": resident_governance_state_ref,
        "resident_governance_snapshot_ref": resident_governance_snapshot_ref,
        "completed_dialogue_turns": completed_turns,
        "incident_count": incident_count,
        "relaunch_recovery_count": relaunch_recovery_count,
        "exit_reason": exit_reason,
        "dominant_driver_family": dominant_driver_family,
        "next_wake_expectation": next_wake_expectation,
        "background_continuity_active": bool(
            idle_governance.get("background_continuity_mode")
        ),
        "background_carryover_generation": background_carryover_generation,
        "background_carryover_parent_run_id": idle_governance.get(
            "background_carryover_parent_run_id"
        ),
        "background_carryover_source_ref_set": list(
            idle_governance.get("background_carryover_source_ref_set", [])
        ),
        "continuity_story": _compose_continuity_story(
            idle_governance=idle_governance,
            dominant_driver_family=dominant_driver_family,
            next_wake_expectation=next_wake_expectation,
            background_carryover_generation=background_carryover_generation,
            completed_turns=completed_turns,
            incident_count=incident_count,
            relaunch_recovery_count=relaunch_recovery_count,
        ),
    }
    report.update(idle_governance)
    reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(reports_dir / "digital_life_resident_governance_explanation.json", report)
    return ResidentGovernanceExplanationResult(report=report)


def _dominant_driver_family(idle_governance: dict[str, Any]) -> str:
    background_generation = _int_or_zero(
        idle_governance.get("background_carryover_generation")
    )
    background_mode = idle_governance.get("background_continuity_mode")
    attention_target = str(idle_governance.get("governance_attention_target") or "")
    attention_reason = str(idle_governance.get("governance_attention_reason") or "")
    offline_learning_pressure = str(
        idle_governance.get("offline_learning_pressure_level") or ""
    )
    offline_pressure = str(idle_governance.get("offline_pressure_level") or "")
    repair_followup_required = bool(idle_governance.get("repair_followup_required"))

    if background_mode and background_generation >= 2:
        return "persistent_background_continuity"
    if background_mode:
        return "background_continuity_carryover"
    if attention_target == "apology_repair_language_trace" or repair_followup_required:
        return "queue_e_repair_guard"
    if offline_learning_pressure in {"urgent", "elevated", "present"}:
        return "offline_learning_reconsolidation"
    if offline_pressure in {"elevated", "present"}:
        return "replay_growth_reconsolidation"
    if attention_target in {"commitment_expression_plan", "relationship_timeline"}:
        return "long_horizon_language_continuity"
    if attention_reason == "no_long_horizon_language_refs":
        return "baseline_waiting_presence"
    return "resident_governance_hold"


def _next_wake_expectation(*, dominant_driver_family: str) -> str:
    if dominant_driver_family == "persistent_background_continuity":
        return "resume_background_lineage_before_accepting_external_turn"
    if dominant_driver_family == "background_continuity_carryover":
        return "reopen_background_carryover_before_accepting_external_turn"
    if dominant_driver_family == "queue_e_repair_guard":
        return "re_evaluate_repair_guard_before_world_contact_release"
    if dominant_driver_family == "offline_learning_reconsolidation":
        return "re_enter_offline_learning_hold_before_accepting_external_turn"
    if dominant_driver_family == "replay_growth_reconsolidation":
        return "refresh_replay_growth_hold_before_accepting_external_turn"
    if dominant_driver_family == "long_horizon_language_continuity":
        return "re_anchor_long_horizon_language_before_accepting_external_turn"
    if dominant_driver_family == "baseline_waiting_presence":
        return "accept_external_turn_when_present"
    return "resume_waiting_governance_before_accepting_external_turn"


def _compose_continuity_story(
    *,
    idle_governance: dict[str, Any],
    dominant_driver_family: str,
    next_wake_expectation: str,
    background_carryover_generation: int,
    completed_turns: int,
    incident_count: int,
    relaunch_recovery_count: int,
) -> list[str]:
    lines = [
        (
            "resident governance closed with "
            f"{completed_turns} completed dialogue turns, "
            f"{incident_count} incidents, and "
            f"{relaunch_recovery_count} relaunch recoveries"
        )
    ]
    attention_target = idle_governance.get("governance_attention_target") or "waiting_presence_maintenance"
    cadence_profile = idle_governance.get("governance_cadence_profile") or "baseline_waiting_presence"
    lines.append(
        "dominant attention target is "
        f"{attention_target} with cadence {cadence_profile}"
    )
    if idle_governance.get("background_continuity_mode"):
        lineage_line = (
            "background continuity is active at generation "
            f"{background_carryover_generation}"
        )
        if idle_governance.get("background_carryover_parent_run_id"):
            lineage_line += (
                " from parent run "
                f"{idle_governance['background_carryover_parent_run_id']}"
            )
        lines.append(lineage_line)
    lines.append(
        "dominant driver family is "
        f"{dominant_driver_family} and next wake should {next_wake_expectation}"
    )
    return lines


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
