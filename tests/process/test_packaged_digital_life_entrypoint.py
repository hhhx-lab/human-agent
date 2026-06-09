import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class PackagedDigitalLifeEntrypointTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_editable_install_exposes_life_v0_and_digital_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            venv_dir = tmp_path / "venv"
            runtime_paths = self._runtime_paths(tmp_path)

            subprocess.run(
                [sys.executable, "-m", "venv", str(venv_dir)],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=True,
            )

            python_bin, bin_dir = self._venv_bins(venv_dir)

            install = subprocess.run(
                [str(python_bin), "-m", "pip", "install", "-e", str(self.repo_root)],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(install.returncode, 0, install.stderr)

            life_v0_help = subprocess.run(
                [str(bin_dir / "life-v0"), "--help"],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(life_v0_help.returncode, 0, life_v0_help.stderr)
            self.assertIn("life-v0", life_v0_help.stdout)

            digital_help = subprocess.run(
                [str(bin_dir / "digital"), "--help"],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(digital_help.returncode, 0, digital_help.stderr)
            self.assertIn("life", digital_help.stdout)

            self._bootstrap(runtime_paths, life_v0_bin=bin_dir / "life-v0")

            digital_life = subprocess.run(
                [
                    str(bin_dir / "digital"),
                    "life",
                    "--state",
                    str(runtime_paths["state_root"]),
                    "--reports",
                    str(runtime_paths["reports"]),
                    "--receipts",
                    str(runtime_paths["receipts"]),
                    "--run-id",
                    "packaged-shell",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                input="你在吗？\n/exit\n",
                capture_output=True,
                check=False,
            )

            self.assertEqual(digital_life.returncode, 0, digital_life.stderr)
            self.assertIn("当前生命回合已恢复", digital_life.stdout)
            self.assertIn("生命回合输出", digital_life.stdout)

            process_report = self._read_json(runtime_paths["reports"] / "digital_life_process_report.json")
            self.assertEqual(process_report["status"], "closed")
            self.assertEqual(process_report["completed_dialogue_turns"], 1)
            self.assertEqual(process_report["exit_reason"], "explicit_exit")

    def test_editable_install_digital_command_bootstraps_empty_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            venv_dir = tmp_path / "venv"
            runtime_paths = self._runtime_paths(tmp_path)

            subprocess.run(
                [sys.executable, "-m", "venv", str(venv_dir)],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=True,
            )

            python_bin, bin_dir = self._venv_bins(venv_dir)

            install = subprocess.run(
                [str(python_bin), "-m", "pip", "install", "-e", str(self.repo_root)],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(install.returncode, 0, install.stderr)

            digital_life = subprocess.run(
                [
                    str(bin_dir / "digital"),
                    "life",
                    "--state",
                    str(runtime_paths["state_root"]),
                    "--reports",
                    str(runtime_paths["reports"]),
                    "--receipts",
                    str(runtime_paths["receipts"]),
                    "--run-id",
                    "packaged-bootstrap-shell",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                input="你刚诞生吗？\n/exit\n",
                capture_output=True,
                check=False,
            )

            self.assertEqual(digital_life.returncode, 0, digital_life.stderr)
            self.assertTrue((runtime_paths["doc_out"] / "doc_carrier_index.json").exists())
            self.assertTrue((runtime_paths["reports"] / "stage_explanation_report.json").exists())
            process_report = self._read_json(runtime_paths["reports"] / "digital_life_process_report.json")

        self.assertEqual(process_report["status"], "closed")
        self.assertEqual(process_report["completed_dialogue_turns"], 1)

    def _bootstrap(self, paths: dict[str, Path], *, life_v0_bin: Path) -> None:
        commands = [
            ["ingest-docs", "--docs", str(self.docs_dir), "--out", str(paths["doc_out"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-ingest", "--strict"],
            ["build-direction-lock", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--out", str(paths["direction_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-direction", "--strict"],
            ["build-source-authority", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--out", str(paths["authority_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-authority", "--strict"],
            ["build-neural-life-core", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--authority", str(paths["authority_state"]), "--out", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-neural", "--strict"],
            ["check-neural-life-core", "--state", str(paths["neural_state"]), "--reports", str(paths["reports"]), "--strict"],
            ["build-state-store", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-state", "--strict"],
            ["check-state-store", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
            ["build-life-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--out", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-membrane", "--strict"],
            ["check-life-membrane", "--membrane", str(paths["membrane_state"]), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
            ["build-language-relationship", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-language", "--strict"],
            ["check-language-relationship", "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--reports", str(paths["reports"]), "--strict"],
            ["check-birth-readiness", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--direction", str(paths["direction_state"]), "--neural-core", str(paths["neural_state"]), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--out", str(paths["life_targets_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-birth", "--strict"],
            ["run-validation-membrane", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--membrane", str(paths["membrane_state"]), "--life-targets", str(paths["life_targets_state"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-validation", "--strict"],
            ["check-validation-membrane", "--state", str(paths["state_root"]), "--validation", str(paths["validation_state"]), "--observation", str(paths["observation_state"]), "--reports", str(paths["reports"]), "--strict"],
            ["build-schema-runner", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-schema", "--strict"],
            ["check-schema-runner", "--state", str(paths["schema_runner_state"]), "--reports", str(paths["reports"]), "--strict"],
            ["run-schema-smoke", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-smoke", "--strict"],
            ["build-life-support", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--validation", str(paths["reports"] / "validation_membrane_report.json"), "--out", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-support", "--strict"],
            ["check-life-support", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--strict"],
            ["run-cycle", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-cycle", "--shadow-only", "--strict"],
            ["check-v0-contracts", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-contracts", "--strict"],
            ["first-activation-preflight", "--docs", str(self.docs_dir), "--doc-index", str(paths["doc_out"] / "doc_carrier_index.json"), "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-preflight", "--strict"],
            ["run-replay-shadow", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-replay", "--strict"],
            ["write-growth-archive", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-archive", "--strict"],
            ["emit-report", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-emit", "--strict"],
            ["explain-stage", "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "package-stage", "--strict"],
        ]

        for command in commands:
            completed = subprocess.run(
                [str(life_v0_bin), *command],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

    def _venv_bins(self, venv_dir: Path) -> tuple[Path, Path]:
        if sys.platform == "win32":
            bin_dir = venv_dir / "Scripts"
            python_bin = bin_dir / "python.exe"
        else:
            bin_dir = venv_dir / "bin"
            python_bin = bin_dir / "python"
        return python_bin, bin_dir

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
