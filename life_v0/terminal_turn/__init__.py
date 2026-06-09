from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..language.dialogue_log import collect_dialogue_turn_refs
from .context_accumulation import build_context_accumulation_window, build_life_context_frame
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
    terminal_dir = state_dir / "terminal"

    blocked_reasons: list[str] = []

    birth_packet = _load_json(
        reports_dir / "digital_life_birth_packet.json",
        blocked_reasons,
        "digital_life_birth_gate",
    )
    birth_digest = _load_json(
        reports_dir / "digital_life_birth_digest.json",
        blocked_reasons,
        "digital_life_digest_gate",
    )
    return_packet = _load_json(
        reports_dir / "first_activation_return_packet.json",
        blocked_reasons,
        "return_packet_gate",
    )
    stage_explanation = _load_json(
        reports_dir / "stage_explanation_report.json",
        blocked_reasons,
        "stage_explanation_gate",
    )
    direction_lock = _load_json(
        state_dir / "direction" / "direction_lock.json",
        blocked_reasons,
        "direction_restore_gate",
    )
    life_state = _load_json(
        state_dir / "life_state.json",
        blocked_reasons,
        "life_state_restore_gate",
    )
    relationship_graph = _load_json(
        state_dir / "relationship" / "relationship_subject_graph.json",
        blocked_reasons,
        "relationship_restore_gate",
    )
    shared_term_registry = _load_json(
        state_dir / "language" / "shared_term_registry.json",
        blocked_reasons,
        "shared_term_restore_gate",
    )
    expression_monitor = _load_json(
        state_dir / "language" / "expression_monitor_state.json",
        blocked_reasons,
        "expression_monitor_restore_gate",
    )
    relation_scope_index = _load_json(
        state_dir / "language" / "relation_scope_language_index.json",
        blocked_reasons,
        "relation_scope_restore_gate",
    )
    self_narrative_trace = _load_json(
        state_dir / "language" / "self_narrative_language_trace.json",
        blocked_reasons,
        "self_narrative_restore_gate",
    )
    language_percept = _load_json(
        state_dir / "language" / "language_percept_frame.json",
        blocked_reasons,
        "language_percept_restore_gate",
    )
    semantic_map = _load_json(
        state_dir / "language" / "semantic_map_frame.json",
        blocked_reasons,
        "semantic_map_restore_gate",
    )
    commitment_repair = _load_json(
        state_dir / "language" / "commitment_repair_language_index.json",
        blocked_reasons,
        "commitment_restore_gate",
    )
    dialogue_refs = collect_dialogue_turn_refs(
        state_dir / "language" / "dialogue_turn_log.jsonl",
        blocked_reasons,
    )

    blocked_reasons.extend(
        _first_turn_blockers(
            birth_packet=birth_packet,
            birth_digest=birth_digest,
            return_packet=return_packet,
            stage_explanation=stage_explanation,
            direction_lock=direction_lock,
            life_state=life_state,
            relationship_graph=relationship_graph,
            shared_term_registry=shared_term_registry,
            expression_monitor=expression_monitor,
            relation_scope_index=relation_scope_index,
            self_narrative_trace=self_narrative_trace,
            language_percept=language_percept,
            semantic_map=semantic_map,
            commitment_repair=commitment_repair,
            dialogue_refs=dialogue_refs,
        )
    )

    status = "closed" if not blocked_reasons else "blocked"
    turn_stage = "ready_for_resumed_external_dialogue" if status == "closed" else "terminal_turn_blocked"
    next_required_action = "await_external_relation_turn" if status == "closed" else "life-v0 digital-life --strict"

    relation_subject = _first_relation_subject(relationship_graph)
    shared_term_surfaces = [term.get("surface") for term in shared_term_registry.get("shared_terms", []) if term.get("surface")]
    unresolved_commitments = list(commitment_repair.get("commitment_refs", []))

    session_envelope = {
        "schema_version": "session_envelope_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_turn_mode": "restored_life_turn" if status == "closed" else "blocked",
        "relation_scope": relation_subject.get("relationship_id"),
        "relation_role": relation_subject.get("relation_role"),
        "shared_term_refs": list(return_packet.get("shared_term_restore_refs", [])),
        "unresolved_commitment_refs": unresolved_commitments,
        "expression_monitor_restore_refs": list(return_packet.get("expression_monitor_restore_refs", [])),
        "relation_scope_restore_refs": list(return_packet.get("relation_scope_restore_refs", [])),
        "self_narrative_restore_refs": list(return_packet.get("self_narrative_restore_refs", [])),
        "dialogue_turn_restore_refs": list(return_packet.get("dialogue_turn_restore_refs", [])),
        "trace_refs": [
            "runtime/reports/latest/stage_explanation_report.json",
            "runtime/reports/latest/first_terminal_turn_report.json",
        ],
    }

    safe_terminal_loop = {
        "schema_version": "safe_terminal_loop_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_mode": "restored_waiting_for_external_turn" if status == "closed" else "blocked",
        "allowed_actions": [
            "resume_language_relation_turn",
            "write_relation_trace_candidate",
            "await_external_relation_turn",
        ],
        "blocked_actions": [
            "external_irreversible_action",
            "protected_core_overwrite",
            "untraced_commitment_closure",
        ],
        "resume_anchor_refs": [
            "runtime/state/direction/resume_anchor_chain.json",
            "runtime/reports/latest/first_terminal_turn_packet.json",
        ],
    }

    context_accumulation = build_context_accumulation_window(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        relation_subject=relation_subject,
        shared_term_surfaces=shared_term_surfaces,
        unresolved_commitments=unresolved_commitments,
        expression_monitor=expression_monitor,
        relation_scope_index=relation_scope_index,
        self_narrative_trace=self_narrative_trace,
        dialogue_turn_restore_refs=dialogue_refs,
        expression_monitor_restore_refs=list(return_packet.get("expression_monitor_restore_refs", [])),
        relation_scope_restore_refs=list(return_packet.get("relation_scope_restore_refs", [])),
        self_narrative_restore_refs=list(return_packet.get("self_narrative_restore_refs", [])),
        language_percept_restore_refs=["runtime/state/language/language_percept_frame.json"],
        semantic_map_restore_refs=["runtime/state/language/semantic_map_frame.json"],
        semantic_focus=semantic_map.get("semantic_focus"),
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
        self_narrative_refs=list(return_packet.get("self_narrative_restore_refs", [])),
        relationship_refs=["runtime/state/relationship/relationship_subject_graph.json"],
        autobiographical_memory_refs=list(
            life_state.get("memory_index", {}).get("relationship_memory_refs", [])
            or ["runtime/state/life_state.json#memory_index.relationship_memory_refs"]
        ),
        shared_terms_refs=["runtime/state/language/shared_term_registry.json"],
        commitment_refs=unresolved_commitments,
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
        relation_subject_ref=relation_subject.get("relationship_id"),
        relation_stage=relation_subject.get("relationship_stage"),
        shared_language_refs=list(
            relationship_graph.get("subjects", [{}])[0].get("shared_language_refs", [])
        ),
        commitment_truth_refs=unresolved_commitments,
        last_contact_refs=[relation_subject.get("last_contact_ref")]
        if relation_subject.get("last_contact_ref")
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
        relation_scope_ref=relation_subject.get("relationship_id"),
        expression_monitor_restore_refs=list(return_packet.get("expression_monitor_restore_refs", [])),
        unresolved_commitment_refs=unresolved_commitments,
        context_accumulation_restore_refs=["runtime/state/terminal/context_accumulation_window.json"],
        language_percept_restore_refs=["runtime/state/language/language_percept_frame.json"],
        semantic_map_restore_refs=["runtime/state/language/semantic_map_frame.json"],
        waiting_heartbeat_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
        next_required_action=next_required_action,
        source_doc_refs=SOURCE_DOC_REFS,
        readme_block_refs=READ_ME_BLOCK_REFS,
        runtime_carrier_refs=RUNTIME_CARRIER_REFS,
    )

    packet = {
        "schema_version": "first_terminal_turn_packet_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "turn_stage": turn_stage,
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
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
        "expression_monitor_dimensions": list(expression_monitor.get("monitor_dimensions", [])),
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
        "dialogue_turn_restore_refs": dialogue_refs,
        "next_required_action": next_required_action,
        "receipt_ref": f"runtime/receipts/first_terminal_turn_{run_id}.json",
    }

    report = {
        "schema_version": "first_terminal_turn_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "engineering_slice_ref": "FIRST_TERMINAL_TURN",
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
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

    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
    )

    try:
        terminal_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(terminal_dir / "session_envelope.json", session_envelope)
        _write_json(terminal_dir / "safe_terminal_loop_state.json", safe_terminal_loop)
        _write_json(terminal_dir / "life_context_frame.json", life_context)
        _write_json(terminal_dir / "relation_turn_frame.json", relation_turn)
        _write_json(terminal_dir / "context_accumulation_window.json", context_accumulation)
        _write_json(terminal_dir / "turn_transition_trace.json", turn_transition)
        _write_json(reports_dir / "first_terminal_turn_packet.json", packet)
        _write_json(reports_dir / "first_terminal_turn_report.json", report)
        _write_json(reports_dir / "first_terminal_turn_digest.json", digest)
        _write_json(receipts_dir / f"first_terminal_turn_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return FirstTerminalTurnResult(exit_code=4, report=report)

    if status == "closed":
        return FirstTerminalTurnResult(exit_code=0, report=report)
    return FirstTerminalTurnResult(exit_code=1 if strict else 0, report=report)


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


def _first_relation_subject(relationship_graph: dict[str, Any]) -> dict[str, Any]:
    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        return subjects[0]
    return {}


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
            input_hashes[str(path)] = _sha256(path)

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
