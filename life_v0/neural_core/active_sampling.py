from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/01w_prediction_active_inference_schema_fixture_contract.md",
    "docs/01y_prediction_active_inference_schema_write_batch.md",
]


def build_active_sampling_plan(
    *,
    run_id: str,
    generated_at: str,
    belief_state: dict[str, Any],
    prediction_error_field: dict[str, Any],
    signal_media_runtime: dict[str, Any] | None = None,
    queue_e_repair_modulation_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    signal_media_runtime = signal_media_runtime or {}
    repair_profile = (
        queue_e_repair_modulation_profile
        or prediction_error_field.get("queue_e_repair_modulation_profile")
        or belief_state.get("queue_e_repair_modulation_profile")
        or signal_media_runtime.get("queue_e_repair_modulation_profile")
        or {}
    )
    pressure_level = repair_profile.get("pressure_level", "quiet")
    relationship_pressure = (
        signal_media_runtime.get("modulation_vector", {}).get("relationship_pressure", 0.0)
    )
    selected_route = "clarify" if relationship_pressure < 0.4 else "inspect"
    if pressure_level == "urgent":
        selected_route = "repair_confirm"
    elif pressure_level == "elevated":
        selected_route = "repair_inspect"
    return {
        "schema_version": "active_sampling_plan_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "sampling_plan_id": f"active-sampling-{run_id}",
        "belief_frame_ref": "runtime/state/prediction/belief_state_frame.json",
        "prediction_error_ref": "runtime/state/prediction/prediction_error_field.json",
        "candidate_refs": [
            "epistemic_candidate_review_semantic_map",
            "epistemic_candidate_review_relation_scope",
            "epistemic_candidate_review_commitment_truth",
            *(
                ["epistemic_candidate_review_repair_obligation"]
                if repair_profile
                else []
            ),
        ],
        "selected_route": selected_route,
        "guard_refs": [
            "direction_anchor_guard",
            "birth_readiness_false_open_guard",
            "relation_scope_guard",
            "external_action_membrane_guard",
            *(
                ["queue_e_repair_pressure_guard"]
                if repair_profile
                else []
            ),
        ],
        "scope_refs": [
            "runtime/state/language/semantic_map_state.json",
            "runtime/state/language/relation_scope_language_index.json",
            "runtime/state/relationship/commitment_truth_state.json",
            *list(repair_profile.get("ref_set", [])),
        ],
        "command_binding_refs": [
            "inspect_language_runtime",
            "inspect_relation_scope",
            "inspect_commitment_truth",
            *(
                ["inspect_responsibility_repair_pressure"]
                if repair_profile
                else []
            ),
        ],
        "expected_observation_refs": [
            "runtime/state/language/language_percept_state.json",
            "runtime/state/language/dialogue_turn_log.jsonl",
            "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs",
            *(
                ["runtime/state/action/responsibility_loop_state.json#repair_obligation_refs"]
                if repair_profile
                else []
            ),
        ],
        "stage_effect": prediction_error_field.get("stage_effect", "hold_for_evidence"),
        "archive_edge_plan": {
            "receipt_ref": f"runtime/receipts/neural_life_core_{run_id}.json",
            "replay_route": "prediction_active_inference_archive_seed",
            "if_conflict": "quarantine_candidate_before_writeback",
        },
        "affected_life_targets": belief_state.get("active_life_targets", []),
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
