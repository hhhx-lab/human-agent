from __future__ import annotations

import json
import re
from typing import Any

SHARED_TERM_REGISTRY_REF = "runtime/state/language/shared_term_registry.json"
SHARED_TERM_PROMOTION_BOUNDARY = (
    "structured_shared_term_promotion_not_spoken_language"
)
MIN_DIALOGUE_TURNS_FOR_PROMOTION = 2
MIN_EVIDENCE_CHANNELS_FOR_PROMOTION = 2


def build_shared_term_registry(
    *,
    run_id: str,
    generated_at: str,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "shared_term_registry_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "shared_terms": [
            {
                "term_id": "shared-term-v0-0001",
                "surface": "共同语言",
                "relation_scope": "friend",
                "meaning_ref": "runtime/state/language/language_relationship_state.json#shared-language-v0-0001",
                "promotion_gate_status": "seed",
                "promotion_evidence_sources": ["seed_registry"],
            }
        ],
        "shared_term_promotion_boundary": SHARED_TERM_PROMOTION_BOUNDARY,
        "source_doc_refs": source_doc_refs,
    }


def project_shared_term_registry_from_live_evidence(
    *,
    shared_term_registry: dict[str, Any],
    generated_at: str,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    language_percept: dict[str, Any] | None = None,
    semantic_map: dict[str, Any] | None = None,
    context_accumulation: dict[str, Any] | None = None,
    relation_scope_index: dict[str, Any] | None = None,
    dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
) -> dict[str, Any]:
    if not shared_term_registry:
        return {}
    if shared_term_registry.get("schema_version") != "shared_term_registry_v0":
        return shared_term_registry

    relationship_graph = relationship_graph or {}
    relationship_timeline = relationship_timeline or {}
    language_percept = language_percept or {}
    semantic_map = semantic_map or {}
    context_accumulation = context_accumulation or {}
    relation_scope_index = relation_scope_index or {}
    dialogue_turn_refs = list(dialogue_turn_refs or [])
    live_language_turn_refs = list(live_language_turn_refs or [])

    updated = json.loads(json.dumps(shared_term_registry))
    relation_scope = _resolve_relation_scope(
        relationship_graph=relationship_graph,
        relation_scope_index=relation_scope_index,
        language_percept=language_percept,
    )
    evidence_by_surface = _collect_surface_evidence(
        relationship_timeline=relationship_timeline,
        language_percept=language_percept,
        semantic_map=semantic_map,
        context_accumulation=context_accumulation,
    )
    dialogue_turn_count = len(_dedupe(dialogue_turn_refs + live_language_turn_refs))

    existing_terms = [
        term
        for term in updated.get("shared_terms", [])
        if isinstance(term, dict) and term.get("surface")
    ]
    existing_by_surface = {
        str(term.get("surface")): term for term in existing_terms
    }
    next_term_index = _next_term_index(existing_terms)

    refreshed_terms: list[dict[str, Any]] = []
    promotion_candidates: list[dict[str, Any]] = []

    for term in existing_terms:
        surface = str(term.get("surface"))
        evidence_sources = list(
            evidence_by_surface.get(surface, term.get("promotion_evidence_sources", []))
        )
        gate_status = _evaluate_promotion_gate(
            surface=surface,
            evidence_sources=evidence_sources,
            dialogue_turn_count=dialogue_turn_count,
            relation_scope=relation_scope,
            existing_status=str(term.get("promotion_gate_status") or "seed"),
        )
        refreshed = dict(term)
        refreshed["relation_scope"] = relation_scope or term.get("relation_scope")
        refreshed["promotion_evidence_sources"] = _dedupe(evidence_sources)
        refreshed["promotion_gate_status"] = gate_status
        refreshed_terms.append(refreshed)

    for surface, evidence_sources in sorted(evidence_by_surface.items()):
        if surface in existing_by_surface:
            continue
        gate_status = _evaluate_promotion_gate(
            surface=surface,
            evidence_sources=evidence_sources,
            dialogue_turn_count=dialogue_turn_count,
            relation_scope=relation_scope,
            existing_status="candidate",
        )
        candidate_entry = {
            "surface": surface,
            "promotion_gate_status": gate_status,
            "promotion_evidence_sources": _dedupe(evidence_sources),
            "relation_scope": relation_scope,
        }
        if gate_status == "promoted":
            term_id = f"shared-term-v0-{next_term_index:04d}"
            next_term_index += 1
            refreshed_terms.append(
                {
                    "term_id": term_id,
                    "surface": surface,
                    "relation_scope": relation_scope,
                    "meaning_ref": (
                        "runtime/state/language/language_relationship_state.json"
                        f"#shared-language-v0-{term_id.rsplit('-', 1)[-1]}"
                    ),
                    "promotion_gate_status": gate_status,
                    "promotion_evidence_sources": _dedupe(evidence_sources),
                    "promotion_source_refs": _promotion_source_refs(
                        dialogue_turn_refs=dialogue_turn_refs,
                        live_language_turn_refs=live_language_turn_refs,
                        context_accumulation=context_accumulation,
                    ),
                }
            )
        else:
            promotion_candidates.append(candidate_entry)

    updated["generated_at"] = generated_at
    updated["shared_terms"] = refreshed_terms
    updated["shared_term_promotion_boundary"] = SHARED_TERM_PROMOTION_BOUNDARY
    updated["live_promotion_refreshed"] = True
    updated["shared_term_promotion_candidate_surfaces"] = [
        entry["surface"] for entry in promotion_candidates
    ]
    updated["shared_term_promotion_candidate_count"] = len(promotion_candidates)
    updated["shared_term_promotion_dialogue_turn_count"] = dialogue_turn_count
    updated["shared_term_promotion_relation_scope"] = relation_scope
    return updated


