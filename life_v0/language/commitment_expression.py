from __future__ import annotations

from typing import Any


def build_commitment_expression_plan(
    *,
    run_id: str,
    generated_at: str,
    expression_plan: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    commitment_truth_state: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    responsibility_loop_state: dict[str, Any],
    relationship_timeline: dict[str, Any],
    source_doc_refs: list[str],
) -> dict[str, Any]:
    repair_refs = list(commitment_repair_index.get("repair_obligation_refs", []))
    commitment_refs = list(commitment_repair_index.get("commitment_refs", []))
    responsibility_event_refs = list(responsibility_ledger.get("responsibility_event_refs", []))
    regret_refs = list(commitment_repair_index.get("regret_trace_refs", []))
    relationship_injury_refs = [
        f"runtime/state/relationship/relationship_timeline.json#{item.get('relationship_injury_id')}"
        for item in relationship_timeline.get("relationship_injury_traces", [])
        if isinstance(item, dict) and item.get("relationship_injury_id")
    ]
    act_type_order = [
        "clarify",
        "commitment",
        "boundary_statement",
        "apology",
        "followup_commitment",
    ]

    language_act_candidates = [
        {
            "act_id": f"commitment-act-{run_id}-0001",
            "act_type": "clarify",
            "surface_goal": "先澄清共同语言和当前承诺的具体含义。",
            "trigger_refs": ["runtime/state/language/expression_plan.json#semantic_goal"],
        },
        {
            "act_id": f"commitment-act-{run_id}-0002",
            "act_type": "commitment",
            "surface_goal": "把未闭合承诺重新说清，并保持可追踪的后续兑现窗口。",
            "trigger_refs": commitment_refs or ["runtime/state/language/commitment_repair_language_index.json#commitment_refs"],
        },
    ]
    if repair_refs or regret_refs or relationship_injury_refs:
        language_act_candidates.append(
            {
                "act_id": f"commitment-act-{run_id}-0003",
                "act_type": "apology",
                "surface_goal": "当修复压力存在时，先承担责任，再表达道歉与回补意图。",
                "trigger_refs": repair_refs + regret_refs + relationship_injury_refs,
            }
        )
        language_act_candidates.append(
            {
                "act_id": f"commitment-act-{run_id}-0004",
                "act_type": "followup_commitment",
                "surface_goal": "给出后续修复与兑现承诺的下一次关系回合探针。",
                "trigger_refs": responsibility_event_refs or ["runtime/state/responsibility/responsibility_ledger.json#responsibility_events"],
            }
        )

    return {
        "schema_version": "commitment_expression_plan_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "semantic_goal": expression_plan.get("semantic_goal", "repair_commitment_shared_language"),
        "delay_or_release_decision": expression_plan.get("delay_or_release_decision", "delay_for_clarification"),
        "repair_pressure": expression_plan.get("repair_pressure", 0),
        "responsibility_pressure": expression_plan.get("responsibility_pressure", 0),
        "act_type_order": act_type_order,
        "language_act_candidates": language_act_candidates,
        "repair_obligation_refs": repair_refs,
        "commitment_truth_refs": list(commitment_truth_state.get("open_commitment_refs", [])) or commitment_refs,
        "responsibility_event_refs": responsibility_event_refs,
        "regret_trace_refs": regret_refs,
        "relationship_injury_refs": relationship_injury_refs,
        "relationship_timeline_ref": "runtime/state/relationship/relationship_timeline.json",
        "responsibility_loop_ref": "runtime/state/action/responsibility_loop_state.json",
        "commitment_repair_index_ref": "runtime/state/language/commitment_repair_language_index.json",
        "source_doc_refs": source_doc_refs,
        "counterfactual_repair_refs": [
            item.get("counterfactual_id")
            for item in responsibility_loop_state.get("counterfactual_repair_frames", [])
            if isinstance(item, dict) and item.get("counterfactual_id")
        ],
    }
