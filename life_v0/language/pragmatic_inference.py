from __future__ import annotations

import json
from typing import Any

PRAGMATIC_INFERENCE_BOUNDARY = (
    "structured_pragmatic_inference_not_spoken_response"
)

_CORRECTION_MARKERS = (
    "记错",
    "记错了",
    "不对",
    "纠正",
    "你搞错",
    "不是这样",
    "没发生过",
    "你记反",
)
_CONFIRMATION_MARKERS = (
    "没错",
    "对的",
    "就是这样",
    "你记得对",
    "记对了",
)
_MISMATCH_MARKERS = (
    "不太对",
    "有点不对",
    "不完全对",
    "好像不是",
)


def detect_memory_feedback_from_utterance(
    utterance: str,
    *,
    dialogue_turn_ref: str | None = None,
) -> dict[str, Any]:
    normalized = " ".join(str(utterance or "").split())
    event_type = None
    if normalized:
        if any(marker in normalized for marker in _CORRECTION_MARKERS):
            event_type = "correction"
        elif any(marker in normalized for marker in _CONFIRMATION_MARKERS):
            event_type = "confirmation"
        elif any(marker in normalized for marker in _MISMATCH_MARKERS):
            event_type = "mismatch"
    return {
        "schema_version": "memory_feedback_event_v0",
        "event_type": event_type,
        "trigger_event_ref": dialogue_turn_ref,
        "utterance_digest": normalized[:120],
        "feedback_boundary": "structured_memory_feedback_not_spoken_reply",
    }


def enrich_semantic_map_with_pragmatic_inference(
    *,
    semantic_map: dict[str, Any],
    language_percept: dict[str, Any],
    relationship_timeline: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    context_accumulation: dict[str, Any] | None = None,
    relation_scope_index: dict[str, Any] | None = None,
    shared_term_registry: dict[str, Any] | None = None,
    relationship_stage: str | None = None,
    generated_at: str,
) -> dict[str, Any]:
    relationship_timeline = relationship_timeline or {}
    commitment_truth_state = commitment_truth_state or {}
    context_accumulation = context_accumulation or {}
    relation_scope_index = relation_scope_index or {}
    shared_term_registry = shared_term_registry or {}

    updated = json.loads(json.dumps(semantic_map))
    profile = _build_pragmatic_inference_profile(
        language_percept=language_percept,
        relationship_timeline=relationship_timeline,
        commitment_truth_state=commitment_truth_state,
        context_accumulation=context_accumulation,
        relation_scope_index=relation_scope_index,
        shared_term_registry=shared_term_registry,
        relationship_stage=relationship_stage,
        generated_at=generated_at,
    )
    updated["pragmatic_inference_profile"] = profile
    updated["pragmatic_inference_mode"] = profile.get(
        "inference_mode", "live_evidence_inference"
    )
    dominant_intent = profile.get("dominant_pragmatic_intent")
    if dominant_intent:
        updated["semantic_focus"] = dominant_intent
        prediction_hooks = dict(updated.get("prediction_hooks", {}))
        prediction_hooks["semantic_prediction_focus"] = dominant_intent
        prediction_hooks["pragmatic_inference_refs"] = [
            "runtime/state/language/semantic_map_frame.json#pragmatic_inference_profile"
        ]
        updated["prediction_hooks"] = prediction_hooks
    updated["pragmatic_inference_boundary"] = PRAGMATIC_INFERENCE_BOUNDARY
    return updated


def pragmatic_inference_inspection_snapshot(
    *,
    semantic_map: dict[str, Any] | None = None,
) -> dict[str, Any]:
    semantic_map = semantic_map or {}
    profile = semantic_map.get("pragmatic_inference_profile", {})
    if not isinstance(profile, dict):
        profile = {}
    speech_acts = [
        item
        for item in profile.get("speech_act_candidates", [])
        if isinstance(item, dict)
    ]
    implicatures = [
        item for item in profile.get("implicature_queue", []) if isinstance(item, dict)
    ]
    grounding = [
        item
        for item in profile.get("grounding_repair_signals", [])
        if isinstance(item, dict)
    ]
    return {
        "pragmatic_inference_present": bool(profile),
        "pragmatic_inference_mode": semantic_map.get("pragmatic_inference_mode"),
        "pragmatic_speech_act_count": len(speech_acts),
        "pragmatic_implicature_count": len(implicatures),
        "pragmatic_grounding_repair_count": len(grounding),
        "dominant_pragmatic_intent": profile.get("dominant_pragmatic_intent"),
        "pragmatic_inference_evidence_ref_count": len(
            profile.get("evidence_refs", [])
        ),
        "pragmatic_inference_boundary": (
            semantic_map.get("pragmatic_inference_boundary")
            or PRAGMATIC_INFERENCE_BOUNDARY
        ),
    }


