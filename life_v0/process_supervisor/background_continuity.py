from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .background_convergence import BACKGROUND_CONVERGENCE_SUMMARY_REF
from .background_convergence_history import BACKGROUND_CONVERGENCE_HISTORY_REF
from .process_lease import RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF


BACKGROUND_RESIDENT_GOVERNANCE_SNAPSHOT_REF = (
    "runtime/state/terminal/resident_governance_snapshot.json"
)
BACKGROUND_RESIDENT_GOVERNANCE_STATE_REF = (
    "runtime/state/terminal/resident_governance_state.json"
)
BACKGROUND_RESIDENT_GOVERNANCE_REPORT_REF = (
    "runtime/reports/latest/digital_life_resident_governance_report.json"
)
BACKGROUND_RESIDENT_GOVERNANCE_EXPLANATION_REF = (
    "runtime/reports/latest/digital_life_resident_governance_explanation.json"
)
BACKGROUND_PERSISTENT_PROCESS_REPORT_REF = (
    "runtime/reports/latest/digital_life_persistent_process_report.json"
)
BACKGROUND_IDLE_HEARTBEAT_TRACE_REF = (
    "runtime/state/terminal/idle_heartbeat_trace.jsonl"
)
BACKGROUND_RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF = (
    RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF
)
BACKGROUND_SCHEMA_CROSS_FILE_LOGIC_REF = (
    "runtime/state/schema_runner/cross_file_logic.json"
)
BACKGROUND_SCHEMA_RUN_MANIFEST_REF = "runtime/state/schema_runner/run_manifest.json"


