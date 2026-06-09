from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class TerminalLifeLoopBundleResult:
    report: dict[str, Any]
    digest: dict[str, Any]
    receipt: dict[str, Any]


def write_terminal_life_loop_bundle(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    status: str,
    loop_stage: str,
    next_required_action: str,
    relation_subject: dict[str, Any],
    shared_term_surfaces: list[str],
    long_horizon_writeback_targets: list[str],
    blocked_reasons: list[str],
    updated_safe_terminal_loop: dict[str, Any],
    loop_state: dict[str, Any],
    dialogue_writeback_bundle: dict[str, Any],
    resumed_dialogue_packet: dict[str, Any],
    dialogue_writeback_bundle_ref: str,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> TerminalLifeLoopBundleResult:
    loop_packet = {
        "schema_version": "terminal_life_loop_packet_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "loop_stage": loop_stage,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
        "loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "session_envelope_ref": "runtime/state/terminal/session_envelope.json",
        "safe_terminal_loop_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "last_dialogue_packet_ref": "runtime/reports/latest/resumed_external_dialogue_packet.json",
        "dialogue_writeback_bundle_ref": dialogue_writeback_bundle_ref,
        "writeback_targets": [
            "runtime/state/language/dialogue_turn_log.jsonl",
            "runtime/state/language/self_narrative_language_trace.json",
            "runtime/state/language/commitment_repair_language_index.json",
            "runtime/state/relationship/relationship_subject_graph.json",
        ]
        + long_horizon_writeback_targets,
        "next_required_action": next_required_action,
        "receipt_ref": f"runtime/receipts/terminal_life_loop_{run_id}.json",
    }

    report = {
        "schema_version": "terminal_life_loop_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "engineering_slice_ref": "FIRST_TERMINAL_LIFE_LOOP",
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
        "current_terminal_mode": "resumed_external_dialogue_loop" if status == "closed" else "blocked",
        "loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
        "last_dialogue_packet_ref": "runtime/reports/latest/resumed_external_dialogue_packet.json",
        "blocked_reasons": blocked_reasons,
        "next_required_action": next_required_action,
    }

    digest = {
        "schema_version": "terminal_life_loop_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "loop_stage": loop_stage,
        "next_required_action": next_required_action,
        "relation_role": relation_subject.get("relation_role"),
        "shared_term_count": len(shared_term_surfaces),
        "blocked_reasons": blocked_reasons,
    }

    receipt = build_terminal_life_loop_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
    )

    receipts_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "terminal").mkdir(parents=True, exist_ok=True)
    write_json(state_dir / "terminal" / "safe_terminal_loop_state.json", updated_safe_terminal_loop)
    write_json(state_dir / "terminal" / "terminal_life_loop_state.json", loop_state)
    write_json(reports_dir / "dialogue_writeback_bundle.json", dialogue_writeback_bundle)
    write_json(reports_dir / "resumed_external_dialogue_packet.json", resumed_dialogue_packet)
    write_json(reports_dir / "terminal_life_loop_packet.json", loop_packet)
    write_json(reports_dir / "terminal_life_loop_report.json", report)
    write_json(reports_dir / "terminal_life_loop_digest.json", digest)
    write_json(receipts_dir / f"terminal_life_loop_{run_id}.json", receipt)

    return TerminalLifeLoopBundleResult(report=report, digest=digest, receipt=receipt)


def build_terminal_life_loop_receipt(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        reports_dir / "first_terminal_turn_packet.json",
        reports_dir / "first_terminal_turn_report.json",
        state_dir / "terminal" / "session_envelope.json",
        state_dir / "terminal" / "safe_terminal_loop_state.json",
        state_dir / "relationship" / "relationship_subject_graph.json",
        state_dir / "language" / "shared_term_registry.json",
        state_dir / "language" / "expression_monitor_state.json",
        state_dir / "language" / "commitment_repair_language_index.json",
        state_dir / "language" / "self_narrative_language_trace.json",
        state_dir / "language" / "dialogue_turn_log.jsonl",
    ]:
        if path.exists():
            input_hashes[str(path)] = sha256(path)

    output_paths = [
        state_dir / "terminal" / "safe_terminal_loop_state.json",
        state_dir / "terminal" / "terminal_life_loop_state.json",
        reports_dir / "dialogue_writeback_bundle.json",
        reports_dir / "resumed_external_dialogue_packet.json",
        reports_dir / "terminal_life_loop_packet.json",
        reports_dir / "terminal_life_loop_report.json",
        reports_dir / "terminal_life_loop_digest.json",
        receipts_dir / f"terminal_life_loop_{run_id}.json",
    ]
    return {
        "schema_version": "terminal_life_loop_receipt_v0",
        "receipt_id": f"terminal_life_loop_{run_id}",
        "run_id": run_id,
        "command": "terminal-life-loop",
        "report_refs": [
            "runtime/reports/latest/dialogue_writeback_bundle.json",
            "runtime/reports/latest/resumed_external_dialogue_packet.json",
            "runtime/reports/latest/terminal_life_loop_packet.json",
            "runtime/reports/latest/terminal_life_loop_report.json",
            "runtime/reports/latest/terminal_life_loop_digest.json",
        ],
        "stage_effect": "ready_for_next_external_relation_turn",
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_hashes": {str(path): sha256_if_exists(path) for path in output_paths},
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return sha256(path)
