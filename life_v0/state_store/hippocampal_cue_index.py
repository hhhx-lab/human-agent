from __future__ import annotations

import hashlib
import re
from typing import Any

MEMORY_TRACE_STORE_REF = "runtime/state/memory/memory_trace_store.json"
HIPPOCAMPAL_CUE_INDEX_REF = "runtime/state/memory/hippocampal_cue_index.json"

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "docs/17_memory_trace_object_model.md",
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_hippocampal_cue_index(
    *,
    run_id: str,
    generated_at: str,
    memory_trace_store: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    bindings: list[dict[str, Any]] = []
    for trace in (memory_trace_store or {}).get("traces", []):
        if not isinstance(trace, dict):
            continue
        if trace.get("lifecycle_state") in {"deprecated", "quarantined", "deleted"}:
            continue
        trace_id = str(trace.get("trace_id") or "")
        if not trace_id:
            continue
        trace_ref = f"{MEMORY_TRACE_STORE_REF}#{trace_id}"
        cue_terms = _dedupe(
            _string_list(trace.get("retrieval_cues"))
            + _string_list(trace.get("semantic_focus"))
            + _string_list(trace.get("utterance_digest"))
            + _tokenize(trace.get("content_summary"))
        )
        for cue_term in cue_terms:
            if not cue_term or len(cue_term) < 2:
                continue
            bindings.append(
                {
                    "binding_id": _binding_id(trace_id, cue_term),
                    "cue_term": cue_term,
                    "trace_id": trace_id,
                    "trace_ref": trace_ref,
                    "relationship_scope": trace.get("relationship_scope"),
                    "relation_subject_id": trace.get("relation_subject_id"),
                    "memory_kind": trace.get("memory_kind"),
                    "live_trace_origin": trace.get("live_trace_origin"),
                    "base_activation": _base_activation(trace),
                    "index_route": "hippocampal_cue_to_trace_binding",
                }
            )
    return {
        "schema_version": "hippocampal_cue_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "index_ref": HIPPOCAMPAL_CUE_INDEX_REF,
        "binding_count": len(bindings),
        "cue_bindings": bindings,
        "active_relation_subject_id": (relationship_memory or {}).get(
            "active_relation_subject_id"
        ),
        "relationship_scope": (relationship_memory or {}).get("relationship_scope"),
        "index_policy": (
            "cue_terms_activate_trace_bindings_for_reconstructive_recall_not_literal_chunks"
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def activate_hippocampal_cues(
    *,
    cue_terms: list[str],
    hippocampal_cue_index: dict[str, Any] | None,
    relationship_scope: str | None = None,
    relation_subject_id: str | None = None,
    blocked_trace_ids: list[str] | None = None,
) -> list[dict[str, Any]]:
    blocked = set(blocked_trace_ids or [])
    activations: dict[str, dict[str, Any]] = {}
    normalized_cues = [_normalize_cue(term) for term in cue_terms if term]
    for binding in (hippocampal_cue_index or {}).get("cue_bindings", []):
        if not isinstance(binding, dict):
            continue
        trace_id = str(binding.get("trace_id") or "")
        if not trace_id or trace_id in blocked:
            continue
        if relationship_scope and binding.get("relationship_scope"):
            if str(binding.get("relationship_scope")) != relationship_scope:
                continue
        if relation_subject_id and binding.get("relation_subject_id"):
            if str(binding.get("relation_subject_id")) != relation_subject_id:
                continue
        cue_term = _normalize_cue(str(binding.get("cue_term") or ""))
        if not cue_term:
            continue
        score = 0.0
        matched_cues: list[str] = []
        for query in normalized_cues:
            if not query:
                continue
            if query == cue_term:
                score += 3.0
                matched_cues.append(query)
            elif query in cue_term or cue_term in query:
                score += 2.0
                matched_cues.append(query)
            elif _token_overlap(query, cue_term):
                score += 1.0
                matched_cues.append(query)
        if score <= 0:
            continue
        score += float(binding.get("base_activation") or 0)
        existing = activations.get(trace_id)
        payload = {
            "trace_id": trace_id,
            "trace_ref": binding.get("trace_ref"),
            "activation_score": round(score, 3),
            "matched_cue_terms": _dedupe(matched_cues),
            "relationship_scope": binding.get("relationship_scope"),
            "relation_subject_id": binding.get("relation_subject_id"),
            "activation_route": "hippocampal_pattern_completion",
        }
        if existing and existing["activation_score"] >= payload["activation_score"]:
            existing["matched_cue_terms"] = _dedupe(
                _string_list(existing.get("matched_cue_terms"))
                + payload["matched_cue_terms"]
            )
            continue
        activations[trace_id] = payload
    ordered = sorted(
        activations.values(),
        key=lambda item: (-float(item.get("activation_score") or 0), str(item.get("trace_id"))),
    )
    return ordered[:12]


def build_reconstruction_fragments(
    *,
    activations: list[dict[str, Any]],
    memory_trace_store: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    trace_by_id = {
        str(trace.get("trace_id")): trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict) and trace.get("trace_id")
    }
    fragments: list[dict[str, Any]] = []
    for activation in activations:
        trace = trace_by_id.get(str(activation.get("trace_id") or ""))
        if not trace:
            continue
        trace_id = str(trace.get("trace_id"))
        fragments.append(
            {
                "fragment_id": f"reconstruction-fragment-{_short_hash(trace_id)}",
                "fragment_kind": "live_episodic_reconstruction",
                "trace_id": trace_id,
                "trace_ref": activation.get("trace_ref")
                or f"{MEMORY_TRACE_STORE_REF}#{trace_id}",
                "activation_score": activation.get("activation_score"),
                "matched_cue_terms": _string_list(activation.get("matched_cue_terms")),
                "semantic_focus": trace.get("semantic_focus"),
                "reconstruction_focus": trace.get("reconstruction_focus"),
                "episode_digest": _episode_digest(trace.get("content_summary")),
                "source_evidence_refs": _string_list(trace.get("source_evidence_refs"))[:8],
                "relationship_scope": trace.get("relationship_scope"),
                "relation_subject_id": trace.get("relation_subject_id"),
                "confidence_label": trace.get("confidence_label"),
                "material_boundary": (
                    "reconstruction_fragment_not_spoken_answer_or_fixed_recall_template"
                ),
            }
        )
    return fragments


def _base_activation(trace: dict[str, Any]) -> float:
    score = 0.2
    if trace.get("live_trace_origin") == "live_dialogue_turn":
        score += 0.25
    score += float(trace.get("accessibility_score") or 0.55) * 0.2
    score += float(trace.get("replay_salience") or 0.5) * 0.15
    if trace.get("lifecycle_state") == "protected":
        score += 0.1
    return round(min(1.0, score), 3)


def _episode_digest(content_summary: Any) -> str:
    text = str(content_summary or "").strip()
    if not text:
        return ""
    return text[:240]


def _binding_id(trace_id: str, cue_term: str) -> str:
    return f"hippocampal-binding-{_short_hash('|'.join([trace_id, cue_term]))}"


def _normalize_cue(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _tokenize(value: Any) -> list[str]:
    text = str(value or "").lower()
    return [token for token in re.findall(r"[a-z0-9_\u4e00-\u9fff]{2,}", text) if token]


def _token_overlap(left: str, right: str) -> bool:
    left_tokens = set(_tokenize(left))
    right_tokens = set(_tokenize(right))
    return bool(left_tokens & right_tokens)


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [str(value)] if value else []


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result