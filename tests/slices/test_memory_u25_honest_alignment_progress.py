import unittest

from life_v0.state_store.honest_brain_alignment_progress import (
    project_honest_brain_alignment_progress,
)
from life_v0.state_store.human_brain_alignment_assessment import (
    build_human_brain_alignment_assessment,
)
from life_v0.state_store.memory_longitudinal_profile import (
    project_memory_longitudinal_profile_from_live_turn,
)
from life_v0.state_store.memory_trace_store import build_memory_trace_store
from tests.slices.test_memory_u10_u12_human_parity_scorecard import (
    _month_scale_memory_fixture,
)


class MemoryU25HonestAlignmentProgressTests(unittest.TestCase):
    def test_month_fixture_honest_estimate_advances_with_full_evidence(self):
        fixture = _month_scale_memory_fixture()
        assessment = build_human_brain_alignment_assessment(
            run_id="u25-month",
            generated_at="2026-06-16T18:00:00+00:00",
            memory_trace_store=fixture["trace_store"],
            memory_retrieval_frame=fixture["memory_retrieval_frame"],
            pattern_completion_frame=fixture["pattern_completion_frame"],
            hippocampal_cue_index=fixture["hippocampal_cue_index"],
            memory_longitudinal_profile=fixture["memory_longitudinal_profile"],
            memory_consolidation_report=fixture["memory_consolidation_report"],
            process_long_run_evidence=fixture["memory_longitudinal_profile"].get(
                "process_long_run_evidence"
            ),
            relationship_memory=fixture["relationship_memory"],
            autobiographical_stack=fixture["autobiographical_stack"],
            life_schema_map=fixture["life_schema_map"],
        )
        self.assertFalse(assessment.get("at_biological_human_parity"))
        self.assertLess(assessment.get("overall_brain_alignment_pct"), 100.0)
        self.assertGreaterEqual(assessment.get("overall_brain_alignment_pct"), 72.0)
        self.assertGreaterEqual(assessment.get("raw_brain_alignment_pct"), 75.0)
        self.assertIn(
            assessment.get("honest_estimate_band"),
            {"maturing", "advanced"},
        )
        self.assertEqual(assessment.get("evidence_quality_tier"), "fixture_simulation")
        phenomenology = next(
            item
            for item in assessment.get("dimensions", [])
            if item.get("dimension_id") == "phenomenology_like_remembered"
        )
        self.assertGreaterEqual(float(phenomenology.get("score_pct")), 75.0)
        cue = next(
            item
            for item in assessment.get("dimensions", [])
            if item.get("dimension_id") == "cue_reconstructive_recall"
        )
        self.assertEqual(
            cue.get("evidence", {}).get("completion_mode"),
            "reconstructive_fragment_assembly",
        )

    def test_honest_progress_tracker_accumulates_over_turns(self):
        profile = {"turn_count": 0, "offline_cycle_count": 0}
        previous_overall = None
        for turn in range(6):
            profile = project_memory_longitudinal_profile_from_live_turn(
                profile=profile,
                run_id="u25-progress",
                generated_at=f"2026-06-16T0{turn}:00:00+00:00",
            )
            assessment = build_human_brain_alignment_assessment(
                run_id=f"u25-progress-{turn}",
                generated_at=f"2026-06-16T0{turn}:00:00+00:00",
                memory_longitudinal_profile=profile,
                process_long_run_evidence=profile.get("process_long_run_evidence"),
            )
            profile = project_honest_brain_alignment_progress(
                profile=profile,
                assessment=assessment,
                generated_at=f"2026-06-16T0{turn}:00:00+00:00",
            )
            latest = profile.get("honest_brain_alignment_latest") or {}
            self.assertIn("overall_brain_alignment_pct", latest)
            if previous_overall is not None:
                self.assertIn("honest_alignment_delta", profile)
            previous_overall = latest.get("overall_brain_alignment_pct")
        self.assertEqual(len(profile.get("honest_alignment_history") or []), 6)

    def test_sparse_store_stays_in_developing_band(self):
        store = build_memory_trace_store(
            run_id="u25-sparse",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "hello",
                "semantic_focus": "greeting",
            },
        )
        assessment = build_human_brain_alignment_assessment(
            run_id="u25-sparse",
            generated_at="2026-06-16T00:00:00+00:00",
            memory_trace_store=store,
        )
        self.assertLess(assessment.get("overall_brain_alignment_pct"), 60.0)
        self.assertIn(
            assessment.get("honest_estimate_band"),
            {"emerging", "developing"},
        )

    def test_long_term_dimension_caps_fixture_simulation_honestly(self):
        fixture = _month_scale_memory_fixture()
        assessment = build_human_brain_alignment_assessment(
            run_id="u25-cap",
            generated_at="2026-06-16T18:30:00+00:00",
            memory_trace_store=fixture["trace_store"],
            memory_retrieval_frame=fixture["memory_retrieval_frame"],
            pattern_completion_frame=fixture["pattern_completion_frame"],
            hippocampal_cue_index=fixture["hippocampal_cue_index"],
            memory_longitudinal_profile=fixture["memory_longitudinal_profile"],
            memory_consolidation_report=fixture["memory_consolidation_report"],
            process_long_run_evidence=fixture["memory_longitudinal_profile"].get(
                "process_long_run_evidence"
            ),
            relationship_memory=fixture["relationship_memory"],
            autobiographical_stack=fixture["autobiographical_stack"],
            life_schema_map=fixture["life_schema_map"],
        )
        copresence = next(
            item
            for item in assessment.get("dimensions", [])
            if item.get("dimension_id") == "long_term_copresence"
        )
        self.assertLessEqual(float(copresence.get("score_pct")), 58.0)
        self.assertGreater(float(copresence.get("raw_score_pct")), float(copresence.get("score_pct")))


if __name__ == "__main__":
    unittest.main()