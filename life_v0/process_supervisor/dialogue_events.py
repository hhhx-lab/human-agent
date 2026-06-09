from __future__ import annotations

from typing import Any


def build_external_turn_event(
    *,
    turn_id: str,
    generated_at: str,
    utterance: str,
    shared_term_registry: dict[str, Any],
    commitment_index: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "dialogue_turn_event_v0",
        "turn_id": turn_id,
        "generated_at": generated_at,
        "event_role": "external_relation_turn",
        "relation_role": "friend",
        "utterance": utterance,
        "shared_term_refs": shared_term_refs(shared_term_registry),
        "commitment_refs": list(commitment_index.get("commitment_refs", [])),
        "expression_monitor_ref": "runtime/state/language/expression_monitor_state.json",
        "narrative_trace_ref": "runtime/state/language/self_narrative_language_trace.json",
    }


def build_life_turn_event(
    *,
    turn_id: str,
    generated_at: str,
    utterance: str,
    shared_term_registry: dict[str, Any],
    commitment_index: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "dialogue_turn_event_v0",
        "turn_id": turn_id,
        "generated_at": generated_at,
        "event_role": "digital_life_turn",
        "relation_role": "friend",
        "utterance": utterance,
        "shared_term_refs": shared_term_refs(shared_term_registry),
        "commitment_refs": list(commitment_index.get("commitment_refs", [])),
        "expression_monitor_ref": "runtime/state/language/expression_monitor_state.json",
        "narrative_trace_ref": "runtime/state/language/self_narrative_language_trace.json",
    }


def shared_term_refs(shared_term_registry: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for term in shared_term_registry.get("shared_terms", []):
        if isinstance(term, dict) and term.get("term_id"):
            refs.append(f"runtime/state/language/shared_term_registry.json#{term['term_id']}")
    return refs
