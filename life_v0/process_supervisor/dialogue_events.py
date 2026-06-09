from __future__ import annotations

from typing import Any


def build_external_turn_event(
    *,
    turn_id: str,
    generated_at: str,
    utterance: str,
    shared_term_registry: dict[str, Any],
    commitment_index: dict[str, Any],
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
) -> dict[str, Any]:
    event = {
        "schema_version": "dialogue_turn_event_v0",
        "turn_id": turn_id,
        "generated_at": generated_at,
        "event_role": "external_relation_turn",
        "relation_role": "friend",
        "utterance": utterance,
        "shared_term_refs": shared_term_refs(shared_term_registry),
        "commitment_refs": list(commitment_index.get("commitment_refs", [])),
        "expression_monitor_ref": "runtime/state/language/expression_monitor_state.json",
        "narrative_trace_ref": "runtime/state/language/self_narrative_language_trace.json",
    }
    _attach_queue_e_refs(
        event=event,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
    )
    return event


def build_life_turn_event(
    *,
    turn_id: str,
    generated_at: str,
    utterance: str,
    shared_term_registry: dict[str, Any],
    commitment_index: dict[str, Any],
    responsibility_loop_state_ref: str | None = None,
    world_contact_summary_ref: str | None = None,
    pain_regret_repair_report_ref: str | None = None,
) -> dict[str, Any]:
    event = {
        "schema_version": "dialogue_turn_event_v0",
        "turn_id": turn_id,
        "generated_at": generated_at,
        "event_role": "digital_life_turn",
        "relation_role": "friend",
        "utterance": utterance,
        "shared_term_refs": shared_term_refs(shared_term_registry),
        "commitment_refs": list(commitment_index.get("commitment_refs", [])),
        "expression_monitor_ref": "runtime/state/language/expression_monitor_state.json",
        "narrative_trace_ref": "runtime/state/language/self_narrative_language_trace.json",
    }
    _attach_queue_e_refs(
        event=event,
        responsibility_loop_state_ref=responsibility_loop_state_ref,
        world_contact_summary_ref=world_contact_summary_ref,
        pain_regret_repair_report_ref=pain_regret_repair_report_ref,
    )
    return event


def shared_term_refs(shared_term_registry: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for term in shared_term_registry.get("shared_terms", []):
        if isinstance(term, dict) and term.get("term_id"):
            refs.append(f"runtime/state/language/shared_term_registry.json#{term['term_id']}")
    return refs


def _attach_queue_e_refs(
    *,
    event: dict[str, Any],
    responsibility_loop_state_ref: str | None,
    world_contact_summary_ref: str | None,
    pain_regret_repair_report_ref: str | None,
) -> None:
    membrane_guard_refs = [
        ref
        for ref in [
            responsibility_loop_state_ref,
            world_contact_summary_ref,
            pain_regret_repair_report_ref,
        ]
        if ref
    ]
    if responsibility_loop_state_ref:
        event["responsibility_loop_ref"] = responsibility_loop_state_ref
    if world_contact_summary_ref:
        event["world_contact_summary_ref"] = world_contact_summary_ref
    if pain_regret_repair_report_ref:
        event["pain_regret_repair_report_ref"] = pain_regret_repair_report_ref
    if membrane_guard_refs:
        event["membrane_guard_refs"] = membrane_guard_refs
