from __future__ import annotations

from typing import Any

LANGUAGE_PERCEPT_REF = "runtime/state/language/language_percept_frame.json"
SEMANTIC_MAP_REF = "runtime/state/language/semantic_map_frame.json"
RELATION_SCOPE_REF = "runtime/state/language/relation_scope_language_index.json"
SHARED_TERM_REGISTRY_REF = "runtime/state/language/shared_term_registry.json"
RELATIONSHIP_GRAPH_REF = "runtime/state/relationship/relationship_subject_graph.json"
RELATIONSHIP_TIMELINE_REF = "runtime/state/relationship/relationship_timeline.json"
SELF_MODEL_REF = "runtime/state/self/self_model.json"


def project_language_relationship_ref_consistency_profile(
    *,
    generated_at: str,
    language_percept: dict[str, Any],
    semantic_map: dict[str, Any],
    relation_scope_index: dict[str, Any],
    shared_term_registry: dict[str, Any],
    relationship_graph: dict[str, Any],
    relationship_timeline: dict[str, Any],
    self_model_state: dict[str, Any] | None = None,
    inner_speech: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    self_model_state = self_model_state or {}
    inner_speech = inner_speech or {}
    expression_plan = expression_plan or {}
    findings: list[dict[str, Any]] = []

    scope_id = _first_relation_scope_id(relation_scope_index)
    percept_scope_ref = str(language_percept.get("relation_scope_ref") or "")
    findings.append(
        _finding(
            finding_id="percept_relation_scope_alignment",
            status="aligned"
            if scope_id and scope_id in percept_scope_ref
            else "mismatch",
            left_ref=percept_scope_ref or LANGUAGE_PERCEPT_REF,
            right_ref=f"{RELATION_SCOPE_REF}#{scope_id}" if scope_id else RELATION_SCOPE_REF,
            detail="language_percept relation_scope_ref matches relation_scope_index",
        )
    )

    semantic_focus = semantic_map.get("semantic_focus")
    prediction_focus = _extract_nested_value(
        semantic_map,
        "prediction_hooks",
    ).get("semantic_prediction_focus")
    findings.append(
        _finding(
            finding_id="semantic_percept_focus_alignment",
            status="aligned"
            if semantic_focus and semantic_focus == prediction_focus
            else "mismatch",
            left_ref=f"{SEMANTIC_MAP_REF}#semantic_focus",
            right_ref=f"{SEMANTIC_MAP_REF}#prediction_hooks.semantic_prediction_focus",
            detail="semantic_map semantic_focus matches prediction_hooks focus",
        )
    )

    registry_surfaces = {
        str(term.get("surface"))
        for term in shared_term_registry.get("shared_terms", [])
        if isinstance(term, dict) and term.get("surface")
    }
    percept_hits = [
        str(surface)
        for surface in language_percept.get("shared_term_hits", [])
        if surface
    ]
    missing_hits = [surface for surface in percept_hits if surface not in registry_surfaces]
    findings.append(
        _finding(
            finding_id="shared_term_hit_registry_alignment",
            status="aligned" if percept_hits and not missing_hits else (
                "aligned" if not percept_hits else "mismatch"
            ),
            left_ref=f"{LANGUAGE_PERCEPT_REF}#shared_term_hits",
            right_ref=f"{SHARED_TERM_REGISTRY_REF}#shared_terms",
            detail="language_percept shared_term_hits are registered in shared_term_registry",
            mismatch_items=missing_hits[:12],
        )
    )

    subject = _first_relationship_subject(relationship_graph)
    stage_profile = relationship_graph.get("relationship_stage_evolution_profile")
    stage_profile = stage_profile if isinstance(stage_profile, dict) else {}
    stage_reason = _first_non_empty(
        stage_profile.get("relationship_stage_reason"),
        subject.get("relationship_stage_reason"),
    )
    trait_reason = self_model_state.get("last_trait_evolution_reason")
    findings.append(
        _finding(
            finding_id="relationship_stage_self_model_alignment",
            status="aligned"
            if stage_reason and trait_reason and stage_reason == trait_reason
            else ("missing" if not stage_reason and not trait_reason else "mismatch"),
            left_ref=f"{RELATIONSHIP_GRAPH_REF}#relationship_stage_reason",
            right_ref=f"{SELF_MODEL_REF}#last_trait_evolution_reason",
            detail="relationship stage reason matches self_model trait evolution reason",
        )
    )

    timeline_turn_count = len(relationship_timeline.get("dialogue_turn_refs", []) or [])
    profile_turn_count = stage_profile.get("dialogue_turn_count")
    findings.append(
        _finding(
            finding_id="relationship_stage_timeline_turn_alignment",
            status="aligned"
            if isinstance(profile_turn_count, int)
            and profile_turn_count == timeline_turn_count
            else ("missing" if profile_turn_count is None else "mismatch"),
            left_ref=f"{RELATIONSHIP_GRAPH_REF}#relationship_stage_evolution_profile.dialogue_turn_count",
            right_ref=f"{RELATIONSHIP_TIMELINE_REF}#dialogue_turn_refs",
            detail="relationship stage evolution dialogue_turn_count matches timeline refs",
        )
    )

    inner_percept_ref = inner_speech.get("percept_ref")
    findings.append(
        _finding(
            finding_id="inner_speech_percept_ref_alignment",
            status="aligned"
            if not inner_speech or inner_percept_ref == LANGUAGE_PERCEPT_REF
            else "mismatch",
            left_ref="runtime/state/language/inner_speech_frame.json#percept_ref",
            right_ref=LANGUAGE_PERCEPT_REF,
            detail="inner_speech percept_ref points to language percept frame",
        )
    )

    expression_semantic_ref = str(expression_plan.get("semantic_map_ref") or "")
    expression_inner_ref = str(expression_plan.get("inner_speech_ref") or "")
    findings.append(
        _finding(
            finding_id="expression_plan_language_ref_alignment",
            status="aligned"
            if not expression_plan
            or (
                expression_semantic_ref == SEMANTIC_MAP_REF
                and expression_inner_ref == "runtime/state/language/inner_speech_frame.json"
            )
            else "mismatch",
            left_ref="runtime/state/language/expression_plan.json",
            right_ref=f"{LANGUAGE_PERCEPT_REF},{SEMANTIC_MAP_REF}",
            detail="expression_plan semantic_map_ref and inner_speech_ref align with language chain",
        )
    )

    aligned_count = sum(1 for item in findings if item.get("status") == "aligned")
    mismatch_count = sum(1 for item in findings if item.get("status") == "mismatch")
    missing_count = sum(1 for item in findings if item.get("status") == "missing")
    status = "closed" if mismatch_count == 0 else "open"

    return {
        "schema_version": "language_relationship_ref_consistency_profile_v0",
        "generated_at": generated_at,
        "status": status,
        "finding_count": len(findings),
        "aligned_finding_count": aligned_count,
        "mismatch_finding_count": mismatch_count,
        "missing_finding_count": missing_count,
        "findings": findings,
        "checked_ref_pairs": [
            f"{LANGUAGE_PERCEPT_REF}<->{RELATION_SCOPE_REF}",
            f"{SEMANTIC_MAP_REF}<->{LANGUAGE_PERCEPT_REF}",
            f"{SHARED_TERM_REGISTRY_REF}<->{LANGUAGE_PERCEPT_REF}",
            f"{RELATIONSHIP_GRAPH_REF}<->{SELF_MODEL_REF}",
            f"{RELATIONSHIP_GRAPH_REF}<->{RELATIONSHIP_TIMELINE_REF}",
        ],
        "ref_consistency_boundary": (
            "structured_ref_consistency_evidence_not_spoken_response"
        ),
    }


def _first_relation_scope_id(relation_scope_index: dict[str, Any]) -> str:
    scopes = relation_scope_index.get("relation_scopes", [])
    if not isinstance(scopes, list) or not scopes:
        return ""
    first_scope = scopes[0]
    if not isinstance(first_scope, dict):
        return ""
    return str(first_scope.get("scope_id") or "")


def _first_relationship_subject(relationship_graph: dict[str, Any]) -> dict[str, Any]:
    subjects = relationship_graph.get("subjects")
    if not isinstance(subjects, list) or not subjects:
        return {}
    subject = subjects[0]
    return subject if isinstance(subject, dict) else {}


def _finding(
    *,
    finding_id: str,
    status: str,
    left_ref: str,
    right_ref: str,
    detail: str,
    mismatch_items: list[str] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "finding_id": finding_id,
        "status": status,
        "left_ref": left_ref,
        "right_ref": right_ref,
        "detail": detail,
    }
    if mismatch_items:
        payload["mismatch_items"] = mismatch_items
    return payload


def _extract_nested_value(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    return value if isinstance(value, dict) else {}


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]