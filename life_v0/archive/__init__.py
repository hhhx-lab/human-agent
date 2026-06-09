from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_DOC_REFS = [
    "docs/61_json_schema_bundle_draft.md",
    "docs/82_incident_report_and_recovery_protocol.md",
    "docs/188_life_reality_first_runner_schema_runtime_growth_archive_receipt_batch.md",
    "docs/189_life_reality_first_runner_schema_runtime_growth_shadow_run_plan.md",
    "docs/197_life_reality_first_runner_schema_runtime_growth_second_cycle_archive_plan.md",
    "docs/223_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_archive_plan.md",
    "docs/232_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_archive_plan.md",
    "docs/238_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_archive_plan.md",
    "docs/250_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_validation_after_reconsolidation_archive_plan.md",
    "docs/255_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_validation_after_archive_validation_replay_shadow_patch_archive_plan.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/architecture/runtime_v0_architecture.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]

ACTIVE_SLICE = "S10_RUNTIME_GROWTH_RECONSOLIDATION"
NEXT_REQUIRED_COMMAND = "life-v0 emit-report --strict"
NEXT_ALLOWED_SLICES = ["S10_RUNTIME_GROWTH_RECONSOLIDATION", "S11_V0_ENGINEERING_CONTRACTS"]
READ_ME_BLOCK_REFS = ["B29_RUNTIME_MOUNT_GROWTH", "B30_RECONSOLIDATION_REPLAY_GROWTH"]
RUNTIME_CARRIER_REFS = ["ActivationGrowthRuntime", "ReconsolidationReplayRuntime"]


@dataclass(frozen=True)
class GrowthArchiveResult:
    exit_code: int
    report: dict[str, Any]


def build_reconsolidation_archive_graph(
    *,
    run_id: str,
    generated_at: str,
    report_refs: list[str],
    state_refs: list[str],
) -> dict[str, Any]:
    archive_edges = [
        {"source": "runtime_mount_state", "target": "run_report", "edge_kind": "mount_to_report"},
        {"source": "shadow_cycle_trace", "target": "run_report", "edge_kind": "trace_to_report"},
        {"source": "dream_consolidation_frame", "target": "growth_reconsolidation_report", "edge_kind": "dream_to_growth"},
        {"source": "pain_regret_responsibility_replay", "target": "growth_reconsolidation_report", "edge_kind": "replay_to_growth"},
        {"source": "growth_patch_queue", "target": "digest", "edge_kind": "queue_to_digest"},
        {"source": "reconsolidation_archive_graph", "target": "receipt", "edge_kind": "archive_to_receipt"},
    ]
    return {
        "schema_version": "reconsolidation_archive_graph_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "archive_edges": archive_edges,
        "report_refs": report_refs,
        "state_refs": state_refs,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def run_write_growth_archive(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> GrowthArchiveResult:
    run_id = run_id or _default_run_id("write-growth-archive-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    runtime_root = state_dir.parent
    archive_dir = state_dir / "archive"
    runtime_archive_dir = runtime_root / "archive"

    blocked_reasons: list[str] = []

    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "life_state_gate")
    growth_patch_queue = _load_json(
        state_dir / "growth" / "growth_patch_queue.json",
        blocked_reasons,
        "growth_patch_queue_gate",
    )
    next_feedback_seed = _load_json(
        state_dir / "growth" / "next_feedback_seed.json",
        blocked_reasons,
        "next_feedback_seed_gate",
    )
    runtime_mount = _load_json(
        state_dir / "growth" / "runtime_mount_state.json",
        blocked_reasons,
        "runtime_mount_gate",
    )
    shadow_trace = _load_json(
        state_dir / "replay" / "shadow_cycle_trace.json",
        blocked_reasons,
        "shadow_trace_gate",
    )
    pain_replay = _load_json(
        state_dir / "replay" / "pain_regret_responsibility_replay.json",
        blocked_reasons,
        "pain_replay_gate",
    )
    replay_seed_bundle = _load_json(
        state_dir / "replay" / "replay_shadow_seed_bundle.json",
        blocked_reasons,
        "replay_seed_bundle_gate",
    )
    language_probe = _load_json(
        state_dir / "replay" / "language_relationship_replay_probe.json",
        blocked_reasons,
        "language_probe_gate",
    )
    dream_probe = _load_json(
        state_dir / "replay" / "dream_pain_regret_replay_probe.json",
        blocked_reasons,
        "dream_probe_gate",
    )
    shadow_expression = _load_json(
        state_dir / "replay" / "shadow_expression_report.json",
        blocked_reasons,
        "shadow_expression_gate",
    )
    replay_arbitration = _load_json(
        state_dir / "replay" / "replay_shadow_arbitration.json",
        blocked_reasons,
        "replay_arbitration_gate",
    )
    replay_report = _load_json(
        reports_dir / "replay_shadow_report.json",
        blocked_reasons,
        "replay_report_gate",
    )
    replay_digest = _load_json(
        reports_dir / "replay_shadow_digest.json",
        blocked_reasons,
        "replay_digest_gate",
    )
    replay_stage_gate = _load_json(
        reports_dir / "replay_shadow_stage_gate.json",
        blocked_reasons,
        "replay_stage_gate_gate",
    )

    blocked_reasons.extend(
        _archive_blockers(
            life_state=life_state,
            growth_patch_queue=growth_patch_queue,
            next_feedback_seed=next_feedback_seed,
            runtime_mount=runtime_mount,
            shadow_trace=shadow_trace,
            pain_replay=pain_replay,
            replay_seed_bundle=replay_seed_bundle,
            language_probe=language_probe,
            dream_probe=dream_probe,
            shadow_expression=shadow_expression,
            replay_arbitration=replay_arbitration,
            replay_report=replay_report,
            replay_digest=replay_digest,
            replay_stage_gate=replay_stage_gate,
        )
    )

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "archive_written" if status == "closed" else "archive_blocked"
    next_allowed_slices = NEXT_ALLOWED_SLICES if status == "closed" else []
    next_required_command = NEXT_REQUIRED_COMMAND if status == "closed" else "life-v0 run-replay-shadow --strict"

    archive_batch = _build_growth_archive_receipt_batch(
        run_id=run_id,
        generated_at=generated_at,
        growth_patch_queue=growth_patch_queue,
        next_feedback_seed=next_feedback_seed,
        replay_seed_bundle=replay_seed_bundle,
        language_probe=language_probe,
        replay_report=replay_report,
    )
    shadow_preconditions = _build_shadow_run_preconditions(
        run_id=run_id,
        generated_at=generated_at,
        replay_arbitration=replay_arbitration,
        replay_stage_gate=replay_stage_gate,
        archive_batch=archive_batch,
    )
    shadow_handoff = _build_growth_archive_to_shadow_handoff(
        run_id=run_id,
        generated_at=generated_at,
        archive_batch=archive_batch,
        shadow_preconditions=shadow_preconditions,
        replay_report=replay_report,
    )

    report_refs = [
        "runtime/reports/latest/run_report.json",
        "runtime/reports/latest/growth_reconsolidation_report.json",
        "runtime/reports/latest/replay_shadow_report.json",
        "runtime/reports/latest/growth_archive_report.json",
        "runtime/reports/latest/growth_archive_digest.json",
        "runtime/reports/latest/growth_archive_stage_gate.json",
    ]
    state_refs = [
        "runtime/state/archive/growth_archive_receipt_batch.json",
        "runtime/state/archive/shadow_run_preconditions.json",
        "runtime/state/archive/growth_archive_to_shadow_handoff.json",
        "runtime/state/archive/reconsolidation_archive_graph.json",
    ]
    archive_graph = build_reconsolidation_archive_graph(
        run_id=run_id,
        generated_at=generated_at,
        report_refs=report_refs,
        state_refs=state_refs,
    )
    receipt_ref = f"runtime/receipts/write_growth_archive_{run_id}.json"
    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        state_refs=state_refs,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
        receipt_ref=receipt_ref,
    )
    digest = _build_digest(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
    )
    stage_gate = _build_stage_gate(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
    )
    archive_events = _build_archive_events(
        generated_at=generated_at,
        archive_batch=archive_batch,
        shadow_preconditions=shadow_preconditions,
        shadow_handoff=shadow_handoff,
        stage_effect=stage_effect,
    )
    updated_life_state = _integrate_archive_refs(
        life_state=life_state,
        archive_refs=[
            "runtime/archive/growth_archive_events.jsonl",
            "runtime/state/archive/growth_archive_receipt_batch.json",
            "runtime/state/archive/shadow_run_preconditions.json",
            "runtime/state/archive/growth_archive_to_shadow_handoff.json",
            receipt_ref,
        ],
    )
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
        state_refs=state_refs,
    )

    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
        runtime_archive_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(archive_dir / "growth_archive_receipt_batch.json", archive_batch)
        _write_json(archive_dir / "shadow_run_preconditions.json", shadow_preconditions)
        _write_json(archive_dir / "growth_archive_to_shadow_handoff.json", shadow_handoff)
        _write_json(archive_dir / "reconsolidation_archive_graph.json", archive_graph)
        _write_json(reports_dir / "growth_archive_report.json", report)
        _write_json(reports_dir / "growth_archive_digest.json", digest)
        _write_json(reports_dir / "growth_archive_stage_gate.json", stage_gate)
        _append_jsonl(runtime_archive_dir / "growth_archive_events.jsonl", archive_events)
        _write_json(state_dir / "life_state.json", updated_life_state)
        _write_json(receipts_dir / f"write_growth_archive_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "archive_write_failed"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return GrowthArchiveResult(exit_code=4, report=report)

    if status == "closed":
        return GrowthArchiveResult(exit_code=0, report=report)
    return GrowthArchiveResult(exit_code=1 if strict else 0, report=report)


def _archive_blockers(
    *,
    life_state: dict[str, Any],
    growth_patch_queue: dict[str, Any],
    next_feedback_seed: dict[str, Any],
    runtime_mount: dict[str, Any],
    shadow_trace: dict[str, Any],
    pain_replay: dict[str, Any],
    replay_seed_bundle: dict[str, Any],
    language_probe: dict[str, Any],
    dream_probe: dict[str, Any],
    shadow_expression: dict[str, Any],
    replay_arbitration: dict[str, Any],
    replay_report: dict[str, Any],
    replay_digest: dict[str, Any],
    replay_stage_gate: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("life_state_gate schema mismatch")
    if growth_patch_queue.get("schema_version") != "growth_patch_queue_v0":
        reasons.append("growth_patch_queue_gate schema mismatch")
    if next_feedback_seed.get("schema_version") != "next_feedback_seed_v0":
        reasons.append("next_feedback_seed_gate schema mismatch")
    if runtime_mount.get("schema_version") != "runtime_mount_state_v0":
        reasons.append("runtime_mount_gate schema mismatch")
    if shadow_trace.get("schema_version") != "shadow_cycle_trace_v0":
        reasons.append("shadow_trace_gate schema mismatch")
    if pain_replay.get("schema_version") != "pain_regret_responsibility_replay_v0":
        reasons.append("pain_replay_gate schema mismatch")
    if replay_seed_bundle.get("schema_version") != "replay_shadow_seed_bundle_v0":
        reasons.append("replay_seed_bundle_gate schema mismatch")
    if language_probe.get("schema_version") != "language_relationship_replay_probe_v0":
        reasons.append("language_probe_gate schema mismatch")
    if dream_probe.get("schema_version") != "dream_pain_regret_replay_probe_v0":
        reasons.append("dream_probe_gate schema mismatch")
    if shadow_expression.get("schema_version") != "shadow_expression_report_v0":
        reasons.append("shadow_expression_gate schema mismatch")
    if replay_arbitration.get("schema_version") != "replay_shadow_arbitration_v0":
        reasons.append("replay_arbitration_gate schema mismatch")
    if replay_arbitration.get("selected_route") != "write_growth_archive":
        reasons.append("replay_arbitration_gate selected route mismatch")
    if replay_report.get("schema_version") != "replay_shadow_report_v0":
        reasons.append("replay_report_gate schema mismatch")
    if replay_report.get("status") != "closed":
        reasons.append("replay_report_gate status is not closed")
    if replay_report.get("next_required_command") != "life-v0 write-growth-archive --strict":
        reasons.append("replay_report_gate next command mismatch")
    if replay_digest.get("schema_version") != "replay_shadow_digest_v0":
        reasons.append("replay_digest_gate schema mismatch")
    if replay_digest.get("current_phase") != "replay_shadow":
        reasons.append("replay_digest_gate current phase mismatch")
    if replay_stage_gate.get("schema_version") != "replay_shadow_stage_gate_v0":
        reasons.append("replay_stage_gate_gate schema mismatch")
    if replay_stage_gate.get("decision") != "closed":
        reasons.append("replay_stage_gate_gate decision is not closed")
    if not replay_seed_bundle.get("source_seed_refs"):
        reasons.append("replay_seed_bundle_gate source seed refs missing")
    if not growth_patch_queue.get("queued_patch_families"):
        reasons.append("growth_patch_queue_gate queued patch families missing")
    if not language_probe.get("shared_language_refs"):
        reasons.append("language_probe_gate shared language refs missing")
    if dream_probe.get("dream_fact_gate") != "closed":
        reasons.append("dream_probe_gate dream fact gate is not closed")
    if not shadow_expression.get("expression_trace"):
        reasons.append("shadow_expression_gate expression trace missing")
    return reasons


def _build_growth_archive_receipt_batch(
    *,
    run_id: str,
    generated_at: str,
    growth_patch_queue: dict[str, Any],
    next_feedback_seed: dict[str, Any],
    replay_seed_bundle: dict[str, Any],
    language_probe: dict[str, Any],
    replay_report: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "growth_archive_receipt_batch_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "growth_patch_receipt_refs": [
            "runtime/state/growth/growth_patch_queue.json",
            "runtime/state/growth/next_feedback_seed.json",
        ],
        "self_rewrite_archive_receipt_refs": [
            "runtime/state/growth/growth_patch_queue.json#anti_forgetting_replay_patch",
            "runtime/state/growth/growth_patch_queue.json#dream_reconsolidation_patch",
        ],
        "language_action_archive_receipt_refs": list(language_probe.get("shared_language_refs", [])),
        "birth_readiness_effect_archive_receipt_refs": [
            "runtime/reports/latest/birth_readiness_report.json",
            "runtime/reports/latest/replay_shadow_report.json",
        ],
        "anti_forgetting_replay_archive_receipt_refs": list(replay_seed_bundle.get("memory_replay_refs", [])),
        "shadow_run_seed_archive_receipt_refs": [
            "runtime/state/replay/replay_shadow_seed_bundle.json",
            "runtime/state/replay/shadow_expression_report.json",
        ],
        "life_target_growth_carrier_receipt_refs": [
            "runtime/reports/latest/life_target_status.json",
            "runtime/reports/latest/replay_shadow_report.json",
        ],
        "direction_growth_archive_receipt_refs": [
            "runtime/state/direction/direction_lock.json",
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
        ],
        "digest_baseline_ref": "runtime/reports/latest/replay_shadow_digest.json",
        "dashboard_stage_receipt_refs": [
            "runtime/reports/latest/replay_shadow_report.json",
            "runtime/reports/latest/replay_shadow_stage_gate.json",
        ],
        "archive_edge_receipt_refs": [
            "runtime/state/archive/reconsolidation_archive_graph.json",
            "runtime/state/archive/growth_archive_receipt_batch.json",
        ],
        "shadow_run_handoff_ref": "runtime/state/archive/growth_archive_to_shadow_handoff.json",
        "queued_patch_families": list(growth_patch_queue.get("queued_patch_families", [])),
        "seed_families": list(next_feedback_seed.get("seed_families", [])),
        "report_ref": replay_report.get("engineering_slice_ref", ACTIVE_SLICE),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_shadow_run_preconditions(
    *,
    run_id: str,
    generated_at: str,
    replay_arbitration: dict[str, Any],
    replay_stage_gate: dict[str, Any],
    archive_batch: dict[str, Any],
) -> dict[str, Any]:
    preconditions_ready = (
        replay_arbitration.get("selected_route") == "write_growth_archive"
        and replay_stage_gate.get("decision") == "closed"
        and bool(archive_batch.get("shadow_run_seed_archive_receipt_refs"))
    )
    return {
        "schema_version": "shadow_run_preconditions_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed" if preconditions_ready else "blocked",
        "preconditions_ready": preconditions_ready,
        "required_refs": [
            "runtime/state/archive/growth_archive_receipt_batch.json",
            "runtime/reports/latest/replay_shadow_stage_gate.json",
            "runtime/state/replay/replay_shadow_arbitration.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_growth_archive_to_shadow_handoff(
    *,
    run_id: str,
    generated_at: str,
    archive_batch: dict[str, Any],
    shadow_preconditions: dict[str, Any],
    replay_report: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "growth_archive_to_shadow_handoff_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed" if shadow_preconditions.get("preconditions_ready") else "blocked",
        "shadow_run_handoff_ready": bool(shadow_preconditions.get("preconditions_ready")),
        "growth_archive_receipt_batch_ref": "runtime/state/archive/growth_archive_receipt_batch.json",
        "shadow_run_precondition_refs": ["runtime/state/archive/shadow_run_preconditions.json"],
        "shadow_run_seed_archive_receipt_refs": list(archive_batch.get("shadow_run_seed_archive_receipt_refs", [])),
        "language_action_archive_receipt_refs": list(archive_batch.get("language_action_archive_receipt_refs", [])),
        "birth_readiness_effect_archive_receipt_refs": list(
            archive_batch.get("birth_readiness_effect_archive_receipt_refs", [])
        ),
        "anti_forgetting_replay_archive_receipt_refs": list(
            archive_batch.get("anti_forgetting_replay_archive_receipt_refs", [])
        ),
        "report_ref": replay_report.get("schema_version", "replay_shadow_report_v0"),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    state_refs: list[str],
    next_allowed_slices: list[str],
    next_required_command: str,
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "growth_archive_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "state_refs": state_refs,
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
        "receipt_ref": receipt_ref,
    }


def _build_digest(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    next_allowed_slices: list[str],
    next_required_command: str,
) -> dict[str, Any]:
    return {
        "schema_version": "growth_archive_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_phase": "growth_archive",
        "status": status,
        "stage_effect": stage_effect,
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
    }


def _build_stage_gate(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    next_allowed_slices: list[str],
    next_required_command: str,
) -> dict[str, Any]:
    return {
        "schema_version": "growth_archive_stage_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "decision": status,
        "stage_effect": stage_effect,
        "gates": {
            "archive_receipt_gate": "closed" if status == "closed" else "blocked",
            "shadow_precondition_gate": "closed" if status == "closed" else "blocked",
            "handoff_gate": "closed" if status == "closed" else "blocked",
            "state_writeback_gate": "closed" if status == "closed" else "blocked",
        },
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
    }


def _build_archive_events(
    *,
    generated_at: str,
    archive_batch: dict[str, Any],
    shadow_preconditions: dict[str, Any],
    shadow_handoff: dict[str, Any],
    stage_effect: str,
) -> list[dict[str, Any]]:
    return [
        {
            "event_type": "growth_archive_receipt_batch",
            "generated_at": generated_at,
            "stage_effect": stage_effect,
            "archive_batch_ref": "runtime/state/archive/growth_archive_receipt_batch.json",
            "shadow_run_preconditions_ref": "runtime/state/archive/shadow_run_preconditions.json",
            "shadow_handoff_ref": "runtime/state/archive/growth_archive_to_shadow_handoff.json",
            "receipt_counts": {
                "growth_patch": len(archive_batch.get("growth_patch_receipt_refs", [])),
                "language_action": len(archive_batch.get("language_action_archive_receipt_refs", [])),
                "anti_forgetting": len(archive_batch.get("anti_forgetting_replay_archive_receipt_refs", [])),
            },
            "preconditions_ready": bool(shadow_preconditions.get("preconditions_ready")),
            "shadow_run_handoff_ready": bool(shadow_handoff.get("shadow_run_handoff_ready")),
        }
    ]


def _integrate_archive_refs(*, life_state: dict[str, Any], archive_refs: list[str]) -> dict[str, Any]:
    updated = json.loads(json.dumps(life_state))
    current = updated.setdefault("archive_refs", [])
    for ref in archive_refs:
        if ref not in current:
            current.append(ref)
    updated.setdefault("runtime_trace_refs", [])
    for ref in [
        "runtime/state/archive/growth_archive_receipt_batch.json",
        "runtime/state/archive/shadow_run_preconditions.json",
        "runtime/state/archive/growth_archive_to_shadow_handoff.json",
    ]:
        if ref not in updated["runtime_trace_refs"]:
            updated["runtime_trace_refs"].append(ref)
    return updated


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
    state_refs: list[str],
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        state_dir / "replay" / "replay_shadow_seed_bundle.json",
        state_dir / "replay" / "language_relationship_replay_probe.json",
        state_dir / "replay" / "dream_pain_regret_replay_probe.json",
        state_dir / "replay" / "shadow_expression_report.json",
        reports_dir / "replay_shadow_report.json",
        reports_dir / "replay_shadow_digest.json",
        reports_dir / "replay_shadow_stage_gate.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)

    output_paths = [
        *(state_dir.parent / ref.replace("runtime/", "") for ref in state_refs),
        reports_dir / "growth_archive_report.json",
        reports_dir / "growth_archive_digest.json",
        reports_dir / "growth_archive_stage_gate.json",
        state_dir.parent / "archive" / "growth_archive_events.jsonl",
        receipts_dir / f"write_growth_archive_{run_id}.json",
    ]

    return {
        "schema_version": "write_growth_archive_receipt_v0",
        "receipt_id": f"write_growth_archive_{run_id}",
        "run_id": run_id,
        "command": "write-growth-archive",
        "state_ref": "runtime/state",
        "report_refs": [
            "runtime/reports/latest/growth_archive_report.json",
            "runtime/reports/latest/growth_archive_digest.json",
            "runtime/reports/latest/growth_archive_stage_gate.json",
        ],
        "archive_refs": [
            "runtime/archive/growth_archive_events.jsonl",
            "runtime/state/archive/growth_archive_receipt_batch.json",
            "runtime/state/archive/shadow_run_preconditions.json",
            "runtime/state/archive/growth_archive_to_shadow_handoff.json",
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
    except FileNotFoundError:
        blocked_reasons.append(f"{gate} missing: {path}")
    except json.JSONDecodeError as exc:
        blocked_reasons.append(f"{gate} decode failed: {exc}")
    except OSError as exc:
        blocked_reasons.append(f"{gate} read failed: {exc}")
    return {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, payloads: list[dict[str, Any]]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for payload in payloads:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return _sha256(path)


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
