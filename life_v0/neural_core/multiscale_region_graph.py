from __future__ import annotations

import json
from typing import Any

SOURCE_DOC_REFS = [
    "docs/01o_multiscale_region_connectome_matrix.md",
    "docs/02_brain_region_and_network_atlas.md",
    "docs/03_default_executive_salience_networks.md",
    "docs/10_consciousness_attention_workspace.md",
]

MULTISCALE_REGION_GRAPH_BOUNDARY = (
    "structured_multiscale_region_graph_not_spoken_brain_atlas"
)

REGION_SPECS: list[dict[str, Any]] = [
    {
        "project_code": "L",
        "region_label": "LanguageNetwork",
        "scale_layer": "network",
        "system_id": "LanguageRelationshipRuntime",
        "cortical_gradient_coordinate": 0.72,
        "intrinsic_timescale": "seconds_to_minutes",
        "hierarchical_depth": "cross_modal_integration",
        "dynamical_stability": "task_dependent",
        "transition_control_cost": 0.35,
        "allowed_overlap": ["P", "O", "S"],
        "receptor_modulation_prior": {
            "language_precision": "high",
            "repair_drive": "medium",
            "arousal": "medium",
        },
    },
    {
        "project_code": "R",
        "region_label": "ReticularRelay",
        "scale_layer": "network",
        "system_id": "ComputerPeripheralRuntime",
        "cortical_gradient_coordinate": 0.18,
        "intrinsic_timescale": "milliseconds_to_seconds",
        "hierarchical_depth": "low_level_perception",
        "dynamical_stability": "fast_switching",
        "transition_control_cost": 0.22,
        "allowed_overlap": ["J", "G"],
        "receptor_modulation_prior": {
            "arousal": "high",
            "precision": "high",
        },
    },
    {
        "project_code": "P",
        "region_label": "ExecutiveWorkspace",
        "scale_layer": "network",
        "system_id": "ConsciousWorkspaceRuntime",
        "cortical_gradient_coordinate": 0.81,
        "intrinsic_timescale": "seconds_to_minutes",
        "hierarchical_depth": "metacognitive_self_narrative",
        "dynamical_stability": "moderate",
        "transition_control_cost": 0.48,
        "allowed_overlap": ["L", "O", "D"],
        "receptor_modulation_prior": {
            "inhibition": "high",
            "uncertainty": "high",
            "repair_drive": "medium",
        },
    },
    {
        "project_code": "J",
        "region_label": "ThalamicRouting",
        "scale_layer": "parcel",
        "system_id": "MultiscaleBrainGraphRuntime",
        "cortical_gradient_coordinate": 0.42,
        "intrinsic_timescale": "milliseconds_to_seconds",
        "hierarchical_depth": "cross_modal_integration",
        "dynamical_stability": "relay_gated",
        "transition_control_cost": 0.30,
        "allowed_overlap": ["R", "G", "O", "S"],
        "receptor_modulation_prior": {
            "arousal": "high",
            "value": "medium",
        },
    },
    {
        "project_code": "G",
        "region_label": "BrainstemArousal",
        "scale_layer": "whole_system",
        "system_id": "SignalMediaRuntime",
        "cortical_gradient_coordinate": 0.12,
        "intrinsic_timescale": "milliseconds_to_minutes",
        "hierarchical_depth": "low_level_perception",
        "dynamical_stability": "rhythmic",
        "transition_control_cost": 0.18,
        "allowed_overlap": ["J", "R", "D"],
        "receptor_modulation_prior": {
            "arousal": "high",
            "consolidation_pressure": "medium",
        },
    },
    {
        "project_code": "S",
        "region_label": "CerebellarPrediction",
        "scale_layer": "network",
        "system_id": "PredictionActiveInferenceRuntime",
        "cortical_gradient_coordinate": 0.55,
        "intrinsic_timescale": "milliseconds_to_seconds",
        "hierarchical_depth": "low_level_perception",
        "dynamical_stability": "error_correcting",
        "transition_control_cost": 0.28,
        "allowed_overlap": ["J", "L", "D"],
        "receptor_modulation_prior": {
            "precision": "high",
            "uncertainty": "high",
        },
    },
    {
        "project_code": "O",
        "region_label": "AffectiveSelfNarrative",
        "scale_layer": "network",
        "system_id": "AffectiveSelfRuntime",
        "cortical_gradient_coordinate": 0.76,
        "intrinsic_timescale": "minutes_to_days",
        "hierarchical_depth": "metacognitive_self_narrative",
        "dynamical_stability": "slow_variable_sensitive",
        "transition_control_cost": 0.52,
        "allowed_overlap": ["P", "L", "D"],
        "receptor_modulation_prior": {
            "repair_drive": "high",
            "value": "high",
            "pain_pressure": "high",
        },
    },
    {
        "project_code": "D",
        "region_label": "ActionSelection",
        "scale_layer": "network",
        "system_id": "ActionResponsibilityRuntime",
        "cortical_gradient_coordinate": 0.34,
        "intrinsic_timescale": "seconds_to_minutes",
        "hierarchical_depth": "cross_modal_integration",
        "dynamical_stability": "inhibition_gated",
        "transition_control_cost": 0.44,
        "allowed_overlap": ["P", "O", "G", "S"],
        "receptor_modulation_prior": {
            "inhibition": "high",
            "repair_drive": "high",
        },
    },
]

