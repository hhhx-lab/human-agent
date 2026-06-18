from __future__ import annotations

from typing import Any

BODY_INTEGRATOR_CONTINUOUS_REF = (
    "runtime/state/body/body_integrator_state.json#continuous"
)

PATCHABLE_INTEGRATOR_FIELDS = (
    "recovery_rate",
    "stress_pulse",
)

BLOCKED_PATCH_TARGET_REFS = (
    "runtime/state/direction/identity_root.json",
    "runtime/state/identity/life_name_registry.json",
    "runtime/state/memory/memory_write_gate.json",
    "runtime/state/dream/dream_fact_gate_decision.json",
    "runtime/state/membrane/dream_fact_boundary.json",
    "runtime/state/membrane/relationship_subject_boundary.json",
    "runtime/state/language/expression_monitor_state.json",
)

SOURCE_DOC_REFS = [
    "docs/v0/动力学升级/11_学习成长与防遗忘.md",
    "docs/93_self_training_kernel_growth_protocol.md",
]


def build_parameter_registry_snapshot(
    *,
    run_id: str,
    generated_at: str,
    body_integrator: dict[str, Any] | None = None,
) -> dict[str, Any]:
    continuous = (body_integrator or {}).get("continuous") or {}
    return {
        "schema_version": "dynamics_parameter_registry_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "patchable_integrator_fields": list(PATCHABLE_INTEGRATOR_FIELDS),
        "blocked_patch_target_refs": list(BLOCKED_PATCH_TARGET_REFS),
        "baseline_continuous": {
            field: continuous.get(field)
            for field in PATCHABLE_INTEGRATOR_FIELDS
            if continuous.get(field) is not None
        },
        "integrator_continuous_ref": BODY_INTEGRATOR_CONTINUOUS_REF,
        "promotion_policy": "replay_shadow_compare_required_before_live_apply",
        "identity_and_write_gate_mutation": "forbidden",
        "source_doc_refs": SOURCE_DOC_REFS,
    }