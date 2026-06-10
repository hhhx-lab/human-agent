from __future__ import annotations

from typing import Any


BACKGROUND_TRAIT_CONVERGENCE_REF_KEYS = (
    "background_resident_governance_state_ref",
    "background_resident_governance_explanation_ref",
    "background_trait_drift_monitor_ref",
    "background_convergence_summary_ref",
    "background_convergence_history_ref",
)


def cross_wake_trait_convergence_profile(
    carrier: dict[str, Any] | None,
) -> dict[str, Any]:
    carrier = carrier or {}
    existing_profile = _dict_or_empty(
        carrier.get("cross_wake_trait_convergence_profile")
    )
    lineage_state = _dict_or_empty(carrier.get("resident_background_lineage_state"))
    trait_presence = _dict_or_empty(lineage_state.get("trait_convergence_presence"))

    focus = (
        existing_profile.get("focus")
        or carrier.get("cross_wake_trait_convergence_focus")
        or trait_presence.get("trait_convergence_history_focus")
        or carrier.get("background_trait_convergence_history_focus")
    )
    unstable_names = _dedupe_string_list(
        _string_list(existing_profile.get("unstable_names"))
        or _string_list(carrier.get("cross_wake_trait_convergence_unstable_names"))
        or _string_list(trait_presence.get("trait_convergence_unstable_names"))
        or _string_list(carrier.get("background_trait_convergence_unstable_names"))
    )
    stable_names = _dedupe_string_list(
        _string_list(existing_profile.get("stable_names"))
        or _string_list(carrier.get("cross_wake_trait_convergence_stable_names"))
        or _string_list(trait_presence.get("trait_convergence_stable_names"))
        or _string_list(carrier.get("background_trait_convergence_stable_names"))
    )
    history_profile = _dict_or_empty(
        existing_profile.get("history_profile")
        or carrier.get("cross_wake_trait_convergence_history_profile")
        or trait_presence.get("trait_convergence_history_profile")
        or carrier.get("background_trait_convergence_history_profile")
    )
    score = (
        existing_profile.get("score")
        if existing_profile.get("score") is not None
        else carrier.get("cross_wake_trait_convergence_score")
        if carrier.get("cross_wake_trait_convergence_score") is not None
        else trait_presence.get("trait_convergence_score")
        if trait_presence.get("trait_convergence_score") is not None
        else carrier.get("background_trait_convergence_score")
    )
    trait_drift_update_mode_summary = _dict_or_empty(
        existing_profile.get("trait_drift_update_mode_summary")
        or carrier.get("cross_wake_trait_drift_update_mode_summary")
        or trait_presence.get("trait_drift_update_mode_summary")
        or carrier.get("background_trait_drift_update_mode_summary")
    )
    trait_drift_recalibration_names = _dedupe_string_list(
        _string_list(existing_profile.get("trait_drift_recalibration_names"))
        or _string_list(carrier.get("cross_wake_trait_drift_recalibration_names"))
        or _string_list(trait_presence.get("trait_drift_recalibration_names"))
        or _string_list(carrier.get("background_trait_drift_recalibration_names"))
        or _string_list(
            trait_drift_update_mode_summary.get("background_history_recalibration")
        )
    )
    trait_drift_stabilized_names = _dedupe_string_list(
        _string_list(existing_profile.get("trait_drift_stabilized_names"))
        or _string_list(carrier.get("cross_wake_trait_drift_stabilized_names"))
        or _string_list(trait_presence.get("trait_drift_stabilized_names"))
        or _string_list(carrier.get("background_trait_drift_stabilized_names"))
        or _string_list(
            trait_drift_update_mode_summary.get("background_history_stabilized")
        )
    )
    refs = _dedupe_string_list(
        _string_list(carrier.get("cross_wake_trait_convergence_refs"))
        + _string_list(existing_profile.get("refs"))
        + _string_list(trait_presence.get("trait_convergence_evidence_refs"))
        + [
            ref
            for ref in [
                trait_presence.get("trait_drift_monitor_ref"),
                *[carrier.get(key) for key in BACKGROUND_TRAIT_CONVERGENCE_REF_KEYS],
            ]
            if isinstance(ref, str) and ref
        ]
    )

    if not any([focus, unstable_names, stable_names, history_profile, score, refs]):
        return {}

    pressure = (
        existing_profile.get("pressure")
        or carrier.get("cross_wake_trait_convergence_pressure")
        or _pressure_from_focus_and_history(
            focus=str(focus or ""),
            unstable_names=unstable_names,
            history_profile=history_profile,
            trend_state=str(
                carrier.get("background_convergence_history_trend_state") or ""
            ),
            trait_drift_recalibration_names=trait_drift_recalibration_names,
        )
    )
    profile = _drop_empty(
        {
            "schema_version": "cross_wake_trait_convergence_profile_v0",
            "focus": focus,
            "pressure": pressure,
            "unstable_names": unstable_names,
            "stable_names": stable_names,
            "score": score,
            "history_profile": history_profile,
            "trait_drift_update_mode_summary": trait_drift_update_mode_summary,
            "trait_drift_recalibration_names": trait_drift_recalibration_names,
            "trait_drift_stabilized_names": trait_drift_stabilized_names,
            "refs": refs,
            "ref_count": len(refs),
        }
    )
    return _drop_empty(
        {
            "cross_wake_trait_convergence_profile": profile,
            "cross_wake_trait_convergence_focus": profile.get("focus"),
            "cross_wake_trait_convergence_pressure": profile.get("pressure"),
            "cross_wake_trait_convergence_unstable_names": profile.get(
                "unstable_names",
                [],
            ),
            "cross_wake_trait_convergence_stable_names": profile.get(
                "stable_names",
                [],
            ),
            "cross_wake_trait_convergence_score": profile.get("score"),
            "cross_wake_trait_convergence_refs": profile.get("refs", []),
            "cross_wake_trait_drift_update_mode_summary": profile.get(
                "trait_drift_update_mode_summary"
            ),
            "cross_wake_trait_drift_recalibration_names": profile.get(
                "trait_drift_recalibration_names",
                [],
            ),
            "cross_wake_trait_drift_stabilized_names": profile.get(
                "trait_drift_stabilized_names",
                [],
            ),
        }
    )


def _pressure_from_focus_and_history(
    *,
    focus: str,
    unstable_names: list[str],
    history_profile: dict[str, Any],
    trend_state: str,
    trait_drift_recalibration_names: list[str],
) -> str:
    if trait_drift_recalibration_names:
        return "recalibration"
    if focus == "trait_recalibration_required":
        return "recalibration"
    if trend_state in {"recent_recalibration_pressure", "elevated_pressure_watch"}:
        return "recalibration"
    if any(
        str(payload.get("latest_band", "")).lower() == "recalibrating"
        or str(payload.get("trend_state", "")).lower()
        == "recent_trait_recalibration"
        for payload in history_profile.values()
        if isinstance(payload, dict)
    ):
        return "recalibration"
    if focus == "trait_stability_hold" or unstable_names:
        return "stability_hold"
    if focus == "trait_convergence_stable":
        return "stable"
    if trend_state == "stable_cross_wake_convergence":
        return "stable"
    if focus:
        return "present"
    return "quiet"


def _dict_or_empty(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value else []
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dedupe_string_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _drop_empty(payload: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in payload.items():
        if value is None:
            continue
        if isinstance(value, str) and not value:
            continue
        if isinstance(value, (list, tuple, dict, set)) and not value:
            continue
        result[key] = value
    return result
