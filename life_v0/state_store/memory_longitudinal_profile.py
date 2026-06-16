from __future__ import annotations

import json
from typing import Any

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/96_real_relationship_longitudinal_timeline.md",
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
    "docs/real—live0/06_relationship_and_commitment.md",
    "docs/real—live0/04_personality_self_identity.md",
]

MEMORY_LONGITUDINAL_PROFILE_REF = (
    "runtime/state/memory/memory_longitudinal_profile.json"
)


def build_memory_longitudinal_profile(
    *,
    run_id: str,
    generated_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": "memory_longitudinal_profile_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "profile_ref": MEMORY_LONGITUDINAL_PROFILE_REF,
        "turn_count": 0,
        "offline_cycle_count": 0,
        "live_trace_count": 0,
        "accessibility_curve": [],
        "relationship_depth_curve": [],
        "self_continuity_curve": [],
        "recall_strength_curve": [],
        "cross_modal_coverage_curve": [],
        "relation_subject_curves": {},
        "slow_variable_summary": {
            "relationship_depth_trend": "baseline",
            "self_continuity_trend": "baseline",
            "mean_accessibility": 0.0,
            "mean_recall_strength": 0.0,
        },
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_memory_longitudinal_profile_from_live_turn(
    *,
    profile: dict[str, Any] | None,
    run_id: str,
    generated_at: str,
    memory_trace_store: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    memory_phenomenology_profile: dict[str, Any] | None = None,
    cross_modal_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(profile or build_memory_longitudinal_profile(
        run_id=run_id,
        generated_at=generated_at,
    )))
    live_traces = [
        trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict)
        and trace.get("live_trace_origin") == "live_dialogue_turn"
        and trace.get("lifecycle_state") != "deprecated"
    ]
    updated["turn_count"] = int(updated.get("turn_count") or 0) + 1
    updated["live_trace_count"] = len(live_traces)
    updated["generated_at"] = generated_at

    accessibility = _mean_trace_field(live_traces, "accessibility_score", default=0.55)
    recall_strength = _mean_trace_field(live_traces, "replay_salience", default=0.5)
    relationship_depth = _relationship_depth_score(relationship_memory)
    self_continuity = _self_continuity_score(autobiographical_stack)
    cross_modal_coverage = int(
        (cross_modal_evidence or {}).get("evidence_modal_count")
        or (memory_phenomenology_profile or {}).get("cross_modal_evidence_ref_count")
        or 0
    )

    point = {
        "turn_index": updated["turn_count"],
        "generated_at": generated_at,
        "accessibility": round(accessibility, 3),
        "recall_strength": round(recall_strength, 3),
        "relationship_depth": round(relationship_depth, 3),
        "self_continuity": round(self_continuity, 3),
        "cross_modal_coverage": cross_modal_coverage,
        "recall_phenomenology": (memory_phenomenology_profile or {}).get(
            "recall_phenomenology"
        ),
    }
    updated["accessibility_curve"] = _append_curve(
        updated.get("accessibility_curve", []), point, key="accessibility"
    )
    updated["recall_strength_curve"] = _append_curve(
        updated.get("recall_strength_curve", []), point, key="recall_strength"
    )
    updated["relationship_depth_curve"] = _append_curve(
        updated.get("relationship_depth_curve", []), point, key="relationship_depth"
    )
    updated["self_continuity_curve"] = _append_curve(
        updated.get("self_continuity_curve", []), point, key="self_continuity"
    )
    updated["cross_modal_coverage_curve"] = _append_curve(
        updated.get("cross_modal_coverage_curve", []),
        point,
        key="cross_modal_coverage",
    )
    updated["relation_subject_curves"] = _update_relation_subject_curves(
        updated.get("relation_subject_curves", {}),
        memory_trace_store=memory_trace_store,
        turn_index=updated["turn_count"],
        generated_at=generated_at,
    )
    updated["slow_variable_summary"] = _slow_variable_summary(updated)
    updated["process_long_run_evidence"] = {
        "process_turn_count": updated["turn_count"],
        "live_trace_count": updated["live_trace_count"],
        "acceptance_boundary": "longitudinal_turn_counter_not_calendar_months",
        "last_live_turn_at": generated_at,
    }
    return updated


def project_memory_longitudinal_profile_from_offline_cycle(
    *,
    profile: dict[str, Any],
    generated_at: str,
    memory_consolidation_report: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(profile))
    updated["offline_cycle_count"] = int(updated.get("offline_cycle_count") or 0) + 1
    updated["generated_at"] = generated_at
    diff = (memory_consolidation_report or {}).get("consolidation_diff") or {}
    salience_updates = diff.get("trace_salience_updates") or []
    mean_replay_salience = 0.0
    if salience_updates:
        mean_replay_salience = sum(
            float(item.get("replay_salience") or 0)
            for item in salience_updates
            if isinstance(item, dict)
        ) / len(salience_updates)
    point = {
        "cycle_index": updated["offline_cycle_count"],
        "generated_at": generated_at,
        "salience_update_count": len(salience_updates),
        "mean_replay_salience": round(mean_replay_salience, 3),
        "relationship_depth": round(_relationship_depth_score(relationship_memory), 3),
        "self_continuity": round(_self_continuity_score(autobiographical_stack), 3),
        "dream_hypothesis_count": len(
            diff.get("dream_hypothesis_residue_diff") or []
        ),
    }
    offline_curve = list(updated.get("offline_consolidation_curve", []))
    offline_curve.append(point)
    updated["offline_consolidation_curve"] = offline_curve[-36:]
    updated["slow_variable_summary"] = _slow_variable_summary(updated)
    return updated


