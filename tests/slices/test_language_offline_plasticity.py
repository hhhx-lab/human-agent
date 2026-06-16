import unittest

from life_v0.language.expression_monitor import (
    apply_body_proactive_release_threshold,
    apply_world_contact_handoff_modulation,
)
from life_v0.language.language_plasticity import (
    build_language_plasticity_update,
    build_language_rhythm_trace,
)
from life_v0.language.offline_influence import (
    enrich_semantic_map_with_offline_influence,
    project_expression_plan_with_offline_influence,
)


class LanguageOfflinePlasticityTests(unittest.TestCase):
    def test_offline_influence_enriches_semantic_map(self):
        result = enrich_semantic_map_with_offline_influence(
            semantic_map={"semantic_focus": "relational_checkin", "prediction_hooks": {}},
            offline_consolidation_frame={"dream_window_refs": ["dream-window-1"]},
            replay_cue_bundle={"anti_forgetting_targets": ["replay-target-1"]},
            generated_at="2026-06-16T03:00:00+00:00",
        )
        self.assertIn("dream-window-1", result["offline_influence_refs"])
        self.assertEqual(result["dream_residue_refs"], ["dream-window-1"])

    def test_expression_plan_gets_dream_fact_boundary(self):
        semantic = enrich_semantic_map_with_offline_influence(
            semantic_map={"prediction_hooks": {}},
            offline_consolidation_frame={"dream_window_refs": ["dream-window-1"]},
            generated_at="2026-06-16T03:00:00+00:00",
        )
        plan = project_expression_plan_with_offline_influence(
            expression_plan={"expression_risk_flags": []},
            enriched_semantic_map=semantic,
            generated_at="2026-06-16T03:00:00+00:00",
        )
        self.assertEqual(plan["dream_fact_boundary"], "dream_experience_not_factual_memory")

    def test_world_contact_handoff_holds_release(self):
        plan = apply_world_contact_handoff_modulation(
            expression_plan={"delay_or_release_decision": "release_guarded_expression"},
            world_contact_summary={
                "world_contact_handoff_presence": {"repair_hold_active": True}
            },
        )
        self.assertEqual(plan["delay_or_release_decision"], "hold_for_world_contact_repair")

    def test_body_fatigue_sets_proactive_threshold(self):
        plan = apply_body_proactive_release_threshold(
            expression_plan={"fatigue_pressure": "critical", "release_caution_level": "elevated"},
            proactive_voice_profile={"release_constraints": []},
        )
        self.assertEqual(plan["proactive_release_threshold"], "elevated")

    def test_language_plasticity_update_tracks_promoted_terms(self):
        result = build_language_plasticity_update(
            run_id="plasticity-run",
            generated_at="2026-06-16T03:00:00+00:00",
            shared_term_registry={
                "shared_terms": [
                    {
                        "surface": "语言系统",
                        "meaning_ref": "meaning-1",
                        "promotion_status": "promoted",
                    }
                ]
            },
            expression_plan={"expression_tempo_mode": "guarded_deliberate"},
            dialogue_turn_count=3,
        )
        self.assertEqual(result["promoted_shared_term_count"], 1)
        self.assertEqual(result["expression_tempo_mode"], "guarded_deliberate")
        rhythm = build_language_rhythm_trace(
            run_id="plasticity-run",
            generated_at="2026-06-16T03:00:00+00:00",
            expression_plan={"expression_tempo_mode": "guarded_deliberate"},
        )
        self.assertTrue(rhythm["tempo_history"])

    def test_body_proactive_profile_receives_release_constraints(self):
        profile = {"release_constraints": []}
        plan = apply_body_proactive_release_threshold(
            expression_plan={"fatigue_pressure": "critical"},
            proactive_voice_profile=profile,
        )
        self.assertEqual(plan["proactive_release_threshold"], "elevated")
        self.assertIn(
            "hold_proactive_voice_until_body_recovery",
            profile["release_constraints"],
        )

    def test_language_rhythm_trace_accumulates_tempo_history(self):
        prior = build_language_rhythm_trace(
            run_id="plasticity-run",
            generated_at="2026-06-16T02:00:00+00:00",
            expression_plan={"expression_tempo_mode": "guarded_deliberate"},
        )
        latest = build_language_rhythm_trace(
            run_id="plasticity-run",
            generated_at="2026-06-16T03:00:00+00:00",
            expression_plan={"expression_tempo_mode": "slow_protective"},
        )
        history = list(prior["tempo_history"])
        history.append(latest["tempo_history"][0])
        self.assertEqual(len(history), 2)
        self.assertEqual(
            history[-1]["expression_tempo_mode"],
            "slow_protective",
        )