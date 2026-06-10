from __future__ import annotations

from typing import Any


BACKGROUND_CONVERGENCE_HISTORY_REF = (
    "runtime/state/terminal/background_convergence_history.json"
)
MAX_BACKGROUND_CONVERGENCE_HISTORY_SAMPLES = 8


def build_background_convergence_history(
    *,
    run_id: str,
    generated_at: str,
    background_convergence_summary: dict[str, Any] | None,
    background_continuity_profile: dict[str, Any] | None,
    source_doc_refs: list[str] | None = None,
) -> dict[str, Any]:
    summary = background_convergence_summary or {}
    profile = background_continuity_profile or {}
    if not summary:
        return {}

    previous_history = _previous_history(profile)
    previous_samples = _sample_list(previous_history.get("convergence_samples", []))
    current_sample = _current_sample(
        run_id=run_id,
        generated_at=generated_at,
        background_convergence_summary=summary,
    )
    samples = (previous_samples + [current_sample])[
        -MAX_BACKGROUND_CONVERGENCE_HISTORY_SAMPLES:
    ]
    state_sequence = [
        sample["convergence_state"]
        for sample in samples
        if sample.get("convergence_state")
    ]
    pressure_sequence = [
        sample["convergence_pressure_level"]
        for sample in samples
        if sample.get("convergence_pressure_level")
    ]
    stage_sequence = [
        sample["relationship_stage_continuity"]
        for sample in samples
        if sample.get("relationship_stage_continuity")
    ]
    trait_scores = [
        sample["trait_convergence_score"]
        for sample in samples
        if isinstance(sample.get("trait_convergence_score"), (int, float))
    ]
    trait_history_profile = _trait_history_profile(samples)
    unstable_trait_names = _trait_names_by_stability(
        trait_history_profile=trait_history_profile,
        stable=False,
    )
    stable_trait_names = _trait_names_by_stability(
        trait_history_profile=trait_history_profile,
        stable=True,
    )
    latest_state = current_sample.get("convergence_state")
    latest_pressure = current_sample.get("convergence_pressure_level")
    trait_drift_update_mode_summary = _dict_of_string_lists(
        current_sample.get("trait_drift_update_mode_summary")
    )
    trait_drift_recalibration_names = (
        _string_list(
            current_sample.get("trait_drift_background_history_recalibration_names")
        )
        or trait_drift_update_mode_summary.get("background_history_recalibration", [])
    )
    trait_drift_stabilized_names = (
        _string_list(current_sample.get("trait_drift_background_history_stabilized_names"))
        or trait_drift_update_mode_summary.get("background_history_stabilized", [])
    )

    return {
        "schema_version": "background_convergence_history_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "history_id": f"background-convergence-history-{run_id}",
        "history_window_size": len(samples),
        "max_history_window_size": MAX_BACKGROUND_CONVERGENCE_HISTORY_SAMPLES,
        "latest_convergence_state": latest_state,
        "latest_convergence_pressure_level": latest_pressure,
        "latest_convergence_attention_target": current_sample.get(
            "convergence_attention_target"
        ),
        "latest_relationship_stage_continuity": current_sample.get(
            "relationship_stage_continuity"
        ),
        "latest_trait_convergence_score": current_sample.get(
            "trait_convergence_score"
        ),
        "dominant_convergence_state": _mode(state_sequence),
        "dominant_convergence_pressure_level": _dominant_pressure(pressure_sequence),
        "relationship_stage_continuity_sequence": stage_sequence,
        "convergence_state_sequence": state_sequence,
        "convergence_pressure_sequence": pressure_sequence,
        "trait_convergence_score_average": _rounded_average(trait_scores),
        "trait_convergence_score_min": min(trait_scores) if trait_scores else None,
        "trait_convergence_history_profile": trait_history_profile,
        "trait_convergence_unstable_names": unstable_trait_names,
        "trait_convergence_stable_names": stable_trait_names,
        "trait_convergence_history_focus": _trait_history_focus(
            trait_history_profile=trait_history_profile,
            unstable_trait_names=unstable_trait_names,
        ),
        "trait_drift_update_mode_summary": trait_drift_update_mode_summary,
        "trait_drift_background_history_recalibration_names": _dedupe(
            trait_drift_recalibration_names
        ),
        "trait_drift_background_history_stabilized_names": _dedupe(
            trait_drift_stabilized_names
        ),
        "trend_state": _trend_state(samples),
        "convergence_samples": samples,
        "background_convergence_summary_ref": (
            "runtime/state/terminal/background_convergence_summary.json"
        ),
        "previous_background_convergence_history_ref": (
            profile.get("background_convergence_history_ref")
            or profile.get("previous_background_convergence_history_ref")
            or profile.get("background_previous_convergence_history_ref")
            or previous_history.get("background_convergence_history_ref")
            or previous_history.get("previous_background_convergence_history_ref")
        ),
        "source_doc_refs": _dedupe(source_doc_refs or []),
    }


