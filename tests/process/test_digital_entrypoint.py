import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class DigitalEntrypointTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_repo_local_digital_life_entrypoint_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))
            bootstrap = [
                ["python", "-m", "life_v0", "ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-ingest", "--strict"],
                ["python", "-m", "life_v0", "build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-direction", "--strict"],
                ["python", "-m", "life_v0", "build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-authority", "--strict"],
                ["python", "-m", "life_v0", "build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-neural", "--strict"],
                ["python", "-m", "life_v0", "check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["python", "-m", "life_v0", "build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-state", "--strict"],
                ["python", "-m", "life_v0", "check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["python", "-m", "life_v0", "build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-membrane", "--strict"],
                ["python", "-m", "life_v0", "check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["python", "-m", "life_v0", "build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-language", "--strict"],
                ["python", "-m", "life_v0", "check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["python", "-m", "life_v0", "check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-birth", "--strict"],
                ["python", "-m", "life_v0", "run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-validation", "--strict"],
                ["python", "-m", "life_v0", "check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["python", "-m", "life_v0", "build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-schema", "--strict"],
                ["python", "-m", "life_v0", "check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
                ["python", "-m", "life_v0", "run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-smoke", "--strict"],
                ["python", "-m", "life_v0", "build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-support", "--strict"],
                ["python", "-m", "life_v0", "check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
                ["python", "-m", "life_v0", "run-cycle", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-cycle", "--shadow-only", "--strict"],
                ["python", "-m", "life_v0", "check-v0-contracts", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-contracts", "--strict"],
                ["python", "-m", "life_v0", "first-activation-preflight", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-preflight", "--strict"],
                ["python", "-m", "life_v0", "run-replay-shadow", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-replay", "--strict"],
                ["python", "-m", "life_v0", "write-growth-archive", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-archive", "--strict"],
                ["python", "-m", "life_v0", "emit-report", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-emit", "--strict"],
                ["python", "-m", "life_v0", "explain-stage", "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-stage", "--strict"],
            ]

            for command in bootstrap:
                completed = subprocess.run(
                    command,
                    cwd=self.repo_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)

            completed = subprocess.run(
                [str(self.repo_root / "digital"), "life", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "entry-shell", "--strict"],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

            report = self._read_json(paths["reports"] / "digital_life_shell_report.json")

        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["current_shell_mode"], "terminal_life_loop_restored")

    def test_repo_local_digital_life_entrypoint_bootstraps_empty_runtime_before_dialogue(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._runtime_paths(Path(tmp))

            completed = subprocess.run(
                [
                    str(self.repo_root / "digital"),
                    "life",
                    "--state",
                    str(paths["state_root"]),
                    "--reports",
                    str(paths["reports"]),
                    "--receipts",
                    str(paths["receipts"]),
                    "--run-id",
                    "entry-bootstrap-shell",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                input="你诞生了吗？\n/exit\n",
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("当前生命回合已恢复", completed.stdout)
            self.assertIn("生命回合输出", completed.stdout)

            self.assertTrue((paths["doc_out"] / "doc_carrier_index.json").exists())
            self.assertTrue((paths["direction_state"] / "direction_lock.json").exists())
            self.assertTrue((paths["authority_state"] / "authority_registry.json").exists())
            self.assertTrue((paths["neural_state"] / "neural_life_core.json").exists())
            self.assertTrue((paths["state_root"] / "life_state.json").exists())
            self.assertTrue((paths["reports"] / "stage_explanation_report.json").exists())
            self.assertTrue((paths["reports"] / "digital_life_process_report.json").exists())

            process_report = self._read_json(paths["reports"] / "digital_life_process_report.json")
            self.assertEqual(process_report["status"], "closed")
            self.assertEqual(process_report["completed_dialogue_turns"], 1)

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