def _relationship_depth_score(relationship_memory: dict[str, Any] | None) -> float:
    memory = relationship_memory or {}
    depth = 0.35
    depth += min(0.25, len(_string_list(memory.get("deep_sediment_memory_refs"))) * 0.02)
    depth += min(0.2, len(_string_list(memory.get("we_memory_traces"))) * 0.03)
    depth += min(0.15, len(_string_list(memory.get("relation_subject_scopes"))) * 0.05)
    depth_profile = memory.get("relationship_memory_depth_profile") or {}
    if isinstance(depth_profile, dict):
        depth += min(
            0.2,
            float(depth_profile.get("longitudinal_depth_score") or 0) * 0.2,
        )
    return min(1.0, depth)


def _self_continuity_score(autobiographical_stack: dict[str, Any] | None) -> float:
    stack = autobiographical_stack or {}
    score = 0.3
    hierarchy = stack.get("memory_hierarchy") or {}
    if isinstance(hierarchy, dict):
        score += min(0.25, len(_string_list(hierarchy.get("specific_episode_refs"))) * 0.02)
        score += min(0.2, len(_string_list(hierarchy.get("general_event_threads"))) * 0.04)
    score += min(0.25, len(_string_list(stack.get("offline_consolidation_episode_refs"))) * 0.02)
    return min(1.0, score)


def _mean_trace_field(
    traces: list[dict[str, Any]],
    field: str,
    *,
    default: float,
) -> float:
    values = [
        float(trace.get(field))
        for trace in traces
        if isinstance(trace, dict) and trace.get(field) is not None
    ]
    if not values:
        return default
    return sum(values) / len(values)


def _append_curve(
    curve: list[Any],
    point: dict[str, Any],
    *,
    key: str,
) -> list[dict[str, Any]]:
    entries = [entry for entry in curve if isinstance(entry, dict)]
    entries.append(
        {
            "index": point.get("turn_index") or point.get("cycle_index"),
            "generated_at": point.get("generated_at"),
            "value": point.get(key),
            "recall_phenomenology": point.get("recall_phenomenology"),
        }
    )
    return entries[-48:]


def _update_relation_subject_curves(
    curves: dict[str, Any],
    *,
    memory_trace_store: dict[str, Any] | None,
    turn_index: int,
    generated_at: str,
) -> dict[str, Any]:
    updated = dict(curves) if isinstance(curves, dict) else {}
    counts: dict[str, int] = {}
    for trace in (memory_trace_store or {}).get("traces", []):
        if not isinstance(trace, dict):
            continue
        if trace.get("live_trace_origin") != "live_dialogue_turn":
            continue
        subject_id = str(trace.get("relation_subject_id") or "unscoped")
        counts[subject_id] = counts.get(subject_id, 0) + 1
    for subject_id, trace_count in counts.items():
        subject_curve = list(updated.get(subject_id, []))
        subject_curve.append(
            {
                "turn_index": turn_index,
                "generated_at": generated_at,
                "live_trace_count": trace_count,
            }
        )
        updated[subject_id] = subject_curve[-48:]
    return updated


def _slow_variable_summary(profile: dict[str, Any]) -> dict[str, Any]:
    accessibility_curve = profile.get("accessibility_curve") or []
    relationship_curve = profile.get("relationship_depth_curve") or []
    self_curve = profile.get("self_continuity_curve") or []
    recall_curve = profile.get("recall_strength_curve") or []
    return {
        "relationship_depth_trend": _curve_trend(relationship_curve),
        "self_continuity_trend": _curve_trend(self_curve),
        "accessibility_trend": _curve_trend(accessibility_curve),
        "recall_strength_trend": _curve_trend(recall_curve),
        "mean_accessibility": _curve_mean(accessibility_curve),
        "mean_recall_strength": _curve_mean(recall_curve),
        "mean_relationship_depth": _curve_mean(relationship_curve),
        "mean_self_continuity": _curve_mean(self_curve),
        "turn_count": profile.get("turn_count"),
        "offline_cycle_count": profile.get("offline_cycle_count"),
    }


def _curve_trend(curve: list[Any]) -> str:
    values = [
        float(entry.get("value"))
        for entry in curve
        if isinstance(entry, dict) and entry.get("value") is not None
    ]
    if len(values) < 2:
        return "baseline"
    delta = values[-1] - values[0]
    if delta > 0.05:
        return "rising"
    if delta < -0.05:
        return "falling"
    return "stable"


def _curve_mean(curve: list[Any]) -> float:
    values = [
        float(entry.get("value"))
        for entry in curve
        if isinstance(entry, dict) and entry.get("value") is not None
    ]
    if not values:
        return 0.0
    return round(sum(values) / len(values), 3)


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [str(value)] if value else []