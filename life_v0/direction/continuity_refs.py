from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/00_research_protocol.md",
    "docs/13_agentic_human_research_synthesis.md",
    "docs/16_digital_life_gap_register.md",
    "docs/258_linear_chain_closure_and_v0_contract_transition.md",
]


def build_continuity_refs(
    *,
    run_id: str,
    generated_at: str,
    resume_order: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "continuity_refs_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "continuity_refs_id": f"continuity-refs-{run_id}",
        "resume_anchor_refs": list(resume_order[:8]),
        "direction_report_refs": [
            "runtime/reports/latest/direction_lock_report.json",
            "runtime/reports/latest/direction_digest.json",
        ],
        "identity_root_refs": ["runtime/state/direction/identity_root.json"],
        "life_state_refs": [
            "runtime/state/life_state.json",
            "runtime/state/self/self_model.json",
            "runtime/state/self/autobiographical_stack.json",
        ],
        "recent_receipt_refs": [
            f"runtime/receipts/direction_lock_{run_id}.json",
            "runtime/receipts/state_store_latest.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }
