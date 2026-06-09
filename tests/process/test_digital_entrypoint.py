import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.helpers.life_v0_bootstrap import activation_bootstrap_commands, build_runtime_paths


class DigitalEntrypointTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_repo_local_digital_life_entrypoint_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            bootstrap = [
                ["python", "-m", "life_v0", *command]
                for command in activation_bootstrap_commands(
                    docs_dir=self.docs_dir,
                    paths=paths,
                    run_id_prefix="entry",
                )
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
            paths = build_runtime_paths(Path(tmp))

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

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
