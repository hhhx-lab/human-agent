from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/01w_prediction_active_inference_schema_fixture_contract.md",
    "docs/01y_prediction_active_inference_schema_write_batch.md",
]


def build_prediction_error_field(
    *,
    run_id: str,
    generated_at: str,
    belief_state: dict[str, Any],
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    signal_media_runtime = signal_media_runtime or {}
    unexpected_uncertainty = (
        signal_media_runtime.get("modulation_vector", {}).get("unexpected_uncertainty", 0.21)
    )
    stage_effect = "hold_for_evidence" if unexpected_uncertainty >= 0.2 else "repair"
    return {
        "schema_version": "prediction_error_field_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "error_field_id": f"prediction-error-{run_id}",
        "belief_frame_ref": "runtime/state/prediction/belief_state_frame.json",
        "error_events": [
            {
                "error_id": "semantic-ambiguity-0001",
                "error_kind": "semantic",
                "expected": "共享语言连续稳定",
                "observed": "仍存在语义歧义待澄清",
                "delta": "clarify_before_commitment",
                "precision_request": "high",
            },
            {
                "error_id": "relationship-guard-0001",
                "error_kind": "social",
                "expected": "关系连续体保持低伤害表达",
                "observed": "需要先审视关系边界与承诺真值",
                "delta": "guarded_review_required",
                "precision_request": "high",
            },
        ],
        "precision_requests": [
            "raise_relationship_precision",
            "hold_external_action",
        ],
        "affected_life_targets": belief_state.get("active_life_targets", []),
        "workspace_entry_candidates": [
            "semantic_disambiguation",
            "relationship_guard_review",
        ],
        "dream_replay_candidates": [
            "runtime/state/dream/dream_consolidation_frame.json#ambiguity_replay_seed",
        ],
        "stage_effect": stage_effect,
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
    }