def shared_term_promotion_inspection_snapshot(
    *,
    shared_term_registry: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    shared_term_registry = shared_term_registry or {}
    terminal_life_loop_state = terminal_life_loop_state or {}
    shared_terms = [
        term
        for term in shared_term_registry.get("shared_terms", [])
        if isinstance(term, dict)
    ]
    promoted_terms = [
        term
        for term in shared_terms
        if term.get("promotion_gate_status") in {"promoted", "seed"}
    ]
    live_promoted_terms = [
        term
        for term in shared_terms
        if term.get("promotion_gate_status") == "promoted"
    ]
    return {
        "shared_term_live_promotion_present": bool(
            shared_term_registry.get("live_promotion_refreshed")
            or terminal_life_loop_state.get("live_shared_term_promotion_refreshed")
        ),
        "shared_term_promotion_count": len(promoted_terms),
        "shared_term_live_promoted_count": len(live_promoted_terms),
        "shared_term_promotion_candidate_count": int(
            shared_term_registry.get("shared_term_promotion_candidate_count")
            or len(shared_term_registry.get("shared_term_promotion_candidate_surfaces", []))
        ),
        "shared_term_promotion_relation_scope": (
            shared_term_registry.get("shared_term_promotion_relation_scope")
            or terminal_life_loop_state.get("live_shared_term_promotion_relation_scope")
        ),
        "shared_term_promotion_dialogue_turn_count": int(
            shared_term_registry.get("shared_term_promotion_dialogue_turn_count")
            or terminal_life_loop_state.get(
                "live_shared_term_promotion_dialogue_turn_count",
                0,
            )
            or 0
        ),
        "shared_term_promotion_boundary": (
            shared_term_registry.get("shared_term_promotion_boundary")
            or SHARED_TERM_PROMOTION_BOUNDARY
        ),
    }


def _resolve_relation_scope(
    *,
    relationship_graph: dict[str, Any],
    relation_scope_index: dict[str, Any],
    language_percept: dict[str, Any],
) -> str | None:
    scopes = relation_scope_index.get("relation_scopes", [])
    if scopes and isinstance(scopes[0], dict):
        role = scopes[0].get("relation_role")
        if role:
            return str(role)

    subjects = relationship_graph.get("relationship_subjects", [])
    if subjects and isinstance(subjects[0], dict):
        role = subjects[0].get("relation_role")
        if role:
            return str(role)

    scope_ref = str(language_percept.get("relation_scope_ref", ""))
    if scope_ref:
        return scope_ref.rsplit("#", 1)[-1]
    return None


def _collect_surface_evidence(
    *,
    relationship_timeline: dict[str, Any],
    language_percept: dict[str, Any],
    semantic_map: dict[str, Any],
    context_accumulation: dict[str, Any],
) -> dict[str, list[str]]:
    evidence: dict[str, list[str]] = {}

    def add(surface: Any, source: str) -> None:
        normalized = _normalize_surface(surface)
        if not normalized:
            return
        evidence.setdefault(normalized, [])
        if source not in evidence[normalized]:
            evidence[normalized].append(source)

    for term in relationship_timeline.get("common_ground_states", []):
        if not isinstance(term, dict):
            continue
        for surface in term.get("shared_terms", []):
            add(surface, "relationship_timeline_common_ground")

    for surface in context_accumulation.get("shared_term_surfaces", []):
        add(surface, "context_accumulation_window")

    for binding in semantic_map.get("shared_meaning_bindings", []):
        if not isinstance(binding, dict):
            continue
        add(binding.get("surface"), "semantic_map_binding")

    for surface in language_percept.get("shared_term_hits", []):
        add(surface, "language_percept_hit")

    return evidence


def _evaluate_promotion_gate(
    *,
    surface: str,
    evidence_sources: list[str],
    dialogue_turn_count: int,
    relation_scope: str | None,
    existing_status: str,
) -> str:
    if existing_status == "seed":
        if evidence_sources:
            return "seed_reinforced"
        return "seed"
    if not relation_scope:
        return "blocked_scope_missing"
    if dialogue_turn_count < MIN_DIALOGUE_TURNS_FOR_PROMOTION:
        return "blocked_premature_single_turn"
    unique_sources = _dedupe(evidence_sources)
    if len(unique_sources) < MIN_EVIDENCE_CHANNELS_FOR_PROMOTION:
        return "candidate_insufficient_evidence"
    if "language_percept_hit" in unique_sources and len(unique_sources) < 2:
        return "blocked_premature_single_turn"
    return "promoted"


def _promotion_source_refs(
    *,
    dialogue_turn_refs: list[str],
    live_language_turn_refs: list[str],
    context_accumulation: dict[str, Any],
) -> list[str]:
    refs = _dedupe(dialogue_turn_refs + live_language_turn_refs)
    context_ref = context_accumulation.get("context_accumulation_ref")
    if context_ref:
        refs.append(str(context_ref))
    return refs[:12]


def _next_term_index(existing_terms: list[dict[str, Any]]) -> int:
    max_index = 0
    for term in existing_terms:
        term_id = str(term.get("term_id", ""))
        match = re.search(r"(\d+)$", term_id)
        if match:
            max_index = max(max_index, int(match.group(1)))
    return max_index + 1


def _normalize_surface(surface: Any) -> str | None:
    if surface is None:
        return None
    normalized = str(surface).strip()
    return normalized or None


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result