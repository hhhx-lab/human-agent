from __future__ import annotations

from typing import Any

LANGUAGE_PLASTICITY_BOUNDARY = "structured_language_plasticity_not_spoken_response"


def build_language_plasticity_update(
    *,
    run_id: str,
    generated_at: str,
    shared_term_registry: dict[str, Any],
    expression_plan: dict[str, Any] | None = None,
    dialogue_turn_count: int = 0,
) -> dict[str, Any]:
    shared_term_registry = shared_term_registry or {}
    expression_plan = expression_plan or {}
    promoted_terms = [
        term
        for term in shared_term_registry.get("shared_terms", [])
        if isinstance(term, dict) and term.get("promotion_status") == "promoted"
    ]
    tempo_mode = expression_plan.get("expression_tempo_mode")
    return {
        "schema_version": "language_plasticity_update_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "dialogue_turn_count": dialogue_turn_count,
        "promoted_shared_term_count": len(promoted_terms),
        "shared_term_promotion_evidence": [
            {
                "surface": term.get("surface"),
                "meaning_ref": term.get("meaning_ref"),
                "promotion_status": term.get("promotion_status"),
            }
            for term in promoted_terms[:12]
        ],
        "expression_tempo_mode": tempo_mode,
        "language_rhythm_trace_ref": "runtime/state/language/language_rhythm_trace.json",
        "language_plasticity_boundary": LANGUAGE_PLASTICITY_BOUNDARY,
    }


def build_language_rhythm_trace(
    *,
    run_id: str,
    generated_at: str,
    expression_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    expression_plan = expression_plan or {}
    return {
        "schema_version": "language_rhythm_trace_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "tempo_history": [
            {
                "expression_tempo_mode": expression_plan.get("expression_tempo_mode"),
                "release_caution_level": expression_plan.get("release_caution_level"),
                "delay_or_release_decision": expression_plan.get(
                    "delay_or_release_decision"
                ),
            }
        ],
        "language_rhythm_boundary": LANGUAGE_PLASTICITY_BOUNDARY,
    }