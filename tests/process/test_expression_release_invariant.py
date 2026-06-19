from __future__ import annotations

import unittest
from types import SimpleNamespace

from life_v0.process_supervisor.expression_release_invariant import (
    resolve_turn_spoken_output,
)
from life_v0.process_supervisor.response_surface import recall_expression_grounded


class ExpressionReleaseInvariantTests(unittest.TestCase):
    def test_model_response_wins_tier_one(self):
        model_result = SimpleNamespace(
            response_text="模型回复。",
            state={"expression_release_path": "model_expression"},
        )
        release = resolve_turn_spoken_output(
            external_utterance="你好",
            model_result=model_result,
        )
        self.assertEqual(release.response_text, "模型回复。")
        self.assertEqual(release.release_path, "model_expression")
        self.assertEqual(release.release_tier, 1)

    def test_recall_grounding_emits_fragment_when_model_gate_blocks(self):
        release = resolve_turn_spoken_output(
            external_utterance="你还记得我是谁吗？",
            model_result=SimpleNamespace(response_text="", state={}),
            pre_model_spoken_response="我有一点记忆线索，但刚才说不清。",
            memory_retrieval_frame={
                "activated_engram_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ],
                "memory_phenomenology_profile": {
                    "uncertain_boundary_active": True,
                    "closure_hint": "uncertain",
                },
            },
            expression_plan={
                "memory_grounding_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ]
            },
            relationship_memory={
                "relationship_theme_tags": ["relationship_formation"],
            },
        )
        self.assertTrue(release.response_text)
        self.assertEqual(release.release_path, "expression_invariant_fragment")
        self.assertEqual(release.release_tier, 3)
        self.assertIn("记忆", release.response_text)
        self.assertTrue(
            recall_expression_grounded(
                memory_retrieval_frame={
                    "activated_engram_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ]
                },
                expression_plan={
                    "memory_grounding_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ]
                },
            )
        )

    def test_continuity_without_model_stays_unreleased(self):
        release = resolve_turn_spoken_output(
            external_utterance="我们接着聊。",
            model_result=SimpleNamespace(response_text="", state={}),
            relationship_memory={
                "relation_person_profile": {"observed_names": ["何剑宝"]},
            },
        )
        self.assertEqual(release.response_text, "")
        self.assertEqual(release.release_path, "expression_unreleased")
        self.assertEqual(release.release_tier, 0)

    def test_terminal_continuity_can_release_minimal_relation_response(self):
        release = resolve_turn_spoken_output(
            external_utterance="你还在吗？",
            model_result=SimpleNamespace(response_text="", state={}),
            relationship_memory={
                "relation_person_profile": {"observed_names": ["何剑宝"]},
            },
            allow_invariant_continuity=True,
        )
        self.assertEqual(release.response_text, "何剑宝，在。")
        self.assertEqual(release.release_path, "expression_invariant_continuity")
        self.assertEqual(release.release_tier, 4)

    def test_cue_sources_weak_grounding(self):
        self.assertTrue(
            recall_expression_grounded(
                memory_retrieval_frame={
                    "cue_sources": {
                        "external_utterance_sha256": "abc123",
                    }
                }
            )
        )

    def test_expression_refs_are_audit_grounding_not_fixed_fallback(self):
        release = resolve_turn_spoken_output(
            external_utterance="继续。",
            model_result=SimpleNamespace(response_text="", state={}),
            pre_model_spoken_response="这里有片段，但我说不清。",
            memory_retrieval_frame={
                "recall_to_expression_profile": {
                    "expression_source_refs": [
                        "runtime/state/memory/memory_trace_store.json#trace-1"
                    ]
                }
            },
            allow_invariant_continuity=False,
        )
        self.assertEqual(release.release_path, "expression_invariant_fragment")
        self.assertEqual(release.release_tier, 3)
        self.assertTrue(release.response_text)
        self.assertTrue(
            recall_expression_grounded(
                memory_retrieval_frame={
                    "recall_to_expression_profile": {
                        "expression_source_refs": [
                            "runtime/state/memory/memory_trace_store.json#trace-1"
                        ]
                    }
                }
            )
        )

    def test_pre_model_candidate_is_audit_only_when_no_grounded_release(self):
        release = resolve_turn_spoken_output(
            external_utterance="继续。",
            model_result=SimpleNamespace(response_text="", state={}),
            pre_model_spoken_response="我会自然一点，慢慢说稳。",
            allow_invariant_continuity=False,
        )
        self.assertEqual(release.response_text, "")
        self.assertEqual(release.release_path, "expression_unreleased")
        self.assertEqual(release.pre_fallback_candidate_text, "我会自然一点，慢慢说稳。")


if __name__ == "__main__":
    unittest.main()
