from __future__ import annotations

from typing import Any


def build_prediction_workspace_frame(
    run_id: str,
    generated_at: str,
    language_continuity: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    belief_state = belief_state or {}
    prediction_error_field = prediction_error_field or {}
    active_sampling_plan = active_sampling_plan or {}
    signal_media_runtime = signal_media_runtime or {}
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
        "prediction_error_refs": list((language_continuity or {}).get("prediction_error_refs", [])),
        "signal_media_refs": list((language_continuity or {}).get("signal_media_refs", [])),
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
            "precision_state": (
                signal_media_runtime.get("precision_policy", {}).get("policy_mode")
                or ("semantic_handoff_seeded" if has_language_handoff else "seed_only")
            ),
            "active_sampling_mode": (
                active_sampling_plan.get("selected_route")
                or ("clarify_ambiguity" if has_ambiguity_queue else "observation_first")
            ),
            "language_continuity_focus": continuity,
            "belief_scope": belief_state.get("state_scope"),
            "sampling_stage_effect": active_sampling_plan.get("stage_effect"),
        },
        "belief_state_ref": (
            "runtime/state/prediction/belief_state_frame.json"
            if belief_state
            else None
        ),
        "prediction_error_ref": (
            "runtime/state/prediction/prediction_error_field.json"
            if prediction_error_field
            else None
        ),
        "active_sampling_plan_ref": (
            "runtime/state/prediction/active_sampling_plan.json"
            if active_sampling_plan
            else None
        ),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "bus_edge_refs": [
            "prediction_error_bus",
            "conscious_broadcast_bus",
        ],
        "downstream_systems": [
            "ConsciousWorkspaceRuntime",
            "LanguageRelationshipRuntime",
        ],
    }
