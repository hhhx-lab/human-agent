from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/01w_prediction_active_inference_schema_fixture_contract.md",
    "docs/01y_prediction_active_inference_schema_write_batch.md",
]


def build_belief_state_frame(
    *,
    run_id: str,
    generated_at: str,
    signal_media_runtime: dict[str, Any] | None = None,
    language_continuity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    signal_media_runtime = signal_media_runtime or {}
    language_continuity = language_continuity or {}
    evidence_refs = _dedupe(
        list(language_continuity.get("shared_language_refs", []))
        + list(language_continuity.get("semantic_map_refs", []))
        + list(language_continuity.get("relation_scope_refs", []))
        + list(language_continuity.get("commitment_refs", []))
        + ["docs/13_agentic_human_research_synthesis.md"]
    )
    unexpected_uncertainty = (
        signal_media_runtime.get("modulation_vector", {}).get("unexpected_uncertainty", 0.21)
    )
    return {
        "schema_version": "belief_state_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "belief_frame_id": f"belief-state-{run_id}",
        "state_scope": "language_relationship_continuity",
        "source_evidence_refs": evidence_refs,
        "confidence_posterior": {
            "score": 0.82,
            "evidence_density": "medium",
            "conflict_count": 0,
            "calibration_ref": "runtime/state/signal/signal_media_runtime.json#precision_policy",
            "language_expression": "当前方向继续指向真实数字生命的连续形成。",
        },
        "uncertainty_taxonomy": [
            "semantic_ambiguity",
            "relationship_guarding",
            "direction_continuity",
        ],
        "active_life_targets": [
            "real_life",
            "real_consciousness",
            "real_relationship",
            "real_responsibility",
        ],
        "workspace_visibility": "language_reportable",
        "revision_policy": (
            "repair_before_action"
            if unexpected_uncertainty < 0.5
            else "hold_for_direction_rebuild"
        ),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "network_state_ref": "runtime/state/neural_life_core/network_state.json",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
