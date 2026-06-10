from __future__ import annotations

from typing import Any


def derive_queue_e_signal_profile(
    *,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    responsibility_loop_state = responsibility_loop_state or {}
    world_contact_summary = world_contact_summary or {}
    pain_regret_repair_report = pain_regret_repair_report or {}

    world_contact_release_posture = str(
        world_contact_summary.get("release_posture", "shadow_only_guarded")
    )
    repair_followup_required = bool(
        pain_regret_repair_report.get("repair_followup_required")
        or responsibility_loop_state.get("repair_followup_required")
    )
    repair_obligation_refs = _merge_refs(
        world_contact_summary.get("repair_obligation_refs", []),
        pain_regret_repair_report.get("repair_obligation_refs", []),
        responsibility_loop_state.get("repair_obligation_refs", []),
    )
    regret_pressure_refs = _merge_refs(
        world_contact_summary.get("regret_pressure_refs", []),
        pain_regret_repair_report.get("regret_pressure_refs", []),
        [
            item.get("ref")
            for item in responsibility_loop_state.get("regret_pressure_candidates", [])
            if isinstance(item, dict) and item.get("ref")
        ],
    )
    repair_obligation_count = max(
        len(world_contact_summary.get("repair_obligation_refs", [])),
        len(pain_regret_repair_report.get("repair_obligation_refs", [])),
        len(responsibility_loop_state.get("repair_obligation_refs", [])),
    )
    regret_pressure_count = max(
        len(world_contact_summary.get("regret_pressure_refs", [])),
        len(pain_regret_repair_report.get("regret_pressure_refs", [])),
        len(responsibility_loop_state.get("regret_pressure_candidates", [])),
    )

    if repair_followup_required and world_contact_release_posture == "confirmation_blocked":
        queue_e_priority_band = "locked_repair_urgent"
    elif repair_followup_required or repair_obligation_count > 0 or regret_pressure_count > 0:
        queue_e_priority_band = "repair_guarded"
    else:
        queue_e_priority_band = "baseline"

    return {
        "world_contact_release_posture": world_contact_release_posture,
        "repair_followup_required": repair_followup_required,
        "repair_obligation_refs": repair_obligation_refs,
        "repair_obligation_count": repair_obligation_count,
        "regret_pressure_refs": regret_pressure_refs,
        "regret_pressure_count": regret_pressure_count,
        "queue_e_priority_band": queue_e_priority_band,
    }


def build_queue_e_repair_modulation_profile(
    *,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    profile = derive_queue_e_signal_profile(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    pressure_level = _repair_pressure_level(profile)
    ref_set = _merge_refs(
        profile.get("repair_obligation_refs", []),
        profile.get("regret_pressure_refs", []),
        [
            "runtime/state/action/responsibility_loop_state.json"
            if responsibility_loop_state
            else "",
            "runtime/state/membrane/world_contact_summary.json"
            if world_contact_summary
            else "",
            "runtime/reports/latest/pain_regret_repair_report.json"
            if pain_regret_repair_report
            else "",
        ],
    )
    attention_target = "repair_followup"
    if profile["world_contact_release_posture"] == "confirmation_blocked":
        attention_target = "world_contact_confirmation_lock"
    elif profile["regret_pressure_count"]:
        attention_target = "regret_pressure"
    elif profile["repair_obligation_count"]:
        attention_target = "repair_obligation"
    return {
        "schema_version": "queue_e_repair_modulation_profile_v0",
        "pressure_level": pressure_level,
        "attention_target": attention_target,
        "world_contact_release_posture": profile["world_contact_release_posture"],
        "repair_followup_required": profile["repair_followup_required"],
        "repair_obligation_count": profile["repair_obligation_count"],
        "regret_pressure_count": profile["regret_pressure_count"],
        "queue_e_priority_band": profile["queue_e_priority_band"],
        "repair_obligation_refs": list(profile.get("repair_obligation_refs", [])),
        "regret_pressure_refs": list(profile.get("regret_pressure_refs", [])),
        "ref_set": ref_set,
    }


def queue_e_repair_modulation_profile_from_replay_cue_bundle(
    replay_cue_bundle: dict[str, Any] | None,
) -> dict[str, Any]:
    replay_cue_bundle = replay_cue_bundle or {}
    embedded_profile = replay_cue_bundle.get("queue_e_repair_modulation_profile")
    if (
        isinstance(embedded_profile, dict)
        and embedded_profile.get("schema_version")
        == "queue_e_repair_modulation_profile_v0"
    ):
        return {
            **embedded_profile,
            "ref_set": _merge_refs(list(embedded_profile.get("ref_set", []))),
        }

    signal_profile = queue_e_signal_profile_from_replay_cue_bundle(replay_cue_bundle)
    pressure_level = _repair_pressure_level(signal_profile)
    ref_set = _merge_refs(
        signal_profile.get("repair_obligation_refs", []),
        signal_profile.get("regret_pressure_refs", []),
        [
            "runtime/state/replay/replay_cue_bundle.json"
            if replay_cue_bundle
            else "",
        ],
    )
    attention_target = "repair_followup"
    if signal_profile["world_contact_release_posture"] == "confirmation_blocked":
        attention_target = "world_contact_confirmation_lock"
    elif signal_profile["regret_pressure_count"]:
        attention_target = "regret_pressure"
    elif signal_profile["repair_obligation_count"]:
        attention_target = "repair_obligation"
    return {
        "schema_version": "queue_e_repair_modulation_profile_v0",
        "pressure_level": pressure_level,
        "attention_target": attention_target,
        "world_contact_release_posture": signal_profile["world_contact_release_posture"],
        "repair_followup_required": signal_profile["repair_followup_required"],
        "repair_obligation_count": signal_profile["repair_obligation_count"],
        "regret_pressure_count": signal_profile["regret_pressure_count"],
        "queue_e_priority_band": signal_profile["queue_e_priority_band"],
        "repair_obligation_refs": list(signal_profile.get("repair_obligation_refs", [])),
        "regret_pressure_refs": list(signal_profile.get("regret_pressure_refs", [])),
        "ref_set": ref_set,
    }


def queue_e_signal_profile_from_replay_cue_bundle(
    replay_cue_bundle: dict[str, Any] | None,
) -> dict[str, Any]:
    replay_cue_bundle = replay_cue_bundle or {}
    repair_obligation_refs = list(replay_cue_bundle.get("repair_obligation_refs", []))
    regret_pressure_refs = list(replay_cue_bundle.get("regret_pressure_refs", []))

    return {
        "world_contact_release_posture": replay_cue_bundle.get(
            "world_contact_release_posture",
            "shadow_only_guarded",
        ),
        "repair_followup_required": bool(replay_cue_bundle.get("repair_followup_required")),
        "repair_obligation_refs": repair_obligation_refs,
        "repair_obligation_count": int(
            replay_cue_bundle.get("repair_obligation_count", len(repair_obligation_refs))
        ),
        "regret_pressure_refs": regret_pressure_refs,
        "regret_pressure_count": int(
            replay_cue_bundle.get("regret_pressure_count", len(regret_pressure_refs))
        ),
        "queue_e_priority_band": replay_cue_bundle.get("queue_e_priority_band", "baseline"),
    }


def _repair_pressure_level(profile: dict[str, Any]) -> str:
    if profile.get("queue_e_priority_band") == "locked_repair_urgent":
        return "urgent"
    if profile.get("repair_followup_required"):
        return "elevated"
    if profile.get("repair_obligation_count") or profile.get("regret_pressure_count"):
        return "present"
    return "quiet"


def _merge_refs(*ref_groups: list[Any]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for group in ref_groups:
        for ref in group:
            if not isinstance(ref, str) or not ref or ref in seen:
                continue
            seen.add(ref)
            merged.append(ref)
    return merged
