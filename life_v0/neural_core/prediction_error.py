from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/01w_prediction_active_inference_schema_fixture_contract.md",
    "docs/01y_prediction_active_inference_schema_write_batch.md",
]


def build_prediction_error_field(
    *,
    run_id: str,
    generated_at: str,
    belief_state: dict[str, Any],
    signal_media_runtime: dict[str, Any] | None = None,
    queue_e_repair_modulation_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    signal_media_runtime = signal_media_runtime or {}
    repair_profile = (
        queue_e_repair_modulation_profile
        or belief_state.get("queue_e_repair_modulation_profile")
        or signal_media_runtime.get("queue_e_repair_modulation_profile")
        or {}
    )
    pressure_level = repair_profile.get("pressure_level", "quiet")
    unexpected_uncertainty = (
        signal_media_runtime.get("modulation_vector", {}).get("unexpected_uncertainty", 0.21)
    )
    stage_effect = "hold_for_evidence" if unexpected_uncertainty >= 0.2 else "repair"
    if pressure_level == "urgent":
        stage_effect = "hold_for_repair_confirmation"
    elif pressure_level == "elevated":
        stage_effect = "repair_pressure_review"
    error_events = [
        {
            "error_id": "semantic-ambiguity-0001",
            "error_kind": "semantic",
            "expected": "共享语言连续稳定",
            "observed": "仍存在语义歧义待澄清",
            "delta": "clarify_before_commitment",
            "precision_request": "high",
        },
        {
            "error_id": "relationship-guard-0001",
            "error_kind": "social",
            "expected": "关系连续体保持低伤害表达",
            "observed": "需要先审视关系边界与承诺真值",
            "delta": "guarded_review_required",
            "precision_request": "high",
        },
    ]
    if repair_profile:
        error_events.append(
            {
                "error_id": "queue-e-repair-pressure-0001",
                "error_kind": "responsibility_repair",
                "expected": "责任、后悔、痛苦与修复路径保持可追踪",
                "observed": pressure_level,
                "delta": repair_profile.get("attention_target", "repair_followup"),
                "precision_request": "very_high" if pressure_level == "urgent" else "high",
            }
        )
    precision_requests = [
        "raise_relationship_precision",
        "hold_external_action",
    ]
    if repair_profile:
        precision_requests.append("raise_repair_obligation_precision")
    return {
        "schema_version": "prediction_error_field_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "error_field_id": f"prediction-error-{run_id}",
        "belief_frame_ref": "runtime/state/prediction/belief_state_frame.json",
        "error_events": error_events,
        "precision_requests": precision_requests,
        "affected_life_targets": belief_state.get("active_life_targets", []),
        "workspace_entry_candidates": [
            "semantic_disambiguation",
            "relationship_guard_review",
            *(
                ["responsibility_repair_pressure_review"]
                if repair_profile
                else []
            ),
        ],
        "dream_replay_candidates": [
            "runtime/state/dream/dream_consolidation_frame.json#ambiguity_replay_seed",
        ],
        "stage_effect": stage_effect,
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "queue_e_repair_modulation_profile": repair_profile if repair_profile else None,
        "queue_e_repair_pressure_level": pressure_level,
        "queue_e_repair_attention_target": repair_profile.get("attention_target", "repair_followup"),
        "queue_e_repair_ref_set": list(repair_profile.get("ref_set", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def refresh_prediction_error_from_live_turn(
    *,
    prediction_error_field: dict[str, Any] | None,
    run_id: str,
    generated_at: str,
    turn_counter: int,
    belief_state: dict[str, Any],
    signal_media_runtime: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
    semantic_map: dict[str, Any] | None,
    body_integrator: dict[str, Any] | None,
    queue_e_repair_modulation_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    language_percept = language_percept or {}
    semantic_map = semantic_map or {}
    signal_media_runtime = signal_media_runtime or {}
    repair_profile = (
        queue_e_repair_modulation_profile
        or (prediction_error_field or {}).get("queue_e_repair_modulation_profile")
        or belief_state.get("queue_e_repair_modulation_profile")
        or signal_media_runtime.get("queue_e_repair_modulation_profile")
        or {}
    )
    pressure_level = repair_profile.get("pressure_level", "quiet")
    unexpected_uncertainty = float(
        signal_media_runtime.get("modulation_vector", {}).get("unexpected_uncertainty", 0.21)
        or 0.21
    )
    ambiguity_queue = list(semantic_map.get("ambiguity_queue", []))
    ambiguity_flags = list(language_percept.get("ambiguity_flags", []))
    ambiguity_count = len(ambiguity_queue) + len(ambiguity_flags)
    continuous = (body_integrator or {}).get("continuous") or {}
    allostatic_load = float(continuous.get("allostatic_load", 0.0) or 0.0)
    cognitive_bandwidth = float(continuous.get("cognitive_bandwidth", 0.82) or 0.82)

    base = prediction_error_field or build_prediction_error_field(
        run_id=run_id,
        generated_at=generated_at,
        belief_state=belief_state,
        signal_media_runtime=signal_media_runtime,
        queue_e_repair_modulation_profile=repair_profile,
    )
    updated = dict(base)
    updated["generated_at"] = generated_at
    updated["run_id"] = run_id

    error_events = [
        event
        for event in list(updated.get("error_events", []))
        if not str(event.get("error_id", "")).startswith("live-")
    ]
    semantic_magnitude = _clamp(0.18 + ambiguity_count * 0.14 + unexpected_uncertainty * 0.2)
    error_events.append(
        {
            "error_id": f"live-semantic-ambiguity-{turn_counter:04d}",
            "error_kind": "semantic",
            "expected": semantic_map.get("semantic_focus") or "共享语义焦点稳定",
            "observed": ambiguity_queue[:3] or ambiguity_flags[:3] or ["no_live_ambiguity"],
            "delta": "clarify_before_commitment" if ambiguity_count else "semantic_alignment_hold",
            "precision_request": "high" if ambiguity_count else "medium",
            "magnitude": semantic_magnitude,
            "turn_counter": turn_counter,
        }
    )
    if allostatic_load >= 0.35 or cognitive_bandwidth <= 0.55:
        error_events.append(
            {
                "error_id": f"live-body-bandwidth-{turn_counter:04d}",
                "error_kind": "interoceptive",
                "expected": "身体带宽足以支撑高精度承诺",
                "observed": {
                    "allostatic_load": round(allostatic_load, 3),
                    "cognitive_bandwidth": round(cognitive_bandwidth, 3),
                },
                "delta": "hold_for_evidence",
                "precision_request": "high" if allostatic_load >= 0.55 else "medium",
                "magnitude": _clamp(allostatic_load * 0.5 + (1.0 - cognitive_bandwidth) * 0.35),
                "turn_counter": turn_counter,
            }
        )

    stage_effect = "hold_for_evidence" if unexpected_uncertainty >= 0.2 else "repair"
    if pressure_level == "urgent":
        stage_effect = "hold_for_repair_confirmation"
    elif pressure_level == "elevated":
        stage_effect = "repair_pressure_review"
    elif ambiguity_count >= 2:
        stage_effect = "clarify_before_commitment"

    updated["error_events"] = error_events
    updated["stage_effect"] = stage_effect
    updated["live_refresh_applied"] = True
    updated["live_turn_counter"] = turn_counter
    updated["live_ambiguity_count"] = ambiguity_count
    updated["unexpected_uncertainty_snapshot"] = round(unexpected_uncertainty, 3)
    return updated


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)
