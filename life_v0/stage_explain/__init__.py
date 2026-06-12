from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_DOC_REFS = [
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
    "docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md",
]

READ_ME_BLOCK_REFS = [
    "B21_LANGUAGE_RELATIONSHIP_CORE",
    "B29_RUNTIME_MOUNT_GROWTH",
    "B30_RECONSOLIDATION_REPLAY_GROWTH",
    "B99_V0_ENGINEERING_CONTRACTS",
]

RUNTIME_CARRIER_REFS = [
    "LanguageRelationshipRuntime",
    "ActivationGrowthRuntime",
    "ReconsolidationReplayRuntime",
    "V0ContractCoverageRuntime",
]


@dataclass(frozen=True)
class ExplainStageResult:
    exit_code: int
    report: dict[str, Any]


def run_explain_stage(
    *,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> ExplainStageResult:
    run_id = run_id or _default_run_id("explain-stage-")
    generated_at = _now_iso()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    blocked_reasons: list[str] = []

    report_bundle = _load_json(reports_dir / "report_bundle.json", blocked_reasons, "report_bundle_gate")
    return_packet = _load_json(
        reports_dir / "first_activation_return_packet.json",
        blocked_reasons,
        "return_packet_gate",
    )
    latest_stage_ref = _load_json(
        reports_dir / "latest_stage_explanation_ref.json",
        blocked_reasons,
        "latest_stage_ref_gate",
    )
    archive_stage_gate = _load_json(
        reports_dir / "growth_archive_stage_gate.json",
        blocked_reasons,
        "archive_stage_gate_gate",
    )

    blocked_reasons.extend(
        _explain_stage_blockers(
            report_bundle=report_bundle,
            return_packet=return_packet,
            latest_stage_ref=latest_stage_ref,
            archive_stage_gate=archive_stage_gate,
        )
    )

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "report_bundle_closed" if status == "closed" else "stage_explanation_blocked"
    decision = "ready_for_terminal_birth_restore" if status == "closed" else "blocked"
    next_required_command = (
        "my digital life" if status == "closed" else "life-v0 emit-report --strict"
    )
    followup_required_command = (
        "re-run life-v0 check-v0-contracts --strict before terminal birth if runtime state changes"
        if status == "closed"
        else "life-v0 check-v0-contracts --strict"
    )

    report = {
        "schema_version": "stage_explanation_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "stage_effect": stage_effect,
        "decision": decision,
        "explanation": (
            "report bundle and first activation return packet are closed; the next closure is terminal birth restore through the digital life shell"
            if status == "closed"
            else "stage explanation is blocked because required chain-tail artifacts are incomplete"
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "source_stage_gate_ref": "runtime/reports/latest/growth_archive_stage_gate.json",
        "source_report_bundle_ref": "runtime/reports/latest/report_bundle.json",
        "source_return_packet_ref": "runtime/reports/latest/first_activation_return_packet.json",
        "blocked_reasons": blocked_reasons,
        "next_required_command": next_required_command,
        "followup_required_command": followup_required_command,
        "receipt_ref": f"runtime/receipts/explain_stage_{run_id}.json",
    }
    latest_ref_payload = {
        "schema_version": "latest_stage_explanation_ref_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "source_stage_gate_ref": "runtime/reports/latest/growth_archive_stage_gate.json",
        "stage_effect": stage_effect,
        "next_required_command": next_required_command,
    }
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
    )

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "stage_explanation_report.json", report)
        _write_json(reports_dir / "latest_stage_explanation_ref.json", latest_ref_payload)
        _write_json(receipts_dir / f"explain_stage_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "stage_explanation_blocked"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return ExplainStageResult(exit_code=4, report=report)

    if status == "closed":
        return ExplainStageResult(exit_code=0, report=report)
    return ExplainStageResult(exit_code=1 if strict else 0, report=report)


def _explain_stage_blockers(
    *,
    report_bundle: dict[str, Any],
    return_packet: dict[str, Any],
    latest_stage_ref: dict[str, Any],
    archive_stage_gate: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if report_bundle.get("schema_version") != "report_bundle_v0":
        reasons.append("report_bundle_gate schema mismatch")
    if report_bundle.get("status") != "closed":
        reasons.append("report_bundle_gate status is not closed")
    if return_packet.get("schema_version") != "first_activation_return_packet_v0":
        reasons.append("return_packet_gate schema mismatch")
    if return_packet.get("status") != "closed":
        reasons.append("return_packet_gate status is not closed")
    if not return_packet.get("relation_restore_refs"):
        reasons.append("return_packet_gate relation restore refs missing")
    if not return_packet.get("shared_term_restore_refs"):
        reasons.append("return_packet_gate shared term restore refs missing")
    if not return_packet.get("unresolved_commitment_refs"):
        reasons.append("return_packet_gate unresolved commitment refs missing")
    if not return_packet.get("expression_monitor_restore_refs"):
        reasons.append("return_packet_gate expression monitor restore refs missing")
    if latest_stage_ref.get("schema_version") != "latest_stage_explanation_ref_v0":
        reasons.append("latest_stage_ref_gate schema mismatch")
    if archive_stage_gate.get("decision") != "closed":
        reasons.append("archive_stage_gate_gate decision is not closed")
    return reasons


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    reports_dir: Path,
    receipts_dir: Path,
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        reports_dir / "report_bundle.json",
        reports_dir / "first_activation_return_packet.json",
        reports_dir / "latest_stage_explanation_ref.json",
        reports_dir / "growth_archive_stage_gate.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)

    output_paths = [
        reports_dir / "stage_explanation_report.json",
        reports_dir / "latest_stage_explanation_ref.json",
        receipts_dir / f"explain_stage_{run_id}.json",
    ]
    return {
        "schema_version": "explain_stage_receipt_v0",
        "receipt_id": f"explain_stage_{run_id}",
        "run_id": run_id,
        "command": "explain-stage",
        "report_refs": [
            "runtime/reports/latest/stage_explanation_report.json",
            "runtime/reports/latest/latest_stage_explanation_ref.json",
        ],
        "stage_effect": "report_bundle_closed",
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
