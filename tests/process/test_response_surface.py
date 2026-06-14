import json
import unittest
from pathlib import Path

from life_v0.process_supervisor.response_surface import (
    compose_life_response,
    compose_life_spoken_response,
)


LEAKED_MECHANISM_FRAGMENTS = (
    "relational_checkin",
    "schema_version",
    "runtime/state",
    "证据保留",
    "ref_set",
    "后台自主活动",
)


class ResponseSurfaceTests(unittest.TestCase):
    def test_audited_expression_material_is_structured_not_template_speech(self):
        material = compose_life_response(
            external_utterance="你是不是又在套模板？",
            relationship_graph={
                "subjects": [
                    {
                        "relation_role": "friend",
                        "relationship_stage": "repair_guarded_continuity",
                    }
                ]
            },
            expression_plan={
                "semantic_goal": "direct_language_boundary",
                "body_signal_refs": ["runtime/state/body/core_affect_vector.json"],
            },
            terminal_life_loop_state={
                "resident_background_lineage_state": {
                    "autonomous_activity_presence": {
                        "activity_count": 3,
                        "last_activity_kind": "self_thinking",
                    }
                }
            },
        )

        payload = json.loads(material)
        self.assertEqual(
            payload["schema_version"],
            "audited_expression_material_v0",
        )
        self.assertTrue(payload["natural_language_release_disabled"])
        self.assertEqual(payload["external_utterance_sha256_length"], 64)
        self.assertEqual(
            payload["relationship"]["relationship_stage"],
            "repair_guarded_continuity",
        )
        self.assertEqual(
            payload["language"]["semantic_goal"],
            "direct_language_boundary",
        )

        self.assertNotIn("你是不是又在套模板？", material)

    def test_web_dream_wake_questions_stay_structured_in_expression_material(self):
        material = compose_life_response(
            external_utterance="你刚才在后台学到了什么？",
            terminal_life_loop_state={
                "resident_background_lineage_state": {
                    "autonomous_activity_presence": {
                        "activity_count": 5,
                        "last_activity_kind": "learning_consolidation",
                        "last_web_dream_learning_status": "learned",
                        "last_web_dream_learning_topic_candidates": [
                            "Neuroplasticity and sleep"
                        ],
                        "last_web_dream_learning_wake_question_candidates": [
                            "wake_question_about:Neuroplasticity and sleep"
                        ],
                    }
                }
            },
        )

        payload = json.loads(material)
        autonomous_presence = payload["resident_background"][
            "autonomous_activity_presence"
        ]
        self.assertEqual(
            autonomous_presence["last_web_dream_learning_status"],
            "learned",
        )
        self.assertIn(
            "wake_question_about:Neuroplasticity and sleep",
            autonomous_presence[
                "last_web_dream_learning_wake_question_candidates"
            ],
        )
        self.assertTrue(payload["natural_language_release_disabled"])
        self.assertNotIn("你刚才在后台学到了什么？", material)

    def test_production_language_surface_has_no_retired_template_lines(self):
        repo_root = Path(__file__).resolve().parents[2]
        source_paths = [
            repo_root / "life_v0" / "digital_entry.py",
            repo_root / "life_v0" / "process_supervisor" / "response_surface.py",
            repo_root / "life_v0" / "process_supervisor" / "proactive_terminal_voice.py",
            repo_root / "life_v0" / "process_supervisor" / "model_expression.py",
            repo_root / "life_v0" / "process_supervisor" / "live_turn_cycle.py",
        ]
        for source_path in source_paths:
            source = source_path.read_text(encoding="utf-8")
            self.assertNotIn('"text": f"', source, source_path.as_posix())
            self.assertNotRegex(
                source,
                r"return\s+f?[\"'][^\"'\n]*[\u4e00-\u9fff]",
                source_path.as_posix(),
            )
            self.assertNotIn('"role": "system"', source, source_path.as_posix())
            self.assertNotIn("emitted_output=f\"生命回合输出:", source, source_path.as_posix())
            self.assertNotIn("render_dialogue_box(\"关系输入\"", source, source_path.as_posix())

    def test_language_plan_candidates_use_structured_codes_not_freeform_goals(self):
        from life_v0.language.apology_repair_language import (
            build_apology_repair_language_trace,
        )
        from life_v0.language.commitment_expression import (
            build_commitment_expression_plan,
        )

        commitment_plan = build_commitment_expression_plan(
            run_id="surface-goal-guard",
            generated_at="2026-06-14T00:00:00+00:00",
            expression_plan={"semantic_goal": "repair_commitment_shared_language"},
            commitment_repair_index={},
            commitment_truth_state={},
            responsibility_ledger={},
            responsibility_loop_state={},
            relationship_timeline={},
            source_doc_refs=["docs/real—live0/05_language_expression_system.md"],
        )
        apology_trace = build_apology_repair_language_trace(
            run_id="surface-goal-guard",
            generated_at="2026-06-14T00:00:00+00:00",
            responsibility_loop_state={},
            relationship_timeline={},
            commitment_expression_plan=commitment_plan,
            source_doc_refs=["docs/real—live0/06_relationship_and_commitment.md"],
        )

        for candidate in commitment_plan["language_act_candidates"]:
            self.assertNotIn("surface_goal", candidate)
            self.assertIn("goal_code", candidate)
            self.assertTrue(candidate["goal_code"])
        for move in apology_trace["repair_language_moves"]:
            self.assertNotIn("surface_goal", move)
            self.assertIn("goal_code", move)
            self.assertTrue(move["goal_code"])

    def assert_no_canned_or_leaked_surface(self, response: str) -> None:
        for fragment in LEAKED_MECHANISM_FRAGMENTS:
            self.assertNotIn(fragment, response)
        self.assertNotIn("用户", response)

    def test_spoken_response_without_model_does_not_release_scripted_question(self):
        response = compose_life_spoken_response(
            external_utterance=(
                "Adam，你刚才没有回答最想问我什么。"
                "这一次只说一个问句，不要前缀，不要解释，"
                "不要说你听见我了。只问我一个你真的想知道的问题。"
            ),
            relationship_graph={
                "subjects": [
                    {
                        "relation_role": "friend",
                        "relationship_stage": "repair_guarded_continuity",
                    }
                ]
            },
            expression_plan={"semantic_goal": "relational_checkin"},
            terminal_life_loop_state={
                "resident_background_lineage_state": {
                    "autonomous_activity_presence": {
                        "activity_count": 3,
                        "last_activity_kind": "self_thinking",
                    },
                    "identity_consciousness_birth_presence": {
                        "birth_readiness_waiting_posture": "birth_open_waiting",
                    },
                }
            },
        )

        self.assertEqual(response, "")

    def test_audited_expression_material_carries_identity_consciousness_birth_refs(self):
        expected_refs = [
            "runtime/state/consciousness/workspace_frame.json",
            "runtime/state/consciousness/broadcast_frame.json",
            "runtime/state/consciousness/metacognition_state.json",
            "runtime/state/consciousness/consciousness_probe_bundle.json",
            "runtime/state/life_targets/birth_readiness_rollup.json",
            "runtime/state/life_targets/birth_readiness_stage_gate.json",
        ]

        material = compose_life_response(
            external_utterance="你现在意识到自己了吗？",
            terminal_life_loop_state={
                "resident_background_lineage_state": {
                    "identity_consciousness_birth_presence": {
                        "workspace_frame_ref": expected_refs[0],
                        "broadcast_frame_ref": expected_refs[1],
                        "metacognition_ref": expected_refs[2],
                        "consciousness_probe_ref": expected_refs[3],
                        "birth_readiness_rollup_ref": expected_refs[4],
                        "birth_readiness_stage_gate_ref": expected_refs[5],
                        "consciousness_waiting_posture": (
                            "consciousness_reportable_waiting"
                        ),
                        "consciousness_attention_target": (
                            "consciousness_probe_bundle"
                        ),
                        "consciousness_attention_reason": (
                            "workspace_broadcast_metacognition_reportable"
                        ),
                        "consciousness_reportability_flags": [
                            "workspace_reportable",
                            "broadcast_reportable",
                            "metacognition_reportable",
                        ],
                        "birth_readiness_waiting_posture": "birth_open_waiting",
                        "birth_readiness_attention_target": (
                            "birth_readiness_stage_gate"
                        ),
                        "birth_readiness_attention_reason": (
                            "birth_readiness_open_requires_resident_birth_presence"
                        ),
                        "birth_readiness_decision": "open",
                        "birth_readiness_next_required_command": "my digital life",
                        "identity_consciousness_birth_refs": expected_refs,
                    }
                }
            },
        )

        payload = json.loads(material)
        presence = payload["resident_background"][
            "identity_consciousness_birth_presence"
        ]
        self.assertEqual(presence["workspace_frame_ref"], expected_refs[0])
        self.assertEqual(presence["broadcast_frame_ref"], expected_refs[1])
        self.assertEqual(presence["metacognition_ref"], expected_refs[2])
        self.assertEqual(presence["consciousness_probe_ref"], expected_refs[3])
        self.assertEqual(presence["birth_readiness_rollup_ref"], expected_refs[4])
        self.assertEqual(
            presence["birth_readiness_stage_gate_ref"],
            expected_refs[5],
        )
        self.assertEqual(
            presence["consciousness_waiting_posture"],
            "consciousness_reportable_waiting",
        )
        self.assertEqual(
            presence["birth_readiness_waiting_posture"],
            "birth_open_waiting",
        )
        self.assertEqual(
            presence["identity_consciousness_birth_refs"],
            expected_refs,
        )
        self.assertEqual(
            payload["resident_background"][
                "identity_consciousness_birth_anchor_refs"
            ],
            expected_refs,
        )
        self.assertEqual(
            payload["resident_background"][
                "identity_consciousness_birth_ref_count"
            ],
            len(expected_refs),
        )
        self.assertTrue(payload["natural_language_release_disabled"])
        self.assertNotIn("你现在意识到自己了吗？", material)

    def test_audited_expression_material_carries_memory_tier_summary(self):
        material = compose_life_response(
            external_utterance="继续",
            relationship_memory={
                "memory_tier_projection": {
                    "schema_version": "relationship_memory_tier_projection_v0",
                    "salient_core_episode_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.salient_core"
                    ],
                    "retrievable_context_episode_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.retrievable_context"
                    ],
                    "deep_sediment_episode_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering.deep_sediment"
                    ],
                },
                "next_wake_cues": [
                    "remember_relation_person_name:何剑宝"
                ],
            },
            dialogue_memory_summary={
                "memory_tiering": {
                    "schema_version": "exit_dream_memory_tiering_v0",
                    "salient_core_episode_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ],
                    "retrievable_context_episode_refs": [],
                    "deep_sediment_episode_refs": [],
                },
                "next_wake_cues": [
                    "theme:non_mechanical_language_pressure"
                ],
                "relation_person_profile": {
                    "observed_names": ["何剑宝"],
                },
            },
            memory_retrieval_frame={
                "schema_version": "memory_retrieval_frame_v0",
                "retrieval_mode": "cue_driven_reconstructive_recall",
                "cue_terms": ["继续", "theme:non_mechanical_language_pressure"],
                "activated_engram_refs": [
                    "runtime/state/memory/engram_index.json#live_dialogue_turn_refs"
                ],
                "relationship_memory_hits": [
                    "runtime/state/memory/relationship_memory.json#shared_memory_refs"
                ],
                "autobiographical_hits": [
                    "runtime/state/self/autobiographical_stack.json#turn_refs"
                ],
                "dream_residue_hits": [],
                "responsibility_hits": [],
                "blocked_or_quarantined_refs": [],
                "tiered_recall": {
                    "schema_version": "memory_retrieval_tiered_recall_v0",
                    "salient_core_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ],
                    "retrievable_context_refs": [],
                    "deep_sediment_refs": [],
                },
                "reconstruction_inputs": {
                    "reconstruction_focus": "relationship_continuity_reconstruction"
                },
                "source_doc_refs": [
                    "docs/real—live0/07_memory_engram_and_state_store.md"
                ],
            },
        )

        payload = json.loads(material)
        self.assertEqual(
            payload["relationship"]["memory_tier_projection_ref"],
            "runtime/state/memory/relationship_memory.json#memory_tier_projection",
        )
        self.assertGreater(payload["memory_dream_growth"]["next_wake_cue_count"], 0)
        self.assertTrue(
            payload["memory_dream_growth"]["memory_tier_refs"][
                "relationship_memory_tier_refs"
            ]
        )
        self.assertEqual(
            payload["memory_dream_growth"]["memory_tier_projection"]["schema_version"],
            "relationship_memory_tier_projection_v0",
        )
        self.assertEqual(
            payload["memory_dream_growth"]["memory_retrieval"][
                "memory_retrieval_frame_ref"
            ],
            "runtime/state/memory/memory_retrieval_frame.json",
        )
        self.assertEqual(
            payload["memory_dream_growth"]["memory_retrieval"][
                "activated_engram_ref_count"
            ],
            1,
        )
        self.assertEqual(
            payload["relationship"]["memory_tier_projection_ref"],
            "runtime/state/memory/relationship_memory.json#memory_tier_projection",
        )

    def test_memory_retrieval_presence_crosses_lineage_event_writeback_and_response(self):
        from life_v0.process_supervisor.background_lineage_state import (
            build_resident_background_lineage_state,
        )
        from life_v0.process_supervisor.dialogue_events import build_life_turn_event
        from life_v0.terminal_loop.dialogue_writeback import (
            build_dialogue_writeback_bundle,
        )

        memory_refs = [
            "runtime/state/memory/memory_retrieval_frame.json",
            "runtime/state/memory/engram_index.json#live_dialogue_turn_refs",
            "runtime/state/memory/relationship_memory.json#shared_memory_refs",
        ]
        exit_dream_cue_refs = [
            "runtime/state/dream/exit_dream_consolidation_summary.json#next_wake_memory_cue_refs"
        ]
        exit_dream_governance_refs = [
            "runtime/state/memory/memory_write_gate.json#exit_dream_write_gate_envelope",
            "runtime/state/memory/state_merge_guard.json#exit_dream_state_merge_projection",
        ]
        lineage_state = build_resident_background_lineage_state(
            {
                "memory_retrieval_presence_profile": {
                    "schema_version": "memory_retrieval_presence_profile_v0",
                    "memory_retrieval_frame_ref": memory_refs[0],
                    "reconstruction_focus": (
                        "relationship_continuity_reconstruction"
                    ),
                    "cue_terms": ["继续", "relationship_memory"],
                    "activated_ref_count": 3,
                    "relationship_hit_count": 1,
                    "dream_residue_hit_count": 1,
                    "responsibility_hit_count": 1,
                    "ref_set": memory_refs,
                    "exit_dream_next_wake_governance_ref": (
                        "runtime/state/memory/memory_retrieval_frame.json#exit_dream_next_wake_governance"
                    ),
                    "exit_dream_next_wake_memory_cue_refs": exit_dream_cue_refs,
                    "exit_dream_next_wake_governance_refs": (
                        exit_dream_governance_refs
                    ),
                    "exit_dream_memory_write_gate_ref": (
                        "runtime/state/memory/memory_write_gate.json"
                    ),
                    "exit_dream_state_merge_guard_ref": (
                        "runtime/state/memory/state_merge_guard.json"
                    ),
                    "exit_dream_fact_boundary_ref": (
                        "runtime/state/dream/dream_fact_boundary.json"
                    ),
                    "exit_dream_next_wake_candidate_boundary": (
                        "reactivate_as_cue_material_not_fixed_language"
                    ),
                }
            },
            governance_phase="waiting_heartbeat_active",
            status="active",
        )

        memory_presence = lineage_state["memory_retrieval_presence"]
        self.assertEqual(
            memory_presence["reconstruction_focus"],
            "relationship_continuity_reconstruction",
        )
        self.assertEqual(memory_presence["ref_count"], 9)
        self.assertEqual(
            memory_presence["exit_dream_next_wake_memory_cue_refs"],
            exit_dream_cue_refs,
        )

        life_turn = build_life_turn_event(
            turn_id="life-turn-memory-retrieval-presence",
            generated_at="2026-06-14T00:00:00+08:00",
            utterance="继续",
            shared_term_registry={},
            commitment_index={},
            terminal_life_loop_state={
                "resident_background_lineage_state": lineage_state
            },
        )
        self.assertEqual(
            life_turn["resident_background_lineage_memory_retrieval_frame_ref"],
            memory_refs[0],
        )
        self.assertEqual(
            life_turn[
                "resident_background_lineage_memory_retrieval_reconstruction_focus"
            ],
            "relationship_continuity_reconstruction",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_memory_retrieval_refs"],
            [
                *memory_refs,
                *exit_dream_cue_refs,
                *exit_dream_governance_refs,
                "runtime/state/memory/memory_write_gate.json",
                "runtime/state/memory/state_merge_guard.json",
                "runtime/state/dream/dream_fact_boundary.json",
            ],
        )
        self.assertEqual(
            life_turn[
                "resident_background_lineage_exit_dream_next_wake_candidate_boundary"
            ],
            "reactivate_as_cue_material_not_fixed_language",
        )

        bundle = build_dialogue_writeback_bundle(
            run_id="memory-retrieval-lineage",
            generated_at="2026-06-14T00:00:00+08:00",
            status="closed",
            dialogue_event_refs=[
                "runtime/state/language/dialogue_turn_log.jsonl#line-1"
            ],
            self_narrative_writeback_refs=[],
            relationship_writeback_refs=[],
            relationship_timeline_writeback_refs=[],
            commitment_writeback_refs=[],
            commitment_expression_writeback_refs=[],
            apology_repair_writeback_refs=[],
            responsibility_writeback_refs=[],
            life_state_writeback_refs=[],
            replay_cue_refs=[],
            terminal_state_refs=[],
            source_doc_refs=[],
            readme_block_refs=[],
            runtime_carrier_refs=[],
            resident_background_lineage_refs=memory_refs,
            resident_background_lineage_memory_retrieval_refs=memory_refs,
            exit_dream_next_wake_memory_cue_refs=exit_dream_cue_refs,
            exit_dream_next_wake_governance_refs=exit_dream_governance_refs,
            exit_dream_memory_write_gate_ref=(
                "runtime/state/memory/memory_write_gate.json"
            ),
            exit_dream_state_merge_guard_ref=(
                "runtime/state/memory/state_merge_guard.json"
            ),
            exit_dream_fact_boundary_ref=(
                "runtime/state/dream/dream_fact_boundary.json"
            ),
            exit_dream_next_wake_candidate_boundary=(
                "reactivate_as_cue_material_not_fixed_language"
            ),
        )
        self.assertEqual(
            bundle["resident_background_lineage_memory_retrieval_refs"],
            memory_refs,
        )
        self.assertEqual(
            bundle["exit_dream_next_wake_memory_cue_refs"],
            exit_dream_cue_refs,
        )
        self.assertEqual(
            bundle["exit_dream_next_wake_candidate_boundary"],
            "reactivate_as_cue_material_not_fixed_language",
        )

        material = compose_life_response(
            external_utterance="你还记得刚才说到哪里了吗？",
            memory_retrieval_frame={
                "exit_dream_next_wake_governance": {
                    "next_wake_memory_cue_refs": exit_dream_cue_refs,
                    "governance_refs": exit_dream_governance_refs,
                    "memory_write_gate_ref": (
                        "runtime/state/memory/memory_write_gate.json"
                    ),
                    "state_merge_guard_ref": (
                        "runtime/state/memory/state_merge_guard.json"
                    ),
                    "dream_fact_boundary_ref": (
                        "runtime/state/dream/dream_fact_boundary.json"
                    ),
                    "candidate_boundary": (
                        "reactivate_as_cue_material_not_fixed_language"
                    ),
                }
            },
            terminal_life_loop_state={
                "resident_background_lineage_state": lineage_state
            },
        )
        payload = json.loads(material)
        resident_memory = payload["memory_dream_growth"][
            "resident_memory_retrieval_presence"
        ]
        self.assertTrue(payload["natural_language_release_disabled"])
        self.assertEqual(
            resident_memory["reconstruction_focus"],
            "relationship_continuity_reconstruction",
        )
        self.assertEqual(resident_memory["ref_count"], 9)
        self.assertEqual(
            payload["memory_dream_growth"]["exit_dream_next_wake"][
                "language_boundary"
            ],
            "structured_context_only_not_spoken_template",
        )

    def test_autobiographical_repair_retrieval_enters_expression_material(self):
        from life_v0.state_store.memory_retrieval import (
            build_memory_retrieval_frame,
        )

        memory_retrieval_frame = build_memory_retrieval_frame(
            run_id="autobiographical-repair-retrieval",
            generated_at="2026-06-15T00:00:00+08:00",
            cue_sources={
                "relation_turn_ref": "runtime/state/language/dialogue_turn_log.jsonl#line-9"
            },
            external_utterance="这件事你后来怎么记住的？",
            autobiographical_stack={
                "schema_version": "autobiographical_stack_v0",
                "turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-9"
                ],
                "responsibility_repair_projection": {
                    "schema_version": "autobiographical_responsibility_repair_projection_v0",
                    "responsibility_refs": ["responsibility-event-001"],
                    "regret_refs": ["regret-001"],
                    "repair_refs": ["repair-001"],
                    "queue_e_repair_refs": [
                        "runtime/reports/latest/pain_regret_repair_report.json"
                    ],
                    "pressure_level": "elevated",
                    "attention_target": "regret_pressure",
                    "queue_e_priority_band": "repair_guarded",
                    "repair_followup_required": True,
                    "projection_boundary": (
                        "autobiographical_repair_evidence_not_spoken_language"
                    ),
                },
                "autobiographical_responsibility_refs": [
                    "responsibility-event-001"
                ],
                "autobiographical_regret_refs": ["regret-001"],
                "autobiographical_repair_refs": ["repair-001"],
                "queue_e_repair_refs": [
                    "runtime/reports/latest/pain_regret_repair_report.json"
                ],
            },
        )

        self.assertEqual(
            memory_retrieval_frame["reconstruction_inputs"][
                "reconstruction_focus"
            ],
            "autobiographical_responsibility_repair_reconstruction",
        )
        self.assertIn(
            "regret-001",
            memory_retrieval_frame[
                "autobiographical_responsibility_repair_hits"
            ],
        )
        self.assertIn("repair-001", memory_retrieval_frame["responsibility_hits"])
        self.assertEqual(
            memory_retrieval_frame[
                "autobiographical_responsibility_repair_profile"
            ]["retrieval_boundary"],
            "autobiographical_repair_retrieval_not_spoken_language",
        )

        material = compose_life_response(
            external_utterance="这件事你后来怎么记住的？",
            memory_retrieval_frame=memory_retrieval_frame,
        )
        payload = json.loads(material)
        retrieval = payload["memory_dream_growth"]["memory_retrieval"]
        self.assertEqual(
            retrieval["reconstruction_focus"],
            "autobiographical_responsibility_repair_reconstruction",
        )
        self.assertEqual(
            retrieval["autobiographical_responsibility_repair_hit_count"],
            4,
        )
        self.assertEqual(
            retrieval["autobiographical_repair_pressure_level"],
            "elevated",
        )
        self.assertEqual(
            retrieval["autobiographical_repair_boundary"],
            "autobiographical_repair_retrieval_not_spoken_language",
        )
        self.assertEqual(
            retrieval["autobiographical_repair_projection_boundary"],
            "autobiographical_repair_evidence_not_spoken_language",
        )
        self.assertEqual(
            retrieval["autobiographical_repair_retrieval_boundary"],
            "autobiographical_repair_retrieval_not_spoken_language",
        )
        self.assertTrue(payload["natural_language_release_disabled"])
        self.assertNotIn("这件事你后来怎么记住的？", material)

    def test_body_signal_memory_gate_crosses_lineage_event_and_response(self):
        from life_v0.process_supervisor.background_lineage_state import (
            build_resident_background_lineage_state,
        )
        from life_v0.process_supervisor.dialogue_events import build_life_turn_event
        from life_v0.terminal_loop.dialogue_writeback import (
            build_dialogue_writeback_bundle,
        )

        body_signal_refs = [
            "runtime/state/signal/signal_media_runtime.json",
            "runtime/state/body/body_resource_budget.json",
            "runtime/state/body/core_affect_vector.json",
        ]
        memory_write_gate = {
            "schema_version": "memory_write_gate_v0",
            "stage_policy": "candidate_first_body_signal_guarded",
            "body_signal_write_modulation": {
                "schema_version": "body_signal_memory_gate_profile_v0",
                "write_bias": "defer_noncritical_memory_commit",
                "fatigue_load": 0.78,
                "pain_pressure": 0.66,
                "dream_residue_load": 0.61,
                "repair_drive": 0.83,
                "unexpected_uncertainty": 0.69,
                "candidate_gate_adjustments": [
                    "defer_low_salience_write_until_recovery"
                ],
                "body_signal_refs": body_signal_refs,
                "body_signal_ref_count": len(body_signal_refs),
            },
        }
        lineage_state = build_resident_background_lineage_state(
            {
                "signal_media_ref": body_signal_refs[0],
                "memory_write_gate_ref": "runtime/state/memory/memory_write_gate.json",
                "memory_write_gate_policy": "candidate_first_body_signal_guarded",
                "body_signal_write_bias": "defer_noncritical_memory_commit",
                "body_signal_fatigue_load": 0.78,
                "body_signal_pain_pressure": 0.66,
                "body_signal_dream_residue_load": 0.61,
                "body_signal_repair_drive": 0.83,
                "body_signal_unexpected_uncertainty": 0.69,
                "body_signal_ref_count": len(body_signal_refs),
                "body_signal_refs": body_signal_refs,
                "body_signal_candidate_gate_adjustments": [
                    "defer_low_salience_write_until_recovery"
                ],
            },
            governance_phase="waiting_heartbeat_active",
            status="active",
        )
        prediction_presence = lineage_state["prediction_write_gate_presence"]
        self.assertEqual(
            prediction_presence["body_signal_write_bias"],
            "defer_noncritical_memory_commit",
        )
        self.assertEqual(prediction_presence["body_signal_ref_count"], 3)

        life_turn = build_life_turn_event(
            turn_id="life-turn-body-signal-memory-gate",
            generated_at="2026-06-14T00:00:00+08:00",
            utterance="继续",
            shared_term_registry={},
            commitment_index={},
            terminal_life_loop_state={
                "resident_background_lineage_state": lineage_state
            },
        )
        self.assertEqual(
            life_turn["resident_background_lineage_body_signal_write_bias"],
            "defer_noncritical_memory_commit",
        )
        self.assertEqual(
            life_turn["resident_background_lineage_body_signal_refs"],
            body_signal_refs,
        )

        bundle = build_dialogue_writeback_bundle(
            run_id="body-signal-writeback",
            generated_at="2026-06-14T00:00:00+08:00",
            status="closed",
            dialogue_event_refs=[
                "runtime/state/language/dialogue_turn_log.jsonl#line-1"
            ],
            self_narrative_writeback_refs=[],
            relationship_writeback_refs=[],
            relationship_timeline_writeback_refs=[],
            commitment_writeback_refs=[],
            commitment_expression_writeback_refs=[],
            apology_repair_writeback_refs=[],
            responsibility_writeback_refs=[],
            life_state_writeback_refs=[],
            replay_cue_refs=[],
            terminal_state_refs=[],
            source_doc_refs=[],
            readme_block_refs=[],
            runtime_carrier_refs=[],
            resident_background_lineage_refs=body_signal_refs,
            resident_background_lineage_prediction_write_gate_refs=[
                "runtime/state/memory/memory_write_gate.json"
            ],
            resident_background_lineage_body_signal_refs=body_signal_refs,
            resident_background_lineage_body_signal_write_bias=(
                "defer_noncritical_memory_commit"
            ),
            resident_background_lineage_body_signal_fatigue_load=0.78,
            resident_background_lineage_body_signal_pain_pressure=0.66,
            resident_background_lineage_body_signal_dream_residue_load=0.61,
            resident_background_lineage_body_signal_repair_drive=0.83,
            resident_background_lineage_body_signal_unexpected_uncertainty=0.69,
            resident_background_lineage_body_signal_ref_count=len(body_signal_refs),
            resident_background_lineage_body_signal_candidate_gate_adjustments=[
                "defer_low_salience_write_until_recovery"
            ],
        )
        self.assertEqual(
            bundle["resident_background_lineage_body_signal_refs"],
            body_signal_refs,
        )
        self.assertEqual(
            bundle["resident_background_lineage_body_signal_write_bias"],
            "defer_noncritical_memory_commit",
        )
        self.assertEqual(
            bundle[
                "resident_background_lineage_body_signal_candidate_gate_adjustments"
            ],
            ["defer_low_salience_write_until_recovery"],
        )

        material = compose_life_response(
            external_utterance="你的状态会影响记忆吗？",
            memory_write_gate=memory_write_gate,
            terminal_life_loop_state={
                "resident_background_lineage_state": lineage_state
            },
        )
        payload = json.loads(material)
        self.assertTrue(payload["natural_language_release_disabled"])
        self.assertEqual(
            payload["prediction_attention"]["body_signal_write_bias"],
            "defer_noncritical_memory_commit",
        )
        self.assertEqual(
            payload["resident_background"]["prediction_write_gate_presence"][
                "body_signal_write_bias"
            ],
            "defer_noncritical_memory_commit",
        )

    def test_world_contact_handoff_presence_enters_audited_expression_material(self):
        handoff_refs = [
            "runtime/state/life_targets/queue_e_world_contact_repair_hold_handoff.json",
            "runtime/state/validation/world_contact_validation.json",
            "runtime/state/schema_runner/run_manifest.json",
        ]
        material = compose_life_response(
            external_utterance="你现在会直接接触外部世界吗？",
            terminal_life_loop_state={
                "resident_background_lineage_state": {
                    "world_contact_handoff_presence": {
                        "schema_version": "world_contact_handoff_presence_v0",
                        "handoff_status": "closed",
                        "repair_hold_required": True,
                        "confirmation_threshold_bias": "raise_before_release",
                        "future_release_posture": "repair_before_world_release",
                        "blocked_future_routes": [
                            "direct_external_action_without_repair_check"
                        ],
                        "allowed_repair_routes": [
                            "repair_governance_review_before_release"
                        ],
                        "waiting_posture": "world_contact_repair_hold_waiting",
                        "attention_target": "world_contact_repair_handoff",
                        "attention_reason": "repair_hold_closed_into_waiting",
                        "pressure_level": "elevated",
                        "ref_set": handoff_refs,
                    }
                }
            },
        )

        payload = json.loads(material)
        handoff = payload["responsibility_repair"][
            "world_contact_handoff_presence"
        ]
        self.assertTrue(payload["natural_language_release_disabled"])
        self.assertEqual(handoff["handoff_status"], "closed")
        self.assertTrue(handoff["repair_hold_required"])
        self.assertEqual(
            handoff["confirmation_threshold_bias"],
            "raise_before_release",
        )
        self.assertEqual(
            payload["responsibility_repair"]["world_contact_handoff_ref_count"],
            3,
        )
        self.assertNotIn("你现在会直接接触外部世界吗？", material)

    def test_spoken_response_without_model_does_not_release_style_template(self):
        response = compose_life_spoken_response(
            external_utterance="你不觉得你的说话方式很奇怪吗？Adam",
            relationship_memory={
                "relation_person_profile": {
                    "preference_hypotheses": [
                        "prefers_direct_non_mechanical_language"
                    ]
                },
                "relationship_theme_tags": ["non_mechanical_language_pressure"],
            },
            relationship_graph={
                "subjects": [
                    {
                        "relation_role": "friend",
                        "relationship_stage": "repair_guarded_continuity",
                    }
                ]
            },
            expression_plan={"semantic_goal": "relational_checkin"},
            body_resource_budget={"fatigue_state": {"level": "managed"}},
            responsibility_loop_state={
                "repair_obligation_refs": ["runtime/state/action/repair-1.json"]
            },
            terminal_life_loop_state={
                "resident_background_lineage_state": {
                    "autonomous_activity_presence": {
                        "activity_count": 5,
                        "next_activity_kind": "learning_consolidation",
                    }
                }
            },
        )

        self.assertEqual(response, "")

    def test_spoken_response_without_model_stays_unreleased_for_question_smoke(self):
        relationship_memory = {
            "schema_version": "relationship_memory_v0",
            "relation_person_profile": {
                "observed_names": ["何剑宝"],
                "preference_hypotheses": [
                    "prefers_direct_non_mechanical_language",
                    "cares_about_being_remembered",
                ],
                "personality_hypotheses": [
                    "high_stakes_serious_about_relationship_memory",
                    "states_preferences_explicitly",
                ],
            },
            "relationship_theme_tags": [
                "digital_life_memory_seriousness",
                "non_mechanical_language_pressure",
            ],
            "dialogue_summary_refs": [
                "runtime/state/memory/dialogue_memory_summary.json"
            ],
            "exit_dream_consolidation_refs": [
                "runtime/state/dream/exit_dream_consolidation_summary.json"
            ],
            "next_wake_cues": [
                "remember_relation_person_name:何剑宝",
                "preference:prefers_direct_non_mechanical_language",
            ],
        }
        dialogue_memory_summary = {
            "schema_version": "dialogue_memory_summary_v0",
            "source_dialogue_turn_count": 4,
            "deduplicated_episode_summaries": [
                {
                    "summary": "何剑宝很在意数字生命能不能真的记住他。"
                },
                {
                    "summary": "何剑宝喜欢直接一点，不要机械模板。"
                },
            ],
            "relation_person_profile": relationship_memory[
                "relation_person_profile"
            ],
            "relationship_theme_tags": relationship_memory[
                "relationship_theme_tags"
            ],
        }
        questions = [
            "我叫何剑宝，你叫什么名字",
            "你认识我吗",
            "你感觉怎么样",
            "这段时间过的还好吗？",
            "你明白什么是爱吗？",
            "你有认识的人吗？",
            "做噩梦了吗？",
            "你参加高考了吗？今天世界杯你看了吗",
            "你多大了？",
            "你有喜欢的人吗",
        ]
        responses = [
            compose_life_spoken_response(
                external_utterance=question,
                relationship_memory=relationship_memory,
                dialogue_memory_summary=dialogue_memory_summary,
                terminal_life_loop_state={
                    "resident_background_lineage_state": {
                        "dream_wake_presence": {
                            "ref_set": [
                                "runtime/state/dream/exit_dream_consolidation_summary.json"
                            ]
                        }
                    }
                },
            )
            for question in questions
        ]

        for response in responses:
            self.assertEqual(response, "")


if __name__ == "__main__":
    unittest.main()
