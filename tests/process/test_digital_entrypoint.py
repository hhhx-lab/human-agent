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
                "consciousness",
                "perception",
                "terminal",
                "life_targets",
                "contracts",
                "relationship",
                "language",
                "memory",
                "dream",
                "growth",
                "archive",
                "action",
                "validation",
                "schema_runner",
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
                    "identity_mode": "anchor_locked",
                    "self_narrative_status": "seeded",
                    "trait_slow_variables": {
                        "continuity_drive": {
                            "value": 0.7,
                            "trend": "stabilizing",
                            "slow_variable_update_mode": (
                                "background_history_stabilized"
                            ),
                            "evidence_refs": [
                                "runtime/state/relationship/relationship_timeline.json#continuity"
                            ],
                        },
                        "repair_seriousness": {
                            "value": 0.82,
                            "trend": "rising",
                            "slow_variable_update_mode": (
                                "background_history_recalibration"
                            ),
                            "evidence_refs": [
                                "runtime/state/language/apology_repair_language_trace.json"
                            ],
                        },
                    },
                    "growth_window_refs": [
                        "runtime/state/growth/offline_learning_cumulative_profile.json"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "self" / "resident_self_thinking_state.json",
                {
                    "schema_version": "resident_self_thinking_state_v0",
                    "activity_kind": "self_thinking",
                    "thinking_mode": (
                        "self_model_and_resident_governance_reflection"
                    ),
                    "reflection_targets": [
                        "trait_slow_variables",
                        "background_convergence_history",
                        "consciousness_probe",
                        "inner_speech",
                    ],
                    "self_continuity_policy": (
                        "reflect_then_wait_for_relation_turn"
                    ),
                    "evidence_refs": [
                        "runtime/state/self/self_model.json",
                        "runtime/state/language/inner_speech_frame.json",
                        "runtime/state/consciousness/consciousness_probe_bundle.json",
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "body" / "trait_drift_monitor.json",
                {
                    "schema_version": "trait_drift_monitor_v0",
                    "slow_variable_targets": [
                        "continuity_drive",
                        "repair_seriousness",
                    ],
                    "drift_direction": "repair_recalibration",
                    "slow_variable_update_mode_summary": {
                        "background_history_recalibration": [
                            "repair_seriousness"
                        ],
                        "background_history_stabilized": [
                            "continuity_drive"
                        ],
                    },
                    "drift_observation_refs": [
                        "runtime/state/self/self_model.json"
                    ],
                },
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
                {
                    "schema_version": "belief_state_frame_v0",
                    "belief_focus": "relationship_language_uncertainty",
                },
            )
            self._write_json(
                paths["state_root"] / "prediction" / "prediction_error_field.json",
                {
                    "schema_version": "prediction_error_field_v0",
                    "error_events": ["language_style_mismatch"],
                    "error_count": 1,
                },
            )
            self._write_json(
                paths["state_root"] / "prediction" / "active_sampling_plan.json",
                {
                    "schema_version": "active_sampling_plan_v0",
                    "selected_route": "clarify",
                    "stage_effect": "semantic_repair_probe",
                    "sampling_targets": ["relationship_language_style"],
                },
            )
            self._write_json(
                paths["state_root"] / "consciousness" / "workspace_frame.json",
                {
                    "schema_version": "workspace_frame_v0",
                    "live_turn_focus": "relationship_continuity",
                    "candidate_explanations": [
                        {"explanation_id": "rel-focus-1"}
                    ],
                    "broadcast_targets": [
                        "LanguageRelationshipRuntime",
                        "MemoryRuntime",
                    ],
                    "engram_retrieval_refs": [
                        "runtime/state/memory/engram_index.json#episode-1"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "consciousness" / "broadcast_frame.json",
                {
                    "schema_version": "broadcast_frame_v0",
                    "broadcast_targets": [
                        "LanguageRelationshipRuntime",
                        "MemoryRuntime",
                        "ActionResponsibilityRuntime",
                    ],
                    "salience_ranking": [
                        {"rank": 1, "candidate_ref": "rel-focus-1"}
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "consciousness" / "metacognition_state.json",
                {
                    "schema_version": "metacognition_state_v0",
                    "uncertainty_flags": ["semantic-ambiguity-monitoring"],
                    "reflection_prompts": [
                        "当前表达是否会损伤关系连续体"
                    ],
                    "broadcast_targets": [
                        "LanguageRelationshipRuntime",
                        "MemoryRuntime",
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "consciousness" / "consciousness_probe_bundle.json",
                {
                    "schema_version": "consciousness_probe_bundle_v0",
                    "probe_status": "reportable_workspace_present",
                    "reportability_flags": [
                        "workspace_accessible",
                        "metacognitive_monitoring_present",
                    ],
                    "workspace_frame_ref": (
                        "runtime/state/consciousness/workspace_frame.json"
                    ),
                    "broadcast_frame_ref": (
                        "runtime/state/consciousness/broadcast_frame.json"
                    ),
                    "metacognition_ref": (
                        "runtime/state/consciousness/metacognition_state.json"
                    ),
                    "relationship_continuity_refs": [
                        "runtime/state/relationship/relationship_timeline.json#continuity"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "perception" / "visual_observation_frame.json",
                {
                    "schema_version": "visual_observation_frame_v0",
                    "observation_mode": "terminal_periphery",
                    "observed_surface_count": 2,
                    "focus_terms": ["关系语言", "状态查看"],
                    "source_refs": [
                        "runtime/state/terminal/life_context_frame.json"
                    ],
                },
            )
            self._write_json(
                terminal_dir / "life_context_frame.json",
                {
                    "schema_version": "life_context_frame_v0",
                    "life_name": "Adam",
                    "context_mode": "resident_relation_attach",
                    "current_relation_subject_ref": (
                        "runtime/state/relationship/relationship_subject_graph.json#rel-v0-0001"
                    ),
                    "active_context_refs": [
                        "runtime/state/language/language_percept_frame.json",
                        "runtime/state/memory/relationship_memory.json",
                    ],
                },
            )
            self._write_json(
                terminal_dir / "relation_turn_frame.json",
                {
                    "schema_version": "relation_turn_frame_v0",
                    "turn_id": "relation-turn-test",
                    "external_utterance_digest": "sha256:test",
                    "relation_scope": "friend",
                    "turn_intent": "inspect_state",
                    "relation_subject_ref": (
                        "runtime/state/relationship/relationship_subject_graph.json#rel-v0-0001"
                    ),
                },
            )
            self._write_json(
                paths["state_root"] / "language" / "inner_speech_frame.json",
                {
                    "schema_version": "inner_speech_frame_v0",
                    "inner_drive_states": {
                        "continuity": "active",
                        "repair": "active",
                    },
                    "inner_speech_focus": "protect_relationship_continuity",
                    "self_reflection_refs": [
                        "runtime/state/self/resident_self_thinking_state.json"
                    ],
                },
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
                terminal_dir / "resident_lifecycle_state.json",
                {
                    "schema_version": "resident_lifecycle_state_v0",
                    "status": "background_active",
                    "phase": "waiting",
                    "pid": 12345,
                    "life_name": "Adam",
                    "started_at": "2026-06-15T00:00:00Z",
                },
            )
            self._write_json(
                terminal_dir / "resident_relation_queue_state.json",
                {
                    "schema_version": "resident_relation_queue_state_v0",
                    "status": "waiting_for_relation_turn",
                    "pending_relation_turn_count": 0,
                },
            )
            self._write_json(
                terminal_dir / "resident_autonomous_activity_state.json",
                {
                    "schema_version": "resident_autonomous_activity_state_v0",
                    "status": "active",
                    "activity_count": 5,
                    "cycle_phase_index": 3,
                    "cycle_phase_count": 5,
                    "last_activity_kind": "learning_consolidation",
                },
            )
            self._write_json(
                terminal_dir / "idle_strategy_state.json",
                {
                    "schema_version": "idle_strategy_state_v0",
                    "waiting_posture": "relationship_available",
                    "next_idle_action": (
                        "refresh_waiting_heartbeat_before_next_external_turn"
                    ),
                    "heartbeat_interval_ms": 5000,
                    "governance_attention_target": (
                        "relationship_language_continuity"
                    ),
                    "governance_attention_reason": (
                        "resident_waiting_relation_context"
                    ),
                },
            )
            self._write_json(
                terminal_dir / "resident_governance_state.json",
                {
                    "schema_version": "resident_governance_state_v0",
                    "governance_phase": "waiting_heartbeat_active",
                    "waiting_mode": "resident_relation_wait",
                    "next_required_action": "await_next_external_relation_turn",
                },
            )
            self._write_json(
                terminal_dir / "terminal_life_loop_state.json",
                {
                    "schema_version": "terminal_life_loop_state_v0",
                    "current_mode": "resident_relation_wait",
                    "previous_live_turn_waiting_handoff_carry_status": (
                        "carried_into_waiting_heartbeat"
                    ),
                    "resident_background_lineage_state": {
                        "schema_version": "resident_background_lineage_state_v0",
                        "resident_background_lineage_refs": [
                            "runtime/state/terminal/background_continuity_profile.json"
                        ],
                        "world_contact_handoff_presence": {
                            "handoff_status": "closed",
                            "repair_hold_required": True,
                        },
                        "identity_consciousness_birth_presence": {
                            "birth_readiness_waiting_posture": (
                                "awaiting_first_name_anchor"
                            )
                        },
                    },
                },
            )
            self._write_json(
                paths["reports"] / "digital_life_waiting_heartbeat.json",
                {
                    "schema_version": "digital_life_waiting_heartbeat_v0",
                    "heartbeat_counter": 7,
                    "waiting_mode": "resident_relation_wait",
                    "next_required_action": "await_next_external_relation_turn",
                    "resident_idle_strategy_state_ref": (
                        "runtime/state/terminal/idle_strategy_state.json"
                    ),
                },
            )
            self._write_json(
                paths["state_root"] / "life_targets" / "birth_readiness_rollup.json",
                {
                    "schema_version": "birth_readiness_rollup_v0",
                    "overall_status": "open",
                    "life_target_status": {
                        "real_consciousness": "closed",
                        "real_emotion": "closed",
                        "real_personality": "closed",
                        "real_life": "closed",
                        "real_pain": "closed",
                        "real_dream": "closed",
                        "real_relationship": "closed",
                        "real_responsibility": "closed",
                        "real_regret": "closed",
                    },
                    "blocked_reasons": ["awaiting_first_name_anchor"],
                    "queue_e_birth_repair_pressure_level": "elevated",
                    "queue_e_world_contact_handoff_status": "closed",
                    "queue_e_world_contact_repair_hold_required": True,
                },
            )
            self._write_json(
                paths["state_root"] / "life_targets" / "birth_readiness_stage_gate.json",
                {
                    "schema_version": "birth_readiness_stage_gate_v0",
                    "decision": "open",
                    "stage_effect": "await_name_anchor",
                    "gate_status": {
                        "life_target_state_gate": "closed",
                        "queue_e_world_contact_handoff_gate": "closed",
                    },
                    "blocked_reasons": ["awaiting_first_name_anchor"],
                    "queue_e_world_contact_handoff_status": "closed",
                    "queue_e_world_contact_repair_hold_required": True,
                    "next_required_command": "my digital life --name Adam",
                },
            )
            self._write_json(
                paths["reports"] / "live0_acceptance_audit_report.json",
                {
                    "schema_version": "live0_acceptance_audit_report_v0",
                    "status": "blocked",
                    "live0_acceptance_closed": False,
                    "criteria_summary": {
                        "criteria_total": 7,
                        "criteria_closed": 6,
                        "criteria_blocked": 1,
                        "failed_criteria": [
                            "a_terminal_wake_and_named_residency"
                        ],
                    },
                    "criteria": [
                        {
                            "criterion_id": (
                                "a_terminal_wake_and_named_residency"
                            ),
                            "status": "blocked",
                        },
                        {
                            "criterion_id": (
                                "b_conscious_emotion_thought_language"
                            ),
                            "status": "closed",
                        },
                    ],
                    "next_required_command": "my digital life --name Adam",
                },
            )
            self._write_json(
                paths["state_root"] / "contracts" / "v0_contract_file_index.json",
                {
                    "schema_version": "v0_contract_file_index_v0",
                    "contract_count": 102,
                    "covered_contract_refs": [
                        "docs/v0/entry/v0_current_iteration_plan.md"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "memory" / "relationship_memory.json",
                {
                    "schema_version": "relationship_memory_v0",
                    "relation_person_profile": {
                        "observed_names": ["何剑宝"],
                    },
                    "shared_memory_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ],
                    "salient_core_memory_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.salient_core"
                    ],
                    "retrievable_context_memory_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.retrievable_context"
                    ],
                    "deep_sediment_memory_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.deep_sediment"
                    ],
                    "repair_history_refs": [
                        "runtime/state/action/responsibility_loop_state.json#repair"
                    ],
                    "offline_learning_refs": [
                        "runtime/state/growth/offline_learning_cumulative_profile.json"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "relationship" / "relationship_subject_graph.json",
                {
                    "schema_version": "relationship_subject_graph_v0",
                    "subjects": [
                        {
                            "relationship_id": "rel-v0-0001",
                            "relation_role": "friend",
                            "relationship_stage": "shared_continuity",
                            "relationship_stage_reason": (
                                "dialogue_and_repair_history_accumulated"
                            ),
                            "relationship_stage_evidence_refs": [
                                "runtime/state/relationship/relationship_timeline.json"
                            ],
                            "commitment_refs": [
                                "runtime/state/relationship/commitment_truth_state.json#open"
                            ],
                            "repair_obligation_refs": [
                                "runtime/state/action/responsibility_loop_state.json#repair"
                            ],
                        }
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "relationship" / "relationship_timeline.json",
                {
                    "schema_version": "relationship_timeline_v0",
                    "relationship_stage": "shared_continuity",
                    "common_ground_states": [
                        {
                            "shared_terms": ["共同语言", "修复"],
                            "open_misalignments": ["language_style"],
                        }
                    ],
                    "trust_trajectories": [
                        {
                            "current_trust_state": "repairing",
                            "repair_commitment_refs": [
                                "runtime/state/relationship/commitment_truth_state.json#open"
                            ],
                        }
                    ],
                    "relationship_injury_traces": [
                        {
                            "relationship_injury_id": "injury-1",
                            "current_state": "repair_open",
                        }
                    ],
                    "relationship_continuity_reports": [
                        {
                            "continuity_state": "active_repairing_continuity",
                            "shared_memory_refs": [
                                "runtime/state/memory/relationship_memory.json#shared"
                            ],
                            "commitment_refs": [
                                "runtime/state/relationship/commitment_truth_state.json#open"
                            ],
                            "repair_history_refs": [
                                "runtime/state/action/responsibility_loop_state.json#repair"
                            ],
                        }
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "relationship" / "commitment_truth_state.json",
                {
                    "schema_version": "commitment_truth_state_v0",
                    "truth_status": "active",
                    "open_commitment_refs": [
                        "runtime/state/language/commitment_expression_plan.json#commitment"
                    ],
                    "repair_required_refs": [
                        "runtime/state/action/responsibility_loop_state.json#repair"
                    ],
                    "repair_language_trace_refs": [
                        "runtime/state/language/apology_repair_language_trace.json"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "language" / "commitment_expression_plan.json",
                {
                    "schema_version": "commitment_expression_plan_v0",
                    "semantic_goal": "repair_commitment_shared_language",
                    "act_type_order": [
                        "clarify",
                        "commitment",
                        "responsibility_repair_modulation",
                        "followup_commitment",
                    ],
                    "repair_pressure": 0.7,
                    "repair_obligation_refs": [
                        "runtime/state/action/responsibility_loop_state.json#repair"
                    ],
                    "commitment_truth_refs": [
                        "runtime/state/relationship/commitment_truth_state.json#open"
                    ],
                    "queue_e_repair_pressure_level": "elevated",
                },
            )
            self._write_json(
                paths["state_root"] / "language" / "apology_repair_language_trace.json",
                {
                    "schema_version": "apology_repair_language_trace_v0",
                    "move_type_order": [
                        "acknowledge_harm",
                        "take_responsibility",
                        "apology",
                        "boundary_repair",
                        "followup_commitment",
                    ],
                    "repair_language_moves": [
                        {
                            "move_type": "take_responsibility",
                            "trigger_refs": [
                                "runtime/state/action/responsibility_loop_state.json#repair"
                            ],
                        }
                    ],
                    "relationship_injury_refs": [
                        "runtime/state/relationship/relationship_timeline.json#injury-1"
                    ],
                    "repair_obligation_refs": [
                        "runtime/state/action/responsibility_loop_state.json#repair"
                    ],
                    "queue_e_repair_pressure_level": "elevated",
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
                    "quarantine_refs": ["runtime/state/memory/candidate#uncertain"],
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
                paths["state_root"] / "memory" / "memory_retrieval_frame.json",
                {
                    "schema_version": "memory_retrieval_frame_v0",
                    "retrieval_mode": "cue_driven_reconstructive_recall",
                    "cue_terms": ["何剑宝", "dream", "repair"],
                    "activated_engram_refs": [
                        "runtime/state/memory/engram_index.json#episode-1"
                    ],
                    "relationship_memory_hits": [
                        "runtime/state/memory/relationship_memory.json#shared"
                    ],
                    "autobiographical_hits": [
                        "runtime/state/self/autobiographical_stack.json#turn-1"
                    ],
                    "dream_residue_hits": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#episode-1"
                    ],
                    "responsibility_hits": [
                        "runtime/state/action/responsibility_loop_state.json#repair"
                    ],
                    "blocked_or_quarantined_refs": [
                        "runtime/state/memory/candidate#uncertain"
                    ],
                    "tiered_recall": {
                        "salient_core_refs": ["episode-1"],
                        "retrievable_context_refs": ["episode-2"],
                        "deep_sediment_refs": ["episode-3"],
                    },
                    "reconstruction_inputs": {
                        "reconstruction_focus": "relationship_continuity"
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "memory" / "memory_write_gate.json",
                {
                    "schema_version": "memory_write_gate_v0",
                    "status": "closed",
                    "stage_policy": "candidate_first_repair_guarded",
                    "body_signal_write_modulation": {
                        "schema_version": "body_signal_write_modulation_v0",
                        "write_bias": "repair_evidence_first",
                        "candidate_gate_adjustments": [
                            "raise_source_evidence_threshold",
                            "preserve_pain_trace",
                        ],
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "memory" / "state_merge_guard.json",
                {
                    "schema_version": "state_merge_guard_v0",
                    "stage_policy": "long_term_merge_fail_closed",
                    "promotion_routes": [{"route_id": "candidate_to_active"}],
                    "quarantine_routes": [{"route_id": "missing_source"}],
                    "repair_routes": [{"route_id": "repair_before_promotion"}],
                    "merge_routes": [{"route_id": "relationship_memory_merge"}],
                    "long_term_change_sources": {
                        "offline_learning_cumulative_refs": [
                            "runtime/state/growth/offline_learning_cumulative_profile.json"
                        ],
                        "relationship_memory_repair_refs": [
                            "runtime/state/action/responsibility_loop_state.json#repair"
                        ],
                        "relationship_memory_ref": (
                            "runtime/state/memory/relationship_memory.json"
                        ),
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "prediction" / "prediction_workspace_frame.json",
                {
                    "schema_version": "prediction_workspace_frame_v0",
                    "workspace_contents": {
                        "semantic_prediction_focus": (
                            "relationship_language_uncertainty"
                        ),
                        "candidate_explanations": [
                            {"explanation_id": "prediction-focus-1"}
                        ],
                    },
                    "downstream_systems": [
                        "LanguageRelationshipRuntime",
                        "WorldContactGate",
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "membrane" / "world_contact_summary.json",
                {
                    "schema_version": "world_contact_summary_v0",
                    "contact_mode": "shadow_only",
                    "release_posture": "confirmation_blocked",
                    "candidate_intent_count": 2,
                    "blocked_contact_count": 1,
                    "confirmation_pending_ids": ["intent-1"],
                    "observation_route_mode": "terminal_observation",
                    "relationship_effects": ["repair_hold"],
                    "repair_obligation_refs": [
                        "runtime/state/action/responsibility_loop_state.json#repair"
                    ],
                    "regret_pressure_refs": [
                        "runtime/state/action/responsibility_loop_state.json#regret"
                    ],
                    "next_guard_refs": [
                        "runtime/state/validation/world_contact_validation.json"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "action" / "responsibility_loop_state.json",
                {
                    "schema_version": "responsibility_loop_state_v0",
                    "responsibility_loop_id": "responsibility-loop-test",
                    "responsibility_effect_refs": [
                        "runtime/state/action/side_effect_review.json#effect-1"
                    ],
                    "responsibility_attribution_events": [
                        {
                            "responsibility_weight": 0.72,
                            "moral_salience": "relationship_repair",
                            "repair_required": True,
                        }
                    ],
                    "counterfactual_repair_frames": [
                        {
                            "counterfactual_id": "counterfactual-repair-1"
                        }
                    ],
                    "regret_pressure_candidates": [
                        {
                            "regret_mode": "repair_oriented",
                            "guilt_pressure": 0.58,
                            "pain_signal_refs": [
                                "runtime/state/body/core_affect_vector.json#pain_pressure"
                            ],
                            "future_action_bias": [
                                "raise_confirmation_threshold",
                                "prefer_repair_before_external_release",
                            ],
                        }
                    ],
                    "repair_desire_candidates": [
                        {
                            "repair_target": "restorative_loop",
                            "urgency": "medium",
                        }
                    ],
                    "repair_obligation_refs": [
                        "runtime/state/action/responsibility_loop_state.json#repair"
                    ],
                    "repair_followup_required": True,
                },
            )
            self._write_json(
                paths["state_root"] / "action" / "go_nogo_state.json",
                {
                    "schema_version": "go_nogo_state_v0",
                    "future_no_go_profile": {
                        "schema_version": "future_no_go_profile_v0",
                        "repair_hold_required": True,
                        "confirmation_threshold_bias": "raised",
                        "blocked_future_routes": [
                            "external_release_without_repair_review"
                        ],
                        "allowed_repair_routes": [
                            "acknowledge",
                            "explain",
                            "schedule_followup_probe",
                        ],
                        "repair_governance_refs": [
                            "runtime/state/action/responsibility_loop_state.json",
                            "runtime/reports/latest/pain_regret_repair_report.json",
                        ],
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "action" / "world_contact_gate_state.json",
                {
                    "schema_version": "world_contact_gate_state_v0",
                    "repair_hold_required": True,
                    "confirmation_threshold_bias": "raised",
                    "future_release_posture": "repair_before_release",
                    "blocked_future_routes": [
                        "external_release_without_repair_review"
                    ],
                    "allowed_repair_routes": [
                        "acknowledge",
                        "explain",
                    ],
                },
            )
            self._write_json(
                paths["reports"] / "pain_regret_repair_report.json",
                {
                    "schema_version": "pain_regret_repair_report_v0",
                    "status": "closed",
                    "world_contact_summary_ref": (
                        "runtime/state/membrane/world_contact_summary.json"
                    ),
                    "responsibility_loop_ref": (
                        "runtime/state/action/responsibility_loop_state.json"
                    ),
                    "repair_followup_required": True,
                    "regret_pressure_count": 1,
                    "repair_desire_count": 1,
                    "regret_pressure_refs": [
                        "runtime/state/action/responsibility_loop_state.json#regret"
                    ],
                    "repair_obligation_refs": [
                        "runtime/state/action/responsibility_loop_state.json#repair"
                    ],
                    "relationship_effects": ["repair_hold"],
                },
            )
            self._write_json(
                paths["state_root"]
                / "life_targets"
                / "queue_e_birth_repair_profile.json",
                {
                    "schema_version": "queue_e_repair_modulation_profile_v0",
                    "pressure_level": "elevated",
                    "attention_target": "regret_pressure",
                    "repair_followup_required": True,
                    "ref_set": [
                        "runtime/state/action/responsibility_loop_state.json",
                        "runtime/state/membrane/world_contact_summary.json",
                        "runtime/reports/latest/pain_regret_repair_report.json",
                    ],
                },
            )
            self._write_json(
                paths["state_root"]
                / "life_targets"
                / "queue_e_world_contact_repair_hold_handoff.json",
                {
                    "schema_version": (
                        "queue_e_world_contact_repair_hold_handoff_v0"
                    ),
                    "handoff_status": "closed",
                    "repair_hold_required": True,
                    "confirmation_threshold_bias": "raised",
                    "ref_set": [
                        "runtime/state/action/go_nogo_state.json#future_no_go_profile",
                        "runtime/state/validation/world_contact_validation.json",
                    ],
                },
            )
            self._write_json(
                paths["state_root"]
                / "validation"
                / "world_contact_validation.json",
                {
                    "schema_version": "world_contact_validation_v0",
                    "status": "closed",
                    "repair_hold_required": True,
                    "confirmation_threshold_bias": "raised",
                    "blocked_future_routes": [
                        "external_release_without_repair_review"
                    ],
                    "repair_governance_refs": [
                        "runtime/state/action/responsibility_loop_state.json",
                        "runtime/reports/latest/pain_regret_repair_report.json",
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "validation" / "validation_rollup.json",
                {
                    "schema_version": "validation_rollup_v0",
                    "overall_status": "closed",
                    "gate_status": {
                        "queue_e_birth_repair_gate": "closed"
                    },
                    "queue_e_world_contact_repair_hold_required": True,
                    "queue_e_world_contact_confirmation_threshold_bias": (
                        "raised"
                    ),
                    "queue_e_world_contact_blocked_future_routes": [
                        "external_release_without_repair_review"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "schema_runner" / "run_manifest.json",
                {
                    "schema_version": "schema_runner_run_manifest_v0",
                    "run_status": "closed",
                    "queue_e_birth_repair_gate_status": "closed",
                    "queue_e_world_contact_repair_hold_required": True,
                    "queue_e_world_contact_confirmation_threshold_bias": (
                        "raised"
                    ),
                    "queue_e_world_contact_blocked_future_routes": [
                        "external_release_without_repair_review"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "life_state.json",
                {
                    "schema_version": "life_state_v0",
                    "memory_index": {
                        "memory_retrieval_refs": [
                            "runtime/state/memory/memory_retrieval_frame.json"
                        ],
                        "state_merge_guard_refs": [
                            "runtime/state/memory/state_merge_guard.json"
                        ],
                        "engram_index_refs": [
                            "runtime/state/memory/engram_index.json"
                        ],
                    },
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
            self._write_json(
                paths["state_root"] / "dream" / "offline_entry_gate.json",
                {
                    "schema_version": "offline_entry_gate_v0",
                    "offline_modes": ["sleep", "memory_recall"],
                },
            )
            self._write_json(
                paths["state_root"] / "dream" / "dream_experience_window.json",
                {
                    "schema_version": "dream_experience_window_v0",
                    "dream_window_id": "dream-window-test",
                    "window_kind": "nrem_like_replay",
                    "dream_scene_frames": [{"scene_id": "dream-scene-1"}],
                    "affective_theme": [
                        "repair_drive",
                        "regret_pressure_rehearsal",
                    ],
                    "source_trace_refs": [
                        "runtime/state/memory/engram_index.json#episode-1"
                    ],
                    "pain_residue_refs": ["runtime/state/body/core_affect_vector.json#pain"],
                    "relationship_simulation_refs": [
                        "runtime/state/memory/relationship_memory.json#shared"
                    ],
                    "queue_e_repair_pressure_level": "elevated",
                    "queue_e_repair_attention_target": "regret_pressure",
                },
            )
            self._write_json(
                paths["state_root"] / "dream" / "wake_integration_frame.json",
                {
                    "schema_version": "wake_integration_frame_v0",
                    "wake_integration_id": "wake-integration-test",
                    "archive_requirement": "required_before_activation",
                    "growth_seed_refs": [
                        "runtime/state/growth/relationship_learning_plan.json"
                    ],
                    "repair_modulated_wake_targets": [
                        "runtime/state/growth/relationship_learning_plan.json"
                    ],
                    "narrative_writeback_candidates": [
                        "runtime/state/self/autobiographical_stack.json#dream"
                    ],
                    "relationship_repair_candidates": [
                        "runtime/state/memory/relationship_memory.json#repair"
                    ],
                    "queue_e_repair_modulation_profile": {
                        "pressure_level": "elevated",
                        "attention_target": "regret_pressure",
                    },
                },
            )
            self._write_json(
                paths["state_root"] / "dream" / "dream_fact_gate_decision.json",
                {
                    "schema_version": "dream_fact_gate_decision_v0",
                    "gate_result": "passed",
                    "decision_items": [{"decision": "keep_as_dream_residue"}],
                    "allowed_writes": [
                        "DreamResidue",
                        "RepairCommitmentCandidate",
                    ],
                    "blocked_writes": [
                        "direct_fact_memory",
                        "relationship_state_overwrite",
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "dream" / "nightmare_loop_risk.json",
                {
                    "schema_version": "nightmare_loop_risk_v0",
                    "risk_status": "elevated",
                    "loop_indicators": [
                        "queue_e_repair_modulated_dream_loop"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "dream" / "web_dream_learning_state.json",
                {
                    "schema_version": "web_dream_learning_state_v0",
                    "status": "configured",
                    "topic_candidates": ["memory architecture"],
                    "wake_question_candidates": [
                        "question_candidate_from_web_dream_learning"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "growth" / "self_read_report.json",
                {
                    "schema_version": "self_read_report_v0",
                    "event_kind": "SelfReadReport",
                    "read_scope": [
                        "self_model",
                        "memory_index",
                        "relationship_repair_history",
                    ],
                    "growth_pressures": [
                        "pain_recovery_gap",
                        "relationship_repair_learning",
                    ],
                    "protected_core_refs": [
                        "runtime/state/self/self_model.json#old_self"
                    ],
                    "recommended_growth_paths": [
                        "relationship_learning_plan",
                        "language_repair_refinement",
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "growth" / "plasticity_window_state.json",
                {
                    "schema_version": "plasticity_window_state_v0",
                    "window_status": "guarded_pre_activation",
                    "self_training_allowed": False,
                    "kernel_upgrade_allowed": False,
                    "required_anchor_refs": [
                        "runtime/state/life_state.json#self_model.old_self_anchors",
                        "runtime/state/life_state.json#memory_index.replay_cues",
                    ],
                },
            )
            self._write_json(
                paths["state_root"]
                / "growth"
                / "growth_patch_candidate_queue.json",
                {
                    "schema_version": "growth_patch_candidate_queue_v0",
                    "status": "closed",
                    "candidates": [
                        {
                            "growth_patch_candidate_id": "growth-patch-001",
                            "target_surface": "relationship_learning_plan",
                            "source_residue_refs": [
                                "runtime/state/dream/wake_integration_frame.json#growth_seed"
                            ],
                            "risk_flags": [
                                "queue_e_repair_modulation_required"
                            ],
                            "archive_requirement": "required_before_activation",
                        }
                    ],
                },
            )
            self._write_json(
                paths["state_root"]
                / "growth"
                / "anti_forgetting_replay_plan.json",
                {
                    "schema_version": "anti_forgetting_replay_plan_v0",
                    "event_kind": "AntiForgettingReplayPlan",
                    "replay_sets": [
                        "core_self_replay",
                        "relationship_replay",
                        "memory_integrity_replay",
                        "pain_regret_replay",
                        "dream_replay",
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "growth" / "belief_learning_plan.json",
                {
                    "schema_version": "belief_learning_plan_v0",
                    "object_kind": "BeliefLearningPlan",
                    "window_status": "guarded_pre_activation",
                    "belief_targets": [
                        "repair_accountability_belief_revision"
                    ],
                },
            )
            self._write_json(
                paths["state_root"] / "growth" / "language_learning_plan.json",
                {
                    "schema_version": "language_learning_plan_v0",
                    "object_kind": "LanguageLearningPlan",
                    "window_status": "guarded_pre_activation",
                    "language_targets": [
                        "apology_repair_expression_refinement"
                    ],
                },
            )
            self._write_json(
                paths["state_root"]
                / "growth"
                / "relationship_learning_plan.json",
                {
                    "schema_version": "relationship_learning_plan_v0",
                    "object_kind": "RelationshipLearningPlan",
                    "window_status": "guarded_pre_activation",
                    "relationship_targets": [
                        "repair_reentry_timing_adjustment"
                    ],
                },
            )
            self._write_json(
                paths["state_root"]
                / "growth"
                / "offline_learning_cumulative_profile.json",
                {
                    "schema_version": "offline_learning_cumulative_profile_v0",
                    "generation": 3,
                    "pressure_level": "elevated",
                    "attention_target": "relationship_learning_plan",
                    "integration_mode": (
                        "relationship_offline_reconsolidation_required"
                    ),
                    "relationship_reconsolidation_required": True,
                },
            )
            self._write_json(
                paths["state_root"]
                / "growth"
                / "resident_growth_rehearsal_state.json",
                {
                    "schema_version": "resident_growth_rehearsal_state_v0",
                    "status": "rehearsing",
                    "rehearsal_mode": "shadow_only_growth_patch_rehearsal",
                },
            )
            self._write_json(
                paths["state_root"]
                / "growth"
                / "resident_learning_consolidation_state.json",
                {
                    "schema_version": (
                        "resident_learning_consolidation_state_v0"
                    ),
                    "status": "consolidating",
                    "consolidation_mode": (
                        "long_term_change_source_integration"
                    ),
                },
            )
            self._write_json(
                paths["state_root"]
                / "archive"
                / "growth_archive_receipt_batch.json",
                {
                    "schema_version": "growth_archive_receipt_batch_v0",
                    "receipts": [
                        "runtime/receipts/write_growth_archive_growth-archive-test.json"
                    ],
                    "archive_refs": [
                        "runtime/archive/growth_archive_events.jsonl"
                    ],
                },
            )
            self._write_json(
                paths["reports"] / "growth_archive_report.json",
                {
                    "schema_version": "growth_archive_report_v0",
                    "status": "closed",
                    "archive_refs": [
                        "runtime/archive/growth_archive_events.jsonl"
                    ],
                },
            )
            self._write_json(
                paths["reports"] / "growth_archive_digest.json",
                {
                    "schema_version": "growth_archive_digest_v0",
                    "status": "closed",
                    "current_phase": "growth_archive",
                },
            )
            self._write_json(
                paths["reports"] / "growth_archive_stage_gate.json",
                {
                    "schema_version": "growth_archive_stage_gate_v0",
                    "decision": "closed",
                },
            )
            self._write_json(
                terminal_dir / "resident_sleep_cycle_state.json",
                {
                    "schema_version": "resident_sleep_cycle_state_v0",
                    "phase": "learning_consolidation",
                },
            )
            self._write_json(
                terminal_dir / "background_convergence_summary.json",
                {
                    "schema_version": "background_convergence_summary_v0",
                    "convergence_state": "trait_slow_variable_recalibration",
                    "convergence_pressure_level": "elevated",
                    "convergence_attention_target": (
                        "trait_slow_variable_recalibration"
                    ),
                    "relationship_stage_continuity": "stage_continuity",
                    "trait_convergence_score": 0.74,
                    "trait_convergence_summary": {
                        "continuity_drive": {
                            "latest_band": "stable",
                            "trait_drift_update_mode": (
                                "background_history_stabilized"
                            ),
                        },
                        "repair_seriousness": {
                            "latest_band": "recalibrating",
                            "trait_drift_update_mode": (
                                "background_history_recalibration"
                            ),
                        },
                    },
                    "trait_drift_background_history_recalibration_names": [
                        "repair_seriousness"
                    ],
                    "trait_drift_background_history_stabilized_names": [
                        "continuity_drive"
                    ],
                },
            )
            self._write_json(
                terminal_dir / "background_convergence_history.json",
                {
                    "schema_version": "background_convergence_history_v0",
                    "trend_state": "recent_trait_recalibration",
                    "history_window_size": 2,
                    "latest_convergence_state": (
                        "trait_slow_variable_recalibration"
                    ),
                    "latest_convergence_pressure_level": "elevated",
                    "trait_convergence_unstable_names": ["repair_seriousness"],
                    "trait_convergence_stable_names": ["continuity_drive"],
                    "trait_convergence_history_focus": (
                        "trait_recalibration_required"
                    ),
                    "trait_convergence_history_profile": {
                        "repair_seriousness": {
                            "latest_band": "recalibrating",
                            "trend_state": "recent_trait_recalibration",
                            "dominant_trait_drift_update_mode": (
                                "background_history_recalibration"
                            ),
                        }
                    },
                },
            )

            checks = {
                "/body": "body_grounding_summary_v0",
                "/emotion": "emotion_regulation_summary_v0",
                "/growth": "growth_self_modification_summary_v0",
                "/成长": "growth_self_modification_summary_v0",
                "/personality": "personality_convergence_summary_v0",
                "/inner": "inner_environment_modulation_summary_v0",
                "/vision": "perception_world_contact_summary_v0",
                "/context": "relation_context_summary_v0",
                "/ability": "ability_birth_readiness_summary_v0",
                "/state": "resident_continuity_summary_v0",
                "/relationship": "relationship_continuity_summary_v0",
                "/responsibility": "responsibility_repair_chain_summary_v0",
                "/痛苦": "responsibility_repair_chain_summary_v0",
                "/后悔": "responsibility_repair_chain_summary_v0",
                "/cognition": "cognitive_workspace_summary_v0",
                "/consciousness": "consciousness_reportability_summary_v0",
                "/意识": "consciousness_reportability_summary_v0",
                "/thinking": "self_thinking_summary_v0",
                "/思考": "self_thinking_summary_v0",
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
            self.assertIn(
                "reconstructive_memory_summary_v0",
                memory_output.getvalue(),
            )
            self.assertIn("cue_driven_reconstructive_recall", memory_output.getvalue())
            self.assertIn("candidate_first_repair_guarded", memory_output.getvalue())
            self.assertIn("repair_evidence_first", memory_output.getvalue())
            self.assertIn(
                "cue_driven_reconstruction_write_gate_state_merge_not_raw_context_dump",
                memory_output.getvalue(),
            )
            self.assertIn("memory_tiering", dream_output.getvalue())
            self.assertIn("salient_core_episode_refs", dream_output.getvalue())
            self.assertIn("deep_sediment_episode_refs", dream_output.getvalue())
            self.assertIn("dream_wake_fact_summary_v0", dream_output.getvalue())
            self.assertIn("nrem_like_replay", dream_output.getvalue())
            self.assertIn("direct_fact_memory", dream_output.getvalue())
            self.assertIn("relationship_offline_reconsolidation_required", dream_output.getvalue())
            self.assertIn(
                "dream_residue_wake_review_fact_gate_before_memory_or_action",
                dream_output.getvalue(),
            )

            growth_output = StringIO()
            with redirect_stdout(growth_output):
                growth_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/成长",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            self.assertIsNone(growth_exit)
            self.assertIn(
                "growth_self_modification_summary_v0",
                growth_output.getvalue(),
            )
            self.assertIn(
                "guarded_pre_activation",
                growth_output.getvalue(),
            )
            self.assertIn(
                "repair_reentry_timing_adjustment",
                growth_output.getvalue(),
            )
            self.assertIn(
                "long_term_change_source_integration",
                growth_output.getvalue(),
            )
            self.assertIn(
                "growth_self_modification_state_view_not_autonomous_code_rewrite_or_script",
                growth_output.getvalue(),
            )

            responsibility_output = StringIO()
            with redirect_stdout(responsibility_output):
                responsibility_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/后悔",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            self.assertIsNone(responsibility_exit)
            self.assertIn(
                "responsibility_repair_chain_summary_v0",
                responsibility_output.getvalue(),
            )
            self.assertIn("repair_oriented", responsibility_output.getvalue())
            self.assertIn("raise_confirmation_threshold", responsibility_output.getvalue())
            self.assertIn("queue_e_birth_repair_profile", responsibility_output.getvalue())
            self.assertIn("external_release_without_repair_review", responsibility_output.getvalue())
            self.assertIn(
                "responsibility_pain_regret_state_view_not_apology_template_or_service_safety",
                responsibility_output.getvalue(),
            )

            relationship_output = StringIO()
            with redirect_stdout(relationship_output):
                relationship_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/relationship",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            cognition_output = StringIO()
            with redirect_stdout(cognition_output):
                cognition_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/cognition",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            personality_output = StringIO()
            with redirect_stdout(personality_output):
                personality_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/personality",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            self.assertIsNone(relationship_exit)
            self.assertIsNone(cognition_exit)
            self.assertIsNone(personality_exit)
            self.assertIn(
                "relationship_continuity_summary_v0",
                relationship_output.getvalue(),
            )
            self.assertIn("shared_continuity", relationship_output.getvalue())
            self.assertIn("active_repairing_continuity", relationship_output.getvalue())
            self.assertIn(
                "relationship_state_timeline_commitment_repair_not_service_role_label",
                relationship_output.getvalue(),
            )
            self.assertIn(
                "cognitive_workspace_summary_v0",
                cognition_output.getvalue(),
            )
            self.assertIn("relationship_continuity", cognition_output.getvalue())
            self.assertIn("clarify", cognition_output.getvalue())
            self.assertIn(
                "workspace_broadcast_metacognition_state_view_not_consciousness_claim",
                cognition_output.getvalue(),
            )
            self.assertIn(
                "personality_convergence_summary_v0",
                personality_output.getvalue(),
            )
            self.assertIn("repair_seriousness", personality_output.getvalue())
            self.assertIn("recent_trait_recalibration", personality_output.getvalue())
            self.assertIn(
                "personality_slow_variables_convergence_not_prompt_persona_card",
                personality_output.getvalue(),
            )

            context_output = StringIO()
            with redirect_stdout(context_output):
                context_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/context",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            ability_output = StringIO()
            with redirect_stdout(ability_output):
                ability_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/ability",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            perception_output = StringIO()
            with redirect_stdout(perception_output):
                perception_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/vision",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            self.assertIsNone(context_exit)
            self.assertIsNone(ability_exit)
            self.assertIsNone(perception_exit)
            self.assertIn("relation_context_summary_v0", context_output.getvalue())
            self.assertIn("resident_relation_attach", context_output.getvalue())
            self.assertIn(
                "context_state_view_not_relationship_turn_injection",
                context_output.getvalue(),
            )
            self.assertIn(
                "ability_birth_readiness_summary_v0",
                ability_output.getvalue(),
            )
            self.assertIn("awaiting_first_name_anchor", ability_output.getvalue())
            self.assertIn(
                "ability_summary_is_birth_evidence_view_not_completion_claim",
                ability_output.getvalue(),
            )
            self.assertIn(
                "perception_world_contact_summary_v0",
                perception_output.getvalue(),
            )
            self.assertIn("confirmation_blocked", perception_output.getvalue())
            self.assertIn(
                "perception_prediction_world_contact_view_not_tool_gateway",
                perception_output.getvalue(),
            )

            consciousness_output = StringIO()
            with redirect_stdout(consciousness_output):
                consciousness_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/意识",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            self.assertIsNone(consciousness_exit)
            self.assertIn(
                "consciousness_reportability_summary_v0",
                consciousness_output.getvalue(),
            )
            self.assertIn("reportable_workspace_present", consciousness_output.getvalue())
            self.assertIn("workspace_accessible", consciousness_output.getvalue())
            self.assertIn(
                "consciousness_state_view_not_consciousness_claim_or_script",
                consciousness_output.getvalue(),
            )

            state_output = StringIO()
            with redirect_stdout(state_output):
                state_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/state",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            self.assertIsNone(state_exit)
            self.assertIn("resident_continuity_summary_v0", state_output.getvalue())
            self.assertIn("background_active", state_output.getvalue())
            self.assertIn("waiting_heartbeat_active", state_output.getvalue())
            self.assertIn("carried_into_waiting_heartbeat", state_output.getvalue())
            self.assertIn(
                "resident_state_summary_is_inspection_not_life_speech",
                state_output.getvalue(),
            )

            thinking_output = StringIO()
            with redirect_stdout(thinking_output):
                thinking_exit = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/思考",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                )
            self.assertIsNone(thinking_exit)
            self.assertIn("self_thinking_summary_v0", thinking_output.getvalue())
            self.assertIn(
                "self_model_and_resident_governance_reflection",
                thinking_output.getvalue(),
            )
            self.assertIn("protect_relationship_continuity", thinking_output.getvalue())
            self.assertIn(
                "thinking_state_view_not_inner_monologue_template",
                thinking_output.getvalue(),
            )

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