def _previous_history(profile: dict[str, Any]) -> dict[str, Any]:
    history = profile.get("background_convergence_history")
    if isinstance(history, dict):
        return history
    history = profile.get("background_convergence_history_summary")
    if isinstance(history, dict):
        return history
    return {}


def _sample_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _current_sample(
    *,
    run_id: str,
    generated_at: str,
    background_convergence_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "generated_at": generated_at,
        "background_carryover_generation": _int_or_zero(
            background_convergence_summary.get("background_carryover_generation")
        ),
        "convergence_state": background_convergence_summary.get("convergence_state"),
        "convergence_pressure_level": background_convergence_summary.get(
            "convergence_pressure_level"
        ),
        "convergence_attention_target": background_convergence_summary.get(
            "convergence_attention_target"
        ),
        "relationship_stage_continuity": background_convergence_summary.get(
            "relationship_stage_continuity"
        ),
        "trait_convergence_score": background_convergence_summary.get(
            "trait_convergence_score"
        ),
        "max_trait_delta_from_background": background_convergence_summary.get(
            "max_trait_delta_from_background"
        ),
        "average_trait_delta_from_background": background_convergence_summary.get(
            "average_trait_delta_from_background"
        ),
        "trait_convergence_summary": _trait_summary(
            background_convergence_summary.get("trait_convergence_summary")
        ),
        "trait_drift_update_mode_summary": _dict_of_string_lists(
            background_convergence_summary.get("trait_drift_update_mode_summary")
        ),
        "trait_drift_background_history_recalibration_names": _string_list(
            background_convergence_summary.get(
                "trait_drift_background_history_recalibration_names"
            )
        ),
        "trait_drift_background_history_stabilized_names": _string_list(
            background_convergence_summary.get(
                "trait_drift_background_history_stabilized_names"
            )
        ),
    }


def _mode(values: list[str]) -> str | None:
    if not values:
        return None
    return sorted(set(values), key=lambda value: (-values.count(value), value))[0]


def _dominant_pressure(values: list[str]) -> str | None:
    if not values:
        return None
    rank = {"light": 1, "present": 2, "elevated": 3}
    return max(values, key=lambda value: rank.get(value, 0))


def _rounded_average(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 3)


