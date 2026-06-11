import json
import os
import subprocess
import sys
import tempfile
import time
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

    def test_editable_install_digital_command_runs_background_resident(self):
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
            self._install_editable(python_bin)

            digital_bin = bin_dir / "digital"
            stop_command = [
                str(digital_bin),
                "life",
                "--state",
                str(runtime_paths["state_root"]),
                "--reports",
                str(runtime_paths["reports"]),
                "--receipts",
                str(runtime_paths["receipts"]),
                "--stop",
                "--stop-timeout-seconds",
                "30",
            ]
            started_pid = 0
            try:
                started = subprocess.run(
                    [
                        str(digital_bin),
                        "life",
                        "--state",
                        str(runtime_paths["state_root"]),
                        "--reports",
                        str(runtime_paths["reports"]),
                        "--receipts",
                        str(runtime_paths["receipts"]),
                        "--run-id",
                        "packaged-background-resident",
                        "--strict",
                        "--background",
                        "--resident-sleep-seconds",
                        "0.2",
                    ],
                    cwd=self.repo_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(started.returncode, 0, started.stderr)
                start_state = json.loads(started.stdout)
                started_pid = int(start_state["pid"])
                self.assertTrue(self._pid_alive(started_pid))
                self.assertEqual(start_state["status"], "background_starting")

                active_state = self._wait_for_resident_status(
                    runtime_paths["terminal_state"],
                    expected_status="background_active",
                    timeout_seconds=30,
                )
                self.assertEqual(active_state["pid"], started_pid)
                self.assertEqual(
                    active_state["residency_posture"],
                    "sleeping_waiting_for_relation_turn",
                )

                autonomous_state = self._wait_for_autonomous_activity(
                    runtime_paths["terminal_state"],
                    timeout_seconds=30,
                    min_count=5,
                )
                self.assertEqual(
                    autonomous_state["current_cycle"],
                    [
                        "sleep",
                        "memory_recall",
                        "self_thinking",
                        "growth_rehearsal",
                        "learning_consolidation",
                    ],
                )

                status = subprocess.run(
                    [
                        str(digital_bin),
                        "life",
                        "--state",
                        str(runtime_paths["state_root"]),
                        "--reports",
                        str(runtime_paths["reports"]),
                        "--receipts",
                        str(runtime_paths["receipts"]),
                        "--status",
                    ],
                    cwd=self.repo_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(status.returncode, 0, status.stderr)
                status_state = json.loads(status.stdout)
                self.assertEqual(status_state["status"], "background_active")
                self.assertEqual(status_state["pid"], started_pid)
                self.assertIn("resident_relation_queue_state", status_state)
                self.assertIn("resident_autonomous_activity_state", status_state)
                self.assertIn("resident_waiting_heartbeat", status_state)
                self.assertIn("resident_governance_state", status_state)
                self.assertIn("resident_idle_strategy_state", status_state)
                self.assertIn("resident_terminal_life_loop_state", status_state)
                self.assertEqual(
                    status_state["resident_relation_queue_state"]["status"],
                    "waiting_for_relation_turn",
                )
                self.assertGreaterEqual(
                    status_state["resident_autonomous_activity_state"]["activity_count"],
                    5,
                )
                self.assertGreaterEqual(
                    status_state["resident_waiting_heartbeat_counter"],
                    1,
                )
                self.assertEqual(
                    status_state["resident_next_required_action"],
                    "await_next_external_relation_turn",
                )
                self.assertEqual(
                    status_state["resident_governance_phase"],
                    "waiting_heartbeat_active",
                )
                self.assertEqual(
                    status_state["resident_terminal_current_mode"],
                    status_state["resident_waiting_mode"],
                )
                self.assertIn(
                    status_state["resident_idle_strategy_state_ref"],
                    status_state["resident_waiting_heartbeat"].values(),
                )

                said = subprocess.run(
                    [
                        str(digital_bin),
                        "life",
                        "--state",
                        str(runtime_paths["state_root"]),
                        "--reports",
                        str(runtime_paths["reports"]),
                        "--receipts",
                        str(runtime_paths["receipts"]),
                        "--say",
                        "你还在安装后的后台吗？",
                        "--say-timeout-seconds",
                        "30",
                    ],
                    cwd=self.repo_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(said.returncode, 0, said.stderr)
                self.assertIn("你还在安装后的后台吗？", said.stdout)
                self.assertIn("后台自主活动", said.stdout)

                bundle = self._read_json(
                    runtime_paths["reports"] / "dialogue_writeback_bundle.json"
                )
                self.assertTrue(
                    bundle["resident_background_lineage_autonomous_activity_refs"]
                )

                stopped = subprocess.run(
                    stop_command,
                    cwd=self.repo_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(stopped.returncode, 0, stopped.stderr)
                stopped_state = json.loads(stopped.stdout)
                self.assertEqual(stopped_state["status"], "stopped")
                self.assertFalse(stopped_state["pid_alive"])
            finally:
                if started_pid and self._pid_alive(started_pid):
                    subprocess.run(
                        stop_command,
                        cwd=self.repo_root,
                        text=True,
                        capture_output=True,
                        check=False,
                    )

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

    def _install_editable(self, python_bin: Path) -> None:
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

    def _wait_for_resident_status(
        self,
        terminal_dir: Path,
        *,
        expected_status: str,
        timeout_seconds: float,
    ) -> dict:
        state_path = terminal_dir / "resident_lifecycle_state.json"
        deadline = time.monotonic() + timeout_seconds
        last_state: dict = {}
        while time.monotonic() < deadline:
            if state_path.exists():
                last_state = self._read_json(state_path)
                pid = int(last_state.get("pid", 0) or 0)
                if (
                    last_state.get("status") == expected_status
                    and pid
                    and self._pid_alive(pid)
                ):
                    return last_state
            time.sleep(0.1)
        self.fail(f"resident did not reach {expected_status}: {last_state}")

    def _wait_for_autonomous_activity(
        self,
        terminal_dir: Path,
        *,
        timeout_seconds: float,
        min_count: int,
    ) -> dict:
        state_path = terminal_dir / "resident_autonomous_activity_state.json"
        deadline = time.monotonic() + timeout_seconds
        last_state: dict = {}
        while time.monotonic() < deadline:
            if state_path.exists():
                last_state = self._read_json(state_path)
                if int(last_state.get("activity_count", 0) or 0) >= min_count:
                    return last_state
            time.sleep(0.1)
        self.fail(f"autonomous activity did not reach {min_count}: {last_state}")

    def _pid_alive(self, pid: int) -> bool:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True


if __name__ == "__main__":
    unittest.main()
