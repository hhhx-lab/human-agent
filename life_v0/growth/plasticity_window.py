from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/40_self_relationship_model_audit_protocol.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]


def build_plasticity_window_state(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    validation_report_ref: str,
    schema_report_ref: str,
    schema_smoke_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "plasticity_window_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": "S06_LIFE_SUPPORT_DEVELOPMENT",
        "window_status": "guarded_pre_activation",
        "slow_variable_update_mode": "bounded_by_direction_lock",
        "self_training_allowed": False,
        "kernel_upgrade_allowed": False,
        "required_anchor_refs": [
            "runtime/state/life_state.json#self_model.old_self_anchors",
            "runtime/state/life_state.json#memory_index.replay_cues",
        ],
        "required_archive_refs": list(life_state.get("archive_refs", [])),
        "validation_report_refs": [
            validation_report_ref,
            schema_report_ref,
            schema_smoke_ref,
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_plasticity_window_state(plasticity_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if plasticity_state.get("schema_version") != "plasticity_window_state_v0":
        reasons.append("plasticity_gate schema mismatch")
    if plasticity_state.get("window_status") != "guarded_pre_activation":
        reasons.append("plasticity_gate window status mismatch")
    if plasticity_state.get("self_training_allowed"):
        reasons.append("plasticity_gate self training must stay blocked")
    if plasticity_state.get("kernel_upgrade_allowed"):
        reasons.append("plasticity_gate kernel upgrade must stay blocked")
    for ref in [
        "runtime/state/life_state.json#self_model.old_self_anchors",
        "runtime/state/life_state.json#memory_index.replay_cues",
    ]:
        if ref not in plasticity_state.get("required_anchor_refs", []):
            reasons.append(f"plasticity_gate missing anchor ref {ref}")
    return reasons
