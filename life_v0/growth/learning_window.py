from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/v0/code_framework/18_queue_d_body_dream_growth_implementation_contract.md",
]


def build_learning_window(
    *,
    run_id: str,
    generated_at: str,
    plasticity_state: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "learning_window_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "learning_window_id": f"learning-window-{run_id}",
        "window_status": "guarded_pre_activation",
        "learning_modes": [
            "belief_tuning",
            "language_style_adjustment",
            "relationship_pacing_adjustment",
        ],
        "replay_seed_refs": list(replay_cue_bundle.get("anti_forgetting_targets", [])),
        "plasticity_window_ref": "runtime/state/growth/plasticity_window_state.json",
        "blocked_learning_modes": [
            "self_training",
            "kernel_upgrade",
        ]
        if not plasticity_state.get("self_training_allowed")
        else [],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_learning_window(learning_window: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if learning_window.get("schema_version") != "learning_window_v0":
        reasons.append("learning_window_gate schema mismatch")
    for field in [
        "learning_window_id",
        "window_status",
        "learning_modes",
        "replay_seed_refs",
        "plasticity_window_ref",
    ]:
        if not learning_window.get(field):
            reasons.append(f"learning_window_gate missing {field}")
    return reasons
