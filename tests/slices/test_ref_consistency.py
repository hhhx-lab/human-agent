import unittest

from life_v0.language.percept import build_language_percept_frame
from life_v0.language.ref_consistency import (
    project_language_relationship_ref_consistency_profile,
)
from life_v0.language.relation_scope import build_relation_scope_language_index
from life_v0.language.semantic_map import build_semantic_map_frame
from life_v0.language.shared_terms import build_shared_term_registry


class RefConsistencyTests(unittest.TestCase):
    def _base_inputs(self) -> dict:
        source_doc_refs = [
            "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md"
        ]
        relation_scope_index = build_relation_scope_language_index(
            run_id="ref-consistency-test",
            generated_at="2026-06-15T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )
        shared_term_registry = build_shared_term_registry(
            run_id="ref-consistency-test",
            generated_at="2026-06-15T00:00:00+00:00",
            source_doc_refs=source_doc_refs,
        )
        language_percept = build_language_percept_frame(
            run_id="ref-consistency-test",
            generated_at="2026-06-15T00:00:00+00:00",
            incoming_turn={
                "incoming_surface": "我们还需要修复共同语言里的约定。",
                "speaker_role": "friend",
            },
            relation_scope_index=relation_scope_index,
            shared_term_registry=shared_term_registry,
            source_doc_refs=source_doc_refs,
        )
        language_state = {
            "shared_language_refs": [
                "runtime/state/language/language_relationship_state.json#shared-language-v0-0001"
            ]
        }
        semantic_map = build_semantic_map_frame(
            run_id="ref-consistency-test",
            generated_at="2026-06-15T00:00:00+00:00",
            language_percept=language_percept,
            language_state=language_state,
            shared_term_registry=shared_term_registry,
            commitment_repair_index={
                "commitment_refs": ["commitment-v0-0001"],
                "repair_language_refs": ["repair-language-v0-0001"],
            },
            self_narrative_trace={"narrative_turn_refs": []},
            source_doc_refs=source_doc_refs,
        )
        return {
            "relation_scope_index": relation_scope_index,
            "shared_term_registry": shared_term_registry,
            "language_percept": language_percept,
            "semantic_map": semantic_map,
        }

    def test_profile_reports_closed_when_refs_align(self):
        inputs = self._base_inputs()
        relationship_graph = {
            "subjects": [
                {
                    "relationship_stage": "shared_language_waiting",
                    "relationship_stage_reason": "shared_language_accumulation_waiting",
                }
            ],
            "relationship_stage_evolution_profile": {
                "relationship_stage_reason": "shared_language_accumulation_waiting",
                "dialogue_turn_count": 2,
            },
        }
        profile = project_language_relationship_ref_consistency_profile(
            generated_at="2026-06-15T00:00:00+00:00",
            language_percept=inputs["language_percept"],
            semantic_map=inputs["semantic_map"],
            relation_scope_index=inputs["relation_scope_index"],
            shared_term_registry=inputs["shared_term_registry"],
            relationship_graph=relationship_graph,
            relationship_timeline={"dialogue_turn_refs": ["turn-1", "turn-2"]},
            self_model_state={
                "last_trait_evolution_reason": "shared_language_accumulation_waiting"
            },
            inner_speech={
                "percept_ref": "runtime/state/language/language_percept_frame.json",
                "semantic_map_ref": "runtime/state/language/semantic_map_frame.json",
            },
            expression_plan={
                "semantic_map_ref": "runtime/state/language/semantic_map_frame.json",
                "inner_speech_ref": "runtime/state/language/inner_speech_frame.json",
            },
        )

        self.assertEqual(profile["status"], "closed")
        self.assertEqual(profile["mismatch_finding_count"], 0)
        self.assertGreaterEqual(profile["aligned_finding_count"], 5)


if __name__ == "__main__":
    unittest.main()