from __future__ import annotations

import json
import os
from typing import Any, Mapping

from life_v0.dynamics.parameter_registry import (
    BLOCKED_PATCH_TARGET_REFS,
    PATCHABLE_INTEGRATOR_FIELDS,
    build_parameter_registry_snapshot,
)
from life_v0.membrane.queue_e_signals import (
    queue_e_repair_modulation_profile_from_replay_cue_bundle,
)


SOURCE_DOC_REFS = [
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/187_life_reality_first_runner_schema_runtime_growth_feedback_patch_plan.md",
    "docs/188_life_reality_first_runner_schema_runtime_growth_archive_receipt_batch.md",
    "docs/189_life_reality_first_runner_schema_runtime_growth_shadow_run_plan.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
    "docs/v0/动力学升级/11_学习成长与防遗忘.md",
]

INTEGRATOR_PARAMETER_PATCH_FAMILY = "integrator_parameter_patch"
MAX_INTEGRATOR_PATCH_DELTA = 0.02


def is_integrator_parameter_patch_enabled(environ: Mapping[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return _parse_bool(env.get("DIGITAL_LIFE_INTEGRATOR_PARAMETER_PATCH"), False)


def build_growth_patch_queue(
    *,
    run_id: str,
    generated_at: str,
    growth_route: dict[str, Any],
    anchor_index: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "growth_patch_queue_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "queued_guarded",
        "queued_patch_families": [
            "anti_forgetting_replay_patch",
            "dream_reconsolidation_patch",
            "responsibility_repair_patch",
            "language_relationship_patch",
        ],
        "candidate_routes": list(growth_route.get("candidate_routes", [])),
        "anchor_ref_count": sum(len(value) for value in anchor_index.get("anchor_families", {}).values()),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_growth_patch_candidate_queue(
    *,
    run_id: str,
    generated_at: str,
    replay_cue_bundle: dict[str, Any],
    growth_route: dict[str, Any],
    learning_window: dict[str, Any],
) -> dict[str, Any]:
    repair_profile = queue_e_repair_modulation_profile_from_replay_cue_bundle(
        replay_cue_bundle
    )
    return {
        "schema_version": "growth_patch_candidate_queue_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "candidates": [
            {
                "growth_patch_candidate_id": f"growth-patch-candidate-{run_id}-0001",
                "source_residue_refs": list(replay_cue_bundle.get("turn_residue_refs", [])),
                "plasticity_window_ref": "runtime/state/growth/plasticity_window_state.json",
                "learning_window_ref": "runtime/state/growth/learning_window.json",
                "risk_flags": [
                    "direction_lock_required",
                    "archive_before_activation",
                    *(
                        ["queue_e_repair_modulation_required"]
                        if repair_profile["pressure_level"] in {"urgent", "elevated"}
                        else []
                    ),
                ],
                "anti_forgetting_requirements": list(replay_cue_bundle.get("anti_forgetting_targets", [])),
                "queue_e_repair_modulation_profile": repair_profile,
                "queue_e_repair_pressure_level": repair_profile["pressure_level"],
                "queue_e_repair_attention_target": repair_profile["attention_target"],
                "queue_e_repair_ref_set": list(repair_profile.get("ref_set", [])),
                "core_continuity_requirements": [
                    "runtime/state/life_state.json#self_model.old_self_anchors",
                    "runtime/state/life_state.json#memory_index.replay_cues",
                ],
                "archive_requirement": "required_before_activation",
                "candidate_routes": list(growth_route.get("candidate_routes", [])),
            }
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def maybe_extend_growth_patch_queue_with_integrator_family(
    growth_patch_queue: dict[str, Any],
    *,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    if not is_integrator_parameter_patch_enabled(environ):
        return growth_patch_queue or {}
    updated = json.loads(json.dumps(growth_patch_queue or {}))
    families = list(updated.get("queued_patch_families", []))
    if INTEGRATOR_PARAMETER_PATCH_FAMILY not in families:
        families.append(INTEGRATOR_PARAMETER_PATCH_FAMILY)
    updated["queued_patch_families"] = families
    updated["integrator_parameter_patch_enabled"] = True
    return updated


def maybe_append_integrator_parameter_patch_candidate(
    *,
    candidate_queue: dict[str, Any],
    body_integrator: dict[str, Any] | None = None,
    self_read_report: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    run_id: str,
    generated_at: str,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    if not is_integrator_parameter_patch_enabled(environ):
        return candidate_queue or {}
    candidate = build_integrator_parameter_patch_candidate(
        body_integrator=body_integrator,
        self_read_report=self_read_report,
        replay_cue_bundle=replay_cue_bundle,
        run_id=run_id,
        generated_at=generated_at,
    )
    blocked = validate_integrator_parameter_patch_candidate(candidate)
    if blocked:
        return candidate_queue or {}

    updated = json.loads(json.dumps(candidate_queue or {}))
    candidates = list(updated.get("candidates", []))
    candidates.append(candidate)
    updated["candidates"] = candidates
    updated["integrator_parameter_patch_applied"] = True
    return updated


def build_integrator_parameter_patch_candidate(
    *,
    body_integrator: dict[str, Any] | None = None,
    self_read_report: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    from life_v0.body.body_integrator import build_body_integrator_state

    integrator = body_integrator or build_body_integrator_state(
        run_id=run_id,
        generated_at=generated_at,
    )
    continuous = dict(integrator.get("continuous") or {})
    baseline = {
        field: float(continuous.get(field, 0.0) or 0.0)
        for field in PATCHABLE_INTEGRATOR_FIELDS
    }
    proposed = dict(baseline)
    patch_deltas = _propose_integrator_patch_deltas(
        baseline=baseline,
        self_read_report=self_read_report,
        replay_cue_bundle=replay_cue_bundle,
    )
    for field, delta in patch_deltas.items():
        proposed[field] = _clamp(
            float(proposed.get(field, 0.0)) + float(delta),
            0.0,
            1.0,
        )

    shadow_compare = compare_integrator_parameter_patch_shadow(
        baseline_continuous=baseline,
        proposed_continuous=proposed,
        run_id=run_id,
        generated_at=generated_at,
    )
    registry = build_parameter_registry_snapshot(
        run_id=run_id,
        generated_at=generated_at,
        body_integrator=integrator,
    )
    return {
        "growth_patch_candidate_id": f"integrator-parameter-patch-{run_id}",
        "patch_kind": INTEGRATOR_PARAMETER_PATCH_FAMILY,
        "patch_family": INTEGRATOR_PARAMETER_PATCH_FAMILY,
        "shadow_only": True,
        "promotion_gate": "replay_shadow_compare_required",
        "target_ref": registry["integrator_continuous_ref"],
        "parameter_registry_ref": "runtime/state/growth/dynamics_parameter_registry.json",
        "baseline_continuous": baseline,
        "proposed_continuous": proposed,
        "patch_deltas": patch_deltas,
        "blocked_patch_targets_checked": list(BLOCKED_PATCH_TARGET_REFS),
        "core_gate_status": "passed",
        "identity_or_write_gate_mutation": False,
        "shadow_compare": shadow_compare,
        "plasticity_window_ref": "runtime/state/growth/plasticity_window_state.json",
        "learning_window_ref": "runtime/state/growth/learning_window.json",
        "risk_flags": [
            "direction_lock_required",
            "archive_before_activation",
            "integrator_parameter_shadow_only",
        ],
        "archive_requirement": "required_before_activation",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def validate_integrator_parameter_patch_candidate(
    candidate: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if candidate.get("patch_kind") != INTEGRATOR_PARAMETER_PATCH_FAMILY:
        reasons.append("integrator_parameter_patch kind mismatch")
    if candidate.get("identity_or_write_gate_mutation"):
        reasons.append("integrator_parameter_patch identity/write_gate mutation forbidden")
    if candidate.get("core_gate_status") != "passed":
        reasons.append("integrator_parameter_patch core gate not passed")

    target_ref = str(candidate.get("target_ref") or "")
    for blocked in BLOCKED_PATCH_TARGET_REFS:
        if blocked in target_ref:
            reasons.append(f"integrator_parameter_patch blocked target {blocked}")

    patch_deltas = candidate.get("patch_deltas") or {}
    if not isinstance(patch_deltas, dict) or not patch_deltas:
        reasons.append("integrator_parameter_patch missing patch_deltas")
    for field in patch_deltas:
        if field not in PATCHABLE_INTEGRATOR_FIELDS:
            reasons.append(f"integrator_parameter_patch non_patchable_field:{field}")
        delta = patch_deltas[field]
        if not isinstance(delta, (int, float)):
            reasons.append(f"integrator_parameter_patch invalid_delta:{field}")
        elif abs(float(delta)) > MAX_INTEGRATOR_PATCH_DELTA:
            reasons.append(f"integrator_parameter_patch delta_too_large:{field}")

    shadow_compare = candidate.get("shadow_compare") or {}
    if shadow_compare.get("status") not in {"passed", "marginal"}:
        reasons.append("integrator_parameter_patch shadow_compare not passed")
    return reasons


def compare_integrator_parameter_patch_shadow(
    *,
    baseline_continuous: dict[str, Any],
    proposed_continuous: dict[str, Any],
    run_id: str,
    generated_at: str,
    tick_count: int = 24,
    dt_ms: int = 3_600_000,
) -> dict[str, Any]:
    from life_v0.body.body_integrator import build_body_integrator_state

    baseline_integrator = build_body_integrator_state(run_id=run_id, generated_at=generated_at)
    proposed_integrator = json.loads(json.dumps(baseline_integrator))
    baseline_integrator["continuous"] = {
        **dict(baseline_integrator.get("continuous") or {}),
        **{k: float(v) for k, v in baseline_continuous.items()},
    }
    proposed_integrator["continuous"] = {
        **dict(proposed_integrator.get("continuous") or {}),
        **{k: float(v) for k, v in proposed_continuous.items()},
    }

    baseline_final = _simulate_integrator_ticks(
        baseline_integrator,
        generated_at=generated_at,
        tick_count=tick_count,
        dt_ms=dt_ms,
    )
    proposed_final = _simulate_integrator_ticks(
        proposed_integrator,
        generated_at=generated_at,
        tick_count=tick_count,
        dt_ms=dt_ms,
    )
    baseline_sleep = float((baseline_final.get("continuous") or {}).get("sleep_pressure", 0.0))
    proposed_sleep = float((proposed_final.get("continuous") or {}).get("sleep_pressure", 0.0))
    baseline_bandwidth = float(
        (baseline_final.get("continuous") or {}).get("cognitive_bandwidth", 0.0)
    )
    proposed_bandwidth = float(
        (proposed_final.get("continuous") or {}).get("cognitive_bandwidth", 0.0)
    )
    sleep_delta = proposed_sleep - baseline_sleep
    bandwidth_delta = proposed_bandwidth - baseline_bandwidth
    improved = sleep_delta <= 0.0 and bandwidth_delta >= 0.0
    status = "passed" if improved else "marginal" if bandwidth_delta >= -0.02 else "failed"

    return {
        "schema_version": "integrator_parameter_patch_shadow_compare_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "simulated_ticks": tick_count,
        "dt_ms": dt_ms,
        "baseline_final_continuous": baseline_final.get("continuous") or {},
        "proposed_final_continuous": proposed_final.get("continuous") or {},
        "sleep_pressure_delta": round(sleep_delta, 4),
        "cognitive_bandwidth_delta": round(bandwidth_delta, 4),
        "improved_recovery_posture": improved,
        "shadow_apply_boundary": "shadow_compare_only_not_live_integrator_write",
    }


def _propose_integrator_patch_deltas(
    *,
    baseline: dict[str, float],
    self_read_report: dict[str, Any] | None,
    replay_cue_bundle: dict[str, Any] | None,
) -> dict[str, float]:
    pressures = set((self_read_report or {}).get("growth_pressures") or [])
    if "architecture_incoherence" in pressures:
        return {}
    if "pain_recovery_gap" in pressures or "capability_gap" in pressures:
        return {"recovery_rate": min(MAX_INTEGRATOR_PATCH_DELTA, 0.01)}
    if (replay_cue_bundle or {}).get("anti_forgetting_targets"):
        return {"stress_pulse": -min(MAX_INTEGRATOR_PATCH_DELTA, 0.01)}
    if baseline.get("recovery_rate", 0.0) < 0.1:
        return {"recovery_rate": 0.005}
    return {}


def _simulate_integrator_ticks(
    integrator: dict[str, Any],
    *,
    generated_at: str,
    tick_count: int,
    dt_ms: int,
) -> dict[str, Any]:
    from life_v0.body.body_integrator import integrate_body_state

    updated = json.loads(json.dumps(integrator))
    for tick in range(1, tick_count + 1):
        updated = integrate_body_state(
            integrator=updated,
            generated_at=f"{generated_at}+shadow{tick:03d}",
            mode="background",
            dt_ms=dt_ms,
            recovery_event=tick % 6 == 0,
        )
    return updated


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _parse_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default
