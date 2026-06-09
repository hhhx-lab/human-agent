import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SchemaRunnerTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_build_schema_runner_writes_registry_lockfile_queue_stage_gate_and_smoke(self):
        from life_v0.authority import run_source_authority
        from life_v0.direction import run_direction_lock
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
            self._run_pre_s09_chain(
                paths,
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
            )

            result = run_schema_runner(
                docs_dir=self.docs_dir,
                doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="schema-runner-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            check = run_check_schema_runner(
                state_dir=paths["schema_runner_state"],
                reports_dir=paths["reports"],
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            smoke = run_schema_smoke(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="schema-smoke-test",
                strict=True,
            )
            self.assertEqual(smoke.exit_code, 0)

            registry = self._read_json(paths["schema_runner_state"] / "schema_registry.json")
            lockfile = self._read_json(paths["schema_runner_state"] / "schema_dependency_lockfile.json")
            queue = self._read_json(paths["schema_runner_state"] / "runner_command_queue.json")
            checker_manifest = self._read_json(paths["schema_runner_state"] / "cross_file_checker_manifest.json")
            artifact_manifest = self._read_json(paths["schema_runner_state"] / "first_code_artifact_manifest.json")
            consistency_logic = self._read_json(paths["schema_runner_state"] / "consistency_logic.json")
            cross_file_logic = self._read_json(paths["schema_runner_state"] / "cross_file_logic.json")
            counterfactual_trace = self._read_json(paths["schema_runner_state"] / "counterfactual_trace.json")
            comparison_trace = self._read_json(paths["schema_runner_state"] / "comparison_trace.json")
            evidence_ranking = self._read_json(paths["schema_runner_state"] / "evidence_ranking.json")
            run_manifest = self._read_json(paths["schema_runner_state"] / "run_manifest.json")
            responsibility_loop = self._read_json(paths["state_root"] / "action" / "responsibility_loop_state.json")
            stage_gate = self._read_json(paths["schema_runner_state"] / "schema_runner_stage_gate.json")
            report = self._read_json(paths["reports"] / "schema_runner_report.json")
            digest = self._read_json(paths["reports"] / "schema_runner_digest.json")
            check_report = self._read_json(paths["reports"] / "schema_runner_check_report.json")
            smoke_report = self._read_json(paths["reports"] / "schema_smoke_report.json")
            receipt = self._read_json(paths["receipts"] / "schema_runner_schema-runner-test.json")

        self.assertEqual(registry["schema_version"], "schema_registry_v0")
        self.assertEqual(registry["active_engineering_slice"], "S09_SCHEMA_RUNNER_CODE")
        self.assertIn("shared_defs", registry["registry_families"])
        self.assertIn("component_schemas", registry["registry_families"])
        self.assertIn("dashboard_schemas", registry["registry_families"])
        self.assertIn("docs/102_life_core_schema_bundle_manifest_and_runner_contract.md", registry["source_doc_refs"])
        self.assertIn("docs/180_life_reality_first_runner_schema_file_archive_receipt_batch.md", registry["source_doc_refs"])

        self.assertEqual(lockfile["schema_version"], "schema_dependency_lockfile_v0")
        self.assertEqual(lockfile["status"], "closed")
        self.assertTrue(lockfile["artifact_nodes"])
        self.assertTrue(lockfile["doc_nodes"])
        self.assertTrue(lockfile["ref_edges"])
        self.assertIn("CONSISTENCY-009 implementation-carrier-present", lockfile["consistency_constraints"])

        self.assertEqual(queue["schema_version"], "runner_command_queue_v0")
        self.assertEqual(queue["status"], "closed")
        self.assertIn("build-schema-runner", queue["commands"])
        self.assertIn("check-schema-runner", queue["commands"])
        self.assertIn("run-schema-smoke", queue["commands"])
        self.assertIn("build-life-support", queue["next_stage_commands"])

        self.assertEqual(checker_manifest["schema_version"], "cross_file_checker_manifest_v0")
        self.assertEqual(checker_manifest["status"], "closed")
        self.assertIn("authority_schema_cross_file", checker_manifest["checker_families"])
        self.assertIn("birth_readiness_cross_file", checker_manifest["checker_families"])
        self.assertIn("full_archive_rollup", checker_manifest["checker_families"])

        self.assertEqual(artifact_manifest["schema_version"], "first_code_artifact_manifest_v0")
        self.assertEqual(artifact_manifest["status"], "closed")
        self.assertIn("life_v0/schema_runner/", artifact_manifest["code_roots"])
        self.assertIn("life_v0/cli.py", artifact_manifest["artifact_refs"])
        self.assertIn("tests/slices/test_schema_runner.py", artifact_manifest["test_refs"])
        self.assertIn("runtime/reports/latest/schema_smoke_report.json", artifact_manifest["smoke_report_refs"])
        self.assertIn("runtime/state/schema_runner/consistency_logic.json", artifact_manifest["artifact_refs"])
        self.assertIn("runtime/state/schema_runner/cross_file_logic.json", artifact_manifest["artifact_refs"])
        self.assertIn("runtime/state/schema_runner/counterfactual_trace.json", artifact_manifest["artifact_refs"])
        self.assertIn("runtime/state/schema_runner/comparison_trace.json", artifact_manifest["artifact_refs"])
        self.assertIn("runtime/state/schema_runner/run_manifest.json", artifact_manifest["artifact_refs"])

        self.assertEqual(consistency_logic["schema_version"], "consistency_logic_v0")
        self.assertTrue(consistency_logic["comparison_axes"])
        self.assertEqual(consistency_logic["inconsistency_findings"], [])
        self.assertIn("runtime/state/action/responsibility_loop_state.json", consistency_logic["state_refs"])
        self.assertIn("responsibility_loop_to_counterfactual_repair", consistency_logic["comparison_axes"])
        self.assertIn("runtime/state/action/responsibility_loop_state.json", consistency_logic["repair_route_refs"])

        self.assertEqual(cross_file_logic["schema_version"], "cross_file_logic_v0")
        self.assertEqual(cross_file_logic["status"], "closed")
        self.assertTrue(cross_file_logic["cross_file_findings"])
        self.assertIn("runtime/state/action/responsibility_loop_state.json", cross_file_logic["state_refs"])
        self.assertIn("runtime/state/validation/observation_truth_review.json", cross_file_logic["state_refs"])
        self.assertTrue(cross_file_logic["repair_priority_refs"])

        self.assertEqual(counterfactual_trace["schema_version"], "counterfactual_trace_v0")
        self.assertTrue(counterfactual_trace["candidate_refs"])
        self.assertTrue(counterfactual_trace["counterfactual_branches"])
        self.assertEqual(counterfactual_trace["archive_requirement"], "required_before_activation")
        self.assertEqual(
            counterfactual_trace["responsibility_loop_ref"],
            "runtime/state/action/responsibility_loop_state.json",
        )
        self.assertEqual(
            counterfactual_trace["repair_obligation_projection"],
            responsibility_loop["repair_obligation_refs"],
        )
        self.assertTrue(counterfactual_trace["regret_pressure_candidate_refs"])

        self.assertEqual(comparison_trace["schema_version"], "comparison_trace_v0")
        self.assertEqual(
            comparison_trace["counterfactual_eval_ref"],
            "runtime/state/schema_runner/counterfactual_trace.json",
        )
        self.assertTrue(comparison_trace["kept_branch_refs"])
        self.assertTrue(comparison_trace["suppressed_branch_refs"])
        self.assertIn("runtime/state/action/responsibility_loop_state.json", comparison_trace["justification_refs"])
        self.assertIn("runtime/state/action/responsibility_loop_state.json", comparison_trace["writeback_targets"])

        self.assertEqual(evidence_ranking["schema_version"], "evidence_ranking_v0")
        self.assertGreaterEqual(evidence_ranking["evidence_density_score"], 0.0)
        self.assertTrue(evidence_ranking["ranked_evidence"])
        self.assertIn("runtime/state/schema_runner/comparison_trace.json", evidence_ranking["state_refs"])
        self.assertIn("runtime/state/schema_runner/cross_file_logic.json", evidence_ranking["state_refs"])
        self.assertTrue(evidence_ranking["priority_budget"])

        self.assertEqual(run_manifest["schema_version"], "schema_runner_run_manifest_v0")
        self.assertEqual(run_manifest["run_status"], "closed")
        self.assertEqual(run_manifest["active_engineering_slice"], "S09_SCHEMA_RUNNER_CODE")
        self.assertIn("build-schema-runner", run_manifest["command_sequence"])
        self.assertIn("runtime/state/schema_runner/cross_file_logic.json", run_manifest["output_refs"])
        self.assertIn("runtime/state/schema_runner/run_manifest.json", run_manifest["output_refs"])
        self.assertIn("runtime/state/action/responsibility_loop_state.json", run_manifest["input_state_refs"])

        self.assertEqual(stage_gate["schema_version"], "schema_runner_stage_gate_v0")
        self.assertEqual(stage_gate["decision"], "closed")
        self.assertEqual(stage_gate["gate_status"]["responsibility_logic_gate"], "closed")
        self.assertEqual(stage_gate["next_allowed_slices"], ["S06_LIFE_SUPPORT_DEVELOPMENT", "S10_RUNTIME_GROWTH_RECONSOLIDATION"])
        self.assertEqual(stage_gate["next_required_command"], "life-v0 build-life-support --strict")

        self.assertEqual(report["schema_version"], "s09_schema_runner_code_report_v0")
        self.assertEqual(report["engineering_slice_ref"], "S09_SCHEMA_RUNNER_CODE")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_next_slice")
        self.assertIn("SchemaBundleCompiler", report["runtime_carrier_refs"])
        self.assertIn("RunnerRepositoryKernel", report["runtime_carrier_refs"])
        self.assertIn("FirstRunnerCodeKernel", report["runtime_carrier_refs"])
        self.assertIn("runtime/state/schema_runner/consistency_logic.json", report["artifact_refs"])
        self.assertIn("runtime/state/schema_runner/cross_file_logic.json", report["artifact_refs"])
        self.assertIn("runtime/state/schema_runner/counterfactual_trace.json", report["artifact_refs"])
        self.assertIn("runtime/state/schema_runner/comparison_trace.json", report["artifact_refs"])
        self.assertIn("runtime/state/schema_runner/evidence_ranking.json", report["artifact_refs"])
        self.assertIn("runtime/state/schema_runner/run_manifest.json", report["artifact_refs"])
        self.assertEqual(report["next_allowed_slices"], ["S06_LIFE_SUPPORT_DEVELOPMENT", "S10_RUNTIME_GROWTH_RECONSOLIDATION"])
        self.assertEqual(report["next_required_command"], "life-v0 build-life-support --strict")

        self.assertEqual(digest["current_slice"], "S09_SCHEMA_RUNNER_CODE")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(smoke_report["schema_version"], "schema_runner_smoke_report_v0")
        self.assertEqual(smoke_report["status"], "closed")
        self.assertEqual(receipt["schema_version"], "schema_runner_receipt_v0")
        self.assertTrue(
            any(key.endswith("responsibility_loop_state.json") for key in receipt["input_hashes"]),
            receipt["input_hashes"],
        )
        self.assertIn(str((paths["schema_runner_state"] / "cross_file_logic.json").resolve()), receipt["output_refs"])
        self.assertIn(str((paths["schema_runner_state"] / "run_manifest.json").resolve()), receipt["output_refs"])

    def test_cli_build_schema_runner_and_smoke_return_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-validation", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli", "--strict"],
                ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "schema-cli-smoke", "--strict"],
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

            report = self._read_json(paths["reports"] / "schema_runner_report.json")
            smoke_report = self._read_json(paths["reports"] / "schema_smoke_report.json")

        self.assertEqual(report["run_id"], "schema-cli")
        self.assertEqual(report["next_required_command"], "life-v0 build-life-support --strict")
        self.assertEqual(smoke_report["status"], "closed")

    def _runtime_paths(self, tmp_path: Path) -> dict[str, Path]:
        return {
            "doc_out": tmp_path / "runtime" / "docs",
            "reports": tmp_path / "runtime" / "reports" / "latest",
            "receipts": tmp_path / "runtime" / "receipts",
            "direction_state": tmp_path / "runtime" / "state" / "direction",
            "authority_state": tmp_path / "runtime" / "state" / "authority",
            "neural_state": tmp_path / "runtime" / "state" / "neural_life_core",
            "state_root": tmp_path / "runtime" / "state",
            "membrane_state": tmp_path / "runtime" / "state" / "membrane",
            "life_targets_state": tmp_path / "runtime" / "state" / "life_targets",
            "validation_state": tmp_path / "runtime" / "state" / "validation",
            "observation_state": tmp_path / "runtime" / "state" / "observation",
            "schema_runner_state": tmp_path / "runtime" / "state" / "schema_runner",
        }

    def _run_pre_s09_chain(self, paths, **kwargs):
        ingest = kwargs["run_doc_ingestion"](
            docs_dir=self.docs_dir,
            out_dir=paths["doc_out"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="schema-ingest",
            strict=True,
        )
        self.assertEqual(ingest.exit_code, 0)

        direction = kwargs["run_direction_lock"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            out_dir=paths["direction_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="schema-direction",
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
            run_id="schema-authority",
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
            run_id="schema-neural",
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
            run_id="schema-state",
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
            run_id="schema-membrane",
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
            run_id="schema-language",
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
            out_dir=paths["life_targets_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="schema-birth",
            strict=True,
        )
        self.assertEqual(birth.exit_code, 0)

        validation = kwargs["run_validation_membrane"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            state_dir=paths["state_root"],
            membrane_dir=paths["membrane_state"],
            life_targets_dir=paths["life_targets_state"],
            validation_dir=paths["validation_state"],
            observation_dir=paths["observation_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="schema-validation",
            strict=True,
        )
        self.assertEqual(validation.exit_code, 0)
        validation_check = kwargs["run_check_validation_membrane"](
            state_dir=paths["state_root"],
            validation_dir=paths["validation_state"],
            observation_dir=paths["observation_state"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(validation_check.exit_code, 0)

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
