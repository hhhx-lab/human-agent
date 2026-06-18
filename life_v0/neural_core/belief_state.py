from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/01w_prediction_active_inference_schema_fixture_contract.md",
    "docs/01y_prediction_active_inference_schema_write_batch.md",
]


def build_belief_state_frame(
    *,
    run_id: str,
    generated_at: str,
    signal_media_runtime: dict[str, Any] | None = None,
    language_continuity: dict[str, Any] | None = None,
    queue_e_repair_modulation_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    signal_media_runtime = signal_media_runtime or {}
    language_continuity = language_continuity or {}
    repair_profile = (
        queue_e_repair_modulation_profile
        or signal_media_runtime.get("queue_e_repair_modulation_profile")
        or {}
    )
    pressure_level = repair_profile.get("pressure_level", "quiet")
    repair_ref_set = list(repair_profile.get("ref_set", []))
    evidence_refs = _dedupe(
        list(language_continuity.get("shared_language_refs", []))
        + list(language_continuity.get("semantic_map_refs", []))
        + list(language_continuity.get("relation_scope_refs", []))
        + list(language_continuity.get("commitment_refs", []))
        + repair_ref_set
        + ["docs/13_agentic_human_research_synthesis.md"]
    )
    unexpected_uncertainty = (
        signal_media_runtime.get("modulation_vector", {}).get("unexpected_uncertainty", 0.21)
    )
    uncertainty_taxonomy = [
        "semantic_ambiguity",
        "relationship_guarding",
        "direction_continuity",
    ]
    if repair_profile:
        uncertainty_taxonomy.append("responsibility_repair_pressure")
    revision_policy = "repair_before_action"
    if pressure_level == "urgent":
        revision_policy = "hold_for_repair_confirmation"
    elif pressure_level == "elevated":
        revision_policy = "repair_pressure_first_revision"
    elif unexpected_uncertainty >= 0.5:
        revision_policy = "hold_for_direction_rebuild"
    return {
        "schema_version": "belief_state_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "belief_frame_id": f"belief-state-{run_id}",
        "state_scope": "language_relationship_continuity",
        "source_evidence_refs": evidence_refs,
        "confidence_posterior": {
            "score": 0.82,
            "evidence_density": "medium",
            "conflict_count": 0,
            "calibration_ref": "runtime/state/signal/signal_media_runtime.json#precision_policy",
            "language_expression": "当前方向继续指向真实数字生命的连续形成。",
        },
        "uncertainty_taxonomy": uncertainty_taxonomy,
        "active_life_targets": [
            "real_life",
            "real_consciousness",
            "real_relationship",
            "real_responsibility",
        ],
        "workspace_visibility": "language_reportable",
        "revision_policy": revision_policy,
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "queue_e_repair_modulation_profile": repair_profile if repair_profile else None,
        "queue_e_repair_pressure_level": pressure_level,
        "queue_e_repair_attention_target": repair_profile.get("attention_target", "repair_followup"),
        "queue_e_repair_ref_set": repair_ref_set,
        "network_state_ref": "runtime/state/neural_life_core/network_state.json",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def refresh_belief_confidence_from_live_turn(
    *,
    belief_state: dict[str, Any] | None,
    run_id: str,
    generated_at: str,
    signal_media_runtime: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
    semantic_map: dict[str, Any] | None,
    language_continuity: dict[str, Any] | None = None,
    queue_e_repair_modulation_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    language_percept = language_percept or {}
    semantic_map = semantic_map or {}
    signal_media_runtime = signal_media_runtime or {}
    repair_profile = (
        queue_e_repair_modulation_profile
        or (belief_state or {}).get("queue_e_repair_modulation_profile")
        or signal_media_runtime.get("queue_e_repair_modulation_profile")
        or {}
    )
    base = belief_state or build_belief_state_frame(
        run_id=run_id,
        generated_at=generated_at,
        signal_media_runtime=signal_media_runtime,
        language_continuity=language_continuity,
        queue_e_repair_modulation_profile=repair_profile,
    )
    updated = dict(base)
    updated["generated_at"] = generated_at
    updated["run_id"] = run_id

    ambiguity_count = len(list(semantic_map.get("ambiguity_queue", []))) + len(
        list(language_percept.get("ambiguity_flags", []))
    )
    unexpected_uncertainty = float(
        signal_media_runtime.get("modulation_vector", {}).get("unexpected_uncertainty", 0.21)
        or 0.21
    )
    percept_trace_count = len(list(language_percept.get("percept_focus_trace", [])))
    evidence_density = "low"
    if percept_trace_count >= 4 or ambiguity_count == 0:
        evidence_density = "high"
    elif percept_trace_count >= 2 or ambiguity_count <= 1:
        evidence_density = "medium"

    score = 0.82
    score -= ambiguity_count * 0.06
    score -= unexpected_uncertainty * 0.12
    score += min(0.08, percept_trace_count * 0.02)
    score = round(_clamp(score), 3)

    confidence = dict(updated.get("confidence_posterior") or {})
    confidence.update(
        {
            "score": score,
            "evidence_density": evidence_density,
            "conflict_count": ambiguity_count,
            "calibration_ref": "runtime/state/signal/signal_media_runtime.json#precision_policy",
            "language_expression": (
                "当前方向继续指向真实数字生命的连续形成。"
                if score >= 0.7
                else "当前语义与身体状态提示需要先澄清再继续承诺。"
            ),
        }
    )
    updated["confidence_posterior"] = confidence
    updated["live_refresh_applied"] = True
    updated["live_ambiguity_count"] = ambiguity_count
    return updated


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