STRUCTURAL_EDGE_SPECS: list[tuple[str, str, str, float]] = [
    ("J", "R", "thalamic_relay_to_peripheral", 0.82),
    ("J", "G", "brainstem_arousal_route", 0.74),
    ("J", "S", "prediction_error_route", 0.71),
    ("J", "O", "affective_salience_route", 0.69),
    ("S", "P", "prediction_to_workspace", 0.66),
    ("O", "P", "affect_to_executive", 0.64),
    ("L", "P", "language_to_workspace", 0.63),
    ("D", "P", "action_to_executive", 0.58),
    ("G", "D", "arousal_to_action_gate", 0.55),
    ("O", "L", "affect_to_language", 0.52),
]


def build_multiscale_region_graph(
    *,
    run_id: str,
    generated_at: str,
    systems_payload: dict[str, Any],
    bus_payload: dict[str, Any],
    brain_graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    brain_graph = brain_graph or {}
    systems = list(systems_payload.get("systems", []))
    system_by_id = {
        system.get("system_id"): system
        for system in systems
        if isinstance(system, dict) and system.get("system_id")
    }
    region_definitions = []
    for spec in REGION_SPECS:
        system = system_by_id.get(spec["system_id"], {})
        region_definitions.append(
            {
                "region_id": f"region-{spec['project_code'].lower()}-{run_id}",
                "project_code": spec["project_code"],
                "region_label": spec["region_label"],
                "scale_layer": spec["scale_layer"],
                "system_id": spec["system_id"],
                "boundary_confidence": 0.78,
                "parcel_evidence_refs": _dedupe(
                    list(system.get("authority_refs", []))[:4]
                    + list(system.get("source_doc_refs", []))[:2]
                    + [f"runtime/state/neural_life_core/brain_graph.json#{spec['system_id']}"]
                ),
                "allowed_overlap": list(spec["allowed_overlap"]),
                "state_dependency": {
                    "relationship_repair": spec["project_code"] in {"O", "L", "D"},
                    "dream_offline": spec["project_code"] in {"O", "G"},
                    "live_dialogue": spec["project_code"] in {"L", "P", "J"},
                },
                "cortical_gradient_coordinate": spec["cortical_gradient_coordinate"],
                "intrinsic_timescale": spec["intrinsic_timescale"],
                "hierarchical_depth": spec["hierarchical_depth"],
                "dynamical_stability": spec["dynamical_stability"],
                "transition_control_cost": spec["transition_control_cost"],
                "cell_type_state_prior": _cell_type_prior(spec["project_code"]),
                "receptor_modulation_prior": dict(spec["receptor_modulation_prior"]),
            }
        )
    structural_edges = [
        {
            "edge_id": f"structural-{from_code.lower()}-{to_code.lower()}-{run_id}",
            "from_project_code": from_code,
            "to_project_code": to_code,
            "edge_kind": edge_kind,
            "bandwidth": round(bandwidth, 3),
            "directionality": "directed",
            "long_term_reliability": round(min(bandwidth + 0.08, 0.95), 3),
        }
        for from_code, to_code, edge_kind, bandwidth in STRUCTURAL_EDGE_SPECS
    ]
    functional_couplings = _functional_couplings_from_bus(bus_payload, run_id)
    hub_regions = ["P", "J", "O", "L"]
    return {
        "schema_version": "multiscale_region_graph_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "multiscale_region_graph_id": f"multiscale-region-graph-{run_id}",
        "region_definitions": region_definitions,
        "structural_edges": structural_edges,
        "functional_couplings": functional_couplings,
        "gradient_axes": [
            {
                "axis_id": "sensorimotor_to_default_mode",
                "low_anchor_project_code": "R",
                "high_anchor_project_code": "O",
            },
            {
                "axis_id": "fast_input_to_slow_narrative",
                "low_anchor_project_code": "G",
                "high_anchor_project_code": "P",
            },
        ],
        "hub_regions": hub_regions,
        "hub_load_monitor": {
            "loaded_hub_count": 0,
            "hub_project_codes": hub_regions,
            "overload_recovery_required": False,
        },
        "connectome_fingerprint": {
            "schema_version": "connectome_fingerprint_v0",
            "baseline_stability": "seeded",
            "habit_route_refs": [],
            "repair_trigger_refs": [],
            "dream_replay_route_refs": [],
        },
        "brain_graph_ref": (
            "runtime/state/neural_life_core/brain_graph.json"
            if brain_graph
            else None
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
        "multiscale_region_graph_boundary": MULTISCALE_REGION_GRAPH_BOUNDARY,
    }


def project_multiscale_region_graph_from_live_turn(
    *,
    multiscale_region_graph: dict[str, Any],
    generated_at: str,
    run_id: str | None = None,
    dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    workspace_frame: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_multiscale_region_graph(
        multiscale_region_graph, generated_at, run_id
    )
    relationship_graph = relationship_graph or {}
    relationship_timeline = relationship_timeline or {}
    self_model_state = self_model_state or {}
    network_state = network_state or {}
    workspace_frame = workspace_frame or {}
    signal_media_runtime = signal_media_runtime or {}

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
    updated["brain_graph_ref"] = "runtime/state/neural_life_core/brain_graph.json"

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

    active_networks = network_state.get("active_networks", [])
    if isinstance(active_networks, list) and active_networks:
        updated["functional_couplings"] = _refresh_functional_couplings(
            existing=updated.get("functional_couplings", []),
            active_networks=active_networks,
            live_turn_focus=live_focus,
            generated_at=generated_at,
        )

    hub_load = dict(updated.get("hub_load_monitor", {}))
    workspace_targets = workspace_frame.get("workspace_contents", {}).get(
        "salience_targets", []
    )
    if not workspace_targets:
        workspace_targets = workspace_frame.get("salience_ranking", [])
    loaded_hubs = _loaded_hub_codes(
        workspace_targets=workspace_targets,
        live_turn_focus=live_focus,
        signal_media_runtime=signal_media_runtime,
    )
    hub_load["loaded_hub_count"] = len(loaded_hubs)
    hub_load["loaded_hub_project_codes"] = loaded_hubs
    hub_load["overload_recovery_required"] = len(loaded_hubs) >= 3
    updated["hub_load_monitor"] = hub_load

    fingerprint = dict(updated.get("connectome_fingerprint", {}))
    if live_focus.get("relationship_stage"):
        fingerprint["repair_trigger_refs"] = _dedupe(
            list(fingerprint.get("repair_trigger_refs", []))
            + [
                (
                    "runtime/state/relationship/relationship_timeline.json#"
                    f"{live_focus['relationship_stage']}"
                )
            ]
        )[:8]
    if self_model_state.get("trait_slow_variable_candidates", {}).get("candidates"):
        fingerprint["habit_route_refs"] = _dedupe(
            list(fingerprint.get("habit_route_refs", []))
            + [
                "runtime/state/self/self_model.json#trait_slow_variable_candidates"
            ]
        )[:8]
    updated["connectome_fingerprint"] = fingerprint

    updated["graph_signal_propagation"] = _graph_signal_propagation(
        signal_media_runtime=signal_media_runtime,
        loaded_hubs=loaded_hubs,
        live_turn_focus=live_focus,
    )
    updated["last_projected_from_live_turn_ref"] = (
        list(updated.get("live_dialogue_turn_refs", []))[-1]
        if updated.get("live_dialogue_turn_refs")
        else None
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    return updated


def multiscale_region_graph_inspection_snapshot(
    *,
    multiscale_region_graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    multiscale_region_graph = multiscale_region_graph or {}
    regions = [
        item
        for item in multiscale_region_graph.get("region_definitions", [])
        if isinstance(item, dict)
    ]
    hub_load = multiscale_region_graph.get("hub_load_monitor", {})
    if not isinstance(hub_load, dict):
        hub_load = {}
    fingerprint = multiscale_region_graph.get("connectome_fingerprint", {})
    if not isinstance(fingerprint, dict):
        fingerprint = {}
    return {
        "multiscale_region_graph_present": bool(regions),
        "multiscale_region_count": len(regions),
        "multiscale_region_project_codes": [
            str(item.get("project_code"))
            for item in regions
            if item.get("project_code")
        ][:12],
        "multiscale_structural_edge_count": len(
            multiscale_region_graph.get("structural_edges", [])
        ),
        "multiscale_functional_coupling_count": len(
            multiscale_region_graph.get("functional_couplings", [])
        ),
        "multiscale_hub_loaded_count": int(hub_load.get("loaded_hub_count", 0)),
        "multiscale_hub_overload_recovery_required": bool(
            hub_load.get("overload_recovery_required")
        ),
        "multiscale_connectome_fingerprint_present": bool(fingerprint),
        "multiscale_region_graph_boundary": (
            multiscale_region_graph.get("multiscale_region_graph_boundary")
            or MULTISCALE_REGION_GRAPH_BOUNDARY
        ),
    }


def _functional_couplings_from_bus(
    bus_payload: dict[str, Any],
    run_id: str,
) -> list[dict[str, Any]]:
    couplings: list[dict[str, Any]] = []
    system_to_code = {spec["system_id"]: spec["project_code"] for spec in REGION_SPECS}
    for edge in bus_payload.get("edges", []):
        if not isinstance(edge, dict):
            continue
        from_code = system_to_code.get(edge.get("from_system"))
        to_code = system_to_code.get(edge.get("to_system"))
        if not from_code or not to_code:
            continue
        couplings.append(
            {
                "coupling_id": (
                    f"functional-{from_code.lower()}-{to_code.lower()}-"
                    f"{edge.get('edge_id', run_id)}"
                ),
                "from_project_code": from_code,
                "to_project_code": to_code,
                "payload_family": edge.get("payload_family"),
                "coupling_mode": "seed_bus_projection",
                "stage_policy": edge.get("stage_policy", "seed_only_no_external_action"),
            }
        )
    return couplings


def _refresh_functional_couplings(
    *,
    existing: list[Any],
    active_networks: list[Any],
    live_turn_focus: dict[str, Any],
    generated_at: str,
) -> list[dict[str, Any]]:
    refreshed = [
        item for item in existing if isinstance(item, dict)
    ]
    network_to_codes = {
        "default_mode_network": ["O", "P"],
        "salience_network": ["J", "S", "G"],
        "executive_workspace_network": ["P", "L", "D"],
    }
    for network in active_networks:
        if not isinstance(network, dict):
            continue
        network_id = network.get("network_id")
        codes = network_to_codes.get(str(network_id), [])
        for from_code in codes:
            for to_code in codes:
                if from_code == to_code:
                    continue
                refreshed.append(
                    {
                        "coupling_id": (
                            f"functional-live-{from_code.lower()}-"
                            f"{to_code.lower()}-{network_id}"
                        ),
                        "from_project_code": from_code,
                        "to_project_code": to_code,
                        "payload_family": "live_network_mode",
                        "coupling_mode": str(network.get("mode") or "live_refresh"),
                        "last_refreshed_at": generated_at,
                        "live_turn_focus": live_turn_focus or {},
                    }
                )
    return _dedupe_couplings(refreshed)


def _loaded_hub_codes(
    *,
    workspace_targets: Any,
    live_turn_focus: dict[str, Any],
    signal_media_runtime: dict[str, Any],
) -> list[str]:
    loaded: list[str] = []
    if workspace_targets:
        loaded.append("P")
    if live_turn_focus.get("relationship_stage"):
        loaded.extend(["O", "L"])
    modulation = signal_media_runtime.get("modulation_vector", {})
    if isinstance(modulation, dict):
        if modulation.get("repair_drive"):
            loaded.append("O")
        if modulation.get("arousal"):
            loaded.append("G")
    return _dedupe(loaded)[:4]


def _graph_signal_propagation(
    *,
    signal_media_runtime: dict[str, Any],
    loaded_hubs: list[str],
    live_turn_focus: dict[str, Any],
) -> dict[str, Any]:
    modulation = signal_media_runtime.get("modulation_vector", {})
    if not isinstance(modulation, dict):
        modulation = {}
    routes = [
        {
            "route_id": f"hub-{code.lower()}-signal-route",
            "target_project_code": code,
            "signal_family": "modulation_vector",
        }
        for code in loaded_hubs
    ]
    if live_turn_focus.get("relationship_stage"):
        routes.append(
            {
                "route_id": "relationship-stage-signal-route",
                "target_project_code": "O",
                "signal_family": "relationship_stage",
            }
        )
    return {
        "propagation_mode": "region_graph_diffusion",
        "active_route_count": len(routes),
        "routes": routes[:8],
        "modulation_snapshot": {
            key: modulation.get(key)
            for key in ["arousal", "repair_drive", "inhibition", "precision"]
            if key in modulation
        },
    }


def _cell_type_prior(project_code: str) -> dict[str, str]:
    mapping = {
        "L": "language_expression_filter",
        "R": "fast_input_filter",
        "P": "workspace_gate",
        "J": "relay_router",
        "G": "rhythmic_arousal_regulator",
        "S": "prediction_error_corrector",
        "O": "long_horizon_affective_integrator",
        "D": "action_inhibition_gate",
    }
    return {"primary_prior": mapping.get(project_code, "cross_modal_integrator")}


def _seed_missing_multiscale_region_graph(
    multiscale_region_graph: dict[str, Any],
    generated_at: str,
    run_id: str | None,
) -> dict[str, Any]:
    if multiscale_region_graph:
        return json.loads(json.dumps(multiscale_region_graph))
    resolved_run_id = run_id or "resident-turn-writeback"
    return {
        "schema_version": "multiscale_region_graph_v0",
        "run_id": resolved_run_id,
        "generated_at": generated_at,
        "status": "closed",
        "multiscale_region_graph_id": f"multiscale-region-graph-{resolved_run_id}",
        "region_definitions": [],
        "structural_edges": [],
        "functional_couplings": [],
        "hub_regions": [],
        "hub_load_monitor": {},
        "connectome_fingerprint": {},
        "source_doc_refs": SOURCE_DOC_REFS,
        "multiscale_region_graph_boundary": MULTISCALE_REGION_GRAPH_BOUNDARY,
    }


def _dedupe_couplings(couplings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for item in couplings:
        key = str(item.get("coupling_id"))
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
