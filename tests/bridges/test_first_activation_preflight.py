import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class FirstActivationPreflightTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_run_first_activation_preflight_writes_activation_bundle(self):
        from life_v0.activation import run_first_activation_preflight
        from life_v0.authority import run_source_authority
        from life_v0.body import run_check_life_support, run_life_support
        from life_v0.contracts import run_check_v0_contracts
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

        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            self._run_pre_activation_chain(
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
                run_check_v0_contracts=run_check_v0_contracts,
            )

            result = run_first_activation_preflight(
                docs_dir=self.docs_dir,
                doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="first-activation-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            context_frame = self._read_json(paths["activation_state"] / "limited_context_frame.json")
            membrane_decision = self._read_json(paths["activation_state"] / "life_membrane_opening_decision.json")
            report = self._read_json(paths["reports"] / "first_activation_preflight_report.json")
            digest = self._read_json(paths["reports"] / "first_activation_preflight_digest.json")
            receipt = self._read_json(paths["receipts"] / "first_activation_preflight_first-activation-test.json")

        self.assertEqual(context_frame["schema_version"], "limited_context_frame_v0")
        self.assertEqual(context_frame["status"], "closed")
        self.assertEqual(context_frame["activation_mode"], "shadow_only")
        self.assertTrue(context_frame["relationship_subject_refs"])
        self.assertTrue(context_frame["expression_monitor_refs"])
        self.assertTrue(context_frame["relation_scope_refs"])
        self.assertTrue(context_frame["self_narrative_trace_refs"])
        self.assertTrue(context_frame["dialogue_turn_log_refs"])
        self.assertTrue(context_frame["commitment_refs"])

        self.assertEqual(membrane_decision["schema_version"], "life_membrane_opening_decision_v0")
        self.assertEqual(membrane_decision["decision"], "open_shadow_only")
        self.assertEqual(membrane_decision["status"], "closed")

        self.assertEqual(report["schema_version"], "first_activation_preflight_report_v0")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_replay_shadow")
        self.assertEqual(report["next_required_command"], "life-v0 run-replay-shadow --strict")
        self.assertEqual(report["activation_mode"], "shadow_only")
        self.assertTrue(report["contract_refs"])

        self.assertEqual(digest["schema_version"], "first_activation_preflight_digest_v0")
        self.assertEqual(digest["current_phase"], "activation_preflight")
        self.assertEqual(digest["status"], "closed")

        self.assertEqual(receipt["schema_version"], "first_activation_preflight_receipt_v0")
        self.assertEqual(receipt["command"], "first-activation-preflight")

    def test_cli_first_activation_preflight_returns_zero_and_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-validation", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-schema", "--strict"],
                ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-smoke", "--strict"],
                ["build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-support", "--strict"],
                ["check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-cycle", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-cycle", "--shadow-only", "--strict"],
                ["check-v0-contracts", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli-contracts", "--strict"],
                ["first-activation-preflight", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "activation-cli", "--strict"],
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

            report = self._read_json(paths["reports"] / "first_activation_preflight_report.json")
            digest = self._read_json(paths["reports"] / "first_activation_preflight_digest.json")
            context_frame = self._read_json(paths["activation_state"] / "limited_context_frame.json")

        self.assertEqual(report["run_id"], "activation-cli")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["next_required_command"], "life-v0 run-replay-shadow --strict")
        self.assertEqual(digest["current_phase"], "activation_preflight")
        self.assertEqual(context_frame["status"], "closed")

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
            "life_targets_state": state_root / "life_targets",
            "validation_state": state_root / "validation",
            "observation_state": state_root / "observation",
            "schema_runner_state": state_root / "schema_runner",
            "activation_state": state_root / "activation",
        }

    def _run_pre_activation_chain(self, *, paths, **kwargs):
        ingest = kwargs["run_doc_ingestion"](
            docs_dir=self.docs_dir,
            out_dir=paths["doc_out"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="activation-ingest",
            strict=True,
        )
        self.assertEqual(ingest.exit_code, 0)

        direction = kwargs["run_direction_lock"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            out_dir=paths["direction_state"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="activation-direction",
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
            run_id="activation-authority",
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
            run_id="activation-neural",
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
            run_id="activation-state",
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
            run_id="activation-membrane",
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
            run_id="activation-language",
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
            run_id="activation-birth",
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
            run_id="activation-validation",
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
            run_id="activation-schema",
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
            run_id="activation-smoke",
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
            run_id="activation-support",
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
            run_id="activation-cycle",
            shadow_only=True,
            strict=True,
        )
        self.assertEqual(cycle.exit_code, 0)

        contracts = kwargs["run_check_v0_contracts"](
            docs_dir=self.docs_dir,
            doc_index_path=paths["doc_out"] / "doc_carrier_index.json",
            state_dir=paths["state_root"],
            reports_dir=paths["reports"],
            receipts_dir=paths["receipts"],
            run_id="activation-contracts",
            strict=True,
        )
        self.assertEqual(contracts.exit_code, 0)

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