def _trait_history_profile(samples: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    names = sorted(
        {
            str(name)
            for sample in samples
            for name in _trait_summary(sample.get("trait_convergence_summary")).keys()
        }
    )
    profile: dict[str, dict[str, Any]] = {}
    for name in names:
        entries = [
            _trait_entry(sample=sample, name=name)
            for sample in samples
            if name in _trait_summary(sample.get("trait_convergence_summary"))
        ]
        band_sequence = [
            str(entry["convergence_band"])
            for entry in entries
            if entry.get("convergence_band")
        ]
        update_mode_sequence = [
            str(entry["trait_drift_update_mode"])
            for entry in entries
            if entry.get("trait_drift_update_mode")
        ]
        deltas = [
            abs(float(entry["delta_from_background"]))
            for entry in entries
            if isinstance(entry.get("delta_from_background"), (int, float))
        ]
        latest_entry = entries[-1] if entries else {}
        profile[name] = {
            "sample_count": len(entries),
            "band_sequence": band_sequence,
            "latest_band": latest_entry.get("convergence_band"),
            "dominant_band": _mode(band_sequence),
            "trend_state": _trait_trend_state(band_sequence),
            "latest_delta_from_background": latest_entry.get(
                "delta_from_background"
            ),
            "max_abs_delta_from_background": (
                round(max(deltas), 3) if deltas else None
            ),
            "average_abs_delta_from_background": _rounded_average(deltas),
            "latest_current_value": latest_entry.get("current_value"),
            "latest_background_value": latest_entry.get("background_value"),
            "trait_drift_update_mode_sequence": update_mode_sequence,
            "latest_trait_drift_update_mode": latest_entry.get(
                "trait_drift_update_mode"
            ),
            "dominant_trait_drift_update_mode": _mode(update_mode_sequence),
            "last_seen_run_id": latest_entry.get("run_id"),
        }
    return profile


def _trait_entry(*, sample: dict[str, Any], name: str) -> dict[str, Any]:
    summary = _trait_summary(sample.get("trait_convergence_summary"))
    payload = summary.get(name, {})
    if not isinstance(payload, dict):
        payload = {}
    return {
        "run_id": sample.get("run_id"),
        "convergence_band": payload.get("convergence_band"),
        "delta_from_background": payload.get("delta_from_background"),
        "current_value": payload.get("current_value"),
        "background_value": payload.get("background_value"),
        "trait_drift_update_mode": payload.get("trait_drift_update_mode"),
    }


def _trait_summary(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    return {str(name): payload for name, payload in value.items()}


def _trait_names_by_stability(
    *,
    trait_history_profile: dict[str, dict[str, Any]],
    stable: bool,
) -> list[str]:
    names: list[str] = []
    for name, payload in trait_history_profile.items():
        latest_band = payload.get("latest_band")
        trend_state = payload.get("trend_state")
        is_stable = latest_band == "stabilized" and trend_state in {
            "stable_trait_convergence",
            "trait_convergence_observed",
        }
        if is_stable == stable:
            names.append(name)
    return sorted(names)


def _trait_history_focus(
    *,
    trait_history_profile: dict[str, dict[str, Any]],
    unstable_trait_names: list[str],
) -> str | None:
    if not trait_history_profile:
        return None
    if any(
        trait_history_profile[name].get("latest_band") == "recalibrating"
        for name in unstable_trait_names
    ):
        return "trait_recalibration_required"
    if unstable_trait_names:
        return "trait_stability_hold"
    return "trait_convergence_stable"


def _trait_trend_state(band_sequence: list[str]) -> str:
    recent = band_sequence[-3:]
    if not recent:
        return "no_trait_convergence_history"
    if recent[-1] == "recalibrating":
        return "recent_trait_recalibration"
    if len(recent) >= 2 and recent[-2:] == ["stabilized", "stabilized"]:
        return "stable_trait_convergence"
    if recent[-1] == "integrating":
        return "integrating_trait_convergence"
    return "trait_convergence_observed"


def _trend_state(samples: list[dict[str, Any]]) -> str:
    states = [
        sample.get("convergence_state")
        for sample in samples[-3:]
        if sample.get("convergence_state")
    ]
    pressures = [
        sample.get("convergence_pressure_level")
        for sample in samples[-3:]
        if sample.get("convergence_pressure_level")
    ]
    if not states:
        return "no_convergence_history"
    if any(state == "recalibrating_cross_process_continuity" for state in states):
        return "recent_recalibration_pressure"
    if len(states) >= 2 and len(set(states)) == 1 and states[-1] == (
        "stabilized_cross_process_continuity"
    ):
        return "stable_cross_wake_convergence"
    if "elevated" in pressures:
        return "elevated_pressure_watch"
    if states[-1] == "integrating_cross_process_continuity":
        return "integrating_cross_wake_convergence"
    return "cross_wake_convergence_observed"


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


def _dedupe(items: list[Any]) -> list[str]:
    result: list[str] = []
    for item in items:
        if isinstance(item, str) and item and item not in result:
            result.append(item)
    return result
