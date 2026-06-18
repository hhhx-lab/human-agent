from __future__ import annotations

import math
import unittest

from life_v0.dynamics.accelerated_simulation_audit import run_accelerated_dynamics_audit


class AcceleratedSimulationAuditTests(unittest.TestCase):
    def test_72h_simulation_smoke_passes_without_anomalies(self):
        report = run_accelerated_dynamics_audit(
            run_id="audit-72h",
            generated_at="2026-06-17T08:00:00Z",
            tick_hours=72,
            ticks_per_hour=1,
            recovery_every=8,
        )
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["simulated_hours"], 72)
        self.assertEqual(report["simulated_ticks"], 72)
        self.assertGreaterEqual(report["final_tick_counter"], 72)
        self.assertEqual(report["anomaly_count"], 0)

        continuous = report["final_continuous"]
        for value in continuous.values():
            if isinstance(value, (int, float)):
                self.assertFalse(math.isnan(float(value)))
                self.assertFalse(math.isinf(float(value)))


if __name__ == "__main__":
    unittest.main()