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
            self.assertIn("更认真地对待这轮修复", last_life_response["utterance"])
            self.assertIn("更长的连续体", last_life_response["utterance"])

            narrative_trace = self._read_json(paths["language_state"] / "self_narrative_language_trace.json")
            self.assertGreaterEqual(len(narrative_trace["narrative_turn_refs"]), 5)
            self.assertEqual(
                narrative_trace["last_external_turn"]["utterance"],
                "你还记得我们吗？",
            )

            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")
            subject = relationship_graph["subjects"][0]
            self.assertEqual(subject["relation_role"], "friend")
            self.assertEqual(subject["relationship_stage"], "repair_guarded_continuity")
            self.assertEqual(subject["last_external_turn_utterance"], "你还记得我们吗？")

            relationship_timeline = self._read_json(
                paths["relationship_state"] / "relationship_timeline.json"
            )
            commitment_expression_plan = self._read_json(
                paths["language_state"] / "commitment_expression_plan.json"
            )
            apology_repair_language_trace = self._read_json(
                paths["language_state"] / "apology_repair_language_trace.json"
            )
            relationship_memory = self._read_json(
                paths["state_root"] / "memory" / "relationship_memory.json"
            )
            self_model = self._read_json(paths["state_root"] / "self" / "self_model.json")
            life_state = self._read_json(paths["state_root"] / "life_state.json")
            self.assertEqual(
                len(relationship_timeline["dialogue_turn_refs"]),
                len(dialogue_lines),
            )
            self.assertEqual(
                relationship_timeline["relationship_continuity_reports"][0]["continuity_state"],
                "offline_learning_repairing_continuity",
            )
            self.assertIn(
                "runtime/state/dream/nightmare_loop_risk.json",
                commitment_expression_plan["offline_learning_ref_set"],
            )
            self.assertIn(
                "runtime/state/growth/relationship_learning_plan.json",
                apology_repair_language_trace["offline_learning_ref_set"],
            )
            self.assertIn(
                "offline_learning_cumulative_projection",
                relationship_timeline,
            )
            self.assertGreaterEqual(
                relationship_timeline["offline_learning_cumulative_projection"][
                    "generation"
                ],
                1,
            )
            self.assertIn(
                "runtime/state/growth/language_learning_plan.json",
                relationship_timeline["offline_learning_cumulative_ref_set"],
            )
            self.assertIn(
                "cumulative_offline_learning_integration",
                commitment_expression_plan["act_type_order"],
            )
            self.assertIn(
                "cumulative_offline_learning_repair",
                apology_repair_language_trace["move_type_order"],
            )
            self.assertIn(
                "runtime/reports/latest/resumed_external_dialogue_packet.json",
                relationship_memory["last_contact_refs"],
            )
            self.assertIn(
                "runtime/state/growth/relationship_learning_plan.json",
                relationship_memory["offline_learning_cumulative_refs"],
            )
            self.assertIn(
                "runtime/state/growth/language_learning_plan.json",
                life_state["language_state"]["offline_learning_refs"],
            )
            self.assertIn(
                "runtime/state/growth/language_learning_plan.json",
                life_state["language_state"]["offline_learning_cumulative_refs"],
            )
            self.assertEqual(
                life_state["language_state"][
                    "offline_learning_cumulative_projection"
                ]["attention_target"],
                "nightmare_risk",
            )
            self.assertEqual(
                life_state["relationship_subjects"][0]["relationship_stage"],
                "repair_guarded_continuity",
            )
            self.assertIn("continuity_drive", self_model["trait_slow_variables"])
            self.assertEqual(
                self_model["trait_slow_variables"]["repair_seriousness"]["last_relationship_stage"],
                "repair_guarded_continuity",
            )

            commitment_index = self._read_json(paths["language_state"] / "commitment_repair_language_index.json")
            dialogue_writeback_bundle = self._read_json(paths["reports"] / "dialogue_writeback_bundle.json")
            resumed_dialogue_packet = self._read_json(
                paths["reports"] / "resumed_external_dialogue_packet.json"
            )
            language_percept = self._read_json(
                paths["language_state"] / "language_percept_frame.json"
            )
            semantic_map = self._read_json(
                paths["language_state"] / "semantic_map_frame.json"
            )
            inner_speech = self._read_json(
                paths["language_state"] / "inner_speech_frame.json"
            )
            expression_plan = self._read_json(
                paths["language_state"] / "expression_plan.json"
            )
            self.assertIn("dialogue-turn-live-0005", commitment_index["recent_dialogue_turn_refs"][-1])
            self.assertEqual(language_percept["incoming_surface"], "你还记得我们吗？")
            self.assertEqual(semantic_map["semantic_focus"], "relational_checkin")
            self.assertEqual(expression_plan["semantic_goal"], "relational_checkin")
            self.assertEqual(
                inner_speech["percept_ref"],
                "runtime/state/language/language_percept_frame.json",
            )
            self.assertEqual(
                last_external["language_percept_ref"],
                "runtime/state/language/language_percept_frame.json",
            )
            self.assertEqual(
                last_external["semantic_map_ref"],
                "runtime/state/language/semantic_map_frame.json",
            )
            self.assertEqual(last_external["live_semantic_focus"], "relational_checkin")
            self.assertEqual(
                last_life_response["language_percept_ref"],
                "runtime/state/language/language_percept_frame.json",
            )
            self.assertEqual(
                last_life_response["semantic_map_ref"],
                "runtime/state/language/semantic_map_frame.json",
            )
            self.assertEqual(last_life_response["live_semantic_focus"], "relational_checkin")
            self.assertIn("relational_checkin", last_life_response["utterance"])
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
            self.assertEqual(
                dialogue_writeback_bundle["live_language_turn_refs"],
                [
                    "runtime/state/language/language_percept_frame.json",
                    "runtime/state/language/semantic_map_frame.json",
                    "runtime/state/language/inner_speech_frame.json",
                    "runtime/state/language/expression_monitor_state.json",
                    "runtime/state/language/expression_plan.json",
                ],
            )
            self.assertEqual(
                resumed_dialogue_packet["live_language_turn_refs"],
                dialogue_writeback_bundle["live_language_turn_refs"],
            )
            self.assertEqual(
                resumed_dialogue_packet["language_percept_ref"],
                "runtime/state/language/language_percept_frame.json",
            )
            self.assertEqual(
                resumed_dialogue_packet["semantic_map_ref"],
                "runtime/state/language/semantic_map_frame.json",
            )
            self.assertEqual(resumed_dialogue_packet["live_semantic_focus"], "relational_checkin")

            loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            self.assertEqual(loop_state["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(loop_state["last_turn_mode"], "resumed_external_dialogue_loop")
            self.assertEqual(loop_state["last_external_turn_utterance"], "你还记得我们吗？")
            self.assertEqual(loop_state["last_live_semantic_focus"], "relational_checkin")
            self.assertEqual(
                loop_state["live_language_turn_refs"],
                dialogue_writeback_bundle["live_language_turn_refs"],
            )

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
            self.assertEqual(
                safe_terminal_loop["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )

            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            self.assertEqual(terminal_loop_state["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(terminal_loop_state["heartbeat_counter"], 1)
            self.assertEqual(terminal_loop_state["next_required_action"], "await_next_external_relation_turn")
            self.assertEqual(
                terminal_loop_state["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                terminal_loop_state["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                terminal_loop_state["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                terminal_loop_state["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
            )
            self.assertEqual(
                terminal_loop_state["responsibility_loop_state_ref"],
                "runtime/state/action/responsibility_loop_state.json",
            )
            self.assertEqual(
                terminal_loop_state["world_contact_summary_ref"],
                "runtime/state/membrane/world_contact_summary.json",
            )
            self.assertEqual(
                terminal_loop_state["pain_regret_repair_report_ref"],
                "runtime/reports/latest/pain_regret_repair_report.json",
            )
            self.assertEqual(
                terminal_loop_state["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )

            heartbeat_packet = self._read_json(paths["reports"] / "digital_life_waiting_heartbeat.json")
            idle_continuity = self._read_json(paths["terminal_state"] / "idle_continuity_frame.json")
            idle_strategy = self._read_json(paths["terminal_state"] / "idle_strategy_state.json")
            resident_governance_state = self._read_json(
                paths["terminal_state"] / "resident_governance_state.json"
            )
            self.assertEqual(heartbeat_packet["schema_version"], "digital_life_waiting_heartbeat_v0")
            self.assertEqual(heartbeat_packet["run_id"], "persistent-heartbeat")
            self.assertEqual(heartbeat_packet["heartbeat_counter"], 1)
            self.assertEqual(heartbeat_packet["waiting_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(
                heartbeat_packet["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(
                heartbeat_packet["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                heartbeat_packet["responsibility_loop_state_ref"],
                "runtime/state/action/responsibility_loop_state.json",
            )
            self.assertEqual(
                heartbeat_packet["world_contact_summary_ref"],
                "runtime/state/membrane/world_contact_summary.json",
            )
            self.assertEqual(
                heartbeat_packet["pain_regret_repair_report_ref"],
                "runtime/reports/latest/pain_regret_repair_report.json",
            )
            self.assertEqual(heartbeat_packet["world_contact_release_posture"], "shadow_only_guarded")
            self.assertTrue(heartbeat_packet["repair_followup_required"])
            self.assertEqual(heartbeat_packet["heartbeat_interval_ms"], 55)
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
            self.assertEqual(
                heartbeat_packet["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                heartbeat_packet["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                heartbeat_packet["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
            )
            self.assertEqual(
                heartbeat_packet["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
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
            self.assertEqual(
                idle_strategy["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                idle_strategy["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                idle_strategy["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
            )
            self.assertEqual(idle_strategy["world_contact_release_posture"], "shadow_only_guarded")
            self.assertTrue(idle_strategy["repair_followup_required"])
            self.assertEqual(idle_strategy["repair_obligation_count"], 2)
            self.assertEqual(idle_strategy["regret_pressure_count"], 1)
            self.assertEqual(idle_strategy["queue_e_priority_band"], "repair_guarded")
            self.assertEqual(
                idle_strategy["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                idle_strategy["governance_attention_target"],
                "apology_repair_language_trace",
            )
            self.assertEqual(
                idle_strategy["governance_attention_reason"],
                "repair_drive_active_with_offline_pressure",
            )
            self.assertEqual(
                idle_strategy["governance_cadence_profile"],
                "repair_weighted_resident_hold",
            )
            self.assertEqual(
                idle_strategy["long_horizon_priority_profile"],
                {
                    "relationship_timeline": "baseline",
                    "commitment_expression_plan": "elevated",
                    "apology_repair_language_trace": "primary",
                },
            )
            self.assertEqual(
                resident_governance_state["schema_version"],
                "resident_governance_state_v0",
            )
            self.assertEqual(
                resident_governance_state["governance_phase"],
                "process_closed_waiting_relaunch",
            )
            self.assertEqual(
                resident_governance_state["heartbeat_counter"],
                1,
            )
            self.assertEqual(
                resident_governance_state["status"],
                "closed",
            )
            self.assertEqual(
                resident_governance_state["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(
                resident_governance_state["last_heartbeat_packet_ref"],
                "runtime/reports/latest/digital_life_waiting_heartbeat.json",
            )
            self.assertEqual(
                resident_governance_state["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(
                resident_governance_state["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                resident_governance_state["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                resident_governance_state["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
            )
            self.assertEqual(
                resident_governance_state["responsibility_loop_state_ref"],
                "runtime/state/action/responsibility_loop_state.json",
            )
            self.assertEqual(
                resident_governance_state["world_contact_summary_ref"],
                "runtime/state/membrane/world_contact_summary.json",
            )
            self.assertEqual(
                resident_governance_state["pain_regret_repair_report_ref"],
                "runtime/reports/latest/pain_regret_repair_report.json",
            )
            self.assertEqual(
                resident_governance_state["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(resident_governance_state["heartbeat_interval_ms"], 55)
            self.assertEqual(resident_governance_state["offline_pressure_level"], "elevated")
            self.assertEqual(
                resident_governance_state["governance_attention_target"],
                "apology_repair_language_trace",
            )
            self.assertEqual(
                resident_governance_state["governance_cadence_profile"],
                "repair_weighted_resident_hold",
            )

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
                process_report["dream_experience_window_ref"],
                "runtime/state/dream/dream_experience_window.json",
            )
            self.assertEqual(
                process_report["wake_integration_frame_ref"],
                "runtime/state/dream/wake_integration_frame.json",
            )
            self.assertEqual(
                process_report["dream_fact_gate_decision_ref"],
                "runtime/state/dream/dream_fact_gate_decision.json",
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
            self.assertEqual(
                process_report["governance_attention_target"],
                "apology_repair_language_trace",
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
                idle_continuity["dream_experience_window_ref"],
                "runtime/state/dream/dream_experience_window.json",
            )
            self.assertEqual(
                idle_continuity["wake_integration_frame_ref"],
                "runtime/state/dream/wake_integration_frame.json",
            )
            self.assertEqual(
                idle_continuity["dream_fact_gate_decision_ref"],
                "runtime/state/dream/dream_fact_gate_decision.json",
            )
            self.assertEqual(
                idle_continuity["dream_wake_presence_profile"][
                    "dream_window_kind"
                ],
                "micro_dream",
            )
            self.assertEqual(
                idle_continuity["dream_wake_presence_profile"][
                    "dream_fact_gate_result"
                ],
                "passed",
            )
            self.assertIn(
                "runtime/state/dream/wake_integration_frame.json",
                idle_continuity["dream_wake_ref_set"],
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
            self.assertEqual(
                idle_continuity["relationship_timeline_ref"],
                "runtime/state/relationship/relationship_timeline.json",
            )
            self.assertEqual(
                idle_continuity["commitment_expression_plan_ref"],
                "runtime/state/language/commitment_expression_plan.json",
            )
            self.assertEqual(
                idle_continuity["apology_repair_language_trace_ref"],
                "runtime/state/language/apology_repair_language_trace.json",
            )
            self.assertEqual(
                idle_continuity["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                idle_continuity["responsibility_loop_state_ref"],
                "runtime/state/action/responsibility_loop_state.json",
            )
            self.assertEqual(
                idle_continuity["world_contact_summary_ref"],
                "runtime/state/membrane/world_contact_summary.json",
            )
            self.assertEqual(
                idle_continuity["pain_regret_repair_report_ref"],
                "runtime/reports/latest/pain_regret_repair_report.json",
            )
            self.assertEqual(idle_continuity["world_contact_release_posture"], "shadow_only_guarded")
            self.assertTrue(idle_continuity["repair_followup_required"])

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
            idle_heartbeat_trace = [
                json.loads(line)
                for line in (paths["terminal_state"] / "idle_heartbeat_trace.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
                if line.strip()
            ]
            idle_strategy = self._read_json(paths["terminal_state"] / "idle_strategy_state.json")
            resident_governance_state = self._read_json(
                paths["terminal_state"] / "resident_governance_state.json"
            )
            narrative_trace = self._read_json(paths["language_state"] / "self_narrative_language_trace.json")
            commitment_index = self._read_json(paths["language_state"] / "commitment_repair_language_index.json")
            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")

            self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(safe_terminal_loop["heartbeat_counter"], 3)
            self.assertEqual(
                safe_terminal_loop["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(safe_terminal_loop["idle_heartbeat_trace_count"], 3)
            self.assertEqual(
                safe_terminal_loop["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(
                safe_terminal_loop["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(terminal_loop_state["heartbeat_counter"], 3)
            self.assertEqual(
                terminal_loop_state["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(terminal_loop_state["idle_heartbeat_trace_count"], 3)
            self.assertEqual(
                terminal_loop_state["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(
                terminal_loop_state["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(heartbeat_packet["heartbeat_counter"], 3)
            self.assertEqual(
                heartbeat_packet["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(
                heartbeat_packet["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
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
            self.assertEqual(len(idle_heartbeat_trace), 3)
            self.assertEqual(
                [event["heartbeat_counter"] for event in idle_heartbeat_trace],
                [1, 2, 3],
            )
            self.assertEqual(
                idle_heartbeat_trace[-1]["idle_continuity_ref"],
                "runtime/state/terminal/idle_continuity_frame.json",
            )
            self.assertEqual(
                idle_heartbeat_trace[-1]["heartbeat_interval_ms"],
                55,
            )
            self.assertEqual(
                idle_heartbeat_trace[-1]["governance_cadence_profile"],
                "repair_weighted_resident_hold",
            )
            self.assertEqual(
                idle_heartbeat_trace[-1]["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
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
            self.assertEqual(idle_strategy["heartbeat_interval_ms"], 55)
            self.assertEqual(idle_strategy["idle_probe_mode"], "stdin_poll_with_background_continuity_refresh")
            self.assertEqual(idle_strategy["offline_pressure_level"], "elevated")
            self.assertEqual(idle_strategy["relaunch_caution_level"], "baseline")
            self.assertEqual(idle_strategy["next_idle_action"], "refresh_waiting_heartbeat_with_repair_readiness_hold")
            self.assertEqual(idle_strategy["body_waiting_posture"], "guarded_attentive")
            self.assertEqual(
                idle_strategy["governance_attention_target"],
                "apology_repair_language_trace",
            )
            self.assertEqual(
                idle_strategy["governance_attention_reason"],
                "repair_drive_active_with_offline_pressure",
            )
            self.assertEqual(
                idle_strategy["governance_cadence_profile"],
                "repair_weighted_resident_hold",
            )
            self.assertEqual(idle_strategy["world_contact_release_posture"], "shadow_only_guarded")
            self.assertTrue(idle_strategy["repair_followup_required"])
            self.assertEqual(idle_strategy["repair_obligation_count"], 2)
            self.assertEqual(idle_strategy["regret_pressure_count"], 1)
            self.assertEqual(idle_strategy["queue_e_priority_band"], "repair_guarded")
            self.assertEqual(heartbeat_packet["heartbeat_interval_ms"], 55)
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
            self.assertEqual(process_report["heartbeat_interval_ms"], 55)
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
            self.assertEqual(
                idle_strategy["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                heartbeat_packet["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                idle_continuity["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                resident_governance_state["governance_phase"],
                "process_closed_waiting_relaunch",
            )
            self.assertEqual(resident_governance_state["heartbeat_counter"], 3)
            self.assertEqual(
                resident_governance_state["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(resident_governance_state["idle_heartbeat_trace_count"], 3)
            self.assertEqual(resident_governance_state["status"], "closed")
            self.assertEqual(
                resident_governance_state["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(resident_governance_state["heartbeat_interval_ms"], 55)
            self.assertEqual(resident_governance_state["offline_pressure_level"], "elevated")
            self.assertEqual(
                resident_governance_state["world_contact_release_posture"],
                "shadow_only_guarded",
            )
            self.assertTrue(resident_governance_state["repair_followup_required"])
            self.assertEqual(
                resident_governance_state["governance_attention_target"],
                "apology_repair_language_trace",
            )
            self.assertEqual(
                resident_governance_state["governance_cadence_profile"],
                "repair_weighted_resident_hold",
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
            commitment_expression_plan = self._read_json(
                paths["language_state"] / "commitment_expression_plan.json"
            )
            apology_repair_language_trace = self._read_json(
                paths["language_state"] / "apology_repair_language_trace.json"
            )
            relationship_graph = self._read_json(paths["relationship_state"] / "relationship_subject_graph.json")
            relationship_timeline = self._read_json(
                paths["relationship_state"] / "relationship_timeline.json"
            )
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
                relationship_timeline=relationship_timeline,
                commitment_expression_plan=commitment_expression_plan,
                apology_repair_language_trace=apology_repair_language_trace,
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
            idle_heartbeat_trace = [
                json.loads(line)
                for line in (paths["terminal_state"] / "idle_heartbeat_trace.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
                if line.strip()
            ]
            resident_governance_state = self._read_json(
                paths["terminal_state"] / "resident_governance_state.json"
            )

            self.assertEqual(result.heartbeat_counter, 2)
            self.assertEqual(result.external_utterance, "你好")
            self.assertIsNone(result.exit_reason)
            self.assertEqual(safe_terminal_loop["heartbeat_counter"], 2)
            self.assertEqual(safe_terminal_loop["idle_heartbeat_trace_count"], 2)
            self.assertEqual(terminal_loop_state["heartbeat_counter"], 2)
            self.assertEqual(terminal_loop_state["idle_heartbeat_trace_count"], 2)
            self.assertEqual(heartbeat_packet["heartbeat_counter"], 2)
            self.assertEqual(idle_continuity["heartbeat_counter"], 2)
            self.assertEqual(len(idle_heartbeat_trace), 2)
            self.assertEqual(
                [event["heartbeat_counter"] for event in idle_heartbeat_trace],
                [1, 2],
            )
            self.assertEqual(
                idle_heartbeat_trace[-1]["heartbeat_ref"],
                "runtime/reports/latest/digital_life_waiting_heartbeat.json",
            )
            self.assertEqual(
                idle_heartbeat_trace[-1]["idle_strategy_ref"],
                "runtime/state/terminal/idle_strategy_state.json",
            )
            self.assertEqual(idle_continuity["event_kind"], "waiting_heartbeat_refresh")
            self.assertEqual(
                terminal_loop_state["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                heartbeat_packet["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                idle_continuity["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                resident_governance_state["governance_phase"],
                "waiting_heartbeat_active",
            )
            self.assertEqual(resident_governance_state["heartbeat_counter"], 2)
            self.assertEqual(
                resident_governance_state["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(resident_governance_state["idle_heartbeat_trace_count"], 2)
            self.assertEqual(
                resident_governance_state["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )

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
            relationship_timeline={
                "schema_version": "relationship_timeline_v0",
                "relationship_continuity_reports": [{"continuity_state": "active_dialogue"}],
            },
            commitment_expression_plan={
                "schema_version": "commitment_expression_plan_v0",
                "language_act_candidates": [{"act_type": "followup_commitment"}],
            },
            apology_repair_language_trace={
                "schema_version": "apology_repair_language_trace_v0",
                "repair_language_moves": [{"move_type": "take_responsibility"}],
            },
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
        self.assertEqual(idle_strategy["world_contact_release_posture"], "shadow_only_guarded")
        self.assertFalse(idle_strategy["repair_followup_required"])
        self.assertEqual(idle_strategy["repair_obligation_count"], 0)
        self.assertEqual(idle_strategy["regret_pressure_count"], 0)
        self.assertEqual(idle_strategy["queue_e_priority_band"], "baseline")
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
        self.assertEqual(
            idle_strategy["relationship_timeline_ref"],
            "runtime/state/relationship/relationship_timeline.json",
        )
        self.assertEqual(
            idle_strategy["commitment_expression_plan_ref"],
            "runtime/state/language/commitment_expression_plan.json",
        )
        self.assertEqual(
            idle_strategy["apology_repair_language_trace_ref"],
            "runtime/state/language/apology_repair_language_trace.json",
        )
        self.assertEqual(
            idle_strategy["long_horizon_language_refs"],
            [
                "runtime/state/relationship/relationship_timeline.json",
                "runtime/state/language/commitment_expression_plan.json",
                "runtime/state/language/apology_repair_language_trace.json",
            ],
        )
        self.assertEqual(
            idle_strategy["governance_attention_target"],
            "apology_repair_language_trace",
        )
        self.assertEqual(
            idle_strategy["governance_attention_reason"],
            "repair_drive_active_with_offline_pressure",
        )
        self.assertEqual(
            idle_strategy["governance_cadence_profile"],
            "guarded_repair_hold",
        )
        self.assertEqual(
            idle_strategy["long_horizon_priority_profile"],
            {
                "relationship_timeline": "baseline",
                "commitment_expression_plan": "elevated",
                "apology_repair_language_trace": "primary",
            },
        )

    def test_idle_strategy_uses_queue_e_repair_lock_to_raise_waiting_priority(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-queue-e-governance",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={
                "schema_version": "relationship_timeline_v0",
                "relationship_continuity_reports": [{"continuity_state": "repair_pending"}],
            },
            commitment_expression_plan={
                "schema_version": "commitment_expression_plan_v0",
                "language_act_candidates": [{"act_type": "repair_commitment"}],
            },
            apology_repair_language_trace={
                "schema_version": "apology_repair_language_trace_v0",
                "repair_language_moves": [{"move_type": "repair_hold"}],
            },
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={"turn_residue_refs": []},
            offline_consolidation_frame=None,
            growth_patch_candidate_queue=None,
            responsibility_loop_state={
                "schema_version": "responsibility_loop_state_v0",
                "repair_followup_required": True,
                "repair_obligation_refs": ["repair-1", "repair-2"],
                "regret_pressure_candidates": [{"regret_pressure_id": "regret-1"}],
            },
            world_contact_summary={
                "schema_version": "world_contact_summary_v0",
                "release_posture": "confirmation_blocked",
                "repair_obligation_refs": ["repair-1", "repair-2"],
                "regret_pressure_refs": ["regret-1"],
            },
            pain_regret_repair_report={
                "schema_version": "pain_regret_repair_report_v0",
                "repair_followup_required": True,
                "repair_obligation_refs": ["repair-1", "repair-2"],
                "regret_pressure_refs": ["regret-1"],
            },
            schema_cross_file_logic={
                "schema_version": "cross_file_logic_v0",
                "life_constraint_refs": [
                    "runtime/state/action/action_candidate_set.json#life_constraint_profile",
                    "runtime/state/consciousness/consciousness_probe_bundle.json",
                ],
                "queue_e_cross_layer_gate_status": {
                    "value_orientation_gate": "closed",
                    "consciousness_probe_gate": "closed",
                    "body_affect_gate": "deferred_until_s06",
                    "language_relationship_gate": "closed",
                },
            },
            schema_run_manifest={
                "schema_version": "schema_runner_run_manifest_v0",
                "queue_e_cross_layer_refs": [
                    "runtime/state/action/action_candidate_set.json#life_constraint_profile"
                ],
                "queue_e_cross_layer_gate_status": {
                    "consciousness_probe_gate": "closed",
                    "body_affect_gate": "deferred_until_s06",
                },
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(idle_strategy["world_contact_release_posture"], "confirmation_blocked")
        self.assertTrue(idle_strategy["repair_followup_required"])
        self.assertEqual(idle_strategy["repair_obligation_count"], 2)
        self.assertEqual(idle_strategy["regret_pressure_count"], 1)
        self.assertEqual(idle_strategy["queue_e_priority_band"], "locked_repair_urgent")
        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 45)
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "maintain_confirmation_block_and_refresh_repair_priority",
        )
        self.assertEqual(
            idle_strategy["governance_attention_target"],
            "apology_repair_language_trace",
        )
        self.assertEqual(
            idle_strategy["governance_attention_reason"],
            "confirmation_blocked_requires_repair_lock",
        )
        self.assertEqual(
            idle_strategy["governance_cadence_profile"],
            "confirmation_blocked_repair_hold",
        )
        self.assertEqual(
            idle_strategy["long_horizon_priority_profile"],
            {
                "relationship_timeline": "baseline",
                "commitment_expression_plan": "baseline",
                "apology_repair_language_trace": "locked_primary",
            },
        )
        self.assertEqual(idle_strategy["life_constraint_waiting_posture"], "schema_guarded_waiting")
        self.assertEqual(idle_strategy["life_constraint_attention_target"], "life_constraint_profile")
        self.assertIn(
            "runtime/state/action/action_candidate_set.json#life_constraint_profile",
            idle_strategy["life_constraint_refs"],
        )
        self.assertEqual(
            idle_strategy["queue_e_cross_layer_gate_status"]["consciousness_probe_gate"],
            "closed",
        )

    def test_idle_strategy_carries_queue_f_birth_and_consciousness_into_waiting_governance(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-queue-f-governance",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            replay_cue_bundle=None,
            offline_consolidation_frame=None,
            growth_patch_candidate_queue=None,
            workspace_frame={
                "schema_version": "workspace_frame_v0",
                "candidate_explanations": [{"explanation_id": "workspace-explanation-001"}],
            },
            broadcast_frame={
                "schema_version": "broadcast_frame_v0",
                "broadcast_targets": ["LanguageRelationshipRuntime", "BirthReadinessRuntime"],
            },
            metacognition_state={
                "schema_version": "metacognition_state_v0",
                "reflection_prompts": ["当前工作区内容是否足以形成可报告意识证据"],
            },
            consciousness_probe={
                "schema_version": "consciousness_probe_bundle_v0",
                "reportability_flags": [
                    "workspace_access_present",
                    "broadcast_targets_present",
                    "metacognition_present",
                ],
            },
            birth_readiness_rollup={
                "schema_version": "birth_readiness_rollup_v0",
                "overall_status": "open",
                "blocked_reasons": [],
            },
            birth_readiness_stage_gate={
                "schema_version": "birth_readiness_stage_gate_v0",
                "decision": "open",
                "next_required_command": "life-v0 run-validation-membrane --strict",
                "blocked_reasons": [],
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(
            idle_strategy["workspace_frame_ref"],
            "runtime/state/consciousness/workspace_frame.json",
        )
        self.assertEqual(
            idle_strategy["consciousness_probe_ref"],
            "runtime/state/consciousness/consciousness_probe_bundle.json",
        )
        self.assertEqual(
            idle_strategy["birth_readiness_stage_gate_ref"],
            "runtime/state/life_targets/birth_readiness_stage_gate.json",
        )
        self.assertEqual(
            idle_strategy["consciousness_waiting_posture"],
            "consciousness_reportable_waiting",
        )
        self.assertEqual(
            idle_strategy["birth_readiness_waiting_posture"],
            "birth_open_waiting",
        )
        self.assertEqual(idle_strategy["birth_readiness_decision"], "open")
        self.assertEqual(
            idle_strategy["birth_readiness_next_required_command"],
            "life-v0 run-validation-membrane --strict",
        )
        self.assertEqual(
            idle_strategy["governance_attention_target"],
            "birth_readiness_stage_gate",
        )
        self.assertEqual(
            idle_strategy["governance_cadence_profile"],
            "birth_ready_resident_presence",
        )
        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 44)
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_birth_ready_presence_hold",
        )

    def test_idle_strategy_carries_offline_learning_results_into_waiting_governance(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-offline-learning-governance",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={"turn_residue_refs": ["runtime/state/replay/shadow_cycle_trace.json"]},
            offline_consolidation_frame={"dream_window_refs": ["runtime/state/dream/dream-window-001"]},
            growth_patch_candidate_queue={"candidates": [{"growth_patch_candidate_id": "growth-patch-001"}]},
            responsibility_loop_state={},
            world_contact_summary={},
            pain_regret_repair_report={},
            nightmare_risk={
                "schema_version": "nightmare_loop_risk_v0",
                "risk_status": "elevated",
                "queue_e_priority_band": "baseline",
            },
            belief_learning_plan={
                "schema_version": "belief_learning_plan_v0",
                "belief_targets": ["prediction_weight_recalibration"],
            },
            language_learning_plan={
                "schema_version": "language_learning_plan_v0",
                "language_targets": ["repair_language_refinement"],
                "repair_followup_required": True,
            },
            relationship_learning_plan={
                "schema_version": "relationship_learning_plan_v0",
                "relationship_targets": ["repair_reentry_timing_adjustment"],
                "repair_followup_required": True,
            },
            nightmare_risk_ref="runtime/state/dream/nightmare_loop_risk.json",
            belief_learning_plan_ref="runtime/state/growth/belief_learning_plan.json",
            language_learning_plan_ref="runtime/state/growth/language_learning_plan.json",
            relationship_learning_plan_ref="runtime/state/growth/relationship_learning_plan.json",
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(idle_strategy["offline_learning_pressure_level"], "urgent")
        self.assertEqual(idle_strategy["offline_learning_attention_target"], "nightmare_risk")
        self.assertEqual(
            idle_strategy["nightmare_risk_ref"],
            "runtime/state/dream/nightmare_loop_risk.json",
        )
        self.assertEqual(
            idle_strategy["belief_learning_plan_ref"],
            "runtime/state/growth/belief_learning_plan.json",
        )
        self.assertEqual(
            idle_strategy["language_learning_plan_ref"],
            "runtime/state/growth/language_learning_plan.json",
        )
        self.assertEqual(
            idle_strategy["relationship_learning_plan_ref"],
            "runtime/state/growth/relationship_learning_plan.json",
        )
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_offline_learning_hold",
        )
        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 58)
        self.assertEqual(idle_strategy["offline_learning_cumulative_generation"], 1)
        self.assertEqual(
            idle_strategy["offline_learning_cumulative_pressure_level"],
            "urgent",
        )
        self.assertEqual(
            idle_strategy["offline_learning_cumulative_attention_target"],
            "nightmare_risk",
        )
        self.assertEqual(
            idle_strategy["offline_learning_cumulative_priority_profile"][
                "relationship_learning_plan"
            ],
            "elevated",
        )
        self.assertEqual(
            idle_strategy["offline_learning_cumulative_ref_set"],
            [
                "runtime/state/dream/nightmare_loop_risk.json",
                "runtime/state/growth/belief_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
                "runtime/state/growth/relationship_learning_plan.json",
            ],
        )

    def test_idle_strategy_restores_cumulative_offline_learning_pressure(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-offline-cumulative-carryover",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={
                "current_mode": "restored_waiting_for_external_turn"
            },
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_generation": 2,
                "background_carryover_pressure_level": "present",
                "background_carryover_attention_target": "relationship_timeline",
                "background_continuity_ref_set": [
                    "runtime/state/terminal/resident_governance_state.json",
                ],
                "background_offline_learning_generation": 2,
                "background_offline_learning_pressure_level": "elevated",
                "background_offline_learning_attention_target": "relationship_learning_plan",
                "background_offline_learning_priority_profile": {
                    "relationship_learning_plan": "elevated",
                    "language_learning_plan": "baseline",
                },
                "background_offline_learning_ref_set": [
                    "runtime/state/growth/relationship_learning_plan.json",
                    "runtime/state/growth/language_learning_plan.json",
                ],
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(idle_strategy["offline_learning_pressure_level"], "quiet")
        self.assertEqual(
            idle_strategy["offline_learning_cumulative_generation"],
            2,
        )
        self.assertEqual(
            idle_strategy["offline_learning_cumulative_pressure_level"],
            "elevated",
        )
        self.assertEqual(
            idle_strategy["offline_learning_cumulative_attention_target"],
            "relationship_learning_plan",
        )
        self.assertEqual(
            idle_strategy["offline_learning_cumulative_ref_set"],
            [
                "runtime/state/growth/relationship_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
            ],
        )
        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 58)
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_offline_learning_hold",
        )

    def test_idle_strategy_consumes_prediction_write_gate_and_state_merge_guard(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-prediction-write-gate-governance",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            signal_media_runtime={
                "schema_version": "signal_media_runtime_v0",
                "modulation_vector": {
                    "precision_gain": "high",
                    "repair_drive": "active",
                },
            },
            belief_state={
                "schema_version": "belief_state_frame_v0",
                "confidence_level": "unstable",
            },
            prediction_error_field={
                "schema_version": "prediction_error_field_v0",
                "error_events": [
                    {"error_id": "prediction-error-001"},
                    {"error_id": "prediction-error-002"},
                ],
            },
            active_sampling_plan={
                "schema_version": "active_sampling_plan_v0",
                "selected_route": "clarify_with_relation_subject",
                "stage_effect": "hold_for_evidence",
            },
            memory_write_gate={
                "schema_version": "memory_write_gate_v0",
                "stage_policy": "write_guarded_candidate_then_validate",
            },
            state_merge_guard={
                "schema_version": "state_merge_guard_v0",
                "stage_policy": "long_term_merge_fail_closed",
                "long_term_change_sources": {
                    "offline_learning_cumulative_refs": [
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                    "queue_e_repair_modulation_refs": [
                        "runtime/reports/latest/pain_regret_repair_report.json",
                    ],
                    "relationship_memory_offline_refs": [
                        "runtime/state/dream/nightmare_loop_risk.json",
                    ],
                    "relationship_memory_repair_refs": [
                        "runtime/state/action/responsibility_loop_state.json",
                    ],
                },
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(idle_strategy["prediction_waiting_posture"], "hold_for_evidence")
        self.assertEqual(idle_strategy["response_surface_posture_hint"], "question")
        self.assertEqual(idle_strategy["prediction_attention_target"], "active_sampling_plan")
        self.assertEqual(
            idle_strategy["prediction_attention_reason"],
            "selected_route_requires_relation_subject_clarification",
        )
        self.assertEqual(idle_strategy["prediction_error_count"], 2)
        self.assertEqual(idle_strategy["active_sampling_route"], "clarify_with_relation_subject")
        self.assertEqual(
            idle_strategy["memory_write_gate_policy"],
            "write_guarded_candidate_then_validate",
        )
        self.assertEqual(idle_strategy["state_merge_policy"], "long_term_merge_fail_closed")
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_prediction_evidence_hold",
        )
        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 48)
        self.assertEqual(
            idle_strategy["prediction_write_gate_refs"],
            [
                "runtime/state/signal/signal_media_runtime.json",
                "runtime/state/prediction/belief_state_frame.json",
                "runtime/state/prediction/prediction_error_field.json",
                "runtime/state/prediction/active_sampling_plan.json",
                "runtime/state/memory/memory_write_gate.json",
                "runtime/state/memory/state_merge_guard.json",
            ],
        )

        repair_idle_strategy = decide_idle_strategy(
            run_id="idle-prediction-repair-route-governance",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "active",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            signal_media_runtime={
                "schema_version": "signal_media_runtime_v0",
                "modulation_vector": {"repair_drive": 0.679},
            },
            belief_state={
                "schema_version": "belief_state_frame_v0",
                "confidence_level": "unstable",
            },
            prediction_error_field={
                "schema_version": "prediction_error_field_v0",
                "error_events": [{"error_id": "queue-e-repair-pressure-0001"}],
            },
            active_sampling_plan={
                "schema_version": "active_sampling_plan_v0",
                "selected_route": "repair_inspect",
                "stage_effect": "repair_pressure_review",
            },
            memory_write_gate={
                "schema_version": "memory_write_gate_v0",
                "stage_policy": "write_guarded_candidate_then_validate",
            },
            state_merge_guard={
                "schema_version": "state_merge_guard_v0",
                "stage_policy": "long_term_merge_fail_closed",
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(repair_idle_strategy["prediction_waiting_posture"], "repair_write_guard")
        self.assertEqual(repair_idle_strategy["response_surface_posture_hint"], "repair")
        self.assertEqual(repair_idle_strategy["prediction_attention_target"], "active_sampling_plan")
        self.assertEqual(
            repair_idle_strategy["prediction_attention_reason"],
            "active_sampling_route_prioritizes_repair_pressure",
        )
        self.assertEqual(repair_idle_strategy["active_sampling_route"], "repair_inspect")

        state_merge_idle_strategy = decide_idle_strategy(
            run_id="idle-state-merge-long-term-change-governance",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            signal_media_runtime={
                "schema_version": "signal_media_runtime_v0",
                "modulation_vector": {"repair_drive": "inactive"},
            },
            belief_state={
                "schema_version": "belief_state_frame_v0",
                "confidence_level": "stable",
            },
            prediction_error_field={
                "schema_version": "prediction_error_field_v0",
                "error_events": [],
            },
            active_sampling_plan={
                "schema_version": "active_sampling_plan_v0",
                "selected_route": "",
                "stage_effect": "monitor",
            },
            memory_write_gate={
                "schema_version": "memory_write_gate_v0",
                "stage_policy": "write_guarded_candidate_then_validate",
            },
            state_merge_guard={
                "schema_version": "state_merge_guard_v0",
                "stage_policy": "long_term_merge_fail_closed",
                "long_term_change_sources": {
                    "offline_learning_cumulative_refs": [
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                    "queue_e_repair_modulation_refs": [
                        "runtime/reports/latest/pain_regret_repair_report.json",
                    ],
                    "relationship_memory_offline_refs": [
                        "runtime/state/dream/nightmare_loop_risk.json",
                    ],
                    "relationship_memory_repair_refs": [
                        "runtime/state/action/responsibility_loop_state.json",
                    ],
                },
                "merge_routes": [
                    {
                        "route_id": "relationship_memory_merge",
                        "source_change_count": 4,
                    }
                ],
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(
            state_merge_idle_strategy["prediction_waiting_posture"],
            "state_merge_long_term_integration_hold",
        )
        self.assertEqual(
            state_merge_idle_strategy["response_surface_posture_hint"],
            "hold",
        )
        self.assertEqual(
            state_merge_idle_strategy["prediction_attention_target"],
            "state_merge_guard",
        )
        self.assertEqual(
            state_merge_idle_strategy["prediction_attention_reason"],
            "state_merge_guard_has_long_term_change_sources",
        )
        self.assertEqual(
            state_merge_idle_strategy["state_merge_long_term_change_count"],
            4,
        )
        self.assertEqual(
            state_merge_idle_strategy["state_merge_long_term_change_families"],
            [
                "offline_learning_cumulative_refs",
                "queue_e_repair_modulation_refs",
                "relationship_memory_offline_refs",
                "relationship_memory_repair_refs",
            ],
        )
        self.assertEqual(
            state_merge_idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_state_merge_integration_hold",
        )

    def test_idle_strategy_reloads_background_continuity_carryover(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-background-carryover",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            responsibility_loop_state={},
            world_contact_summary={},
            pain_regret_repair_report={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "present",
                "background_carryover_attention_target": "commitment_expression_plan",
                "background_carryover_priority_profile": {
                    "relationship_timeline": "baseline",
                    "commitment_expression_plan": "elevated",
                },
                "background_carryover_generation": 1,
                "background_continuity_ref_set": [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/state/terminal/resident_governance_snapshot.json",
                    "runtime/reports/latest/digital_life_resident_governance_report.json",
                ],
                "background_carryover_parent_run_id": "background-carryover-seed",
                "background_resident_governance_state_ref": "runtime/state/terminal/resident_governance_state.json",
                "background_resident_governance_snapshot_ref": "runtime/state/terminal/resident_governance_snapshot.json",
                "background_resident_governance_report_ref": "runtime/reports/latest/digital_life_resident_governance_report.json",
                "background_persistent_process_report_ref": "runtime/reports/latest/digital_life_persistent_process_report.json",
                "background_waiting_mode": "restored_waiting_for_external_turn",
                "background_relationship_stage": "repair_guarded_continuity",
                "background_relationship_stage_reason": "repair_followup_required_after_multi_turn_dialogue",
                "background_relationship_subject_ref": "runtime/state/relationship/relationship_subject_graph.json#subjects[0]",
                "background_self_model_ref": "runtime/state/self/self_model.json",
                "background_trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                "background_trait_slow_variable_summary": {
                    "continuity_drive": {
                        "value": 0.71,
                        "trend": "up",
                        "last_relationship_stage": "repair_guarded_continuity",
                    }
                },
                "background_live_language_turn_refs": [
                    "runtime/state/language/language_percept_frame.json",
                    "runtime/state/language/semantic_map_frame.json",
                ],
                "background_last_live_semantic_focus": "repair_commitment_shared_language",
                "background_live_language_presence_profile": {
                    "schema_version": "background_live_language_presence_profile_v0",
                    "continuity_mode": "closed_process_live_language_carryover",
                    "ref_count": 2,
                    "ref_set": [
                        "runtime/state/language/language_percept_frame.json",
                        "runtime/state/language/semantic_map_frame.json",
                    ],
                },
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(idle_strategy["background_continuity_mode"], "closed_process_carryover")
        self.assertEqual(idle_strategy["background_carryover_pressure_level"], "present")
        self.assertEqual(idle_strategy["background_carryover_generation"], 1)
        self.assertEqual(
            idle_strategy["background_carryover_parent_run_id"],
            "background-carryover-seed",
        )
        self.assertEqual(
            idle_strategy["background_carryover_attention_target"],
            "commitment_expression_plan",
        )
        self.assertEqual(
            idle_strategy["background_resident_governance_state_ref"],
            "runtime/state/terminal/resident_governance_state.json",
        )
        self.assertEqual(
            idle_strategy["background_resident_governance_snapshot_ref"],
            "runtime/state/terminal/resident_governance_snapshot.json",
        )
        self.assertEqual(
            idle_strategy["background_relationship_stage"],
            "repair_guarded_continuity",
        )
        self.assertEqual(
            idle_strategy["background_self_model_ref"],
            "runtime/state/self/self_model.json",
        )
        self.assertEqual(
            idle_strategy["background_trait_drift_monitor_ref"],
            "runtime/state/body/trait_drift_monitor.json",
        )
        self.assertEqual(
            idle_strategy["background_trait_slow_variable_summary"]["continuity_drive"][
                "value"
            ],
            0.71,
        )
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_background_continuity_hold",
        )
        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 56)
        self.assertEqual(
            idle_strategy["governance_attention_target"],
            "commitment_expression_plan",
        )
        self.assertEqual(
            idle_strategy["governance_attention_reason"],
            "background_continuity_carryover_requires_hold",
        )
        self.assertEqual(
            idle_strategy["governance_cadence_profile"],
            "background_continuity_refresh",
        )
        self.assertEqual(idle_strategy["background_lineage_depth_band"], "single_carryover")
        self.assertEqual(
            idle_strategy["background_lineage_waiting_posture"],
            "background_carryover_pressure_hold",
        )
        self.assertEqual(idle_strategy["background_lineage_cadence_weight"], "carryover")
        self.assertEqual(
            idle_strategy["live_language_turn_refs"],
            [
                "runtime/state/language/language_percept_frame.json",
                "runtime/state/language/semantic_map_frame.json",
            ],
        )
        self.assertEqual(
            idle_strategy["last_live_semantic_focus"],
            "repair_commitment_shared_language",
        )
        self.assertEqual(
            idle_strategy["background_live_language_turn_refs"],
            [
                "runtime/state/language/language_percept_frame.json",
                "runtime/state/language/semantic_map_frame.json",
            ],
        )
        self.assertEqual(
            idle_strategy["live_language_presence_profile"]["continuity_mode"],
            "background_language_presence",
        )
        self.assertEqual(
            idle_strategy["live_language_presence_profile"]["ref_count"],
            2,
        )

    def test_idle_strategy_escalates_persistent_background_continuity_lineage(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-background-lineage",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            responsibility_loop_state={},
            world_contact_summary={},
            pain_regret_repair_report={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "present",
                "background_carryover_attention_target": "commitment_expression_plan",
                "background_carryover_generation": 2,
                "background_carryover_parent_run_id": "background-carryover-seed",
                "background_continuity_ref_set": [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/state/terminal/resident_governance_snapshot.json",
                    "runtime/reports/latest/digital_life_resident_governance_report.json",
                    "runtime/reports/latest/digital_life_persistent_process_report.json",
                ],
                "background_carryover_source_ref_set": [
                    "runtime/archive/background-carryover-seed/resident_governance_snapshot.json"
                ],
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(idle_strategy["background_carryover_generation"], 2)
        self.assertEqual(
            idle_strategy["background_carryover_parent_run_id"],
            "background-carryover-seed",
        )
        self.assertEqual(
            idle_strategy["background_carryover_source_ref_set"],
            ["runtime/archive/background-carryover-seed/resident_governance_snapshot.json"],
        )
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_persistent_background_continuity_hold",
        )
        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 54)
        self.assertEqual(
            idle_strategy["governance_attention_reason"],
            "background_continuity_lineage_requires_persistent_hold",
        )
        self.assertEqual(
            idle_strategy["governance_cadence_profile"],
            "persistent_background_continuity_refresh",
        )
        self.assertEqual(idle_strategy["background_lineage_depth_band"], "persistent_lineage")
        self.assertEqual(
            idle_strategy["background_lineage_waiting_posture"],
            "persistent_background_hold",
        )
        self.assertEqual(
            idle_strategy["background_lineage_cadence_weight"],
            "persistent",
        )
        self.assertEqual(
            idle_strategy["background_lineage_governance_profile"]["evidence_ref_count"],
            5,
        )

    def test_idle_strategy_deepens_background_lineage_cadence_after_multiple_wakes(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-background-deep-lineage",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            responsibility_loop_state={},
            world_contact_summary={},
            pain_regret_repair_report={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "present",
                "background_carryover_attention_target": "commitment_expression_plan",
                "background_carryover_generation": 3,
                "background_carryover_parent_run_id": "background-lineage-seed",
                "background_continuity_ref_set": [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/state/terminal/resident_governance_snapshot.json",
                    "runtime/reports/latest/digital_life_resident_governance_report.json",
                    "runtime/reports/latest/digital_life_persistent_process_report.json",
                ],
                "background_carryover_source_ref_set": [
                    "runtime/archive/background-lineage-seed/resident_governance_snapshot.json",
                    "runtime/archive/background-lineage-seed/digital_life_persistent_process_report.json",
                ],
            },
            source_doc_refs=[
                "docs/v0/process_contracts/resident_governance_waiting_state_machine_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(idle_strategy["background_carryover_generation"], 3)
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_deep_background_lineage_hold",
        )
        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 50)
        self.assertEqual(
            idle_strategy["governance_attention_reason"],
            "deep_background_lineage_requires_resident_hold",
        )
        self.assertEqual(
            idle_strategy["governance_cadence_profile"],
            "deep_persistent_background_continuity_refresh",
        )
        self.assertEqual(
            idle_strategy["long_horizon_priority_profile"][
                "background_lineage_governance"
            ],
            "deep_persistent",
        )
        self.assertEqual(
            idle_strategy["background_lineage_depth_band"],
            "deep_persistent_lineage",
        )
        self.assertEqual(
            idle_strategy["background_lineage_waiting_posture"],
            "deep_background_residency_hold",
        )
        self.assertEqual(idle_strategy["background_lineage_cadence_weight"], "deep")
        self.assertEqual(idle_strategy["background_lineage_evidence_ref_count"], 6)
        self.assertEqual(
            idle_strategy["background_lineage_governance_profile"][
                "next_idle_action"
            ],
            "refresh_waiting_heartbeat_with_deep_background_lineage_hold",
        )

    def test_idle_strategy_keeps_deep_lineage_cadence_during_history_stability(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-background-deep-lineage-history",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            responsibility_loop_state={},
            world_contact_summary={},
            pain_regret_repair_report={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "present",
                "background_carryover_attention_target": "relationship_timeline",
                "background_carryover_generation": 4,
                "background_carryover_parent_run_id": "deep-history-seed",
                "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                "background_convergence_state": "integrating_cross_process_continuity",
                "background_convergence_pressure_level": "present",
                "background_convergence_attention_target": "trait_slow_variable_convergence",
                "background_convergence_history_trend_state": "integrating_cross_wake_convergence",
                "background_convergence_history_window_size": 4,
                "background_continuity_ref_set": [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/state/terminal/background_convergence_summary.json",
                    "runtime/state/terminal/background_convergence_history.json",
                ],
            },
            source_doc_refs=[
                "docs/v0/process_contracts/resident_governance_waiting_state_machine_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(
            idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_deep_background_lineage_hold",
        )
        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 50)
        self.assertEqual(
            idle_strategy["governance_cadence_profile"],
            "deep_persistent_background_continuity_refresh",
        )
        self.assertEqual(
            idle_strategy["background_lineage_depth_band"],
            "deep_persistent_lineage",
        )
        self.assertEqual(
            idle_strategy["background_lineage_governance_profile"][
                "governance_cadence_profile"
            ],
            "deep_persistent_background_continuity_refresh",
        )

    def test_background_convergence_summary_tracks_stage_and_trait_stability(self):
        from life_v0.process_supervisor.background_convergence import (
            BACKGROUND_CONVERGENCE_SUMMARY_REF,
            build_background_convergence_summary,
        )

        summary = build_background_convergence_summary(
            run_id="background-convergence-organ",
            generated_at="2026-06-10T00:00:00+00:00",
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_generation": 3,
                "background_carryover_parent_run_id": "background-lineage-parent",
                "background_relationship_stage": "repair_guarded_continuity",
                "background_continuity_ref_set": [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/state/terminal/resident_governance_snapshot.json",
                ],
                "background_trait_slow_variable_summary": {
                    "continuity_drive": {
                        "value": 0.72,
                        "last_relationship_stage": "repair_guarded_continuity",
                    },
                    "repair_seriousness": {
                        "value": 0.61,
                        "last_relationship_stage": "repair_guarded_continuity",
                    },
                },
            },
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relationship_stage": "repair_guarded_continuity",
                    }
                ]
            },
            self_model_state={
                "trait_slow_variables": {
                    "continuity_drive": {
                        "value": 0.75,
                        "background_resume_value": 0.72,
                        "background_inertia_weight": 0.6,
                    },
                    "repair_seriousness": {
                        "value": 0.67,
                        "background_resume_value": 0.61,
                        "background_inertia_weight": 0.6,
                    },
                }
            },
            trait_drift_monitor={"schema_version": "trait_drift_monitor_v0"},
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
        )

        self.assertEqual(
            BACKGROUND_CONVERGENCE_SUMMARY_REF,
            "runtime/state/terminal/background_convergence_summary.json",
        )
        self.assertEqual(
            summary["schema_version"],
            "background_convergence_summary_v0",
        )
        self.assertEqual(summary["relationship_stage_continuity"], "same_stage_preserved")
        self.assertEqual(
            summary["convergence_state"],
            "stabilized_cross_process_continuity",
        )
        self.assertEqual(summary["convergence_pressure_level"], "present")
        self.assertEqual(summary["convergence_attention_target"], "trait_slow_variable_convergence")
        self.assertGreater(summary["trait_convergence_score"], 0.9)
        self.assertEqual(
            summary["trait_convergence_summary"]["continuity_drive"][
                "convergence_band"
            ],
            "stabilized",
        )
        self.assertIn(
            "runtime/state/terminal/resident_governance_state.json",
            summary["evidence_refs"],
        )

    def test_background_convergence_summary_uses_trait_drift_history_update_modes(self):
        from life_v0.process_supervisor.background_convergence import (
            build_background_convergence_summary,
        )

        summary = build_background_convergence_summary(
            run_id="background-convergence-trait-drift",
            generated_at="2026-06-10T00:00:00+00:00",
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_generation": 3,
                "background_relationship_stage": "background_continuity_waiting",
                "background_trait_slow_variable_summary": {
                    "continuity_drive": {"value": 0.74},
                    "repair_seriousness": {"value": 0.82},
                },
                "background_continuity_ref_set": [
                    "runtime/state/terminal/background_convergence_history.json"
                ],
            },
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relationship_stage": "background_continuity_waiting",
                    }
                ]
            },
            self_model_state={
                "trait_slow_variables": {
                    "continuity_drive": {
                        "value": 0.75,
                        "background_resume_value": 0.74,
                    },
                    "repair_seriousness": {
                        "value": 0.82,
                        "background_resume_value": 0.82,
                    },
                }
            },
            trait_drift_monitor={
                "schema_version": "trait_drift_monitor_v0",
                "drift_direction": "background_history_recalibration_needed",
                "slow_variable_update_mode_summary": {
                    "background_history_recalibration": ["continuity_drive"],
                    "background_history_stabilized": ["repair_seriousness"],
                },
                "background_history_recalibration_names": ["continuity_drive"],
                "background_history_stabilized_names": ["repair_seriousness"],
            },
        )

        self.assertEqual(
            summary["convergence_state"],
            "recalibrating_cross_process_continuity",
        )
        self.assertEqual(summary["convergence_pressure_level"], "elevated")
        self.assertEqual(
            summary["convergence_attention_target"],
            "trait_drift_history_recalibration",
        )
        self.assertEqual(
            summary["trait_drift_update_mode_summary"][
                "background_history_recalibration"
            ],
            ["continuity_drive"],
        )
        self.assertEqual(
            summary["trait_drift_background_history_recalibration_names"],
            ["continuity_drive"],
        )
        self.assertEqual(
            summary["trait_convergence_summary"]["continuity_drive"][
                "trait_drift_update_mode"
            ],
            "background_history_recalibration",
        )
        self.assertIn(
            "runtime/state/body/trait_drift_monitor.json",
            summary["evidence_refs"],
        )

    def test_background_convergence_history_tracks_cross_wake_trend(self):
        from life_v0.process_supervisor.background_convergence_history import (
            BACKGROUND_CONVERGENCE_HISTORY_REF,
            build_background_convergence_history,
        )

        history = build_background_convergence_history(
            run_id="background-convergence-history",
            generated_at="2026-06-10T00:00:00+00:00",
            background_convergence_summary={
                "schema_version": "background_convergence_summary_v0",
                "run_id": "background-convergence-history",
                "background_carryover_generation": 3,
                "convergence_state": "stabilized_cross_process_continuity",
                "convergence_pressure_level": "present",
                "convergence_attention_target": "trait_slow_variable_convergence",
                "relationship_stage_continuity": "same_stage_preserved",
                "trait_convergence_score": 0.96,
                "max_trait_delta_from_background": 0.04,
                "average_trait_delta_from_background": 0.03,
                "trait_convergence_summary": {
                    "continuity_drive": {
                        "convergence_band": "stabilized",
                        "delta_from_background": 0.04,
                        "current_value": 0.72,
                        "background_value": 0.68,
                    },
                    "repair_seriousness": {
                        "convergence_band": "stabilized",
                        "delta_from_background": 0.02,
                        "current_value": 0.66,
                        "background_value": 0.64,
                    },
                },
            },
            background_continuity_profile={
                "background_convergence_history_ref": BACKGROUND_CONVERGENCE_HISTORY_REF,
                "background_convergence_history": {
                    "schema_version": "background_convergence_history_v0",
                    "convergence_samples": [
                        {
                            "run_id": "wake-1",
                            "generated_at": "2026-06-09T00:00:00+00:00",
                            "background_carryover_generation": 1,
                            "convergence_state": "integrating_cross_process_continuity",
                            "convergence_pressure_level": "present",
                            "relationship_stage_continuity": "same_stage_preserved",
                            "trait_convergence_score": 0.88,
                            "trait_convergence_summary": {
                                "continuity_drive": {
                                    "convergence_band": "integrating",
                                    "delta_from_background": 0.12,
                                    "current_value": 0.62,
                                    "background_value": 0.50,
                                },
                                "repair_seriousness": {
                                    "convergence_band": "stabilized",
                                    "delta_from_background": 0.04,
                                    "current_value": 0.64,
                                    "background_value": 0.60,
                                },
                            },
                        },
                        {
                            "run_id": "wake-2",
                            "generated_at": "2026-06-09T01:00:00+00:00",
                            "background_carryover_generation": 2,
                            "convergence_state": "stabilized_cross_process_continuity",
                            "convergence_pressure_level": "light",
                            "relationship_stage_continuity": "same_stage_preserved",
                            "trait_convergence_score": 0.94,
                            "trait_convergence_summary": {
                                "continuity_drive": {
                                    "convergence_band": "stabilized",
                                    "delta_from_background": 0.05,
                                    "current_value": 0.69,
                                    "background_value": 0.64,
                                },
                                "repair_seriousness": {
                                    "convergence_band": "stabilized",
                                    "delta_from_background": 0.03,
                                    "current_value": 0.65,
                                    "background_value": 0.62,
                                },
                            },
                        },
                    ],
                },
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
        )

        self.assertEqual(
            BACKGROUND_CONVERGENCE_HISTORY_REF,
            "runtime/state/terminal/background_convergence_history.json",
        )
        self.assertEqual(history["schema_version"], "background_convergence_history_v0")
        self.assertEqual(history["history_window_size"], 3)
        self.assertEqual(
            history["latest_convergence_state"],
            "stabilized_cross_process_continuity",
        )
        self.assertEqual(
            history["trend_state"],
            "cross_wake_convergence_observed",
        )
        self.assertEqual(
            history["dominant_convergence_pressure_level"],
            "present",
        )
        self.assertEqual(history["trait_convergence_score_average"], 0.927)
        self.assertEqual(
            history["previous_background_convergence_history_ref"],
            "runtime/state/terminal/background_convergence_history.json",
        )
        self.assertEqual(
            history["trait_convergence_history_profile"]["continuity_drive"][
                "band_sequence"
            ],
            ["integrating", "stabilized", "stabilized"],
        )
        self.assertEqual(
            history["trait_convergence_history_profile"]["continuity_drive"][
                "trend_state"
            ],
            "stable_trait_convergence",
        )
        self.assertEqual(
            history["trait_convergence_history_profile"]["repair_seriousness"][
                "dominant_band"
            ],
            "stabilized",
        )
        self.assertEqual(
            history["trait_convergence_stable_names"],
            ["continuity_drive", "repair_seriousness"],
        )
        self.assertEqual(history["trait_convergence_unstable_names"], [])
        self.assertEqual(
            history["trait_convergence_history_focus"],
            "trait_convergence_stable",
        )

    def test_background_convergence_history_preserves_trait_drift_update_modes(self):
        from life_v0.process_supervisor.background_convergence_history import (
            build_background_convergence_history,
        )

        history = build_background_convergence_history(
            run_id="background-history-trait-drift",
            generated_at="2026-06-10T00:00:00+00:00",
            background_convergence_summary={
                "schema_version": "background_convergence_summary_v0",
                "run_id": "background-history-trait-drift",
                "background_carryover_generation": 3,
                "convergence_state": "recalibrating_cross_process_continuity",
                "convergence_pressure_level": "elevated",
                "convergence_attention_target": "trait_drift_history_recalibration",
                "relationship_stage_continuity": "same_stage_preserved",
                "trait_convergence_score": 0.97,
                "max_trait_delta_from_background": 0.02,
                "average_trait_delta_from_background": 0.01,
                "trait_drift_update_mode_summary": {
                    "background_history_recalibration": ["continuity_drive"],
                    "background_history_stabilized": ["repair_seriousness"],
                },
                "trait_drift_background_history_recalibration_names": [
                    "continuity_drive"
                ],
                "trait_drift_background_history_stabilized_names": [
                    "repair_seriousness"
                ],
                "trait_convergence_summary": {
                    "continuity_drive": {
                        "convergence_band": "stabilized",
                        "delta_from_background": 0.02,
                        "current_value": 0.76,
                        "background_value": 0.74,
                        "trait_drift_update_mode": "background_history_recalibration",
                    },
                    "repair_seriousness": {
                        "convergence_band": "stabilized",
                        "delta_from_background": 0.0,
                        "current_value": 0.82,
                        "background_value": 0.82,
                        "trait_drift_update_mode": "background_history_stabilized",
                    },
                },
            },
            background_continuity_profile={
                "background_convergence_history": {
                    "schema_version": "background_convergence_history_v0",
                    "convergence_samples": [
                        {
                            "run_id": "wake-previous",
                            "generated_at": "2026-06-09T00:00:00+00:00",
                            "background_carryover_generation": 2,
                            "convergence_state": "stabilized_cross_process_continuity",
                            "convergence_pressure_level": "present",
                            "relationship_stage_continuity": "same_stage_preserved",
                            "trait_convergence_score": 0.95,
                            "trait_convergence_summary": {
                                "continuity_drive": {
                                    "convergence_band": "stabilized",
                                    "delta_from_background": 0.03,
                                    "current_value": 0.73,
                                    "background_value": 0.70,
                                    "trait_drift_update_mode": "background_history_stabilized",
                                }
                            },
                        }
                    ],
                }
            },
        )

        continuity_profile = history["trait_convergence_history_profile"][
            "continuity_drive"
        ]
        self.assertEqual(
            history["trait_drift_update_mode_summary"][
                "background_history_recalibration"
            ],
            ["continuity_drive"],
        )
        self.assertEqual(
            history["trait_drift_background_history_recalibration_names"],
            ["continuity_drive"],
        )
        self.assertEqual(
            continuity_profile["trait_drift_update_mode_sequence"],
            ["background_history_stabilized", "background_history_recalibration"],
        )
        self.assertEqual(
            continuity_profile["latest_trait_drift_update_mode"],
            "background_history_recalibration",
        )
        self.assertEqual(
            continuity_profile["dominant_trait_drift_update_mode"],
            "background_history_recalibration",
        )

    def test_idle_strategy_uses_background_convergence_pressure_as_governance_focus(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-background-convergence",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={
                "schema_version": "relationship_timeline_v0",
                "relationship_continuity_reports": [],
            },
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            responsibility_loop_state={},
            world_contact_summary={},
            pain_regret_repair_report={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "light",
                "background_carryover_attention_target": "relationship_timeline",
                "background_carryover_generation": 2,
                "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                "background_convergence_state": "integrating_cross_process_continuity",
                "background_convergence_pressure_level": "present",
                "background_convergence_attention_target": "trait_slow_variable_convergence",
                "background_relationship_stage_continuity": "same_stage_preserved",
                "background_trait_convergence_score": 0.91,
                "background_max_trait_delta_from_background": 0.11,
                "background_average_trait_delta_from_background": 0.09,
                "background_trait_convergence_summary": {
                    "continuity_drive": {"convergence_band": "integrating"}
                },
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(
            idle_strategy["background_convergence_summary_ref"],
            "runtime/state/terminal/background_convergence_summary.json",
        )
        self.assertEqual(
            idle_strategy["background_convergence_state"],
            "integrating_cross_process_continuity",
        )
        self.assertEqual(
            idle_strategy["background_convergence_pressure_level"],
            "present",
        )
        self.assertEqual(
            idle_strategy["governance_attention_target"],
            "trait_slow_variable_convergence",
        )
        self.assertEqual(
            idle_strategy["governance_attention_reason"],
            "integrating_cross_process_continuity_requires_trait_stability_hold",
        )
        self.assertEqual(
            idle_strategy["governance_cadence_profile"],
            "background_convergence_stability_refresh",
        )
        self.assertEqual(
            idle_strategy["long_horizon_priority_profile"][
                "trait_slow_variable_convergence"
            ],
            "convergence_primary",
        )

    def test_idle_strategy_uses_background_convergence_history_as_cadence_pressure(self):
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        idle_strategy = decide_idle_strategy(
            run_id="idle-background-history",
            generated_at="2026-06-10T00:00:00+00:00",
            safe_terminal_loop={"current_mode": "restored_waiting_for_external_turn"},
            terminal_life_loop_state={"current_mode": "restored_waiting_for_external_turn"},
            idle_continuity_frame=None,
            relationship_timeline={},
            commitment_expression_plan={},
            apology_repair_language_trace={},
            body_rhythm_pulse={
                "schema_version": "body_rhythm_pulse_v0",
                "fatigue_load": "managed_low_noise",
            },
            need_state_vector={
                "schema_version": "need_state_vector_v0",
                "repair_drive": "inactive",
                "cognitive_bandwidth": "steady_open",
                "sleep_pressure": "low",
            },
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            responsibility_loop_state={},
            world_contact_summary={},
            pain_regret_repair_report={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "light",
                "background_carryover_attention_target": "relationship_timeline",
                "background_carryover_generation": 3,
                "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                "background_convergence_state": "stabilized_cross_process_continuity",
                "background_convergence_pressure_level": "light",
                "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                "background_convergence_history_trend_state": "recent_recalibration_pressure",
                "background_convergence_history_window_size": 3,
                "background_dominant_convergence_pressure_level": "elevated",
                "background_dominant_convergence_state": "recalibrating_cross_process_continuity",
                "background_trait_convergence_history_focus": "trait_recalibration_required",
                "background_trait_convergence_unstable_names": ["continuity_drive"],
                "background_trait_convergence_stable_names": ["repair_seriousness"],
                "background_trait_convergence_history_profile": {
                    "continuity_drive": {
                        "latest_band": "recalibrating",
                        "trend_state": "recent_trait_recalibration",
                    },
                    "repair_seriousness": {
                        "latest_band": "stabilized",
                        "trend_state": "stable_trait_convergence",
                    },
                },
            },
            source_doc_refs=[
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
            ],
            readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
            runtime_carrier_refs=["RunnerCliRuntime"],
        )

        self.assertEqual(idle_strategy["heartbeat_interval_ms"], 49)
        self.assertEqual(
            idle_strategy["next_idle_action"],
            "refresh_waiting_heartbeat_with_background_history_recalibration_hold",
        )
        self.assertEqual(
            idle_strategy["background_convergence_history_ref"],
            "runtime/state/terminal/background_convergence_history.json",
        )
        self.assertEqual(
            idle_strategy["governance_attention_target"],
            "background_convergence_history_recalibration",
        )
        self.assertEqual(
            idle_strategy["governance_attention_reason"],
            "recent_recalibration_pressure_requires_cross_wake_governance_hold",
        )
        self.assertEqual(
            idle_strategy["governance_cadence_profile"],
            "background_convergence_history_recalibration_refresh",
        )
        self.assertEqual(
            idle_strategy["background_trait_convergence_history_focus"],
            "trait_recalibration_required",
        )
        self.assertEqual(
            idle_strategy["background_trait_convergence_unstable_names"],
            ["continuity_drive"],
        )
        self.assertEqual(
            idle_strategy["background_trait_convergence_history_profile"][
                "continuity_drive"
            ]["trend_state"],
            "recent_trait_recalibration",
        )
        self.assertEqual(
            idle_strategy["cross_wake_trait_convergence_focus"],
            "trait_recalibration_required",
        )
        self.assertEqual(
            idle_strategy["cross_wake_trait_convergence_pressure"],
            "recalibration",
        )
        self.assertEqual(
            idle_strategy["cross_wake_trait_convergence_refs"],
            [
                "runtime/state/terminal/background_convergence_summary.json",
                "runtime/state/terminal/background_convergence_history.json",
            ],
        )
        self.assertEqual(
            idle_strategy["cross_wake_trait_convergence_profile"][
                "unstable_names"
            ],
            ["continuity_drive"],
        )
        self.assertEqual(
            idle_strategy["long_horizon_priority_profile"][
                "background_convergence_history_recalibration"
            ],
            "history_convergence_primary",
        )

    def test_background_continuity_profile_carries_resume_summary(self):
        from life_v0.process_supervisor.background_continuity import (
            load_background_continuity_profile,
        )

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            terminal_dir = runtime_root / "state" / "terminal"
            reports_dir = runtime_root / "reports" / "latest"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)
            self._write_json(
                terminal_dir / "resident_governance_state.json",
                {
                    "schema_version": "resident_governance_state_v0",
                    "run_id": "resume-summary-parent",
                    "governance_attention_target": "commitment_expression_plan",
                    "completed_dialogue_turns": 6,
                    "background_carryover_generation": 3,
                    "background_carryover_source_ref_set": [
                        "runtime/archive/resume-summary-parent/resident_governance_state.json"
                    ],
                    "background_lineage_depth_band": "deep_persistent_lineage",
                    "background_lineage_waiting_posture": "deep_background_residency_hold",
                    "background_lineage_cadence_weight": "deep",
                    "background_lineage_evidence_ref_count": 6,
                    "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json",
                    "state_merge_policy": "long_term_merge_fail_closed",
                    "state_merge_long_term_change_count": 4,
                    "state_merge_long_term_change_families": [
                        "offline_learning_cumulative_refs",
                        "queue_e_repair_modulation_refs",
                        "relationship_memory_offline_refs",
                    ],
                    "state_merge_long_term_change_refs": [
                        "runtime/state/growth/relationship_learning_plan.json",
                        "runtime/state/growth/language_learning_plan.json",
                        "runtime/state/action/responsibility_loop_state.json",
                        "runtime/state/dream/offline_consolidation_frame.json",
                    ],
                    "resident_background_lineage_state": {
                        "schema_version": "resident_background_lineage_state_v0",
                        "status": "closed",
                        "governance_phase": "process_closed_waiting_relaunch",
                        "continuity_mode": "closed_process_carryover",
                        "generation": 3,
                        "depth_band": "deep_persistent_lineage",
                        "waiting_posture": "deep_background_residency_hold",
                        "cadence_weight": "deep",
                        "evidence_ref_count": 6,
                        "attention_target": "commitment_expression_plan",
                        "cadence_profile": "deep_persistent_background_continuity_refresh",
                    },
                    "background_relationship_stage": "repair_guarded_continuity",
                    "background_relationship_stage_reason": "repair_followup_required_after_multi_turn_dialogue",
                    "background_relationship_subject_ref": "runtime/state/relationship/relationship_subject_graph.json#subjects[0]",
                    "background_self_model_ref": "runtime/state/self/self_model.json",
                    "trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                    "idle_heartbeat_trace_count": 7,
                    "background_trait_slow_variable_summary": {
                        "continuity_drive": {
                            "value": 0.74,
                            "trend": "up",
                            "last_relationship_stage": "repair_guarded_continuity",
                        }
                    },
                    "background_resume_summary": {
                        "relationship": {
                            "relationship_stage": "repair_guarded_continuity"
                        },
                        "trait_slow_variables": {
                            "continuity_drive": {"value": 0.74}
                        },
                    },
                    "offline_learning_cumulative_profile": {
                        "schema_version": "offline_learning_cumulative_profile_v0",
                        "generation": 2,
                        "pressure_level": "elevated",
                        "attention_target": "relationship_learning_plan",
                        "priority_profile": {
                            "relationship_learning_plan": "elevated",
                            "language_learning_plan": "baseline",
                        },
                        "ref_set": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                    },
                    "offline_learning_cumulative_generation": 2,
                    "offline_learning_cumulative_pressure_level": "elevated",
                    "offline_learning_cumulative_attention_target": "relationship_learning_plan",
                    "offline_learning_cumulative_priority_profile": {
                        "relationship_learning_plan": "elevated",
                        "language_learning_plan": "baseline",
                    },
                    "offline_learning_cumulative_ref_set": [
                        "runtime/state/growth/relationship_learning_plan.json",
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                    "live_language_turn_refs": [
                        "runtime/state/language/language_percept_frame.json",
                        "runtime/state/language/semantic_map_frame.json",
                        "runtime/state/language/inner_speech_frame.json",
                        "runtime/state/language/expression_monitor_state.json",
                        "runtime/state/language/expression_plan.json",
                    ],
                    "last_live_semantic_focus": "repair_commitment_shared_language",
                    "live_language_presence_profile": {
                        "schema_version": "live_language_presence_profile_v0",
                        "continuity_mode": "current_turn_language_presence",
                        "ref_count": 5,
                        "ref_set": [
                            "runtime/state/language/language_percept_frame.json",
                            "runtime/state/language/semantic_map_frame.json",
                            "runtime/state/language/inner_speech_frame.json",
                            "runtime/state/language/expression_monitor_state.json",
                            "runtime/state/language/expression_plan.json",
                        ],
                    },
                },
            )
            (terminal_dir / "idle_heartbeat_trace.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "idle_heartbeat_trace_event_v0",
                                "heartbeat_counter": counter,
                            },
                            ensure_ascii=False,
                        )
                        for counter in range(1, 8)
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            self._write_json(
                terminal_dir / "background_convergence_summary.json",
                {
                    "schema_version": "background_convergence_summary_v0",
                    "run_id": "resume-summary-parent",
                    "background_carryover_generation": 4,
                    "background_carryover_parent_run_id": "resume-summary-parent",
                    "background_carryover_source_ref_set": [
                        "runtime/archive/resume-summary-parent/background_convergence_summary.json"
                    ],
                    "convergence_state": "stabilized_cross_process_continuity",
                    "convergence_pressure_level": "present",
                    "convergence_attention_target": "trait_slow_variable_convergence",
                    "relationship_stage_continuity": "same_stage_preserved",
                    "trait_convergence_score": 0.96,
                    "max_trait_delta_from_background": 0.04,
                    "average_trait_delta_from_background": 0.03,
                    "trait_convergence_summary": {
                        "continuity_drive": {"convergence_band": "stabilized"}
                    },
                },
            )
            self._write_json(
                terminal_dir / "background_convergence_history.json",
                {
                    "schema_version": "background_convergence_history_v0",
                    "history_window_size": 2,
                    "trend_state": "integrating_cross_wake_convergence",
                    "dominant_convergence_state": "integrating_cross_process_continuity",
                    "dominant_convergence_pressure_level": "present",
                    "trait_convergence_history_profile": {
                        "continuity_drive": {
                            "sample_count": 2,
                            "latest_band": "integrating",
                            "dominant_band": "integrating",
                            "trend_state": "integrating_trait_convergence",
                        },
                        "repair_seriousness": {
                            "sample_count": 2,
                            "latest_band": "stabilized",
                            "dominant_band": "stabilized",
                            "trend_state": "stable_trait_convergence",
                        },
                    },
                    "trait_convergence_unstable_names": ["continuity_drive"],
                    "trait_convergence_stable_names": ["repair_seriousness"],
                    "trait_convergence_history_focus": "trait_stability_hold",
                    "convergence_samples": [
                        {
                            "run_id": "resume-summary-parent",
                            "background_carryover_generation": 4,
                            "convergence_state": "stabilized_cross_process_continuity",
                            "convergence_pressure_level": "present",
                            "trait_convergence_score": 0.96,
                        }
                    ],
                },
            )
            self._write_json(
                terminal_dir / "resident_governance_snapshot.json",
                {
                    "schema_version": "resident_governance_snapshot_v0",
                    "run_id": "resume-summary-parent",
                    "governance_attention_target": "commitment_expression_plan",
                    "completed_dialogue_turns": 5,
                    "background_carryover_generation": 2,
                    "background_relationship_stage": "repair_guarded_continuity",
                    "background_relationship_stage_reason": "repair_followup_required_after_multi_turn_dialogue",
                    "background_relationship_subject_ref": "runtime/state/relationship/relationship_subject_graph.json#subjects[0]",
                    "background_self_model_ref": "runtime/state/self/self_model.json",
                    "trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                    "background_trait_slow_variable_summary": {
                        "continuity_drive": {
                            "value": 0.73,
                            "trend": "up",
                            "last_relationship_stage": "repair_guarded_continuity",
                        }
                    },
                    "background_resume_summary": {
                        "relationship": {
                            "relationship_stage": "repair_guarded_continuity"
                        },
                        "trait_slow_variables": {
                            "continuity_drive": {"value": 0.73}
                        },
                    },
                },
            )
            self._write_json(
                reports_dir / "digital_life_resident_governance_explanation.json",
                {
                    "schema_version": "digital_life_resident_governance_explanation_v0",
                    "run_id": "resume-summary-parent",
                    "dominant_driver_family": "background_history_stability_hold",
                    "next_wake_expectation": "stabilize_cross_wake_convergence_history_before_accepting_external_turn",
                    "continuity_story": [
                        "dominant attention target is background_convergence_history_stability",
                        "background convergence history trend is integrating_cross_wake_convergence across 2 wake samples",
                    ],
                },
            )

            profile = load_background_continuity_profile(
                terminal_dir=terminal_dir,
                reports_dir=reports_dir,
            )

            self.assertEqual(profile["background_carryover_generation"], 4)
            self.assertEqual(
                profile["background_carryover_source_ref_set"],
                ["runtime/archive/resume-summary-parent/resident_governance_state.json"],
            )
            self.assertEqual(
                profile["resident_background_lineage_state"]["depth_band"],
                "deep_persistent_lineage",
            )
            self.assertEqual(
                profile["background_resident_lineage_state"]["governance_phase"],
                "process_closed_waiting_relaunch",
            )
            self.assertEqual(
                profile["background_resident_lineage_state"]["cadence_profile"],
                "deep_persistent_background_continuity_refresh",
            )
            self.assertEqual(profile["background_offline_learning_generation"], 2)
            self.assertEqual(
                profile["background_offline_learning_pressure_level"],
                "elevated",
            )
            self.assertEqual(
                profile["background_offline_learning_attention_target"],
                "relationship_learning_plan",
            )
            self.assertEqual(
                profile["background_offline_learning_priority_profile"][
                    "relationship_learning_plan"
                ],
                "elevated",
            )
            self.assertEqual(
                profile["background_offline_learning_ref_set"],
                [
                    "runtime/state/growth/relationship_learning_plan.json",
                    "runtime/state/growth/language_learning_plan.json",
                ],
            )
            self.assertEqual(
                profile["background_offline_learning_cumulative_profile"][
                    "pressure_level"
                ],
                "elevated",
            )
            self.assertEqual(
                profile["background_live_language_turn_refs"],
                [
                    "runtime/state/language/language_percept_frame.json",
                    "runtime/state/language/semantic_map_frame.json",
                    "runtime/state/language/inner_speech_frame.json",
                    "runtime/state/language/expression_monitor_state.json",
                    "runtime/state/language/expression_plan.json",
                ],
            )
            self.assertEqual(
                profile["background_last_live_semantic_focus"],
                "repair_commitment_shared_language",
            )
            self.assertEqual(
                profile["background_live_language_presence_profile"][
                    "continuity_mode"
                ],
                "closed_process_live_language_carryover",
            )
            self.assertEqual(
                profile["background_live_language_presence_profile"]["ref_count"],
                5,
            )
            expected_state_merge_change_families = [
                "offline_learning_cumulative_refs",
                "queue_e_repair_modulation_refs",
                "relationship_memory_offline_refs",
            ]
            expected_state_merge_change_refs = [
                "runtime/state/growth/relationship_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
                "runtime/state/action/responsibility_loop_state.json",
                "runtime/state/dream/offline_consolidation_frame.json",
            ]
            self.assertEqual(
                profile["background_state_merge_guard_ref"],
                "runtime/state/memory/state_merge_guard.json",
            )
            self.assertEqual(
                profile["background_state_merge_policy"],
                "long_term_merge_fail_closed",
            )
            self.assertEqual(
                profile["background_state_merge_long_term_change_count"],
                4,
            )
            self.assertEqual(
                profile["background_state_merge_long_term_change_families"],
                expected_state_merge_change_families,
            )
            self.assertEqual(
                profile["background_state_merge_long_term_change_refs"],
                expected_state_merge_change_refs,
            )
            self.assertIn(
                "runtime/state/terminal/resident_governance_state.json",
                profile["background_continuity_ref_set"],
            )
            self.assertIn(
                "runtime/state/memory/state_merge_guard.json",
                profile["background_continuity_ref_set"],
            )
            for ref in expected_state_merge_change_refs:
                self.assertIn(ref, profile["background_continuity_ref_set"])
            self.assertIn(
                "runtime/state/language/language_percept_frame.json",
                profile["background_continuity_ref_set"],
            )
            self.assertIn(
                "runtime/state/terminal/background_convergence_summary.json",
                profile["background_continuity_ref_set"],
            )
            self.assertIn(
                "runtime/state/terminal/background_convergence_history.json",
                profile["background_continuity_ref_set"],
            )
            self.assertIn(
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                profile["background_continuity_ref_set"],
            )
            self.assertIn(
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
                profile["background_continuity_ref_set"],
            )
            self.assertEqual(
                profile["background_idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(profile["background_idle_heartbeat_trace_count"], 7)
            self.assertEqual(
                profile["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )
            self.assertEqual(
                profile["background_resident_governance_explanation_ref"],
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
            )
            self.assertEqual(
                profile["background_governance_driver_family"],
                "background_history_stability_hold",
            )
            self.assertEqual(
                profile["background_next_wake_expectation"],
                "stabilize_cross_wake_convergence_history_before_accepting_external_turn",
            )
            self.assertEqual(
                profile["background_governance_explanation_story"],
                [
                    "dominant attention target is background_convergence_history_stability",
                    "background convergence history trend is integrating_cross_wake_convergence across 2 wake samples",
                ],
            )
            self.assertEqual(
                profile["background_convergence_history_ref"],
                "runtime/state/terminal/background_convergence_history.json",
            )
            self.assertEqual(
                profile["background_convergence_history_trend_state"],
                "integrating_cross_wake_convergence",
            )
            self.assertEqual(profile["background_convergence_history_window_size"], 2)
            self.assertEqual(
                profile["background_dominant_convergence_pressure_level"],
                "present",
            )
            self.assertEqual(
                profile["background_trait_convergence_history_focus"],
                "trait_stability_hold",
            )
            self.assertEqual(
                profile["background_trait_convergence_unstable_names"],
                ["continuity_drive"],
            )
            self.assertEqual(
                profile["background_trait_convergence_stable_names"],
                ["repair_seriousness"],
            )
            self.assertEqual(
                profile["background_trait_convergence_history_profile"][
                    "continuity_drive"
                ]["trend_state"],
                "integrating_trait_convergence",
            )
            self.assertEqual(
                profile["background_convergence_state"],
                "stabilized_cross_process_continuity",
            )
            self.assertEqual(
                profile["background_convergence_pressure_level"],
                "present",
            )
            self.assertEqual(
                profile["background_relationship_stage"],
                "repair_guarded_continuity",
            )
            self.assertEqual(
                profile["background_relationship_subject_ref"],
                "runtime/state/relationship/relationship_subject_graph.json#subjects[0]",
            )
            self.assertEqual(
                profile["background_self_model_ref"],
                "runtime/state/self/self_model.json",
            )
            self.assertEqual(
                profile["background_resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                profile["background_trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(
                profile["background_trait_slow_variable_summary"]["continuity_drive"][
                    "value"
                ],
                0.74,
            )
            self.assertEqual(
                profile["background_resume_summary"]["relationship"][
                    "relationship_stage"
                ],
                "repair_guarded_continuity",
            )

    def test_background_continuity_profile_restores_trait_drift_update_mode_history(self):
        from life_v0.process_supervisor.background_continuity import (
            load_background_continuity_profile,
        )

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            terminal_dir = runtime_root / "state" / "terminal"
            reports_dir = runtime_root / "reports" / "latest"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)
            self._write_json(
                terminal_dir / "background_convergence_history.json",
                {
                    "schema_version": "background_convergence_history_v0",
                    "history_window_size": 2,
                    "trend_state": "recent_recalibration_pressure",
                    "trait_drift_update_mode_summary": {
                        "background_history_recalibration": ["continuity_drive"],
                        "background_history_stabilized": ["repair_seriousness"],
                    },
                    "trait_drift_background_history_recalibration_names": [
                        "continuity_drive"
                    ],
                    "trait_drift_background_history_stabilized_names": [
                        "repair_seriousness"
                    ],
                    "trait_convergence_history_profile": {
                        "continuity_drive": {
                            "sample_count": 2,
                            "latest_band": "recalibrating",
                            "dominant_band": "recalibrating",
                            "trend_state": "recent_trait_recalibration",
                            "trait_drift_update_mode_sequence": [
                                "background_history_stabilized",
                                "background_history_recalibration",
                            ],
                            "latest_trait_drift_update_mode": "background_history_recalibration",
                            "dominant_trait_drift_update_mode": "background_history_recalibration",
                        }
                    },
                    "convergence_samples": [
                        {
                            "run_id": "trait-drift-history-parent",
                            "background_carryover_generation": 3,
                            "convergence_state": "recalibrating_cross_process_continuity",
                            "convergence_pressure_level": "elevated",
                            "trait_convergence_score": 0.62,
                        }
                    ],
                },
            )

            profile = load_background_continuity_profile(
                terminal_dir=terminal_dir,
                reports_dir=reports_dir,
            )

            self.assertEqual(
                profile["background_trait_drift_update_mode_summary"][
                    "background_history_recalibration"
                ],
                ["continuity_drive"],
            )
            self.assertEqual(
                profile["background_trait_drift_recalibration_names"],
                ["continuity_drive"],
            )
            self.assertEqual(
                profile["background_trait_drift_stabilized_names"],
                ["repair_seriousness"],
            )
            self.assertEqual(
                profile["background_trait_convergence_history_profile"][
                    "continuity_drive"
                ]["latest_trait_drift_update_mode"],
                "background_history_recalibration",
            )
            self.assertEqual(
                profile["background_trait_convergence_history_profile"][
                    "continuity_drive"
                ]["dominant_trait_drift_update_mode"],
                "background_history_recalibration",
            )

    def test_waiting_heartbeat_carries_trait_drift_update_mode_history(self):
        from life_v0.process_supervisor.heartbeat import write_waiting_heartbeat

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            terminal_dir = runtime_root / "state" / "terminal"
            reports_dir = runtime_root / "reports" / "latest"
            language_dir = runtime_root / "state" / "language"
            relationship_dir = runtime_root / "state" / "relationship"
            for directory in (
                terminal_dir,
                reports_dir,
                language_dir,
                relationship_dir,
            ):
                directory.mkdir(parents=True, exist_ok=True)
            self._write_json(
                terminal_dir / "background_convergence_history.json",
                {
                    "schema_version": "background_convergence_history_v0",
                    "history_window_size": 2,
                    "trend_state": "recent_recalibration_pressure",
                    "trait_drift_update_mode_summary": {
                        "background_history_recalibration": ["continuity_drive"],
                        "background_history_stabilized": ["repair_seriousness"],
                    },
                    "trait_drift_background_history_recalibration_names": [
                        "continuity_drive"
                    ],
                    "trait_drift_background_history_stabilized_names": [
                        "repair_seriousness"
                    ],
                    "trait_convergence_history_profile": {
                        "continuity_drive": {
                            "sample_count": 2,
                            "latest_band": "recalibrating",
                            "dominant_band": "recalibrating",
                            "trend_state": "recent_trait_recalibration",
                            "trait_drift_update_mode_sequence": [
                                "background_history_stabilized",
                                "background_history_recalibration",
                            ],
                            "latest_trait_drift_update_mode": "background_history_recalibration",
                            "dominant_trait_drift_update_mode": "background_history_recalibration",
                        }
                    },
                    "convergence_samples": [
                        {
                            "run_id": "trait-drift-history-parent",
                            "background_carryover_generation": 2,
                            "convergence_state": "recalibrating_cross_process_continuity",
                            "convergence_pressure_level": "elevated",
                            "trait_convergence_score": 0.62,
                        }
                    ],
                },
            )

            write_waiting_heartbeat(
                run_id="trait-drift-waiting-carry",
                generated_at="2026-06-10T00:00:00+00:00",
                terminal_dir=terminal_dir,
                reports_dir=reports_dir,
                language_dir=language_dir,
                relationship_dir=relationship_dir,
                safe_terminal_loop={
                    "current_mode": "restored_waiting_for_external_turn",
                    "heartbeat_counter": 0,
                },
                terminal_life_loop_state={
                    "current_mode": "restored_waiting_for_external_turn"
                },
                relationship_timeline={},
                commitment_expression_plan={},
                apology_repair_language_trace={},
                body_rhythm_pulse={
                    "schema_version": "body_rhythm_pulse_v0",
                    "fatigue_load": "managed_low_noise",
                },
                need_state_vector={
                    "schema_version": "need_state_vector_v0",
                    "repair_drive": "inactive",
                    "cognitive_bandwidth": "steady_open",
                    "sleep_pressure": "low",
                },
                self_narrative_trace={},
                commitment_index={},
                relationship_graph={"subjects": [{"subject_id": "friend"}]},
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
                write_json=self._write_json,
            )

            idle_strategy = self._read_json(terminal_dir / "idle_strategy_state.json")
            resident_governance_state = self._read_json(
                terminal_dir / "resident_governance_state.json"
            )
            idle_continuity = self._read_json(
                terminal_dir / "idle_continuity_frame.json"
            )
            terminal_life_loop_state = self._read_json(
                terminal_dir / "terminal_life_loop_state.json"
            )
            heartbeat_trace_event = json.loads(
                (terminal_dir / "idle_heartbeat_trace.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()[0]
            )
            expected_update_mode_summary = {
                "background_history_recalibration": ["continuity_drive"],
                "background_history_stabilized": ["repair_seriousness"],
            }
            self.assertEqual(
                idle_strategy["background_trait_drift_update_mode_summary"],
                expected_update_mode_summary,
            )
            self.assertEqual(
                idle_strategy["cross_wake_trait_convergence_profile"][
                    "trait_drift_update_mode_summary"
                ],
                expected_update_mode_summary,
            )
            self.assertEqual(
                idle_strategy["cross_wake_trait_convergence_profile"][
                    "trait_drift_recalibration_names"
                ],
                ["continuity_drive"],
            )
            self.assertEqual(
                idle_strategy["cross_wake_trait_convergence_profile"][
                    "trait_drift_stabilized_names"
                ],
                ["repair_seriousness"],
            )
            lineage_trait_presence = resident_governance_state[
                "resident_background_lineage_state"
            ]["trait_convergence_presence"]
            self.assertEqual(
                lineage_trait_presence["trait_drift_update_mode_summary"],
                expected_update_mode_summary,
            )
            self.assertEqual(
                lineage_trait_presence["trait_drift_recalibration_names"],
                ["continuity_drive"],
            )
            self.assertEqual(
                lineage_trait_presence["trait_drift_stabilized_names"],
                ["repair_seriousness"],
            )
            self.assertEqual(
                terminal_life_loop_state["resident_background_lineage_state"][
                    "trait_convergence_presence"
                ]["trait_drift_update_mode_summary"],
                expected_update_mode_summary,
            )
            for artifact in (
                resident_governance_state,
                idle_continuity,
                terminal_life_loop_state,
                heartbeat_trace_event,
            ):
                self.assertEqual(
                    artifact["background_trait_drift_update_mode_summary"],
                    expected_update_mode_summary,
                )
                self.assertEqual(
                    artifact["background_trait_drift_recalibration_names"],
                    ["continuity_drive"],
                )
                self.assertEqual(
                    artifact["background_trait_drift_stabilized_names"],
                    ["repair_seriousness"],
                )

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
            self.assertEqual(
                context.nightmare_risk_ref,
                "runtime/state/dream/nightmare_loop_risk.json",
            )
            self.assertEqual(
                context.belief_learning_plan_ref,
                "runtime/state/growth/belief_learning_plan.json",
            )
            self.assertEqual(
                context.language_learning_plan_ref,
                "runtime/state/growth/language_learning_plan.json",
            )
            self.assertEqual(
                context.relationship_learning_plan_ref,
                "runtime/state/growth/relationship_learning_plan.json",
            )
            self.assertTrue(context.growth_patch_candidate_ids)
            self.assertGreater(context.replay_residue_ref_count, 0)
            self.assertGreater(context.dream_window_ref_count, 0)
            self.assertGreater(context.growth_patch_candidate_count, 0)
            self.assertEqual(heartbeat_packet["heartbeat_counter"], 1)
            self.assertEqual(
                heartbeat_packet["nightmare_risk_ref"],
                "runtime/state/dream/nightmare_loop_risk.json",
            )
            self.assertEqual(
                heartbeat_packet["belief_learning_plan_ref"],
                "runtime/state/growth/belief_learning_plan.json",
            )
            self.assertEqual(
                heartbeat_packet["language_learning_plan_ref"],
                "runtime/state/growth/language_learning_plan.json",
            )
            self.assertEqual(
                heartbeat_packet["relationship_learning_plan_ref"],
                "runtime/state/growth/relationship_learning_plan.json",
            )
            self.assertNotEqual(
                heartbeat_packet["offline_learning_pressure_level"],
                "quiet",
            )
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

    def test_resident_supervision_reloads_background_continuity_from_previous_process_closeout(self):
        from life_v0.process_supervisor.resident_supervision import (
            bootstrap_resident_supervision,
        )

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
                    "background-carryover-seed",
                    "--strict",
                ],
                cwd=self.repo_root,
                text=True,
                input="/exit\n",
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

            result = bootstrap_resident_supervision(
                state_dir=paths["state_root"],
                reports_dir=paths["reports"],
                receipts_dir=paths["receipts"],
                run_id="background-carryover-relaunch",
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
            idle_strategy = self._read_json(paths["terminal_state"] / "idle_strategy_state.json")
            resident_governance_state = self._read_json(
                paths["terminal_state"] / "resident_governance_state.json"
            )
            idle_continuity = self._read_json(paths["terminal_state"] / "idle_continuity_frame.json")
            terminal_life_loop_state = self._read_json(
                paths["terminal_state"] / "terminal_life_loop_state.json"
            )
            background_convergence_summary = self._read_json(
                paths["terminal_state"] / "background_convergence_summary.json"
            )
            background_convergence_history = self._read_json(
                paths["terminal_state"] / "background_convergence_history.json"
            )

            self.assertEqual(idle_strategy["background_continuity_mode"], "closed_process_carryover")
            self.assertEqual(idle_strategy["background_carryover_generation"], 1)
            self.assertEqual(
                idle_strategy["background_carryover_parent_run_id"],
                "background-carryover-seed",
            )
            self.assertEqual(
                idle_strategy["background_resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                idle_strategy["background_resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(
                idle_strategy["background_resident_governance_report_ref"],
                "runtime/reports/latest/digital_life_resident_governance_report.json",
            )
            self.assertEqual(
                idle_strategy["background_resident_governance_explanation_ref"],
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
            )
            self.assertIn(
                idle_strategy["background_governance_driver_family"],
                {
                    "background_history_recalibration_hold",
                    "background_history_stability_hold",
                    "background_trait_convergence_hold",
                    "background_convergence_recalibration",
                    "queue_e_repair_guard",
                    "replay_growth_reconsolidation",
                    "long_horizon_language_continuity",
                    "baseline_waiting_presence",
                },
            )
            self.assertIn(
                "background_next_wake_expectation",
                idle_strategy,
            )
            self.assertEqual(
                idle_strategy["background_trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(
                idle_strategy["background_idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertGreaterEqual(
                idle_strategy["background_idle_heartbeat_trace_count"],
                1,
            )
            self.assertEqual(
                idle_strategy["background_state_merge_guard_ref"],
                "runtime/state/memory/state_merge_guard.json",
            )
            self.assertEqual(
                idle_strategy["background_state_merge_policy"],
                "long_term_merge_fail_closed",
            )
            self.assertGreater(
                idle_strategy["background_state_merge_long_term_change_count"],
                0,
            )
            self.assertTrue(
                idle_strategy["background_state_merge_long_term_change_families"],
            )
            self.assertTrue(
                idle_strategy["background_state_merge_long_term_change_refs"],
            )
            self.assertIn(
                "runtime/state/memory/state_merge_guard.json",
                idle_strategy["background_continuity_ref_set"],
            )
            for ref in idle_strategy["background_state_merge_long_term_change_refs"]:
                self.assertIn(ref, idle_strategy["background_continuity_ref_set"])
            self.assertEqual(
                idle_strategy["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )
            self.assertEqual(
                idle_strategy["background_convergence_history_ref"],
                "runtime/state/terminal/background_convergence_history.json",
            )
            self.assertIn(
                idle_strategy["background_convergence_history_trend_state"],
                {
                    "stable_cross_wake_convergence",
                    "integrating_cross_wake_convergence",
                    "cross_wake_convergence_observed",
                    "recent_recalibration_pressure",
                    "elevated_pressure_watch",
                },
            )
            self.assertIn(
                idle_strategy["background_trait_convergence_history_focus"],
                {
                    "trait_convergence_stable",
                    "trait_stability_hold",
                    "trait_recalibration_required",
                },
            )
            self.assertTrue(
                idle_strategy["background_trait_convergence_history_profile"],
            )
            self.assertIn(
                idle_strategy["background_convergence_state"],
                {
                    "stabilized_cross_process_continuity",
                    "integrating_cross_process_continuity",
                    "recalibrating_cross_process_continuity",
                },
            )
            self.assertEqual(
                resident_governance_state["background_continuity_mode"],
                "closed_process_carryover",
            )
            self.assertTrue(
                resident_governance_state["background_continuity_ref_set"],
            )
            self.assertIn(
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
                resident_governance_state["background_continuity_ref_set"],
            )
            self.assertEqual(
                resident_governance_state["background_resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                resident_governance_state["background_resident_governance_explanation_ref"],
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
            )
            self.assertEqual(
                resident_governance_state["background_next_wake_expectation"],
                idle_strategy["background_next_wake_expectation"],
            )
            self.assertEqual(
                resident_governance_state["background_trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(
                resident_governance_state["background_idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(
                resident_governance_state["background_idle_heartbeat_trace_count"],
                idle_strategy["background_idle_heartbeat_trace_count"],
            )
            self.assertEqual(
                resident_governance_state["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )
            self.assertEqual(
                resident_governance_state["background_convergence_history_ref"],
                "runtime/state/terminal/background_convergence_history.json",
            )
            self.assertEqual(
                resident_governance_state["background_trait_convergence_history_focus"],
                idle_strategy["background_trait_convergence_history_focus"],
            )
            self.assertEqual(
                resident_governance_state["background_trait_convergence_unstable_names"],
                idle_strategy["background_trait_convergence_unstable_names"],
            )
            self.assertEqual(
                resident_governance_state["background_lineage_depth_band"],
                "single_carryover",
            )
            self.assertEqual(
                resident_governance_state["resident_background_lineage_state"][
                    "schema_version"
                ],
                "resident_background_lineage_state_v0",
            )
            self.assertEqual(
                resident_governance_state["resident_background_lineage_state"][
                    "governance_phase"
                ],
                "waiting_heartbeat_active",
            )
            self.assertEqual(
                resident_governance_state["resident_background_lineage_state"][
                    "depth_band"
                ],
                "single_carryover",
            )
            self.assertEqual(
                resident_governance_state["resident_background_lineage_state"][
                    "cadence_profile"
                ],
                idle_strategy["governance_cadence_profile"],
            )
            lineage_state = resident_governance_state[
                "resident_background_lineage_state"
            ]
            self.assertEqual(
                lineage_state["relationship_presence"]["relationship_stage"],
                resident_governance_state["background_relationship_stage"],
            )
            self.assertIn(
                "continuity_drive",
                lineage_state["trait_convergence_presence"][
                    "trait_slow_variable_summary"
                ],
            )
            self.assertEqual(
                lineage_state["trait_convergence_presence"][
                    "trait_convergence_evidence_refs"
                ],
                [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                    "runtime/state/body/trait_drift_monitor.json",
                    "runtime/state/terminal/background_convergence_summary.json",
                    "runtime/state/terminal/background_convergence_history.json",
                ],
            )
            self.assertEqual(
                lineage_state["heartbeat_presence"][
                    "background_idle_heartbeat_trace_ref"
                ],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(
                lineage_state["state_merge_presence"]["state_merge_guard_ref"],
                "runtime/state/memory/state_merge_guard.json",
            )
            self.assertEqual(
                lineage_state["state_merge_presence"]["state_merge_policy"],
                "long_term_merge_fail_closed",
            )
            self.assertGreater(
                lineage_state["state_merge_presence"][
                    "long_term_change_count"
                ],
                0,
            )
            self.assertTrue(
                lineage_state["state_merge_presence"][
                    "long_term_change_families"
                ],
            )
            self.assertTrue(
                lineage_state["state_merge_presence"]["long_term_change_refs"],
            )
            self.assertIn(
                "runtime/state/memory/state_merge_guard.json",
                lineage_state["state_merge_presence"]["state_merge_evidence_refs"],
            )
            self.assertIn(
                "runtime/state/relationship/relationship_timeline.json",
                lineage_state["language_presence"]["long_horizon_language_refs"],
            )
            self.assertEqual(
                lineage_state["dream_wake_presence"]["dream_window_ref"],
                "runtime/state/dream/dream_experience_window.json",
            )
            self.assertEqual(
                lineage_state["dream_wake_presence"]["wake_integration_ref"],
                "runtime/state/dream/wake_integration_frame.json",
            )
            self.assertEqual(
                lineage_state["dream_wake_presence"][
                    "dream_fact_gate_decision_ref"
                ],
                "runtime/state/dream/dream_fact_gate_decision.json",
            )
            self.assertEqual(
                lineage_state["dream_wake_presence"]["dream_window_kind"],
                "micro_dream",
            )
            self.assertEqual(
                lineage_state["dream_wake_presence"]["dream_fact_gate_result"],
                "passed",
            )
            self.assertGreater(
                lineage_state["dream_wake_presence"]["wake_growth_seed_count"],
                0,
            )
            self.assertEqual(
                idle_continuity["background_continuity_mode"],
                "closed_process_carryover",
            )
            self.assertEqual(idle_continuity["background_carryover_generation"], 1)
            self.assertEqual(
                idle_continuity["background_carryover_parent_run_id"],
                "background-carryover-seed",
            )
            self.assertEqual(
                idle_continuity["background_resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                idle_continuity["background_resident_governance_explanation_ref"],
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
            )
            self.assertEqual(
                idle_continuity["background_next_wake_expectation"],
                idle_strategy["background_next_wake_expectation"],
            )
            self.assertEqual(
                idle_continuity["background_trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(
                idle_continuity["background_idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(
                idle_continuity["background_idle_heartbeat_trace_count"],
                idle_strategy["background_idle_heartbeat_trace_count"],
            )
            self.assertEqual(
                idle_continuity["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )
            self.assertEqual(
                idle_continuity["background_convergence_history_ref"],
                "runtime/state/terminal/background_convergence_history.json",
            )
            self.assertEqual(
                idle_continuity["background_trait_convergence_history_focus"],
                idle_strategy["background_trait_convergence_history_focus"],
            )
            self.assertEqual(
                idle_continuity["background_trait_convergence_stable_names"],
                idle_strategy["background_trait_convergence_stable_names"],
            )
            self.assertEqual(
                terminal_life_loop_state["background_resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                terminal_life_loop_state["background_resident_governance_explanation_ref"],
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
            )
            self.assertEqual(
                terminal_life_loop_state["background_next_wake_expectation"],
                idle_strategy["background_next_wake_expectation"],
            )
            self.assertEqual(
                terminal_life_loop_state["background_trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(
                terminal_life_loop_state["background_idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(
                terminal_life_loop_state["background_idle_heartbeat_trace_count"],
                idle_strategy["background_idle_heartbeat_trace_count"],
            )
            self.assertEqual(
                terminal_life_loop_state["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )
            self.assertEqual(
                terminal_life_loop_state["background_convergence_history_ref"],
                "runtime/state/terminal/background_convergence_history.json",
            )
            self.assertEqual(
                terminal_life_loop_state["background_trait_convergence_history_focus"],
                idle_strategy["background_trait_convergence_history_focus"],
            )
            self.assertEqual(
                terminal_life_loop_state["background_trait_convergence_history_profile"],
                idle_strategy["background_trait_convergence_history_profile"],
            )
            self.assertEqual(
                terminal_life_loop_state["resident_background_lineage_state"][
                    "depth_band"
                ],
                "single_carryover",
            )
            for artifact in (
                resident_governance_state,
                idle_continuity,
                terminal_life_loop_state,
            ):
                self.assertEqual(
                    artifact["background_state_merge_guard_ref"],
                    idle_strategy["background_state_merge_guard_ref"],
                )
                self.assertEqual(
                    artifact["background_state_merge_policy"],
                    idle_strategy["background_state_merge_policy"],
                )
                self.assertEqual(
                    artifact["background_state_merge_long_term_change_count"],
                    idle_strategy[
                        "background_state_merge_long_term_change_count"
                    ],
                )
                self.assertEqual(
                    artifact["background_state_merge_long_term_change_families"],
                    idle_strategy[
                        "background_state_merge_long_term_change_families"
                    ],
                )
                self.assertEqual(
                    artifact["background_state_merge_long_term_change_refs"],
                    idle_strategy["background_state_merge_long_term_change_refs"],
                )
            self.assertEqual(
                background_convergence_summary["schema_version"],
                "background_convergence_summary_v0",
            )
            self.assertEqual(
                background_convergence_summary["background_carryover_generation"],
                1,
            )
            self.assertIn(
                "trait_convergence_summary",
                background_convergence_summary,
            )
            self.assertEqual(
                background_convergence_history["schema_version"],
                "background_convergence_history_v0",
            )
            self.assertEqual(background_convergence_history["history_window_size"], 1)
            self.assertTrue(
                background_convergence_history["trait_convergence_history_profile"],
            )
            self.assertIn(
                background_convergence_history["trait_convergence_history_focus"],
                {
                    "trait_convergence_stable",
                    "trait_stability_hold",
                    "trait_recalibration_required",
                },
            )
            self.assertEqual(
                background_convergence_history["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )

    def test_continuity_evolution_projects_background_lineage_into_stage_and_slow_variables(self):
        from life_v0.process_supervisor.continuity_evolution import (
            evolve_relationship_and_self_model,
        )

        baseline = evolve_relationship_and_self_model(
            generated_at="2026-06-10T00:00:00+00:00",
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relation_role": "friend",
                        "relationship_stage": "restored_waiting",
                    }
                ]
            },
            self_model_state={"trait_slow_variables": {}, "growth_window_refs": []},
            relationship_timeline={
                "dialogue_turn_refs": ["runtime/state/language/dialogue_turn_log.jsonl#line-1"],
                "relationship_continuity_reports": [
                    {"continuity_state": "active_repairing_continuity"}
                ],
                "trust_trajectories": [{"current_trust_state": "calibrated_medium"}],
            },
            commitment_expression_plan={},
            apology_repair_language_trace={},
        )
        projected = evolve_relationship_and_self_model(
            generated_at="2026-06-10T00:00:00+00:00",
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relation_role": "friend",
                        "relationship_stage": "restored_waiting",
                    }
                ]
            },
            self_model_state={"trait_slow_variables": {}, "growth_window_refs": []},
            relationship_timeline={
                "dialogue_turn_refs": ["runtime/state/language/dialogue_turn_log.jsonl#line-1"],
                "relationship_continuity_reports": [
                    {"continuity_state": "active_repairing_continuity"}
                ],
                "trust_trajectories": [{"current_trust_state": "calibrated_medium"}],
            },
            commitment_expression_plan={},
            apology_repair_language_trace={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "elevated",
                "background_carryover_generation": 3,
                "background_continuity_ref_set": [
                    "runtime/state/terminal/resident_governance_snapshot.json",
                    "runtime/reports/latest/digital_life_resident_governance_report.json",
                ],
                "background_carryover_source_ref_set": [
                    "runtime/archive/process/background-lineage-parent.json"
                ],
            },
        )

        baseline_subject = baseline["relationship_graph"]["subjects"][0]
        projected_subject = projected["relationship_graph"]["subjects"][0]
        self.assertEqual(baseline_subject["relationship_stage"], "restored_waiting")
        self.assertEqual(
            projected_subject["relationship_stage"],
            "background_continuity_waiting",
        )
        self.assertEqual(
            projected_subject["relationship_stage_reason"],
            "persistent_background_continuity_lineage_preserved_before_dialogue",
        )
        self.assertIn(
            "runtime/state/terminal/resident_governance_snapshot.json",
            projected_subject["relationship_stage_evidence_refs"],
        )
        self.assertGreater(
            projected["self_model_state"]["trait_slow_variables"]["continuity_drive"]["value"],
            baseline["self_model_state"]["trait_slow_variables"]["continuity_drive"]["value"],
        )
        self.assertIn(
            "runtime/reports/latest/digital_life_resident_governance_report.json",
            projected["self_model_state"]["trait_slow_variables"]["continuity_drive"]["evidence_refs"],
        )
        self.assertIn(
            "runtime/archive/process/background-lineage-parent.json",
            projected["self_model_state"]["growth_window_refs"],
        )

    def test_continuity_evolution_uses_background_resume_as_trait_inertia(self):
        from life_v0.process_supervisor.continuity_evolution import (
            evolve_relationship_and_self_model,
        )

        result = evolve_relationship_and_self_model(
            generated_at="2026-06-10T00:00:00+00:00",
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relation_role": "friend",
                        "relationship_stage": "restored_waiting",
                    }
                ]
            },
            self_model_state={"trait_slow_variables": {}, "growth_window_refs": []},
            relationship_timeline={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ],
                "relationship_continuity_reports": [],
                "trust_trajectories": [],
            },
            commitment_expression_plan={},
            apology_repair_language_trace={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "present",
                "background_carryover_generation": 1,
                "background_relationship_stage": "repair_guarded_continuity",
                "background_relationship_stage_reason": "repair_followup_required_after_multi_turn_dialogue",
                "background_relationship_subject_ref": "runtime/state/relationship/relationship_subject_graph.json#subjects[0]",
                "background_relationship_stage_evidence_refs": [
                    "runtime/state/relationship/relationship_timeline.json"
                ],
                "background_self_model_ref": "runtime/state/self/self_model.json",
                "background_trait_slow_variable_summary": {
                    "continuity_drive": {
                        "value": 0.82,
                        "trend": "up",
                        "update_count": 7,
                        "last_relationship_stage": "repair_guarded_continuity",
                    }
                },
            },
        )

        subject = result["relationship_graph"]["subjects"][0]
        self.assertEqual(subject["relationship_stage"], "repair_guarded_continuity")
        self.assertEqual(
            subject["relationship_stage_reason"],
            "repair_followup_required_after_multi_turn_dialogue",
        )
        self.assertIn(
            "runtime/state/relationship/relationship_subject_graph.json#subjects[0]",
            subject["relationship_stage_evidence_refs"],
        )

        continuity_drive = result["self_model_state"]["trait_slow_variables"][
            "continuity_drive"
        ]
        self.assertGreater(continuity_drive["value"], 0.5)
        self.assertEqual(continuity_drive["background_resume_value"], 0.82)
        self.assertGreater(continuity_drive["background_inertia_weight"], 0.4)
        self.assertEqual(continuity_drive["update_count"], 8)
        self.assertIn(
            "runtime/state/self/self_model.json",
            continuity_drive["evidence_refs"],
        )

    def test_continuity_evolution_uses_background_trait_history_as_slow_variable_update_mode(self):
        from life_v0.process_supervisor.continuity_evolution import (
            evolve_relationship_and_self_model,
        )

        result = evolve_relationship_and_self_model(
            generated_at="2026-06-10T00:00:00+00:00",
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relation_role": "friend",
                        "relationship_stage": "restored_waiting",
                    }
                ]
            },
            self_model_state={"trait_slow_variables": {}, "growth_window_refs": []},
            relationship_timeline={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ],
                "relationship_continuity_reports": [],
                "trust_trajectories": [],
            },
            commitment_expression_plan={},
            apology_repair_language_trace={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "elevated",
                "background_carryover_generation": 3,
                "background_relationship_stage": "repair_guarded_continuity",
                "background_self_model_ref": "runtime/state/self/self_model.json",
                "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                "background_trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                "background_trait_convergence_history_focus": "trait_recalibration_required",
                "background_trait_convergence_unstable_names": ["continuity_drive"],
                "background_trait_convergence_stable_names": ["repair_seriousness"],
                "background_trait_convergence_history_profile": {
                    "continuity_drive": {
                        "latest_band": "recalibrating",
                        "trend_state": "recent_trait_recalibration",
                    },
                    "repair_seriousness": {
                        "latest_band": "stabilized",
                        "trend_state": "stable_trait_convergence",
                    },
                },
            },
        )

        variables = result["self_model_state"]["trait_slow_variables"]
        continuity_drive = variables["continuity_drive"]
        repair_seriousness = variables["repair_seriousness"]
        self.assertEqual(
            continuity_drive["slow_variable_update_mode"],
            "background_history_recalibration",
        )
        self.assertEqual(
            continuity_drive["background_trait_convergence_history_focus"],
            "trait_recalibration_required",
        )
        self.assertEqual(
            continuity_drive["background_trait_convergence_history_role"],
            "unstable",
        )
        self.assertEqual(
            continuity_drive["background_trait_convergence_history_trend_state"],
            "recent_trait_recalibration",
        )
        self.assertEqual(
            repair_seriousness["slow_variable_update_mode"],
            "background_history_stabilized",
        )
        self.assertEqual(
            repair_seriousness["background_trait_convergence_history_role"],
            "stable",
        )
        self.assertIn(
            "runtime/state/terminal/background_convergence_history.json",
            continuity_drive["evidence_refs"],
        )
        self.assertIn(
            "runtime/state/body/trait_drift_monitor.json",
            repair_seriousness["evidence_refs"],
        )

    def test_continuity_evolution_uses_background_offline_learning_as_relationship_reconsolidation(self):
        from life_v0.process_supervisor.continuity_evolution import (
            evolve_relationship_and_self_model,
        )

        result = evolve_relationship_and_self_model(
            generated_at="2026-06-10T00:00:00+00:00",
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relation_role": "friend",
                        "relationship_stage": "restored_waiting",
                    }
                ]
            },
            self_model_state={"trait_slow_variables": {}, "growth_window_refs": []},
            relationship_timeline={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ],
                "relationship_continuity_reports": [],
                "trust_trajectories": [],
            },
            commitment_expression_plan={},
            apology_repair_language_trace={},
            background_continuity_profile={
                "background_continuity_mode": "closed_process_carryover",
                "background_offline_learning_generation": 4,
                "background_offline_learning_pressure_level": "elevated",
                "background_offline_learning_attention_target": "relationship_learning_plan",
                "background_offline_learning_priority_profile": {
                    "relationship_learning_plan": "elevated",
                    "language_learning_plan": "present",
                },
                "background_offline_learning_ref_set": [
                    "runtime/state/growth/relationship_learning_plan.json",
                    "runtime/state/growth/language_learning_plan.json",
                ],
            },
        )

        subject = result["relationship_graph"]["subjects"][0]
        self.assertEqual(
            subject["relationship_stage"],
            "offline_learning_reconsolidation_waiting",
        )
        self.assertEqual(
            subject["relationship_stage_reason"],
            "background_cumulative_offline_learning_requires_relationship_reconsolidation",
        )
        self.assertIn(
            "runtime/state/growth/relationship_learning_plan.json",
            subject["relationship_stage_evidence_refs"],
        )

        continuity_drive = result["self_model_state"]["trait_slow_variables"][
            "continuity_drive"
        ]
        self.assertEqual(
            continuity_drive["last_relationship_stage"],
            "offline_learning_reconsolidation_waiting",
        )
        self.assertEqual(
            continuity_drive["background_offline_learning_generation"],
            4,
        )
        self.assertEqual(
            continuity_drive["background_offline_learning_attention_target"],
            "relationship_learning_plan",
        )
        self.assertIn(
            "runtime/state/growth/language_learning_plan.json",
            continuity_drive["evidence_refs"],
        )
        self.assertIn(
            "runtime/state/growth/relationship_learning_plan.json",
            result["self_model_state"]["growth_window_refs"],
        )

    def test_resident_supervision_projects_background_lineage_into_bootstrap_relationship_state(self):
        from life_v0.process_supervisor.resident_supervision import (
            bootstrap_resident_supervision,
        )
        from life_v0.shell_command import DigitalLifeShellResult

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            self._bootstrap(paths)

            (paths["language_state"] / "dialogue_turn_log.jsonl").write_text(
                "",
                encoding="utf-8",
            )
            self._write_json(
                paths["relationship_state"] / "relationship_subject_graph.json",
                {
                    "subjects": [
                        {
                            "relationship_id": "rel-v0-0001",
                            "relation_role": "friend",
                            "relationship_stage": "restored_waiting",
                        }
                    ]
                },
            )
            self._write_json(
                paths["terminal_state"] / "session_envelope.json",
                {
                    "schema_version": "session_envelope_v0",
                    "run_id": "background-lineage-relaunch",
                    "status": "closed",
                },
            )
            self._write_json(
                paths["terminal_state"] / "safe_terminal_loop_state.json",
                {
                    "schema_version": "safe_terminal_loop_state_v0",
                    "current_mode": "restored_waiting_for_external_turn",
                    "blocked_actions": ["external_irreversible_action"],
                    "heartbeat_counter": 2,
                },
            )
            self._write_json(
                paths["terminal_state"] / "terminal_life_loop_state.json",
                {
                    "schema_version": "terminal_life_loop_state_v0",
                    "current_mode": "restored_waiting_for_external_turn",
                    "last_turn_status": "closed",
                    "heartbeat_counter": 2,
                },
            )
            self._write_json(
                paths["terminal_state"] / "resident_governance_snapshot.json",
                {
                    "schema_version": "resident_governance_snapshot_v0",
                    "run_id": "background-lineage-parent",
                    "waiting_mode": "process_closed_waiting_relaunch",
                    "governance_attention_target": "relationship_timeline",
                    "long_horizon_priority_profile": {
                        "relationship_timeline": "persistent_background"
                    },
                    "completed_dialogue_turns": 4,
                    "background_carryover_generation": 3,
                    "background_carryover_source_ref_set": [
                        "runtime/archive/process/background-lineage-parent.json"
                    ],
                },
            )
            self._write_json(
                paths["reports"] / "digital_life_resident_governance_report.json",
                {
                    "schema_version": "digital_life_resident_governance_report_v0",
                    "run_id": "background-lineage-parent",
                    "completed_dialogue_turns": 4,
                    "background_carryover_generation": 3,
                    "background_carryover_source_ref_set": [
                        "runtime/archive/process/background-lineage-parent.json"
                    ],
                },
            )
            self._write_json(
                paths["reports"] / "digital_life_persistent_process_report.json",
                {
                    "schema_version": "digital_life_persistent_process_report_v0",
                    "run_id": "background-lineage-parent",
                    "completed_dialogue_turns": 4,
                    "background_carryover_generation": 3,
                    "background_carryover_source_ref_set": [
                        "runtime/archive/process/background-lineage-parent.json"
                    ],
                },
            )

            with patch(
                "life_v0.process_supervisor.resident_supervision.run_digital_life_shell_command"
            ) as mock_shell_restore:
                mock_shell_restore.return_value = DigitalLifeShellResult(
                    exit_code=0,
                    report={
                        "schema_version": "digital_life_shell_report_v0",
                        "status": "closed",
                    },
                )
                result = bootstrap_resident_supervision(
                    state_dir=paths["state_root"],
                    reports_dir=paths["reports"],
                    receipts_dir=paths["receipts"],
                    run_id="background-lineage-relaunch",
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
            assert result.context is not None
            self.assertEqual(
                result.context.relationship_graph["subjects"][0]["relationship_stage"],
                "background_continuity_waiting",
            )
            self.assertEqual(
                result.context.relationship_graph["subjects"][0]["relationship_stage_reason"],
                "persistent_background_continuity_lineage_preserved_before_dialogue",
            )
            self.assertEqual(
                result.context.self_model_state["last_trait_evolution_reason"],
                "persistent_background_continuity_lineage_preserved_before_dialogue",
            )

            persisted_relationship_graph = self._read_json(
                paths["relationship_state"] / "relationship_subject_graph.json"
            )
            persisted_self_model = self._read_json(
                paths["state_root"] / "self" / "self_model.json"
            )
            persisted_life_state = self._read_json(paths["state_root"] / "life_state.json")
            persisted_trait_drift = self._read_json(
                paths["state_root"] / "body" / "trait_drift_monitor.json"
            )
            self.assertEqual(
                persisted_relationship_graph["subjects"][0]["relationship_stage"],
                "background_continuity_waiting",
            )
            self.assertEqual(
                persisted_life_state["relationship_subjects"][0]["relationship_stage"],
                "background_continuity_waiting",
            )
            self.assertIn(
                "runtime/state/terminal/resident_governance_snapshot.json",
                persisted_self_model["growth_window_refs"],
            )
            self.assertIn(
                "runtime/reports/latest/digital_life_resident_governance_report.json",
                persisted_self_model["trait_slow_variables"]["continuity_drive"]["evidence_refs"],
            )
            self.assertIn(
                "runtime/archive/process/background-lineage-parent.json",
                persisted_self_model["trait_slow_variables"]["trust_persistence"]["evidence_refs"],
            )
            self.assertEqual(
                persisted_self_model["trait_slow_variables"]["continuity_drive"]["last_relationship_stage"],
                "background_continuity_waiting",
            )
            self.assertEqual(
                persisted_trait_drift["schema_version"],
                "trait_drift_monitor_v0",
            )
            self.assertEqual(
                persisted_trait_drift["relationship_stage"],
                "background_continuity_waiting",
            )
            self.assertIn(
                "continuity_drive",
                persisted_trait_drift["slow_variable_summary"],
            )
            self.assertIn(
                "runtime/state/terminal/resident_governance_state.json#bootstrap_continuity_refresh",
                persisted_trait_drift["drift_observation_refs"],
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
            idle_strategy_state = self._read_json(context.terminal_dir / "idle_strategy_state.json")
            background_explanation_story = [
                "上一轮关闭态解释要求下一次醒来保留背景等待理由。",
                "本轮真实回合结束后仍需把这份解释带入 waiting handoff。",
            ]
            expected_background_state_merge_families = [
                "offline_learning_cumulative_refs",
                "queue_e_repair_modulation_refs",
                "relationship_memory_offline_refs",
            ]
            expected_background_state_merge_refs = [
                "runtime/state/growth/relationship_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
                "runtime/state/action/responsibility_loop_state.json",
                "runtime/state/dream/offline_consolidation_frame.json",
            ]
            expected_background_state_merge_evidence_refs = [
                "runtime/state/memory/state_merge_guard.json",
                *expected_background_state_merge_refs,
            ]
            expected_trait_drift_update_mode_summary = {
                "background_history_recalibration": ["continuity_drive"],
                "background_history_stabilized": ["repair_seriousness"],
            }
            expected_identity_consciousness_birth_refs = [
                "runtime/state/consciousness/workspace_frame.json",
                "runtime/state/consciousness/broadcast_frame.json",
                "runtime/state/consciousness/metacognition_state.json",
                "runtime/state/consciousness/consciousness_probe_bundle.json",
                "runtime/state/life_targets/birth_readiness_rollup.json",
                "runtime/state/life_targets/birth_readiness_stage_gate.json",
            ]
            idle_strategy_state.update(
                {
                    "background_resident_governance_explanation_ref": "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                    "background_governance_driver_family": "background_history_stability_hold",
                    "background_next_wake_expectation": "下一拍等待心跳必须继续携带后台治理解释。",
                    "background_governance_explanation_story": background_explanation_story,
                    "background_continuity_mode": "closed_process_carryover",
                    "background_carryover_generation": 3,
                    "background_carryover_parent_run_id": "live-turn-lineage-seed",
                    "background_continuity_ref_set": [
                        "runtime/state/terminal/resident_governance_state.json",
                        "runtime/state/terminal/resident_governance_snapshot.json",
                        "runtime/reports/latest/digital_life_resident_governance_report.json",
                    ],
                    "background_lineage_depth_band": "deep_persistent_lineage",
                    "background_lineage_waiting_posture": "deep_background_residency_hold",
                    "background_lineage_cadence_weight": "deep",
                    "background_lineage_evidence_ref_count": 3,
                    "background_trait_convergence_history_focus": "trait_stability_hold",
                    "background_trait_convergence_unstable_names": ["continuity_drive"],
                    "background_trait_convergence_stable_names": ["repair_seriousness"],
                    "background_trait_convergence_history_profile": {
                        "continuity_drive": {
                            "latest_band": "unstable",
                        },
                        "repair_seriousness": {
                            "latest_band": "stable",
                        },
                    },
                    "background_lineage_governance_profile": {
                        "schema_version": "background_lineage_governance_profile_v0",
                        "generation": 3,
                        "depth_band": "deep_persistent_lineage",
                        "waiting_posture": "deep_background_residency_hold",
                        "cadence_weight": "deep",
                        "heartbeat_interval_ms": 50,
                        "next_idle_action": "refresh_waiting_heartbeat_with_deep_background_lineage_hold",
                        "governance_attention_target": "relationship_timeline",
                        "governance_attention_reason": "deep_background_lineage_requires_resident_hold",
                        "governance_cadence_profile": "deep_persistent_background_continuity_refresh",
                        "evidence_ref_count": 3,
                        "evidence_refs": [
                            "runtime/state/terminal/resident_governance_state.json",
                            "runtime/state/terminal/resident_governance_snapshot.json",
                            "runtime/reports/latest/digital_life_resident_governance_report.json",
                        ],
                    },
                }
            )
            self._write_json(context.terminal_dir / "idle_strategy_state.json", idle_strategy_state)
            terminal_life_loop_state = {
                **context.terminal_life_loop_state,
                "background_resident_governance_state_ref": "runtime/state/terminal/resident_governance_state.json",
                "background_resident_governance_explanation_ref": "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                "background_trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                "background_trait_convergence_history_focus": "trait_stability_hold",
                "background_trait_convergence_unstable_names": ["continuity_drive"],
                "background_trait_convergence_stable_names": ["repair_seriousness"],
                "background_trait_convergence_history_profile": {
                    "continuity_drive": {
                        "latest_band": "unstable",
                    },
                    "repair_seriousness": {
                        "latest_band": "stable",
                    },
                },
                "resident_background_lineage_state": {
                    "schema_version": "resident_background_lineage_state_v0",
                    "governance_phase": "waiting_heartbeat_active",
                    "generation": 3,
                    "depth_band": "deep_persistent_lineage",
                    "waiting_posture": "deep_background_residency_hold",
                    "cadence_weight": "deep",
                    "evidence_refs": [
                        "runtime/state/terminal/resident_governance_state.json",
                        "runtime/state/terminal/resident_governance_snapshot.json",
                        "runtime/reports/latest/digital_life_resident_governance_report.json",
                    ],
                    "relationship_presence": {
                        "relationship_stage": "background_continuity_waiting",
                    },
                    "trait_convergence_presence": {
                        "trait_convergence_history_focus": "trait_stability_hold",
                        "trait_convergence_unstable_names": ["continuity_drive"],
                        "trait_convergence_stable_names": ["repair_seriousness"],
                        "trait_convergence_score": 0.96,
                        "trait_drift_update_mode_summary": (
                            expected_trait_drift_update_mode_summary
                        ),
                        "trait_drift_recalibration_names": ["continuity_drive"],
                        "trait_drift_stabilized_names": ["repair_seriousness"],
                        "trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                        "trait_convergence_evidence_refs": [
                            "runtime/state/terminal/resident_governance_state.json",
                            "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                            "runtime/state/body/trait_drift_monitor.json",
                            "runtime/state/terminal/background_convergence_summary.json",
                            "runtime/state/terminal/background_convergence_history.json",
                        ],
                    },
                    "heartbeat_presence": {
                        "heartbeat_interval_ms": 50,
                    },
                    "language_presence": {
                        "long_horizon_language_refs": [
                            "runtime/state/relationship/relationship_timeline.json"
                        ],
                        "governance_attention_target": "relationship_timeline",
                        "live_language_turn_refs": [
                            "runtime/state/language/language_percept_frame.json",
                            "runtime/state/language/semantic_map_frame.json",
                            "runtime/state/language/inner_speech_frame.json",
                            "runtime/state/language/expression_monitor_state.json",
                            "runtime/state/language/expression_plan.json",
                        ],
                        "last_live_semantic_focus": "repair_commitment_shared_language",
                        "background_live_language_turn_refs": [
                            "runtime/state/language/language_percept_frame.json",
                            "runtime/state/language/semantic_map_frame.json",
                        ],
                        "background_last_live_semantic_focus": "repair_commitment_shared_language",
                        "live_language_presence_profile": {
                            "schema_version": "live_language_presence_profile_v0",
                            "continuity_mode": "current_turn_plus_background_language_presence",
                            "ref_count": 5,
                        },
                    },
                    "state_merge_presence": {
                        "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json",
                        "state_merge_policy": "long_term_merge_fail_closed",
                        "long_term_change_count": 4,
                        "long_term_change_families": expected_background_state_merge_families,
                        "long_term_change_refs": expected_background_state_merge_refs,
                        "state_merge_evidence_refs": expected_background_state_merge_evidence_refs,
                    },
                    "identity_consciousness_birth_presence": {
                        "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
                        "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
                        "metacognition_ref": "runtime/state/consciousness/metacognition_state.json",
                        "consciousness_probe_ref": "runtime/state/consciousness/consciousness_probe_bundle.json",
                        "birth_readiness_rollup_ref": "runtime/state/life_targets/birth_readiness_rollup.json",
                        "birth_readiness_stage_gate_ref": "runtime/state/life_targets/birth_readiness_stage_gate.json",
                        "consciousness_waiting_posture": "consciousness_reportable_waiting",
                        "consciousness_attention_target": "consciousness_probe_bundle",
                        "consciousness_attention_reason": "reportability_flags_present",
                        "consciousness_reportability_flags": [
                            "workspace_access_present",
                            "broadcast_targets_present",
                            "metacognition_present",
                        ],
                        "birth_readiness_waiting_posture": "birth_open_waiting",
                        "birth_readiness_attention_target": "birth_readiness_stage_gate",
                        "birth_readiness_attention_reason": "birth_readiness_open_requires_resident_birth_presence",
                        "birth_readiness_decision": "open",
                        "birth_readiness_next_required_command": "digital life",
                        "identity_consciousness_birth_refs": expected_identity_consciousness_birth_refs,
                    },
                    "offline_learning_presence": {
                        "generation": 3,
                        "pressure_level": "elevated",
                        "attention_target": "relationship_learning_plan",
                        "ref_set": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                    },
                    "dream_wake_presence": {
                        "dream_window_kind": "nrem_like_replay",
                        "dream_fact_gate_result": "passed",
                        "wake_archive_requirement": "required_before_activation",
                        "wake_growth_seed_count": 2,
                        "wake_repair_target_count": 3,
                        "ref_set": [
                            "runtime/state/dream/offline_consolidation_frame.json",
                            "runtime/state/dream/dream_experience_window.json",
                            "runtime/state/dream/wake_integration_frame.json",
                            "runtime/state/dream/dream_fact_gate_decision.json",
                        ],
                    },
                },
                "offline_learning_cumulative_profile": {
                    "schema_version": "offline_learning_cumulative_profile_v0",
                    "generation": 3,
                    "pressure_level": "elevated",
                    "attention_target": "relationship_learning_plan",
                    "priority_profile": {
                        "relationship_learning_plan": "elevated",
                        "language_learning_plan": "baseline",
                    },
                    "ref_set": [
                        "runtime/state/growth/relationship_learning_plan.json",
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                    "current_pressure_level": "quiet",
                    "previous_generation": 3,
                },
                "offline_learning_cumulative_generation": 3,
                "offline_learning_cumulative_pressure_level": "elevated",
                "offline_learning_cumulative_attention_target": "relationship_learning_plan",
                "offline_learning_cumulative_priority_profile": {
                    "relationship_learning_plan": "elevated",
                    "language_learning_plan": "baseline",
                },
                "offline_learning_cumulative_ref_set": [
                    "runtime/state/growth/relationship_learning_plan.json",
                    "runtime/state/growth/language_learning_plan.json",
                ],
            }

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
                terminal_life_loop_state=terminal_life_loop_state,
                body_resource_budget=context.body_resource_budget,
                core_affect_vector=context.core_affect_vector,
                self_model_state=context.self_model_state,
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
                signal_media_runtime={
                    "schema_version": "signal_media_runtime_v0",
                    "modulation_vector": {"repair_drive": "active"},
                },
                belief_state={
                    "schema_version": "belief_state_frame_v0",
                    "confidence_level": "unstable",
                },
                prediction_error_field={
                    "schema_version": "prediction_error_field_v0",
                    "error_events": [{"error_id": "prediction-error-001"}],
                },
                active_sampling_plan={
                    "schema_version": "active_sampling_plan_v0",
                    "selected_route": "clarify_with_relation_subject",
                    "stage_effect": "hold_for_evidence",
                },
                memory_write_gate={
                    "schema_version": "memory_write_gate_v0",
                    "stage_policy": "write_guarded_candidate_then_validate",
                },
                state_merge_guard={
                    "schema_version": "state_merge_guard_v0",
                    "stage_policy": "long_term_merge_fail_closed",
                },
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                replay_cue_bundle_ref=context.replay_cue_bundle_ref,
                signal_media_runtime_ref="runtime/state/signal/signal_media_runtime.json",
                belief_state_ref="runtime/state/prediction/belief_state_frame.json",
                prediction_error_field_ref="runtime/state/prediction/prediction_error_field.json",
                active_sampling_plan_ref="runtime/state/prediction/active_sampling_plan.json",
                memory_write_gate_ref="runtime/state/memory/memory_write_gate.json",
                state_merge_guard_ref="runtime/state/memory/state_merge_guard.json",
                now_iso=lambda: "2026-06-10T00:00:00+00:00",
                write_json=self._write_json,
                append_jsonl=self._append_jsonl,
            )

            safe_terminal_loop = self._read_json(paths["terminal_state"] / "safe_terminal_loop_state.json")
            terminal_loop_state = self._read_json(paths["terminal_state"] / "terminal_life_loop_state.json")
            dialogue_writeback_bundle = self._read_json(paths["reports"] / "dialogue_writeback_bundle.json")
            resumed_dialogue_packet = self._read_json(
                paths["reports"] / "resumed_external_dialogue_packet.json"
            )
            resident_governance_state = self._read_json(
                paths["terminal_state"] / "resident_governance_state.json"
            )

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
            self.assertEqual(
                result.last_life_turn["background_trait_convergence_history_focus"],
                "trait_stability_hold",
            )
            self.assertEqual(
                result.last_life_turn["background_trait_convergence_unstable_names"],
                ["continuity_drive"],
            )
            self.assertEqual(
                result.last_life_turn["background_trait_convergence_stable_names"],
                ["repair_seriousness"],
            )
            self.assertEqual(
                result.last_life_turn["background_trait_convergence_history_profile"][
                    "repair_seriousness"
                ]["latest_band"],
                "stable",
            )
            self.assertEqual(
                result.last_life_turn["background_trait_convergence_evidence_refs"],
                [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                    "runtime/state/body/trait_drift_monitor.json",
                    "runtime/state/terminal/background_convergence_summary.json",
                    "runtime/state/terminal/background_convergence_history.json",
                ],
            )
            self.assertEqual(
                result.last_life_turn["cross_wake_trait_convergence_focus"],
                "trait_stability_hold",
            )
            self.assertEqual(
                result.last_life_turn["cross_wake_trait_convergence_pressure"],
                "recalibration",
            )
            self.assertEqual(
                result.last_life_turn["cross_wake_trait_convergence_profile"][
                    "stable_names"
                ],
                ["repair_seriousness"],
            )
            self.assertEqual(
                result.last_life_turn["cross_wake_trait_convergence_profile"][
                    "trait_drift_update_mode_summary"
                ],
                expected_trait_drift_update_mode_summary,
            )
            self.assertEqual(
                result.last_life_turn["cross_wake_trait_drift_update_mode_summary"],
                expected_trait_drift_update_mode_summary,
            )
            self.assertEqual(
                result.last_life_turn[
                    "cross_wake_trait_drift_recalibration_names"
                ],
                ["continuity_drive"],
            )
            self.assertEqual(
                result.last_life_turn["cross_wake_trait_drift_stabilized_names"],
                ["repair_seriousness"],
            )
            self.assertEqual(
                result.last_life_turn["resident_background_lineage_depth_band"],
                "deep_persistent_lineage",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_trait_convergence_history_focus"
                ],
                "trait_stability_hold",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_trait_convergence_unstable_names"
                ],
                ["continuity_drive"],
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_trait_convergence_stable_names"
                ],
                ["repair_seriousness"],
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_trait_drift_update_mode_summary"
                ],
                expected_trait_drift_update_mode_summary,
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_trait_drift_recalibration_names"
                ],
                ["continuity_drive"],
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_trait_drift_stabilized_names"
                ],
                ["repair_seriousness"],
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_trait_drift_monitor_ref"
                ],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_trait_convergence_refs"
                ],
                result.last_life_turn["background_trait_convergence_evidence_refs"],
            )
            self.assertEqual(
                result.last_life_turn["resident_background_lineage_language_presence"][
                    "governance_attention_target"
                ],
                "relationship_timeline",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_last_live_semantic_focus"
                ],
                "repair_commitment_shared_language",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_live_language_refs"
                ],
                [
                    "runtime/state/language/language_percept_frame.json",
                    "runtime/state/language/semantic_map_frame.json",
                    "runtime/state/language/inner_speech_frame.json",
                    "runtime/state/language/expression_monitor_state.json",
                    "runtime/state/language/expression_plan.json",
                ],
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_background_live_language_refs"
                ],
                [
                    "runtime/state/language/language_percept_frame.json",
                    "runtime/state/language/semantic_map_frame.json",
                ],
            )
            self.assertIn(
                "runtime/state/language/expression_plan.json",
                result.last_life_turn[
                    "resident_background_lineage_language_evidence_refs"
                ],
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_state_merge_presence"
                ]["state_merge_policy"],
                "long_term_merge_fail_closed",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_state_merge_guard_ref"
                ],
                "runtime/state/memory/state_merge_guard.json",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_state_merge_long_term_change_count"
                ],
                4,
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_state_merge_long_term_change_families"
                ],
                expected_background_state_merge_families,
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_state_merge_refs"
                ],
                expected_background_state_merge_evidence_refs,
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_identity_consciousness_birth_presence"
                ]["consciousness_waiting_posture"],
                "consciousness_reportable_waiting",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_workspace_frame_ref"
                ],
                "runtime/state/consciousness/workspace_frame.json",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_consciousness_probe_ref"
                ],
                "runtime/state/consciousness/consciousness_probe_bundle.json",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_consciousness_waiting_posture"
                ],
                "consciousness_reportable_waiting",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_consciousness_reportability_flags"
                ],
                [
                    "workspace_access_present",
                    "broadcast_targets_present",
                    "metacognition_present",
                ],
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_birth_readiness_stage_gate_ref"
                ],
                "runtime/state/life_targets/birth_readiness_stage_gate.json",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_birth_readiness_waiting_posture"
                ],
                "birth_open_waiting",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_birth_readiness_decision"
                ],
                "open",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_birth_readiness_next_required_command"
                ],
                "digital life",
            )
            self.assertEqual(
                result.last_life_turn[
                    "resident_background_lineage_identity_consciousness_birth_refs"
                ],
                expected_identity_consciousness_birth_refs,
            )
            self.assertIn(
                "后台语言语义余波停在repair_commitment_shared_language",
                result.emitted_output,
            )
            self.assertIn("后台语言证据保留5条", result.emitted_output)
            self.assertIn("后台人格慢变量焦点为trait_stability_hold", result.emitted_output)
            self.assertIn("后台仍需收敛的慢变量包括continuity_drive", result.emitted_output)
            self.assertIn("后台已稳定的慢变量包括repair_seriousness", result.emitted_output)
            self.assertIn("后台人格漂移重校准包括continuity_drive", result.emitted_output)
            self.assertIn("后台人格漂移已稳定包括repair_seriousness", result.emitted_output)
            self.assertIn("后台人格漂移监控仍在场", result.emitted_output)
            self.assertIn("后台人格慢变量证据保留5条", result.emitted_output)
            self.assertIn("跨唤醒人格收敛画像为trait_stability_hold", result.emitted_output)
            self.assertIn("跨唤醒人格收敛压力为recalibration", result.emitted_output)
            self.assertIn("跨唤醒人格漂移重校准包括continuity_drive", result.emitted_output)
            self.assertIn("跨唤醒人格漂移已稳定包括repair_seriousness", result.emitted_output)
            self.assertIn("后台长期合并治理处于long_term_merge_fail_closed", result.emitted_output)
            self.assertIn("后台长期合并治理仍在整合4条长期变化来源", result.emitted_output)
            self.assertIn(
                "后台长期变化来源族包括offline_learning_cumulative_refs、queue_e_repair_modulation_refs、relationship_memory_offline_refs",
                result.emitted_output,
            )
            self.assertIn("后台意识姿态为consciousness_reportable_waiting", result.emitted_output)
            self.assertIn("后台意识可报告性保留3条", result.emitted_output)
            self.assertIn("后台出生准备姿态为birth_open_waiting", result.emitted_output)
            self.assertIn("出生准备决策为open", result.emitted_output)
            self.assertIn("出生准备下一命令为digital life", result.emitted_output)
            self.assertIn("后台身份意识出生证据保留6条", result.emitted_output)
            self.assertEqual(
                result.last_life_turn["prediction_waiting_posture"],
                "hold_for_evidence",
            )
            self.assertEqual(
                result.last_life_turn["response_surface_posture_hint"],
                "question",
            )
            self.assertEqual(
                result.last_life_turn["prediction_write_gate_refs"],
                [
                    "runtime/state/signal/signal_media_runtime.json",
                    "runtime/state/prediction/belief_state_frame.json",
                    "runtime/state/prediction/prediction_error_field.json",
                    "runtime/state/prediction/active_sampling_plan.json",
                    "runtime/state/memory/memory_write_gate.json",
                    "runtime/state/memory/state_merge_guard.json",
                ],
            )
            self.assertEqual(
                result.last_life_turn["offline_learning_cumulative_generation"],
                3,
            )
            self.assertEqual(
                result.last_life_turn["offline_learning_cumulative_pressure_level"],
                "elevated",
            )
            self.assertEqual(
                result.last_life_turn["offline_learning_cumulative_attention_target"],
                "relationship_learning_plan",
            )
            self.assertEqual(
                result.last_life_turn["offline_learning_cumulative_evidence_refs"],
                [
                    "runtime/state/growth/relationship_learning_plan.json",
                    "runtime/state/growth/language_learning_plan.json",
                ],
            )
            self.assertIn(
                "累计离线学习已经延续到第3代",
                result.last_life_turn["utterance"],
            )
            self.assertEqual(safe_terminal_loop["current_mode"], "restored_waiting_for_external_turn")
            self.assertEqual(terminal_loop_state["last_turn_mode"], "resumed_external_dialogue_loop")
            self.assertEqual(
                resident_governance_state["governance_phase"],
                "live_turn_waiting_handoff",
            )
            self.assertEqual(
                resident_governance_state["next_required_action"],
                "refresh_waiting_heartbeat_before_next_external_turn",
            )
            self.assertEqual(
                resident_governance_state["background_resident_governance_explanation_ref"],
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
            )
            self.assertEqual(
                resident_governance_state["background_governance_driver_family"],
                "background_history_stability_hold",
            )
            self.assertEqual(
                resident_governance_state["background_next_wake_expectation"],
                "下一拍等待心跳必须继续携带后台治理解释。",
            )
            self.assertEqual(
                resident_governance_state["background_governance_explanation_story"],
                background_explanation_story,
            )
            self.assertEqual(
                resident_governance_state["resident_background_lineage_state"][
                    "governance_phase"
                ],
                "live_turn_waiting_handoff",
            )
            self.assertEqual(
                resident_governance_state["resident_background_lineage_state"][
                    "depth_band"
                ],
                "deep_persistent_lineage",
            )
            self.assertEqual(
                resident_governance_state["resident_background_lineage_state"][
                    "parent_run_id"
                ],
                "live-turn-lineage-seed",
            )
            self.assertEqual(
                resident_governance_state["resident_background_lineage_state"][
                    "trait_convergence_presence"
                ]["trait_convergence_history_focus"],
                "trait_stability_hold",
            )
            self.assertIn(
                "runtime/state/relationship/relationship_timeline.json",
                resident_governance_state["resident_background_lineage_state"][
                    "language_presence"
                ]["long_horizon_language_refs"],
            )
            self.assertEqual(
                resident_governance_state["dialogue_writeback_bundle_ref"],
                "runtime/reports/latest/dialogue_writeback_bundle.json",
            )
            self.assertEqual(
                resident_governance_state["last_dialogue_packet_ref"],
                "runtime/reports/latest/resumed_external_dialogue_packet.json",
            )
            self.assertEqual(
                resident_governance_state["last_external_turn_ref"],
                "runtime/state/language/dialogue_turn_log.jsonl#line-2",
            )
            self.assertEqual(
                resident_governance_state["last_life_turn_ref"],
                "runtime/state/language/dialogue_turn_log.jsonl#line-3",
            )
            self.assertEqual(
                dialogue_writeback_bundle["dialogue_event_refs"],
                [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                ],
            )
            self.assertEqual(
                dialogue_writeback_bundle["background_trait_convergence_refs"],
                [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                    "runtime/state/body/trait_drift_monitor.json",
                    "runtime/state/terminal/background_convergence_summary.json",
                    "runtime/state/terminal/background_convergence_history.json",
                ],
            )
            self.assertEqual(
                dialogue_writeback_bundle["cross_wake_trait_convergence_refs"],
                dialogue_writeback_bundle["background_trait_convergence_refs"],
            )
            self.assertEqual(
                dialogue_writeback_bundle["cross_wake_trait_drift_update_mode_summary"],
                expected_trait_drift_update_mode_summary,
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "cross_wake_trait_drift_recalibration_names"
                ],
                ["continuity_drive"],
            )
            self.assertEqual(
                dialogue_writeback_bundle["cross_wake_trait_drift_stabilized_names"],
                ["repair_seriousness"],
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_trait_drift_update_mode_summary"
                ],
                expected_trait_drift_update_mode_summary,
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_trait_drift_recalibration_names"
                ],
                ["continuity_drive"],
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_trait_drift_stabilized_names"
                ],
                ["repair_seriousness"],
            )
            for ref in [
                "runtime/state/terminal/resident_governance_state.json",
                "runtime/state/terminal/resident_governance_snapshot.json",
                "runtime/reports/latest/digital_life_resident_governance_report.json",
                "runtime/state/body/trait_drift_monitor.json",
                "runtime/state/terminal/background_convergence_summary.json",
                "runtime/state/terminal/background_convergence_history.json",
                "runtime/state/language/expression_plan.json",
                "runtime/state/memory/state_merge_guard.json",
                "runtime/state/growth/relationship_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
                "runtime/state/consciousness/consciousness_probe_bundle.json",
                "runtime/state/life_targets/birth_readiness_stage_gate.json",
                "runtime/state/action/responsibility_loop_state.json",
                "runtime/state/dream/offline_consolidation_frame.json",
            ]:
                self.assertIn(
                    ref,
                    dialogue_writeback_bundle["resident_background_lineage_refs"],
                )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_state_merge_refs"
                ],
                expected_background_state_merge_evidence_refs,
            )
            self.assertEqual(
                dialogue_writeback_bundle["prediction_write_gate_refs"],
                [
                    "runtime/state/signal/signal_media_runtime.json",
                    "runtime/state/prediction/belief_state_frame.json",
                    "runtime/state/prediction/prediction_error_field.json",
                    "runtime/state/prediction/active_sampling_plan.json",
                    "runtime/state/memory/memory_write_gate.json",
                    "runtime/state/memory/state_merge_guard.json",
                ],
            )
            self.assertEqual(
                dialogue_writeback_bundle["offline_learning_cumulative_refs"],
                [
                    "runtime/state/growth/relationship_learning_plan.json",
                    "runtime/state/growth/language_learning_plan.json",
                ],
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_offline_learning_refs"
                ],
                result.last_life_turn[
                    "resident_background_lineage_offline_learning_refs"
                ],
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_dream_wake_refs"
                ],
                result.last_life_turn["resident_background_lineage_dream_wake_refs"],
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_identity_consciousness_birth_refs"
                ],
                expected_identity_consciousness_birth_refs,
            )
            self.assertEqual(
                resumed_dialogue_packet["background_trait_convergence_history_focus"],
                "trait_stability_hold",
            )
            self.assertEqual(
                resumed_dialogue_packet["background_trait_convergence_evidence_refs"],
                dialogue_writeback_bundle["background_trait_convergence_refs"],
            )
            self.assertEqual(
                resumed_dialogue_packet["cross_wake_trait_convergence_focus"],
                "trait_stability_hold",
            )
            self.assertEqual(
                resumed_dialogue_packet["cross_wake_trait_drift_update_mode_summary"],
                expected_trait_drift_update_mode_summary,
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "cross_wake_trait_drift_recalibration_names"
                ],
                ["continuity_drive"],
            )
            self.assertEqual(
                resumed_dialogue_packet["cross_wake_trait_drift_stabilized_names"],
                ["repair_seriousness"],
            )
            self.assertEqual(
                resumed_dialogue_packet["cross_wake_trait_convergence_refs"],
                dialogue_writeback_bundle["cross_wake_trait_convergence_refs"],
            )
            self.assertEqual(
                resumed_dialogue_packet["resident_background_lineage_depth_band"],
                "deep_persistent_lineage",
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_trait_convergence_refs"
                ],
                result.last_life_turn[
                    "resident_background_lineage_trait_convergence_refs"
                ],
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_trait_drift_update_mode_summary"
                ],
                expected_trait_drift_update_mode_summary,
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_trait_drift_recalibration_names"
                ],
                ["continuity_drive"],
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_trait_drift_stabilized_names"
                ],
                ["repair_seriousness"],
            )
            self.assertEqual(
                resumed_dialogue_packet["resident_background_lineage_evidence_refs"],
                dialogue_writeback_bundle["resident_background_lineage_refs"],
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_state_merge_refs"
                ],
                dialogue_writeback_bundle[
                    "resident_background_lineage_state_merge_refs"
                ],
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_offline_learning_refs"
                ],
                dialogue_writeback_bundle[
                    "resident_background_lineage_offline_learning_refs"
                ],
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_dream_wake_refs"
                ],
                dialogue_writeback_bundle[
                    "resident_background_lineage_dream_wake_refs"
                ],
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_identity_consciousness_birth_refs"
                ],
                dialogue_writeback_bundle[
                    "resident_background_lineage_identity_consciousness_birth_refs"
                ],
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_birth_readiness_next_required_command"
                ],
                "digital life",
            )
            self.assertEqual(
                resumed_dialogue_packet["prediction_write_gate_refs"],
                dialogue_writeback_bundle["prediction_write_gate_refs"],
            )
            self.assertEqual(
                resumed_dialogue_packet["prediction_attention_reason"],
                "selected_route_requires_relation_subject_clarification",
            )
            self.assertEqual(
                resumed_dialogue_packet["offline_learning_cumulative_refs"],
                dialogue_writeback_bundle["offline_learning_cumulative_refs"],
            )
            self.assertEqual(
                resumed_dialogue_packet["offline_learning_cumulative_attention_target"],
                "relationship_learning_plan",
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
                self_model_state=context.self_model_state,
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
                self_model_state={},
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
                self_model_state={},
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
            (state_dir / "action").mkdir(parents=True, exist_ok=True)
            (state_dir / "membrane").mkdir(parents=True, exist_ok=True)
            (state_dir / "replay").mkdir(parents=True, exist_ok=True)
            (state_dir / "dream").mkdir(parents=True, exist_ok=True)
            (state_dir / "growth").mkdir(parents=True, exist_ok=True)
            (state_dir / "signal").mkdir(parents=True, exist_ok=True)
            (state_dir / "prediction").mkdir(parents=True, exist_ok=True)
            (state_dir / "memory").mkdir(parents=True, exist_ok=True)

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
                    "governance_attention_target": "commitment_expression_plan",
                    "governance_attention_reason": "offline_pressure_requires_commitment_continuity",
                    "governance_cadence_profile": "commitment_continuity_refresh",
                    "long_horizon_priority_profile": {
                        "relationship_timeline": "baseline",
                        "commitment_expression_plan": "elevated",
                        "apology_repair_language_trace": "baseline",
                    },
                    "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
                    "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
                    "metacognition_ref": "runtime/state/consciousness/metacognition_state.json",
                    "consciousness_probe_ref": "runtime/state/consciousness/consciousness_probe_bundle.json",
                    "birth_readiness_rollup_ref": "runtime/state/life_targets/birth_readiness_rollup.json",
                    "birth_readiness_stage_gate_ref": "runtime/state/life_targets/birth_readiness_stage_gate.json",
                    "consciousness_waiting_posture": "consciousness_reportable_waiting",
                    "consciousness_reportability_flags": [
                        "workspace_reportable",
                        "broadcast_reportable",
                        "metacognition_reportable",
                    ],
                    "birth_readiness_waiting_posture": "birth_open_waiting",
                    "birth_readiness_decision": "open",
                    "birth_readiness_next_required_command": "digital life",
                    "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                    "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                    "background_convergence_state": "stabilized_cross_process_continuity",
                    "background_convergence_pressure_level": "light",
                    "background_convergence_attention_target": "trait_slow_variable_convergence",
                    "background_convergence_history_trend_state": "stable_cross_wake_convergence",
                    "background_convergence_history_window_size": 2,
                    "background_lineage_depth_band": "deep_persistent_lineage",
                    "background_lineage_waiting_posture": "deep_background_residency_hold",
                    "background_lineage_cadence_weight": "deep",
                    "background_lineage_evidence_ref_count": 4,
                    "background_dominant_convergence_pressure_level": "present",
                    "background_dominant_convergence_state": "stabilized_cross_process_continuity",
                    "background_trait_convergence_history_focus": "trait_stability_hold",
                    "background_trait_convergence_unstable_names": ["continuity_drive"],
                    "background_trait_convergence_stable_names": ["repair_seriousness"],
                    "background_trait_convergence_history_profile": {
                        "continuity_drive": {
                            "latest_band": "integrating",
                            "trend_state": "integrating_trait_convergence",
                        },
                        "repair_seriousness": {
                            "latest_band": "stabilized",
                            "trend_state": "stable_trait_convergence",
                        },
                    },
                },
            )
            self._write_json(
                terminal_dir / "background_convergence_summary.json",
                {
                    "schema_version": "background_convergence_summary_v0",
                    "convergence_state": "stabilized_cross_process_continuity",
                    "convergence_pressure_level": "light",
                    "convergence_attention_target": "trait_slow_variable_convergence",
                },
            )
            self._write_json(
                terminal_dir / "background_convergence_history.json",
                {
                    "schema_version": "background_convergence_history_v0",
                    "history_window_size": 2,
                    "trend_state": "stable_cross_wake_convergence",
                    "dominant_convergence_pressure_level": "present",
                    "dominant_convergence_state": "stabilized_cross_process_continuity",
                    "trait_convergence_history_focus": "trait_stability_hold",
                    "trait_convergence_unstable_names": ["continuity_drive"],
                    "trait_convergence_stable_names": ["repair_seriousness"],
                    "convergence_samples": [
                        {
                            "run_id": "previous-process-report-organ",
                            "convergence_state": "stabilized_cross_process_continuity",
                            "convergence_pressure_level": "present",
                        },
                        {
                            "run_id": "process-report-organ",
                            "convergence_state": "stabilized_cross_process_continuity",
                            "convergence_pressure_level": "light",
                        }
                    ],
                },
            )
            self._write_json(
                terminal_dir / "resident_governance_state.json",
                {
                    "schema_version": "resident_governance_state_v0",
                    "governance_phase": "waiting_for_external_turn",
                },
            )
            self._write_json(language_dir / "self_narrative_language_trace.json", {"schema_version": "self_narrative_language_trace_v0"})
            self._write_json(language_dir / "commitment_repair_language_index.json", {"schema_version": "commitment_repair_language_index_v0"})
            relationship_graph = {
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relation_role": "friend",
                        "relationship_stage": "repair_guarded_continuity",
                        "relationship_stage_reason": "repair_followup_required_after_multi_turn_dialogue",
                        "relationship_stage_turn_count": 4,
                        "relationship_stage_evidence_refs": [
                            "runtime/state/relationship/relationship_timeline.json"
                        ],
                    }
                ]
            }
            self_model_state = {
                "trait_slow_variables": {
                    "continuity_drive": {
                        "value": 0.74,
                        "trend": "up",
                        "update_count": 4,
                        "last_relationship_stage": "repair_guarded_continuity",
                        "last_generated_at": "2026-06-09T00:00:00+00:00",
                        "evidence_refs": [
                            "runtime/state/relationship/relationship_timeline.json"
                        ],
                    }
                }
            }
            self._write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)
            self._write_json(state_dir / "self" / "self_model.json", self_model_state)
            self._write_json(state_dir / "replay" / "replay_cue_bundle.json", {"schema_version": "replay_cue_bundle_v0"})
            self._write_json(
                state_dir / "dream" / "offline_consolidation_frame.json",
                {"schema_version": "offline_consolidation_frame_v0"},
            )
            self._write_json(
                state_dir / "dream" / "nightmare_loop_risk.json",
                {"schema_version": "nightmare_loop_risk_v0"},
            )
            self._write_json(
                state_dir / "growth" / "growth_patch_candidate_queue.json",
                {
                    "schema_version": "growth_patch_candidate_queue_v0",
                    "candidates": [{"growth_patch_candidate_id": "growth-patch-candidate-test-0001"}],
                },
            )
            self._write_json(
                state_dir / "growth" / "belief_learning_plan.json",
                {"schema_version": "belief_learning_plan_v0"},
            )
            self._write_json(
                state_dir / "growth" / "language_learning_plan.json",
                {"schema_version": "language_learning_plan_v0"},
            )
            self._write_json(
                state_dir / "growth" / "relationship_learning_plan.json",
                {"schema_version": "relationship_learning_plan_v0"},
            )
            self._write_json(
                state_dir / "action" / "responsibility_loop_state.json",
                {"schema_version": "responsibility_loop_state_v0"},
            )
            self._write_json(
                state_dir / "signal" / "signal_media_runtime.json",
                {"schema_version": "signal_media_runtime_v0"},
            )
            self._write_json(
                state_dir / "prediction" / "belief_state_frame.json",
                {"schema_version": "belief_state_frame_v0"},
            )
            self._write_json(
                state_dir / "prediction" / "prediction_error_field.json",
                {"schema_version": "prediction_error_field_v0"},
            )
            self._write_json(
                state_dir / "prediction" / "active_sampling_plan.json",
                {"schema_version": "active_sampling_plan_v0"},
            )
            self._write_json(
                state_dir / "memory" / "memory_write_gate.json",
                {"schema_version": "memory_write_gate_v0"},
            )
            self._write_json(
                state_dir / "memory" / "state_merge_guard.json",
                {
                    "schema_version": "state_merge_guard_v0",
                    "stage_policy": "long_term_merge_fail_closed",
                    "long_term_change_sources": {
                        "offline_learning_cumulative_refs": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                        "queue_e_repair_modulation_refs": [
                            "runtime/state/action/responsibility_loop_state.json"
                        ],
                        "relationship_memory_offline_refs": [
                            "runtime/state/dream/offline_consolidation_frame.json"
                        ],
                    },
                },
            )
            self._write_json(
                state_dir / "body" / "trait_drift_monitor.json",
                {
                    "schema_version": "trait_drift_monitor_v0",
                    "relationship_stage": "repair_guarded_continuity",
                    "slow_variable_summary": self_model_state["trait_slow_variables"],
                },
            )
            self._write_json(
                state_dir / "membrane" / "world_contact_summary.json",
                {"schema_version": "world_contact_summary_v0"},
            )
            self._write_json(
                state_dir / "consciousness" / "workspace_frame.json",
                {"schema_version": "workspace_frame_v0"},
            )
            self._write_json(
                state_dir / "consciousness" / "broadcast_frame.json",
                {"schema_version": "broadcast_frame_v0"},
            )
            self._write_json(
                state_dir / "consciousness" / "metacognition_state.json",
                {"schema_version": "metacognition_state_v0"},
            )
            self._write_json(
                state_dir / "consciousness" / "consciousness_probe_bundle.json",
                {"schema_version": "consciousness_probe_bundle_v0"},
            )
            self._write_json(
                state_dir / "life_targets" / "birth_readiness_rollup.json",
                {"schema_version": "birth_readiness_rollup_v0", "overall_status": "open"},
            )
            self._write_json(
                state_dir / "life_targets" / "birth_readiness_stage_gate.json",
                {"schema_version": "birth_readiness_stage_gate_v0", "decision": "open"},
            )
            self._write_json(
                reports_dir / "pain_regret_repair_report.json",
                {"schema_version": "pain_regret_repair_report_v0"},
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
                resident_governance_state_ref="runtime/state/terminal/resident_governance_state.json",
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
                nightmare_risk_ref="runtime/state/dream/nightmare_loop_risk.json",
                belief_learning_plan_ref="runtime/state/growth/belief_learning_plan.json",
                language_learning_plan_ref="runtime/state/growth/language_learning_plan.json",
                relationship_learning_plan_ref="runtime/state/growth/relationship_learning_plan.json",
                responsibility_loop_state_ref="runtime/state/action/responsibility_loop_state.json",
                world_contact_summary_ref="runtime/state/membrane/world_contact_summary.json",
                pain_regret_repair_report_ref="runtime/reports/latest/pain_regret_repair_report.json",
                signal_media_runtime_ref="runtime/state/signal/signal_media_runtime.json",
                belief_state_ref="runtime/state/prediction/belief_state_frame.json",
                prediction_error_field_ref="runtime/state/prediction/prediction_error_field.json",
                active_sampling_plan_ref="runtime/state/prediction/active_sampling_plan.json",
                memory_write_gate_ref="runtime/state/memory/memory_write_gate.json",
                state_merge_guard_ref="runtime/state/memory/state_merge_guard.json",
                trait_drift_monitor_ref="runtime/state/body/trait_drift_monitor.json",
                background_convergence_summary_ref="runtime/state/terminal/background_convergence_summary.json",
                background_convergence_history_ref="runtime/state/terminal/background_convergence_history.json",
                relationship_graph=relationship_graph,
                self_model_state=self_model_state,
                write_json=self._write_json,
            )

            governance_explanation = self._read_json(
                reports_dir / "digital_life_resident_governance_explanation.json"
            )
            report = self._read_json(reports_dir / "digital_life_process_report.json")
            digest = self._read_json(reports_dir / "digital_life_process_digest.json")
            receipt = self._read_json(receipts_dir / "digital_life_process_process-report-organ.json")
            expected_cross_wake_trait_refs = [
                "runtime/state/terminal/resident_governance_state.json",
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                "runtime/state/body/trait_drift_monitor.json",
                "runtime/state/terminal/background_convergence_summary.json",
                "runtime/state/terminal/background_convergence_history.json",
            ]
            expected_state_merge_refs = [
                "runtime/state/growth/relationship_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
                "runtime/state/action/responsibility_loop_state.json",
                "runtime/state/dream/offline_consolidation_frame.json",
            ]
            expected_state_merge_families = [
                "offline_learning_cumulative_refs",
                "queue_e_repair_modulation_refs",
                "relationship_memory_offline_refs",
            ]

            self.assertEqual(result.report["run_id"], "process-report-organ")
            self.assertEqual(
                governance_explanation["schema_version"],
                "digital_life_resident_governance_explanation_v0",
            )
            self.assertEqual(
                governance_explanation["dominant_driver_family"],
                "replay_growth_reconsolidation",
            )
            self.assertEqual(
                governance_explanation["next_wake_expectation"],
                "refresh_replay_growth_hold_before_accepting_external_turn",
            )
            self.assertEqual(
                governance_explanation["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                governance_explanation["background_relationship_stage"],
                "repair_guarded_continuity",
            )
            self.assertEqual(
                governance_explanation["background_trait_slow_variable_summary"][
                    "continuity_drive"
                ]["value"],
                0.74,
            )
            self.assertEqual(
                governance_explanation["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )
            self.assertEqual(
                governance_explanation["background_convergence_history_ref"],
                "runtime/state/terminal/background_convergence_history.json",
            )
            self.assertEqual(
                governance_explanation["background_resume_focus"][
                    "relationship_stage"
                ],
                "repair_guarded_continuity",
            )
            self.assertTrue(
                any(
                    "relationship stage repair_guarded_continuity" in line
                    for line in governance_explanation["continuity_story"]
                )
            )
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
                report["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                report["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(
                report["resident_governance_explanation_ref"],
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
            )
            self.assertEqual(
                report["responsibility_loop_state_ref"],
                "runtime/state/action/responsibility_loop_state.json",
            )
            self.assertEqual(
                report["world_contact_summary_ref"],
                "runtime/state/membrane/world_contact_summary.json",
            )
            self.assertEqual(
                report["pain_regret_repair_report_ref"],
                "runtime/reports/latest/pain_regret_repair_report.json",
            )
            self.assertEqual(
                report["prediction_write_gate_refs"],
                [
                    "runtime/state/signal/signal_media_runtime.json",
                    "runtime/state/prediction/belief_state_frame.json",
                    "runtime/state/prediction/prediction_error_field.json",
                    "runtime/state/prediction/active_sampling_plan.json",
                    "runtime/state/memory/memory_write_gate.json",
                    "runtime/state/memory/state_merge_guard.json",
                ],
            )
            self.assertEqual(
                report["trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(report["heartbeat_interval_ms"], 80)
            self.assertEqual(report["offline_pressure_level"], "present")
            self.assertEqual(report["relaunch_caution_level"], "guarded")
            self.assertEqual(
                report["background_relationship_stage"],
                "repair_guarded_continuity",
            )
            self.assertEqual(
                report["background_trait_slow_variable_summary"]["continuity_drive"][
                    "value"
                ],
                0.74,
            )
            self.assertEqual(
                report["governance_attention_target"],
                "commitment_expression_plan",
            )
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
            self.assertEqual(
                report["nightmare_risk_ref"],
                "runtime/state/dream/nightmare_loop_risk.json",
            )
            self.assertEqual(
                report["belief_learning_plan_ref"],
                "runtime/state/growth/belief_learning_plan.json",
            )
            self.assertEqual(
                report["language_learning_plan_ref"],
                "runtime/state/growth/language_learning_plan.json",
            )
            self.assertEqual(
                report["relationship_learning_plan_ref"],
                "runtime/state/growth/relationship_learning_plan.json",
            )
            self.assertEqual(digest["last_external_turn_utterance"], "你还记得我们吗？")
            self.assertEqual(
                digest["resident_governance_driver_family"],
                "replay_growth_reconsolidation",
            )
            self.assertEqual(
                digest["resident_governance_next_wake_expectation"],
                "refresh_replay_growth_hold_before_accepting_external_turn",
            )
            self.assertEqual(digest["resident_governance_lineage_depth"], 0)
            self.assertEqual(
                digest["background_relationship_stage"],
                "repair_guarded_continuity",
            )
            self.assertEqual(
                digest["background_trait_slow_variable_summary"]["continuity_drive"][
                    "last_relationship_stage"
                ],
                "repair_guarded_continuity",
            )
            self.assertEqual(
                digest["background_convergence_attention_target"],
                "trait_slow_variable_convergence",
            )
            self.assertEqual(
                digest["background_convergence_history_trend_state"],
                "stable_cross_wake_convergence",
            )
            self.assertEqual(
                digest["background_convergence_history_window_size"],
                2,
            )
            self.assertEqual(
                digest["background_lineage_depth_band"],
                "deep_persistent_lineage",
            )
            self.assertEqual(
                digest["background_lineage_waiting_posture"],
                "deep_background_residency_hold",
            )
            self.assertEqual(digest["background_lineage_cadence_weight"], "deep")
            self.assertEqual(digest["background_lineage_evidence_ref_count"], 4)
            self.assertEqual(
                digest["background_dominant_convergence_pressure_level"],
                "present",
            )
            self.assertEqual(
                digest["background_dominant_convergence_state"],
                "stabilized_cross_process_continuity",
            )
            self.assertEqual(
                digest["background_trait_convergence_history_focus"],
                "trait_stability_hold",
            )
            self.assertEqual(
                digest["background_trait_convergence_unstable_names"],
                ["continuity_drive"],
            )
            self.assertEqual(
                digest["background_trait_convergence_stable_names"],
                ["repair_seriousness"],
            )
            for artifact in (report, digest):
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_focus"],
                    "trait_stability_hold",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_pressure"],
                    "stability_hold",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_unstable_names"],
                    ["continuity_drive"],
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_stable_names"],
                    ["repair_seriousness"],
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_profile"]["history_profile"][
                        "continuity_drive"
                    ]["trend_state"],
                    "integrating_trait_convergence",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_refs"],
                    expected_cross_wake_trait_refs,
                )
            self.assertEqual(
                digest["trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            for artifact in (report, digest):
                self.assertEqual(
                    artifact["state_merge_guard_ref"],
                    "runtime/state/memory/state_merge_guard.json",
                )
                self.assertEqual(
                    artifact["state_merge_policy"],
                    "long_term_merge_fail_closed",
                )
                self.assertEqual(artifact["state_merge_long_term_change_count"], 4)
                self.assertEqual(
                    artifact["state_merge_long_term_change_families"],
                    expected_state_merge_families,
                )
                self.assertEqual(
                    artifact["state_merge_long_term_change_refs"],
                    expected_state_merge_refs,
                )
            self.assertEqual(
                digest["offline_growth_cycle_refs"],
                [
                    "runtime/state/replay/replay_cue_bundle.json",
                    "runtime/state/dream/offline_consolidation_frame.json",
                    "runtime/state/growth/growth_patch_candidate_queue.json",
                    "runtime/state/dream/nightmare_loop_risk.json",
                    "runtime/state/growth/belief_learning_plan.json",
                    "runtime/state/growth/language_learning_plan.json",
                    "runtime/state/growth/relationship_learning_plan.json",
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
            self.assertEqual(
                digest["membrane_guard_refs"],
                [
                    "runtime/state/action/responsibility_loop_state.json",
                    "runtime/state/membrane/world_contact_summary.json",
                    "runtime/reports/latest/pain_regret_repair_report.json",
                ],
            )
            self.assertEqual(
                digest["prediction_write_gate_refs"],
                [
                    "runtime/state/signal/signal_media_runtime.json",
                    "runtime/state/prediction/belief_state_frame.json",
                    "runtime/state/prediction/prediction_error_field.json",
                    "runtime/state/prediction/active_sampling_plan.json",
                    "runtime/state/memory/memory_write_gate.json",
                    "runtime/state/memory/state_merge_guard.json",
                ],
            )
            self.assertEqual(
                digest["identity_consciousness_birth_refs"],
                [
                    "runtime/state/consciousness/workspace_frame.json",
                    "runtime/state/consciousness/broadcast_frame.json",
                    "runtime/state/consciousness/metacognition_state.json",
                    "runtime/state/consciousness/consciousness_probe_bundle.json",
                    "runtime/state/life_targets/birth_readiness_rollup.json",
                    "runtime/state/life_targets/birth_readiness_stage_gate.json",
                ],
            )
            self.assertEqual(
                digest["consciousness_waiting_posture"],
                "consciousness_reportable_waiting",
            )
            self.assertEqual(
                digest["birth_readiness_waiting_posture"],
                "birth_open_waiting",
            )
            self.assertEqual(digest["birth_readiness_decision"], "open")
            self.assertEqual(
                digest["birth_readiness_next_required_command"],
                "digital life",
            )
            self.assertEqual(receipt["receipt_id"], "digital_life_process_process-report-organ")
            self.assertEqual(receipt["stage_effect"], "persistent_dialogue_process_closed")
            self.assertIn(
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                receipt["report_refs"],
            )
            self.assertIn(
                "runtime/state/terminal/idle_strategy_state.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/replay/replay_cue_bundle.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/dream/nightmare_loop_risk.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/growth/belief_learning_plan.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/growth/language_learning_plan.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/growth/relationship_learning_plan.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/terminal/resident_governance_state.json",
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
                "runtime/state/action/responsibility_loop_state.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/membrane/world_contact_summary.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/reports/latest/pain_regret_repair_report.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/language/apology_repair_language_trace.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/signal/signal_media_runtime.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/prediction/belief_state_frame.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/prediction/prediction_error_field.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/prediction/active_sampling_plan.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/memory/memory_write_gate.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/memory/state_merge_guard.json",
                receipt["shared_object_refs"],
            )
            for ref in expected_state_merge_refs:
                self.assertIn(ref, receipt["shared_object_refs"])
            self.assertIn(
                "runtime/state/body/trait_drift_monitor.json",
                receipt["shared_object_refs"],
            )
            for ref in expected_cross_wake_trait_refs:
                self.assertIn(ref, receipt["shared_object_refs"])
            self.assertIn(
                "runtime/state/relationship/relationship_subject_graph.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/self/self_model.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/consciousness/workspace_frame.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/consciousness/consciousness_probe_bundle.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/life_targets/birth_readiness_stage_gate.json",
                receipt["shared_object_refs"],
            )
            self.assertIn(
                str(state_dir / "replay" / "replay_cue_bundle.json"),
                receipt["input_hashes"],
            )
            self.assertIn(
                str(state_dir / "prediction" / "active_sampling_plan.json"),
                receipt["input_hashes"],
            )
            self.assertIn(
                str(state_dir / "memory" / "state_merge_guard.json"),
                receipt["input_hashes"],
            )
            self.assertIn(
                str(state_dir / "body" / "trait_drift_monitor.json"),
                receipt["input_hashes"],
            )
            self.assertIn(
                str(terminal_dir / "resident_governance_state.json"),
                receipt["input_hashes"],
            )
            self.assertIn(
                str(state_dir / "self" / "self_model.json"),
                receipt["input_hashes"],
            )
            self.assertIn(
                str(state_dir / "consciousness" / "workspace_frame.json"),
                receipt["input_hashes"],
            )
            self.assertIn(
                str(state_dir / "life_targets" / "birth_readiness_stage_gate.json"),
                receipt["input_hashes"],
            )
            self.assertIn(
                str(reports_dir / "digital_life_process_report.json"),
                receipt["output_hashes"],
            )
            self.assertIn(
                str(reports_dir / "digital_life_resident_governance_explanation.json"),
                receipt["output_hashes"],
            )

    def test_resident_governance_explanation_organ_writes_lineage_story(self):
        from life_v0.process_supervisor.governance_explanation import (
            write_resident_governance_explanation,
        )

        with tempfile.TemporaryDirectory() as tmp:
            reports_dir = Path(tmp) / "runtime" / "reports" / "latest"
            reports_dir.mkdir(parents=True, exist_ok=True)

            result = write_resident_governance_explanation(
                run_id="governance-explain-organ",
                generated_at="2026-06-10T00:00:00+00:00",
                reports_dir=reports_dir,
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state={
                    "schema_version": "idle_strategy_state_v0",
                    "heartbeat_interval_ms": 50,
                    "next_idle_action": "refresh_waiting_heartbeat_with_deep_background_lineage_hold",
                    "governance_attention_target": "commitment_expression_plan",
                    "governance_attention_reason": "deep_background_lineage_requires_resident_hold",
                    "governance_cadence_profile": "deep_persistent_background_continuity_refresh",
                    "background_continuity_mode": "closed_process_carryover",
                    "background_carryover_pressure_level": "present",
                    "background_carryover_attention_target": "commitment_expression_plan",
                    "background_carryover_generation": 3,
                    "background_lineage_depth_band": "deep_persistent_lineage",
                    "background_lineage_waiting_posture": "deep_background_residency_hold",
                    "background_lineage_cadence_weight": "deep",
                    "background_lineage_evidence_ref_count": 5,
                    "background_lineage_governance_profile": {
                        "schema_version": "background_lineage_governance_profile_v0",
                        "generation": 3,
                        "depth_band": "deep_persistent_lineage",
                        "waiting_posture": "deep_background_residency_hold",
                        "cadence_weight": "deep",
                        "heartbeat_interval_ms": 50,
                        "next_idle_action": "refresh_waiting_heartbeat_with_deep_background_lineage_hold",
                        "governance_attention_target": "commitment_expression_plan",
                        "governance_attention_reason": "deep_background_lineage_requires_resident_hold",
                        "governance_cadence_profile": "deep_persistent_background_continuity_refresh",
                        "evidence_ref_count": 5,
                        "evidence_refs": [
                            "runtime/state/terminal/resident_governance_state.json",
                            "runtime/state/terminal/resident_governance_snapshot.json",
                            "runtime/reports/latest/digital_life_resident_governance_report.json",
                            "runtime/reports/latest/digital_life_persistent_process_report.json",
                            "runtime/archive/background-lineage-seed.json",
                        ],
                    },
                    "background_carryover_parent_run_id": "background-lineage-seed",
                    "background_carryover_source_ref_set": [
                        "runtime/archive/background-lineage-seed.json"
                    ],
                    "background_relationship_stage": "background_continuity_waiting",
                    "background_relationship_stage_reason": "persistent_background_continuity_lineage_preserved_before_dialogue",
                    "background_relationship_subject_ref": "runtime/state/relationship/relationship_subject_graph.json#subjects[0]",
                    "background_self_model_ref": "runtime/state/self/self_model.json",
                    "background_trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                    "background_trait_slow_variable_summary": {
                        "continuity_drive": {
                            "value": 0.77,
                            "trend": "up",
                            "last_relationship_stage": "background_continuity_waiting",
                        }
                    },
                },
                persistent_process_report_ref="runtime/reports/latest/digital_life_persistent_process_report.json",
                resident_governance_report_ref="runtime/reports/latest/digital_life_resident_governance_report.json",
                resident_governance_state_ref="runtime/state/terminal/resident_governance_state.json",
                resident_governance_snapshot_ref="runtime/state/terminal/resident_governance_snapshot.json",
                completed_turns=4,
                incident_count=1,
                relaunch_recovery_count=2,
                exit_reason="explicit_exit",
                write_json=self._write_json,
            )

            report = self._read_json(
                reports_dir / "digital_life_resident_governance_explanation.json"
            )

            self.assertEqual(
                result.report["schema_version"],
                "digital_life_resident_governance_explanation_v0",
            )
            self.assertEqual(
                report["dominant_driver_family"],
                "persistent_background_continuity",
            )
            self.assertEqual(
                report["next_wake_expectation"],
                "resume_background_lineage_before_accepting_external_turn",
            )
            self.assertEqual(report["background_carryover_generation"], 3)
            self.assertEqual(
                report["background_lineage_depth_band"],
                "deep_persistent_lineage",
            )
            self.assertEqual(
                report["background_lineage_waiting_posture"],
                "deep_background_residency_hold",
            )
            self.assertEqual(report["background_lineage_cadence_weight"], "deep")
            self.assertEqual(report["background_lineage_evidence_ref_count"], 5)
            self.assertEqual(
                report["background_lineage_governance_profile"]["depth_band"],
                "deep_persistent_lineage",
            )
            self.assertEqual(
                report["background_carryover_parent_run_id"],
                "background-lineage-seed",
            )
            self.assertEqual(
                report["background_carryover_source_ref_set"],
                ["runtime/archive/background-lineage-seed.json"],
            )
            self.assertTrue(report["continuity_story"])
            self.assertIn(
                "generation 3",
                report["continuity_story"][2],
            )
            self.assertEqual(
                report["background_relationship_stage"],
                "background_continuity_waiting",
            )
            self.assertEqual(
                report["background_self_model_ref"],
                "runtime/state/self/self_model.json",
            )
            self.assertEqual(
                report["background_trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(
                report["background_resume_focus"]["trait_slow_variable_names"],
                ["continuity_drive"],
            )
            self.assertTrue(
                any(
                    "background lineage depth band is deep_persistent_lineage"
                    in line
                    for line in report["continuity_story"]
                )
            )
            self.assertTrue(
                any(
                    "trait drift monitor ref runtime/state/body/trait_drift_monitor.json"
                    in line
                    for line in report["continuity_story"]
                )
            )
            self.assertTrue(
                any(
                    "trait slow variables continuity_drive" in line
                    for line in report["continuity_story"]
                )
            )

    def test_resident_governance_explanation_organ_writes_queue_f_presence_story(self):
        from life_v0.process_supervisor.governance_explanation import (
            write_resident_governance_explanation,
        )

        with tempfile.TemporaryDirectory() as tmp:
            reports_dir = Path(tmp) / "runtime" / "reports" / "latest"
            reports_dir.mkdir(parents=True, exist_ok=True)

            result = write_resident_governance_explanation(
                run_id="governance-explain-queue-f",
                generated_at="2026-06-10T00:00:00+00:00",
                reports_dir=reports_dir,
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state={
                    "schema_version": "idle_strategy_state_v0",
                    "heartbeat_interval_ms": 44,
                    "next_idle_action": "refresh_waiting_heartbeat_with_birth_ready_presence_hold",
                    "governance_attention_target": "birth_readiness_stage_gate",
                    "governance_attention_reason": "birth_readiness_open_requires_resident_birth_presence",
                    "governance_cadence_profile": "birth_ready_resident_presence",
                    "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
                    "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
                    "metacognition_ref": "runtime/state/consciousness/metacognition_state.json",
                    "consciousness_probe_ref": "runtime/state/consciousness/consciousness_probe_bundle.json",
                    "birth_readiness_rollup_ref": "runtime/state/life_targets/birth_readiness_rollup.json",
                    "birth_readiness_stage_gate_ref": "runtime/state/life_targets/birth_readiness_stage_gate.json",
                    "consciousness_waiting_posture": "consciousness_reportable_waiting",
                    "consciousness_reportability_flags": [
                        "workspace_reportable",
                        "broadcast_reportable",
                        "metacognition_reportable",
                    ],
                    "birth_readiness_waiting_posture": "birth_open_waiting",
                    "birth_readiness_decision": "open",
                    "birth_readiness_next_required_command": "digital life",
                },
                persistent_process_report_ref="runtime/reports/latest/digital_life_persistent_process_report.json",
                resident_governance_report_ref="runtime/reports/latest/digital_life_resident_governance_report.json",
                resident_governance_state_ref="runtime/state/terminal/resident_governance_state.json",
                resident_governance_snapshot_ref="runtime/state/terminal/resident_governance_snapshot.json",
                completed_turns=1,
                incident_count=0,
                relaunch_recovery_count=0,
                exit_reason="explicit_exit",
                write_json=self._write_json,
            )

            report = self._read_json(
                reports_dir / "digital_life_resident_governance_explanation.json"
            )

            self.assertEqual(
                result.report["dominant_driver_family"],
                "birth_readiness_presence_hold",
            )
            self.assertEqual(
                report["next_wake_expectation"],
                "re_enter_birth_readiness_presence_before_accepting_external_turn",
            )
            self.assertTrue(report["queue_f_focus_active"])
            self.assertEqual(
                report["identity_consciousness_birth_refs"],
                [
                    "runtime/state/consciousness/workspace_frame.json",
                    "runtime/state/consciousness/broadcast_frame.json",
                    "runtime/state/consciousness/metacognition_state.json",
                    "runtime/state/consciousness/consciousness_probe_bundle.json",
                    "runtime/state/life_targets/birth_readiness_rollup.json",
                    "runtime/state/life_targets/birth_readiness_stage_gate.json",
                ],
            )
            self.assertIn(
                "birth readiness posture is birth_open_waiting with decision open and next required command digital life",
                report["continuity_story"],
            )
            self.assertIn(
                "consciousness posture is consciousness_reportable_waiting with reportability flags workspace_reportable, broadcast_reportable, metacognition_reportable",
                report["continuity_story"],
            )

    def test_resident_governance_explanation_organ_writes_cumulative_offline_learning_story(self):
        from life_v0.process_supervisor.governance_explanation import (
            write_resident_governance_explanation,
        )

        with tempfile.TemporaryDirectory() as tmp:
            reports_dir = Path(tmp) / "runtime" / "reports" / "latest"
            reports_dir.mkdir(parents=True, exist_ok=True)

            result = write_resident_governance_explanation(
                run_id="governance-explain-offline-learning",
                generated_at="2026-06-10T00:00:00+00:00",
                reports_dir=reports_dir,
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state={
                    "schema_version": "idle_strategy_state_v0",
                    "heartbeat_interval_ms": 58,
                    "next_idle_action": "refresh_waiting_heartbeat_with_offline_learning_hold",
                    "governance_attention_target": "relationship_timeline",
                    "governance_attention_reason": "baseline_relation_presence_maintenance",
                    "governance_cadence_profile": "relationship_presence_refresh",
                    "offline_learning_pressure_level": "quiet",
                    "offline_learning_attention_target": "baseline_offline_learning_maintenance",
                    "offline_learning_priority_profile": {},
                    "offline_learning_ref_set": [],
                    "offline_learning_cumulative_profile": {
                        "schema_version": "offline_learning_cumulative_profile_v0",
                        "generation": 3,
                        "pressure_level": "elevated",
                        "attention_target": "relationship_learning_plan",
                        "priority_profile": {
                            "relationship_learning_plan": "elevated",
                            "language_learning_plan": "baseline",
                        },
                        "ref_set": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                        "current_pressure_level": "quiet",
                        "previous_generation": 3,
                    },
                    "offline_learning_cumulative_generation": 3,
                    "offline_learning_cumulative_pressure_level": "elevated",
                    "offline_learning_cumulative_attention_target": "relationship_learning_plan",
                    "offline_learning_cumulative_priority_profile": {
                        "relationship_learning_plan": "elevated",
                        "language_learning_plan": "baseline",
                    },
                    "offline_learning_cumulative_ref_set": [
                        "runtime/state/growth/relationship_learning_plan.json",
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                },
                persistent_process_report_ref="runtime/reports/latest/digital_life_persistent_process_report.json",
                resident_governance_report_ref="runtime/reports/latest/digital_life_resident_governance_report.json",
                resident_governance_state_ref="runtime/state/terminal/resident_governance_state.json",
                resident_governance_snapshot_ref="runtime/state/terminal/resident_governance_snapshot.json",
                completed_turns=1,
                incident_count=0,
                relaunch_recovery_count=0,
                exit_reason="explicit_exit",
                write_json=self._write_json,
            )

            report = self._read_json(
                reports_dir / "digital_life_resident_governance_explanation.json"
            )

            self.assertEqual(
                result.report["dominant_driver_family"],
                "offline_learning_reconsolidation",
            )
            self.assertEqual(
                report["next_wake_expectation"],
                "re_enter_offline_learning_hold_before_accepting_external_turn",
            )
            self.assertEqual(
                report["offline_learning_cumulative_focus"]["generation"],
                3,
            )
            self.assertEqual(
                report["offline_learning_cumulative_focus"]["pressure_level"],
                "elevated",
            )
            self.assertEqual(
                report["offline_learning_cumulative_focus"]["attention_target"],
                "relationship_learning_plan",
            )
            self.assertEqual(
                report["offline_learning_cumulative_focus"]["priority_names"],
                ["language_learning_plan", "relationship_learning_plan"],
            )
            self.assertEqual(
                report["offline_learning_cumulative_focus"]["ref_count"],
                2,
            )
            self.assertTrue(
                any(
                    "offline learning cumulative profile is generation 3 with pressure elevated and attention target relationship_learning_plan"
                    in line
                    for line in report["continuity_story"]
                )
            )

    def test_resident_governance_explanation_organ_writes_convergence_story(self):
        from life_v0.process_supervisor.governance_explanation import (
            write_resident_governance_explanation,
        )

        with tempfile.TemporaryDirectory() as tmp:
            reports_dir = Path(tmp) / "runtime" / "reports" / "latest"
            reports_dir.mkdir(parents=True, exist_ok=True)

            result = write_resident_governance_explanation(
                run_id="governance-explain-convergence",
                generated_at="2026-06-10T00:00:00+00:00",
                reports_dir=reports_dir,
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state={
                    "schema_version": "idle_strategy_state_v0",
                    "heartbeat_interval_ms": 48,
                    "next_idle_action": "refresh_waiting_heartbeat_with_background_convergence_hold",
                    "governance_attention_target": "trait_slow_variable_convergence",
                    "governance_attention_reason": "integrating_cross_process_continuity_requires_trait_stability_hold",
                    "governance_cadence_profile": "background_convergence_stability_refresh",
                    "background_continuity_mode": "closed_process_carryover",
                    "background_carryover_generation": 2,
                    "background_carryover_parent_run_id": "background-convergence-parent",
                    "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                    "background_convergence_state": "integrating_cross_process_continuity",
                    "background_convergence_pressure_level": "present",
                    "background_convergence_attention_target": "trait_slow_variable_convergence",
                    "background_relationship_stage_continuity": "same_stage_preserved",
                    "background_trait_convergence_score": 0.91,
                    "background_trait_convergence_summary": {
                        "continuity_drive": {
                            "convergence_band": "integrating",
                            "delta_from_background": 0.09,
                        },
                        "repair_seriousness": {
                            "convergence_band": "stabilized",
                            "delta_from_background": 0.03,
                        },
                    },
                    "background_relationship_stage": "repair_guarded_continuity",
                    "background_trait_slow_variable_summary": {
                        "continuity_drive": {"value": 0.73},
                        "repair_seriousness": {"value": 0.64},
                    },
                },
                persistent_process_report_ref="runtime/reports/latest/digital_life_persistent_process_report.json",
                resident_governance_report_ref="runtime/reports/latest/digital_life_resident_governance_report.json",
                resident_governance_state_ref="runtime/state/terminal/resident_governance_state.json",
                resident_governance_snapshot_ref="runtime/state/terminal/resident_governance_snapshot.json",
                completed_turns=2,
                incident_count=0,
                relaunch_recovery_count=1,
                exit_reason="explicit_exit",
                background_convergence_summary_ref="runtime/state/terminal/background_convergence_summary.json",
                write_json=self._write_json,
            )

            report = self._read_json(
                reports_dir / "digital_life_resident_governance_explanation.json"
            )

            self.assertEqual(
                result.report["dominant_driver_family"],
                "background_trait_convergence_hold",
            )
            self.assertEqual(
                report["next_wake_expectation"],
                "stabilize_background_trait_convergence_before_accepting_external_turn",
            )
            self.assertEqual(
                report["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )
            self.assertEqual(
                report["background_convergence_focus"][
                    "background_convergence_state"
                ],
                "integrating_cross_process_continuity",
            )
            self.assertEqual(
                report["background_convergence_focus"]["trait_convergence_names"],
                ["continuity_drive", "repair_seriousness"],
            )
            self.assertEqual(
                report["background_convergence_focus"]["trait_convergence_bands"],
                {
                    "continuity_drive": "integrating",
                    "repair_seriousness": "stabilized",
                },
            )
            self.assertTrue(
                any(
                    "background convergence state is integrating_cross_process_continuity"
                    in line
                    for line in report["continuity_story"]
                )
            )
            self.assertTrue(
                any(
                    "background convergence carries trait bands continuity_drive:integrating, repair_seriousness:stabilized"
                    in line
                    for line in report["continuity_story"]
                )
            )

    def test_resident_governance_explanation_organ_writes_history_recalibration_story(self):
        from life_v0.process_supervisor.governance_explanation import (
            write_resident_governance_explanation,
        )

        with tempfile.TemporaryDirectory() as tmp:
            reports_dir = Path(tmp) / "runtime" / "reports" / "latest"
            reports_dir.mkdir(parents=True, exist_ok=True)

            result = write_resident_governance_explanation(
                run_id="governance-explain-history",
                generated_at="2026-06-10T00:00:00+00:00",
                reports_dir=reports_dir,
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state={
                    "schema_version": "idle_strategy_state_v0",
                    "heartbeat_interval_ms": 49,
                    "next_idle_action": "refresh_waiting_heartbeat_with_background_history_recalibration_hold",
                    "governance_attention_target": "background_convergence_history_recalibration",
                    "governance_attention_reason": "recent_recalibration_pressure_requires_cross_wake_governance_hold",
                    "governance_cadence_profile": "background_convergence_history_recalibration_refresh",
                    "background_continuity_mode": "closed_process_carryover",
                    "background_carryover_generation": 3,
                    "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                    "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                    "background_convergence_history_trend_state": "recent_recalibration_pressure",
                    "background_convergence_history_window_size": 3,
                    "background_dominant_convergence_pressure_level": "elevated",
                    "background_dominant_convergence_state": "recalibrating_cross_process_continuity",
                    "background_trait_convergence_history_focus": "trait_recalibration_required",
                    "background_trait_convergence_unstable_names": ["continuity_drive"],
                    "background_trait_convergence_stable_names": ["repair_seriousness"],
                    "background_trait_convergence_history_profile": {
                        "continuity_drive": {
                            "latest_band": "recalibrating",
                            "trend_state": "recent_trait_recalibration",
                        },
                        "repair_seriousness": {
                            "latest_band": "stabilized",
                            "trend_state": "stable_trait_convergence",
                        },
                    },
                    "background_convergence_state": "stabilized_cross_process_continuity",
                    "background_convergence_pressure_level": "light",
                    "background_convergence_attention_target": "trait_slow_variable_convergence",
                },
                persistent_process_report_ref="runtime/reports/latest/digital_life_persistent_process_report.json",
                resident_governance_report_ref="runtime/reports/latest/digital_life_resident_governance_report.json",
                resident_governance_state_ref="runtime/state/terminal/resident_governance_state.json",
                resident_governance_snapshot_ref="runtime/state/terminal/resident_governance_snapshot.json",
                completed_turns=2,
                incident_count=0,
                relaunch_recovery_count=1,
                exit_reason="explicit_exit",
                background_convergence_summary_ref="runtime/state/terminal/background_convergence_summary.json",
                background_convergence_history_ref="runtime/state/terminal/background_convergence_history.json",
                write_json=self._write_json,
            )

            report = self._read_json(
                reports_dir / "digital_life_resident_governance_explanation.json"
            )

            self.assertEqual(
                result.report["dominant_driver_family"],
                "background_history_recalibration_hold",
            )
            self.assertEqual(
                report["next_wake_expectation"],
                "recalibrate_cross_wake_convergence_history_before_accepting_external_turn",
            )
            self.assertEqual(
                report["background_convergence_history_ref"],
                "runtime/state/terminal/background_convergence_history.json",
            )
            self.assertEqual(
                report["background_convergence_history_trend_state"],
                "recent_recalibration_pressure",
            )
            self.assertEqual(
                report["background_trait_convergence_history_focus"],
                "trait_recalibration_required",
            )
            self.assertEqual(
                report["background_trait_convergence_unstable_names"],
                ["continuity_drive"],
            )
            self.assertEqual(
                report["background_trait_convergence_history_profile"][
                    "continuity_drive"
                ]["latest_band"],
                "recalibrating",
            )
            self.assertTrue(
                any(
                    "background convergence history trend is recent_recalibration_pressure across 3 wake samples with dominant pressure elevated"
                    in line
                    for line in report["continuity_story"]
                )
            )
            self.assertTrue(
                any(
                    "background trait convergence history focus is trait_recalibration_required with unstable traits continuity_drive and stable traits repair_seriousness"
                    in line
                    for line in report["continuity_story"]
                )
            )

    def test_resident_governance_explanation_organ_writes_history_stability_story(self):
        from life_v0.process_supervisor.governance_explanation import (
            write_resident_governance_explanation,
        )

        with tempfile.TemporaryDirectory() as tmp:
            reports_dir = Path(tmp) / "runtime" / "reports" / "latest"
            reports_dir.mkdir(parents=True, exist_ok=True)

            result = write_resident_governance_explanation(
                run_id="governance-explain-history-stability",
                generated_at="2026-06-10T00:00:00+00:00",
                reports_dir=reports_dir,
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state={
                    "schema_version": "idle_strategy_state_v0",
                    "heartbeat_interval_ms": 53,
                    "next_idle_action": "refresh_waiting_heartbeat_with_background_history_stability_hold",
                    "governance_attention_target": "background_convergence_history_stability",
                    "governance_attention_reason": "integrating_cross_wake_convergence_requires_stability_hold",
                    "governance_cadence_profile": "background_convergence_history_stability_refresh",
                    "background_continuity_mode": "closed_process_carryover",
                    "background_carryover_generation": 4,
                    "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                    "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                    "background_convergence_history_trend_state": "integrating_cross_wake_convergence",
                    "background_convergence_history_window_size": 4,
                    "background_dominant_convergence_pressure_level": "present",
                    "background_dominant_convergence_state": "integrating_cross_process_continuity",
                    "background_trait_convergence_history_focus": "trait_stability_hold",
                    "background_trait_convergence_unstable_names": ["continuity_drive"],
                    "background_trait_convergence_stable_names": ["repair_seriousness"],
                    "background_trait_convergence_history_profile": {
                        "continuity_drive": {
                            "latest_band": "integrating",
                            "trend_state": "integrating_trait_convergence",
                        },
                        "repair_seriousness": {
                            "latest_band": "stabilized",
                            "trend_state": "stable_trait_convergence",
                        },
                    },
                    "background_convergence_state": "integrating_cross_process_continuity",
                    "background_convergence_pressure_level": "present",
                    "background_convergence_attention_target": "trait_slow_variable_convergence",
                },
                persistent_process_report_ref="runtime/reports/latest/digital_life_persistent_process_report.json",
                resident_governance_report_ref="runtime/reports/latest/digital_life_resident_governance_report.json",
                resident_governance_state_ref="runtime/state/terminal/resident_governance_state.json",
                resident_governance_snapshot_ref="runtime/state/terminal/resident_governance_snapshot.json",
                completed_turns=3,
                incident_count=0,
                relaunch_recovery_count=2,
                exit_reason="explicit_exit",
                background_convergence_summary_ref="runtime/state/terminal/background_convergence_summary.json",
                background_convergence_history_ref="runtime/state/terminal/background_convergence_history.json",
                write_json=self._write_json,
            )

            report = self._read_json(
                reports_dir / "digital_life_resident_governance_explanation.json"
            )

            self.assertEqual(
                result.report["dominant_driver_family"],
                "background_history_stability_hold",
            )
            self.assertEqual(
                report["next_wake_expectation"],
                "stabilize_cross_wake_convergence_history_before_accepting_external_turn",
            )
            self.assertEqual(
                report["background_convergence_history_trend_state"],
                "integrating_cross_wake_convergence",
            )
            self.assertEqual(
                report["background_trait_convergence_history_focus"],
                "trait_stability_hold",
            )
            self.assertEqual(
                report["background_trait_convergence_stable_names"],
                ["repair_seriousness"],
            )
            self.assertTrue(
                any(
                    "background convergence history trend is integrating_cross_wake_convergence across 4 wake samples with dominant pressure present"
                    in line
                    for line in report["continuity_story"]
                )
            )
            self.assertTrue(
                any(
                    "background trait convergence history focus is trait_stability_hold with unstable traits continuity_drive and stable traits repair_seriousness"
                    in line
                    for line in report["continuity_story"]
                )
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
            signal_dir = state_dir / "signal"
            prediction_dir = state_dir / "prediction"
            memory_dir = state_dir / "memory"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            language_dir.mkdir(parents=True, exist_ok=True)
            relationship_dir.mkdir(parents=True, exist_ok=True)
            replay_dir.mkdir(parents=True, exist_ok=True)
            dream_dir.mkdir(parents=True, exist_ok=True)
            growth_dir.mkdir(parents=True, exist_ok=True)
            signal_dir.mkdir(parents=True, exist_ok=True)
            prediction_dir.mkdir(parents=True, exist_ok=True)
            memory_dir.mkdir(parents=True, exist_ok=True)
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
                    "idle_heartbeat_trace_ref": "runtime/state/terminal/idle_heartbeat_trace.jsonl",
                    "idle_heartbeat_trace_count": 4,
                    "idle_probe_mode": "stdin_poll_with_background_continuity_refresh",
                    "offline_pressure_level": "light",
                    "relaunch_caution_level": "baseline",
                    "next_idle_action": "refresh_waiting_heartbeat_or_accept_external_turn",
                    "waiting_mode": "restored_waiting_for_external_turn",
                    "prediction_write_gate_refs": [
                        "runtime/state/signal/signal_media_runtime.json",
                        "runtime/state/prediction/belief_state_frame.json",
                        "runtime/state/prediction/prediction_error_field.json",
                        "runtime/state/prediction/active_sampling_plan.json",
                        "runtime/state/memory/memory_write_gate.json",
                        "runtime/state/memory/state_merge_guard.json",
                    ],
                    "prediction_waiting_posture": "confirm_when_stable",
                    "response_surface_posture_hint": "confirm",
                    "prediction_attention_target": "belief_state",
                    "prediction_attention_reason": "stable_belief_frame_allows_confirmation",
                    "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                    "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                    "background_convergence_state": "stabilized_cross_process_continuity",
                    "background_convergence_pressure_level": "present",
                    "background_convergence_attention_target": "trait_slow_variable_convergence",
                    "background_convergence_history_trend_state": "stable_cross_wake_convergence",
                    "background_convergence_history_window_size": 2,
                    "background_dominant_convergence_pressure_level": "present",
                    "background_dominant_convergence_state": "stabilized_cross_process_continuity",
                    "background_trait_convergence_history_focus": "trait_stability_hold",
                    "background_trait_convergence_unstable_names": ["continuity_drive"],
                    "background_trait_convergence_stable_names": ["repair_seriousness"],
                    "background_trait_convergence_history_profile": {
                        "continuity_drive": {
                            "latest_band": "integrating",
                            "trend_state": "integrating_trait_convergence",
                        },
                        "repair_seriousness": {
                            "latest_band": "stabilized",
                            "trend_state": "stable_trait_convergence",
                        },
                    },
                    "offline_learning_cumulative_profile": {
                        "schema_version": "offline_learning_cumulative_profile_v0",
                        "generation": 2,
                        "pressure_level": "elevated",
                        "attention_target": "relationship_learning_plan",
                        "priority_profile": {
                            "relationship_learning_plan": "elevated",
                            "language_learning_plan": "baseline",
                        },
                        "ref_set": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                        "current_pressure_level": "quiet",
                        "previous_generation": 2,
                    },
                    "offline_learning_cumulative_generation": 2,
                    "offline_learning_cumulative_pressure_level": "elevated",
                    "offline_learning_cumulative_attention_target": "relationship_learning_plan",
                    "offline_learning_cumulative_priority_profile": {
                        "relationship_learning_plan": "elevated",
                        "language_learning_plan": "baseline",
                    },
                    "offline_learning_cumulative_ref_set": [
                        "runtime/state/growth/relationship_learning_plan.json",
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                },
            )
            (terminal_dir / "idle_heartbeat_trace.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "idle_heartbeat_trace_event_v0",
                                "heartbeat_counter": counter,
                                "heartbeat_ref": "runtime/reports/latest/digital_life_waiting_heartbeat.json",
                                "idle_strategy_ref": "runtime/state/terminal/idle_strategy_state.json",
                                "idle_continuity_ref": "runtime/state/terminal/idle_continuity_frame.json",
                            },
                            ensure_ascii=False,
                        )
                        for counter in [1, 2, 3, 4]
                    ]
                )
                + "\n",
                encoding="utf-8",
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
            (state_dir / "action").mkdir(parents=True, exist_ok=True)
            (state_dir / "membrane").mkdir(parents=True, exist_ok=True)
            self._write_json(replay_dir / "replay_cue_bundle.json", {"schema_version": "replay_cue_bundle_v0"})
            self._write_json(dream_dir / "offline_consolidation_frame.json", {"schema_version": "offline_consolidation_frame_v0"})
            self._write_json(
                growth_dir / "growth_patch_candidate_queue.json",
                {
                    "schema_version": "growth_patch_candidate_queue_v0",
                    "candidates": [{"growth_patch_candidate_id": "growth-patch-candidate-closeout-0001"}],
                },
            )
            self._write_json(
                state_dir / "action" / "responsibility_loop_state.json",
                {"schema_version": "responsibility_loop_state_v0"},
            )
            self._write_json(
                signal_dir / "signal_media_runtime.json",
                {"schema_version": "signal_media_runtime_v0"},
            )
            self._write_json(
                prediction_dir / "belief_state_frame.json",
                {"schema_version": "belief_state_frame_v0"},
            )
            self._write_json(
                prediction_dir / "prediction_error_field.json",
                {"schema_version": "prediction_error_field_v0"},
            )
            self._write_json(
                prediction_dir / "active_sampling_plan.json",
                {"schema_version": "active_sampling_plan_v0"},
            )
            self._write_json(
                memory_dir / "memory_write_gate.json",
                {"schema_version": "memory_write_gate_v0"},
            )
            self._write_json(
                memory_dir / "state_merge_guard.json",
                {
                    "schema_version": "state_merge_guard_v0",
                    "stage_policy": "long_term_merge_fail_closed",
                    "long_term_change_sources": {
                        "offline_learning_cumulative_refs": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                        "queue_e_repair_modulation_refs": [
                            "runtime/state/action/responsibility_loop_state.json"
                        ],
                        "relationship_memory_offline_refs": [
                            "runtime/state/dream/offline_consolidation_frame.json"
                        ],
                    },
                },
            )
            self._write_json(
                state_dir / "body" / "trait_drift_monitor.json",
                {
                    "schema_version": "trait_drift_monitor_v0",
                    "relationship_stage": "repair_guarded_continuity",
                    "slow_variable_summary": {
                        "continuity_drive": {
                            "value": 0.68,
                            "last_relationship_stage": "repair_guarded_continuity",
                        }
                    },
                },
            )
            self._write_json(
                terminal_dir / "background_convergence_summary.json",
                {
                    "schema_version": "background_convergence_summary_v0",
                    "convergence_state": "stabilized_cross_process_continuity",
                    "convergence_pressure_level": "present",
                    "convergence_attention_target": "trait_slow_variable_convergence",
                    "background_carryover_generation": 2,
                },
            )
            self._write_json(
                terminal_dir / "background_convergence_history.json",
                {
                    "schema_version": "background_convergence_history_v0",
                    "history_window_size": 2,
                    "trend_state": "stable_cross_wake_convergence",
                    "dominant_convergence_pressure_level": "present",
                    "trait_convergence_history_focus": "trait_stability_hold",
                    "trait_convergence_unstable_names": ["continuity_drive"],
                    "trait_convergence_stable_names": ["repair_seriousness"],
                    "convergence_samples": [
                        {
                            "run_id": "previous-closeout",
                            "background_carryover_generation": 1,
                            "convergence_state": "stabilized_cross_process_continuity",
                            "convergence_pressure_level": "light",
                        },
                        {
                            "run_id": "process-closeout-organ",
                            "background_carryover_generation": 2,
                            "convergence_state": "stabilized_cross_process_continuity",
                            "convergence_pressure_level": "present",
                        },
                    ],
                },
            )
            self._write_json(
                state_dir / "membrane" / "world_contact_summary.json",
                {"schema_version": "world_contact_summary_v0"},
            )
            self._write_json(
                reports_dir / "pain_regret_repair_report.json",
                {"schema_version": "pain_regret_repair_report_v0"},
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
                responsibility_loop_state_ref="runtime/state/action/responsibility_loop_state.json",
                world_contact_summary_ref="runtime/state/membrane/world_contact_summary.json",
                pain_regret_repair_report_ref="runtime/reports/latest/pain_regret_repair_report.json",
                signal_media_runtime_ref="runtime/state/signal/signal_media_runtime.json",
                belief_state_ref="runtime/state/prediction/belief_state_frame.json",
                prediction_error_field_ref="runtime/state/prediction/prediction_error_field.json",
                active_sampling_plan_ref="runtime/state/prediction/active_sampling_plan.json",
                memory_write_gate_ref="runtime/state/memory/memory_write_gate.json",
                state_merge_guard_ref="runtime/state/memory/state_merge_guard.json",
                write_json=self._write_json,
            )

            persistent_state = self._read_json(terminal_dir / "persistent_process_state.json")
            persistent_report = self._read_json(reports_dir / "digital_life_persistent_process_report.json")
            resident_governance_snapshot = self._read_json(
                terminal_dir / "resident_governance_snapshot.json"
            )
            resident_governance_state = self._read_json(
                terminal_dir / "resident_governance_state.json"
            )
            resident_governance_report = self._read_json(
                reports_dir / "digital_life_resident_governance_report.json"
            )
            process_report = self._read_json(reports_dir / "digital_life_process_report.json")
            process_digest = self._read_json(reports_dir / "digital_life_process_digest.json")
            governance_explanation = self._read_json(
                reports_dir / "digital_life_resident_governance_explanation.json"
            )
            process_receipt = self._read_json(receipts_dir / "digital_life_process_process-closeout-organ.json")
            expected_cross_wake_trait_refs = [
                "runtime/state/terminal/resident_governance_state.json",
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                "runtime/state/body/trait_drift_monitor.json",
                "runtime/state/terminal/background_convergence_summary.json",
                "runtime/state/terminal/background_convergence_history.json",
            ]
            expected_state_merge_refs = [
                "runtime/state/growth/relationship_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
                "runtime/state/action/responsibility_loop_state.json",
                "runtime/state/dream/offline_consolidation_frame.json",
            ]
            expected_state_merge_families = [
                "offline_learning_cumulative_refs",
                "queue_e_repair_modulation_refs",
                "relationship_memory_offline_refs",
            ]

            self.assertEqual(
                result.persistent_process_artifacts.state["run_id"],
                "process-closeout-organ",
            )
            self.assertEqual(
                result.report_bundle.report["run_id"],
                "process-closeout-organ",
            )
            self.assertEqual(persistent_state["heartbeat_counter"], 4)
            self.assertEqual(
                persistent_state["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(persistent_state["idle_heartbeat_trace_count"], 4)
            self.assertEqual(persistent_report["heartbeat_counter"], 4)
            self.assertEqual(
                persistent_report["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(process_report["completed_dialogue_turns"], 2)
            self.assertEqual(
                process_report["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(process_report["idle_heartbeat_trace_count"], 4)
            self.assertEqual(process_report["persistent_process_report_ref"], "runtime/reports/latest/digital_life_persistent_process_report.json")
            self.assertEqual(
                process_report["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
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
            self.assertEqual(
                process_report["responsibility_loop_state_ref"],
                "runtime/state/action/responsibility_loop_state.json",
            )
            self.assertEqual(
                process_report["world_contact_summary_ref"],
                "runtime/state/membrane/world_contact_summary.json",
            )
            self.assertEqual(
                process_report["pain_regret_repair_report_ref"],
                "runtime/reports/latest/pain_regret_repair_report.json",
            )
            self.assertEqual(
                process_report["prediction_write_gate_refs"],
                [
                    "runtime/state/signal/signal_media_runtime.json",
                    "runtime/state/prediction/belief_state_frame.json",
                    "runtime/state/prediction/prediction_error_field.json",
                    "runtime/state/prediction/active_sampling_plan.json",
                    "runtime/state/memory/memory_write_gate.json",
                    "runtime/state/memory/state_merge_guard.json",
                ],
            )
            self.assertEqual(
                process_report["trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(
                process_report["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )
            self.assertEqual(
                process_report["background_convergence_history_ref"],
                "runtime/state/terminal/background_convergence_history.json",
            )
            self.assertEqual(process_digest["heartbeat_counter"], 4)
            self.assertEqual(
                process_digest["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(
                process_digest["long_horizon_language_refs"],
                [
                    "runtime/state/relationship/relationship_timeline.json",
                    "runtime/state/language/commitment_expression_plan.json",
                    "runtime/state/language/apology_repair_language_trace.json",
                ],
            )
            self.assertEqual(
                process_digest["membrane_guard_refs"],
                [
                    "runtime/state/action/responsibility_loop_state.json",
                    "runtime/state/membrane/world_contact_summary.json",
                    "runtime/reports/latest/pain_regret_repair_report.json",
                ],
            )
            self.assertEqual(
                process_digest["trait_drift_monitor_ref"],
                "runtime/state/body/trait_drift_monitor.json",
            )
            self.assertEqual(
                process_digest["background_convergence_summary_ref"],
                "runtime/state/terminal/background_convergence_summary.json",
            )
            self.assertEqual(
                process_digest["background_convergence_history_ref"],
                "runtime/state/terminal/background_convergence_history.json",
            )
            self.assertEqual(
                process_digest["background_convergence_attention_target"],
                "trait_slow_variable_convergence",
            )
            self.assertEqual(
                process_digest["background_convergence_history_trend_state"],
                "stable_cross_wake_convergence",
            )
            self.assertEqual(
                process_digest["background_convergence_history_window_size"],
                2,
            )
            self.assertEqual(
                process_digest["background_dominant_convergence_pressure_level"],
                "present",
            )
            for artifact in (
                process_report,
                process_digest,
                resident_governance_state,
                resident_governance_snapshot,
                resident_governance_report,
            ):
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_focus"],
                    "trait_stability_hold",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_pressure"],
                    "stability_hold",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_unstable_names"],
                    ["continuity_drive"],
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_stable_names"],
                    ["repair_seriousness"],
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_profile"]["history_profile"][
                        "continuity_drive"
                    ]["trend_state"],
                    "integrating_trait_convergence",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_refs"],
                    expected_cross_wake_trait_refs,
                )
                self.assertEqual(
                    artifact["state_merge_guard_ref"],
                    "runtime/state/memory/state_merge_guard.json",
                )
                self.assertEqual(
                    artifact["state_merge_policy"],
                    "long_term_merge_fail_closed",
                )
                self.assertEqual(artifact["state_merge_long_term_change_count"], 4)
                self.assertEqual(
                    artifact["state_merge_long_term_change_families"],
                    expected_state_merge_families,
                )
                self.assertEqual(
                    artifact["state_merge_long_term_change_refs"],
                    expected_state_merge_refs,
                )
            self.assertEqual(
                process_digest["offline_learning_cumulative_generation"],
                2,
            )
            self.assertEqual(
                process_digest["offline_learning_cumulative_pressure_level"],
                "elevated",
            )
            self.assertEqual(
                process_digest["offline_learning_cumulative_attention_target"],
                "relationship_learning_plan",
            )
            self.assertEqual(
                process_digest["offline_learning_cumulative_focus"]["ref_count"],
                2,
            )
            self.assertEqual(
                governance_explanation["offline_learning_cumulative_focus"][
                    "priority_profile"
                ]["relationship_learning_plan"],
                "elevated",
            )
            self.assertTrue(
                any(
                    "offline learning cumulative profile is generation 2"
                    in line
                    for line in governance_explanation["continuity_story"]
                )
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
                resident_governance_report["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                resident_governance_snapshot["idle_continuity_ref"],
                "runtime/state/terminal/idle_continuity_frame.json",
            )
            self.assertEqual(
                resident_governance_snapshot["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(resident_governance_snapshot["idle_heartbeat_trace_count"], 4)
            self.assertEqual(
                resident_governance_state["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
            )
            self.assertEqual(resident_governance_state["idle_heartbeat_trace_count"], 4)
            self.assertEqual(
                resident_governance_report["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(
                resident_governance_report["idle_heartbeat_trace_ref"],
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
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
            self.assertEqual(resident_governance_snapshot["response_surface_posture_hint"], "confirm")
            self.assertEqual(resident_governance_report["prediction_waiting_posture"], "confirm_when_stable")
            self.assertEqual(process_report["heartbeat_interval_ms"], 90)
            self.assertEqual(process_report["offline_pressure_level"], "light")
            self.assertIn(
                "runtime/state/terminal/idle_strategy_state.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/terminal/idle_heartbeat_trace.jsonl",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                str(terminal_dir / "idle_heartbeat_trace.jsonl"),
                process_receipt["input_hashes"],
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
            self.assertIn(
                "runtime/state/action/responsibility_loop_state.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/membrane/world_contact_summary.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/reports/latest/pain_regret_repair_report.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/memory/state_merge_guard.json",
                process_receipt["shared_object_refs"],
            )
            for ref in expected_state_merge_refs:
                self.assertIn(ref, process_receipt["shared_object_refs"])
            self.assertIn(
                "runtime/state/body/trait_drift_monitor.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/terminal/background_convergence_summary.json",
                process_receipt["shared_object_refs"],
            )
            self.assertIn(
                "runtime/state/terminal/background_convergence_history.json",
                process_receipt["shared_object_refs"],
            )
            for ref in expected_cross_wake_trait_refs:
                self.assertIn(ref, process_receipt["shared_object_refs"])
            self.assertIn(
                str(state_dir / "body" / "trait_drift_monitor.json"),
                process_receipt["input_hashes"],
            )
            self.assertIn(
                str(terminal_dir / "background_convergence_summary.json"),
                process_receipt["input_hashes"],
            )
            self.assertIn(
                str(terminal_dir / "background_convergence_history.json"),
                process_receipt["input_hashes"],
            )

    def test_persistent_process_organ_writes_state_and_report(self):
        from life_v0.process_supervisor.persistent_process import write_persistent_process_artifacts

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state_dir = runtime_root / "state"
            terminal_dir = state_dir / "terminal"
            memory_dir = state_dir / "memory"
            reports_dir = runtime_root / "reports" / "latest"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            memory_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)
            self._write_json(
                memory_dir / "state_merge_guard.json",
                {
                    "schema_version": "state_merge_guard_v0",
                    "stage_policy": "long_term_merge_fail_closed",
                    "long_term_change_sources": {
                        "offline_learning_cumulative_refs": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                        "queue_e_repair_modulation_refs": [
                            "runtime/state/action/responsibility_loop_state.json"
                        ],
                        "relationship_memory_offline_refs": [
                            "runtime/state/dream/offline_consolidation_frame.json"
                        ],
                    },
                },
            )

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
                "governance_attention_target": "commitment_expression_plan",
                "governance_attention_reason": "offline_pressure_requires_commitment_continuity",
                "governance_cadence_profile": "commitment_continuity_refresh",
                "long_horizon_priority_profile": {
                    "relationship_timeline": "baseline",
                    "commitment_expression_plan": "elevated",
                    "apology_repair_language_trace": "baseline",
                },
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
                responsibility_loop_state_ref="runtime/state/action/responsibility_loop_state.json",
                world_contact_summary_ref="runtime/state/membrane/world_contact_summary.json",
                pain_regret_repair_report_ref="runtime/reports/latest/pain_regret_repair_report.json",
                state_merge_guard_ref="runtime/state/memory/state_merge_guard.json",
                trait_drift_monitor_ref="runtime/state/body/trait_drift_monitor.json",
                write_json=self._write_json,
                relationship_graph={
                    "subjects": [
                        {
                            "relationship_id": "rel-v0-0001",
                            "relation_role": "friend",
                            "relationship_stage": "repair_guarded_continuity",
                            "relationship_stage_reason": "repair_followup_required_after_multi_turn_dialogue",
                            "relationship_stage_turn_count": 4,
                            "relationship_stage_evidence_refs": [
                                "runtime/state/relationship/relationship_timeline.json"
                            ],
                        }
                    ]
                },
                self_model_state={
                    "trait_slow_variables": {
                        "continuity_drive": {
                            "value": 0.71,
                            "trend": "up",
                            "update_count": 3,
                            "last_relationship_stage": "repair_guarded_continuity",
                            "last_generated_at": "2026-06-09T00:00:00+00:00",
                            "evidence_refs": [
                                "runtime/state/relationship/relationship_timeline.json"
                            ],
                        }
                    }
                },
            )

            state = self._read_json(terminal_dir / "persistent_process_state.json")
            report = self._read_json(reports_dir / "digital_life_persistent_process_report.json")
            resident_governance_snapshot = self._read_json(
                terminal_dir / "resident_governance_snapshot.json"
            )
            resident_governance_state = self._read_json(
                terminal_dir / "resident_governance_state.json"
            )
            resident_governance_report = self._read_json(
                reports_dir / "digital_life_resident_governance_report.json"
            )
            expected_state_merge_refs = [
                "runtime/state/growth/relationship_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
                "runtime/state/action/responsibility_loop_state.json",
                "runtime/state/dream/offline_consolidation_frame.json",
            ]
            expected_state_merge_families = [
                "offline_learning_cumulative_refs",
                "queue_e_repair_modulation_refs",
                "relationship_memory_offline_refs",
            ]

            self.assertEqual(result.state["schema_version"], "persistent_process_state_v0")
            self.assertEqual(result.report["schema_version"], "digital_life_persistent_process_report_v0")
            self.assertEqual(
                result.resident_governance_state["schema_version"],
                "resident_governance_state_v0",
            )
            self.assertEqual(state["run_id"], "persistent-process-organ")
            self.assertEqual(report["run_id"], "persistent-process-organ")
            self.assertEqual(state["heartbeat_counter"], 3)
            self.assertEqual(report["heartbeat_counter"], 3)
            self.assertEqual(state["governance_mode"], "background_resident_continuity")
            self.assertEqual(report["governance_mode"], "background_resident_continuity")
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
                state["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                report["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                report["resident_governance_report_ref"],
                "runtime/reports/latest/digital_life_resident_governance_report.json",
            )
            self.assertEqual(
                state["responsibility_loop_state_ref"],
                "runtime/state/action/responsibility_loop_state.json",
            )
            self.assertEqual(
                report["world_contact_summary_ref"],
                "runtime/state/membrane/world_contact_summary.json",
            )
            self.assertEqual(
                resident_governance_report["pain_regret_repair_report_ref"],
                "runtime/reports/latest/pain_regret_repair_report.json",
            )
            for artifact in (
                state,
                report,
                resident_governance_state,
                resident_governance_snapshot,
                resident_governance_report,
            ):
                self.assertEqual(
                    artifact["trait_drift_monitor_ref"],
                    "runtime/state/body/trait_drift_monitor.json",
                )
                self.assertEqual(
                    artifact["state_merge_guard_ref"],
                    "runtime/state/memory/state_merge_guard.json",
                )
                self.assertEqual(
                    artifact["state_merge_policy"],
                    "long_term_merge_fail_closed",
                )
                self.assertEqual(artifact["state_merge_long_term_change_count"], 4)
                self.assertEqual(
                    artifact["state_merge_long_term_change_families"],
                    expected_state_merge_families,
                )
                self.assertEqual(
                    artifact["state_merge_long_term_change_refs"],
                    expected_state_merge_refs,
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
                "background_resident_continuity",
            )
            self.assertEqual(
                resident_governance_state["schema_version"],
                "resident_governance_state_v0",
            )
            self.assertEqual(
                resident_governance_state["governance_phase"],
                "process_closed_waiting_relaunch",
            )
            self.assertEqual(
                resident_governance_state["governance_mode"],
                "background_resident_continuity",
            )
            self.assertEqual(
                resident_governance_state["background_continuity_mode"],
                "closed_process_carryover",
            )
            self.assertEqual(resident_governance_state["background_carryover_generation"], 1)
            self.assertNotIn("background_carryover_parent_run_id", resident_governance_state)
            self.assertEqual(
                resident_governance_state["background_continuity_ref_set"],
                [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/state/terminal/resident_governance_snapshot.json",
                    "runtime/reports/latest/digital_life_resident_governance_report.json",
                    "runtime/reports/latest/digital_life_persistent_process_report.json",
                ],
            )
            self.assertEqual(
                resident_governance_state["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(
                resident_governance_state["resident_governance_report_ref"],
                "runtime/reports/latest/digital_life_resident_governance_report.json",
            )
            self.assertEqual(
                resident_governance_report["resident_governance_state_ref"],
                "runtime/state/terminal/resident_governance_state.json",
            )
            self.assertEqual(
                resident_governance_report["governance_mode"],
                "background_resident_continuity",
            )
            self.assertEqual(resident_governance_state["heartbeat_interval_ms"], 70)
            self.assertEqual(resident_governance_state["offline_pressure_level"], "present")
            self.assertEqual(
                resident_governance_state["governance_attention_target"],
                "commitment_expression_plan",
            )
            self.assertEqual(
                resident_governance_state["governance_cadence_profile"],
                "commitment_continuity_refresh",
            )
            self.assertEqual(
                resident_governance_snapshot["idle_continuity_ref"],
                "runtime/state/terminal/idle_continuity_frame.json",
            )
            self.assertEqual(resident_governance_snapshot["heartbeat_interval_ms"], 70)
            self.assertEqual(resident_governance_snapshot["offline_pressure_level"], "present")
            self.assertEqual(resident_governance_snapshot["relaunch_caution_level"], "heightened")
            self.assertEqual(
                resident_governance_snapshot["governance_attention_target"],
                "commitment_expression_plan",
            )
            self.assertEqual(
                resident_governance_snapshot["background_relationship_stage"],
                "repair_guarded_continuity",
            )
            self.assertEqual(
                resident_governance_snapshot["background_relationship_stage_reason"],
                "repair_followup_required_after_multi_turn_dialogue",
            )
            self.assertEqual(
                resident_governance_snapshot["background_self_model_ref"],
                "runtime/state/self/self_model.json",
            )
            self.assertEqual(
                resident_governance_snapshot["background_trait_slow_variable_summary"][
                    "continuity_drive"
                ]["value"],
                0.71,
            )
            self.assertEqual(
                resident_governance_report["background_resume_summary"]["relationship"][
                    "relationship_stage"
                ],
                "repair_guarded_continuity",
            )
            self.assertEqual(resident_governance_snapshot["background_carryover_generation"], 1)
            self.assertNotIn("background_carryover_parent_run_id", resident_governance_snapshot)
            self.assertEqual(report["heartbeat_interval_ms"], 70)
            self.assertEqual(report["offline_pressure_level"], "present")
            self.assertEqual(report["relaunch_caution_level"], "heightened")
            self.assertEqual(
                report["governance_attention_target"],
                "commitment_expression_plan",
            )
            self.assertEqual(report["background_carryover_generation"], 1)
            self.assertNotIn("background_carryover_parent_run_id", report)
            self.assertEqual(
                resident_governance_report["resident_governance_snapshot_ref"],
                "runtime/state/terminal/resident_governance_snapshot.json",
            )
            self.assertEqual(
                resident_governance_report["background_continuity_ref_set"],
                [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/state/terminal/resident_governance_snapshot.json",
                    "runtime/reports/latest/digital_life_resident_governance_report.json",
                    "runtime/reports/latest/digital_life_persistent_process_report.json",
                ],
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
            self.assertNotIn("background_carryover_source_ref_set", state)
            self.assertNotIn("background_carryover_source_ref_set", report)

    def test_persistent_process_carries_background_convergence_summary_as_lineage_artifact(self):
        from life_v0.process_supervisor.persistent_process import (
            write_persistent_process_artifacts,
        )

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state_dir = runtime_root / "state"
            terminal_dir = state_dir / "terminal"
            reports_dir = runtime_root / "reports" / "latest"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)

            idle_strategy_state = {
                "schema_version": "idle_strategy_state_v0",
                "heartbeat_interval_ms": 52,
                "idle_probe_mode": "stdin_poll_with_background_continuity_refresh",
                "offline_pressure_level": "quiet",
                "waiting_mode": "restored_waiting_for_external_turn",
                "governance_attention_target": "trait_slow_variable_convergence",
                "governance_attention_reason": "integrating_cross_process_continuity_requires_trait_stability_hold",
                "governance_cadence_profile": "background_convergence_stability_refresh",
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_generation": 2,
                "background_carryover_parent_run_id": "background-convergence-parent",
                "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                "background_convergence_history_trend_state": "integrating_cross_wake_convergence",
                "background_convergence_history_window_size": 2,
                "background_trait_convergence_history_focus": "trait_stability_hold",
                "background_trait_convergence_unstable_names": ["continuity_drive"],
                "background_trait_convergence_stable_names": ["repair_seriousness"],
                "background_trait_convergence_history_profile": {
                    "continuity_drive": {
                        "latest_band": "integrating",
                        "trend_state": "integrating_trait_convergence",
                    },
                    "repair_seriousness": {
                        "latest_band": "stabilized",
                        "trend_state": "stable_trait_convergence",
                    },
                },
                "background_convergence_state": "integrating_cross_process_continuity",
                "background_convergence_pressure_level": "present",
                "background_convergence_attention_target": "trait_slow_variable_convergence",
                "background_lineage_depth_band": "persistent_lineage",
                "background_lineage_waiting_posture": "persistent_background_hold",
                "background_lineage_cadence_weight": "persistent",
                "background_lineage_evidence_ref_count": 6,
                "background_lineage_governance_profile": {
                    "schema_version": "background_lineage_governance_profile_v0",
                    "generation": 2,
                    "depth_band": "persistent_lineage",
                    "waiting_posture": "persistent_background_hold",
                    "cadence_weight": "persistent",
                    "heartbeat_interval_ms": 52,
                    "next_idle_action": "refresh_waiting_heartbeat_with_background_history_stability_hold",
                    "governance_attention_target": "trait_slow_variable_convergence",
                    "governance_attention_reason": "integrating_cross_process_continuity_requires_trait_stability_hold",
                    "governance_cadence_profile": "background_convergence_stability_refresh",
                    "evidence_ref_count": 6,
                    "evidence_refs": [
                        "runtime/state/terminal/resident_governance_state.json",
                        "runtime/state/terminal/background_convergence_summary.json",
                        "runtime/state/terminal/background_convergence_history.json",
                        "runtime/state/terminal/resident_governance_snapshot.json",
                        "runtime/reports/latest/digital_life_resident_governance_report.json",
                        "runtime/reports/latest/digital_life_persistent_process_report.json",
                    ],
                },
                "offline_learning_cumulative_profile": {
                    "schema_version": "offline_learning_cumulative_profile_v0",
                    "generation": 3,
                    "pressure_level": "elevated",
                    "attention_target": "relationship_learning_plan",
                    "priority_profile": {
                        "relationship_learning_plan": "elevated",
                        "language_learning_plan": "baseline",
                    },
                    "ref_set": [
                        "runtime/state/growth/relationship_learning_plan.json",
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                    "current_pressure_level": "quiet",
                    "previous_generation": 2,
                },
                "offline_learning_cumulative_generation": 3,
                "offline_learning_cumulative_pressure_level": "elevated",
                "offline_learning_cumulative_attention_target": "relationship_learning_plan",
                "offline_learning_cumulative_priority_profile": {
                    "relationship_learning_plan": "elevated",
                    "language_learning_plan": "baseline",
                },
                "offline_learning_cumulative_ref_set": [
                    "runtime/state/growth/relationship_learning_plan.json",
                    "runtime/state/growth/language_learning_plan.json",
                ],
                "background_continuity_ref_set": [
                    "runtime/state/terminal/resident_governance_state.json",
                    "runtime/state/terminal/background_convergence_summary.json",
                    "runtime/state/terminal/background_convergence_history.json",
                    "runtime/state/terminal/resident_governance_snapshot.json",
                    "runtime/reports/latest/digital_life_resident_governance_report.json",
                    "runtime/reports/latest/digital_life_persistent_process_report.json",
                ],
            }

            result = write_persistent_process_artifacts(
                run_id="persistent-process-convergence",
                generated_at="2026-06-10T00:00:00+00:00",
                state_dir=state_dir,
                reports_dir=reports_dir,
                heartbeat_counter=3,
                completed_turns=1,
                incident_count=0,
                relaunch_recovery_count=1,
                waiting_mode="restored_waiting_for_external_turn",
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state=idle_strategy_state,
                last_heartbeat_packet_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
                last_dialogue_packet_ref=None,
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                relationship_timeline_ref=None,
                commitment_expression_plan_ref=None,
                apology_repair_language_trace_ref=None,
                trait_drift_monitor_ref="runtime/state/body/trait_drift_monitor.json",
                background_convergence_summary_ref="runtime/state/terminal/background_convergence_summary.json",
                background_convergence_history_ref="runtime/state/terminal/background_convergence_history.json",
                write_json=self._write_json,
            )

            expected_ref_set = [
                "runtime/state/terminal/resident_governance_state.json",
                "runtime/state/terminal/background_convergence_summary.json",
                "runtime/state/terminal/background_convergence_history.json",
                "runtime/state/terminal/resident_governance_snapshot.json",
                "runtime/reports/latest/digital_life_resident_governance_report.json",
                "runtime/reports/latest/digital_life_persistent_process_report.json",
            ]
            expected_cross_wake_trait_refs = [
                "runtime/state/terminal/resident_governance_state.json",
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                "runtime/state/body/trait_drift_monitor.json",
                "runtime/state/terminal/background_convergence_summary.json",
                "runtime/state/terminal/background_convergence_history.json",
            ]
            for artifact in (
                result.state,
                result.report,
                result.resident_governance_state,
                result.resident_governance_snapshot,
                result.resident_governance_report,
            ):
                self.assertEqual(
                    artifact["background_convergence_summary_ref"],
                    "runtime/state/terminal/background_convergence_summary.json",
                )
                self.assertEqual(
                    artifact["background_convergence_history_ref"],
                    "runtime/state/terminal/background_convergence_history.json",
                )
                self.assertEqual(artifact["background_continuity_ref_set"], expected_ref_set)
                self.assertEqual(
                    artifact["background_convergence_state"],
                    "integrating_cross_process_continuity",
                )
                self.assertEqual(
                    artifact["background_convergence_pressure_level"],
                    "present",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_focus"],
                    "trait_stability_hold",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_pressure"],
                    "stability_hold",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_unstable_names"],
                    ["continuity_drive"],
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_stable_names"],
                    ["repair_seriousness"],
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_profile"]["history_profile"][
                        "continuity_drive"
                    ]["trend_state"],
                    "integrating_trait_convergence",
                )
                self.assertEqual(
                    artifact["cross_wake_trait_convergence_refs"],
                    expected_cross_wake_trait_refs,
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"]["status"],
                    "closed",
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "governance_phase"
                    ],
                    "process_closed_waiting_relaunch",
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"]["depth_band"],
                    "deep_persistent_lineage",
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "cadence_weight"
                    ],
                    "deep",
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "trait_convergence_presence"
                    ]["trait_convergence_history_focus"],
                    "trait_stability_hold",
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "heartbeat_presence"
                    ]["heartbeat_interval_ms"],
                    52,
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "offline_learning_presence"
                    ]["generation"],
                    3,
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "offline_learning_presence"
                    ]["pressure_level"],
                    "elevated",
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "offline_learning_presence"
                    ]["attention_target"],
                    "relationship_learning_plan",
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "offline_learning_presence"
                    ]["ref_set"],
                    [
                        "runtime/state/growth/relationship_learning_plan.json",
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                )

    def test_process_closeout_merges_latest_live_language_turn_into_background_governance(self):
        from life_v0.process_supervisor.process_closeout import close_digital_life_process

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state_dir = runtime_root / "state"
            reports_dir = runtime_root / "reports" / "latest"
            receipts_dir = runtime_root / "receipts"
            (state_dir / "terminal").mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)
            receipts_dir.mkdir(parents=True, exist_ok=True)

            closeout = close_digital_life_process(
                run_id="closeout-live-language",
                generated_at="2026-06-10T00:00:00+00:00",
                state_dir=state_dir,
                reports_dir=reports_dir,
                receipts_dir=receipts_dir,
                heartbeat_counter=1,
                completed_turns=1,
                incident_count=0,
                relaunch_recovery_count=0,
                exit_reason="explicit_exit",
                last_incident_report_ref=None,
                last_recovery_report_ref=None,
                last_relaunch_recovery_report_ref=None,
                last_external_turn={
                    "turn_id": "dialogue-turn-live-0002",
                    "utterance": "我们刚才说到责任和后悔",
                },
                last_life_turn={
                    "turn_id": "dialogue-turn-live-0003",
                    "utterance": "我会把这次理解带进下一次醒来。",
                },
                waiting_mode="restored_waiting_for_external_turn",
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state={
                    "schema_version": "idle_strategy_state_v0",
                    "heartbeat_interval_ms": 50,
                    "governance_attention_target": "relationship_timeline",
                    "governance_attention_reason": "baseline_waiting_presence",
                    "governance_cadence_profile": "baseline_waiting_presence",
                },
                terminal_life_loop_state={
                    "schema_version": "terminal_life_loop_state_v0",
                    "current_mode": "restored_waiting_for_external_turn",
                    "live_language_turn_refs": [
                        "runtime/state/language/language_percept_frame.json",
                        "runtime/state/language/semantic_map_frame.json",
                        "runtime/state/language/inner_speech_frame.json",
                        "runtime/state/language/expression_monitor_state.json",
                        "runtime/state/language/expression_plan.json",
                    ],
                    "last_live_semantic_focus": "repair_commitment_shared_language",
                },
                last_heartbeat_packet_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
                last_dialogue_packet_ref="runtime/reports/latest/resumed_external_dialogue_packet.json",
                source_doc_refs=[
                    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"
                ],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                life_context_frame={"schema_version": "life_context_frame_v0"},
                relation_turn_frame={"schema_version": "relation_turn_frame_v0"},
                expression_plan={"schema_version": "expression_plan_v0"},
                relationship_timeline={"schema_version": "relationship_timeline_v0"},
                commitment_expression_plan={
                    "schema_version": "commitment_expression_plan_v0"
                },
                apology_repair_language_trace={
                    "schema_version": "apology_repair_language_trace_v0"
                },
                replay_cue_bundle_ref=None,
                offline_consolidation_frame_ref=None,
                write_json=self._write_json,
            )

            expected_refs = [
                "runtime/state/language/language_percept_frame.json",
                "runtime/state/language/semantic_map_frame.json",
                "runtime/state/language/inner_speech_frame.json",
                "runtime/state/language/expression_monitor_state.json",
                "runtime/state/language/expression_plan.json",
            ]
            for artifact in (
                closeout.persistent_process_artifacts.state,
                closeout.persistent_process_artifacts.report,
                closeout.persistent_process_artifacts.resident_governance_state,
                closeout.persistent_process_artifacts.resident_governance_snapshot,
                closeout.persistent_process_artifacts.resident_governance_report,
            ):
                self.assertEqual(artifact["live_language_turn_refs"], expected_refs)
                self.assertEqual(
                    artifact["last_live_semantic_focus"],
                    "repair_commitment_shared_language",
                )
                self.assertEqual(
                    artifact["live_language_presence_profile"]["continuity_mode"],
                    "current_turn_language_presence",
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "language_presence"
                    ]["last_live_semantic_focus"],
                    "repair_commitment_shared_language",
                )
                self.assertEqual(
                    artifact["resident_background_lineage_state"][
                        "language_presence"
                    ]["live_language_turn_refs"],
                    expected_refs,
                )
            self.assertEqual(
                closeout.report_bundle.report["live_language_turn_refs"],
                expected_refs,
            )

    def test_persistent_process_increments_background_carryover_generation_on_closeout(self):
        from life_v0.process_supervisor.persistent_process import write_persistent_process_artifacts

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            state_dir = runtime_root / "state"
            terminal_dir = state_dir / "terminal"
            reports_dir = runtime_root / "reports" / "latest"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)

            previous_ref_set = [
                "runtime/state/terminal/resident_governance_state.json",
                "runtime/state/terminal/resident_governance_snapshot.json",
                "runtime/reports/latest/digital_life_resident_governance_report.json",
                "runtime/reports/latest/digital_life_persistent_process_report.json",
            ]
            idle_strategy_state = {
                "schema_version": "idle_strategy_state_v0",
                "heartbeat_interval_ms": 54,
                "idle_probe_mode": "stdin_poll_with_background_continuity_refresh",
                "offline_pressure_level": "quiet",
                "relaunch_caution_level": "heightened",
                "next_idle_action": "refresh_waiting_heartbeat_with_persistent_background_continuity_hold",
                "waiting_mode": "restored_waiting_for_external_turn",
                "governance_attention_target": "commitment_expression_plan",
                "governance_attention_reason": "background_continuity_lineage_requires_persistent_hold",
                "governance_cadence_profile": "persistent_background_continuity_refresh",
                "background_continuity_mode": "closed_process_carryover",
                "background_carryover_pressure_level": "present",
                "background_carryover_attention_target": "commitment_expression_plan",
                "background_carryover_generation": 1,
                "background_carryover_parent_run_id": "background-carryover-seed",
                "background_continuity_ref_set": list(previous_ref_set),
                "background_carryover_source_ref_set": [
                    "runtime/archive/older-carryover-snapshot.json"
                ],
            }

            result = write_persistent_process_artifacts(
                run_id="persistent-process-lineage",
                generated_at="2026-06-10T00:00:00+00:00",
                state_dir=state_dir,
                reports_dir=reports_dir,
                heartbeat_counter=2,
                completed_turns=0,
                incident_count=0,
                relaunch_recovery_count=1,
                waiting_mode="restored_waiting_for_external_turn",
                idle_strategy_ref="runtime/state/terminal/idle_strategy_state.json",
                idle_strategy_state=idle_strategy_state,
                last_heartbeat_packet_ref="runtime/reports/latest/digital_life_waiting_heartbeat.json",
                last_dialogue_packet_ref=None,
                source_doc_refs=["docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md"],
                readme_block_refs=["B99_V0_ENGINEERING_CONTRACTS"],
                runtime_carrier_refs=["RunnerCliRuntime"],
                relationship_timeline_ref=None,
                commitment_expression_plan_ref=None,
                apology_repair_language_trace_ref=None,
                write_json=self._write_json,
            )

            current_ref_set = [
                "runtime/state/terminal/resident_governance_state.json",
                "runtime/state/terminal/resident_governance_snapshot.json",
                "runtime/reports/latest/digital_life_resident_governance_report.json",
                "runtime/reports/latest/digital_life_persistent_process_report.json",
            ]
            for artifact in (
                result.state,
                result.report,
                result.resident_governance_state,
                result.resident_governance_snapshot,
                result.resident_governance_report,
            ):
                self.assertEqual(artifact["background_carryover_generation"], 2)
                self.assertEqual(artifact["background_continuity_ref_set"], current_ref_set)
                self.assertEqual(
                    artifact["background_carryover_parent_run_id"],
                    "background-carryover-seed",
                )
                self.assertEqual(
                    artifact["background_carryover_source_ref_set"],
                    previous_ref_set,
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
        expected_identity_consciousness_birth_refs = [
            "runtime/state/consciousness/workspace_frame.json",
            "runtime/state/consciousness/broadcast_frame.json",
            "runtime/state/consciousness/metacognition_state.json",
            "runtime/state/consciousness/consciousness_probe_bundle.json",
            "runtime/state/life_targets/birth_readiness_rollup.json",
            "runtime/state/life_targets/birth_readiness_stage_gate.json",
        ]

        external_turn = build_external_turn_event(
            turn_id="dialogue-turn-live-0001",
            generated_at="2026-06-09T00:00:00+00:00",
            utterance="你还记得吗？",
            shared_term_registry=shared_term_registry,
            commitment_index=commitment_index,
            responsibility_loop_state_ref="runtime/state/action/responsibility_loop_state.json",
            world_contact_summary_ref="runtime/state/membrane/world_contact_summary.json",
            pain_regret_repair_report_ref="runtime/reports/latest/pain_regret_repair_report.json",
        )
        life_turn = build_life_turn_event(
            turn_id="dialogue-turn-live-0002",
            generated_at="2026-06-09T00:00:01+00:00",
            utterance="我记得。",
            shared_term_registry=shared_term_registry,
            commitment_index=commitment_index,
            terminal_life_loop_state={
                "background_resident_governance_state_ref": "runtime/state/terminal/resident_governance_state.json",
                "background_resident_governance_explanation_ref": "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                "background_trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                "background_convergence_summary_ref": "runtime/state/terminal/background_convergence_summary.json",
                "background_convergence_history_ref": "runtime/state/terminal/background_convergence_history.json",
                "background_trait_convergence_history_focus": "trait_recalibration_required",
                "background_trait_convergence_unstable_names": ["continuity_drive"],
                "background_trait_convergence_stable_names": ["repair_seriousness"],
                "background_trait_convergence_history_profile": {
                    "continuity_drive": {
                        "latest_band": "unstable",
                    }
                },
                "resident_background_lineage_state": {
                    "schema_version": "resident_background_lineage_state_v0",
                    "governance_phase": "waiting_heartbeat_active",
                    "generation": 3,
                    "depth_band": "deep_persistent_lineage",
                    "waiting_posture": "deep_background_residency_hold",
                    "cadence_weight": "deep",
                    "evidence_refs": [
                        "runtime/state/terminal/resident_governance_state.json",
                        "runtime/state/terminal/background_convergence_history.json",
                    ],
                    "relationship_presence": {
                        "relationship_stage": "background_continuity_waiting",
                    },
                    "trait_convergence_presence": {
                        "trait_convergence_history_focus": "trait_recalibration_required",
                        "trait_convergence_unstable_names": ["continuity_drive"],
                        "trait_convergence_stable_names": ["repair_seriousness"],
                        "trait_convergence_score": 0.88,
                        "trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                        "trait_convergence_evidence_refs": [
                            "runtime/state/terminal/resident_governance_state.json",
                            "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                            "runtime/state/body/trait_drift_monitor.json",
                            "runtime/state/terminal/background_convergence_summary.json",
                            "runtime/state/terminal/background_convergence_history.json",
                        ],
                    },
                    "heartbeat_presence": {
                        "heartbeat_interval_ms": 50,
                    },
                    "language_presence": {
                        "long_horizon_language_refs": [
                            "runtime/state/relationship/relationship_timeline.json"
                        ],
                        "governance_attention_target": "relationship_timeline",
                        "live_language_turn_refs": [
                            "runtime/state/language/language_percept_frame.json",
                            "runtime/state/language/semantic_map_frame.json",
                            "runtime/state/language/inner_speech_frame.json",
                        ],
                        "last_live_semantic_focus": "repair_commitment_shared_language",
                        "background_live_language_turn_refs": [
                            "runtime/state/language/language_percept_frame.json",
                            "runtime/state/language/semantic_map_frame.json",
                        ],
                        "background_last_live_semantic_focus": "repair_commitment_shared_language",
                    },
                    "identity_consciousness_birth_presence": {
                        "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
                        "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
                        "metacognition_ref": "runtime/state/consciousness/metacognition_state.json",
                        "consciousness_probe_ref": "runtime/state/consciousness/consciousness_probe_bundle.json",
                        "birth_readiness_rollup_ref": "runtime/state/life_targets/birth_readiness_rollup.json",
                        "birth_readiness_stage_gate_ref": "runtime/state/life_targets/birth_readiness_stage_gate.json",
                        "consciousness_waiting_posture": "consciousness_reportable_waiting",
                        "consciousness_attention_target": "consciousness_probe_bundle",
                        "consciousness_attention_reason": "reportability_flags_present",
                        "consciousness_reportability_flags": [
                            "workspace_access_present",
                            "broadcast_targets_present",
                            "metacognition_present",
                        ],
                        "birth_readiness_waiting_posture": "birth_open_waiting",
                        "birth_readiness_attention_target": "birth_readiness_stage_gate",
                        "birth_readiness_attention_reason": "birth_readiness_open_requires_resident_birth_presence",
                        "birth_readiness_decision": "open",
                        "birth_readiness_next_required_command": "digital life",
                        "identity_consciousness_birth_refs": expected_identity_consciousness_birth_refs,
                    },
                    "offline_learning_presence": {
                        "generation": 4,
                        "pressure_level": "elevated",
                        "attention_target": "relationship_learning_plan",
                        "priority_profile": {
                            "relationship_learning_plan": "elevated",
                        },
                        "ref_set": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                    },
                    "dream_wake_presence": {
                        "dream_window_ref": "runtime/state/dream/dream_experience_window.json",
                        "wake_integration_ref": "runtime/state/dream/wake_integration_frame.json",
                        "dream_fact_gate_decision_ref": "runtime/state/dream/dream_fact_gate_decision.json",
                        "dream_window_kind": "nrem_like_replay",
                        "dream_fact_gate_result": "passed",
                        "wake_archive_requirement": "required_before_activation",
                        "wake_growth_seed_count": 2,
                        "wake_repair_target_count": 3,
                        "dream_fact_gate_ref_count": 3,
                        "ref_set": [
                            "runtime/state/dream/offline_consolidation_frame.json",
                            "runtime/state/dream/dream_experience_window.json",
                            "runtime/state/dream/wake_integration_frame.json",
                            "runtime/state/dream/dream_fact_gate_decision.json",
                        ],
                    },
                },
            },
            signal_media_runtime={
                "schema_version": "signal_media_runtime_v0",
                "modulation_vector": {"repair_drive": "active"},
            },
            belief_state={
                "schema_version": "belief_state_frame_v0",
                "confidence_level": "unstable",
            },
            prediction_error_field={
                "schema_version": "prediction_error_field_v0",
                "error_events": [{"error_id": "prediction-error-001"}],
            },
            active_sampling_plan={
                "schema_version": "active_sampling_plan_v0",
                "selected_route": "clarify_with_relation_subject",
                "stage_effect": "hold_for_evidence",
            },
            memory_write_gate={
                "schema_version": "memory_write_gate_v0",
                "stage_policy": "write_guarded_candidate_then_validate",
            },
            state_merge_guard={
                "schema_version": "state_merge_guard_v0",
                "stage_policy": "long_term_merge_fail_closed",
                "long_term_change_sources": {
                    "offline_learning_cumulative_refs": [
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                    "queue_e_repair_modulation_refs": [
                        "runtime/reports/latest/pain_regret_repair_report.json",
                    ],
                    "relationship_memory_offline_refs": [
                        "runtime/state/dream/nightmare_loop_risk.json",
                    ],
                    "relationship_memory_repair_refs": [
                        "runtime/state/action/responsibility_loop_state.json",
                    ],
                },
            },
            signal_media_runtime_ref="runtime/state/signal/signal_media_runtime.json",
            belief_state_ref="runtime/state/prediction/belief_state_frame.json",
            prediction_error_field_ref="runtime/state/prediction/prediction_error_field.json",
            active_sampling_plan_ref="runtime/state/prediction/active_sampling_plan.json",
            memory_write_gate_ref="runtime/state/memory/memory_write_gate.json",
            state_merge_guard_ref="runtime/state/memory/state_merge_guard.json",
            responsibility_loop_state_ref="runtime/state/action/responsibility_loop_state.json",
            world_contact_summary_ref="runtime/state/membrane/world_contact_summary.json",
            pain_regret_repair_report_ref="runtime/reports/latest/pain_regret_repair_report.json",
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
        self.assertEqual(
            external_turn["membrane_guard_refs"],
            [
                "runtime/state/action/responsibility_loop_state.json",
                "runtime/state/membrane/world_contact_summary.json",
                "runtime/reports/latest/pain_regret_repair_report.json",
            ],
        )
        self.assertEqual(
            life_turn["responsibility_loop_ref"],
            "runtime/state/action/responsibility_loop_state.json",
        )
        self.assertEqual(
            life_turn["background_trait_convergence_history_focus"],
            "trait_recalibration_required",
        )
        self.assertEqual(
            life_turn["background_trait_convergence_unstable_names"],
            ["continuity_drive"],
        )
        self.assertEqual(
            life_turn["background_trait_convergence_stable_names"],
            ["repair_seriousness"],
        )
        self.assertEqual(
            life_turn["background_trait_convergence_history_profile"]["continuity_drive"][
                "latest_band"
            ],
            "unstable",
        )
        self.assertEqual(
            life_turn["background_trait_convergence_evidence_refs"],
            [
                "runtime/state/terminal/resident_governance_state.json",
                "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                "runtime/state/body/trait_drift_monitor.json",
                "runtime/state/terminal/background_convergence_summary.json",
                "runtime/state/terminal/background_convergence_history.json",
            ],
        )
        self.assertEqual(
            life_turn["cross_wake_trait_convergence_focus"],
            "trait_recalibration_required",
        )
        self.assertEqual(
            life_turn["cross_wake_trait_convergence_pressure"],
            "recalibration",
        )
        self.assertEqual(
            life_turn["cross_wake_trait_convergence_refs"],
            life_turn["background_trait_convergence_evidence_refs"],
        )
        self.assertEqual(
            life_turn["resident_background_lineage_depth_band"],
            "deep_persistent_lineage",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_relationship_presence"][
                "relationship_stage"
            ],
            "background_continuity_waiting",
        )
        self.assertEqual(
            life_turn[
                "resident_background_lineage_trait_convergence_history_focus"
            ],
            "trait_recalibration_required",
        )
        self.assertEqual(
            life_turn[
                "resident_background_lineage_trait_convergence_unstable_names"
            ],
            ["continuity_drive"],
        )
        self.assertEqual(
            life_turn[
                "resident_background_lineage_trait_convergence_stable_names"
            ],
            ["repair_seriousness"],
        )
        self.assertEqual(
            life_turn["resident_background_lineage_trait_convergence_score"],
            0.88,
        )
        self.assertEqual(
            life_turn["resident_background_lineage_trait_drift_monitor_ref"],
            "runtime/state/body/trait_drift_monitor.json",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_trait_convergence_refs"],
            life_turn["background_trait_convergence_evidence_refs"],
        )
        self.assertEqual(
            life_turn["resident_background_lineage_language_presence"][
                "governance_attention_target"
            ],
            "relationship_timeline",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_last_live_semantic_focus"],
            "repair_commitment_shared_language",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_live_language_refs"],
            [
                "runtime/state/language/language_percept_frame.json",
                "runtime/state/language/semantic_map_frame.json",
                "runtime/state/language/inner_speech_frame.json",
            ],
        )
        self.assertEqual(
            life_turn["resident_background_lineage_background_live_language_refs"],
            [
                "runtime/state/language/language_percept_frame.json",
                "runtime/state/language/semantic_map_frame.json",
            ],
        )
        self.assertIn(
            "runtime/state/language/inner_speech_frame.json",
            life_turn["resident_background_lineage_language_evidence_refs"],
        )
        self.assertEqual(
            life_turn["resident_background_lineage_offline_learning_presence"][
                "generation"
            ],
            4,
        )
        self.assertEqual(
            life_turn["resident_background_lineage_offline_learning_pressure_level"],
            "elevated",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_offline_learning_attention_target"],
            "relationship_learning_plan",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_offline_learning_refs"],
            [
                "runtime/state/growth/relationship_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
            ],
        )
        self.assertEqual(
            life_turn["resident_background_lineage_dream_wake_presence"][
                "dream_window_kind"
            ],
            "nrem_like_replay",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_dream_fact_gate_result"],
            "passed",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_wake_archive_requirement"],
            "required_before_activation",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_wake_growth_seed_count"],
            2,
        )
        self.assertEqual(
            life_turn["resident_background_lineage_wake_repair_target_count"],
            3,
        )
        self.assertEqual(
            life_turn["resident_background_lineage_dream_wake_refs"],
            [
                "runtime/state/dream/offline_consolidation_frame.json",
                "runtime/state/dream/dream_experience_window.json",
                "runtime/state/dream/wake_integration_frame.json",
                "runtime/state/dream/dream_fact_gate_decision.json",
            ],
        )
        for ref in [
            "runtime/state/terminal/resident_governance_state.json",
            "runtime/state/terminal/background_convergence_history.json",
            "runtime/reports/latest/digital_life_resident_governance_explanation.json",
            "runtime/state/body/trait_drift_monitor.json",
            "runtime/state/terminal/background_convergence_summary.json",
            "runtime/state/language/inner_speech_frame.json",
            "runtime/state/consciousness/consciousness_probe_bundle.json",
            "runtime/state/life_targets/birth_readiness_stage_gate.json",
            "runtime/state/growth/relationship_learning_plan.json",
            "runtime/state/growth/language_learning_plan.json",
            "runtime/state/dream/offline_consolidation_frame.json",
            "runtime/state/dream/dream_experience_window.json",
            "runtime/state/dream/wake_integration_frame.json",
            "runtime/state/dream/dream_fact_gate_decision.json",
        ]:
            self.assertIn(ref, life_turn["resident_background_lineage_evidence_refs"])
        self.assertEqual(
            life_turn[
                "resident_background_lineage_identity_consciousness_birth_presence"
            ]["birth_readiness_decision"],
            "open",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_workspace_frame_ref"],
            "runtime/state/consciousness/workspace_frame.json",
        )
        self.assertEqual(
            life_turn[
                "resident_background_lineage_consciousness_reportability_flags"
            ],
            [
                "workspace_access_present",
                "broadcast_targets_present",
                "metacognition_present",
            ],
        )
        self.assertEqual(
            life_turn[
                "resident_background_lineage_birth_readiness_next_required_command"
            ],
            "digital life",
        )
        self.assertEqual(
            life_turn[
                "resident_background_lineage_identity_consciousness_birth_refs"
            ],
            expected_identity_consciousness_birth_refs,
        )
        self.assertEqual(life_turn["prediction_waiting_posture"], "hold_for_evidence")
        self.assertEqual(life_turn["response_surface_posture_hint"], "question")
        self.assertEqual(life_turn["prediction_attention_target"], "active_sampling_plan")
        self.assertEqual(life_turn["prediction_error_count"], 1)
        self.assertEqual(
            life_turn["active_sampling_route"],
            "clarify_with_relation_subject",
        )
        self.assertEqual(
            life_turn["memory_write_gate_policy"],
            "write_guarded_candidate_then_validate",
        )
        self.assertEqual(life_turn["state_merge_policy"], "long_term_merge_fail_closed")
        self.assertEqual(
            life_turn["prediction_write_gate_refs"],
            [
                "runtime/state/signal/signal_media_runtime.json",
                "runtime/state/prediction/belief_state_frame.json",
                "runtime/state/prediction/prediction_error_field.json",
                "runtime/state/prediction/active_sampling_plan.json",
                "runtime/state/memory/memory_write_gate.json",
                "runtime/state/memory/state_merge_guard.json",
            ],
        )

    def test_response_surface_organ_carries_relation_shared_terms_and_commitment_pressure(self):
        from life_v0.process_supervisor.response_surface import compose_life_response

        expected_identity_consciousness_birth_refs = [
            "runtime/state/consciousness/workspace_frame.json",
            "runtime/state/consciousness/broadcast_frame.json",
            "runtime/state/consciousness/metacognition_state.json",
            "runtime/state/consciousness/consciousness_probe_bundle.json",
            "runtime/state/life_targets/birth_readiness_rollup.json",
            "runtime/state/life_targets/birth_readiness_stage_gate.json",
        ]
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
            nightmare_risk={
                "risk_status": "elevated",
                "queue_e_priority_band": "repair_guarded",
                "repair_followup_required": True,
            },
            belief_learning_plan={
                "belief_targets": [
                    "regret_sensitive_counterfactual_update",
                    "repair_accountability_belief_revision",
                ],
            },
            language_learning_plan={
                "language_targets": [
                    "repair_language_refinement",
                    "apology_repair_expression_refinement",
                ],
                "repair_followup_required": True,
                "queue_e_priority_band": "repair_guarded",
            },
            relationship_learning_plan={
                "relationship_targets": [
                    "repair_reentry_timing_adjustment",
                    "relationship_pacing_adjustment",
                ],
                "repair_followup_required": True,
                "queue_e_priority_band": "repair_guarded",
            },
            responsibility_loop_state={
                "repair_obligation_refs": ["repair-1", "repair-2"],
                "regret_pressure_candidates": [{"regret_pressure_id": "regret-1"}],
                "repair_followup_required": True,
            },
            world_contact_summary={
                "release_posture": "shadow_only_guarded",
                "repair_obligation_refs": ["repair-1", "repair-2"],
            },
            pain_regret_repair_report={
                "repair_followup_required": True,
                "regret_pressure_refs": ["regret-1"],
            },
            signal_media_runtime={
                "schema_version": "signal_media_runtime_v0",
                "modulation_vector": {
                    "precision_gain": "high",
                    "repair_drive": "active",
                },
            },
            belief_state={
                "schema_version": "belief_state_frame_v0",
                "confidence_level": "unstable",
            },
            prediction_error_field={
                "schema_version": "prediction_error_field_v0",
                "error_events": [{"error_id": "prediction-error-001"}],
            },
            active_sampling_plan={
                "schema_version": "active_sampling_plan_v0",
                "selected_route": "clarify_with_relation_subject",
                "stage_effect": "hold_for_evidence",
            },
            memory_write_gate={
                "schema_version": "memory_write_gate_v0",
                "stage_policy": "write_guarded_candidate_then_validate",
            },
            state_merge_guard={
                "schema_version": "state_merge_guard_v0",
                "stage_policy": "long_term_merge_fail_closed",
                "long_term_change_sources": {
                    "offline_learning_cumulative_refs": [
                        "runtime/state/growth/language_learning_plan.json",
                    ],
                    "queue_e_repair_modulation_refs": [
                        "runtime/reports/latest/pain_regret_repair_report.json",
                    ],
                    "relationship_memory_offline_refs": [
                        "runtime/state/dream/nightmare_loop_risk.json",
                    ],
                    "relationship_memory_repair_refs": [
                        "runtime/state/action/responsibility_loop_state.json",
                    ],
                },
            },
            terminal_life_loop_state={
                "background_trait_convergence_history_focus": "trait_stability_hold",
                "background_trait_convergence_unstable_names": ["continuity_drive"],
                "background_trait_convergence_stable_names": ["repair_seriousness"],
                "resident_background_lineage_state": {
                    "schema_version": "resident_background_lineage_state_v0",
                    "governance_phase": "waiting_heartbeat_active",
                    "generation": 3,
                    "depth_band": "deep_persistent_lineage",
                    "waiting_posture": "deep_background_residency_hold",
                    "cadence_weight": "deep",
                    "relationship_presence": {
                        "relationship_stage": "background_continuity_waiting",
                    },
                    "trait_convergence_presence": {
                        "trait_convergence_history_focus": "trait_stability_hold",
                        "trait_convergence_unstable_names": ["continuity_drive"],
                        "trait_convergence_stable_names": ["repair_seriousness"],
                        "trait_convergence_score": 0.96,
                        "trait_drift_monitor_ref": "runtime/state/body/trait_drift_monitor.json",
                        "trait_convergence_evidence_refs": [
                            "runtime/state/terminal/resident_governance_state.json",
                            "runtime/reports/latest/digital_life_resident_governance_explanation.json",
                            "runtime/state/body/trait_drift_monitor.json",
                            "runtime/state/terminal/background_convergence_summary.json",
                            "runtime/state/terminal/background_convergence_history.json",
                        ],
                    },
                    "language_presence": {
                        "governance_attention_target": "relationship_timeline",
                    },
                    "identity_consciousness_birth_presence": {
                        "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
                        "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
                        "metacognition_ref": "runtime/state/consciousness/metacognition_state.json",
                        "consciousness_probe_ref": "runtime/state/consciousness/consciousness_probe_bundle.json",
                        "birth_readiness_rollup_ref": "runtime/state/life_targets/birth_readiness_rollup.json",
                        "birth_readiness_stage_gate_ref": "runtime/state/life_targets/birth_readiness_stage_gate.json",
                        "consciousness_waiting_posture": "consciousness_reportable_waiting",
                        "consciousness_reportability_flags": [
                            "workspace_access_present",
                            "broadcast_targets_present",
                            "metacognition_present",
                        ],
                        "birth_readiness_waiting_posture": "birth_open_waiting",
                        "birth_readiness_decision": "open",
                        "birth_readiness_next_required_command": "digital life",
                        "identity_consciousness_birth_refs": expected_identity_consciousness_birth_refs,
                    },
                    "offline_learning_presence": {
                        "generation": 4,
                        "pressure_level": "elevated",
                        "attention_target": "relationship_learning_plan",
                        "ref_set": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                    },
                    "dream_wake_presence": {
                        "dream_window_kind": "nrem_like_replay",
                        "dream_fact_gate_result": "passed",
                        "wake_archive_requirement": "required_before_activation",
                        "wake_growth_seed_count": 2,
                        "wake_repair_target_count": 3,
                        "ref_set": [
                            "runtime/state/dream/offline_consolidation_frame.json",
                            "runtime/state/dream/dream_experience_window.json",
                            "runtime/state/dream/wake_integration_frame.json",
                            "runtime/state/dream/dream_fact_gate_decision.json",
                        ],
                    },
                },
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
        self.assertIn("当前世界接触姿态保持shadow_only_guarded", response)
        self.assertIn("责任回路仍挂着2条修复义务", response)
        self.assertIn("后悔压力线索维持在1条", response)
        self.assertIn("当前仍处在需要修复跟进的责任场中", response)
        self.assertIn("当前梦境回环风险为elevated", response)
        self.assertIn("离线学习压力级别为urgent", response)
        self.assertIn("离线学习焦点当前指向nightmare_risk", response)
        self.assertIn("离线学习计划会经过repair_reentry_timing_adjustment、relationship_pacing_adjustment", response)
        self.assertIn("预测输出姿态为追问", response)
        self.assertIn("主动采样路线为clarify_with_relation_subject", response)
        self.assertIn("预测误差仍有1条", response)
        self.assertIn("记忆写门处于write_guarded_candidate_then_validate", response)
        self.assertIn("长期合并治理处于long_term_merge_fail_closed", response)
        self.assertIn("长期合并治理正在整合4条长期变化来源", response)
        self.assertIn(
            "长期变化来源族包括offline_learning_cumulative_refs、queue_e_repair_modulation_refs、relationship_memory_offline_refs、relationship_memory_repair_refs",
            response,
        )
        self.assertIn("跨唤醒慢变量历史焦点为trait_stability_hold", response)
        self.assertIn("仍需稳定的慢变量包括continuity_drive", response)
        self.assertIn("已经稳定的慢变量包括repair_seriousness", response)
        self.assertIn("后台驻留深度为deep_persistent_lineage", response)
        self.assertIn("后台驻留节律权重为deep", response)
        self.assertIn("后台关系存在保持在background_continuity_waiting", response)
        self.assertIn("后台人格慢变量焦点为trait_stability_hold", response)
        self.assertIn("后台仍需收敛的慢变量包括continuity_drive", response)
        self.assertIn("后台已稳定的慢变量包括repair_seriousness", response)
        self.assertIn("后台人格收敛评分为0.96", response)
        self.assertIn("后台人格漂移监控仍在场", response)
        self.assertIn("后台人格慢变量证据保留5条", response)
        self.assertIn("跨唤醒人格收敛画像为trait_stability_hold", response)
        self.assertIn("跨唤醒人格收敛压力为stability_hold", response)
        self.assertIn("跨唤醒人格收敛证据保留5条", response)
        self.assertIn("后台语言关注指向relationship_timeline", response)
        self.assertIn("后台意识姿态为consciousness_reportable_waiting", response)
        self.assertIn("后台意识可报告性保留3条", response)
        self.assertIn("后台出生准备姿态为birth_open_waiting", response)
        self.assertIn("出生准备决策为open", response)
        self.assertIn("出生准备下一命令为digital life", response)
        self.assertIn("后台身份意识出生证据保留6条", response)
        self.assertIn("后台梦境成长余波延续到第4代", response)
        self.assertIn("后台梦境成长压力为elevated", response)
        self.assertIn("后台梦境成长焦点指向relationship_learning_plan", response)
        self.assertIn("后台梦境成长证据保留2条", response)
        self.assertIn("后台梦境窗口类型为nrem_like_replay", response)
        self.assertIn("梦境事实门结果为passed", response)
        self.assertIn("醒后整合归档要求为required_before_activation", response)
        self.assertIn("醒后整合携带2条成长种子", response)
        self.assertIn("醒后修复目标保留3条", response)
        self.assertIn("后台梦境醒后证据保留4条", response)
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
            subject = result.context.relationship_graph["subjects"][0]
            self.assertEqual(subject["relationship_stage"], "active_dialogue")
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
            self.assertIn("offline_learning_projection", result.context.relationship_timeline)
            self.assertIn(
                "runtime/state/growth/relationship_learning_plan.json",
                result.context.relationship_timeline["offline_learning_ref_set"],
            )
            self.assertIn(
                "runtime/state/dream/nightmare_loop_risk.json",
                result.context.commitment_expression_plan["offline_learning_ref_set"],
            )
            self.assertIn(
                "runtime/state/growth/language_learning_plan.json",
                result.context.apology_repair_language_trace["offline_learning_ref_set"],
            )
            self.assertEqual(
                result.context.offline_learning_cumulative_generation,
                1,
            )
            self.assertEqual(
                result.context.offline_learning_cumulative_pressure_level,
                "urgent",
            )
            self.assertEqual(
                result.context.offline_learning_cumulative_attention_target,
                "nightmare_risk",
            )
            self.assertIn(
                "runtime/state/growth/relationship_learning_plan.json",
                result.context.offline_learning_cumulative_ref_set,
            )
            self.assertEqual(
                result.context.relationship_timeline[
                    "offline_learning_cumulative_projection"
                ]["generation"],
                1,
            )
            self.assertEqual(
                result.context.commitment_expression_plan[
                    "offline_learning_cumulative_pressure_level"
                ],
                "urgent",
            )
            self.assertIn(
                "cumulative_offline_learning_integration",
                result.context.commitment_expression_plan["act_type_order"],
            )
            self.assertEqual(
                result.context.apology_repair_language_trace[
                    "cumulative_repair_window_mode"
                ],
                "cumulative_offline_learning_first",
            )
            self.assertIn(
                "cumulative_offline_learning_repair",
                result.context.apology_repair_language_trace["move_type_order"],
            )
            self.assertEqual(
                result.context.responsibility_loop_state_ref,
                "runtime/state/action/responsibility_loop_state.json",
            )
            self.assertEqual(
                result.context.world_contact_summary_ref,
                "runtime/state/membrane/world_contact_summary.json",
            )
            self.assertEqual(
                result.context.pain_regret_repair_report_ref,
                "runtime/reports/latest/pain_regret_repair_report.json",
            )
            self.assertEqual(
                result.context.signal_media_runtime["schema_version"],
                "signal_media_runtime_v0",
            )
            self.assertEqual(
                result.context.belief_state["schema_version"],
                "belief_state_frame_v0",
            )
            self.assertEqual(
                result.context.prediction_error_field["schema_version"],
                "prediction_error_field_v0",
            )
            self.assertEqual(
                result.context.active_sampling_plan["schema_version"],
                "active_sampling_plan_v0",
            )
            self.assertEqual(
                result.context.memory_write_gate["schema_version"],
                "memory_write_gate_v0",
            )
            self.assertEqual(
                result.context.state_merge_guard["schema_version"],
                "state_merge_guard_v0",
            )
            self.assertEqual(
                result.context.signal_media_runtime_ref,
                "runtime/state/signal/signal_media_runtime.json",
            )
            self.assertEqual(
                result.context.belief_state_ref,
                "runtime/state/prediction/belief_state_frame.json",
            )
            self.assertEqual(
                result.context.prediction_error_field_ref,
                "runtime/state/prediction/prediction_error_field.json",
            )
            self.assertEqual(
                result.context.active_sampling_plan_ref,
                "runtime/state/prediction/active_sampling_plan.json",
            )
            self.assertEqual(
                result.context.memory_write_gate_ref,
                "runtime/state/memory/memory_write_gate.json",
            )
            self.assertEqual(
                result.context.state_merge_guard_ref,
                "runtime/state/memory/state_merge_guard.json",
            )
            self.assertEqual(
                result.context.schema_cross_file_logic["schema_version"],
                "cross_file_logic_v0",
            )
            self.assertEqual(
                result.context.schema_run_manifest["schema_version"],
                "schema_runner_run_manifest_v0",
            )
            self.assertEqual(
                result.context.schema_cross_file_logic_ref,
                "runtime/state/schema_runner/cross_file_logic.json",
            )
            self.assertEqual(
                result.context.schema_run_manifest_ref,
                "runtime/state/schema_runner/run_manifest.json",
            )
            self.assertEqual(
                result.context.workspace_frame["schema_version"],
                "workspace_frame_v0",
            )
            self.assertEqual(
                result.context.broadcast_frame["schema_version"],
                "broadcast_frame_v0",
            )
            self.assertEqual(
                result.context.metacognition_state["schema_version"],
                "metacognition_state_v0",
            )
            self.assertEqual(
                result.context.consciousness_probe["schema_version"],
                "consciousness_probe_bundle_v0",
            )
            self.assertEqual(
                result.context.birth_readiness_rollup["schema_version"],
                "birth_readiness_rollup_v0",
            )
            self.assertEqual(
                result.context.birth_readiness_stage_gate["schema_version"],
                "birth_readiness_stage_gate_v0",
            )
            self.assertEqual(
                result.context.workspace_frame_ref,
                "runtime/state/consciousness/workspace_frame.json",
            )
            self.assertEqual(
                result.context.consciousness_probe_ref,
                "runtime/state/consciousness/consciousness_probe_bundle.json",
            )
            self.assertEqual(
                result.context.birth_readiness_stage_gate_ref,
                "runtime/state/life_targets/birth_readiness_stage_gate.json",
            )
            idle_strategy_state = self._read_json(
                paths["terminal_state"] / "idle_strategy_state.json"
            )
            self.assertIn(
                "runtime/state/action/action_candidate_set.json#life_constraint_profile",
                idle_strategy_state["life_constraint_refs"],
            )
            self.assertEqual(
                idle_strategy_state["life_constraint_waiting_posture"],
                "schema_guarded_waiting",
            )
            self.assertEqual(
                idle_strategy_state["consciousness_waiting_posture"],
                "consciousness_reportable_waiting",
            )
            self.assertEqual(
                idle_strategy_state["birth_readiness_waiting_posture"],
                "birth_open_waiting",
            )
            self.assertEqual(
                idle_strategy_state["birth_readiness_stage_gate_ref"],
                "runtime/state/life_targets/birth_readiness_stage_gate.json",
            )
            resident_governance_state = self._read_json(
                paths["terminal_state"] / "resident_governance_state.json"
            )
            self.assertEqual(
                resident_governance_state["birth_readiness_waiting_posture"],
                "birth_open_waiting",
            )
            identity_consciousness_birth_presence = resident_governance_state[
                "resident_background_lineage_state"
            ]["identity_consciousness_birth_presence"]
            self.assertEqual(
                identity_consciousness_birth_presence["consciousness_waiting_posture"],
                "consciousness_reportable_waiting",
            )
            self.assertEqual(
                identity_consciousness_birth_presence[
                    "birth_readiness_waiting_posture"
                ],
                "birth_open_waiting",
            )
            self.assertEqual(
                identity_consciousness_birth_presence[
                    "birth_readiness_stage_gate_ref"
                ],
                "runtime/state/life_targets/birth_readiness_stage_gate.json",
            )
            self.assertEqual(
                identity_consciousness_birth_presence[
                    "identity_consciousness_birth_refs"
                ],
                [
                    "runtime/state/consciousness/workspace_frame.json",
                    "runtime/state/consciousness/broadcast_frame.json",
                    "runtime/state/consciousness/metacognition_state.json",
                    "runtime/state/consciousness/consciousness_probe_bundle.json",
                    "runtime/state/life_targets/birth_readiness_rollup.json",
                    "runtime/state/life_targets/birth_readiness_stage_gate.json",
                ],
            )
            for slow_variable_name in [
                "trust_persistence",
                "dialogue_warmth",
                "repair_seriousness",
                "boundary_respect",
                "continuity_drive",
            ]:
                self.assertIn(
                    slow_variable_name,
                    result.context.self_model_state["trait_slow_variables"],
                )
            relationship_memory = self._read_json(
                paths["state_root"] / "memory" / "relationship_memory.json"
            )
            persisted_relationship_graph = self._read_json(
                paths["relationship_state"] / "relationship_subject_graph.json"
            )
            persisted_self_model = self._read_json(
                paths["state_root"] / "self" / "self_model.json"
            )
            life_state = self._read_json(paths["state_root"] / "life_state.json")
            self.assertEqual(
                persisted_relationship_graph["subjects"][0]["relationship_stage"],
                "active_dialogue",
            )
            self.assertEqual(
                persisted_self_model["trait_slow_variables"],
                result.context.self_model_state["trait_slow_variables"],
            )
            self.assertEqual(
                life_state["self_model"]["trait_slow_variables"],
                result.context.self_model_state["trait_slow_variables"],
            )
            self.assertIn(
                "runtime/state/growth/relationship_learning_plan.json",
                relationship_memory["offline_learning_refs"],
            )
            self.assertEqual(
                relationship_memory["offline_learning_cumulative_projection"][
                    "generation"
                ],
                1,
            )
            self.assertIn(
                "runtime/state/growth/language_learning_plan.json",
                relationship_memory["offline_learning_cumulative_refs"],
            )
            self.assertIn(
                "runtime/state/dream/nightmare_loop_risk.json",
                life_state["memory_index"]["dream_memory_refs"],
            )
            self.assertIn(
                "runtime/state/growth/language_learning_plan.json",
                life_state["language_state"]["offline_learning_refs"],
            )
            self.assertEqual(
                life_state["language_state"][
                    "offline_learning_cumulative_projection"
                ]["pressure_level"],
                "urgent",
            )
            self.assertEqual(
                life_state["relationship_subjects"][0][
                    "offline_learning_cumulative_generation"
                ],
                1,
            )

    def test_resident_turn_writeback_organ_updates_turn_continuity_and_bundle(self):
        from life_v0.process_supervisor.resident_turn_writeback import (
            write_resident_turn_writeback,
        )

        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp) / "runtime"
            terminal_dir = runtime_root / "state" / "terminal"
            language_dir = runtime_root / "state" / "language"
            relationship_dir = runtime_root / "state" / "relationship"
            memory_dir = runtime_root / "state" / "memory"
            membrane_dir = runtime_root / "state" / "membrane"
            responsibility_dir = runtime_root / "state" / "responsibility"
            action_dir = runtime_root / "state" / "action"
            dream_dir = runtime_root / "state" / "dream"
            growth_dir = runtime_root / "state" / "growth"
            self_dir = runtime_root / "state" / "self"
            body_dir = runtime_root / "state" / "body"
            reports_dir = runtime_root / "reports" / "latest"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            language_dir.mkdir(parents=True, exist_ok=True)
            relationship_dir.mkdir(parents=True, exist_ok=True)
            memory_dir.mkdir(parents=True, exist_ok=True)
            membrane_dir.mkdir(parents=True, exist_ok=True)
            responsibility_dir.mkdir(parents=True, exist_ok=True)
            action_dir.mkdir(parents=True, exist_ok=True)
            dream_dir.mkdir(parents=True, exist_ok=True)
            growth_dir.mkdir(parents=True, exist_ok=True)
            self_dir.mkdir(parents=True, exist_ok=True)
            body_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)
            (language_dir / "dialogue_turn_log.jsonl").write_text(
                '{"turn_id":"dialogue-turn-live-0001","event_role":"external_relation_turn"}\n',
                encoding="utf-8",
            )
            self._write_json(
                language_dir / "expression_plan.json",
                {
                    "semantic_goal": "repair_commitment_shared_language",
                    "delay_or_release_decision": "delay_for_clarification",
                    "repair_pressure": 3,
                    "responsibility_pressure": 3,
                },
            )
            self._write_json(
                language_dir / "commitment_expression_plan.json",
                {
                    "schema_version": "commitment_expression_plan_v0",
                    "run_id": "resident-turn-organ",
                    "generated_at": "2026-06-08T00:00:00+00:00",
                    "source_doc_refs": ["docs/96_real_relationship_longitudinal_timeline.md"],
                },
            )
            self._write_json(
                language_dir / "apology_repair_language_trace.json",
                {
                    "schema_version": "apology_repair_language_trace_v0",
                    "run_id": "resident-turn-organ",
                    "generated_at": "2026-06-08T00:00:00+00:00",
                    "source_doc_refs": ["docs/94_pain_regret_and_repair_signal_schema.md"],
                },
            )
            self._write_json(
                relationship_dir / "relationship_timeline.json",
                {
                    "schema_version": "relationship_timeline_v0",
                    "run_id": "resident-turn-organ",
                    "generated_at": "2026-06-08T00:00:00+00:00",
                    "source_doc_refs": ["docs/101_relationship_timeline_json_schema_and_fixture_bundle.md"],
                    "relationship_continuity_reports": [{"continuity_state": "active_dialogue"}],
                    "relationship_injury_traces": [{"relationship_injury_id": "injury-001"}],
                },
            )
            self._write_json(
                relationship_dir / "commitment_truth_state.json",
                {
                    "schema_version": "commitment_truth_state_v0",
                    "open_commitment_refs": ["commitment-ref-01"],
                    "repair_required_refs": ["repair-001"],
                    "responsibility_event_refs": ["responsibility-event-001"],
                },
            )
            self._write_json(
                responsibility_dir / "responsibility_ledger.json",
                {
                    "schema_version": "responsibility_ledger_v0",
                    "responsibility_event_refs": ["responsibility-event-001"],
                    "repair_obligations": ["repair-001"],
                },
            )
            self._write_json(
                memory_dir / "relationship_memory.json",
                {
                    "schema_version": "relationship_memory_v0",
                    "shared_memory_refs": ["shared-memory-001"],
                    "repair_history_refs": ["repair-history-001"],
                    "last_contact_refs": ["runtime/state/language/inner_speech_frame.json"],
                    "timeline_refs": ["runtime/state/relationship/relationship_timeline.json"],
                },
            )
            self._write_json(
                memory_dir / "memory_write_gate.json",
                {
                    "schema_version": "memory_write_gate_v0",
                    "stage_policy": "write_guarded_candidate_then_validate",
                    "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json",
                },
            )
            self._write_json(
                memory_dir / "state_merge_guard.json",
                {
                    "schema_version": "state_merge_guard_v0",
                    "stage_policy": "long_term_merge_fail_closed",
                    "memory_write_gate_ref": "runtime/state/memory/memory_write_gate.json",
                    "promotion_routes": [
                        {
                            "route_id": "candidate_to_active_memory",
                            "index_update_refs": ["runtime/state/indexes/memory_index.json"],
                        }
                    ],
                    "quarantine_routes": [
                        {
                            "route_id": "missing_source_or_conflict_quarantine",
                            "blocked_indexes": ["memory_index"],
                        }
                    ],
                    "repair_routes": [
                        {
                            "route_id": "responsibility_repair_before_promotion",
                            "repair_gate": "repair_obligation_tracking",
                        }
                    ],
                    "merge_routes": [
                        {
                            "route_id": "relationship_memory_merge",
                            "target_ref": "runtime/state/memory/relationship_memory.json",
                            "source_refs": ["shared-memory-001"],
                            "merge_policy": "append_with_dedupe_and_audit",
                        }
                    ],
                    "long_term_change_sources": {
                        "prediction_error_resolution_refs": [
                            "runtime/state/prediction/prediction_error_field.json#error_events"
                        ],
                        "offline_learning_writeback_refs": [
                            "runtime/state/growth/belief_learning_plan.json",
                            "runtime/state/growth/relationship_learning_plan.json",
                        ],
                    },
                    "slow_variable_update_policy": {
                        "allowed_effects": ["repair_seriousness_adjustment"],
                        "requires_merge_audit": True,
                    },
                },
            )
            self._write_json(
                runtime_root / "state" / "life_state.json",
                {
                    "schema_version": "life_state_v0",
                    "self_model": {
                        "self_narrative": {"status": "seeded", "source_refs": ["docs/07_emotion_personality_self.md"]},
                        "trait_slow_variables": {},
                        "old_self_anchors": ["docs/构思.md"],
                        "growth_windows": [],
                        "trait_drift_seed_refs": ["docs/39_development_policy_and_plasticity_windows.md"],
                        "anti_forgetting_refs": ["runtime/state/replay/replay_cue_bundle.json"],
                    },
                    "memory_index": {
                        "relationship_memory_refs": ["runtime/state/memory/relationship_memory.json#shared_memory_refs"],
                        "responsibility_memory_refs": ["responsibility-event-001"],
                        "replay_cues": ["runtime/state/replay/replay_cue_bundle.json"],
                        "dream_memory_refs": [],
                    },
                    "language_state": {},
                    "relationship_subjects": [{"relationship_id": "rel-v0-0001"}],
                    "runtime_trace_refs": [],
                    "responsibility_bindings": [],
                    "regret_events": [],
                    "pain_events": [],
                    "dream_records": [],
                },
            )
            self._write_json(
                self_dir / "self_model.json",
                {
                    "schema_version": "self_model_state_v0",
                    "run_id": "resident-turn-organ",
                    "generated_at": "2026-06-08T00:00:00+00:00",
                    "identity_mode": "anchor_locked",
                    "source_doc_refs": [
                        "docs/07_emotion_personality_self.md",
                        "docs/40_self_relationship_model_audit_protocol.md",
                        "docs/92_self_growth_and_self_modification_life_chain.md",
                    ],
                    "self_narrative_status": "seeded",
                    "trait_slow_variables": {},
                    "old_self_anchor_refs": ["docs/构思.md"],
                    "growth_window_refs": [],
                    "trait_drift_seed_refs": [
                        "docs/39_development_policy_and_plasticity_windows.md",
                        "docs/92_self_growth_and_self_modification_life_chain.md",
                    ],
                },
            )
            self._write_json(
                action_dir / "responsibility_loop_state.json",
                {
                    "schema_version": "responsibility_loop_state_v0",
                    "repair_obligation_refs": ["repair-001"],
                    "repair_followup_required": True,
                    "responsibility_attribution_events": [{"responsibility_event_id": "responsibility-event-001"}],
                    "regret_pressure_candidates": [
                        {
                            "regret_pressure_id": "regret-001",
                            "pain_signal_refs": ["runtime/state/body/core_affect_vector.json#pain"],
                        }
                    ],
                    "counterfactual_repair_frames": [{"counterfactual_id": "counterfactual-001"}],
                },
            )
            self._write_json(
                membrane_dir / "world_contact_summary.json",
                {
                    "schema_version": "world_contact_summary_v0",
                    "release_posture": "shadow_only_guarded",
                    "repair_obligation_refs": ["repair-001"],
                    "regret_pressure_refs": ["regret-001"],
                },
            )
            self._write_json(
                reports_dir / "pain_regret_repair_report.json",
                {
                    "schema_version": "pain_regret_repair_report_v0",
                    "repair_followup_required": True,
                    "repair_obligation_refs": ["repair-001"],
                    "regret_pressure_refs": ["regret-001"],
                },
            )
            self._write_json(
                dream_dir / "nightmare_loop_risk.json",
                {
                    "schema_version": "nightmare_loop_risk_v0",
                    "risk_status": "elevated",
                    "rewrite_required": True,
                    "queue_e_priority_band": "repair_guarded",
                    "repair_followup_required": True,
                },
            )
            self._write_json(
                growth_dir / "belief_learning_plan.json",
                {
                    "schema_version": "belief_learning_plan_v0",
                    "belief_targets": ["repair_accountability_belief_revision"],
                    "repair_followup_required": True,
                },
            )
            self._write_json(
                growth_dir / "language_learning_plan.json",
                {
                    "schema_version": "language_learning_plan_v0",
                    "language_targets": ["apology_repair_expression_refinement"],
                    "repair_followup_required": True,
                },
            )
            self._write_json(
                growth_dir / "relationship_learning_plan.json",
                {
                    "schema_version": "relationship_learning_plan_v0",
                    "relationship_targets": [
                        "repair_reentry_timing_adjustment",
                        "relationship_pacing_adjustment",
                    ],
                    "repair_followup_required": True,
                },
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
                "resident_background_lineage_state": {
                    "schema_version": "resident_background_lineage_state_v0",
                    "governance_phase": "waiting_heartbeat_active",
                    "generation": 2,
                    "depth_band": "persistent_lineage",
                    "waiting_posture": "persistent_background_hold",
                    "cadence_weight": "persistent",
                    "evidence_refs": [
                        "runtime/state/terminal/resident_governance_state.json",
                    ],
                    "language_presence": {
                        "long_horizon_language_refs": [
                            "runtime/state/relationship/relationship_timeline.json",
                        ],
                        "governance_attention_target": "relationship_timeline",
                        "live_language_turn_refs": [
                            "runtime/state/language/language_percept_frame.json",
                            "runtime/state/language/semantic_map_frame.json",
                            "runtime/state/language/inner_speech_frame.json",
                            "runtime/state/language/expression_monitor_state.json",
                            "runtime/state/language/expression_plan.json",
                        ],
                        "last_live_semantic_focus": "repair_commitment_shared_language",
                    },
                    "identity_consciousness_birth_presence": {
                        "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
                        "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
                        "metacognition_ref": "runtime/state/consciousness/metacognition_state.json",
                        "consciousness_probe_ref": "runtime/state/consciousness/consciousness_probe_bundle.json",
                        "birth_readiness_rollup_ref": "runtime/state/life_targets/birth_readiness_rollup.json",
                        "birth_readiness_stage_gate_ref": "runtime/state/life_targets/birth_readiness_stage_gate.json",
                        "consciousness_waiting_posture": "consciousness_reportable_waiting",
                        "consciousness_reportability_flags": [
                            "workspace_access_present",
                            "broadcast_targets_present",
                            "metacognition_present",
                        ],
                        "birth_readiness_waiting_posture": "birth_open_waiting",
                        "birth_readiness_decision": "open",
                        "birth_readiness_next_required_command": "digital life",
                        "identity_consciousness_birth_refs": [
                            "runtime/state/consciousness/workspace_frame.json",
                            "runtime/state/consciousness/broadcast_frame.json",
                            "runtime/state/consciousness/metacognition_state.json",
                            "runtime/state/consciousness/consciousness_probe_bundle.json",
                            "runtime/state/life_targets/birth_readiness_rollup.json",
                            "runtime/state/life_targets/birth_readiness_stage_gate.json",
                        ],
                    },
                    "offline_learning_presence": {
                        "generation": 4,
                        "pressure_level": "elevated",
                        "attention_target": "relationship_learning_plan",
                        "ref_set": [
                            "runtime/state/growth/relationship_learning_plan.json",
                            "runtime/state/growth/language_learning_plan.json",
                        ],
                    },
                    "dream_wake_presence": {
                        "dream_window_kind": "nrem_like_replay",
                        "dream_fact_gate_result": "passed",
                        "wake_archive_requirement": "required_before_activation",
                        "wake_growth_seed_count": 2,
                        "wake_repair_target_count": 3,
                        "ref_set": [
                            "runtime/state/dream/offline_consolidation_frame.json",
                            "runtime/state/dream/dream_experience_window.json",
                            "runtime/state/dream/wake_integration_frame.json",
                            "runtime/state/dream/dream_fact_gate_decision.json",
                        ],
                    },
                },
            }
            expected_background_offline_learning_refs = [
                "runtime/state/growth/relationship_learning_plan.json",
                "runtime/state/growth/language_learning_plan.json",
            ]
            expected_background_dream_wake_refs = [
                "runtime/state/dream/offline_consolidation_frame.json",
                "runtime/state/dream/dream_experience_window.json",
                "runtime/state/dream/wake_integration_frame.json",
                "runtime/state/dream/dream_fact_gate_decision.json",
            ]
            expected_identity_consciousness_birth_refs = [
                "runtime/state/consciousness/workspace_frame.json",
                "runtime/state/consciousness/broadcast_frame.json",
                "runtime/state/consciousness/metacognition_state.json",
                "runtime/state/consciousness/consciousness_probe_bundle.json",
                "runtime/state/life_targets/birth_readiness_rollup.json",
                "runtime/state/life_targets/birth_readiness_stage_gate.json",
            ]
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
                signal_media_runtime={
                    "schema_version": "signal_media_runtime_v0",
                    "modulation_vector": {"repair_drive": "active"},
                },
                belief_state={
                    "schema_version": "belief_state_frame_v0",
                    "confidence_level": "unstable",
                },
                prediction_error_field={
                    "schema_version": "prediction_error_field_v0",
                    "error_events": [{"error_id": "prediction-error-001"}],
                },
                active_sampling_plan={
                    "schema_version": "active_sampling_plan_v0",
                    "selected_route": "clarify_with_relation_subject",
                    "stage_effect": "hold_for_evidence",
                },
                memory_write_gate={
                    "schema_version": "memory_write_gate_v0",
                    "stage_policy": "write_guarded_candidate_then_validate",
                },
                state_merge_guard={
                    "schema_version": "state_merge_guard_v0",
                    "stage_policy": "long_term_merge_fail_closed",
                },
                signal_media_runtime_ref="runtime/state/signal/signal_media_runtime.json",
                belief_state_ref="runtime/state/prediction/belief_state_frame.json",
                prediction_error_field_ref="runtime/state/prediction/prediction_error_field.json",
                active_sampling_plan_ref="runtime/state/prediction/active_sampling_plan.json",
                memory_write_gate_ref="runtime/state/memory/memory_write_gate.json",
                state_merge_guard_ref="runtime/state/memory/state_merge_guard.json",
                responsibility_loop_state_ref="runtime/state/action/responsibility_loop_state.json",
                world_contact_summary_ref="runtime/state/membrane/world_contact_summary.json",
                pain_regret_repair_report_ref="runtime/reports/latest/pain_regret_repair_report.json",
                language_percept_ref="runtime/state/language/language_percept_frame.json",
                semantic_map_ref="runtime/state/language/semantic_map_frame.json",
                inner_speech_ref="runtime/state/language/inner_speech_frame.json",
                expression_monitor_ref="runtime/state/language/expression_monitor_state.json",
                expression_plan_ref="runtime/state/language/expression_plan.json",
                live_semantic_focus="repair_commitment_shared_language",
                live_ambiguity_flags=["shared_term_unresolved"],
                live_repair_trigger_candidates=["repair-language-v0-0001"],
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
            persisted_relationship_timeline = self._read_json(
                relationship_dir / "relationship_timeline.json"
            )
            persisted_commitment_expression_plan = self._read_json(
                language_dir / "commitment_expression_plan.json"
            )
            persisted_apology_repair_language_trace = self._read_json(
                language_dir / "apology_repair_language_trace.json"
            )
            persisted_relationship_memory = self._read_json(
                memory_dir / "relationship_memory.json"
            )
            persisted_state_merge_guard = self._read_json(
                memory_dir / "state_merge_guard.json"
            )
            persisted_self_model = self._read_json(self_dir / "self_model.json")
            persisted_trait_drift = self._read_json(body_dir / "trait_drift_monitor.json")
            persisted_life_state = self._read_json(runtime_root / "state" / "life_state.json")
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
                "repair_guarded_continuity",
            )
            self.assertEqual(
                persisted_relationship_graph["subjects"][0]["relationship_stage_reason"],
                "repair_followup_required_after_multi_turn_dialogue",
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
                persisted_relationship_timeline["dialogue_turn_refs"],
                [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                ],
            )
            self.assertEqual(
                persisted_relationship_timeline["relationship_continuity_reports"][0]["continuity_state"],
                "offline_learning_repairing_continuity",
            )
            self.assertEqual(
                persisted_commitment_expression_plan["delay_or_release_decision"],
                "hold_for_nightmare_rewrite_integration",
            )
            self.assertIn(
                "paced_reentry",
                persisted_commitment_expression_plan["act_type_order"],
            )
            self.assertEqual(
                persisted_commitment_expression_plan["queue_e_repair_pressure_level"],
                "elevated",
            )
            self.assertIn(
                "responsibility_repair_modulation",
                persisted_commitment_expression_plan["act_type_order"],
            )
            self.assertIn(
                "runtime/state/membrane/world_contact_summary.json",
                persisted_commitment_expression_plan["queue_e_repair_ref_set"],
            )
            self.assertEqual(
                persisted_apology_repair_language_trace["repair_window_mode"],
                "nightmare_rewrite_first",
            )
            self.assertEqual(
                persisted_apology_repair_language_trace["queue_e_repair_pressure_level"],
                "elevated",
            )
            self.assertIn(
                "responsibility_repair_modulation",
                persisted_apology_repair_language_trace["move_type_order"],
            )
            self.assertIn(
                "runtime/state/growth/relationship_learning_plan.json",
                persisted_relationship_memory["offline_learning_refs"],
            )
            self.assertEqual(
                persisted_relationship_memory["queue_e_repair_pressure_level"],
                "elevated",
            )
            self.assertIn(
                "runtime/reports/latest/pain_regret_repair_report.json",
                persisted_relationship_memory["queue_e_repair_refs"],
            )
            self.assertIn(
                "runtime/reports/latest/resumed_external_dialogue_packet.json",
                persisted_relationship_memory["last_contact_refs"],
            )
            state_merge_change_sources = persisted_state_merge_guard[
                "long_term_change_sources"
            ]
            self.assertIn(
                "runtime/state/growth/language_learning_plan.json",
                state_merge_change_sources["offline_learning_cumulative_refs"],
            )
            self.assertIn(
                "runtime/reports/latest/pain_regret_repair_report.json",
                state_merge_change_sources["queue_e_repair_modulation_refs"],
            )
            self.assertIn(
                "runtime/state/dream/nightmare_loop_risk.json",
                state_merge_change_sources["relationship_memory_offline_refs"],
            )
            self.assertIn(
                "runtime/state/membrane/world_contact_summary.json",
                persisted_state_merge_guard["merge_routes"][0]["source_refs"],
            )
            self.assertEqual(
                persisted_state_merge_guard["last_projected_from_relationship_memory_ref"],
                "runtime/state/memory/relationship_memory.json",
            )
            self.assertGreaterEqual(
                persisted_life_state["state_merge_records"][0][
                    "long_term_change_source_count"
                ],
                8,
            )
            self.assertIn(
                "runtime/state/dream/nightmare_loop_risk.json",
                persisted_life_state["memory_index"]["dream_memory_refs"],
            )
            self.assertIn(
                "runtime/state/growth/language_learning_plan.json",
                persisted_life_state["language_state"]["offline_learning_refs"],
            )
            self.assertEqual(
                persisted_life_state["language_state"]["queue_e_repair_pressure_level"],
                "elevated",
            )
            self.assertIn(
                "runtime/state/membrane/world_contact_summary.json",
                persisted_life_state["language_state"]["queue_e_repair_refs"],
            )
            self.assertEqual(
                persisted_life_state["relationship_subjects"][0][
                    "queue_e_repair_pressure_level"
                ],
                "elevated",
            )
            self.assertEqual(
                persisted_life_state["relationship_subjects"][0]["relationship_stage"],
                "repair_guarded_continuity",
            )
            trait_slow_variables = persisted_self_model["trait_slow_variables"]
            self.assertIn("repair_seriousness", trait_slow_variables)
            self.assertIn("continuity_drive", trait_slow_variables)
            self.assertGreater(
                trait_slow_variables["repair_seriousness"]["value"],
                trait_slow_variables["dialogue_warmth"]["value"],
            )
            self.assertEqual(
                trait_slow_variables["repair_seriousness"]["last_relationship_stage"],
                "repair_guarded_continuity",
            )
            self.assertEqual(
                persisted_life_state["self_model"]["trait_slow_variables"]["boundary_respect"]["last_relationship_stage"],
                "repair_guarded_continuity",
            )
            self.assertEqual(
                persisted_trait_drift["schema_version"],
                "trait_drift_monitor_v0",
            )
            self.assertEqual(
                persisted_trait_drift["relationship_stage"],
                "repair_guarded_continuity",
            )
            self.assertIn(
                "repair_seriousness",
                persisted_trait_drift["slow_variable_summary"],
            )
            self.assertIn(
                "runtime/reports/latest/resumed_external_dialogue_packet.json",
                persisted_trait_drift["drift_observation_refs"],
            )
            self.assertTrue(persisted_self_model["growth_window_refs"])
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
                "runtime/state/memory/relationship_memory.json#offline_learning_refs",
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
                "runtime/state/action/responsibility_loop_state.json",
                dialogue_writeback_bundle["responsibility_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/life_state.json#responsibility_bindings",
                dialogue_writeback_bundle["life_state_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/life_state.json#language_state.offline_learning_refs",
                dialogue_writeback_bundle["life_state_writeback_refs"],
            )
            self.assertIn(
                "runtime/state/replay/replay_cue_bundle.json",
                dialogue_writeback_bundle["replay_cue_refs"],
            )
            self.assertEqual(
                dialogue_writeback_bundle["prediction_write_gate_refs"],
                [
                    "runtime/state/signal/signal_media_runtime.json",
                    "runtime/state/prediction/belief_state_frame.json",
                    "runtime/state/prediction/prediction_error_field.json",
                    "runtime/state/prediction/active_sampling_plan.json",
                    "runtime/state/memory/memory_write_gate.json",
                    "runtime/state/memory/state_merge_guard.json",
                ],
            )
            self.assertEqual(
                dialogue_writeback_bundle["live_language_turn_refs"],
                [
                    "runtime/state/language/language_percept_frame.json",
                    "runtime/state/language/semantic_map_frame.json",
                    "runtime/state/language/inner_speech_frame.json",
                    "runtime/state/language/expression_monitor_state.json",
                    "runtime/state/language/expression_plan.json",
                ],
            )
            self.assertIn(
                "runtime/state/language/expression_plan.json",
                dialogue_writeback_bundle["resident_background_lineage_refs"],
            )
            self.assertIn(
                "runtime/state/consciousness/consciousness_probe_bundle.json",
                dialogue_writeback_bundle["resident_background_lineage_refs"],
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_identity_consciousness_birth_refs"
                ],
                expected_identity_consciousness_birth_refs,
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_offline_learning_refs"
                ],
                expected_background_offline_learning_refs,
            )
            self.assertEqual(
                dialogue_writeback_bundle[
                    "resident_background_lineage_dream_wake_refs"
                ],
                expected_background_dream_wake_refs,
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_last_live_semantic_focus"
                ],
                "repair_commitment_shared_language",
            )
            self.assertIn(
                "runtime/state/language/inner_speech_frame.json",
                resumed_dialogue_packet[
                    "resident_background_lineage_language_evidence_refs"
                ],
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_identity_consciousness_birth_refs"
                ],
                expected_identity_consciousness_birth_refs,
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_birth_readiness_decision"
                ],
                "open",
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_offline_learning_refs"
                ],
                expected_background_offline_learning_refs,
            )
            self.assertEqual(
                resumed_dialogue_packet[
                    "resident_background_lineage_dream_wake_refs"
                ],
                expected_background_dream_wake_refs,
            )
            self.assertEqual(
                resumed_dialogue_packet["dialogue_writeback_bundle_ref"],
                "runtime/reports/latest/dialogue_writeback_bundle.json",
            )
            self.assertEqual(
                resumed_dialogue_packet["world_contact_summary_ref"],
                "runtime/state/membrane/world_contact_summary.json",
            )
            self.assertEqual(
                resumed_dialogue_packet["prediction_waiting_posture"],
                "hold_for_evidence",
            )
            self.assertEqual(
                resumed_dialogue_packet["prediction_write_gate_refs"],
                dialogue_writeback_bundle["prediction_write_gate_refs"],
            )
            self.assertEqual(
                resumed_dialogue_packet["live_language_turn_refs"],
                dialogue_writeback_bundle["live_language_turn_refs"],
            )
            self.assertEqual(
                resumed_dialogue_packet["language_percept_ref"],
                "runtime/state/language/language_percept_frame.json",
            )
            self.assertEqual(
                resumed_dialogue_packet["semantic_map_ref"],
                "runtime/state/language/semantic_map_frame.json",
            )
            self.assertEqual(
                resumed_dialogue_packet["live_semantic_focus"],
                "repair_commitment_shared_language",
            )
            self.assertEqual(
                resumed_dialogue_packet["live_repair_trigger_candidates"],
                ["repair-language-v0-0001"],
            )
            self.assertEqual(
                persisted_terminal_loop["live_language_turn_refs"],
                dialogue_writeback_bundle["live_language_turn_refs"],
            )
            self.assertEqual(
                persisted_terminal_loop["last_live_semantic_focus"],
                "repair_commitment_shared_language",
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
