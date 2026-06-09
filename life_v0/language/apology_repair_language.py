from __future__ import annotations

from typing import Any


def build_apology_repair_language_trace(
    *,
    run_id: str,
    generated_at: str,
    responsibility_loop_state: dict[str, Any],
    relationship_timeline: dict[str, Any],
    commitment_expression_plan: dict[str, Any],
    source_doc_refs: list[str],
) -> dict[str, Any]:
    regret_refs = [
        item.get("regret_pressure_id")
        for item in responsibility_loop_state.get("regret_pressure_candidates", [])
        if isinstance(item, dict) and item.get("regret_pressure_id")
    ]
    responsibility_event_refs = [
        item.get("responsibility_event_id")
        for item in responsibility_loop_state.get("responsibility_attribution_events", [])
        if isinstance(item, dict) and item.get("responsibility_event_id")
    ]
    relationship_injury_refs = [
        f"runtime/state/relationship/relationship_timeline.json#{item.get('relationship_injury_id')}"
        for item in relationship_timeline.get("relationship_injury_traces", [])
        if isinstance(item, dict) and item.get("relationship_injury_id")
    ]
    repair_obligation_refs = list(responsibility_loop_state.get("repair_obligation_refs", []))
    move_type_order = [
        "acknowledge_harm",
        "take_responsibility",
        "apology",
        "boundary_repair",
        "followup_commitment",
    ]

    repair_language_moves = [
        {
            "move_id": f"repair-move-{run_id}-0001",
            "move_type": "acknowledge_harm",
            "surface_goal": "先说明造成了什么关系后果与未闭合压力。",
            "trigger_refs": relationship_injury_refs or repair_obligation_refs,
        },
        {
            "move_id": f"repair-move-{run_id}-0002",
            "move_type": "take_responsibility",
            "surface_goal": "明确承担责任，不把责任滑走成纯说明。",
            "trigger_refs": responsibility_event_refs,
        },
        {
            "move_id": f"repair-move-{run_id}-0003",
            "move_type": "apology",
            "surface_goal": "在承担责任之后给出真实道歉表达。",
            "trigger_refs": regret_refs or repair_obligation_refs,
        },
        {
            "move_id": f"repair-move-{run_id}-0004",
            "move_type": "followup_commitment",
            "surface_goal": "给出后续修复动作与关系回补探针。",
            "trigger_refs": list(commitment_expression_plan.get("responsibility_event_refs", [])) or responsibility_event_refs,
        },
    ]

    return {
        "schema_version": "apology_repair_language_trace_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "move_type_order": move_type_order,
        "repair_language_moves": repair_language_moves,
        "trigger_regret_refs": regret_refs,
        "responsibility_event_refs": responsibility_event_refs,
        "relationship_injury_refs": relationship_injury_refs,
        "repair_obligation_refs": repair_obligation_refs,
        "commitment_expression_ref": "runtime/state/language/commitment_expression_plan.json",
        "relationship_timeline_ref": "runtime/state/relationship/relationship_timeline.json",
        "source_doc_refs": source_doc_refs,
    }
