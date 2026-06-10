from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/22_state_transition_and_threshold_model.md",
    "docs/64_real_runtime_observation_ingestion_policy.md",
    "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md",
]


def build_periphery_normalization_trace(
    *,
    run_id: str,
    generated_at: str,
    world_observation_route: dict[str, Any],
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    need_state: dict[str, Any] | None = None,
    core_affect: dict[str, Any] | None = None,
) -> dict[str, Any]:
    belief_state = belief_state or {}
    prediction_error_field = prediction_error_field or {}
    signal_media_runtime = signal_media_runtime or {}
    need_state = need_state or {}
    core_affect = core_affect or {}

    modulation = signal_media_runtime.get("modulation_vector", {})
    fatigue_load = modulation.get("fatigue_load", 0.26)
    relationship_pressure = modulation.get("relationship_pressure", 0.29)
    error_events = list(prediction_error_field.get("error_events", []))
    prioritized_channels = list(world_observation_route.get("prioritized_channels", []))

    normalized_channels: list[dict[str, Any]] = []
    promoted_channels: list[str] = []
    suppressed_channels: list[str] = []
    deferred_channels: list[str] = []
    for channel in prioritized_channels:
        channel_id = channel.get("channel_id")
        priority = channel.get("priority", "medium")
        if not channel_id:
            continue
        mode = _normalization_mode(
            channel_id=channel_id,
            priority=priority,
            fatigue_load=fatigue_load,
            relationship_pressure=relationship_pressure,
        )
        weight = _normalization_weight(
            mode=mode,
            priority=priority,
            fatigue_load=fatigue_load,
            relationship_pressure=relationship_pressure,
        )
        normalized_channels.append(
            {
                "channel_id": channel_id,
                "source_ref": channel.get("ref"),
                "priority": priority,
                "normalization_mode": mode,
                "weight": weight,
            }
        )
        if mode == "promote":
            promoted_channels.append(channel_id)
        elif mode == "suppress":
            suppressed_channels.append(channel_id)
        else:
            deferred_channels.append(channel_id)

    return {
        "schema_version": "periphery_normalization_trace_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "periphery_normalization_id": f"periphery-normalization-{run_id}",
        "world_observation_route_ref": "runtime/state/observation/world_observation_route.json",
        "belief_state_ref": (
            "runtime/state/prediction/belief_state_frame.json" if belief_state else None
        ),
        "prediction_error_ref": (
            "runtime/state/prediction/prediction_error_field.json"
            if prediction_error_field
            else None
        ),
        "signal_media_ref": (
            "runtime/state/signal/signal_media_runtime.json"
            if signal_media_runtime
            else None
        ),
        "normalization_policy": "belief_error_guarded_periphery",
        "normalized_channels": normalized_channels,
        "promoted_channels": promoted_channels,
        "suppressed_channels": suppressed_channels,
        "deferred_channels": deferred_channels,
        "error_focus_ids": [
            event.get("error_id")
            for event in error_events
            if isinstance(event, dict) and event.get("error_id")
        ],
        "body_pressure": {
            "fatigue_load": fatigue_load,
            "allostatic_load": need_state.get("allostatic_load", 0.18),
            "pain_pressure": core_affect.get("pain_pressure", 0.11),
            "relationship_pressure": relationship_pressure,
        },
        "write_target_refs": [
            "runtime/state/observation/runtime_observation_intake.json",
            "runtime/state/action/side_effect_review.json",
            "runtime/state/membrane/world_contact_summary.json",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_periphery_normalization_trace(trace: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if trace.get("schema_version") != "periphery_normalization_trace_v0":
        reasons.append("periphery_normalization_gate schema mismatch")
    required_values = [
        "periphery_normalization_id",
        "world_observation_route_ref",
        "normalization_policy",
        "normalized_channels",
        "body_pressure",
        "write_target_refs",
        "source_doc_refs",
    ]
    for field in required_values:
        if not trace.get(field):
            reasons.append(f"periphery_normalization_gate missing {field}")
    for field in ["promoted_channels", "suppressed_channels", "deferred_channels"]:
        if field not in trace:
            reasons.append(f"periphery_normalization_gate missing {field}")
    if trace.get("world_observation_route_ref") != "runtime/state/observation/world_observation_route.json":
        reasons.append("periphery_normalization_gate world observation ref mismatch")
    return reasons


def _normalization_mode(
    *,
    channel_id: str,
    priority: str,
    fatigue_load: float,
    relationship_pressure: float,
) -> str:
    if channel_id in {"commitment_truth_state", "relation_scope_language_index", "semantic_map_state"}:
        return "promote"
    if fatigue_load >= 0.4 and channel_id in {"dialogue_turn_log", "language_percept_state"}:
        return "defer"
    if relationship_pressure >= 0.25 and channel_id in {"dialogue_turn_log", "language_percept_state"}:
        return "promote" if priority == "high" else "defer"
    return "defer" if priority == "medium" else "suppress"


def _normalization_weight(
    *,
    mode: str,
    priority: str,
    fatigue_load: float,
    relationship_pressure: float,
) -> float:
    base = 0.55 if priority == "high" else 0.42
    if mode == "promote":
        return round(min(0.95, base + relationship_pressure), 2)
    if mode == "defer":
        return round(max(0.15, base - fatigue_load / 2), 2)
    return round(max(0.05, base - fatigue_load), 2)
