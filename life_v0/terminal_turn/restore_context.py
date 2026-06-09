from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..language.dialogue_log import collect_dialogue_turn_refs


@dataclass(frozen=True)
class FirstTerminalRestoreContext:
    birth_packet: dict[str, Any]
    birth_digest: dict[str, Any]
    return_packet: dict[str, Any]
    stage_explanation: dict[str, Any]
    direction_lock: dict[str, Any]
    life_state: dict[str, Any]
    relationship_graph: dict[str, Any]
    shared_term_registry: dict[str, Any]
    expression_monitor: dict[str, Any]
    relation_scope_index: dict[str, Any]
    self_narrative_trace: dict[str, Any]
    language_percept: dict[str, Any]
    semantic_map: dict[str, Any]
    commitment_repair: dict[str, Any]
    dialogue_refs: list[str]
    relation_subject: dict[str, Any]
    shared_term_surfaces: list[str]
    unresolved_commitments: list[str]


def load_first_terminal_restore_context(
    *,
    state_dir: Path,
    reports_dir: Path,
    blocked_reasons: list[str],
) -> FirstTerminalRestoreContext:
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

    relation_subject = _first_relation_subject(relationship_graph)
    shared_term_surfaces = [
        term.get("surface")
        for term in shared_term_registry.get("shared_terms", [])
        if term.get("surface")
    ]
    unresolved_commitments = list(commitment_repair.get("commitment_refs", []))

    return FirstTerminalRestoreContext(
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
        relation_subject=relation_subject,
        shared_term_surfaces=shared_term_surfaces,
        unresolved_commitments=unresolved_commitments,
    )


def build_restored_session_envelope(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    relation_subject: dict[str, Any],
    return_packet: dict[str, Any],
    unresolved_commitments: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "session_envelope_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_turn_mode": "restored_life_turn" if status == "closed" else "blocked",
        "relation_scope": relation_subject.get("relationship_id"),
        "relation_role": relation_subject.get("relation_role"),
        "shared_term_refs": list(return_packet.get("shared_term_restore_refs", [])),
        "unresolved_commitment_refs": unresolved_commitments,
        "expression_monitor_restore_refs": list(
            return_packet.get("expression_monitor_restore_refs", [])
        ),
        "relation_scope_restore_refs": list(return_packet.get("relation_scope_restore_refs", [])),
        "self_narrative_restore_refs": list(
            return_packet.get("self_narrative_restore_refs", [])
        ),
        "dialogue_turn_restore_refs": list(return_packet.get("dialogue_turn_restore_refs", [])),
        "trace_refs": [
            "runtime/reports/latest/stage_explanation_report.json",
            "runtime/reports/latest/first_terminal_turn_report.json",
        ],
    }


def build_safe_terminal_loop_state(
    *,
    run_id: str,
    generated_at: str,
    status: str,
) -> dict[str, Any]:
    return {
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


def _first_relation_subject(relationship_graph: dict[str, Any]) -> dict[str, Any]:
    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        return subjects[0]
    return {}
