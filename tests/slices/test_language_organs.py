import tempfile
import unittest
from pathlib import Path


class LanguageOrgansTests(unittest.TestCase):
    def test_shared_terms_commitment_narrative_and_dialogue_helpers(self):
        from life_v0.language.commitment_repair import build_commitment_repair_language_index
        from life_v0.language.dialogue_log import build_dialogue_turn_log_entries, collect_dialogue_turn_refs
        from life_v0.language.narrative_trace import build_self_narrative_language_trace
        from life_v0.language.shared_terms import build_shared_term_registry

        shared_terms = build_shared_term_registry(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=["docs/09_language_symbolic_top_layer.md"],
        )
        commitment_index = build_commitment_repair_language_index(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            responsibility_loop_state={
                "repair_obligation_refs": [
                    "runtime/state/membrane/responsibility_repair_boundary.json#repair_obligation",
                    "repair-desire-001",
                ],
                "regret_pressure_candidates": [
                    {"regret_pressure_id": "regret-pressure-001"},
                    {"regret_pressure_id": "regret-pressure-002"},
                ],
                "responsibility_attribution_events": [
                    {"responsibility_event_id": "responsibility-001"},
                ],
            },
            source_doc_refs=["docs/94_pain_regret_and_repair_signal_schema.md"],
        )
        narrative_trace = build_self_narrative_language_trace(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=["docs/85_language_system_life_expression_core.md"],
        )
        dialogue_entries = build_dialogue_turn_log_entries(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=["docs/90_language_event_examples_and_timeline_bundle.md"],
        )

        self.assertEqual(shared_terms["schema_version"], "shared_term_registry_v0")
        self.assertEqual(shared_terms["shared_terms"][0]["surface"], "共同语言")
        self.assertEqual(commitment_index["schema_version"], "commitment_repair_language_index_v0")
        self.assertTrue(commitment_index["commitment_refs"])
        self.assertEqual(narrative_trace["schema_version"], "self_narrative_language_trace_v0")
        self.assertTrue(narrative_trace["narrative_turn_refs"])
        self.assertEqual(dialogue_entries[0]["schema_version"], "dialogue_turn_event_v0")
        self.assertEqual(dialogue_entries[0]["turn_id"], "dialogue-turn-v0-0001")

        with tempfile.TemporaryDirectory() as tmp:
            dialogue_log = Path(tmp) / "dialogue_turn_log.jsonl"
            dialogue_log.write_text('{"turn_id":"t1"}\n{"turn_id":"t2"}\n', encoding="utf-8")
            blocked_reasons: list[str] = []
            refs = collect_dialogue_turn_refs(dialogue_log, blocked_reasons)

        self.assertEqual(blocked_reasons, [])
        self.assertEqual(
            refs,
            [
                "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                "runtime/state/language/dialogue_turn_log.jsonl#line-2",
            ],
        )

    def test_inner_speech_expression_monitor_and_relationship_graph_organs(self):
        from life_v0.language.expression_monitor import build_expression_monitor_state, build_expression_plan
        from life_v0.language.inner_speech import build_inner_speech_frame
        from life_v0.language.relationship_graph import build_relationship_subject_graph

        life_state = {
            "self_model": {
                "old_self_anchors": [
                    "runtime/state/self/self_model.json#old-self-anchor-001",
                ]
            }
        }
        source_doc_refs = [
            "docs/86_language_neuroscience_pragmatics_and_inner_speech.md",
            "docs/96_real_relationship_longitudinal_timeline.md",
        ]

        inner_speech = build_inner_speech_frame(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            life_state=life_state,
            source_doc_refs=source_doc_refs,
        )
        expression_monitor = build_expression_monitor_state(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )
        relationship_graph = build_relationship_subject_graph(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )

        self.assertEqual(inner_speech["schema_version"], "inner_speech_frame_v0")
        self.assertEqual(inner_speech["old_self_anchor_refs"], ["runtime/state/self/self_model.json#old-self-anchor-001"])
        self.assertIn("inner_language_bus", inner_speech["bus_channel_refs"])

        self.assertEqual(expression_monitor["schema_version"], "expression_monitor_state_v0")
        self.assertIn("relationship_consequence", expression_monitor["monitor_dimensions"])
        self.assertIn("service_object", expression_monitor["blocked_language"])

        self.assertEqual(relationship_graph["schema_version"], "relationship_subject_graph_v0")
        self.assertEqual(relationship_graph["subjects"][0]["relation_role"], "friend")
        self.assertEqual(
            relationship_graph["graph_edges"][0]["edge_type"],
            "shared_language",
        )

        expression_plan = build_expression_plan(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            inner_speech={
                "semantic_map_ref": "runtime/state/language/semantic_map_frame.json",
            },
            semantic_map={
                "semantic_focus": "repair_commitment_shared_language",
            },
            language_percept={
                "ambiguity_flags": ["待确认关系语义细节"],
                "cross_scope_risk_terms": ["service_object"],
                "repair_trigger_candidates": ["repair-trigger-001"],
                "commitment_trigger_candidates": ["commitment-trigger-001"],
                "shared_term_hits": ["共同语言"],
            },
            commitment_repair_index={
                "commitment_refs": ["commitment-ref-001", "commitment-ref-002"],
                "repair_obligation_refs": [
                    "runtime/state/membrane/responsibility_repair_boundary.json#repair_obligation",
                    "repair-desire-001",
                ],
                "regret_trace_refs": ["regret-pressure-001", "regret-pressure-002"],
                "responsibility_trace_refs": ["responsibility-001"],
            },
            replay_cue_bundle={
                "anti_forgetting_targets": [
                    "runtime/state/replay/replay-cue-001",
                    "runtime/state/replay/replay-cue-002",
                ]
            },
            offline_consolidation_frame={
                "dream_window_refs": [
                    "runtime/state/dream/dream-window-001",
                    "runtime/state/dream/dream-window-002",
                ]
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
            core_affect_vector={
                "valence": -0.21,
                "arousal": 0.73,
                "responsibility_weight": 0.44,
                "repair_drive": "active",
            },
            source_doc_refs=source_doc_refs,
        )

        self.assertEqual(expression_plan["schema_version"], "expression_plan_v0")
        self.assertIn("repair_pressure_present", expression_plan["expression_risk_flags"])
        self.assertIn("commitment_trace_present", expression_plan["expression_risk_flags"])
        self.assertIn("responsibility_repair_language_pressure_present", expression_plan["expression_risk_flags"])
        self.assertIn("offline_replay_pressure_present", expression_plan["expression_risk_flags"])
        self.assertIn("dream_integration_pressure_present", expression_plan["expression_risk_flags"])
        self.assertIn("growth_candidate_pressure_present", expression_plan["expression_risk_flags"])
        self.assertEqual(expression_plan["responsibility_pressure"], 3)
        self.assertEqual(expression_plan["repair_pressure"], 3)
        self.assertEqual(expression_plan["replay_cue_pressure"], 2)
        self.assertEqual(expression_plan["dream_integration_pressure"], 2)
        self.assertEqual(expression_plan["growth_candidate_pressure"], 2)
        self.assertEqual(expression_plan["fatigue_pressure"], "managed_low_noise")
        self.assertEqual(expression_plan["body_repair_drive"], "active")
        self.assertEqual(expression_plan["affect_arousal"], 0.73)
        self.assertEqual(expression_plan["affect_valence"], -0.21)
        self.assertEqual(expression_plan["affect_responsibility_weight"], 0.44)
        self.assertEqual(expression_plan["expression_tempo_mode"], "guarded_deliberate")
        self.assertEqual(expression_plan["release_caution_level"], "elevated")
        self.assertEqual(
            expression_plan["body_signal_refs"],
            [
                "runtime/state/body/body_resource_budget.json",
                "runtime/state/body/core_affect_vector.json",
            ],
        )
        self.assertIn("fatigue_pressure_present", expression_plan["body_modulation_flags"])
        self.assertIn("repair_drive_present", expression_plan["body_modulation_flags"])
        self.assertIn("affect_arousal_present", expression_plan["body_modulation_flags"])
        self.assertIn("body_signal_refs_present", expression_plan["body_modulation_flags"])
        self.assertEqual(
            expression_plan["offline_influence_refs"],
            [
                "runtime/state/replay/replay_cue_bundle.json",
                "runtime/state/dream/offline_consolidation_frame.json",
                "runtime/state/growth/growth_patch_candidate_queue.json",
            ],
        )

    def test_language_state_dream_gate_action_shadow_and_relation_scope_organs(self):
        from life_v0.language.action_shadow import build_language_action_bridge_shadow
        from life_v0.language.dream_gate import build_dream_report_language_gate
        from life_v0.language.language_state import build_language_relationship_state
        from life_v0.language.relation_scope import build_relation_scope_language_index

        source_doc_refs = [
            "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
            "docs/90_language_event_examples_and_timeline_bundle.md",
        ]
        life_state = {
            "language_state": {
                "dialogue_turn_log_refs": ["runtime/state/language/dialogue_turn_log.jsonl#line-1"],
            }
        }

        language_state = build_language_relationship_state(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            life_state=life_state,
            source_doc_refs=source_doc_refs,
        )
        dream_gate = build_dream_report_language_gate(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            dream_fact_boundary={"schema_version": "dream_fact_boundary_v0"},
            source_doc_refs=source_doc_refs,
        )
        action_shadow = build_language_action_bridge_shadow(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            shadow_action_gate={"schema_version": "shadow_action_gate_v0"},
            source_doc_refs=source_doc_refs,
        )
        relation_scope = build_relation_scope_language_index(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )

        self.assertEqual(language_state["schema_version"], "language_relationship_state_v0")
        self.assertEqual(language_state["status"], "closed")
        self.assertIn("friend", language_state["relationship_kinds"])
        self.assertEqual(
            language_state["existing_language_state"]["dialogue_turn_log_refs"],
            ["runtime/state/language/dialogue_turn_log.jsonl#line-1"],
        )

        self.assertEqual(dream_gate["schema_version"], "dream_report_language_gate_v0")
        self.assertEqual(dream_gate["dream_fact_gate"], "closed")

        self.assertEqual(action_shadow["schema_version"], "language_action_bridge_shadow_v0")
        self.assertTrue(action_shadow["shadow_only"])
        self.assertEqual(action_shadow["shadow_gate_status"], "closed")

        self.assertEqual(relation_scope["schema_version"], "relation_scope_language_index_v0")
        self.assertEqual(relation_scope["status"], "closed")
        self.assertEqual(relation_scope["relation_scopes"][0]["relation_role"], "friend")
        self.assertIn("service_object", relation_scope["relation_scopes"][0]["blocked_cross_scope_terms"])

    def test_language_percept_and_semantic_map_organs(self):
        from life_v0.language.commitment_repair import build_commitment_repair_language_index
        from life_v0.language.language_state import build_language_relationship_state
        from life_v0.language.narrative_trace import build_self_narrative_language_trace
        from life_v0.language.percept import build_language_percept_frame
        from life_v0.language.relation_scope import build_relation_scope_language_index
        from life_v0.language.semantic_map import build_semantic_map_frame
        from life_v0.language.shared_terms import build_shared_term_registry

        source_doc_refs = [
            "docs/86_language_neuroscience_pragmatics_and_inner_speech.md",
            "docs/90_language_event_examples_and_timeline_bundle.md",
        ]
        life_state = {
            "language_state": {
                "dialogue_turn_log_refs": ["runtime/state/language/dialogue_turn_log.jsonl#line-1"],
            }
        }
        relation_scope = build_relation_scope_language_index(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )
        shared_terms = build_shared_term_registry(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )
        language_state = build_language_relationship_state(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            life_state=life_state,
            source_doc_refs=source_doc_refs,
        )
        commitment_index = build_commitment_repair_language_index(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )
        narrative_trace = build_self_narrative_language_trace(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )

        incoming_turn = {
            "incoming_surface": "我们之前说好的共同语言和修复，还记得吗？",
            "speaker_role": "friend",
        }
        percept = build_language_percept_frame(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            incoming_turn=incoming_turn,
            relation_scope_index=relation_scope,
            shared_term_registry=shared_terms,
            source_doc_refs=source_doc_refs,
        )
        semantic_map = build_semantic_map_frame(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            language_percept=percept,
            language_state=language_state,
            shared_term_registry=shared_terms,
            commitment_repair_index=commitment_index,
            self_narrative_trace=narrative_trace,
            source_doc_refs=source_doc_refs,
        )

        self.assertEqual(percept["schema_version"], "language_percept_frame_v0")
        self.assertEqual(percept["incoming_surface"], incoming_turn["incoming_surface"])
        self.assertEqual(percept["speaker_role"], "friend")
        self.assertEqual(percept["relation_scope_ref"], "runtime/state/language/relation_scope_language_index.json#relation-scope-v0-0001")
        self.assertTrue(percept["shared_term_hits"])
        self.assertTrue(percept["commitment_trigger_candidates"])
        self.assertTrue(percept["repair_trigger_candidates"])
        self.assertIn("共同语言", percept["shared_term_hits"])
        self.assertIn("待确认关系语义细节", percept["ambiguity_flags"])

        self.assertEqual(semantic_map["schema_version"], "semantic_map_frame_v0")
        self.assertEqual(semantic_map["semantic_focus"], "repair_commitment_shared_language")
        self.assertTrue(semantic_map["shared_meaning_bindings"])
        self.assertTrue(semantic_map["commitment_trace_refs"])
        self.assertTrue(semantic_map["repair_trace_refs"])
        self.assertTrue(semantic_map["narrative_bindings"])
        self.assertTrue(semantic_map["ambiguity_queue"])
        self.assertEqual(
            semantic_map["prediction_hooks"]["semantic_prediction_focus"],
            "repair_commitment_shared_language",
        )


if __name__ == "__main__":
    unittest.main()
