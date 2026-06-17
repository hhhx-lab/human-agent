from __future__ import annotations

import unittest

from life_v0.language.pragmatic_inference import _build_pragmatic_inference_profile
from life_v0.language.repair_closeout_chain import (
    advance_repair_closeout_on_confirmation,
    build_repair_closeout_state,
    project_apology_repair_trace_for_closeout,
    repair_closeout_allows_repair_focus,
)
from life_v0.process_supervisor.continuity_evolution import _derive_relationship_stage
from life_v0.process_supervisor.idle_strategy import _resident_governance_language_priority
from life_v0.process_supervisor.resident_turn_writeback import (
    _align_memory_retrieval_focus_with_live_turn,
)


class RepairCloseoutChainTests(unittest.TestCase):
    def test_confirmation_advances_closeout_toward_dormant(self):
        state = build_repair_closeout_state(
            run_id="closeout-test",
            generated_at="2026-06-17T00:00:00Z",
            commitment_truth_state={"repair_required_refs": ["repair-1"]},
        )
        self.assertEqual(state["closeout_phase"], "active_repair")
        advanced = advance_repair_closeout_on_confirmation(
            state,
            run_id="closeout-test",
            generated_at="2026-06-17T00:01:00Z",
            feedback_event_type="confirmation",
        )
        self.assertEqual(advanced["closeout_phase"], "awaiting_confirmation")
        advanced = advance_repair_closeout_on_confirmation(
            advanced,
            run_id="closeout-test",
            generated_at="2026-06-17T00:02:00Z",
            feedback_event_type="confirmation",
        )
        self.assertIn(
            advanced["closeout_phase"],
            {"confirmed", "dormant"},
        )

    def test_dormant_closeout_blocks_repair_semantic_focus(self):
        profile = _build_pragmatic_inference_profile(
            language_percept={
                "incoming_surface": "你还记得我们上次聊什么吗？",
                "utterance_signal_profile": {
                    "repair_request": False,
                    "apology": False,
                },
                "repair_trigger_candidates": ["repair-language-v0-0001"],
                "semantic_focus": "repair_relational_trace",
            },
            relationship_timeline={
                "relationship_continuity_reports": [
                    {"continuity_state": "repair_guarded_continuity"}
                ]
            },
            commitment_truth_state={"repair_required_refs": ["repair-1"]},
            context_accumulation={},
            relation_scope_index={},
            shared_term_registry={},
            relationship_stage="repair_guarded_continuity",
            repair_closeout_state={"closeout_phase": "dormant"},
            generated_at="2026-06-17T00:00:00Z",
        )
        self.assertEqual(profile["dominant_pragmatic_intent"], "relational_checkin")

    def test_align_memory_focus_decouples_repair_stain_when_dormant(self):
        aligned = _align_memory_retrieval_focus_with_live_turn(
            {
                "reconstruction_inputs": {
                    "reconstruction_focus": "relationship_continuity_reconstruction",
                }
            },
            semantic_map={"semantic_focus": "repair_relational_trace"},
            live_turn_focus="repair_relational_trace",
            repair_closeout_state={"closeout_phase": "dormant"},
        )
        self.assertEqual(aligned["live_semantic_focus"], "relational_checkin")
        self.assertEqual(
            aligned["reconstruction_focus"],
            "relationship_continuity_reconstruction",
        )

    def test_closeout_confirmed_advances_relationship_stage(self):
        stage, reason = _derive_relationship_stage(
            current_stage="repair_guarded_continuity",
            dialogue_turn_count=4,
            continuity_state="repair_guarded_continuity",
            trust_state="calibrated",
            queue_e_signal_profile={
                "repair_followup_required": True,
                "queue_e_priority_band": "repair_guarded",
                "world_contact_release_posture": "shadow_only_guarded",
            },
            offline_learning_profile={
                "offline_learning_pressure_level": "quiet"
            },
            background_continuity_profile={},
            growth_self_modification_presence={},
            repair_closeout_state={"closeout_phase": "confirmed"},
        )
        self.assertEqual(stage, "active_dialogue")
        self.assertIn("repair_closeout", reason)

    def test_idle_governance_demotes_apology_attention_when_dormant(self):
        target, reason, cadence, _profile = _resident_governance_language_priority(
            relationship_timeline_ref="runtime/state/relationship/relationship_timeline.json",
            commitment_expression_plan_ref=None,
            apology_repair_language_trace_ref=(
                "runtime/state/language/apology_repair_language_trace.json"
            ),
            apology_repair_language_trace={
                "repair_window_mode": "dormant",
                "queue_e_repair_pressure_level": "baseline",
            },
            repair_closeout_phase="dormant",
            offline_pressure_level="present",
            need_state_vector={"repair_drive": "active"},
            body_waiting_posture="low_bandwidth_guarded",
            world_contact_release_posture="shadow_only_guarded",
            repair_followup_required=True,
            repair_obligation_count=2,
            regret_pressure_count=1,
            queue_e_priority_band="repair_guarded",
            background_carryover_attention_target=None,
            background_carryover_generation=0,
        )
        self.assertNotEqual(target, "apology_repair_language_trace")
        self.assertTrue(reason)

    def test_apology_trace_projected_to_dormant_window(self):
        projected = project_apology_repair_trace_for_closeout(
            {
                "schema_version": "apology_repair_language_trace_v0",
                "repair_window_mode": "guarded_repair_hold",
                "queue_e_repair_pressure_level": "elevated",
            },
            closeout_state={"closeout_phase": "dormant"},
            generated_at="2026-06-17T00:00:00Z",
        )
        self.assertEqual(projected["repair_window_mode"], "dormant")
        self.assertEqual(projected["queue_e_repair_pressure_level"], "baseline")

    def test_repair_focus_allowed_only_in_active_phases(self):
        self.assertTrue(
            repair_closeout_allows_repair_focus({"closeout_phase": "active_repair"})
        )
        self.assertFalse(
            repair_closeout_allows_repair_focus({"closeout_phase": "dormant"})
        )


if __name__ == "__main__":
    unittest.main()