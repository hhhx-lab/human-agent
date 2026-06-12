from __future__ import annotations

from typing import Any


ACTIVE_HANDOFF_PROFILE_KEY = "live_turn_waiting_handoff_profile"
ACTIVE_HANDOFF_PROFILE_REF_KEY = "live_turn_waiting_handoff_profile_ref"
ACTIVE_HANDOFF_PROFILE_REF = (
    "runtime/state/terminal/terminal_life_loop_state.json"
    "#live_turn_waiting_handoff_profile"
)
PREVIOUS_HANDOFF_PROFILE_KEY = "previous_live_turn_waiting_handoff_profile"
PREVIOUS_HANDOFF_PROFILE_REF_KEY = "previous_live_turn_waiting_handoff_profile_ref"
PREVIOUS_HANDOFF_PROFILE_REF = (
    "runtime/state/terminal/terminal_life_loop_state.json"
    "#previous_live_turn_waiting_handoff_profile"
)


HANDOFF_CARRY_FIELD_NAMES = (
    PREVIOUS_HANDOFF_PROFILE_KEY,
    PREVIOUS_HANDOFF_PROFILE_REF_KEY,
    "previous_live_turn_waiting_handoff_carry_status",
    "previous_live_turn_waiting_handoff_next_required_action",
    "previous_live_turn_waiting_handoff_lineage_depth_band",
    "previous_live_turn_waiting_handoff_evidence_ref_count",
    "previous_live_turn_waiting_handoff_carried_presence_keys",
)


def select_handoff_profile(*sources: dict[str, Any] | None) -> dict[str, Any]:
    for source in sources:
        if not isinstance(source, dict):
            continue
        for key in (PREVIOUS_HANDOFF_PROFILE_KEY, ACTIVE_HANDOFF_PROFILE_KEY):
            profile = _dict_or_empty(source.get(key))
            if profile:
                return dict(profile)
    return {}


def active_handoff_profile_fields(profile: dict[str, Any]) -> dict[str, Any]:
    if not profile:
        return {}
    return {
        ACTIVE_HANDOFF_PROFILE_KEY: dict(profile),
        ACTIVE_HANDOFF_PROFILE_REF_KEY: ACTIVE_HANDOFF_PROFILE_REF,
    }


def previous_handoff_profile_fields(
    profile: dict[str, Any],
    *,
    carry_status: str,
) -> dict[str, Any]:
    if not profile:
        return {}
    fields: dict[str, Any] = {
        PREVIOUS_HANDOFF_PROFILE_KEY: dict(profile),
        PREVIOUS_HANDOFF_PROFILE_REF_KEY: PREVIOUS_HANDOFF_PROFILE_REF,
        "previous_live_turn_waiting_handoff_carry_status": carry_status,
    }
    for source_key, target_key in (
        (
            "next_required_action",
            "previous_live_turn_waiting_handoff_next_required_action",
        ),
        ("lineage_depth_band", "previous_live_turn_waiting_handoff_lineage_depth_band"),
    ):
        if profile.get(source_key):
            fields[target_key] = str(profile[source_key])
    evidence_ref_count = _int_or_none(profile.get("handoff_evidence_ref_count"))
    if evidence_ref_count is not None:
        fields["previous_live_turn_waiting_handoff_evidence_ref_count"] = (
            evidence_ref_count
        )
    carried_presence_keys = _string_list(profile.get("carried_presence_keys"))
    if carried_presence_keys:
        fields["previous_live_turn_waiting_handoff_carried_presence_keys"] = (
            carried_presence_keys
        )
    return fields


def _dict_or_empty(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
