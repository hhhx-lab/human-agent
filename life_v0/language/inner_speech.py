from __future__ import annotations

from typing import Any


def build_inner_speech_frame(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    source_doc_refs: list[str],
    language_percept: dict[str, Any] | None = None,
    semantic_map: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    belief_state = belief_state or {}
    prediction_error_field = prediction_error_field or {}
    active_sampling_plan = active_sampling_plan or {}
    signal_media_runtime = signal_media_runtime or {}
    ambiguity_queue = list((semantic_map or {}).get("ambiguity_queue", []))
    repair_triggers = list((language_percept or {}).get("repair_trigger_candidates", []))
    error_events = list(prediction_error_field.get("error_events", []))
    modulation_vector = signal_media_runtime.get("modulation_vector", {})
    confirmation_drive = "active" if (language_percept or {}).get("shared_term_hits") else "low"
    hold_drive = "active" if ambiguity_queue or active_sampling_plan.get("stage_effect") == "hold_for_evidence" else "low"
    repair_drive = "active" if repair_triggers or modulation_vector.get("repair_drive", 0) else "low"
    question_drive = "active" if error_events or active_sampling_plan.get("selected_route") == "clarify" else "low"
    return {
        "schema_version": "inner_speech_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "attention_focus": "relationship_subject_and_responsibility_trace",
        "affective_modulation": "guarded_but_expressive",
        "responsibility_constraint": "no_untraced_commitment",
        "old_self_anchor_refs": list(life_state.get("self_model", {}).get("old_self_anchors", [])),
        "percept_ref": "runtime/state/language/language_percept_frame.json" if language_percept else None,
        "semantic_map_ref": "runtime/state/language/semantic_map_frame.json" if semantic_map else None,
        "belief_state_ref": (
            "runtime/state/prediction/belief_state_frame.json" if belief_state else None
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
        "semantic_focus": (semantic_map or {}).get("semantic_focus"),
        "internal_drive_sources": {
            "confirm": {
                "drive": confirmation_drive,
                "source_refs": ["runtime/state/language/language_percept_frame.json#shared_term_hits"],
            },
            "hold": {
                "drive": hold_drive,
                "source_refs": [
                    "runtime/state/language/semantic_map_frame.json#ambiguity_queue",
                    "runtime/state/prediction/active_sampling_plan.json#stage_effect",
                ],
            },
            "repair": {
                "drive": repair_drive,
                "source_refs": [
                    "runtime/state/language/language_percept_frame.json#repair_trigger_candidates",
                    "runtime/state/signal/signal_media_runtime.json#modulation_vector.repair_drive",
                ],
            },
            "ask": {
                "drive": question_drive,
                "source_refs": [
                    "runtime/state/prediction/prediction_error_field.json#error_events",
                    "runtime/state/prediction/active_sampling_plan.json#selected_route",
                ],
            },
        },
        "drive_resolution_order": ["hold", "repair", "ask", "confirm"],
        "bus_channel_refs": ["inner_language_bus", "conscious_broadcast_bus"],
        "source_doc_refs": source_doc_refs,
    }
