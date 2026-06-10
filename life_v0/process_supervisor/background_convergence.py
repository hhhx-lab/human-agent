from __future__ import annotations

from typing import Any


BACKGROUND_CONVERGENCE_SUMMARY_REF = (
    "runtime/state/terminal/background_convergence_summary.json"
)
RELATIONSHIP_SUBJECT_REF = "runtime/state/relationship/relationship_subject_graph.json#subjects[0]"
SELF_MODEL_REF = "runtime/state/self/self_model.json"
TRAIT_DRIFT_MONITOR_REF = "runtime/state/body/trait_drift_monitor.json"


def build_background_convergence_summary(
    *,
    run_id: str,
    generated_at: str,
    background_continuity_profile: dict[str, Any] | None,
    relationship_graph: dict[str, Any],
    self_model_state: dict[str, Any],
    trait_drift_monitor: dict[str, Any] | None = None,
    source_doc_refs: list[str] | None = None,
) -> dict[str, Any]:
    background_continuity_profile = background_continuity_profile or {}
    if not _has_background_profile(background_continuity_profile):
        return {}

    subject = _first_subject(relationship_graph)
    current_stage = str(subject.get("relationship_stage", "") or "")
    background_stage = str(
        background_continuity_profile.get("background_relationship_stage", "") or ""
    )
    stage_continuity = _stage_continuity(
        current_stage=current_stage,
        background_stage=background_stage,
    )
    trait_summary = _trait_convergence_summary(
        self_model_state=self_model_state,
        background_continuity_profile=background_continuity_profile,
        trait_drift_monitor=trait_drift_monitor or {},
    )
    trait_drift_update_mode_summary = _dict_of_string_lists(
        (trait_drift_monitor or {}).get("slow_variable_update_mode_summary")
    )
    trait_drift_recalibration_names = (
        _string_list(
            (trait_drift_monitor or {}).get("background_history_recalibration_names")
        )
        or trait_drift_update_mode_summary.get("background_history_recalibration", [])
    )
    trait_drift_stabilized_names = (
        _string_list(
            (trait_drift_monitor or {}).get("background_history_stabilized_names")
        )
        or trait_drift_update_mode_summary.get("background_history_stabilized", [])
    )
    trait_drift_recalibration_active = _trait_drift_recalibration_active(
        trait_drift_monitor=trait_drift_monitor or {},
        recalibration_names=trait_drift_recalibration_names,
    )
    deltas = [
        abs(payload["delta_from_background"])
        for payload in trait_summary.values()
        if isinstance(payload.get("delta_from_background"), (int, float))
    ]
    inertia_weights = [
        payload["background_inertia_weight"]
        for payload in trait_summary.values()
        if isinstance(payload.get("background_inertia_weight"), (int, float))
    ]
    max_delta = max(deltas, default=0.0)
    average_delta = sum(deltas) / len(deltas) if deltas else 0.0
    background_generation = _int_or_zero(
        background_continuity_profile.get("background_carryover_generation")
    )
    convergence_state = _convergence_state(
        stage_continuity=stage_continuity,
        max_delta=max_delta,
        average_delta=average_delta,
        trait_drift_recalibration_active=trait_drift_recalibration_active,
    )
    pressure_level = _pressure_level(
        convergence_state=convergence_state,
        background_generation=background_generation,
        max_delta=max_delta,
        average_delta=average_delta,
        inertia_weights=inertia_weights,
        trait_drift_recalibration_active=trait_drift_recalibration_active,
    )
    attention_target = _attention_target(
        convergence_state=convergence_state,
        pressure_level=pressure_level,
        stage_continuity=stage_continuity,
        trait_summary=trait_summary,
        trait_drift_recalibration_active=trait_drift_recalibration_active,
    )
    evidence_refs = _dedupe(
        [
            RELATIONSHIP_SUBJECT_REF if subject else "",
            SELF_MODEL_REF if self_model_state else "",
            TRAIT_DRIFT_MONITOR_REF if trait_drift_monitor else "",
        ]
        + _string_list(background_continuity_profile.get("background_continuity_ref_set"))
        + _string_list(
            background_continuity_profile.get("background_carryover_source_ref_set")
        )
        + _string_list(
            background_continuity_profile.get(
                "background_relationship_stage_evidence_refs"
            )
        )
    )

    return {
        "schema_version": "background_convergence_summary_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "convergence_id": f"background-convergence-{run_id}",
        "convergence_mode": "cross_process_relationship_trait_stability",
        "background_carryover_generation": background_generation,
        "background_carryover_parent_run_id": background_continuity_profile.get(
            "background_carryover_parent_run_id"
        ),
        "background_relationship_stage": background_stage,
        "current_relationship_stage": current_stage,
        "relationship_stage_continuity": stage_continuity,
        "convergence_state": convergence_state,
        "convergence_pressure_level": pressure_level,
        "convergence_attention_target": attention_target,
        "trait_convergence_score": round(max(0.0, 1.0 - average_delta), 3),
        "max_trait_delta_from_background": round(max_delta, 3),
        "average_trait_delta_from_background": round(average_delta, 3),
        "trait_convergence_summary": trait_summary,
        "trait_drift_update_mode_summary": trait_drift_update_mode_summary,
        "trait_drift_background_history_recalibration_names": _dedupe(
            trait_drift_recalibration_names
        ),
        "trait_drift_background_history_stabilized_names": _dedupe(
            trait_drift_stabilized_names
        ),
        "background_continuity_ref_set": _string_list(
            background_continuity_profile.get("background_continuity_ref_set")
        ),
        "background_carryover_source_ref_set": _string_list(
            background_continuity_profile.get("background_carryover_source_ref_set")
        ),
        "relationship_subject_ref": RELATIONSHIP_SUBJECT_REF if subject else None,
        "self_model_ref": SELF_MODEL_REF if self_model_state else None,
        "trait_drift_monitor_ref": TRAIT_DRIFT_MONITOR_REF if trait_drift_monitor else None,
        "evidence_refs": evidence_refs,
        "source_doc_refs": _dedupe(source_doc_refs or []),
    }


