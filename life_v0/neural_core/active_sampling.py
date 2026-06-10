from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/01w_prediction_active_inference_schema_fixture_contract.md",
    "docs/01y_prediction_active_inference_schema_write_batch.md",
]


def build_active_sampling_plan(
    *,
    run_id: str,
    generated_at: str,
    belief_state: dict[str, Any],
    prediction_error_field: dict[str, Any],
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    signal_media_runtime = signal_media_runtime or {}
    relationship_pressure = (
        signal_media_runtime.get("modulation_vector", {}).get("relationship_pressure", 0.0)
    )
    selected_route = "clarify" if relationship_pressure < 0.4 else "inspect"
    return {
        "schema_version": "active_sampling_plan_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "sampling_plan_id": f"active-sampling-{run_id}",
        "belief_frame_ref": "runtime/state/prediction/belief_state_frame.json",
        "prediction_error_ref": "runtime/state/prediction/prediction_error_field.json",
        "candidate_refs": [
            "epistemic_candidate_review_semantic_map",
            "epistemic_candidate_review_relation_scope",
            "epistemic_candidate_review_commitment_truth",
        ],
        "selected_route": selected_route,
        "guard_refs": [
            "direction_anchor_guard",
            "birth_readiness_false_open_guard",
            "relation_scope_guard",
            "external_action_membrane_guard",
        ],
        "scope_refs": [
            "runtime/state/language/semantic_map_state.json",
            "runtime/state/language/relation_scope_language_index.json",
            "runtime/state/relationship/commitment_truth_state.json",
        ],
        "command_binding_refs": [
            "inspect_language_runtime",
            "inspect_relation_scope",
            "inspect_commitment_truth",
        ],
        "expected_observation_refs": [
            "runtime/state/language/language_percept_state.json",
            "runtime/state/language/dialogue_turn_log.jsonl",
            "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs",
        ],
        "stage_effect": prediction_error_field.get("stage_effect", "hold_for_evidence"),
        "archive_edge_plan": {
            "receipt_ref": f"runtime/receipts/neural_life_core_{run_id}.json",
            "replay_route": "prediction_active_inference_archive_seed",
            "if_conflict": "quarantine_candidate_before_writeback",
        },
        "affected_life_targets": belief_state.get("active_life_targets", []),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
    }
