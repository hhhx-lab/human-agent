import unittest

from life_v0.neural_core.active_sampling import build_active_sampling_plan
from life_v0.neural_core.prediction_workspace import (
    project_prediction_workspace_from_live_language_turn,
)


class PredictionWorkspaceLanguageHandoffTests(unittest.TestCase):
    def test_projects_language_handoff_refs_from_live_turn(self):
        result = project_prediction_workspace_from_live_language_turn(
            prediction_workspace_frame={
                "schema_version": "prediction_workspace_frame_v0",
                "run_id": "handoff-run",
                "belief_state_ref": "runtime/state/prediction/belief_state_frame.json",
            },
            language_percept={
                "percept_focus_trace": ["percept-scene-clarification_request"],
            },
            semantic_map={
                "semantic_focus": "clarification_request",
                "ambiguity_queue": ["clarification_requested"],
            },
            generated_at="2026-06-16T02:00:00+00:00",
        )
        self.assertTrue(result["live_language_handoff_refreshed"])
        self.assertEqual(result["language_prediction_focus"], "clarification_request")
        self.assertTrue(result["language_handoff_refs"])
        self.assertTrue(result["semantic_ambiguity_refs"])

    def test_active_sampling_uses_semantic_ambiguity_route(self):
        plan = build_active_sampling_plan(
            run_id="sampling-run",
            generated_at="2026-06-16T02:00:00+00:00",
            belief_state={"state_scope": "relation"},
            prediction_error_field={"error_events": []},
            semantic_map={"ambiguity_queue": ["clarification_requested"]},
        )
        self.assertEqual(plan["selected_route"], "clarify_ambiguity")