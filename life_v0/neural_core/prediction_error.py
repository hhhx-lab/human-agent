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
