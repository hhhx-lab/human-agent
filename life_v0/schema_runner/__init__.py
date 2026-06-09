from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .comparison_trace import build_comparison_trace, check_comparison_trace
from .consistency_logic import build_consistency_logic, check_consistency_logic
from .counterfactual_eval import build_counterfactual_trace, check_counterfactual_trace

ACTIVE_SLICE = "S09_SCHEMA_RUNNER_CODE"
NEXT_ALLOWED_SLICES = ["S06_LIFE_SUPPORT_DEVELOPMENT", "S10_RUNTIME_GROWTH_RECONSOLIDATION"]
NEXT_REQUIRED_COMMAND = "life-v0 build-life-support --strict"

READ_ME_BLOCK_REFS = [
    "B24_SCHEMA_BUNDLE_RUNNER",
    "B26_REPOSITORY_RUNNER_MATERIALIZATION",
    "B28_FIRST_CODE_SCHEMA_ARTIFACT",
]

RUNTIME_CARRIERS = [
    "SchemaBundleCompiler",
    "RunnerRepositoryKernel",
    "FirstRunnerCodeKernel",
]

EXTRA_SOURCE_DOCS = [
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md",
    "docs/v0/slice_contracts/s09_schema_runner_code_engineering_contract.md",
]


@dataclass(frozen=True)
class SchemaRunnerResult:
    exit_code: int
    report: dict[str, Any]


