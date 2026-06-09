import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers.life_v0_bootstrap import activation_bootstrap_commands, build_runtime_paths


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
            runtime_paths = build_runtime_paths(tmp_path)

            subprocess.run(
                [sys.executable, "-m", "venv", "--system-site-packages", str(venv_dir)],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=True,
            )

            python_bin, bin_dir = self._venv_bins(venv_dir)

            install = subprocess.run(
                [
                    str(python_bin),
                    "-m",
                    "pip",
                    "install",
                    "--no-build-isolation",
                    "-e",
                    str(self.repo_root),
                ],
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
            runtime_paths = build_runtime_paths(tmp_path)

            subprocess.run(
                [sys.executable, "-m", "venv", "--system-site-packages", str(venv_dir)],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=True,
            )

            python_bin, bin_dir = self._venv_bins(venv_dir)

            install = subprocess.run(
                [
                    str(python_bin),
                    "-m",
                    "pip",
                    "install",
                    "--no-build-isolation",
                    "-e",
                    str(self.repo_root),
                ],
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
        commands = activation_bootstrap_commands(
            docs_dir=self.docs_dir,
            paths=paths,
            run_id_prefix="package",
        )

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

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
