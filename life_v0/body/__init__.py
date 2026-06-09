from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from life_v0.body.core_affect import build_core_affect_vector, check_core_affect_vector
from life_v0.body.emotion_episode import build_affective_episode, check_affective_episode
from life_v0.body.emotion_regulation import (
    build_emotion_regulation_loop,
    check_emotion_regulation_loop,
)
from life_v0.body.need_state import build_need_state_vector, check_need_state_vector
from life_v0.body.recovery import build_recovery_path, check_recovery_path
from life_v0.body.resource_budget import build_body_resource_budget
from life_v0.body.rhythm import build_body_rhythm_pulse, check_body_rhythm_pulse
from life_v0.body.trait_drift import build_trait_drift_monitor, check_trait_drift_monitor
from life_v0.defense import (
    SOURCE_DOC_REFS as DEFENSE_DOC_REFS,
    build_defense_boundary_state,
    check_defense_boundary_state,
)
from life_v0.growth import (
    SOURCE_DOC_REFS as GROWTH_DOC_REFS,
    build_anti_forgetting_anchor_index,
    build_plasticity_window_state,
    build_self_growth_route,
    check_anti_forgetting_anchor_index,
    check_plasticity_window_state,
    check_self_growth_route,
)


ACTIVE_SLICE = "S06_LIFE_SUPPORT_DEVELOPMENT"
NEXT_ALLOWED_SLICES = ["S10_RUNTIME_GROWTH_RECONSOLIDATION"]
NEXT_REQUIRED_COMMAND = "life-v0 run-cycle --shadow-only --strict"

