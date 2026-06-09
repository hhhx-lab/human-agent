from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .context_accumulation import build_context_accumulation_window, build_life_context_frame
from .restore_context import FirstTerminalRestoreContext
from .turn_transition import build_relation_turn_frame, build_turn_transition_trace


WAITING_HEARTBEAT_REF = "runtime/reports/latest/digital_life_waiting_heartbeat.json"


@dataclass(frozen=True)
class FirstTerminalConversationCarryover:
    context_accumulation: dict[str, Any]
    life_context: dict[str, Any]
    relation_turn: dict[str, Any]
    turn_transition: dict[str, Any]


def build_first_terminal_turn_carryover(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    turn_stage: str,
    next_required_action: str,
    restored: FirstTerminalRestoreContext,
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
) -> FirstTerminalConversationCarryover:
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
        waiting_heartbeat_ref=WAITING_HEARTBEAT_REF,
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
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
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
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
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
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
        waiting_heartbeat_ref=WAITING_HEARTBEAT_REF,
        next_required_action=next_required_action,
        source_doc_refs=source_doc_refs,
        readme_block_refs=readme_block_refs,
        runtime_carrier_refs=runtime_carrier_refs,
    )

    return FirstTerminalConversationCarryover(
        context_accumulation=context_accumulation,
        life_context=life_context,
        relation_turn=relation_turn,
        turn_transition=turn_transition,
    )
