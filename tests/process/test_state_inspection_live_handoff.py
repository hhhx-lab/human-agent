import unittest

from life_v0.process_supervisor.state_inspection import (
    _collect_ability_birth_readiness_summary,
    _collect_language_generation_consumption_summary,
    _collect_life_membrane_validation_summary,
    _collect_perception_world_contact_summary,
    _collect_prediction_world_contact_summary,
    _collect_signal_modulation_consumption_summary,
)


class StateInspectionLiveHandoffTests(unittest.TestCase):
    def test_membrane_summary_exposes_live_queue_e_handoff_fields(self):
        section = {
            "queue_e_world_contact_handoff": {
                "handoff_status": "deferred_until_s05_s09",
                "live_queue_e_world_contact_handoff_refreshed": True,
                "live_turn_focus": "repair_hold_after_live_turn",
                "handoff_boundary": "structured_handoff_not_spoken_language",
                "live_responsibility_consciousness_context_refs": [
                    "runtime/state/consciousness/workspace_frame.json",
                    "runtime/state/action/responsibility_loop_state.json#consciousness_context_profile",
                ],
            },
            "terminal_life_loop_state": {
                "live_queue_e_world_contact_handoff_refreshed": True,
                "live_queue_e_world_contact_handoff_turn_focus": (
                    "repair_hold_after_live_turn"
                ),
            },
        }

        summary = _collect_life_membrane_validation_summary(section)

        self.assertEqual(
            summary["schema_version"],
            "life_membrane_validation_summary_v0",
        )
        self.assertTrue(summary["live_queue_e_world_contact_handoff_refreshed"])
        self.assertEqual(
            summary["queue_e_world_contact_handoff_status"],
            "deferred_until_s05_s09",
        )
        self.assertEqual(
            summary["live_queue_e_world_contact_handoff_turn_focus"],
            "repair_hold_after_live_turn",
        )
        self.assertEqual(
            summary["live_responsibility_consciousness_context_ref_count"],
            2,
        )
        self.assertIn(
            "live_queue_e_world_contact_handoff",
            summary["domain_presence"],
        )
        self.assertTrue(summary["domain_presence"]["live_queue_e_world_contact_handoff"])

    def test_prediction_summary_exposes_live_queue_e_handoff_fields(self):
        section = {
            "queue_e_world_contact_handoff": {
                "handoff_status": "deferred_until_s05_s09",
                "last_projected_from_live_turn_ref": (
                    "runtime/state/terminal/terminal_life_loop_state.json"
                ),
                "live_turn_focus": "world_contact_repair_hold",
            },
            "terminal_life_loop_state": {
                "resident_background_lineage_state": {
                    "world_contact_handoff_presence": {
                        "live_queue_e_world_contact_handoff_refreshed": True,
                        "live_queue_e_world_contact_handoff_boundary": (
                            "structured_handoff_not_spoken_language"
                        ),
                    }
                }
            },
        }

        summary = _collect_prediction_world_contact_summary(section)

        self.assertEqual(
            summary["schema_version"],
            "prediction_world_contact_summary_v0",
        )
        self.assertTrue(summary["live_queue_e_world_contact_handoff_refreshed"])
        self.assertEqual(
            summary["queue_e_world_contact_handoff_status"],
            "deferred_until_s05_s09",
        )
        self.assertEqual(
            summary["live_queue_e_world_contact_handoff_turn_focus"],
            "world_contact_repair_hold",
        )
        self.assertEqual(
            summary["live_queue_e_world_contact_handoff_boundary"],
            "structured_handoff_not_spoken_language",
        )
        self.assertIn(
            "live_queue_e_world_contact_handoff",
            summary["domain_presence"],
        )


    def test_ability_summary_merges_birth_readiness_and_live_handoff_status(self):
        section = {
            "birth_readiness_rollup": {
                "queue_e_world_contact_handoff_status": "closed",
            },
            "birth_readiness_stage_gate": {},
            "live0_acceptance_audit": {
                "criteria": [
                    {
                        "probes": [
                            {
                                "probe_id": (
                                    "live_queue_e_world_contact_handoff_closeout_audited"
                                ),
                                "status": "passed",
                            }
                        ]
                    }
                ]
            },
            "queue_e_world_contact_handoff": {
                "handoff_status": "deferred_until_s05_s09",
                "live_queue_e_world_contact_handoff_refreshed": True,
            },
            "digital_life_process_report": {
                "live_queue_e_world_contact_handoff_refreshed": True,
                "live_queue_e_world_contact_handoff_report_boundary": (
                    "live_queue_e_world_contact_handoff_structured_report_not_spoken_language"
                ),
            },
        }

        summary = _collect_ability_birth_readiness_summary(section)

        self.assertEqual(summary["queue_e_world_contact_handoff_status"], "closed")
        self.assertTrue(summary["live_queue_e_world_contact_handoff_refreshed"])
        self.assertEqual(
            summary["live_queue_e_world_contact_handoff_closeout_audited"],
            "passed",
        )

    def test_signal_summary_exposes_live_queue_e_handoff_in_repair_consumption(self):
        section = {
            "queue_e_world_contact_handoff": {
                "handoff_status": "deferred_until_s05_s09",
                "live_queue_e_world_contact_handoff_refreshed": True,
                "live_turn_focus": "repair_hold_signal_chain",
                "live_responsibility_consciousness_context_refs": [
                    "runtime/state/consciousness/workspace_frame.json"
                ],
            },
        }

        summary = _collect_signal_modulation_consumption_summary(section)

        self.assertTrue(summary["live_queue_e_world_contact_handoff_refreshed"])
        self.assertEqual(
            summary["responsibility_repair_consumption"][
                "live_queue_e_world_contact_handoff_turn_focus"
            ],
            "repair_hold_signal_chain",
        )
        self.assertIn(
            "live_queue_e_world_contact_handoff",
            summary["domain_presence"],
        )

    def test_language_summary_merges_runtime_and_model_expression_handoff(self):
        section = {
            "model_expression_state": {
                "model_expression_context_summary": {
                    "world_contact_handoff_status": "deferred_until_s05_s09",
                    "world_contact_handoff_live_refreshed": True,
                    "world_contact_handoff_live_turn_focus": "repair_hold_language_chain",
                    "world_contact_handoff_live_responsibility_context_ref_count": 2,
                    "world_contact_handoff_boundary": (
                        "structured_handoff_not_spoken_language"
                    ),
                }
            },
            "queue_e_world_contact_handoff": {
                "live_queue_e_world_contact_handoff_refreshed": True,
            },
        }

        summary = _collect_language_generation_consumption_summary(section)

        self.assertTrue(
            summary["model_expression_world_contact_handoff_live_refreshed"]
        )
        self.assertEqual(
            summary["model_expression_world_contact_handoff_live_turn_focus"],
            "repair_hold_language_chain",
        )
        self.assertTrue(summary["live_queue_e_world_contact_handoff_refreshed"])
        self.assertIn(
            "model_expression_world_contact_handoff",
            summary["domain_presence"],
        )

    def test_perception_summary_exposes_live_queue_e_handoff_fields(self):
        section = {
            "queue_e_world_contact_handoff": {
                "handoff_status": "deferred_until_s05_s09",
                "live_queue_e_world_contact_handoff_refreshed": True,
                "live_turn_focus": "world_contact_repair_hold",
            },
        }

        summary = _collect_perception_world_contact_summary(section)

        self.assertTrue(summary["live_queue_e_world_contact_handoff_refreshed"])
        self.assertEqual(
            summary["live_queue_e_world_contact_handoff_turn_focus"],
            "world_contact_repair_hold",
        )


if __name__ == "__main__":
    unittest.main()