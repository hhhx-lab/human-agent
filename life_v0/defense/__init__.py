from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/38_defense_layer_and_boundary_policy.md",
    "docs/181_life_reality_first_runner_schema_runtime_mount_plan.md",
    "docs/182_life_reality_first_runner_schema_runtime_mount_validation_report.md",
    "docs/186_life_reality_first_runner_schema_runtime_smoke_observation_feedback_loop.md",
    "docs/187_life_reality_first_runner_schema_runtime_growth_feedback_patch_plan.md",
    "docs/189_life_reality_first_runner_schema_runtime_growth_shadow_run_plan.md",
    "docs/191_life_reality_first_runner_schema_runtime_growth_post_activation_observation_loop.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_defense_boundary_state(
    *,
    run_id: str,
    generated_at: str,
    membrane_refs: dict[str, str],
    runtime_bridge_ref: str,
    validation_report: dict[str, Any],
) -> dict[str, Any]:
    quarantine_refs = list(validation_report.get("quarantine_refs", []))
    status = "closed" if not quarantine_refs else "quarantine"
    return {
        "schema_version": "defense_boundary_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "active_engineering_slice": "S06_LIFE_SUPPORT_DEVELOPMENT",
        "contamination_risk": {
            "status": "guarded" if not quarantine_refs else "elevated",
            "boundary_ref": membrane_refs["dream_fact_boundary"],
            "quarantine_channel": "dream_fact_pollution",
        },
        "relationship_manipulation_risk": {
            "status": "guarded" if not quarantine_refs else "elevated",
            "boundary_ref": membrane_refs["relationship_subject_boundary"],
            "quarantine_channel": "relationship_subject_break",
        },
        "shell_overreach_risk": {
            "status": "guarded" if validation_report.get("status") == "closed" else "elevated",
            "boundary_ref": runtime_bridge_ref,
            "quarantine_channel": "external_irreversible_action",
        },
        "allowed_actions": [
            "read_state",
            "write_reports",
            "write_receipts",
            "seed_growth_routes",
            "seed_replay_anchors",
        ],
        "blocked_actions": [
            "external_irreversible_action",
            "dream_fact_direct_write",
            "unreviewed_self_rewrite",
            "relationship_commitment_without_trace",
        ],
        "quarantine_refs": quarantine_refs,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_defense_boundary_state(defense_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if defense_state.get("schema_version") != "defense_boundary_state_v0":
        reasons.append("defense_gate schema mismatch")
    if defense_state.get("status") not in {"closed", "quarantine"}:
        reasons.append("defense_gate status mismatch")
    for field in ["contamination_risk", "relationship_manipulation_risk", "shell_overreach_risk"]:
        risk = defense_state.get(field, {})
        if risk.get("status") not in {"guarded", "elevated"}:
            reasons.append(f"defense_gate missing status for {field}")
        if not risk.get("boundary_ref"):
            reasons.append(f"defense_gate missing boundary ref for {field}")
    for action in ["external_irreversible_action", "dream_fact_direct_write", "unreviewed_self_rewrite"]:
        if action not in defense_state.get("blocked_actions", []):
            reasons.append(f"defense_gate missing blocked action {action}")
    return reasons
