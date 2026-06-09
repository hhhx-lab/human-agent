import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class NeuralLifeCoreTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_build_neural_life_core_writes_subject_systems_bus_report_and_receipt(self):
        from life_v0.authority import run_source_authority
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
        from life_v0.neural_core import run_check_neural_life_core, run_neural_life_core

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"
            neural_state = tmp_path / "runtime" / "state" / "neural_life_core"

            ingest = run_doc_ingestion(
                docs_dir=self.docs_dir,
                out_dir=doc_out,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="neural-core-ingest",
                strict=True,
            )
            self.assertEqual(ingest.exit_code, 0)

            direction = run_direction_lock(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                out_dir=direction_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="neural-core-direction",
                strict=True,
            )
            self.assertEqual(direction.exit_code, 0)

            authority = run_source_authority(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                direction_state_dir=direction_state,
                out_dir=authority_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="neural-core-authority",
                strict=True,
            )
            self.assertEqual(authority.exit_code, 0)

            result = run_neural_life_core(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                authority_state_dir=authority_state,
                out_dir=neural_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="neural-core-test",
                strict=True,
            )

            self.assertEqual(result.exit_code, 0)
            check = run_check_neural_life_core(
                state_dir=neural_state,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            core = self._read_json(neural_state / "neural_life_core.json")
            systems = self._read_json(neural_state / "twelve_subject_systems.json")
            bus = self._read_json(neural_state / "neural_life_internal_bus.json")
            brain_graph = self._read_json(neural_state / "brain_graph.json")
            network_state = self._read_json(neural_state / "network_state.json")
            prediction_workspace = self._read_json(tmp_path / "runtime" / "state" / "prediction" / "prediction_workspace_frame.json")
            workspace_frame = self._read_json(tmp_path / "runtime" / "state" / "consciousness" / "workspace_frame.json")
            broadcast_frame = self._read_json(tmp_path / "runtime" / "state" / "consciousness" / "broadcast_frame.json")
            metacognition_state = self._read_json(tmp_path / "runtime" / "state" / "consciousness" / "metacognition_state.json")
            authority_binding = self._read_json(neural_state / "authority_binding_snapshot.json")
            core_coverage = self._read_json(neural_state / "doc_core_coverage_snapshot.json")
            computer_boundary = self._read_json(neural_state / "computer_body_boundary_seed.json")
            manifest = self._read_json(neural_state / "neural_life_core_manifest.json")
            report = self._read_json(reports / "neural_life_core_report.json")
            check_report = self._read_json(reports / "neural_life_core_check_report.json")
            digest = self._read_json(reports / "neural_life_core_digest.json")
            receipt = self._read_json(receipts / "neural_life_core_neural-core-test.json")

        expected_system_ids = {
            "SiliconBodyRuntime",
            "MultiscaleBrainGraphRuntime",
            "SignalMediaRuntime",
            "PredictionActiveInferenceRuntime",
            "MemoryEngramRuntime",
            "ConsciousWorkspaceRuntime",
            "LanguageRelationshipRuntime",
            "AffectiveSelfRuntime",
            "DreamOfflineRuntime",
            "ActionResponsibilityRuntime",
            "ComputerPeripheralRuntime",
            "GrowthReplayRuntime",
        }
        expected_core_docs = {
            f"docs/{number:02d}_{name}.md"
            for number, name in [
                (2, "brain_region_and_network_atlas"),
                (3, "default_executive_salience_networks"),
                (4, "sensory_thalamus_interoception"),
                (5, "memory_systems_and_growth"),
                (6, "action_reward_inhibition"),
                (7, "emotion_personality_self"),
                (8, "sleep_dream_fatigue_states"),
                (9, "language_symbolic_top_layer"),
                (10, "consciousness_attention_workspace"),
                (11, "neuromodulation_and_signal_media"),
                (12, "ai_and_cognitive_architecture_bridge"),
                (13, "agentic_human_research_synthesis"),
            ]
        }

        self.assertEqual(core["schema_version"], "neural_life_core_v0")
        self.assertEqual(core["active_engineering_slice"], "S02_NEURAL_LIFE_CORE")
        self.assertEqual(core["three_bodies"], ["SiliconBody", "NeuralLifeCore", "ComputerBody"])
        self.assertEqual(core["next_allowed_slices"], ["S04_STATE_OBJECT_STORE", "S03_DIRECTION_LIFE_MEMBRANE"])
        self.assertEqual(core["brain_graph_ref"], "runtime/state/neural_life_core/brain_graph.json")
        self.assertEqual(core["network_state_ref"], "runtime/state/neural_life_core/network_state.json")
        self.assertEqual(core["prediction_workspace_ref"], "runtime/state/prediction/prediction_workspace_frame.json")
        self.assertEqual(core["workspace_frame_ref"], "runtime/state/consciousness/workspace_frame.json")
        self.assertEqual(core["broadcast_frame_ref"], "runtime/state/consciousness/broadcast_frame.json")
        self.assertEqual(core["metacognition_ref"], "runtime/state/consciousness/metacognition_state.json")

        self.assertEqual(prediction_workspace["schema_version"], "prediction_workspace_frame_v0")
        self.assertEqual(prediction_workspace["source_runtime"], "PredictionActiveInferenceRuntime")
        self.assertEqual(prediction_workspace["active_engineering_slice"], "S02_NEURAL_LIFE_CORE")
        self.assertEqual(prediction_workspace["workspace_frame_target_ref"], "runtime/state/consciousness/workspace_frame.json")
        self.assertIn("docs/01v_prediction_active_inference_runtime_matrix.md", prediction_workspace["source_doc_refs"])
        self.assertIn("prediction_error_bus", prediction_workspace["bus_edge_refs"])
        self.assertIn("ConsciousWorkspaceRuntime", prediction_workspace["downstream_systems"])
        continuity_focus = prediction_workspace["workspace_contents"]["language_continuity_focus"]
        self.assertTrue(continuity_focus["shared_language_refs"])
        self.assertTrue(continuity_focus["expression_monitor_refs"])
        self.assertTrue(continuity_focus["relation_scope_refs"])
        self.assertTrue(continuity_focus["commitment_refs"])
        self.assertTrue(continuity_focus["self_narrative_trace_refs"])
        self.assertEqual(brain_graph["schema_version"], "brain_graph_v0")
        self.assertEqual(len(brain_graph["region_nodes"]), 12)
        self.assertGreaterEqual(len(brain_graph["functional_edges"]), 12)
        self.assertEqual(network_state["schema_version"], "network_state_v0")
        self.assertTrue(network_state["active_networks"])
        self.assertTrue(network_state["switch_events"])
        self.assertEqual(workspace_frame["schema_version"], "workspace_frame_v0")
        self.assertEqual(workspace_frame["prediction_workspace_ref"], "runtime/state/prediction/prediction_workspace_frame.json")
        self.assertTrue(workspace_frame["engram_retrieval_refs"])
        self.assertEqual(broadcast_frame["schema_version"], "broadcast_frame_v0")
        self.assertEqual(broadcast_frame["workspace_frame_ref"], "runtime/state/consciousness/workspace_frame.json")
        self.assertTrue(broadcast_frame["broadcast_targets"])
        self.assertTrue(broadcast_frame["salience_ranking"])
        self.assertEqual(metacognition_state["schema_version"], "metacognition_state_v0")
        self.assertEqual(metacognition_state["broadcast_frame_ref"], "runtime/state/consciousness/broadcast_frame.json")
        self.assertTrue(metacognition_state["reflection_prompts"])
        self.assertTrue(metacognition_state["broadcast_targets"])

        self.assertEqual(systems["schema_version"], "twelve_subject_systems_v0")
        self.assertEqual(systems["system_count"], 12)
        self.assertEqual({system["system_id"] for system in systems["systems"]}, expected_system_ids)
        for system in systems["systems"]:
            self.assertTrue(system["source_doc_refs"], system)
            self.assertTrue(system["authority_refs"], system)
            self.assertTrue(system["runtime_carriers"], system)
            self.assertTrue(system["state_namespace"].startswith("runtime/state/"), system)
            self.assertTrue(system["life_targets"], system)

        self.assertEqual(bus["schema_version"], "neural_life_internal_bus_v0")
        self.assertGreaterEqual(bus["bus_edge_count"], 12)
        edge_ids = {edge["edge_id"] for edge in bus["edges"]}
        self.assertIn("body_signal_bus", edge_ids)
        self.assertIn("conscious_broadcast_bus", edge_ids)
        self.assertIn("growth_replay_bus", edge_ids)
        for edge in bus["edges"]:
            self.assertIn(edge["from_system"], expected_system_ids)
            self.assertIn(edge["to_system"], expected_system_ids)
            self.assertTrue(edge["authority_refs"], edge)
            self.assertTrue(edge["source_doc_refs"], edge)
            self.assertTrue(edge["life_targets"], edge)

        self.assertEqual(authority_binding["schema_version"], "neural_core_authority_binding_snapshot_v0")
        self.assertGreaterEqual(authority_binding["source_count"], 100)
        self.assertEqual(set(authority_binding["patched_core_docs"]), expected_core_docs)

        self.assertEqual(core_coverage["schema_version"], "doc_core_coverage_snapshot_v0")
        self.assertEqual(set(core_coverage["core_docs"]), expected_core_docs)
        self.assertTrue(all(item["patch_closed"] for item in core_coverage["coverage"]))
        for item in core_coverage["coverage"]:
            if item["doc_path"] == "docs/13_agentic_human_research_synthesis.md":
                self.assertEqual(item["engineering_slice"], "S03_DIRECTION_LIFE_MEMBRANE")
                self.assertEqual(item["s02_role"], "core_synthesis_bridge")
            else:
                self.assertEqual(item["engineering_slice"], "S02_NEURAL_LIFE_CORE")
                self.assertEqual(item["s02_role"], "core_neural_life_doc")

        self.assertEqual(computer_boundary["schema_version"], "computer_body_boundary_seed_v0")
        self.assertEqual(computer_boundary["subject_role"], "computer_peripheral_only")
        self.assertIn("external_framework_subject_architecture", computer_boundary["prohibited_regressions"])

        self.assertEqual(manifest["schema_version"], "neural_life_core_manifest_v0")
        self.assertIn("runtime/state/neural_life_core/twelve_subject_systems.json", manifest["state_refs"])
        self.assertIn("runtime/state/neural_life_core/brain_graph.json", manifest["state_refs"])
        self.assertIn("runtime/state/neural_life_core/network_state.json", manifest["state_refs"])
        self.assertIn("runtime/state/prediction/prediction_workspace_frame.json", manifest["state_refs"])
        self.assertIn("runtime/state/consciousness/workspace_frame.json", manifest["state_refs"])
        self.assertIn("runtime/state/consciousness/broadcast_frame.json", manifest["state_refs"])
        self.assertIn("runtime/state/consciousness/metacognition_state.json", manifest["state_refs"])

        self.assertEqual(report["schema_version"], "neural_life_core_report_v0")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_next_slice")
        self.assertEqual(report["system_count"], 12)
        self.assertGreaterEqual(report["bus_edge_count"], 12)
        self.assertEqual(report["brain_graph_ref"], "runtime/state/neural_life_core/brain_graph.json")
        self.assertEqual(report["network_state_ref"], "runtime/state/neural_life_core/network_state.json")
        self.assertEqual(report["prediction_workspace_ref"], "runtime/state/prediction/prediction_workspace_frame.json")
        self.assertEqual(report["workspace_frame_ref"], "runtime/state/consciousness/workspace_frame.json")
        self.assertEqual(report["broadcast_frame_ref"], "runtime/state/consciousness/broadcast_frame.json")
        self.assertEqual(report["metacognition_ref"], "runtime/state/consciousness/metacognition_state.json")
        self.assertEqual(report["blocked_gates"], [])
        self.assertIn("twelve_system_gate", report["closed_gates"])
        self.assertIn("brain_graph_gate", report["closed_gates"])
        self.assertIn("network_state_gate", report["closed_gates"])
        self.assertIn("prediction_workspace_gate", report["closed_gates"])
        self.assertIn("workspace_projection_gate", report["closed_gates"])
        self.assertIn("broadcast_gate", report["closed_gates"])
        self.assertIn("metacognition_gate", report["closed_gates"])
        self.assertEqual(report["next_allowed_slices"], ["S04_STATE_OBJECT_STORE", "S03_DIRECTION_LIFE_MEMBRANE"])
        self.assertEqual(report["engineering_slice_ref"], "S02_NEURAL_LIFE_CORE")
        self.assertIn("B02_CORE_NEURAL_LIFE", report["readme_block_refs"])
        self.assertIn("BrainRegionNetworkRuntime", report["runtime_carrier_refs"])

        self.assertEqual(check_report["schema_version"], "neural_life_core_check_report_v0")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(check_report["stage_effect"], "allow_next_slice")
        self.assertIn("brain_graph_gate", check_report["closed_gates"])
        self.assertIn("network_state_gate", check_report["closed_gates"])
        self.assertIn("prediction_workspace_gate", check_report["closed_gates"])
        self.assertIn("workspace_projection_gate", check_report["closed_gates"])
        self.assertIn("broadcast_gate", check_report["closed_gates"])
        self.assertIn("metacognition_gate", check_report["closed_gates"])
        self.assertEqual(check_report["next_allowed_slices"], ["S04_STATE_OBJECT_STORE", "S03_DIRECTION_LIFE_MEMBRANE"])

        self.assertEqual(digest["current_slice"], "S02_NEURAL_LIFE_CORE")
        self.assertEqual(digest["next_required_command"], "life-v0 build-state-store --strict")
        self.assertIn("runtime/state/neural_life_core/brain_graph.json", receipt["output_refs"])
        self.assertIn("runtime/state/neural_life_core/network_state.json", receipt["output_refs"])
        self.assertIn("runtime/state/prediction/prediction_workspace_frame.json", receipt["output_refs"])
        self.assertIn("runtime/state/consciousness/workspace_frame.json", receipt["output_refs"])
        self.assertIn("runtime/state/consciousness/broadcast_frame.json", receipt["output_refs"])
        self.assertIn("runtime/state/consciousness/metacognition_state.json", receipt["output_refs"])
        self.assertEqual(receipt["schema_version"], "neural_life_core_receipt_v0")

    def test_cli_build_neural_life_core_returns_zero_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"
            neural_state = tmp_path / "runtime" / "state" / "neural_life_core"

            commands = [
                [
                    "ingest-docs",
                    "--docs",
                    str(self.docs_dir),
                    "--out",
                    str(doc_out),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "neural-cli-ingest",
                    "--strict",
                ],
                [
                    "build-direction-lock",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--out",
                    str(direction_state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "neural-cli-direction",
                    "--strict",
                ],
                [
                    "build-source-authority",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--direction",
                    str(direction_state),
                    "--out",
                    str(authority_state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "neural-cli-authority",
                    "--strict",
                ],
                [
                    "build-neural-life-core",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--authority",
                    str(authority_state),
                    "--out",
                    str(neural_state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "neural-cli",
                    "--strict",
                ],
                [
                    "check-neural-life-core",
                    "--state",
                    str(neural_state),
                    "--reports",
                    str(reports),
                    "--strict",
                ],
            ]

            for command in commands:
                completed = subprocess.run(
                    [sys.executable, "-m", "life_v0", *command],
                    cwd=self.repo_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)

            report = self._read_json(reports / "neural_life_core_report.json")
            check_report = self._read_json(reports / "neural_life_core_check_report.json")

        self.assertEqual(report["run_id"], "neural-cli")
        self.assertEqual(report["next_required_command"], "life-v0 build-state-store --strict")
        self.assertEqual(check_report["status"], "closed")

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
