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


def build_validation_rollup(
    *,
    run_id: str,
    generated_at: str,
    observation_truth_review: dict[str, Any],
    world_contact_validation: dict[str, Any],
    prediction_trace_validation: dict[str, Any],
    boundary_audit: dict[str, Any],
) -> dict[str, Any]:
    cross_layer_gate_status = dict(world_contact_validation.get("life_constraint_validation", {}))
    life_constraint_blocked = any(
        status == "missing" or status == "blocked"
        for status in cross_layer_gate_status.values()
    )
    gate_status = {
        "observation_truth_gate": "closed" if not observation_truth_review.get("missing_fields") else "guarded",
        "world_contact_validation_gate": world_contact_validation.get("status", "blocked"),
        "prediction_trace_validation_gate": prediction_trace_validation.get("status", "blocked"),
        "boundary_audit_gate": "closed" if not boundary_audit.get("audit_findings") else "guarded",
        "life_constraint_validation_gate": "blocked" if life_constraint_blocked else "closed",
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
        "queue_e_cross_layer_refs": list(world_contact_validation.get("life_constraint_refs", [])),
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
        "state_refs",
        "next_stage_ready",
        "source_doc_refs",
    ]:
        if not rollup.get(field):
            reasons.append(f"validation_rollup_gate missing {field}")
    return reasons
