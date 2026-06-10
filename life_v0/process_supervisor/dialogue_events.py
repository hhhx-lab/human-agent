from __future__ import annotations

from typing import Any


BACKGROUND_TRAIT_CONVERGENCE_REF_KEYS = (
    "background_resident_governance_state_ref",
    "background_resident_governance_explanation_ref",
    "background_trait_drift_monitor_ref",
    "background_convergence_summary_ref",
    "background_convergence_history_ref",
)


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
    terminal_life_loop_state: dict[str, Any] | None = None,
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
    event.update(build_background_trait_convergence_payload(terminal_life_loop_state))
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


def build_background_trait_convergence_payload(
    terminal_life_loop_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not terminal_life_loop_state:
        return {}

    payload: dict[str, Any] = {}
    evidence_refs: list[str] = []
    for key in BACKGROUND_TRAIT_CONVERGENCE_REF_KEYS:
        value = terminal_life_loop_state.get(key)
        if isinstance(value, str) and value:
            payload[key] = value
            evidence_refs.append(value)

    focus = terminal_life_loop_state.get("background_trait_convergence_history_focus")
    if isinstance(focus, str) and focus:
        payload["background_trait_convergence_history_focus"] = focus

    for key in (
        "background_trait_convergence_unstable_names",
        "background_trait_convergence_stable_names",
    ):
        names = _string_list(terminal_life_loop_state.get(key))
        if names:
            payload[key] = names

    profile = terminal_life_loop_state.get("background_trait_convergence_history_profile")
    if isinstance(profile, dict) and profile:
        payload["background_trait_convergence_history_profile"] = dict(profile)

    if evidence_refs:
        payload["background_trait_convergence_evidence_refs"] = evidence_refs
    return payload


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]
