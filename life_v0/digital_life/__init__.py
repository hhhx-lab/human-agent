from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_DOC_REFS = [
    "docs/v0/references/current_agent_shell_reference_2026.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/architecture/runtime_v0_architecture.md",
    "docs/v0/architecture/first_activation_engineering_roadmap.md",
    "docs/v0/slice_contracts/s00_direction_foundation_engineering_contract.md",
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
]

READ_ME_BLOCK_REFS = [
    "B21_LANGUAGE_RELATIONSHIP_CORE",
    "B29_RUNTIME_MOUNT_GROWTH",
    "B30_RECONSOLIDATION_REPLAY_GROWTH",
    "B99_V0_ENGINEERING_CONTRACTS",
]

RUNTIME_CARRIER_REFS = [
    "DirectionLockKernel",
    "LifeStateStore",
    "LanguageRelationshipRuntime",
    "ActivationGrowthRuntime",
    "ReconsolidationReplayRuntime",
]


@dataclass(frozen=True)
class DigitalLifeBirthResult:
    exit_code: int
    report: dict[str, Any]


def run_digital_life_birth(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> DigitalLifeBirthResult:
    run_id = run_id or _default_run_id("digital-life-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    blocked_reasons: list[str] = []

    direction_lock = _load_json(
        state_dir / "direction" / "direction_lock.json",
        blocked_reasons,
        "direction_restore_gate",
    )
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "life_state_restore_gate")
    report_bundle = _load_json(reports_dir / "report_bundle.json", blocked_reasons, "report_bundle_gate")
    return_packet = _load_json(
        reports_dir / "first_activation_return_packet.json",
        blocked_reasons,
        "return_packet_gate",
    )
    latest_stage_ref = _load_json(
        reports_dir / "latest_stage_explanation_ref.json",
        blocked_reasons,
        "stage_ref_gate",
    )
    stage_explanation = _load_json(
        reports_dir / "stage_explanation_report.json",
        blocked_reasons,
        "stage_explanation_gate",
    )

    blocked_reasons.extend(
        _birth_blockers(
            direction_lock=direction_lock,
            life_state=life_state,
            report_bundle=report_bundle,
            return_packet=return_packet,
            latest_stage_ref=latest_stage_ref,
            stage_explanation=stage_explanation,
        )
    )

    status = "closed" if not blocked_reasons else "blocked"
    birth_stage = "ready_for_first_terminal_turn" if status == "closed" else "birth_blocked"
    next_required_action = "enter_first_terminal_turn" if status == "closed" else "life-v0 explain-stage --strict"

    birth_packet = {
        "schema_version": "digital_life_birth_packet_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "birth_stage": birth_stage,
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "restore_refs": {
            "direction_restore_ref": "runtime/state/direction/direction_lock.json",
            "life_state_restore_ref": "runtime/state/life_state.json",
            "report_bundle_ref": "runtime/reports/latest/report_bundle.json",
            "return_packet_ref": "runtime/reports/latest/first_activation_return_packet.json",
            "stage_explanation_ref": "runtime/reports/latest/stage_explanation_report.json",
        },
        "terminal_birth_contract": {
            "direction_statement": direction_lock.get("direction_statement"),
            "activation_mode": return_packet.get("activation_mode"),
            "return_phase": return_packet.get("return_phase"),
            "stage_decision": stage_explanation.get("decision"),
        },
        "blocked_reasons": blocked_reasons,
        "next_required_action": next_required_action,
        "receipt_ref": f"runtime/receipts/digital_life_birth_{run_id}.json",
    }
    birth_digest = {
        "schema_version": "digital_life_birth_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "birth_stage": birth_stage,
        "next_required_action": next_required_action,
        "blocked_reasons": blocked_reasons,
    }
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
    )

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "digital_life_birth_packet.json", birth_packet)
        _write_json(reports_dir / "digital_life_birth_digest.json", birth_digest)
        _write_json(receipts_dir / f"digital_life_birth_{run_id}.json", receipt)
    except OSError as exc:
        birth_packet["status"] = "blocked"
        birth_packet["birth_stage"] = "birth_blocked"
        birth_packet["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return DigitalLifeBirthResult(exit_code=4, report=birth_packet)

    if status == "closed":
        return DigitalLifeBirthResult(exit_code=0, report=birth_packet)
    return DigitalLifeBirthResult(exit_code=1 if strict else 0, report=birth_packet)


def _birth_blockers(
    *,
    direction_lock: dict[str, Any],
    life_state: dict[str, Any],
    report_bundle: dict[str, Any],
    return_packet: dict[str, Any],
    latest_stage_ref: dict[str, Any],
    stage_explanation: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if direction_lock.get("direction_statement") != "build_real_digital_life":
        reasons.append("direction_restore_gate direction mismatch")
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("life_state_restore_gate schema mismatch")
    if report_bundle.get("schema_version") != "report_bundle_v0" or report_bundle.get("status") != "closed":
        reasons.append("report_bundle_gate bundle not closed")
    if return_packet.get("schema_version") != "first_activation_return_packet_v0" or return_packet.get("status") != "closed":
        reasons.append("return_packet_gate packet not closed")
    if latest_stage_ref.get("next_required_command") != "digital life":
        reasons.append("stage_ref_gate next command mismatch")
    if stage_explanation.get("decision") != "ready_for_terminal_birth_restore":
        reasons.append("stage_explanation_gate decision mismatch")
    return reasons


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        state_dir / "direction" / "direction_lock.json",
        state_dir / "life_state.json",
        reports_dir / "report_bundle.json",
        reports_dir / "first_activation_return_packet.json",
        reports_dir / "latest_stage_explanation_ref.json",
        reports_dir / "stage_explanation_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)

    output_paths = [
        reports_dir / "digital_life_birth_packet.json",
        reports_dir / "digital_life_birth_digest.json",
        receipts_dir / f"digital_life_birth_{run_id}.json",
    ]
    return {
        "schema_version": "digital_life_birth_receipt_v0",
        "receipt_id": f"digital_life_birth_{run_id}",
        "run_id": run_id,
        "command": "digital-life",
        "report_refs": [
            "runtime/reports/latest/digital_life_birth_packet.json",
            "runtime/reports/latest/digital_life_birth_digest.json",
        ],
        "stage_effect": "ready_for_terminal_birth_restore",
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
