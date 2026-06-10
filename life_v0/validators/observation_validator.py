from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/64_real_runtime_observation_ingestion_policy.md",
    "docs/68_runtime_observation_report_mock_and_redaction_fixture.md",
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_observation_truth_review(
    *,
    run_id: str,
    generated_at: str,
    observation_intake: dict[str, Any],
    prediction_workspace: dict[str, Any],
    action_candidate_set: dict[str, Any],
    world_observation_route: dict[str, Any] | None = None,
    periphery_normalization_trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    world_observation_route = world_observation_route or {}
    periphery_normalization_trace = periphery_normalization_trace or {}
    missing_fields: list[str] = []
    if prediction_workspace.get("schema_version") != "prediction_workspace_frame_v0":
        missing_fields.append("prediction_workspace")
    if not action_candidate_set.get("candidate_actions"):
        missing_fields.append("candidate_actions")
    if world_observation_route.get("schema_version") != "world_observation_route_v0":
        missing_fields.append("world_observation_route")
    if periphery_normalization_trace.get("schema_version") != "periphery_normalization_trace_v0":
        missing_fields.append("periphery_normalization_trace")
    return {
        "schema_version": "observation_truth_review_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "observation_validation_id": f"observation-truth-review-{run_id}",
        "observation_event_refs": list(observation_intake.get("report_refs", []))
        + list(observation_intake.get("observation_route_refs", []))
        + ["runtime/state/action/action_candidate_set.json"],
        "scene_frame_ref": "runtime/state/observation/runtime_observation_intake.json",
        "prediction_workspace_ref": "runtime/state/prediction/prediction_workspace_frame.json",
        "world_observation_route_ref": (
            "runtime/state/observation/world_observation_route.json"
            if world_observation_route
            else None
        ),
        "periphery_normalization_ref": (
            "runtime/state/observation/periphery_normalization_trace.json"
            if periphery_normalization_trace
            else None
        ),
        "missing_fields": missing_fields,
        "truth_review_required": bool(action_candidate_set.get("world_contact_needed")),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_observation_truth_review(review: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if review.get("schema_version") != "observation_truth_review_v0":
        reasons.append("observation_truth_gate schema mismatch")
    for field in [
        "observation_validation_id",
        "observation_event_refs",
        "scene_frame_ref",
        "prediction_workspace_ref",
        "world_observation_route_ref",
        "periphery_normalization_ref",
    ]:
        if not review.get(field):
            reasons.append(f"observation_truth_gate missing {field}")
    return reasons
