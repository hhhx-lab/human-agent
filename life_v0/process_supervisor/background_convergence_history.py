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
    latest_state = current_sample.get("convergence_state")
    latest_pressure = current_sample.get("convergence_pressure_level")

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


def _dedupe(items: list[Any]) -> list[str]:
    result: list[str] = []
    for item in items:
        if isinstance(item, str) and item and item not in result:
            result.append(item)
    return result