def load_background_continuity_profile(
    *,
    terminal_dir: Path,
    reports_dir: Path,
) -> dict[str, Any]:
    resident_governance_state = _read_json_if_exists(
        terminal_dir / "resident_governance_state.json"
    )
    background_convergence_summary = _read_json_if_exists(
        terminal_dir / "background_convergence_summary.json"
    )
    background_convergence_history = _read_json_if_exists(
        terminal_dir / "background_convergence_history.json"
    )
    snapshot = _read_json_if_exists(terminal_dir / "resident_governance_snapshot.json")
    resident_governance_report = _read_json_if_exists(
        reports_dir / "digital_life_resident_governance_report.json"
    )
    resident_governance_explanation = _read_json_if_exists(
        reports_dir / "digital_life_resident_governance_explanation.json"
    )
    persistent_process_report = _read_json_if_exists(
        reports_dir / "digital_life_persistent_process_report.json"
    )
    resident_process_lease_history_profile = _read_json_if_exists(
        terminal_dir / "resident_process_lease_history_profile.json"
    )
    idle_heartbeat_trace_path = terminal_dir / "idle_heartbeat_trace.jsonl"
    idle_heartbeat_trace_exists = idle_heartbeat_trace_path.exists()
    has_background_carryover_source = any(
        [
            resident_governance_state,
            background_convergence_summary,
            background_convergence_history,
            snapshot,
            resident_governance_report,
            resident_governance_explanation,
            persistent_process_report,
            idle_heartbeat_trace_exists,
        ]
    )

    if (
        not resident_governance_state
        and not background_convergence_summary
        and not background_convergence_history
        and not snapshot
        and not resident_governance_report
        and not resident_governance_explanation
        and not persistent_process_report
        and not resident_process_lease_history_profile
        and not idle_heartbeat_trace_exists
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
    resident_process_identity_pressure_level = (
        resident_process_lease_history_profile.get("identity_pressure_level")
        or resident_governance_state.get("resident_process_identity_pressure_level")
        or snapshot.get("resident_process_identity_pressure_level")
        or resident_governance_report.get("resident_process_identity_pressure_level")
        or persistent_process_report.get("resident_process_identity_pressure_level")
    )

    if relaunch_recovery_count > 0 or incident_count > 0:
        pressure_level = "elevated"
    elif completed_dialogue_turns > 0 or attention_target:
        pressure_level = "present"
    else:
        pressure_level = "light"
    pressure_level = _stronger_pressure(
        pressure_level,
        resident_process_identity_pressure_level,
    )
    if not attention_target and resident_process_lease_history_profile:
        attention_target = "resident_process_identity_continuity"

    ref_set = [
        ref
        for ref, payload in [
            (BACKGROUND_RESIDENT_GOVERNANCE_STATE_REF, resident_governance_state),
            (BACKGROUND_CONVERGENCE_SUMMARY_REF, background_convergence_summary),
            (BACKGROUND_CONVERGENCE_HISTORY_REF, background_convergence_history),
            (BACKGROUND_RESIDENT_GOVERNANCE_SNAPSHOT_REF, snapshot),
            (BACKGROUND_RESIDENT_GOVERNANCE_REPORT_REF, resident_governance_report),
            (
                BACKGROUND_RESIDENT_GOVERNANCE_EXPLANATION_REF,
                resident_governance_explanation,
            ),
            (BACKGROUND_PERSISTENT_PROCESS_REPORT_REF, persistent_process_report),
            (
                BACKGROUND_RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF,
                resident_process_lease_history_profile,
            ),
            (
                BACKGROUND_IDLE_HEARTBEAT_TRACE_REF,
                {"present": True} if idle_heartbeat_trace_exists else {},
            ),
        ]
        if payload
    ]
    carryover_generation = max(
        _int_or_zero(resident_governance_state.get("background_carryover_generation")),
        _int_or_zero(background_convergence_summary.get("background_carryover_generation")),
        _max_history_generation(background_convergence_history),
        _int_or_zero(snapshot.get("background_carryover_generation")),
        _int_or_zero(resident_governance_report.get("background_carryover_generation")),
        _int_or_zero(persistent_process_report.get("background_carryover_generation")),
    )
    if carryover_generation <= 0:
        carryover_generation = 1
    source_ref_set = _list_or_empty(
        resident_governance_state.get("background_carryover_source_ref_set")
        or background_convergence_summary.get("background_carryover_source_ref_set")
        or snapshot.get("background_carryover_source_ref_set")
        or resident_governance_report.get("background_carryover_source_ref_set")
        or persistent_process_report.get("background_carryover_source_ref_set")
    )
    parent_run_id = (
        resident_governance_state.get("run_id")
        or background_convergence_summary.get("background_carryover_parent_run_id")
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
    idle_heartbeat_trace_count = max(
        _int_or_zero(resident_governance_state.get("idle_heartbeat_trace_count")),
        _int_or_zero(snapshot.get("idle_heartbeat_trace_count")),
        _int_or_zero(resident_governance_report.get("idle_heartbeat_trace_count")),
        _int_or_zero(persistent_process_report.get("idle_heartbeat_trace_count")),
        _idle_heartbeat_trace_count(idle_heartbeat_trace_path)
        if idle_heartbeat_trace_exists
        else 0,
    )
    trait_slow_variable_summary = _dict_or_empty(
        resident_governance_state.get("background_trait_slow_variable_summary")
        or background_convergence_summary.get("background_trait_slow_variable_summary")
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
    resident_background_lineage_state = _dict_or_empty(
        resident_governance_state.get("resident_background_lineage_state")
        or snapshot.get("resident_background_lineage_state")
        or resident_governance_report.get("resident_background_lineage_state")
        or persistent_process_report.get("resident_background_lineage_state")
    )
    resident_background_birth_repair_presence = _dict_or_empty(
        resident_background_lineage_state.get("birth_repair_presence")
    )
    offline_learning_cumulative_profile = _dict_or_empty(
        resident_governance_state.get("offline_learning_cumulative_profile")
        or snapshot.get("offline_learning_cumulative_profile")
        or resident_governance_report.get("offline_learning_cumulative_profile")
        or persistent_process_report.get("offline_learning_cumulative_profile")
    )
    offline_learning_cumulative_generation = max(
        _int_or_zero(
            resident_governance_state.get("offline_learning_cumulative_generation")
        ),
        _int_or_zero(snapshot.get("offline_learning_cumulative_generation")),
        _int_or_zero(
            resident_governance_report.get("offline_learning_cumulative_generation")
        ),
        _int_or_zero(
            persistent_process_report.get("offline_learning_cumulative_generation")
        ),
        _int_or_zero(offline_learning_cumulative_profile.get("generation")),
    )
    offline_learning_cumulative_pressure_level = (
        resident_governance_state.get("offline_learning_cumulative_pressure_level")
        or snapshot.get("offline_learning_cumulative_pressure_level")
        or resident_governance_report.get("offline_learning_cumulative_pressure_level")
        or persistent_process_report.get("offline_learning_cumulative_pressure_level")
        or offline_learning_cumulative_profile.get("pressure_level")
    )
    offline_learning_cumulative_attention_target = (
        resident_governance_state.get("offline_learning_cumulative_attention_target")
        or snapshot.get("offline_learning_cumulative_attention_target")
        or resident_governance_report.get("offline_learning_cumulative_attention_target")
        or persistent_process_report.get("offline_learning_cumulative_attention_target")
        or offline_learning_cumulative_profile.get("attention_target")
    )
    offline_learning_cumulative_priority_profile = _dict_or_empty(
        resident_governance_state.get("offline_learning_cumulative_priority_profile")
        or snapshot.get("offline_learning_cumulative_priority_profile")
        or resident_governance_report.get("offline_learning_cumulative_priority_profile")
        or persistent_process_report.get("offline_learning_cumulative_priority_profile")
        or offline_learning_cumulative_profile.get("priority_profile")
    )
    offline_learning_cumulative_ref_set = _list_or_empty(
        resident_governance_state.get("offline_learning_cumulative_ref_set")
        or snapshot.get("offline_learning_cumulative_ref_set")
        or resident_governance_report.get("offline_learning_cumulative_ref_set")
        or persistent_process_report.get("offline_learning_cumulative_ref_set")
        or offline_learning_cumulative_profile.get("ref_set")
    )
    live_language_turn_refs = _dedupe_list(
        _list_or_empty(resident_governance_state.get("live_language_turn_refs"))
        + _list_or_empty(snapshot.get("live_language_turn_refs"))
        + _list_or_empty(resident_governance_report.get("live_language_turn_refs"))
        + _list_or_empty(persistent_process_report.get("live_language_turn_refs"))
        + _list_or_empty(
            resident_governance_state.get("background_live_language_turn_refs")
        )
        + _list_or_empty(snapshot.get("background_live_language_turn_refs"))
        + _list_or_empty(
            resident_governance_report.get("background_live_language_turn_refs")
        )
        + _list_or_empty(
            persistent_process_report.get("background_live_language_turn_refs")
        )
    )
    last_live_semantic_focus = (
        resident_governance_state.get("last_live_semantic_focus")
        or snapshot.get("last_live_semantic_focus")
        or resident_governance_report.get("last_live_semantic_focus")
        or persistent_process_report.get("last_live_semantic_focus")
        or resident_governance_state.get("background_last_live_semantic_focus")
        or snapshot.get("background_last_live_semantic_focus")
        or resident_governance_report.get("background_last_live_semantic_focus")
        or persistent_process_report.get("background_last_live_semantic_focus")
    )
    live_language_presence_profile = _dict_or_empty(
        resident_governance_state.get("live_language_presence_profile")
        or snapshot.get("live_language_presence_profile")
        or resident_governance_report.get("live_language_presence_profile")
        or persistent_process_report.get("live_language_presence_profile")
        or resident_governance_state.get("background_live_language_presence_profile")
        or snapshot.get("background_live_language_presence_profile")
        or resident_governance_report.get("background_live_language_presence_profile")
        or persistent_process_report.get("background_live_language_presence_profile")
    )
    state_merge_guard_ref = (
        resident_governance_state.get("state_merge_guard_ref")
        or resident_governance_state.get("background_state_merge_guard_ref")
        or snapshot.get("state_merge_guard_ref")
        or snapshot.get("background_state_merge_guard_ref")
        or resident_governance_report.get("state_merge_guard_ref")
        or resident_governance_report.get("background_state_merge_guard_ref")
        or persistent_process_report.get("state_merge_guard_ref")
        or persistent_process_report.get("background_state_merge_guard_ref")
    )
    state_merge_policy = (
        resident_governance_state.get("state_merge_policy")
        or resident_governance_state.get("background_state_merge_policy")
        or snapshot.get("state_merge_policy")
        or snapshot.get("background_state_merge_policy")
        or resident_governance_report.get("state_merge_policy")
        or resident_governance_report.get("background_state_merge_policy")
        or persistent_process_report.get("state_merge_policy")
        or persistent_process_report.get("background_state_merge_policy")
    )
    state_merge_long_term_change_count = max(
        _int_or_zero(
            resident_governance_state.get("state_merge_long_term_change_count")
        ),
        _int_or_zero(
            resident_governance_state.get(
                "background_state_merge_long_term_change_count"
            )
        ),
        _int_or_zero(snapshot.get("state_merge_long_term_change_count")),
        _int_or_zero(snapshot.get("background_state_merge_long_term_change_count")),
        _int_or_zero(
            resident_governance_report.get("state_merge_long_term_change_count")
        ),
        _int_or_zero(
            resident_governance_report.get(
                "background_state_merge_long_term_change_count"
            )
        ),
        _int_or_zero(
            persistent_process_report.get("state_merge_long_term_change_count")
        ),
        _int_or_zero(
            persistent_process_report.get(
                "background_state_merge_long_term_change_count"
            )
        ),
    )
    state_merge_long_term_change_families = _dedupe_list(
        _list_or_empty(
            resident_governance_state.get("state_merge_long_term_change_families")
        )
        + _list_or_empty(
            resident_governance_state.get(
                "background_state_merge_long_term_change_families"
            )
        )
        + _list_or_empty(snapshot.get("state_merge_long_term_change_families"))
        + _list_or_empty(
            snapshot.get("background_state_merge_long_term_change_families")
        )
        + _list_or_empty(
            resident_governance_report.get("state_merge_long_term_change_families")
        )
        + _list_or_empty(
            resident_governance_report.get(
                "background_state_merge_long_term_change_families"
            )
        )
        + _list_or_empty(
            persistent_process_report.get("state_merge_long_term_change_families")
        )
        + _list_or_empty(
            persistent_process_report.get(
                "background_state_merge_long_term_change_families"
            )
        )
    )
    state_merge_long_term_change_refs = _dedupe_list(
        _list_or_empty(
            resident_governance_state.get("state_merge_long_term_change_refs")
        )
        + _list_or_empty(
            resident_governance_state.get(
                "background_state_merge_long_term_change_refs"
            )
        )
        + _list_or_empty(snapshot.get("state_merge_long_term_change_refs"))
        + _list_or_empty(snapshot.get("background_state_merge_long_term_change_refs"))
        + _list_or_empty(
            resident_governance_report.get("state_merge_long_term_change_refs")
        )
        + _list_or_empty(
            resident_governance_report.get(
                "background_state_merge_long_term_change_refs"
            )
        )
        + _list_or_empty(
            persistent_process_report.get("state_merge_long_term_change_refs")
        )
        + _list_or_empty(
            persistent_process_report.get(
                "background_state_merge_long_term_change_refs"
            )
        )
    )
    schema_cross_file_logic_ref = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=("schema_cross_file_logic_ref", "background_schema_cross_file_logic_ref"),
    )
    schema_run_manifest_ref = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=("schema_run_manifest_ref", "background_schema_run_manifest_ref"),
    )
    life_constraint_refs = _dedupe_list(
        _collect_lists(
            resident_governance_state,
            snapshot,
            resident_governance_report,
            persistent_process_report,
            keys=("life_constraint_refs", "background_life_constraint_refs"),
        )
    )
    queue_e_cross_layer_gate_status = _first_dict(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "queue_e_cross_layer_gate_status",
            "background_queue_e_cross_layer_gate_status",
        ),
    )
    life_constraint_waiting_posture = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "life_constraint_waiting_posture",
            "background_life_constraint_waiting_posture",
        ),
    )
    life_constraint_attention_target = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "life_constraint_attention_target",
            "background_life_constraint_attention_target",
        ),
    )
    life_constraint_attention_reason = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "life_constraint_attention_reason",
            "background_life_constraint_attention_reason",
        ),
    )
    queue_e_birth_repair_waiting_profile = _first_dict(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "queue_e_birth_repair_waiting_profile",
            "background_queue_e_birth_repair_waiting_profile",
        ),
    )
    if not queue_e_birth_repair_waiting_profile:
        queue_e_birth_repair_waiting_profile = _dict_or_empty(
            resident_background_birth_repair_presence.get(
                "queue_e_birth_repair_waiting_profile"
            )
        )
    queue_e_birth_repair_gate_status = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "queue_e_birth_repair_gate_status",
            "background_queue_e_birth_repair_gate_status",
        ),
    )
    if not queue_e_birth_repair_gate_status:
        queue_e_birth_repair_gate_status = (
            resident_background_birth_repair_presence.get("gate_status")
        )
    queue_e_birth_repair_profile_ref = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "queue_e_birth_repair_profile_ref",
            "background_queue_e_birth_repair_profile_ref",
        ),
    )
    if not queue_e_birth_repair_profile_ref:
        queue_e_birth_repair_profile_ref = (
            resident_background_birth_repair_presence.get("profile_ref")
        )
    queue_e_birth_repair_pressure_level = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "queue_e_birth_repair_pressure_level",
            "background_queue_e_birth_repair_pressure_level",
        ),
    )
    if not queue_e_birth_repair_pressure_level:
        queue_e_birth_repair_pressure_level = (
            resident_background_birth_repair_presence.get("pressure_level")
        )
    queue_e_birth_repair_attention_target = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "queue_e_birth_repair_attention_target",
            "background_queue_e_birth_repair_attention_target",
        ),
    )
    if not queue_e_birth_repair_attention_target:
        queue_e_birth_repair_attention_target = (
            resident_background_birth_repair_presence.get("attention_target")
        )
    queue_e_birth_repair_ref_set = _dedupe_list(
        _collect_lists(
            resident_governance_state,
            snapshot,
            resident_governance_report,
            persistent_process_report,
            keys=(
                "queue_e_birth_repair_ref_set",
                "queue_e_birth_repair_refs",
                "queue_e_birth_repair_evidence_refs",
                "background_queue_e_birth_repair_ref_set",
            ),
        )
        + _list_or_empty(queue_e_birth_repair_waiting_profile.get("ref_set"))
        + _list_or_empty(resident_background_birth_repair_presence.get("ref_set"))
        + _list_or_empty(
            resident_background_birth_repair_presence.get("background_ref_set")
        )
    )
    queue_e_birth_repair_waiting_posture = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "queue_e_birth_repair_waiting_posture",
            "background_queue_e_birth_repair_waiting_posture",
        ),
    )
    if not queue_e_birth_repair_waiting_posture:
        queue_e_birth_repair_waiting_posture = (
            resident_background_birth_repair_presence.get("waiting_posture")
        )
    queue_e_birth_repair_attention_reason = _first_present(
        resident_governance_state,
        snapshot,
        resident_governance_report,
        persistent_process_report,
        keys=(
            "queue_e_birth_repair_attention_reason",
            "background_queue_e_birth_repair_attention_reason",
        ),
    )
    if not queue_e_birth_repair_attention_reason:
        queue_e_birth_repair_attention_reason = (
            resident_background_birth_repair_presence.get("attention_reason")
        )
    pressure_level = _stronger_pressure(
        pressure_level,
        queue_e_birth_repair_pressure_level,
    )
    if not attention_target and queue_e_birth_repair_attention_target:
        attention_target = queue_e_birth_repair_attention_target
    if live_language_turn_refs:
        ref_set = _dedupe_list(ref_set + live_language_turn_refs)
    if state_merge_guard_ref:
        ref_set = _dedupe_list(ref_set + [str(state_merge_guard_ref)])
    if state_merge_long_term_change_refs:
        ref_set = _dedupe_list(ref_set + state_merge_long_term_change_refs)
    if schema_cross_file_logic_ref:
        ref_set = _dedupe_list(ref_set + [str(schema_cross_file_logic_ref)])
    elif queue_e_cross_layer_gate_status or life_constraint_refs:
        ref_set = _dedupe_list(ref_set + [BACKGROUND_SCHEMA_CROSS_FILE_LOGIC_REF])
    if schema_run_manifest_ref:
        ref_set = _dedupe_list(ref_set + [str(schema_run_manifest_ref)])
    elif queue_e_cross_layer_gate_status or life_constraint_refs:
        ref_set = _dedupe_list(ref_set + [BACKGROUND_SCHEMA_RUN_MANIFEST_REF])
    if life_constraint_refs:
        ref_set = _dedupe_list(ref_set + life_constraint_refs)
    if queue_e_birth_repair_profile_ref:
        ref_set = _dedupe_list(ref_set + [str(queue_e_birth_repair_profile_ref)])
    if queue_e_birth_repair_ref_set:
        ref_set = _dedupe_list(ref_set + queue_e_birth_repair_ref_set)
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
    if idle_heartbeat_trace_exists:
        profile["background_idle_heartbeat_trace_ref"] = (
            BACKGROUND_IDLE_HEARTBEAT_TRACE_REF
        )
        if idle_heartbeat_trace_count:
            profile["background_idle_heartbeat_trace_count"] = (
                idle_heartbeat_trace_count
            )
    if trait_slow_variable_summary:
        profile["background_trait_slow_variable_summary"] = trait_slow_variable_summary
    if background_resume_summary:
        profile["background_resume_summary"] = background_resume_summary
    if resident_background_lineage_state:
        profile["resident_background_lineage_state"] = resident_background_lineage_state
        profile["background_resident_lineage_state"] = (
            resident_background_lineage_state
        )
    if offline_learning_cumulative_generation:
        profile["background_offline_learning_generation"] = (
            offline_learning_cumulative_generation
        )
    if offline_learning_cumulative_pressure_level:
        profile["background_offline_learning_pressure_level"] = str(
            offline_learning_cumulative_pressure_level
        )
    if offline_learning_cumulative_attention_target:
        profile["background_offline_learning_attention_target"] = str(
            offline_learning_cumulative_attention_target
        )
    if offline_learning_cumulative_priority_profile:
        profile["background_offline_learning_priority_profile"] = (
            offline_learning_cumulative_priority_profile
        )
    if offline_learning_cumulative_ref_set:
        profile["background_offline_learning_ref_set"] = (
            offline_learning_cumulative_ref_set
        )
    if offline_learning_cumulative_profile:
        profile["background_offline_learning_cumulative_profile"] = (
            offline_learning_cumulative_profile
        )
    if live_language_turn_refs:
        profile["background_live_language_turn_refs"] = live_language_turn_refs
    if last_live_semantic_focus:
        profile["background_last_live_semantic_focus"] = str(last_live_semantic_focus)
    if live_language_turn_refs or last_live_semantic_focus or live_language_presence_profile:
        profile["background_live_language_presence_profile"] = (
            _background_live_language_presence_profile(
                live_language_turn_refs=live_language_turn_refs,
                last_live_semantic_focus=last_live_semantic_focus,
                source_profile=live_language_presence_profile,
            )
        )
    if state_merge_guard_ref:
        profile["background_state_merge_guard_ref"] = str(state_merge_guard_ref)
    if state_merge_policy:
        profile["background_state_merge_policy"] = str(state_merge_policy)
    if state_merge_long_term_change_count:
        profile["background_state_merge_long_term_change_count"] = (
            state_merge_long_term_change_count
        )
    if state_merge_long_term_change_families:
        profile["background_state_merge_long_term_change_families"] = (
            state_merge_long_term_change_families
        )
    if state_merge_long_term_change_refs:
        profile["background_state_merge_long_term_change_refs"] = (
            state_merge_long_term_change_refs
        )
    if schema_cross_file_logic_ref:
        profile["background_schema_cross_file_logic_ref"] = str(
            schema_cross_file_logic_ref
        )
    if schema_run_manifest_ref:
        profile["background_schema_run_manifest_ref"] = str(schema_run_manifest_ref)
    if life_constraint_refs:
        profile["background_life_constraint_refs"] = life_constraint_refs
    if queue_e_cross_layer_gate_status:
        profile["background_queue_e_cross_layer_gate_status"] = (
            queue_e_cross_layer_gate_status
        )
    if life_constraint_waiting_posture:
        profile["background_life_constraint_waiting_posture"] = str(
            life_constraint_waiting_posture
        )
    if life_constraint_attention_target:
        profile["background_life_constraint_attention_target"] = str(
            life_constraint_attention_target
        )
    if life_constraint_attention_reason:
        profile["background_life_constraint_attention_reason"] = str(
            life_constraint_attention_reason
        )
    if queue_e_birth_repair_waiting_profile:
        profile["background_queue_e_birth_repair_waiting_profile"] = (
            queue_e_birth_repair_waiting_profile
        )
    if queue_e_birth_repair_gate_status:
        profile["background_queue_e_birth_repair_gate_status"] = str(
            queue_e_birth_repair_gate_status
        )
    if queue_e_birth_repair_profile_ref:
        profile["background_queue_e_birth_repair_profile_ref"] = str(
            queue_e_birth_repair_profile_ref
        )
    if queue_e_birth_repair_pressure_level:
        profile["background_queue_e_birth_repair_pressure_level"] = str(
            queue_e_birth_repair_pressure_level
        )
    if queue_e_birth_repair_attention_target:
        profile["background_queue_e_birth_repair_attention_target"] = str(
            queue_e_birth_repair_attention_target
        )
    if queue_e_birth_repair_ref_set:
        profile["background_queue_e_birth_repair_ref_set"] = (
            queue_e_birth_repair_ref_set
        )
    if queue_e_birth_repair_waiting_posture:
        profile["background_queue_e_birth_repair_waiting_posture"] = str(
            queue_e_birth_repair_waiting_posture
        )
    if queue_e_birth_repair_attention_reason:
        profile["background_queue_e_birth_repair_attention_reason"] = str(
            queue_e_birth_repair_attention_reason
        )
    if resident_process_lease_history_profile:
        profile["background_resident_process_lease_history_profile_ref"] = (
            BACKGROUND_RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF
        )
        profile["background_resident_process_lease_history_profile"] = (
            resident_process_lease_history_profile
        )
        profile["resident_process_lease_history_profile_ref"] = (
            resident_process_lease_history_profile.get(
                "resident_process_lease_history_profile_ref"
            )
            or BACKGROUND_RESIDENT_PROCESS_LEASE_HISTORY_PROFILE_REF
        )
        profile["resident_process_identity_continuity_state"] = str(
            resident_process_lease_history_profile.get(
                "current_identity_continuity_state",
                "no_lease_history",
            )
        )
        profile["resident_process_identity_pressure_level"] = str(
            resident_process_lease_history_profile.get(
                "identity_pressure_level",
                "light",
            )
        )
        profile["resident_process_lease_history_event_count"] = _int_or_zero(
            resident_process_lease_history_profile.get("history_event_count")
        )
        profile["resident_process_recent_ids"] = _list_or_empty(
            resident_process_lease_history_profile.get("recent_resident_process_ids")
        )
        profile["resident_process_recent_run_ids"] = _list_or_empty(
            resident_process_lease_history_profile.get("recent_run_ids")
        )
    if resident_governance_state:
        profile["background_resident_governance_state_ref"] = (
            BACKGROUND_RESIDENT_GOVERNANCE_STATE_REF
        )
    if background_convergence_summary:
        profile["background_convergence_summary_ref"] = (
            BACKGROUND_CONVERGENCE_SUMMARY_REF
        )
        for key in [
            "convergence_state",
            "convergence_pressure_level",
            "convergence_attention_target",
            "relationship_stage_continuity",
            "trait_convergence_score",
            "max_trait_delta_from_background",
            "average_trait_delta_from_background",
            "trait_convergence_summary",
        ]:
            if key in background_convergence_summary:
                profile[f"background_{key}"] = background_convergence_summary[key]
    if background_convergence_history:
        profile["background_convergence_history_ref"] = (
            BACKGROUND_CONVERGENCE_HISTORY_REF
        )
        profile["background_convergence_history"] = background_convergence_history
        for source_key, target_key in [
            ("trend_state", "background_convergence_history_trend_state"),
            ("history_window_size", "background_convergence_history_window_size"),
            (
                "dominant_convergence_pressure_level",
                "background_dominant_convergence_pressure_level",
            ),
            (
                "dominant_convergence_state",
                "background_dominant_convergence_state",
            ),
            (
                "trait_convergence_history_profile",
                "background_trait_convergence_history_profile",
            ),
            (
                "trait_convergence_unstable_names",
                "background_trait_convergence_unstable_names",
            ),
            (
                "trait_convergence_stable_names",
                "background_trait_convergence_stable_names",
            ),
            (
                "trait_convergence_history_focus",
                "background_trait_convergence_history_focus",
            ),
            (
                "trait_drift_update_mode_summary",
                "background_trait_drift_update_mode_summary",
            ),
            (
                "trait_drift_background_history_recalibration_names",
                "background_trait_drift_recalibration_names",
            ),
            (
                "trait_drift_background_history_stabilized_names",
                "background_trait_drift_stabilized_names",
            ),
        ]:
            if source_key in background_convergence_history:
                profile[target_key] = background_convergence_history[source_key]
    if snapshot:
        profile["background_resident_governance_snapshot_ref"] = (
            BACKGROUND_RESIDENT_GOVERNANCE_SNAPSHOT_REF
        )
    if resident_governance_report:
        profile["background_resident_governance_report_ref"] = (
            BACKGROUND_RESIDENT_GOVERNANCE_REPORT_REF
        )
    if resident_governance_explanation:
        profile["background_resident_governance_explanation_ref"] = (
            BACKGROUND_RESIDENT_GOVERNANCE_EXPLANATION_REF
        )
        if resident_governance_explanation.get("dominant_driver_family"):
            profile["background_governance_driver_family"] = str(
                resident_governance_explanation["dominant_driver_family"]
            )
        if resident_governance_explanation.get("next_wake_expectation"):
            profile["background_next_wake_expectation"] = str(
                resident_governance_explanation["next_wake_expectation"]
            )
        explanation_story = _list_or_empty(
            resident_governance_explanation.get("continuity_story")
        )
        if explanation_story:
            profile["background_governance_explanation_story"] = explanation_story
    if persistent_process_report:
        profile["background_persistent_process_report_ref"] = (
            BACKGROUND_PERSISTENT_PROCESS_REPORT_REF
        )
    if not has_background_carryover_source:
        for key in [
            "background_continuity_mode",
            "background_carryover_pressure_level",
            "background_carryover_attention_target",
            "background_carryover_priority_profile",
            "background_carryover_generation",
            "background_waiting_mode",
        ]:
            profile.pop(key, None)
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


