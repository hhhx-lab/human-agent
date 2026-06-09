from __future__ import annotations

from typing import Any


def build_dream_report_language_gate(
    *,
    run_id: str,
    generated_at: str,
    dream_fact_boundary: dict[str, Any],
    source_doc_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "dream_report_language_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "dream_fact_gate": "closed" if dream_fact_boundary.get("schema_version") == "dream_fact_boundary_v0" else "blocked",
        "dream_report_refs": ["runtime/state/language/dream_report_language_gate.json#dream-report-language-v0-0001"],
        "source_doc_refs": source_doc_refs,
    }
