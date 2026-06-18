from __future__ import annotations

import unittest

from life_v0.growth.self_read import build_self_read_report


class SelfReadDynamicsMetricsTests(unittest.TestCase):
    def test_self_read_projects_body_integrator_metrics(self):
        report = build_self_read_report(
            run_id="growth-read",
            generated_at="2026-06-18T08:00:00Z",
            life_state={},
            replay_cue_bundle={},
            growth_route={},
            learning_window={},
            body_integrator={
                "integrator_id": "body-integrator-growth-read",
                "phase": {"tick_counter": 12},
                "continuous": {
                    "sleep_pressure": 0.2,
                    "recovery_rate": 0.08,
                },
            },
        )
        metrics = report.get("dynamics_metrics") or {}
        self.assertEqual(
            metrics.get("body_integrator_ref"),
            "runtime/state/body/body_integrator_state.json",
        )
        self.assertEqual(metrics.get("tick_counter"), 12)
        self.assertEqual(metrics["continuous"]["recovery_rate"], 0.08)


if __name__ == "__main__":
    unittest.main()