def _has_background_profile(profile: dict[str, Any]) -> bool:
    return any(
        [
            profile.get("background_continuity_mode"),
            profile.get("background_relationship_stage"),
            profile.get("background_trait_slow_variable_summary"),
            profile.get("background_resume_summary"),
            profile.get("background_continuity_ref_set"),
        ]
    )


def _first_subject(relationship_graph: dict[str, Any]) -> dict[str, Any]:
    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        return subjects[0]
    return {}


def _stage_continuity(*, current_stage: str, background_stage: str) -> str:
    if not background_stage:
        return "no_background_stage"
    if not current_stage:
        return "background_stage_waiting_for_current_subject"
    if current_stage == background_stage:
        return "same_stage_preserved"
    if current_stage == "background_continuity_waiting":
        return "background_lineage_integrated_before_dialogue"
    return "stage_shift_requires_trait_recalibration"


def _trait_convergence_summary(
    *,
    self_model_state: dict[str, Any],
    background_continuity_profile: dict[str, Any],
    trait_drift_monitor: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    current_variables = self_model_state.get("trait_slow_variables", {})
    if not isinstance(current_variables, dict):
        current_variables = {}
    background_values = _background_trait_values(background_continuity_profile)
    trait_drift_update_modes = _trait_drift_update_modes_by_name(trait_drift_monitor)
    names = sorted(set(current_variables.keys()) | set(background_values.keys()))
    summary: dict[str, dict[str, Any]] = {}
    for name in names:
        current_payload = current_variables.get(name, {})
        current_value = _value_from_payload(current_payload)
        background_value = _background_value_for_name(
            name=name,
            current_payload=current_payload,
            background_values=background_values,
        )
        payload: dict[str, Any] = {}
        if current_value is not None:
            payload["current_value"] = round(current_value, 3)
        if background_value is not None:
            payload["background_value"] = round(background_value, 3)
        if current_value is not None and background_value is not None:
            delta = current_value - background_value
            payload["delta_from_background"] = round(delta, 3)
            payload["convergence_band"] = _convergence_band(abs(delta))
        else:
            payload["convergence_band"] = "missing_current_or_background_value"
        if isinstance(current_payload, dict):
            for key in [
                "trend",
                "update_count",
                "last_relationship_stage",
                "background_inertia_weight",
            ]:
                if key in current_payload:
                    payload[key] = current_payload[key]
        trait_drift_update_mode = trait_drift_update_modes.get(str(name))
        if trait_drift_update_mode:
            payload["trait_drift_update_mode"] = trait_drift_update_mode
        summary[str(name)] = payload
    return summary


def _background_trait_values(
    background_continuity_profile: dict[str, Any],
) -> dict[str, float]:
    summary = background_continuity_profile.get(
        "background_trait_slow_variable_summary",
        {},
    )
    if not isinstance(summary, dict):
        return {}
    values: dict[str, float] = {}
    for name, payload in summary.items():
        value = _value_from_payload(payload)
        if value is not None:
            values[str(name)] = value
    return values


def _background_value_for_name(
    *,
    name: str,
    current_payload: Any,
    background_values: dict[str, float],
) -> float | None:
    if isinstance(current_payload, dict):
        resume_value = current_payload.get("background_resume_value")
        if isinstance(resume_value, (int, float)):
            return float(resume_value)
    return background_values.get(name)


def _value_from_payload(payload: Any) -> float | None:
    if isinstance(payload, dict):
        value = payload.get("value")
    else:
        value = payload
    if isinstance(value, (int, float)):
        return max(0.0, min(1.0, float(value)))
    return None


def _convergence_band(delta: float) -> str:
    if delta <= 0.08:
        return "stabilized"
    if delta <= 0.18:
        return "integrating"
    return "recalibrating"


def _convergence_state(
    *,
    stage_continuity: str,
    max_delta: float,
    average_delta: float,
    trait_drift_recalibration_active: bool,
) -> str:
    if trait_drift_recalibration_active:
        return "recalibrating_cross_process_continuity"
    if stage_continuity in {
        "stage_shift_requires_trait_recalibration",
        "background_stage_waiting_for_current_subject",
    }:
        return "recalibrating_cross_process_continuity"
    if max_delta > 0.18:
        return "recalibrating_cross_process_continuity"
    if average_delta > 0.08:
        return "integrating_cross_process_continuity"
    return "stabilized_cross_process_continuity"


def _pressure_level(
    *,
    convergence_state: str,
    background_generation: int,
    max_delta: float,
    average_delta: float,
    inertia_weights: list[Any],
    trait_drift_recalibration_active: bool,
) -> str:
    if trait_drift_recalibration_active:
        return "elevated"
    if convergence_state == "recalibrating_cross_process_continuity":
        return "elevated"
    if max_delta > 0.18:
        return "elevated"
    if average_delta > 0.08 or background_generation >= 2:
        return "present"
    if any(float(weight) >= 0.55 for weight in inertia_weights):
        return "present"
    return "light"


def _attention_target(
    *,
    convergence_state: str,
    pressure_level: str,
    stage_continuity: str,
    trait_summary: dict[str, dict[str, Any]],
    trait_drift_recalibration_active: bool,
) -> str:
    if trait_drift_recalibration_active:
        return "trait_drift_history_recalibration"
    if stage_continuity in {
        "stage_shift_requires_trait_recalibration",
        "background_stage_waiting_for_current_subject",
        "background_lineage_integrated_before_dialogue",
    }:
        return "relationship_stage_convergence"
    if convergence_state == "recalibrating_cross_process_continuity":
        return "trait_slow_variable_recalibration"
    if pressure_level in {"present", "elevated"}:
        return "trait_slow_variable_convergence"
    if trait_summary:
        return "background_convergence_summary"
    return "background_continuity_maintenance"


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


def _dict_of_string_lists(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): _string_list(item)
        for key, item in value.items()
        if _string_list(item)
    }


def _trait_drift_update_modes_by_name(
    trait_drift_monitor: dict[str, Any],
) -> dict[str, str]:
    update_mode_summary = _dict_of_string_lists(
        trait_drift_monitor.get("slow_variable_update_mode_summary")
    )
    modes_by_name: dict[str, str] = {}
    for mode, names in update_mode_summary.items():
        for name in names:
            modes_by_name.setdefault(name, mode)
    return modes_by_name


def _trait_drift_recalibration_active(
    *,
    trait_drift_monitor: dict[str, Any],
    recalibration_names: list[str],
) -> bool:
    return (
        bool(recalibration_names)
        or trait_drift_monitor.get("drift_direction")
        == "background_history_recalibration_needed"
    )


def _dedupe(items: list[Any]) -> list[str]:
    result: list[str] = []
    for item in items:
        if isinstance(item, str) and item and item not in result:
            result.append(item)
    return result
