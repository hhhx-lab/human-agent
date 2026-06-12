import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class V0ContractCoverageTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_v0_doc_references_to_theory_docs_resolve(self):
        pattern = re.compile(r"`(docs/[^`\n*]+?\.md)`")
        missing: list[tuple[str, str]] = []

        for path in (self.docs_dir / "v0").rglob("*.md"):
            content = path.read_text(encoding="utf-8")
            for ref in pattern.findall(content):
                if not (self.repo_root / ref).exists():
                    missing.append((str(path.relative_to(self.repo_root)), ref))

        self.assertEqual(missing, [], f"unresolved docs/v0 theory refs: {missing}")

    def test_check_v0_contracts_writes_coverage_matrices_and_preflight_report(self):
        from life_v0.authority import run_source_authority
        from life_v0.body import run_check_life_support, run_life_support
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
        from life_v0.growth import run_cycle
        from life_v0.language import run_build_language_relationship, run_check_language_relationship
        from life_v0.life_targets import run_birth_readiness
        from life_v0.membrane import run_check_life_membrane, run_life_membrane
        from life_v0.neural_core import run_check_neural_life_core, run_neural_life_core
        from life_v0.schema_runner import run_check_schema_runner, run_schema_runner, run_schema_smoke
        from life_v0.state_store import run_check_state_store, run_state_store
        from life_v0.validators import run_check_validation_membrane, run_validation_membrane

        from life_v0.contracts import run_check_v0_contracts

        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            self._run_pre_s11_chain(
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
                run_schema_runner=run_schema_runner,
                run_check_schema_runner=run_check_schema_runner,
                run_schema_smoke=run_schema_smoke,
                run_life_support=run_life_support,
                run_check_life_support=run_check_life_support,
                run_cycle=run_cycle,
            )

            result = run_check_v0_contracts(
                docs_dir=self.docs_dir,
                doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="v0-contracts-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            contract_index = self._read_json(paths["contracts_state"] / "v0_contract_file_index.json")
            doc_to_code = self._read_json(paths["contracts_state"] / "doc_to_code_coverage_matrix.json")
            slice_matrix = self._read_json(paths["contracts_state"] / "slice_report_receipt_matrix.json")
            carrier_matrix = self._read_json(paths["contracts_state"] / "runtime_carrier_coverage_matrix.json")
            preflight = self._read_json(paths["contracts_state"] / "first_activation_preflight_contract_check.json")
            report = self._read_json(paths["reports"] / "v0_contract_coverage_report.json")
            digest = self._read_json(paths["reports"] / "v0_contract_coverage_digest.json")
            receipt = self._read_json(paths["receipts"] / "v0_contract_coverage_v0-contracts-test.json")

        self.assertEqual(contract_index["schema_version"], "v0_contract_file_index_v0")
        self.assertIn("docs/v0/README.md", contract_index["files"])
        self.assertIn("docs/v0/entry/README.md", contract_index["files"])
        self.assertIn("docs/v0/mapping/README.md", contract_index["files"])
        self.assertIn("docs/v0/architecture/README.md", contract_index["files"])
        self.assertIn("docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md", contract_index["files"])
        self.assertIn("docs/v0/process_contracts/README.md", contract_index["files"])
        self.assertIn("docs/v0/references/README.md", contract_index["files"])
        self.assertIn("docs/v0/shared_contracts/README.md", contract_index["files"])
        self.assertIn("docs/v0/slice_contracts/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_framework/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_framework/foundation/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_framework/playbooks/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_framework/delivery/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_framework/queues/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_framework/assembly/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_architecture/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_blueprints/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_blueprints/01_full_system_code_blueprint.md", contract_index["files"])
        self.assertIn("docs/v0/code_blueprints/02_conversation_language_relationship_blueprint.md", contract_index["files"])
        self.assertIn("docs/v0/code_blueprints/03_body_affect_dream_growth_blueprint.md", contract_index["files"])
        self.assertIn("docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md", contract_index["files"])
        self.assertIn("docs/v0/code_blueprints/05_birth_residency_terminal_blueprint.md", contract_index["files"])
        self.assertIn("docs/v0/code_blueprints/06_runtime_state_report_receipt_manifest.md", contract_index["files"])
        self.assertIn("docs/v0/code_blueprints/07_theory_to_package_trace_contract.md", contract_index["files"])
        self.assertIn("docs/v0/code_scaffolds/README.md", contract_index["files"])
        self.assertIn("docs/v0/code_scaffolds/01_life_code_scaffold_tree.md", contract_index["files"])
        self.assertIn("docs/v0/code_scaffolds/02_cognitive_loop_code_scaffold.md", contract_index["files"])
        self.assertIn("docs/v0/code_scaffolds/03_frontier_module_build_packets.md", contract_index["files"])
        self.assertIn("docs/v0/code_scaffolds/04_packet_b_world_observation_periphery_scaffold.md", contract_index["files"])
        self.assertIn("docs/v0/code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md", contract_index["files"])
        self.assertIn("docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md", contract_index["files"])
        self.assertIn("docs/v0/code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md", contract_index["files"])
        self.assertIn(
            "docs/v0/code_architecture/01_life_code_stack_and_package_layers.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/code_architecture/02_runtime_object_bus_and_flow_contract.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/code_architecture/03_build_order_and_definition_of_done.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/code_architecture/04_language_as_primary_expression_system.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/code_architecture/05_module_reading_and_execution_map.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/code_architecture/06_theory_gap_closure_register.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/code_framework/delivery/22_live0_acceptance_audit_contract.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
            contract_index["files"],
        )
        self.assertIn("docs/v0/implementation_architecture/README.md", contract_index["files"])
        self.assertIn(
            "docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/implementation_architecture/02_turn_and_cycle_lifecycle_contract.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/implementation_architecture/03_module_authoring_traceability_protocol.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/implementation_architecture/code_organs/README.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/implementation_architecture/code_organs/01_life_v0_package_organ_split_map.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/implementation_architecture/code_organs/02_heavy_init_refactor_wave_contract.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md",
            contract_index["files"],
        )
        self.assertIn("docs/v0/engineering_depth/README.md", contract_index["files"])
        self.assertIn(
            "docs/v0/engineering_depth/01_full_life_layer_implementation_deep_spec.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/engineering_depth/02_state_object_runtime_evidence_map.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/engineering_depth/03_language_relationship_longitudinal_engineering.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/engineering_depth/04_body_affect_dream_growth_engineering.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md",
            contract_index["files"],
        )
        self.assertIn(
            "docs/v0/engineering_depth/07_theory_to_code_trace_matrix.md",
            contract_index["files"],
        )
        self.assertIn("docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md", contract_index["files"])
        self.assertIn("docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md", contract_index["files"])

        self.assertEqual(doc_to_code["schema_version"], "doc_to_code_coverage_matrix_v0")
        self.assertEqual(doc_to_code["coverage_summary"]["uncovered_docs"], [])
        self.assertIn("docs/258_linear_chain_closure_and_v0_contract_transition.md", doc_to_code["documents"])
        self.assertEqual(
            doc_to_code["documents"]["docs/258_linear_chain_closure_and_v0_contract_transition.md"]["engineering_slice"],
            "S00_DIRECTION_FOUNDATION",
        )

        self.assertEqual(slice_matrix["schema_version"], "slice_report_receipt_matrix_v0")
        self.assertEqual(slice_matrix["slices"]["P0_DOC_CORPUS_INGESTION"]["status"], "closed")
        self.assertEqual(slice_matrix["slices"]["S10_RUNTIME_GROWTH_RECONSOLIDATION"]["status"], "closed")
        self.assertEqual(slice_matrix["slices"]["S07_LANGUAGE_RELATIONSHIP"]["status"], "closed")

        self.assertEqual(carrier_matrix["schema_version"], "runtime_carrier_coverage_matrix_v0")
        self.assertIn("DirectionLockKernel", carrier_matrix["runtime_carriers"])
        self.assertIn("V0ContractCoverageRuntime", carrier_matrix["runtime_carriers"])

        self.assertEqual(preflight["schema_version"], "first_activation_preflight_contract_check_v0")
        self.assertTrue(preflight["activation_preflight_allowed"])
        self.assertEqual(preflight["required_reports"]["run_report"]["status"], "closed")
        self.assertEqual(preflight["required_reports"]["stage_gate"]["status"], "closed")

        self.assertEqual(report["schema_version"], "s11_v0_contract_coverage_report_v0")
        self.assertEqual(report["engineering_slice_ref"], "S11_V0_ENGINEERING_CONTRACTS")
        self.assertEqual(report["status"], "closed")
        self.assertTrue(report["activation_preflight_allowed"])
        self.assertEqual(report["readme_block_refs"], ["B99_V0_ENGINEERING_CONTRACTS"])
        self.assertEqual(report["runtime_carrier_refs"], ["V0ContractCoverageRuntime"])
        self.assertEqual(report["next_required_command"], "life-v0 first-activation-preflight --strict")

        self.assertEqual(digest["schema_version"], "v0_contract_coverage_digest_v0")
        self.assertEqual(digest["current_slice"], "S11_V0_ENGINEERING_CONTRACTS")
        self.assertEqual(digest["status"], "closed")
        self.assertEqual(digest["next_required_command"], "life-v0 first-activation-preflight --strict")
        self.assertEqual(receipt["schema_version"], "v0_contract_coverage_receipt_v0")

    def test_cli_check_v0_contracts_returns_zero_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-validation", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-schema", "--strict"],
                ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-smoke", "--strict"],
                ["build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-support", "--strict"],
                ["check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-cycle", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli-cycle", "--shadow-only", "--strict"],
                ["check-v0-contracts", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "contracts-cli", "--strict"],
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

            report = self._read_json(paths["reports"] / "v0_contract_coverage_report.json")
            digest = self._read_json(paths["reports"] / "v0_contract_coverage_digest.json")
            preflight = self._read_json(paths["contracts_state"] / "first_activation_preflight_contract_check.json")

        self.assertEqual(report["run_id"], "contracts-cli")
        self.assertEqual(report["status"], "closed")
        self.assertTrue(report["activation_preflight_allowed"])
        self.assertEqual(report["next_required_command"], "life-v0 first-activation-preflight --strict")
        self.assertEqual(digest["current_slice"], "S11_V0_ENGINEERING_CONTRACTS")
        self.assertEqual(digest["next_required_command"], "life-v0 first-activation-preflight --strict")
        self.assertTrue(preflight["activation_preflight_allowed"])

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
            "life_targets_state": state_root / "life_targets",
            "validation_state": state_root / "validation",
            "observation_state": state_root / "observation",
            "schema_runner_state": state_root / "schema_runner",
            "contracts_state": state_root / "contracts",
        }

    def _run_pre_s11_chain(self, paths, **kwargs):
        ingest = kwargs["run_doc_ingestion"](
            docs_dir=self.docs_dir,
            out_dir=paths["doc_out"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="contracts-ingest",
            strict=True,
        )
        self.assertEqual(ingest.exit_code, 0)

        direction = kwargs["run_direction_lock"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            out_dir=paths["direction_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="contracts-direction",
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
            run_id="contracts-authority",
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
            run_id="contracts-neural",
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
            run_id="contracts-state",
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
            run_id="contracts-membrane",
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
            run_id="contracts-language",
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
            run_id="contracts-birth",
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
            run_id="contracts-validation",
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

        schema_runner = kwargs["run_schema_runner"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="contracts-schema",
            strict=True,
        )
        self.assertEqual(schema_runner.exit_code, 0)
        schema_check = kwargs["run_check_schema_runner"](
            state_dir=paths["schema_runner_state"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(schema_check.exit_code, 0)
        schema_smoke = kwargs["run_schema_smoke"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="contracts-schema-smoke",
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
            run_id="contracts-life-support",
            strict=True,
        )
        self.assertEqual(life_support.exit_code, 0)
        life_support_check = kwargs["run_check_life_support"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            strict=True,
        )
        self.assertEqual(life_support_check.exit_code, 0)

        cycle = kwargs["run_cycle"](
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="contracts-cycle",
            shadow_only=True,
            strict=True,
        )
        self.assertEqual(cycle.exit_code, 0)

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
