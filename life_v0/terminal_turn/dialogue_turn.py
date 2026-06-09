from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FirstTerminalDialogueTurn:
    utterance_scaffold: dict[str, Any]
    dialogue_turn_restore_refs: list[str]


def build_first_terminal_dialogue_turn(
    *,
    status: str,
    relation_subject: dict[str, Any],
    shared_term_surfaces: list[str],
    unresolved_commitments: list[str],
    expression_monitor: dict[str, Any],
    semantic_map: dict[str, Any],
    return_packet: dict[str, Any],
    dialogue_turn_restore_refs: list[str],
) -> FirstTerminalDialogueTurn:
    utterance_scaffold = {
        "intent": "resume_life_continuity_before_new_work",
        "surface_strategy": "resume_before_new_content" if status == "closed" else "blocked_until_restore_closure",
        "dialogue_mode": "restored_relation_turn_ready" if status == "closed" else "blocked",
        "relation_scope": relation_subject.get("relationship_id"),
        "relation_role": relation_subject.get("relation_role"),
        "relationship_stage": relation_subject.get("relationship_stage"),
        "shared_term_surfaces": shared_term_surfaces,
        "unresolved_commitment_refs": unresolved_commitments,
        "semantic_focus": semantic_map.get("semantic_focus"),
        "expression_monitor_dimensions": list(
            expression_monitor.get("monitor_dimensions", [])
        ),
        "must_restore_before_speaking": [
            "relation_identity",
            "shared_terms",
            "unresolved_commitments",
            "language_percept",
            "semantic_map",
            "expression_monitor",
        ],
        "carryover_restore_refs": {
            "shared_term_restore_refs": list(return_packet.get("shared_term_restore_refs", [])),
            "expression_monitor_restore_refs": list(
                return_packet.get("expression_monitor_restore_refs", [])
            ),
            "relation_scope_restore_refs": list(
                return_packet.get("relation_scope_restore_refs", [])
            ),
            "self_narrative_restore_refs": list(
                return_packet.get("self_narrative_restore_refs", [])
            ),
            "dialogue_turn_restore_refs": dialogue_turn_restore_refs,
        },
        "response_release_policy": "restore_before_new_input",
    }
    return FirstTerminalDialogueTurn(
        utterance_scaffold=utterance_scaffold,
        dialogue_turn_restore_refs=dialogue_turn_restore_refs,
    )
