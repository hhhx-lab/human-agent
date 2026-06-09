from __future__ import annotations

from typing import Any

from life_v0.membrane.queue_e_signals import queue_e_signal_profile_from_replay_cue_bundle


SOURCE_DOC_REFS = [
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md",
]


def build_belief_learning_plan(
    *,
    run_id: str,
    generated_at: str,
    learning_window: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
    self_read_report: dict[str, Any],
) -> dict[str, Any]:
    queue_e_signal_profile = queue_e_signal_profile_from_replay_cue_bundle(replay_cue_bundle)
    belief_targets = ["prediction_weight_recalibration", "continuity_preserving_belief_revision"]
    if replay_cue_bundle.get("pain_regret_residue_refs"):
        belief_targets.append("regret_sensitive_counterfactual_update")
    if queue_e_signal_profile["repair_followup_required"]:
        belief_targets.append("repair_accountability_belief_revision")
    if queue_e_signal_profile["queue_e_priority_band"] == "locked_repair_urgent":
        belief_targets.append("confirmation_locked_contact_model_revision")
    return {
        "schema_version": "belief_learning_plan_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "BeliefLearningPlan",
        "belief_learning_id": f"belief-learning-{run_id}",
        "window_status": learning_window.get("window_status", "guarded_pre_activation"),
        "belief_targets": belief_targets,
        "evidence_inputs": list(replay_cue_bundle.get("turn_residue_refs", []))
        + list(replay_cue_bundle.get("pain_regret_residue_refs", [])),
        "growth_pressure_refs": list(self_read_report.get("growth_pressures", [])),
        "continuity_guard_refs": [
            "runtime/state/life_state.json#self_model",
            "runtime/state/direction/direction_lock.json",
        ],
        "world_contact_release_posture": queue_e_signal_profile["world_contact_release_posture"],
        "repair_followup_required": queue_e_signal_profile["repair_followup_required"],
        "repair_obligation_count": queue_e_signal_profile["repair_obligation_count"],
        "regret_pressure_count": queue_e_signal_profile["regret_pressure_count"],
        "queue_e_priority_band": queue_e_signal_profile["queue_e_priority_band"],
        "blocked_learning_modes": list(learning_window.get("blocked_learning_modes", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_belief_learning_plan(plan: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if plan.get("schema_version") != "belief_learning_plan_v0":
        reasons.append("belief_learning_gate schema mismatch")
    if plan.get("object_kind") != "BeliefLearningPlan":
        reasons.append("belief_learning_gate object kind mismatch")
    for field in [
        "belief_learning_id",
        "window_status",
        "belief_targets",
        "evidence_inputs",
        "continuity_guard_refs",
    ]:
        if not plan.get(field):
            reasons.append(f"belief_learning_gate missing {field}")
    return reasons
