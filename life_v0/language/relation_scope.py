from __future__ import annotations


def build_relation_scope_language_index(
    *,
    run_id: str,
    generated_at: str,
    source_doc_refs: list[str],
) -> dict[str, object]:
    return {
        "schema_version": "relation_scope_language_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "relation_scopes": [
            {
                "scope_id": "relation-scope-v0-0001",
                "relation_role": "friend",
                "allowed_terms": ["共同语言", "承诺", "修复"],
                "blocked_cross_scope_terms": ["service_object", "task_requester"],
            }
        ],
        "source_doc_refs": source_doc_refs,
    }