BODY_DOC_REFS = [
    "docs/37_life_support_layer_policy.md",
    "docs/38_defense_layer_and_boundary_policy.md",
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/40_self_relationship_model_audit_protocol.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
    "docs/181_life_reality_first_runner_schema_runtime_mount_plan.md",
    "docs/182_life_reality_first_runner_schema_runtime_mount_validation_report.md",
    "docs/183_life_reality_first_runner_schema_runtime_smoke_fixture_plan.md",
    "docs/184_life_reality_first_runner_schema_runtime_smoke_repair_queue.md",
    "docs/185_life_reality_first_runner_schema_runtime_smoke_archive_receipt_batch.md",
    "docs/186_life_reality_first_runner_schema_runtime_smoke_observation_feedback_loop.md",
    "docs/187_life_reality_first_runner_schema_runtime_growth_feedback_patch_plan.md",
    "docs/188_life_reality_first_runner_schema_runtime_growth_archive_receipt_batch.md",
    "docs/189_life_reality_first_runner_schema_runtime_growth_shadow_run_plan.md",
    "docs/190_life_reality_first_runner_schema_runtime_growth_activation_report_plan.md",
    "docs/191_life_reality_first_runner_schema_runtime_growth_post_activation_observation_loop.md",
    "docs/192_life_reality_first_runner_schema_runtime_growth_activation_archive_receipt_batch.md",
    "docs/193_life_reality_first_runner_schema_runtime_growth_consolidation_cycle_plan.md",
    "docs/194_life_reality_first_runner_schema_runtime_growth_next_feedback_seed_plan.md",
    "docs/195_life_reality_first_runner_schema_runtime_growth_replay_shadow_seed_plan.md",
    "docs/196_life_reality_first_runner_schema_runtime_growth_second_cycle_patch_plan.md",
    "docs/197_life_reality_first_runner_schema_runtime_growth_second_cycle_archive_plan.md",
    "docs/198_life_reality_first_runner_schema_runtime_growth_cycle_closure_validation_plan.md",
    "docs/199_life_reality_first_runner_schema_runtime_growth_third_cycle_seed_plan.md",
    "docs/200_life_reality_first_runner_schema_runtime_growth_longitudinal_cycle_audit_plan.md",
    "docs/201_life_reality_first_runner_schema_runtime_growth_longitudinal_drift_repair_plan.md",
    "docs/202_life_reality_first_runner_schema_runtime_growth_longitudinal_repair_archive_plan.md",
    "docs/203_life_reality_first_runner_schema_runtime_growth_replay_shadow_reentry_plan.md",
    "docs/204_life_reality_first_runner_schema_runtime_growth_post_repair_cycle_validation_plan.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/shared_contracts/life_state_store_v0_schema.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]

S06_SOURCE_DOCS = sorted(set(BODY_DOC_REFS + DEFENSE_DOC_REFS + GROWTH_DOC_REFS))
READ_ME_BLOCK_REFS = [
    "B09_LIFE_SUPPORT_DEFENSE_DEVELOPMENT",
    "B23_NINE_LIFE_TARGETS",
    "B29_RUNTIME_MOUNT_GROWTH",
]
RUNTIME_CARRIERS = [
    "LifeSupportDefenseRuntime",
    "ActivationGrowthRuntime",
    "GrowthReplayRuntime",
]


@dataclass(frozen=True)
class LifeSupportResult:
    exit_code: int
    report: dict[str, Any]


def run_life_support(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    validation_report_path: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> LifeSupportResult:
    run_id = run_id or _default_run_id()
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    state_dir = state_dir.resolve()
    validation_report_path = validation_report_path.resolve()
    out_dir = out_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    body_dir = out_dir / "body"
    growth_dir = out_dir / "growth"
    defense_dir = out_dir / "defense"

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"input path is not a directory: {docs_dir}")
    if not doc_index_path.exists():
        blocked_reasons.append(f"doc carrier index is missing: {doc_index_path}")
    if not validation_report_path.exists():
        blocked_reasons.append(f"validation report is missing: {validation_report_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "state_store_gate")
    direction_lock = _load_json(state_dir / "direction" / "direction_lock.json", blocked_reasons, "direction_lock_gate")
    dream_fact = _load_json(state_dir / "membrane" / "dream_fact_boundary.json", blocked_reasons, "dream_fact_gate")
    relationship = _load_json(state_dir / "membrane" / "relationship_subject_boundary.json", blocked_reasons, "relationship_subject_gate")
    responsibility = _load_json(state_dir / "membrane" / "responsibility_repair_boundary.json", blocked_reasons, "responsibility_gate")
    runtime_bridge = _load_json(state_dir / "objects" / "runtime_bridge_boundary.json", blocked_reasons, "runtime_bridge_gate")
    validation_report = _load_json(validation_report_path, blocked_reasons, "validation_membrane_gate") if validation_report_path.exists() else {}
    validation_check = _load_json(reports_dir / "validation_membrane_check_report.json", blocked_reasons, "validation_check_gate")
    schema_report = _load_json(reports_dir / "schema_runner_report.json", blocked_reasons, "schema_runner_gate")
    schema_check = _load_json(reports_dir / "schema_runner_check_report.json", blocked_reasons, "schema_runner_check_gate")
    schema_smoke = _load_json(reports_dir / "schema_smoke_report.json", blocked_reasons, "schema_smoke_gate")

    blocked_reasons.extend(_doc_blockers(doc_index))
    blocked_reasons.extend(_state_blockers(life_state, direction_lock))
    blocked_reasons.extend(
        _previous_slice_blockers(
            validation_report=validation_report,
            validation_check=validation_check,
            schema_report=schema_report,
            schema_check=schema_check,
            schema_smoke=schema_smoke,
        )
    )
    blocked_reasons.extend(_boundary_blockers(dream_fact, relationship, responsibility, runtime_bridge))

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_next_slice" if status == "closed" else "block_activation"
    state_refs = [
        "runtime/state/body/need_state_vector.json",
        "runtime/state/body/body_rhythm_pulse.json",
        "runtime/state/body/body_resource_budget.json",
        "runtime/state/body/recovery_path.json",
        "runtime/state/body/core_affect_vector.json",
        "runtime/state/body/affective_episode.json",
        "runtime/state/body/emotion_regulation_loop.json",
        "runtime/state/body/trait_drift_monitor.json",
        "runtime/state/defense/defense_boundary_state.json",
        "runtime/state/growth/plasticity_window_state.json",
        "runtime/state/growth/self_growth_route.json",
        "runtime/state/growth/anti_forgetting_anchor_index.json",
        "runtime/state/growth/life_support_stage_gate.json",
    ]
    receipt_ref = f"runtime/receipts/life_support_development_{run_id}.json"

    membrane_refs = {
        "dream_fact_boundary": "runtime/state/membrane/dream_fact_boundary.json",
        "relationship_subject_boundary": "runtime/state/membrane/relationship_subject_boundary.json",
        "responsibility_repair_boundary": "runtime/state/membrane/responsibility_repair_boundary.json",
    }
    need_state = build_need_state_vector(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        validation_report=validation_report,
        schema_report=schema_report,
        schema_smoke=schema_smoke,
    )
    rhythm_pulse = build_body_rhythm_pulse(
        run_id=run_id,
        generated_at=generated_at,
        need_state=need_state,
        resource_budget={"fatigue_state": {"level": "managed_low_noise"}},
    )
    recovery_path = build_recovery_path(
        run_id=run_id,
        generated_at=generated_at,
        need_state=need_state,
    )
    body_budget = _build_body_resource_budget(
        run_id=run_id,
        generated_at=generated_at,
        validation_report=validation_report,
        schema_report=schema_report,
        schema_smoke=schema_smoke,
        life_state=life_state,
        need_state=need_state,
        rhythm_pulse=rhythm_pulse,
        recovery_path=recovery_path,
    )
    core_affect = build_core_affect_vector(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        need_state=need_state,
    )
    affective_episode = build_affective_episode(
        run_id=run_id,
        generated_at=generated_at,
        core_affect=core_affect,
        life_state=life_state,
    )
    emotion_regulation = build_emotion_regulation_loop(
        run_id=run_id,
        generated_at=generated_at,
        episode=affective_episode,
        recovery_path=recovery_path,
    )
    trait_drift = build_trait_drift_monitor(
        run_id=run_id,
        generated_at=generated_at,
        episode=affective_episode,
        life_state=life_state,
    )
    defense_state = build_defense_boundary_state(
        run_id=run_id,
        generated_at=generated_at,
        membrane_refs=membrane_refs,
        runtime_bridge_ref="runtime/state/objects/runtime_bridge_boundary.json",
        validation_report=validation_report,
    )
    plasticity_state = build_plasticity_window_state(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        validation_report_ref="runtime/reports/latest/validation_membrane_report.json",
        schema_report_ref="runtime/reports/latest/schema_runner_report.json",
        schema_smoke_ref="runtime/reports/latest/schema_smoke_report.json",
    )
    growth_route = build_self_growth_route(
        run_id=run_id,
        generated_at=generated_at,
        direction_lock_ref="runtime/state/direction/direction_lock.json",
        validation_report_ref="runtime/reports/latest/validation_membrane_report.json",
        schema_report_ref="runtime/reports/latest/schema_runner_report.json",
        next_runtime_command=NEXT_REQUIRED_COMMAND,
    )
    anchor_index = build_anti_forgetting_anchor_index(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        membrane_refs=membrane_refs,
    )
    stage_gate = _build_stage_gate(run_id, generated_at, status, stage_effect, blocked_reasons)
    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        state_refs=state_refs,
        receipt_ref=receipt_ref,
    )
    digest = _build_digest(run_id, generated_at, status, stage_effect, blocked_reasons, state_refs)
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        state_dir=state_dir,
        validation_report_path=validation_report_path,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        body_dir=body_dir,
        growth_dir=growth_dir,
        defense_dir=defense_dir,
        stage_effect=stage_effect,
    )

    try:
        body_dir.mkdir(parents=True, exist_ok=True)
        growth_dir.mkdir(parents=True, exist_ok=True)
        defense_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(body_dir / "need_state_vector.json", need_state)
        _write_json(body_dir / "body_rhythm_pulse.json", rhythm_pulse)
        _write_json(body_dir / "body_resource_budget.json", body_budget)
        _write_json(body_dir / "recovery_path.json", recovery_path)
        _write_json(body_dir / "core_affect_vector.json", core_affect)
        _write_json(body_dir / "affective_episode.json", affective_episode)
        _write_json(body_dir / "emotion_regulation_loop.json", emotion_regulation)
        _write_json(body_dir / "trait_drift_monitor.json", trait_drift)
        _write_json(defense_dir / "defense_boundary_state.json", defense_state)
        _write_json(growth_dir / "plasticity_window_state.json", plasticity_state)
        _write_json(growth_dir / "self_growth_route.json", growth_route)
        _write_json(growth_dir / "anti_forgetting_anchor_index.json", anchor_index)
        _write_json(growth_dir / "life_support_stage_gate.json", stage_gate)
        _write_json(reports_dir / "life_support_development_report.json", report)
        _write_json(reports_dir / "life_support_development_digest.json", digest)
        _write_json(receipts_dir / f"life_support_development_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return LifeSupportResult(exit_code=4, report=report)

    if status == "closed":
        return LifeSupportResult(exit_code=0, report=report)
    return LifeSupportResult(exit_code=1 if strict else 0, report=report)


def run_check_life_support(
    *,
    state_dir: Path,
    reports_dir: Path,
    strict: bool = False,
) -> LifeSupportResult:
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    generated_at = _now_iso()
    blocked_reasons: list[str] = []

    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "state_store_gate")
    need_state = _load_json(state_dir / "body" / "need_state_vector.json", blocked_reasons, "need_state_gate")
    rhythm_pulse = _load_json(state_dir / "body" / "body_rhythm_pulse.json", blocked_reasons, "body_rhythm_gate")
    body_budget = _load_json(state_dir / "body" / "body_resource_budget.json", blocked_reasons, "resource_budget_gate")
    recovery_path = _load_json(state_dir / "body" / "recovery_path.json", blocked_reasons, "recovery_path_gate")
    core_affect = _load_json(state_dir / "body" / "core_affect_vector.json", blocked_reasons, "core_affect_gate")
    affective_episode = _load_json(state_dir / "body" / "affective_episode.json", blocked_reasons, "affective_episode_gate")
    emotion_regulation = _load_json(
        state_dir / "body" / "emotion_regulation_loop.json",
        blocked_reasons,
        "emotion_regulation_gate",
    )
    trait_drift = _load_json(state_dir / "body" / "trait_drift_monitor.json", blocked_reasons, "trait_drift_gate")
    defense_state = _load_json(state_dir / "defense" / "defense_boundary_state.json", blocked_reasons, "defense_gate")
    plasticity_state = _load_json(state_dir / "growth" / "plasticity_window_state.json", blocked_reasons, "plasticity_gate")
    growth_route = _load_json(state_dir / "growth" / "self_growth_route.json", blocked_reasons, "self_growth_gate")
    anchor_index = _load_json(state_dir / "growth" / "anti_forgetting_anchor_index.json", blocked_reasons, "anti_forgetting_gate")
    stage_gate = _load_json(state_dir / "growth" / "life_support_stage_gate.json", blocked_reasons, "next_slice_gate")
    build_report = _load_json(reports_dir / "life_support_development_report.json", blocked_reasons, "build_report_gate")

    blocked_reasons.extend(_check_life_state(life_state))
    blocked_reasons.extend(check_need_state_vector(need_state))
    blocked_reasons.extend(check_body_rhythm_pulse(rhythm_pulse))
    blocked_reasons.extend(_check_body_resource_budget(body_budget))
    blocked_reasons.extend(check_recovery_path(recovery_path))
    blocked_reasons.extend(check_core_affect_vector(core_affect))
    blocked_reasons.extend(check_affective_episode(affective_episode))
    blocked_reasons.extend(check_emotion_regulation_loop(emotion_regulation))
    blocked_reasons.extend(check_trait_drift_monitor(trait_drift))
    blocked_reasons.extend(check_defense_boundary_state(defense_state))
    blocked_reasons.extend(check_plasticity_window_state(plasticity_state))
    blocked_reasons.extend(check_self_growth_route(growth_route, NEXT_REQUIRED_COMMAND))
    blocked_reasons.extend(check_anti_forgetting_anchor_index(anchor_index))
    blocked_reasons.extend(_check_stage_gate(stage_gate))
    blocked_reasons.extend(_check_build_report(build_report))

    status = "closed" if not blocked_reasons else "blocked"
    report = {
        "schema_version": "life_support_development_check_report_v0",
        "generated_at": generated_at,
        "status": status,
        "stage_effect": "allow_next_slice" if status == "closed" else "block_activation",
        "checked_state_dir": str(state_dir),
        "active_engineering_slice": ACTIVE_SLICE,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
    }

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "life_support_development_check_report.json", report)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"check_report_write_gate failed: {exc}")
        return LifeSupportResult(exit_code=4, report=report)

    if status == "closed":
        return LifeSupportResult(exit_code=0, report=report)
    return LifeSupportResult(exit_code=1 if strict else 0, report=report)


