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
            self.assertTrue((paths["terminal_state"] / "resident_process_lease.json").exists())
            self.assertTrue((paths["terminal_state"] / "resident_process_lease_history.jsonl").exists())

            lease = self._read_json(paths["terminal_state"] / "resident_process_lease.json")
            lease_history = [
                json.loads(line)
                for line in (paths["terminal_state"] / "resident_process_lease_history.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line.strip()
            ]
            process_report = self._read_json(paths["reports"] / "digital_life_process_report.json")
            self.assertEqual(lease["schema_version"], "resident_process_lease_v0")
            self.assertEqual(lease["run_id"], "entry-bootstrap-shell")
            self.assertEqual(lease["resident_process_id"], "resident-process-entry-bootstrap-shell")
            self.assertEqual(lease["lease_state"], "closed")
            self.assertEqual(lease["completed_dialogue_turns"], 1)
            self.assertEqual(lease["exit_reason"], "explicit_exit")
            self.assertEqual(
                lease["process_report_ref"],
                "runtime/reports/latest/digital_life_process_report.json",
            )
            self.assertEqual(
                lease["resident_process_lease_history_ref"],
                "runtime/state/terminal/resident_process_lease_history.jsonl",
            )
            self.assertEqual(lease_history[-1]["event_kind"], "lease_closed")
            self.assertEqual(lease_history[-1]["resident_process_id"], "resident-process-entry-bootstrap-shell")
            self.assertEqual(process_report["status"], "closed")
            self.assertEqual(process_report["completed_dialogue_turns"], 1)
            self.assertEqual(
                process_report["resident_process_lease_ref"],
                "runtime/state/terminal/resident_process_lease.json",
            )
            self.assertEqual(
                process_report["resident_process_lease_history_ref"],
                "runtime/state/terminal/resident_process_lease_history.jsonl",
            )

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
