from __future__ import annotations

import json
from typing import Any


def project_body_rhythm_pulse_from_live_turn(
    *,
    body_rhythm_pulse: dict[str, Any] | None,
    generated_at: str,
    run_id: str,
    live_turn_focus: str | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    external_utterance: str | None = None,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(body_rhythm_pulse or {}))
    if not updated:
        updated = {
            "schema_version": "body_rhythm_pulse_v0",
            "pulse_id": f"body-rhythm-pulse-{run_id}",
            "heartbeat_counter": 0,
        }
    fatigue_level = (body_resource_budget or {}).get("fatigue_state", {}).get(
        "level",
        "managed_low_noise",
    )
    energy_level = (body_resource_budget or {}).get("energy_state", {}).get(
        "level",
        "baseline",
    )
    rhythm_state = "live_dialogue_engaged" if str(external_utterance or "").strip() else (
        updated.get("rhythm_state") or "waiting_presence"
    )
    updated.update(
        {
            "schema_version": "body_rhythm_pulse_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "rhythm_state": rhythm_state,
            "fatigue_load": fatigue_level,
            "energy_level": energy_level,
            "allostatic_load": updated.get("allostatic_load")
            or (body_resource_budget or {})
            .get("maintenance_pressure", {})
            .get("level", "guarded_maintenance"),
            "live_turn_focus": live_turn_focus,
            "arousal_level": (core_affect_vector or {}).get("arousal"),
            "body_repair_drive": (core_affect_vector or {}).get("repair_drive")
            or (body_resource_budget or {})
            .get("maintenance_pressure", {})
            .get("repair_drive"),
        }
    )
    return updated


def project_need_state_from_live_turn(
    *,
    need_state_vector: dict[str, Any] | None,
    generated_at: str,
    run_id: str,
    live_turn_focus: str | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    external_utterance: str | None = None,
) -> dict[str, Any]:
    updated = json.loads(json.dumps(need_state_vector or {}))
    if not updated:
        updated = {
            "schema_version": "need_state_vector_v0",
            "need_vector_id": f"need-state-{run_id}",
        }
    social_readiness = (
        "dialogic_live_engaged"
        if str(external_utterance or "").strip()
        else updated.get("social_readiness") or "protected_low_contact"
    )
    updated.update(
        {
            "schema_version": "need_state_vector_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "social_readiness": social_readiness,
            "cognitive_bandwidth": (
                "live_dialogic"
                if str(external_utterance or "").strip()
                else updated.get("cognitive_bandwidth") or "guarded_dialogic"
            ),
            "repair_drive": (core_affect_vector or {}).get("repair_drive")
            or updated.get("repair_drive")
            or "low",
            "resource_deficit": (body_resource_budget or {})
            .get("fatigue_state", {})
            .get("level", updated.get("resource_deficit") or "guarded_maintenance"),
            "live_turn_focus": live_turn_focus,
        }
    )
    return updated


def body_presence_digest(
    *,
    body_rhythm_pulse: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rhythm = body_rhythm_pulse or {}
    budget = body_resource_budget or {}
    affect = core_affect_vector or {}
    world = world_contact_summary or {}
    return {
        "schema_version": "body_presence_digest_v0",
        "rhythm_state": rhythm.get("rhythm_state"),
        "fatigue_load": rhythm.get("fatigue_load")
        or budget.get("fatigue_state", {}).get("level"),
        "energy_level": rhythm.get("energy_level")
        or budget.get("energy_state", {}).get("level"),
        "arousal_level": affect.get("arousal"),
        "body_repair_drive": affect.get("repair_drive")
        or rhythm.get("body_repair_drive"),
        "world_contact_posture": world.get("release_posture"),
        "world_contact_kind": world.get("contact_kind") or world.get("contact_mode"),
    }