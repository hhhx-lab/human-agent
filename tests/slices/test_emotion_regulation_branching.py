import unittest

from life_v0.body.emotion_episode import (
    build_affective_episode,
    project_affective_episode_from_live_turn,
    resolve_affective_episode_profile,
)
from life_v0.body.emotion_regulation import (
    build_emotion_regulation_loop,
    project_emotion_regulation_from_live_turn,
    resolve_emotion_regulation_profile,
)


class EmotionRegulationBranchingTests(unittest.TestCase):
    def _core_affect(self, **overrides) -> dict:
        base = {
            "pain_pressure": 0.2,
            "arousal": 0.35,
            "relationship_tension": 0.3,
            "dream_residue_load": 0.2,
            "responsibility_weight": 0.25,
        }
        base.update(overrides)
        return base

    def test_pain_pressure_selects_recovery_window_episode(self):
        profile = resolve_affective_episode_profile(
            core_affect=self._core_affect(pain_pressure=0.7),
            life_state={"runtime_trace_refs": ["runtime/state/life_state.json"]},
            pain_regret_repair_report={"repair_followup_required": True},
        )
        self.assertEqual(profile["episode_label"], "pain_peak_regret_pull")
        self.assertEqual(profile["regulation_route"], "recovery_window")

    def test_dream_residue_selects_dream_integration_episode(self):
        profile = resolve_affective_episode_profile(
            core_affect=self._core_affect(dream_residue_load=0.8),
            life_state={"runtime_trace_refs": []},
        )
        self.assertEqual(profile["episode_label"], "dream_residue_repair_pull")
        self.assertEqual(profile["regulation_route"], "dream_integration")

    def test_high_arousal_and_tension_select_reappraisal(self):
        profile = resolve_affective_episode_profile(
            core_affect=self._core_affect(arousal=0.72, relationship_tension=0.55),
            life_state={"runtime_trace_refs": []},
        )
        self.assertEqual(profile["episode_label"], "relationship_tension_clarify")
        self.assertEqual(profile["regulation_route"], "reappraisal")

    def test_arousal_peak_selects_action_slowdown(self):
        profile = resolve_affective_episode_profile(
            core_affect=self._core_affect(arousal=0.82, relationship_tension=0.2),
            life_state={"runtime_trace_refs": []},
        )
        self.assertEqual(profile["episode_label"], "high_arousal_guard")
        self.assertEqual(profile["regulation_route"], "action_slowdown")

    def test_regulation_profile_branches_from_episode_route(self):
        episode = {
            "regulation_route": "dream_integration",
            "expression_risk": "guarded",
        }
        profile = resolve_emotion_regulation_profile(
            episode=episode,
            core_affect=self._core_affect(),
            recovery_path={"blocked_reasons": []},
            body_resource_budget={"fatigue_state": {"level": "managed_low_noise"}},
        )
        self.assertEqual(profile["regulation_mode"], "dream_consolidation_hold")
        self.assertEqual(profile["regulation_route"], "dream_integration")

    def test_fatigue_biases_expression_monitoring_to_recovery_window(self):
        episode = {
            "regulation_route": "expression_monitoring",
            "expression_risk": "guarded",
        }
        profile = resolve_emotion_regulation_profile(
            episode=episode,
            core_affect=self._core_affect(),
            recovery_path={"blocked_reasons": []},
            body_resource_budget={"fatigue_state": {"level": "high"}},
        )
        self.assertEqual(profile["regulation_route"], "recovery_window")
        self.assertEqual(profile["regulation_mode"], "recovery_window_hold")

    def test_build_and_live_project_preserve_branch_fields(self):
        core_affect = self._core_affect(pain_pressure=0.65)
        life_state = {"runtime_trace_refs": ["runtime/state/life_state.json"]}
        episode = build_affective_episode(
            run_id="emotion-branch-test",
            generated_at="2026-06-15T00:00:00+00:00",
            core_affect=core_affect,
            life_state=life_state,
            pain_regret_repair_report={"repair_followup_required": True},
        )
        regulation = build_emotion_regulation_loop(
            run_id="emotion-branch-test",
            generated_at="2026-06-15T00:00:00+00:00",
            episode=episode,
            recovery_path={"blocked_reasons": []},
            core_affect=core_affect,
            body_resource_budget={"fatigue_state": {"level": "managed_low_noise"}},
        )
        self.assertEqual(episode["regulation_route"], "recovery_window")
        self.assertEqual(regulation["regulation_mode"], "recovery_window_hold")
        self.assertTrue(regulation["regulation_branch_reason"])

        live_episode = project_affective_episode_from_live_turn(
            affective_episode=episode,
            generated_at="2026-06-15T00:01:00+00:00",
            run_id="emotion-branch-live",
            core_affect_vector=core_affect,
            life_state=life_state,
            pain_regret_repair_report={"repair_followup_required": True},
            live_dialogue_turn_refs=["runtime/state/dialogue/dialogue_turn_log.jsonl#1"],
            live_turn_focus="repair_followup",
        )
        live_regulation = project_emotion_regulation_from_live_turn(
            emotion_regulation=regulation,
            generated_at="2026-06-15T00:01:00+00:00",
            run_id="emotion-branch-live",
            episode=live_episode,
            core_affect_vector=core_affect,
            recovery_path={"blocked_reasons": []},
            body_resource_budget={"fatigue_state": {"level": "managed_low_noise"}},
        )
        self.assertTrue(live_episode["live_affective_episode_refreshed"])
        self.assertTrue(live_regulation["live_emotion_regulation_refreshed"])
        self.assertEqual(live_regulation["previous_regulation_mode"], "recovery_window_hold")


if __name__ == "__main__":
    unittest.main()