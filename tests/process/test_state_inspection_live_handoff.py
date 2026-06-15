import unittest

from life_v0.process_supervisor.state_inspection import (
    _collect_life_membrane_validation_summary,
    _collect_prediction_world_contact_summary,
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


if __name__ == "__main__":
    unittest.main()