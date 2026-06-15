import unittest

from life_v0.language.pragmatic_inference import (
    enrich_semantic_map_with_pragmatic_inference,
    pragmatic_inference_inspection_snapshot,
)
from life_v0.language.semantic_map import project_semantic_map_from_live_evidence


class PragmaticInferenceTests(unittest.TestCase):
    def test_enriches_semantic_map_from_live_evidence(self):
        semantic_map = {
            "schema_version": "semantic_map_frame_v0",
            "semantic_focus": "relational_checkin",
            "ambiguity_queue": [],
        }
        language_percept = {
            "ambiguity_flags": ["shared_term_unresolved"],
            "repair_trigger_candidates": ["repair-language-v0-0001"],
        }
        result = enrich_semantic_map_with_pragmatic_inference(
            semantic_map=semantic_map,
            language_percept=language_percept,
            relationship_timeline={
                "trust_trajectories": [{"current_trust_state": "guarded"}],
                "relationship_continuity_reports": [
                    {"continuity_state": "repair_guarded_continuity"}
                ],
            },
            commitment_truth_state={
                "open_commitment_refs": ["commitment-1"],
                "repair_required_refs": ["repair-1"],
            },
            context_accumulation={
                "unresolved_commitment_refs": ["commitment-1"],
            },
            generated_at="2026-06-15T07:00:00+00:00",
        )

        profile = result["pragmatic_inference_profile"]
        self.assertEqual(result["pragmatic_inference_mode"], "live_evidence_inference")
        self.assertEqual(result["semantic_focus"], "repair_relational_trace")
        self.assertTrue(profile["speech_act_candidates"])
        self.assertTrue(profile["grounding_repair_signals"])
        self.assertTrue(profile["implicature_queue"])

    def test_project_semantic_map_from_live_evidence_wrapper(self):
        result = project_semantic_map_from_live_evidence(
            semantic_map={"semantic_focus": "relational_checkin"},
            language_percept={"ambiguity_flags": ["relation_role_mismatch"]},
            commitment_truth_state={"open_commitment_refs": ["c-1"]},
            generated_at="2026-06-15T07:30:00+00:00",
        )
        self.assertIn("pragmatic_inference_profile", result)

    def test_inspection_snapshot_fields(self):
        snapshot = pragmatic_inference_inspection_snapshot(
            semantic_map={
                "pragmatic_inference_mode": "live_evidence_inference",
                "pragmatic_inference_profile": {
                    "dominant_pragmatic_intent": "repair_relational_trace",
                    "speech_act_candidates": [{"speech_act_id": "repair_request"}],
                    "implicature_queue": [{"implicature_id": "i-1"}],
                    "grounding_repair_signals": [{"signal_id": "g-1"}],
                    "evidence_refs": ["ref-a"],
                },
            }
        )
        self.assertTrue(snapshot["pragmatic_inference_present"])
        self.assertEqual(snapshot["pragmatic_speech_act_count"], 1)
        self.assertEqual(snapshot["dominant_pragmatic_intent"], "repair_relational_trace")