import unittest

from life_v0.language.shared_terms import (
    build_shared_term_registry,
    project_shared_term_registry_from_live_evidence,
    shared_term_promotion_inspection_snapshot,
)


class SharedTermsLivePromotionTests(unittest.TestCase):
    def test_promotes_surface_with_multi_source_evidence(self):
        seed = build_shared_term_registry(
            run_id="shared-term-promotion",
            generated_at="2026-06-15T00:00:00+00:00",
            source_doc_refs=["docs/real—live0/06_relationship_and_commitment.md"],
        )
        updated = project_shared_term_registry_from_live_evidence(
            shared_term_registry=seed,
            generated_at="2026-06-15T01:00:00+00:00",
            relationship_graph={
                "relationship_subjects": [{"relation_role": "friend"}],
            },
            relationship_timeline={
                "common_ground_states": [
                    {"shared_terms": ["生命膜", "共同语言"]},
                ],
            },
            language_percept={
                "shared_term_hits": ["共同语言"],
                "relation_scope_ref": (
                    "runtime/state/language/relation_scope_language_index.json"
                    "#relation-scope-v0-0001"
                ),
            },
            semantic_map={
                "shared_meaning_bindings": [{"surface": "生命膜"}],
            },
            context_accumulation={
                "shared_term_surfaces": ["生命膜", "共同语言"],
                "context_accumulation_ref": (
                    "runtime/state/terminal/context_accumulation_window.json"
                ),
            },
            relation_scope_index={
                "relation_scopes": [{"relation_role": "friend"}],
            },
            dialogue_turn_refs=[
                "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                "runtime/state/language/dialogue_turn_log.jsonl#line-2",
            ],
            live_language_turn_refs=[
                "runtime/state/language/live_language_turn_log.jsonl#line-1",
            ],
        )

        surfaces = [term["surface"] for term in updated["shared_terms"]]
        self.assertIn("生命膜", surfaces)
        self.assertTrue(updated["live_promotion_refreshed"])
        promoted = next(
            term for term in updated["shared_terms"] if term["surface"] == "生命膜"
        )
        self.assertEqual(promoted["promotion_gate_status"], "promoted")
        self.assertIn("relationship_timeline_common_ground", promoted["promotion_evidence_sources"])
        self.assertIn("context_accumulation_window", promoted["promotion_evidence_sources"])

    def test_blocks_premature_single_turn_promotion(self):
        seed = build_shared_term_registry(
            run_id="shared-term-premature",
            generated_at="2026-06-15T00:00:00+00:00",
            source_doc_refs=["docs/87_language_event_schema_fixture_and_validator_plan.md"],
        )
        updated = project_shared_term_registry_from_live_evidence(
            shared_term_registry=seed,
            generated_at="2026-06-15T01:00:00+00:00",
            relationship_graph={
                "relationship_subjects": [{"relation_role": "friend"}],
            },
            language_percept={"shared_term_hits": ["生命膜"]},
            context_accumulation={"shared_term_surfaces": ["生命膜"]},
            relation_scope_index={
                "relation_scopes": [{"relation_role": "friend"}],
            },
            dialogue_turn_refs=[
                "runtime/state/language/dialogue_turn_log.jsonl#line-1",
            ],
        )

        surfaces = [term["surface"] for term in updated["shared_terms"]]
        self.assertNotIn("生命膜", surfaces)
        self.assertIn("生命膜", updated["shared_term_promotion_candidate_surfaces"])

    def test_inspection_snapshot_reports_live_promotion(self):
        registry = {
            "live_promotion_refreshed": True,
            "shared_term_promotion_candidate_count": 1,
            "shared_term_promotion_relation_scope": "friend",
            "shared_term_promotion_dialogue_turn_count": 3,
            "shared_terms": [
                {
                    "surface": "共同语言",
                    "promotion_gate_status": "seed",
                },
                {
                    "surface": "生命膜",
                    "promotion_gate_status": "promoted",
                },
            ],
        }
        snapshot = shared_term_promotion_inspection_snapshot(
            shared_term_registry=registry,
            terminal_life_loop_state={"live_shared_term_promotion_refreshed": True},
        )

        self.assertTrue(snapshot["shared_term_live_promotion_present"])
        self.assertEqual(snapshot["shared_term_promotion_count"], 2)
        self.assertEqual(snapshot["shared_term_live_promoted_count"], 1)
        self.assertEqual(snapshot["shared_term_promotion_candidate_count"], 1)


if __name__ == "__main__":
    unittest.main()