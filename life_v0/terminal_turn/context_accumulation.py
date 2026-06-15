from __future__ import annotations

import json
from typing import Any

CONTEXT_ACCUMULATION_WINDOW_REF = (
    "runtime/state/terminal/context_accumulation_window.json"
)
WAITING_HEARTBEAT_REF = "runtime/reports/latest/digital_life_waiting_heartbeat.json"
LANGUAGE_PERCEPT_REF = "runtime/state/language/language_percept_frame.json"
SEMANTIC_MAP_REF = "runtime/state/language/semantic_map_frame.json"
EXPRESSION_MONITOR_REF = "runtime/state/language/expression_monitor_state.json"
RELATION_SCOPE_INDEX_REF = (
    "runtime/state/language/relation_scope_language_index.json"
)
SELF_NARRATIVE_TRACE_REF = (
    "runtime/state/language/self_narrative_language_trace.json"
)

SOURCE_DOC_REFS = [
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
    "docs/v0/process_contracts/first_terminal_turn_engineering_contract.md",
]


def build_life_context_frame(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    direction_refs: list[str],
    self_narrative_refs: list[str],
    relationship_refs: list[str],
    autobiographical_memory_refs: list[str],
    shared_terms_refs: list[str],
    commitment_refs: list[str],
    body_state_refs: list[str],
    prediction_seed_refs: list[str],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "life_context_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "life_context_id": f"life-context-{run_id}",
        "direction_refs": direction_refs,
        "self_narrative_refs": self_narrative_refs,
        "relationship_refs": relationship_refs,
        "autobiographical_memory_refs": autobiographical_memory_refs,
        "shared_terms_refs": shared_terms_refs,
        "commitment_refs": commitment_refs,
        "body_state_refs": body_state_refs,
        "prediction_seed_refs": prediction_seed_refs,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }


def build_context_accumulation_window(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    relation_subject: dict[str, Any],
    shared_term_surfaces: list[str],
    unresolved_commitments: list[str],
    expression_monitor: dict[str, Any],
    relation_scope_index: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    dialogue_turn_restore_refs: list[str],
    expression_monitor_restore_refs: list[str],
    relation_scope_restore_refs: list[str],
    self_narrative_restore_refs: list[str],
    language_percept_restore_refs: list[str],
    semantic_map_restore_refs: list[str],
    semantic_focus: str | None,
    waiting_heartbeat_ref: str,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
) -> dict[str, Any]:
    relation_scopes = relation_scope_index.get("relation_scopes", [])
    current_relation_scope = relation_scopes[0] if relation_scopes and isinstance(relation_scopes[0], dict) else {}

    return {
        "schema_version": "context_accumulation_window_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_relation_id": relation_subject.get("relationship_id"),
        "current_relation_role": relation_subject.get("relation_role"),
        "current_relationship_stage": relation_subject.get("relationship_stage"),
        "shared_term_surfaces": shared_term_surfaces,
        "unresolved_commitment_refs": unresolved_commitments,
        "expression_monitor_dimensions": list(expression_monitor.get("monitor_dimensions", [])),
        "expression_monitor_restore_refs": expression_monitor_restore_refs,
        "relation_scope_refs": [scope.get("scope_ref") for scope in relation_scopes if scope.get("scope_ref")],
        "relation_scope_restore_refs": relation_scope_restore_refs,
        "active_scope_id": current_relation_scope.get("scope_id"),
        "active_scope_label": current_relation_scope.get("scope_label"),
        "narrative_turn_refs": list(self_narrative_trace.get("narrative_turn_refs", [])),
        "self_narrative_restore_refs": self_narrative_restore_refs,
        "language_percept_restore_refs": language_percept_restore_refs,
        "semantic_map_restore_refs": semantic_map_restore_refs,
        "semantic_focus": semantic_focus,
        "dialogue_turn_restore_refs": dialogue_turn_restore_refs,
        "waiting_heartbeat_ref": waiting_heartbeat_ref,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }


def project_context_accumulation_window_from_live_turn(
    *,
    context_accumulation: dict[str, Any],
    generated_at: str,
    relationship_graph: dict[str, Any],
    language_percept: dict[str, Any] | None = None,
    semantic_map: dict[str, Any] | None = None,
    expression_monitor: dict[str, Any] | None = None,
    relation_scope_index: dict[str, Any] | None = None,
    self_narrative_trace: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    live_turn_focus: str | None = None,
    run_id: str | None = None,
    waiting_heartbeat_ref: str | None = None,
) -> dict[str, Any]:
    language_percept = language_percept or {}
    semantic_map = semantic_map or {}
    expression_monitor = expression_monitor or {}
    relation_scope_index = relation_scope_index or {}
    self_narrative_trace = self_narrative_trace or {}
    commitment_truth_state = commitment_truth_state or {}
    updated = (
        json.loads(json.dumps(context_accumulation))
        if context_accumulation
        else {}
    )
    subjects = relationship_graph.get("subjects")
    relation_subject = (
        subjects[0] if isinstance(subjects, list) and subjects else {}
    )
    if not isinstance(relation_subject, dict):
        relation_subject = {}
    if not updated:
        updated = build_context_accumulation_window(
            run_id=run_id or "resident-turn-writeback",
            generated_at=generated_at,
            status="closed",
            relation_subject=relation_subject,
            shared_term_surfaces=_shared_term_surfaces(
                semantic_map=semantic_map,
                language_percept=language_percept,
            ),
            unresolved_commitments=_unresolved_commitment_refs(
                commitment_truth_state
            ),
            expression_monitor=expression_monitor,
            relation_scope_index=relation_scope_index,
            self_narrative_trace=self_narrative_trace,
            dialogue_turn_restore_refs=list(dialogue_turn_refs or []),
            expression_monitor_restore_refs=[EXPRESSION_MONITOR_REF],
            relation_scope_restore_refs=[RELATION_SCOPE_INDEX_REF],
            self_narrative_restore_refs=[SELF_NARRATIVE_TRACE_REF],
            language_percept_restore_refs=[LANGUAGE_PERCEPT_REF],
            semantic_map_restore_refs=[SEMANTIC_MAP_REF],
            semantic_focus=_semantic_focus(
                live_turn_focus=live_turn_focus,
                semantic_map=semantic_map,
                language_percept=language_percept,
            ),
            waiting_heartbeat_ref=waiting_heartbeat_ref or WAITING_HEARTBEAT_REF,
            source_doc_refs=SOURCE_DOC_REFS,
            readme_block_refs=[],
            runtime_carrier_refs=[CONTEXT_ACCUMULATION_WINDOW_REF],
        )
    updated["generated_at"] = generated_at
    updated["status"] = "closed"
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["current_relation_id"] = relation_subject.get("relationship_id")
    updated["current_relation_role"] = relation_subject.get("relation_role")
    updated["current_relationship_stage"] = relation_subject.get("relationship_stage")
    updated["shared_term_surfaces"] = _dedupe(
        list(updated.get("shared_term_surfaces", []))
        + _shared_term_surfaces(
            semantic_map=semantic_map,
            language_percept=language_percept,
        )
    )
    updated["unresolved_commitment_refs"] = _dedupe(
        list(updated.get("unresolved_commitment_refs", []))
        + _unresolved_commitment_refs(commitment_truth_state)
    )
    updated["expression_monitor_dimensions"] = list(
        expression_monitor.get("monitor_dimensions", [])
        or updated.get("expression_monitor_dimensions", [])
    )
    updated["expression_monitor_restore_refs"] = _dedupe(
        list(updated.get("expression_monitor_restore_refs", []))
        + [EXPRESSION_MONITOR_REF]
    )
    relation_scopes = relation_scope_index.get("relation_scopes", [])
    current_relation_scope = (
        relation_scopes[0]
        if isinstance(relation_scopes, list) and relation_scopes
        else {}
    )
    if not isinstance(current_relation_scope, dict):
        current_relation_scope = {}
    updated["relation_scope_refs"] = _dedupe(
        [
            scope.get("scope_ref")
            for scope in relation_scopes
            if isinstance(scope, dict) and scope.get("scope_ref")
        ]
        or list(updated.get("relation_scope_refs", []))
    )
    updated["relation_scope_restore_refs"] = _dedupe(
        list(updated.get("relation_scope_restore_refs", []))
        + [RELATION_SCOPE_INDEX_REF]
    )
    updated["active_scope_id"] = current_relation_scope.get("scope_id")
    updated["active_scope_label"] = current_relation_scope.get("scope_label")
    updated["narrative_turn_refs"] = _dedupe(
        list(updated.get("narrative_turn_refs", []))
        + list(self_narrative_trace.get("narrative_turn_refs", []))
    )
    updated["self_narrative_restore_refs"] = _dedupe(
        list(updated.get("self_narrative_restore_refs", []))
        + [SELF_NARRATIVE_TRACE_REF]
    )
    updated["language_percept_restore_refs"] = _dedupe(
        list(updated.get("language_percept_restore_refs", []))
        + [LANGUAGE_PERCEPT_REF]
    )
    updated["semantic_map_restore_refs"] = _dedupe(
        list(updated.get("semantic_map_restore_refs", []))
        + [SEMANTIC_MAP_REF]
    )
    updated["semantic_focus"] = _semantic_focus(
        live_turn_focus=live_turn_focus,
        semantic_map=semantic_map,
        language_percept=language_percept,
        existing=updated.get("semantic_focus"),
    )
    updated["dialogue_turn_restore_refs"] = _dedupe(
        list(updated.get("dialogue_turn_restore_refs", []))
        + list(dialogue_turn_refs or [])
    )
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", []))
        + list(dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    updated["waiting_heartbeat_ref"] = (
        waiting_heartbeat_ref or updated.get("waiting_heartbeat_ref") or WAITING_HEARTBEAT_REF
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    updated["runtime_carrier_refs"] = _dedupe(
        list(updated.get("runtime_carrier_refs", []))
        + [CONTEXT_ACCUMULATION_WINDOW_REF]
    )
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    return updated


def _shared_term_surfaces(
    *,
    semantic_map: dict[str, Any],
    language_percept: dict[str, Any],
) -> list[str]:
    surfaces: list[str] = []
    for binding in semantic_map.get("shared_meaning_bindings", []):
        if not isinstance(binding, dict):
            continue
        surface = binding.get("surface")
        if surface:
            surfaces.append(str(surface))
    for surface in language_percept.get("shared_term_hits", []):
        if surface:
            surfaces.append(str(surface))
    return _dedupe(surfaces)


def _unresolved_commitment_refs(commitment_truth_state: dict[str, Any]) -> list[str]:
    refs = list(commitment_truth_state.get("open_commitment_refs", []))
    refs.extend(commitment_truth_state.get("repair_required_refs", []))
    return _dedupe([str(ref) for ref in refs if ref])


def _semantic_focus(
    *,
    live_turn_focus: str | None,
    semantic_map: dict[str, Any],
    language_percept: dict[str, Any],
    existing: str | None = None,
) -> str | None:
    return (
        live_turn_focus
        or semantic_map.get("semantic_focus")
        or language_percept.get("semantic_focus")
        or existing
    )


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def project_context_accumulation_window_from_live_turn(
    *,
    context_accumulation: dict[str, Any],
    generated_at: str,
    relationship_graph: dict[str, Any],
    language_percept: dict[str, Any] | None = None,
    semantic_map: dict[str, Any] | None = None,
    expression_monitor: dict[str, Any] | None = None,
    relation_scope_index: dict[str, Any] | None = None,
    self_narrative_trace: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    live_turn_focus: str | None = None,
    run_id: str | None = None,
    waiting_heartbeat_ref: str | None = None,
) -> dict[str, Any]:
    language_percept = language_percept or {}
    semantic_map = semantic_map or {}
    expression_monitor = expression_monitor or {}
    relation_scope_index = relation_scope_index or {}
    self_narrative_trace = self_narrative_trace or {}
    commitment_truth_state = commitment_truth_state or {}
    updated = (
        json.loads(json.dumps(context_accumulation))
        if context_accumulation
        else {}
    )
    subjects = relationship_graph.get("subjects")
    relation_subject = (
        subjects[0] if isinstance(subjects, list) and subjects else {}
    )
    if not isinstance(relation_subject, dict):
        relation_subject = {}
    if not updated:
        updated = build_context_accumulation_window(
            run_id=run_id or "resident-turn-writeback",
            generated_at=generated_at,
            status="closed",
            relation_subject=relation_subject,
            shared_term_surfaces=_shared_term_surfaces(
                semantic_map=semantic_map,
                language_percept=language_percept,
            ),
            unresolved_commitments=_unresolved_commitment_refs(
                commitment_truth_state
            ),
            expression_monitor=expression_monitor,
            relation_scope_index=relation_scope_index,
            self_narrative_trace=self_narrative_trace,
            dialogue_turn_restore_refs=list(dialogue_turn_refs or []),
            expression_monitor_restore_refs=[EXPRESSION_MONITOR_REF],
            relation_scope_restore_refs=[RELATION_SCOPE_INDEX_REF],
            self_narrative_restore_refs=[SELF_NARRATIVE_TRACE_REF],
            language_percept_restore_refs=[LANGUAGE_PERCEPT_REF],
            semantic_map_restore_refs=[SEMANTIC_MAP_REF],
            semantic_focus=_semantic_focus(
                live_turn_focus=live_turn_focus,
                semantic_map=semantic_map,
                language_percept=language_percept,
            ),
            waiting_heartbeat_ref=waiting_heartbeat_ref or WAITING_HEARTBEAT_REF,
            source_doc_refs=SOURCE_DOC_REFS,
            readme_block_refs=[],
            runtime_carrier_refs=[CONTEXT_ACCUMULATION_WINDOW_REF],
        )
    updated["generated_at"] = generated_at
    updated["status"] = "closed"
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["current_relation_id"] = relation_subject.get("relationship_id")
    updated["current_relation_role"] = relation_subject.get("relation_role")
    updated["current_relationship_stage"] = relation_subject.get("relationship_stage")
    updated["shared_term_surfaces"] = _dedupe(
        list(updated.get("shared_term_surfaces", []))
        + _shared_term_surfaces(
            semantic_map=semantic_map,
            language_percept=language_percept,
        )
    )
    updated["unresolved_commitment_refs"] = _dedupe(
        list(updated.get("unresolved_commitment_refs", []))
        + _unresolved_commitment_refs(commitment_truth_state)
    )
    updated["expression_monitor_dimensions"] = list(
        expression_monitor.get("monitor_dimensions", [])
        or updated.get("expression_monitor_dimensions", [])
    )
    updated["expression_monitor_restore_refs"] = _dedupe(
        list(updated.get("expression_monitor_restore_refs", []))
        + [EXPRESSION_MONITOR_REF]
    )
    relation_scopes = relation_scope_index.get("relation_scopes", [])
    current_relation_scope = (
        relation_scopes[0]
        if isinstance(relation_scopes, list) and relation_scopes
        else {}
    )
    if not isinstance(current_relation_scope, dict):
        current_relation_scope = {}
    updated["relation_scope_refs"] = _dedupe(
        [
            scope.get("scope_ref")
            for scope in relation_scopes
            if isinstance(scope, dict) and scope.get("scope_ref")
        ]
        or list(updated.get("relation_scope_refs", []))
    )
    updated["relation_scope_restore_refs"] = _dedupe(
        list(updated.get("relation_scope_restore_refs", []))
        + [RELATION_SCOPE_INDEX_REF]
    )
    updated["active_scope_id"] = current_relation_scope.get("scope_id")
    updated["active_scope_label"] = current_relation_scope.get("scope_label")
    updated["narrative_turn_refs"] = _dedupe(
        list(updated.get("narrative_turn_refs", []))
        + list(self_narrative_trace.get("narrative_turn_refs", []))
    )
    updated["self_narrative_restore_refs"] = _dedupe(
        list(updated.get("self_narrative_restore_refs", []))
        + [SELF_NARRATIVE_TRACE_REF]
    )
    updated["language_percept_restore_refs"] = _dedupe(
        list(updated.get("language_percept_restore_refs", []))
        + [LANGUAGE_PERCEPT_REF]
    )
    updated["semantic_map_restore_refs"] = _dedupe(
        list(updated.get("semantic_map_restore_refs", []))
        + [SEMANTIC_MAP_REF]
    )
    updated["semantic_focus"] = _semantic_focus(
        live_turn_focus=live_turn_focus,
        semantic_map=semantic_map,
        language_percept=language_percept,
        existing=updated.get("semantic_focus"),
    )
    updated["dialogue_turn_restore_refs"] = _dedupe(
        list(updated.get("dialogue_turn_restore_refs", []))
        + list(dialogue_turn_refs or [])
    )
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", []))
        + list(dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    updated["waiting_heartbeat_ref"] = (
        waiting_heartbeat_ref or updated.get("waiting_heartbeat_ref") or WAITING_HEARTBEAT_REF
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    updated["runtime_carrier_refs"] = _dedupe(
        list(updated.get("runtime_carrier_refs", []))
        + [CONTEXT_ACCUMULATION_WINDOW_REF]
    )
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    return updated


def _shared_term_surfaces(
    *,
    semantic_map: dict[str, Any],
    language_percept: dict[str, Any],
) -> list[str]:
    surfaces: list[str] = []
    for binding in semantic_map.get("shared_meaning_bindings", []):
        if not isinstance(binding, dict):
            continue
        surface = binding.get("surface")
        if surface:
            surfaces.append(str(surface))
    for surface in language_percept.get("shared_term_hits", []):
        if surface:
            surfaces.append(str(surface))
    return _dedupe(surfaces)


def _unresolved_commitment_refs(commitment_truth_state: dict[str, Any]) -> list[str]:
    refs = list(commitment_truth_state.get("open_commitment_refs", []))
    refs.extend(commitment_truth_state.get("repair_required_refs", []))
    return _dedupe([str(ref) for ref in refs if ref])


def _semantic_focus(
    *,
    live_turn_focus: str | None,
    semantic_map: dict[str, Any],
    language_percept: dict[str, Any],
    existing: str | None = None,
) -> str | None:
    return (
        live_turn_focus
        or semantic_map.get("semantic_focus")
        or language_percept.get("semantic_focus")
        or existing
    )


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
