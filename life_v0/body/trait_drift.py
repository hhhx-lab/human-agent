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
    growth_self_modification_profile = _growth_self_modification_profile(
        self_model_state=self_model_state,
        slow_variable_summary=slow_variable_summary,
    )
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
        "growth_self_modification_observation_profile": growth_self_modification_profile,
        "growth_self_modification_trait_names": list(
            growth_self_modification_profile.get("trait_names", [])
        ),
        "growth_self_modification_ref_count": growth_self_modification_profile.get(
            "growth_ref_count",
            0,
        ),
        "growth_self_modification_pressure_level": growth_self_modification_profile.get(
            "pressure_level"
        ),
        "growth_self_modification_boundary": growth_self_modification_profile.get(
            "boundary"
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
                "growth_self_modification_update_mode",
                "background_growth_self_modification_pressure_level",
                "background_growth_self_modification_attention_target",
                "background_growth_self_modification_waiting_posture",
                "background_growth_self_modification_boundary",
                "background_growth_self_modification_active_domain_count",
                "background_growth_self_modification_growth_pressure_count",
                "background_growth_self_modification_patch_candidate_count",
                "background_growth_self_modification_archive_receipt_count",
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
    if "growth_self_modification_rehearsal_hold" in {
        str(payload.get("growth_self_modification_update_mode"))
        for payload in slow_variable_summary.values()
        if payload.get("growth_self_modification_update_mode")
    }:
        return "growth_self_modification_reconsolidation_observed"
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


def _growth_self_modification_profile(
    *,
    self_model_state: dict[str, Any],
    slow_variable_summary: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    trait_names: list[str] = []
    growth_refs: list[str] = []
    pressure_levels: list[str] = []
    attention_targets: list[str] = []
    waiting_postures: list[str] = []
    boundaries: list[str] = []
    active_domain_count = 0
    growth_pressure_count = 0
    patch_candidate_count = 0
    archive_receipt_count = 0
    for name, payload in slow_variable_summary.items():
        if not payload.get("growth_self_modification_update_mode"):
            continue
        trait_names.append(name)
        growth_refs.extend(_string_list(payload.get("evidence_refs")))
        pressure_levels.extend(
            _string_list(payload.get("background_growth_self_modification_pressure_level"))
        )
        attention_targets.extend(
            _string_list(payload.get("background_growth_self_modification_attention_target"))
        )
        waiting_postures.extend(
            _string_list(payload.get("background_growth_self_modification_waiting_posture"))
        )
        boundaries.extend(
            _string_list(payload.get("background_growth_self_modification_boundary"))
        )
        active_domain_count = max(
            active_domain_count,
            _int_or_zero(
                payload.get("background_growth_self_modification_active_domain_count")
            ),
        )
        growth_pressure_count = max(
            growth_pressure_count,
            _int_or_zero(
                payload.get("background_growth_self_modification_growth_pressure_count")
            ),
        )
        patch_candidate_count = max(
            patch_candidate_count,
            _int_or_zero(
                payload.get("background_growth_self_modification_patch_candidate_count")
            ),
        )
        archive_receipt_count = max(
            archive_receipt_count,
            _int_or_zero(
                payload.get("background_growth_self_modification_archive_receipt_count")
            ),
        )
    growth_refs = _dedupe(
        growth_refs + _string_list(self_model_state.get("growth_window_refs"))
    )
    return {
        "schema_version": "growth_self_modification_trait_observation_v0",
        "trait_names": _dedupe(trait_names),
        "trait_count": len(_dedupe(trait_names)),
        "growth_ref_count": len(growth_refs),
        "growth_refs": growth_refs,
        "pressure_level": _first(pressure_levels),
        "attention_target": _first(attention_targets),
        "waiting_posture": _first(waiting_postures),
        "boundary": _first(boundaries),
        "active_domain_count": active_domain_count,
        "growth_pressure_count": growth_pressure_count,
        "patch_candidate_count": patch_candidate_count,
        "archive_receipt_count": archive_receipt_count,
        "observation_boundary": "structured_trait_growth_evidence_not_spoken_language",
    }


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


def _first(items: list[str]) -> str | None:
    deduped = _dedupe(items)
    return deduped[0] if deduped else None


def _dedupe(items: list[Any]) -> list[str]:
    result: list[str] = []
    for item in items:
        if isinstance(item, str) and item and item not in result:
            result.append(item)
    return result
