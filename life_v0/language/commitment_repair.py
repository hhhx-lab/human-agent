from __future__ import annotations

from typing import Any


def build_commitment_repair_language_index(
    *,
    run_id: str,
    generated_at: str,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "commitment_repair_language_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "commitment_refs": ["commitment-v0-0001"],
        "repair_language_refs": ["repair-language-v0-0001"],
        "repair_obligation_refs": ["repair-obligation-v0-0001"],
        "regret_trace_refs": ["runtime/state/life_state.json#regret_events"],
        "responsibility_trace_refs": ["runtime/state/life_state.json#responsibility_bindings"],
        "source_doc_refs": source_doc_refs,
    }
