from __future__ import annotations

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
) -> dict[str, Any]:
    brain_graph = brain_graph or {}
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
        "source_doc_refs": SOURCE_DOC_REFS,
        "bus_edge_refs": [edge.get("edge_id") for edge in bus_payload.get("edges", [])],
    }
