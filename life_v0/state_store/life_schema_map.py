from __future__ import annotations

from typing import Any


MIN_SCHEMA_PROMOTION_TURN_COUNT = 21
MIN_SCHEMA_EVIDENCE_COUNT = 3

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/29_memory_validator_rules.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "docs/v0/entry/v0_memory_module_rebuild_plan.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_life_schema_map(
    *,
    run_id: str,
    generated_at: str,
    memory_trace_store: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    memory_trace_store = memory_trace_store or {}
    memory_retrieval_frame = memory_retrieval_frame or {}
    relationship_memory = relationship_memory or {}
    autobiographical_stack = autobiographical_stack or {}
    self_model_state = self_model_state or {}
    responsibility_ledger = responsibility_ledger or {}

    schemas = [
        _schema(
            run_id=run_id,
            schema_kind="self_schema",
            source_refs=_dedupe(
                _string_list((autobiographical_stack or {}).get("anchor_refs"))
                + _string_list((self_model_state or {}).get("old_self_anchor_refs"))
                + ["runtime/state/self/self_model.json"]
            ),
            trace_refs=_string_list((memory_trace_store or {}).get("trace_ids"))[:8],
            output_focus="self_continuity_and_growth",
            integration_mode="self_narrative_and_trait_slow_variables",
        ),
        _schema(
            run_id=run_id,
            schema_kind="relationship_schema",
            source_refs=_dedupe(
                _string_list((relationship_memory or {}).get("shared_memory_refs"))
                + _string_list((relationship_memory or {}).get("timeline_refs"))
                + ["runtime/state/memory/relationship_memory.json"]
            ),
            trace_refs=_trace_refs_by_kind(memory_trace_store, ("relationship",))[:8],
            output_focus="relationship_continuity_and_repair",
            integration_mode="shared_language_and_commitment_truth",
        ),
        _schema(
            run_id=run_id,
            schema_kind="task_schema",
            source_refs=_dedupe(
                _string_list((memory_retrieval_frame or {}).get("cue_terms"))
                + _string_list((memory_retrieval_frame or {}).get("activated_engram_refs"))
                + ["runtime/state/memory/memory_retrieval_frame.json"]
            ),
            trace_refs=_trace_refs_by_kind(memory_trace_store, ("episodic", "procedural"))[:8],
            output_focus="future_task_action_and_repair_path",
            integration_mode="workflow_and_action_gate",
        ),
        _schema(
            run_id=run_id,
            schema_kind="body_recovery_schema",
            source_refs=_dedupe(
                _string_list((memory_retrieval_frame or {}).get("dream_residue_hits"))
                + _string_list((memory_retrieval_frame or {}).get("responsibility_hits"))
                + ["runtime/state/body/core_affect_vector.json"]
            ),
            trace_refs=_trace_refs_by_kind(memory_trace_store, ("value",))[:8],
            output_focus="restoration_and_load_shedding",
            integration_mode="fatigue_and_dream_reconsolidation",
        ),
        _schema(
            run_id=run_id,
            schema_kind="responsibility_schema",
            source_refs=_dedupe(
                _string_list((responsibility_ledger or {}).get("responsibility_event_refs"))
                + _string_list((relationship_memory or {}).get("responsibility_event_refs"))
                + ["runtime/state/responsibility/responsibility_ledger.json"]
            ),
            trace_refs=_trace_refs_by_kind(memory_trace_store, ("value", "self_narrative"))[:8],
            output_focus="repair_obligation_and_future_constraint",
            integration_mode="value_and_self_narrative_governance",
        ),
    ]

    schemas = [schema for schema in schemas if schema["source_refs"] or schema["trace_refs"]]
    schema_kinds = [schema["schema_kind"] for schema in schemas]
    schema_refs = [schema["schema_ref"] for schema in schemas]
    return {
        "schema_version": "life_schema_map_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "schema_map_ref": "runtime/state/memory/life_schema_map.json",
        "schema_kinds": schema_kinds,
        "schema_refs": schema_refs,
        "schemas": schemas,
        "dominant_schema_kind": schema_kinds[0] if schema_kinds else None,
        "dominant_schema_focus": schemas[0]["output_focus"] if schemas else None,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_life_schema_map_from_live_turn(
    *,
    life_schema_map: dict[str, Any] | None,
    generated_at: str,
    run_id: str | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    memory_longitudinal_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current = dict(life_schema_map or {})
    updated = build_life_schema_map(
        run_id=run_id or str(current.get("run_id") or "life-schema-map"),
        generated_at=generated_at,
        memory_trace_store=memory_trace_store,
        memory_retrieval_frame=memory_retrieval_frame,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        self_model_state=self_model_state,
        responsibility_ledger=responsibility_ledger,
    )
    if current.get("schema_kinds"):
        updated["previous_schema_kinds"] = _dedupe(
            _string_list(current.get("schema_kinds"))
            + _string_list(current.get("previous_schema_kinds"))
        )
    live_trace_refs = _live_episode_trace_refs(memory_trace_store)
    schema_evidence_counts = _schema_evidence_counts(
        schemas=updated.get("schemas", []),
        live_trace_refs=live_trace_refs,
        memory_trace_store=memory_trace_store,
    )
    updated["schema_evidence_counts"] = schema_evidence_counts
    turn_count = int((memory_longitudinal_profile or {}).get("turn_count") or 0)
    updated["schema_promotion_turn_count"] = turn_count
    updated["schema_promotion_policy"] = "multi_week_evidence_not_count_only"
    promoted_schemas: list[str] = []
    for schema in updated.get("schemas", []):
        if not isinstance(schema, dict):
            continue
        schema_id = str(schema.get("schema_id") or "")
        evidence_count = int(schema_evidence_counts.get(schema_id, 0))
        schema["schema_evidence_count"] = evidence_count
        eligible, eligibility_reason = _schema_promotion_eligible(
            schema=schema,
            evidence_count=evidence_count,
            turn_count=turn_count,
            memory_trace_store=memory_trace_store,
        )
        schema["promotion_eligibility_reason"] = eligibility_reason
        if eligible:
            schema["last_promoted_at"] = generated_at
            schema["promotion_status"] = "schema_candidate_promoted"
            promoted_schemas.append(schema_id)
        else:
            schema.setdefault("promotion_status", "accumulating_evidence")
    if promoted_schemas:
        updated["last_promoted_at"] = generated_at
        updated["last_promoted_schema_ids"] = promoted_schemas
    return updated


def _schema_promotion_eligible(
    *,
    schema: dict[str, Any],
    evidence_count: int,
    turn_count: int,
    memory_trace_store: dict[str, Any] | None,
) -> tuple[bool, str]:
    if evidence_count < MIN_SCHEMA_EVIDENCE_COUNT:
        return False, "insufficient_schema_evidence_count"
    if turn_count < MIN_SCHEMA_PROMOTION_TURN_COUNT:
        return False, "insufficient_multiweek_turn_span"
    focus = str(schema.get("output_focus") or "")
    if not focus:
        return False, "missing_schema_output_focus"
    cluster_hits = _semantic_cluster_hit_count(
        focus=focus,
        memory_trace_store=memory_trace_store,
    )
    if cluster_hits < 2:
        return False, "insufficient_semantic_cluster_repetition"
    return True, "multiweek_evidence_threshold_met"


def _semantic_cluster_hit_count(
    *,
    focus: str,
    memory_trace_store: dict[str, Any] | None,
) -> int:
    hits = 0
    for trace in (memory_trace_store or {}).get("traces", []):
        if not isinstance(trace, dict):
            continue
        if trace.get("live_trace_origin") != "live_dialogue_turn":
            continue
        if trace.get("lifecycle_state") == "deprecated":
            continue
        semantic_focus = str(trace.get("semantic_focus") or "")
        content_summary = str(trace.get("content_summary") or "")
        if focus in semantic_focus or focus in content_summary:
            hits += 1
    return hits


def _live_episode_trace_refs(memory_trace_store: dict[str, Any] | None) -> list[str]:
    refs: list[str] = []
    for trace in (memory_trace_store or {}).get("traces", []):
        if not isinstance(trace, dict):
            continue
        if trace.get("live_trace_origin") != "live_dialogue_turn":
            continue
        if trace.get("lifecycle_state") == "deprecated":
            continue
        trace_id = trace.get("trace_id")
        if trace_id:
            refs.append(
                f"runtime/state/memory/memory_trace_store.json#trace:{trace_id}"
            )
    return _dedupe(refs)


def _schema_evidence_counts(
    *,
    schemas: list[Any],
    live_trace_refs: list[str],
    memory_trace_store: dict[str, Any] | None,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    live_traces = [
        trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict)
        and trace.get("live_trace_origin") == "live_dialogue_turn"
    ]
    for schema in schemas:
        if not isinstance(schema, dict):
            continue
        schema_id = str(schema.get("schema_id") or "")
        if not schema_id:
            continue
        trace_refs = _dedupe(
            _string_list(schema.get("trace_refs")) + live_trace_refs
        )
        counts[schema_id] = len(trace_refs)
        focus = str(schema.get("output_focus") or "")
        if focus:
            focus_hits = sum(
                1
                for trace in live_traces
                if focus in str(trace.get("semantic_focus") or "")
                or focus in str(trace.get("content_summary") or "")
            )
            counts[schema_id] = max(counts[schema_id], focus_hits)
    return counts


def _schema(
    *,
    run_id: str,
    schema_kind: str,
    source_refs: list[str],
    trace_refs: list[str],
    output_focus: str,
    integration_mode: str,
) -> dict[str, Any]:
    schema_id = f"life-schema-{schema_kind}-{_short_hash('|'.join([run_id, schema_kind] + source_refs[:4]))}"
    return {
        "schema_id": schema_id,
        "schema_kind": schema_kind,
        "schema_ref": f"runtime/state/memory/life_schema_map.json#schema:{schema_id}",
        "source_refs": _dedupe(source_refs),
        "trace_refs": _dedupe(trace_refs),
        "output_focus": output_focus,
        "integration_mode": integration_mode,
        "write_policy": "confirm_required" if schema_kind in {"relationship_schema", "self_schema", "responsibility_schema"} else "auto_candidate",
    }


def _trace_refs_by_kind(memory_trace_store: dict[str, Any], kinds: tuple[str, ...]) -> list[str]:
    refs: list[str] = []
    for trace in memory_trace_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        if str(trace.get("memory_kind")) in kinds and trace.get("trace_id"):
            refs.append(f"runtime/state/memory/memory_trace_store.json#trace:{trace['trace_id']}")
    return _dedupe(refs)


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
    import hashlib

    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