def _build_pragmatic_inference_profile(
    *,
    language_percept: dict[str, Any],
    relationship_timeline: dict[str, Any],
    commitment_truth_state: dict[str, Any],
    context_accumulation: dict[str, Any],
    relation_scope_index: dict[str, Any],
    shared_term_registry: dict[str, Any],
    relationship_stage: str | None,
    generated_at: str,
) -> dict[str, Any]:
    speech_act_candidates: list[dict[str, Any]] = []
    implicature_queue: list[dict[str, Any]] = []
    grounding_repair_signals: list[dict[str, Any]] = []
    evidence_refs: list[str] = []

    open_commitments = _string_list(commitment_truth_state.get("open_commitment_refs"))
    repair_required = _string_list(
        commitment_truth_state.get("repair_required_refs")
    )
    unresolved_commitments = _string_list(
        context_accumulation.get("unresolved_commitment_refs")
    )
    trust_state = _trust_state(relationship_timeline)
    continuity_state = _continuity_state(relationship_timeline)
    ambiguity_flags = _string_list(language_percept.get("ambiguity_flags"))
    cross_scope_risks = _string_list(language_percept.get("cross_scope_risk_terms"))
    utterance_signals = language_percept.get("utterance_signal_profile") or {}
    incoming_surface = str(language_percept.get("incoming_surface", ""))

    _append_surface_speech_acts(
        speech_act_candidates=speech_act_candidates,
        implicature_queue=implicature_queue,
        grounding_repair_signals=grounding_repair_signals,
        evidence_refs=evidence_refs,
        utterance_signals=utterance_signals,
        incoming_surface=incoming_surface,
        cross_scope_risks=cross_scope_risks,
    )

    if open_commitments or unresolved_commitments:
        speech_act_candidates.append(
            {
                "speech_act_id": "commitment_followup",
                "evidence_kind": "commitment_truth_open",
                "confidence": 0.78,
            }
        )
        evidence_refs.append(
            "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs"
        )
    if repair_required or language_percept.get("repair_trigger_candidates"):
        speech_act_candidates.append(
            {
                "speech_act_id": "repair_request",
                "evidence_kind": "repair_obligation",
                "confidence": 0.82,
            }
        )
        evidence_refs.append(
            "runtime/state/relationship/commitment_truth_state.json#repair_required_refs"
        )
    if trust_state in {"low", "calibrated_low", "guarded"}:
        speech_act_candidates.append(
            {
                "speech_act_id": "trust_calibration",
                "evidence_kind": "trust_trajectory",
                "confidence": 0.7,
            }
        )
        evidence_refs.append(
            "runtime/state/relationship/relationship_timeline.json#trust_trajectories"
        )
    if ambiguity_flags:
        speech_act_candidates.append(
            {
                "speech_act_id": "clarification_request",
                "evidence_kind": "semantic_ambiguity",
                "confidence": 0.74,
            }
        )
        evidence_refs.append(
            "runtime/state/language/language_percept_frame.json#ambiguity_flags"
        )

    for flag in ambiguity_flags:
        implicature_queue.append(
            {
                "implicature_id": f"implicature-{flag}",
                "kind": "grounding_uncertainty",
                "source_flag": flag,
            }
        )
    for term in cross_scope_risks:
        implicature_queue.append(
            {
                "implicature_id": f"implicature-scope-{term}",
                "kind": "relation_scope_boundary",
                "source_term": term,
            }
        )

    promoted_terms = [
        term
        for term in shared_term_registry.get("shared_terms", [])
        if isinstance(term, dict) and term.get("promotion_status") == "promoted"
    ]
    for term in promoted_terms[:4]:
        implicature_queue.append(
            {
                "implicature_id": f"implicature-shared-{term.get('surface')}",
                "kind": "shared_meaning_binding",
                "surface": term.get("surface"),
            }
        )
        evidence_refs.append("runtime/state/language/shared_term_registry.json")

    if unresolved_commitments:
        grounding_repair_signals.append(
            {
                "signal_id": "unresolved_commitment_grounding",
                "ref_count": len(unresolved_commitments),
            }
        )
        evidence_refs.append(
            "runtime/state/terminal/context_accumulation_window.json#unresolved_commitment_refs"
        )
    if continuity_state in {"repair_guarded_continuity", "strained_continuity"}:
        grounding_repair_signals.append(
            {
                "signal_id": "continuity_repair_grounding",
                "continuity_state": continuity_state,
            }
        )
        evidence_refs.append(
            "runtime/state/relationship/relationship_timeline.json#relationship_continuity_reports"
        )

    dominant_pragmatic_intent = _dominant_pragmatic_intent(
        relationship_stage=relationship_stage,
        continuity_state=continuity_state,
        trust_state=trust_state,
        speech_act_candidates=speech_act_candidates,
        semantic_focus=language_percept.get("semantic_focus"),
    )

    return {
        "schema_version": "pragmatic_inference_profile_v0",
        "generated_at": generated_at,
        "inference_mode": "live_evidence_inference",
        "dominant_pragmatic_intent": dominant_pragmatic_intent,
        "relationship_stage": relationship_stage,
        "continuity_state": continuity_state,
        "trust_state": trust_state,
        "speech_act_candidates": speech_act_candidates[:8],
        "implicature_queue": implicature_queue[:12],
        "grounding_repair_signals": grounding_repair_signals[:8],
        "evidence_refs": _dedupe(evidence_refs)[:12],
        "pragmatic_inference_boundary": PRAGMATIC_INFERENCE_BOUNDARY,
    }


