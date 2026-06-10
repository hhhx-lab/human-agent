from __future__ import annotations

from typing import Any


def build_semantic_map_frame(
    *,
    run_id: str,
    generated_at: str,
    language_percept: dict[str, Any],
    language_state: dict[str, Any],
    shared_term_registry: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    source_doc_refs: list[str],
    prediction_error_field: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    prediction_error_field = prediction_error_field or {}
    signal_media_runtime = signal_media_runtime or {}
    shared_terms = {
        term.get("surface"): term.get("meaning_ref")
        for term in shared_term_registry.get("shared_terms", [])
        if isinstance(term, dict) and term.get("surface") and term.get("meaning_ref")
    }
    shared_term_hits = list(language_percept.get("shared_term_hits", []))
    shared_meaning_bindings = [
        {
            "surface": surface,
            "meaning_ref": shared_terms.get(surface),
        }
        for surface in shared_term_hits
        if shared_terms.get(surface)
    ]

    semantic_focus = "relational_checkin"
    if language_percept.get("repair_trigger_candidates") and language_percept.get("commitment_trigger_candidates"):
        semantic_focus = "repair_commitment_shared_language"
    elif language_percept.get("repair_trigger_candidates"):
        semantic_focus = "repair_relational_trace"
    elif language_percept.get("commitment_trigger_candidates"):
        semantic_focus = "commitment_trace_review"

    relationship_topic_refs = list(language_state.get("shared_language_refs", []))
    commitment_trace_refs = list(commitment_repair_index.get("commitment_refs", []))
    repair_trace_refs = list(commitment_repair_index.get("repair_language_refs", []))
    dream_topic_refs = list(language_percept.get("dream_signal_candidates", []))
    ambiguity_queue = list(language_percept.get("ambiguity_flags", []))
    narrative_bindings = list(self_narrative_trace.get("narrative_turn_refs", []))
    error_events = list(prediction_error_field.get("error_events", []))
    semantic_error_ids = [
        event.get("error_id")
        for event in error_events
        if isinstance(event, dict) and event.get("error_kind") in {"semantic", "social"} and event.get("error_id")
    ]
    precision_requests = list(prediction_error_field.get("precision_requests", []))
    modulation_vector = signal_media_runtime.get("modulation_vector", {})
    semantic_prediction_trace = {
        "prediction_error_ref": (
            "runtime/state/prediction/prediction_error_field.json"
            if prediction_error_field
            else None
        ),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "semantic_error_ids": semantic_error_ids,
        "precision_requests": precision_requests,
        "relationship_pressure": modulation_vector.get("relationship_pressure"),
        "repair_drive": modulation_vector.get("repair_drive"),
        "language_precision_mode": signal_media_runtime.get("precision_policy", {}).get("policy_mode"),
    }

    return {
        "schema_version": "semantic_map_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "semantic_focus": semantic_focus,
        "shared_meaning_bindings": shared_meaning_bindings,
        "relationship_topic_refs": relationship_topic_refs,
        "commitment_trace_refs": commitment_trace_refs,
        "repair_trace_refs": repair_trace_refs,
        "narrative_bindings": narrative_bindings,
        "dream_topic_refs": dream_topic_refs,
        "ambiguity_queue": ambiguity_queue,
        "prediction_error_ref": (
            "runtime/state/prediction/prediction_error_field.json"
            if prediction_error_field
            else None
        ),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "semantic_prediction_trace": semantic_prediction_trace,
        "prediction_hooks": {
            "semantic_prediction_focus": semantic_focus,
            "semantic_ambiguity_refs": ["runtime/state/language/semantic_map_frame.json#ambiguity_queue"],
            "prediction_error_refs": [
                "runtime/state/prediction/prediction_error_field.json#error_events"
            ]
            if prediction_error_field
            else [],
            "signal_media_refs": [
                "runtime/state/signal/signal_media_runtime.json#modulation_vector"
            ]
            if signal_media_runtime
            else [],
        },
        "source_doc_refs": source_doc_refs,
    }
