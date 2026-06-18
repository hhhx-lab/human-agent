from __future__ import annotations

import hashlib
import json
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
    live_turn_context: dict[str, Any] | None = None,
    existing_memory_trace_store: dict[str, Any] | None = None,
) -> dict[str, Any]:
    accumulated_store = bool(
        existing_memory_trace_store
        and existing_memory_trace_store.get("traces")
    )
    if accumulated_store:
        traces = [
            json.loads(json.dumps(trace))
            for trace in existing_memory_trace_store.get("traces", [])
            if isinstance(trace, dict)
        ]
    else:
        traces = _build_seed_traces(
            run_id=run_id,
            generated_at=generated_at,
            engram_index=engram_index,
            autobiographical_stack=autobiographical_stack,
            relationship_memory=relationship_memory,
            memory_retrieval_frame=memory_retrieval_frame,
            responsibility_ledger=responsibility_ledger,
            commitment_truth_state=commitment_truth_state,
        )
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
    live_traces = project_live_dialogue_episode_traces(
        run_id=run_id,
        generated_at=generated_at,
        live_turn_context=live_turn_context,
        memory_retrieval_frame=memory_retrieval_frame,
        relationship_memory=relationship_memory,
        responsibility_ledger=responsibility_ledger,
        commitment_truth_state=commitment_truth_state,
    )
    if live_traces:
        if accumulated_store:
            existing_dialogue_refs = {
                str(trace.get("dialogue_turn_ref") or "")
                for trace in traces
                if isinstance(trace, dict)
            }
            for live_trace in live_traces:
                dialogue_ref = str(live_trace.get("dialogue_turn_ref") or "")
                if dialogue_ref and dialogue_ref in existing_dialogue_refs:
                    continue
                traces.append(live_trace)
                if dialogue_ref:
                    existing_dialogue_refs.add(dialogue_ref)
        else:
            traces.extend(live_traces)
            traces = _merge_prior_live_traces(
                traces,
                existing_memory_trace_store=existing_memory_trace_store,
                new_live_traces=live_traces,
            )
    traces = _dedupe_traces_by_trace_id(traces)
    fast_episodic_buffer = build_fast_episodic_buffer(
        traces=traces,
        run_id=run_id,
        generated_at=generated_at,
    )
    return {
        "schema_version": "memory_trace_store_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "store_ref": MEMORY_TRACE_STORE_REF,
        "stage_policy": (
            "live_trace_accumulation_on_existing_store"
            if accumulated_store
            else "seed_trace_objects_before_live_trace_growth"
        ),
        "trace_count": len(traces),
        "trace_ids": [trace["trace_id"] for trace in traces],
        "traces": traces,
        "fast_episodic_buffer": fast_episodic_buffer,
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


def _build_seed_traces(
    *,
    run_id: str,
    generated_at: str,
    engram_index: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    memory_retrieval_frame: dict[str, Any] | None,
    responsibility_ledger: dict[str, Any] | None,
    commitment_truth_state: dict[str, Any] | None,
) -> list[dict[str, Any]]:
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
    return [trace for trace in traces if trace.get("source_evidence_refs")]


def guard_offline_trace_mutations(
    *,
    before_traces: list[dict[str, Any]],
    after_traces: list[dict[str, Any]],
) -> dict[str, Any]:
    before_by_id = {
        str(trace.get("trace_id")): trace
        for trace in before_traces
        if isinstance(trace, dict) and trace.get("trace_id")
    }
    blocked_mutations: list[dict[str, Any]] = []
    protected_fields = (
        "content_summary",
        "claim_type",
        "lifecycle_state",
        "source_evidence_refs",
        "contradiction_links",
    )
    for trace in after_traces:
        if not isinstance(trace, dict):
            continue
        trace_id = str(trace.get("trace_id") or "")
        before = before_by_id.get(trace_id)
        if not before or before.get("lifecycle_state") != "protected":
            continue
        changed_fields = [
            field
            for field in protected_fields
            if trace.get(field) != before.get(field)
        ]
        if changed_fields:
            blocked_mutations.append(
                {
                    "trace_id": trace_id,
                    "rule_id": "MEM-PRO-001",
                    "changed_fields": changed_fields,
                    "decision": "block_protected_update",
                }
            )
    return {
        "schema_version": "offline_trace_mutation_guard_v0",
        "protected_mutation_blocked": bool(blocked_mutations),
        "blocked_mutation_count": len(blocked_mutations),
        "blocked_mutations": blocked_mutations,
        "guard_boundary": "offline_replay_dream_cannot_rewrite_protected_traces",
    }


def project_live_dialogue_episode_traces(
    *,
    run_id: str,
    generated_at: str,
    live_turn_context: dict[str, Any] | None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    context = live_turn_context or {}
    dialogue_turn_refs = _string_list(context.get("dialogue_turn_refs"))
    if not dialogue_turn_refs:
        return []
    external_turn_ref = dialogue_turn_refs[0] if dialogue_turn_refs else None
    life_turn_ref = dialogue_turn_refs[1] if len(dialogue_turn_refs) > 1 else None
    external_utterance = str(context.get("external_utterance") or "").strip()
    life_response = str(context.get("life_response") or "").strip()
    semantic_focus = str(
        context.get("semantic_focus")
        or context.get("live_turn_focus")
        or (memory_retrieval_frame or {}).get("live_semantic_focus")
        or (memory_retrieval_frame or {}).get("reconstruction_focus")
        or "live_dialogue_episode"
    )
    reconstruction_focus = str(
        context.get("reconstruction_focus")
        or (memory_retrieval_frame or {}).get("reconstruction_focus")
        or semantic_focus
    )
    expression_outcome = str(
        context.get("expression_outcome") or "released"
    )
    utterance_digest = _utterance_digest(external_utterance)
    source_evidence_refs = _dedupe(
        dialogue_turn_refs
        + _string_list(context.get("live_language_turn_refs"))
        + _string_list(context.get("expression_monitor_refs"))
        + _string_list(context.get("post_expression_gate_refs"))
        + _string_list(context.get("cross_modal_evidence_refs"))
        + _string_list(context.get("percept_frame_refs"))
        + _string_list(context.get("world_contact_refs"))
        + [
            "runtime/state/language/language_percept_frame.json",
            "runtime/state/language/semantic_map_frame.json",
        ]
    )
    if not any("dialogue_turn_log.jsonl#line-" in ref for ref in source_evidence_refs):
        return []
    responsibility_refs = _dedupe(
        _string_list((responsibility_ledger or {}).get("repair_obligations"))
        + _string_list((responsibility_ledger or {}).get("responsibility_event_refs"))
        + _string_list((commitment_truth_state or {}).get("repair_required_refs"))
    )
    content_summary = _live_episode_content_summary(
        semantic_focus=semantic_focus,
        expression_outcome=expression_outcome,
        external_utterance=external_utterance,
        life_response=life_response,
    )
    trace = _trace(
        run_id=run_id,
        generated_at=generated_at,
        memory_kind="episodic",
        event_boundary=f"live_dialogue_episode:{external_turn_ref or dialogue_turn_refs[-1]}",
        source_evidence_refs=source_evidence_refs,
        retrieval_cues=_dedupe(
            _string_list((memory_retrieval_frame or {}).get("cue_terms"))
            + [semantic_focus, reconstruction_focus, utterance_digest]
        ),
        internal_state_snapshot_refs=_dedupe(
            _string_list(context.get("body_snapshot_refs"))
            + _string_list(context.get("core_affect_snapshot_refs"))
            + [
                "runtime/state/body/core_affect_vector.json",
                "runtime/state/body/body_resource_budget.json",
            ]
        ),
        social_context_refs=_dedupe(
            [
                "runtime/state/memory/relationship_memory.json#relation_person_profile",
                "runtime/state/relationship/relationship_timeline.json",
            ]
            + _string_list((relationship_memory or {}).get("shared_memory_refs"))
        ),
        salience_vector={
            "novelty": "live_turn",
            "relationship_weight": "high",
            "responsibility_pressure": "high" if responsibility_refs else "tracked",
            "body_state_debt": "live_snapshot",
            "semantic_focus": semantic_focus,
        },
        consolidation_state="episodic",
        lifecycle_state="active",
        confidence=0.79,
        confidence_label="live_dialogue_source_evidence_present",
        revision_history_refs=[],
        extra_fields={
            "live_trace_origin": "live_dialogue_turn",
            "dialogue_turn_ref": external_turn_ref or dialogue_turn_refs[0],
            "external_utterance_ref": external_turn_ref,
            "life_response_ref": life_turn_ref,
            "utterance_digest": utterance_digest,
            "semantic_focus": semantic_focus,
            "reconstruction_focus": reconstruction_focus,
            "expression_outcome": expression_outcome,
            "relationship_scope": str(
                context.get("relationship_scope")
                or context.get("relation_subject_scope")
                or "relation_scoped_live_episode"
            ),
            "relation_subject_id": context.get("relation_subject_id"),
            "cross_modal_evidence_refs": _string_list(
                context.get("cross_modal_evidence_refs")
            ),
            "cross_modal_feature_bundle": context.get("cross_modal_feature_bundle"),
            "relation_person_profile_ref": (
                "runtime/state/memory/relationship_memory.json#relation_person_profile"
            ),
            "responsibility_refs": responsibility_refs,
            "post_expression_gate_status": str(
                context.get("post_expression_gate_status") or expression_outcome
            ),
            "accessibility_score": float(context.get("accessibility_score") or 0.55),
            "replay_salience": float(context.get("replay_salience") or 0.5),
            "content_summary": content_summary,
        },
    )
    return [trace]


def project_exit_dream_episode_traces(
    *,
    run_id: str,
    generated_at: str,
    exit_dream_summary: dict[str, Any],
    existing_memory_trace_store: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    memory_tiering = exit_dream_summary.get("memory_tiering")
    if not isinstance(memory_tiering, dict):
        memory_tiering = {}
    core_refs = set(
        _string_list(memory_tiering.get("salient_core_episode_refs"))
    )
    context_refs = set(
        _string_list(memory_tiering.get("retrievable_context_episode_refs"))
    )
    sediment_refs = set(
        _string_list(memory_tiering.get("deep_sediment_episode_refs"))
    )
    existing_by_source: dict[str, dict[str, Any]] = {}
    for trace in (existing_memory_trace_store or {}).get("traces", []):
        if not isinstance(trace, dict):
            continue
        if trace.get("exit_dream_origin") != "terminal_exit_consolidation":
            continue
        for ref in _string_list(trace.get("source_evidence_refs")):
            existing_by_source[ref] = trace

    projected: list[dict[str, Any]] = []
    for episode in exit_dream_summary.get("deduplicated_episode_summaries", []):
        if not isinstance(episode, dict):
            continue
        source_ref = str(episode.get("source_ref") or "")
        if not source_ref:
            continue
        tier_profile = _exit_dream_accessibility_profile(
            source_ref=source_ref,
            core_refs=core_refs,
            context_refs=context_refs,
            sediment_refs=sediment_refs,
        )
        semantic_key = str(episode.get("semantic_key") or "")
        summary = str(episode.get("summary") or "")
        memory_kind = _exit_dream_memory_kind(semantic_key=semantic_key)
        source_evidence_refs = _dedupe(
            [
                source_ref,
                "runtime/state/dream/exit_dream_consolidation_summary.json",
                "runtime/state/memory/dialogue_memory_summary.json",
            ]
        )
        if source_ref in existing_by_source:
            trace = json.loads(json.dumps(existing_by_source[source_ref]))
            trace.update(
                {
                    "salience_vector": tier_profile["salience_vector"],
                    "accessibility_tier": tier_profile["accessibility_tier"],
                    "deep_recall_threshold": tier_profile["deep_recall_threshold"],
                    "retrieval_suppression_reason": tier_profile[
                        "retrieval_suppression_reason"
                    ],
                    "lifecycle_state": tier_profile["lifecycle_state"],
                    "cue_bindings": tier_profile["cue_bindings"],
                    "content_summary": summary[:96] or trace.get("content_summary"),
                    "updated_at": generated_at,
                }
            )
            projected.append(trace)
            continue
        trace = _trace(
            run_id=run_id,
            generated_at=generated_at,
            memory_kind=memory_kind,
            event_boundary=f"exit_dream_episode:{source_ref}",
            source_evidence_refs=source_evidence_refs,
            retrieval_cues=_dedupe(
                [semantic_key, summary[:32], "exit_dream_dialogue"]
                + _string_list(exit_dream_summary.get("relationship_theme_tags"))
            ),
            internal_state_snapshot_refs=[
                "runtime/state/dream/exit_dream_consolidation_summary.json",
                "runtime/state/memory/dialogue_memory_summary.json",
            ],
            social_context_refs=[
                "runtime/state/memory/relationship_memory.json#relation_person_profile"
            ],
            salience_vector=tier_profile["salience_vector"],
            consolidation_state="merged",
            lifecycle_state=tier_profile["lifecycle_state"],
            confidence=0.76,
            confidence_label="exit_dream_tier_projection",
            revision_history_refs=[],
            extra_fields={
                "exit_dream_origin": "terminal_exit_consolidation",
                "episode_id": episode.get("episode_id"),
                "semantic_key": semantic_key,
                "event_role": episode.get("event_role"),
                "accessibility_tier": tier_profile["accessibility_tier"],
                "deep_recall_threshold": tier_profile["deep_recall_threshold"],
                "retrieval_suppression_reason": tier_profile[
                    "retrieval_suppression_reason"
                ],
                "cue_bindings": tier_profile["cue_bindings"],
                "dream_residue_refs": [
                    "runtime/state/dream/exit_dream_consolidation_summary.json"
                ],
                "content_summary": summary[:96],
                "accessibility_score": tier_profile["accessibility_score"],
                "replay_salience": tier_profile["replay_salience"],
            },
        )
        projected.append(trace)
    return projected


def merge_exit_dream_traces_into_store(
    *,
    memory_trace_store: dict[str, Any],
    exit_dream_traces: list[dict[str, Any]],
    generated_at: str,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(memory_trace_store or {}))
    traces = [
        trace
        for trace in updated.get("traces", [])
        if isinstance(trace, dict)
        and trace.get("exit_dream_origin") != "terminal_exit_consolidation"
    ]
    exit_sources = {
        ref
        for trace in exit_dream_traces
        for ref in _string_list(trace.get("source_evidence_refs"))
        if "dialogue_turn_log.jsonl#line-" in ref
    }
    traces = [
        trace
        for trace in traces
        if not (
            trace.get("exit_dream_origin") == "terminal_exit_consolidation"
            or any(
                ref in exit_sources
                for ref in _string_list(trace.get("source_evidence_refs"))
            )
        )
    ]
    traces.extend(exit_dream_traces)
    traces = _dedupe_traces_by_trace_id(traces)
    updated["traces"] = traces
    updated["trace_ids"] = [
        str(trace.get("trace_id"))
        for trace in traces
        if isinstance(trace, dict) and trace.get("trace_id")
    ]
    updated["trace_count"] = len(updated["trace_ids"])
    updated["updated_at"] = generated_at
    updated["exit_dream_trace_projection_ref"] = (
        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering"
    )
    return updated


def _exit_dream_accessibility_profile(
    *,
    source_ref: str,
    core_refs: set[str],
    context_refs: set[str],
    sediment_refs: set[str],
) -> dict[str, Any]:
    if source_ref in core_refs:
        return {
            "accessibility_tier": "salient_core",
            "lifecycle_state": "active",
            "deep_recall_threshold": 0.25,
            "retrieval_suppression_reason": "",
            "accessibility_score": 0.82,
            "replay_salience": 0.78,
            "salience_vector": {
                "emotional": 0.72,
                "relationship": 0.68,
                "salience": 0.75,
            },
            "cue_bindings": ["relation_theme", "language_episode", "identity_cue"],
        }
    if source_ref in sediment_refs:
        return {
            "accessibility_tier": "deep_sediment",
            "lifecycle_state": "deep_sediment",
            "deep_recall_threshold": 0.85,
            "retrieval_suppression_reason": "low_salience_edge_detail",
            "accessibility_score": 0.18,
            "replay_salience": 0.22,
            "salience_vector": {
                "emotional": 0.22,
                "relationship": 0.18,
                "salience": 0.2,
            },
            "cue_bindings": ["dream_cue", "autobiographical_review"],
        }
    if source_ref in context_refs:
        return {
            "accessibility_tier": "retrievable_context",
            "lifecycle_state": "active",
            "deep_recall_threshold": 0.55,
            "retrieval_suppression_reason": "",
            "accessibility_score": 0.52,
            "replay_salience": 0.48,
            "salience_vector": {
                "emotional": 0.5,
                "relationship": 0.45,
                "salience": 0.48,
            },
            "cue_bindings": ["relation_theme", "language_episode"],
        }
    return {
        "accessibility_tier": "retrievable_context",
        "lifecycle_state": "active",
        "deep_recall_threshold": 0.55,
        "retrieval_suppression_reason": "",
        "accessibility_score": 0.5,
        "replay_salience": 0.45,
        "salience_vector": {
            "emotional": 0.45,
            "relationship": 0.4,
            "salience": 0.42,
        },
        "cue_bindings": ["language_episode"],
    }


def _exit_dream_memory_kind(semantic_key: str) -> str:
    lowered = semantic_key.lower()
    if any(token in lowered for token in ("relationship", "relation", "朋友", "家人")):
        return "relationship"
    if any(token in lowered for token in ("identity", "self", "名字", "我叫")):
        return "self_narrative"
    return "episodic"


def build_fast_episodic_buffer(
    *,
    traces: list[dict[str, Any]],
    run_id: str,
    generated_at: str,
    window_size: int = 12,
) -> dict[str, Any]:
    live_traces = [
        trace
        for trace in traces
        if isinstance(trace, dict)
        and trace.get("live_trace_origin") == "live_dialogue_turn"
        and trace.get("lifecycle_state") != "deprecated"
    ]
    entries: list[dict[str, Any]] = []
    for index, trace in enumerate(reversed(live_traces[:window_size])):
        trace_id = str(trace.get("trace_id") or "")
        decay_weight = round(max(0.35, 1.0 - (index * 0.08)), 2)
        entries.append(
            {
                "trace_ref": f"{MEMORY_TRACE_STORE_REF}#{trace_id}",
                "trace_id": trace_id,
                "decay_weight": decay_weight,
                "salience": trace.get("salience_vector") or {},
                "relationship_scope": trace.get("relationship_scope"),
                "dialogue_turn_ref": trace.get("dialogue_turn_ref"),
            }
        )
    return {
        "schema_version": "fast_episodic_buffer_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "buffer_ref": "runtime/state/memory/fast_episodic_buffer.json",
        "window_size": window_size,
        "entry_count": len(entries),
        "trace_refs": [entry["trace_ref"] for entry in entries],
        "entries": entries,
    }


def apply_retrieval_salience_delta(
    memory_trace_store: dict[str, Any],
    *,
    retrieval_hits: list[str],
    run_id: str,
    generated_at: str,
    turn_counter: int | None = None,
    allostatic_load: float = 0.0,
    mean_activation_score: float | None = None,
) -> dict[str, Any]:
    updated_store = json.loads(json.dumps(memory_trace_store or {}))
    trace_ids = _trace_ids_from_retrieval_hits(retrieval_hits)
    if not trace_ids:
        return {
            "memory_trace_store": updated_store,
            "salience_tick_report": _empty_salience_tick_report(
                run_id=run_id,
                generated_at=generated_at,
                reason="no_retrieval_hits",
            ),
        }

    suppression = max(0.15, 1.0 - float(allostatic_load or 0.0) * 0.65)
    activation_factor = 1.0
    if mean_activation_score is not None and mean_activation_score > 0:
        activation_factor = min(1.25, 0.75 + float(mean_activation_score) * 0.35)
    base_delta = 0.06 * activation_factor * suppression

    trace_updates: list[dict[str, Any]] = []
    for trace in updated_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        trace_id = str(trace.get("trace_id") or "")
        if trace_id not in trace_ids:
            continue
        if trace.get("lifecycle_state") in {"deprecated", "quarantined", "deleted", "protected"}:
            continue

        before_replay = float(trace.get("replay_salience") or 0.5)
        before_accessibility = float(trace.get("accessibility_score") or 0.55)
        salience_vector = dict(trace.get("salience_vector") or {})
        before_scalar = float(salience_vector.get("salience") or before_replay)

        replay_delta = round(base_delta, 4)
        accessibility_delta = round(base_delta * 0.55, 4)
        salience_delta = round(base_delta * 0.85, 4)

        trace["replay_salience"] = round(min(0.98, before_replay + replay_delta), 3)
        trace["accessibility_score"] = round(
            min(0.98, before_accessibility + accessibility_delta),
            3,
        )
        salience_vector["salience"] = round(min(0.98, before_scalar + salience_delta), 3)
        salience_vector["last_retrieval_tick_at"] = generated_at
        if turn_counter is not None:
            salience_vector["last_retrieval_turn_counter"] = turn_counter
        trace["salience_vector"] = salience_vector
        trace["retrieval_access_count"] = int(trace.get("retrieval_access_count") or 0) + 1
        trace["last_retrieved_at"] = generated_at
        trace["updated_at"] = generated_at

        revision_ref = (
            f"revision-retrieval-salience-{turn_counter:04d}"
            if turn_counter is not None
            else f"revision-retrieval-salience-{generated_at}"
        )
        trace["revision_history_refs"] = _dedupe(
            _string_list(trace.get("revision_history_refs")) + [revision_ref]
        )

        trace_updates.append(
            {
                "trace_id": trace_id,
                "replay_salience_delta": replay_delta,
                "salience_delta": salience_delta,
                "revision_ref": revision_ref,
            }
        )

    updated_store["last_retrieval_salience_tick_at"] = generated_at
    return {
        "memory_trace_store": updated_store,
        "salience_tick_report": {
            "schema_version": "memory_retrieval_salience_tick_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "applied": bool(trace_updates),
            "hit_count": len(trace_ids),
            "updated_trace_count": len(trace_updates),
            "allostatic_suppression": round(suppression, 3),
            "effective_delta": round(base_delta, 4),
            "trace_updates": trace_updates,
            "source_doc_refs": SOURCE_DOC_REFS,
        },
    }


def _trace_ids_from_retrieval_hits(retrieval_hits: list[str]) -> set[str]:
    trace_ids: set[str] = set()
    for ref in retrieval_hits:
        text = str(ref or "")
        if "memory_trace_store.json#" not in text:
            continue
        trace_id = text.rsplit("#", 1)[-1]
        if trace_id:
            trace_ids.add(trace_id)
    return trace_ids


def _empty_salience_tick_report(
    *,
    run_id: str,
    generated_at: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "schema_version": "memory_retrieval_salience_tick_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "applied": False,
        "reason": reason,
        "hit_count": 0,
        "updated_trace_count": 0,
        "trace_updates": [],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def apply_post_expression_reconsolidation(
    memory_trace_store: dict[str, Any],
    *,
    feedback_event: dict[str, Any],
    run_id: str,
    generated_at: str,
    relationship_memory: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    exclude_dialogue_turn_ref: str | None = None,
) -> dict[str, Any]:
    updated_store = json.loads(json.dumps(memory_trace_store or {}))
    event_type = str((feedback_event or {}).get("event_type") or "")
    if event_type not in {"correction", "confirmation", "mismatch"}:
        return {
            "memory_trace_store": updated_store,
            "memory_reconsolidation_report": _empty_reconsolidation_report(
                run_id=run_id,
                generated_at=generated_at,
                reason="no_feedback_event",
            ),
            "relationship_memory": relationship_memory,
            "state_merge_guard": state_merge_guard,
        }

    traces = [
        trace
        for trace in updated_store.get("traces", [])
        if isinstance(trace, dict)
    ]
    live_traces = [
        trace
        for trace in traces
        if trace.get("live_trace_origin") == "live_dialogue_turn"
    ]
    target_trace = _select_reconsolidation_target_trace(
        live_traces,
        event_type=event_type,
        exclude_dialogue_turn_ref=exclude_dialogue_turn_ref,
    )
    if not target_trace:
        return {
            "memory_trace_store": updated_store,
            "memory_reconsolidation_report": _empty_reconsolidation_report(
                run_id=run_id,
                generated_at=generated_at,
                reason="no_live_trace_target",
                trigger_event_ref=feedback_event.get("trigger_event_ref"),
            ),
            "relationship_memory": relationship_memory,
            "state_merge_guard": state_merge_guard,
        }

    old_trace_id = str(target_trace.get("trace_id") or "")
    old_trace_refs = [f"{MEMORY_TRACE_STORE_REF}#{old_trace_id}"]
    new_trace_refs: list[str] = []
    lifecycle_updates: list[dict[str, Any]] = []
    contradiction_links: list[dict[str, Any]] = []

    if event_type == "correction":
        target_trace["lifecycle_state"] = "deprecated"
        target_trace["consolidation_state"] = "deprecated"
        target_trace["updated_at"] = generated_at
        lifecycle_updates.append(
            {
                "trace_id": old_trace_id,
                "from_state": "active",
                "to_state": "deprecated",
                "reason": "relation_correction",
            }
        )
        new_trace = _trace(
            run_id=run_id,
            generated_at=generated_at,
            memory_kind="episodic",
            event_boundary=f"reconsolidated_episode:{old_trace_id}",
            source_evidence_refs=_dedupe(
                _string_list(target_trace.get("source_evidence_refs"))
                + _string_list([feedback_event.get("trigger_event_ref")])
            ),
            retrieval_cues=_dedupe(
                _string_list(target_trace.get("retrieval_cues"))
                + ["correction", "reconsolidation"]
            ),
            internal_state_snapshot_refs=_string_list(
                target_trace.get("internal_state_snapshot_refs")
            ),
            social_context_refs=_string_list(target_trace.get("social_context_refs")),
            salience_vector=dict(target_trace.get("salience_vector") or {}),
            consolidation_state="candidate",
            lifecycle_state="active",
            confidence=0.72,
            confidence_label="correction_reconsolidated_trace",
            revision_history_refs=_dedupe(
                _string_list(target_trace.get("revision_history_refs"))
                + [f"revision-{old_trace_id}-deprecated"]
            ),
            extra_fields={
                "live_trace_origin": "live_dialogue_turn",
                "reconsolidation_origin": "post_expression_correction",
                "supersedes_trace_id": old_trace_id,
                "content_summary": (
                    f"Corrected live episode replacing {old_trace_id} after relation feedback."
                ),
                "feedback_event_type": event_type,
            },
        )
        new_trace_id = str(new_trace.get("trace_id") or "")
        target_trace.setdefault("contradiction_links", []).append(new_trace_id)
        new_trace["contradiction_links"] = _dedupe(
            _string_list(new_trace.get("contradiction_links")) + [old_trace_id]
        )
        new_trace["supersedes_trace_id"] = old_trace_id
        contradiction_links.append(
            {
                "old_trace_id": old_trace_id,
                "new_trace_id": new_trace_id,
                "link_kind": "correction_supersedes",
            }
        )
        traces.append(new_trace)
        new_trace_refs = [f"{MEMORY_TRACE_STORE_REF}#{new_trace_id}"]
        lifecycle_updates.append(
            {
                "trace_id": new_trace_id,
                "from_state": "candidate",
                "to_state": "active",
                "reason": "correction_replacement",
            }
        )
    elif event_type == "confirmation":
        target_trace["lifecycle_state"] = "active"
        target_trace["consolidation_state"] = "episodic"
        target_trace["confidence"] = min(
            0.95, float(target_trace.get("confidence") or 0.7) + 0.05
        )
        target_trace["accessibility_score"] = min(
            0.98,
            float(target_trace.get("accessibility_score") or 0.55) + 0.12,
        )
        target_trace["replay_salience"] = min(
            0.98,
            float(target_trace.get("replay_salience") or 0.5) + 0.06,
        )
        target_trace["updated_at"] = generated_at
        lifecycle_updates.append(
            {
                "trace_id": old_trace_id,
                "from_state": "active",
                "to_state": "active",
                "reason": "confirmation_strengthened",
            }
        )
    else:
        target_trace["lifecycle_state"] = "candidate"
        target_trace["consolidation_state"] = "candidate"
        target_trace["updated_at"] = generated_at
        lifecycle_updates.append(
            {
                "trace_id": old_trace_id,
                "from_state": "active",
                "to_state": "candidate",
                "reason": "mismatch_requires_confirmation",
            }
        )

    updated_store["traces"] = traces
    updated_store["trace_ids"] = [
        str(trace.get("trace_id"))
        for trace in traces
        if isinstance(trace, dict) and trace.get("trace_id")
    ]
    updated_store["trace_count"] = len(updated_store["trace_ids"])

    updated_relationship = json.loads(json.dumps(relationship_memory or {}))
    if event_type == "correction":
        correction_refs = _dedupe(
            _string_list(updated_relationship.get("correction_refs"))
            + old_trace_refs
            + new_trace_refs
            + _string_list([feedback_event.get("trigger_event_ref")])
        )
        updated_relationship["correction_refs"] = correction_refs

    updated_merge_guard = json.loads(json.dumps(state_merge_guard or {}))
    reconsolidation_records = updated_merge_guard.setdefault(
        "reconsolidation_records", []
    )
    if isinstance(reconsolidation_records, list):
        reconsolidation_records.append(
            {
                "record_id": f"reconsolidation-{run_id}-{generated_at}",
                "event_type": event_type,
                "old_trace_refs": old_trace_refs,
                "new_trace_refs": new_trace_refs,
                "trigger_event_ref": feedback_event.get("trigger_event_ref"),
                "generated_at": generated_at,
            }
        )
    else:
        long_term_sources = updated_merge_guard.setdefault(
            "long_term_change_sources", {}
        )
        if isinstance(long_term_sources, dict):
            long_term_sources["reconsolidation_record_refs"] = _dedupe(
                _string_list(long_term_sources.get("reconsolidation_record_refs"))
                + old_trace_refs
                + new_trace_refs
            )

    from .memory_validator import build_memory_validator_report

    validator_report = build_memory_validator_report(
        run_id=run_id,
        generated_at=generated_at,
        memory_trace_store=updated_store,
        state_merge_guard=updated_merge_guard,
    )
    mem_cor_002_findings = [
        finding
        for finding in validator_report.get("findings", [])
        if isinstance(finding, dict) and finding.get("rule_id") == "MEM-COR-002"
    ]
    report = {
        "schema_version": "memory_reconsolidation_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "trigger_event_ref": feedback_event.get("trigger_event_ref"),
        "feedback_event_type": event_type,
        "old_trace_refs": old_trace_refs,
        "new_trace_refs": new_trace_refs,
        "lifecycle_updates": lifecycle_updates,
        "contradiction_links": contradiction_links,
        "validator_result": validator_report.get("result"),
        "validator_report_ref": "runtime/state/memory/memory_validator_report.json",
        "mem_cor_002_finding_count": len(mem_cor_002_findings),
        "mem_cor_002_satisfied": len(mem_cor_002_findings) == 0
        if event_type == "correction"
        else None,
        "relationship_updates": {
            "correction_refs": _string_list(
                updated_relationship.get("correction_refs")
            ),
            "field_backfill_required": "correction_refs"
            not in (relationship_memory or {}),
        },
        "merge_guard_result": "reconsolidation_record_appended",
    }
    return {
        "memory_trace_store": updated_store,
        "memory_reconsolidation_report": report,
        "memory_validator_report": validator_report,
        "relationship_memory": updated_relationship,
        "state_merge_guard": updated_merge_guard,
    }


def _empty_reconsolidation_report(
    *,
    run_id: str,
    generated_at: str,
    reason: str,
    trigger_event_ref: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "memory_reconsolidation_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "trigger_event_ref": trigger_event_ref,
        "feedback_event_type": None,
        "old_trace_refs": [],
        "new_trace_refs": [],
        "lifecycle_updates": [],
        "contradiction_links": [],
        "validator_result": reason,
        "relationship_updates": {},
        "merge_guard_result": "no_op",
    }


def merge_live_trace_refs_into_memory_organs(
    *,
    memory_trace_store: dict[str, Any],
    engram_index: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    dialogue_turn_refs: list[str] | None = None,
) -> dict[str, Any]:
    live_trace_refs = [
        f"{MEMORY_TRACE_STORE_REF}#{trace['trace_id']}"
        for trace in memory_trace_store.get("traces", [])
        if isinstance(trace, dict)
        and trace.get("live_trace_origin") == "live_dialogue_turn"
        and trace.get("trace_id")
    ]
    live_trace_ids = [
        str(trace.get("trace_id"))
        for trace in memory_trace_store.get("traces", [])
        if isinstance(trace, dict)
        and trace.get("live_trace_origin") == "live_dialogue_turn"
        and trace.get("trace_id")
    ]
    updated_engram = json.loads(json.dumps(engram_index or {}))
    updated_autobiographical = json.loads(json.dumps(autobiographical_stack or {}))
    updated_relationship = json.loads(json.dumps(relationship_memory or {}))
    if live_trace_refs:
        updated_engram["live_memory_trace_refs"] = _dedupe(
            _string_list(updated_engram.get("live_memory_trace_refs")) + live_trace_refs
        )
        updated_engram["memory_trace_refs"] = _dedupe(
            _string_list(updated_engram.get("memory_trace_refs")) + live_trace_refs
        )
    if live_trace_ids and updated_autobiographical:
        hierarchy = updated_autobiographical.setdefault("memory_hierarchy", {})
        if not isinstance(hierarchy, dict):
            hierarchy = {}
            updated_autobiographical["memory_hierarchy"] = hierarchy
        specific_episode_refs = _dedupe(
            _string_list(hierarchy.get("specific_episode_refs"))
            + live_trace_refs
            + _string_list(dialogue_turn_refs)
        )
        hierarchy["specific_episode_refs"] = specific_episode_refs
        updated_autobiographical["specific_episode_refs"] = specific_episode_refs
        for thread in hierarchy.get("general_event_threads", []):
            if isinstance(thread, dict):
                thread["specific_episode_refs"] = _dedupe(
                    _string_list(thread.get("specific_episode_refs")) + live_trace_refs
                )
        for goal in hierarchy.get("working_self_goal_links", []):
            if isinstance(goal, dict):
                goal["supporting_episode_refs"] = _dedupe(
                    _string_list(goal.get("supporting_episode_refs")) + live_trace_refs
                )
    if live_trace_refs and updated_relationship:
        we_memory = updated_relationship.setdefault("we_memory_traces", [])
        if isinstance(we_memory, list):
            we_memory.append(
                {
                    "trace_ref": live_trace_refs[0],
                    "dialogue_turn_refs": _string_list(dialogue_turn_refs),
                    "trace_kind": "live_dialogue_episode",
                }
            )
    return {
        "engram_index": updated_engram,
        "autobiographical_stack": updated_autobiographical,
        "relationship_memory": updated_relationship,
        "live_trace_refs": live_trace_refs,
        "live_trace_ids": live_trace_ids,
    }


def _utterance_digest(utterance: str, *, limit: int = 120) -> str:
    normalized = " ".join(utterance.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def _live_episode_content_summary(
    *,
    semantic_focus: str,
    expression_outcome: str,
    external_utterance: str,
    life_response: str,
) -> str:
    utterance_hint = _utterance_digest(external_utterance, limit=48) or "relation_turn"
    response_hint = _utterance_digest(life_response, limit=48)
    parts = [
        f"Live relation episode centered on {semantic_focus}",
        f"after external turn '{utterance_hint}'",
        f"with expression outcome {expression_outcome}",
    ]
    if response_hint:
        parts.append(f"and life response '{response_hint}'")
    return " ".join(parts) + "."


def _merge_prior_live_traces(
    traces: list[dict[str, Any]],
    *,
    existing_memory_trace_store: dict[str, Any] | None,
    new_live_traces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not existing_memory_trace_store:
        return traces
    new_dialogue_refs = {
        str(trace.get("dialogue_turn_ref"))
        for trace in new_live_traces
        if trace.get("dialogue_turn_ref")
    }
    prior_live = [
        trace
        for trace in existing_memory_trace_store.get("traces", [])
        if isinstance(trace, dict)
        and trace.get("live_trace_origin") == "live_dialogue_turn"
        and str(trace.get("dialogue_turn_ref") or "") not in new_dialogue_refs
    ]
    if not prior_live:
        return traces
    merged = list(traces)
    existing_ids = {
        str(trace.get("trace_id"))
        for trace in merged
        if trace.get("trace_id")
    }
    for trace in prior_live:
        trace_id = str(trace.get("trace_id") or "")
        if trace_id and trace_id in existing_ids:
            continue
        merged.append(trace)
        if trace_id:
            existing_ids.add(trace_id)
    return merged


def _select_reconsolidation_target_trace(
    live_traces: list[dict[str, Any]],
    *,
    event_type: str,
    exclude_dialogue_turn_ref: str | None,
) -> dict[str, Any] | None:
    if not live_traces:
        return None
    if event_type == "correction" and exclude_dialogue_turn_ref:
        candidates = [
            trace
            for trace in live_traces
            if str(trace.get("dialogue_turn_ref") or "") != exclude_dialogue_turn_ref
        ]
        return candidates[-1] if candidates else live_traces[-1]
    return live_traces[-1]


def _dedupe_traces_by_trace_id(traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for trace in traces:
        trace_id = str(trace.get("trace_id") or "")
        if trace_id and trace_id in seen:
            continue
        if trace_id:
            seen.add(trace_id)
        result.append(trace)
    return result


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
    extra_fields: dict[str, Any] | None = None,
) -> dict[str, Any]:
    trace_seed = "|".join(
        [run_id, memory_kind, event_boundary] + source_evidence_refs[:4]
    )
    trace_id = f"memory-trace-{_short_hash(trace_seed)}"
    payload = {
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
    if extra_fields:
        for key, value in extra_fields.items():
            if value is not None:
                payload[key] = value
        if extra_fields.get("content_summary"):
            payload["content_summary"] = extra_fields["content_summary"]
    return payload


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
