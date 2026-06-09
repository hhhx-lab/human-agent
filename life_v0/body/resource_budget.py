from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/37_life_support_layer_policy.md",
    "docs/181_life_reality_first_runner_schema_runtime_mount_plan.md",
    "docs/186_life_reality_first_runner_schema_runtime_smoke_observation_feedback_loop.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_body_resource_budget(
    *,
    run_id: str,
    generated_at: str,
    validation_report: dict[str, Any],
    schema_report: dict[str, Any],
    schema_smoke: dict[str, Any],
    life_state: dict[str, Any],
    need_state: dict[str, Any],
    rhythm_pulse: dict[str, Any],
    recovery_path: dict[str, Any],
) -> dict[str, Any]:
    readiness_status = life_state.get("birth_readiness", {}).get("overall_status", "state_root_seeded")
    language_state = life_state.get("language_state", {})
    continuity_pressure = {
        "shared_language_ref_count": len(language_state.get("shared_language_refs", [])),
        "expression_monitor_ref_count": len(language_state.get("expression_monitor_refs", [])),
        "relation_scope_ref_count": len(language_state.get("relation_scope_refs", [])),
        "commitment_ref_count": len(language_state.get("promise_refs", [])),
        "self_narrative_trace_ref_count": len(language_state.get("self_narrative_trace_refs", [])),
        "language_percept_ref_count": len(language_state.get("language_percept_refs", [])),
        "semantic_map_ref_count": len(language_state.get("semantic_map_refs", [])),
    }
    return {
        "schema_version": "body_resource_budget_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": "S06_LIFE_SUPPORT_DEVELOPMENT",
        "body_mode": "pre_activation_guarded_body",
        "need_state_ref": "runtime/state/body/need_state_vector.json",
        "rhythm_ref": "runtime/state/body/body_rhythm_pulse.json",
        "recovery_path_ref": "runtime/state/body/recovery_path.json",
        "energy_state": {
            "level": "guarded_reserve",
            "reserve_fraction": 0.72,
            "direction_lock_mode": "preserve_core_continuity_before_activation",
        },
        "fatigue_state": {
            "level": rhythm_pulse.get("fatigue_load", "managed_low_noise"),
            "policy": "shadow_only_no_irreversible_action",
            "life_state_birth_readiness": readiness_status,
        },
        "maintenance_pressure": {
            "status": "validation_closed_schema_ready",
            "validation_stage_effect": validation_report.get("stage_effect"),
            "schema_stage_effect": schema_report.get("stage_effect"),
            "schema_smoke_status": schema_smoke.get("status"),
            "language_continuity_pressure": continuity_pressure,
            "resource_deficit": need_state.get("resource_deficit"),
            "repair_drive": need_state.get("repair_drive"),
        },
        "recovery_priority": list(recovery_path.get("recovery_priority", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
        "report_refs": [
            "runtime/reports/latest/validation_membrane_report.json",
            "runtime/reports/latest/schema_runner_report.json",
            "runtime/reports/latest/schema_smoke_report.json",
        ],
    }
