from __future__ import annotations

from typing import Any


NIGHTMARE_RISK_REF = "runtime/state/dream/nightmare_loop_risk.json"
BELIEF_LEARNING_PLAN_REF = "runtime/state/growth/belief_learning_plan.json"
LANGUAGE_LEARNING_PLAN_REF = "runtime/state/growth/language_learning_plan.json"
RELATIONSHIP_LEARNING_PLAN_REF = "runtime/state/growth/relationship_learning_plan.json"


def derive_offline_learning_profile(
    *,
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    nightmare_risk = nightmare_risk or {}
    belief_learning_plan = belief_learning_plan or {}
    language_learning_plan = language_learning_plan or {}
    relationship_learning_plan = relationship_learning_plan or {}

    priority_profile: dict[str, str] = {}

    nightmare_priority = _nightmare_priority(nightmare_risk)
    if nightmare_priority is not None:
        priority_profile["nightmare_risk"] = nightmare_priority

    belief_priority = _belief_priority(belief_learning_plan)
    if belief_priority is not None:
        priority_profile["belief_learning_plan"] = belief_priority

    language_priority = _language_priority(language_learning_plan)
    if language_priority is not None:
        priority_profile["language_learning_plan"] = language_priority

    relationship_priority = _relationship_priority(relationship_learning_plan)
    if relationship_priority is not None:
        priority_profile["relationship_learning_plan"] = relationship_priority

    if "urgent" in priority_profile.values():
        pressure_level = "urgent"
    elif "elevated" in priority_profile.values():
        pressure_level = "elevated"
    elif priority_profile:
        pressure_level = "present"
    else:
        pressure_level = "quiet"

    if priority_profile.get("nightmare_risk") == "urgent":
        attention_target = "nightmare_risk"
    elif priority_profile.get("relationship_learning_plan") in {"urgent", "elevated"}:
        attention_target = "relationship_learning_plan"
    elif priority_profile.get("language_learning_plan") in {"urgent", "elevated"}:
        attention_target = "language_learning_plan"
    elif priority_profile.get("belief_learning_plan") in {"urgent", "elevated"}:
        attention_target = "belief_learning_plan"
    elif "nightmare_risk" in priority_profile:
        attention_target = "nightmare_risk"
    elif "relationship_learning_plan" in priority_profile:
        attention_target = "relationship_learning_plan"
    elif "language_learning_plan" in priority_profile:
        attention_target = "language_learning_plan"
    elif "belief_learning_plan" in priority_profile:
        attention_target = "belief_learning_plan"
    else:
        attention_target = "baseline_offline_learning_maintenance"

    ref_set = [
        ref
        for payload, ref in [
            (nightmare_risk, NIGHTMARE_RISK_REF),
            (belief_learning_plan, BELIEF_LEARNING_PLAN_REF),
            (language_learning_plan, LANGUAGE_LEARNING_PLAN_REF),
            (relationship_learning_plan, RELATIONSHIP_LEARNING_PLAN_REF),
        ]
        if payload
    ]

    blocked_learning_modes: list[str] = []
    for payload in [belief_learning_plan, language_learning_plan, relationship_learning_plan]:
        for mode in payload.get("blocked_learning_modes", []):
            if isinstance(mode, str) and mode not in blocked_learning_modes:
                blocked_learning_modes.append(mode)

    return {
        "offline_learning_pressure_level": pressure_level,
        "offline_learning_attention_target": attention_target,
        "offline_learning_priority_profile": priority_profile,
        "offline_learning_ref_set": ref_set,
        "blocked_learning_modes": blocked_learning_modes,
    }


def build_offline_learning_cumulative_profile(
    *,
    current_profile: dict[str, Any],
    background_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    background_profile = background_profile or {}
    current_priority = _priority_profile(
        current_profile.get("offline_learning_priority_profile")
    )
    background_priority = _priority_profile(
        background_profile.get("background_offline_learning_priority_profile")
        or background_profile.get("offline_learning_cumulative_priority_profile")
    )
    cumulative_priority = _merge_priority_profiles(
        background_priority,
        current_priority,
    )
    current_refs = _string_list(current_profile.get("offline_learning_ref_set"))
    background_refs = _string_list(
        background_profile.get("background_offline_learning_ref_set")
        or background_profile.get("offline_learning_cumulative_ref_set")
    )
    cumulative_refs = _dedupe_string_list([*background_refs, *current_refs])
    background_generation = _int_or_zero(
        background_profile.get("background_offline_learning_generation")
        or background_profile.get("offline_learning_cumulative_generation")
    )
    current_pressure = str(
        current_profile.get("offline_learning_pressure_level") or "quiet"
    )
    generation = background_generation + (
        1 if current_pressure != "quiet" or current_refs else 0
    )
    pressure_level = _pressure_from_priority(cumulative_priority)
    if pressure_level == "quiet" and background_generation > 0:
        pressure_level = str(
            background_profile.get("background_offline_learning_pressure_level")
            or background_profile.get("offline_learning_cumulative_pressure_level")
            or "present"
        )
    dominant_target = _dominant_target(
        priority_profile=cumulative_priority,
        fallback=str(
            current_profile.get("offline_learning_attention_target")
            or background_profile.get("background_offline_learning_attention_target")
            or background_profile.get("offline_learning_cumulative_attention_target")
            or "baseline_offline_learning_maintenance"
        ),
    )
    return {
        "schema_version": "offline_learning_cumulative_profile_v0",
        "generation": generation,
        "pressure_level": pressure_level,
        "attention_target": dominant_target,
        "priority_profile": cumulative_priority,
        "ref_set": cumulative_refs,
        "current_pressure_level": current_pressure,
        "previous_generation": background_generation,
    }


def _nightmare_priority(nightmare_risk: dict[str, Any]) -> str | None:
    if not nightmare_risk:
        return None
    if nightmare_risk.get("queue_e_priority_band") == "locked_repair_urgent":
        return "urgent"
    if nightmare_risk.get("risk_status") == "elevated":
        return "urgent"
    if nightmare_risk.get("repair_followup_required"):
        return "elevated"
    return "baseline"


def _belief_priority(plan: dict[str, Any]) -> str | None:
    if not plan:
        return None
    targets = list(plan.get("belief_targets", []))
    if plan.get("queue_e_priority_band") == "locked_repair_urgent" and (
        "confirmation_locked_contact_model_revision" in targets
    ):
        return "urgent"
    if plan.get("repair_followup_required") or any(
        "repair" in target or "regret" in target for target in targets
    ):
        return "elevated"
    return "baseline"


def _language_priority(plan: dict[str, Any]) -> str | None:
    if not plan:
        return None
    targets = list(plan.get("language_targets", []))
    if plan.get("queue_e_priority_band") == "locked_repair_urgent" or (
        "confirmation_locked_expression_restraint" in targets
    ):
        return "urgent"
    if plan.get("repair_followup_required") or (
        "apology_repair_expression_refinement" in targets
    ):
        return "elevated"
    return "baseline"


def _relationship_priority(plan: dict[str, Any]) -> str | None:
    if not plan:
        return None
    targets = list(plan.get("relationship_targets", []))
    if plan.get("queue_e_priority_band") == "locked_repair_urgent" or (
        plan.get("world_contact_release_posture") == "confirmation_blocked"
    ):
        return "urgent"
    if plan.get("repair_followup_required") or any("repair" in target for target in targets):
        return "elevated"
    return "baseline"


def _priority_profile(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {str(key): str(priority) for key, priority in value.items() if priority}


def _merge_priority_profiles(
    previous: dict[str, str],
    current: dict[str, str],
) -> dict[str, str]:
    merged = dict(previous)
    for key, priority in current.items():
        if _priority_rank(priority) >= _priority_rank(merged.get(key)):
            merged[key] = priority
    return merged


def _pressure_from_priority(priority_profile: dict[str, str]) -> str:
    if any(priority == "urgent" for priority in priority_profile.values()):
        return "urgent"
    if any(priority == "elevated" for priority in priority_profile.values()):
        return "elevated"
    if priority_profile:
        return "present"
    return "quiet"


def _dominant_target(*, priority_profile: dict[str, str], fallback: str) -> str:
    preferred_order = [
        "nightmare_risk",
        "relationship_learning_plan",
        "language_learning_plan",
        "belief_learning_plan",
    ]
    for level in ["urgent", "elevated", "present", "baseline"]:
        for target in preferred_order:
            if priority_profile.get(target) == level:
                return target
    return fallback


def _priority_rank(priority: str | None) -> int:
    return {
        "urgent": 4,
        "elevated": 3,
        "present": 2,
        "baseline": 1,
    }.get(str(priority or ""), 0)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _dedupe_string_list(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
