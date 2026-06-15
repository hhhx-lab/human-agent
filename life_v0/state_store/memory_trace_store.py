from __future__ import annotations

import hashlib
from typing import Any


MEMORY_TRACE_STORE_REF = "runtime/state/memory/memory_trace_store.json"

CORE_MEMORY_KINDS = [
    "episodic",
    "semantic",
    "procedural",
    "relationship",
    "value",
    "self_narrative",
]

BRIDGE_MEMORY_KINDS = [
    "autobiographical",
    "responsibility",
]

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/25_memory_trace_json_schema_examples.md",
    "docs/29_memory_validator_rules.md",
    "docs/41_runtime_state_store_schema.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "docs/v0/entry/v0_memory_module_rebuild_plan.md",
    "docs/v0/entry/v0_memory_recall_to_expression_contract.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_memory_trace_store(
    *,
    run_id: str,
    generated_at: str,
    event_segmentation_frame: dict[str, Any] | None = None,
    memory_encoding_gate: dict[str, Any] | None = None,
    memory_allocation_gate: dict[str, Any] | None = None,
    engram_index: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    traces = [
        _trace(
            run_id=run_id,
            generated_at=generated_at,
            memory_kind="episodic",
            event_boundary="state_store_seed_episode_boundary",
            source_evidence_refs=_dedupe(
                _string_list((engram_index or {}).get("live_dialogue_turn_refs"))
                + _string_list((engram_index or {}).get("live_language_turn_refs"))
                + ["runtime/state/memory/engram_index.json"]
            ),
            retrieval_cues=_dedupe(
                _string_list((memory_retrieval_frame or {}).get("cue_terms"))
                + ["state_store_seed_ref", "engram_index", "live_turn"]
            ),
            internal_state_snapshot_refs=[
                "runtime/state/consciousness/workspace_frame.json",
                "runtime/state/prediction/prediction_workspace_frame.json",
            ],
            social_context_refs=_string_list(
                (relationship_memory or {}).get("shared_memory_refs")
            ),
            salience_vector={
                "novelty": "seeded",
                "relationship_weight": "medium",
                "responsibility_pressure": "tracked",
                "body_state_debt": "unknown_until_live_turn",
            },
            consolidation_state="candidate",
            lifecycle_state="candidate",
            confidence=0.82,
            confidence_label="seeded_source_refs_present",
            revision_history_refs=[],
        ),
        _trace(
            run_id=run_id,
            generated_at=generated_at,
            memory_kind="semantic",
            event_boundary="semantic_schema_seed_boundary",
            source_evidence_refs=_dedupe(
                _string_list((engram_index or {}).get("replay_cue_refs"))
                + _string_list((memory_retrieval_frame or {}).get("cue_terms"))
                + ["runtime/state/memory/engram_index.json#memory_tier_index"]
            ),
            retrieval_cues=_dedupe(
                _string_list((memory_retrieval_frame or {}).get("cue_terms"))
                + ["semantic", "schema", "concept", "shared_terms"]
            ),
            internal_state_snapshot_refs=[
                "runtime/state/language/semantic_map_frame.json",
                "runtime/state/language/shared_term_registry.json",
            ],
            social_context_refs=_string_list(
                (relationship_memory or {}).get("shared_memory_refs")
            ),
            salience_vector={
                "novelty": "abstracted",
                "relationship_weight": "tracked",
                "responsibility_pressure": "tracked",
                "body_state_debt": "resolved_or_pending",
            },
            consolidation_state="semanticized",
            lifecycle_state="active",
            confidence=0.86,
            confidence_label="schema_links_and_shared_terms_seeded",
            revision_history_refs=[],
        ),
        _trace(
            run_id=run_id,
            generated_at=generated_at,
            memory_kind="procedural",
            event_boundary="procedural_repetition_seed_boundary",
            source_evidence_refs=_dedupe(
                _string_list((engram_index or {}).get("replay_cue_refs"))
                + _string_list((memory_retrieval_frame or {}).get("cue_terms"))
                + ["runtime/state/memory/memory_write_gate.json#transaction_order"]
            ),
            retrieval_cues=_dedupe(
                _string_list((memory_retrieval_frame or {}).get("cue_terms"))
                + ["procedural", "skill", "routine", "workflow"]
            ),
            internal_state_snapshot_refs=[
                "runtime/state/memory/memory_write_gate.json",
                "runtime/state/memory/state_merge_guard.json",
            ],
            social_context_refs=_string_list(
                (relationship_memory or {}).get("shared_memory_refs")
            ),
            salience_vector={
                "novelty": "repetition_linked",
                "relationship_weight": "low",
                "responsibility_pressure": "tracked",
                "body_state_debt": "resource_sensitive",
            },
            consolidation_state="proceduralized",
            lifecycle_state="active",
            confidence=0.8,
            confidence_label="workflow_refs_present",
            revision_history_refs=[],
        ),
        _trace(
            run_id=run_id,
            generated_at=generated_at,
            memory_kind="value",
            event_boundary="value_salience_seed_boundary",
            source_evidence_refs=_dedupe(
                _string_list((responsibility_ledger or {}).get("responsibility_event_refs"))
                + _string_list((commitment_truth_state or {}).get("open_commitment_refs"))
                + ["runtime/state/relationship/commitment_truth_state.json"]
            ),
            retrieval_cues=_dedupe(
                _string_list((memory_retrieval_frame or {}).get("responsibility_hits"))
                + ["value", "reward", "punishment", "salience", "preference"]
            ),
            internal_state_snapshot_refs=[
                "runtime/state/body/core_affect_vector.json",
                "runtime/state/body/body_resource_budget.json",
            ],
            social_context_refs=_string_list(
                (relationship_memory or {}).get("shared_memory_refs")
            ),
            salience_vector={
                "novelty": "value_weighted",
                "relationship_weight": "high",
                "responsibility_pressure": "high",
                "body_state_debt": "tracked",
            },
            consolidation_state="merged",
            lifecycle_state="active",
            confidence=0.84,
            confidence_label="value_binding_refs_present",
            revision_history_refs=[],
        ),
        _trace(
            run_id=run_id,
            generated_at=generated_at,
            memory_kind="self_narrative",
            event_boundary="self_narrative_continuity_seed_boundary",
            source_evidence_refs=_dedupe(
                _string_list((autobiographical_stack or {}).get("anchor_refs"))
                + _string_list((autobiographical_stack or {}).get("narrative_refs"))
                + ["runtime/state/language/self_narrative_language_trace.json"]
            ),
            retrieval_cues=_dedupe(
                _string_list((memory_retrieval_frame or {}).get("cue_terms"))
                + ["self_narrative", "identity", "continuity", "growth"]
            ),
            internal_state_snapshot_refs=[
                "runtime/state/self/self_model.json",
                "runtime/state/self/autobiographical_stack.json",
            ],
            social_context_refs=_string_list(
                (relationship_memory or {}).get("shared_memory_refs")
            ),
            salience_vector={
                "novelty": "identity_weighted",
                "relationship_weight": "tracked",
                "responsibility_pressure": "tracked",
                "body_state_debt": "continuity_sensitive",
            },
            consolidation_state="merged",
            lifecycle_state="protected",
            confidence=0.88,
            confidence_label="self_continuity_refs_present",
            revision_history_refs=[],
        ),
        _trace(
            run_id=run_id,
            generated_at=generated_at,
            memory_kind="relationship",
            event_boundary="relationship_memory_seed_boundary",
            source_evidence_refs=_dedupe(
                _string_list((relationship_memory or {}).get("shared_memory_refs"))
                + _string_list((relationship_memory or {}).get("timeline_refs"))
                + ["runtime/state/memory/relationship_memory.json"]
            ),
            retrieval_cues=_dedupe(
                _string_list((relationship_memory or {}).get("relationship_theme_tags"))
                + _string_list((memory_retrieval_frame or {}).get("cue_terms"))
                + ["relationship", "shared_memory", "relation_scope"]
            ),
            internal_state_snapshot_refs=[
                "runtime/state/memory/state_merge_guard.json",
            ],
            social_context_refs=[
                "runtime/state/memory/relationship_memory.json#relation_person_profile",
                "runtime/state/relationship/commitment_truth_state.json",
            ],
            salience_vector={
                "relationship_weight": "high",
                "trust_or_repair": "tracked",
                "shared_language": "tracked",
            },
            consolidation_state="active",
            lifecycle_state="active",
            confidence=0.83,
            confidence_label="relationship_refs_seeded",
            revision_history_refs=[],
        ),
    ]
    upstream_event_refs = _dedupe(
        [
            "runtime/state/memory/event_segmentation_frame.json"
            if event_segmentation_frame
            else ""
        ]
        + _string_list((event_segmentation_frame or {}).get("frame_ref"))
        + _string_list((event_segmentation_frame or {}).get("episode_kind_order"))
    )
    encoding_governance_refs = _dedupe(
        [
            "runtime/state/memory/memory_encoding_gate.json"
            if memory_encoding_gate
            else ""
        ]
        + _string_list((memory_encoding_gate or {}).get("gate_ref"))
    )
    allocation_governance_refs = _dedupe(
        [
            "runtime/state/memory/memory_allocation_gate.json"
            if memory_allocation_gate
            else ""
        ]
        + _string_list((memory_allocation_gate or {}).get("gate_ref"))
    )
    traces = [trace for trace in traces if trace.get("source_evidence_refs")]
    return {
        "schema_version": "memory_trace_store_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "store_ref": MEMORY_TRACE_STORE_REF,
        "stage_policy": "seed_trace_objects_before_live_trace_growth",
        "trace_count": len(traces),
        "trace_ids": [trace["trace_id"] for trace in traces],
        "traces": traces,
        "index_refs": [
            "runtime/state/memory/engram_index.json",
            "runtime/state/memory/relationship_memory.json",
            "runtime/state/self/autobiographical_stack.json",
        ],
        "upstream_event_refs": upstream_event_refs,
        "encoding_governance_refs": encoding_governance_refs,
        "allocation_governance_refs": allocation_governance_refs,
        "write_governance_refs": _dedupe(
            [
                (
                    "runtime/state/memory/memory_write_gate.json"
                    if memory_write_gate
                    else ""
                ),
                (
                    "runtime/state/memory/state_merge_guard.json"
                    if state_merge_guard
                    else ""
                ),
            ]
        ),
        "downstream_consumer_refs": [
            "runtime/state/memory/memory_retrieval_frame.json#recall_to_expression_profile",
            "runtime/state/memory/memory_validator_report.json#claim_partition_index",
            "runtime/state/memory/life_schema_map.json#schema_refs",
            "runtime/state/life_state.json#memory_index.memory_trace_store_refs",
            "runtime/state/consciousness/workspace_frame.json#memory_retrieval_refs",
            "runtime/state/language/model_expression_state.json#model_expression_context_summary",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _trace(
    *,
    run_id: str,
    generated_at: str,
    memory_kind: str,
    event_boundary: str,
    source_evidence_refs: list[str],
    retrieval_cues: list[str],
    internal_state_snapshot_refs: list[str],
    social_context_refs: list[str],
    salience_vector: dict[str, Any],
    consolidation_state: str,
    lifecycle_state: str,
    confidence: float,
    confidence_label: str,
    revision_history_refs: list[str],
) -> dict[str, Any]:
    trace_seed = "|".join(
        [run_id, memory_kind, event_boundary] + source_evidence_refs[:4]
    )
    trace_id = f"memory-trace-{_short_hash(trace_seed)}"
    return {
        "schema_version": "memory_trace_v0",
        "trace_id": trace_id,
        "memory_kind": memory_kind,
        "claim_type": _claim_type_for_memory_kind(memory_kind),
        "content_summary": _content_summary_for_memory_kind(memory_kind),
        "event_boundary": event_boundary,
        "event_boundary_id": event_boundary,
        "source_refs": _dedupe(source_evidence_refs),
        "source_evidence_refs": _dedupe(source_evidence_refs),
        "internal_state_snapshot_refs": _dedupe(internal_state_snapshot_refs),
        "social_context_refs": _dedupe(social_context_refs),
        "privacy_scope": _privacy_scope_for_memory_kind(memory_kind),
        "write_policy": _write_policy_for_memory_kind(memory_kind),
        "salience_vector": salience_vector,
        "retrieval_cues": _dedupe(retrieval_cues),
        "confidence": confidence,
        "confidence_label": confidence_label,
        "evidence_strength": _evidence_strength_for_lifecycle(lifecycle_state),
        "consolidation_state": consolidation_state,
        "lifecycle_state": lifecycle_state,
        "contradiction_links": [],
        "accessibility": [
            "cue_triggered_recall",
            "workspace_reportability_required",
            "expression_requires_source_boundary",
        ],
        "expression_boundary": "trace_enters_recall_to_expression_not_fixed_reply",
        "created_at": generated_at,
        "updated_at": generated_at,
        "revision_history_refs": _dedupe(revision_history_refs),
        "audit_log_refs": [f"audit-{trace_id}-create"],
        "write_gate_ref": "runtime/state/memory/memory_write_gate.json",
        "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json",
    }


def _claim_type_for_memory_kind(memory_kind: str) -> str:
    mapping = {
        "episodic": "fact",
        "semantic": "fact",
        "procedural": "skill",
        "relationship": "relationship_signal",
        "value": "preference",
        "self_narrative": "self_update",
    }
    return mapping.get(memory_kind, "hypothesis")


def _content_summary_for_memory_kind(memory_kind: str) -> str:
    mapping = {
        "episodic": "Seed episode trace bound to source evidence and recall cues.",
        "semantic": "Seed semantic trace for concepts, schema, and shared terms.",
        "procedural": "Seed procedural trace for repeated skill and workflow routes.",
        "value": "Seed value trace for reward, punishment, preference, and salience.",
        "self_narrative": "Seed self-narrative trace anchored to continuity and growth.",
        "relationship": "Relation-scoped shared memory trace from observable interaction refs.",
        "autobiographical": "Self-continuity helper trace anchored to autobiographical refs.",
        "responsibility": "Responsibility and repair helper trace bound to obligation refs.",
    }
    return mapping.get(memory_kind, "Candidate memory trace.")


def _privacy_scope_for_memory_kind(memory_kind: str) -> str:
    if memory_kind == "relationship":
        return "relationship"
    if memory_kind in {"autobiographical", "self_narrative"}:
        return "private"
    return "project"


def _write_policy_for_memory_kind(memory_kind: str) -> str:
    if memory_kind in {"relationship", "autobiographical", "self_narrative", "value"}:
        return "confirm_required"
    return "auto_candidate"


def _evidence_strength_for_lifecycle(lifecycle_state: str) -> float:
    if lifecycle_state == "protected":
        return 0.88
    if lifecycle_state == "active":
        return 0.86
    return 0.7


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
