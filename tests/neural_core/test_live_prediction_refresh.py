from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from life_v0.neural_core.active_sampling import build_active_sampling_plan, compute_efe_score
from life_v0.neural_core.live_prediction_refresh import (
    is_prediction_refresh_enabled,
    maybe_run_prediction_refresh_hook,
    project_prediction_stack_from_live_turn,
)
from life_v0.neural_core.prediction_error import refresh_prediction_error_from_live_turn
from life_v0.neural_core.signal_media import refresh_signal_media_from_integrator


class LivePredictionRefreshTests(unittest.TestCase):
    def test_disabled_by_default(self):
        self.assertFalse(is_prediction_refresh_enabled({}))

    def test_signal_media_tracks_integrator_scalars(self):
        refreshed = refresh_signal_media_from_integrator(
            signal_media_runtime={
                "schema_version": "signal_media_runtime_v0",
                "modulation_vector": {"unexpected_uncertainty": 0.21},
                "queue_e_repair_pressure_level": "quiet",
            },
            run_id="signal-run",
            generated_at="2026-06-17T01:00:00Z",
            body_integrator={
                "continuous": {
                    "allostatic_load": 0.72,
                    "sleep_pressure": 0.55,
                    "body_state_debt": 0.4,
                    "cognitive_bandwidth": 0.35,
                    "stress_pulse": 0.48,
                }
            },
            core_affect_vector={"arousal": 0.4},
            body_resource_budget={"fatigue_state": {"level": "high"}},
            network_state={"network_id": "net-1"},
        )
        self.assertTrue(refreshed["live_refresh_applied"])
        self.assertGreater(
            refreshed["modulation_vector"]["unexpected_uncertainty"],
            0.21,
        )
        self.assertEqual(refreshed["queue_e_repair_pressure_level"], "quiet")

    def test_prediction_error_changes_between_turns(self):
        shared = {
            "belief_state": {"active_life_targets": ["real_life"]},
            "signal_media_runtime": {
                "modulation_vector": {"unexpected_uncertainty": 0.3},
            },
            "language_percept": {"ambiguity_flags": []},
            "semantic_map": {"semantic_focus": "greeting", "ambiguity_queue": []},
            "body_integrator": {"continuous": {"allostatic_load": 0.2, "cognitive_bandwidth": 0.8}},
        }
        turn_one = refresh_prediction_error_from_live_turn(
            prediction_error_field=None,
            run_id="err-run",
            generated_at="2026-06-17T01:00:00Z",
            turn_counter=1,
            **shared,
        )
        turn_two = refresh_prediction_error_from_live_turn(
            prediction_error_field=turn_one,
            run_id="err-run",
            generated_at="2026-06-17T01:01:00Z",
            turn_counter=2,
            language_percept={"ambiguity_flags": ["term_unresolved", "scope_unclear"]},
            semantic_map={
                "semantic_focus": "clarification_request",
                "ambiguity_queue": ["clarification_requested", "term_unresolved"],
            },
            belief_state=shared["belief_state"],
            signal_media_runtime=shared["signal_media_runtime"],
            body_integrator=shared["body_integrator"],
        )
        self.assertNotEqual(
            turn_one["error_events"][-1]["error_id"],
            turn_two["error_events"][-1]["error_id"],
        )
        self.assertGreater(turn_two["live_ambiguity_count"], turn_one["live_ambiguity_count"])
        self.assertGreater(
            turn_two["error_events"][-1]["magnitude"],
            turn_one["error_events"][-1]["magnitude"],
        )

    def test_high_ambiguity_routes_to_clarify(self):
        plan = build_active_sampling_plan(
            run_id="sampling-run",
            generated_at="2026-06-17T01:00:00Z",
            belief_state={"state_scope": "relation"},
            prediction_error_field={"error_events": [], "stage_effect": "hold_for_evidence"},
            semantic_map={"ambiguity_queue": ["clarification_requested", "term_unresolved"]},
            body_integrator={"continuous": {"cognitive_bandwidth": 0.4}},
            turn_counter=3,
        )
        self.assertEqual(plan["selected_route"], "clarify_ambiguity")
        self.assertIn("efe_score", plan)
        self.assertGreater(plan["efe_score"], 0.0)

    def test_efe_score_rises_with_ambiguity_and_low_bandwidth(self):
        low = compute_efe_score(
            signal_media_runtime={"modulation_vector": {"expected_uncertainty": 0.3, "unexpected_uncertainty": 0.2}},
            semantic_map={"ambiguity_queue": []},
            body_integrator={"continuous": {"cognitive_bandwidth": 0.8}},
        )
        high = compute_efe_score(
            signal_media_runtime={"modulation_vector": {"expected_uncertainty": 0.5, "unexpected_uncertainty": 0.4}},
            semantic_map={"ambiguity_queue": ["a", "b"]},
            body_integrator={"continuous": {"cognitive_bandwidth": 0.3}},
            repair_profile={"pressure_level": "elevated"},
        )
        self.assertGreater(high, low)

    def test_project_stack_preserves_queue_e_fields(self):
        repair_profile = {
            "schema_version": "queue_e_repair_modulation_profile_v0",
            "pressure_level": "elevated",
            "attention_target": "repair_followup",
            "ref_set": ["runtime/state/action/responsibility_loop_state.json"],
        }
        result = project_prediction_stack_from_live_turn(
            run_id="stack-run",
            generated_at="2026-06-17T02:00:00Z",
            turn_counter=4,
            signal_media_runtime={
                "schema_version": "signal_media_runtime_v0",
                "queue_e_repair_modulation_profile": repair_profile,
                "queue_e_repair_pressure_level": "elevated",
            },
            belief_state={"active_life_targets": ["real_life"]},
            prediction_error_field={"error_events": []},
            active_sampling_plan={},
            language_percept={"ambiguity_flags": ["scope_unclear"]},
            semantic_map={"ambiguity_queue": ["scope_unclear"]},
            core_affect_vector={},
            body_integrator={"continuous": {"allostatic_load": 0.5, "cognitive_bandwidth": 0.6}},
            body_resource_budget={},
            network_state={},
        )
        self.assertTrue(result.applied)
        self.assertEqual(result.active_sampling_plan["queue_e_repair_pressure_level"], "elevated")
        self.assertEqual(result.active_sampling_plan["selected_route"], "repair_inspect")
        self.assertTrue(result.signal_media_runtime["live_refresh_applied"])
        self.assertTrue(result.belief_state["live_refresh_applied"])
        self.assertTrue(result.prediction_error_field["live_refresh_applied"])

    def test_hook_writes_runtime_files_when_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            (state_dir / "body").mkdir(parents=True)
            (state_dir / "signal").mkdir(parents=True)
            (state_dir / "prediction").mkdir(parents=True)
            (state_dir / "body" / "body_integrator_state.json").write_text(
                json.dumps(
                    {
                        "continuous": {
                            "allostatic_load": 0.4,
                            "sleep_pressure": 0.3,
                            "body_state_debt": 0.2,
                            "cognitive_bandwidth": 0.7,
                            "stress_pulse": 0.2,
                        }
                    }
                ),
                encoding="utf-8",
            )
            writes: list[str] = []

            def write_json(path: Path, payload: dict) -> None:
                writes.append(path.name)
                path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            result = maybe_run_prediction_refresh_hook(
                state_dir=state_dir,
                run_id="hook-run",
                generated_at="2026-06-17T03:00:00Z",
                turn_counter=2,
                signal_media_runtime={"schema_version": "signal_media_runtime_v0"},
                belief_state={"active_life_targets": ["real_life"]},
                prediction_error_field={"error_events": []},
                active_sampling_plan={},
                language_percept={},
                semantic_map={"ambiguity_queue": ["clarify"]},
                core_affect_vector={},
                body_resource_budget={},
                network_state={},
                offline_learning_cumulative_profile=None,
                write_json=write_json,
                environ={"DIGITAL_LIFE_PREDICTION_REFRESH": "1"},
            )
            self.assertTrue(result.applied)
            self.assertIn("signal_media_runtime.json", writes)
            self.assertIn("belief_state_frame.json", writes)
            self.assertIn("prediction_error_field.json", writes)
            self.assertIn("active_sampling_plan.json", writes)
            self.assertTrue((state_dir / "signal" / "signal_media_runtime.json").exists())

    def test_hook_noop_when_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            (state_dir / "signal").mkdir(parents=True)
            result = maybe_run_prediction_refresh_hook(
                state_dir=state_dir,
                run_id="noop-run",
                generated_at="2026-06-17T03:00:00Z",
                turn_counter=1,
                signal_media_runtime={"schema_version": "signal_media_runtime_v0"},
                belief_state={},
                prediction_error_field={},
                active_sampling_plan={},
                language_percept={},
                semantic_map={},
                core_affect_vector={},
                body_resource_budget={},
                network_state={},
                offline_learning_cumulative_profile=None,
                write_json=lambda path, payload: None,
                environ={"DIGITAL_LIFE_PREDICTION_REFRESH": "0"},
            )
            self.assertFalse(result.applied)


if __name__ == "__main__":
    unittest.main()