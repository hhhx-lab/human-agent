from __future__ import annotations

from typing import Any


def build_prediction_workspace_frame(
    run_id: str,
    generated_at: str,
    language_continuity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    continuity = {
        "shared_language_refs": list((language_continuity or {}).get("shared_language_refs", [])),
        "expression_monitor_refs": list((language_continuity or {}).get("expression_monitor_refs", [])),
        "relation_scope_refs": list((language_continuity or {}).get("relation_scope_refs", [])),
        "commitment_refs": list((language_continuity or {}).get("commitment_refs", [])),
        "self_narrative_trace_refs": list((language_continuity or {}).get("self_narrative_trace_refs", [])),
        "dialogue_turn_log_refs": list((language_continuity or {}).get("dialogue_turn_log_refs", [])),
        "language_percept_refs": list((language_continuity or {}).get("language_percept_refs", [])),
        "semantic_map_refs": list((language_continuity or {}).get("semantic_map_refs", [])),
        "semantic_ambiguity_refs": list((language_continuity or {}).get("semantic_ambiguity_refs", [])),
        "semantic_prediction_focus": (language_continuity or {}).get("semantic_prediction_focus"),
    }
    has_language_handoff = bool(continuity["language_percept_refs"] or continuity["semantic_map_refs"])
    has_ambiguity_queue = bool(continuity["semantic_ambiguity_refs"])
    semantic_focus = continuity["semantic_prediction_focus"] or "continuity-seed-focus"
    return {
        "schema_version": "prediction_workspace_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": "S02_NEURAL_LIFE_CORE",
        "source_runtime": "PredictionActiveInferenceRuntime",
        "workspace_frame_target_ref": "runtime/state/consciousness/workspace_frame.json",
        "source_doc_refs": [
            "docs/01v_prediction_active_inference_runtime_matrix.md",
            "docs/04_sensory_thalamus_interoception.md",
            "docs/10_consciousness_attention_workspace.md",
            "docs/11_neuromodulation_and_signal_media.md",
        ],
        "workspace_contents": {
            "candidate_explanations": (
                [
                    {
                        "explanation_id": "semantic-focus-v0-0001",
                        "explanation_family": "language_semantic_handoff",
                        "focus": semantic_focus,
                    }
                ]
                if semantic_focus
                else []
            ),
            "precision_state": "semantic_handoff_seeded" if has_language_handoff else "seed_only",
            "active_sampling_mode": "clarify_ambiguity" if has_ambiguity_queue else "observation_first",
            "language_continuity_focus": continuity,
        },
        "bus_edge_refs": [
            "prediction_error_bus",
            "conscious_broadcast_bus",
        ],
        "downstream_systems": [
            "ConsciousWorkspaceRuntime",
            "LanguageRelationshipRuntime",
        ],
    }
