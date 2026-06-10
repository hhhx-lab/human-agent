from __future__ import annotations

from typing import Any


def build_resident_background_lineage_state(
    idle_governance: dict[str, Any] | None,
    *,
    governance_phase: str,
    status: str,
) -> dict[str, Any]:
    governance = idle_governance or {}
    profile = _dict_or_empty(governance.get("background_lineage_governance_profile"))
    explicit_depth_band = (
        governance.get("background_lineage_depth_band")
        or profile.get("depth_band")
    )
    generation = _int_or_zero(
        governance.get("background_carryover_generation")
        if governance.get("background_carryover_generation") is not None
        else profile.get("generation")
    )
    depth_band = _deeper_depth_band(
        str(explicit_depth_band or ""),
        _depth_band_for_generation(generation),
    )
    if not depth_band:
        return {}

    lineage_state = {
        "schema_version": "resident_background_lineage_state_v0",
        "status": status,
        "governance_phase": governance_phase,
        "continuity_mode": governance.get("background_continuity_mode"),
        "generation": generation,
        "depth_band": str(depth_band),
        "waiting_posture": _waiting_posture_for_depth(
            depth_band,
            pressure_level=governance.get("background_carryover_pressure_level"),
        ),
        "cadence_weight": _cadence_weight_for_depth(depth_band),
        "evidence_ref_count": _int_or_zero(
            governance.get("background_lineage_evidence_ref_count")
            if governance.get("background_lineage_evidence_ref_count") is not None
            else profile.get("evidence_ref_count")
        ),
        "attention_target": governance.get("governance_attention_target")
        or profile.get("governance_attention_target"),
        "attention_reason": governance.get("governance_attention_reason")
        or profile.get("governance_attention_reason"),
        "cadence_profile": governance.get("governance_cadence_profile")
        or profile.get("governance_cadence_profile"),
        "next_idle_action": governance.get("next_idle_action")
        or profile.get("next_idle_action"),
        "heartbeat_interval_ms": _int_or_zero(
            governance.get("heartbeat_interval_ms")
            if governance.get("heartbeat_interval_ms") is not None
            else profile.get("heartbeat_interval_ms")
        ),
    }
    _copy_if_present(
        lineage_state,
        "parent_run_id",
        governance.get("background_carryover_parent_run_id")
        or profile.get("parent_run_id"),
    )
    evidence_refs = _string_list(
        profile.get("evidence_refs")
        or governance.get("background_continuity_ref_set")
    )
    if evidence_refs:
        lineage_state["evidence_refs"] = evidence_refs
    source_refs = _string_list(governance.get("background_carryover_source_ref_set"))
    if source_refs:
        lineage_state["source_refs"] = source_refs
    continuity_refs = _string_list(governance.get("background_continuity_ref_set"))
    if continuity_refs:
        lineage_state["continuity_refs"] = continuity_refs
    if profile:
        lineage_state["governance_profile_ref"] = (
            "background_lineage_governance_profile"
        )
    return {
        key: value
        for key, value in lineage_state.items()
        if value is not None and value != ""
    }


def _copy_if_present(target: dict[str, Any], key: str, value: Any) -> None:
    if value:
        target[key] = str(value)


def _dict_or_empty(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _depth_band_for_generation(generation: int) -> str:
    if generation >= 5:
        return "entrenched_background_presence"
    if generation >= 3:
        return "deep_persistent_lineage"
    if generation == 2:
        return "persistent_lineage"
    if generation == 1:
        return "single_carryover"
    return ""


def _deeper_depth_band(left: str, right: str) -> str:
    order = {
        "": 0,
        "no_background_lineage": 0,
        "single_carryover": 1,
        "persistent_lineage": 2,
        "deep_persistent_lineage": 3,
        "entrenched_background_presence": 4,
    }
    return left if order.get(left, 0) >= order.get(right, 0) else right


def _waiting_posture_for_depth(depth_band: str, *, pressure_level: Any) -> str:
    if depth_band == "entrenched_background_presence":
        return "entrenched_background_residency_hold"
    if depth_band == "deep_persistent_lineage":
        return "deep_background_residency_hold"
    if depth_band == "persistent_lineage":
        return "persistent_background_hold"
    if depth_band == "single_carryover":
        return (
            "background_carryover_pressure_hold"
            if pressure_level in {"present", "elevated"}
            else "background_carryover_hold"
        )
    return "no_background_lineage_hold"


def _cadence_weight_for_depth(depth_band: str) -> str:
    if depth_band == "entrenched_background_presence":
        return "entrenched"
    if depth_band == "deep_persistent_lineage":
        return "deep"
    if depth_band == "persistent_lineage":
        return "persistent"
    if depth_band == "single_carryover":
        return "carryover"
    return "none"