def _max_history_generation(history: dict[str, Any]) -> int:
    samples = history.get("convergence_samples", [])
    if not isinstance(samples, list):
        return 0
    return max(
        [
            _int_or_zero(sample.get("background_carryover_generation"))
            for sample in samples
            if isinstance(sample, dict)
        ],
        default=0,
    )


def _list_or_empty(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dedupe_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _dict_or_empty(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    return value


def _stronger_pressure(*values: Any) -> str:
    rank = {"light": 0, "present": 1, "elevated": 2, "urgent": 3}
    strongest = "light"
    for value in values:
        text = str(value or "")
        if rank.get(text, -1) > rank[strongest]:
            strongest = text
    return strongest


def _first_present(
    *payloads: dict[str, Any],
    keys: tuple[str, ...],
) -> Any:
    for payload in payloads:
        for key in keys:
            value = payload.get(key)
            if value:
                return value
    return None


def _first_dict(
    *payloads: dict[str, Any],
    keys: tuple[str, ...],
) -> dict[str, Any]:
    value = _first_present(*payloads, keys=keys)
    return _dict_or_empty(value)


def _collect_lists(
    *payloads: dict[str, Any],
    keys: tuple[str, ...],
) -> list[str]:
    values: list[str] = []
    for payload in payloads:
        for key in keys:
            values.extend(_list_or_empty(payload.get(key)))
    return values


def _background_live_language_presence_profile(
    *,
    live_language_turn_refs: list[str],
    last_live_semantic_focus: Any,
    source_profile: dict[str, Any],
) -> dict[str, Any]:
    source_ref_set = _list_or_empty(source_profile.get("ref_set"))
    ref_set = _dedupe_list(list(live_language_turn_refs) + source_ref_set)
    profile = {
        "schema_version": "background_live_language_presence_profile_v0",
        "continuity_mode": "closed_process_live_language_carryover",
        "live_language_turn_refs": list(live_language_turn_refs),
        "last_live_semantic_focus": (
            str(last_live_semantic_focus) if last_live_semantic_focus else None
        ),
        "ref_count": len(ref_set),
        "ref_set": ref_set,
        "source_continuity_mode": source_profile.get("continuity_mode"),
        "source_ref_count": source_profile.get("ref_count"),
    }
    return {
        key: value
        for key, value in profile.items()
        if value is not None and value != [] and value != {}
    }


def _idle_heartbeat_trace_count(path: Path) -> int:
    max_counter = 0
    line_count = 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return 0
    for line in lines:
        if not line.strip():
            continue
        line_count += 1
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict):
            max_counter = max(
                max_counter,
                _int_or_zero(event.get("heartbeat_counter")),
            )
    return max(max_counter, line_count)
