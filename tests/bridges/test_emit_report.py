import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class EmitReportTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_run_emit_report_writes_first_activation_return_bundle(self):
        from life_v0.archive import run_write_growth_archive
        from life_v0.reporting import run_emit_report
        from tests.bridges.test_growth_archive import GrowthArchiveTests

        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            helper = GrowthArchiveTests()
            helper._run_pre_growth_archive_chain(
                paths=paths,
                run_doc_ingestion=__import__("life_v0.doc_index", fromlist=["run_doc_ingestion"]).run_doc_ingestion,
                run_direction_lock=__import__("life_v0.direction", fromlist=["run_direction_lock"]).run_direction_lock,
                run_source_authority=__import__("life_v0.authority", fromlist=["run_source_authority"]).run_source_authority,
                run_neural_life_core=__import__("life_v0.neural_core", fromlist=["run_neural_life_core"]).run_neural_life_core,
                run_check_neural_life_core=__import__("life_v0.neural_core", fromlist=["run_check_neural_life_core"]).run_check_neural_life_core,
                run_state_store=__import__("life_v0.state_store", fromlist=["run_state_store"]).run_state_store,
                run_check_state_store=__import__("life_v0.state_store", fromlist=["run_check_state_store"]).run_check_state_store,
                run_life_membrane=__import__("life_v0.membrane", fromlist=["run_life_membrane"]).run_life_membrane,
                run_check_life_membrane=__import__("life_v0.membrane", fromlist=["run_check_life_membrane"]).run_check_life_membrane,
                run_build_language_relationship=__import__("life_v0.language", fromlist=["run_build_language_relationship"]).run_build_language_relationship,
                run_check_language_relationship=__import__("life_v0.language", fromlist=["run_check_language_relationship"]).run_check_language_relationship,
                run_birth_readiness=__import__("life_v0.life_targets", fromlist=["run_birth_readiness"]).run_birth_readiness,
                run_validation_membrane=__import__("life_v0.validators", fromlist=["run_validation_membrane"]).run_validation_membrane,
                run_check_validation_membrane=__import__("life_v0.validators", fromlist=["run_check_validation_membrane"]).run_check_validation_membrane,
                run_schema_runner=__import__("life_v0.schema_runner", fromlist=["run_schema_runner"]).run_schema_runner,
                run_check_schema_runner=__import__("life_v0.schema_runner", fromlist=["run_check_schema_runner"]).run_check_schema_runner,
                run_schema_smoke=__import__("life_v0.schema_runner", fromlist=["run_schema_smoke"]).run_schema_smoke,
                run_life_support=__import__("life_v0.body", fromlist=["run_life_support"]).run_life_support,
                run_check_life_support=__import__("life_v0.body", fromlist=["run_check_life_support"]).run_check_life_support,
                run_cycle=__import__("life_v0.growth", fromlist=["run_cycle"]).run_cycle,
                run_check_v0_contracts=__import__("life_v0.contracts", fromlist=["run_check_v0_contracts"]).run_check_v0_contracts,
                run_first_activation_preflight=__import__("life_v0.activation", fromlist=["run_first_activation_preflight"]).run_first_activation_preflight,
                run_replay_shadow=__import__("life_v0.replay", fromlist=["run_replay_shadow"]).run_replay_shadow,
            )

            archive = run_write_growth_archive(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="emit-archive",
                strict=True,
            )
            self.assertEqual(archive.exit_code, 0)

            result = run_emit_report(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="emit-report-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            bundle = self._read_json(paths["reports"] / "report_bundle.json")
            bundle_digest = self._read_json(paths["reports"] / "report_bundle_digest.json")
            return_packet = self._read_json(paths["reports"] / "first_activation_return_packet.json")
            latest_stage_ref = self._read_json(paths["reports"] / "latest_stage_explanation_ref.json")
            receipt = self._read_json(paths["receipts"] / "emit_report_emit-report-test.json")

        self.assertEqual(bundle["schema_version"], "report_bundle_v0")
        self.assertEqual(bundle["status"], "closed")
        self.assertEqual(bundle["next_required_command"], "life-v0 explain-stage --strict")
        self.assertTrue(bundle["report_refs"])

        self.assertEqual(bundle_digest["schema_version"], "report_bundle_digest_v0")
        self.assertEqual(bundle_digest["status"], "closed")

        self.assertEqual(return_packet["schema_version"], "first_activation_return_packet_v0")
        self.assertEqual(return_packet["status"], "closed")
        self.assertTrue(return_packet["relation_restore_refs"])
        self.assertTrue(return_packet["shared_term_restore_refs"])
        self.assertTrue(return_packet["expression_monitor_restore_refs"])

        self.assertEqual(latest_stage_ref["schema_version"], "latest_stage_explanation_ref_v0")
        self.assertEqual(latest_stage_ref["next_required_command"], "life-v0 explain-stage --strict")
        self.assertEqual(receipt["schema_version"], "emit_report_receipt_v0")

    def test_cli_emit_report_returns_zero_and_writes_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            commands = [
                ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-ingest", "--strict"],
                ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-direction", "--strict"],
                ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-authority", "--strict"],
                ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-neural", "--strict"],
                ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-state", "--strict"],
                ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-membrane", "--strict"],
                ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-language", "--strict"],
                ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-birth", "--strict"],
                ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-validation", "--strict"],
                ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-schema", "--strict"],
                ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-smoke", "--strict"],
                ["build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-support", "--strict"],
                ["check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["run-cycle", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-cycle", "--shadow-only", "--strict"],
                ["check-v0-contracts", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-contracts", "--strict"],
                ["first-activation-preflight", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-preflight", "--strict"],
                ["run-replay-shadow", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-replay", "--strict"],
                ["write-growth-archive", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli-archive", "--strict"],
                ["emit-report", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "emit-cli", "--strict"],
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

            bundle = self._read_json(paths["reports"] / "report_bundle.json")
            return_packet = self._read_json(paths["reports"] / "first_activation_return_packet.json")

        self.assertEqual(bundle["run_id"], "emit-cli")
        self.assertEqual(bundle["status"], "closed")
        self.assertEqual(return_packet["status"], "closed")

    def _runtime_paths(self, tmp_path: Path) -> dict[str, Path]:
        state_root = tmp_path / "runtime" / "state"
        runtime_root = tmp_path / "runtime"
        return {
            "runtime_root": runtime_root,
            "doc_out": runtime_root / "docs",
            "reports": runtime_root / "reports" / "latest",
            "receipts": runtime_root / "receipts",
            "direction_state": state_root / "direction",
            "authority_state": state_root / "authority",
            "neural_state": state_root / "neural_life_core",
            "state_root": state_root,
            "membrane_state": state_root / "membrane",
            "life_targets_state": state_root / "life_targets",
            "validation_state": state_root / "validation",
            "observation_state": state_root / "observation",
            "schema_runner_state": state_root / "schema_runner",
        }

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
