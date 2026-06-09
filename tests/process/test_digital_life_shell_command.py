import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers.life_v0_bootstrap import activation_bootstrap_commands, build_runtime_paths


class DigitalLifeShellCommandTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_cli_digital_life_shell_returns_zero_and_writes_shell_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            commands = activation_bootstrap_commands(
                docs_dir=self.docs_dir,
                paths=paths,
                run_id_prefix="shell-cli",
            ) + [
                ["digital life", "--state", str(paths["state_root"]), "--reports", str(paths["reports"]), "--receipts", str(paths["receipts"]), "--run-id", "shell-cli", "--strict"],
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

            packet = self._read_json(paths["reports"] / "digital_life_shell_packet.json")
            report = self._read_json(paths["reports"] / "digital_life_shell_report.json")
            digest = self._read_json(paths["reports"] / "digital_life_shell_digest.json")
            receipt = self._read_json(paths["receipts"] / "digital_life_shell_shell-cli.json")

        self.assertEqual(packet["schema_version"], "digital_life_shell_packet_v0")
        self.assertEqual(packet["status"], "closed")
        self.assertEqual(packet["shell_mode"], "terminal_life_loop_restored")
        self.assertEqual(packet["next_required_action"], "await_next_external_relation_turn")

        self.assertEqual(report["schema_version"], "digital_life_shell_report_v0")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["engineering_slice_ref"], "DIGITAL_LIFE_SHELL_COMMAND")
        self.assertEqual(report["current_shell_mode"], "terminal_life_loop_restored")

        self.assertEqual(digest["schema_version"], "digital_life_shell_digest_v0")
        self.assertEqual(digest["status"], "closed")
        self.assertEqual(digest["terminal_state_ref"], "runtime/state/terminal/terminal_life_loop_state.json")

        self.assertEqual(receipt["schema_version"], "digital_life_shell_receipt_v0")
        self.assertEqual(receipt["command"], "digital life")

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
