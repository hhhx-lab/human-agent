from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .loop_state import build_terminal_life_loop_state
from .dialogue_writeback import build_dialogue_writeback_bundle
from .loop_report import write_terminal_life_loop_bundle
from .resume_packet import build_resumed_external_dialogue_packet


SOURCE_DOC_REFS = [
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
    "docs/90_language_event_examples_and_timeline_bundle.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/process_contracts/first_terminal_turn_engineering_contract.md",
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
    "docs/v0/process_contracts/terminal_life_loop_engineering_contract.md",
]

READ_ME_BLOCK_REFS = [
    "B21_LANGUAGE_RELATIONSHIP_CORE",
    "B29_RUNTIME_MOUNT_GROWTH",
    "B30_RECONSOLIDATION_REPLAY_GROWTH",
    "B99_V0_ENGINEERING_CONTRACTS",
]

RUNTIME_CARRIER_REFS = [
    "LanguageRelationshipRuntime",
    "RunnerCliRuntime",
    "ComputerPeripheralRuntime",
    "ActivationGrowthRuntime",
]


@dataclass(frozen=True)
class TerminalLifeLoopResult:
    exit_code: int
    report: dict[str, Any]


def run_terminal_life_loop(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> TerminalLifeLoopResult:
    run_id = run_id or _default_run_id("terminal-life-loop-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    terminal_dir = state_dir / "terminal"

    blocked_reasons: list[str] = []

    first_turn_packet = _load_json(
        reports_dir / "first_terminal_turn_packet.json",
        blocked_reasons,
        "first_terminal_turn_gate",
    )
    first_turn_report = _load_json(
        reports_dir / "first_terminal_turn_report.json",
        blocked_reasons,
        "first_terminal_report_gate",
    )
    session_envelope = _load_json(
        terminal_dir / "session_envelope.json",
        blocked_reasons,
        "session_envelope_gate",
    )
    safe_terminal_loop = _load_json(
        terminal_dir / "safe_terminal_loop_state.json",
        blocked_reasons,
        "safe_terminal_loop_gate",
    )
    relationship_graph = _load_json(
        state_dir / "relationship" / "relationship_subject_graph.json",
        blocked_reasons,
        "relation_identity_gate",
    )
    shared_term_registry = _load_json(
        state_dir / "language" / "shared_term_registry.json",
        blocked_reasons,
        "shared_term_continuity_gate",
    )
    expression_monitor = _load_json(
        state_dir / "language" / "expression_monitor_state.json",
        blocked_reasons,
        "expression_monitor_gate",
    )
    commitment_repair = _load_json(
        state_dir / "language" / "commitment_repair_language_index.json",
        blocked_reasons,
        "commitment_continuity_gate",
    )
    self_narrative_trace = _load_json(
        state_dir / "language" / "self_narrative_language_trace.json",
        blocked_reasons,
        "turn_writeback_gate",
    )
    dialogue_turn_refs = _collect_dialogue_turn_refs(
        state_dir / "language" / "dialogue_turn_log.jsonl",
        blocked_reasons,
    )

    blocked_reasons.extend(
        _loop_blockers(
            first_turn_packet=first_turn_packet,
            first_turn_report=first_turn_report,
            session_envelope=session_envelope,
            safe_terminal_loop=safe_terminal_loop,
            relationship_graph=relationship_graph,
            shared_term_registry=shared_term_registry,
            expression_monitor=expression_monitor,
            commitment_repair=commitment_repair,
            self_narrative_trace=self_narrative_trace,
            dialogue_turn_refs=dialogue_turn_refs,
        )
    )

    status = "closed" if not blocked_reasons else "blocked"
    loop_stage = (
        "restored_loop_waiting_next_external_turn"
        if status == "closed"
        else "terminal_life_loop_blocked"
    )
    next_required_action = (
        "await_next_external_relation_turn"
        if status == "closed"
        else "life-v0 first-terminal-turn --strict"
    )

    relation_subject = _first_relation_subject(relationship_graph)
    shared_term_surfaces = [
        term.get("surface")
        for term in shared_term_registry.get("shared_terms", [])
        if term.get("surface")
    ]
    commitment_refs = list(commitment_repair.get("commitment_refs", []))
    dialogue_writeback_bundle_ref = "runtime/reports/latest/dialogue_writeback_bundle.json"

    dialogue_writeback_bundle = build_dialogue_writeback_bundle(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        dialogue_event_refs=dialogue_turn_refs,
        self_narrative_writeback_refs=list(self_narrative_trace.get("narrative_turn_refs", [])),
        relationship_writeback_refs=[
            "runtime/state/relationship/relationship_subject_graph.json"
        ],
        commitment_writeback_refs=commitment_refs,
        replay_cue_refs=[
            "runtime/state/life_state.json#memory_index.replay_cues"
        ],
        terminal_state_refs=[
            "runtime/state/terminal/safe_terminal_loop_state.json",
            "runtime/state/terminal/terminal_life_loop_state.json",
        ],
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
    )

    resumed_dialogue_packet = build_resumed_external_dialogue_packet(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        relation_subject=relation_subject,
        shared_term_surfaces=shared_term_surfaces,
        commitment_refs=commitment_refs,
        session_envelope=session_envelope,
        dialogue_turn_restore_refs=dialogue_turn_refs,
        dialogue_writeback_bundle_ref=dialogue_writeback_bundle_ref,
        next_required_action=next_required_action,
    )

    loop_state = build_terminal_life_loop_state(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        next_required_action=next_required_action,
    )

    updated_safe_terminal_loop = {
        **safe_terminal_loop,
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_mode": "restored_waiting_for_external_turn" if status == "closed" else "blocked",
        "last_completed_turn_mode": "resumed_external_dialogue_loop" if status == "closed" else "blocked",
        "last_dialogue_packet_ref": "runtime/reports/latest/resumed_external_dialogue_packet.json",
    }

    try:
        report_bundle = write_terminal_life_loop_bundle(
            run_id=run_id,
            generated_at=generated_at,
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            source_doc_refs=SOURCE_DOC_REFS,
            readme_block_refs=READ_ME_BLOCK_REFS,
            runtime_carrier_refs=RUNTIME_CARRIER_REFS,
            status=status,
            loop_stage=loop_stage,
            next_required_action=next_required_action,
            relation_subject=relation_subject,
            shared_term_surfaces=shared_term_surfaces,
            blocked_reasons=blocked_reasons,
            updated_safe_terminal_loop=updated_safe_terminal_loop,
            loop_state=loop_state,
            dialogue_writeback_bundle=dialogue_writeback_bundle,
            resumed_dialogue_packet=resumed_dialogue_packet,
            dialogue_writeback_bundle_ref=dialogue_writeback_bundle_ref,
            write_json=_write_json,
        )
    except OSError as exc:
        blocked_report = {
            "schema_version": "terminal_life_loop_report_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "status": "blocked",
            "engineering_slice_ref": "FIRST_TERMINAL_LIFE_LOOP",
            "source_doc_refs": SOURCE_DOC_REFS,
            "readme_block_refs": READ_ME_BLOCK_REFS,
            "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
            "current_terminal_mode": "blocked",
            "loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
            "last_dialogue_packet_ref": "runtime/reports/latest/resumed_external_dialogue_packet.json",
            "blocked_reasons": [*blocked_reasons, f"output_write_gate failed: {exc}"],
            "next_required_action": next_required_action,
        }
        return TerminalLifeLoopResult(exit_code=4, report=blocked_report)

    if status == "closed":
        return TerminalLifeLoopResult(exit_code=0, report=report_bundle.report)
    return TerminalLifeLoopResult(exit_code=1 if strict else 0, report=report_bundle.report)


def _loop_blockers(
    *,
    first_turn_packet: dict[str, Any],
    first_turn_report: dict[str, Any],
    session_envelope: dict[str, Any],
    safe_terminal_loop: dict[str, Any],
    relationship_graph: dict[str, Any],
    shared_term_registry: dict[str, Any],
    expression_monitor: dict[str, Any],
    commitment_repair: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    dialogue_turn_refs: list[str],
) -> list[str]:
    reasons: list[str] = []
    if first_turn_packet.get("schema_version") != "first_terminal_turn_packet_v0" or first_turn_packet.get("status") != "closed":
        reasons.append("first_terminal_turn_gate packet not closed")
    if first_turn_packet.get("turn_stage") != "ready_for_resumed_external_dialogue":
        reasons.append("first_terminal_turn_gate turn stage mismatch")
    if first_turn_report.get("current_terminal_mode") != "restored_life_turn":
        reasons.append("first_terminal_report_gate current mode mismatch")
    if session_envelope.get("schema_version") != "session_envelope_v0":
        reasons.append("session_envelope_gate schema mismatch")
    if session_envelope.get("current_turn_mode") != "restored_life_turn":
        reasons.append("session_envelope_gate current turn mode mismatch")
    if safe_terminal_loop.get("schema_version") != "safe_terminal_loop_state_v0":
        reasons.append("safe_terminal_loop_gate schema mismatch")
    if safe_terminal_loop.get("current_mode") != "restored_waiting_for_external_turn":
        reasons.append("safe_terminal_loop_gate current mode mismatch")
    if "external_irreversible_action" not in safe_terminal_loop.get("blocked_actions", []):
        reasons.append("safe_terminal_loop_gate irreversible action block missing")
    if not relationship_graph.get("subjects"):
        reasons.append("relation_identity_gate subjects missing")
    if not shared_term_registry.get("shared_terms"):
        reasons.append("shared_term_continuity_gate shared terms missing")
    if expression_monitor.get("schema_version") != "expression_monitor_state_v0":
        reasons.append("expression_monitor_gate schema mismatch")
    if not commitment_repair.get("commitment_refs"):
        reasons.append("commitment_continuity_gate commitment refs missing")
    if not self_narrative_trace.get("narrative_turn_refs"):
        reasons.append("turn_writeback_gate narrative refs missing")
    if not dialogue_turn_refs:
        reasons.append("turn_writeback_gate dialogue refs missing")
    return reasons


def _first_relation_subject(relationship_graph: dict[str, Any]) -> dict[str, Any]:
    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        return subjects[0]
    return {}


def _collect_dialogue_turn_refs(path: Path, blocked_reasons: list[str]) -> list[str]:
    try:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError as exc:
        blocked_reasons.append(f"turn_writeback_gate failed: {exc}")
        return []
    return [f"runtime/state/language/dialogue_turn_log.jsonl#line-{idx}" for idx, _ in enumerate(lines, start=1)]


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


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
