from __future__ import annotations

from typing import Any


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
    return updated


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
