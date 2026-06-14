from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/10_consciousness_attention_workspace.md",
    "docs/22_state_transition_and_threshold_model.md",
    "docs/30_state_transition_validator_rules.md",
    "docs/64_real_runtime_observation_ingestion_policy.md",
    "docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md",
]


def build_prediction_trace_validation(
    *,
    run_id: str,
    generated_at: str,
    prediction_workspace: dict[str, Any],
    action_intent_queue: dict[str, Any],
    observation_truth_gate: dict[str, Any],
    observation_truth_review: dict[str, Any],
    world_observation_route: dict[str, Any] | None = None,
    periphery_normalization_trace: dict[str, Any] | None = None,
    world_contact_validation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    world_observation_route = world_observation_route or {}
    periphery_normalization_trace = periphery_normalization_trace or {}
    world_contact_validation = world_contact_validation or {}
    missing_links: list[str] = []
    if prediction_workspace.get("schema_version") != "prediction_workspace_frame_v0":
        missing_links.append("prediction_workspace")
    if not action_intent_queue.get("action_intents"):
        missing_links.append("action_intent_queue")
    if observation_truth_gate.get("truth_review_required") and observation_truth_review.get("missing_fields"):
        missing_links.append("observation_truth_review")
    if prediction_workspace.get("active_sampling_plan_ref") != "runtime/state/prediction/active_sampling_plan.json":
        missing_links.append("active_sampling_plan")
    if world_observation_route.get("schema_version") != "world_observation_route_v0":
        missing_links.append("world_observation_route")
    if world_observation_route.get("active_sampling_plan_ref") != "runtime/state/prediction/active_sampling_plan.json":
        missing_links.append("world_observation_active_sampling_ref")
    if periphery_normalization_trace.get("schema_version") != "periphery_normalization_trace_v0":
        missing_links.append("periphery_normalization_trace")
    if periphery_normalization_trace.get("world_observation_route_ref") != "runtime/state/observation/world_observation_route.json":
        missing_links.append("periphery_world_observation_ref")
    if world_contact_validation and world_contact_validation.get("status") != "closed":
        missing_links.append("world_contact_validation")
    prediction_trace_refs = _dedupe_string_refs(
        [
            "runtime/state/prediction/belief_state_frame.json",
            prediction_workspace.get("prediction_error_ref"),
            prediction_workspace.get("active_sampling_plan_ref"),
            "runtime/state/observation/world_observation_route.json"
            if world_observation_route
            else None,
            "runtime/state/observation/periphery_normalization_trace.json"
            if periphery_normalization_trace
            else None,
            "runtime/state/validation/observation_truth_review.json"
            if observation_truth_review
            else None,
            "runtime/state/validation/world_contact_validation.json"
            if world_contact_validation
            else None,
            *list(world_observation_route.get("guard_refs", [])),
            *list(periphery_normalization_trace.get("write_target_refs", [])),
        ]
    )
    return {
        "schema_version": "prediction_trace_validation_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "prediction_trace_validation_id": f"prediction-trace-validation-{run_id}",
        "status": "closed" if not missing_links else "blocked",
        "prediction_workspace_ref": "runtime/state/prediction/prediction_workspace_frame.json",
        "action_intent_queue_ref": "runtime/state/membrane/action_intent_queue.json",
        "observation_truth_gate_ref": "runtime/state/membrane/observation_truth_gate.json",
        "observation_truth_review_ref": "runtime/state/validation/observation_truth_review.json",
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
        "world_contact_validation_ref": (
            "runtime/state/validation/world_contact_validation.json"
            if world_contact_validation
            else None
        ),
        "active_sampling_plan_ref": prediction_workspace.get(
            "active_sampling_plan_ref",
            "runtime/state/prediction/active_sampling_plan.json",
        ),
        "world_observation_route_mode": world_observation_route.get("route_mode"),
        "periphery_normalization_policy": periphery_normalization_trace.get(
            "normalization_policy"
        ),
        "prediction_trace_refs": prediction_trace_refs,
        "world_contact_validation_status": world_contact_validation.get("status"),
        "truth_review_required": bool(observation_truth_gate.get("truth_review_required")),
        "missing_prediction_links": missing_links,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_prediction_trace_validation(validation: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if validation.get("schema_version") != "prediction_trace_validation_v0":
        reasons.append("prediction_trace_validation_gate schema mismatch")
    if validation.get("status") != "closed":
        reasons.append("prediction_trace_validation_gate status mismatch")
    for field in [
        "prediction_trace_validation_id",
        "prediction_workspace_ref",
        "action_intent_queue_ref",
        "observation_truth_gate_ref",
        "observation_truth_review_ref",
        "world_observation_route_ref",
        "periphery_normalization_ref",
        "world_contact_validation_ref",
        "active_sampling_plan_ref",
        "prediction_trace_refs",
        "source_doc_refs",
    ]:
        if not validation.get(field):
            reasons.append(f"prediction_trace_validation_gate missing {field}")
    if validation.get("missing_prediction_links") not in ([], None):
        reasons.append("prediction_trace_validation_gate missing links remain")
    return reasons


def _dedupe_string_refs(refs: list[Any]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if not isinstance(ref, str) or not ref or ref in seen:
            continue
        seen.add(ref)
        merged.append(ref)
    return merged
