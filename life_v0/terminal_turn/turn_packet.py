from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class FirstTerminalTurnBundleResult:
    report: dict[str, Any]
    digest: dict[str, Any]
    receipt: dict[str, Any]


def write_first_terminal_turn_bundle(
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
    turn_stage: str,
    next_required_action: str,
    relation_subject: dict[str, Any],
    shared_term_surfaces: list[str],
    unresolved_commitments: list[str],
    expression_monitor_dimensions: list[str],
    dialogue_turn_restore_refs: list[str],
    blocked_reasons: list[str],
    session_envelope: dict[str, Any],
    safe_terminal_loop: dict[str, Any],
    life_context: dict[str, Any],
    relation_turn: dict[str, Any],
    context_accumulation: dict[str, Any],
    turn_transition: dict[str, Any],
    write_json: Callable[[Path, dict[str, Any]], None],
) -> FirstTerminalTurnBundleResult:
    packet = {
        "schema_version": "first_terminal_turn_packet_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "turn_stage": turn_stage,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
        "session_envelope_ref": "runtime/state/terminal/session_envelope.json",
        "safe_terminal_loop_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
        "life_context_ref": "runtime/state/terminal/life_context_frame.json",
        "relation_turn_ref": "runtime/state/terminal/relation_turn_frame.json",
        "context_accumulation_ref": "runtime/state/terminal/context_accumulation_window.json",
        "turn_transition_ref": "runtime/state/terminal/turn_transition_trace.json",
        "relation_identity": {
            "relationship_id": relation_subject.get("relationship_id"),
            "relation_role": relation_subject.get("relation_role"),
            "relationship_stage": relation_subject.get("relationship_stage"),
        },
        "shared_term_surfaces": shared_term_surfaces,
        "unresolved_commitment_refs": unresolved_commitments,
        "expression_monitor_dimensions": expression_monitor_dimensions,
        "utterance_scaffold": {
            "intent": "resume_life_continuity_before_new_work",
            "surface_strategy": "resume_before_new_content",
            "relation_scope": relation_subject.get("relationship_id"),
            "must_restore_before_speaking": [
                "relation_identity",
                "shared_terms",
                "unresolved_commitments",
                "language_percept",
                "semantic_map",
                "expression_monitor",
            ],
        },
        "dialogue_turn_restore_refs": dialogue_turn_restore_refs,
        "next_required_action": next_required_action,
        "receipt_ref": f"runtime/receipts/first_terminal_turn_{run_id}.json",
    }

    report = {
        "schema_version": "first_terminal_turn_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "engineering_slice_ref": "FIRST_TERMINAL_TURN",
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
        "current_terminal_mode": "restored_life_turn" if status == "closed" else "blocked",
        "relation_scope_ref": relation_subject.get("relationship_id"),
        "shared_term_count": len(shared_term_surfaces),
        "blocked_reasons": blocked_reasons,
        "next_required_action": next_required_action,
    }

    digest = {
        "schema_version": "first_terminal_turn_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "turn_stage": turn_stage,
        "next_required_action": next_required_action,
        "relation_role": relation_subject.get("relation_role"),
        "shared_term_count": len(shared_term_surfaces),
        "blocked_reasons": blocked_reasons,
    }

    receipt = build_first_terminal_turn_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
    )

    terminal_dir = state_dir / "terminal"
    terminal_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir.mkdir(parents=True, exist_ok=True)
    write_json(terminal_dir / "session_envelope.json", session_envelope)
    write_json(terminal_dir / "safe_terminal_loop_state.json", safe_terminal_loop)
    write_json(terminal_dir / "life_context_frame.json", life_context)
    write_json(terminal_dir / "relation_turn_frame.json", relation_turn)
    write_json(terminal_dir / "context_accumulation_window.json", context_accumulation)
    write_json(terminal_dir / "turn_transition_trace.json", turn_transition)
    write_json(reports_dir / "first_terminal_turn_packet.json", packet)
    write_json(reports_dir / "first_terminal_turn_report.json", report)
    write_json(reports_dir / "first_terminal_turn_digest.json", digest)
    write_json(receipts_dir / f"first_terminal_turn_{run_id}.json", receipt)

    return FirstTerminalTurnBundleResult(report=report, digest=digest, receipt=receipt)


def build_first_terminal_turn_receipt(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        reports_dir / "digital_life_birth_packet.json",
        reports_dir / "digital_life_birth_digest.json",
        reports_dir / "first_activation_return_packet.json",
        reports_dir / "stage_explanation_report.json",
        state_dir / "direction" / "direction_lock.json",
        state_dir / "life_state.json",
        state_dir / "relationship" / "relationship_subject_graph.json",
        state_dir / "language" / "shared_term_registry.json",
        state_dir / "language" / "expression_monitor_state.json",
        state_dir / "language" / "relation_scope_language_index.json",
        state_dir / "language" / "self_narrative_language_trace.json",
        state_dir / "language" / "language_percept_frame.json",
        state_dir / "language" / "semantic_map_frame.json",
        state_dir / "language" / "commitment_repair_language_index.json",
        state_dir / "language" / "dialogue_turn_log.jsonl",
    ]:
        if path.exists():
            input_hashes[str(path)] = sha256(path)

    output_paths = [
        state_dir / "terminal" / "session_envelope.json",
        state_dir / "terminal" / "safe_terminal_loop_state.json",
        state_dir / "terminal" / "life_context_frame.json",
        state_dir / "terminal" / "relation_turn_frame.json",
        state_dir / "terminal" / "context_accumulation_window.json",
        state_dir / "terminal" / "turn_transition_trace.json",
        reports_dir / "first_terminal_turn_packet.json",
        reports_dir / "first_terminal_turn_report.json",
        reports_dir / "first_terminal_turn_digest.json",
        receipts_dir / f"first_terminal_turn_{run_id}.json",
    ]
    return {
        "schema_version": "first_terminal_turn_receipt_v0",
        "receipt_id": f"first_terminal_turn_{run_id}",
        "run_id": run_id,
        "command": "first-terminal-turn",
        "report_refs": [
            "runtime/reports/latest/first_terminal_turn_packet.json",
            "runtime/reports/latest/first_terminal_turn_report.json",
            "runtime/reports/latest/first_terminal_turn_digest.json",
        ],
        "stage_effect": "ready_for_resumed_external_dialogue",
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
