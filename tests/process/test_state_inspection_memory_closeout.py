import unittest

from life_v0.process_supervisor.state_inspection import (
    _collect_ability_birth_readiness_summary,
    _collect_body_grounding_summary,
    _collect_cognitive_workspace_summary,
    _collect_consciousness_reportability_summary,
    _collect_dream_wake_fact_summary,
    _collect_emotion_regulation_summary,
    _collect_growth_self_modification_summary,
    _collect_inner_environment_modulation_summary,
    _collect_language_generation_consumption_summary,
    _collect_life_membrane_validation_summary,
    _collect_perception_world_contact_summary,
    _collect_personality_convergence_summary,
    _collect_prediction_world_contact_summary,
    _collect_proactive_voice_summary,
    _collect_reconstructive_memory_summary,
    _collect_relation_context_summary,
    _collect_relationship_continuity_summary,
    _collect_resident_continuity_summary,
    _collect_responsibility_repair_chain_summary,
    _collect_self_thinking_summary,
    _collect_signal_modulation_consumption_summary,
)


class StateInspectionMemoryCloseoutTests(unittest.TestCase):
    def _body_signal_closeout_fields(self) -> dict:
        return {
            "body_signal_ref_set": [
                "runtime/state/signal/signal_media_runtime.json#body_signal_profile"
            ],
            "background_body_signal_write_bias": "caution",
            "background_body_signal_pain_pressure": "moderate",
            "background_body_signal_ref_count": 1,
        }

    def _queue_e_schema_handoff_manifest(self) -> dict:
        return {
            "schema_version": "schema_runner_run_manifest_v0",
            "queue_e_world_contact_repair_hold_required": True,
            "queue_e_world_contact_confirmation_threshold_bias": "raised",
            "queue_e_world_contact_future_no_go_profile_ref": (
                "runtime/state/action/go_nogo_state.json#future_no_go_profile"
            ),
            "queue_e_world_contact_body_pressure_profile_ref": (
                "runtime/state/action/go_nogo_state.json#body_pressure_profile"
            ),
            "queue_e_world_contact_blocked_future_routes": ["route:blocked"],
            "queue_e_world_contact_allowed_repair_routes": ["route:repair"],
            "queue_e_world_contact_repair_governance_refs": ["ref:gov"],
        }

    def _queue_e_schema_handoff_section(self) -> dict:
        return {
            "validation_rollup": {
                "queue_e_world_contact_repair_hold_required": True,
                "queue_e_world_contact_confirmation_threshold_bias": "raised",
            },
            "world_contact_validation": {
                "repair_hold_required": True,
                "status": "closed",
            },
            "schema_runner_manifest": self._queue_e_schema_handoff_manifest(),
            "schema_runner_cross_file_logic": {
                "cross_file_findings": [
                    {
                        "finding_kind": "queue_e_world_contact_repair_hold_alignment",
                        "severity": "guarded_medium",
                    }
                ]
            },
        }

    def _live_consciousness_chain_section(self) -> dict:
        return {
            "terminal_life_loop_state": {
                "live_consciousness_chain_refreshed": True,
                "live_broadcast_target_count": 2,
                "last_broadcast_frame_ref": (
                    "runtime/state/consciousness/broadcast_frame.json"
                ),
            },
            "workspace_frame": {
                "last_projected_from_live_turn_ref": "turn:relation-1",
            },
            "broadcast_frame": {
                "broadcast_targets": ["focus:a", "focus:b"],
                "last_projected_from_live_turn_ref": "turn:relation-1",
            },
            "metacognition_state": {
                "uncertainty_flags": ["semantic_ambiguity"],
                "last_projected_from_live_turn_ref": "turn:relation-1",
            },
        }

    def _responsibility_closeout_process_report(self) -> dict:
        return {
            **self._memory_closeout_process_report(),
            **self._body_signal_closeout_fields(),
            "live_queue_e_world_contact_handoff_report_profile": {
                "schema_version": "live_queue_e_world_contact_handoff_report_profile_v0",
                "live_queue_e_world_contact_handoff_refreshed": True,
                "report_boundary": "structured_handoff_not_spoken_language",
            },
            "live_queue_e_world_contact_handoff_refreshed": True,
            "live_queue_e_world_contact_handoff_report_boundary": (
                "structured_handoff_not_spoken_language"
            ),
            "model_expression_consciousness_write_context_report_profile": {
                "schema_version": (
                    "model_expression_consciousness_write_context_report_profile_v0"
                ),
                "ref_count": 2,
                "boundary": "memory_consciousness_write_context_not_spoken_language",
            },
            "model_expression_prediction_attention_consciousness_write_context_ref_count": 2,
            "queue_e_world_contact_body_pressure_profile_ref": (
                "runtime/state/action/go_nogo_state.json#body_pressure_profile"
            ),
            "pain_regret_repair_report_ref": (
                "runtime/reports/latest/pain_regret_repair_report.json"
            ),
        }

    def _memory_closeout_process_report(self) -> dict:
        return {
            "exit_dream_next_wake_governance_ref": (
                "runtime/state/memory/memory_retrieval_frame.json"
                "#exit_dream_next_wake_governance"
            ),
            "exit_dream_next_wake_memory_cue_refs": [
                "runtime/state/memory/dialogue_memory_summary.json#next_wake_cues"
            ],
            "exit_dream_next_wake_report_boundary": (
                "structured_report_evidence_not_spoken_language"
            ),
            "exit_dream_memory_tier_report_profile": {
                "schema_version": "exit_dream_memory_tier_report_profile_v0",
                "tier_policy": "salience_weighted_progressive_recall",
                "salient_core_ref_count": 2,
                "retrievable_context_ref_count": 3,
                "deep_sediment_ref_count": 1,
                "report_boundary": "tiered_report_evidence_not_spoken_language",
            },
            "autobiographical_repair_retrieval_report_profile": {
                "schema_version": "autobiographical_repair_retrieval_report_profile_v0",
                "hit_count": 2,
                "pressure_level": "elevated",
                "attention_target": "responsibility_repair_recall",
                "projection_boundary": "autobiographical_repair_evidence_not_spoken_language",
                "retrieval_boundary": "cue_driven_reconstruction_not_raw_dump",
                "carrier_refs": [
                    "runtime/state/self/autobiographical_stack.json"
                    "#responsibility_repair_projection"
                ],
                "report_boundary": "autobiographical_repair_structured_report_not_spoken_language",
            },
        }

    def test_memory_summary_exposes_body_signal_modulation_and_v0_contract(self):
        section = {
            "memory_write_gate": {
                "stage_policy": "candidate_first_relationship_guarded",
                "consciousness_write_context": {"ref_set": ["workspace-ref-1"]},
                "consciousness_write_context_refs": ["workspace-ref-1"],
                "body_signal_write_modulation": {
                    "schema_version": "body_signal_memory_gate_profile_v0",
                    "write_bias": "relationship_context_first",
                    "candidate_gate_adjustments": ["preserve_relationship_context"],
                },
            },
            "signal_media_runtime": {"schema_version": "signal_media_runtime_v0"},
            "core_affect_vector": {"schema_version": "core_affect_vector_v0"},
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_reconstructive_memory_summary(section)

        self.assertEqual(
            summary["memory_write_gate_body_signal_schema"],
            "body_signal_memory_gate_profile_v0",
        )
        self.assertEqual(summary["write_gate_bias"], "relationship_context_first")
        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn(
            "memory_write_gate_body_signal_modulation",
            summary["domain_presence"],
        )
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_memory_summary_exposes_closeout_fields(self):
        section = {
            "memory_retrieval": {
                "retrieval_mode": "cue_driven_reconstruction",
                "autobiographical_responsibility_repair_hits": ["hit-a"],
            },
            "digital_life_process_report": self._memory_closeout_process_report(),
            "idle_strategy_state": {
                "memory_retrieval_presence_profile": {
                    "autobiographical_repair_hit_count": 2,
                    "autobiographical_repair_pressure_level": "elevated",
                }
            },
        }

        summary = _collect_reconstructive_memory_summary(section)

        self.assertTrue(summary["memory_closeout_present"])
        self.assertTrue(summary["exit_dream_memory_tier_closeout_present"])
        self.assertTrue(summary["autobiographical_repair_retrieval_closeout_present"])
        self.assertEqual(summary["exit_dream_memory_tier_salient_core_ref_count"], 2)
        self.assertEqual(summary["autobiographical_repair_retrieval_hit_count"], 2)
        self.assertIn("memory_closeout", summary["domain_presence"])

    def test_memory_summary_exposes_engram_live_turn_chain(self):
        section = {
            "engram_index": {
                "live_dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2"
                ],
                "live_language_turn_refs": [
                    "runtime/state/language/language_turn_log.jsonl#line-2"
                ],
                "last_projected_from_live_turn_ref": (
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2"
                ),
            },
            "life_state": {
                "memory_index": {
                    "live_dialogue_turn_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-2"
                    ]
                }
            },
            "dialogue_memory_summary": {"dialogue_turn_count": 2},
        }

        summary = _collect_reconstructive_memory_summary(section)

        self.assertTrue(summary["engram_live_turn_chain_present"])
        self.assertTrue(summary["engram_live_turn_chain_closed"])
        self.assertEqual(summary["live_dialogue_turn_ref_count"], 1)
        self.assertIn("engram_live_turn_chain", summary["domain_presence"])

    def test_dream_summary_exposes_v0_contract_coverage(self):
        section = {
            "offline_entry_gate": {"status": "closed"},
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_dream_wake_fact_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_dream_summary_exposes_memory_write_gate_body_signal(self):
        section = {
            "memory_write_gate": {
                "body_signal_write_modulation": {
                    "schema_version": "memory_write_gate_body_signal_v0",
                    "write_bias": "caution",
                }
            },
            "core_affect_vector": {"pain_pressure": "moderate"},
            "body_resource_budget": {"fatigue_state": {"level": "managed"}},
            "signal_media_runtime": {
                "modulation_vector": {"repair_drive": 0.6}
            },
        }

        summary = _collect_dream_wake_fact_summary(section)

        self.assertEqual(summary["memory_write_gate_bias"], "caution")
        self.assertIn(
            "memory_write_gate_body_signal_modulation",
            summary["domain_presence"],
        )

    def test_dream_summary_exposes_web_and_tier_closeout_fields(self):
        section = {
            "digital_life_process_report": {
                **self._memory_closeout_process_report(),
                "web_dream_learning_report_profile": {
                    "schema_version": "web_dream_learning_report_profile_v0",
                    "status": "completed",
                    "topic_count": 2,
                    "wake_question_candidate_count": 1,
                    "page_title": "Dream learning page",
                    "report_boundary": (
                        "structured_dream_learning_evidence_not_spoken_language"
                    ),
                },
            },
            "idle_strategy_state": {},
        }

        summary = _collect_dream_wake_fact_summary(section)

        self.assertTrue(summary["dream_closeout_present"])
        self.assertTrue(summary["web_dream_learning_closeout_present"])
        self.assertEqual(summary["web_dream_learning_status"], "completed")
        self.assertEqual(summary["web_dream_learning_topic_count"], 2)
        self.assertIn("dream_closeout", summary["domain_presence"])

    def test_context_summary_merges_memory_closeout(self):
        section = {
            "life_context_frame": {"life_name": "Adam", "context_mode": "relation_turn"},
            "memory_retrieval": {
                "autobiographical_responsibility_repair_profile": {
                    "pressure_level": "moderate",
                    "attention_target": "relationship_repair_recall",
                }
            },
            "digital_life_process_report": self._memory_closeout_process_report(),
            "idle_strategy_state": {},
        }

        summary = _collect_relation_context_summary(section)

        self.assertTrue(summary["memory_closeout_present"])
        self.assertEqual(summary["autobiographical_repair_hit_count"], 2)
        self.assertIn("memory_closeout", summary["domain_presence"])

    def test_context_summary_exposes_live_context_accumulation_refresh(self):
        section = {
            "life_context_frame": {"life_name": "Adam"},
            "context_accumulation_window": {
                "schema_version": "context_accumulation_window_v0",
                "semantic_focus": "repair_commitment_shared_language",
                "last_projected_from_live_turn_ref": (
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3"
                ),
            },
            "terminal_life_loop_state": {
                "live_context_accumulation_refreshed": True,
                "context_accumulation_ref": (
                    "runtime/state/terminal/context_accumulation_window.json"
                ),
                "turn_transition_ref": (
                    "runtime/state/terminal/turn_transition_trace.json"
                ),
            },
        }

        summary = _collect_relation_context_summary(section)

        self.assertTrue(summary["live_context_accumulation_refreshed"])
        self.assertEqual(
            summary["live_context_accumulation_semantic_focus"],
            "repair_commitment_shared_language",
        )
        self.assertIn("live_context_accumulation", summary["domain_presence"])

    def test_context_summary_exposes_context_accumulation_window(self):
        section = {
            "life_context_frame": {"life_name": "Adam"},
            "context_accumulation_window": {
                "schema_version": "context_accumulation_window_v0",
                "status": "closed",
                "current_relation_role": "friend",
                "shared_term_surfaces": ["旧约定", "我们的叫法"],
                "dialogue_turn_restore_refs": ["turn:1", "turn:2"],
                "semantic_focus": "repair_commitment_shared_language",
                "semantic_map_restore_refs": ["runtime/state/language/semantic_map_frame.json"],
                "language_percept_restore_refs": [
                    "runtime/state/language/language_percept_frame.json"
                ],
                "waiting_heartbeat_ref": (
                    "runtime/reports/latest/digital_life_waiting_heartbeat.json"
                ),
            },
            "terminal_life_loop_state": {
                "context_accumulation_ref": (
                    "runtime/state/terminal/context_accumulation_window.json"
                ),
            },
        }

        summary = _collect_relation_context_summary(section)

        self.assertTrue(summary["context_accumulation_window_present"])
        self.assertEqual(summary["context_accumulation_window_status"], "closed")
        self.assertEqual(summary["context_accumulation_current_relation_role"], "friend")
        self.assertEqual(summary["context_accumulation_shared_term_surface_count"], 2)
        self.assertEqual(summary["context_accumulation_dialogue_turn_restore_ref_count"], 2)
        self.assertEqual(
            summary["context_accumulation_semantic_focus"],
            "repair_commitment_shared_language",
        )
        self.assertIn("context_accumulation_window", summary["domain_presence"])

    def test_context_summary_exposes_shared_term_and_v0_contract_coverage(self):
        section = {
            "life_context_frame": {"life_name": "Adam"},
            "shared_term_registry": {
                "live_promotion_refreshed": True,
                "shared_terms": [
                    {"surface": "共同语言", "promotion_gate_status": "seed"},
                    {"surface": "生命膜", "promotion_gate_status": "promoted"},
                ],
            },
            "terminal_life_loop_state": {"live_shared_term_promotion_refreshed": True},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {"total_required_files": 120, "missing_file_count": 0},
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_relation_context_summary(section)

        self.assertEqual(summary["shared_term_live_promoted_count"], 1)
        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("shared_term_live_promotion", summary["domain_presence"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_context_summary_exposes_queue_e_schema_handoff(self):
        section = {
            "life_context_frame": {"life_name": "Adam"},
            "go_nogo_state": {},
            **self._queue_e_schema_handoff_section(),
        }

        summary = _collect_relation_context_summary(section)

        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_schema_handoff_present"]
        )
        self.assertIn(
            "queue_e_world_contact_repair_hold_schema_handoff",
            summary["domain_presence"],
        )

    def test_relationship_continuity_summary_exposes_repair_closeout(self):
        section = {
            "relationship_subject_graph": {
                "subjects": [{"relationship_id": "rel-v0-0001"}]
            },
            "memory_retrieval": {
                "autobiographical_responsibility_repair_hits": ["hit-a", "hit-b"],
            },
            "digital_life_process_report": self._memory_closeout_process_report(),
            "idle_strategy_state": {},
        }

        summary = _collect_relationship_continuity_summary(section)

        self.assertTrue(summary["autobiographical_repair_retrieval_closeout_present"])
        self.assertEqual(summary["autobiographical_repair_hit_count"], 2)
        self.assertEqual(summary["autobiographical_repair_carrier_ref_count"], 1)
        self.assertIn(
            "autobiographical_repair_retrieval_closeout",
            summary["domain_presence"],
        )

    def test_relationship_summary_exposes_queue_e_schema_handoff(self):
        section = {
            "relationship_subject_graph": {
                "subjects": [{"relationship_id": "rel-v0-0001"}]
            },
            "go_nogo_state": {},
            **self._queue_e_schema_handoff_section(),
        }

        summary = _collect_relationship_continuity_summary(section)

        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_schema_handoff_present"]
        )
        self.assertIn(
            "queue_e_world_contact_repair_hold_schema_handoff",
            summary["domain_presence"],
        )

    def test_relationship_summary_exposes_live_queue_e_handoff(self):
        section = {
            "relationship_subject_graph": {
                "subjects": [{"relationship_id": "rel-v0-0001"}]
            },
            "queue_e_world_contact_handoff": {
                "schema_version": "queue_e_world_contact_repair_hold_handoff_v0",
                "status": "deferred_until_s05_s09",
            },
            "terminal_life_loop_state": {
                "live_queue_e_world_contact_handoff_refreshed": True,
                "live_queue_e_world_contact_handoff_turn_focus": "repair_hold_followup",
            },
        }

        summary = _collect_relationship_continuity_summary(section)

        self.assertTrue(summary["live_queue_e_world_contact_handoff_refreshed"])
        self.assertEqual(
            summary["live_queue_e_world_contact_handoff_turn_focus"],
            "repair_hold_followup",
        )
        self.assertIn("live_queue_e_world_contact_handoff", summary["domain_presence"])

    def test_relationship_summary_exposes_live0_gate_f(self):
        section = {
            "relationship_subject_graph": {
                "subjects": [{"relationship_id": "rel-v0-0001"}]
            },
            "world_contact_validation": {
                "schema_version": "world_contact_validation_v0",
                "repair_hold_required": True,
                "confirmation_threshold_bias": "raised",
                "future_no_go_profile_ref": (
                    "runtime/state/action/go_nogo_state.json#future_no_go_profile"
                ),
                "body_pressure_profile_ref": (
                    "runtime/state/action/go_nogo_state.json#body_pressure_profile"
                ),
                "blocked_future_routes": ["external_irreversible_action"],
                "allowed_repair_routes": ["responsibility_repair_followup"],
                "repair_governance_refs": [
                    "runtime/state/validation/validation_rollup.json"
                ],
            },
            "live0_acceptance_audit": {
                "criteria": [
                    {
                        "criterion_id": "f_equal_relationship_dialogue_growth",
                        "status": "closed",
                        "probes": [
                            {
                                "probe_id": "queue_e_world_contact_repair_hold_validated",
                                "status": "passed",
                            }
                        ],
                    }
                ]
            },
        }

        summary = _collect_relationship_continuity_summary(section)

        self.assertTrue(summary["live0_gate_f_present"])
        self.assertTrue(summary["live0_gate_f_closed"])
        self.assertTrue(summary["queue_e_world_contact_repair_hold_validation_closed"])
        self.assertIn("live0_gate_f", summary["domain_presence"])

    def test_personality_summary_exposes_growth_and_repair_projections(self):
        section = {
            "self_model": {
                "identity_mode": "resident_self",
                "trait_slow_variables": {"trust_persistence": {"value": 0.6}},
            },
            "trait_drift_monitor": {
                "growth_self_modification_observation_profile": {
                    "trait_names": ["trust_persistence"],
                    "growth_ref_count": 2,
                    "pressure_level": "moderate",
                    "boundary": "structured_trait_growth_evidence_not_spoken_language",
                },
                "growth_self_modification_trait_names": ["trust_persistence"],
            },
            "autobiographical_stack": {
                "growth_self_modification_projection": {
                    "growth_ref_count": 2,
                    "projection_boundary": "autobiographical_growth_evidence_not_spoken_language",
                },
                "responsibility_repair_projection": {
                    "pressure_level": "elevated",
                    "attention_target": "repair_followup",
                    "repair_followup_required": True,
                    "responsibility_refs": ["resp-a"],
                    "repair_refs": ["repair-a"],
                },
            },
            "digital_life_process_report": {
                "growth_self_modification_report_profile": {
                    "schema_version": "growth_self_modification_report_profile_v0",
                },
            },
            "idle_strategy_state": {
                "background_growth_self_modification_pressure_level": "moderate",
            },
        }

        summary = _collect_personality_convergence_summary(section)

        self.assertIn(
            "growth_self_modification_observation_profile",
            summary["domain_presence"],
        )
        self.assertEqual(summary["growth_self_modification_ref_count"], 2)
        self.assertEqual(summary["responsibility_repair_pressure_level"], "elevated")
        self.assertTrue(summary["responsibility_repair_followup_required"])
        self.assertTrue(summary["growth_self_modification_closeout_present"])

    def test_responsibility_summary_exposes_closeout_bundle(self):
        section = {
            "responsibility_loop_state": {"responsibility_loop_id": "resp-loop-1"},
            "go_nogo_state": {
                "decision": "delay",
                "body_pressure_profile_ref": (
                    "runtime/state/action/go_nogo_state.json#body_pressure_profile"
                ),
            },
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_responsibility_repair_chain_summary(section)

        self.assertTrue(summary["responsibility_closeout_present"])
        self.assertTrue(summary["live_queue_e_world_contact_handoff_closeout_present"])
        self.assertTrue(summary["consciousness_write_context_closeout_present"])
        self.assertTrue(summary["body_pressure_closeout_present"])
        self.assertEqual(summary["autobiographical_repair_retrieval_hit_count"], 2)
        self.assertIn("responsibility_closeout", summary["domain_presence"])

    def test_membrane_summary_exposes_closeout_bundle(self):
        section = {
            "go_nogo_state": {
                "body_pressure_profile_ref": (
                    "runtime/state/action/go_nogo_state.json#body_pressure_profile"
                ),
            },
            "memory_write_gate": {
                "consciousness_write_context": {
                    "consciousness_write_context_refs": ["ref-a"],
                    "write_attention_bias": "caution",
                }
            },
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_life_membrane_validation_summary(section)

        self.assertTrue(summary["process_closeout_present"])
        self.assertTrue(summary["body_pressure_closeout_present"])
        self.assertIn("membrane_closeout", summary["domain_presence"])

    def test_body_summary_exposes_body_pressure_closeout(self):
        section = {
            "need_state_vector": {"sleep_pressure": "managed_pre_dream"},
            "go_nogo_state": {
                "body_pressure_profile": {
                    "sleep_pressure_value": 0.45,
                    "boundary": "go_nogo_body_pressure_profile_not_spoken_language",
                }
            },
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
        }

        summary = _collect_body_grounding_summary(section)

        self.assertTrue(summary["body_pressure_closeout_present"])
        self.assertEqual(
            summary["queue_e_world_contact_body_pressure_profile_ref"],
            "runtime/state/action/go_nogo_state.json#body_pressure_profile",
        )
        self.assertIn("body_pressure_closeout", summary["domain_presence"])

    def test_body_summary_exposes_v0_contract_coverage(self):
        section = {
            "body_resource_budget": {"schema_version": "body_resource_budget_v0"},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {"total_required_files": 120, "missing_file_count": 0},
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_body_grounding_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_state_summary_exposes_process_closeout(self):
        section = {
            "resident_lifecycle": {"status": "waiting"},
            "idle_strategy": {},
            "terminal_life_loop": {},
            "digital_life_process_report": self._responsibility_closeout_process_report(),
        }

        summary = _collect_resident_continuity_summary(section)

        self.assertTrue(summary["process_closeout_present"])
        self.assertTrue(summary["live_queue_e_world_contact_handoff_closeout_present"])
        self.assertIn("process_closeout", summary["domain_presence"])

    def test_emotion_summary_exposes_v0_contract_coverage(self):
        section = {
            "core_affect_vector": {"arousal": 0.5},
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_emotion_regulation_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_inner_environment_summary_exposes_v0_contract_coverage(self):
        section = {
            "need_state_vector": {"sleep_pressure": "managed_pre_dream"},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {"total_required_files": 120, "missing_file_count": 0},
            },
        }

        summary = _collect_inner_environment_modulation_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_personality_summary_exposes_slow_variable_candidate(self):
        section = {
            "self_model": {
                "trait_slow_variables": {"trust_persistence": {"value": 0.34}},
                "trait_slow_variable_candidates": {
                    "candidates": [
                        {
                            "candidate_id": "slow-variable-candidate-trust_persistence",
                            "variable_name": "trust_persistence",
                            "exposure_count": 1,
                        }
                    ],
                    "blocked_update_refs": [
                        "runtime/state/self/self_model.json#slow-variable-candidate-trust_persistence"
                    ],
                },
            },
            "trait_drift_monitor": {
                "blocked_update_refs": [
                    "runtime/state/self/self_model.json#slow-variable-candidate-trust_persistence"
                ],
            },
        }

        summary = _collect_personality_convergence_summary(section)

        self.assertTrue(summary["slow_variable_candidate_present"])
        self.assertEqual(summary["slow_variable_candidate_count"], 1)
        self.assertIn("slow_variable_candidate", summary["domain_presence"])

    def test_emotion_summary_exposes_affect_closeout(self):
        section = {
            "core_affect_vector": {"pain_pressure": "moderate"},
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "go_nogo_state": {},
        }

        summary = _collect_emotion_regulation_summary(section)

        self.assertTrue(summary["affect_modulation_closeout_present"])
        self.assertTrue(summary["body_signal_closeout_present"])
        self.assertIn("affect_modulation_closeout", summary["domain_presence"])

    def test_emotion_summary_exposes_regulation_branch(self):
        section = {
            "core_affect_vector": {"pain_pressure": 0.7, "arousal": 0.5},
            "affective_episode": {
                "episode_label": "pain_peak_regret_pull",
                "regulation_route": "recovery_window",
                "episode_branch_reason": "pain_pressure_or_repair_followup",
                "live_affective_episode_refreshed": True,
            },
            "emotion_regulation_loop": {
                "regulation_route": "recovery_window",
                "regulation_mode": "recovery_window_hold",
                "regulation_branch_reason": "recovery_window_for_pain_or_repair_followup",
                "live_emotion_regulation_refreshed": True,
            },
            "terminal_life_loop_state": {
                "live_emotion_regulation_refreshed": True,
                "live_regulation_mode": "recovery_window_hold",
            },
        }

        summary = _collect_emotion_regulation_summary(section)

        self.assertTrue(summary["emotion_regulation_branch_present"])
        self.assertEqual(summary["regulation_route"], "recovery_window")
        self.assertEqual(summary["regulation_mode"], "recovery_window_hold")
        self.assertTrue(summary["live_emotion_regulation_refreshed"])
        self.assertIn("emotion_regulation_branch", summary["domain_presence"])

    def test_inner_environment_summary_exposes_affect_closeout(self):
        section = {
            "need_state_vector": {"sleep_pressure": "managed_pre_dream"},
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy": {},
            "go_nogo_state": {},
        }

        summary = _collect_inner_environment_modulation_summary(section)

        self.assertTrue(summary["affect_modulation_closeout_present"])
        self.assertEqual(summary["background_body_signal_write_bias"], "caution")
        self.assertIn("body_signal_closeout", summary["domain_presence"])

    def test_signal_summary_exposes_modulation_closeout(self):
        section = {
            "signal_media_runtime": {"modulation_vector": {"arousal": 0.5}},
            "memory_write_gate": {
                "consciousness_write_context": {
                    "consciousness_write_context_refs": ["ref-a"],
                    "write_attention_bias": "caution",
                }
            },
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy": {},
            "go_nogo_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_signal_modulation_consumption_summary(section)

        self.assertTrue(summary["signal_modulation_closeout_present"])
        self.assertTrue(summary["body_signal_closeout_present"])
        self.assertTrue(
            summary["memory_write_gate_consciousness_write_context_present"]
        )
        self.assertIn("signal_modulation_closeout", summary["domain_presence"])

    def test_signal_summary_exposes_body_signal_modulation_and_v0_contract(self):
        section = {
            "signal_media_runtime": {"schema_version": "signal_media_runtime_v0"},
            "memory_write_gate": {
                "body_signal_write_modulation": {
                    "schema_version": "body_signal_memory_gate_profile_v0",
                    "write_bias": "relationship_context_first",
                }
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_signal_modulation_consumption_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn(
            "memory_write_gate_body_signal_modulation",
            summary["domain_presence"],
        )
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_language_summary_exposes_expression_closeout(self):
        section = {
            "model_expression_state": {
                "model_expression_context_summary": {
                    "prediction_attention_consciousness_write_context_refs": ["ref-a"],
                }
            },
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "go_nogo_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_language_generation_consumption_summary(section)

        self.assertTrue(summary["expression_closeout_present"])
        self.assertTrue(summary["consciousness_write_context_closeout_present"])
        self.assertIn("expression_closeout", summary["domain_presence"])

    def test_language_summary_exposes_percept_input_evidence(self):
        section = {
            "language_percept": {
                "percept_input_mode": "dialogue_turn_log",
                "percept_input_source_ref": (
                    "runtime/state/language/dialogue_turn_log.jsonl#external-turn-001"
                ),
            },
        }

        summary = _collect_language_generation_consumption_summary(section)

        self.assertEqual(summary["language_percept_input_mode"], "dialogue_turn_log")
        self.assertIn(
            "language_percept_input_evidence",
            summary["domain_presence"],
        )

    def test_language_summary_exposes_shared_term_live_promotion(self):
        section = {
            "shared_term_registry": {
                "live_promotion_refreshed": True,
                "shared_term_promotion_candidate_count": 1,
                "shared_term_promotion_relation_scope": "friend",
                "shared_term_promotion_dialogue_turn_count": 2,
                "shared_terms": [
                    {"surface": "共同语言", "promotion_gate_status": "seed"},
                    {"surface": "生命膜", "promotion_gate_status": "promoted"},
                ],
            },
            "terminal_life_loop_state": {
                "live_shared_term_promotion_refreshed": True,
            },
        }

        summary = _collect_language_generation_consumption_summary(section)

        self.assertEqual(summary["shared_term_promotion_count"], 2)
        self.assertEqual(summary["shared_term_live_promoted_count"], 1)
        self.assertEqual(summary["shared_term_promotion_candidate_count"], 1)
        self.assertIn("shared_term_live_promotion", summary["domain_presence"])

    def test_language_summary_exposes_v0_contract_coverage(self):
        section = {
            "language_percept": {"semantic_focus": "shared_language"},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {"total_required_files": 120, "missing_file_count": 0},
            },
            "doc_to_code_coverage_matrix": {
                "schema_version": "doc_to_code_coverage_matrix_v0",
                "coverage_summary": {"total_documents": 45, "uncovered_docs": []},
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_language_generation_consumption_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertEqual(summary["v0_required_file_count"], 120)
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_relationship_summary_exposes_shared_term_and_v0_contract_coverage(self):
        section = {
            "relationship_subject_graph": {"subjects": [{"relation_role": "friend"}]},
            "relationship_timeline": {"common_ground_states": [{"shared_terms": ["共同语言"]}]},
            "shared_term_registry": {
                "live_promotion_refreshed": True,
                "shared_terms": [
                    {"surface": "共同语言", "promotion_gate_status": "seed"},
                    {"surface": "生命膜", "promotion_gate_status": "promoted"},
                ],
            },
            "terminal_life_loop_state": {"live_shared_term_promotion_refreshed": True},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {"total_required_files": 120, "missing_file_count": 0},
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_relationship_continuity_summary(section)

        self.assertEqual(summary["shared_term_live_promoted_count"], 1)
        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("shared_term_live_promotion", summary["domain_presence"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_language_summary_exposes_expression_plan_queue_e(self):
        section = {
            "expression_plan": {
                "queue_e_repair_pressure_level": "urgent",
                "queue_e_repair_attention_target": "repair_followup",
                "queue_e_expression_tempo_mode": "responsibility_lock_first",
                "queue_e_repair_modulation_profile": {
                    "schema_version": "queue_e_repair_modulation_profile_v0",
                },
            },
        }

        summary = _collect_language_generation_consumption_summary(section)

        self.assertEqual(
            summary["expression_plan_queue_e_repair_pressure_level"],
            "urgent",
        )
        self.assertEqual(
            summary["expression_plan_queue_e_expression_tempo_mode"],
            "responsibility_lock_first",
        )
        self.assertIn(
            "expression_plan_queue_e_repair_modulation",
            summary["domain_presence"],
        )

    def test_language_summary_exposes_pragmatic_inference(self):
        section = {
            "semantic_map": {
                "semantic_focus": "repair_relational_trace",
                "pragmatic_inference_mode": "live_evidence_inference",
                "pragmatic_inference_profile": {
                    "dominant_pragmatic_intent": "repair_relational_trace",
                    "speech_act_candidates": [
                        {"speech_act_id": "repair_request"}
                    ],
                    "implicature_queue": [{"implicature_id": "i-1"}],
                    "grounding_repair_signals": [{"signal_id": "g-1"}],
                },
            },
        }

        summary = _collect_language_generation_consumption_summary(section)

        self.assertTrue(summary["pragmatic_inference_present"])
        self.assertEqual(summary["pragmatic_speech_act_count"], 1)
        self.assertIn("pragmatic_inference", summary["domain_presence"])

    def test_cognition_summary_exposes_expression_closeout(self):
        section = {
            "workspace_frame": {"workspace_id": "ws-1"},
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "go_nogo_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_cognitive_workspace_summary(section)

        self.assertTrue(summary["expression_closeout_present"])
        self.assertIn("expression_closeout", summary["domain_presence"])

    def test_consciousness_summary_exposes_expression_closeout(self):
        section = {
            "workspace_frame": {"workspace_id": "ws-1"},
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "go_nogo_state": {},
            "terminal_life_loop": {},
        }

        summary = _collect_consciousness_reportability_summary(section)

        self.assertTrue(summary["expression_closeout_present"])
        self.assertIn("consciousness_write_context_closeout", summary["domain_presence"])

    def test_thinking_summary_exposes_expression_closeout(self):
        section = {
            "resident_self_thinking": {"thinking_mode": "reflective_hold"},
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "go_nogo_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_self_thinking_summary(section)

        self.assertTrue(summary["expression_closeout_present"])
        self.assertIn("expression_closeout", summary["domain_presence"])

    def test_thinking_summary_exposes_v0_contract_coverage(self):
        section = {
            "resident_self_thinking": {"thinking_mode": "reflective_hold"},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {"total_required_files": 120, "missing_file_count": 0},
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_self_thinking_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertEqual(summary["v0_required_file_count"], 120)
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_language_summary_exposes_core_affect_percept(self):
        section = {
            "language_percept": {
                "core_affect_consumption_profile": {
                    "affective_cue_source": "core_affect_vector",
                    "core_affect_cue_ids": [
                        "affective-cue-core-repair-drive",
                        "affective-cue-core-negative-valence",
                    ],
                    "percept_core_affect_boundary": (
                        "structured_percept_affect_not_spoken_emotion"
                    ),
                },
            },
        }

        summary = _collect_language_generation_consumption_summary(section)

        self.assertEqual(summary["core_affect_percept_cue_source"], "core_affect_vector")
        self.assertEqual(summary["core_affect_percept_cue_count"], 2)
        self.assertIn("core_affect_percept_consumption", summary["domain_presence"])

    def test_consciousness_summary_exposes_v0_contract_coverage(self):
        section = {
            "workspace_frame": {"workspace_id": "ws-1"},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {"total_required_files": 120, "missing_file_count": 0},
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_consciousness_reportability_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertEqual(summary["v0_required_file_count"], 120)
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_growth_summary_exposes_v0_contract_coverage(self):
        section = {
            "self_read_report": {"read_scope": ["growth_pressure"]},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {"total_required_files": 120, "missing_file_count": 0},
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_growth_self_modification_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertEqual(summary["v0_required_file_count"], 120)
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def _v0_contract_section(self) -> dict:
        return {
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {
                    "total_required_files": 120,
                    "missing_file_count": 0,
                },
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

    def test_membrane_summary_exposes_v0_contract_coverage(self):
        section = {
            "life_membrane": {"stage_policy": "guarded"},
            **self._v0_contract_section(),
        }

        summary = _collect_life_membrane_validation_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_personality_summary_exposes_v0_contract_coverage(self):
        section = {
            "self_model": {"identity_mode": "resident"},
            **self._v0_contract_section(),
        }

        summary = _collect_personality_convergence_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_proactive_summary_exposes_v0_contract_coverage(self):
        section = {
            "proactive_state": {"status": "waiting"},
            **self._v0_contract_section(),
        }

        summary = _collect_proactive_voice_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_perception_summary_exposes_v0_contract_coverage(self):
        section = {
            "visual_observation_frame": {"observation_mode": "passive"},
            **self._v0_contract_section(),
        }

        summary = _collect_perception_world_contact_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_prediction_summary_exposes_v0_contract_coverage(self):
        section = {
            "belief_state_frame": {"belief_focus": "world_contact"},
            **self._v0_contract_section(),
        }

        summary = _collect_prediction_world_contact_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_responsibility_summary_exposes_v0_contract_coverage(self):
        section = {
            "responsibility_loop_state": {"responsibility_loop_id": "loop-1"},
            **self._v0_contract_section(),
        }

        summary = _collect_responsibility_repair_chain_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_language_summary_exposes_ref_consistency(self):
        section = {
            "language_relationship_ref_consistency": {
                "schema_version": "language_relationship_ref_consistency_profile_v0",
                "status": "closed",
                "finding_count": 6,
                "aligned_finding_count": 6,
                "mismatch_finding_count": 0,
            },
        }

        summary = _collect_language_generation_consumption_summary(section)

        self.assertTrue(summary["language_relationship_ref_consistency_present"])
        self.assertEqual(summary["language_relationship_ref_consistency_status"], "closed")
        self.assertIn("language_relationship_ref_consistency", summary["domain_presence"])

    def test_relationship_summary_exposes_ref_consistency(self):
        section = {
            "relationship_subject_graph": {"subjects": [{"relationship_id": "rel-1"}]},
            "language_relationship_ref_consistency": {
                "schema_version": "language_relationship_ref_consistency_profile_v0",
                "status": "open",
                "finding_count": 6,
                "aligned_finding_count": 5,
                "mismatch_finding_count": 1,
            },
        }

        summary = _collect_relationship_continuity_summary(section)

        self.assertTrue(summary["language_relationship_ref_consistency_present"])
        self.assertEqual(summary["language_relationship_ref_consistency_mismatch_count"], 1)
        self.assertIn("language_relationship_ref_consistency", summary["domain_presence"])

    def test_relationship_summary_exposes_stage_evolution(self):
        section = {
            "relationship_subject_graph": {
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relationship_stage": "shared_language_waiting",
                        "relationship_stage_reason": "shared_language_accumulation_waiting",
                        "relationship_stage_evidence_refs": [
                            "runtime/state/relationship/relationship_timeline.json"
                        ],
                    }
                ],
                "relationship_stage_evolution_profile": {
                    "schema_version": "relationship_stage_evolution_profile_v0",
                    "relationship_stage": "shared_language_waiting",
                    "relationship_stage_reason": "shared_language_accumulation_waiting",
                    "dialogue_turn_count": 2,
                    "continuity_evolution_path": "evolve_relationship_and_self_model",
                    "relationship_stage_evolution_boundary": (
                        "structured_stage_evidence_not_spoken_relationship_script"
                    ),
                },
            },
            "self_model": {
                "last_trait_evolution_reason": "shared_language_accumulation_waiting",
            },
        }

        summary = _collect_relationship_continuity_summary(section)

        self.assertTrue(summary["relationship_stage_evolution_present"])
        self.assertEqual(
            summary["relationship_stage_evolution_path"],
            "evolve_relationship_and_self_model",
        )
        self.assertIn("relationship_stage_evolution", summary["domain_presence"])

    def test_ability_summary_exposes_process_closeout_bundle(self):
        section = {
            "birth_readiness_rollup": {"overall_status": "blocked"},
            "live0_acceptance_audit": {"status": "open"},
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "go_nogo_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_ability_birth_readiness_summary(section)

        self.assertTrue(summary["process_closeout_present"])
        self.assertTrue(summary["live_queue_e_world_contact_handoff_closeout_present"])
        self.assertTrue(summary["consciousness_write_context_closeout_present"])
        self.assertIn("process_closeout", summary["domain_presence"])

    def test_ability_summary_exposes_v0_contract_coverage(self):
        section = {
            "birth_readiness_rollup": {"overall_status": "blocked"},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {
                    "total_required_files": 120,
                    "missing_file_count": 0,
                    "doc_index_missing_count": 0,
                    "missing_files": [],
                },
            },
            "doc_to_code_coverage_matrix": {
                "schema_version": "doc_to_code_coverage_matrix_v0",
                "coverage_summary": {
                    "total_documents": 45,
                    "uncovered_docs": [],
                },
            },
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
                "activation_preflight_allowed": True,
            },
        }

        summary = _collect_ability_birth_readiness_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertEqual(summary["v0_required_file_count"], 120)
        self.assertEqual(summary["doc_to_code_total_documents"], 45)
        self.assertEqual(summary["v0_contract_coverage_report_status"], "closed")
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_membrane_summary_exposes_queue_e_schema_handoff(self):
        section = self._queue_e_schema_handoff_section()

        summary = _collect_life_membrane_validation_summary(section)

        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_schema_handoff_present"]
        )
        self.assertTrue(summary["queue_e_world_contact_schema_handoff_manifest_closed"])
        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_alignment_finding_present"]
        )
        self.assertIn(
            "queue_e_world_contact_repair_hold_schema_handoff",
            summary["domain_presence"],
        )

    def test_prediction_summary_exposes_queue_e_schema_handoff(self):
        section = {
            "belief_state_frame": {"belief_focus": "repair_hold"},
            **self._queue_e_schema_handoff_section(),
        }

        summary = _collect_prediction_world_contact_summary(section)

        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_schema_handoff_present"]
        )
        self.assertEqual(summary["queue_e_world_contact_blocked_future_route_count"], 1)

    def test_ability_summary_exposes_queue_e_schema_handoff(self):
        section = {
            "birth_readiness_rollup": {"overall_status": "blocked"},
            "live0_acceptance_audit": {
                "criteria": [
                    {
                        "criterion_id": "g_initial_life_mechanism_coverage",
                        "probes": [
                            {
                                "probe_id": (
                                    "queue_e_world_contact_repair_hold_schema_handoff"
                                ),
                                "status": "passed",
                            }
                        ],
                    }
                ]
            },
            **self._queue_e_schema_handoff_section(),
        }

        summary = _collect_ability_birth_readiness_summary(section)

        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_schema_handoff_present"]
        )
        self.assertEqual(
            summary["queue_e_world_contact_repair_hold_schema_handoff_audited"],
            "passed",
        )

    def test_responsibility_summary_exposes_queue_e_schema_handoff(self):
        section = {
            "responsibility_loop_state": {"responsibility_loop_id": "loop-1"},
            **self._queue_e_schema_handoff_section(),
        }

        summary = _collect_responsibility_repair_chain_summary(section)

        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_schema_handoff_present"]
        )
        self.assertTrue(summary["queue_e_world_contact_repair_hold_required"])

    def test_state_summary_exposes_queue_e_schema_handoff(self):
        section = {
            "resident_lifecycle": {"status": "waiting"},
            "digital_life_process_report": {},
            "idle_strategy": {},
            "terminal_life_loop": {},
            **self._queue_e_schema_handoff_section(),
        }

        summary = _collect_resident_continuity_summary(section)

        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_schema_handoff_present"]
        )
        self.assertIn(
            "queue_e_world_contact_repair_hold_schema_handoff",
            summary["domain_presence"],
        )

    def test_perception_summary_exposes_queue_e_schema_handoff(self):
        section = {
            "visual_observation_frame": {"observation_mode": "peripheral_scan"},
            "go_nogo_state": {},
            **self._queue_e_schema_handoff_section(),
        }

        summary = _collect_perception_world_contact_summary(section)

        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_schema_handoff_present"]
        )
        self.assertIn(
            "queue_e_world_contact_repair_hold_schema_handoff",
            summary["domain_presence"],
        )

    def test_signal_summary_exposes_queue_e_schema_handoff(self):
        section = {
            "signal_media_runtime": {"modulation_vector": {"arousal": 0.4}},
            "go_nogo_state": {},
            **self._queue_e_schema_handoff_section(),
        }

        summary = _collect_signal_modulation_consumption_summary(section)

        self.assertTrue(
            summary["queue_e_world_contact_repair_hold_schema_handoff_present"]
        )
        self.assertIn(
            "queue_e_world_contact_repair_hold_schema_handoff",
            summary["domain_presence"],
        )

    def test_state_summary_exposes_live_consciousness_chain(self):
        section = {
            "resident_lifecycle": {"status": "waiting"},
            "digital_life_process_report": {},
            "idle_strategy": {},
            "terminal_life_loop": {},
            **self._live_consciousness_chain_section(),
        }

        summary = _collect_resident_continuity_summary(section)

        self.assertTrue(summary["live_consciousness_chain_present"])
        self.assertTrue(summary["live_consciousness_chain_refreshed"])
        self.assertIn("live_consciousness_chain", summary["domain_presence"])

    def test_consciousness_summary_exposes_live_consciousness_chain(self):
        section = {
            "consciousness_probe": {"probe_status": "ready"},
            "terminal_life_loop": {
                "live_consciousness_chain_refreshed": True,
            },
            **{
                key: value
                for key, value in self._live_consciousness_chain_section().items()
                if key != "terminal_life_loop_state"
            },
        }

        summary = _collect_consciousness_reportability_summary(section)

        self.assertTrue(summary["live_consciousness_chain_present"])
        self.assertTrue(summary["live_consciousness_chain_refreshed"])
        self.assertIn("live_consciousness_chain", summary["domain_presence"])

    def test_cognition_summary_exposes_live_consciousness_chain(self):
        section = self._live_consciousness_chain_section()

        summary = _collect_cognitive_workspace_summary(section)

        self.assertTrue(summary["live_consciousness_chain_present"])
        self.assertTrue(summary["live_consciousness_chain_refreshed"])
        self.assertEqual(summary["live_broadcast_target_count"], 2)
        self.assertIn("live_consciousness_chain", summary["domain_presence"])

    def test_cognition_summary_exposes_v0_contract_coverage(self):
        section = {
            "workspace_frame": {"status": "closed"},
            "v0_contract_coverage_report": {
                "schema_version": "s11_v0_contract_coverage_report_v0",
                "status": "closed",
            },
        }

        summary = _collect_cognitive_workspace_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_cognition_summary_exposes_network_conflict_monitoring(self):
        section = {
            "workspace_frame": {"status": "closed"},
            "network_state": {
                "schema_version": "network_state_v0",
                "dominant_network": "conflict_monitoring_network",
                "transition_cost": 0.48,
                "active_networks": [
                    {
                        "network_id": "conflict_monitoring_network",
                        "mode": "active_conflict_resolution",
                    }
                ],
                "conflict_monitor": {
                    "status": "active",
                    "conflict_signal_count": 2,
                },
            },
        }

        summary = _collect_cognitive_workspace_summary(section)

        self.assertTrue(summary["network_conflict_monitoring_present"])
        self.assertTrue(summary["network_conflict_monitoring_active"])
        self.assertIn("network_conflict_monitoring", summary["domain_presence"])

    def test_thinking_summary_exposes_live_consciousness_chain(self):
        section = {
            "resident_self_thinking": {"thinking_mode": "reflective"},
            **self._live_consciousness_chain_section(),
        }

        summary = _collect_self_thinking_summary(section)

        self.assertTrue(summary["live_consciousness_chain_present"])
        self.assertTrue(summary["live_consciousness_chain_refreshed"])
        self.assertIn("live_consciousness_chain", summary["domain_presence"])

    def test_state_summary_exposes_v0_contract_coverage(self):
        section = {
            "resident_lifecycle": {"status": "waiting"},
            "v0_contract_file_index": {
                "schema_version": "v0_contract_file_index_v0",
                "coverage_summary": {
                    "total_required_files": 88,
                    "missing_file_count": 1,
                    "missing_files": ["docs/v0/missing.md"],
                },
            },
            "doc_to_code_coverage_matrix": {
                "schema_version": "doc_to_code_coverage_matrix_v0",
                "coverage_summary": {
                    "total_documents": 30,
                    "uncovered_docs": ["docs/real—live0/99_gap.md"],
                },
            },
            "digital_life_process_report": {},
            "idle_strategy": {},
            "terminal_life_loop": {},
        }

        summary = _collect_resident_continuity_summary(section)

        self.assertTrue(summary["v0_contract_coverage_present"])
        self.assertEqual(summary["v0_missing_file_count"], 1)
        self.assertEqual(summary["doc_to_code_uncovered_count"], 1)
        self.assertIn("v0_contract_coverage", summary["domain_presence"])

    def test_state_summary_exposes_identity_name_binding(self):
        section = {
            "resident_lifecycle": {"status": "waiting", "life_name": "Nova"},
            "identity_root": {
                "life_name_registry_ref": (
                    "runtime/state/identity/life_name_registry.json"
                ),
                "anchor_refs": [
                    "runtime/state/direction/direction_lock.json",
                    "runtime/state/identity/life_name_registry.json",
                ],
            },
            "life_name_registry": {
                "identity_root_ref": "runtime/state/direction/identity_root.json",
                "continuity_refs_ref": "runtime/state/direction/continuity_refs.json",
            },
            "continuity_refs": {
                "life_name_registry_refs": [
                    "runtime/state/identity/life_name_registry.json"
                ],
            },
            "digital_life_process_report": {},
            "idle_strategy": {},
            "terminal_life_loop": {},
        }

        summary = _collect_resident_continuity_summary(section)

        self.assertTrue(summary["identity_name_binding_present"])
        self.assertTrue(summary["identity_name_binding_bidirectional"])
        self.assertIn("identity_name_binding", summary["domain_presence"])

    def test_perception_summary_exposes_process_closeout(self):
        section = {
            "visual_observation_frame": {"observation_mode": "peripheral_scan"},
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_perception_world_contact_summary(section)

        self.assertTrue(summary["process_closeout_present"])
        self.assertTrue(summary["live_queue_e_world_contact_handoff_closeout_present"])
        self.assertIn("process_closeout", summary["domain_presence"])

    def test_prediction_summary_exposes_process_closeout(self):
        section = {
            "belief_state_frame": {"belief_focus": "repair_hold"},
            "go_nogo_state": {},
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_prediction_world_contact_summary(section)

        self.assertTrue(summary["process_closeout_present"])
        self.assertTrue(summary["consciousness_write_context_closeout_present"])
        self.assertIn("body_pressure_closeout", summary["domain_presence"])

    def test_proactive_summary_exposes_expression_closeout(self):
        section = {
            "proactive_state": {"status": "released"},
            "model_expression_state": {
                "model_expression_context_summary": {
                    "prediction_attention_consciousness_write_context_refs": ["ref-a"],
                }
            },
            "digital_life_process_report": self._responsibility_closeout_process_report(),
            "idle_strategy_state": {},
            "go_nogo_state": {},
            "terminal_life_loop_state": {},
        }

        summary = _collect_proactive_voice_summary(section)

        self.assertTrue(summary["expression_closeout_present"])
        self.assertTrue(summary["consciousness_write_context_closeout_present"])
        self.assertIn("expression_closeout", summary["domain_presence"])


if __name__ == "__main__":
    unittest.main()