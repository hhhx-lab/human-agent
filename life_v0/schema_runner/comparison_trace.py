from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/35_minimal_validator_runner_design.md",
    "docs/65_schema_cross_ref_checker_design.md",
    "docs/66_runner_report_json_examples.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_comparison_trace(
    *,
    run_id: str,
    generated_at: str,
    counterfactual_trace: dict[str, Any],
    consistency_logic: dict[str, Any],
) -> dict[str, Any]:
    branches = list(counterfactual_trace.get("counterfactual_branches", []))
    kept = [branches[0]["branch_id"]] if branches else []
    suppressed = [branch["branch_id"] for branch in branches[1:]]
    return {
        "schema_version": "comparison_trace_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "comparison_trace_id": f"comparison-trace-{run_id}",
        "counterfactual_eval_ref": "runtime/state/schema_runner/counterfactual_trace.json",
        "kept_branch_refs": kept,
        "suppressed_branch_refs": suppressed or ["shadow_release_without_review"],
        "justification_refs": [
            "runtime/state/schema_runner/consistency_logic.json",
            *list(consistency_logic.get("repair_route_refs", []))[:1],
        ],
        "writeback_targets": [
            "runtime/state/action/go_nogo_state.json",
            "runtime/state/action/world_contact_gate_state.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_comparison_trace(trace: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if trace.get("schema_version") != "comparison_trace_v0":
        reasons.append("comparison_trace_gate schema mismatch")
    for field in [
        "comparison_trace_id",
        "counterfactual_eval_ref",
        "kept_branch_refs",
        "suppressed_branch_refs",
        "justification_refs",
        "writeback_targets",
    ]:
        if not trace.get(field):
            reasons.append(f"comparison_trace_gate missing {field}")
    return reasons