def _dominant_pragmatic_intent(
    *,
    relationship_stage: str | None,
    continuity_state: str | None,
    trust_state: str | None,
    speech_act_candidates: list[dict[str, Any]],
    semantic_focus: Any,
) -> str:
    speech_act_ids = {
        str(item.get("speech_act_id"))
        for item in speech_act_candidates
        if item.get("speech_act_id")
    }
    if "relation_recalibration" in speech_act_ids:
        return "relation_scope_recalibration"
    if "boundary_declaration" in speech_act_ids:
        return "boundary_declaration"
    if "repair_request" in speech_act_ids or "apology" in speech_act_ids:
        return "repair_relational_trace"
    if "commitment_followup" in speech_act_ids or "commitment_request" in speech_act_ids:
        return "repair_commitment_shared_language"
    if "clarification_request" in speech_act_ids:
        return "clarification_request"
    if continuity_state in {"repair_guarded_continuity", "strained_continuity"}:
        return "repair_relational_trace"
    if trust_state in {"low", "calibrated_low", "guarded"}:
        return "relational_checkin"
    if relationship_stage and "repair" in str(relationship_stage):
        return "repair_relational_trace"
    if isinstance(semantic_focus, str) and semantic_focus:
        return semantic_focus
    return "relational_checkin"


def _trust_state(relationship_timeline: dict[str, Any]) -> str | None:
    trajectories = relationship_timeline.get("trust_trajectories", [])
    if trajectories and isinstance(trajectories[0], dict):
        return trajectories[0].get("current_trust_state")
    return None


def _continuity_state(relationship_timeline: dict[str, Any]) -> str | None:
    reports = relationship_timeline.get("relationship_continuity_reports", [])
    if reports and isinstance(reports[0], dict):
        return reports[0].get("continuity_state")
    return None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def _append_surface_speech_acts(
    *,
    speech_act_candidates: list[dict[str, Any]],
    implicature_queue: list[dict[str, Any]],
    grounding_repair_signals: list[dict[str, Any]],
    evidence_refs: list[str],
    utterance_signals: dict[str, Any],
    incoming_surface: str,
    cross_scope_risks: list[str],
) -> None:
    mapping = (
        ("apology", "apology", "repair_obligation_surface"),
        ("boundary_declaration", "boundary_declaration", "boundary_maintenance_surface"),
        ("clarification_request", "clarification_request", "grounding_uncertainty_surface"),
        ("commitment_request", "commitment_request", "commitment_request_surface"),
        ("relation_recalibration", "relation_recalibration", "relation_scope_surface"),
    )
    for signal_key, speech_act_id, evidence_kind in mapping:
        if not utterance_signals.get(signal_key):
            continue
        speech_act_candidates.append(
            {
                "speech_act_id": speech_act_id,
                "evidence_kind": evidence_kind,
                "confidence": 0.86,
            }
        )
        evidence_refs.append(
            "runtime/state/language/language_percept_frame.json#utterance_signal_profile"
        )
        implicature_queue.append(
            {
                "implicature_id": f"implicature-surface-{speech_act_id}",
                "kind": evidence_kind,
                "utterance_digest": incoming_surface[:80],
            }
        )
    if cross_scope_risks:
        grounding_repair_signals.append(
            {
                "signal_id": "cross_scope_risk_grounding",
                "risk_terms": cross_scope_risks[:4],
            }
        )
        evidence_refs.append(
            "runtime/state/language/language_percept_frame.json#cross_scope_risk_terms"
        )
