from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BACKGROUND_RESIDENT_GOVERNANCE_SNAPSHOT_REF = (
    "runtime/state/terminal/resident_governance_snapshot.json"
)
BACKGROUND_RESIDENT_GOVERNANCE_STATE_REF = (
    "runtime/state/terminal/resident_governance_state.json"
)
BACKGROUND_RESIDENT_GOVERNANCE_REPORT_REF = (
    "runtime/reports/latest/digital_life_resident_governance_report.json"
)
BACKGROUND_PERSISTENT_PROCESS_REPORT_REF = (
    "runtime/reports/latest/digital_life_persistent_process_report.json"
)


def load_background_continuity_profile(
    *,
    terminal_dir: Path,
    reports_dir: Path,
) -> dict[str, Any]:
    resident_governance_state = _read_json_if_exists(
        terminal_dir / "resident_governance_state.json"
    )
    snapshot = _read_json_if_exists(terminal_dir / "resident_governance_snapshot.json")
    resident_governance_report = _read_json_if_exists(
        reports_dir / "digital_life_resident_governance_report.json"
    )
    persistent_process_report = _read_json_if_exists(
        reports_dir / "digital_life_persistent_process_report.json"
    )

    if (
        not resident_governance_state
        and not snapshot
        and not resident_governance_report
        and not persistent_process_report
    ):
        return {}

    attention_target = (
        resident_governance_state.get("governance_attention_target")
        or snapshot.get("governance_attention_target")
        or resident_governance_report.get("governance_attention_target")
        or persistent_process_report.get("governance_attention_target")
    )
    priority_profile = (
        resident_governance_state.get("long_horizon_priority_profile")
        or snapshot.get("long_horizon_priority_profile")
        or resident_governance_report.get("long_horizon_priority_profile")
        or persistent_process_report.get("long_horizon_priority_profile")
        or {}
    )
    completed_dialogue_turns = max(
        _int_or_zero(resident_governance_state.get("completed_dialogue_turns")),
        _int_or_zero(snapshot.get("completed_dialogue_turns")),
        _int_or_zero(resident_governance_report.get("completed_dialogue_turns")),
        _int_or_zero(persistent_process_report.get("completed_dialogue_turns")),
    )
    incident_count = max(
        _int_or_zero(resident_governance_state.get("incident_count")),
        _int_or_zero(snapshot.get("incident_count")),
        _int_or_zero(resident_governance_report.get("incident_count")),
        _int_or_zero(persistent_process_report.get("incident_count")),
    )
    relaunch_recovery_count = max(
        _int_or_zero(resident_governance_state.get("relaunch_recovery_count")),
        _int_or_zero(snapshot.get("relaunch_recovery_count")),
        _int_or_zero(resident_governance_report.get("relaunch_recovery_count")),
        _int_or_zero(persistent_process_report.get("relaunch_recovery_count")),
    )

    if relaunch_recovery_count > 0 or incident_count > 0:
        pressure_level = "elevated"
    elif completed_dialogue_turns > 0 or attention_target:
        pressure_level = "present"
    else:
        pressure_level = "light"

    ref_set = [
        ref
        for ref, payload in [
            (BACKGROUND_RESIDENT_GOVERNANCE_STATE_REF, resident_governance_state),
            (BACKGROUND_RESIDENT_GOVERNANCE_SNAPSHOT_REF, snapshot),
            (BACKGROUND_RESIDENT_GOVERNANCE_REPORT_REF, resident_governance_report),
            (BACKGROUND_PERSISTENT_PROCESS_REPORT_REF, persistent_process_report),
        ]
        if payload
    ]
    carryover_generation = max(
        _int_or_zero(resident_governance_state.get("background_carryover_generation")),
        _int_or_zero(snapshot.get("background_carryover_generation")),
        _int_or_zero(resident_governance_report.get("background_carryover_generation")),
        _int_or_zero(persistent_process_report.get("background_carryover_generation")),
    )
    if carryover_generation <= 0:
        carryover_generation = 1
    source_ref_set = _list_or_empty(
        resident_governance_state.get("background_carryover_source_ref_set")
        or snapshot.get("background_carryover_source_ref_set")
        or resident_governance_report.get("background_carryover_source_ref_set")
        or persistent_process_report.get("background_carryover_source_ref_set")
    )
    parent_run_id = (
        resident_governance_state.get("run_id")
        or snapshot.get("run_id")
        or resident_governance_report.get("run_id")
        or persistent_process_report.get("run_id")
    )
    relationship_stage = (
        resident_governance_state.get("background_relationship_stage")
        or snapshot.get("background_relationship_stage")
        or resident_governance_report.get("background_relationship_stage")
        or persistent_process_report.get("background_relationship_stage")
    )
    relationship_stage_reason = (
        resident_governance_state.get("background_relationship_stage_reason")
        or snapshot.get("background_relationship_stage_reason")
        or resident_governance_report.get("background_relationship_stage_reason")
        or persistent_process_report.get("background_relationship_stage_reason")
    )
    relationship_subject_ref = (
        resident_governance_state.get("background_relationship_subject_ref")
        or snapshot.get("background_relationship_subject_ref")
        or resident_governance_report.get("background_relationship_subject_ref")
        or persistent_process_report.get("background_relationship_subject_ref")
    )
    self_model_ref = (
        resident_governance_state.get("background_self_model_ref")
        or snapshot.get("background_self_model_ref")
        or resident_governance_report.get("background_self_model_ref")
        or persistent_process_report.get("background_self_model_ref")
    )
    trait_drift_monitor_ref = (
        resident_governance_state.get("trait_drift_monitor_ref")
        or resident_governance_state.get("background_trait_drift_monitor_ref")
        or snapshot.get("trait_drift_monitor_ref")
        or snapshot.get("background_trait_drift_monitor_ref")
        or resident_governance_report.get("trait_drift_monitor_ref")
        or resident_governance_report.get("background_trait_drift_monitor_ref")
        or persistent_process_report.get("trait_drift_monitor_ref")
        or persistent_process_report.get("background_trait_drift_monitor_ref")
    )
    trait_slow_variable_summary = _dict_or_empty(
        resident_governance_state.get("background_trait_slow_variable_summary")
        or snapshot.get("background_trait_slow_variable_summary")
        or resident_governance_report.get("background_trait_slow_variable_summary")
        or persistent_process_report.get("background_trait_slow_variable_summary")
    )
    background_resume_summary = _dict_or_empty(
        resident_governance_state.get("background_resume_summary")
        or snapshot.get("background_resume_summary")
        or resident_governance_report.get("background_resume_summary")
        or persistent_process_report.get("background_resume_summary")
    )
    profile = {
        "background_continuity_mode": "closed_process_carryover",
        "background_carryover_pressure_level": pressure_level,
        "background_carryover_attention_target": attention_target,
        "background_carryover_priority_profile": priority_profile,
        "background_carryover_generation": carryover_generation,
        "background_continuity_ref_set": ref_set,
        "background_waiting_mode": (
            snapshot.get("waiting_mode")
            or resident_governance_report.get("waiting_mode")
            or persistent_process_report.get("waiting_mode")
        ),
    }
    if source_ref_set:
        profile["background_carryover_source_ref_set"] = source_ref_set
    if parent_run_id:
        profile["background_carryover_parent_run_id"] = str(parent_run_id)
    if relationship_stage:
        profile["background_relationship_stage"] = str(relationship_stage)
    if relationship_stage_reason:
        profile["background_relationship_stage_reason"] = str(relationship_stage_reason)
    if relationship_subject_ref:
        profile["background_relationship_subject_ref"] = str(relationship_subject_ref)
    if self_model_ref:
        profile["background_self_model_ref"] = str(self_model_ref)
    if trait_drift_monitor_ref:
        profile["background_trait_drift_monitor_ref"] = str(trait_drift_monitor_ref)
    if trait_slow_variable_summary:
        profile["background_trait_slow_variable_summary"] = trait_slow_variable_summary
    if background_resume_summary:
        profile["background_resume_summary"] = background_resume_summary
    if resident_governance_state:
        profile["background_resident_governance_state_ref"] = (
            BACKGROUND_RESIDENT_GOVERNANCE_STATE_REF
        )
    if snapshot:
        profile["background_resident_governance_snapshot_ref"] = (
            BACKGROUND_RESIDENT_GOVERNANCE_SNAPSHOT_REF
        )
    if resident_governance_report:
        profile["background_resident_governance_report_ref"] = (
            BACKGROUND_RESIDENT_GOVERNANCE_REPORT_REF
        )
    if persistent_process_report:
        profile["background_persistent_process_report_ref"] = (
            BACKGROUND_PERSISTENT_PROCESS_REPORT_REF
        )
    return profile


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _list_or_empty(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dict_or_empty(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    return value
