import unittest

from life_v0.process_supervisor.state_inspection import (
    _collect_dream_wake_fact_summary,
    _collect_personality_convergence_summary,
    _collect_reconstructive_memory_summary,
    _collect_relation_context_summary,
    _collect_relationship_continuity_summary,
)


class StateInspectionMemoryCloseoutTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()