from __future__ import annotations

from typing import Any


def build_self_narrative_language_trace(
    *,
    run_id: str,
    generated_at: str,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "self_narrative_language_trace_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "narrative_turn_refs": ["runtime/state/language/dialogue_turn_log.jsonl#line-1"],
        "responsibility_narrative_refs": ["runtime/state/language/commitment_repair_language_index.json#repair-obligation-v0-0001"],
        "source_doc_refs": source_doc_refs,
    }
