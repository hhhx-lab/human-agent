from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/22_state_transition_and_threshold_model.md",
    "docs/64_real_runtime_observation_ingestion_policy.md",
    "docs/68_runtime_observation_report_mock_and_redaction_fixture.md",
    "docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]


def build_world_observation_route(
    *,
    run_id: str,
    generated_at: str,
    active_sampling_plan: dict[str, Any],
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    prediction_workspace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    belief_state = belief_state or {}
    prediction_error_field = prediction_error_field or {}
    signal_media_runtime = signal_media_runtime or {}
    prediction_workspace = prediction_workspace or {}

    modulation = signal_media_runtime.get("modulation_vector", {})
    unexpected_uncertainty = modulation.get("unexpected_uncertainty", 0.21)
    relationship_pressure = modulation.get("relationship_pressure", 0.29)
    selected_route = active_sampling_plan.get("selected_route", "clarify")
    route_mode = "clarify_before_release" if selected_route == "clarify" else "inspect_before_release"
    expected_refs = list(active_sampling_plan.get("expected_observation_refs", []))
    scope_refs = list(active_sampling_plan.get("scope_refs", []))
    workspace_focus = prediction_workspace.get("workspace_contents", {}).get("language_continuity_focus", {})
    channel_seed_refs = (
        expected_refs
        + scope_refs
        + list(workspace_focus.get("dialogue_turn_log_refs", []))
        + list(workspace_focus.get("language_percept_refs", []))
        + list(workspace_focus.get("semantic_map_refs", []))
    )
    observation_targets = _dedupe(channel_seed_refs)
    error_events = list(prediction_error_field.get("error_events", []))
    prioritized_channels = [
        {
            "channel_id": _channel_id_from_ref(ref),
            "ref": ref,
            "priority": _priority_for_ref(
                ref=ref,
                selected_route=selected_route,
                unexpected_uncertainty=unexpected_uncertainty,
                relationship_pressure=relationship_pressure,
            ),
            "reason": _reason_for_ref(ref=ref, selected_route=selected_route),
        }
        for ref in observation_targets
    ]

    return {
        "schema_version": "world_observation_route_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "world_observation_route_id": f"world-observation-route-{run_id}",
        "selected_route": selected_route,
        "route_mode": route_mode,
        "active_sampling_plan_ref": "runtime/state/prediction/active_sampling_plan.json",
        "belief_state_ref": (
            "runtime/state/prediction/belief_state_frame.json" if belief_state else None
        ),
        "prediction_error_ref": (
            "runtime/state/prediction/prediction_error_field.json"
            if prediction_error_field
            else None
        ),
        "prediction_workspace_ref": (
            "runtime/state/prediction/prediction_workspace_frame.json"
            if prediction_workspace
            else None
        ),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "guard_refs": list(active_sampling_plan.get("guard_refs", [])),
        "command_binding_refs": list(active_sampling_plan.get("command_binding_refs", [])),
        "observation_targets": observation_targets,
        "prioritized_channels": prioritized_channels,
        "error_focus_ids": [
            event.get("error_id")
            for event in error_events
            if isinstance(event, dict) and event.get("error_id")
        ],
        "relationship_pressure": relationship_pressure,
        "unexpected_uncertainty": unexpected_uncertainty,
        "observation_status": "shadow_observation_only",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_world_observation_route(route: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if route.get("schema_version") != "world_observation_route_v0":
        reasons.append("world_observation_gate schema mismatch")
    for field in [
        "world_observation_route_id",
        "selected_route",
        "route_mode",
        "active_sampling_plan_ref",
        "guard_refs",
        "command_binding_refs",
        "observation_targets",
        "prioritized_channels",
        "observation_status",
        "source_doc_refs",
    ]:
        if not route.get(field):
            reasons.append(f"world_observation_gate missing {field}")
    if "runtime/state/prediction/active_sampling_plan.json" != route.get("active_sampling_plan_ref"):
        reasons.append("world_observation_gate active sampling ref mismatch")
    return reasons


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def _channel_id_from_ref(ref: str) -> str:
    tail = ref.split("/")[-1]
    return tail.replace(".json", "").replace(".jsonl", "")


def _priority_for_ref(
    *,
    ref: str,
    selected_route: str,
    unexpected_uncertainty: float,
    relationship_pressure: float,
) -> str:
    ref = ref.lower()
    if "commitment_truth" in ref or "relation" in ref:
        return "high" if relationship_pressure >= 0.25 else "medium"
    if "semantic" in ref or "dialogue" in ref or "percept" in ref:
        return "high" if selected_route == "clarify" or unexpected_uncertainty >= 0.2 else "medium"
    return "medium"


def _reason_for_ref(*, ref: str, selected_route: str) -> str:
    ref = ref.lower()
    if "commitment_truth" in ref:
        return "repair_and_commitment_truth_check"
    if "relation" in ref:
        return "relationship_scope_recheck"
    if "semantic" in ref:
        return "semantic_ambiguity_resolution"
    if "dialogue" in ref or "percept" in ref:
        return "current_turn_observation_refresh"
    return f"{selected_route}_route_default"
