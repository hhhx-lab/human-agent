from __future__ import annotations

from typing import Any

from life_v0.membrane.queue_e_signals import (
    queue_e_repair_modulation_profile_from_replay_cue_bundle,
)


SOURCE_DOC_REFS = [
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/187_life_reality_first_runner_schema_runtime_growth_feedback_patch_plan.md",
    "docs/188_life_reality_first_runner_schema_runtime_growth_archive_receipt_batch.md",
    "docs/189_life_reality_first_runner_schema_runtime_growth_shadow_run_plan.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]


def build_growth_patch_queue(
    *,
    run_id: str,
    generated_at: str,
    growth_route: dict[str, Any],
    anchor_index: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "growth_patch_queue_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "queued_guarded",
        "queued_patch_families": [
            "anti_forgetting_replay_patch",
            "dream_reconsolidation_patch",
            "responsibility_repair_patch",
            "language_relationship_patch",
        ],
        "candidate_routes": list(growth_route.get("candidate_routes", [])),
        "anchor_ref_count": sum(len(value) for value in anchor_index.get("anchor_families", {}).values()),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_growth_patch_candidate_queue(
    *,
    run_id: str,
    generated_at: str,
    replay_cue_bundle: dict[str, Any],
    growth_route: dict[str, Any],
    learning_window: dict[str, Any],
) -> dict[str, Any]:
    repair_profile = queue_e_repair_modulation_profile_from_replay_cue_bundle(
        replay_cue_bundle
    )
    return {
        "schema_version": "growth_patch_candidate_queue_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "candidates": [
            {
                "growth_patch_candidate_id": f"growth-patch-candidate-{run_id}-0001",
                "source_residue_refs": list(replay_cue_bundle.get("turn_residue_refs", [])),
                "plasticity_window_ref": "runtime/state/growth/plasticity_window_state.json",
                "learning_window_ref": "runtime/state/growth/learning_window.json",
                "risk_flags": [
                    "direction_lock_required",
                    "archive_before_activation",
                    *(
                        ["queue_e_repair_modulation_required"]
                        if repair_profile["pressure_level"] in {"urgent", "elevated"}
                        else []
                    ),
                ],
                "anti_forgetting_requirements": list(replay_cue_bundle.get("anti_forgetting_targets", [])),
                "queue_e_repair_modulation_profile": repair_profile,
                "queue_e_repair_pressure_level": repair_profile["pressure_level"],
                "queue_e_repair_attention_target": repair_profile["attention_target"],
                "queue_e_repair_ref_set": list(repair_profile.get("ref_set", [])),
                "core_continuity_requirements": [
                    "runtime/state/life_state.json#self_model.old_self_anchors",
                    "runtime/state/life_state.json#memory_index.replay_cues",
                ],
                "archive_requirement": "required_before_activation",
                "candidate_routes": list(growth_route.get("candidate_routes", [])),
            }
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }
