import unittest

from life_v0.process_supervisor.continuity_evolution import (
    evolve_relationship_and_self_model,
)
from life_v0.state_store.slow_variable_candidate import (
    DRAMATIC_DELTA_THRESHOLD,
    project_trait_slow_variables_with_candidate_gate,
)


class SlowVariableCandidateTests(unittest.TestCase):
    def test_blocks_dramatic_single_turn_delta(self):
        previous = {
            "trust_persistence": {
                "value": 0.30,
                "update_count": 2,
                "evidence_refs": ["ref-a"],
            }
        }
        proposed = {
            "trust_persistence": {
                "value": 0.55,
                "update_count": 3,
                "evidence_refs": ["ref-b"],
                "last_relationship_stage": "active_dialogue",
            }
        }
        result = project_trait_slow_variables_with_candidate_gate(
            previous_variables=previous,
            proposed_variables=proposed,
            generated_at="2026-06-15T01:00:00+00:00",
            relationship_stage="active_dialogue",
            evidence_refs=["ref-b"],
        )

        committed = result["trait_slow_variables"]["trust_persistence"]
        self.assertLess(
            abs(committed["value"] - 0.30),
            DRAMATIC_DELTA_THRESHOLD,
        )
        self.assertEqual(
            committed["slow_variable_update_mode"],
            "candidate_gated_incremental_commit",
        )
        candidates = result["trait_slow_variable_candidates"]["candidates"]
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["promotion_gate_status"], "blocked_dramatic_single_turn")
        self.assertTrue(result["blocked_update_refs"])

    def test_promotes_after_multi_window_exposure(self):
        previous = {
            "repair_seriousness": {
                "value": 0.28,
                "update_count": 4,
            }
        }
        proposed = {
            "repair_seriousness": {
                "value": 0.52,
                "update_count": 5,
                "evidence_refs": ["ref-c"],
            }
        }
        previous_candidates = {
            "candidates": [
                {
                    "candidate_id": "slow-variable-candidate-repair_seriousness",
                    "variable_name": "repair_seriousness",
                    "exposure_count": 1,
                    "first_seen_at": "2026-06-14T00:00:00+00:00",
                }
            ]
        }
        result = project_trait_slow_variables_with_candidate_gate(
            previous_variables=previous,
            proposed_variables=proposed,
            previous_candidates=previous_candidates,
            generated_at="2026-06-15T02:00:00+00:00",
            relationship_stage="repair_guarded_continuity",
            evidence_refs=["ref-c"],
        )

        committed = result["trait_slow_variables"]["repair_seriousness"]
        self.assertEqual(committed["value"], 0.52)
        self.assertEqual(
            committed["slow_variable_update_mode"],
            "candidate_promoted_multi_window",
        )
        self.assertEqual(result["trait_slow_variable_candidates"]["candidates"], [])

    def test_continuity_evolution_writes_candidate_queue(self):
        baseline = evolve_relationship_and_self_model(
            generated_at="2026-06-15T00:00:00+00:00",
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "rel-1",
                        "relation_role": "friend",
                        "relationship_stage": "pre_activation",
                        "relationship_stage_turn_count": 0,
                    }
                ]
            },
            self_model_state={
                "trait_slow_variables": {
                    "trust_persistence": {"value": 0.20, "update_count": 1},
                    "dialogue_warmth": {"value": 0.20, "update_count": 1},
                    "repair_seriousness": {"value": 0.20, "update_count": 1},
                    "boundary_respect": {"value": 0.20, "update_count": 1},
                    "continuity_drive": {"value": 0.20, "update_count": 1},
                }
            },
            relationship_timeline={
                "relationship_continuity_reports": [{"continuity_state": "seeded"}],
                "trust_trajectories": [{"current_trust_state": "calibrated_medium"}],
                "dialogue_turn_refs": ["turn-1", "turn-2", "turn-3", "turn-4"],
            },
            commitment_expression_plan={
                "queue_e_repair_pressure_level": "urgent",
            },
            apology_repair_language_trace={
                "repair_language_moves": [{"move_type": "repair_followup"}],
            },
            responsibility_loop_state={
                "repair_followup_required": True,
                "repair_obligation_refs": ["obligation-1", "obligation-2"],
                "regret_pressure_candidates": [{"ref": "regret-1"}],
            },
            world_contact_summary={"release_posture": "confirmation_blocked"},
            pain_regret_repair_report={"repair_followup_required": True},
            nightmare_risk=None,
            belief_learning_plan=None,
            language_learning_plan=None,
            relationship_learning_plan=None,
            background_continuity_profile={},
        )
        self_model = baseline["self_model_state"]
        self.assertIn("trait_slow_variable_candidates", self_model)
        candidate_queue = self_model["trait_slow_variable_candidates"]
        self.assertEqual(
            candidate_queue.get("schema_version"),
            "self_model_slow_variable_candidate_queue_v0",
        )