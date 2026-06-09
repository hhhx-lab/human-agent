from __future__ import annotations

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
