from __future__ import annotations

from typing import Any


def build_shared_term_registry(
    *,
    run_id: str,
    generated_at: str,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "shared_term_registry_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "shared_terms": [
            {
                "term_id": "shared-term-v0-0001",
                "surface": "共同语言",
                "relation_scope": "friend",
                "meaning_ref": "runtime/state/language/language_relationship_state.json#shared-language-v0-0001",
            }
        ],
        "source_doc_refs": source_doc_refs,
    }
