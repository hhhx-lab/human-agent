from __future__ import annotations

from typing import Any


def build_commitment_repair_language_index(
    *,
    run_id: str,
    generated_at: str,
    responsibility_loop_state: dict[str, Any] | None = None,
    source_doc_refs: list[str],
) -> dict[str, Any]:
    responsibility_loop_state = responsibility_loop_state or {}
    repair_obligation_refs = list(responsibility_loop_state.get("repair_obligation_refs", []))
    regret_trace_refs = [
        item.get("regret_pressure_id")
        for item in responsibility_loop_state.get("regret_pressure_candidates", [])
        if isinstance(item, dict) and item.get("regret_pressure_id")
    ]
    responsibility_trace_refs = [
        item.get("responsibility_event_id")
        for item in responsibility_loop_state.get("responsibility_attribution_events", [])
        if isinstance(item, dict) and item.get("responsibility_event_id")
    ]
    return {
        "schema_version": "commitment_repair_language_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "commitment_refs": ["commitment-v0-0001"],
        "repair_language_refs": ["repair-language-v0-0001"],
        "repair_obligation_refs": repair_obligation_refs or ["repair-obligation-v0-0001"],
        "regret_trace_refs": regret_trace_refs or ["runtime/state/life_state.json#regret_events"],
        "responsibility_trace_refs": responsibility_trace_refs or ["runtime/state/life_state.json#responsibility_bindings"],
        "responsibility_loop_ref": "runtime/state/action/responsibility_loop_state.json",
        "source_doc_refs": source_doc_refs,
    }
