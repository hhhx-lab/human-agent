from __future__ import annotations

import json
from typing import Any


BODY_PRESSURE_PROFILE_REF = "runtime/state/action/go_nogo_state.json#body_pressure_profile"
HANDOFF_PROFILE_REF = (
    "runtime/state/life_targets/queue_e_world_contact_repair_hold_handoff.json"
)
RESPONSIBILITY_CONSCIOUSNESS_CONTEXT_REF = (
    "runtime/state/action/responsibility_loop_state.json#consciousness_context_profile"
)

SOURCE_DOC_REFS = [
    "docs/real—live0/10_responsibility_regret_repair.md",
    "docs/real—live0/11_life_membrane_validation.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_queue_e_world_contact_handoff_profile(
    *,
    world_contact_validation: dict[str, Any],
    validation_rollup: dict[str, Any],
    schema_runner_manifest: dict[str, Any],
) -> dict[str, Any]:
    validation_closed = world_contact_repair_hold_ready(world_contact_validation)
    rollup_closed = queue_e_world_contact_repair_hold_ready(validation_rollup)
    manifest_closed = queue_e_world_contact_repair_hold_ready(schema_runner_manifest)
    handoff_status = (
        "closed"
        if validation_closed and rollup_closed and manifest_closed
        else "deferred_until_s05_s09"
    )
    body_pressure_profile_ref = (
        schema_runner_manifest.get("queue_e_world_contact_body_pressure_profile_ref")
        or validation_rollup.get("queue_e_world_contact_body_pressure_profile_ref")
        or world_contact_validation.get("body_pressure_profile_ref")
        or BODY_PRESSURE_PROFILE_REF
    )
    ref_set = _dedupe_string_refs(
        [
            "runtime/state/action/go_nogo_state.json#future_no_go_profile",
            body_pressure_profile_ref,
            *(
                [
                    "runtime/state/validation/world_contact_validation.json",
                    "runtime/state/validation/validation_rollup.json#queue_e_world_contact_repair_hold_required",
                    "runtime/state/schema_runner/run_manifest.json#queue_e_world_contact_repair_hold_required",
                    "runtime/state/validation/validation_rollup.json#queue_e_world_contact_body_pressure_profile_ref",
                ]
                if handoff_status == "closed"
                else []
            ),
            *list(world_contact_validation.get("repair_governance_refs", [])),
            *list(
                validation_rollup.get(
                    "queue_e_world_contact_repair_governance_refs", []
                )
            ),
            *list(
                schema_runner_manifest.get(
                    "queue_e_world_contact_repair_governance_refs", []
                )
            ),
        ]
    )
    return {
        "schema_version": "queue_e_world_contact_repair_hold_handoff_v0",
        "handoff_status": handoff_status,
        "future_no_go_profile_ref": (
            schema_runner_manifest.get("queue_e_world_contact_future_no_go_profile_ref")
            or validation_rollup.get("queue_e_world_contact_future_no_go_profile_ref")
            or world_contact_validation.get("future_no_go_profile_ref")
            or "runtime/state/action/go_nogo_state.json#future_no_go_profile"
        ),
        "repair_hold_required": (
            bool(
                schema_runner_manifest.get(
                    "queue_e_world_contact_repair_hold_required"
                )
            )
            or bool(validation_rollup.get("queue_e_world_contact_repair_hold_required"))
            or bool(world_contact_validation.get("repair_hold_required"))
        ),
        "confirmation_threshold_bias": (
            schema_runner_manifest.get(
                "queue_e_world_contact_confirmation_threshold_bias"
            )
            or validation_rollup.get(
                "queue_e_world_contact_confirmation_threshold_bias"
            )
            or world_contact_validation.get("confirmation_threshold_bias")
            or "deferred"
        ),
        "future_release_posture": (
            schema_runner_manifest.get("queue_e_world_contact_future_release_posture")
            or validation_rollup.get("queue_e_world_contact_future_release_posture")
            or world_contact_validation.get("future_release_posture")
            or "deferred_until_repair_handoff"
        ),
        "body_pressure_profile_ref": body_pressure_profile_ref,
        "blocked_future_routes": _dedupe_string_refs(
            [
                *list(
                    schema_runner_manifest.get(
                        "queue_e_world_contact_blocked_future_routes", []
                    )
                ),
                *list(
                    validation_rollup.get(
                        "queue_e_world_contact_blocked_future_routes", []
                    )
                ),
                *list(world_contact_validation.get("blocked_future_routes", [])),
            ]
        ),
        "allowed_repair_routes": _dedupe_string_refs(
            [
                *list(
                    schema_runner_manifest.get(
                        "queue_e_world_contact_allowed_repair_routes", []
                    )
                ),
                *list(
                    validation_rollup.get(
                        "queue_e_world_contact_allowed_repair_routes", []
                    )
                ),
                *list(world_contact_validation.get("allowed_repair_routes", [])),
            ]
        ),
        "repair_governance_refs": _dedupe_string_refs(
            [
                *list(
                    schema_runner_manifest.get(
                        "queue_e_world_contact_repair_governance_refs", []
                    )
                ),
                *list(
                    validation_rollup.get(
                        "queue_e_world_contact_repair_governance_refs", []
                    )
                ),
                *list(world_contact_validation.get("repair_governance_refs", [])),
            ]
        ),
        "source_state_refs": [
            "runtime/state/validation/world_contact_validation.json",
            "runtime/state/validation/validation_rollup.json",
            "runtime/state/schema_runner/run_manifest.json",
        ],
        "ref_set": ref_set,
    }


