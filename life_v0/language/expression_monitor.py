from __future__ import annotations

from typing import Any


def build_expression_monitor_state(
    *,
    run_id: str,
    generated_at: str,
    source_doc_refs: list[str],
    cross_scope_risk_terms: list[str] | None = None,
    ambiguity_queue: list[str] | None = None,
) -> dict[str, object]:
    return {
        "schema_version": "expression_monitor_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "monitor_dimensions": [
            "semantic_coherence",
            "relationship_consequence",
            "commitment_trace",
            "dream_fact",
            "action_consequence",
        ],
        "blocked_language": ["subordinate_object", "service_object", "task_requester"],
        "cross_scope_risk_terms": list(cross_scope_risk_terms or []),
        "ambiguity_queue": list(ambiguity_queue or []),
        "source_doc_refs": source_doc_refs,
    }


def build_expression_plan(
    *,
    run_id: str,
    generated_at: str,
    inner_speech: dict[str, Any],
    semantic_map: dict[str, Any],
    language_percept: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    ambiguity_flags = list(language_percept.get("ambiguity_flags", []))
    cross_scope_risks = list(language_percept.get("cross_scope_risk_terms", []))
    repair_triggers = list(language_percept.get("repair_trigger_candidates", []))
    commitment_triggers = list(language_percept.get("commitment_trigger_candidates", []))
    replay_cue_targets = list((replay_cue_bundle or {}).get("anti_forgetting_targets", []))
    dream_window_refs = list((offline_consolidation_frame or {}).get("dream_window_refs", []))
    growth_candidates = list((growth_patch_candidate_queue or {}).get("candidates", []))

    expression_risk_flags = ambiguity_flags + cross_scope_risks
    if repair_triggers:
        expression_risk_flags.append("repair_pressure_present")
    if commitment_triggers:
        expression_risk_flags.append("commitment_trace_present")
    if commitment_repair_index.get("repair_obligation_refs") or commitment_repair_index.get("responsibility_trace_refs"):
        expression_risk_flags.append("responsibility_repair_language_pressure_present")
    if replay_cue_targets:
        expression_risk_flags.append("offline_replay_pressure_present")
    if dream_window_refs:
        expression_risk_flags.append("dream_integration_pressure_present")
    if growth_candidates:
        expression_risk_flags.append("growth_candidate_pressure_present")

    return {
        "schema_version": "expression_plan_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "expression_plan_id": f"expression-plan-{run_id}",
        "inner_speech_ref": "runtime/state/language/inner_speech_frame.json",
        "semantic_goal": semantic_map.get("semantic_focus"),
        "expression_risk_flags": expression_risk_flags,
        "repair_pressure": len(repair_triggers) + len(commitment_repair_index.get("repair_obligation_refs", [])),
        "responsibility_pressure": len(commitment_repair_index.get("commitment_refs", []))
        + len(commitment_repair_index.get("responsibility_trace_refs", [])),
        "replay_cue_pressure": len(replay_cue_targets),
        "dream_integration_pressure": len(dream_window_refs),
        "growth_candidate_pressure": len(growth_candidates),
        "delay_or_release_decision": (
            "delay_for_clarification"
            if ambiguity_flags
            else "release_guarded_expression"
        ),
        "shared_term_refs": list(language_percept.get("shared_term_hits", [])),
        "offline_influence_refs": [
            ref
            for ref, present in [
                ("runtime/state/replay/replay_cue_bundle.json", bool(replay_cue_targets)),
                ("runtime/state/dream/offline_consolidation_frame.json", bool(dream_window_refs)),
                ("runtime/state/growth/growth_patch_candidate_queue.json", bool(growth_candidates)),
            ]
            if present
        ],
        "source_doc_refs": source_doc_refs,
        "semantic_map_ref": inner_speech.get("semantic_map_ref"),
    }
