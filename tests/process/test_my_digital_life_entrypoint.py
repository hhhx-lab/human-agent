import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers.life_v0_bootstrap import (
    DigitalLifeRuntimeEnvIsolationMixin,
    build_runtime_paths,
)


class MyDigitalLifeEntrypointTests(
    DigitalLifeRuntimeEnvIsolationMixin,
    unittest.TestCase,
):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    def test_my_digital_life_requires_name_on_first_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0.my_entry",
                    "digital",
                    "life",
                    "--state",
                    str(paths["state_root"]),
                    "--reports",
                    str(paths["reports"]),
                    "--receipts",
                    str(paths["receipts"]),
                    "--status",
                    "--json",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 2)
        payload = json.loads(completed.stderr)
        self.assertEqual(payload["status"], "name_required")
        self.assertEqual(payload["required_command"], "my digital life --name <name>")

    def test_my_digital_life_binds_name_and_reuses_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            first_launch = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0.my_entry",
                    "digital",
                    "life",
                    "--state",
                    str(paths["state_root"]),
                    "--reports",
                    str(paths["reports"]),
                    "--receipts",
                    str(paths["receipts"]),
                    "--run-id",
                    "my-digital-life-shell",
                    "--strict",
                    "--name",
                    "星火",
                ],
                cwd=self.repo_root,
                text=True,
                input="你记住这个名字了吗？\n/exit\n",
                capture_output=True,
                check=False,
            )
            self.assertEqual(first_launch.returncode, 0, first_launch.stderr)
            self.assertIn("当前生命回合已恢复", first_launch.stdout)

            registry = self._read_json(
                paths["state_root"] / "identity" / "life_name_registry.json"
            )
            self.assertEqual(registry["schema_version"], "digital_life_name_registry_v0")
            self.assertEqual(registry["canonical_name"], "星火")
            self.assertEqual(registry["name_lock_state"], "permanent_for_runtime")
            command_manifest = self._read_json(
                paths["state_root"] / "identity" / "life_name_command_manifest.json"
            )
            self.assertEqual(
                command_manifest["schema_version"],
                "life_name_direct_command_manifest_v0",
            )
            self.assertEqual(command_manifest["status"], "active")
            self.assertTrue(command_manifest["direct_command_enabled"])
            self.assertEqual(command_manifest["command_name"], "星火")
            direct_command_path = Path(command_manifest["command_path"])
            self.assertTrue(direct_command_path.exists())

            status = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0.my_entry",
                    "digital",
                    "life",
                    "--state",
                    str(paths["state_root"]),
                    "--reports",
                    str(paths["reports"]),
                    "--receipts",
                    str(paths["receipts"]),
                    "--status",
                    "--json",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(status.returncode, 0, status.stderr)
            status_payload = json.loads(status.stdout)
            self.assertEqual(status_payload["life_name"], "星火")
            self.assertEqual(
                status_payload["resident_long_term_residency_status"]["life_name"],
                "星火",
            )
            direct_status = subprocess.run(
                [
                    str(direct_command_path),
                    "--status",
                    "--json",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(direct_status.returncode, 0, direct_status.stderr)
            direct_status_payload = json.loads(direct_status.stdout)
            self.assertEqual(direct_status_payload["life_name"], "星火")

            mismatch = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0.my_entry",
                    "digital",
                    "life",
                    "--state",
                    str(paths["state_root"]),
                    "--reports",
                    str(paths["reports"]),
                    "--receipts",
                    str(paths["receipts"]),
                    "--status",
                    "--json",
                    "--name",
                    "另一个名字",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(mismatch.returncode, 2)
            mismatch_payload = json.loads(mismatch.stderr)
            self.assertEqual(mismatch_payload["status"], "name_mismatch")
            self.assertEqual(mismatch_payload["canonical_name"], "星火")

    def test_repo_local_my_script_binds_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            repo_my = self.repo_root / "my"
            first_launch = subprocess.run(
                [
                    str(repo_my),
                    "digital",
                    "life",
                    "--state",
                    str(paths["state_root"]),
                    "--reports",
                    str(paths["reports"]),
                    "--receipts",
                    str(paths["receipts"]),
                    "--run-id",
                    "repo-local-my-shell",
                    "--strict",
                    "--name",
                    "星火",
                ],
                cwd=self.repo_root,
                text=True,
                input="你从名字开始醒来了吗？\n/exit\n",
                capture_output=True,
                check=False,
            )

            self.assertEqual(first_launch.returncode, 0, first_launch.stderr)
            self.assertIn("当前生命回合已恢复", first_launch.stdout)
            registry = self._read_json(
                paths["state_root"] / "identity" / "life_name_registry.json"
            )
            command_manifest = self._read_json(
                paths["state_root"] / "identity" / "life_name_command_manifest.json"
            )

        self.assertEqual(registry["canonical_name"], "星火")
        self.assertEqual(command_manifest["status"], "active")

    def test_my_digital_life_status_defaults_to_terminal_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            launch = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0.my_entry",
                    "digital",
                    "life",
                    "--state",
                    str(paths["state_root"]),
                    "--reports",
                    str(paths["reports"]),
                    "--receipts",
                    str(paths["receipts"]),
                    "--run-id",
                    "my-summary-shell",
                    "--strict",
                    "--name",
                    "星火",
                ],
                cwd=self.repo_root,
                text=True,
                input="/exit\n",
                capture_output=True,
                check=False,
            )
            self.assertEqual(launch.returncode, 0, launch.stderr)

            status = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "life_v0.my_entry",
                    "digital",
                    "life",
                    "--state",
                    str(paths["state_root"]),
                    "--reports",
                    str(paths["reports"]),
                    "--receipts",
                    str(paths["receipts"]),
                    "--status",
                ],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(status.returncode, 0, status.stderr)
            payload = json.loads(status.stdout)
            self.assertEqual(
                payload["schema_version"],
                "resident_lifecycle_terminal_summary_v0",
            )
            self.assertEqual(payload["life_name"], "星火")
            self.assertNotIn("resident_waiting_heartbeat", payload)
            self.assertIn("--json", payload["full_json_hint"])

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
