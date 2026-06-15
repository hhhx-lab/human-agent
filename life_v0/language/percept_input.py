from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DIALOGUE_LOG_REF = "runtime/state/language/dialogue_turn_log.jsonl"
PERCEPT_INPUT_BOUNDARY = "structured_percept_input_not_spoken_response"


def resolve_incoming_turn_for_language_build(
    *,
    state_dir: Path,
    relation_scope_index: dict[str, Any],
    shared_term_registry: dict[str, Any],
    commitment_repair_index: dict[str, Any] | None = None,
    self_narrative_trace: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    speaker_role = _active_relation_role(relation_scope_index)
    dialogue_log_path = state_dir / "language" / "dialogue_turn_log.jsonl"

    dialogue_turn = _latest_external_dialogue_turn(dialogue_log_path)
    if dialogue_turn:
        utterance = str(dialogue_turn.get("utterance", "")).strip()
        if utterance:
            turn_id = str(dialogue_turn.get("turn_id", "")).strip()
            source_ref = (
                f"{DIALOGUE_LOG_REF}#{turn_id}"
                if turn_id
                else f"{DIALOGUE_LOG_REF}#external_relation_turn"
            )
            return _resolved_turn(
                incoming_surface=utterance,
                speaker_role=str(dialogue_turn.get("relation_role") or speaker_role),
                percept_input_mode="dialogue_turn_log",
                percept_input_source_ref=source_ref,
            )

    terminal_life_loop_state = terminal_life_loop_state or {}
    terminal_utterance = str(
        terminal_life_loop_state.get("last_external_turn_utterance", "")
    ).strip()
    if terminal_utterance:
        return _resolved_turn(
            incoming_surface=terminal_utterance,
            speaker_role=speaker_role,
            percept_input_mode="terminal_life_loop",
            percept_input_source_ref=(
                "runtime/state/terminal/terminal_life_loop_state.json"
                "#last_external_turn_utterance"
            ),
        )

    commitment_repair_index = commitment_repair_index or {}
    commitment_utterance = str(
        commitment_repair_index.get("last_external_turn_utterance", "")
    ).strip()
    if commitment_utterance:
        return _resolved_turn(
            incoming_surface=commitment_utterance,
            speaker_role=speaker_role,
            percept_input_mode="commitment_repair_index",
            percept_input_source_ref=(
                "runtime/state/language/commitment_repair_language_index.json"
                "#last_external_turn_utterance"
            ),
        )

    self_narrative_trace = self_narrative_trace or {}
    narrative_turn = self_narrative_trace.get("last_external_turn")
    if isinstance(narrative_turn, dict):
        narrative_utterance = str(narrative_turn.get("utterance", "")).strip()
        if narrative_utterance:
            return _resolved_turn(
                incoming_surface=narrative_utterance,
                speaker_role=speaker_role,
                percept_input_mode="self_narrative_trace",
                percept_input_source_ref=(
                    "runtime/state/language/self_narrative_language_trace.json"
                    "#last_external_turn"
                ),
            )

    relationship_memory = relationship_memory or {}
    memory_utterance = _relationship_memory_external_utterance(relationship_memory)
    if memory_utterance:
        return _resolved_turn(
            incoming_surface=memory_utterance,
            speaker_role=speaker_role,
            percept_input_mode="relationship_memory",
            percept_input_source_ref=(
                "runtime/state/memory/relationship_memory.json"
                "#last_external_turn_utterance"
            ),
        )

    evidence_surface = _bootstrap_evidence_surface(
        shared_term_registry=shared_term_registry,
        commitment_repair_index=commitment_repair_index,
    )
    return _resolved_turn(
        incoming_surface=evidence_surface,
        speaker_role=speaker_role,
        percept_input_mode="relationship_evidence_bootstrap",
        percept_input_source_ref=(
            "runtime/state/language/shared_term_registry.json"
            "#relationship_evidence_bootstrap"
        ),
    )


def _resolved_turn(
    *,
    incoming_surface: str,
    speaker_role: str,
    percept_input_mode: str,
    percept_input_source_ref: str,
) -> dict[str, Any]:
    return {
        "incoming_turn": {
            "incoming_surface": incoming_surface,
            "speaker_role": speaker_role or "friend",
        },
        "percept_input_mode": percept_input_mode,
        "percept_input_source_ref": percept_input_source_ref,
        "percept_input_boundary": PERCEPT_INPUT_BOUNDARY,
    }


def _latest_external_dialogue_turn(dialogue_log_path: Path) -> dict[str, Any] | None:
    entries = _read_jsonl(dialogue_log_path)
    for entry in reversed(entries):
        if not isinstance(entry, dict):
            continue
        if entry.get("schema_version") != "dialogue_turn_event_v0":
            continue
        utterance = str(entry.get("utterance", "")).strip()
        if not utterance:
            continue
        if entry.get("event_role") == "external_relation_turn":
            return entry
    for entry in reversed(entries):
        if not isinstance(entry, dict):
            continue
        utterance = str(entry.get("utterance", "")).strip()
        if utterance:
            return entry
    return None


def _relationship_memory_external_utterance(
    relationship_memory: dict[str, Any],
) -> str:
    for key in (
        "last_external_turn_utterance",
        "last_relation_turn_utterance",
        "last_dialogue_utterance",
    ):
        utterance = str(relationship_memory.get(key, "")).strip()
        if utterance:
            return utterance
    subjects = relationship_memory.get("relationship_subjects", [])
    if isinstance(subjects, list):
        for subject in subjects:
            if not isinstance(subject, dict):
                continue
            utterance = str(subject.get("last_external_turn_utterance", "")).strip()
            if utterance:
                return utterance
    return ""


def _bootstrap_evidence_surface(
    *,
    shared_term_registry: dict[str, Any],
    commitment_repair_index: dict[str, Any],
) -> str:
    tokens: list[str] = []
    for term in shared_term_registry.get("shared_terms", []):
        if not isinstance(term, dict):
            continue
        surface = str(term.get("surface", "")).strip()
        if surface and surface not in tokens:
            tokens.append(surface)
    if commitment_repair_index.get("repair_obligation_refs") and "修复" not in tokens:
        tokens.append("修复")
    if commitment_repair_index.get("commitment_refs") and "承诺" not in tokens:
        tokens.append("承诺")
    return " ".join(tokens)


def _active_relation_role(relation_scope_index: dict[str, Any]) -> str:
    relation_scopes = relation_scope_index.get("relation_scopes", [])
    if relation_scopes and isinstance(relation_scopes[0], dict):
        relation_role = str(relation_scopes[0].get("relation_role", "")).strip()
        if relation_role:
            return relation_role
    return "friend"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    entries: list[dict[str, Any]] = []
    for line in lines:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except (ValueError, TypeError):
            continue
        if isinstance(payload, dict):
            entries.append(payload)
    return entries