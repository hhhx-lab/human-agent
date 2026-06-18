from __future__ import annotations

import unittest

from life_v0.dynamics.parameter_registry import BLOCKED_PATCH_TARGET_REFS
from life_v0.growth.patch_queue import (
    INTEGRATOR_PARAMETER_PATCH_FAMILY,
    build_integrator_parameter_patch_candidate,
    compare_integrator_parameter_patch_shadow,
    is_integrator_parameter_patch_enabled,
    maybe_append_integrator_parameter_patch_candidate,
    validate_integrator_parameter_patch_candidate,
)
from life_v0.replay import extract_integrator_parameter_patch_shadow


class IntegratorParameterPatchTests(unittest.TestCase):
    def test_disabled_by_default(self):
        self.assertFalse(is_integrator_parameter_patch_enabled({}))

    def test_parameter_patch_shadow_only_with_patchable_fields(self):
        candidate = build_integrator_parameter_patch_candidate(
            body_integrator={
                "continuous": {"recovery_rate": 0.08, "stress_pulse": 0.05}
            },
            self_read_report={"growth_pressures": ["pain_recovery_gap"]},
            replay_cue_bundle={},
            run_id="patch-run",
            generated_at="2026-06-17T05:00:00Z",
        )
        self.assertEqual(candidate["patch_kind"], INTEGRATOR_PARAMETER_PATCH_FAMILY)
        self.assertTrue(candidate["shadow_only"])
        self.assertFalse(candidate["identity_or_write_gate_mutation"])
        self.assertIn("recovery_rate", candidate["patch_deltas"])
        self.assertNotIn(
            "runtime/state/direction/identity_root.json",
            candidate.get("target_ref", ""),
        )
        self.assertEqual(validate_integrator_parameter_patch_candidate(candidate), [])

    def test_core_gate_blocks_identity_patch_target(self):
        candidate = build_integrator_parameter_patch_candidate(
            body_integrator={"continuous": {"recovery_rate": 0.08, "stress_pulse": 0.05}},
            self_read_report={"growth_pressures": ["pain_recovery_gap"]},
            replay_cue_bundle={},
            run_id="patch-run",
            generated_at="2026-06-17T05:00:00Z",
        )
        candidate["target_ref"] = BLOCKED_PATCH_TARGET_REFS[0]
        reasons = validate_integrator_parameter_patch_candidate(candidate)
        self.assertTrue(any("blocked target" in reason for reason in reasons))

    def test_maybe_append_adds_candidate_when_enabled(self):
        queue = {
            "schema_version": "growth_patch_candidate_queue_v0",
            "candidates": [{"growth_patch_candidate_id": "base"}],
        }
        updated = maybe_append_integrator_parameter_patch_candidate(
            candidate_queue=queue,
            body_integrator={"continuous": {"recovery_rate": 0.08, "stress_pulse": 0.05}},
            self_read_report={"growth_pressures": ["capability_gap"]},
            replay_cue_bundle={},
            run_id="patch-run",
            generated_at="2026-06-17T05:00:00Z",
            environ={"DIGITAL_LIFE_INTEGRATOR_PARAMETER_PATCH": "true"},
        )
        self.assertTrue(updated.get("integrator_parameter_patch_applied"))
        self.assertEqual(len(updated["candidates"]), 2)

    def test_replay_seed_extracts_integrator_shadow(self):
        shadow = extract_integrator_parameter_patch_shadow(
            {
                "candidates": [
                    {
                        "patch_kind": INTEGRATOR_PARAMETER_PATCH_FAMILY,
                        "growth_patch_candidate_id": "integrator-parameter-patch-x",
                        "patch_deltas": {"recovery_rate": 0.01},
                        "shadow_compare": {
                            "status": "passed",
                            "shadow_apply_boundary": "shadow_compare_only_not_live_integrator_write",
                        },
                    }
                ]
            }
        )
        self.assertIsNotNone(shadow)
        self.assertEqual(shadow["patch_kind"], INTEGRATOR_PARAMETER_PATCH_FAMILY)
        self.assertEqual(shadow["shadow_compare"]["status"], "passed")

    def test_shadow_compare_reports_metric_deltas(self):
        result = compare_integrator_parameter_patch_shadow(
            baseline_continuous={"recovery_rate": 0.08, "stress_pulse": 0.05},
            proposed_continuous={"recovery_rate": 0.09, "stress_pulse": 0.05},
            run_id="shadow-compare",
            generated_at="2026-06-17T06:00:00Z",
            tick_count=8,
            dt_ms=3_600_000,
        )
        self.assertIn(result["status"], {"passed", "marginal", "failed"})
        self.assertIn("sleep_pressure_delta", result)
        self.assertIn("cognitive_bandwidth_delta", result)


if __name__ == "__main__":
    unittest.main()