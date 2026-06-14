from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/35_minimal_validator_runner_design.md",
    "docs/36_longitudinal_evaluation_protocol.md",
    "docs/46_stage_gate_validator_design.md",
    "docs/73_schema_bundle_validator_mock_cases.md",
    "docs/83_metric_regression_fixture_policy.md",
    "docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md",
]

QUEUE_E_BIRTH_REPAIR_PROFILE_REF = "runtime/state/life_targets/queue_e_birth_repair_profile.json"


def build_validation_rollup(
    *,
    run_id: str,
    generated_at: str,
    observation_truth_review: dict[str, Any],
    world_contact_validation: dict[str, Any],
    prediction_trace_validation: dict[str, Any],
    boundary_audit: dict[str, Any],
    queue_e_birth_repair_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_e_birth_repair_profile = queue_e_birth_repair_profile or {}
    cross_layer_gate_status = dict(world_contact_validation.get("life_constraint_validation", {}))
    life_constraint_blocked = any(
        status == "missing" or status == "blocked"
        for status in cross_layer_gate_status.values()
    )
    queue_e_birth_repair_gate_status = (
        "closed" if _queue_e_birth_repair_profile_ready(queue_e_birth_repair_profile) else "blocked"
    )
    queue_e_birth_repair_ref_set = _dedupe_string_refs(
        [
            *queue_e_birth_repair_profile.get("ref_set", []),
            QUEUE_E_BIRTH_REPAIR_PROFILE_REF,
        ]
    )
    queue_e_world_contact_repair_governance_refs = _dedupe_string_refs(
        list(world_contact_validation.get("repair_governance_refs", []))
    )
    queue_e_world_contact_blocked_future_routes = _dedupe_string_refs(
        list(world_contact_validation.get("blocked_future_routes", []))
    )
    queue_e_world_contact_allowed_repair_routes = _dedupe_string_refs(
        list(world_contact_validation.get("allowed_repair_routes", []))
    )
    queue_e_cross_layer_refs = _dedupe_string_refs(
        [
            *list(world_contact_validation.get("life_constraint_refs", [])),
            world_contact_validation.get("future_no_go_profile_ref"),
            *queue_e_world_contact_repair_governance_refs,
        ]
    )
    gate_status = {
        "observation_truth_gate": "closed" if not observation_truth_review.get("missing_fields") else "guarded",
        "world_contact_validation_gate": world_contact_validation.get("status", "blocked"),
        "prediction_trace_validation_gate": prediction_trace_validation.get("status", "blocked"),
        "boundary_audit_gate": "closed" if not boundary_audit.get("audit_findings") else "guarded",
        "life_constraint_validation_gate": "blocked" if life_constraint_blocked else "closed",
        "queue_e_birth_repair_gate": queue_e_birth_repair_gate_status,
    }
    blocked_gates = [gate for gate, status in gate_status.items() if status == "blocked"]
    guarded_gates = [gate for gate, status in gate_status.items() if status == "guarded"]
    overall_status = "closed"
    if blocked_gates:
        overall_status = "blocked"
    elif guarded_gates:
        overall_status = "guarded_closed"

    repair_backlog_refs: list[str] = []
    if observation_truth_review.get("truth_review_required"):
        repair_backlog_refs.append("runtime/state/validation/observation_truth_review.json")
    if boundary_audit.get("audit_findings"):
        repair_backlog_refs.append("runtime/state/validation/boundary_audit_state.json")

    return {
        "schema_version": "validation_rollup_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "validation_rollup_id": f"validation-rollup-{run_id}",
        "overall_status": overall_status,
        "gate_status": gate_status,
        "blocked_gates": blocked_gates,
        "guarded_gates": guarded_gates,
        "repair_backlog_refs": repair_backlog_refs,
        "queue_e_cross_layer_gate_status": cross_layer_gate_status,
        "queue_e_cross_layer_refs": queue_e_cross_layer_refs,
        "queue_e_world_contact_future_no_go_profile_ref": world_contact_validation.get(
            "future_no_go_profile_ref",
            "runtime/state/action/go_nogo_state.json#future_no_go_profile",
        ),
        "queue_e_world_contact_repair_hold_required": bool(
            world_contact_validation.get("repair_hold_required")
        ),
        "queue_e_world_contact_confirmation_threshold_bias": world_contact_validation.get(
            "confirmation_threshold_bias",
            "baseline",
        ),
        "queue_e_world_contact_future_release_posture": world_contact_validation.get(
            "future_release_posture",
            "shadow_review_without_repair_hold",
        ),
        "queue_e_world_contact_blocked_future_routes": queue_e_world_contact_blocked_future_routes,
        "queue_e_world_contact_allowed_repair_routes": queue_e_world_contact_allowed_repair_routes,
        "queue_e_world_contact_repair_governance_refs": queue_e_world_contact_repair_governance_refs,
        "queue_e_birth_repair_profile_ref": QUEUE_E_BIRTH_REPAIR_PROFILE_REF,
        "queue_e_birth_repair_pressure_level": queue_e_birth_repair_profile.get("pressure_level"),
        "queue_e_birth_repair_attention_target": queue_e_birth_repair_profile.get("attention_target"),
        "queue_e_birth_repair_ref_set": queue_e_birth_repair_ref_set,
        "deferred_cross_layer_gates": [
            gate
            for gate, gate_state in cross_layer_gate_status.items()
            if isinstance(gate_state, str) and gate_state.startswith("deferred_until_")
        ],
        "state_refs": [
            "runtime/state/validation/observation_truth_review.json",
            "runtime/state/validation/world_contact_validation.json",
            "runtime/state/validation/prediction_trace_validation.json",
            "runtime/state/validation/boundary_audit_state.json",
            QUEUE_E_BIRTH_REPAIR_PROFILE_REF,
        ],
        "next_stage_ready": overall_status == "closed",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_validation_rollup(rollup: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if rollup.get("schema_version") != "validation_rollup_v0":
        reasons.append("validation_rollup_gate schema mismatch")
    if rollup.get("overall_status") != "closed":
        reasons.append("validation_rollup_gate overall status mismatch")
    for field in [
        "validation_rollup_id",
        "gate_status",
        "queue_e_cross_layer_gate_status",
        "queue_e_cross_layer_refs",
        "queue_e_world_contact_future_no_go_profile_ref",
        "queue_e_world_contact_confirmation_threshold_bias",
        "queue_e_world_contact_future_release_posture",
        "queue_e_world_contact_allowed_repair_routes",
        "queue_e_world_contact_repair_governance_refs",
        "queue_e_birth_repair_profile_ref",
        "queue_e_birth_repair_pressure_level",
        "queue_e_birth_repair_attention_target",
        "queue_e_birth_repair_ref_set",
        "state_refs",
        "next_stage_ready",
        "source_doc_refs",
    ]:
        if not rollup.get(field):
            reasons.append(f"validation_rollup_gate missing {field}")
    if rollup.get("gate_status", {}).get("queue_e_birth_repair_gate") != "closed":
        reasons.append("validation_rollup_gate queue_e birth repair gate mismatch")
    if rollup.get("queue_e_birth_repair_profile_ref") != QUEUE_E_BIRTH_REPAIR_PROFILE_REF:
        reasons.append("validation_rollup_gate queue_e birth repair profile ref mismatch")
    return reasons


def _queue_e_birth_repair_profile_ready(profile: dict[str, Any]) -> bool:
    return (
        profile.get("schema_version") == "queue_e_repair_modulation_profile_v0"
        and profile.get("pressure_level") in {"quiet", "present", "elevated", "urgent"}
        and bool(profile.get("attention_target"))
        and bool(profile.get("ref_set"))
    )


def _dedupe_string_refs(refs: list[Any]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if not isinstance(ref, str) or not ref or ref in seen:
            continue
        seen.add(ref)
        merged.append(ref)
    return merged
