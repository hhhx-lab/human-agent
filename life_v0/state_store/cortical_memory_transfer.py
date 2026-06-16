from __future__ import annotations

from typing import Any

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/01q_memory_engram_consolidation_matrix.md",
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
]

CORTICAL_TRANSFER_POLICY = "swr_replay_then_cortical_slow_integration"


def apply_cortical_memory_transfer(
    *,
    memory_trace_store: dict[str, Any],
    life_schema_map: dict[str, Any] | None,
    replay_trace_ids: list[str],
    generated_at: str,
    swr_replay_weights: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    updated_store = memory_trace_store
    updated_schema = dict(life_schema_map or {})
    weight_by_id = {
        str(item.get("trace_id")): float(item.get("swr_weight") or 0)
        for item in (swr_replay_weights or [])
        if isinstance(item, dict) and item.get("trace_id")
    }
    transfer_diff: list[dict[str, Any]] = []
    cortical_refs: list[str] = []
    replay_id_set = set(replay_trace_ids)
    for trace in updated_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        trace_id = str(trace.get("trace_id") or "")
        if trace_id not in replay_id_set:
            continue
        if trace.get("lifecycle_state") == "protected":
            continue
        replay_count = int(trace.get("offline_replay_count") or 0)
        salience = float(trace.get("replay_salience") or 0.5)
        swr_weight = weight_by_id.get(trace_id, salience)
        if replay_count < 1 or swr_weight < 0.55:
            continue
        before_state = trace.get("cortical_transfer_state")
        if replay_count >= 2 and salience >= 0.62:
            trace["cortical_transfer_state"] = "cortical_linked"
            trace["consolidation_state"] = "cortical_linked"
        else:
            trace["cortical_transfer_state"] = "hippocampal_to_cortical_candidate"
        trace["cortical_integration_ref"] = (
            f"runtime/state/memory/life_schema_map.json#cortical_integration#{trace_id}"
        )
        trace["last_cortical_transfer_at"] = generated_at
        trace["updated_at"] = generated_at
        cortical_refs.append(trace["cortical_integration_ref"])
        transfer_diff.append(
            {
                "trace_id": trace_id,
                "from_state": before_state,
                "to_state": trace.get("cortical_transfer_state"),
                "swr_weight": round(swr_weight, 4),
                "offline_replay_count": replay_count,
                "reason": "swr_weighted_replay_cortical_slow_transfer",
            }
        )
    if cortical_refs:
        updated_schema["cortical_integration_refs"] = _dedupe(
            _string_list(updated_schema.get("cortical_integration_refs")) + cortical_refs
        )[-24:]
        updated_schema["last_cortical_transfer_at"] = generated_at
        updated_schema["cortical_transfer_policy"] = CORTICAL_TRANSFER_POLICY
    return {
        "memory_trace_store": updated_store,
        "life_schema_map": updated_schema,
        "cortical_transfer_diff": transfer_diff,
        "cortical_transfer_count": len(transfer_diff),
        "cortical_transfer_policy": CORTICAL_TRANSFER_POLICY,
    }


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [str(value)] if value else []


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result