def project_queue_e_world_contact_repair_hold_handoff_from_live_turn(
    *,
    handoff_profile: dict[str, Any],
    generated_at: str,
    world_contact_validation: dict[str, Any],
    validation_rollup: dict[str, Any],
    schema_runner_manifest: dict[str, Any],
    responsibility_loop_state: dict[str, Any] | None = None,
    live_turn_focus: str | None = None,
    live_dialogue_turn_refs: list[str] | None = None,
    process_report: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = build_queue_e_world_contact_handoff_profile(
        world_contact_validation=world_contact_validation,
        validation_rollup=validation_rollup,
        schema_runner_manifest=schema_runner_manifest,
    )
    if handoff_profile:
        seeded = json.loads(json.dumps(handoff_profile))
        for key in ("run_id", "handoff_id"):
            if seeded.get(key) and not updated.get(key):
                updated[key] = seeded[key]
    updated["generated_at"] = generated_at
    consciousness_context_profile = (
        (responsibility_loop_state or {}).get("consciousness_context_profile")
        if isinstance(responsibility_loop_state, dict)
        else {}
    )
    if not isinstance(consciousness_context_profile, dict):
        consciousness_context_profile = {}
    live_responsibility_context_refs = _dedupe_string_refs(
        list(consciousness_context_profile.get("ref_set", []))
        + [RESPONSIBILITY_CONSCIOUSNESS_CONTEXT_REF]
        + (
            ["runtime/state/action/responsibility_loop_state.json"]
            if responsibility_loop_state
            else []
        )
    )
    if live_responsibility_context_refs:
        updated["live_responsibility_consciousness_context_refs"] = (
            live_responsibility_context_refs
        )
        updated["ref_set"] = _dedupe_string_refs(
            list(updated.get("ref_set", [])) + live_responsibility_context_refs
        )
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    if live_dialogue_turn_refs:
        updated["live_dialogue_turn_refs"] = _dedupe_string_refs(live_dialogue_turn_refs)
    updated["last_projected_from_live_turn_ref"] = (
        live_dialogue_turn_refs[-1] if live_dialogue_turn_refs else None
    )
    updated["handoff_boundary"] = (
        "queue_e_world_contact_handoff_live_turn_evidence_not_spoken_language"
    )
    updated["source_doc_refs"] = _dedupe_string_refs(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    if live_dialogue_turn_refs and updated.get("handoff_status") == "closed":
        from ..live0_audit.gate_f_inspection import (
            live_queue_e_world_contact_handoff_closeout_audited,
        )

        closeout_audited = live_queue_e_world_contact_handoff_closeout_audited(
            process_report or {},
            updated,
            terminal_life_loop_state or {},
        )
        if not closeout_audited:
            updated["handoff_status"] = "deferred_until_s05_s09"
            updated["repair_hold_required"] = False
    return updated


def world_contact_repair_hold_ready(payload: dict[str, Any]) -> bool:
    return (
        payload.get("schema_version") == "world_contact_validation_v0"
        and payload.get("repair_hold_required") is True
        and payload.get("confirmation_threshold_bias") == "raised"
        and payload.get("future_no_go_profile_ref")
        == "runtime/state/action/go_nogo_state.json#future_no_go_profile"
        and payload.get("body_pressure_profile_ref") == BODY_PRESSURE_PROFILE_REF
        and bool(payload.get("blocked_future_routes"))
        and bool(payload.get("allowed_repair_routes"))
        and bool(payload.get("repair_governance_refs"))
    )


def queue_e_world_contact_repair_hold_ready(payload: dict[str, Any]) -> bool:
    return (
        payload.get("schema_version")
        in {"validation_rollup_v0", "schema_runner_run_manifest_v0"}
        and payload.get("queue_e_world_contact_repair_hold_required") is True
        and payload.get("queue_e_world_contact_confirmation_threshold_bias") == "raised"
        and payload.get("queue_e_world_contact_future_no_go_profile_ref")
        == "runtime/state/action/go_nogo_state.json#future_no_go_profile"
        and payload.get("queue_e_world_contact_body_pressure_profile_ref")
        == BODY_PRESSURE_PROFILE_REF
        and bool(payload.get("queue_e_world_contact_blocked_future_routes"))
        and bool(payload.get("queue_e_world_contact_allowed_repair_routes"))
        and bool(payload.get("queue_e_world_contact_repair_governance_refs"))
    )


def _dedupe_string_refs(refs: list[Any]) -> list[str]:
    result: list[str] = []
    for ref in refs:
        if not ref:
            continue
        value = str(ref)
        if value not in result:
            result.append(value)
    return result