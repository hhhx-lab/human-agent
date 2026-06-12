from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..digital_life import run_digital_life_birth
from ..terminal_loop import run_terminal_life_loop
from ..terminal_turn import run_first_terminal_turn


SOURCE_DOC_REFS = [
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
    "docs/90_language_event_examples_and_timeline_bundle.md",
    "docs/v0/references/current_agent_shell_reference_2026.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/process_contracts/first_terminal_turn_engineering_contract.md",
    "docs/v0/process_contracts/terminal_life_loop_engineering_contract.md",
    "docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md",
]

READ_ME_BLOCK_REFS = [
    "B21_LANGUAGE_RELATIONSHIP_CORE",
    "B29_RUNTIME_MOUNT_GROWTH",
    "B30_RECONSOLIDATION_REPLAY_GROWTH",
    "B99_V0_ENGINEERING_CONTRACTS",
]

RUNTIME_CARRIER_REFS = [
    "RunnerCliRuntime",
    "ComputerPeripheralRuntime",
    "LanguageRelationshipRuntime",
    "ActivationGrowthRuntime",
]


@dataclass(frozen=True)
class DigitalLifeShellResult:
    exit_code: int
    report: dict[str, Any]


def run_digital_life_shell_command(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> DigitalLifeShellResult:
    run_id = run_id or _default_run_id("digital-life-shell-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    blocked_reasons: list[str] = []
    stage_explanation = _load_json(
        reports_dir / "stage_explanation_report.json",
        blocked_reasons,
        "stage_explanation_gate",
    )

    if stage_explanation.get("next_required_command") not in {
        "my digital life",
        "digital life",
    }:
        blocked_reasons.append("stage_explanation_gate next command mismatch")

    if stage_explanation.get("decision") != "ready_for_terminal_birth_restore":
        blocked_reasons.append("stage_explanation_gate decision mismatch")

    if blocked_reasons:
        report = _build_blocked_report(
            run_id=run_id,
            generated_at=generated_at,
            blocked_reasons=blocked_reasons,
        )
        return DigitalLifeShellResult(exit_code=1 if strict else 0, report=report)

    birth_result = run_digital_life_birth(
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        run_id=f"{run_id}-birth",
        strict=strict,
    )
    if birth_result.exit_code != 0:
        report = _build_blocked_report(
            run_id=run_id,
            generated_at=generated_at,
            blocked_reasons=["digital_birth_gate internal closure failed"],
            nested_refs={"digital_life_birth_report": "runtime/reports/latest/digital_life_birth_packet.json"},
        )
        return DigitalLifeShellResult(exit_code=birth_result.exit_code, report=report)

    first_turn_result = run_first_terminal_turn(
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        run_id=f"{run_id}-turn",
        strict=strict,
    )
    if first_turn_result.exit_code != 0:
        report = _build_blocked_report(
            run_id=run_id,
            generated_at=generated_at,
            blocked_reasons=["first_terminal_turn_gate internal closure failed"],
            nested_refs={"first_terminal_turn_report": "runtime/reports/latest/first_terminal_turn_report.json"},
        )
        return DigitalLifeShellResult(exit_code=first_turn_result.exit_code, report=report)

    loop_result = run_terminal_life_loop(
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        run_id=f"{run_id}-loop",
        strict=strict,
    )
    if loop_result.exit_code != 0:
        report = _build_blocked_report(
            run_id=run_id,
            generated_at=generated_at,
            blocked_reasons=["terminal_life_loop_gate internal closure failed"],
            nested_refs={"terminal_life_loop_report": "runtime/reports/latest/terminal_life_loop_report.json"},
        )
        return DigitalLifeShellResult(exit_code=loop_result.exit_code, report=report)

    packet = {
        "schema_version": "digital_life_shell_packet_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "engineering_slice_ref": "DIGITAL_LIFE_SHELL_COMMAND",
        "shell_mode": "terminal_life_loop_restored",
        "birth_packet_ref": "runtime/reports/latest/digital_life_birth_packet.json",
        "first_terminal_turn_ref": "runtime/reports/latest/first_terminal_turn_packet.json",
        "terminal_life_loop_ref": "runtime/reports/latest/terminal_life_loop_packet.json",
        "session_envelope_ref": "runtime/state/terminal/session_envelope.json",
        "safe_terminal_loop_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "next_required_action": "await_next_external_relation_turn",
        "receipt_ref": f"runtime/receipts/digital_life_shell_{run_id}.json",
    }

    report = {
        "schema_version": "digital_life_shell_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "engineering_slice_ref": "DIGITAL_LIFE_SHELL_COMMAND",
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "current_shell_mode": "terminal_life_loop_restored",
        "birth_packet_ref": "runtime/reports/latest/digital_life_birth_packet.json",
        "first_terminal_turn_ref": "runtime/reports/latest/first_terminal_turn_packet.json",
        "terminal_life_loop_ref": "runtime/reports/latest/terminal_life_loop_packet.json",
        "next_required_action": "await_next_external_relation_turn",
        "blocked_reasons": [],
    }

    digest = {
        "schema_version": "digital_life_shell_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "shell_mode": "terminal_life_loop_restored",
        "next_required_action": "await_next_external_relation_turn",
        "terminal_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
    }

    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        state_dir=state_dir,
    )

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "digital_life_shell_packet.json", packet)
        _write_json(reports_dir / "digital_life_shell_report.json", report)
        _write_json(reports_dir / "digital_life_shell_digest.json", digest)
        _write_json(receipts_dir / f"digital_life_shell_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["blocked_reasons"] = [f"shell_writeback_gate failed: {exc}"]
        return DigitalLifeShellResult(exit_code=4, report=report)

    return DigitalLifeShellResult(exit_code=0, report=report)


def _build_blocked_report(
    *,
    run_id: str,
    generated_at: str,
    blocked_reasons: list[str],
    nested_refs: dict[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "digital_life_shell_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "blocked",
        "engineering_slice_ref": "DIGITAL_LIFE_SHELL_COMMAND",
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "current_shell_mode": "blocked",
        "blocked_reasons": blocked_reasons,
        "nested_refs": nested_refs or {},
        "next_required_action": "digital life",
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    reports_dir: Path,
    receipts_dir: Path,
    state_dir: Path,
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        reports_dir / "stage_explanation_report.json",
        reports_dir / "digital_life_birth_packet.json",
        reports_dir / "first_terminal_turn_packet.json",
        reports_dir / "terminal_life_loop_packet.json",
        state_dir / "terminal" / "session_envelope.json",
        state_dir / "terminal" / "safe_terminal_loop_state.json",
        state_dir / "terminal" / "terminal_life_loop_state.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)

    output_paths = [
        reports_dir / "digital_life_shell_packet.json",
        reports_dir / "digital_life_shell_report.json",
        reports_dir / "digital_life_shell_digest.json",
        receipts_dir / f"digital_life_shell_{run_id}.json",
    ]
    return {
        "schema_version": "digital_life_shell_receipt_v0",
        "receipt_id": f"digital_life_shell_{run_id}",
        "run_id": run_id,
        "command": "digital life",
        "report_refs": [
            "runtime/reports/latest/digital_life_shell_packet.json",
            "runtime/reports/latest/digital_life_shell_report.json",
            "runtime/reports/latest/digital_life_shell_digest.json",
        ],
        "stage_effect": "allow_external_relation_turn_wait",
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
