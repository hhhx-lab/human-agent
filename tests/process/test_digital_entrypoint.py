import json
import os
import subprocess
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

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

    def test_resident_terminal_slash_state_commands_inspect_without_relation_turn(self):
        from life_v0.digital_entry import _handle_resident_terminal_utterance

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory").mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "dream").mkdir(parents=True, exist_ok=True)
            (terminal_dir / "resident_lifecycle_state.json").write_text(
                json.dumps(
                    {
                    "schema_version": "resident_lifecycle_state_v0",
                    "status": "background_active",
                    "life_name": "Adam",
                    "residency_posture": "sleeping_waiting_for_relation_turn",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (paths["state_root"] / "memory" / "relationship_memory.json").write_text(
                json.dumps(
                    {
                    "schema_version": "relationship_memory_v0",
                    "relation_person_profile": {
                        "observed_names": ["何剑宝"],
                        "preference_hypotheses": [
                            "prefers_direct_non_mechanical_language"
                        ],
                    },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (
                paths["state_root"] / "memory" / "dialogue_memory_summary.json"
            ).write_text(
                json.dumps(
                    {
                    "schema_version": "dialogue_memory_summary_v0",
                    "source_dialogue_turn_count": 4,
                    "deduplicated_episode_summaries": [
                        {"summary": "何剑宝要求不要机械模板。"}
                    ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (
                paths["state_root"]
                / "dream"
                / "exit_dream_consolidation_summary.json"
            ).write_text(
                json.dumps(
                    {
                    "schema_version": "exit_dream_consolidation_summary_v0",
                    "entry_state": "dreaming_after_terminal_exit",
                    "relationship_theme_tags": ["non_mechanical_language_pressure"],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            memory_stdout = StringIO()
            with redirect_stdout(memory_stdout):
                memory_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/memory",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            dream_stdout = StringIO()
            with redirect_stdout(dream_stdout):
                dream_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/dream",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )

            self.assertIsNone(memory_exit)
            self.assertIsNone(dream_exit)
            self.assertIn("resident_state_inspection_v0", memory_stdout.getvalue())
            self.assertIn("memory", memory_stdout.getvalue())
            self.assertIn("何剑宝", memory_stdout.getvalue())
            self.assertIn("prefers_direct_non_mechanical_language", memory_stdout.getvalue())
            self.assertIn("resident_state_inspection_v0", dream_stdout.getvalue())
            self.assertIn("dream", dream_stdout.getvalue())
            self.assertIn("dreaming_after_terminal_exit", dream_stdout.getvalue())
            self.assertFalse((terminal_dir / "resident_relation_inbox.jsonl").exists())

    def test_resident_terminal_proactive_state_command_inspects_proactive_voice(self):
        from life_v0.digital_entry import _handle_resident_terminal_utterance

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (terminal_dir / "resident_terminal_proactive_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "resident_terminal_proactive_state_v0",
                        "status": "held_internal",
                        "last_focus": "relationship_memory",
                        "last_utterance": "",
                        "last_proactive_voice_profile": {
                            "schema_version": "resident_proactive_voice_profile_v0",
                            "surface_kind": "relationship_checkin",
                            "utterance_candidate_code_count": 2,
                            "utterance_candidate_codes": [
                                "wake_cue:remember_relation_person_name:何剑宝"
                            ],
                            "question_candidates": [
                                "wake_cue:remember_relation_person_name:何剑宝"
                            ],
                            "profile_coverage": {
                                "schema_version": "resident_proactive_voice_profile_coverage_v0",
                                "active_domains": ["memory", "waiting_governance"],
                                "active_domain_count": 2,
                                "domain_presence": {
                                    "memory": True,
                                    "memory_tier": False,
                                    "dream": False,
                                    "web_dream_learning": False,
                                    "resident_autonomous_activity": False,
                                    "waiting_governance": True,
                                },
                            },
                        },
                        "last_profile_coverage": {
                            "schema_version": "resident_proactive_voice_profile_coverage_v0",
                            "active_domains": ["memory", "waiting_governance"],
                            "active_domain_count": 2,
                            "domain_presence": {
                                "memory": True,
                                "memory_tier": False,
                                "dream": False,
                                "web_dream_learning": False,
                                "resident_autonomous_activity": False,
                                "waiting_governance": True,
                            },
                        },
                        "last_utterance_candidate_code_count": 2,
                        "last_release_scope": "open_terminal_idle_hidden",
                        "last_natural_language_released": False,
                        "last_post_expression_gate_status": "skipped",
                        "event_count": 1,
                        "release_count": 0,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            output = StringIO()
            with redirect_stdout(output):
                exit_code = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/proactive",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )

            self.assertIsNone(exit_code)
            self.assertIn("resident_state_inspection_v0", output.getvalue())
            self.assertIn("proactive_voice", output.getvalue())
            self.assertIn("relationship_checkin", output.getvalue())
            self.assertIn("coverage_summary", output.getvalue())
            self.assertIn("resident_proactive_voice_profile_coverage_v0", output.getvalue())
            self.assertIn("waiting_governance", output.getvalue())
            self.assertIn("utterance_candidate_code_count", output.getvalue())
            self.assertIn(
                "state_codes_only_model_expression_required",
                output.getvalue(),
            )

    def test_resident_terminal_relation_turn_without_model_release_stays_silent(self):
        from life_v0.digital_entry import _handle_resident_terminal_utterance

        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            terminal_dir.mkdir(parents=True, exist_ok=True)
            stdout = StringIO()
            with patch(
                "life_v0.digital_entry.send_resident_relation_turn",
                return_value=SimpleNamespace(
                    exit_code=0,
                    state={
                        "send_status": "completed",
                        "response_text": "",
                        "response_event": {"status": "completed_unreleased"},
                    },
                ),
            ):
                with redirect_stdout(stdout):
                    exit_code = _handle_resident_terminal_utterance(
                        terminal_dir=terminal_dir,
                        utterance="不要给我固定回答",
                        life_name="Adam",
                        say_timeout_seconds=0.1,
                    )

            self.assertIsNone(exit_code)
            self.assertEqual(stdout.getvalue(), "")

    def test_resident_terminal_slash_commands_cover_life_state_surfaces(self):
        from life_v0.digital_entry import _handle_resident_terminal_utterance

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            for relative_dir in [
                "body",
                "self",
                "signal",
                "prediction",
                "perception",
                "terminal",
                "life_targets",
                "contracts",
            ]:
                (paths["state_root"] / relative_dir).mkdir(
                    parents=True,
                    exist_ok=True,
                )
            self._write_json(
                paths["state_root"] / "body" / "core_affect_vector.json",
                {
                    "schema_version": "core_affect_vector_v0",
                    "valence": -0.2,
                    "arousal": 0.42,
                    "dominance": 0.5,
                    "pain_pressure": 0.35,
                    "relationship_tension": 0.45,
                    "dream_residue_load": 0.4,
                    "responsibility_weight": 0.5,
                    "repair_drive": "active",
                },
            )
            self._write_json(
                paths["state_root"] / "body" / "affective_episode.json",
                {
                    "schema_version": "affective_episode_v0",
                    "episode_label": "guarded_repair_tension",
                    "expression_risk": "guarded",
                    "repair_bias": "relationship_and_responsibility_repair",
                },
            )
            self._write_json(
                paths["state_root"] / "body" / "emotion_regulation_loop.json",
                {
                    "schema_version": "emotion_regulation_loop_v0",
                    "regulation_mode": "hold_then_articulate",
                    "expression_delay_required": True,
                    "suppression_cost": 0.18,
                },
            )
            self._write_json(
                paths["state_root"] / "self" / "self_model.json",
                {
                    "schema_version": "self_model_state_v0",
                    "trait_slow_variables": {"continuity_drive": {"value": 0.7}},
                },
            )
            self._write_json(
                paths["state_root"] / "body" / "trait_drift_monitor.json",
                {"schema_version": "trait_drift_monitor_v0"},
            )
            self._write_json(
                paths["state_root"] / "body" / "need_state_vector.json",
                {
                    "schema_version": "need_state_vector_v0",
                    "resource_deficit": "guarded_maintenance",
                    "repair_drive": "active",
                    "social_readiness": "dialogic_guarded_open",
                    "cognitive_bandwidth": "guarded_dialogic",
                    "sleep_pressure": "offline_ready",
                },
            )
            self._write_json(
                paths["state_root"] / "body" / "body_resource_budget.json",
                {
                    "schema_version": "body_resource_budget_v0",
                    "energy_state": {"level": "guarded_reserve"},
                    "fatigue_state": {"level": "managed_low_noise"},
                    "maintenance_pressure": {
                        "resource_deficit": "guarded_maintenance",
                        "repair_drive": "active",
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "body" / "body_rhythm_pulse.json",
                {
                    "schema_version": "body_rhythm_pulse_v0",
                    "rhythm_state": "pre_activation_guarded",
                    "heartbeat_counter": 4,
                    "fatigue_load": "managed_low_noise",
                    "allostatic_load": "guarded_maintenance",
                },
            )
            self._write_json(
                paths["state_root"] / "signal" / "signal_media_runtime.json",
                {
                    "schema_version": "signal_media_runtime_v0",
                    "modulation_vector": {
                        "arousal": "awake",
                        "precision": "relationship_high",
                        "repair_drive": "active",
                        "language_precision": "careful",
                    },
                    "body_signal_profile": {
                        "schema_version": "body_signal_modulation_profile_v0",
                        "memory_write_bias": "repair_evidence_first",
                        "dream_pressure_bias": "offline_consolidation_pressure",
                        "language_tempo_bias": "guarded_deliberate",
                        "body_signal_strength": 0.71,
                        "offline_learning_pressure_level": "elevated",
                        "offline_learning_integration_mode": (
                            "relationship_offline_reconsolidation_required"
                        ),
                    },
                },
            )
            self._write_json(
                terminal_dir / "idle_strategy_state.json",
                {
                    "schema_version": "idle_strategy_state_v0",
                    "waiting_posture": "repair_weighted_waiting",
                    "governance_attention_target": "body_signal_memory_gate",
                    "governance_attention_reason": "repair_drive_active",
                    "next_idle_action": "memory_recall",
                    "heartbeat_interval_ms": 1200,
                    "body_signal_write_bias": "repair_evidence_first",
                },
            )
            self._write_json(
                paths["state_root"] / "prediction" / "belief_state_frame.json",
                {"schema_version": "belief_state_frame_v0"},
            )
            self._write_json(
                paths["state_root"] / "perception" / "visual_observation_frame.json",
                {"schema_version": "visual_observation_frame_v0"},
            )
            self._write_json(
                terminal_dir / "life_context_frame.json",
                {"schema_version": "life_context_frame_v0"},
            )
            self._write_json(
                terminal_dir / "relation_turn_frame.json",
                {"schema_version": "relation_turn_frame_v0"},
            )
            self._write_json(
                terminal_dir / "terminal_input_profile.json",
                {
                    "schema_version": "terminal_input_profile_v0",
                    "input_mode": "char_line_editor_with_idle_voice",
                    "line_editing": {
                        "backspace": "delete_previous_character",
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "life_targets" / "birth_readiness_rollup.json",
                {"schema_version": "birth_readiness_rollup_v0"},
            )
            self._write_json(
                paths["state_root"] / "contracts" / "v0_contract_file_index.json",
                {"schema_version": "v0_contract_file_index_v0"},
            )
            self._write_json(
                paths["state_root"] / "memory" / "relationship_memory.json",
                {
                    "schema_version": "relationship_memory_v0",
                    "salient_core_memory_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.salient_core"
                    ],
                    "retrievable_context_memory_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.retrievable_context"
                    ],
                    "deep_sediment_memory_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.deep_sediment"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "memory" / "dialogue_memory_summary.json",
                {
                    "schema_version": "dialogue_memory_summary_v0",
                    "memory_tiering_ref": (
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering"
                    ),
                },
            )
            self._write_json(
                paths["state_root"] / "memory" / "engram_index.json",
                {
                    "schema_version": "engram_index_v0",
                    "memory_tier_index": {
                        "schema_version": "engram_memory_tier_index_v0",
                        "salient_core_refs": [
                            "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.salient_core"
                        ],
                        "retrievable_context_refs": [
                            "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.retrievable_context"
                        ],
                        "deep_sediment_refs": [
                            "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.deep_sediment"
                        ],
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "self" / "autobiographical_stack.json",
                {
                    "schema_version": "autobiographical_stack_v0",
                    "anchor_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ],
                },
            )
            self._write_json(
                paths["state_root"]
                / "dream"
                / "exit_dream_consolidation_summary.json",
                {
                    "schema_version": "exit_dream_consolidation_summary_v0",
                    "memory_tiering": {
                        "schema_version": "exit_dream_memory_tiering_v0",
                        "salient_core_episode_refs": ["episode-1"],
                        "retrievable_context_episode_refs": ["episode-2"],
                        "deep_sediment_episode_refs": ["episode-3"],
                    },
                },
            )

            checks = {
                "/body": "body_grounding_summary_v0",
                "/emotion": "emotion_regulation_summary_v0",
                "/personality": "self_model_state_v0",
                "/inner": "inner_environment_modulation_summary_v0",
                "/vision": "visual_observation_frame_v0",
                "/context": "life_context_frame_v0",
                "/ability": "birth_readiness_rollup_v0",
                "/state": "terminal_input_profile_v0",
            }
            for command, expected_fragment in checks.items():
                output = StringIO()
                with redirect_stdout(output):
                    exit_code = _handle_resident_terminal_utterance(
                        terminal_dir=terminal_dir,
                        utterance=command,
                        life_name="Adam",
                        say_timeout_seconds=0.1,
                    )
                self.assertIsNone(exit_code)
                self.assertIn("resident_state_inspection_v0", output.getvalue())
                self.assertIn(expected_fragment, output.getvalue())

            body_output = StringIO()
            with redirect_stdout(body_output):
                body_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/body",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            emotion_output = StringIO()
            with redirect_stdout(emotion_output):
                emotion_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/emotion",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            inner_output = StringIO()
            with redirect_stdout(inner_output):
                inner_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/inner",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            self.assertIsNone(body_exit)
            self.assertIsNone(emotion_exit)
            self.assertIsNone(inner_exit)
            self.assertIn("body_signal_modulation_profile_v0", body_output.getvalue())
            self.assertIn("repair_evidence_first", body_output.getvalue())
            self.assertIn(
                "body_state_modulates_expression_without_spoken_signal_dump",
                body_output.getvalue(),
            )
            self.assertIn("guarded_repair_tension", emotion_output.getvalue())
            self.assertIn(
                "emotion_state_modulates_language_not_template_emotion_speech",
                emotion_output.getvalue(),
            )
            self.assertIn(
                "inner_environment_summary_is_state_view_not_dialogue_response",
                inner_output.getvalue(),
            )
            self.assertIn("guarded_deliberate", inner_output.getvalue())

            memory_output = StringIO()
            with redirect_stdout(memory_output):
                memory_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/memory",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            dream_output = StringIO()
            with redirect_stdout(dream_output):
                dream_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/dream",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            self.assertIsNone(memory_exit)
            self.assertIsNone(dream_exit)
            self.assertIn("tiering", memory_output.getvalue())
            self.assertIn("salient_core_memory_refs", memory_output.getvalue())
            self.assertIn("deep_sediment_memory_refs", memory_output.getvalue())
            self.assertIn("memory_tiering", dream_output.getvalue())
            self.assertIn("salient_core_episode_refs", dream_output.getvalue())
            self.assertIn("deep_sediment_episode_refs", dream_output.getvalue())

            self.assertFalse((terminal_dir / "resident_relation_inbox.jsonl").exists())

    def test_resident_terminal_language_command_shows_generation_consumption_summary(self):
        from life_v0.digital_entry import _handle_resident_terminal_utterance

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            for relative_dir in [
                "language",
                "memory",
                "dream",
                "body",
                "signal",
                "relationship",
                "action",
                "prediction",
                "terminal",
            ]:
                (paths["state_root"] / relative_dir).mkdir(
                    parents=True,
                    exist_ok=True,
                )
            paths["reports"].mkdir(parents=True, exist_ok=True)
            self._write_json(
                paths["state_root"] / "language" / "language_percept_frame.json",
                {
                    "schema_version": "language_percept_frame_v0",
                    "semantic_focus": "关系语言不要机械化",
                },
            )
            self._write_json(
                paths["state_root"] / "language" / "semantic_map_frame.json",
                {
                    "schema_version": "semantic_map_frame_v0",
                    "semantic_focus": "关系语言不要机械化",
                },
            )
            self._write_json(
                paths["state_root"] / "language" / "inner_speech_frame.json",
                {
                    "schema_version": "inner_speech_frame_v0",
                    "inner_drive_states": {
                        "repair": "active",
                        "continuity": "active",
                    },
                },
            )
            self._write_json(
                paths["state_root"]
                / "language"
                / "expression_monitor_state.json",
                {
                    "schema_version": "expression_monitor_state_v0",
                    "monitor_status": "guarding_non_template_expression",
                },
            )
            self._write_json(
                paths["state_root"] / "language" / "expression_plan.json",
                {
                    "schema_version": "expression_plan_v0",
                    "semantic_goal": "answer_from_relation_context",
                },
            )
            self._write_json(
                paths["state_root"] / "language" / "model_expression_state.json",
                {
                    "schema_version": "model_expression_state_v0",
                    "model_expression_status": "model_expression_applied",
                    "model_expression_context_summary": {
                        "relationship_stage": "shared_continuity",
                    },
                    "post_expression_gate": {
                        "schema_version": "post_expression_gate_v0",
                        "gate_status": "accepted",
                        "required_evidence_flags": [
                            "relationship_continuity",
                            "memory_continuity",
                            "body_affect",
                            "prediction_attention",
                        ],
                        "missing_evidence_flags": [],
                        "soft_missing_evidence_flags": [],
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "memory" / "relationship_memory.json",
                {
                    "schema_version": "relationship_memory_v0",
                    "relation_person_profile": {
                        "observed_names": ["何剑宝"],
                    },
                    "next_wake_cues": [
                        "continue_less_mechanical_language"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "memory" / "dialogue_memory_summary.json",
                {
                    "schema_version": "dialogue_memory_summary_v0",
                    "next_wake_cues": ["ask_about_current_language_feel"],
                },
            )
            self._write_json(
                paths["state_root"] / "memory" / "memory_retrieval_frame.json",
                {
                    "schema_version": "memory_retrieval_frame_v0",
                    "reconstruction_focus": "relationship_continuity",
                    "activated_refs": [
                        "runtime/state/memory/engram_index.json#episode/non_template"
                    ],
                },
            )
            self._write_json(
                paths["state_root"]
                / "dream"
                / "exit_dream_consolidation_summary.json",
                {
                    "schema_version": "exit_dream_consolidation_summary_v0",
                    "memory_tiering": {
                        "salient_core_episode_refs": ["episode-1"],
                        "retrievable_context_episode_refs": ["episode-2"],
                        "deep_sediment_episode_refs": ["episode-3"],
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "body" / "core_affect_vector.json",
                {
                    "schema_version": "core_affect_vector_v0",
                    "arousal": 0.55,
                    "repair_drive": "active",
                },
            )
            self._write_json(
                paths["state_root"] / "body" / "body_resource_budget.json",
                {
                    "schema_version": "body_resource_budget_v0",
                    "fatigue_state": {"level": "low"},
                },
            )
            self._write_json(
                paths["state_root"] / "signal" / "signal_media_runtime.json",
                {
                    "schema_version": "signal_media_runtime_v0",
                    "modulation_vector": {
                        "arousal": "awake",
                        "precision": "relationship_high",
                        "repair_drive": "active",
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "relationship" / "relationship_timeline.json",
                {
                    "schema_version": "relationship_timeline_v0",
                    "relationship_stage": "shared_continuity",
                },
            )
            self._write_json(
                paths["state_root"] / "relationship" / "commitment_truth_state.json",
                {
                    "schema_version": "commitment_truth_state_v0",
                    "truth_status": "active",
                },
            )
            self._write_json(
                paths["state_root"] / "action" / "responsibility_loop_state.json",
                {
                    "schema_version": "responsibility_loop_state_v0",
                    "repair_followup_required": True,
                    "regret_pressure_candidates": ["template_language_regret"],
                },
            )
            self._write_json(
                paths["reports"] / "pain_regret_repair_report.json",
                {
                    "schema_version": "pain_regret_repair_report_v0",
                    "repair_followup_required": True,
                    "regret_pressure_refs": ["runtime/state/action/responsibility_loop_state.json"],
                },
            )
            self._write_json(
                paths["state_root"] / "prediction" / "belief_state_frame.json",
                {
                    "schema_version": "belief_state_frame_v0",
                },
            )
            self._write_json(
                paths["state_root"] / "prediction" / "prediction_error_field.json",
                {
                    "schema_version": "prediction_error_field_v0",
                    "error_events": ["language_style_mismatch"],
                },
            )
            self._write_json(
                paths["state_root"] / "prediction" / "active_sampling_plan.json",
                {
                    "schema_version": "active_sampling_plan_v0",
                    "selected_route": "clarify",
                },
            )
            self._write_json(
                terminal_dir / "resident_autonomous_activity_state.json",
                {
                    "schema_version": "resident_autonomous_activity_state_v0",
                    "last_activity_kind": "memory_recall",
                },
            )
            self._write_json(
                terminal_dir / "resident_terminal_proactive_state.json",
                {
                    "schema_version": "resident_terminal_proactive_state_v0",
                    "status": "held_internal",
                },
            )

            output = StringIO()
            with redirect_stdout(output):
                exit_code = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/language",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )

            rendered = output.getvalue()
            self.assertIsNone(exit_code)
            self.assertIn("resident_state_inspection_v0", rendered)
            self.assertIn("language_generation_consumption_summary_v0", rendered)
            self.assertIn("generation_consumption_summary", rendered)
            self.assertIn("relationship_memory", rendered)
            self.assertIn("dream_residue", rendered)
            self.assertIn("body_affect", rendered)
            self.assertIn("responsibility_repair", rendered)
            self.assertIn("prediction_attention", rendered)
            self.assertIn("resident_autonomous_activity", rendered)
            self.assertIn("proactive_voice", rendered)
            self.assertIn("state_inspection_only_model_expression_then_post_gate", rendered)
            self.assertIn("no_code_spoken_template_no_inspection_summary_as_reply", rendered)
            self.assertIn("relationship_continuity", rendered)
            self.assertIn("memory_continuity", rendered)
            self.assertIn("何剑宝", rendered)
            self.assertFalse((terminal_dir / "resident_relation_inbox.jsonl").exists())

    def test_resident_terminal_proactive_voice_uses_state_without_relation_turn(self):
        from life_v0.process_supervisor.proactive_terminal_voice import (
            build_resident_proactive_terminal_event,
            write_resident_proactive_terminal_event,
        )

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory").mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "dream").mkdir(parents=True, exist_ok=True)
            (terminal_dir / "resident_autonomous_activity_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "resident_autonomous_activity_state_v0",
                        "activity_count": 7,
                        "last_activity_kind": "learning_consolidation",
                        "next_activity_kind": "memory_recall",
                        "cycle_completion_count": 1,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (paths["state_root"] / "memory" / "relationship_memory.json").write_text(
                json.dumps(
                    {
                        "schema_version": "relationship_memory_v0",
                        "relation_person_profile": {
                            "observed_names": ["何剑宝"],
                            "preference_hypotheses": [
                                "prefers_direct_non_mechanical_language",
                                "cares_about_being_remembered",
                            ],
                        },
                        "relationship_theme_tags": [
                            "digital_life_memory_seriousness",
                            "non_mechanical_language_pressure",
                        ],
                        "next_wake_cues": [
                            "ask_about_language_naturalness_without_template"
                        ],
                        "memory_tier_projection": {
                            "salient_core_episode_refs": [
                                "runtime/state/memory/engram_index.json#episode/non_mechanical_language_pressure"
                            ],
                            "retrievable_context_episode_refs": [
                                "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering/retrievable_context"
                            ],
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (
                paths["state_root"]
                / "dream"
                / "exit_dream_consolidation_summary.json"
            ).write_text(
                json.dumps(
                    {
                        "schema_version": "exit_dream_consolidation_summary_v0",
                        "entry_state": "dreaming_after_terminal_exit",
                        "relationship_theme_tags": [
                            "non_mechanical_language_pressure"
                        ],
                        "next_wake_cues": [
                            "follow_up_on_being_less_mechanical"
                        ],
                        "memory_tiering": {
                            "deep_sediment_episode_refs": [
                                "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering/deep_sediment"
                            ]
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (terminal_dir / "idle_strategy_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "idle_strategy_state_v0",
                        "governance_attention_target": "relationship_memory",
                        "next_idle_action": "open_terminal_idle_model_expression",
                        "body_waiting_posture": "quiet_relation_available",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            event = build_resident_proactive_terminal_event(
                terminal_dir=terminal_dir,
                life_name="Adam",
                now_iso=lambda: "2026-06-13T10:00:00+08:00",
            )
            written = write_resident_proactive_terminal_event(
                terminal_dir=terminal_dir,
                event=event,
            )

            self.assertEqual(
                written["schema_version"],
                "resident_proactive_terminal_event_v0",
            )
            self.assertEqual(written["status"], "held_internal")
            self.assertEqual(written["release_scope"], "open_terminal_idle_hidden")
            self.assertFalse(written["natural_language_released"])
            self.assertEqual(written["utterance"], "")
            self.assertEqual(written["focus"], "memory_tiered_wake_cue")
            profile = written["proactive_voice_profile"]
            self.assertEqual(profile["schema_version"], "resident_proactive_voice_profile_v0")
            self.assertGreaterEqual(profile["utterance_candidate_code_count"], 4)
            self.assertTrue(
                all(":" in code for code in profile["utterance_candidate_codes"])
            )
            self.assertEqual(profile["question_candidates"], profile["utterance_candidate_codes"])
            coverage = profile["profile_coverage"]
            self.assertEqual(
                coverage["schema_version"],
                "resident_proactive_voice_profile_coverage_v0",
            )
            self.assertEqual(coverage["active_domain_count"], 5)
            self.assertEqual(
                set(coverage["active_domains"]),
                {
                    "memory",
                    "memory_tier",
                    "dream",
                    "resident_autonomous_activity",
                    "waiting_governance",
                },
            )
            self.assertEqual(coverage["domain_presence"]["web_dream_learning"], False)
            self.assertTrue(
                (terminal_dir / "resident_terminal_proactive_events.jsonl").exists()
            )
            self.assertTrue(
                (terminal_dir / "resident_terminal_proactive_state.json").exists()
            )
            state = self._read_json(terminal_dir / "resident_terminal_proactive_state.json")
            self.assertEqual(
                state["last_profile_coverage"]["active_domains"],
                coverage["active_domains"],
            )
            self.assertEqual(
                state["last_utterance_candidate_code_count"],
                profile["utterance_candidate_code_count"],
            )
            self.assertFalse((terminal_dir / "resident_relation_inbox.jsonl").exists())

    def test_resident_terminal_proactive_voice_prints_without_relation_inbox(self):
        from life_v0.digital_entry import _emit_resident_proactive_terminal_voice

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory").mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory" / "relationship_memory.json").write_text(
                json.dumps(
                    {
                        "schema_version": "relationship_memory_v0",
                        "relation_person_profile": {
                            "observed_names": ["何剑宝"],
                            "preference_hypotheses": [
                                "prefers_direct_non_mechanical_language"
                            ],
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            output = StringIO()
            with redirect_stdout(output):
                emitted = _emit_resident_proactive_terminal_voice(
                    terminal_dir=terminal_dir,
                    life_name="Adam",
                    now_iso=lambda: "2026-06-13T10:10:00+08:00",
                )

            self.assertFalse(emitted)
            self.assertEqual(output.getvalue(), "")
            self.assertTrue(
                (terminal_dir / "resident_terminal_proactive_events.jsonl").exists()
            )
            self.assertFalse((terminal_dir / "resident_relation_inbox.jsonl").exists())

    def test_resident_terminal_proactive_voice_releases_only_model_expression(self):
        from life_v0.digital_entry import _emit_resident_proactive_terminal_voice

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory").mkdir(parents=True, exist_ok=True)
            self._write_json(
                paths["state_root"] / "memory" / "relationship_memory.json",
                {
                    "schema_version": "relationship_memory_v0",
                    "relation_person_profile": {
                        "observed_names": ["RelationPeer"],
                    },
                },
            )

            captured_payload = {}

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                captured_payload["payload"] = payload
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": "MODEL_PROACTIVE_TOKEN"},
                        }
                    ]
                }

            output = StringIO()
            with redirect_stdout(output):
                emitted = _emit_resident_proactive_terminal_voice(
                    terminal_dir=terminal_dir,
                    life_name="Adam",
                    now_iso=lambda: "2026-06-13T10:20:00+08:00",
                    model_transport=fake_transport,
                    environ={
                        "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                        "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                        "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                        "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                    },
                )

            self.assertTrue(emitted)
            self.assertIn("MODEL_PROACTIVE_TOKEN", output.getvalue())
            self.assertIn("expression_context", json.dumps(captured_payload["payload"]))
            state = self._read_json(
                terminal_dir / "resident_terminal_proactive_state.json"
            )
            self.assertEqual(state["last_utterance"], "MODEL_PROACTIVE_TOKEN")
            self.assertEqual(
                state["last_model_expression_status"],
                "model_expression_applied",
            )
            self.assertEqual(state["status"], "released_model_expression")
            self.assertEqual(state["last_release_scope"], "open_terminal_idle_model_expression")
            self.assertTrue(state["last_natural_language_released"])
            self.assertEqual(state["release_count"], 1)
            self.assertFalse((terminal_dir / "resident_relation_inbox.jsonl").exists())

    def test_resident_terminal_proactive_voice_blocks_template_model_surface(self):
        from life_v0.digital_entry import _emit_resident_proactive_terminal_voice

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory").mkdir(parents=True, exist_ok=True)
            self._write_json(
                paths["state_root"] / "memory" / "relationship_memory.json",
                {
                    "schema_version": "relationship_memory_v0",
                    "relation_person_profile": {
                        "observed_names": ["RelationPeer"],
                    },
                },
            )

            def fake_transport(endpoint, headers, payload, timeout_seconds):
                return {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {
                                "content": "作为一个AI，我会根据你的要求处理。schema_version"
                            },
                        }
                    ]
                }

            output = StringIO()
            with redirect_stdout(output):
                emitted = _emit_resident_proactive_terminal_voice(
                    terminal_dir=terminal_dir,
                    life_name="Adam",
                    now_iso=lambda: "2026-06-13T10:25:00+08:00",
                    model_transport=fake_transport,
                    environ={
                        "DIGITAL_LIFE_MODEL_PROVIDER": "openai-compatible",
                        "DIGITAL_LIFE_MODEL_NAME": "gpt-5.5",
                        "DIGITAL_LIFE_MODEL_BASE_URL": "https://model.example/v1",
                        "DIGITAL_LIFE_MODEL_API_KEY": "secret-token",
                    },
                )

            self.assertFalse(emitted)
            self.assertEqual(output.getvalue(), "")
            state = self._read_json(
                terminal_dir / "resident_terminal_proactive_state.json"
            )
            self.assertEqual(state["status"], "held_internal")
            self.assertFalse(state["last_natural_language_released"])
            self.assertEqual(state["release_count"], 0)
            self.assertEqual(
                state["last_model_expression_status"],
                "model_expression_unreleased",
            )
            self.assertEqual(state["last_post_expression_gate_status"], "blocked")
            events = [
                json.loads(line)
                for line in (terminal_dir / "resident_terminal_proactive_events.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line.strip()
            ]
            self.assertEqual(events[-1]["utterance"], "")
            self.assertFalse(events[-1]["natural_language_released"])
            self.assertFalse((terminal_dir / "resident_relation_inbox.jsonl").exists())

    def test_resident_terminal_proactive_voice_can_surface_web_dream_learning_topic(self):
        from life_v0.digital_entry import _emit_resident_proactive_terminal_voice

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            dream_dir = paths["state_root"] / "dream"
            dream_dir.mkdir(parents=True, exist_ok=True)
            (dream_dir / "web_dream_learning_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "web_dream_learning_state_v0",
                        "status": "learned",
                        "topic_candidates": ["Neuroplasticity and sleep"],
                        "wake_question_candidates": [
                            "wake_question_about:Neuroplasticity and sleep"
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            output = StringIO()
            with redirect_stdout(output):
                emitted = _emit_resident_proactive_terminal_voice(
                    terminal_dir=terminal_dir,
                    life_name="Adam",
                    now_iso=lambda: "2026-06-13T10:30:00+08:00",
                )

            self.assertFalse(emitted)
            self.assertEqual(output.getvalue(), "")
            state = self._read_json(
                terminal_dir / "resident_terminal_proactive_state.json"
            )
            self.assertEqual(state["last_focus"], "web_dream_learning")
            self.assertEqual(state["status"], "held_internal")
            self.assertEqual(state["release_count"], 0)
            self.assertFalse((terminal_dir / "resident_relation_inbox.jsonl").exists())

    def test_interactive_resident_terminal_client_can_emit_idle_voice_before_exit(self):
        from life_v0.digital_entry import _run_interactive_resident_terminal_client

        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory").mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory" / "relationship_memory.json").write_text(
                json.dumps(
                    {
                        "schema_version": "relationship_memory_v0",
                        "relation_person_profile": {
                            "observed_names": ["何剑宝"],
                            "preference_hypotheses": [
                                "prefers_direct_non_mechanical_language"
                            ],
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            def read_line_fn(**kwargs):
                self.assertFalse(kwargs["idle_voice_fn"]())
                return "/exit"

            output = StringIO()
            with redirect_stdout(output):
                exit_code = _run_interactive_resident_terminal_client(
                    terminal_dir=terminal_dir,
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                    read_line_fn=read_line_fn,
                )

            self.assertEqual(exit_code, 0)
            self.assertNotIn("何剑宝", output.getvalue())
            self.assertTrue(
                (terminal_dir / "resident_terminal_proactive_events.jsonl").exists()
            )
            state = self._read_json(terminal_dir / "resident_terminal_proactive_state.json")
            self.assertIn(state["status"], {"held_internal", "released_model_expression"})
            self.assertFalse((terminal_dir / "resident_relation_inbox.jsonl").exists())

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
            model_expression_state["unreleased_reason"],
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
            self.assertIn("Digital Life", completed.stdout)
            self.assertIn("终端已连接：Digital Life", completed.stdout)
            self.assertNotIn("这段关系本身", completed.stdout)
            self.assertNotIn("relational_checkin", completed.stdout)

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
                self.assertFalse(said.stdout.strip())
                self.assertNotIn("你还在后台吗？", said.stdout)

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
                self.assertEqual(outbox_events[-1]["status"], "completed_unreleased")
                self.assertEqual(outbox_events[-1]["response_text"], "")
                self.assertNotIn("你还在后台吗？", outbox_events[-1]["response_text"])
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
                self.assertNotIn("你能继续存在吗？", attached.stdout)

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

    def _write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

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
