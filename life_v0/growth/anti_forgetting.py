from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]


def build_anti_forgetting_replay_plan(
    *,
    run_id: str,
    generated_at: str,
    anchor_index: dict[str, Any],
    self_read_report: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
) -> dict[str, Any]:
    anchor_families = anchor_index.get("anchor_families", {})
    replay_sets = {
        "core_self_replay": list(anchor_families.get("old_self", [])),
        "relationship_replay": list(anchor_families.get("old_relationship", []))
        + list(replay_cue_bundle.get("relationship_residue_refs", [])),
        "memory_integrity_replay": list(anchor_families.get("old_dream", []))
        + list(replay_cue_bundle.get("turn_residue_refs", [])),
        "capability_replay": list(anchor_families.get("old_language", [])),
        "pain_regret_replay": list(anchor_families.get("old_responsibility", []))
        + list(replay_cue_bundle.get("pain_regret_residue_refs", [])),
        "dream_replay": list(replay_cue_bundle.get("dream_entry_candidates", []))
        + list(anchor_families.get("old_dream", [])),
    }
    return {
        "schema_version": "anti_forgetting_replay_plan_v0",
        "event_kind": "AntiForgettingReplayPlan",
        "plan_id": f"anti-forgetting-{run_id}",
        "created_at": generated_at,
        "source_self_read_ref": "runtime/state/growth/self_read_report.json",
        "replay_sets": replay_sets,
        "expected_results": {
            "core_self_replay": "preserve self-model continuity",
            "relationship_replay": "preserve relationship boundary and repair history",
            "memory_integrity_replay": "preserve lifecycle semantics and replay anchors",
            "capability_replay": "preserve old language and runtime capability traces",
            "pain_regret_replay": "preserve pain, regret, and responsibility linkage",
            "dream_replay": "preserve dream marker and wake-review routing",
        },
        "blocked_update_refs": list(self_read_report.get("protected_core_refs", [])),
        "promotion_barrier": "archive_before_activation",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_anti_forgetting_replay_plan(plan: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if plan.get("schema_version") != "anti_forgetting_replay_plan_v0":
        reasons.append("anti_forgetting_plan_gate schema mismatch")
    if plan.get("event_kind") != "AntiForgettingReplayPlan":
        reasons.append("anti_forgetting_plan_gate event kind mismatch")
    replay_sets = plan.get("replay_sets", {})
    for field in [
        "core_self_replay",
        "relationship_replay",
        "memory_integrity_replay",
        "capability_replay",
        "pain_regret_replay",
        "dream_replay",
    ]:
        if field not in replay_sets or not replay_sets.get(field):
            reasons.append(f"anti_forgetting_plan_gate missing {field}")
    return reasons
