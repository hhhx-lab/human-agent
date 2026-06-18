from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from life_v0.body.body_integrator import (
    BODY_INTEGRATOR_SCHEMA,
    build_body_integrator_state,
    integrate_body_state,
    is_body_integrate_enabled,
    maybe_run_body_integrate_hook,
    project_core_affect_from_integrator,
)


class BodyIntegratorTests(unittest.TestCase):
    def test_disabled_by_default(self):
        self.assertFalse(is_body_integrate_enabled({}))

    def test_integrate_advances_tick_counter(self):
        seed = build_body_integrator_state(
            run_id="tick-test",
            generated_at="2026-06-17T00:00:00Z",
        )
        updated = integrate_body_state(
            integrator=seed,
            generated_at="2026-06-17T00:00:30Z",
            mode="background",
            dt_ms=30_000,
        )
        self.assertEqual(updated["phase"]["tick_counter"], 1)
        self.assertEqual(updated["schema_version"], BODY_INTEGRATOR_SCHEMA)

    def test_debt_monotonic_without_recovery(self):
        seed = build_body_integrator_state(
            run_id="debt-test",
            generated_at="2026-06-17T00:00:00Z",
        )
        first = integrate_body_state(
            integrator=seed,
            generated_at="2026-06-17T00:01:00Z",
            mode="background",
            dt_ms=60_000,
            dialogue_turn=False,
            recovery_event=False,
        )
        second = integrate_body_state(
            integrator=first,
            generated_at="2026-06-17T00:02:00Z",
            mode="background",
            dt_ms=60_000,
            dialogue_turn=False,
            recovery_event=False,
        )
        self.assertGreaterEqual(
            second["continuous"]["body_state_debt"],
            first["continuous"]["body_state_debt"],
        )

    def test_recovery_reduces_pressure_and_debt(self):
        seed = build_body_integrator_state(
            run_id="recovery-test",
            generated_at="2026-06-17T00:00:00Z",
        )
        stressed = integrate_body_state(
            integrator=seed,
            generated_at="2026-06-17T00:10:00Z",
            mode="background",
            dt_ms=600_000,
            dialogue_turn=True,
        )
        recovered = integrate_body_state(
            integrator=stressed,
            generated_at="2026-06-17T00:20:00Z",
            mode="background",
            dt_ms=600_000,
            recovery_event=True,
        )
        self.assertLess(
            recovered["continuous"]["sleep_pressure"],
            stressed["continuous"]["sleep_pressure"],
        )
        self.assertLessEqual(
            recovered["continuous"]["body_state_debt"],
            stressed["continuous"]["body_state_debt"],
        )

    def test_core_affect_tracks_integrator_not_only_event_count(self):
        integrator = integrate_body_state(
            integrator=build_body_integrator_state(
                run_id="affect-test",
                generated_at="2026-06-17T00:00:00Z",
            ),
            generated_at="2026-06-17T00:30:00Z",
            mode="foreground",
            dt_ms=1_800_000,
            dialogue_turn=True,
        )
        low_load = project_core_affect_from_integrator(
            core_affect_vector={},
            integrator=integrator,
            life_state={"pain_events": [], "dream_records": [], "relationship_subjects": [], "responsibility_bindings": []},
            run_id="affect-test",
            generated_at="2026-06-17T00:30:00Z",
        )
        integrator["continuous"]["allostatic_load"] = 0.85
        integrator["continuous"]["body_state_debt"] = 0.7
        high_load = project_core_affect_from_integrator(
            core_affect_vector=low_load,
            integrator=integrator,
            life_state={"pain_events": [], "dream_records": [], "relationship_subjects": [], "responsibility_bindings": []},
            run_id="affect-test",
            generated_at="2026-06-17T00:31:00Z",
        )
        self.assertLess(high_load["valence"], low_load["valence"])
        self.assertGreater(high_load["pain_pressure"], low_load["pain_pressure"])

    def test_hook_writes_runtime_files_when_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            body_dir = Path(tmp)
            writes: list[str] = []

            def write_json(path: Path, payload: dict) -> None:
                writes.append(path.name)
                path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = maybe_run_body_integrate_hook(
                body_dir=body_dir,
                run_id="hook-test",
                generated_at="2026-06-17T01:00:00Z",
                mode="foreground",
                write_json=write_json,
                dialogue_turn=True,
                environ={"DIGITAL_LIFE_BODY_INTEGRATE": "1"},
            )
            self.assertTrue(result.applied)
            self.assertIn("body_integrator_state.json", writes)
            self.assertIn("core_affect_vector.json", writes)
            self.assertTrue((body_dir / "body_integrator_state.json").exists())

    def test_hook_noop_when_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            body_dir = Path(tmp)
            result = maybe_run_body_integrate_hook(
                body_dir=body_dir,
                run_id="noop-test",
                generated_at="2026-06-17T01:00:00Z",
                mode="background",
                write_json=lambda path, payload: None,
                environ={"DIGITAL_LIFE_BODY_INTEGRATE": "0"},
            )
            self.assertFalse(result.applied)
            self.assertFalse((body_dir / "body_integrator_state.json").exists())


if __name__ == "__main__":
    unittest.main()