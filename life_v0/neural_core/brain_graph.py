from __future__ import annotations

import json
from typing import Any


SOURCE_DOC_REFS = [
    "docs/02_brain_region_and_network_atlas.md",
    "docs/03_default_executive_salience_networks.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
]


def build_brain_graph(
    *,
    run_id: str,
    generated_at: str,
    systems_payload: dict[str, Any],
    bus_payload: dict[str, Any],
) -> dict[str, Any]:
    systems = list(systems_payload.get("systems", []))
    region_nodes = [
        {
            "node_id": system.get("system_id"),
            "body_layer": system.get("body_layer"),
            "state_namespace": system.get("state_namespace"),
            "runtime_carriers": list(system.get("runtime_carriers", [])),
            "life_targets": list(system.get("life_targets", [])),
        }
        for system in systems
    ]
    functional_edges = [
        {
            "edge_id": edge.get("edge_id"),
            "from_node": edge.get("from_system"),
            "to_node": edge.get("to_system"),
            "payload_family": edge.get("payload_family"),
            "life_targets": list(edge.get("life_targets", [])),
        }
        for edge in bus_payload.get("edges", [])
    ]
    carrier_refs = sorted(
        {
            carrier
            for system in systems
            for carrier in system.get("runtime_carriers", [])
        }
    )
    life_target_bindings = {
        target: [
            system.get("system_id")
            for system in systems
            if target in system.get("life_targets", [])
        ]
        for target in sorted(
            {
                target
                for system in systems
                for target in system.get("life_targets", [])
            }
        )
    }
    return {
        "schema_version": "brain_graph_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "brain_graph_id": f"brain-graph-{run_id}",
        "region_nodes": region_nodes,
        "functional_edges": functional_edges,
        "carrier_refs": carrier_refs,
        "source_doc_refs": SOURCE_DOC_REFS,
        "life_target_bindings": life_target_bindings,
    }


def project_brain_graph_from_live_turn(
    *,
    brain_graph: dict[str, Any],
    generated_at: str,
    run_id: str | None = None,
    dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    workspace_frame: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_brain_graph(brain_graph, generated_at, run_id)
    relationship_graph = relationship_graph or {}
    relationship_timeline = relationship_timeline or {}
    self_model_state = self_model_state or {}
    network_state = network_state or {}
    workspace_frame = workspace_frame or {}

    updated["generated_at"] = generated_at
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["status"] = "closed"
    updated["live_dialogue_turn_refs"] = _dedupe(
        list(updated.get("live_dialogue_turn_refs", [])) + list(dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    updated["network_state_ref"] = "runtime/state/neural_life_core/network_state.json"
    updated["workspace_frame_ref"] = "runtime/state/consciousness/workspace_frame.json"
    updated["prediction_workspace_ref"] = "runtime/state/prediction/prediction_workspace_frame.json"
    updated["carrier_refs"] = _dedupe(
        list(updated.get("carrier_refs", []))
        + [
            ref
            for ref in [
                updated.get("network_state_ref"),
                updated.get("workspace_frame_ref"),
                updated.get("prediction_workspace_ref"),
            ]
            if ref
        ]
    )
    live_focus: dict[str, Any] = {}
    subject = next(
        (
            item
            for item in relationship_graph.get("subjects", [])
            if isinstance(item, dict)
        ),
        {},
    )
    if subject.get("relationship_stage"):
        live_focus["relationship_stage"] = subject["relationship_stage"]
    if relationship_timeline.get("relationship_continuity_reports"):
        live_focus["continuity_state"] = relationship_timeline[
            "relationship_continuity_reports"
        ][0].get("continuity_state")
    if self_model_state.get("trait_slow_variables"):
        live_focus["trait_names"] = sorted(self_model_state["trait_slow_variables"].keys())
    if live_focus:
        updated["live_turn_focus"] = live_focus
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    return updated


def _seed_missing_brain_graph(
    brain_graph: dict[str, Any],
    generated_at: str,
    run_id: str | None,
) -> dict[str, Any]:
    if brain_graph:
        return json.loads(json.dumps(brain_graph))
    resolved_run_id = run_id or "resident-turn-writeback"
    return {
        "schema_version": "brain_graph_v0",
        "run_id": resolved_run_id,
        "generated_at": generated_at,
        "status": "closed",
        "brain_graph_id": f"brain-graph-{resolved_run_id}",
        "region_nodes": [],
        "functional_edges": [],
        "carrier_refs": [],
        "source_doc_refs": SOURCE_DOC_REFS,
        "life_target_bindings": {},
    }


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
