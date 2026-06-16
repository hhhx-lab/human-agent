from __future__ import annotations

from typing import Any

OFFLINE_DREAM_ENTRY_VECTOR_REF = "runtime/state/dream/offline_dream_entry_vector.json"
DREAM_CUE_POLICY_STATE_REF = "runtime/state/dream/dream_cue_policy_state.json"

SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/v0/entry/v0_dream_module_implementation_plan.md",
    "docs/real—live0/08_dream_sleep_offline_life.md",
]


def build_offline_dream_entry_vector(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    pain_replay: dict[str, Any] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    need_state_vector: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    exit_dream_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    life_state = life_state or {}
    replay_cue_bundle = replay_cue_bundle or {}
    pain_replay = pain_replay or {}
    memory_trace_store = memory_trace_store or {}
    need_state_vector = need_state_vector or {}
    body_resource_budget = body_resource_budget or {}
    relationship_memory = relationship_memory or {}
    exit_dream_summary = exit_dream_summary or {}

    traces = [
        trace for trace in memory_trace_store.get("traces", []) if isinstance(trace, dict)
    ]
    unmerged = sum(
        1
        for trace in traces
        if str(trace.get("lifecycle_state") or "") in {"candidate", "active", "encoding"}
    )
    dream_records = list(life_state.get("dream_records", []))
    turn_residue = list(replay_cue_bundle.get("turn_residue_refs", []))
    relationship_residue = list(replay_cue_bundle.get("relationship_residue_refs", []))
    repair_obligations = list(pain_replay.get("repair_obligation_refs", []))
    anti_forgetting = list(replay_cue_bundle.get("anti_forgetting_targets", []))

    sleep_pressure = float(need_state_vector.get("sleep_pressure", 0.0) or 0.0)
    sleep_pressure += min(len(dream_records) * 0.08, 0.4)
    sleep_pressure += min(unmerged * 0.03, 0.35)
    if exit_dream_summary.get("source_dialogue_turn_count"):
        sleep_pressure += 0.15

    fatigue_level = str(
        ((body_resource_budget.get("fatigue_state") or {}).get("level") or "baseline")
    )
    fatigue_load = 0.2 if fatigue_level in {"elevated", "high", "critical"} else 0.05

    relationship_pressure = min(
        1.0,
        len(relationship_residue) * 0.1
        + len(relationship_memory.get("relationship_theme_tags", [])) * 0.05,
    )
    pain_regret_load = min(1.0, len(repair_obligations) * 0.12)

    selected_modes: list[str] = []
    blocked: list[str] = []
    if sleep_pressure >= 0.2 or unmerged >= 3:
        selected_modes.append("NREMReplayCycle")
    if relationship_pressure >= 0.15 or pain_regret_load >= 0.2:
        selected_modes.append("REMDreamGeneration")
    if turn_residue or exit_dream_summary.get("deduplicated_episode_summaries"):
        selected_modes.append("DefaultDriftMode")
    if fatigue_load >= 0.15 or anti_forgetting:
        selected_modes.append("FatigueRecoveryMode")
    if not selected_modes:
        selected_modes = ["DefaultDriftMode"]
        blocked.append("no_strong_pressure_default_drift_only")

    return {
        "schema_version": "offline_dream_entry_vector_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "OfflineDreamEntryVector",
        "sleep_pressure_vector": {
            "sleep_pressure": round(sleep_pressure, 3),
            "dream_record_count": len(dream_records),
            "unmerged_trace_count": unmerged,
            "exit_dialogue_turn_count": exit_dream_summary.get("source_dialogue_turn_count", 0),
        },
        "circadian_gate": {
            "fatigue_level": fatigue_level,
            "fatigue_load": fatigue_load,
        },
        "body_state_debt": {
            "fatigue_state_ref": "runtime/state/body/body_resource_budget.json",
            "maintenance_pressure": len(turn_residue),
        },
        "memory_consolidation_need": {
            "trace_count": len(traces),
            "unmerged_trace_count": unmerged,
            "memory_trace_store_ref": "runtime/state/memory/memory_trace_store.json",
        },
        "relationship_pressure": {
            "residue_ref_count": len(relationship_residue),
            "theme_tag_count": len(relationship_memory.get("relationship_theme_tags", [])),
        },
        "pain_regret_load": {
            "repair_obligation_count": len(repair_obligations),
            "pain_residue_count": len(replay_cue_bundle.get("pain_regret_residue_refs", [])),
        },
        "selected_offline_modes": selected_modes,
        "entry_reason_refs": _dedupe(
            [
                "runtime/state/dream/offline_dream_entry_vector.json",
                "runtime/state/memory/memory_trace_store.json" if traces else "",
                "runtime/state/dream/exit_dream_consolidation_summary.json"
                if exit_dream_summary
                else "",
            ]
        ),
        "blocked_or_deferred_reasons": blocked,
        "offline_dream_entry_vector_ref": OFFLINE_DREAM_ENTRY_VECTOR_REF,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_dream_cue_policy_state(
    *,
    run_id: str,
    generated_at: str,
    entry_vector: dict[str, Any] | None = None,
    exit_dream_summary: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    web_dream_learning_state: dict[str, Any] | None = None,
    topic_history: dict[str, Any] | None = None,
) -> dict[str, Any]:
    entry_vector = entry_vector or {}
    exit_dream_summary = exit_dream_summary or {}
    relationship_memory = relationship_memory or {}
    replay_cue_bundle = replay_cue_bundle or {}
    web_dream_learning_state = web_dream_learning_state or {}
    topic_history = topic_history or {}

    candidate_cues: list[dict[str, Any]] = []
    for episode in exit_dream_summary.get("deduplicated_episode_summaries", [])[:6]:
        if not isinstance(episode, dict):
            continue
        candidate_cues.append(
            {
                "cue_id": f"exit-episode-{episode.get('episode_id', 'unknown')}",
                "cue_family": "language_episode",
                "source_ref": episode.get("source_ref"),
                "semantic_key": episode.get("semantic_key"),
                "weight": 0.7,
            }
        )
    for tag in relationship_memory.get("relationship_theme_tags", [])[:4]:
        candidate_cues.append(
            {
                "cue_id": f"relation-theme-{tag}",
                "cue_family": "relationship",
                "source_ref": "runtime/state/memory/relationship_memory.json",
                "semantic_key": str(tag),
                "weight": 0.55,
            }
        )
    for topic in web_dream_learning_state.get("topic_candidates", [])[:3]:
        candidate_cues.append(
            {
                "cue_id": f"web-topic-{_short_id(str(topic))}",
                "cue_family": "web_residue",
                "source_ref": web_dream_learning_state.get("web_dream_learning_state_ref"),
                "semantic_key": str(topic),
                "weight": 0.45,
            }
        )
    for ref in replay_cue_bundle.get("pain_regret_residue_refs", [])[:2]:
        candidate_cues.append(
            {
                "cue_id": f"pain-residue-{_short_id(str(ref))}",
                "cue_family": "pain_regret",
                "source_ref": str(ref),
                "weight": 0.6,
            }
        )

    used_clusters = {
        str(item.get("topic_cluster_id") or "")
        for item in topic_history.get("entries", [])
        if isinstance(item, dict)
    }
    suppressed: list[dict[str, Any]] = []
    selected: list[dict[str, Any]] = []
    for cue in sorted(candidate_cues, key=lambda item: -float(item.get("weight", 0))):
        cluster = str(cue.get("semantic_key") or cue.get("cue_id") or "")
        if cluster in used_clusters:
            suppressed.append(
                {
                    "cue_id": cue["cue_id"],
                    "reason": "topic_cluster_cooldown",
                }
            )
            continue
        selected.append(cue)
        if len(selected) >= 5:
            break

    return {
        "schema_version": "dream_cue_policy_state_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "DreamCuePolicy",
        "candidate_cues": candidate_cues,
        "selected_cues": selected,
        "suppressed_cues": suppressed,
        "selection_rationale": {
            "mode_bias": entry_vector.get("selected_offline_modes", []),
            "selected_count": len(selected),
            "suppressed_count": len(suppressed),
        },
        "cooldown_state": {
            "topic_history_entry_count": len(topic_history.get("entries", [])),
            "recent_cluster_ids": list(used_clusters)[:8],
        },
        "source_refs": _dedupe(
            [
                OFFLINE_DREAM_ENTRY_VECTOR_REF,
                "runtime/state/dream/exit_dream_consolidation_summary.json"
                if exit_dream_summary
                else "",
                web_dream_learning_state.get("web_dream_learning_state_ref", ""),
            ]
        ),
        "dream_cue_policy_state_ref": DREAM_CUE_POLICY_STATE_REF,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _short_id(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in value)
    return cleaned[:24] or "cue"


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result