import json
import subprocess
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from tests.helpers.life_v0_bootstrap import activation_bootstrap_commands, build_runtime_paths


class DelayedInputStream:
    def __init__(self, idle_polls_before_lines: int, lines: list[str]) -> None:
        self._idle_polls_before_lines = idle_polls_before_lines
        self._lines = list(lines)

    def poll_line(self, timeout_seconds: float) -> str | None:
        if self._idle_polls_before_lines > 0:
            self._idle_polls_before_lines -= 1
            return None
        if self._lines:
            return self._lines.pop(0)
        return ""


class PersistentDigitalLifeProcessTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_repo_local_digital_life_process_keeps_dialogue_alive_and_writes_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

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
                    "persistent-shell",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                input="你好\n你还记得我们吗？\n/exit\n",
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("当前生命回合已恢复", completed.stdout)
            self.assertIn("生命回合输出", completed.stdout)

            dialogue_lines = [
                json.loads(line)
                for line in (paths["language_state"] / "dialogue_turn_log.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertGreaterEqual(len(dialogue_lines), 5)

            last_external = dialogue_lines[-2]
            last_life_response = dialogue_lines[-1]
            self.assertEqual(last_external["event_role"], "external_relation_turn")
            self.assertEqual(last_external["utterance"], "你还记得我们吗？")
            self.assertEqual(last_life_response["event_role"], "digital_life_turn")
            self.assertIn("朋友", last_life_response["utterance"])
            self.assertIn("离线重放线索", last_life_response["utterance"])
            self.assertIn("梦境整合窗口", last_life_response["utterance"])
            self.assertIn("成长补丁候选", last_life_response["utterance"])

            narrative_trace = self._read_json(paths["language_state"] / "self_narrative_language_trace.json")
            self.assertGreaterEqual(len(narrative_trace["narrative_turn_refs"]), 5)
            self.assertEqual(
                narrative_trace["last_external_turn"]["utterance"],
                "你还记得我们吗？",
            )

            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")
            subject = relationship_graph["subjects"][0]
            self.assertEqual(subject["relation_role"], "friend")
            self.assertEqual(subject["relationship_stage"], "active_dialogue")
            self.assertEqual(subject["last_external_turn_utterance"], "你还记得我们吗？")

            commitment_index = self._read_json(paths["language_state"] / "commitment_repair_language_index.json")
            self.assertIn("dialogue-turn-live-0005", commitment_index["recent_dialogue_turn_refs"][-1])

            loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            self.assertEqual(loop_state["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(loop_state["last_turn_mode"], "resumed_external_dialogue_loop")
            self.assertEqual(loop_state["last_external_turn_utterance"], "你还记得我们吗？")

    def test_repo_local_digital_life_process_writes_waiting_heartbeat_before_first_turn(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

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
                    "persistent-heartbeat",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                input="/exit\n",
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)

            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(safe_terminal_loop["last_heartbeat_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(safe_terminal_loop["heartbeat_counter"], 1)
            self.assertEqual(
                safe_terminal_loop["last_heartbeat_packet_ref"],
                "runtime/reports/latest/digital_life_waiting_heartbeat.json",
            )

            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            self.assertEqual(terminal_loop_state["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(terminal_loop_state["heartbeat_counter"], 1)
            self.assertEqual(terminal_loop_state["next_required_action"], "await_next_external_relation_turn")

            heartbeat_packet = self._read_json(paths["reports"] / "digital_life_waiting_heartbeat.json")
            idle_continuity = self._read_json(paths["terminal_state"] / "idle_continuity_frame.json")
            idle_strategy = self._read_json(paths["terminal_state"] / "idle_strategy_state.json")
            self.assertEqual(heartbeat_packet["schema_version"], "digital_life_waiting_heartbeat_v0")
            self.assertEqual(heartbeat_packet["run_id"], "persistent-heartbeat")
            self.assertEqual(heartbeat_packet["heartbeat_counter"], 1)
            self.assertEqual(heartbeat_packet["waiting_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(
                heartbeat_packet["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(idle_strategy["schema_version"], "idle_strategy_state_v0")
            self.assertEqual(idle_strategy["run_id"], "persistent-heartbeat")
            self.assertIn("strategy_id", idle_strategy)
            self.assertEqual(idle_strategy["idle_probe_mode"], "stdin_poll_with_background_continuity_refresh")
            self.assertEqual(idle_strategy["next_idle_action"], "refresh_waiting_heartbeat_or_accept_external_turn")

            process_report = self._read_json(paths["reports"] / "digital_life_process_report.json")
            self.assertEqual(process_report["completed_dialogue_turns"], 0)
            self.assertEqual(process_report["heartbeat_counter"], 1)
            self.assertEqual(
                process_report["last_heartbeat_packet_ref"],
                "runtime/reports/latest/digital_life_waiting_heartbeat.json",
            )
            self.assertEqual(process_report["exit_reason"], "explicit_exit")
            self.assertEqual(
                process_report["life_context_frame_ref"],
                "runtime/state/terminal/life_context_frame.json",
            )
            self.assertEqual(
                process_report["relation_turn_frame_ref"],
                "runtime/state/terminal/relation_turn_frame.json",
            )
            self.assertEqual(
                process_report["expression_plan_ref"],
                "runtime/state/language/expression_plan.json",
            )
            self.assertEqual(
                process_report["dialogue_writeback_bundle_ref"],
                "runtime/reports/latest/dialogue_writeback_bundle.json",
            )
            self.assertEqual(
                process_report["replay_cue_bundle_ref"],
                "runtime/state/replay/replay_cue_bundle.json",
            )
            self.assertEqual(
                process_report["offline_consolidation_frame_ref"],
                "runtime/state/dream/offline_consolidation_frame.json",
            )
            self.assertEqual(
                process_report["growth_patch_candidate_queue_ref"],
                "runtime/state/growth/growth_patch_candidate_queue.json",
            )
            self.assertEqual(
                process_report["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(
                process_report["persistent_process_report_ref"],
                "runtime/reports/latest/digital_life_persistent_process_report.json",
            )
            self.assertEqual(
                idle_continuity["replay_cue_bundle_ref"],
                "runtime/state/replay/replay_cue_bundle.json",
            )
            self.assertEqual(
                idle_continuity["offline_consolidation_frame_ref"],
                "runtime/state/dream/offline_consolidation_frame.json",
            )
            self.assertEqual(
                idle_continuity["growth_patch_candidate_queue_ref"],
                "runtime/state/growth/growth_patch_candidate_queue.json",
            )
            self.assertTrue(idle_continuity["growth_patch_candidate_ids"])
            self.assertGreater(idle_continuity["replay_residue_ref_count"], 0)
            self.assertGreater(idle_continuity["dream_window_ref_count"], 0)
            self.assertGreater(idle_continuity["growth_patch_candidate_count"], 0)
            self.assertIn(
                "runtime/state/replay/replay_cue_bundle.json",
                idle_continuity["replay_seed_refs"],
            )

    def test_digital_life_process_refreshes_waiting_heartbeat_while_idle(self):
        from life_v0.process_supervisor import run_digital_life_process

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

            input_stream = DelayedInputStream(
                idle_polls_before_lines=2,
                lines=["/exit\n"],
            )
            output_stream = StringIO()

            result = run_digital_life_process(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="persistent-idle-heartbeat",
                strict=True,
                input_stream=input_stream,
                output_stream=output_stream,
            )

            self.assertEqual(result.exit_code, 0)

            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            heartbeat_packet = self._read_json(paths["reports"] / "digital_life_waiting_heartbeat.json")
            process_report = self._read_json(paths["reports"] / "digital_life_process_report.json")
            process_digest = self._read_json(paths["reports"] / "digital_life_process_digest.json")
            idle_continuity = self._read_json(paths["terminal_state"] / "idle_continuity_frame.json")
            idle_strategy = self._read_json(paths["terminal_state"] / "idle_strategy_state.json")
            narrative_trace = self._read_json(paths["language_state"] / "self_narrative_language_trace.json")
            commitment_index = self._read_json(paths["language_state"] / "commitment_repair_language_index.json")
            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")

            self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(safe_terminal_loop["heartbeat_counter"], 3)
            self.assertEqual(
                safe_terminal_loop["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(terminal_loop_state["heartbeat_counter"], 3)
            self.assertEqual(
                terminal_loop_state["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(heartbeat_packet["heartbeat_counter"], 3)
            self.assertEqual(
                heartbeat_packet["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(process_report["heartbeat_counter"], 3)
            self.assertEqual(process_digest["heartbeat_counter"], 3)
            self.assertEqual(process_report["completed_dialogue_turns"], 0)
            self.assertEqual(process_report["exit_reason"], "explicit_exit")
            self.assertEqual(
                process_report["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(
                process_report["persistent_process_report_ref"],
                "runtime/reports/latest/digital_life_persistent_process_report.json",
            )
            self.assertEqual(idle_continuity["schema_version"], "idle_continuity_frame_v0")
            self.assertEqual(idle_continuity["status"], "closed")
            self.assertEqual(idle_continuity["heartbeat_counter"], 3)
            self.assertEqual(idle_continuity["event_kind"], "waiting_heartbeat_refresh")
            self.assertEqual(
                idle_continuity["heartbeat_ref"],
                "runtime/reports/latest/digital_life_waiting_heartbeat.json",
            )
            self.assertIn("idle_continuity_id", idle_continuity)
            self.assertEqual(
                idle_continuity["waiting_state"],
                "restored_waiting_for_external_turn",
            )
            self.assertTrue(idle_continuity["self_narrative_idle_refs"])
            self.assertTrue(idle_continuity["commitment_idle_refs"])
            self.assertTrue(idle_continuity["relationship_idle_refs"])
            self.assertTrue(idle_continuity["replay_seed_refs"])
            self.assertGreater(idle_continuity["replay_residue_ref_count"], 0)
            self.assertGreater(idle_continuity["dream_window_ref_count"], 0)
            self.assertGreater(idle_continuity["growth_patch_candidate_count"], 0)
            self.assertEqual(idle_strategy["schema_version"], "idle_strategy_state_v0")
            self.assertEqual(idle_strategy["heartbeat_interval_ms"], 50)
            self.assertEqual(idle_strategy["idle_probe_mode"], "stdin_poll_with_background_continuity_refresh")
            self.assertEqual(idle_strategy["offline_pressure_level"], "elevated")
            self.assertEqual(idle_strategy["relaunch_caution_level"], "baseline")
            self.assertEqual(idle_strategy["next_idle_action"], "refresh_waiting_heartbeat_or_accept_external_turn")
            self.assertEqual(
                idle_strategy["idle_continuity_ref"],
                "runtime/state/terminal/idle_continuity_frame.json",
            )
            self.assertEqual(narrative_trace["idle_continuity_counter"], 3)
            self.assertEqual(len(narrative_trace["idle_continuity_refs"]), 3)
            self.assertEqual(
                narrative_trace["last_idle_continuity"]["heartbeat_ref"],
                "runtime/reports/latest/digital_life_waiting_heartbeat.json",
            )
            self.assertEqual(narrative_trace["last_idle_continuity"]["heartbeat_counter"], 3)

            self.assertEqual(commitment_index["idle_presence_counter"], 3)
            self.assertEqual(len(commitment_index["idle_presence_refs"]), 3)
            self.assertEqual(
                commitment_index["last_idle_presence"]["heartbeat_ref"],
                "runtime/reports/latest/digital_life_waiting_heartbeat.json",
            )
            self.assertEqual(commitment_index["last_idle_presence"]["heartbeat_counter"], 3)

            self.assertEqual(relationship_graph["idle_presence_counter"], 3)
            self.assertEqual(len(relationship_graph["idle_presence_refs"]), 3)
            subject = relationship_graph["subjects"][0]
            self.assertEqual(subject["idle_presence_counter"], 3)
            self.assertEqual(subject["last_idle_continuity_event_kind"], "waiting_heartbeat_refresh")
            self.assertEqual(
                subject["last_idle_continuity_report_ref"],
                "runtime/reports/latest/digital_life_waiting_heartbeat.json",
            )

    def test_turn_io_poll_input_line_uses_custom_poll_hook_before_fileno(self):
        from life_v0.process_supervisor.turn_io import poll_input_line

        delayed = DelayedInputStream(idle_polls_before_lines=1, lines=["你好\n"])
        first = poll_input_line(delayed, timeout_seconds=0.01)
        second = poll_input_line(delayed, timeout_seconds=0.01)

        self.assertIsNone(first)
        self.assertEqual(second, "你好\n")

    def test_incident_recovery_organ_writes_reports_and_restores_waiting_state(self):
        from life_v0.process_supervisor.incident_recovery import recover_from_dialogue_turn_exception

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            reports_dir = runtime_root / "reports" / "latest"
            terminal_dir = runtime_root / "state" / "terminal"
            language_dir = runtime_root / "state" / "language"
            relationship_dir = runtime_root / "state" / "relationship"
            reports_dir.mkdir(parents=True, exist_ok=True)
            terminal_dir.mkdir(parents=True, exist_ok=True)
            language_dir.mkdir(parents=True, exist_ok=True)
            relationship_dir.mkdir(parents=True, exist_ok=True)

            safe_terminal_loop = {
                "current_mode": "resumed_external_dialogue_loop",
            }
            terminal_life_loop_state = {
                "current_mode": "resumed_external_dialogue_loop",
                "last_turn_status": "open",
                "next_required_action": "continue_interrupted_relation_turn",
            }
            self_narrative_trace: dict[str, object] = {}
            commitment_index: dict[str, object] = {}
            relationship_graph = {
                "subjects": [
                    {
                        "relation_role": "friend",
                    }
                ]
            }

            result = recover_from_dialogue_turn_exception(
                run_id="incident-organ",
                incident_count=1,
                external_utterance="这次回合会触发异常",
                exc=RuntimeError("simulated-dialogue-processing-failure"),
                reports_dir=reports_dir,
                terminal_dir=terminal_dir,
                language_dir=language_dir,
                relationship_dir=relationship_dir,
                safe_terminal_loop=safe_terminal_loop,
                terminal_life_loop_state=terminal_life_loop_state,
                self_narrative_trace=self_narrative_trace,
                commitment_index=commitment_index,
                relationship_graph=relationship_graph,
                write_json=self._write_json,
                now_iso=lambda: "2026-06-09T00:00:00+00:00",
            )

            self.assertEqual(
                result.incident_report_ref,
                "runtime/reports/latest/digital_life_process_incident_report.json",
            )
            self.assertEqual(
                result.recovery_report_ref,
                "runtime/reports/latest/digital_life_process_recovery_report.json",
            )
            self.assertEqual(result.incident_report["incident_kind"], "dialogue_turn_processing_failure")
            self.assertEqual(result.recovery_report["result"], "recovered_to_waiting_state")

            incident_report = self._read_json(reports_dir / "digital_life_process_incident_report.json")
            recovery_report = self._read_json(reports_dir / "digital_life_process_recovery_report.json")
            persisted_safe_terminal = self._read_json(terminal_dir / "safe_terminal_loop_state.json")
            persisted_terminal_loop = self._read_json(terminal_dir / "terminal_life_loop_state.json")
            persisted_narrative_trace = self._read_json(language_dir / "self_narrative_language_trace.json")
            persisted_commitment_index = self._read_json(language_dir / "commitment_repair_language_index.json")
            persisted_relationship_graph = self._read_json(relationship_dir / "relationship_subject_graph.json")

            self.assertEqual(incident_report["error_type"], "RuntimeError")
            self.assertEqual(recovery_report["release_decision"], "resume_waiting_for_next_external_turn")
            self.assertEqual(persisted_safe_terminal["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(persisted_terminal_loop["last_turn_status"], "incident_recovered")
            self.assertIn(
                "runtime/reports/latest/digital_life_process_recovery_report.json",
                persisted_narrative_trace["recovery_event_refs"],
            )
            self.assertEqual(
                persisted_commitment_index["last_recovery_event_kind"],
                "dialogue_incident_recovery",
            )
            self.assertEqual(
                persisted_relationship_graph["subjects"][0]["last_continuity_event_kind"],
                "dialogue_incident_recovery",
            )

    def test_process_report_organ_writes_report_digest_and_receipt(self):
        from life_v0.process_supervisor.process_report import write_process_report_bundle

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            reports_dir = runtime_root / "reports" / "latest"
            receipts_dir = runtime_root / "receipts"
            state_dir = runtime_root / "state"
            terminal_dir = state_dir / "terminal"
            language_dir = state_dir / "language"
            relationship_dir = state_dir / "relationship"
            reports_dir.mkdir(parents=True, exist_ok=True)
            receipts_dir.mkdir(parents=True, exist_ok=True)
            terminal_dir.mkdir(parents=True, exist_ok=True)
            language_dir.mkdir(parents=True, exist_ok=True)
            relationship_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "replay").mkdir(parents=True, exist_ok=True)
            (state_dir / "dream").mkdir(parents=True, exist_ok=True)
            (state_dir / "growth").mkdir(parents=True, exist_ok=True)

            self._write_json(reports_dir / "digital_life_shell_report.json", {"status": "closed"})
            self._write_json(reports_dir / "digital_life_waiting_heartbeat.json", {"heartbeat_counter": 3})
            self._write_json(terminal_dir / "session_envelope.json", {"schema_version": "session_envelope_v0"})
            self._write_json(terminal_dir / "safe_terminal_loop_state.json", {"current_mode": "restored_waiting_for_external_turn"})
            self._write_json(terminal_dir / "terminal_life_loop_state.json", {"current_mode": "restored_waiting_for_external_turn"})
            self._write_json(language_dir / "self_narrative_language_trace.json", {"schema_version": "self_narrative_language_trace_v0"})
            self._write_json(language_dir / "commitment_repair_language_index.json", {"schema_version": "commitment_repair_language_index_v0"})
            self._write_json(relationship_dir / "relationship_subject_graph.json", {"subjects": []})
            self._write_json(state_dir / "replay" / "replay_cue_bundle.json", {"schema_version": "replay_cue_bundle_v0"})
            self._write_json(
                state_dir / "dream" / "offline_consolidation_frame.json",
                {"schema_version": "offline_consolidation_frame_v0"},
            )
            self._write_json(
                state_dir / "growth" / "growth_patch_candidate_queue.json",
                {
                    "schema_version": "growth_patch_candidate_queue_v0",
                    "candidates": [{"growth_patch_candidate_id": "growth-patch-candidate-test-0001"}],
                },
            )
            (language_dir / "dialogue_turn_log.jsonl").write_text('{"turn_id":"dialogue-turn-live-0001"}\n', encoding="utf-8")

            result = write_process_report_bundle(
                run_id="process-report-organ",
                generated_at="2026-06-09T00:00:00+00:00",
                state_dir=state_dir,
                reports_dir=reports_dir,
                receipts_dir=receipts_dir,
                source_doc_refs=["docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                completed_turns=2,
                incident_count=1,
                relaunch_recovery_count=1,
                heartbeat_counter=3,
                exit_reason="explicit_exit",
                last_incident_report_ref="runtime/reports/latest/digital_life_process_incident_report.json",
                last_recovery_report_ref="runtime/reports/latest/digital_life_process_recovery_report.json",
                last_relaunch_recovery_report_ref="runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
                last_external_turn={"utterance": "你还记得我们吗？"},
                last_life_turn={"utterance": "我当然记得。"},
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                persistent_process_report_ref="runtime/reports/latest/digital_life_persistent_process_report.json",
                life_context_frame_ref="runtime/state/terminal/life_context_frame.json",
                relation_turn_frame_ref="runtime/state/terminal/relation_turn_frame.json",
                expression_plan_ref="runtime/state/language/expression_plan.json",
                dialogue_writeback_bundle_ref="runtime/reports/latest/dialogue_writeback_bundle.json",
                replay_cue_bundle_ref="runtime/state/replay/replay_cue_bundle.json",
                offline_consolidation_frame_ref="runtime/state/dream/offline_consolidation_frame.json",
                growth_patch_candidate_queue_ref="runtime/state/growth/growth_patch_candidate_queue.json",
                write_json=self._write_json,
            )

            report = self._read_json(reports_dir / "digital_life_process_report.json")
            digest = self._read_json(reports_dir / "digital_life_process_digest.json")
            receipt = self._read_json(receipts_dir / "digital_life_process_process-report-organ.json")

            self.assertEqual(result.report["run_id"], "process-report-organ")
            self.assertEqual(report["completed_dialogue_turns"], 2)
            self.assertEqual(report["incident_count"], 1)
            self.assertEqual(report["relaunch_recovery_count"], 1)
            self.assertEqual(report["heartbeat_counter"], 3)
            self.assertEqual(report["exit_reason"], "explicit_exit")
            self.assertEqual(report["last_life_turn"]["utterance"], "我当然记得。")
            self.assertEqual(
                report["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(
                report["replay_cue_bundle_ref"],
                "runtime/state/replay/replay_cue_bundle.json",
            )
            self.assertEqual(
                report["offline_consolidation_frame_ref"],
                "runtime/state/dream/offline_consolidation_frame.json",
            )
            self.assertEqual(
                report["growth_patch_candidate_queue_ref"],
                "runtime/state/growth/growth_patch_candidate_queue.json",
            )
            self.assertEqual(digest["last_external_turn_utterance"], "你还记得我们吗？")
            self.assertEqual(
                digest["offline_growth_cycle_refs"],
                [
                    "runtime/state/replay/replay_cue_bundle.json",
                    "runtime/state/dream/offline_consolidation_frame.json",
                    "runtime/state/growth/growth_patch_candidate_queue.json",
                ],
            )
            self.assertEqual(receipt["receipt_id"], "digital_life_process_process-report-organ")
            self.assertEqual(receipt["stage_effect"], "persistent_dialogue_process_closed")
            self.assertIn(
                "runtime/state/terminal/idle_strategy_state.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/replay/replay_cue_bundle.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                str(state_dir / "replay" / "replay_cue_bundle.json"),
                receipt["input_hashes"],
            )
            self.assertIn(
                str(reports_dir / "digital_life_process_report.json"),
                receipt["output_hashes"],
            )

    def test_persistent_process_organ_writes_state_and_report(self):
        from life_v0.process_supervisor.persistent_process import write_persistent_process_artifacts

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state_dir = runtime_root / "state"
            terminal_dir = state_dir / "terminal"
            reports_dir = runtime_root / "reports" / "latest"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)

            self._write_json(
                terminal_dir / "safe_terminal_loop_state.json",
                {
                    "current_mode": "restored_waiting_for_external_turn",
                    "heartbeat_counter": 3,
                },
            )
            self._write_json(
                terminal_dir / "terminal_life_loop_state.json",
                {
                    "current_mode": "restored_waiting_for_external_turn",
                    "last_turn_status": "closed",
                    "next_required_action": "await_next_external_relation_turn",
                },
            )

            result = write_persistent_process_artifacts(
                run_id="persistent-process-organ",
                generated_at="2026-06-09T00:00:00+00:00",
                state_dir=state_dir,
                reports_dir=reports_dir,
                heartbeat_counter=3,
                completed_turns=1,
                incident_count=1,
                relaunch_recovery_count=1,
                waiting_mode="restored_waiting_for_external_turn",
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                last_heartbeat_packet_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
                last_dialogue_packet_ref="runtime/reports/latest/resumed_external_dialogue_packet.json",
                source_doc_refs=["docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                write_json=self._write_json,
            )

            state = self._read_json(terminal_dir / "persistent_process_state.json")
            report = self._read_json(reports_dir / "digital_life_persistent_process_report.json")

            self.assertEqual(result.state["schema_version"], "persistent_process_state_v0")
            self.assertEqual(result.report["schema_version"], "digital_life_persistent_process_report_v0")
            self.assertEqual(state["run_id"], "persistent-process-organ")
            self.assertEqual(report["run_id"], "persistent-process-organ")
            self.assertEqual(state["heartbeat_counter"], 3)
            self.assertEqual(report["heartbeat_counter"], 3)
            self.assertEqual(state["governance_mode"], "foreground_terminal_residency")
            self.assertEqual(report["governance_mode"], "foreground_terminal_residency")
            self.assertEqual(state["waiting_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(report["waiting_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(
                state["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(
                report["persistent_process_state_ref"],
                "runtime/state/terminal/persistent_process_state.json",
            )
            self.assertEqual(
                report["safe_terminal_loop_state_ref"],
                "runtime/state/terminal/safe_terminal_loop_state.json",
            )
            self.assertEqual(
                report["terminal_life_loop_state_ref"],
                "runtime/state/terminal/terminal_life_loop_state.json",
            )

    def test_dialogue_events_organ_builds_external_and_life_turn_events(self):
        from life_v0.process_supervisor.dialogue_events import (
            build_external_turn_event,
            build_life_turn_event,
        )

        shared_term_registry = {
            "shared_terms": [
                {
                    "term_id": "shared-term-v0-0001",
                    "surface": "旧约定",
                }
            ]
        }
        commitment_index = {
            "commitment_refs": [
                "commitment-ref-01",
                "commitment-ref-02",
            ]
        }

        external_turn = build_external_turn_event(
            turn_id="dialogue-turn-live-0001",
            generated_at="2026-06-09T00:00:00+00:00",
            utterance="你还记得吗？",
            shared_term_registry=shared_term_registry,
            commitment_index=commitment_index,
        )
        life_turn = build_life_turn_event(
            turn_id="dialogue-turn-live-0002",
            generated_at="2026-06-09T00:00:01+00:00",
            utterance="我记得。",
            shared_term_registry=shared_term_registry,
            commitment_index=commitment_index,
        )

        self.assertEqual(external_turn["event_role"], "external_relation_turn")
        self.assertEqual(life_turn["event_role"], "digital_life_turn")
        self.assertEqual(external_turn["relation_role"], "friend")
        self.assertEqual(life_turn["relation_role"], "friend")
        self.assertEqual(
            external_turn["shared_term_refs"],
            ["runtime/state/language/shared_term_registry.json#shared-term-v0-0001"],
        )
        self.assertEqual(life_turn["commitment_refs"], ["commitment-ref-01", "commitment-ref-02"])
        self.assertEqual(
            life_turn["expression_monitor_ref"],
            "runtime/state/language/expression_monitor_state.json",
        )
        self.assertEqual(
            life_turn["narrative_trace_ref"],
            "runtime/state/language/self_narrative_language_trace.json",
        )

    def test_response_surface_organ_carries_relation_shared_terms_and_commitment_pressure(self):
        from life_v0.process_supervisor.response_surface import compose_life_response

        response = compose_life_response(
            external_utterance="你还记得我们吗？",
            relationship_graph={
                "subjects": [
                    {
                        "relation_role": "friend",
                    }
                ]
            },
            shared_term_registry={
                "shared_terms": [
                    {
                        "term_id": "shared-term-v0-0001",
                        "surface": "旧约定",
                    }
                ]
            },
            commitment_index={
                "commitment_refs": [
                    "commitment-ref-01",
                    "commitment-ref-02",
                    "commitment-ref-03",
                ]
            },
            relation_turn_frame={
                "relation_subject_ref": "rel-v0-0001",
            },
            expression_plan={
                "semantic_goal": "repair_commitment_shared_language",
            },
            life_context_frame={
                "self_narrative_refs": [
                    "runtime/state/language/self_narrative_language_trace.json#line-1",
                    "runtime/state/language/self_narrative_language_trace.json#line-2",
                ]
            },
            replay_cue_bundle={
                "anti_forgetting_targets": [
                    "runtime/state/replay/replay-cue-001",
                    "runtime/state/replay/replay-cue-002",
                ],
            },
            offline_consolidation_frame={
                "dream_window_refs": [
                    "runtime/state/dream/dream-window-001",
                    "runtime/state/dream/dream-window-002",
                ],
            },
            growth_patch_candidate_queue={
                "candidates": [
                    {"growth_patch_candidate_id": "growth-patch-candidate-001"},
                    {"growth_patch_candidate_id": "growth-patch-candidate-002"},
                ]
            },
        )

        self.assertIn("朋友", response)
        self.assertIn("旧约定", response)
        self.assertIn("3条未闭合承诺", response)
        self.assertIn("repair_commitment_shared_language", response)
        self.assertIn("2条自我叙事连续锚点", response)
        self.assertIn("离线表达压力", response)
        self.assertIn("2条离线重放线索", response)
        self.assertIn("2个梦境整合窗口", response)
        self.assertIn("2个成长补丁候选", response)
        self.assertIn("你还记得我们吗？", response)

    def test_digital_life_process_recovers_from_dialogue_turn_exception_and_returns_to_waiting_state(self):
        from life_v0.process_supervisor import run_digital_life_process

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

            input_stream = StringIO("这次回合会触发一次异常\n/exit\n")
            output_stream = StringIO()

            with patch(
                "life_v0.process_supervisor._compose_life_response",
                side_effect=RuntimeError("simulated-dialogue-processing-failure"),
            ):
                result = run_digital_life_process(
                    state_dir=paths["state_root"],
                    reports_dir=paths["reports"],
                    receipts_dir=paths["receipts"],
                    run_id="persistent-incident",
                    strict=True,
                    input_stream=input_stream,
                    output_stream=output_stream,
                )

            self.assertEqual(result.exit_code, 0)
            self.assertIn("当前生命回合已恢复", output_stream.getvalue())
            self.assertIn("异常恢复", output_stream.getvalue())

            incident_report = self._read_json(paths["reports"] / "digital_life_process_incident_report.json")
            recovery_report = self._read_json(paths["reports"] / "digital_life_process_recovery_report.json")
            process_report = self._read_json(paths["reports"] / "digital_life_process_report.json")
            process_digest = self._read_json(paths["reports"] / "digital_life_process_digest.json")
            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            narrative_trace = self._read_json(paths["language_state"] / "self_narrative_language_trace.json")
            commitment_index = self._read_json(paths["language_state"] / "commitment_repair_language_index.json")
            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")

            self.assertEqual(incident_report["report_kind"], "incident_report")
            self.assertEqual(incident_report["severity"], "high")
            self.assertEqual(incident_report["incident_kind"], "dialogue_turn_processing_failure")
            self.assertEqual(
                incident_report["containment"]["stage_decision"],
                "restored_waiting_for_external_turn",
            )
            self.assertEqual(recovery_report["report_kind"], "incident_recovery_report")
            self.assertEqual(recovery_report["result"], "recovered_to_waiting_state")

            self.assertEqual(process_report["incident_count"], 1)
            self.assertEqual(
                process_report["last_incident_report_ref"],
                "runtime/reports/latest/digital_life_process_incident_report.json",
            )
            self.assertEqual(
                process_report["last_recovery_report_ref"],
                "runtime/reports/latest/digital_life_process_recovery_report.json",
            )
            self.assertEqual(process_digest["incident_count"], 1)

            self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(safe_terminal_loop["last_incident_status"], "recovered_to_waiting_state")
            self.assertEqual(
                safe_terminal_loop["last_incident_report_ref"],
                "runtime/reports/latest/digital_life_process_incident_report.json",
            )
            self.assertEqual(terminal_loop_state["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(terminal_loop_state["last_turn_status"], "incident_recovered")
            self.assertEqual(terminal_loop_state["next_required_action"], "await_next_external_relation_turn")

            self.assertIn(
                "runtime/reports/latest/digital_life_process_recovery_report.json",
                narrative_trace["recovery_event_refs"],
            )
            self.assertEqual(
                narrative_trace["last_recovery_event"]["event_kind"],
                "dialogue_incident_recovery",
            )

            self.assertIn(
                "runtime/reports/latest/digital_life_process_recovery_report.json",
                commitment_index["recovery_history_refs"],
            )
            self.assertEqual(
                commitment_index["last_recovery_event_kind"],
                "dialogue_incident_recovery",
            )

            subject = relationship_graph["subjects"][0]
            self.assertEqual(subject["last_continuity_event_kind"], "dialogue_incident_recovery")
            self.assertEqual(
                subject["last_continuity_report_ref"],
                "runtime/reports/latest/digital_life_process_recovery_report.json",
            )

    def test_digital_life_process_detects_interrupted_previous_run_and_normalizes_on_relaunch(self):
        from life_v0.process_supervisor import run_digital_life_process

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

            seed_result = run_digital_life_process(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="persistent-relaunch-seed",
                strict=True,
                input_stream=StringIO("/exit\n"),
                output_stream=StringIO(),
            )
            self.assertEqual(seed_result.exit_code, 0)

            stale_safe_terminal = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            stale_terminal_loop = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            stale_safe_terminal["current_mode"] = "resumed_external_dialogue_loop"
            stale_safe_terminal["last_completed_turn_mode"] = "resumed_external_dialogue_loop"
            stale_terminal_loop["current_mode"] = "resumed_external_dialogue_loop"
            stale_terminal_loop["last_turn_status"] = "open"
            stale_terminal_loop["last_turn_mode"] = "resumed_external_dialogue_loop"
            stale_terminal_loop["next_required_action"] = "continue_interrupted_relation_turn"
            self._write_json(paths["terminal_state"] / "safe_terminal_loop_state.json", stale_safe_terminal)
            self._write_json(paths["terminal_state"] / "terminal_life_loop_state.json", stale_terminal_loop)

            result = run_digital_life_process(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="persistent-relaunch",
                strict=True,
                input_stream=StringIO("/exit\n"),
                output_stream=StringIO(),
            )

            self.assertEqual(result.exit_code, 0)

            relaunch_recovery_report = self._read_json(paths["reports"] / "digital_life_process_relaunch_recovery_report.json")
            process_report = self._read_json(paths["reports"] / "digital_life_process_report.json")
            process_digest = self._read_json(paths["reports"] / "digital_life_process_digest.json")
            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            narrative_trace = self._read_json(paths["language_state"] / "self_narrative_language_trace.json")
            commitment_index = self._read_json(paths["language_state"] / "commitment_repair_language_index.json")
            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")

            self.assertEqual(relaunch_recovery_report["report_kind"], "relaunch_recovery_report")
            self.assertEqual(
                relaunch_recovery_report["relaunch_recovery_kind"],
                "interrupted_previous_process_state",
            )
            self.assertEqual(
                relaunch_recovery_report["previous_safe_terminal_mode"],
                "resumed_external_dialogue_loop",
            )
            self.assertEqual(
                relaunch_recovery_report["previous_terminal_loop_mode"],
                "resumed_external_dialogue_loop",
            )
            self.assertEqual(
                relaunch_recovery_report["normalized_mode"],
                "restored_waiting_for_external_turn",
            )

            self.assertEqual(process_report["relaunch_recovery_count"], 1)
            self.assertEqual(
                process_report["last_relaunch_recovery_report_ref"],
                "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
            )
            self.assertEqual(process_digest["relaunch_recovery_count"], 1)

            self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(
                safe_terminal_loop["last_relaunch_recovery_report_ref"],
                "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
            )
            self.assertEqual(terminal_loop_state["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(
                terminal_loop_state["last_relaunch_recovery_report_ref"],
                "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
            )

            self.assertIn(
                "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
                narrative_trace["recovery_event_refs"],
            )
            self.assertEqual(
                narrative_trace["last_recovery_event"]["event_kind"],
                "relaunch_recovery_normalization",
            )

            self.assertIn(
                "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
                commitment_index["recovery_history_refs"],
            )
            self.assertEqual(
                commitment_index["last_recovery_event_kind"],
                "relaunch_recovery_normalization",
            )

            subject = relationship_graph["subjects"][0]
            self.assertEqual(subject["last_continuity_event_kind"], "relaunch_recovery_normalization")
            self.assertEqual(
                subject["last_continuity_report_ref"],
                "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
            )

    def _bootstrap(self, paths: dict[str, Path]) -> None:
        commands = [
            ["python", "-m", "life_v0", *command]
            for command in activation_bootstrap_commands(
                docs_dir=self.docs_dir,
                paths=paths,
                run_id_prefix="persistent",
            )
        ]

        for command in commands:
            completed = subprocess.run(
                command,
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_json(self, path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
