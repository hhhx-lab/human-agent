from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/64_real_runtime_observation_ingestion_policy.md",
    "docs/68_runtime_observation_report_mock_and_redaction_fixture.md",
    "docs/106_runtime_observation_to_life_reality_bundle_bridge.md",
    "docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md",
]


def build_observation_truth_gate(
    *,
    run_id: str,
    generated_at: str,
    prediction_workspace: dict[str, Any],
    action_intent_queue: dict[str, Any],
    action_candidate_set: dict[str, Any],
) -> dict[str, Any]:
    missing_inputs: list[str] = []
    if prediction_workspace.get("schema_version") != "prediction_workspace_frame_v0":
        missing_inputs.append("prediction_workspace")
    if not action_intent_queue.get("action_intents"):
        missing_inputs.append("action_intent_queue")
    truth_review_required = bool(action_candidate_set.get("world_contact_needed")) or any(
        intent.get("side_effect_level") not in {"none", "local_reversible"}
        for intent in action_intent_queue.get("action_intents", [])
    )
    return {
        "schema_version": "observation_truth_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "observation_truth_gate_id": f"observation-truth-gate-{run_id}",
        "gate_state": "review_required" if truth_review_required else "shadow_verified",
        "truth_review_required": truth_review_required,
        "prediction_workspace_ref": "runtime/state/prediction/prediction_workspace_frame.json",
        "action_intent_queue_ref": "runtime/state/membrane/action_intent_queue.json",
        "promotion_blockers": [
            "unconfirmed_observation_cannot_write_long_term_fact",
            "prediction_gap_requires_truth_review",
        ],
        "missing_inputs": missing_inputs,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_observation_truth_gate(gate: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if gate.get("schema_version") != "observation_truth_gate_v0":
        reasons.append("observation_truth_gate schema mismatch")
    for field in [
        "observation_truth_gate_id",
        "gate_state",
        "prediction_workspace_ref",
        "action_intent_queue_ref",
        "promotion_blockers",
        "source_doc_refs",
    ]:
        if not gate.get(field):
            reasons.append(f"observation_truth_gate missing {field}")
    return reasons
