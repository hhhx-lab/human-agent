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
    core_affect_vector: dict[str, Any] | None = None,
) -> dict[str, Any]:
    belief_state = belief_state or {}
    active_sampling_plan = active_sampling_plan or {}
    core_affect_vector = core_affect_vector or {}
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
    utterance_signals = _classify_utterance_signals(incoming_surface, lowered_surface)

    commitment_trigger_candidates = []
    if utterance_signals["commitment_request"]:
        commitment_trigger_candidates.append("commitment-v0-0001")

    repair_trigger_candidates = []
    if utterance_signals["repair_request"] or utterance_signals["apology"]:
        repair_trigger_candidates.append("repair-language-v0-0001")

    dream_signal_candidates = []
    if "梦" in incoming_surface or "dream" in lowered_surface:
        dream_signal_candidates.append("dream-topic-v0-0001")

    affective_cue_candidates = []
    if any(token in incoming_surface for token in ["后悔", "难过", "痛苦", "生气", "开心"]):
        affective_cue_candidates.append("affective-cue-keyword-v0-0001")
    core_affect_cues = _affective_cues_from_core_affect(core_affect_vector)
    affective_cue_candidates.extend(core_affect_cues)
    affective_cue_candidates = _dedupe(affective_cue_candidates)

    blocked_terms = set(active_scope.get("blocked_cross_scope_terms", []))
    cross_scope_risk_terms = [term for term in blocked_terms if term in incoming_surface]

    ambiguity_flags = ["待确认关系语义细节"]
    if not shared_term_hits:
        ambiguity_flags.append("shared_term_unresolved")
    if speaker_role != active_scope.get("relation_role"):
        ambiguity_flags.append("relation_role_mismatch")
    if utterance_signals["clarification_request"]:
        ambiguity_flags.append("clarification_requested")
    if utterance_signals["relation_recalibration"]:
        ambiguity_flags.append("relation_scope_recalibration_requested")

    active_sampling_targets = list(active_sampling_plan.get("expected_observation_refs", []))
    active_sampling_scopes = list(active_sampling_plan.get("scope_refs", []))
    scene_tags = [
        tag
        for tag, active in utterance_signals.items()
        if active and tag not in {"commitment_request", "repair_request"}
    ]
    percept_focus_trace = _dedupe(
        [
            *active_sampling_targets,
            *active_sampling_scopes,
            *belief_state.get("source_evidence_refs", []),
            *[f"percept-scene-{tag}" for tag in scene_tags],
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
        "utterance_signal_profile": {
            "schema_version": "utterance_signal_profile_v0",
            **utterance_signals,
        },
        "core_affect_vector_ref": (
            "runtime/state/body/core_affect_vector.json"
            if core_affect_vector
            else None
        ),
        "core_affect_consumption_profile": (
            {
                "schema_version": "percept_core_affect_consumption_v0",
                "affective_cue_source": (
                    "core_affect_vector"
                    if core_affect_cues
                    else "keyword_only"
                ),
                "core_affect_cue_ids": core_affect_cues,
                "valence": core_affect_vector.get("valence"),
                "arousal": core_affect_vector.get("arousal"),
                "pain_pressure": core_affect_vector.get("pain_pressure"),
                "relationship_tension": core_affect_vector.get("relationship_tension"),
                "repair_drive": core_affect_vector.get("repair_drive"),
                "percept_core_affect_boundary": (
                    "structured_percept_affect_not_spoken_emotion"
                ),
            }
            if core_affect_vector
            else None
        ),
        "source_doc_refs": source_doc_refs,
    }


def _affective_cues_from_core_affect(
    core_affect_vector: dict[str, Any],
) -> list[str]:
    if not core_affect_vector:
        return []
    cues: list[str] = []
    pain_pressure = core_affect_vector.get("pain_pressure")
    if isinstance(pain_pressure, str) and pain_pressure not in {"low", "none", ""}:
        cues.append("affective-cue-core-pain-pressure")
    relationship_tension = core_affect_vector.get("relationship_tension")
    if isinstance(relationship_tension, (int, float)) and relationship_tension >= 0.55:
        cues.append("affective-cue-core-relationship-tension")
    repair_drive = core_affect_vector.get("repair_drive")
    if isinstance(repair_drive, (int, float)) and repair_drive >= 0.55:
        cues.append("affective-cue-core-repair-drive")
    valence = core_affect_vector.get("valence")
    if isinstance(valence, (int, float)):
        if valence <= 0.35:
            cues.append("affective-cue-core-negative-valence")
        elif valence >= 0.65:
            cues.append("affective-cue-core-positive-valence")
    arousal = core_affect_vector.get("arousal")
    if isinstance(arousal, (int, float)) and arousal >= 0.7:
        cues.append("affective-cue-core-high-arousal")
    return cues


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def _classify_utterance_signals(
    incoming_surface: str,
    lowered_surface: str,
) -> dict[str, bool]:
    return {
        "commitment_request": any(
            token in incoming_surface
            for token in ("承诺", "说好", "答应", "保证")
        )
        or "promise" in lowered_surface,
        "repair_request": any(
            token in incoming_surface for token in ("修复", "补救", "弥补")
        )
        or "repair" in lowered_surface,
        "apology": "道歉" in incoming_surface or "sorry" in lowered_surface,
        "clarification_request": any(
            token in incoming_surface
            for token in ("什么意思", "说清楚", "不明白", "解释一下", "你没懂")
        ),
        "boundary_declaration": any(
            token in incoming_surface
            for token in ("边界", "不要这样", "越界", "别再", "停一下")
        ),
        "relation_recalibration": any(
            token in incoming_surface
            for token in ("当成用户", "把我当用户", "用户了吗", "服务对象", "任务请求者")
        ),
    }
