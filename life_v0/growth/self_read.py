from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]


def build_self_read_report(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
    growth_route: dict[str, Any],
    learning_window: dict[str, Any],
) -> dict[str, Any]:
    relationship_refs = list(life_state.get("relationship_subjects", []))
    growth_pressures: list[str] = []
    if replay_cue_bundle.get("turn_residue_refs"):
        growth_pressures.append("capability_gap")
    if replay_cue_bundle.get("relationship_residue_refs"):
        growth_pressures.append("relationship_gap")
    if replay_cue_bundle.get("pain_regret_residue_refs"):
        growth_pressures.append("pain_recovery_gap")
    if replay_cue_bundle.get("dream_entry_candidates"):
        growth_pressures.append("dream_consolidation_gap")
    if replay_cue_bundle.get("anti_forgetting_targets"):
        growth_pressures.append("architecture_incoherence")
    if not growth_pressures:
        growth_pressures.append("maintenance_review")

    recommended_growth_paths = list(growth_route.get("candidate_routes", [])) + list(
        learning_window.get("learning_modes", [])
    )

    return {
        "schema_version": "self_read_report_v0",
        "event_kind": "SelfReadReport",
        "report_id": f"self-read-{run_id}",
        "created_at": generated_at,
        "read_scope": [
            "memory",
            "language",
            "relationship",
            "state",
            "runtime",
            "architecture",
            "model_kernel",
        ],
        "trigger_refs": list(replay_cue_bundle.get("turn_residue_refs", []))[:2]
        + list(replay_cue_bundle.get("relationship_residue_refs", []))[:1]
        + list(replay_cue_bundle.get("pain_regret_residue_refs", []))[:1],
        "current_structure_summary": {
            "strengths": [
                "direction_locked_growth_route",
                "dream_replay_bridge_active",
                "relationship_language_continuity_present",
            ],
            "weak_paths": ["kernel_upgrade_not_probed", "offline_growth_not_promoted"],
            "overloaded_paths": ["relationship_repair" if relationship_refs else "turn_residue_review"],
            "stale_paths": ["architecture_patch_followup_pending"],
        },
        "growth_pressures": growth_pressures,
        "protected_core_refs": [
            "runtime/state/life_state.json#self_model",
            "runtime/state/life_state.json#responsibility_bindings",
            "runtime/state/life_state.json#dream_records",
        ],
        "uncertainty_map": {
            "kernel_capacity": "not_probed",
            "relationship_repair_outcome": "pending_wake_review",
            "dream_fact_promotion": "requires_fact_gate",
        },
        "recommended_growth_paths": recommended_growth_paths,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_self_read_report(report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if report.get("schema_version") != "self_read_report_v0":
        reasons.append("self_read_gate schema mismatch")
    if report.get("event_kind") != "SelfReadReport":
        reasons.append("self_read_gate event kind mismatch")
    for field in [
        "report_id",
        "read_scope",
        "growth_pressures",
        "protected_core_refs",
        "recommended_growth_paths",
    ]:
        if not report.get(field):
            reasons.append(f"self_read_gate missing {field}")
    return reasons
