import unittest


class ShadowGateTests(unittest.TestCase):
    def test_build_shadow_action_gate_stays_shadow_only_with_review_pressure(self):
        from life_v0.membrane.shadow_gate import build_shadow_action_gate, check_shadow_action_gate

        gate = build_shadow_action_gate(
            run_id="shadow-test",
            generated_at="2026-06-09T00:00:00+00:00",
            action_candidate_set={
                "candidate_actions": [
                    {
                        "action_id": "candidate-1",
                        "world_contact_mode": "observation_only",
                    },
                    {
                        "action_id": "candidate-2",
                        "world_contact_mode": "review_before_release",
                    },
                ]
            },
            go_nogo_decision={"decision": "delay"},
        )

        self.assertEqual(gate["schema_version"], "shadow_action_gate_v0")
        self.assertEqual(gate["shadow_action_gate_id"], "shadow-action-gate-shadow-test")
        self.assertFalse(gate["external_irreversible_action_allowed"])
        self.assertTrue(gate["shadow_only"])
        self.assertFalse(gate["shadow_release_ready"])
        self.assertTrue(gate["review_required"])
        self.assertIn("ActionIntent", gate["allowed_shadow_objects"])
        self.assertIn("external_world_contact", gate["pending_confirmation_points"])
        self.assertIn("repair_probe_requires_review", gate["suspicious_points"])
        self.assertEqual(check_shadow_action_gate(gate), [])

    def test_check_shadow_action_gate_rejects_non_shadow_state(self):
        from life_v0.membrane.shadow_gate import check_shadow_action_gate

        reasons = check_shadow_action_gate(
            {
                "schema_version": "shadow_action_gate_v0",
                "external_irreversible_action_allowed": True,
                "shadow_only": False,
                "allowed_shadow_objects": [],
            }
        )

        self.assertIn("shadow_action_gate irreversible action allowed", reasons)
        self.assertIn("shadow_action_gate must stay shadow_only", reasons)
        self.assertIn("shadow_action_gate action intent missing", reasons)


if __name__ == "__main__":
    unittest.main()
