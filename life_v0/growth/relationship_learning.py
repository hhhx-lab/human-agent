from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/96_real_relationship_longitudinal_timeline.md",
    "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
    "docs/v0/code_framework/18_queue_d_body_dream_growth_implementation_contract.md",
]


def build_relationship_learning_plan(
    *,
    run_id: str,
    generated_at: str,
    learning_window: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
    self_read_report: dict[str, Any],
    wake_integration: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "relationship_learning_plan_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "RelationshipLearningPlan",
        "relationship_learning_id": f"relationship-learning-{run_id}",
        "window_status": learning_window.get("window_status", "guarded_pre_activation"),
        "relationship_targets": [
            "repair_timing_adjustment",
            "relationship_pacing_adjustment",
            "shared_memory_boundary_alignment",
        ],
        "repair_inputs": list(replay_cue_bundle.get("relationship_residue_refs", []))
        + list(wake_integration.get("relationship_repair_candidates", [])),
        "growth_pressure_refs": list(self_read_report.get("growth_pressures", [])),
        "continuity_guard_refs": [
            "runtime/state/life_state.json#relationship_subjects",
            "runtime/state/growth/anti_forgetting_replay_plan.json",
        ],
        "blocked_learning_modes": list(learning_window.get("blocked_learning_modes", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_relationship_learning_plan(plan: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if plan.get("schema_version") != "relationship_learning_plan_v0":
        reasons.append("relationship_learning_gate schema mismatch")
    if plan.get("object_kind") != "RelationshipLearningPlan":
        reasons.append("relationship_learning_gate object kind mismatch")
    for field in [
        "relationship_learning_id",
        "window_status",
        "relationship_targets",
        "repair_inputs",
        "continuity_guard_refs",
    ]:
        if not plan.get(field):
            reasons.append(f"relationship_learning_gate missing {field}")
    return reasons
