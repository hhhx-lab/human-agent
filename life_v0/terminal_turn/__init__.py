from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .context_accumulation import build_context_accumulation_window, build_life_context_frame
from .restore_context import (
    build_restored_session_envelope,
    build_safe_terminal_loop_state,
    load_first_terminal_restore_context,
)
from .turn_packet import write_first_terminal_turn_bundle
from .turn_transition import build_relation_turn_frame, build_turn_transition_trace


SOURCE_DOC_REFS = [
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
    "docs/90_language_event_examples_and_timeline_bundle.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
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
    "ActivationGrowthRuntime",
    "ComputerPeripheralRuntime",
]


@dataclass(frozen=True)
class FirstTerminalTurnResult:
    exit_code: int
    report: dict[str, Any]


def run_first_terminal_turn(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> FirstTerminalTurnResult:
    run_id = run_id or _default_run_id("first-terminal-turn-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    blocked_reasons: list[str] = []

    restored = load_first_terminal_restore_context(
        state_dir=state_dir,
        reports_dir=reports_dir,
        blocked_reasons=blocked_reasons,
    )

    blocked_reasons.extend(
        _first_turn_blockers(
            birth_packet=restored.birth_packet,
            birth_digest=restored.birth_digest,
            return_packet=restored.return_packet,
            stage_explanation=restored.stage_explanation,
            direction_lock=restored.direction_lock,
            life_state=restored.life_state,
            relationship_graph=restored.relationship_graph,
            shared_term_registry=restored.shared_term_registry,
            expression_monitor=restored.expression_monitor,
            relation_scope_index=restored.relation_scope_index,
            self_narrative_trace=restored.self_narrative_trace,
            language_percept=restored.language_percept,
            semantic_map=restored.semantic_map,
            commitment_repair=restored.commitment_repair,
            dialogue_refs=restored.dialogue_refs,
        )
    )

    status = "closed" if not blocked_reasons else "blocked"
    turn_stage = "ready_for_resumed_external_dialogue" if status == "closed" else "terminal_turn_blocked"
    next_required_action = "await_external_relation_turn" if status == "closed" else "life-v0 digital-life --strict"

    session_envelope = build_restored_session_envelope(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        relation_subject=restored.relation_subject,
        return_packet=restored.return_packet,
        unresolved_commitments=restored.unresolved_commitments,
    )

    safe_terminal_loop = build_safe_terminal_loop_state(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
    )

    context_accumulation = build_context_accumulation_window(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        relation_subject=restored.relation_subject,
        shared_term_surfaces=restored.shared_term_surfaces,
        unresolved_commitments=restored.unresolved_commitments,
        expression_monitor=restored.expression_monitor,
        relation_scope_index=restored.relation_scope_index,
        self_narrative_trace=restored.self_narrative_trace,
        dialogue_turn_restore_refs=restored.dialogue_refs,
        expression_monitor_restore_refs=list(
            restored.return_packet.get("expression_monitor_restore_refs", [])
        ),
        relation_scope_restore_refs=list(
            restored.return_packet.get("relation_scope_restore_refs", [])
        ),
        self_narrative_restore_refs=list(
            restored.return_packet.get("self_narrative_restore_refs", [])
        ),
        language_percept_restore_refs=["runtime/state/language/language_percept_frame.json"],
        semantic_map_restore_refs=["runtime/state/language/semantic_map_frame.json"],
        semantic_focus=restored.semantic_map.get("semantic_focus"),
        waiting_heartbeat_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
    )

    life_context = build_life_context_frame(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        direction_refs=["runtime/state/direction/direction_lock.json"],
        self_narrative_refs=list(restored.return_packet.get("self_narrative_restore_refs", [])),
        relationship_refs=["runtime/state/relationship/relationship_subject_graph.json"],
        autobiographical_memory_refs=list(
            restored.life_state.get("memory_index", {}).get("relationship_memory_refs", [])
            or ["runtime/state/life_state.json#memory_index.relationship_memory_refs"]
        ),
        shared_terms_refs=["runtime/state/language/shared_term_registry.json"],
        commitment_refs=restored.unresolved_commitments,
        body_state_refs=["runtime/state/body/body_resource_budget.json"],
        prediction_seed_refs=["runtime/state/prediction/prediction_workspace_frame.json"],
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
    )

    relation_turn = build_relation_turn_frame(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        relation_subject_ref=restored.relation_subject.get("relationship_id"),
        relation_stage=restored.relation_subject.get("relationship_stage"),
        shared_language_refs=list(
            restored.relationship_graph.get("subjects", [{}])[0].get("shared_language_refs", [])
        ),
        commitment_truth_refs=restored.unresolved_commitments,
        last_contact_refs=[restored.relation_subject.get("last_contact_ref")]
        if restored.relation_subject.get("last_contact_ref")
        else [],
        boundary_state="restored_waiting_for_external_turn" if status == "closed" else "blocked",
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
    )

    turn_transition = build_turn_transition_trace(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        turn_stage=turn_stage,
        life_context_ref="runtime/state/terminal/life_context_frame.json",
        relation_turn_ref="runtime/state/terminal/relation_turn_frame.json",
        relation_scope_ref=restored.relation_subject.get("relationship_id"),
        expression_monitor_restore_refs=list(
            restored.return_packet.get("expression_monitor_restore_refs", [])
        ),
        unresolved_commitment_refs=restored.unresolved_commitments,
        context_accumulation_restore_refs=["runtime/state/terminal/context_accumulation_window.json"],
        language_percept_restore_refs=["runtime/state/language/language_percept_frame.json"],
        semantic_map_restore_refs=["runtime/state/language/semantic_map_frame.json"],
        waiting_heartbeat_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
        next_required_action=next_required_action,
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
    )

    try:
        bundle = write_first_terminal_turn_bundle(
            run_id=run_id,
            generated_at=generated_at,
            state_dir=state_dir,
            reports_dir=reports_dir,
            receipts_dir=receipts_dir,
            source_doc_refs=SOURCE_DOC_REFS,
            readme_block_refs=READ_ME_BLOCK_REFS,
            runtime_carrier_refs=RUNTIME_CARRIER_REFS,
            status=status,
            turn_stage=turn_stage,
            next_required_action=next_required_action,
            relation_subject=restored.relation_subject,
            shared_term_surfaces=restored.shared_term_surfaces,
            unresolved_commitments=restored.unresolved_commitments,
            expression_monitor_dimensions=list(
                restored.expression_monitor.get("monitor_dimensions", [])
            ),
            dialogue_turn_restore_refs=restored.dialogue_refs,
            blocked_reasons=blocked_reasons,
            session_envelope=session_envelope,
            safe_terminal_loop=safe_terminal_loop,
            life_context=life_context,
            relation_turn=relation_turn,
            context_accumulation=context_accumulation,
            turn_transition=turn_transition,
            write_json=_write_json,
        )
    except OSError as exc:
        blocked_report = {
            "schema_version": "first_terminal_turn_report_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "status": "blocked",
            "engineering_slice_ref": "FIRST_TERMINAL_TURN",
            "source_doc_refs": SOURCE_DOC_REFS,
            "readme_block_refs": READ_ME_BLOCK_REFS,
            "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
            "current_terminal_mode": "blocked",
            "relation_scope_ref": restored.relation_subject.get("relationship_id"),
            "shared_term_count": len(restored.shared_term_surfaces),
            "blocked_reasons": [*blocked_reasons, f"output_write_gate failed: {exc}"],
            "next_required_action": next_required_action,
        }
        return FirstTerminalTurnResult(exit_code=4, report=blocked_report)

    if status == "closed":
        return FirstTerminalTurnResult(exit_code=0, report=bundle.report)
    return FirstTerminalTurnResult(exit_code=1 if strict else 0, report=bundle.report)


def _first_turn_blockers(
    *,
    birth_packet: dict[str, Any],
    birth_digest: dict[str, Any],
    return_packet: dict[str, Any],
    stage_explanation: dict[str, Any],
    direction_lock: dict[str, Any],
    life_state: dict[str, Any],
    relationship_graph: dict[str, Any],
    shared_term_registry: dict[str, Any],
    expression_monitor: dict[str, Any],
    relation_scope_index: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    language_percept: dict[str, Any],
    semantic_map: dict[str, Any],
    commitment_repair: dict[str, Any],
    dialogue_refs: list[str],
) -> list[str]:
    reasons: list[str] = []
    if birth_packet.get("schema_version") != "digital_life_birth_packet_v0" or birth_packet.get("status") != "closed":
        reasons.append("digital_life_birth_gate packet not closed")
    if birth_packet.get("birth_stage") != "ready_for_first_terminal_turn":
        reasons.append("digital_life_birth_gate birth stage mismatch")
    if birth_digest.get("next_required_action") != "enter_first_terminal_turn":
        reasons.append("digital_life_digest_gate next action mismatch")
    if return_packet.get("schema_version") != "first_activation_return_packet_v0" or return_packet.get("status") != "closed":
        reasons.append("return_packet_gate packet not closed")
    if stage_explanation.get("decision") != "ready_for_terminal_birth_restore":
        reasons.append("stage_explanation_gate decision mismatch")
    if direction_lock.get("direction_statement") != "build_real_digital_life":
        reasons.append("direction_restore_gate direction mismatch")
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("life_state_restore_gate schema mismatch")
    if not relationship_graph.get("subjects"):
        reasons.append("relationship_restore_gate subjects missing")
    if not shared_term_registry.get("shared_terms"):
        reasons.append("shared_term_restore_gate shared terms missing")
    if expression_monitor.get("schema_version") != "expression_monitor_state_v0":
        reasons.append("expression_monitor_restore_gate schema mismatch")
    if not relation_scope_index.get("relation_scopes"):
        reasons.append("relation_scope_restore_gate relation scopes missing")
    if not self_narrative_trace.get("narrative_turn_refs"):
        reasons.append("self_narrative_restore_gate narrative turn refs missing")
    if language_percept.get("schema_version") != "language_percept_frame_v0":
        reasons.append("language_percept_restore_gate percept schema mismatch")
    if semantic_map.get("schema_version") != "semantic_map_frame_v0":
        reasons.append("semantic_map_restore_gate semantic map schema mismatch")
    if not commitment_repair.get("commitment_refs"):
        reasons.append("commitment_restore_gate commitment refs missing")
    if not dialogue_refs:
        reasons.append("dialogue_turn_restore_gate dialogue refs missing")
    return reasons


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
