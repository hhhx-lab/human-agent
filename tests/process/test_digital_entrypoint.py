import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

from tests.helpers.life_v0_bootstrap import (
    DigitalLifeRuntimeEnvIsolationMixin,
    activation_bootstrap_commands,
    build_runtime_paths,
)


class DigitalEntrypointTests(DigitalLifeRuntimeEnvIsolationMixin, unittest.TestCase):
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

    def test_repo_local_digital_life_entrypoint_reads_env_runtime_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            env_path = Path(tmp) / "digital-life.env"
            env_path.write_text(
                "\n".join(
                    [
                        "DIGITAL_LIFE_RUNTIME_PROFILE=quiet-lab",
                        "DIGITAL_LIFE_MODEL_PROVIDER=test-provider",
                        "DIGITAL_LIFE_MODEL_NAME=test-model",
                        "DIGITAL_LIFE_MODEL_BASE_URL=https://example.invalid/api",
                        "DIGITAL_LIFE_MODEL_API_KEY=test-secret-token",
                        "DIGITAL_LIFE_MODEL_TEMPERATURE=0.25",
                        "DIGITAL_LIFE_MODEL_MAX_OUTPUT_TOKENS=256",
                        "DIGITAL_LIFE_MODEL_TIMEOUT_SECONDS=12.5",
                        "DIGITAL_LIFE_RESPONSE_LANGUAGE=zh-Hans",
                        "DIGITAL_LIFE_DIALOGUE_STYLE=relationship",
                        "DIGITAL_LIFE_STRICT_DEFAULT=true",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["DIGITAL_LIFE_ENV_FILE"] = str(env_path)
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
                    "entry-env-config",
                    "--strict",
                ],
                cwd=self.repo_root,
                env=env,
                text=True,
                input="你好\n/exit\n",
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            config_state = self._read_json(paths["terminal_state"] / "runtime_config_state.json")
            config_report = self._read_json(paths["reports"] / "digital_life_runtime_config_report.json")
            model_expression_state = self._read_json(
                paths["language_state"] / "model_expression_state.json"
            )
            model_expression_report = self._read_json(
                paths["reports"] / "digital_life_model_expression_report.json"
            )
            process_report = self._read_json(paths["reports"] / "digital_life_process_report.json")

        self.assertEqual(config_state["runtime_profile"], "quiet-lab")
        self.assertEqual(config_state["model_provider"], "test-provider")
        self.assertEqual(config_state["model_name"], "test-model")
        self.assertEqual(config_state["model_base_url"], "https://example.invalid/api")
        self.assertTrue(config_state["model_api_key_present"])
        self.assertEqual(config_state["model_api_key_redacted"], "<redacted>")
        self.assertEqual(config_state["model_temperature"], 0.25)
        self.assertEqual(config_state["model_max_output_tokens"], 256)
        self.assertEqual(config_state["model_timeout_seconds"], 12.5)
        self.assertEqual(config_state["response_language"], "zh-Hans")
        self.assertEqual(config_state["dialogue_style"], "relationship")
        self.assertTrue(config_state["strict_default"])
        self.assertTrue(config_state["env_source"].startswith("env_file:"))
        self.assertEqual(config_report["runtime_config_ref"], "runtime/state/terminal/runtime_config_state.json")
        self.assertEqual(
            process_report["runtime_config_state_ref"],
            "runtime/state/terminal/runtime_config_state.json",
        )
        self.assertEqual(
            process_report["runtime_config_report_ref"],
            "runtime/reports/latest/digital_life_runtime_config_report.json",
        )
        self.assertEqual(
            model_expression_state["model_expression_status"],
            "model_expression_skipped",
        )
        self.assertEqual(
            model_expression_state["fallback_reason"],
            "provider_not_enabled_for_model_expression:test-provider",
        )
        self.assertEqual(
            model_expression_state["post_expression_gate_status"],
            "skipped",
        )
        self.assertEqual(
            model_expression_report["runtime_config_state_ref"],
            "runtime/state/terminal/runtime_config_state.json",
        )
        self.assertEqual(
            model_expression_state["model_expression_context_summary"][
                "language_percept_ref"
            ],
            "runtime/state/language/language_percept_frame.json",
        )
        self.assertEqual(
            model_expression_state["model_expression_context_summary"][
                "semantic_map_ref"
            ],
            "runtime/state/language/semantic_map_frame.json",
        )
        self.assertEqual(
            model_expression_state["model_expression_context_summary"][
                "inner_speech_ref"
            ],
            "runtime/state/language/inner_speech_frame.json",
        )
        self.assertEqual(
            model_expression_state["model_expression_context_summary"][
                "expression_monitor_ref"
            ],
            "runtime/state/language/expression_monitor_state.json",
        )
        self.assertEqual(
            process_report["model_expression_state_ref"],
            "runtime/state/language/model_expression_state.json",
        )
        self.assertEqual(
            process_report["model_expression_report_ref"],
            "runtime/reports/latest/digital_life_model_expression_report.json",
        )
        self.assertEqual(process_report["post_expression_gate_status"], "skipped")
        self.assertEqual(
            process_report["last_life_turn"]["model_expression_status"],
            "model_expression_skipped",
        )
        self.assertEqual(
            process_report["last_life_turn"]["post_expression_gate_status"],
            "skipped",
        )

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

    def test_repo_local_digital_life_background_resident_stays_alive_until_stop(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            start_command = [
                str(self.repo_root / "digital"),
                "life",
                "--state",
                str(paths["state_root"]),
                "--reports",
                str(paths["reports"]),
                "--receipts",
                str(paths["receipts"]),
                "--run-id",
                "entry-background-resident",
                "--strict",
                "--background",
                "--resident-sleep-seconds",
                "0.2",
            ]
            stop_command = [
                str(self.repo_root / "digital"),
                "life",
                "--state",
                str(paths["state_root"]),
                "--reports",
                str(paths["reports"]),
                "--receipts",
                str(paths["receipts"]),
                "--stop",
                "--json",
                "--stop-timeout-seconds",
                "30",
            ]
            started_pid = 0
            try:
                paths["terminal_state"].mkdir(parents=True, exist_ok=True)
                (
                    paths["terminal_state"] / "resident_lifecycle_command.json"
                ).write_text(
                    json.dumps(
                        {
                            "schema_version": "resident_lifecycle_command_v0",
                            "command": "stop",
                            "status": "requested",
                            "requested_at": "2026-06-11T00:00:00+00:00",
                        },
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

                started = subprocess.run(
                    start_command,
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
                cleared_command = self._read_json(
                    paths["terminal_state"] / "resident_lifecycle_command.json"
                )
                self.assertEqual(cleared_command["status"], "cleared_for_start")
                self.assertEqual(cleared_command["previous_command"], "stop")

                active_state = self._wait_for_resident_status(
                    paths["terminal_state"],
                    expected_status="background_active",
                    timeout_seconds=30,
                )
                self.assertEqual(active_state["run_id"], "entry-background-resident")
                self.assertEqual(active_state["pid"], started_pid)
                self.assertTrue(active_state["pid_alive"])
                self.assertEqual(
                    active_state["residency_posture"],
                    "sleeping_waiting_for_relation_turn",
                )
                autonomous_state = self._wait_for_autonomous_activity(
                    paths["terminal_state"],
                    timeout_seconds=30,
                    min_count=5,
                )
                self.assertGreaterEqual(autonomous_state["activity_count"], 5)
                self.assertGreaterEqual(
                    autonomous_state["cycle_completion_count"],
                    1,
                )
                self.assertTrue(autonomous_state["cycle_coverage_complete"])
                self.assertEqual(autonomous_state["missing_activity_kinds"], [])
                self.assertEqual(
                    autonomous_state["covered_activity_kinds"],
                    [
                        "sleep",
                        "memory_recall",
                        "self_thinking",
                        "growth_rehearsal",
                        "learning_consolidation",
                    ],
                )
                for activity_kind in [
                    "sleep",
                    "memory_recall",
                    "self_thinking",
                    "growth_rehearsal",
                    "learning_consolidation",
                ]:
                    self.assertGreaterEqual(
                        autonomous_state["activity_kind_counts"][activity_kind],
                        1,
                    )
                self.assertEqual(
                    autonomous_state["activity_state_refs"]["sleep"],
                    "runtime/state/terminal/resident_sleep_cycle_state.json",
                )
                self.assertTrue(
                    (
                        paths["terminal_state"] / "resident_sleep_cycle_state.json"
                    ).exists()
                )
                self.assertTrue(
                    (
                        paths["state_root"] / "memory" / "resident_memory_recall_state.json"
                    ).exists()
                )
                self.assertTrue(
                    (
                        paths["state_root"] / "self" / "resident_self_thinking_state.json"
                    ).exists()
                )
                self.assertTrue(
                    (
                        paths["state_root"] / "growth" / "resident_growth_rehearsal_state.json"
                    ).exists()
                )
                learning_state = self._read_json(
                    paths["state_root"]
                    / "growth"
                    / "resident_learning_consolidation_state.json"
                )
                self.assertEqual(
                    learning_state["consolidation_mode"],
                    "long_term_change_source_integration",
                )

                status = subprocess.run(
                    [
                        str(self.repo_root / "digital"),
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
                status_state = json.loads(status.stdout)
                self.assertEqual(status_state["pid"], started_pid)
                self.assertTrue(status_state["pid_alive"])
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
                self.assertEqual(
                    status_state[
                        "resident_autonomous_activity_cycle_phase_index"
                    ],
                    status_state["resident_autonomous_activity_state"][
                        "cycle_phase_index"
                    ],
                )
                self.assertEqual(
                    status_state[
                        "resident_autonomous_activity_cycle_phase_count"
                    ],
                    5,
                )
                self.assertGreaterEqual(
                    status_state[
                        "resident_autonomous_activity_cycle_completion_count"
                    ],
                    1,
                )
                self.assertTrue(
                    status_state[
                        "resident_autonomous_activity_cycle_coverage_complete"
                    ]
                )
                self.assertEqual(
                    status_state["resident_autonomous_activity_missing_kinds"],
                    [],
                )
                self.assertEqual(
                    status_state["resident_autonomous_activity_covered_kinds"],
                    [
                        "sleep",
                        "memory_recall",
                        "self_thinking",
                        "growth_rehearsal",
                        "learning_consolidation",
                    ],
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
                self.assertIn("resident_long_term_residency_status", status_state)
                self.assertIn("resident_process_lease", status_state)
                self.assertIn(
                    "resident_process_lease_history_profile",
                    status_state,
                )
                self.assertEqual(
                    status_state["resident_process_lease_ref"],
                    "runtime/state/terminal/resident_process_lease.json",
                )
                self.assertEqual(
                    status_state["resident_process_lease_history_ref"],
                    "runtime/state/terminal/resident_process_lease_history.jsonl",
                )
                self.assertEqual(
                    status_state["resident_process_lease_history_profile_ref"],
                    "runtime/state/terminal/resident_process_lease_history_profile.json",
                )
                self.assertEqual(
                    status_state["resident_process_id"],
                    "resident-process-entry-background-resident",
                )
                self.assertEqual(status_state["resident_process_lease_state"], "active")
                self.assertEqual(
                    status_state["resident_process_identity_continuity_state"],
                    "active_residency",
                )
                self.assertGreaterEqual(
                    status_state["resident_process_lease_history_event_count"],
                    1,
                )
                self.assertIn(
                    "runtime/state/terminal/resident_process_lease.json",
                    status_state["resident_long_term_residency_status"][
                        "evidence_refs"
                    ],
                )
                self.assertIn(
                    "runtime/state/terminal/resident_process_lease_history_profile.json",
                    status_state["resident_long_term_residency_status"][
                        "evidence_refs"
                    ],
                )

                said = subprocess.run(
                    [
                        str(self.repo_root / "digital"),
                        "life",
                        "--state",
                        str(paths["state_root"]),
                        "--reports",
                        str(paths["reports"]),
                        "--receipts",
                        str(paths["receipts"]),
                        "--say",
                        "你还在后台吗？",
                        "--say-timeout-seconds",
                        "30",
                    ],
                    cwd=self.repo_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(said.returncode, 0, said.stderr)
                self.assertIn("你还在后台吗？", said.stdout)

                inbox_events = self._read_jsonl(
                    paths["terminal_state"] / "resident_relation_inbox.jsonl"
                )
                outbox_events = self._read_jsonl(
                    paths["terminal_state"] / "resident_relation_outbox.jsonl"
                )
                queue_state = self._read_json(
                    paths["terminal_state"] / "resident_relation_queue_state.json"
                )
                dialogue_events = self._read_jsonl(
                    paths["language_state"] / "dialogue_turn_log.jsonl"
                )
                self.assertEqual(inbox_events[-1]["utterance"], "你还在后台吗？")
                self.assertEqual(outbox_events[-1]["sequence"], inbox_events[-1]["sequence"])
                self.assertEqual(outbox_events[-1]["status"], "completed")
                self.assertIn("你还在后台吗？", outbox_events[-1]["response_text"])
                self.assertEqual(queue_state["status"], "waiting_for_relation_turn")
                self.assertEqual(queue_state["last_completed_sequence"], 1)
                self.assertEqual(
                    dialogue_events[-2]["event_role"],
                    "external_relation_turn",
                )
                self.assertEqual(
                    dialogue_events[-1]["event_role"],
                    "digital_life_turn",
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
                self.assertEqual(
                    stopped_state["resident_process_lease_state"],
                    "closed",
                )
                self.assertEqual(
                    stopped_state["resident_persistent_process_status"],
                    "closed",
                )
                self.assertEqual(
                    stopped_state["resident_persistent_process_state_ref"],
                    "runtime/state/terminal/persistent_process_state.json",
                )
                self.assertEqual(
                    stopped_state["resident_persistent_process_report_ref"],
                    "runtime/reports/latest/digital_life_persistent_process_report.json",
                )

                final_state = self._read_json(
                    paths["terminal_state"] / "resident_lifecycle_state.json"
                )
                process_report = self._read_json(
                    paths["reports"] / "digital_life_process_report.json"
                )
                self.assertEqual(final_state["status"], "stopped")
                self.assertEqual(final_state["run_id"], "entry-background-resident")
                self.assertEqual(final_state["last_relation_turn_sequence"], 1)
                self.assertGreaterEqual(final_state["autonomous_activity_count"], 5)
                self.assertIn(
                    "learning_consolidation",
                    final_state["resident_autonomous_activity_state_refs"],
                )
                self.assertEqual(process_report["status"], "closed")
                self.assertEqual(process_report["completed_dialogue_turns"], 1)
                self.assertEqual(process_report["exit_reason"], "explicit_exit")
            finally:
                if started_pid and self._pid_alive(started_pid):
                    subprocess.run(
                        stop_command,
                        cwd=self.repo_root,
                        text=True,
                        capture_output=True,
                        check=False,
                    )

    def test_repo_local_digital_life_attach_detaches_without_stopping_resident(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            stop_command = [
                str(self.repo_root / "digital"),
                "life",
                "--state",
                str(paths["state_root"]),
                "--reports",
                str(paths["reports"]),
                "--receipts",
                str(paths["receipts"]),
                "--stop",
                "--json",
                "--stop-timeout-seconds",
                "30",
            ]
            started_pid = 0
            try:
                attached = subprocess.run(
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
                        "entry-attach-resident",
                        "--strict",
                        "--attach",
                        "--resident-sleep-seconds",
                        "0.2",
                        "--say-timeout-seconds",
                        "30",
                    ],
                    cwd=self.repo_root,
                    text=True,
                    input="你能继续存在吗？\n/exit\n",
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(attached.returncode, 0, attached.stderr)
                self.assertIn("你能继续存在吗？", attached.stdout)

                active_state = self._wait_for_resident_status(
                    paths["terminal_state"],
                    expected_status="background_active",
                    timeout_seconds=30,
                )
                started_pid = int(active_state["pid"])
                self.assertTrue(self._pid_alive(started_pid))
                self.assertEqual(active_state["run_id"], "entry-attach-resident")
                self.assertEqual(active_state["last_relation_turn_sequence"], 1)

                queue_state = self._read_json(
                    paths["terminal_state"] / "resident_relation_queue_state.json"
                )
                self.assertEqual(queue_state["status"], "waiting_for_relation_turn")
                self.assertEqual(queue_state["last_completed_sequence"], 1)

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

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _read_jsonl(self, path: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

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
                last_state["pid_alive"] = self._pid_alive(pid)
                if last_state.get("status") == expected_status:
                    return last_state
            time.sleep(0.1)
        self.fail(f"resident status did not reach {expected_status}: {last_state}")

    def _wait_for_autonomous_activity(
        self,
        terminal_dir: Path,
        *,
        timeout_seconds: float,
        min_count: int = 1,
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
        self.fail(f"resident autonomous activity did not start: {last_state}")

    def _pid_alive(self, pid: int) -> bool:
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True


if __name__ == "__main__":
    unittest.main()
