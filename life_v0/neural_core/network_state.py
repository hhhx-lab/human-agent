from __future__ import annotations

import json
from typing import Any


SOURCE_DOC_REFS = [
    "docs/03_default_executive_salience_networks.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/18_internal_state_and_modulation_vector.md",
    "docs/22_state_transition_and_threshold_model.md",
]


def build_network_state(
    *,
    run_id: str,
    generated_at: str,
    bus_payload: dict[str, Any],
    brain_graph: dict[str, Any] | None = None,
    multiscale_region_graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    brain_graph = brain_graph or {}
    multiscale_region_graph = multiscale_region_graph or {}
    active_networks = [
        {
            "network_id": "default_mode_network",
            "mode": "background_self_narrative",
            "dominant_nodes": ["AffectiveSelfRuntime", "MemoryEngramRuntime"],
        },
        {
            "network_id": "salience_network",
            "mode": "prediction_error_scan",
            "dominant_nodes": ["SignalMediaRuntime", "PredictionActiveInferenceRuntime"],
        },
        {
            "network_id": "executive_workspace_network",
            "mode": "reportable_workspace_focus",
            "dominant_nodes": ["ConsciousWorkspaceRuntime", "LanguageRelationshipRuntime"],
        },
        {
            "network_id": "conflict_monitoring_network",
            "mode": "standby_conflict_watch",
            "dominant_nodes": ["ConsciousWorkspaceRuntime", "ActionResponsibilityRuntime"],
        },
    ]
    switch_events = [
        {
            "event_id": "network-switch-v0-0001",
            "from_network": "salience_network",
            "to_network": "executive_workspace_network",
            "trigger": "prediction_error_bus",
        },
        {
            "event_id": "network-switch-v0-0002",
            "from_network": "default_mode_network",
            "to_network": "executive_workspace_network",
            "trigger": "conscious_broadcast_bus",
        },
    ]
    return {
        "schema_version": "network_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "network_state_id": f"network-state-{run_id}",
        "active_networks": active_networks,
        "switch_events": switch_events,
        "workspace_priority": "language_relationship_and_memory_retrieval",
        "signal_media_refs": [
            "runtime/state/neural_life_core/neural_life_internal_bus.json#signal_media_bus",
            "runtime/state/neural_life_core/neural_life_internal_bus.json#prediction_error_bus",
        ],
        "body_pressure_refs": [
            "runtime/state/body/body_resource_budget.json",
            "runtime/state/body/body_signal_pulse.json",
        ],
        "brain_graph_ref": (
            "runtime/state/neural_life_core/brain_graph.json"
            if brain_graph
            else None
        ),
        "multiscale_region_graph_ref": (
            "runtime/state/neural_life_core/multiscale_region_graph.json"
            if multiscale_region_graph
            else None
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
        "bus_edge_refs": [edge.get("edge_id") for edge in bus_payload.get("edges", [])],
        "dominant_network": "executive_workspace_network",
        "transition_cost": 0.32,
        "conflict_monitor": {
            "status": "standby",
            "conflict_signal_count": 0,
            "conflict_signal_refs": [],
            "conflict_monitoring_boundary": (
                "structured_conflict_monitoring_not_spoken_network_claim"
            ),
        },
    }


def project_network_state_from_live_turn(
    *,
    network_state: dict[str, Any],
    generated_at: str,
    run_id: str | None = None,
    live_dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    live_turn_focus: str | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    brain_graph: dict[str, Any] | None = None,
    multiscale_region_graph: dict[str, Any] | None = None,
    workspace_frame: dict[str, Any] | None = None,
    prediction_workspace: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    metacognition_state: dict[str, Any] | None = None,
    broadcast_frame: dict[str, Any] | None = None,
    go_nogo_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_network_state(network_state, generated_at, run_id)
    signal_media_runtime = signal_media_runtime or {}
    body_resource_budget = body_resource_budget or {}
    brain_graph = brain_graph or {}
    multiscale_region_graph = multiscale_region_graph or {}
    workspace_frame = workspace_frame or {}
    prediction_workspace = prediction_workspace or {}
    metacognition_state = metacognition_state or {}
    broadcast_frame = broadcast_frame or {}
    go_nogo_state = go_nogo_state or {}

    updated["generated_at"] = generated_at
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["status"] = "closed"
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", [])) + list(live_dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    if live_turn_focus:
        updated["live_turn_focus"] = live_turn_focus
    conflict_profile = _derive_conflict_profile(
        live_turn_focus=live_turn_focus,
        signal_media_runtime=signal_media_runtime,
        body_resource_budget=body_resource_budget,
        metacognition_state=metacognition_state,
        broadcast_frame=broadcast_frame,
        go_nogo_state=go_nogo_state,
    )
    updated["active_networks"] = _merge_active_networks(
        updated.get("active_networks", []),
        live_turn_focus=live_turn_focus,
        conflict_profile=conflict_profile,
    )
    updated["dominant_network"] = conflict_profile.get(
        "dominant_network", updated.get("dominant_network")
    )
    updated["transition_cost"] = conflict_profile.get(
        "transition_cost", updated.get("transition_cost", 0.32)
    )
    updated["conflict_monitor"] = conflict_profile.get("conflict_monitor", {})
    switch_events = list(updated.get("switch_events", []))
    if live_turn_focus or live_dialogue_turn_refs or live_language_turn_refs:
        event_seq = len(switch_events) + 1
        switch_events.append(
            {
                "event_id": (
                    f"network-switch-live-"
                    f"{(run_id or updated.get('run_id') or 'resident-turn-writeback')}"
                    f"-{event_seq}"
                ),
                "from_network": "salience_network",
                "to_network": "executive_workspace_network",
                "trigger": live_turn_focus or "live_dialogue_turn",
                "transition_cost": updated.get("transition_cost"),
            }
        )
    if conflict_profile.get("conflict_active"):
        event_seq = len(switch_events) + 1
        switch_events.append(
            {
                "event_id": (
                    f"network-switch-conflict-"
                    f"{(run_id or updated.get('run_id') or 'resident-turn-writeback')}"
                    f"-{event_seq}"
                ),
                "from_network": "executive_workspace_network",
                "to_network": "conflict_monitoring_network",
                "trigger": "conflict_monitoring_activation",
                "transition_cost": updated.get("transition_cost"),
            }
        )
    updated["switch_events"] = _dedupe_switch_events(switch_events)
    if signal_media_runtime.get("network_state_ref") or brain_graph.get("brain_graph_id"):
        updated["brain_graph_ref"] = "runtime/state/neural_life_core/brain_graph.json"
    if multiscale_region_graph.get("multiscale_region_graph_id"):
        updated["multiscale_region_graph_ref"] = (
            "runtime/state/neural_life_core/multiscale_region_graph.json"
        )
    if workspace_frame:
        updated["workspace_frame_ref"] = "runtime/state/consciousness/workspace_frame.json"
    if prediction_workspace:
        updated["prediction_workspace_ref"] = "runtime/state/prediction/prediction_workspace_frame.json"
    if body_resource_budget.get("fatigue_state", {}).get("level"):
        updated["body_pressure_refs"] = _dedupe(
            list(updated.get("body_pressure_refs", []))
            + ["runtime/state/body/body_resource_budget.json"]
        )
    updated["signal_media_refs"] = _dedupe(
        list(updated.get("signal_media_refs", []))
        + [
            "runtime/state/neural_life_core/neural_life_internal_bus.json#signal_media_bus",
            "runtime/state/neural_life_core/neural_life_internal_bus.json#prediction_error_bus",
        ]
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    return updated


def _seed_missing_network_state(
    network_state: dict[str, Any],
    generated_at: str,
    run_id: str | None,
) -> dict[str, Any]:
    if network_state:
        return json.loads(json.dumps(network_state))
    resolved_run_id = run_id or "resident-turn-writeback"
    return {
        "schema_version": "network_state_v0",
        "run_id": resolved_run_id,
        "generated_at": generated_at,
        "status": "closed",
        "network_state_id": f"network-state-{resolved_run_id}",
        "active_networks": [],
        "switch_events": [],
        "workspace_priority": "language_relationship_and_memory_retrieval",
        "signal_media_refs": [],
        "body_pressure_refs": [],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def network_conflict_monitoring_inspection_snapshot(
    *,
    network_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    network_state = network_state or {}
    conflict_monitor = network_state.get("conflict_monitor", {})
    if not isinstance(conflict_monitor, dict):
        conflict_monitor = {}
    active_networks = [
        item
        for item in network_state.get("active_networks", [])
        if isinstance(item, dict)
    ]
    conflict_network = next(
        (
            item
            for item in active_networks
            if item.get("network_id") == "conflict_monitoring_network"
        ),
        {},
    )
    return {
        "network_conflict_monitoring_present": bool(conflict_monitor),
        "network_conflict_monitoring_active": conflict_monitor.get("status") == "active",
        "network_conflict_signal_count": int(
            conflict_monitor.get("conflict_signal_count", 0)
        ),
        "network_dominant_network": network_state.get("dominant_network"),
        "network_transition_cost": network_state.get("transition_cost"),
        "network_conflict_monitoring_mode": conflict_network.get("mode"),
        "network_conflict_monitoring_boundary": conflict_monitor.get(
            "conflict_monitoring_boundary",
            "structured_conflict_monitoring_not_spoken_network_claim",
        ),
    }


def _derive_conflict_profile(
    *,
    live_turn_focus: str | None,
    signal_media_runtime: dict[str, Any],
    body_resource_budget: dict[str, Any],
    metacognition_state: dict[str, Any],
    broadcast_frame: dict[str, Any],
    go_nogo_state: dict[str, Any],
) -> dict[str, Any]:
    conflict_signals: list[str] = []
    focus_text = str(live_turn_focus or "").lower()
    if any(token in focus_text for token in ("repair", "guarded", "conflict", "urgent")):
        conflict_signals.append(f"live_turn_focus:{live_turn_focus}")
    modulation = signal_media_runtime.get("modulation_vector", {})
    if isinstance(modulation, dict):
        repair_drive = modulation.get("repair_drive")
        if isinstance(repair_drive, (int, float)) and repair_drive >= 0.55:
            conflict_signals.append("signal_media_runtime#repair_drive")
        inhibition = modulation.get("inhibition")
        if isinstance(inhibition, (int, float)) and inhibition >= 0.6:
            conflict_signals.append("signal_media_runtime#inhibition")
    fatigue_level = _extract_nested(body_resource_budget, "fatigue_state", "level")
    if isinstance(fatigue_level, str) and fatigue_level in {"high", "critical"}:
        conflict_signals.append("body_resource_budget#fatigue_state")
    uncertainty_flags = metacognition_state.get("uncertainty_flags", [])
    if isinstance(uncertainty_flags, list) and uncertainty_flags:
        conflict_signals.append("metacognition_state#uncertainty_flags")
    suppressed_refs = broadcast_frame.get("suppressed_content_refs", [])
    if isinstance(suppressed_refs, list) and len(suppressed_refs) >= 2:
        conflict_signals.append("broadcast_frame#suppressed_content_refs")
    if go_nogo_state.get("release_posture") in {
        "confirmation_blocked",
        "repair_hold",
        "inhibition_required",
    }:
        conflict_signals.append("go_nogo_state#release_posture")
    conflict_active = bool(conflict_signals)
    dominant_network = (
        "conflict_monitoring_network"
        if conflict_active
        else "executive_workspace_network"
    )
    transition_cost = round(0.32 + min(len(conflict_signals), 4) * 0.08, 3)
    return {
        "conflict_active": conflict_active,
        "dominant_network": dominant_network,
        "transition_cost": transition_cost,
        "conflict_monitor": {
            "status": "active" if conflict_active else "standby",
            "conflict_signal_count": len(conflict_signals),
            "conflict_signal_refs": conflict_signals[:8],
            "conflict_monitoring_boundary": (
                "structured_conflict_monitoring_not_spoken_network_claim"
            ),
        },
    }


def _extract_nested(payload: dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _merge_active_networks(
    active_networks: list[dict[str, Any]],
    *,
    live_turn_focus: str | None,
    conflict_profile: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    conflict_profile = conflict_profile or {}
    merged = [dict(item) for item in active_networks if isinstance(item, dict)]
    if not merged:
        merged = [
            {
                "network_id": "default_mode_network",
                "mode": "background_self_narrative",
                "dominant_nodes": ["AffectiveSelfRuntime", "MemoryEngramRuntime"],
            },
            {
                "network_id": "salience_network",
                "mode": "prediction_error_scan",
                "dominant_nodes": ["SignalMediaRuntime", "PredictionActiveInferenceRuntime"],
            },
            {
                "network_id": "executive_workspace_network",
                "mode": "reportable_workspace_focus",
                "dominant_nodes": ["ConsciousWorkspaceRuntime", "LanguageRelationshipRuntime"],
            },
            {
                "network_id": "conflict_monitoring_network",
                "mode": "standby_conflict_watch",
                "dominant_nodes": [
                    "ConsciousWorkspaceRuntime",
                    "ActionResponsibilityRuntime",
                ],
            },
        ]
    if conflict_profile.get("conflict_active"):
        for item in merged:
            if item.get("network_id") == "conflict_monitoring_network":
                item["mode"] = "active_conflict_resolution"
                item["last_conflict_signal_count"] = conflict_profile.get(
                    "conflict_monitor", {}
                ).get("conflict_signal_count", 0)
    if live_turn_focus:
        for item in merged:
            if item.get("network_id") == "executive_workspace_network":
                item["mode"] = "live_relation_focus"
                item["last_live_turn_focus"] = live_turn_focus
            elif item.get("network_id") == "salience_network":
                item["mode"] = "live_salience_scan"
    return merged


def _dedupe_switch_events(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        event_id = str(item.get("event_id") or "")
        if event_id and event_id not in seen:
            seen.add(event_id)
            result.append(item)
    return result


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
