from __future__ import annotations

from typing import Any


def build_language_relationship_state(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    source_doc_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "language_relationship_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "relationship_kinds": ["friend", "family", "classmate", "stranger", "co_present_subject"],
        "expression_style": "reflective_relational_traceable",
        "shared_language_refs": ["runtime/state/language/language_relationship_state.json#shared-language-v0-0001"],
        "repair_language_refs": ["runtime/state/language/commitment_repair_language_index.json#repair-language-v0-0001"],
        "promise_trace_refs": ["runtime/state/language/commitment_repair_language_index.json#commitment-v0-0001"],
        "source_doc_refs": source_doc_refs,
        "existing_language_state": dict(life_state.get("language_state", {})),
    }
