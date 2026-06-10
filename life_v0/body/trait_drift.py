from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/40_self_relationship_model_audit_protocol.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_trait_drift_monitor(
    *,
    run_id: str,
    generated_at: str,
    episode: dict[str, Any],
    life_state: dict[str, Any],
) -> dict[str, Any]:
    old_self_anchors = list(life_state.get("self_model", {}).get("old_self_anchors", []))
    return {
        "schema_version": "trait_drift_monitor_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "trait_drift_id": f"trait-drift-{run_id}",
        "slow_variable_targets": [
            "trust_persistence",
            "dialogue_warmth",
            "repair_seriousness",
        ],
        "drift_direction": "guarded_stability",
        "required_anchor_refs": old_self_anchors or ["runtime/state/life_state.json#self_model.old_self_anchors"],
        "blocked_update_refs": [],
        "archive_requirement": "required_before_trait_commit",
        "episode_ref": "runtime/state/body/affective_episode.json",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_trait_drift_monitor_from_self_model(
    *,
    run_id: str,
    generated_at: str,
    self_model_state: dict[str, Any],
    relationship_graph: dict[str, Any],
    trigger_ref: str,
    previous_monitor: dict[str, Any] | None = None,
    source_doc_refs: list[str] | None = None,
) -> dict[str, Any]:
    previous_monitor = previous_monitor or {}
    slow_variable_summary = _slow_variable_summary(self_model_state)
    update_mode_summary = _slow_variable_update_mode_summary(slow_variable_summary)
    relationship_subject = _first_subject(relationship_graph)
    background_inertia_weights = [
        payload["background_inertia_weight"]
        for payload in slow_variable_summary.values()
        if isinstance(payload.get("background_inertia_weight"), (int, float))
    ]
    evidence_refs = _dedupe(
        [trigger_ref, "runtime/state/self/self_model.json"]
        + _string_list(relationship_subject.get("relationship_stage_evidence_refs"))
        + _slow_variable_evidence_refs(slow_variable_summary)
    )
    return {
        "schema_version": "trait_drift_monitor_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "trait_drift_id": f"trait-drift-{run_id}",
        "revision": _int_or_zero(previous_monitor.get("revision")) + 1,
        "slow_variable_targets": list(slow_variable_summary.keys())
        or [
            "trust_persistence",
            "dialogue_warmth",
            "repair_seriousness",
            "boundary_respect",
            "continuity_drive",
        ],
        "slow_variable_summary": slow_variable_summary,
        "slow_variable_update_mode_summary": update_mode_summary,
        "background_history_recalibration_names": _names_for_update_modes(
            update_mode_summary,
            {"background_history_recalibration"},
        ),
        "background_history_stabilized_names": _names_for_update_modes(
            update_mode_summary,
            {"background_history_stabilized"},
        ),
        "relationship_stage": relationship_subject.get("relationship_stage"),
        "relationship_stage_reason": relationship_subject.get("relationship_stage_reason"),
        "background_inertia_active": bool(background_inertia_weights),
        "max_background_inertia_weight": (
            round(max(background_inertia_weights), 3)
            if background_inertia_weights
            else 0.0
        ),
        "drift_direction": _drift_direction(slow_variable_summary),
        "required_anchor_refs": _required_anchor_refs(self_model_state),
        "drift_observation_refs": evidence_refs,
        "blocked_update_refs": [],
        "archive_requirement": "required_before_trait_commit",
        "episode_ref": trigger_ref,
        "source_doc_refs": _dedupe((source_doc_refs or []) + SOURCE_DOC_REFS),
    }


def check_trait_drift_monitor(trait_drift: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if trait_drift.get("schema_version") != "trait_drift_monitor_v0":
        reasons.append("trait_drift_gate schema mismatch")
    for field in [
        "trait_drift_id",
        "slow_variable_targets",
        "drift_direction",
        "required_anchor_refs",
        "archive_requirement",
    ]:
        if not trait_drift.get(field):
            reasons.append(f"trait_drift_gate missing {field}")
    return reasons


def _slow_variable_summary(self_model_state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    variables = self_model_state.get("trait_slow_variables", {})
    if not isinstance(variables, dict):
        return {}
    summary: dict[str, dict[str, Any]] = {}
    for name, payload in variables.items():
        if not isinstance(payload, dict):
            continue
        summary[str(name)] = {
            key: payload[key]
            for key in [
                "value",
                "trend",
                "update_count",
                "last_relationship_stage",
                "background_resume_value",
                "background_inertia_weight",
                "slow_variable_update_mode",
                "background_trait_convergence_history_focus",
                "background_trait_convergence_history_role",
                "background_trait_convergence_history_latest_band",
                "background_trait_convergence_history_trend_state",
                "evidence_refs",
            ]
            if key in payload
        }
    return summary


def _slow_variable_evidence_refs(
    slow_variable_summary: dict[str, dict[str, Any]],
) -> list[str]:
    refs: list[str] = []
    for payload in slow_variable_summary.values():
        refs.extend(_string_list(payload.get("evidence_refs")))
    return refs


def _slow_variable_update_mode_summary(
    slow_variable_summary: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    summary: dict[str, list[str]] = {}
    for name, payload in slow_variable_summary.items():
        mode = payload.get("slow_variable_update_mode")
        if not isinstance(mode, str) or not mode:
            continue
        summary.setdefault(mode, []).append(name)
    return summary


def _names_for_update_modes(
    update_mode_summary: dict[str, list[str]],
    modes: set[str],
) -> list[str]:
    names: list[str] = []
    for mode in modes:
        names.extend(update_mode_summary.get(mode, []))
    return _dedupe(names)


def _first_subject(relationship_graph: dict[str, Any]) -> dict[str, Any]:
    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        return subjects[0]
    return {}


def _drift_direction(slow_variable_summary: dict[str, dict[str, Any]]) -> str:
    update_modes = {
        str(payload.get("slow_variable_update_mode"))
        for payload in slow_variable_summary.values()
        if payload.get("slow_variable_update_mode")
    }
    if "background_history_recalibration" in update_modes:
        return "background_history_recalibration_needed"
    if "background_history_stability_hold" in update_modes:
        return "background_history_stability_hold"
    if "background_history_stabilized" in update_modes:
        return "background_history_stabilized"
    trends = {
        str(payload.get("trend"))
        for payload in slow_variable_summary.values()
        if payload.get("trend")
    }
    if any(
        payload.get("background_inertia_weight")
        for payload in slow_variable_summary.values()
    ):
        return "background_inertia_stabilized"
    if "rising" in trends:
        return "relationship_growth_rising"
    if "falling" in trends:
        return "guarded_stability_repair_needed"
    return "guarded_stability"


def _required_anchor_refs(self_model_state: dict[str, Any]) -> list[str]:
    refs = (
        _string_list(self_model_state.get("old_self_anchor_refs"))
        + _string_list(self_model_state.get("growth_window_refs"))
        + _string_list(self_model_state.get("trait_drift_seed_refs"))
    )
    return _dedupe(refs) or ["runtime/state/life_state.json#self_model.old_self_anchors"]


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _dedupe(items: list[Any]) -> list[str]:
    result: list[str] = []
    for item in items:
        if isinstance(item, str) and item and item not in result:
            result.append(item)
    return result
