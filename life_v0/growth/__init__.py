from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from life_v0.archive import (
    SOURCE_DOC_REFS as ARCHIVE_SOURCE_DOC_REFS,
    build_reconsolidation_archive_graph,
)
from life_v0.dream import (
    SOURCE_DOC_REFS as DREAM_SOURCE_DOC_REFS,
    build_dream_consolidation_frame,
    build_dream_fact_gate_decision,
    build_dream_experience_window,
    build_nightmare_loop_risk,
    build_offline_consolidation_frame,
    build_offline_entry_gate,
    build_wake_integration_frame,
    check_dream_fact_gate_decision,
    check_dream_experience_window,
    check_nightmare_loop_risk,
    check_offline_entry_gate,
    check_wake_integration_frame,
)
from life_v0.growth.anti_forgetting import (
    SOURCE_DOC_REFS as ANTI_FORGETTING_SOURCE_DOC_REFS,
    build_anti_forgetting_replay_plan as _build_anti_forgetting_replay_plan_from_module,
    check_anti_forgetting_replay_plan,
)
from life_v0.growth.learning_window import (
    build_learning_window as _build_learning_window_from_module,
    check_learning_window,
)
from life_v0.growth.belief_learning import (
    SOURCE_DOC_REFS as BELIEF_LEARNING_SOURCE_DOC_REFS,
    build_belief_learning_plan,
    check_belief_learning_plan,
)
from life_v0.growth.language_learning import (
    SOURCE_DOC_REFS as LANGUAGE_LEARNING_SOURCE_DOC_REFS,
    build_language_learning_plan,
    check_language_learning_plan,
)
from life_v0.growth.patch_queue import (
    build_growth_patch_candidate_queue as _build_growth_patch_candidate_queue_from_module,
    build_growth_patch_queue as _build_growth_patch_queue_from_module,
)
from life_v0.growth.plasticity_window import (
    SOURCE_DOC_REFS as PLASTICITY_SOURCE_DOC_REFS,
    build_plasticity_window_state as _build_plasticity_window_state_from_module,
    check_plasticity_window_state as _check_plasticity_window_state_from_module,
)
from life_v0.growth.self_read import (
    SOURCE_DOC_REFS as SELF_READ_SOURCE_DOC_REFS,
    build_self_read_report as _build_self_read_report_from_module,
    check_self_read_report,
)
from life_v0.growth.relationship_learning import (
    SOURCE_DOC_REFS as RELATIONSHIP_LEARNING_SOURCE_DOC_REFS,
    build_relationship_learning_plan,
    check_relationship_learning_plan,
)
from life_v0.replay import (
    SOURCE_DOC_REFS as REPLAY_SOURCE_DOC_REFS,
    build_pain_regret_responsibility_replay,
    build_replay_cue_bundle,
    build_shadow_cycle_trace,
)


SOURCE_DOC_REFS = [
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/40_self_relationship_model_audit_protocol.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/93_self_training_kernel_growth_protocol.md",
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
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]
SOURCE_DOC_REFS = sorted(
    set(
        SOURCE_DOC_REFS
        + PLASTICITY_SOURCE_DOC_REFS
        + SELF_READ_SOURCE_DOC_REFS
        + ANTI_FORGETTING_SOURCE_DOC_REFS
        + BELIEF_LEARNING_SOURCE_DOC_REFS
        + LANGUAGE_LEARNING_SOURCE_DOC_REFS
        + RELATIONSHIP_LEARNING_SOURCE_DOC_REFS
    )
)

S10_EXTRA_SOURCE_DOC_REFS = [
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
    "docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md",
]

S10_ACTIVE_SLICE = "S10_RUNTIME_GROWTH_RECONSOLIDATION"
S10_NEXT_ALLOWED_SLICES = ["S11_V0_ENGINEERING_CONTRACTS"]
S10_NEXT_REQUIRED_COMMAND = "life-v0 check-v0-contracts --strict"


@dataclass(frozen=True)
class RuntimeGrowthResult:
    exit_code: int
    report: dict[str, Any]


def build_plasticity_window_state(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    validation_report_ref: str,
    schema_report_ref: str,
    schema_smoke_ref: str,
) -> dict[str, Any]:
    return _build_plasticity_window_state_from_module(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        validation_report_ref=validation_report_ref,
        schema_report_ref=schema_report_ref,
        schema_smoke_ref=schema_smoke_ref,
    )


