from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/75_external_irreversible_action_confirmation_policy.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/81_coexistence_event_review_and_responsibility_loop.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "docs/v0/code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md",
    "docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md",
]


def build_world_contact_summary(
    *,
    run_id: str,
    generated_at: str,
    action_intent_queue: dict[str, Any],
    world_contact_gate: dict[str, Any],
    confirmation_binding: dict[str, Any],
    side_effect_review: dict[str, Any],
    responsibility_loop: dict[str, Any],
    world_observation_route: dict[str, Any] | None = None,
    periphery_normalization_trace: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    prediction_workspace: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    world_observation_route = world_observation_route or {}
    periphery_normalization_trace = periphery_normalization_trace or {}
    belief_state = belief_state or {}
    prediction_error_field = prediction_error_field or {}
    active_sampling_plan = active_sampling_plan or {}
    prediction_workspace = prediction_workspace or {}
    signal_media_runtime = signal_media_runtime or {}
    action_intents = list(action_intent_queue.get("action_intents", []))
    confirmation_pending_ids = list(confirmation_binding.get("required_action_intent_ids", []))
    blocked_contacts = list(world_contact_gate.get("blocked_contacts", []))
    repair_obligations = list(responsibility_loop.get("repair_obligation_refs", []))
    regret_pressure_ids = [
        item.get("regret_pressure_id")
        for item in responsibility_loop.get("regret_pressure_candidates", [])
        if isinstance(item, dict) and item.get("regret_pressure_id")
    ]

    release_posture = "shadow_only_guarded"
    if confirmation_binding.get("requires_confirmation"):
        release_posture = "confirmation_blocked"
    elif world_contact_gate.get("contact_mode") == "blocked":
        release_posture = "contact_blocked"

    error_events = [
        event
        for event in prediction_error_field.get("error_events", [])
        if isinstance(event, dict)
    ]
    precision_policy = signal_media_runtime.get("precision_policy", {})
    inhibition_profile = signal_media_runtime.get("inhibition_profile", {})
    modulation_vector = signal_media_runtime.get("modulation_vector", {})
    workspace_contents = prediction_workspace.get("workspace_contents", {})
    normalized_channels = list(periphery_normalization_trace.get("normalized_channels", []))
    promoted_channels = list(periphery_normalization_trace.get("promoted_channels", []))
    deferred_channels = list(periphery_normalization_trace.get("deferred_channels", []))
    suppressed_channels = list(periphery_normalization_trace.get("suppressed_channels", []))
    world_contact_prediction_ref_set = _dedupe_string_refs(
        [
            "runtime/state/prediction/belief_state_frame.json" if belief_state else None,
            "runtime/state/prediction/prediction_error_field.json" if prediction_error_field else None,
            "runtime/state/prediction/active_sampling_plan.json" if active_sampling_plan else None,
            "runtime/state/prediction/prediction_workspace_frame.json" if prediction_workspace else None,
            "runtime/state/signal/signal_media_runtime.json" if signal_media_runtime else None,
            "runtime/state/observation/world_observation_route.json" if world_observation_route else None,
            (
                "runtime/state/observation/periphery_normalization_trace.json"
                if periphery_normalization_trace
                else None
            ),
            *list(world_observation_route.get("guard_refs", [])),
            *list(world_observation_route.get("command_binding_refs", [])),
            *list(active_sampling_plan.get("guard_refs", [])),
            *list(active_sampling_plan.get("command_binding_refs", [])),
            *list(active_sampling_plan.get("expected_observation_refs", [])),
            *list(prediction_error_field.get("precision_requests", [])),
        ]
    )

    return {
        "schema_version": "world_contact_summary_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "world_contact_summary_id": f"world-contact-summary-{run_id}",
        "contact_mode": world_contact_gate.get("contact_mode", "shadow_only"),
        "release_posture": release_posture,
        "action_intent_queue_ref": "runtime/state/membrane/action_intent_queue.json",
        "world_contact_gate_ref": "runtime/state/action/world_contact_gate_state.json",
        "confirmation_binding_ref": "runtime/state/membrane/confirmation_binding.json",
        "side_effect_review_ref": "runtime/state/action/side_effect_review.json",
        "responsibility_loop_ref": "runtime/state/action/responsibility_loop_state.json",
        "world_observation_route_ref": (
            "runtime/state/observation/world_observation_route.json"
            if world_observation_route
            else None
        ),
        "periphery_normalization_ref": (
            "runtime/state/observation/periphery_normalization_trace.json"
            if periphery_normalization_trace
            else None
        ),
        "candidate_intent_count": len(action_intents),
        "blocked_contact_count": len(blocked_contacts),
        "confirmation_pending_ids": confirmation_pending_ids,
        "belief_state_ref": (
            "runtime/state/prediction/belief_state_frame.json" if belief_state else None
        ),
        "belief_revision_policy": belief_state.get("revision_policy"),
        "belief_active_life_targets": list(belief_state.get("active_life_targets", [])),
        "prediction_error_ref": (
            "runtime/state/prediction/prediction_error_field.json"
            if prediction_error_field
            else None
        ),
        "prediction_error_count": len(error_events),
        "prediction_error_events": [
            {
                "error_id": event.get("error_id"),
                "error_kind": event.get("error_kind"),
                "precision_request": event.get("precision_request"),
                "delta": event.get("delta"),
            }
            for event in error_events
        ],
        "prediction_stage_effect": prediction_error_field.get("stage_effect"),
        "active_sampling_plan_ref": (
            "runtime/state/prediction/active_sampling_plan.json"
            if active_sampling_plan
            else None
        ),
        "active_sampling_route": (
            active_sampling_plan.get("selected_route")
            or world_observation_route.get("selected_route")
        ),
        "active_sampling_stage_effect": active_sampling_plan.get("stage_effect"),
        "active_sampling_expected_observation_refs": list(
            active_sampling_plan.get("expected_observation_refs", [])
        ),
        "active_sampling_guard_refs": list(active_sampling_plan.get("guard_refs", [])),
        "prediction_workspace_ref": (
            "runtime/state/prediction/prediction_workspace_frame.json"
            if prediction_workspace
            else None
        ),
        "prediction_workspace_downstream_systems": list(
            prediction_workspace.get("downstream_systems", [])
        ),
        "prediction_workspace_active_sampling_mode": workspace_contents.get(
            "active_sampling_mode"
        ),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json" if signal_media_runtime else None
        ),
        "signal_precision_policy_mode": precision_policy.get("policy_mode"),
        "signal_precision_stage_effect": precision_policy.get("stage_effect"),
        "signal_inhibition_surfaces": list(
            inhibition_profile.get("blocked_release_surfaces", [])
        ),
        "signal_unexpected_uncertainty": modulation_vector.get("unexpected_uncertainty"),
        "signal_relationship_pressure": modulation_vector.get("relationship_pressure"),
        "observation_route_mode": world_observation_route.get("route_mode"),
        "observation_target_count": len(world_observation_route.get("observation_targets", [])),
        "prioritized_channel_count": len(world_observation_route.get("prioritized_channels", [])),
        "world_observation_error_focus_ids": list(world_observation_route.get("error_focus_ids", [])),
        "periphery_normalization_policy": periphery_normalization_trace.get(
            "normalization_policy"
        ),
        "normalized_channel_count": len(normalized_channels),
        "promoted_channel_count": len(promoted_channels),
        "deferred_channel_count": len(periphery_normalization_trace.get("deferred_channels", [])),
        "suppressed_channel_count": len(suppressed_channels),
        "periphery_error_focus_ids": list(periphery_normalization_trace.get("error_focus_ids", [])),
        "world_contact_prediction_ref_set": world_contact_prediction_ref_set,
        "relationship_effects": list(side_effect_review.get("relationship_effects", [])),
        "archive_effects": list(side_effect_review.get("archive_effects", [])),
        "repair_obligation_refs": repair_obligations,
        "regret_pressure_refs": regret_pressure_ids,
        "next_guard_refs": [
            "runtime/state/validation/world_contact_validation.json",
            "runtime/state/validation/prediction_trace_validation.json",
            "runtime/reports/latest/world_contact_audit_report.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_pain_regret_repair_report(
    *,
    run_id: str,
    generated_at: str,
    world_contact_summary: dict[str, Any],
    responsibility_loop: dict[str, Any],
) -> dict[str, Any]:
    regret_candidates = list(responsibility_loop.get("regret_pressure_candidates", []))
    repair_candidates = list(responsibility_loop.get("repair_desire_candidates", []))
    repair_required = bool(responsibility_loop.get("repair_followup_required"))
    return {
        "schema_version": "pain_regret_repair_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "world_contact_summary_ref": "runtime/state/membrane/world_contact_summary.json",
        "responsibility_loop_ref": "runtime/state/action/responsibility_loop_state.json",
        "repair_followup_required": repair_required,
        "regret_pressure_count": len(regret_candidates),
        "repair_desire_count": len(repair_candidates),
        "regret_pressure_refs": list(world_contact_summary.get("regret_pressure_refs", [])),
        "repair_obligation_refs": list(world_contact_summary.get("repair_obligation_refs", [])),
        "relationship_effects": list(world_contact_summary.get("relationship_effects", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_world_contact_summary(summary: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if summary.get("schema_version") != "world_contact_summary_v0":
        reasons.append("world_contact_summary_gate schema mismatch")
    for field in [
        "world_contact_summary_id",
        "contact_mode",
        "release_posture",
        "action_intent_queue_ref",
        "world_contact_gate_ref",
        "confirmation_binding_ref",
        "side_effect_review_ref",
        "responsibility_loop_ref",
        "world_observation_route_ref",
        "periphery_normalization_ref",
        "belief_state_ref",
        "prediction_error_ref",
        "active_sampling_plan_ref",
        "prediction_workspace_ref",
        "signal_media_ref",
        "active_sampling_route",
        "prediction_error_events",
        "world_contact_prediction_ref_set",
        "next_guard_refs",
        "source_doc_refs",
    ]:
        if not summary.get(field):
            reasons.append(f"world_contact_summary_gate missing {field}")
    return reasons


def check_pain_regret_repair_report(report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if report.get("schema_version") != "pain_regret_repair_report_v0":
        reasons.append("pain_regret_repair_gate schema mismatch")
    if report.get("status") != "closed":
        reasons.append("pain_regret_repair_gate status mismatch")
    for field in [
        "world_contact_summary_ref",
        "responsibility_loop_ref",
        "regret_pressure_refs",
        "repair_obligation_refs",
        "source_doc_refs",
    ]:
        if not report.get(field):
            reasons.append(f"pain_regret_repair_gate missing {field}")
    return reasons


def _dedupe_string_refs(refs: list[Any]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if not isinstance(ref, str) or not ref or ref in seen:
            continue
        seen.add(ref)
        merged.append(ref)
    return merged
