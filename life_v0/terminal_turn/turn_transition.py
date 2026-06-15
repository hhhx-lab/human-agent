from __future__ import annotations

import json
from typing import Any

TURN_TRANSITION_TRACE_REF = "runtime/state/terminal/turn_transition_trace.json"
CONTEXT_ACCUMULATION_WINDOW_REF = (
    "runtime/state/terminal/context_accumulation_window.json"
)
WAITING_HEARTBEAT_REF = "runtime/reports/latest/digital_life_waiting_heartbeat.json"
LANGUAGE_PERCEPT_REF = "runtime/state/language/language_percept_frame.json"
SEMANTIC_MAP_REF = "runtime/state/language/semantic_map_frame.json"

SOURCE_DOC_REFS = [
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
    "docs/v0/process_contracts/first_terminal_turn_engineering_contract.md",
]


def build_relation_turn_frame(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    relation_subject_ref: str | None,
    relation_stage: str | None,
    shared_language_refs: list[str],
    commitment_truth_refs: list[str],
    last_contact_refs: list[str],
    boundary_state: str,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "relation_turn_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "relation_turn_id": f"relation-turn-{run_id}",
        "relation_subject_ref": relation_subject_ref,
        "relation_stage": relation_stage,
        "shared_language_refs": shared_language_refs,
        "commitment_truth_refs": commitment_truth_refs,
        "last_contact_refs": last_contact_refs,
        "boundary_state": boundary_state,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }


def build_turn_transition_trace(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    turn_stage: str,
    life_context_ref: str,
    relation_turn_ref: str,
    relation_scope_ref: str | None,
    expression_monitor_restore_refs: list[str],
    unresolved_commitment_refs: list[str],
    context_accumulation_restore_refs: list[str],
    language_percept_restore_refs: list[str],
    semantic_map_restore_refs: list[str],
    waiting_heartbeat_ref: str,
    next_required_action: str,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "turn_transition_trace_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "transition_kind": "birth_restore_to_first_terminal_turn",
        "from_stage": "ready_for_first_terminal_turn",
        "to_stage": turn_stage,
        "turn_transition_chain": [
            "waiting_heartbeat",
            "restore_identity_and_commitments",
            "listening_state",
            "inner_speech_draft",
            "expression_monitoring",
            "utterance_release",
            "responsibility_relation_writeback",
        ],
        "life_context_ref": life_context_ref,
        "relation_turn_ref": relation_turn_ref,
        "context_accumulation_ref": "runtime/state/terminal/context_accumulation_window.json",
        "context_accumulation_restore_refs": context_accumulation_restore_refs,
        "session_envelope_ref": "runtime/state/terminal/session_envelope.json",
        "safe_terminal_loop_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "relation_scope_ref": relation_scope_ref,
        "expression_monitor_restore_refs": expression_monitor_restore_refs,
        "language_percept_restore_refs": language_percept_restore_refs,
        "semantic_map_restore_refs": semantic_map_restore_refs,
        "unresolved_commitment_refs": unresolved_commitment_refs,
        "waiting_heartbeat_ref": waiting_heartbeat_ref,
        "next_required_action": next_required_action,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }


def project_turn_transition_trace_from_live_turn(
    *,
    turn_transition: dict[str, Any],
    generated_at: str,
    dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    live_turn_focus: str | None = None,
    semantic_focus: str | None = None,
    unresolved_commitment_refs: list[str] | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    updated = (
        json.loads(json.dumps(turn_transition)) if turn_transition else {}
    )
    if not updated:
        updated = build_turn_transition_trace(
            run_id=run_id or "resident-turn-writeback",
            generated_at=generated_at,
            status="closed",
            turn_stage="resumed_external_dialogue_loop",
            life_context_ref="runtime/state/terminal/life_context_frame.json",
            relation_turn_ref="runtime/state/terminal/relation_turn_frame.json",
            relation_scope_ref=None,
            expression_monitor_restore_refs=[
                "runtime/state/language/expression_monitor_state.json"
            ],
            unresolved_commitment_refs=list(unresolved_commitment_refs or []),
            context_accumulation_restore_refs=[CONTEXT_ACCUMULATION_WINDOW_REF],
            language_percept_restore_refs=[LANGUAGE_PERCEPT_REF],
            semantic_map_restore_refs=[SEMANTIC_MAP_REF],
            waiting_heartbeat_ref=WAITING_HEARTBEAT_REF,
            next_required_action="await_next_external_relation_turn",
            source_doc_refs=SOURCE_DOC_REFS,
            readme_block_refs=[],
            runtime_carrier_refs=[TURN_TRANSITION_TRACE_REF],
        )
    updated["generated_at"] = generated_at
    updated["status"] = "closed"
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["transition_kind"] = "live_relation_turn"
    updated["to_stage"] = "resumed_external_dialogue_loop"
    updated["context_accumulation_ref"] = CONTEXT_ACCUMULATION_WINDOW_REF
    updated["context_accumulation_restore_refs"] = _dedupe(
        list(updated.get("context_accumulation_restore_refs", []))
        + [CONTEXT_ACCUMULATION_WINDOW_REF]
    )
    updated["language_percept_restore_refs"] = _dedupe(
        list(updated.get("language_percept_restore_refs", []))
        + [LANGUAGE_PERCEPT_REF]
    )
    updated["semantic_map_restore_refs"] = _dedupe(
        list(updated.get("semantic_map_restore_refs", []))
        + [SEMANTIC_MAP_REF]
    )
    if unresolved_commitment_refs:
        updated["unresolved_commitment_refs"] = _dedupe(
            list(updated.get("unresolved_commitment_refs", []))
            + list(unresolved_commitment_refs)
        )
    if semantic_focus:
        updated["semantic_focus"] = semantic_focus
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", []))
        + list(dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    updated["runtime_carrier_refs"] = _dedupe(
        list(updated.get("runtime_carrier_refs", [])) + [TURN_TRANSITION_TRACE_REF]
    )
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    return updated


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
