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


class TimeoutRecordingInputStream:
    def __init__(self, lines: list[str]) -> None:
        self._lines = list(lines)
        self.timeouts: list[float] = []

    def poll_line(self, timeout_seconds: float) -> str | None:
        self.timeouts.append(timeout_seconds)
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
            dialogue_writeback_bundle = self._read_json(paths["reports"] / "dialogue_writeback_bundle.json")
            self.assertIn("dialogue-turn-live-0005", commitment_index["recent_dialogue_turn_refs"][-1])
            self.assertEqual(
                dialogue_writeback_bundle["dialogue_event_refs"],
                [
                    f"runtime/state/language/dialogue_turn_log.jsonl#line-{len(dialogue_lines) - 1}",
                    f"runtime/state/language/dialogue_turn_log.jsonl#line-{len(dialogue_lines)}",
                ],
            )
            self.assertIn(
                "runtime/state/relationship/relationship_subject_graph.json",
                dialogue_writeback_bundle["relationship_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/memory/relationship_memory.json#repair_history_refs",
                dialogue_writeback_bundle["relationship_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/relationship/commitment_truth_state.json#repair_required_refs",
                dialogue_writeback_bundle["commitment_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/responsibility/responsibility_ledger.json#repair_obligations",
                dialogue_writeback_bundle["responsibility_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/life_state.json#memory_index.responsibility_memory_refs",
                dialogue_writeback_bundle["life_state_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/replay/replay_cue_bundle.json",
                dialogue_writeback_bundle["replay_cue_refs"],
            )

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
            self.assertEqual(heartbeat_packet["heartbeat_interval_ms"], 70)
            self.assertEqual(
                heartbeat_packet["idle_probe_mode"],
                "stdin_poll_with_background_continuity_refresh",
            )
            self.assertEqual(heartbeat_packet["offline_pressure_level"], "elevated")
            self.assertEqual(heartbeat_packet["relaunch_caution_level"], "baseline")
            self.assertEqual(heartbeat_packet["body_waiting_posture"], "guarded_attentive")
            self.assertEqual(
                heartbeat_packet["next_idle_action"],
                "refresh_waiting_heartbeat_with_repair_readiness_hold",
            )
            self.assertEqual(idle_strategy["schema_version"], "idle_strategy_state_v0")
            self.assertEqual(idle_strategy["run_id"], "persistent-heartbeat")
            self.assertIn("strategy_id", idle_strategy)
            self.assertEqual(idle_strategy["idle_probe_mode"], "stdin_poll_with_background_continuity_refresh")
            self.assertEqual(idle_strategy["next_idle_action"], "refresh_waiting_heartbeat_with_repair_readiness_hold")
            self.assertEqual(idle_strategy["body_waiting_posture"], "guarded_attentive")
            self.assertEqual(
                idle_strategy["body_rhythm_ref"],
                "runtime/state/body/body_rhythm_pulse.json",
            )
            self.assertEqual(
                idle_strategy["need_state_ref"],
                "runtime/state/body/need_state_vector.json",
            )
            self.assertIn("body_rhythm_present", idle_strategy["body_governance_flags"])
            self.assertIn("need_state_present", idle_strategy["body_governance_flags"])
            self.assertIn("fatigue_regulates_heartbeat", idle_strategy["body_governance_flags"])

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
                process_report["resident_governance_report_ref"],
                "runtime/reports/latest/digital_life_resident_governance_report.json",
            )
            self.assertEqual(
                process_report["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(process_report["body_waiting_posture"], "guarded_attentive")
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
            self.assertEqual(idle_strategy["heartbeat_interval_ms"], 70)
            self.assertEqual(idle_strategy["idle_probe_mode"], "stdin_poll_with_background_continuity_refresh")
            self.assertEqual(idle_strategy["offline_pressure_level"], "elevated")
            self.assertEqual(idle_strategy["relaunch_caution_level"], "baseline")
            self.assertEqual(idle_strategy["next_idle_action"], "refresh_waiting_heartbeat_with_repair_readiness_hold")
            self.assertEqual(idle_strategy["body_waiting_posture"], "guarded_attentive")
            self.assertEqual(heartbeat_packet["heartbeat_interval_ms"], 70)
            self.assertEqual(
                heartbeat_packet["idle_probe_mode"],
                "stdin_poll_with_background_continuity_refresh",
            )
            self.assertEqual(heartbeat_packet["offline_pressure_level"], "elevated")
            self.assertEqual(heartbeat_packet["relaunch_caution_level"], "baseline")
            self.assertEqual(heartbeat_packet["body_waiting_posture"], "guarded_attentive")
            self.assertEqual(
                heartbeat_packet["next_idle_action"],
                "refresh_waiting_heartbeat_with_repair_readiness_hold",
            )
            self.assertEqual(process_report["waiting_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(process_report["heartbeat_interval_ms"], 70)
            self.assertEqual(
                process_report["idle_probe_mode"],
                "stdin_poll_with_background_continuity_refresh",
            )
            self.assertEqual(process_report["offline_pressure_level"], "elevated")
            self.assertEqual(process_report["relaunch_caution_level"], "baseline")
            self.assertEqual(process_report["body_waiting_posture"], "guarded_attentive")
            self.assertEqual(
                process_report["next_idle_action"],
                "refresh_waiting_heartbeat_with_repair_readiness_hold",
            )
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

    def test_idle_refresh_loop_organ_refreshes_heartbeat_until_external_turn(self):
        from life_v0.process_supervisor.idle_refresh_loop import (
            wait_for_next_external_relation_turn,
        )
        from life_v0.shell_command import run_digital_life_shell_command

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)
            shell_result = run_digital_life_shell_command(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="idle-refresh-organ-restore",
                strict=True,
            )
            self.assertEqual(shell_result.exit_code, 0)

            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            narrative_trace = self._read_json(paths["language_state"] / "self_narrative_language_trace.json")
            commitment_index = self._read_json(paths["language_state"] / "commitment_repair_language_index.json")
            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")
            replay_cue_bundle = self._read_json(paths["state_root"] / "replay" / "replay_cue_bundle.json")
            offline_consolidation_frame = self._read_json(
                paths["state_root"] / "dream" / "offline_consolidation_frame.json"
            )
            growth_patch_candidate_queue = self._read_json(
                paths["state_root"] / "growth" / "growth_patch_candidate_queue.json"
            )
            growth_patch_candidate_ids = [
                candidate["growth_patch_candidate_id"]
                for candidate in growth_patch_candidate_queue["candidates"]
            ]

            result = wait_for_next_external_relation_turn(
                input_stream=DelayedInputStream(
                    idle_polls_before_lines=2,
                    lines=["你好\n"],
                ),
                run_id="idle-refresh-organ",
                generated_at="2026-06-09T00:00:00+00:00",
                terminal_dir=paths["terminal_state"],
                reports_dir=paths["reports"],
                language_dir=paths["language_state"],
                relationship_dir=paths["relationship_state"],
                safe_terminal_loop=safe_terminal_loop,
                terminal_life_loop_state=terminal_loop_state,
                self_narrative_trace=narrative_trace,
                commitment_index=commitment_index,
                relationship_graph=relationship_graph,
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                replay_cue_bundle=replay_cue_bundle,
                offline_consolidation_frame=offline_consolidation_frame,
                growth_patch_candidate_queue=growth_patch_candidate_queue,
                replay_cue_bundle_ref="runtime/state/replay/replay_cue_bundle.json",
                offline_consolidation_frame_ref="runtime/state/dream/offline_consolidation_frame.json",
                growth_patch_candidate_queue_ref="runtime/state/growth/growth_patch_candidate_queue.json",
                growth_patch_candidate_ids=growth_patch_candidate_ids,
                replay_residue_ref_count=len(replay_cue_bundle["turn_residue_refs"]),
                dream_window_ref_count=len(offline_consolidation_frame["dream_window_refs"]),
                growth_patch_candidate_count=len(growth_patch_candidate_queue["candidates"]),
                heartbeat_counter=0,
                now_iso=lambda: "2026-06-09T00:00:00+00:00",
                write_json=self._write_json,
            )

            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            heartbeat_packet = self._read_json(paths["reports"] / "digital_life_waiting_heartbeat.json")
            idle_continuity = self._read_json(paths["terminal_state"] / "idle_continuity_frame.json")

            self.assertEqual(result.heartbeat_counter, 2)
            self.assertEqual(result.external_utterance, "你好")
            self.assertIsNone(result.exit_reason)
            self.assertEqual(safe_terminal_loop["heartbeat_counter"], 2)
            self.assertEqual(terminal_loop_state["heartbeat_counter"], 2)
            self.assertEqual(heartbeat_packet["heartbeat_counter"], 2)
            self.assertEqual(idle_continuity["heartbeat_counter"], 2)
            self.assertEqual(idle_continuity["event_kind"], "waiting_heartbeat_refresh")

    def test_idle_refresh_loop_uses_idle_strategy_interval_as_poll_timeout(self):
        from life_v0.process_supervisor.idle_refresh_loop import (
            wait_for_next_external_relation_turn,
        )
        from life_v0.shell_command import run_digital_life_shell_command

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)
            shell_result = run_digital_life_shell_command(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="idle-timeout-restore",
                strict=True,
            )
            self.assertEqual(shell_result.exit_code, 0)

            self._write_json(
                paths["terminal_state"] / "idle_strategy_state.json",
                {
                    "schema_version": "idle_strategy_state_v0",
                    "run_id": "idle-timeout",
                    "heartbeat_interval_ms": 125,
                },
            )

            input_stream = TimeoutRecordingInputStream(lines=["/exit\n"])
            result = wait_for_next_external_relation_turn(
                input_stream=input_stream,
                run_id="idle-timeout",
                generated_at="2026-06-10T00:00:00+00:00",
                terminal_dir=paths["terminal_state"],
                reports_dir=paths["reports"],
                language_dir=paths["language_state"],
                relationship_dir=paths["relationship_state"],
                safe_terminal_loop=self._read_json(
                    paths["terminal_state"] / "safe_terminal_loop_state.json"
                ),
                terminal_life_loop_state=self._read_json(
                    paths["terminal_state"] / "terminal_life_loop_state.json"
                ),
                self_narrative_trace=self._read_json(
                    paths["language_state"] / "self_narrative_language_trace.json"
                ),
                commitment_index=self._read_json(
                    paths["language_state"] / "commitment_repair_language_index.json"
                ),
                relationship_graph=self._read_json(
                    paths["relationship_state"] / "relationship_subject_graph.json"
                ),
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                heartbeat_counter=0,
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
                write_json=self._write_json,
            )

            self.assertEqual(result.exit_reason, "explicit_exit")
            self.assertEqual(input_stream.timeouts, [0.125])

    def test_idle_strategy_uses_body_rhythm_and_need_state_to_regulate_waiting_governance(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-body-governance",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "active",
                "cognitive_bandwidth": "narrow_guarded",
                "sleep_pressure": "offline_ready",
            },
            replay_cue_bundle={"turn_residue_refs": ["runtime/state/replay/replay-cue-001"]},
            offline_consolidation_frame={"dream_window_refs": ["runtime/state/dream/dream-window-001"]},
            growth_patch_candidate_queue={"candidates": [{"growth_patch_candidate_id": "growth-patch-001"}]},
            replay_cue_bundle_ref="runtime/state/replay/replay_cue_bundle.json",
            offline_consolidation_frame_ref="runtime/state/dream/offline_consolidation_frame.json",
            growth_patch_candidate_queue_ref="runtime/state/growth/growth_patch_candidate_queue.json",
            growth_patch_candidate_ids=["growth-patch-001"],
            replay_residue_ref_count=1,
            dream_window_ref_count=1,
            growth_patch_candidate_count=1,
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 120)
        self.assertEqual(idle_strategy["offline_pressure_level"], "elevated")
        self.assertEqual(idle_strategy["body_waiting_posture"], "low_bandwidth_guarded")
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "downshift_probe_and_preserve_recovery_bandwidth",
        )
        self.assertEqual(
            idle_strategy["body_rhythm_ref"],
            "runtime/state/body/body_rhythm_pulse.json",
        )
        self.assertEqual(
            idle_strategy["need_state_ref"],
            "runtime/state/body/need_state_vector.json",
        )
        self.assertIn("body_rhythm_present", idle_strategy["body_governance_flags"])
        self.assertIn("need_state_present", idle_strategy["body_governance_flags"])
        self.assertIn("sleep_pressure_present", idle_strategy["body_governance_flags"])
        self.assertIn("cognitive_bandwidth_narrowed", idle_strategy["body_governance_flags"])

    def test_resident_supervision_organ_restores_shell_normalizes_relaunch_and_writes_initial_heartbeat(self):
        from life_v0.process_supervisor.resident_supervision import (
            bootstrap_resident_supervision,
        )
        from life_v0.shell_command import run_digital_life_shell_command

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

            seed_result = run_digital_life_shell_command(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="resident-supervision-seed",
                strict=True,
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

            result = bootstrap_resident_supervision(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="resident-supervision-organ",
                generated_at="2026-06-10T00:00:00+00:00",
                strict=True,
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                read_json=self._read_json,
                read_json_if_exists=lambda path: self._read_json(path) if path.exists() else {},
                write_json=self._write_json,
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
            )

            self.assertEqual(result.exit_code, 0)
            self.assertIsNotNone(result.context)
            assert result.context is not None

            context = result.context
            heartbeat_packet = self._read_json(paths["reports"] / "digital_life_waiting_heartbeat.json")
            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            narrative_trace = self._read_json(paths["language_state"] / "self_narrative_language_trace.json")
            commitment_index = self._read_json(paths["language_state"] / "commitment_repair_language_index.json")
            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")

            self.assertEqual(context.heartbeat_counter, 1)
            self.assertEqual(context.relaunch_recovery_count, 1)
            self.assertEqual(
                context.last_relaunch_recovery_report_ref,
                "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
            )
            self.assertEqual(
                context.replay_cue_bundle_ref,
                "runtime/state/replay/replay_cue_bundle.json",
            )
            self.assertEqual(
                context.offline_consolidation_frame_ref,
                "runtime/state/dream/offline_consolidation_frame.json",
            )
            self.assertEqual(
                context.growth_patch_candidate_queue_ref,
                "runtime/state/growth/growth_patch_candidate_queue.json",
            )
            self.assertTrue(context.growth_patch_candidate_ids)
            self.assertGreater(context.replay_residue_ref_count, 0)
            self.assertGreater(context.dream_window_ref_count, 0)
            self.assertGreater(context.growth_patch_candidate_count, 0)
            self.assertEqual(heartbeat_packet["heartbeat_counter"], 1)
            self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(terminal_loop_state["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(
                safe_terminal_loop["last_relaunch_recovery_report_ref"],
                "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
            )
            self.assertEqual(
                terminal_loop_state["last_relaunch_recovery_report_ref"],
                "runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
            )
            self.assertEqual(
                narrative_trace["last_recovery_event"]["event_kind"],
                "relaunch_recovery_normalization",
            )
            self.assertEqual(
                commitment_index["last_recovery_event_kind"],
                "relaunch_recovery_normalization",
            )
            self.assertEqual(
                relationship_graph["subjects"][0]["last_continuity_event_kind"],
                "relaunch_recovery_normalization",
            )

    def test_live_turn_cycle_organ_writes_response_and_returns_to_waiting_state(self):
        from life_v0.process_supervisor.live_turn_cycle import run_live_turn_cycle
        from life_v0.process_supervisor.resident_supervision import (
            bootstrap_resident_supervision,
        )

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

            supervision = bootstrap_resident_supervision(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="live-turn-cycle-organ",
                generated_at="2026-06-10T00:00:00+00:00",
                strict=True,
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                read_json=self._read_json,
                read_json_if_exists=lambda path: self._read_json(path) if path.exists() else {},
                write_json=self._write_json,
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
            )
            self.assertEqual(supervision.exit_code, 0)
            assert supervision.context is not None
            context = supervision.context

            result = run_live_turn_cycle(
                run_id="live-turn-cycle-organ",
                incident_count=0,
                turn_counter=1,
                external_utterance="你还记得我们吗？",
                terminal_dir=context.terminal_dir,
                language_dir=context.language_dir,
                relationship_dir=context.relationship_dir,
                reports_dir=paths["reports"],
                safe_terminal_loop=context.safe_terminal_loop,
                terminal_life_loop_state=context.terminal_life_loop_state,
                body_resource_budget=context.body_resource_budget,
                core_affect_vector=context.core_affect_vector,
                self_narrative_trace=context.self_narrative_trace,
                commitment_index=context.commitment_index,
                relationship_graph=context.relationship_graph,
                relationship_timeline=context.relationship_timeline,
                shared_term_registry=context.shared_term_registry,
                commitment_expression_plan=context.commitment_expression_plan,
                apology_repair_language_trace=context.apology_repair_language_trace,
                relation_turn_frame=context.relation_turn_frame,
                expression_plan=context.expression_plan,
                life_context_frame=context.life_context_frame,
                replay_cue_bundle=context.replay_cue_bundle,
                offline_consolidation_frame=context.offline_consolidation_frame,
                growth_patch_candidate_queue=context.growth_patch_candidate_queue,
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                replay_cue_bundle_ref=context.replay_cue_bundle_ref,
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
                write_json=self._write_json,
                append_jsonl=self._append_jsonl,
            )

            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            dialogue_writeback_bundle = self._read_json(paths["reports"] / "dialogue_writeback_bundle.json")

            self.assertEqual(result.turn_counter, 3)
            self.assertEqual(result.completed_turns_delta, 1)
            self.assertEqual(result.incident_count_delta, 0)
            self.assertEqual(result.cycle_status, "completed")
            self.assertIn("生命回合输出:", result.emitted_output)
            self.assertIsNotNone(result.last_external_turn)
            self.assertIsNotNone(result.last_life_turn)
            self.assertEqual(
                result.last_external_turn["event_role"],
                "external_relation_turn",
            )
            self.assertEqual(
                result.last_life_turn["event_role"],
                "digital_life_turn",
            )
            self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(terminal_loop_state["last_turn_mode"], "resumed_external_dialogue_loop")
            self.assertEqual(
                dialogue_writeback_bundle["dialogue_event_refs"],
                [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                ],
            )

    def test_live_turn_cycle_organ_recovers_from_response_exception(self):
        from life_v0.process_supervisor.live_turn_cycle import run_live_turn_cycle
        from life_v0.process_supervisor.resident_supervision import (
            bootstrap_resident_supervision,
        )

        def raise_compose_error(**_: object) -> str:
            raise RuntimeError("simulated-live-turn-cycle-failure")

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

            supervision = bootstrap_resident_supervision(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="live-turn-cycle-incident",
                generated_at="2026-06-10T00:00:00+00:00",
                strict=True,
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                read_json=self._read_json,
                read_json_if_exists=lambda path: self._read_json(path) if path.exists() else {},
                write_json=self._write_json,
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
            )
            self.assertEqual(supervision.exit_code, 0)
            assert supervision.context is not None
            context = supervision.context

            result = run_live_turn_cycle(
                run_id="live-turn-cycle-incident",
                incident_count=0,
                turn_counter=1,
                external_utterance="这次回合会触发一次异常",
                terminal_dir=context.terminal_dir,
                language_dir=context.language_dir,
                relationship_dir=context.relationship_dir,
                reports_dir=paths["reports"],
                safe_terminal_loop=context.safe_terminal_loop,
                terminal_life_loop_state=context.terminal_life_loop_state,
                body_resource_budget=context.body_resource_budget,
                core_affect_vector=context.core_affect_vector,
                self_narrative_trace=context.self_narrative_trace,
                commitment_index=context.commitment_index,
                relationship_graph=context.relationship_graph,
                relationship_timeline=context.relationship_timeline,
                shared_term_registry=context.shared_term_registry,
                commitment_expression_plan=context.commitment_expression_plan,
                apology_repair_language_trace=context.apology_repair_language_trace,
                relation_turn_frame=context.relation_turn_frame,
                expression_plan=context.expression_plan,
                life_context_frame=context.life_context_frame,
                replay_cue_bundle=context.replay_cue_bundle,
                offline_consolidation_frame=context.offline_consolidation_frame,
                growth_patch_candidate_queue=context.growth_patch_candidate_queue,
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                replay_cue_bundle_ref=context.replay_cue_bundle_ref,
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
                write_json=self._write_json,
                append_jsonl=self._append_jsonl,
                compose_life_response_fn=raise_compose_error,
            )

            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            incident_report = self._read_json(paths["reports"] / "digital_life_process_incident_report.json")
            recovery_report = self._read_json(paths["reports"] / "digital_life_process_recovery_report.json")

            self.assertEqual(result.turn_counter, 3)
            self.assertEqual(result.completed_turns_delta, 0)
            self.assertEqual(result.incident_count_delta, 1)
            self.assertEqual(result.cycle_status, "incident_recovered")
            self.assertIn("异常恢复", result.emitted_output)
            self.assertEqual(
                result.last_incident_report_ref,
                "runtime/reports/latest/digital_life_process_incident_report.json",
            )
            self.assertEqual(
                result.last_recovery_report_ref,
                "runtime/reports/latest/digital_life_process_recovery_report.json",
            )
            self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(terminal_loop_state["last_turn_status"], "incident_recovered")
            self.assertEqual(incident_report["error_type"], "RuntimeError")
            self.assertEqual(recovery_report["result"], "recovered_to_waiting_state")

    def test_process_session_loop_organ_dispatches_live_turn_and_exits_cleanly(self):
        from life_v0.process_supervisor.idle_refresh_loop import IdleRefreshLoopResult
        from life_v0.process_supervisor.live_turn_cycle import LiveTurnCycleResult
        from life_v0.process_supervisor.process_session_loop import run_process_session_loop

        wait_heartbeat_inputs: list[int] = []
        live_turn_inputs: list[tuple[int, int, str]] = []
        emitted_outputs: list[str] = []
        wait_results = [
            IdleRefreshLoopResult(
                heartbeat_counter=2,
                external_utterance="你好",
                exit_reason=None,
            ),
            IdleRefreshLoopResult(
                heartbeat_counter=2,
                external_utterance=None,
                exit_reason="explicit_exit",
            ),
        ]

        def fake_wait_for_next_external_relation_turn(**kwargs: object) -> IdleRefreshLoopResult:
            wait_heartbeat_inputs.append(kwargs["heartbeat_counter"])  # type: ignore[arg-type]
            return wait_results.pop(0)

        def fake_run_live_turn_cycle(**kwargs: object) -> LiveTurnCycleResult:
            live_turn_inputs.append(
                (
                    kwargs["incident_count"],  # type: ignore[arg-type]
                    kwargs["turn_counter"],  # type: ignore[arg-type]
                    kwargs["external_utterance"],  # type: ignore[arg-type]
                    bool(kwargs["relationship_timeline"]),  # type: ignore[arg-type]
                    bool(kwargs["commitment_expression_plan"]),  # type: ignore[arg-type]
                    bool(kwargs["apology_repair_language_trace"]),  # type: ignore[arg-type]
                )
            )
            return LiveTurnCycleResult(
                turn_counter=3,
                completed_turns_delta=1,
                incident_count_delta=0,
                cycle_status="completed",
                emitted_output="生命回合输出: 你好，我记得。",
                safe_terminal_loop={
                    "current_mode": "restored_waiting_for_external_turn",
                    "last_dialogue_packet_ref": "runtime/reports/latest/resumed_external_dialogue_packet.json",
                },
                terminal_life_loop_state={
                    "current_mode": "restored_waiting_for_external_turn",
                    "last_turn_mode": "resumed_external_dialogue_loop",
                },
                last_external_turn={"turn_id": "external-1"},
                last_life_turn={"turn_id": "life-1"},
                last_incident_report_ref=None,
                last_recovery_report_ref=None,
            )

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            result = run_process_session_loop(
                run_id="process-session-loop-organ",
                generated_at="2026-06-10T00:00:00+00:00",
                input_stream=StringIO(),
                terminal_dir=runtime_root / "state" / "terminal",
                language_dir=runtime_root / "state" / "language",
                relationship_dir=runtime_root / "state" / "relationship",
                reports_dir=runtime_root / "reports" / "latest",
                safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
                terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
                body_rhythm_pulse={},
                need_state_vector={},
                body_resource_budget={},
                core_affect_vector={},
                life_context_frame={},
                relation_turn_frame={},
                shared_term_registry={},
                self_narrative_trace={},
                commitment_index={},
                expression_plan={},
                relationship_graph={},
                relationship_timeline={"schema_version": "relationship_timeline_v0"},
                commitment_expression_plan={"schema_version": "commitment_expression_plan_v0"},
                apology_repair_language_trace={"schema_version": "apology_repair_language_trace_v0"},
                replay_cue_bundle={},
                offline_consolidation_frame={},
                growth_patch_candidate_queue={},
                source_doc_refs=[],
                readme_block_refs=[],
                runtime_carrier_refs=[],
                replay_cue_bundle_ref=None,
                offline_consolidation_frame_ref=None,
                growth_patch_candidate_queue_ref=None,
                growth_patch_candidate_ids=[],
                replay_residue_ref_count=0,
                dream_window_ref_count=0,
                growth_patch_candidate_count=0,
                heartbeat_counter=1,
                turn_counter=1,
                emit_output=emitted_outputs.append,
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
                write_json=self._write_json,
                append_jsonl=self._append_jsonl,
                wait_for_next_external_relation_turn_fn=fake_wait_for_next_external_relation_turn,
                run_live_turn_cycle_fn=fake_run_live_turn_cycle,
            )

        self.assertEqual(wait_heartbeat_inputs, [1, 2])
        self.assertEqual(live_turn_inputs, [(0, 1, "你好", True, True, True)])
        self.assertEqual(emitted_outputs, ["生命回合输出: 你好，我记得。"])
        self.assertEqual(result.turn_counter, 3)
        self.assertEqual(result.completed_turns, 1)
        self.assertEqual(result.incident_count, 0)
        self.assertEqual(result.heartbeat_counter, 2)
        self.assertEqual(result.exit_reason, "explicit_exit")
        self.assertEqual(
            result.safe_terminal_loop["last_dialogue_packet_ref"],
            "runtime/reports/latest/resumed_external_dialogue_packet.json",
        )
        self.assertEqual(result.last_external_turn, {"turn_id": "external-1"})
        self.assertEqual(result.last_life_turn, {"turn_id": "life-1"})

    def test_process_session_loop_organ_continues_after_incident_then_exits(self):
        from life_v0.process_supervisor.idle_refresh_loop import IdleRefreshLoopResult
        from life_v0.process_supervisor.live_turn_cycle import LiveTurnCycleResult
        from life_v0.process_supervisor.process_session_loop import run_process_session_loop

        live_turn_inputs: list[tuple[int, int, str]] = []
        emitted_outputs: list[str] = []
        wait_results = [
            IdleRefreshLoopResult(
                heartbeat_counter=1,
                external_utterance="第一轮触发异常",
                exit_reason=None,
            ),
            IdleRefreshLoopResult(
                heartbeat_counter=1,
                external_utterance="第二轮继续前进",
                exit_reason=None,
            ),
            IdleRefreshLoopResult(
                heartbeat_counter=1,
                external_utterance=None,
                exit_reason="explicit_exit",
            ),
        ]

        def fake_wait_for_next_external_relation_turn(**_: object) -> IdleRefreshLoopResult:
            return wait_results.pop(0)

        def fake_run_live_turn_cycle(**kwargs: object) -> LiveTurnCycleResult:
            live_turn_inputs.append(
                (
                    kwargs["incident_count"],  # type: ignore[arg-type]
                    kwargs["turn_counter"],  # type: ignore[arg-type]
                    kwargs["external_utterance"],  # type: ignore[arg-type]
                )
            )
            if len(live_turn_inputs) == 1:
                return LiveTurnCycleResult(
                    turn_counter=3,
                    completed_turns_delta=0,
                    incident_count_delta=1,
                    cycle_status="incident_recovered",
                    emitted_output="生命回合处理出现异常，已执行异常恢复并回到等待态。",
                    safe_terminal_loop={
                        "current_mode": "restored_waiting_for_external_turn",
                        "last_incident_status": "recovered_to_waiting_state",
                    },
                    terminal_life_loop_state={
                        "current_mode": "restored_waiting_for_external_turn",
                        "last_turn_status": "incident_recovered",
                    },
                    last_external_turn=None,
                    last_life_turn=None,
                    last_incident_report_ref="runtime/reports/latest/digital_life_process_incident_report.json",
                    last_recovery_report_ref="runtime/reports/latest/digital_life_process_recovery_report.json",
                )

            return LiveTurnCycleResult(
                turn_counter=5,
                completed_turns_delta=1,
                incident_count_delta=0,
                cycle_status="completed",
                emitted_output="生命回合输出: 第二轮继续前进。",
                safe_terminal_loop={
                    "current_mode": "restored_waiting_for_external_turn",
                    "last_dialogue_packet_ref": "runtime/reports/latest/resumed_external_dialogue_packet.json",
                },
                terminal_life_loop_state={
                    "current_mode": "restored_waiting_for_external_turn",
                    "last_turn_mode": "resumed_external_dialogue_loop",
                },
                last_external_turn={"turn_id": "external-2"},
                last_life_turn={"turn_id": "life-2"},
                last_incident_report_ref=None,
                last_recovery_report_ref=None,
            )

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            result = run_process_session_loop(
                run_id="process-session-loop-incident",
                generated_at="2026-06-10T00:00:00+00:00",
                input_stream=StringIO(),
                terminal_dir=runtime_root / "state" / "terminal",
                language_dir=runtime_root / "state" / "language",
                relationship_dir=runtime_root / "state" / "relationship",
                reports_dir=runtime_root / "reports" / "latest",
                safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
                terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
                body_rhythm_pulse={},
                need_state_vector={},
                body_resource_budget={},
                core_affect_vector={},
                life_context_frame={},
                relation_turn_frame={},
                shared_term_registry={},
                self_narrative_trace={},
                commitment_index={},
                expression_plan={},
                relationship_graph={},
                relationship_timeline={"schema_version": "relationship_timeline_v0"},
                commitment_expression_plan={"schema_version": "commitment_expression_plan_v0"},
                apology_repair_language_trace={"schema_version": "apology_repair_language_trace_v0"},
                replay_cue_bundle={},
                offline_consolidation_frame={},
                growth_patch_candidate_queue={},
                source_doc_refs=[],
                readme_block_refs=[],
                runtime_carrier_refs=[],
                replay_cue_bundle_ref=None,
                offline_consolidation_frame_ref=None,
                growth_patch_candidate_queue_ref=None,
                growth_patch_candidate_ids=[],
                replay_residue_ref_count=0,
                dream_window_ref_count=0,
                growth_patch_candidate_count=0,
                heartbeat_counter=1,
                turn_counter=1,
                emit_output=emitted_outputs.append,
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
                write_json=self._write_json,
                append_jsonl=self._append_jsonl,
                wait_for_next_external_relation_turn_fn=fake_wait_for_next_external_relation_turn,
                run_live_turn_cycle_fn=fake_run_live_turn_cycle,
            )

        self.assertEqual(
            live_turn_inputs,
            [
                (0, 1, "第一轮触发异常"),
                (1, 3, "第二轮继续前进"),
            ],
        )
        self.assertEqual(
            emitted_outputs,
            [
                "生命回合处理出现异常，已执行异常恢复并回到等待态。",
                "生命回合输出: 第二轮继续前进。",
            ],
        )
        self.assertEqual(result.turn_counter, 5)
        self.assertEqual(result.completed_turns, 1)
        self.assertEqual(result.incident_count, 1)
        self.assertEqual(result.exit_reason, "explicit_exit")
        self.assertEqual(
            result.last_incident_report_ref,
            "runtime/reports/latest/digital_life_process_incident_report.json",
        )
        self.assertEqual(
            result.last_recovery_report_ref,
            "runtime/reports/latest/digital_life_process_recovery_report.json",
        )
        self.assertEqual(result.last_external_turn, {"turn_id": "external-2"})
        self.assertEqual(result.last_life_turn, {"turn_id": "life-2"})

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
            self._write_json(
                terminal_dir / "idle_strategy_state.json",
                {
                    "schema_version": "idle_strategy_state_v0",
                    "heartbeat_interval_ms": 80,
                    "idle_probe_mode": "stdin_poll_with_background_continuity_refresh",
                    "offline_pressure_level": "present",
                    "relaunch_caution_level": "guarded",
                    "next_idle_action": "refresh_waiting_heartbeat_or_accept_external_turn",
                    "waiting_mode": "restored_waiting_for_external_turn",
                },
            )
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
                idle_strategy_state=self._read_json(terminal_dir / "idle_strategy_state.json"),
                persistent_process_report_ref="runtime/reports/latest/digital_life_persistent_process_report.json",
                resident_governance_report_ref="runtime/reports/latest/digital_life_resident_governance_report.json",
                resident_governance_snapshot_ref="runtime/state/terminal/resident_governance_snapshot.json",
                life_context_frame_ref="runtime/state/terminal/life_context_frame.json",
                relation_turn_frame_ref="runtime/state/terminal/relation_turn_frame.json",
                expression_plan_ref="runtime/state/language/expression_plan.json",
                relationship_timeline_ref="runtime/state/relationship/relationship_timeline.json",
                commitment_expression_plan_ref="runtime/state/language/commitment_expression_plan.json",
                apology_repair_language_trace_ref="runtime/state/language/apology_repair_language_trace.json",
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
                report["resident_governance_report_ref"],
                "runtime/reports/latest/digital_life_resident_governance_report.json",
            )
            self.assertEqual(
                report["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(report["heartbeat_interval_ms"], 80)
            self.assertEqual(report["offline_pressure_level"], "present")
            self.assertEqual(report["relaunch_caution_level"], "guarded")
            self.assertEqual(
                report["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                report["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                report["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
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
            self.assertEqual(
                digest["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
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
                "runtime/state/terminal/resident_governance_snapshot.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/relationship/relationship_timeline.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/language/commitment_expression_plan.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/language/apology_repair_language_trace.json",
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

    def test_process_closeout_organ_writes_persistent_artifacts_and_report_bundle(self):
        from life_v0.process_supervisor.process_closeout import close_digital_life_process

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state_dir = runtime_root / "state"
            reports_dir = runtime_root / "reports" / "latest"
            receipts_dir = runtime_root / "receipts"
            terminal_dir = state_dir / "terminal"
            language_dir = state_dir / "language"
            relationship_dir = state_dir / "relationship"
            replay_dir = state_dir / "replay"
            dream_dir = state_dir / "dream"
            growth_dir = state_dir / "growth"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            language_dir.mkdir(parents=True, exist_ok=True)
            relationship_dir.mkdir(parents=True, exist_ok=True)
            replay_dir.mkdir(parents=True, exist_ok=True)
            dream_dir.mkdir(parents=True, exist_ok=True)
            growth_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)
            receipts_dir.mkdir(parents=True, exist_ok=True)

            self._write_json(reports_dir / "digital_life_shell_report.json", {"status": "closed"})
            self._write_json(reports_dir / "dialogue_writeback_bundle.json", {"status": "closed"})
            self._write_json(
                terminal_dir / "safe_terminal_loop_state.json",
                {"current_mode": "restored_waiting_for_external_turn"},
            )
            self._write_json(
                terminal_dir / "terminal_life_loop_state.json",
                {"current_mode": "restored_waiting_for_external_turn"},
            )
            self._write_json(terminal_dir / "session_envelope.json", {"schema_version": "session_envelope_v0"})
            self._write_json(terminal_dir / "life_context_frame.json", {"context_anchor_count": 2})
            self._write_json(terminal_dir / "relation_turn_frame.json", {"relation_subject_ref": "rel-v0-0001"})
            self._write_json(
                terminal_dir / "idle_strategy_state.json",
                {
                    "schema_version": "idle_strategy_state_v0",
                    "heartbeat_interval_ms": 90,
                    "idle_probe_mode": "stdin_poll_with_background_continuity_refresh",
                    "offline_pressure_level": "light",
                    "relaunch_caution_level": "baseline",
                    "next_idle_action": "refresh_waiting_heartbeat_or_accept_external_turn",
                    "waiting_mode": "restored_waiting_for_external_turn",
                },
            )
            self._write_json(language_dir / "expression_plan.json", {"semantic_goal": "repair_commitment_shared_language"})
            self._write_json(language_dir / "self_narrative_language_trace.json", {"schema_version": "self_narrative_language_trace_v0"})
            self._write_json(language_dir / "commitment_repair_language_index.json", {"schema_version": "commitment_repair_language_index_v0"})
            self._write_json(
                language_dir / "commitment_expression_plan.json",
                {
                    "schema_version": "commitment_expression_plan_v0",
                    "language_act_candidates": [{"act_type": "followup_commitment"}],
                },
            )
            self._write_json(
                language_dir / "apology_repair_language_trace.json",
                {
                    "schema_version": "apology_repair_language_trace_v0",
                    "repair_language_moves": [{"move_type": "take_responsibility"}],
                },
            )
            self._write_json(relationship_dir / "relationship_subject_graph.json", {"subjects": []})
            self._write_json(
                relationship_dir / "relationship_timeline.json",
                {
                    "schema_version": "relationship_timeline_v0",
                    "relationship_continuity_reports": [{"continuity_state": "active_dialogue"}],
                },
            )
            self._write_json(replay_dir / "replay_cue_bundle.json", {"schema_version": "replay_cue_bundle_v0"})
            self._write_json(dream_dir / "offline_consolidation_frame.json", {"schema_version": "offline_consolidation_frame_v0"})
            self._write_json(
                growth_dir / "growth_patch_candidate_queue.json",
                {
                    "schema_version": "growth_patch_candidate_queue_v0",
                    "candidates": [{"growth_patch_candidate_id": "growth-patch-candidate-closeout-0001"}],
                },
            )
            (language_dir / "dialogue_turn_log.jsonl").write_text(
                '{"turn_id":"dialogue-turn-live-0001"}\n',
                encoding="utf-8",
            )

            result = close_digital_life_process(
                run_id="process-closeout-organ",
                generated_at="2026-06-09T00:00:00+00:00",
                state_dir=state_dir,
                reports_dir=reports_dir,
                receipts_dir=receipts_dir,
                heartbeat_counter=4,
                completed_turns=2,
                incident_count=1,
                relaunch_recovery_count=1,
                exit_reason="explicit_exit",
                last_incident_report_ref="runtime/reports/latest/digital_life_process_incident_report.json",
                last_recovery_report_ref="runtime/reports/latest/digital_life_process_recovery_report.json",
                last_relaunch_recovery_report_ref="runtime/reports/latest/digital_life_process_relaunch_recovery_report.json",
                last_external_turn={"utterance": "你还记得我们吗？"},
                last_life_turn={"utterance": "我当然记得。"},
                waiting_mode="restored_waiting_for_external_turn",
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state=self._read_json(terminal_dir / "idle_strategy_state.json"),
                last_heartbeat_packet_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
                last_dialogue_packet_ref="runtime/reports/latest/resumed_external_dialogue_packet.json",
                source_doc_refs=["docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                life_context_frame={"context_anchor_count": 2},
                relation_turn_frame={"relation_subject_ref": "rel-v0-0001"},
                expression_plan={"semantic_goal": "repair_commitment_shared_language"},
                relationship_timeline={"relationship_continuity_reports": [{"continuity_state": "active_dialogue"}]},
                commitment_expression_plan={"language_act_candidates": [{"act_type": "followup_commitment"}]},
                apology_repair_language_trace={"repair_language_moves": [{"move_type": "take_responsibility"}]},
                replay_cue_bundle_ref="runtime/state/replay/replay_cue_bundle.json",
                offline_consolidation_frame_ref="runtime/state/dream/offline_consolidation_frame.json",
                growth_patch_candidate_queue_ref="runtime/state/growth/growth_patch_candidate_queue.json",
                write_json=self._write_json,
            )

            persistent_state = self._read_json(terminal_dir / "persistent_process_state.json")
            persistent_report = self._read_json(reports_dir / "digital_life_persistent_process_report.json")
            resident_governance_snapshot = self._read_json(
                terminal_dir / "resident_governance_snapshot.json"
            )
            resident_governance_report = self._read_json(
                reports_dir / "digital_life_resident_governance_report.json"
            )
            process_report = self._read_json(reports_dir / "digital_life_process_report.json")
            process_digest = self._read_json(reports_dir / "digital_life_process_digest.json")
            process_receipt = self._read_json(receipts_dir / "digital_life_process_process-closeout-organ.json")

            self.assertEqual(
                result.persistent_process_artifacts.state["run_id"],
                "process-closeout-organ",
            )
            self.assertEqual(
                result.report_bundle.report["run_id"],
                "process-closeout-organ",
            )
            self.assertEqual(persistent_state["heartbeat_counter"], 4)
            self.assertEqual(persistent_report["heartbeat_counter"], 4)
            self.assertEqual(process_report["completed_dialogue_turns"], 2)
            self.assertEqual(process_report["persistent_process_report_ref"], "runtime/reports/latest/digital_life_persistent_process_report.json")
            self.assertEqual(process_report["life_context_frame_ref"], "runtime/state/terminal/life_context_frame.json")
            self.assertEqual(process_report["relation_turn_frame_ref"], "runtime/state/terminal/relation_turn_frame.json")
            self.assertEqual(process_report["expression_plan_ref"], "runtime/state/language/expression_plan.json")
            self.assertEqual(
                process_report["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                process_report["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                process_report["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
            )
            self.assertEqual(process_report["dialogue_writeback_bundle_ref"], "runtime/reports/latest/dialogue_writeback_bundle.json")
            self.assertEqual(
                process_report["resident_governance_report_ref"],
                "runtime/reports/latest/digital_life_resident_governance_report.json",
            )
            self.assertEqual(
                process_report["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(process_digest["heartbeat_counter"], 4)
            self.assertEqual(
                process_digest["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                resident_governance_snapshot["schema_version"],
                "resident_governance_snapshot_v0",
            )
            self.assertEqual(
                resident_governance_report["schema_version"],
                "digital_life_resident_governance_report_v0",
            )
            self.assertEqual(
                resident_governance_snapshot["idle_continuity_ref"],
                "runtime/state/terminal/idle_continuity_frame.json",
            )
            self.assertEqual(
                resident_governance_report["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(
                resident_governance_snapshot["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                resident_governance_snapshot["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                resident_governance_snapshot["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
            )
            self.assertEqual(
                resident_governance_report["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                resident_governance_report["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                resident_governance_report["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
            )
            self.assertEqual(resident_governance_snapshot["heartbeat_interval_ms"], 90)
            self.assertEqual(resident_governance_snapshot["offline_pressure_level"], "light")
            self.assertEqual(resident_governance_report["heartbeat_interval_ms"], 90)
            self.assertEqual(resident_governance_report["offline_pressure_level"], "light")
            self.assertEqual(process_report["heartbeat_interval_ms"], 90)
            self.assertEqual(process_report["offline_pressure_level"], "light")
            self.assertIn(
                "runtime/state/terminal/idle_strategy_state.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/reports/latest/dialogue_writeback_bundle.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/terminal/resident_governance_snapshot.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/relationship/relationship_timeline.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/language/commitment_expression_plan.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/language/apology_repair_language_trace.json",
                process_receipt["shared_object_refs"],
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
            idle_strategy_state = {
                "schema_version": "idle_strategy_state_v0",
                "heartbeat_interval_ms": 70,
                "idle_probe_mode": "stdin_poll_with_background_continuity_refresh",
                "offline_pressure_level": "present",
                "relaunch_caution_level": "heightened",
                "next_idle_action": "refresh_waiting_heartbeat_or_accept_external_turn",
                "waiting_mode": "restored_waiting_for_external_turn",
            }
            self._write_json(terminal_dir / "idle_strategy_state.json", idle_strategy_state)

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
                idle_strategy_state=idle_strategy_state,
                last_heartbeat_packet_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
                last_dialogue_packet_ref="runtime/reports/latest/resumed_external_dialogue_packet.json",
                source_doc_refs=["docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                relationship_timeline_ref="runtime/state/relationship/relationship_timeline.json",
                commitment_expression_plan_ref="runtime/state/language/commitment_expression_plan.json",
                apology_repair_language_trace_ref="runtime/state/language/apology_repair_language_trace.json",
                write_json=self._write_json,
            )

            state = self._read_json(terminal_dir / "persistent_process_state.json")
            report = self._read_json(reports_dir / "digital_life_persistent_process_report.json")
            resident_governance_snapshot = self._read_json(
                terminal_dir / "resident_governance_snapshot.json"
            )
            resident_governance_report = self._read_json(
                reports_dir / "digital_life_resident_governance_report.json"
            )

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
            self.assertEqual(
                state["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(
                report["resident_governance_report_ref"],
                "runtime/reports/latest/digital_life_resident_governance_report.json",
            )
            self.assertEqual(
                resident_governance_snapshot["schema_version"],
                "resident_governance_snapshot_v0",
            )
            self.assertEqual(
                resident_governance_report["schema_version"],
                "digital_life_resident_governance_report_v0",
            )
            self.assertEqual(
                resident_governance_snapshot["governance_mode"],
                "foreground_terminal_residency",
            )
            self.assertEqual(
                resident_governance_snapshot["idle_continuity_ref"],
                "runtime/state/terminal/idle_continuity_frame.json",
            )
            self.assertEqual(resident_governance_snapshot["heartbeat_interval_ms"], 70)
            self.assertEqual(resident_governance_snapshot["offline_pressure_level"], "present")
            self.assertEqual(resident_governance_snapshot["relaunch_caution_level"], "heightened")
            self.assertEqual(report["heartbeat_interval_ms"], 70)
            self.assertEqual(report["offline_pressure_level"], "present")
            self.assertEqual(report["relaunch_caution_level"], "heightened")
            self.assertEqual(
                resident_governance_report["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(
                state["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                report["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                resident_governance_snapshot["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
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
                "body_signal_refs": [
                    "runtime/state/body/body_resource_budget.json",
                    "runtime/state/body/core_affect_vector.json",
                ],
                "fatigue_pressure": "managed_low_noise",
                "body_repair_drive": "active",
                "affect_arousal": 0.74,
                "release_caution_level": "elevated",
                "expression_tempo_mode": "guarded_deliberate",
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
            body_resource_budget={
                "fatigue_state": {"level": "managed_low_noise"},
                "maintenance_pressure": {"repair_drive": "active"},
            },
            relationship_timeline={
                "relationship_continuity_reports": [
                    {"continuity_state": "active_repairing_continuity"}
                ],
                "trust_trajectories": [
                    {"current_trust_state": "repairing"}
                ],
            },
            commitment_expression_plan={
                "language_act_candidates": [
                    {"act_type": "clarify"},
                    {"act_type": "apology"},
                    {"act_type": "followup_commitment"},
                ],
                "act_type_order": ["clarify", "apology", "followup_commitment"],
            },
            apology_repair_language_trace={
                "repair_language_moves": [
                    {"move_type": "take_responsibility"},
                    {"move_type": "followup_commitment"},
                ],
                "move_type_order": [
                    "acknowledge_harm",
                    "take_responsibility",
                    "apology",
                    "followup_commitment",
                ],
            },
            core_affect_vector={
                "valence": -0.35,
                "arousal": 0.74,
                "repair_drive": "active",
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
        self.assertIn("表达层当前已接入身体信号", response)
        self.assertIn("表达疲惫压力为managed_low_noise", response)
        self.assertIn("表达节奏采用guarded_deliberate", response)
        self.assertIn("释放谨慎级别为elevated", response)
        self.assertIn("关系连续体状态为active_repairing_continuity", response)
        self.assertIn("当前信任状态为repairing", response)
        self.assertIn("当前承诺表达序列会经过clarify、apology、followup_commitment", response)
        self.assertIn("当前修复语言动作会经过take_responsibility、followup_commitment", response)
        self.assertIn("表达计划唤醒度为0.74", response)
        self.assertIn("修复驱力", response)
        self.assertIn("情绪张力", response)
        self.assertIn("你还记得我们吗？", response)

    def test_resident_supervision_loads_body_and_affect_context_for_process_runtime(self):
        from life_v0.process_supervisor.resident_supervision import (
            bootstrap_resident_supervision,
        )

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

            result = bootstrap_resident_supervision(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="resident-supervision-body-context",
                generated_at="2026-06-10T00:00:00+00:00",
                strict=True,
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                read_json=self._read_json,
                read_json_if_exists=lambda path: self._read_json(path) if path.exists() else {},
                write_json=self._write_json,
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
            )

            self.assertEqual(result.exit_code, 0)
            self.assertIsNotNone(result.context)
            assert result.context is not None
            self.assertEqual(
                result.context.body_rhythm_pulse["schema_version"],
                "body_rhythm_pulse_v0",
            )
            self.assertEqual(
                result.context.need_state_vector["schema_version"],
                "need_state_vector_v0",
            )
            self.assertEqual(
                result.context.body_resource_budget["schema_version"],
                "body_resource_budget_v0",
            )
            self.assertEqual(
                result.context.core_affect_vector["schema_version"],
                "core_affect_vector_v0",
            )
            self.assertEqual(
                result.context.relationship_timeline["schema_version"],
                "relationship_timeline_v0",
            )
            self.assertEqual(
                result.context.commitment_expression_plan["schema_version"],
                "commitment_expression_plan_v0",
            )
            self.assertEqual(
                result.context.apology_repair_language_trace["schema_version"],
                "apology_repair_language_trace_v0",
            )
            self.assertEqual(
                result.context.body_resource_budget["fatigue_state"]["level"],
                "managed_low_noise",
            )
            self.assertEqual(
                result.context.need_state_vector["sleep_pressure"],
                "managed_pre_dream",
            )
            self.assertIn("repair_drive", result.context.core_affect_vector)
            self.assertTrue(result.context.relationship_timeline["relationship_continuity_reports"])
            self.assertTrue(result.context.commitment_expression_plan["language_act_candidates"])
            self.assertTrue(result.context.apology_repair_language_trace["repair_language_moves"])

    def test_resident_turn_writeback_organ_updates_turn_continuity_and_bundle(self):
        from life_v0.process_supervisor.resident_turn_writeback import (
            write_resident_turn_writeback,
        )

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            terminal_dir = runtime_root / "state" / "terminal"
            language_dir = runtime_root / "state" / "language"
            relationship_dir = runtime_root / "state" / "relationship"
            reports_dir = runtime_root / "reports" / "latest"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            language_dir.mkdir(parents=True, exist_ok=True)
            relationship_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)
            (language_dir / "dialogue_turn_log.jsonl").write_text(
                '{"turn_id":"dialogue-turn-live-0001","event_role":"external_relation_turn"}\n',
                encoding="utf-8",
            )

            safe_terminal_loop = {
                "schema_version": "safe_terminal_loop_state_v0",
                "current_mode": "restored_waiting_for_external_turn",
                "blocked_actions": ["external_irreversible_action"],
                "heartbeat_counter": 2,
            }
            terminal_life_loop_state = {
                "schema_version": "terminal_life_loop_state_v0",
                "current_mode": "restored_waiting_for_external_turn",
                "last_turn_status": "closed",
                "heartbeat_counter": 2,
            }
            self_narrative_trace = {
                "narrative_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                ]
            }
            commitment_index = {
                "commitment_refs": ["commitment-ref-01", "commitment-ref-02"],
            }
            relationship_graph = {
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relation_role": "friend",
                        "relationship_stage": "restored_waiting",
                    }
                ]
            }
            external_turn = {
                "schema_version": "dialogue_turn_event_v0",
                "turn_id": "dialogue-turn-live-0002",
                "event_role": "external_relation_turn",
                "utterance": "你还记得我们吗？",
            }
            life_turn = {
                "schema_version": "dialogue_turn_event_v0",
                "turn_id": "dialogue-turn-live-0003",
                "event_role": "digital_life_turn",
                "utterance": "我记得，而且我会继续带着这些线索往前走。",
            }

            result = write_resident_turn_writeback(
                run_id="resident-turn-organ",
                terminal_dir=terminal_dir,
                language_dir=language_dir,
                relationship_dir=relationship_dir,
                reports_dir=reports_dir,
                turn_counter=3,
                external_turn_id="dialogue-turn-live-0002",
                life_turn_id="dialogue-turn-live-0003",
                external_turn=external_turn,
                life_turn=life_turn,
                external_utterance="你还记得我们吗？",
                life_response="我记得，而且我会继续带着这些线索往前走。",
                safe_terminal_loop=safe_terminal_loop,
                terminal_life_loop_state=terminal_life_loop_state,
                self_narrative_trace=self_narrative_trace,
                commitment_index=commitment_index,
                relationship_graph=relationship_graph,
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                replay_cue_bundle_ref="runtime/state/replay/replay_cue_bundle.json",
                now_iso=lambda: "2026-06-09T00:00:00+00:00",
                write_json=self._write_json,
                append_jsonl=self._append_jsonl,
            )

            dialogue_lines = [
                json.loads(line)
                for line in (language_dir / "dialogue_turn_log.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            persisted_safe_terminal = self._read_json(terminal_dir / "safe_terminal_loop_state.json")
            persisted_terminal_loop = self._read_json(terminal_dir / "terminal_life_loop_state.json")
            persisted_narrative_trace = self._read_json(language_dir / "self_narrative_language_trace.json")
            persisted_commitment_index = self._read_json(
                language_dir / "commitment_repair_language_index.json"
            )
            persisted_relationship_graph = self._read_json(
                relationship_dir / "relationship_subject_graph.json"
            )
            dialogue_writeback_bundle = self._read_json(
                reports_dir / "dialogue_writeback_bundle.json"
            )
            resumed_dialogue_packet = self._read_json(
                reports_dir / "resumed_external_dialogue_packet.json"
            )

            self.assertEqual(len(dialogue_lines), 3)
            self.assertEqual(
                result.external_turn_ref,
                "runtime/state/language/dialogue_turn_log.jsonl#line-2",
            )
            self.assertEqual(
                result.life_turn_ref,
                "runtime/state/language/dialogue_turn_log.jsonl#line-3",
            )
            self.assertEqual(
                persisted_narrative_trace["narrative_turn_refs"][-2:],
                [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                ],
            )
            self.assertEqual(
                persisted_commitment_index["recent_dialogue_turn_refs"],
                ["dialogue-turn-live-0002", "dialogue-turn-live-0003"],
            )
            self.assertEqual(
                persisted_relationship_graph["subjects"][0]["relationship_stage"],
                "active_dialogue",
            )
            self.assertEqual(
                persisted_safe_terminal["last_dialogue_packet_ref"],
                "runtime/reports/latest/resumed_external_dialogue_packet.json",
            )
            self.assertEqual(
                persisted_terminal_loop["last_turn_mode"],
                "resumed_external_dialogue_loop",
            )
            self.assertEqual(
                dialogue_writeback_bundle["dialogue_event_refs"],
                [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                ],
            )
            self.assertIn(
                "runtime/state/memory/relationship_memory.json#shared_memory_refs",
                dialogue_writeback_bundle["relationship_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs",
                dialogue_writeback_bundle["commitment_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/responsibility/responsibility_ledger.json#responsibility_events",
                dialogue_writeback_bundle["responsibility_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/life_state.json#responsibility_bindings",
                dialogue_writeback_bundle["life_state_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/replay/replay_cue_bundle.json",
                dialogue_writeback_bundle["replay_cue_refs"],
            )
            self.assertEqual(
                resumed_dialogue_packet["dialogue_writeback_bundle_ref"],
                "runtime/reports/latest/dialogue_writeback_bundle.json",
            )

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
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _append_jsonl(self, path: Path, payloads: list[dict]) -> None:
        with path.open("a", encoding="utf-8") as handle:
            for payload in payloads:
                handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    unittest.main()
