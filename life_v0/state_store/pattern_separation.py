from __future__ import annotations

import hashlib
from typing import Any


PATTERN_SEPARATION_REF = "runtime/state/memory/pattern_separation_index.json"

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/29_memory_validator_rules.md",
    "docs/54_scope_aware_retrieval_policy.md",
    "docs/v0/entry/v0_memory_module_rebuild_plan.md",
    "docs/v0/entry/v0_memory_recall_to_expression_contract.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_pattern_separation_index(
    *,
    run_id: str,
    generated_at: str,
    engram_cluster: dict[str, Any] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
) -> dict[str, Any]:
    clusters = [
        cluster
        for cluster in (engram_cluster or {}).get("clusters", [])
        if isinstance(cluster, dict)
    ]
    traces = [
        trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict)
    ]
    relation_subject_scopes = [
        scope
        for scope in (relationship_memory or {}).get("relation_subject_scopes", [])
        if isinstance(scope, dict)
    ]
    routes = [
        _route(
            run_id=run_id,
            route_kind="relationship_subject_scope",
            positive_refs=_dedupe(
                _cluster_refs(clusters, "relationship_subject")
                + _string_list((relationship_memory or {}).get("shared_memory_refs"))
                + ["runtime/state/memory/relationship_memory.json#relation_person_profile"]
            ),
            separation_keys=["relation_subject_id", "shared_language", "trust_repair_history"],
            guard="relationship_scope_prevents_cross_person_memory_bleed",
        ),
        _route(
            run_id=run_id,
            route_kind="dream_fact_boundary",
            positive_refs=_dedupe(
                _cluster_refs(clusters, "dream_residue")
                + _string_list((memory_retrieval_frame or {}).get("dream_residue_hits"))
                + ["runtime/state/dream/dream_fact_gate_decision.json"]
            ),
            separation_keys=["dream_source", "wake_observation", "fact_gate_status"],
            guard="dream_residue_never_promotes_to_fact_without_gate",
        ),
        _route(
            run_id=run_id,
            route_kind="responsibility_repair_scope",
            positive_refs=_dedupe(
                _cluster_refs(clusters, "responsibility_regret_repair")
                + _string_list((memory_retrieval_frame or {}).get("responsibility_hits"))
                + ["runtime/state/responsibility/responsibility_ledger.json"]
            ),
            separation_keys=["commitment_ref", "repair_obligation_ref", "action_outcome_ref"],
            guard="responsibility_trace_keeps_action_and_relation_scope",
        ),
        _route(
            run_id=run_id,
            route_kind="similar_episode_temporal_context",
            positive_refs=_dedupe(
                [
                    f"runtime/state/memory/memory_trace_store.json#trace:{trace.get('trace_id')}"
                    for trace in traces
                    if trace.get("trace_id")
                ]
                + _string_list((memory_retrieval_frame or {}).get("activated_engram_refs"))
            ),
            separation_keys=["event_boundary", "time_window", "source_evidence_refs"],
            guard="similar_events_require_event_boundary_before_completion",
        ),
    ]
    for scope in relation_subject_scopes:
        subject_id = str(scope.get("relation_subject_id") or "")
        relationship_scope = str(scope.get("relationship_scope") or "")
        if not subject_id:
            continue
        routes.append(
            _route(
                run_id=run_id,
                route_kind="multi_relation_subject_scope",
                positive_refs=_dedupe(
                    _trace_refs_for_scope(traces, relationship_scope=relationship_scope)
                    + _string_list([scope.get("subject_ref")])
                ),
                separation_keys=[
                    "relation_subject_id",
                    "relationship_scope",
                    "preference_hypothesis",
                ],
                guard="multi_relation_subject_scope_prevents_cross_person_bleed",
            )
        )
    routes = [route for route in routes if route["positive_refs"]]
    return {
        "schema_version": "pattern_separation_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "index_ref": PATTERN_SEPARATION_REF,
        "separation_policy": "dentate_gyrus_like_relation_event_dream_source_decorrelation",
        "separation_dimensions": [
            "relationship_subject_scope",
            "event_boundary",
            "source_evidence_scope",
            "dream_fact_boundary",
            "responsibility_action_scope",
            "body_affect_state_scope",
        ],
        "separation_guards": [
            "relationship_scope_prevents_cross_person_memory_bleed",
            "multi_relation_subject_scope_prevents_cross_person_bleed",
            "dream_residue_never_promotes_to_fact_without_gate",
            "similar_events_require_event_boundary_before_completion",
            "responsibility_trace_keeps_action_and_relation_scope",
        ],
        "multi_relation_subject_scope_count": len(relation_subject_scopes),
        "separation_routes": routes,
        "blocked_merge_refs": _dedupe(
            _string_list((state_merge_guard or {}).get("quarantine_routes"))
            + _string_list((memory_retrieval_frame or {}).get("blocked_or_quarantined_refs"))
        ),
        "downstream_consumer_refs": [
            "runtime/state/memory/pattern_completion_frame.json#source_separation_index_ref",
            "runtime/state/memory/memory_retrieval_frame.json#pattern_separation_profile",
            "runtime/state/life_state.json#memory_index.pattern_separation_refs",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _trace_refs_for_scope(
    traces: list[dict[str, Any]],
    *,
    relationship_scope: str,
) -> list[str]:
    refs: list[str] = []
    for trace in traces:
        if not isinstance(trace, dict):
            continue
        if str(trace.get("relationship_scope") or "") != relationship_scope:
            continue
        trace_id = trace.get("trace_id")
        if trace_id:
            refs.append(
                f"runtime/state/memory/memory_trace_store.json#trace:{trace_id}"
            )
    return _dedupe(refs)


def _route(
    *,
    run_id: str,
    route_kind: str,
    positive_refs: list[str],
    separation_keys: list[str],
    guard: str,
) -> dict[str, Any]:
    route_id = f"pattern-separation-{_short_hash('|'.join([run_id, route_kind] + positive_refs[:4]))}"
    return {
        "route_id": route_id,
        "route_kind": route_kind,
        "route_ref": f"{PATTERN_SEPARATION_REF}#route:{route_id}",
        "positive_refs": _dedupe(positive_refs),
        "separation_keys": _dedupe(separation_keys),
        "guard": guard,
    }


def _cluster_refs(clusters: list[dict[str, Any]], cluster_kind: str) -> list[str]:
    return [
        str(cluster.get("cluster_ref"))
        for cluster in clusters
        if cluster.get("cluster_kind") == cluster_kind and cluster.get("cluster_ref")
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
