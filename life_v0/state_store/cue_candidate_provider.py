from __future__ import annotations

from typing import Any, Protocol


class CueCandidateProvider(Protocol):
    provider_name: str

    def collect_candidates(
        self,
        *,
        cue_terms: list[str],
        memory_trace_store: dict[str, Any] | None,
        relationship_memory: dict[str, Any] | None,
        scope_boundary: str | None = None,
    ) -> dict[str, Any]: ...


def noop_cue_candidate_provider(
    *,
    cue_terms: list[str] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    scope_boundary: str | None = None,
    validator_boundary: str | None = None,
) -> dict[str, Any]:
    return {
        "provider_name": "noop",
        "candidate_trace_refs": [],
        "candidate_cue_terms": [],
        "scores": [],
        "source_boundary": None,
        "scope_boundary": scope_boundary or "relation_scoped_live_episode",
        "validator_boundary": validator_boundary or "lifecycle_and_claim_partition_required",
        "provider_status": "noop_no_candidates",
    }


def local_full_text_cue_candidate_provider(
    *,
    cue_terms: list[str] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    scope_boundary: str | None = None,
    validator_boundary: str | None = None,
) -> dict[str, Any]:
    terms = _string_list(cue_terms)
    if not terms or not memory_trace_store:
        return noop_cue_candidate_provider(
            cue_terms=terms,
            memory_trace_store=memory_trace_store,
            relationship_memory=relationship_memory,
            scope_boundary=scope_boundary,
            validator_boundary=validator_boundary,
        )
    candidate_trace_refs: list[str] = []
    candidate_cue_terms: list[str] = []
    scores: list[float] = []
    for trace in memory_trace_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        if trace.get("lifecycle_state") in {"deprecated", "deleted", "quarantined", "sandboxed"}:
            continue
        haystack = " ".join(
            [
                str(trace.get("content_summary") or ""),
                str(trace.get("utterance_digest") or ""),
                str(trace.get("semantic_focus") or ""),
            ]
        ).lower()
        matched_terms = [term for term in terms if term.lower() in haystack]
        if not matched_terms:
            continue
        trace_id = str(trace.get("trace_id") or "")
        if not trace_id:
            continue
        candidate_trace_refs.append(
            f"runtime/state/memory/memory_trace_store.json#{trace_id}"
        )
        candidate_cue_terms.extend(matched_terms)
        scores.append(min(0.95, 0.45 + (0.1 * len(matched_terms))))
    return {
        "provider_name": "local_full_text",
        "candidate_trace_refs": _dedupe(candidate_trace_refs)[:12],
        "candidate_cue_terms": _dedupe(candidate_cue_terms)[:12],
        "scores": scores[:12],
        "source_boundary": "live_trace",
        "scope_boundary": scope_boundary or "relation_scoped_live_episode",
        "validator_boundary": validator_boundary or "lifecycle_and_claim_partition_required",
        "provider_status": "local_full_text_candidates_collected",
    }


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, tuple):
        return [str(item) for item in value if item]
    if isinstance(value, set):
        return [str(item) for item in sorted(value) if item]
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