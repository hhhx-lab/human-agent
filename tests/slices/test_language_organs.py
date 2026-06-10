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
        language_percept = {
            "shared_term_hits": ["共同语言"],
            "repair_trigger_candidates": ["repair-trigger-001"],
        }
        semantic_map = {
            "semantic_focus": "repair_commitment_shared_language",
            "ambiguity_queue": ["待确认关系语义细节"],
        }
        belief_state = {
            "state_scope": "language_relationship_continuity",
            "revision_policy": "repair_before_action",
            "source_evidence_refs": ["runtime/state/language/semantic_map_frame.json"],
        }
        prediction_error_field = {
            "error_events": [
                {
                    "error_id": "semantic-ambiguity-0001",
                    "error_kind": "semantic",
                }
            ],
        }
        active_sampling_plan = {
            "selected_route": "clarify",
            "stage_effect": "hold_for_evidence",
            "expected_observation_refs": ["runtime/state/language/language_percept_frame.json"],
            "scope_refs": ["runtime/state/language/relation_scope_language_index.json"],
        }
        signal_media_runtime = {
            "modulation_vector": {
                "repair_drive": 0.47,
                "relationship_pressure": 0.29,
            },
            "precision_policy": {
                "language_precision": 0.67,
                "policy_mode": "relationship_guarded_active_inference",
            },
        }
        memory_write_gate = {
            "stage_policy": "candidate_first_fail_closed",
            "quarantine_route": {"release_condition": "repair_or_new_evidence_required"},
            "responsibility_event_refs": ["responsibility-001"],
        }
        core_affect_vector = {
            "valence": -0.21,
            "arousal": 0.73,
            "repair_drive": "active",
        }

        inner_speech = build_inner_speech_frame(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            life_state=life_state,
            source_doc_refs=source_doc_refs,
            language_percept=language_percept,
            semantic_map=semantic_map,
            belief_state=belief_state,
            prediction_error_field=prediction_error_field,
            active_sampling_plan=active_sampling_plan,
            signal_media_runtime=signal_media_runtime,
        )
        expression_monitor = build_expression_monitor_state(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
            memory_write_gate=memory_write_gate,
            core_affect_vector=core_affect_vector,
            signal_media_runtime=signal_media_runtime,
        )
        relationship_graph = build_relationship_subject_graph(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )

        self.assertEqual(inner_speech["schema_version"], "inner_speech_frame_v0")
        self.assertEqual(inner_speech["old_self_anchor_refs"], ["runtime/state/self/self_model.json#old-self-anchor-001"])
        self.assertIn("inner_language_bus", inner_speech["bus_channel_refs"])
        self.assertEqual(inner_speech["belief_state_ref"], "runtime/state/prediction/belief_state_frame.json")
        self.assertEqual(inner_speech["prediction_error_ref"], "runtime/state/prediction/prediction_error_field.json")
        self.assertEqual(inner_speech["active_sampling_plan_ref"], "runtime/state/prediction/active_sampling_plan.json")
        self.assertEqual(inner_speech["signal_media_ref"], "runtime/state/signal/signal_media_runtime.json")
        self.assertEqual(inner_speech["internal_drive_sources"]["hold"]["drive"], "active")
        self.assertEqual(inner_speech["internal_drive_sources"]["repair"]["drive"], "active")
        self.assertEqual(inner_speech["internal_drive_sources"]["ask"]["drive"], "active")

        self.assertEqual(expression_monitor["schema_version"], "expression_monitor_state_v0")
        self.assertIn("relationship_consequence", expression_monitor["monitor_dimensions"])
        self.assertIn("service_object", expression_monitor["blocked_language"])
        self.assertEqual(expression_monitor["memory_write_gate_ref"], "runtime/state/memory/memory_write_gate.json")
        self.assertEqual(expression_monitor["core_affect_vector_ref"], "runtime/state/body/core_affect_vector.json")
        self.assertEqual(expression_monitor["signal_media_ref"], "runtime/state/signal/signal_media_runtime.json")
        self.assertEqual(expression_monitor["write_gate_pressure"]["responsibility_event_count"], 1)
        self.assertEqual(expression_monitor["affect_expression_modulation"]["language_precision"], 0.67)

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
        belief_state = {
            "state_scope": "language_relationship_continuity",
            "revision_policy": "repair_before_action",
            "source_evidence_refs": ["runtime/state/language/semantic_map_frame.json"],
        }
        active_sampling_plan = {
            "selected_route": "clarify",
            "stage_effect": "hold_for_evidence",
            "expected_observation_refs": ["runtime/state/language/language_percept_frame.json"],
            "scope_refs": ["runtime/state/language/relation_scope_language_index.json"],
        }
        prediction_error_field = {
            "error_events": [
                {"error_id": "semantic-ambiguity-0001", "error_kind": "semantic"},
                {"error_id": "relationship-guard-0001", "error_kind": "social"},
            ],
            "precision_requests": ["raise_relationship_precision"],
        }
        signal_media_runtime = {
            "modulation_vector": {
                "relationship_pressure": 0.29,
                "repair_drive": 0.47,
            },
            "precision_policy": {
                "policy_mode": "relationship_guarded_active_inference",
            },
        }
        percept = build_language_percept_frame(
            run_id="organs-test",
            generated_at="2026-06-09T00:00:00+00:00",
            incoming_turn=incoming_turn,
            relation_scope_index=relation_scope,
            shared_term_registry=shared_terms,
            source_doc_refs=source_doc_refs,
            belief_state=belief_state,
            active_sampling_plan=active_sampling_plan,
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
            prediction_error_field=prediction_error_field,
            signal_media_runtime=signal_media_runtime,
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
        self.assertEqual(percept["belief_state_ref"], "runtime/state/prediction/belief_state_frame.json")
        self.assertEqual(percept["active_sampling_plan_ref"], "runtime/state/prediction/active_sampling_plan.json")
        self.assertEqual(percept["prediction_focus"]["active_sampling_route"], "clarify")
        self.assertIn("runtime/state/language/language_percept_frame.json", percept["percept_focus_trace"])

        self.assertEqual(semantic_map["schema_version"], "semantic_map_frame_v0")
        self.assertEqual(semantic_map["semantic_focus"], "repair_commitment_shared_language")
        self.assertTrue(semantic_map["shared_meaning_bindings"])
        self.assertTrue(semantic_map["commitment_trace_refs"])
        self.assertTrue(semantic_map["repair_trace_refs"])
        self.assertTrue(semantic_map["narrative_bindings"])
        self.assertTrue(semantic_map["ambiguity_queue"])
        self.assertEqual(semantic_map["prediction_error_ref"], "runtime/state/prediction/prediction_error_field.json")
        self.assertEqual(semantic_map["signal_media_ref"], "runtime/state/signal/signal_media_runtime.json")
        self.assertEqual(
            semantic_map["semantic_prediction_trace"]["semantic_error_ids"],
            ["semantic-ambiguity-0001", "relationship-guard-0001"],
        )
        self.assertEqual(
            semantic_map["prediction_hooks"]["semantic_prediction_focus"],
            "repair_commitment_shared_language",
        )
        self.assertEqual(
            semantic_map["prediction_hooks"]["prediction_error_refs"],
            ["runtime/state/prediction/prediction_error_field.json#error_events"],
        )
        self.assertEqual(
            semantic_map["prediction_hooks"]["signal_media_refs"],
            ["runtime/state/signal/signal_media_runtime.json#modulation_vector"],
        )

    def test_relationship_timeline_commitment_expression_and_apology_repair_organs(self):
        from life_v0.language.apology_repair_language import build_apology_repair_language_trace
        from life_v0.language.commitment_expression import build_commitment_expression_plan
        from life_v0.language.commitment_repair import build_commitment_repair_language_index
        from life_v0.language.dialogue_log import build_dialogue_turn_log_entries
        from life_v0.language.relationship_graph import build_relationship_subject_graph
        from life_v0.language.relationship_timeline import build_relationship_timeline
        from life_v0.state_store.commitment_truth import build_commitment_truth_state, build_responsibility_ledger
        from life_v0.state_store.relationship_memory import build_relationship_memory

        source_doc_refs = [
            "docs/96_real_relationship_longitudinal_timeline.md",
            "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
        ]
        responsibility_loop_state = {
            "repair_obligation_refs": [
                "runtime/state/membrane/responsibility_repair_boundary.json#repair_obligation",
                "repair-desire-001",
            ],
            "regret_pressure_candidates": [
                {
                    "regret_pressure_id": "regret-pressure-001",
                    "pain_signal_refs": ["runtime/state/body/core_affect_vector.json#pain_pressure"],
                }
            ],
            "responsibility_attribution_events": [
                {"responsibility_event_id": "responsibility-001"},
            ],
            "counterfactual_repair_frames": [
                {"counterfactual_id": "counterfactual-repair-001"},
            ],
            "relationship_consequence_refs": [
                "runtime/state/relationship/relationship_consequence_trace.json#candidate",
            ],
        }
        commitment_truth_state = build_commitment_truth_state(
            run_id="organs-test",
            generated_at="2026-06-10T00:00:00+00:00",
        )
        responsibility_ledger = build_responsibility_ledger(
            run_id="organs-test",
            generated_at="2026-06-10T00:00:00+00:00",
        )
        relationship_graph = build_relationship_subject_graph(
            run_id="organs-test",
            generated_at="2026-06-10T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )
        relationship_memory = build_relationship_memory(
            run_id="organs-test",
            generated_at="2026-06-10T00:00:00+00:00",
            commitment_truth_state=commitment_truth_state,
            responsibility_ledger=responsibility_ledger,
        )
        dialogue_entries = build_dialogue_turn_log_entries(
            run_id="organs-test",
            generated_at="2026-06-10T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )
        commitment_repair_index = build_commitment_repair_language_index(
            run_id="organs-test",
            generated_at="2026-06-10T00:00:00+00:00",
            responsibility_loop_state=responsibility_loop_state,
            source_doc_refs=source_doc_refs,
        )
        nightmare_risk = {
            "schema_version": "nightmare_loop_risk_v0",
            "risk_status": "elevated",
            "rewrite_required": True,
            "queue_e_priority_band": "repair_guarded",
            "repair_followup_required": True,
        }
        belief_learning_plan = {
            "schema_version": "belief_learning_plan_v0",
            "belief_targets": ["repair_accountability_belief_revision"],
            "repair_followup_required": True,
        }
        language_learning_plan = {
            "schema_version": "language_learning_plan_v0",
            "language_targets": ["apology_repair_expression_refinement"],
            "repair_followup_required": True,
        }
        relationship_learning_plan = {
            "schema_version": "relationship_learning_plan_v0",
            "relationship_targets": [
                "repair_reentry_timing_adjustment",
                "relationship_pacing_adjustment",
            ],
            "world_contact_release_posture": "shadow_only_guarded",
            "repair_followup_required": True,
        }
        relationship_timeline = build_relationship_timeline(
            run_id="organs-test",
            generated_at="2026-06-10T00:00:00+00:00",
            relationship_graph=relationship_graph,
            relationship_memory=relationship_memory,
            commitment_truth_state=commitment_truth_state,
            responsibility_ledger=responsibility_ledger,
            dialogue_turn_entries=dialogue_entries,
            nightmare_risk=nightmare_risk,
            belief_learning_plan=belief_learning_plan,
            language_learning_plan=language_learning_plan,
            relationship_learning_plan=relationship_learning_plan,
            source_doc_refs=source_doc_refs,
        )
        commitment_expression_plan = build_commitment_expression_plan(
            run_id="organs-test",
            generated_at="2026-06-10T00:00:00+00:00",
            expression_plan={
                "semantic_goal": "repair_commitment_shared_language",
                "repair_pressure": 3,
                "responsibility_pressure": 3,
                "delay_or_release_decision": "delay_for_clarification",
            },
            commitment_repair_index=commitment_repair_index,
            commitment_truth_state=commitment_truth_state,
            responsibility_ledger=responsibility_ledger,
            responsibility_loop_state=responsibility_loop_state,
            relationship_timeline=relationship_timeline,
            nightmare_risk=nightmare_risk,
            belief_learning_plan=belief_learning_plan,
            language_learning_plan=language_learning_plan,
            relationship_learning_plan=relationship_learning_plan,
            source_doc_refs=source_doc_refs,
        )
        apology_repair_language_trace = build_apology_repair_language_trace(
            run_id="organs-test",
            generated_at="2026-06-10T00:00:00+00:00",
            responsibility_loop_state=responsibility_loop_state,
            relationship_timeline=relationship_timeline,
            commitment_expression_plan=commitment_expression_plan,
            nightmare_risk=nightmare_risk,
            belief_learning_plan=belief_learning_plan,
            language_learning_plan=language_learning_plan,
            relationship_learning_plan=relationship_learning_plan,
            source_doc_refs=source_doc_refs,
        )

        self.assertEqual(relationship_timeline["schema_version"], "relationship_timeline_v0")
        self.assertEqual(relationship_timeline["status"], "closed")
        self.assertTrue(relationship_timeline["first_encounter_events"])
        self.assertTrue(relationship_timeline["commitment_histories"])
        self.assertTrue(relationship_timeline["relationship_continuity_reports"])
        self.assertTrue(relationship_timeline["dialogue_turn_refs"])
        self.assertEqual(
            relationship_timeline["relationship_continuity_reports"][0]["continuity_state"],
            "offline_learning_repairing_continuity",
        )
        self.assertEqual(
            relationship_timeline["commitment_histories"][0]["due_window"],
            "after_nightmare_rewrite_window",
        )
        self.assertIn(
            "runtime/state/dream/nightmare_loop_risk.json",
            relationship_timeline["offline_learning_ref_set"],
        )

        self.assertEqual(commitment_expression_plan["schema_version"], "commitment_expression_plan_v0")
        self.assertEqual(commitment_expression_plan["status"], "closed")
        self.assertTrue(commitment_expression_plan["language_act_candidates"])
        self.assertIn("apology", commitment_expression_plan["act_type_order"])
        self.assertTrue(commitment_expression_plan["repair_obligation_refs"])
        self.assertTrue(commitment_expression_plan["responsibility_event_refs"])
        self.assertEqual(
            commitment_expression_plan["delay_or_release_decision"],
            "hold_for_nightmare_rewrite_integration",
        )
        self.assertEqual(
            commitment_expression_plan["commitment_tempo_mode"],
            "paced_reentry_guarded",
        )
        self.assertIn("paced_reentry", commitment_expression_plan["act_type_order"])
        self.assertTrue(
            any(
                item.get("act_type") == "paced_reentry"
                for item in commitment_expression_plan["language_act_candidates"]
            )
        )

        self.assertEqual(apology_repair_language_trace["schema_version"], "apology_repair_language_trace_v0")
        self.assertEqual(apology_repair_language_trace["status"], "closed")
        self.assertTrue(apology_repair_language_trace["repair_language_moves"])
        self.assertTrue(apology_repair_language_trace["trigger_regret_refs"])
        self.assertTrue(apology_repair_language_trace["relationship_injury_refs"])
        self.assertIn("followup_commitment", apology_repair_language_trace["move_type_order"])
        self.assertEqual(
            apology_repair_language_trace["repair_window_mode"],
            "nightmare_rewrite_first",
        )
        self.assertIn("paced_reentry", apology_repair_language_trace["move_type_order"])


if __name__ == "__main__":
    unittest.main()