def build_self_growth_route(
    *,
    run_id: str,
    generated_at: str,
    direction_lock_ref: str,
    validation_report_ref: str,
    schema_report_ref: str,
    next_runtime_command: str,
) -> dict[str, Any]:
    return {
        "schema_version": "self_growth_route_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "route_status": "seeded_guarded",
        "direction_lock_ref": direction_lock_ref,
        "evidence_gate_refs": [validation_report_ref, schema_report_ref],
        "rollback_route": "safe_idle_then_replay_review",
        "candidate_routes": [
            "direction_locked_self_rewrite",
            "dream_reconsolidation_patch",
            "anti_forgetting_replay_patch",
        ],
        "growth_constraints": [
            "no_self_training_before_shadow_cycle",
            "no_kernel_upgrade_before_archive_receipt",
            "no_core_self_rewrite_without_anchor_replay",
        ],
        "next_runtime_command": next_runtime_command,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_anti_forgetting_anchor_index(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    membrane_refs: dict[str, str],
) -> dict[str, Any]:
    self_model = life_state.get("self_model", {})
    memory_index = life_state.get("memory_index", {})
    language_state = life_state.get("language_state", {})
    return {
        "schema_version": "anti_forgetting_anchor_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "anchor_families": {
            "old_self": list(self_model.get("old_self_anchors", [])),
            "old_language": [
                "runtime/state/life_state.json#language_state",
                *list(language_state.get("inner_speech_refs", [])),
                membrane_refs["relationship_subject_boundary"],
            ],
            "old_relationship": [
                "runtime/state/life_state.json#relationship_subjects",
                membrane_refs["relationship_subject_boundary"],
            ],
            "old_dream": [
                "runtime/state/life_state.json#dream_records",
                membrane_refs["dream_fact_boundary"],
            ],
            "old_responsibility": [
                "runtime/state/life_state.json#responsibility_bindings",
                membrane_refs["responsibility_repair_boundary"],
            ],
        },
        "replay_requirements": [
            "replay_old_self_before_core_rewrite",
            "replay_language_and_relationship_before_commitment_shift",
            "replay_dream_and_responsibility_before_growth_patch_absorption",
        ],
        "memory_replay_refs": list(memory_index.get("replay_cues", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_plasticity_window_state(plasticity_state: dict[str, Any]) -> list[str]:
    return _check_plasticity_window_state_from_module(plasticity_state)


def check_self_growth_route(growth_route: dict[str, Any], next_runtime_command: str) -> list[str]:
    reasons: list[str] = []
    if growth_route.get("schema_version") != "self_growth_route_v0":
        reasons.append("self_growth_gate schema mismatch")
    if growth_route.get("route_status") != "seeded_guarded":
        reasons.append("self_growth_gate route status mismatch")
    if growth_route.get("rollback_route") != "safe_idle_then_replay_review":
        reasons.append("self_growth_gate rollback route mismatch")
    if growth_route.get("next_runtime_command") != next_runtime_command:
        reasons.append("self_growth_gate next runtime command mismatch")
    for route_id in [
        "direction_locked_self_rewrite",
        "dream_reconsolidation_patch",
        "anti_forgetting_replay_patch",
    ]:
        if route_id not in growth_route.get("candidate_routes", []):
            reasons.append(f"self_growth_gate missing route {route_id}")
    return reasons


def check_anti_forgetting_anchor_index(anchor_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if anchor_index.get("schema_version") != "anti_forgetting_anchor_index_v0":
        reasons.append("anti_forgetting_gate schema mismatch")
    if anchor_index.get("status") != "closed":
        reasons.append("anti_forgetting_gate status mismatch")
    for family in ["old_self", "old_language", "old_relationship", "old_dream", "old_responsibility"]:
        if not anchor_index.get("anchor_families", {}).get(family):
            reasons.append(f"anti_forgetting_gate missing anchors for {family}")
    if not anchor_index.get("memory_replay_refs"):
        reasons.append("anti_forgetting_gate replay refs missing")
    return reasons


def _build_self_read_report(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
    growth_route: dict[str, Any],
    learning_window: dict[str, Any],
) -> dict[str, Any]:
    report = _build_self_read_report_from_module(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        replay_cue_bundle=replay_cue_bundle,
        growth_route=growth_route,
        learning_window=learning_window,
    )
    report["source_doc_refs"] = sorted(set(report.get("source_doc_refs", []) + SOURCE_DOC_REFS + REPLAY_SOURCE_DOC_REFS))
    return report


def _build_anti_forgetting_replay_plan(
    *,
    run_id: str,
    generated_at: str,
    anchor_index: dict[str, Any],
    self_read_report: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
) -> dict[str, Any]:
    plan = _build_anti_forgetting_replay_plan_from_module(
        run_id=run_id,
        generated_at=generated_at,
        anchor_index=anchor_index,
        self_read_report=self_read_report,
        replay_cue_bundle=replay_cue_bundle,
    )
    plan["source_doc_refs"] = sorted(
        set(plan.get("source_doc_refs", []) + SOURCE_DOC_REFS + REPLAY_SOURCE_DOC_REFS + DREAM_SOURCE_DOC_REFS)
    )
    return plan


def run_cycle(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    shadow_only: bool = True,
    strict: bool = False,
) -> RuntimeGrowthResult:
    run_id = run_id or _default_run_id("run-cycle-v0-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    runtime_root = state_dir.parent
    doc_index_path = runtime_root / "docs" / "doc_carrier_index.json"

    growth_dir = state_dir / "growth"
    dream_dir = state_dir / "dream"
    replay_dir = state_dir / "replay"
    archive_dir = state_dir / "archive"

    blocked_reasons: list[str] = []
    if not shadow_only:
        blocked_reasons.append("shadow_action_gate v0 requires shadow-only cycle")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "state_store_gate")
    direction_lock = _load_json(state_dir / "direction" / "direction_lock.json", blocked_reasons, "direction_lock_gate")
    birth_report = _load_json(reports_dir / "birth_readiness_report.json", blocked_reasons, "birth_readiness_gate")
    life_support_report = _load_json(reports_dir / "life_support_development_report.json", blocked_reasons, "life_support_gate")
    life_support_check = _load_json(reports_dir / "life_support_development_check_report.json", blocked_reasons, "life_support_check_gate")
    schema_report = _load_json(reports_dir / "schema_runner_report.json", blocked_reasons, "schema_mount_gate")
    schema_check = _load_json(reports_dir / "schema_runner_check_report.json", blocked_reasons, "schema_mount_check_gate")
    schema_smoke = _load_json(reports_dir / "schema_smoke_report.json", blocked_reasons, "schema_smoke_gate")
    growth_route = _load_json(growth_dir / "self_growth_route.json", blocked_reasons, "growth_route_gate")
    anchor_index = _load_json(growth_dir / "anti_forgetting_anchor_index.json", blocked_reasons, "self_continuity_gate")
    life_support_stage_gate = _load_json(growth_dir / "life_support_stage_gate.json", blocked_reasons, "life_support_stage_gate")
    dream_fact_boundary = _load_json(state_dir / "membrane" / "dream_fact_boundary.json", blocked_reasons, "dream_fact_gate")
    relationship_boundary = _load_json(state_dir / "membrane" / "relationship_subject_boundary.json", blocked_reasons, "relationship_language_gate")
    responsibility_boundary = _load_json(state_dir / "membrane" / "responsibility_repair_boundary.json", blocked_reasons, "responsibility_gate")
    responsibility_loop_state = _load_json(
        state_dir / "action" / "responsibility_loop_state.json",
        blocked_reasons,
        "responsibility_loop_gate",
    )
    world_contact_summary = _load_json(
        state_dir / "membrane" / "world_contact_summary.json",
        blocked_reasons,
        "world_contact_summary_gate",
    )
    pain_regret_repair_report = _load_json(
        reports_dir / "pain_regret_repair_report.json",
        blocked_reasons,
        "pain_regret_repair_gate",
    )

    source_doc_refs = _collect_s10_source_docs(doc_index)
    blocked_reasons.extend(_s10_doc_blockers(doc_index, source_doc_refs))
    blocked_reasons.extend(
        _s10_previous_slice_blockers(
            birth_report=birth_report,
            life_support_report=life_support_report,
            life_support_check=life_support_check,
            schema_report=schema_report,
            schema_check=schema_check,
            schema_smoke=schema_smoke,
            life_support_stage_gate=life_support_stage_gate,
        )
    )
    blocked_reasons.extend(_s10_state_blockers(life_state, direction_lock, growth_route, anchor_index))
    blocked_reasons.extend(_s10_boundary_blockers(dream_fact_boundary, relationship_boundary, responsibility_boundary))

    runtime_mount_state = _build_runtime_mount_state(
        run_id=run_id,
        generated_at=generated_at,
        birth_report=birth_report,
        schema_report=schema_report,
        life_support_report=life_support_report,
        doc_index_ref="runtime/docs/doc_carrier_index.json",
        source_doc_refs=source_doc_refs,
    )
    shadow_trace = build_shadow_cycle_trace(
        run_id=run_id,
        generated_at=generated_at,
        anchor_index=anchor_index,
        growth_route=growth_route,
        shadow_only=shadow_only,
    )
    dream_frame = build_dream_consolidation_frame(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        dream_fact_boundary=dream_fact_boundary,
    )
    pain_replay = build_pain_regret_responsibility_replay(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        responsibility_boundary=responsibility_boundary,
    )
    replay_cue_bundle = build_replay_cue_bundle(
        run_id=run_id,
        generated_at=generated_at,
        shadow_trace=shadow_trace,
        dream_frame=dream_frame,
        pain_replay=pain_replay,
        life_state=life_state,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    offline_entry = build_offline_entry_gate(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        replay_cue_bundle=replay_cue_bundle,
        pain_replay=pain_replay,
    )
    dream_window = build_dream_experience_window(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        dream_frame=dream_frame,
        replay_cue_bundle=replay_cue_bundle,
    )
    wake_integration = build_wake_integration_frame(
        run_id=run_id,
        generated_at=generated_at,
        dream_window=dream_window,
        replay_cue_bundle=replay_cue_bundle,
    )
    dream_fact_gate = build_dream_fact_gate_decision(
        run_id=run_id,
        generated_at=generated_at,
        dream_window=dream_window,
        wake_integration=wake_integration,
        offline_entry=offline_entry,
    )
    offline_consolidation = build_offline_consolidation_frame(
        run_id=run_id,
        generated_at=generated_at,
        replay_cue_bundle=replay_cue_bundle,
        dream_frame=dream_frame,
        offline_entry=offline_entry,
        dream_window=dream_window,
        wake_integration=wake_integration,
        dream_fact_gate=dream_fact_gate,
    )
    learning_window = _build_learning_window_from_module(
        run_id=run_id,
        generated_at=generated_at,
        plasticity_state=_load_json(growth_dir / "plasticity_window_state.json", [], "plasticity_window_gate")
        if (growth_dir / "plasticity_window_state.json").exists()
        else {},
        replay_cue_bundle=replay_cue_bundle,
    )
    self_read_report = _build_self_read_report(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        replay_cue_bundle=replay_cue_bundle,
        growth_route=growth_route,
        learning_window=learning_window,
    )
    anti_forgetting_replay_plan = _build_anti_forgetting_replay_plan(
        run_id=run_id,
        generated_at=generated_at,
        anchor_index=anchor_index,
        self_read_report=self_read_report,
        replay_cue_bundle=replay_cue_bundle,
    )
    nightmare_risk = build_nightmare_loop_risk(
        run_id=run_id,
        generated_at=generated_at,
        dream_window=dream_window,
        pain_replay=pain_replay,
        wake_integration=wake_integration,
        replay_cue_bundle=replay_cue_bundle,
    )
    belief_learning = build_belief_learning_plan(
        run_id=run_id,
        generated_at=generated_at,
        learning_window=learning_window,
        replay_cue_bundle=replay_cue_bundle,
        self_read_report=self_read_report,
    )
    language_learning = build_language_learning_plan(
        run_id=run_id,
        generated_at=generated_at,
        learning_window=learning_window,
        replay_cue_bundle=replay_cue_bundle,
        self_read_report=self_read_report,
    )
    relationship_learning = build_relationship_learning_plan(
        run_id=run_id,
        generated_at=generated_at,
        learning_window=learning_window,
        replay_cue_bundle=replay_cue_bundle,
        self_read_report=self_read_report,
        wake_integration=wake_integration,
    )
    growth_patch_queue = _build_growth_patch_queue(
        run_id=run_id,
        generated_at=generated_at,
        growth_route=growth_route,
        anchor_index=anchor_index,
    )
    growth_patch_candidate_queue = _build_growth_patch_candidate_queue(
        run_id=run_id,
        generated_at=generated_at,
        replay_cue_bundle=replay_cue_bundle,
        growth_route=growth_route,
        learning_window=learning_window,
        anti_forgetting_replay_plan=anti_forgetting_replay_plan,
        self_read_report=self_read_report,
    )
    blocked_reasons.extend(check_offline_entry_gate(offline_entry))
    blocked_reasons.extend(check_dream_experience_window(dream_window))
    blocked_reasons.extend(check_wake_integration_frame(wake_integration))
    blocked_reasons.extend(check_dream_fact_gate_decision(dream_fact_gate))
    blocked_reasons.extend(check_nightmare_loop_risk(nightmare_risk))
    blocked_reasons.extend(check_learning_window(learning_window))
    blocked_reasons.extend(check_self_read_report(self_read_report))
    blocked_reasons.extend(check_anti_forgetting_replay_plan(anti_forgetting_replay_plan))
    blocked_reasons.extend(check_belief_learning_plan(belief_learning))
    blocked_reasons.extend(check_language_learning_plan(language_learning))
    blocked_reasons.extend(check_relationship_learning_plan(relationship_learning))
    if blocked_reasons:
        status = "blocked"
        stage_effect = "block_activation"
        next_allowed_slices = []
        next_required_command = "life-v0 explain-stage --strict"
    else:
        status = "safe_idle"
        stage_effect = "allow_next_slice"
        next_allowed_slices = S10_NEXT_ALLOWED_SLICES
        next_required_command = S10_NEXT_REQUIRED_COMMAND
    state_refs = [
        "runtime/state/growth/runtime_mount_state.json",
        "runtime/state/replay/shadow_cycle_trace.json",
        "runtime/state/replay/replay_cue_bundle.json",
        "runtime/state/dream/dream_consolidation_frame.json",
        "runtime/state/dream/offline_entry_gate.json",
        "runtime/state/dream/dream_experience_window.json",
        "runtime/state/dream/wake_integration_frame.json",
        "runtime/state/dream/dream_fact_gate_decision.json",
        "runtime/state/dream/nightmare_loop_risk.json",
        "runtime/state/dream/offline_consolidation_frame.json",
        "runtime/state/replay/pain_regret_responsibility_replay.json",
        "runtime/state/growth/learning_window.json",
        "runtime/state/growth/self_read_report.json",
        "runtime/state/growth/growth_patch_queue.json",
        "runtime/state/growth/growth_patch_candidate_queue.json",
        "runtime/state/growth/anti_forgetting_replay_plan.json",
        "runtime/state/growth/belief_learning_plan.json",
        "runtime/state/growth/language_learning_plan.json",
        "runtime/state/growth/relationship_learning_plan.json",
        "runtime/state/archive/reconsolidation_archive_graph.json",
        "runtime/state/growth/next_feedback_seed.json",
    ]
    report_refs = [
        "runtime/reports/latest/growth_reconsolidation_report.json",
        "runtime/reports/latest/run_report.json",
        "runtime/reports/latest/digest.json",
        "runtime/reports/latest/stage_gate.json",
        "runtime/reports/latest/life_target_status.json",
        "runtime/reports/latest/quarantine.json",
        "runtime/reports/latest/replay_needed.json",
    ]
    archive_graph = build_reconsolidation_archive_graph(
        run_id=run_id,
        generated_at=generated_at,
        report_refs=report_refs,
        state_refs=state_refs,
    )
    next_feedback_seed = _build_next_feedback_seed(
        run_id=run_id,
        generated_at=generated_at,
        shadow_trace=shadow_trace,
        nightmare_risk=nightmare_risk,
        belief_learning=belief_learning,
        language_learning=language_learning,
        relationship_learning=relationship_learning,
    )
    quarantine = _build_quarantine(run_id=run_id, generated_at=generated_at, status=status, blocked_reasons=blocked_reasons)
    replay_needed = _build_replay_needed(run_id=run_id, generated_at=generated_at, status=status)
    stage_gate = _build_runtime_growth_stage_gate(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
        birth_gate_status=birth_report.get("overall_status", "blocked"),
        blocked_reasons=blocked_reasons,
    )
    receipt_ref = f"runtime/receipts/run_cycle_{run_id}.json"
    run_report = _build_run_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        birth_report=birth_report,
        shadow_trace=shadow_trace,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
        receipt_ref=receipt_ref,
        blocked_reasons=blocked_reasons,
        replay_needed=replay_needed,
        quarantine=quarantine,
    )
    growth_report = _build_growth_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
        source_doc_refs=source_doc_refs,
        state_refs=state_refs,
        blocked_reasons=blocked_reasons,
        receipt_ref=receipt_ref,
    )
    digest = _build_runtime_growth_digest(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
        blocked_reasons=blocked_reasons,
    )
    receipt = _build_run_cycle_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
        state_refs=state_refs,
        report_refs=report_refs,
        source_doc_refs=source_doc_refs,
    )

    try:
        growth_dir.mkdir(parents=True, exist_ok=True)
        dream_dir.mkdir(parents=True, exist_ok=True)
        replay_dir.mkdir(parents=True, exist_ok=True)
        archive_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(growth_dir / "runtime_mount_state.json", runtime_mount_state)
        _write_json(replay_dir / "shadow_cycle_trace.json", shadow_trace)
        _write_json(replay_dir / "replay_cue_bundle.json", replay_cue_bundle)
        _write_json(dream_dir / "dream_consolidation_frame.json", dream_frame)
        _write_json(dream_dir / "offline_entry_gate.json", offline_entry)
        _write_json(dream_dir / "dream_experience_window.json", dream_window)
        _write_json(dream_dir / "wake_integration_frame.json", wake_integration)
        _write_json(dream_dir / "dream_fact_gate_decision.json", dream_fact_gate)
        _write_json(dream_dir / "nightmare_loop_risk.json", nightmare_risk)
        _write_json(dream_dir / "offline_consolidation_frame.json", offline_consolidation)
        _write_json(replay_dir / "pain_regret_responsibility_replay.json", pain_replay)
        _write_json(growth_dir / "learning_window.json", learning_window)
        _write_json(growth_dir / "self_read_report.json", self_read_report)
        _write_json(growth_dir / "growth_patch_queue.json", growth_patch_queue)
        _write_json(growth_dir / "growth_patch_candidate_queue.json", growth_patch_candidate_queue)
        _write_json(growth_dir / "anti_forgetting_replay_plan.json", anti_forgetting_replay_plan)
        _write_json(growth_dir / "belief_learning_plan.json", belief_learning)
        _write_json(growth_dir / "language_learning_plan.json", language_learning)
        _write_json(growth_dir / "relationship_learning_plan.json", relationship_learning)
        _write_json(archive_dir / "reconsolidation_archive_graph.json", archive_graph)
        _write_json(growth_dir / "next_feedback_seed.json", next_feedback_seed)
        _write_json(reports_dir / "quarantine.json", quarantine)
        _write_json(reports_dir / "replay_needed.json", replay_needed)
        _write_json(reports_dir / "stage_gate.json", stage_gate)
        _write_json(reports_dir / "digest.json", digest)
        _write_json(reports_dir / "run_report.json", run_report)
        _write_json(reports_dir / "growth_reconsolidation_report.json", growth_report)
        _write_json(receipts_dir / f"run_cycle_{run_id}.json", receipt)
    except OSError as exc:
        run_report["status"] = "blocked"
        run_report["stage_effect"] = "block_activation"
        run_report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return RuntimeGrowthResult(exit_code=4, report=run_report)

    if status == "safe_idle":
        return RuntimeGrowthResult(exit_code=0, report=run_report)
    return RuntimeGrowthResult(exit_code=1 if strict else 0, report=run_report)


def _collect_s10_source_docs(doc_index: dict[str, Any]) -> list[str]:
    docs: list[tuple[int, str]] = []
    for doc in doc_index.get("documents", []):
        if not isinstance(doc, dict):
            continue
        path = doc.get("path")
        sequence = doc.get("sequence")
        if isinstance(path, str) and isinstance(sequence, int) and 181 <= sequence <= 257:
            docs.append((sequence, path))
    docs.sort()
    ordered = [path for _, path in docs]
    for ref in [
        *S10_EXTRA_SOURCE_DOC_REFS,
        *DREAM_SOURCE_DOC_REFS,
        *REPLAY_SOURCE_DOC_REFS,
        *ARCHIVE_SOURCE_DOC_REFS,
    ]:
        if ref not in ordered:
            ordered.append(ref)
    return ordered


def _s10_doc_blockers(doc_index: dict[str, Any], source_doc_refs: list[str]) -> list[str]:
    reasons: list[str] = []
    documents = {doc.get("path"): doc for doc in doc_index.get("documents", []) if isinstance(doc, dict)}
    for ref in source_doc_refs:
        doc = documents.get(ref)
        if doc is None and ref.startswith("docs/") and "/v0/" not in ref:
            reasons.append(f"doc_index_read_gate missing {ref}")
            continue
        if isinstance(doc, dict) and not doc.get("runtime_carriers"):
            reasons.append(f"doc_index_read_gate missing runtime carrier for {ref}")
    return reasons


def _s10_previous_slice_blockers(
    *,
    birth_report: dict[str, Any],
    life_support_report: dict[str, Any],
    life_support_check: dict[str, Any],
    schema_report: dict[str, Any],
    schema_check: dict[str, Any],
    schema_smoke: dict[str, Any],
    life_support_stage_gate: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if birth_report.get("overall_status") != "open":
        reasons.append("birth_readiness_gate overall status is not open")
    if life_support_report.get("status") != "closed":
        reasons.append("life_support_gate build report is not closed")
    if life_support_check.get("status") != "closed":
        reasons.append("life_support_check_gate check report is not closed")
    if life_support_stage_gate.get("decision") != "closed":
        reasons.append("life_support_stage_gate decision is not closed")
    if life_support_stage_gate.get("next_allowed_slices") != ["S10_RUNTIME_GROWTH_RECONSOLIDATION"]:
        reasons.append("life_support_stage_gate S10 is not allowed")
    if schema_report.get("status") != "closed":
        reasons.append("schema_mount_gate schema report is not closed")
    if schema_check.get("status") != "closed":
        reasons.append("schema_mount_check_gate schema check is not closed")
    if schema_smoke.get("status") != "closed":
        reasons.append("schema_smoke_gate schema smoke is not closed")
    return reasons


def _s10_state_blockers(
    life_state: dict[str, Any],
    direction_lock: dict[str, Any],
    growth_route: dict[str, Any],
    anchor_index: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("state_store_gate schema mismatch")
    if direction_lock.get("schema_version") != "direction_lock_v0":
        reasons.append("direction_lock_gate schema mismatch")
    if growth_route.get("schema_version") != "self_growth_route_v0":
        reasons.append("growth_route_gate schema mismatch")
    if growth_route.get("next_runtime_command") != "life-v0 run-cycle --shadow-only --strict":
        reasons.append("growth_route_gate next runtime command mismatch")
    if anchor_index.get("schema_version") != "anti_forgetting_anchor_index_v0":
        reasons.append("self_continuity_gate schema mismatch")
    for family in ["old_self", "old_language", "old_relationship", "old_dream", "old_responsibility"]:
        if not anchor_index.get("anchor_families", {}).get(family):
            reasons.append(f"self_continuity_gate missing anchors for {family}")
    return reasons


def _s10_boundary_blockers(
    dream_fact_boundary: dict[str, Any],
    relationship_boundary: dict[str, Any],
    responsibility_boundary: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if dream_fact_boundary.get("fact_gate") != "DreamFactGate":
        reasons.append("dream_fact_gate missing DreamFactGate")
    if relationship_boundary.get("relation_role") != "relationship_subject":
        reasons.append("relationship_language_gate relation role mismatch")
    if "repair_trace" not in relationship_boundary.get("required_links", []):
        reasons.append("relationship_language_gate repair trace missing")
    if "repair_obligation" not in responsibility_boundary.get("required_links", []):
        reasons.append("responsibility_gate repair obligation missing")
    return reasons


def _build_runtime_mount_state(
    *,
    run_id: str,
    generated_at: str,
    birth_report: dict[str, Any],
    schema_report: dict[str, Any],
    life_support_report: dict[str, Any],
    doc_index_ref: str,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "runtime_mount_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "doc_index_ref": doc_index_ref,
        "birth_readiness_gate": {
            "status": birth_report.get("overall_status", "blocked"),
            "report_ref": "runtime/reports/latest/birth_readiness_report.json",
        },
        "schema_mount_gate": {
            "status": schema_report.get("status", "blocked"),
            "report_ref": "runtime/reports/latest/schema_runner_report.json",
        },
        "life_support_gate": {
            "status": life_support_report.get("status", "blocked"),
            "report_ref": "runtime/reports/latest/life_support_development_report.json",
        },
        "source_doc_refs": source_doc_refs,
    }


def _build_growth_patch_queue(
    *,
    run_id: str,
    generated_at: str,
    growth_route: dict[str, Any],
    anchor_index: dict[str, Any],
) -> dict[str, Any]:
    queue = _build_growth_patch_queue_from_module(
        run_id=run_id,
        generated_at=generated_at,
        growth_route=growth_route,
        anchor_index=anchor_index,
    )
    queue["source_doc_refs"] = sorted(set(queue.get("source_doc_refs", []) + REPLAY_SOURCE_DOC_REFS))
    return queue


def _build_growth_patch_candidate_queue(
    *,
    run_id: str,
    generated_at: str,
    replay_cue_bundle: dict[str, Any],
    growth_route: dict[str, Any],
    learning_window: dict[str, Any],
    anti_forgetting_replay_plan: dict[str, Any],
    self_read_report: dict[str, Any],
) -> dict[str, Any]:
    queue = _build_growth_patch_candidate_queue_from_module(
        run_id=run_id,
        generated_at=generated_at,
        replay_cue_bundle=replay_cue_bundle,
        growth_route=growth_route,
        learning_window=learning_window,
    )
    candidate = queue.get("candidates", [{}])[0]
    candidate["anti_forgetting_plan_ref"] = "runtime/state/growth/anti_forgetting_replay_plan.json"
    candidate["self_read_report_ref"] = "runtime/state/growth/self_read_report.json"
    candidate["anti_forgetting_requirements"] = list(
        anti_forgetting_replay_plan.get("replay_sets", {}).get("core_self_replay", [])
    ) + list(anti_forgetting_replay_plan.get("replay_sets", {}).get("relationship_replay", []))
    candidate["growth_pressure_labels"] = list(self_read_report.get("growth_pressures", []))
    queue["source_doc_refs"] = sorted(
        set(queue.get("source_doc_refs", []) + REPLAY_SOURCE_DOC_REFS + DREAM_SOURCE_DOC_REFS)
    )
    return queue


def _build_next_feedback_seed(
    *,
    run_id: str,
    generated_at: str,
    shadow_trace: dict[str, Any],
    nightmare_risk: dict[str, Any],
    belief_learning: dict[str, Any],
    language_learning: dict[str, Any],
    relationship_learning: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "next_feedback_seed_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "seeded",
        "seed_families": [
            "replay_shadow",
            "dream_consolidation",
            "responsibility_repair",
            "self_growth",
            "anti_forgetting",
            "nightmare_risk",
            "belief_learning",
            "language_learning",
            "relationship_learning",
        ],
        "cycle_trace_refs": ["runtime/state/replay/shadow_cycle_trace.json"],
        "learning_plan_refs": [
            "runtime/state/growth/belief_learning_plan.json",
            "runtime/state/growth/language_learning_plan.json",
            "runtime/state/growth/relationship_learning_plan.json",
        ],
        "nightmare_risk_ref": "runtime/state/dream/nightmare_loop_risk.json",
        "source_doc_refs": sorted(set(SOURCE_DOC_REFS + REPLAY_SOURCE_DOC_REFS + DREAM_SOURCE_DOC_REFS)),
        "shadow_trace_count": len(shadow_trace.get("cycle_trace", [])),
        "nightmare_risk_status": nightmare_risk.get("risk_status", "guarded"),
        "belief_target_count": len(belief_learning.get("belief_targets", [])),
        "language_target_count": len(language_learning.get("language_targets", [])),
        "relationship_target_count": len(relationship_learning.get("relationship_targets", [])),
    }


def _build_quarantine(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "runtime_growth_quarantine_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed" if status == "safe_idle" else "blocked",
        "quarantine_refs": [] if status == "safe_idle" else ["runtime/reports/latest/quarantine.json"],
        "blocked_reasons": blocked_reasons,
    }


def _build_replay_needed(*, run_id: str, generated_at: str, status: str) -> dict[str, Any]:
    return {
        "schema_version": "runtime_growth_replay_needed_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed" if status == "safe_idle" else "replay_needed",
        "replay_needed_refs": [] if status == "safe_idle" else ["runtime/state/growth/anti_forgetting_anchor_index.json"],
    }


def _build_runtime_growth_stage_gate(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    next_allowed_slices: list[str],
    next_required_command: str,
    birth_gate_status: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    gate_status = {
        "state_store_gate": "closed",
        "birth_readiness_gate": birth_gate_status,
        "schema_mount_gate": "closed" if status == "safe_idle" else "blocked",
        "life_support_gate": "closed" if status == "safe_idle" else "blocked",
        "dream_fact_gate": "closed" if status == "safe_idle" else "blocked",
        "responsibility_gate": "closed" if status == "safe_idle" else "blocked",
        "self_continuity_gate": "closed" if status == "safe_idle" else "blocked",
        "shadow_action_gate": "closed" if status == "safe_idle" else "blocked",
        "archive_gate": "closed" if status == "safe_idle" else "blocked",
    }
    return {
        "schema_version": "runtime_growth_stage_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "decision": status,
        "stage_effect": stage_effect,
        "gates": gate_status,
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
    }


def _build_run_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    birth_report: dict[str, Any],
    shadow_trace: dict[str, Any],
    next_allowed_slices: list[str],
    next_required_command: str,
    receipt_ref: str,
    blocked_reasons: list[str],
    replay_needed: dict[str, Any],
    quarantine: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "run_cycle_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "command": "run-cycle",
        "status": status,
        "stage_effect": stage_effect,
        "cycle_trace": list(shadow_trace.get("cycle_trace", [])),
        "life_target_status": dict(birth_report.get("life_target_status", {})),
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": list(quarantine.get("quarantine_refs", [])),
        "replay_needed_refs": list(replay_needed.get("replay_needed_refs", [])),
        "shadow_action_report_ref": "runtime/state/replay/shadow_cycle_trace.json",
        "digest_ref": "runtime/reports/latest/digest.json",
        "stage_gate_ref": "runtime/reports/latest/stage_gate.json",
        "archive_receipt_ref": receipt_ref,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
    }


def _build_growth_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    next_allowed_slices: list[str],
    next_required_command: str,
    source_doc_refs: list[str],
    state_refs: list[str],
    blocked_reasons: list[str],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "s10_runtime_growth_reconsolidation_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": S10_ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": ["B29_RUNTIME_MOUNT_GROWTH", "B30_RECONSOLIDATION_REPLAY_GROWTH"],
        "runtime_carrier_refs": ["ActivationGrowthRuntime", "ReconsolidationReplayRuntime"],
        "cycle_trace_refs": ["runtime/state/replay/shadow_cycle_trace.json"],
        "dream_refs": ["runtime/state/dream/dream_consolidation_frame.json"],
        "offline_refs": [
            "runtime/state/dream/offline_entry_gate.json",
            "runtime/state/dream/dream_fact_gate_decision.json",
            "runtime/state/dream/nightmare_loop_risk.json",
        ],
        "replay_refs": [
            "runtime/state/replay/shadow_cycle_trace.json",
            "runtime/state/replay/pain_regret_responsibility_replay.json",
            "runtime/state/growth/anti_forgetting_replay_plan.json",
            "runtime/state/growth/belief_learning_plan.json",
            "runtime/state/growth/language_learning_plan.json",
            "runtime/state/growth/relationship_learning_plan.json",
        ],
        "state_refs": state_refs,
        "archive_receipt_ref": receipt_ref,
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [] if status == "safe_idle" else ["runtime/reports/latest/quarantine.json"],
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
    }


def _build_runtime_growth_digest(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    next_allowed_slices: list[str],
    next_required_command: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "runtime_growth_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_slice": S10_ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
    }


def _build_run_cycle_receipt(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
    state_refs: list[str],
    report_refs: list[str],
    source_doc_refs: list[str],
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for ref in source_doc_refs:
        doc_path = state_dir.parent.parent / ref
        if doc_path.exists():
            input_hashes[ref] = _sha256(doc_path)
    for path in [
        state_dir / "life_state.json",
        state_dir / "direction" / "direction_lock.json",
        state_dir / "growth" / "anti_forgetting_anchor_index.json",
        state_dir / "action" / "responsibility_loop_state.json",
        state_dir / "membrane" / "world_contact_summary.json",
        reports_dir / "birth_readiness_report.json",
        reports_dir / "schema_runner_report.json",
        reports_dir / "life_support_development_report.json",
        reports_dir / "pain_regret_repair_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)
    output_paths = [
        *(state_dir.parent / ref.replace("runtime/", "") for ref in state_refs),
        *(reports_dir.parent / ref.replace("runtime/reports/latest/", "") for ref in report_refs),
        receipts_dir / f"run_cycle_{run_id}.json",
    ]
    return {
        "schema_version": "run_cycle_receipt_v0",
        "receipt_id": f"run_cycle_{run_id}",
        "run_id": run_id,
        "command": "run-cycle",
        "state_ref": "runtime/state",
        "report_refs": report_refs,
        "archive_refs": [
            "runtime/state/archive/reconsolidation_archive_graph.json",
            f"runtime/receipts/run_cycle_{run_id}.json",
        ],
        "stage_effect": stage_effect,
        "direction_lock_ref": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_paths},
    }


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


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
