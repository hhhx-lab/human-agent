from __future__ import annotations

from typing import Any

from life_v0.membrane.queue_e_signals import queue_e_signal_profile_from_replay_cue_bundle


SOURCE_DOC_REFS = [
    "docs/86_language_neuroscience_pragmatics_and_inner_speech.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md",
]


def build_language_learning_plan(
    *,
    run_id: str,
    generated_at: str,
    learning_window: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
    self_read_report: dict[str, Any],
) -> dict[str, Any]:
    queue_e_signal_profile = queue_e_signal_profile_from_replay_cue_bundle(replay_cue_bundle)
    language_targets = [
        "shared_terms_alignment",
        "repair_language_refinement",
        "dream_report_expression_refinement",
    ]
    if queue_e_signal_profile["repair_followup_required"]:
        language_targets.append("apology_repair_expression_refinement")
    if queue_e_signal_profile["queue_e_priority_band"] == "locked_repair_urgent":
        language_targets.append("confirmation_locked_expression_restraint")
    return {
        "schema_version": "language_learning_plan_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "LanguageLearningPlan",
        "language_learning_id": f"language-learning-{run_id}",
        "window_status": learning_window.get("window_status", "guarded_pre_activation"),
        "language_targets": language_targets,
        "continuity_inputs": list(replay_cue_bundle.get("relationship_residue_refs", []))
        + list(replay_cue_bundle.get("turn_residue_refs", [])),
        "protected_language_refs": [
            "runtime/state/language/language_relationship_state.json",
            "runtime/state/growth/anti_forgetting_replay_plan.json",
        ],
        "growth_pressure_refs": list(self_read_report.get("growth_pressures", [])),
        "world_contact_release_posture": queue_e_signal_profile["world_contact_release_posture"],
        "repair_followup_required": queue_e_signal_profile["repair_followup_required"],
        "repair_obligation_count": queue_e_signal_profile["repair_obligation_count"],
        "regret_pressure_count": queue_e_signal_profile["regret_pressure_count"],
        "queue_e_priority_band": queue_e_signal_profile["queue_e_priority_band"],
        "blocked_learning_modes": list(learning_window.get("blocked_learning_modes", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_language_learning_plan(plan: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if plan.get("schema_version") != "language_learning_plan_v0":
        reasons.append("language_learning_gate schema mismatch")
    if plan.get("object_kind") != "LanguageLearningPlan":
        reasons.append("language_learning_gate object kind mismatch")
    for field in [
        "language_learning_id",
        "window_status",
        "language_targets",
        "continuity_inputs",
        "protected_language_refs",
    ]:
        if not plan.get(field):
            reasons.append(f"language_learning_gate missing {field}")
    return reasons
