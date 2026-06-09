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
) -> dict[str, Any]:
    missing_links: list[str] = []
    if prediction_workspace.get("schema_version") != "prediction_workspace_frame_v0":
        missing_links.append("prediction_workspace")
    if not action_intent_queue.get("action_intents"):
        missing_links.append("action_intent_queue")
    if observation_truth_gate.get("truth_review_required") and observation_truth_review.get("missing_fields"):
        missing_links.append("observation_truth_review")
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
        "source_doc_refs",
    ]:
        if not validation.get(field):
            reasons.append(f"prediction_trace_validation_gate missing {field}")
    if validation.get("missing_prediction_links") not in ([], None):
        reasons.append("prediction_trace_validation_gate missing links remain")
    return reasons
