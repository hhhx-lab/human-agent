import unittest

from life_v0.neural_core.multiscale_region_graph import (
    build_multiscale_region_graph,
    multiscale_region_graph_inspection_snapshot,
    project_multiscale_region_graph_from_live_turn,
)
from life_v0.process_supervisor.state_inspection import (
    _collect_cognitive_workspace_summary,
)


class MultiscaleRegionGraphTests(unittest.TestCase):
    def _seed_systems_and_bus(self) -> tuple[dict, dict]:
        systems_payload = {
            "system_count": 12,
            "systems": [
                {
                    "system_id": "LanguageRelationshipRuntime",
                    "authority_refs": ["auth-language"],
                    "source_doc_refs": ["docs/09_language_symbolic_top_layer.md"],
                },
                {
                    "system_id": "ConsciousWorkspaceRuntime",
                    "authority_refs": ["auth-workspace"],
                    "source_doc_refs": ["docs/10_consciousness_attention_workspace.md"],
                },
                {
                    "system_id": "MultiscaleBrainGraphRuntime",
                    "authority_refs": ["auth-brain"],
                    "source_doc_refs": ["docs/02_brain_region_and_network_atlas.md"],
                },
                {
                    "system_id": "SignalMediaRuntime",
                    "authority_refs": ["auth-signal"],
                    "source_doc_refs": ["docs/11_neuromodulation_and_signal_media.md"],
                },
                {
                    "system_id": "PredictionActiveInferenceRuntime",
                    "authority_refs": ["auth-prediction"],
                    "source_doc_refs": ["docs/01v_prediction_active_inference_runtime_matrix.md"],
                },
                {
                    "system_id": "AffectiveSelfRuntime",
                    "authority_refs": ["auth-affect"],
                    "source_doc_refs": ["docs/04_sensory_thalamus_interoception.md"],
                },
                {
                    "system_id": "ActionResponsibilityRuntime",
                    "authority_refs": ["auth-action"],
                    "source_doc_refs": ["docs/10_responsibility_regret_repair.md"],
                },
                {
                    "system_id": "ComputerPeripheralRuntime",
                    "authority_refs": ["auth-peripheral"],
                    "source_doc_refs": ["docs/37_life_support_layer_policy.md"],
                },
            ],
        }
        bus_payload = {
            "bus_edge_count": 2,
            "edges": [
                {
                    "edge_id": "signal_media_bus",
                    "from_system": "SignalMediaRuntime",
                    "to_system": "ConsciousWorkspaceRuntime",
                    "payload_family": "modulation_vector",
                    "stage_policy": "seed_only_no_external_action",
                },
                {
                    "edge_id": "prediction_error_bus",
                    "from_system": "PredictionActiveInferenceRuntime",
                    "to_system": "ConsciousWorkspaceRuntime",
                    "payload_family": "prediction_error",
                    "stage_policy": "seed_only_no_external_action",
                },
            ],
        }
        return systems_payload, bus_payload

    def test_build_multiscale_region_graph_seed(self):
        systems_payload, bus_payload = self._seed_systems_and_bus()
        graph = build_multiscale_region_graph(
            run_id="msrg-test",
            generated_at="2026-06-15T03:00:00+00:00",
            systems_payload=systems_payload,
            bus_payload=bus_payload,
            brain_graph={"brain_graph_id": "brain-graph-msrg-test"},
        )

        self.assertEqual(graph["schema_version"], "multiscale_region_graph_v0")
        self.assertEqual(len(graph["region_definitions"]), 8)
        self.assertTrue(graph["structural_edges"])
        self.assertTrue(graph["functional_couplings"])
        self.assertIn("connectome_fingerprint", graph)

    def test_live_projection_updates_hub_load(self):
        systems_payload, bus_payload = self._seed_systems_and_bus()
        seeded = build_multiscale_region_graph(
            run_id="msrg-live",
            generated_at="2026-06-15T03:00:00+00:00",
            systems_payload=systems_payload,
            bus_payload=bus_payload,
            brain_graph={"brain_graph_id": "brain-graph-msrg-live"},
        )
        projected = project_multiscale_region_graph_from_live_turn(
            multiscale_region_graph=seeded,
            generated_at="2026-06-15T04:00:00+00:00",
            run_id="msrg-live-turn",
            dialogue_turn_refs=["turn-live-1"],
            relationship_graph={
                "subjects": [{"relationship_stage": "repair_guarded_continuity"}]
            },
            signal_media_runtime={
                "modulation_vector": {"repair_drive": 0.7, "arousal": 0.5}
            },
            workspace_frame={"workspace_contents": {"salience_targets": ["focus-a"]}},
        )

        hub_load = projected["hub_load_monitor"]
        self.assertGreaterEqual(hub_load.get("loaded_hub_count", 0), 1)
        self.assertIn("graph_signal_propagation", projected)

    def test_cognition_summary_exposes_multiscale_region_graph(self):
        section = {
            "multiscale_region_graph": {
                "schema_version": "multiscale_region_graph_v0",
                "region_definitions": [
                    {"project_code": "L", "region_label": "LanguageNetwork"},
                    {"project_code": "P", "region_label": "ExecutiveWorkspace"},
                ],
                "structural_edges": [{"edge_id": "structural-j-p"}],
                "functional_couplings": [{"coupling_id": "functional-live"}],
                "hub_load_monitor": {"loaded_hub_count": 2},
                "connectome_fingerprint": {"schema_version": "connectome_fingerprint_v0"},
            },
            "network_state": {"schema_version": "network_state_v0"},
            "workspace_frame": {"status": "closed"},
        }

        summary = _collect_cognitive_workspace_summary(section)

        self.assertTrue(summary["multiscale_region_graph_present"])
        self.assertEqual(summary["multiscale_region_count"], 2)
        self.assertIn("multiscale_region_graph", summary["domain_presence"])

    def test_inspection_snapshot_fields(self):
        snapshot = multiscale_region_graph_inspection_snapshot(
            multiscale_region_graph={
                "region_definitions": [{"project_code": "O"}],
                "structural_edges": [{}],
                "functional_couplings": [{}],
                "hub_load_monitor": {"loaded_hub_count": 1},
                "connectome_fingerprint": {},
            }
        )
        self.assertTrue(snapshot["multiscale_region_graph_present"])
        self.assertEqual(snapshot["multiscale_region_count"], 1)