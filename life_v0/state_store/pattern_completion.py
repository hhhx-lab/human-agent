from __future__ import annotations

import hashlib
from typing import Any


PATTERN_COMPLETION_REF = "runtime/state/memory/pattern_completion_frame.json"

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/29_memory_validator_rules.md",
    "docs/v0/entry/v0_memory_module_rebuild_plan.md",
    "docs/v0/entry/v0_memory_recall_to_expression_contract.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_pattern_completion_frame(
    *,
    run_id: str,
    generated_at: str,
    engram_cluster: dict[str, Any] | None = None,
    pattern_separation_index: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
) -> dict[str, Any]:
    clusters = [
        cluster
        for cluster in (engram_cluster or {}).get("clusters", [])
        if isinstance(cluster, dict)
    ]
    routes = [
        route
        for route in (pattern_separation_index or {}).get("separation_routes", [])
        if isinstance(route, dict)
    ]
    candidates = [
        _candidate(
            run_id=run_id,
            candidate_kind="relationship_episode_completion",
            cue_refs=_dedupe(
                _routes_by_kind(routes, "relationship_subject_scope")
                + _cluster_refs(clusters, "relationship_subject")
                + _string_list((memory_retrieval_frame or {}).get("relationship_memory_hits"))
            ),
            completed_refs=["runtime/state/memory/relationship_memory.json#shared_memory_refs"],
            confidence="source_scoped_seed_confidence",
            boundary="relationship_completion_keeps_relation_scope",
        ),
        _candidate(
            run_id=run_id,
            candidate_kind="responsibility_repair_completion",
            cue_refs=_dedupe(
                _routes_by_kind(routes, "responsibility_repair_scope")
                + _cluster_refs(clusters, "responsibility_regret_repair")
                + _string_list((memory_retrieval_frame or {}).get("responsibility_hits"))
            ),
            completed_refs=["runtime/state/responsibility/responsibility_ledger.json"],
            confidence="repair_source_refs_present",
            boundary="responsibility_completion_keeps_action_outcome_scope",
        ),
        _candidate(
            run_id=run_id,
            candidate_kind="autobiographical_self_continuity_completion",
            cue_refs=_dedupe(
                _cluster_refs(clusters, "self_autobiographical")
                + _string_list((memory_retrieval_frame or {}).get("autobiographical_hits"))
            ),
            completed_refs=["runtime/state/self/autobiographical_stack.json#anchor_refs"],
            confidence="self_anchor_refs_present",
            boundary="self_completion_keeps_old_self_anchor",
        ),
        _candidate(
            run_id=run_id,
            candidate_kind="dream_residue_completion",
            cue_refs=_dedupe(
                _routes_by_kind(routes, "dream_fact_boundary")
                + _cluster_refs(clusters, "dream_residue")
                + _string_list((memory_retrieval_frame or {}).get("dream_residue_hits"))
            ),
            completed_refs=["runtime/state/dream/wake_integration_frame.json"],
            confidence="dream_source_confidence_not_fact_confidence",
            boundary="dream_completion_keeps_dream_boundary",
        ),
    ]
    candidates = [candidate for candidate in candidates if candidate["cue_refs"]]
    return {
        "schema_version": "pattern_completion_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "frame_ref": PATTERN_COMPLETION_REF,
        "source_separation_index_ref": "runtime/state/memory/pattern_separation_index.json"
        if pattern_separation_index
        else None,
        "completion_policy": [
            "partial_cue_completion_preserves_source_confidence",
            "completion_is_reconstructive_not_literal_chunk_return",
            "completion_requires_pattern_separation_before_expression",
            "completed_material_enters_recall_to_expression_not_fixed_reply",
        ],
        "completion_candidates": candidates,
        "completion_boundaries": [
            "dream_completion_keeps_dream_boundary",
            "relationship_completion_keeps_relation_scope",
            "responsibility_completion_keeps_action_outcome_scope",
            "source_confidence_must_survive_language_expression",
        ],
        "source_trace_count": len(
            [
                trace
                for trace in (memory_trace_store or {}).get("traces", [])
                if isinstance(trace, dict)
            ]
        ),
        "downstream_consumer_refs": [
            "runtime/state/memory/memory_retrieval_frame.json#recall_to_expression_profile",
            "runtime/state/language/model_expression_state.json#memory_retrieval",
            "runtime/state/life_state.json#memory_index.pattern_completion_refs",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _candidate(
    *,
    run_id: str,
    candidate_kind: str,
    cue_refs: list[str],
    completed_refs: list[str],
    confidence: str,
    boundary: str,
) -> dict[str, Any]:
    candidate_id = f"pattern-completion-{_short_hash('|'.join([run_id, candidate_kind] + cue_refs[:4]))}"
    return {
        "candidate_id": candidate_id,
        "candidate_kind": candidate_kind,
        "candidate_ref": f"{PATTERN_COMPLETION_REF}#candidate:{candidate_id}",
        "cue_refs": _dedupe(cue_refs),
        "completed_refs": _dedupe(completed_refs),
        "source_confidence": confidence,
        "boundary": boundary,
        "writeback_route": "memory_write_gate_then_state_merge_guard_after_expression_feedback",
    }


def _cluster_refs(clusters: list[dict[str, Any]], cluster_kind: str) -> list[str]:
    return [
        str(cluster.get("cluster_ref"))
        for cluster in clusters
        if cluster.get("cluster_kind") == cluster_kind and cluster.get("cluster_ref")
    ]


def _routes_by_kind(routes: list[dict[str, Any]], route_kind: str) -> list[str]:
    return [
        str(route.get("route_ref"))
        for route in routes
        if route.get("route_kind") == route_kind and route.get("route_ref")
    ]


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


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