def _build_body_resource_budget(
    *,
    run_id: str,
    generated_at: str,
    validation_report: dict[str, Any],
    schema_report: dict[str, Any],
    schema_smoke: dict[str, Any],
    life_state: dict[str, Any],
    need_state: dict[str, Any],
    rhythm_pulse: dict[str, Any],
    recovery_path: dict[str, Any],
) -> dict[str, Any]:
    return build_body_resource_budget(
        run_id=run_id,
        generated_at=generated_at,
        validation_report=validation_report,
        schema_report=schema_report,
        schema_smoke=schema_smoke,
        life_state=life_state,
        need_state=need_state,
        rhythm_pulse=rhythm_pulse,
        recovery_path=recovery_path,
    )


def _build_stage_gate(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    gate_state = "closed" if status == "closed" else "blocked"
    return {
        "schema_version": "life_support_stage_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "decision": status,
        "stage_effect": stage_effect,
        "gates": {
            "resource_budget_gate": gate_state,
            "defense_gate": gate_state,
            "plasticity_gate": gate_state,
            "self_growth_gate": gate_state,
            "anti_forgetting_gate": gate_state,
            "next_slice_gate": gate_state,
        },
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    state_refs: list[str],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "s06_life_support_development_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "source_doc_refs": S06_SOURCE_DOCS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIERS,
        "state_refs": state_refs,
        "report_refs": [
            "runtime/reports/latest/validation_membrane_report.json",
            "runtime/reports/latest/schema_runner_report.json",
            "runtime/reports/latest/schema_smoke_report.json",
            "runtime/reports/latest/life_support_development_report.json",
        ],
        "receipt_refs": [receipt_ref],
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "replay_needed_refs": [] if status == "closed" else ["runtime/state/growth/anti_forgetting_anchor_index.json"],
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
    }


def _build_digest(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    state_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "life_support_development_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_slice": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "state_refs": state_refs,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "blocked_reasons": blocked_reasons,
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    validation_report_path: Path,
    reports_dir: Path,
    receipts_dir: Path,
    body_dir: Path,
    growth_dir: Path,
    defense_dir: Path,
    stage_effect: str,
) -> dict[str, Any]:
    input_hashes = {
        ref: _sha256(docs_dir.parent / ref)
        for ref in S06_SOURCE_DOCS
        if (docs_dir.parent / ref).exists()
    }
    for path in [
        doc_index_path,
        state_dir / "life_state.json",
        state_dir / "direction" / "direction_lock.json",
        state_dir / "membrane" / "dream_fact_boundary.json",
        state_dir / "membrane" / "relationship_subject_boundary.json",
        state_dir / "membrane" / "responsibility_repair_boundary.json",
        state_dir / "objects" / "runtime_bridge_boundary.json",
        validation_report_path,
        reports_dir / "validation_membrane_check_report.json",
        reports_dir / "schema_runner_report.json",
        reports_dir / "schema_runner_check_report.json",
        reports_dir / "schema_smoke_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)
    output_refs = [
        body_dir / "need_state_vector.json",
        body_dir / "body_rhythm_pulse.json",
        body_dir / "body_resource_budget.json",
        body_dir / "recovery_path.json",
        body_dir / "core_affect_vector.json",
        body_dir / "affective_episode.json",
        body_dir / "emotion_regulation_loop.json",
        body_dir / "trait_drift_monitor.json",
        defense_dir / "defense_boundary_state.json",
        growth_dir / "plasticity_window_state.json",
        growth_dir / "self_growth_route.json",
        growth_dir / "anti_forgetting_anchor_index.json",
        growth_dir / "life_support_stage_gate.json",
        reports_dir / "life_support_development_report.json",
        reports_dir / "life_support_development_digest.json",
        receipts_dir / f"life_support_development_{run_id}.json",
    ]
    return {
        "schema_version": "life_support_development_receipt_v0",
        "receipt_id": f"life_support_development_{run_id}",
        "run_id": run_id,
        "command": "build-life-support",
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_refs": [str(path) for path in output_refs],
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_refs},
        "stage_effect": stage_effect,
        "direction_lock_ref": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    }


def _doc_blockers(doc_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    documents = doc_index.get("documents", []) if isinstance(doc_index, dict) else []
    doc_paths = {doc.get("path") for doc in documents if isinstance(doc, dict)}
    missing = [ref for ref in S06_SOURCE_DOCS if ref not in doc_paths]
    if missing:
        reasons.append("doc_index_read_gate missing S06 docs: " + ", ".join(missing[:8]))
    return reasons


def _state_blockers(life_state: dict[str, Any], direction_lock: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("state_store_gate schema mismatch")
    if not life_state.get("self_model", {}).get("old_self_anchors"):
        reasons.append("state_store_gate old self anchors missing")
    if not life_state.get("memory_index", {}).get("replay_cues"):
        reasons.append("state_store_gate replay cues missing")
    if "language_state" not in life_state:
        reasons.append("state_store_gate language state missing")
    language_state = life_state.get("language_state", {})
    for field in [
        "shared_language_refs",
        "expression_monitor_refs",
        "relation_scope_refs",
        "promise_refs",
        "self_narrative_trace_refs",
        "language_percept_refs",
        "semantic_map_refs",
    ]:
        if not language_state.get(field):
            reasons.append(f"state_store_gate missing language continuity field {field}")
    if "runtime/state/prediction/prediction_workspace_frame.json" not in life_state.get("runtime_trace_refs", []):
        reasons.append("state_store_gate prediction workspace runtime trace missing")
    if direction_lock.get("schema_version") != "direction_lock_v0":
        reasons.append("direction_lock_gate schema mismatch")
    if direction_lock.get("stage_effect") not in {"allow_s01_when_closed", "allow_next_slice"}:
        reasons.append("direction_lock_gate stage effect mismatch")
    if not direction_lock.get("next_allowed_slices"):
        reasons.append("direction_lock_gate next allowed slices missing")
    return reasons


def _previous_slice_blockers(
    *,
    validation_report: dict[str, Any],
    validation_check: dict[str, Any],
    schema_report: dict[str, Any],
    schema_check: dict[str, Any],
    schema_smoke: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if validation_report.get("schema_version") != "s05_validation_membrane_observation_report_v0":
        reasons.append("validation_membrane_gate schema mismatch")
    if validation_report.get("status") != "closed":
        reasons.append("validation_membrane_gate status mismatch")
    if validation_check.get("schema_version") != "validation_membrane_check_report_v0":
        reasons.append("validation_check_gate schema mismatch")
    if validation_check.get("status") != "closed":
        reasons.append("validation_check_gate status mismatch")
    if schema_report.get("schema_version") != "s09_schema_runner_code_report_v0":
        reasons.append("schema_runner_gate schema mismatch")
    if schema_report.get("status") != "closed":
        reasons.append("schema_runner_gate status mismatch")
    if schema_report.get("next_required_command") != "life-v0 build-life-support --strict":
        reasons.append("schema_runner_gate next required command mismatch")
    if schema_check.get("schema_version") != "schema_runner_check_report_v0":
        reasons.append("schema_runner_check_gate schema mismatch")
    if schema_check.get("status") != "closed":
        reasons.append("schema_runner_check_gate status mismatch")
    if schema_smoke.get("schema_version") != "schema_runner_smoke_report_v0":
        reasons.append("schema_smoke_gate schema mismatch")
    if schema_smoke.get("status") != "closed":
        reasons.append("schema_smoke_gate status mismatch")
    return reasons


def _boundary_blockers(
    dream_fact: dict[str, Any],
    relationship: dict[str, Any],
    responsibility: dict[str, Any],
    runtime_bridge: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if dream_fact.get("fact_gate") != "DreamFactGate":
        reasons.append("dream_fact_gate missing DreamFactGate")
    if relationship.get("relation_role") != "relationship_subject":
        reasons.append("relationship_subject_gate relation role mismatch")
    if "repair_trace" not in relationship.get("required_links", []):
        reasons.append("relationship_subject_gate repair trace missing")
    if "repair_obligation" not in responsibility.get("required_links", []):
        reasons.append("responsibility_gate repair obligation missing")
    if runtime_bridge.get("schema_version") != "runtime_bridge_boundary_v0":
        reasons.append("runtime_bridge_gate schema mismatch")
    if runtime_bridge.get("allowed_role") != "computer_peripheral_observation_and_action_shell":
        reasons.append("runtime_bridge_gate allowed role mismatch")
    return reasons


def _check_life_state(life_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("state_store_gate schema mismatch")
    if not life_state.get("self_model", {}).get("old_self_anchors"):
        reasons.append("state_store_gate old self anchors missing")
    if not life_state.get("memory_index", {}).get("replay_cues"):
        reasons.append("state_store_gate replay cues missing")
    return reasons


def _check_body_resource_budget(body_budget: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if body_budget.get("schema_version") != "body_resource_budget_v0":
        reasons.append("resource_budget_gate schema mismatch")
    if body_budget.get("energy_state", {}).get("level") != "guarded_reserve":
        reasons.append("resource_budget_gate energy level mismatch")
    if body_budget.get("fatigue_state", {}).get("level") != "managed_low_noise":
        reasons.append("resource_budget_gate fatigue level mismatch")
    for priority in [
        "direction_lock_continuity",
        "dream_fact_integrity",
        "responsibility_repair_integrity",
        "anti_forgetting_replay_protection",
        "language_relationship_continuity",
    ]:
        if priority not in body_budget.get("recovery_priority", []):
            reasons.append(f"resource_budget_gate missing recovery priority {priority}")
    continuity_pressure = body_budget.get("maintenance_pressure", {}).get("language_continuity_pressure", {})
    for field in [
        "shared_language_ref_count",
        "expression_monitor_ref_count",
        "relation_scope_ref_count",
        "commitment_ref_count",
        "self_narrative_trace_ref_count",
        "language_percept_ref_count",
        "semantic_map_ref_count",
    ]:
        if continuity_pressure.get(field, 0) < 1:
            reasons.append(f"resource_budget_gate missing language continuity pressure {field}")
    return reasons


def _check_stage_gate(stage_gate: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if stage_gate.get("schema_version") != "life_support_stage_gate_v0":
        reasons.append("next_slice_gate schema mismatch")
    if stage_gate.get("decision") != "closed":
        reasons.append("next_slice_gate decision mismatch")
    if stage_gate.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("next_slice_gate next allowed slices mismatch")
    if stage_gate.get("next_required_command") != NEXT_REQUIRED_COMMAND:
        reasons.append("next_slice_gate next required command mismatch")
    return reasons


def _check_build_report(build_report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if build_report.get("schema_version") != "s06_life_support_development_report_v0":
        reasons.append("build_report_gate schema mismatch")
    if build_report.get("status") != "closed":
        reasons.append("build_report_gate status mismatch")
    if build_report.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("build_report_gate next allowed slices mismatch")
    if build_report.get("next_required_command") != NEXT_REQUIRED_COMMAND:
        reasons.append("build_report_gate next required command mismatch")
    return reasons


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blocked_reasons.append(f"{gate} failed: {exc}")
        return {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_if_exists(path: Path) -> str | None:
    if path.exists():
        return _sha256(path)
    return None


def _default_run_id() -> str:
    return "life-support-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    gates = {
        "doc_index_read_gate",
        "state_store_gate",
        "direction_lock_gate",
        "validation_membrane_gate",
        "validation_check_gate",
        "schema_runner_gate",
        "schema_runner_check_gate",
        "schema_smoke_gate",
        "dream_fact_gate",
        "relationship_subject_gate",
        "responsibility_gate",
        "runtime_bridge_gate",
        "resource_budget_gate",
        "defense_gate",
        "plasticity_gate",
        "self_growth_gate",
        "anti_forgetting_gate",
        "next_slice_gate",
        "build_report_gate",
    }
    for reason in blocked_reasons:
        gate = reason.split(" ", 1)[0]
        gates.discard(gate)
    return sorted(gates)


def _blocked_gates(blocked_reasons: list[str]) -> list[str]:
    return sorted({reason.split(" ", 1)[0] for reason in blocked_reasons})
