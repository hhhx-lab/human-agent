from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/40_self_relationship_model_audit_protocol.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_trait_drift_monitor(
    *,
    run_id: str,
    generated_at: str,
    episode: dict[str, Any],
    life_state: dict[str, Any],
) -> dict[str, Any]:
    old_self_anchors = list(life_state.get("self_model", {}).get("old_self_anchors", []))
    return {
        "schema_version": "trait_drift_monitor_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "trait_drift_id": f"trait-drift-{run_id}",
        "slow_variable_targets": [
            "trust_persistence",
            "dialogue_warmth",
            "repair_seriousness",
        ],
        "drift_direction": "guarded_stability",
        "required_anchor_refs": old_self_anchors or ["runtime/state/life_state.json#self_model.old_self_anchors"],
        "blocked_update_refs": [],
        "archive_requirement": "required_before_trait_commit",
        "episode_ref": "runtime/state/body/affective_episode.json",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_trait_drift_monitor(trait_drift: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if trait_drift.get("schema_version") != "trait_drift_monitor_v0":
        reasons.append("trait_drift_gate schema mismatch")
    for field in [
        "trait_drift_id",
        "slow_variable_targets",
        "drift_direction",
        "required_anchor_refs",
        "archive_requirement",
    ]:
        if not trait_drift.get(field):
            reasons.append(f"trait_drift_gate missing {field}")
    return reasons
