from __future__ import annotations

import hashlib
from typing import Any


ENGRAM_CLUSTER_REF = "runtime/state/memory/engram_cluster.json"

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/25_memory_trace_json_schema_examples.md",
    "docs/29_memory_validator_rules.md",
    "docs/v0/entry/v0_memory_module_rebuild_plan.md",
    "docs/v0/entry/v0_memory_recall_to_expression_contract.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_engram_like_trace_cluster(
    *,
    run_id: str,
    generated_at: str,
    memory_trace_store: dict[str, Any] | None = None,
    engram_index: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    memory_allocation_gate: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
) -> dict[str, Any]:
    traces = [
        trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict)
    ]
    trace_by_kind = _trace_by_kind(traces)
    clusters = [
        _cluster(
            run_id=run_id,
            generated_at=generated_at,
            cluster_kind="language_episode",
            primary_trace=trace_by_kind.get("episodic"),
            seed_refs=_dedupe(
                _string_list((engram_index or {}).get("live_language_turn_refs"))
                + _string_list((engram_index or {}).get("live_dialogue_turn_refs"))
                + ["runtime/state/memory/memory_retrieval_frame.json#cue_terms"]
            ),
            activation_cues=["language", "semantic_map", "live_turn", "current_phrase"],
            modulation_refs=[
                "runtime/state/language/language_percept_frame.json",
                "runtime/state/consciousness/workspace_frame.json",
            ],
            reportability="workspace_reportable_with_source_boundary",
        ),
        _cluster(
            run_id=run_id,
            generated_at=generated_at,
            cluster_kind="relationship_subject",
            primary_trace=trace_by_kind.get("relationship"),
            seed_refs=_dedupe(
                _string_list((relationship_memory or {}).get("shared_memory_refs"))
                + _string_list((relationship_memory or {}).get("timeline_refs"))
                + ["runtime/state/memory/relationship_memory.json#relation_person_profile"]
            ),
            activation_cues=["relationship", "shared_language", "relation_scope", "trust_repair"],
            modulation_refs=[
                "runtime/state/relationship/commitment_truth_state.json",
                "runtime/state/memory/state_merge_guard.json",
            ],
            reportability="relationship_scoped_reportable",
        ),
        _cluster(
            run_id=run_id,
            generated_at=generated_at,
            cluster_kind="self_autobiographical",
            primary_trace=trace_by_kind.get("autobiographical"),
            seed_refs=_dedupe(
                _string_list((autobiographical_stack or {}).get("anchor_refs"))
                + _string_list((autobiographical_stack or {}).get("turn_refs"))
                + _string_list((engram_index or {}).get("autobiographical_memory_refs"))
                + ["runtime/state/self/autobiographical_stack.json"]
            ),
            activation_cues=["autobiographical", "self_continuity", "old_self_anchor", "growth"],
            modulation_refs=[
                "runtime/state/self/self_model.json",
                "runtime/state/growth/offline_learning_cumulative_profile.json",
            ],
            reportability="self_memory_reportable_after_continuity_check",
        ),
        _cluster(
            run_id=run_id,
            generated_at=generated_at,
            cluster_kind="responsibility_regret_repair",
            primary_trace=trace_by_kind.get("responsibility"),
            seed_refs=_dedupe(
                _string_list((engram_index or {}).get("responsibility_memory_refs"))
                + _string_list((memory_retrieval_frame or {}).get("responsibility_hits"))
                + ["runtime/state/responsibility/responsibility_ledger.json"]
            ),
            activation_cues=["responsibility", "regret", "repair", "commitment"],
            modulation_refs=[
                "runtime/state/memory/memory_write_gate.json",
                "runtime/state/memory/state_merge_guard.json",
            ],
            reportability="responsibility_reportable_with_repair_context",
        ),
        _cluster(
            run_id=run_id,
            generated_at=generated_at,
            cluster_kind="dream_residue",
            primary_trace=None,
            seed_refs=_dedupe(
                _string_list((engram_index or {}).get("dream_memory_refs"))
                + _string_list((memory_retrieval_frame or {}).get("dream_residue_hits"))
                + ["runtime/state/dream/wake_integration_frame.json"]
            ),
            activation_cues=["dream", "wake_integration", "offline_replay", "dream_fact_boundary"],
            modulation_refs=[
                "runtime/state/dream/dream_fact_gate_decision.json",
                "runtime/state/memory/memory_write_gate.json#dream_sandbox_route",
            ],
            reportability="dream_residue_not_fact_reportable",
        ),
    ]
    clusters = [cluster for cluster in clusters if cluster["seed_refs"]]
    cluster_refs = [cluster["cluster_ref"] for cluster in clusters]
    silent_trace_refs = _dedupe(
        [
            f"{ENGRAM_CLUSTER_REF}#silent:{cluster['cluster_id']}"
            for cluster in clusters
            if cluster["cluster_kind"] in {"dream_residue", "self_autobiographical"}
        ]
        + [
            f"{ENGRAM_CLUSTER_REF}#silent:{trace.get('trace_id')}"
            for trace in traces
            if trace.get("lifecycle_state") in {"candidate", "protected", "silent"}
        ]
    )
    reactivated_trace_refs = _dedupe(
        [
            f"{ENGRAM_CLUSTER_REF}#reactivated:{cluster['cluster_id']}"
            for cluster in clusters
            if cluster["cluster_kind"] != "dream_residue"
        ]
        + _string_list((memory_retrieval_frame or {}).get("activated_engram_refs"))[:16]
    )
    return {
        "schema_version": "engram_like_trace_cluster_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "cluster_ref": ENGRAM_CLUSTER_REF,
        "cluster_count": len(clusters),
        "clusters": clusters,
        "cluster_refs": cluster_refs,
        "reactivation_modalities": [
            "language",
            "relationship",
            "body_affect",
            "dream",
            "responsibility",
        ],
        "silent_trace_refs": silent_trace_refs,
        "reactivated_trace_refs": reactivated_trace_refs,
        "trace_cluster_cue_routes": [
            {
                "route_ref": f"{ENGRAM_CLUSTER_REF}#route:{cluster['cluster_id']}",
                "cluster_ref": cluster["cluster_ref"],
                "activation_cues": cluster["activation_cues"],
                "modulation_refs": cluster["modulation_refs"],
                "reportability": cluster["reportability"],
            }
            for cluster in clusters
        ],
        "retrieval_expression_split_policy": [
            "trace_existence_retrieval_reportability_action_are_split",
            "silent_trace_can_exist_without_current_report",
            "reactivated_trace_requires_source_boundary_before_expression",
            "action_permission_requires_memory_write_gate_and_state_merge_guard",
        ],
        "lifecycle_state_model": [
            "active",
            "silent",
            "reactivated",
            "transformed",
            "protected",
            "quarantined",
            "forgotten",
        ],
        "allocation_gate_ref": "runtime/state/memory/memory_allocation_gate.json"
        if memory_allocation_gate
        else None,
        "memory_write_gate_ref": "runtime/state/memory/memory_write_gate.json"
        if memory_write_gate
        else None,
        "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json"
        if state_merge_guard
        else None,
        "downstream_consumer_refs": [
            "runtime/state/memory/memory_retrieval_frame.json#cue_activation_profile",
            "runtime/state/memory/pattern_separation_index.json",
            "runtime/state/memory/pattern_completion_frame.json",
            "runtime/state/life_state.json#memory_index.engram_cluster_refs",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _cluster(
    *,
    run_id: str,
    generated_at: str,
    cluster_kind: str,
    primary_trace: dict[str, Any] | None,
    seed_refs: list[str],
    activation_cues: list[str],
    modulation_refs: list[str],
    reportability: str,
) -> dict[str, Any]:
    trace_ref = ""
    if primary_trace and primary_trace.get("trace_id"):
        trace_ref = f"runtime/state/memory/memory_trace_store.json#trace:{primary_trace['trace_id']}"
    cluster_id = f"engram-cluster-{_short_hash('|'.join([run_id, cluster_kind] + seed_refs[:4]))}"
    return {
        "cluster_id": cluster_id,
        "cluster_kind": cluster_kind,
        "cluster_ref": f"{ENGRAM_CLUSTER_REF}#cluster:{cluster_id}",
        "primary_trace_ref": trace_ref,
        "seed_refs": _dedupe(([trace_ref] if trace_ref else []) + seed_refs),
        "activation_cues": _dedupe(activation_cues),
        "modulation_refs": _dedupe(modulation_refs),
        "reportability": reportability,
        "created_at": generated_at,
    }


def _trace_by_kind(traces: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for trace in traces:
        kind = str(trace.get("memory_kind", ""))
        if kind and kind not in result:
            result[kind] = trace
    return result


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
