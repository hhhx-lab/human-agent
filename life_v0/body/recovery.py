from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/37_life_support_layer_policy.md",
    "docs/38_defense_layer_and_boundary_policy.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_recovery_path(
    *,
    run_id: str,
    generated_at: str,
    need_state: dict[str, Any],
) -> dict[str, Any]:
    recovery_priority = [
        "direction_lock_continuity",
        "dream_fact_integrity",
        "responsibility_repair_integrity",
        "anti_forgetting_replay_protection",
        "language_relationship_continuity",
    ]
    blocked_reasons: list[str] = []
    if need_state.get("cognitive_bandwidth") == "narrow_guarded":
        blocked_reasons.append("cognitive_bandwidth_is_narrow")
    return {
        "schema_version": "recovery_path_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "recovery_id": f"recovery-path-{run_id}",
        "recovery_priority": recovery_priority,
        "repair_targets": [
            "runtime/state/direction/direction_lock.json",
            "runtime/state/membrane/dream_fact_boundary.json",
            "runtime/state/membrane/responsibility_repair_boundary.json",
            "runtime/state/growth/anti_forgetting_anchor_index.json",
        ],
        "blocked_reasons": blocked_reasons,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_recovery_path(recovery_path: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if recovery_path.get("schema_version") != "recovery_path_v0":
        reasons.append("recovery_path_gate schema mismatch")
    for field in ["recovery_id", "recovery_priority", "repair_targets"]:
        if not recovery_path.get(field):
            reasons.append(f"recovery_path_gate missing {field}")
    return reasons
