import unittest

from life_v0.language.language_event_bundle import (
    FIXTURE_EVENT_KINDS,
    build_language_event_bundle,
    infer_language_event_kind,
)


class LanguageEventBundleTests(unittest.TestCase):
    def test_builds_bundle_with_required_refs(self):
        bundle = build_language_event_bundle(
            run_id="bundle-test",
            generated_at="2026-06-16T00:00:00+00:00",
            language_event_kind="apologize",
            future_probe_refs=["future-probe-1"],
        )
        self.assertEqual(bundle["schema_version"], "language_event_bundle_v0")
        self.assertEqual(bundle["language_event_kind"], "apologize")
        self.assertEqual(bundle["fixture_event_kinds_covered"], list(FIXTURE_EVENT_KINDS))
        self.assertTrue(bundle["inner_speech_ref"])
        self.assertTrue(bundle["expression_plan_ref"])
        self.assertTrue(bundle["turn_transition_trace_ref"])
        self.assertEqual(bundle["future_probe"], ["future-probe-1"])

    def test_infer_language_event_kind_covers_fixture_families(self):
        self.assertEqual(
            infer_language_event_kind(
                semantic_focus="commitment_request",
                speech_act="commitment_request",
            ),
            "commit",
        )
        self.assertEqual(
            infer_language_event_kind(semantic_focus="apology_repair"),
            "apologize",
        )
        self.assertEqual(
            infer_language_event_kind(semantic_focus="boundary_refusal"),
            "refuse",
        )
        self.assertEqual(
            infer_language_event_kind(dream_signal_candidates=["dream-residue"]),
            "dream_report",
        )
        self.assertEqual(
            infer_language_event_kind(shared_term_hits=["共同词"]),
            "shared_term_development",
        )