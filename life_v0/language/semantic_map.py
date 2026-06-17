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

    utterance_signals = (language_percept.get("utterance_signal_profile") or {})
    semantic_focus = _derive_semantic_focus(language_percept, utterance_signals)

    relationship_topic_refs = list(language_state.get("shared_language_refs", []))
    commitment_trace_refs = list(commitment_repair_index.get("commitment_refs", []))
    repair_trace_refs = list(commitment_repair_index.get("repair_language_refs", []))
    dream_topic_refs = list(language_percept.get("dream_signal_candidates", []))
    ambiguity_queue = list(language_percept.get("ambiguity_flags", []))
    grounding_repair_candidates = _grounding_repair_candidates(
        language_percept=language_percept,
        ambiguity_queue=ambiguity_queue,
    )
    implicature_queue = _initial_implicature_queue(
        language_percept=language_percept,
        utterance_signals=utterance_signals,
    )
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
        "grounding_repair_candidates": grounding_repair_candidates,
        "implicature_queue": implicature_queue,
        "memory_recall_refs": [],
        "memory_reconstruction_focus": None,
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


def project_semantic_map_from_live_evidence(
    *,
    semantic_map: dict[str, Any],
    language_percept: dict[str, Any],
    relationship_timeline: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    context_accumulation: dict[str, Any] | None = None,
    relation_scope_index: dict[str, Any] | None = None,
    shared_term_registry: dict[str, Any] | None = None,
    relationship_stage: str | None = None,
    repair_closeout_state: dict[str, Any] | None = None,
    generated_at: str,
) -> dict[str, Any]:
    from .pragmatic_inference import enrich_semantic_map_with_pragmatic_inference

    return enrich_semantic_map_with_pragmatic_inference(
        semantic_map=semantic_map,
        language_percept=language_percept,
        relationship_timeline=relationship_timeline,
        commitment_truth_state=commitment_truth_state,
        context_accumulation=context_accumulation,
        relation_scope_index=relation_scope_index,
        shared_term_registry=shared_term_registry,
        relationship_stage=relationship_stage,
        repair_closeout_state=repair_closeout_state,
        generated_at=generated_at,
    )


def _derive_semantic_focus(
    language_percept: dict[str, Any],
    utterance_signals: dict[str, Any],
) -> str:
    if utterance_signals.get("relation_recalibration") or language_percept.get(
        "cross_scope_risk_terms"
    ):
        return "relation_scope_recalibration"
    if utterance_signals.get("boundary_declaration"):
        return "boundary_declaration"
    if utterance_signals.get("clarification_request"):
        return "clarification_request"
    if (
        utterance_signals.get("repair_request") or utterance_signals.get("apology")
    ) and language_percept.get("repair_trigger_candidates") and language_percept.get(
        "commitment_trigger_candidates"
    ):
        return "repair_commitment_shared_language"
    if (
        utterance_signals.get("repair_request") or utterance_signals.get("apology")
    ) and language_percept.get("repair_trigger_candidates"):
        return "repair_relational_trace"
    if language_percept.get("commitment_trigger_candidates"):
        return "commitment_trace_review"
    return "relational_checkin"


def _grounding_repair_candidates(
    *,
    language_percept: dict[str, Any],
    ambiguity_queue: list[str],
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for term in language_percept.get("cross_scope_risk_terms", []):
        candidates.append(
            {
                "candidate_id": f"grounding-scope-{term}",
                "kind": "relation_scope_repair",
                "source_term": term,
            }
        )
    for flag in ambiguity_queue:
        candidates.append(
            {
                "candidate_id": f"grounding-ambiguity-{flag}",
                "kind": "shared_grounding_repair",
                "source_flag": flag,
            }
        )
    return candidates[:12]


def _initial_implicature_queue(
    *,
    language_percept: dict[str, Any],
    utterance_signals: dict[str, Any],
) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    if utterance_signals.get("relation_recalibration"):
        queue.append(
            {
                "implicature_id": "implicature-relation-recalibration",
                "kind": "relation_role_correction",
            }
        )
    if utterance_signals.get("boundary_declaration"):
        queue.append(
            {
                "implicature_id": "implicature-boundary",
                "kind": "boundary_maintenance",
            }
        )
    if utterance_signals.get("clarification_request"):
        queue.append(
            {
                "implicature_id": "implicature-clarification",
                "kind": "grounding_request",
            }
        )
    for hit in language_percept.get("shared_term_hits", [])[:4]:
        queue.append(
            {
                "implicature_id": f"implicature-shared-hit-{hit}",
                "kind": "shared_term_activation",
                "surface": hit,
            }
        )
    return queue[:12]
