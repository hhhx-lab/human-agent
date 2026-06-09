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
) -> dict[str, Any]:
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
        "prediction_hooks": {
            "semantic_prediction_focus": semantic_focus,
            "semantic_ambiguity_refs": ["runtime/state/language/semantic_map_frame.json#ambiguity_queue"],
        },
        "source_doc_refs": source_doc_refs,
    }
