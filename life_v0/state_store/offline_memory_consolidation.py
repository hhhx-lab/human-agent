from __future__ import annotations

import hashlib
import json
from typing import Any

from .memory_longitudinal_profile import (
    project_memory_longitudinal_profile_from_offline_cycle,
)
from .memory_trace_store import MEMORY_TRACE_STORE_REF, guard_offline_trace_mutations
from .cortical_memory_transfer import apply_cortical_memory_transfer
from .relationship_self_narrative_writeback import (
    apply_relationship_self_narrative_writeback,
)

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/55_scope_aware_replay_and_consolidation_policy.md",
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]

MEMORY_CONSOLIDATION_REPORT_REF = (
    "runtime/reports/latest/memory_consolidation_report.json"
)


def apply_offline_memory_consolidation(
    *,
    run_id: str,
    generated_at: str,
    memory_trace_store: dict[str, Any],
    life_schema_map: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    dream_window: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    memory_allocation_gate: dict[str, Any] | None = None,
    memory_longitudinal_profile: dict[str, Any] | None = None,
    body_integrator: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sleep_pressure = float(
        ((body_integrator or {}).get("continuous") or {}).get("sleep_pressure", 0.0) or 0.0
    )
    before_traces = json.loads(
        json.dumps(memory_trace_store.get("traces", []))
    )
    updated_store = json.loads(json.dumps(memory_trace_store))
    updated_schema = json.loads(json.dumps(life_schema_map or {}))
    updated_relationship = json.loads(json.dumps(relationship_memory or {}))
    updated_autobiographical = json.loads(json.dumps(autobiographical_stack or {}))

    replay_trace_ids, swr_replay_weights = _select_replay_trace_ids(
        memory_trace_store=updated_store,
        replay_cue_bundle=replay_cue_bundle,
        memory_allocation_gate=memory_allocation_gate,
        dream_window=dream_window,
        sleep_pressure=sleep_pressure,
    )
    salience_updates = _apply_replay_salience_updates(
        updated_store,
        trace_ids=replay_trace_ids,
        generated_at=generated_at,
        sleep_pressure=sleep_pressure,
    )
    schema_promotion_diff = _apply_schema_promotion_side_effects(
        updated_store,
        life_schema_map=updated_schema,
        generated_at=generated_at,
    )
    dream_hypothesis_diff = _apply_dream_hypothesis_residue(
        updated_store,
        run_id=run_id,
        generated_at=generated_at,
        dream_window=dream_window,
        replay_trace_ids=replay_trace_ids,
    )
    relationship_diff = _apply_relationship_offline_writeback(
        updated_relationship,
        replay_trace_ids=replay_trace_ids,
        memory_trace_store=updated_store,
        generated_at=generated_at,
        dream_window=dream_window,
    )
    autobiographical_diff = _apply_autobiographical_offline_writeback(
        updated_autobiographical,
        replay_trace_ids=replay_trace_ids,
        memory_trace_store=updated_store,
        generated_at=generated_at,
    )
    demotion_diff = _collect_demotion_diff(updated_store, before_traces=before_traces)
    self_diff = _apply_self_slow_variable_writeback(
        updated_autobiographical,
        replay_trace_ids=replay_trace_ids,
        generated_at=generated_at,
    )
    _apply_relationship_depth_slow_variable(
        updated_relationship,
        replay_trace_ids=replay_trace_ids,
        generated_at=generated_at,
    )
    narrative_rewrite_result = apply_relationship_self_narrative_writeback(
        relationship_memory=updated_relationship,
        autobiographical_stack=updated_autobiographical,
        memory_trace_store=updated_store,
        replay_trace_ids=replay_trace_ids,
        generated_at=generated_at,
    )
    updated_relationship = narrative_rewrite_result["relationship_memory"]
    updated_autobiographical = narrative_rewrite_result["autobiographical_stack"]
    updated_store = narrative_rewrite_result["memory_trace_store"]
    narrative_rewrite_diff = narrative_rewrite_result.get("narrative_rewrite_diff") or []
    cortical_transfer_result = apply_cortical_memory_transfer(
        memory_trace_store=updated_store,
        life_schema_map=updated_schema,
        replay_trace_ids=replay_trace_ids,
        generated_at=generated_at,
        swr_replay_weights=swr_replay_weights,
    )
    updated_store = cortical_transfer_result["memory_trace_store"]
    updated_schema = cortical_transfer_result["life_schema_map"]
    cortical_transfer_diff = cortical_transfer_result.get("cortical_transfer_diff") or []

    after_traces = updated_store.get("traces", [])
    offline_mutation_guard = guard_offline_trace_mutations(
        before_traces=before_traces,
        after_traces=after_traces,
    )
    if offline_mutation_guard.get("protected_mutation_blocked"):
        updated_store["traces"] = before_traces
        updated_store["trace_ids"] = [
            str(trace.get("trace_id"))
            for trace in before_traces
            if isinstance(trace, dict) and trace.get("trace_id")
        ]
        salience_updates = []
        dream_hypothesis_diff = []
        schema_promotion_diff = []

    consolidation_diff = {
        "trace_salience_updates": salience_updates,
        "schema_promotion_diff": schema_promotion_diff,
        "dream_hypothesis_residue_diff": dream_hypothesis_diff,
        "relationship_deepening_diff": relationship_diff,
        "autobiographical_integration_diff": autobiographical_diff,
        "self_slow_variable_diff": self_diff,
        "demotion_diff": demotion_diff,
        "relationship_self_narrative_rewrite_diff": narrative_rewrite_diff,
        "cortical_transfer_diff": cortical_transfer_diff,
    }
    updated_longitudinal = project_memory_longitudinal_profile_from_offline_cycle(
        profile=memory_longitudinal_profile
        or {
            "schema_version": "memory_longitudinal_profile_v0",
            "turn_count": 0,
            "offline_cycle_count": 0,
            "accessibility_curve": [],
            "relationship_depth_curve": [],
            "self_continuity_curve": [],
            "recall_strength_curve": [],
        },
        generated_at=generated_at,
        memory_consolidation_report={
            "consolidation_diff": {
                "trace_salience_updates": salience_updates,
                "dream_hypothesis_residue_diff": dream_hypothesis_diff,
            }
        },
        relationship_memory=updated_relationship,
        autobiographical_stack=updated_autobiographical,
    )
    promotion_diff = schema_promotion_diff + [
        {
            "source": "offline_replay",
            "trace_id": item.get("trace_id"),
            "reason": "replay_salience_strengthened",
        }
        for item in salience_updates
    ]
    hygiene_actions = _hygiene_actions_from_store(memory_trace_store)
    memory_consolidation_report = {
        "schema_version": "memory_consolidation_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "report_ref": MEMORY_CONSOLIDATION_REPORT_REF,
        "consolidation_route": (
            (offline_consolidation_frame or {}).get("consolidation_route")
            or "dream_replay_trace_relationship_autobiographical_writeback"
        ),
        "fact_boundary": (
            "offline_consolidation_mutates_salience_and_hypothesis_without_fact_promotion"
        ),
        "consolidation_diff": consolidation_diff,
        "promotion_diff": promotion_diff,
        "demotion_diff": demotion_diff,
        "replay_trace_ids": replay_trace_ids,
        "replay_selection_policy": "swr_weighted",
        "cortical_transfer_policy": cortical_transfer_result.get(
            "cortical_transfer_policy"
        ),
        "swr_replay_weights": swr_replay_weights,
        "offline_mutation_guard": offline_mutation_guard,
        "schema_evidence_counts": dict(
            updated_schema.get("schema_evidence_counts") or {}
        ),
        "hygiene_actions": hygiene_actions,
        "sleep_pressure_snapshot": round(sleep_pressure, 4),
        "body_integrator_ref": (
            "runtime/state/body/body_integrator_state.json"
            if body_integrator
            else None
        ),
        "consumer_refs": [
            "runtime/reports/latest/growth_reconsolidation_report.json#consolidation_diff",
            "runtime/state/dream/offline_consolidation_frame.json#memory_consolidation_diff",
            "runtime/state/dream/wake_integration_frame.json#reconsolidation_diff",
            "runtime/state/memory/offline_memory_hygiene_report.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }
    updated_store["last_offline_consolidation_at"] = generated_at
    updated_store["offline_consolidation_report_ref"] = MEMORY_CONSOLIDATION_REPORT_REF
    return {
        "memory_trace_store": updated_store,
        "life_schema_map": updated_schema,
        "relationship_memory": updated_relationship,
        "autobiographical_stack": updated_autobiographical,
        "memory_longitudinal_profile": updated_longitudinal,
        "memory_consolidation_report": memory_consolidation_report,
        "offline_mutation_guard": offline_mutation_guard,
    }


def _apply_relationship_depth_slow_variable(
    relationship_memory: dict[str, Any],
    *,
    replay_trace_ids: list[str],
    generated_at: str,
) -> None:
    depth_profile = dict(
        relationship_memory.get("relationship_memory_depth_profile") or {}
    )
    previous = float(depth_profile.get("longitudinal_depth_score") or 0.35)
    depth_profile["longitudinal_depth_score"] = round(
        min(1.0, previous + len(replay_trace_ids) * 0.04),
        3,
    )
    depth_profile["last_offline_deepening_at"] = generated_at
    depth_profile["offline_replay_trace_count"] = len(replay_trace_ids)
    relationship_memory["relationship_memory_depth_profile"] = depth_profile


def _apply_self_slow_variable_writeback(
    autobiographical_stack: dict[str, Any],
    *,
    replay_trace_ids: list[str],
    generated_at: str,
) -> list[dict[str, Any]]:
    if not replay_trace_ids:
        return []
    slow_refs = [
        f"{MEMORY_TRACE_STORE_REF}#{trace_id}" for trace_id in replay_trace_ids[:6]
    ]
    autobiographical_stack["self_continuity_slow_variable_refs"] = _dedupe(
        _string_list(autobiographical_stack.get("self_continuity_slow_variable_refs"))
        + slow_refs
    )[:24]
    autobiographical_stack["self_narrative_continuity_score"] = round(
        min(
            1.0,
            float(autobiographical_stack.get("self_narrative_continuity_score") or 0.35)
            + len(replay_trace_ids) * 0.03,
        ),
        3,
    )
    autobiographical_stack["last_self_slow_variable_update_at"] = generated_at
    return [
        {
            "integration_kind": "self_slow_variable_offline_update",
            "trace_refs": slow_refs,
            "generated_at": generated_at,
        }
    ]


def _select_replay_trace_ids(
    *,
    memory_trace_store: dict[str, Any],
    replay_cue_bundle: dict[str, Any] | None,
    memory_allocation_gate: dict[str, Any] | None,
    dream_window: dict[str, Any] | None,
    sleep_pressure: float = 0.0,
) -> tuple[list[str], list[dict[str, Any]]]:
    priority_boost: dict[str, float] = {}
    for item in (memory_allocation_gate or {}).get("replay_priority_vector", []):
        if not isinstance(item, dict):
            continue
        trace_ref = str(item.get("trace_ref") or "")
        if "#" not in trace_ref:
            continue
        trace_id = trace_ref.rsplit("#", 1)[-1]
        priority_boost[trace_id] = max(
            priority_boost.get(trace_id, 0.0),
            float(item.get("priority_score") or 0.75),
        )
    bridge = (replay_cue_bundle or {}).get("memory_consolidation_bridge") or {}
    for ref in _string_list(bridge.get("trace_store_refs")):
        if "#" in ref:
            trace_id = ref.rsplit("#", 1)[-1]
            priority_boost[trace_id] = max(priority_boost.get(trace_id, 0.0), 0.85)
    for ref in _string_list((dream_window or {}).get("memory_consolidation_trace_refs")):
        if "memory_trace_store.json#" in ref:
            trace_id = ref.rsplit("#", 1)[-1].replace("trace:", "")
            priority_boost[trace_id] = max(priority_boost.get(trace_id, 0.0), 0.9)

    weighted_candidates: list[tuple[str, float]] = []
    for trace in memory_trace_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        if trace.get("live_trace_origin") != "live_dialogue_turn":
            continue
        if trace.get("lifecycle_state") == "deprecated":
            continue
        trace_id = str(trace.get("trace_id") or "")
        if not trace_id:
            continue
        salience = float(trace.get("replay_salience") or 0.5)
        accessibility = float(trace.get("accessibility_score") or 0.55)
        replay_count = int(trace.get("offline_replay_count") or 0)
        swr_weight = round(
            salience * 0.45
            + accessibility * 0.35
            + min(0.2, replay_count * 0.04)
            + priority_boost.get(trace_id, 0.0) * 0.25
            + sleep_pressure * 0.15,
            4,
        )
        weighted_candidates.append((trace_id, swr_weight))

    weighted_candidates.sort(key=lambda item: item[1], reverse=True)
    trace_ids = _dedupe([trace_id for trace_id, _ in weighted_candidates])[:12]
    swr_replay_weights = [
        {"trace_id": trace_id, "swr_weight": weight}
        for trace_id, weight in weighted_candidates[:12]
    ]
    return trace_ids, swr_replay_weights


def _apply_replay_salience_updates(
    memory_trace_store: dict[str, Any],
    *,
    trace_ids: list[str],
    generated_at: str,
    sleep_pressure: float = 0.0,
) -> list[dict[str, Any]]:
    updates: list[dict[str, Any]] = []
    trace_id_set = set(trace_ids)
    for trace in memory_trace_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        trace_id = str(trace.get("trace_id") or "")
        if trace_id not in trace_id_set:
            continue
        if trace.get("lifecycle_state") == "protected":
            continue
        before_replay = int(trace.get("offline_replay_count") or 0)
        before_salience = float((trace.get("replay_salience") or 0.5))
        salience_vector = dict(trace.get("salience_vector") or {})
        before_scalar = float(salience_vector.get("salience") or before_salience)
        salience_boost = round(0.08 * (0.5 + sleep_pressure * 0.5), 3)
        trace["offline_replay_count"] = before_replay + 1
        trace["replay_salience"] = round(min(0.98, before_salience + salience_boost), 3)
        salience_vector["salience"] = round(min(0.98, before_scalar + salience_boost * 0.85), 3)
        salience_vector["last_offline_consolidation_at"] = generated_at
        trace["salience_vector"] = salience_vector
        trace["last_replayed_at"] = generated_at
        if trace.get("consolidation_state") == "episodic":
            trace["consolidation_state"] = "consolidating"
        trace["updated_at"] = generated_at
        updates.append(
            {
                "trace_id": trace_id,
                "offline_replay_count": trace["offline_replay_count"],
                "replay_salience": trace["replay_salience"],
                "consolidation_state": trace.get("consolidation_state"),
            }
        )
    return updates


def _apply_schema_promotion_side_effects(
    memory_trace_store: dict[str, Any],
    *,
    life_schema_map: dict[str, Any],
    generated_at: str,
) -> list[dict[str, Any]]:
    promotion_diff: list[dict[str, Any]] = []
    promoted_ids = _string_list(life_schema_map.get("last_promoted_schema_ids"))
    if not promoted_ids:
        return promotion_diff
    for schema in life_schema_map.get("schemas", []):
        if not isinstance(schema, dict):
            continue
        schema_id = str(schema.get("schema_id") or "")
        if schema_id not in promoted_ids:
            continue
        promotion_diff.append(
            {
                "schema_id": schema_id,
                "schema_kind": schema.get("schema_kind"),
                "source": "life_schema_map",
                "reason": "schema_evidence_threshold_met",
                "last_promoted_at": generated_at,
            }
        )
        for trace_ref in _string_list(schema.get("trace_refs")):
            trace_id = trace_ref.rsplit("#", 1)[-1].replace("trace:", "")
            for trace in memory_trace_store.get("traces", []):
                if not isinstance(trace, dict):
                    continue
                if str(trace.get("trace_id")) != trace_id:
                    continue
                if trace.get("lifecycle_state") == "protected":
                    continue
                trace["schema_promotion_refs"] = _dedupe(
                    _string_list(trace.get("schema_promotion_refs"))
                    + [f"runtime/state/memory/life_schema_map.json#schema:{schema_id}"]
                )
                trace["consolidation_state"] = "schema_linked"
                trace["updated_at"] = generated_at
    life_schema_map["last_offline_consolidation_at"] = generated_at
    return promotion_diff


def _apply_dream_hypothesis_residue(
    memory_trace_store: dict[str, Any],
    *,
    run_id: str,
    generated_at: str,
    dream_window: dict[str, Any] | None,
    replay_trace_ids: list[str],
) -> list[dict[str, Any]]:
    if not dream_window:
        return []
    dream_window_id = str(dream_window.get("dream_window_id") or f"dream-window-{run_id}")
    source_refs = _dedupe(
        _string_list(dream_window.get("memory_consolidation_trace_refs"))
        + _string_list(dream_window.get("source_trace_refs"))
    )
    residue_id = f"memory-trace-dream-hypothesis-{_short_hash('|'.join([run_id, dream_window_id]))}"
    if any(
        str(trace.get("trace_id")) == residue_id
        for trace in memory_trace_store.get("traces", [])
        if isinstance(trace, dict)
    ):
        return []
    hypothesis_trace = {
        "trace_id": residue_id,
        "memory_kind": "episodic",
        "claim_type": "hypothesis",
        "event_boundary": f"dream_hypothesis_residue:{dream_window_id}",
        "source_evidence_refs": source_refs[:8],
        "retrieval_cues": ["dream_residue", "offline_replay"],
        "internal_state_snapshot_refs": [
            "runtime/state/dream/dream_experience_window.json"
        ],
        "social_context_refs": _string_list(
            dream_window.get("relationship_deep_dream_refs")
        )[:4],
        "salience_vector": {
            "dream_residue": "tracked",
            "reportability": "guarded",
        },
        "consolidation_state": "sandboxed",
        "lifecycle_state": "active",
        "confidence": 0.41,
        "confidence_label": "dream_hypothesis_not_fact",
        "revision_history_refs": [],
        "live_trace_origin": "offline_dream_replay",
        "dream_window_ref": f"runtime/state/dream/dream_experience_window.json#{dream_window_id}",
        "replayed_trace_ids": replay_trace_ids[:6],
        "content_summary": (
            "Offline dream replay residue linked to replayed live traces; hypothesis only."
        ),
        "created_at": generated_at,
        "updated_at": generated_at,
        "run_id": run_id,
    }
    traces = list(memory_trace_store.get("traces", []))
    traces.append(hypothesis_trace)
    memory_trace_store["traces"] = traces
    memory_trace_store["trace_ids"] = [
        str(trace.get("trace_id"))
        for trace in traces
        if isinstance(trace, dict) and trace.get("trace_id")
    ]
    memory_trace_store["trace_count"] = len(memory_trace_store["trace_ids"])
    return [
        {
            "trace_id": residue_id,
            "claim_type": "hypothesis",
            "lifecycle_state": "active",
            "consolidation_state": "sandboxed",
            "reason": "dream_replay_hypothesis_residue",
            "dream_window_ref": hypothesis_trace["dream_window_ref"],
        }
    ]


def _apply_relationship_offline_writeback(
    relationship_memory: dict[str, Any],
    *,
    replay_trace_ids: list[str],
    memory_trace_store: dict[str, Any],
    generated_at: str,
    dream_window: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    deepening: list[dict[str, Any]] = []
    deep_refs: list[str] = []
    for trace_id in replay_trace_ids:
        trace_ref = f"{MEMORY_TRACE_STORE_REF}#{trace_id}"
        deep_refs.append(trace_ref)
        deepening.append(
            {
                "relation_subject_id": _trace_relation_subject_id(
                    memory_trace_store, trace_id
                ),
                "trace_ref": trace_ref,
                "writeback_kind": "deep_sediment_replay",
                "generated_at": generated_at,
            }
        )
    if deep_refs:
        relationship_memory["deep_sediment_memory_refs"] = _dedupe(
            _string_list(relationship_memory.get("deep_sediment_memory_refs"))
            + deep_refs
        )[:24]
        relationship_memory["exit_dream_consolidation_refs"] = _dedupe(
            _string_list(relationship_memory.get("exit_dream_consolidation_refs"))
            + _string_list((dream_window or {}).get("relationship_deep_dream_refs"))
        )
        we_memory = list(relationship_memory.get("we_memory_traces", []))
        if isinstance(we_memory, list):
            we_memory.append(
                {
                    "trace_refs": deep_refs[:6],
                    "consolidation_kind": "offline_replay_deepening",
                    "generated_at": generated_at,
                }
            )
            relationship_memory["we_memory_traces"] = we_memory[-12:]
        relationship_memory["last_offline_consolidation_at"] = generated_at
    return deepening


def _apply_autobiographical_offline_writeback(
    autobiographical_stack: dict[str, Any],
    *,
    replay_trace_ids: list[str],
    memory_trace_store: dict[str, Any],
    generated_at: str,
) -> list[dict[str, Any]]:
    integration: list[dict[str, Any]] = []
    episode_refs = [
        f"{MEMORY_TRACE_STORE_REF}#{trace_id}" for trace_id in replay_trace_ids
    ]
    if not episode_refs:
        return integration
    autobiographical_stack["offline_consolidation_episode_refs"] = _dedupe(
        _string_list(autobiographical_stack.get("offline_consolidation_episode_refs"))
        + episode_refs
    )[:24]
    hierarchy = dict(autobiographical_stack.get("memory_hierarchy") or {})
    specific = _string_list(hierarchy.get("specific_episode_refs"))
    hierarchy["specific_episode_refs"] = _dedupe(specific + episode_refs)[:24]
    autobiographical_stack["memory_hierarchy"] = hierarchy
    autobiographical_stack["last_offline_consolidation_at"] = generated_at
    for trace_id in replay_trace_ids:
        integration.append(
            {
                "trace_id": trace_id,
                "integration_kind": "autobiographical_offline_replay",
                "semantic_focus": _trace_semantic_focus(memory_trace_store, trace_id),
                "generated_at": generated_at,
            }
        )
    return integration


def _collect_demotion_diff(
    memory_trace_store: dict[str, Any],
    *,
    before_traces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    before_by_id = {
        str(trace.get("trace_id")): trace
        for trace in before_traces
        if isinstance(trace, dict) and trace.get("trace_id")
    }
    demotions: list[dict[str, Any]] = []
    for trace in memory_trace_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        trace_id = str(trace.get("trace_id") or "")
        before = before_by_id.get(trace_id)
        if not before:
            continue
        if (
            before.get("consolidation_state") == "episodic"
            and trace.get("consolidation_state") == "consolidating"
        ):
            demotions.append(
                {
                    "trace_id": trace_id,
                    "from_state": "episodic",
                    "to_state": "consolidating",
                    "reason": "offline_replay_without_fact_promotion",
                }
            )
    return demotions


def _trace_relation_subject_id(
    memory_trace_store: dict[str, Any], trace_id: str
) -> str | None:
    for trace in memory_trace_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        if str(trace.get("trace_id")) == trace_id:
            return trace.get("relation_subject_id")
    return None


def _trace_semantic_focus(
    memory_trace_store: dict[str, Any], trace_id: str
) -> str | None:
    for trace in memory_trace_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        if str(trace.get("trace_id")) == trace_id:
            return trace.get("semantic_focus")
    return None


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def _hygiene_actions_from_store(memory_trace_store: dict[str, Any]) -> list[dict[str, Any]]:
    hygiene_ref = str(memory_trace_store.get("last_hygiene_report_ref") or "")
    if not hygiene_ref:
        return []
    return [
        {
            "source_ref": hygiene_ref,
            "action": "offline_memory_hygiene_applied",
            "reason": "trace_store_last_hygiene_report_ref_present",
        }
    ]


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, tuple):
        return [str(item) for item in value if item]
    if isinstance(value, set):
        return [str(item) for item in sorted(value) if item]
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