def run_schema_runner(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> SchemaRunnerResult:
    run_id = run_id or _default_run_id()
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    out_dir = state_dir / "schema_runner"

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"input path is not a directory: {docs_dir}")
    if not doc_index_path.exists():
        blocked_reasons.append(f"doc carrier index is missing: {doc_index_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    birth_report = _load_json(reports_dir / "birth_readiness_report.json", blocked_reasons, "birth_readiness_gate")
    validation_report = _load_json(reports_dir / "validation_membrane_report.json", blocked_reasons, "validation_membrane_gate")
    validation_check = _load_json(reports_dir / "validation_membrane_check_report.json", blocked_reasons, "validation_membrane_check_gate")
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "state_store_gate")
    validation_stage = _load_json(state_dir / "validation" / "validation_stage_gate.json", blocked_reasons, "validation_stage_gate")
    action_candidate_set = _load_json(state_dir / "action" / "action_candidate_set.json", blocked_reasons, "action_candidate_gate")
    world_contact_gate = _load_json(state_dir / "action" / "world_contact_gate_state.json", blocked_reasons, "world_contact_gate")
    observation_truth_review = _load_json(
        state_dir / "validation" / "observation_truth_review.json",
        blocked_reasons,
        "observation_truth_gate",
    )
    boundary_audit = _load_json(state_dir / "validation" / "boundary_audit_state.json", blocked_reasons, "boundary_audit_gate")
    side_effect_review = _load_json(state_dir / "action" / "side_effect_review.json", blocked_reasons, "side_effect_gate")

    source_docs = _collect_s09_source_docs(doc_index)
    blocked_reasons.extend(_doc_blockers(doc_index, source_docs))
    blocked_reasons.extend(_previous_slice_blockers(birth_report, validation_report, validation_check, validation_stage))
    blocked_reasons.extend(_state_blockers(life_state))

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_next_slice" if status == "closed" else "block_activation"
    receipt_ref = f"runtime/receipts/schema_runner_{run_id}.json"

    registry = _build_schema_registry(run_id, generated_at, source_docs)
    lockfile = _build_dependency_lockfile(run_id, generated_at, source_docs, status)
    command_queue = _build_command_queue(run_id, generated_at, status)
    checker_manifest = _build_checker_manifest(run_id, generated_at, status)
    consistency_logic = build_consistency_logic(
        run_id=run_id,
        generated_at=generated_at,
        action_candidate_set=action_candidate_set,
        observation_truth_review=observation_truth_review,
        boundary_audit=boundary_audit,
    )
    counterfactual_trace = build_counterfactual_trace(
        run_id=run_id,
        generated_at=generated_at,
        action_candidate_set=action_candidate_set,
        world_contact_gate=world_contact_gate,
        side_effect_review=side_effect_review,
    )
    comparison_trace = build_comparison_trace(
        run_id=run_id,
        generated_at=generated_at,
        counterfactual_trace=counterfactual_trace,
        consistency_logic=consistency_logic,
    )
    artifact_manifest = _build_artifact_manifest(run_id, generated_at, status)
    stage_gate = _build_stage_gate(run_id, generated_at, status, stage_effect, blocked_reasons)
    report = _build_report(run_id, generated_at, status, stage_effect, source_docs, blocked_reasons, receipt_ref)
    digest = _build_digest(run_id, generated_at, status, stage_effect, blocked_reasons)
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        state_dir=state_dir,
        out_dir=out_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
        source_docs=source_docs,
    )

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(out_dir / "schema_registry.json", registry)
        _write_json(out_dir / "schema_dependency_lockfile.json", lockfile)
        _write_json(out_dir / "runner_command_queue.json", command_queue)
        _write_json(out_dir / "cross_file_checker_manifest.json", checker_manifest)
        _write_json(out_dir / "first_code_artifact_manifest.json", artifact_manifest)
        _write_json(out_dir / "consistency_logic.json", consistency_logic)
        _write_json(out_dir / "counterfactual_trace.json", counterfactual_trace)
        _write_json(out_dir / "comparison_trace.json", comparison_trace)
        _write_json(out_dir / "schema_runner_stage_gate.json", stage_gate)
        _write_json(reports_dir / "schema_runner_report.json", report)
        _write_json(reports_dir / "schema_runner_digest.json", digest)
        _write_json(receipts_dir / f"schema_runner_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return SchemaRunnerResult(exit_code=4, report=report)

    if status == "closed":
        return SchemaRunnerResult(exit_code=0, report=report)
    return SchemaRunnerResult(exit_code=1 if strict else 0, report=report)


def run_check_schema_runner(
    *,
    state_dir: Path,
    reports_dir: Path,
    strict: bool = False,
) -> SchemaRunnerResult:
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    generated_at = _now_iso()
    blocked_reasons: list[str] = []

    registry = _load_json(state_dir / "schema_registry.json", blocked_reasons, "schema_bundle_gate")
    lockfile = _load_json(state_dir / "schema_dependency_lockfile.json", blocked_reasons, "registry_gate")
    command_queue = _load_json(state_dir / "runner_command_queue.json", blocked_reasons, "command_queue_gate")
    checker_manifest = _load_json(state_dir / "cross_file_checker_manifest.json", blocked_reasons, "checker_manifest_gate")
    artifact_manifest = _load_json(state_dir / "first_code_artifact_manifest.json", blocked_reasons, "code_artifact_gate")
    consistency_logic = _load_json(state_dir / "consistency_logic.json", blocked_reasons, "consistency_logic_gate")
    counterfactual_trace = _load_json(state_dir / "counterfactual_trace.json", blocked_reasons, "counterfactual_gate")
    comparison_trace = _load_json(state_dir / "comparison_trace.json", blocked_reasons, "comparison_trace_gate")
    stage_gate = _load_json(state_dir / "schema_runner_stage_gate.json", blocked_reasons, "next_slice_gate")
    build_report = _load_json(reports_dir / "schema_runner_report.json", blocked_reasons, "build_report_gate")

    blocked_reasons.extend(_check_registry(registry))
    blocked_reasons.extend(_check_lockfile(lockfile))
    blocked_reasons.extend(_check_command_queue(command_queue))
    blocked_reasons.extend(_check_checker_manifest(checker_manifest))
    blocked_reasons.extend(_check_artifact_manifest(artifact_manifest))
    blocked_reasons.extend(check_consistency_logic(consistency_logic))
    blocked_reasons.extend(check_counterfactual_trace(counterfactual_trace))
    blocked_reasons.extend(check_comparison_trace(comparison_trace))
    blocked_reasons.extend(_check_stage_gate(stage_gate))
    blocked_reasons.extend(_check_build_report(build_report))

    status = "closed" if not blocked_reasons else "blocked"
    report = {
        "schema_version": "schema_runner_check_report_v0",
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
        _write_json(reports_dir / "schema_runner_check_report.json", report)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"check_report_write_gate failed: {exc}")
        return SchemaRunnerResult(exit_code=4, report=report)

    if status == "closed":
        return SchemaRunnerResult(exit_code=0, report=report)
    return SchemaRunnerResult(exit_code=1 if strict else 0, report=report)


def run_schema_smoke(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> SchemaRunnerResult:
    run_id = run_id or _default_smoke_run_id()
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    schema_state_dir = state_dir / "schema_runner"
    blocked_reasons: list[str] = []

    registry = _load_json(schema_state_dir / "schema_registry.json", blocked_reasons, "schema_bundle_gate")
    lockfile = _load_json(schema_state_dir / "schema_dependency_lockfile.json", blocked_reasons, "registry_gate")
    command_queue = _load_json(schema_state_dir / "runner_command_queue.json", blocked_reasons, "command_queue_gate")
    stage_gate = _load_json(schema_state_dir / "schema_runner_stage_gate.json", blocked_reasons, "next_slice_gate")
    build_report = _load_json(reports_dir / "schema_runner_report.json", blocked_reasons, "build_report_gate")

    blocked_reasons.extend(_check_registry(registry))
    blocked_reasons.extend(_check_lockfile(lockfile))
    blocked_reasons.extend(_check_command_queue(command_queue))
    blocked_reasons.extend(_check_stage_gate(stage_gate))
    blocked_reasons.extend(_check_build_report(build_report))

    status = "closed" if not blocked_reasons else "blocked"
    smoke_report = {
        "schema_version": "schema_runner_smoke_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "stage_effect": "allow_next_slice" if status == "closed" else "block_activation",
        "active_engineering_slice": ACTIVE_SLICE,
        "smoke_commands": ["build-schema-runner", "check-schema-runner", "run-schema-smoke"],
        "report_refs": [
            "runtime/reports/latest/schema_runner_report.json",
            "runtime/reports/latest/schema_runner_check_report.json",
            "runtime/reports/latest/schema_smoke_report.json",
        ],
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "schema_smoke_report.json", smoke_report)
        _write_json(
            receipts_dir / f"schema_smoke_{run_id}.json",
            {
                "schema_version": "schema_smoke_receipt_v0",
                "receipt_id": f"schema_smoke_{run_id}",
                "run_id": run_id,
                "command": "run-schema-smoke",
                "created_at": generated_at,
                "report_refs": ["runtime/reports/latest/schema_smoke_report.json"],
                "stage_effect": smoke_report["stage_effect"],
            },
        )
    except OSError as exc:
        smoke_report["status"] = "blocked"
        smoke_report["stage_effect"] = "block_activation"
        smoke_report["blocked_reasons"].append(f"smoke_report_write_gate failed: {exc}")
        return SchemaRunnerResult(exit_code=4, report=smoke_report)

    if status == "closed":
        return SchemaRunnerResult(exit_code=0, report=smoke_report)
    return SchemaRunnerResult(exit_code=1 if strict else 0, report=smoke_report)


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blocked_reasons.append(f"{gate} failed: {exc}")
        return {}


def _collect_s09_source_docs(doc_index: dict[str, Any]) -> list[str]:
    docs = []
    for doc in doc_index.get("documents", []):
        if not isinstance(doc, dict):
            continue
        path = doc.get("path")
        sequence = doc.get("sequence")
        if isinstance(path, str) and isinstance(sequence, int) and 102 <= sequence <= 180:
            docs.append((sequence, path))
    docs.sort()
    ordered = [path for _, path in docs]
    for path in EXTRA_SOURCE_DOCS:
        if path not in ordered:
            ordered.append(path)
    return ordered


def _doc_blockers(doc_index: dict[str, Any], source_docs: list[str]) -> list[str]:
    reasons: list[str] = []
    documents = {doc.get("path"): doc for doc in doc_index.get("documents", []) if isinstance(doc, dict)}
    for doc_path in source_docs:
        doc = documents.get(doc_path)
        if not doc:
            reasons.append(f"schema_bundle_gate missing {doc_path}")
            continue
        if not doc.get("runtime_carriers"):
            reasons.append(f"schema_bundle_gate missing runtime carrier for {doc_path}")
    return reasons


def _previous_slice_blockers(
    birth_report: dict[str, Any],
    validation_report: dict[str, Any],
    validation_check: dict[str, Any],
    validation_stage: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if birth_report.get("overall_status") != "open":
        reasons.append("birth_readiness_gate overall status is not open")
    if validation_report.get("status") != "closed":
        reasons.append("validation_membrane_gate validation report is not closed")
    if ACTIVE_SLICE not in validation_report.get("next_allowed_slices", []):
        reasons.append("validation_membrane_gate S09 is not allowed")
    if validation_check.get("status") != "closed":
        reasons.append("validation_membrane_check_gate validation check is not closed")
    if validation_stage.get("decision") != "closed":
        reasons.append("validation_stage_gate decision is not closed")
    return reasons


def _state_blockers(life_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("state_store_gate schema mismatch")
    if not life_state.get("archive_refs"):
        reasons.append("state_store_gate archive refs missing")
    return reasons


def _build_schema_registry(run_id: str, generated_at: str, source_docs: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "schema_registry_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": ACTIVE_SLICE,
        "source_doc_refs": source_docs,
        "registry_families": [
            "shared_defs",
            "runtime_observation",
            "component_schemas",
            "report_schemas",
            "dashboard_schemas",
            "runner_repository",
            "cross_file_checkers",
            "code_artifacts",
        ],
        "schema_refs": [
            "runtime/state/schema_runner/schema_registry.json#shared_defs",
            "runtime/state/schema_runner/schema_registry.json#component_schemas",
            "runtime/state/schema_runner/schema_registry.json#dashboard_schemas",
        ],
        "artifact_roots": [
            "life_reality_runner/schemas/",
            "life_reality_runner/generation/",
            "life_reality_runner/reports/",
            "life_reality_runner/dashboard/",
        ],
    }


def _build_dependency_lockfile(run_id: str, generated_at: str, source_docs: list[str], status: str) -> dict[str, Any]:
    artifact_nodes = [
        {"artifact_ref": "runtime/state/schema_runner/schema_registry.json", "artifact_kind": "schema_registry"},
        {"artifact_ref": "runtime/state/schema_runner/schema_dependency_lockfile.json", "artifact_kind": "dependency_lockfile"},
        {"artifact_ref": "runtime/state/schema_runner/runner_command_queue.json", "artifact_kind": "runner_command_queue"},
        {"artifact_ref": "runtime/state/schema_runner/cross_file_checker_manifest.json", "artifact_kind": "checker_manifest"},
        {"artifact_ref": "runtime/state/schema_runner/first_code_artifact_manifest.json", "artifact_kind": "code_artifact_manifest"},
    ]
    doc_nodes = [{"doc_path": path, "future_runtime_carrier": _carrier_hint(path)} for path in source_docs]
    ref_edges = [
        {"source": "schema_registry", "target": "dependency_lockfile", "ref_kind": "registry_depends_on_bundle"},
        {"source": "dependency_lockfile", "target": "runner_command_queue", "ref_kind": "lockfile_drives_queue"},
        {"source": "runner_command_queue", "target": "first_code_artifact_manifest", "ref_kind": "queue_emits_artifacts"},
    ]
    return {
        "schema_version": "schema_dependency_lockfile_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "artifact_nodes": artifact_nodes,
        "doc_nodes": doc_nodes,
        "ref_edges": ref_edges,
        "consistency_constraints": [
            "CONSISTENCY-001 life-target-canonical",
            "CONSISTENCY-005 shell-not-core",
            "CONSISTENCY-006 language-as-core",
            "CONSISTENCY-009 implementation-carrier-present",
        ],
        "next_growth_artifacts": ["life_v0/body/", "life_v0/growth/", "life_v0/archive/"],
    }


def _build_command_queue(run_id: str, generated_at: str, status: str) -> dict[str, Any]:
    return {
        "schema_version": "runner_command_queue_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "commands": [
            "build-schema-runner",
            "check-schema-runner",
            "run-schema-smoke",
        ],
        "preconditions": [
            "birth_readiness_report_open",
            "validation_membrane_report_closed",
            "validation_membrane_check_report_closed",
        ],
        "next_stage_commands": [
            "build-life-support",
            "check-life-support",
            "run-cycle",
        ],
        "exit_code_contract": {
            "0": "allow_next_slice",
            "1": "blocked",
            "4": "write_failed",
        },
    }


def _build_checker_manifest(run_id: str, generated_at: str, status: str) -> dict[str, Any]:
    return {
        "schema_version": "cross_file_checker_manifest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "checker_families": [
            "language_action_cross_file",
            "authority_schema_cross_file",
            "birth_readiness_cross_file",
            "full_archive_rollup",
        ],
        "report_refs": [
            "runtime/reports/latest/birth_readiness_report.json",
            "runtime/reports/latest/validation_membrane_report.json",
            "runtime/reports/latest/validation_membrane_check_report.json",
        ],
        "lockfile_refs": [
            "runtime/state/schema_runner/schema_dependency_lockfile.json",
            "runtime/state/schema_runner/runner_command_queue.json",
        ],
    }


def _build_artifact_manifest(run_id: str, generated_at: str, status: str) -> dict[str, Any]:
    return {
        "schema_version": "first_code_artifact_manifest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "code_roots": [
            "life_v0/schema_runner/",
            "life_v0/cli.py",
        ],
        "artifact_refs": [
            "life_v0/schema_runner/__init__.py",
            "life_v0/cli.py",
            "runtime/state/schema_runner/schema_registry.json",
            "runtime/state/schema_runner/runner_command_queue.json",
            "runtime/state/schema_runner/consistency_logic.json",
            "runtime/state/schema_runner/counterfactual_trace.json",
            "runtime/state/schema_runner/comparison_trace.json",
        ],
        "test_refs": [
            "tests/slices/test_schema_runner.py",
        ],
        "smoke_report_refs": [
            "runtime/reports/latest/schema_smoke_report.json",
        ],
    }


def _build_stage_gate(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    gates = [
        "schema_bundle_gate",
        "registry_gate",
        "checker_manifest_gate",
        "code_artifact_gate",
        "cli_report_gate",
        "next_slice_gate",
    ]
    return {
        "schema_version": "schema_runner_stage_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "decision": status,
        "stage_effect": stage_effect,
        "gate_status": {gate: "closed" for gate in gates} if status == "closed" else {gate: "blocked" for gate in _blocked_gates(blocked_reasons)},
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_report(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    source_docs: list[str],
    blocked_reasons: list[str],
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "s09_schema_runner_code_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "source_doc_refs": source_docs,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIERS,
        "schema_refs": [
            "runtime/state/schema_runner/schema_registry.json",
            "runtime/state/schema_runner/schema_dependency_lockfile.json",
        ],
        "command_refs": [
            "life-v0 build-schema-runner",
            "life-v0 check-schema-runner",
            "life-v0 run-schema-smoke",
        ],
        "artifact_refs": [
            "runtime/state/schema_runner/runner_command_queue.json",
            "runtime/state/schema_runner/cross_file_checker_manifest.json",
            "runtime/state/schema_runner/first_code_artifact_manifest.json",
            "runtime/state/schema_runner/consistency_logic.json",
            "runtime/state/schema_runner/counterfactual_trace.json",
            "runtime/state/schema_runner/comparison_trace.json",
        ],
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "receipt_refs": [receipt_ref],
    }


def _build_digest(
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "schema_runner_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_slice": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
    source_docs: list[str],
) -> dict[str, Any]:
    input_hashes = {
        ref: _sha256(docs_dir.parent / ref)
        for ref in source_docs
        if (docs_dir.parent / ref).exists()
    }
    for path in [
        doc_index_path,
        state_dir / "life_state.json",
        reports_dir / "birth_readiness_report.json",
        reports_dir / "validation_membrane_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)
    output_refs = [
        out_dir / "schema_registry.json",
        out_dir / "schema_dependency_lockfile.json",
        out_dir / "runner_command_queue.json",
        out_dir / "cross_file_checker_manifest.json",
        out_dir / "first_code_artifact_manifest.json",
        out_dir / "consistency_logic.json",
        out_dir / "counterfactual_trace.json",
        out_dir / "comparison_trace.json",
        out_dir / "schema_runner_stage_gate.json",
        reports_dir / "schema_runner_report.json",
        reports_dir / "schema_runner_digest.json",
        receipts_dir / f"schema_runner_{run_id}.json",
    ]
    return {
        "schema_version": "schema_runner_receipt_v0",
        "receipt_id": f"schema_runner_{run_id}",
        "run_id": run_id,
        "command": "build-schema-runner",
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_refs": [str(path) for path in output_refs],
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_refs},
        "stage_effect": stage_effect,
        "direction_lock_ref": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    }


def _check_registry(registry: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if registry.get("schema_version") != "schema_registry_v0":
        reasons.append("schema_bundle_gate schema mismatch")
    for family in ["shared_defs", "component_schemas", "dashboard_schemas"]:
        if family not in registry.get("registry_families", []):
            reasons.append(f"schema_bundle_gate missing {family}")
    return reasons


def _check_lockfile(lockfile: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if lockfile.get("schema_version") != "schema_dependency_lockfile_v0":
        reasons.append("registry_gate schema mismatch")
    if lockfile.get("status") != "closed":
        reasons.append("registry_gate status mismatch")
    if not lockfile.get("artifact_nodes"):
        reasons.append("registry_gate artifact nodes missing")
    if not lockfile.get("doc_nodes"):
        reasons.append("registry_gate doc nodes missing")
    if not lockfile.get("ref_edges"):
        reasons.append("registry_gate ref edges missing")
    if "CONSISTENCY-009 implementation-carrier-present" not in lockfile.get("consistency_constraints", []):
        reasons.append("registry_gate consistency constraint missing")
    return reasons


def _check_command_queue(command_queue: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if command_queue.get("schema_version") != "runner_command_queue_v0":
        reasons.append("command_queue_gate schema mismatch")
    if command_queue.get("status") != "closed":
        reasons.append("command_queue_gate status mismatch")
    for command in ["build-schema-runner", "check-schema-runner", "run-schema-smoke"]:
        if command not in command_queue.get("commands", []):
            reasons.append(f"command_queue_gate missing {command}")
    return reasons


def _check_checker_manifest(manifest: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if manifest.get("schema_version") != "cross_file_checker_manifest_v0":
        reasons.append("checker_manifest_gate schema mismatch")
    if manifest.get("status") != "closed":
        reasons.append("checker_manifest_gate status mismatch")
    for checker in ["authority_schema_cross_file", "birth_readiness_cross_file", "full_archive_rollup"]:
        if checker not in manifest.get("checker_families", []):
            reasons.append(f"checker_manifest_gate missing {checker}")
    return reasons


def _check_artifact_manifest(artifact_manifest: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if artifact_manifest.get("schema_version") != "first_code_artifact_manifest_v0":
        reasons.append("code_artifact_gate schema mismatch")
    if artifact_manifest.get("status") != "closed":
        reasons.append("code_artifact_gate status mismatch")
    if "life_v0/schema_runner/" not in artifact_manifest.get("code_roots", []):
        reasons.append("code_artifact_gate schema_runner root missing")
    if "tests/slices/test_schema_runner.py" not in artifact_manifest.get("test_refs", []):
        reasons.append("code_artifact_gate schema runner tests missing")
    return reasons


def _check_stage_gate(stage_gate: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if stage_gate.get("schema_version") != "schema_runner_stage_gate_v0":
        reasons.append("next_slice_gate schema mismatch")
    if stage_gate.get("decision") != "closed":
        reasons.append("next_slice_gate decision mismatch")
    if stage_gate.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("next_slice_gate next allowed mismatch")
    return reasons


def _check_build_report(report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if report.get("schema_version") != "s09_schema_runner_code_report_v0":
        reasons.append("build_report_gate schema mismatch")
    if report.get("status") != "closed":
        reasons.append("build_report_gate status mismatch")
    if report.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("build_report_gate next allowed mismatch")
    return reasons


def _carrier_hint(path: str) -> str:
    try:
        sequence = int(path.split("/", 1)[1].split("_", 1)[0])
    except (IndexError, ValueError):
        return "SchemaBundleCompiler"
    if 102 <= sequence <= 118:
        return "SchemaBundleCompiler"
    if 120 <= sequence <= 139:
        return "RunnerRepositoryKernel"
    if 140 <= sequence <= 157:
        return "AuthorityReadinessRuntime"
    if 158 <= sequence <= 180:
        return "FirstRunnerCodeKernel"
    return "RunnerRepositoryKernel"


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    if blocked_reasons:
        return []
    return [
        "schema_bundle_gate",
        "registry_gate",
        "checker_manifest_gate",
        "code_artifact_gate",
        "cli_report_gate",
        "next_slice_gate",
    ]


def _blocked_gates(blocked_reasons: list[str]) -> list[str]:
    gates = []
    for reason in blocked_reasons:
        gate = reason.split(" ", 1)[0]
        if gate not in gates:
            gates.append(gate)
    return gates


def _default_run_id() -> str:
    return "schema-runner-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _default_smoke_run_id() -> str:
    return "schema-smoke-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_if_exists(path: Path) -> str:
    if not path.exists():
        return "pending_write"
    return _sha256(path)
