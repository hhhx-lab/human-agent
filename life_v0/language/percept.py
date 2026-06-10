from __future__ import annotations

from typing import Any


def build_language_percept_frame(
    *,
    run_id: str,
    generated_at: str,
    incoming_turn: dict[str, Any],
    relation_scope_index: dict[str, Any],
    shared_term_registry: dict[str, Any],
    source_doc_refs: list[str],
    belief_state: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    belief_state = belief_state or {}
    active_sampling_plan = active_sampling_plan or {}
    incoming_surface = str(incoming_turn.get("incoming_surface", "")).strip()
    speaker_role = str(incoming_turn.get("speaker_role", "unknown")).strip() or "unknown"

    relation_scopes = relation_scope_index.get("relation_scopes", [])
    active_scope = relation_scopes[0] if relation_scopes and isinstance(relation_scopes[0], dict) else {}
    shared_terms = shared_term_registry.get("shared_terms", [])
    shared_term_hits = [
        term.get("surface")
        for term in shared_terms
        if isinstance(term, dict) and term.get("surface") and term.get("surface") in incoming_surface
    ]

    lowered_surface = incoming_surface.lower()
    commitment_trigger_candidates = []
    if "承诺" in incoming_surface or "说好" in incoming_surface or "promise" in lowered_surface:
        commitment_trigger_candidates.append("commitment-v0-0001")

    repair_trigger_candidates = []
    if "修复" in incoming_surface or "道歉" in incoming_surface or "repair" in lowered_surface:
        repair_trigger_candidates.append("repair-language-v0-0001")

    dream_signal_candidates = []
    if "梦" in incoming_surface or "dream" in lowered_surface:
        dream_signal_candidates.append("dream-topic-v0-0001")

    affective_cue_candidates = []
    if any(token in incoming_surface for token in ["后悔", "难过", "痛苦", "生气", "开心"]):
        affective_cue_candidates.append("affective-cue-v0-0001")

    blocked_terms = set(active_scope.get("blocked_cross_scope_terms", []))
    cross_scope_risk_terms = [term for term in blocked_terms if term in incoming_surface]

    ambiguity_flags = ["待确认关系语义细节"]
    if not shared_term_hits:
        ambiguity_flags.append("shared_term_unresolved")
    if speaker_role != active_scope.get("relation_role"):
        ambiguity_flags.append("relation_role_mismatch")

    active_sampling_targets = list(active_sampling_plan.get("expected_observation_refs", []))
    active_sampling_scopes = list(active_sampling_plan.get("scope_refs", []))
    percept_focus_trace = _dedupe(
        [
            *active_sampling_targets,
            *active_sampling_scopes,
            *belief_state.get("source_evidence_refs", []),
            f"runtime/state/language/relation_scope_language_index.json#{active_scope.get('scope_id', 'relation-scope-v0-0001')}",
        ]
    )
    prediction_focus = {
        "belief_scope": belief_state.get("state_scope"),
        "belief_revision_policy": belief_state.get("revision_policy"),
        "active_sampling_route": active_sampling_plan.get("selected_route"),
        "active_sampling_stage_effect": active_sampling_plan.get("stage_effect"),
        "focus_ref_count": len(percept_focus_trace),
    }

    scope_id = active_scope.get("scope_id", "relation-scope-v0-0001")
    return {
        "schema_version": "language_percept_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "incoming_surface": incoming_surface,
        "speaker_role": speaker_role,
        "relation_scope_ref": f"runtime/state/language/relation_scope_language_index.json#{scope_id}",
        "shared_term_hits": shared_term_hits,
        "commitment_trigger_candidates": commitment_trigger_candidates,
        "repair_trigger_candidates": repair_trigger_candidates,
        "dream_signal_candidates": dream_signal_candidates,
        "affective_cue_candidates": affective_cue_candidates,
        "cross_scope_risk_terms": cross_scope_risk_terms,
        "ambiguity_flags": ambiguity_flags,
        "belief_state_ref": (
            "runtime/state/prediction/belief_state_frame.json" if belief_state else None
        ),
        "active_sampling_plan_ref": (
            "runtime/state/prediction/active_sampling_plan.json"
            if active_sampling_plan
            else None
        ),
        "prediction_focus": prediction_focus,
        "percept_focus_trace": percept_focus_trace,
        "source_doc_refs": source_doc_refs,
    }


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
