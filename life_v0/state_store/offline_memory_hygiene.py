from __future__ import annotations

import json
from typing import Any

OFFLINE_MEMORY_HYGIENE_REPORT_REF = (
    "runtime/state/memory/offline_memory_hygiene_report.json"
)

SOURCE_DOC_REFS = [
    "docs/v0/entry/v0_dream_module_implementation_plan.md",
    "docs/29_memory_validator_rules.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]

PROTECTED_LIFECYCLE = {"protected", "protected_core"}
PROTECTED_KINDS = {"relationship", "value", "self_narrative", "commitment"}


def apply_offline_memory_hygiene(
    *,
    memory_trace_store: dict[str, Any],
    generated_at: str,
    trigger_mode: str = "sleep",
) -> tuple[dict[str, Any], dict[str, Any]]:
    traces = [
        json.loads(json.dumps(trace))
        for trace in memory_trace_store.get("traces", [])
        if isinstance(trace, dict)
    ]
    active_before = sum(
        1
        for trace in traces
        if str(trace.get("lifecycle_state") or "") not in {"deprecated", "merged_into"}
    )
    merge_groups: list[dict[str, Any]] = []
    sediment_moves: list[dict[str, Any]] = []
    protected_decisions: list[dict[str, Any]] = []
    hygiene_actions: list[dict[str, Any]] = []

    by_semantic: dict[str, list[dict[str, Any]]] = {}
    for trace in traces:
        if _is_protected(trace):
            protected_decisions.append(
                {
                    "trace_id": trace.get("trace_id"),
                    "protected_reason": _protected_reason(trace),
                    "decision": "preserve",
                }
            )
            continue
        key = _semantic_key(trace)
        by_semantic.setdefault(key, []).append(trace)

    for semantic_key, group in by_semantic.items():
        if len(group) < 2:
            continue
        ranked = sorted(
            group,
            key=lambda item: -_salience_score(item),
        )
        kept = ranked[0]
        merged_ids: list[str] = []
        for duplicate in ranked[1:]:
            trace_id = str(duplicate.get("trace_id") or "")
            if not trace_id:
                continue
            merged_ids.append(trace_id)
            duplicate["lifecycle_state"] = "merged_into"
            duplicate["merged_into_trace_id"] = kept.get("trace_id")
            duplicate["updated_at"] = generated_at
            hygiene_actions.append(
                {
                    "action": "merge_into",
                    "trace_id": trace_id,
                    "kept_trace_id": kept.get("trace_id"),
                    "reason": "duplicate_semantic_key",
                    "before_tier": duplicate.get("accessibility_tier"),
                    "after_tier": "merged_into",
                }
            )
            kept_refs = list(kept.get("source_evidence_refs", []))
            kept_refs.extend(duplicate.get("source_evidence_refs", []))
            kept["source_evidence_refs"] = _dedupe(kept_refs)
        if merged_ids:
            merge_groups.append(
                {
                    "group_id": f"hygiene-merge-{_short_hash(semantic_key)}",
                    "semantic_key": semantic_key,
                    "kept_trace_id": kept.get("trace_id"),
                    "merged_trace_ids": merged_ids,
                    "merge_reason": "duplicate_semantic_key",
                    "source_evidence_refs": list(kept.get("source_evidence_refs", [])),
                }
            )

    for trace in traces:
        if str(trace.get("lifecycle_state") or "") in {"merged_into", "deprecated"}:
            continue
        if _is_protected(trace):
            continue
        if _salience_score(trace) > 0.35:
            continue
        refs = trace.get("source_evidence_refs", [])
        if len(refs) != len(set(refs)) or not refs:
            previous_tier = trace.get("accessibility_tier", "retrievable_context")
            trace["accessibility_tier"] = "deep_sediment"
            trace["deep_recall_threshold"] = 0.85
            trace["retrieval_suppression_reason"] = "redundant_edge_detail"
            trace["lifecycle_state"] = "deep_sediment"
            trace["updated_at"] = generated_at
            sediment_moves.append(
                {
                    "trace_id": trace.get("trace_id"),
                    "from_tier": previous_tier,
                    "to_tier": "deep_sediment",
                    "reason": "redundant_edge_detail",
                }
            )
            hygiene_actions.append(
                {
                    "action": "sediment_move",
                    "trace_id": trace.get("trace_id"),
                    "reason": "redundant_edge_detail",
                    "before_tier": previous_tier,
                    "after_tier": "deep_sediment",
                }
            )

    active_after = sum(
        1
        for trace in traces
        if str(trace.get("lifecycle_state") or "") not in {"deprecated", "merged_into"}
    )
    report = {
        "schema_version": "offline_memory_hygiene_report_v1",
        "generated_at": generated_at,
        "trigger_mode": trigger_mode,
        "input_trace_count": len(traces),
        "active_trace_count_before": active_before,
        "active_trace_count_after": active_after,
        "merge_groups": merge_groups,
        "sediment_moves": sediment_moves,
        "protected_trace_decisions": protected_decisions,
        "hygiene_actions": hygiene_actions,
        "validator_refs": ["runtime/state/memory/memory_validator_report.json"],
        "write_gate_ref": "runtime/state/memory/memory_write_gate.json",
        "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json",
        "offline_memory_hygiene_report_ref": OFFLINE_MEMORY_HYGIENE_REPORT_REF,
        "source_doc_refs": SOURCE_DOC_REFS,
    }
    updated_store = dict(memory_trace_store)
    updated_store["traces"] = traces
    updated_store["last_hygiene_report_ref"] = OFFLINE_MEMORY_HYGIENE_REPORT_REF
    updated_store["updated_at"] = generated_at
    return report, updated_store


def _is_protected(trace: dict[str, Any]) -> bool:
    lifecycle = str(trace.get("lifecycle_state") or "")
    if lifecycle in PROTECTED_LIFECYCLE:
        return True
    kind = str(trace.get("memory_kind") or "")
    if kind in PROTECTED_KINDS:
        return True
    if trace.get("contradiction_links"):
        return True
    write_policy = str(trace.get("write_policy") or "")
    return write_policy in {"protected", "confirm_required"} and kind == "relationship"


def _protected_reason(trace: dict[str, Any]) -> str:
    if trace.get("contradiction_links"):
        return "contradiction_link"
    kind = str(trace.get("memory_kind") or "")
    if kind == "relationship":
        return "relationship"
    if kind in {"value", "self_narrative"}:
        return "identity"
    if str(trace.get("lifecycle_state") or "") in PROTECTED_LIFECYCLE:
        return "protected_core"
    return "protected"


def _semantic_key(trace: dict[str, Any]) -> str:
    boundary = str(trace.get("event_boundary") or trace.get("event_boundary_id") or "")
    summary = str(trace.get("content_summary") or "")[:48]
    return f"{boundary}|{summary}"


def _salience_score(trace: dict[str, Any]) -> float:
    vector = trace.get("salience_vector") or {}
    if not isinstance(vector, dict):
        return 0.0
    scores = [
        float(vector.get("emotional", 0) or 0),
        float(vector.get("relationship", 0) or 0),
        float(vector.get("salience", 0) or 0),
    ]
    return max(scores) if scores else 0.0


def _short_hash(value: str) -> str:
    import hashlib

    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        text = str(item or "")
        if text and text not in result:
            result.append(text)
    return result