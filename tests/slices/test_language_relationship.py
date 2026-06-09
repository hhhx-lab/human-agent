import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class LanguageRelationshipTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_build_language_relationship_writes_language_and_relationship_runtime_bundle(self):
        from life_v0.authority import run_source_authority
        from life_v0.body import run_check_life_support, run_life_support
        from life_v0.direction import run_direction_lock
        from life_v0.growth import run_cycle
        from life_v0.doc_index import run_doc_ingestion
        from life_v0.language import run_build_language_relationship, run_check_language_relationship
        from life_v0.life_targets import run_birth_readiness
        from life_v0.membrane import run_check_life_membrane, run_life_membrane
        from life_v0.neural_core import run_check_neural_life_core, run_neural_life_core
        from life_v0.schema_runner import run_check_schema_runner, run_schema_runner, run_schema_smoke
        from life_v0.state_store import run_check_state_store, run_state_store
        from life_v0.validators import run_check_validation_membrane, run_validation_membrane

        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            self._run_pre_s07_chain(
                paths=paths,
                run_doc_ingestion=run_doc_ingestion,
                run_direction_lock=run_direction_lock,
                run_source_authority=run_source_authority,
                run_neural_life_core=run_neural_life_core,
                run_check_neural_life_core=run_check_neural_life_core,
                run_state_store=run_state_store,
                run_check_state_store=run_check_state_store,
                run_life_membrane=run_life_membrane,
                run_check_life_membrane=run_check_life_membrane,
                run_build_language_relationship=run_build_language_relationship,
                run_check_language_relationship=run_check_language_relationship,
                run_birth_readiness=run_birth_readiness,
                run_validation_membrane=run_validation_membrane,
                run_check_validation_membrane=run_check_validation_membrane,
                run_schema_runner=run_schema_runner,
                run_check_schema_runner=run_check_schema_runner,
                run_schema_smoke=run_schema_smoke,
                run_life_support=run_life_support,
                run_check_life_support=run_check_life_support,
                run_cycle=run_cycle,
            )

            result = run_build_language_relationship(
                docs_dir=self.docs_dir,
                doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
                neural_core_state_dir=paths["neural_state"],
                state_dir=paths["state_root"],
                membrane_dir=paths["membrane_state"],
                out_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="language-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            check = run_check_language_relationship(
                state_dir=paths["state_root"],
                membrane_dir=paths["membrane_state"],
                reports_dir=paths["reports"],
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            inner_speech = self._read_json(paths["language_state"] / "inner_speech_frame.json")
            expression_monitor = self._read_json(paths["language_state"] / "expression_monitor_state.json")
            expression_plan = self._read_json(paths["language_state"] / "expression_plan.json")
            language_state = self._read_json(paths["language_state"] / "language_relationship_state.json")
            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")
            repair_language = self._read_json(paths["language_state"] / "commitment_repair_language_index.json")
            dream_language_gate = self._read_json(paths["language_state"] / "dream_report_language_gate.json")
            shadow_bridge = self._read_json(paths["language_state"] / "language_action_bridge_shadow.json")
            language_percept = self._read_json(paths["language_state"] / "language_percept_frame.json")
            semantic_map = self._read_json(paths["language_state"] / "semantic_map_frame.json")
            prediction_workspace = self._read_json(paths["prediction_state"] / "prediction_workspace_frame.json")
            shared_term_registry = self._read_json(paths["language_state"] / "shared_term_registry.json")
            relation_scope_index = self._read_json(paths["language_state"] / "relation_scope_language_index.json")
            self_narrative_trace = self._read_json(paths["language_state"] / "self_narrative_language_trace.json")
            dialogue_log_path = paths["language_state"] / "dialogue_turn_log.jsonl"
            dialogue_lines = dialogue_log_path.read_text(encoding="utf-8").strip().splitlines()
            report = self._read_json(paths["reports"] / "language_relationship_report.json")
            digest = self._read_json(paths["reports"] / "language_relationship_digest.json")
            check_report = self._read_json(paths["reports"] / "language_relationship_check_report.json")
            receipt = self._read_json(paths["receipts"] / "language_relationship_language-test.json")
            life_state = self._read_json(paths["state_root"] / "life_state.json")

        self.assertEqual(inner_speech["schema_version"], "inner_speech_frame_v0")
        self.assertEqual(inner_speech["status"], "closed")
        self.assertIn("inner_language_bus", inner_speech["bus_channel_refs"])

        self.assertEqual(expression_monitor["schema_version"], "expression_monitor_state_v0")
        self.assertEqual(expression_monitor["status"], "closed")
        self.assertIn("relationship_consequence", expression_monitor["monitor_dimensions"])
        self.assertIn("dream_fact", expression_monitor["monitor_dimensions"])

        self.assertEqual(expression_plan["schema_version"], "expression_plan_v0")
        self.assertEqual(expression_plan["status"], "closed")
        self.assertEqual(
            expression_plan["inner_speech_ref"],
            "runtime/state/language/inner_speech_frame.json",
        )
        self.assertEqual(
            expression_plan["semantic_goal"],
            semantic_map["semantic_focus"],
        )
        self.assertTrue(expression_plan["expression_risk_flags"])
        self.assertEqual(expression_plan["delay_or_release_decision"], "delay_for_clarification")
        self.assertGreaterEqual(expression_plan["repair_pressure"], 2)
        self.assertGreaterEqual(expression_plan["responsibility_pressure"], 2)
        self.assertIn("responsibility_repair_language_pressure_present", expression_plan["expression_risk_flags"])
        self.assertGreater(expression_plan["replay_cue_pressure"], 0)
        self.assertGreater(expression_plan["dream_integration_pressure"], 0)
        self.assertGreater(expression_plan["growth_candidate_pressure"], 0)
        self.assertIn("offline_replay_pressure_present", expression_plan["expression_risk_flags"])
        self.assertIn("dream_integration_pressure_present", expression_plan["expression_risk_flags"])
        self.assertIn("growth_candidate_pressure_present", expression_plan["expression_risk_flags"])
        self.assertEqual(
            expression_plan["offline_influence_refs"],
            [
                "runtime/state/replay/replay_cue_bundle.json",
                "runtime/state/dream/offline_consolidation_frame.json",
                "runtime/state/growth/growth_patch_candidate_queue.json",
            ],
        )

        self.assertEqual(language_state["schema_version"], "language_relationship_state_v0")
        self.assertEqual(language_state["status"], "closed")
        self.assertIn("friend", language_state["relationship_kinds"])
        self.assertTrue(language_state["shared_language_refs"])

        self.assertEqual(relationship_graph["schema_version"], "relationship_subject_graph_v0")
        self.assertEqual(relationship_graph["status"], "closed")
        self.assertTrue(relationship_graph["subjects"])
        self.assertEqual(relationship_graph["subjects"][0]["relation_role"], "friend")

        self.assertEqual(repair_language["schema_version"], "commitment_repair_language_index_v0")
        self.assertEqual(repair_language["status"], "closed")
        self.assertTrue(repair_language["repair_language_refs"])
        self.assertEqual(
            repair_language["responsibility_loop_ref"],
            "runtime/state/action/responsibility_loop_state.json",
        )
        self.assertTrue(repair_language["repair_obligation_refs"])
        self.assertTrue(repair_language["regret_trace_refs"])
        self.assertTrue(repair_language["responsibility_trace_refs"])

        self.assertEqual(dream_language_gate["schema_version"], "dream_report_language_gate_v0")
        self.assertEqual(dream_language_gate["dream_fact_gate"], "closed")

        self.assertEqual(shadow_bridge["schema_version"], "language_action_bridge_shadow_v0")
        self.assertTrue(shadow_bridge["shadow_only"])
        self.assertIn("shadow_action_candidate", shadow_bridge["bridge_refs"])

        self.assertEqual(language_percept["schema_version"], "language_percept_frame_v0")
        self.assertEqual(language_percept["status"], "closed")
        self.assertTrue(language_percept["shared_term_hits"])
        self.assertTrue(language_percept["repair_trigger_candidates"])
        self.assertTrue(language_percept["ambiguity_flags"])

        self.assertEqual(semantic_map["schema_version"], "semantic_map_frame_v0")
        self.assertEqual(semantic_map["status"], "closed")
        self.assertTrue(semantic_map["shared_meaning_bindings"])
        self.assertTrue(semantic_map["commitment_trace_refs"])
        self.assertTrue(semantic_map["repair_trace_refs"])
        self.assertTrue(semantic_map["ambiguity_queue"])
        self.assertEqual(semantic_map["prediction_hooks"]["semantic_prediction_focus"], semantic_map["semantic_focus"])

        self.assertEqual(prediction_workspace["schema_version"], "prediction_workspace_frame_v0")
        self.assertEqual(prediction_workspace["source_runtime"], "PredictionActiveInferenceRuntime")
        self.assertEqual(
            prediction_workspace["workspace_contents"]["precision_state"],
            "semantic_handoff_seeded",
        )
        self.assertEqual(
            prediction_workspace["workspace_contents"]["active_sampling_mode"],
            "clarify_ambiguity",
        )
        continuity_focus = prediction_workspace["workspace_contents"]["language_continuity_focus"]
        self.assertEqual(
            continuity_focus["language_percept_refs"],
            ["runtime/state/language/language_percept_frame.json"],
        )
        self.assertEqual(
            continuity_focus["semantic_map_refs"],
            ["runtime/state/language/semantic_map_frame.json"],
        )
        self.assertEqual(
            continuity_focus["semantic_prediction_focus"],
            semantic_map["semantic_focus"],
        )
        self.assertEqual(
            continuity_focus["semantic_ambiguity_refs"],
            ["runtime/state/language/semantic_map_frame.json#ambiguity_queue"],
        )
        self.assertTrue(prediction_workspace["workspace_contents"]["candidate_explanations"])

        self.assertEqual(shared_term_registry["schema_version"], "shared_term_registry_v0")
        self.assertEqual(shared_term_registry["status"], "closed")
        self.assertTrue(shared_term_registry["shared_terms"])

        self.assertEqual(relation_scope_index["schema_version"], "relation_scope_language_index_v0")
        self.assertEqual(relation_scope_index["status"], "closed")
        self.assertTrue(relation_scope_index["relation_scopes"])

        self.assertEqual(self_narrative_trace["schema_version"], "self_narrative_language_trace_v0")
        self.assertEqual(self_narrative_trace["status"], "closed")
        self.assertTrue(self_narrative_trace["narrative_turn_refs"])
        self.assertGreaterEqual(len(dialogue_lines), 1)

        self.assertEqual(report["schema_version"], "s07_language_relationship_report_v0")
        self.assertEqual(report["engineering_slice_ref"], "S07_LANGUAGE_RELATIONSHIP")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["next_allowed_slices"], ["S08_LIFE_TARGET_RUNTIMES"])
        self.assertEqual(report["next_required_command"], "life-v0 check-birth-readiness --strict")
        self.assertIn("LanguageRelationshipRuntime", report["runtime_carrier_refs"])
        self.assertTrue(report["language_percept_refs"])
        self.assertTrue(report["semantic_map_refs"])
        self.assertTrue(report["prediction_language_handoff_refs"])
        self.assertIn("repair_commitment_shared_language", report["semantic_focuses"])
        self.assertIn("runtime/state/language/expression_plan.json", report["state_refs"])
        self.assertIn("runtime/state/prediction/prediction_workspace_frame.json", report["state_refs"])

        self.assertEqual(digest["current_slice"], "S07_LANGUAGE_RELATIONSHIP")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(receipt["schema_version"], "language_relationship_receipt_v0")
        self.assertEqual(
            receipt["language_percept_ref"],
            "runtime/state/language/language_percept_frame.json",
        )
        self.assertEqual(
            receipt["semantic_map_ref"],
            "runtime/state/language/semantic_map_frame.json",
        )
        self.assertTrue(
            any(key.endswith("responsibility_loop_state.json") for key in receipt["input_hashes"]),
            receipt["input_hashes"],
        )
        self.assertTrue(
            any(ref.endswith("/runtime/state/language/expression_plan.json") for ref in receipt["output_refs"])
        )
        self.assertTrue(receipt["downstream_handoff_refs"])

        self.assertTrue(life_state["language_state"]["inner_speech_refs"])
        self.assertTrue(life_state["language_state"]["shared_language_refs"])
        self.assertTrue(life_state["language_state"]["repair_language_refs"])
        self.assertTrue(life_state["language_state"]["shared_term_registry_refs"])
        self.assertTrue(life_state["language_state"]["relation_scope_refs"])
        self.assertTrue(life_state["language_state"]["self_narrative_trace_refs"])
        self.assertTrue(life_state["language_state"]["dialogue_turn_log_refs"])
        self.assertTrue(life_state["language_state"]["language_percept_refs"])
        self.assertTrue(life_state["language_state"]["semantic_map_refs"])
        self.assertIn("runtime/state/prediction/prediction_workspace_frame.json", life_state["runtime_trace_refs"])
        self.assertTrue(life_state["relationship_subjects"])

    def test_cli_build_language_relationship_returns_zero_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "lang-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "lang-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "lang-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "lang-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "lang-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "lang-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "lang-cli", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
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

            report = self._read_json(paths["reports"] / "language_relationship_report.json")
            check_report = self._read_json(paths["reports"] / "language_relationship_check_report.json")
            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")

        self.assertEqual(report["run_id"], "lang-cli")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["next_required_command"], "life-v0 check-birth-readiness --strict")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(relationship_graph["status"], "closed")

    def _runtime_paths(self, tmp_path: Path) -> dict[str, Path]:
        state_root = tmp_path / "runtime" / "state"
        return {
            "doc_out": tmp_path / "runtime" / "docs",
            "reports": tmp_path / "runtime" / "reports" / "latest",
            "receipts": tmp_path / "runtime" / "receipts",
            "direction_state": state_root / "direction",
            "authority_state": state_root / "authority",
            "neural_state": state_root / "neural_life_core",
            "state_root": state_root,
            "membrane_state": state_root / "membrane",
            "language_state": state_root / "language",
            "relationship_state": state_root / "relationship",
            "prediction_state": state_root / "prediction",
        }

    def _run_pre_s07_chain(self, *, paths, **kwargs):
        ingest = kwargs["run_doc_ingestion"](
            docs_dir=self.docs_dir,
            out_dir=paths["doc_out"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-ingest",
            strict=True,
        )
        self.assertEqual(ingest.exit_code, 0)

        direction = kwargs["run_direction_lock"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            out_dir=paths["direction_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-direction",
            strict=True,
        )
        self.assertEqual(direction.exit_code, 0)

        authority = kwargs["run_source_authority"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            direction_state_dir=paths["direction_state"],
            out_dir=paths["authority_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-authority",
            strict=True,
        )
        self.assertEqual(authority.exit_code, 0)

        neural = kwargs["run_neural_life_core"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            authority_state_dir=paths["authority_state"],
            out_dir=paths["neural_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-neural",
            strict=True,
        )
        self.assertEqual(neural.exit_code, 0)

        neural_check = kwargs["run_check_neural_life_core"](
            state_dir=paths["neural_state"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(neural_check.exit_code, 0)

        state_store = kwargs["run_state_store"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            neural_core_state_dir=paths["neural_state"],
            out_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-state",
            strict=True,
        )
        self.assertEqual(state_store.exit_code, 0)

        state_check = kwargs["run_check_state_store"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(state_check.exit_code, 0)

        membrane = kwargs["run_life_membrane"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            direction_state_dir=paths["direction_state"],
            neural_core_state_dir=paths["neural_state"],
            state_dir=paths["state_root"],
            out_dir=paths["membrane_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-membrane",
            strict=True,
        )
        self.assertEqual(membrane.exit_code, 0)

        membrane_check = kwargs["run_check_life_membrane"](
            membrane_dir=paths["membrane_state"],
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(membrane_check.exit_code, 0)

        language = kwargs["run_build_language_relationship"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            neural_core_state_dir=paths["neural_state"],
            state_dir=paths["state_root"],
            membrane_dir=paths["membrane_state"],
            out_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-bootstrap",
            strict=True,
        )
        self.assertEqual(language.exit_code, 0)

        language_check = kwargs["run_check_language_relationship"](
            state_dir=paths["state_root"],
            membrane_dir=paths["membrane_state"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(language_check.exit_code, 0)

        birth = kwargs["run_birth_readiness"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            direction_state_dir=paths["direction_state"],
            neural_core_state_dir=paths["neural_state"],
            state_dir=paths["state_root"],
            membrane_dir=paths["membrane_state"],
            out_dir=paths["state_root"] / "life_targets",
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-birth",
            strict=True,
        )
        self.assertEqual(birth.exit_code, 0)

        validation = kwargs["run_validation_membrane"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            state_dir=paths["state_root"],
            membrane_dir=paths["membrane_state"],
            life_targets_dir=paths["state_root"] / "life_targets",
            validation_dir=paths["state_root"] / "validation",
            observation_dir=paths["state_root"] / "observation",
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-validation",
            strict=True,
        )
        self.assertEqual(validation.exit_code, 0)

        validation_check = kwargs["run_check_validation_membrane"](
            state_dir=paths["state_root"],
            validation_dir=paths["state_root"] / "validation",
            observation_dir=paths["state_root"] / "observation",
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(validation_check.exit_code, 0)

        schema_runner = kwargs["run_schema_runner"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-schema",
            strict=True,
        )
        self.assertEqual(schema_runner.exit_code, 0)

        schema_check = kwargs["run_check_schema_runner"](
            state_dir=paths["state_root"] / "schema_runner",
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(schema_check.exit_code, 0)

        schema_smoke = kwargs["run_schema_smoke"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-smoke",
            strict=True,
        )
        self.assertEqual(schema_smoke.exit_code, 0)

        life_support = kwargs["run_life_support"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            state_dir=paths["state_root"],
            validation_report_path=paths["reports"] / "validation_membrane_report.json",
            out_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-support",
            strict=True,
        )
        self.assertEqual(life_support.exit_code, 0)

        life_support_check = kwargs["run_check_life_support"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(life_support_check.exit_code, 0)

        runtime_growth = kwargs["run_cycle"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="lang-cycle",
            strict=True,
            shadow_only=True,
        )
        self.assertEqual(runtime_growth.exit_code, 0)

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
