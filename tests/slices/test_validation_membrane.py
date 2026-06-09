import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ValidationMembraneTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_run_validation_membrane_writes_rule_observation_dashboard_and_receipt(self):
        from life_v0.authority import run_source_authority
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
        from life_v0.language import run_build_language_relationship, run_check_language_relationship
        from life_v0.life_targets import run_birth_readiness
        from life_v0.membrane import run_check_life_membrane, run_life_membrane
        from life_v0.neural_core import run_check_neural_life_core, run_neural_life_core
        from life_v0.state_store import run_check_state_store, run_state_store
        from life_v0.validators import run_check_validation_membrane, run_validation_membrane

        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            self._run_pre_s05_chain(
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
            )

            result = run_validation_membrane(
                docs_dir=self.docs_dir,
                doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
                state_dir=paths["state_root"],
                membrane_dir=paths["membrane_state"],
                life_targets_dir=paths["life_targets_state"],
                validation_dir=paths["validation_state"],
                observation_dir=paths["observation_state"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="validation-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            check = run_check_validation_membrane(
                state_dir=paths["state_root"],
                validation_dir=paths["validation_state"],
                observation_dir=paths["observation_state"],
                reports_dir=paths["reports"],
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            rules = self._read_json(paths["validation_state"] / "validator_rule_index.json")
            observation = self._read_json(paths["observation_state"] / "runtime_observation_intake.json")
            quarantine = self._read_json(paths["validation_state"] / "quarantine_packet_index.json")
            dashboard = self._read_json(paths["validation_state"] / "dashboard_metric_source.json")
            findings = self._read_json(paths["validation_state"] / "cross_file_finding_index.json")
            truth_review = self._read_json(paths["validation_state"] / "observation_truth_review.json")
            world_contact_validation = self._read_json(paths["validation_state"] / "world_contact_validation.json")
            prediction_trace_validation = self._read_json(paths["validation_state"] / "prediction_trace_validation.json")
            boundary_audit = self._read_json(paths["validation_state"] / "boundary_audit_state.json")
            validation_rollup = self._read_json(paths["validation_state"] / "validation_rollup.json")
            stage_gate = self._read_json(paths["validation_state"] / "validation_stage_gate.json")
            report = self._read_json(paths["reports"] / "validation_membrane_report.json")
            world_contact_report = self._read_json(paths["reports"] / "world_contact_audit_report.json")
            side_effect_report = self._read_json(paths["reports"] / "side_effect_review_report.json")
            digest = self._read_json(paths["reports"] / "validation_membrane_digest.json")
            check_report = self._read_json(paths["reports"] / "validation_membrane_check_report.json")
            receipt = self._read_json(paths["receipts"] / "validation_membrane_validation-test.json")

        self.assertEqual(rules["schema_version"], "validator_rule_index_v0")
        self.assertEqual(rules["active_engineering_slice"], "S05_VALIDATION_MEMBRANE_OBSERVATION")
        expected_rule_docs = {
            "docs/29_memory_validator_rules.md",
            "docs/30_state_transition_validator_rules.md",
            "docs/31_consolidation_validator_rules.md",
            "docs/32_runtime_adapter_validator_rules.md",
            "docs/33_validator_input_contracts.md",
            "docs/34_validator_fixture_catalog.md",
            "docs/35_minimal_validator_runner_design.md",
            "docs/36_longitudinal_evaluation_protocol.md",
        }
        self.assertTrue(expected_rule_docs.issubset(set(rules["source_doc_refs"])))
        self.assertIn("MemoryTraceValidator", rules["rule_families"])
        self.assertIn("RuntimeAdapterManifestValidator", rules["rule_families"])
        self.assertIn("LongitudinalEvaluationRule", rules["rule_families"])

        self.assertEqual(observation["schema_version"], "runtime_observation_intake_v0")
        self.assertEqual(observation["redaction_policy"], "runtime_observation_redaction")
        self.assertEqual(observation["side_effect_policy"], "shadow_only_external_action")
        self.assertIn("runtime/state/membrane/shadow_action_gate.json", observation["membrane_refs"])
        self.assertIn("runtime/reports/latest/birth_readiness_report.json", observation["report_refs"])

        self.assertEqual(quarantine["schema_version"], "quarantine_packet_index_v0")
        self.assertEqual(quarantine["status"], "closed")
        self.assertEqual(quarantine["quarantine_refs"], [])
        self.assertIn("dream_fact_pollution", quarantine["quarantine_channels"])
        self.assertIn("external_irreversible_action", quarantine["quarantine_channels"])

        self.assertEqual(dashboard["schema_version"], "dashboard_metric_source_v0")
        self.assertIn("life_membrane_panel", dashboard["panels"])
        self.assertIn("birth_readiness_panel", dashboard["panels"])
        self.assertIn("validation_findings_panel", dashboard["panels"])
        self.assertIn("archive_cross_file_panel", dashboard["panels"])

        self.assertEqual(findings["schema_version"], "cross_file_finding_index_v0")
        self.assertEqual(findings["status"], "closed")
        self.assertEqual(findings["findings"], [])
        self.assertIn("docs/153_life_reality_full_archive_cross_file_checker_rollup_plan.md", findings["source_doc_refs"])
        self.assertIn("runtime/receipts/validation_membrane_validation-test.json", findings["receipt_refs"])

        self.assertEqual(truth_review["schema_version"], "observation_truth_review_v0")
        self.assertTrue(truth_review["observation_event_refs"])
        self.assertEqual(
            truth_review["prediction_workspace_ref"],
            "runtime/state/prediction/prediction_workspace_frame.json",
        )
        self.assertEqual(truth_review["missing_fields"], [])

        self.assertEqual(world_contact_validation["schema_version"], "world_contact_validation_v0")
        self.assertEqual(world_contact_validation["status"], "closed")
        self.assertEqual(
            world_contact_validation["confirmation_binding_ref"],
            "runtime/state/membrane/confirmation_binding.json",
        )
        self.assertEqual(world_contact_validation["validation_findings"], [])

        self.assertEqual(prediction_trace_validation["schema_version"], "prediction_trace_validation_v0")
        self.assertEqual(prediction_trace_validation["status"], "closed")
        self.assertEqual(
            prediction_trace_validation["action_intent_queue_ref"],
            "runtime/state/membrane/action_intent_queue.json",
        )
        self.assertEqual(prediction_trace_validation["missing_prediction_links"], [])

        self.assertEqual(validation_rollup["schema_version"], "validation_rollup_v0")
        self.assertEqual(validation_rollup["overall_status"], "closed")
        self.assertEqual(validation_rollup["blocked_gates"], [])
        self.assertEqual(validation_rollup["guarded_gates"], [])
        self.assertTrue(validation_rollup["next_stage_ready"])
        self.assertIn("runtime/state/validation/world_contact_validation.json", validation_rollup["state_refs"])

        self.assertEqual(boundary_audit["schema_version"], "boundary_audit_state_v0")
        self.assertEqual(boundary_audit["life_membrane_ref"], "runtime/state/membrane/life_membrane.json")
        self.assertEqual(
            boundary_audit["world_contact_gate_ref"],
            "runtime/state/action/world_contact_gate_state.json",
        )
        self.assertEqual(boundary_audit["audit_findings"], [])

        self.assertEqual(stage_gate["schema_version"], "validation_stage_gate_v0")
        self.assertEqual(stage_gate["decision"], "closed")
        self.assertEqual(stage_gate["next_allowed_slices"], ["S09_SCHEMA_RUNNER_CODE"])
        self.assertEqual(stage_gate["next_required_command"], "life-v0 build-schema-runner --strict")

        self.assertEqual(report["schema_version"], "s05_validation_membrane_observation_report_v0")
        self.assertEqual(report["engineering_slice_ref"], "S05_VALIDATION_MEMBRANE_OBSERVATION")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_next_slice")
        self.assertIn("LifeMembraneStageGate", report["runtime_carrier_refs"])
        self.assertIn("RuntimeObservationIngestor", report["runtime_carrier_refs"])
        self.assertIn("ActionResponsibilityRuntime", report["runtime_carrier_refs"])
        self.assertIn("runtime/state/validation/observation_truth_review.json", report["state_refs"])
        self.assertIn("runtime/state/validation/world_contact_validation.json", report["state_refs"])
        self.assertIn("runtime/state/validation/prediction_trace_validation.json", report["state_refs"])
        self.assertIn("runtime/state/validation/validation_rollup.json", report["state_refs"])
        self.assertIn("runtime/state/validation/boundary_audit_state.json", report["state_refs"])
        self.assertEqual(report["next_allowed_slices"], ["S09_SCHEMA_RUNNER_CODE"])
        self.assertEqual(report["next_required_command"], "life-v0 build-schema-runner --strict")

        self.assertEqual(world_contact_report["schema_version"], "world_contact_audit_report_v0")
        self.assertEqual(world_contact_report["status"], "closed")
        self.assertEqual(
            world_contact_report["world_contact_gate_ref"],
            "runtime/state/action/world_contact_gate_state.json",
        )

        self.assertEqual(side_effect_report["schema_version"], "side_effect_review_report_v0")
        self.assertEqual(side_effect_report["status"], "closed")
        self.assertEqual(
            side_effect_report["side_effect_review_ref"],
            "runtime/state/action/side_effect_review.json",
        )

        self.assertEqual(digest["current_slice"], "S05_VALIDATION_MEMBRANE_OBSERVATION")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(receipt["schema_version"], "validation_membrane_receipt_v0")

    def test_cli_run_validation_membrane_returns_zero_and_writes_check_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "validation-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "validation-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "validation-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "validation-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "validation-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "validation-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "validation-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "validation-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "validation-cli", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
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

            report = self._read_json(paths["reports"] / "validation_membrane_report.json")
            check_report = self._read_json(paths["reports"] / "validation_membrane_check_report.json")

        self.assertEqual(report["run_id"], "validation-cli")
        self.assertEqual(report["next_required_command"], "life-v0 build-schema-runner --strict")
        self.assertEqual(check_report["status"], "closed")

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
        }

    def _run_pre_s05_chain(self, paths, **kwargs):
        ingest = kwargs["run_doc_ingestion"](
            docs_dir=self.docs_dir,
            out_dir=paths["doc_out"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="validation-ingest",
            strict=True,
        )
        self.assertEqual(ingest.exit_code, 0)

        direction = kwargs["run_direction_lock"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            out_dir=paths["direction_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="validation-direction",
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
            run_id="validation-authority",
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
            run_id="validation-neural",
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
            run_id="validation-state",
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
            run_id="validation-membrane",
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
            run_id="validation-language",
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
            run_id="validation-birth",
            strict=True,
        )
        self.assertEqual(birth.exit_code, 0)

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
