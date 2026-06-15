import unittest

from life_v0.live0_audit.gate_f_inspection import live0_gate_f_inspection_snapshot


class Live0GateFInspectionTests(unittest.TestCase):
    def _valid_world_contact_validation(self) -> dict:
        return {
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
        }

    def test_gate_f_closed_when_validation_and_audit_probes_pass(self):
        snapshot = live0_gate_f_inspection_snapshot(
            world_contact_validation=self._valid_world_contact_validation(),
            process_report={},
            handoff={},
            terminal_loop={},
            live0_audit={
                "criteria": [
                    {
                        "criterion_id": "f_equal_relationship_dialogue_growth",
                        "status": "closed",
                        "probes": [
                            {
                                "probe_id": "queue_e_world_contact_repair_hold_validated",
                                "status": "passed",
                            },
                            {
                                "probe_id": (
                                    "live_queue_e_world_contact_handoff_closeout_audited"
                                ),
                                "status": "passed",
                            },
                        ],
                    }
                ]
            },
        )
        self.assertTrue(snapshot["live0_gate_f_closed"])
        self.assertTrue(snapshot["queue_e_world_contact_repair_hold_validation_closed"])
        self.assertEqual(
            snapshot["queue_e_world_contact_repair_hold_validated_probe_status"],
            "passed",
        )

    def test_gate_f_open_when_validation_missing_repair_hold(self):
        invalid = self._valid_world_contact_validation()
        invalid["repair_hold_required"] = False
        snapshot = live0_gate_f_inspection_snapshot(
            world_contact_validation=invalid,
            process_report={},
            handoff={},
            terminal_loop={},
        )
        self.assertFalse(snapshot["live0_gate_f_closed"])
        self.assertEqual(
            snapshot["queue_e_world_contact_repair_hold_validated_probe_status"],
            "blocked",
        )


if __name__ == "__main__":
    unittest.main()