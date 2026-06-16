import unittest

from life_v0.state_store.cue_candidate_provider import (
    local_full_text_cue_candidate_provider,
    noop_cue_candidate_provider,
)
from life_v0.state_store.memory_retrieval import (
    build_memory_retrieval_frame,
    merge_cue_candidates,
)


class MemoryCueProviderTests(unittest.TestCase):
    def test_noop_provider_returns_empty_candidates(self):
        result = noop_cue_candidate_provider(
            cue_terms=["coffee", "preference"],
            memory_trace_store={"traces": []},
        )
        self.assertEqual(result["provider_name"], "noop")
        self.assertEqual(result["candidate_trace_refs"], [])
        self.assertEqual(result["candidate_cue_terms"], [])

    def test_merge_cue_candidates_noop_does_not_change_activated_refs(self):
        merge = merge_cue_candidates(
            cue_terms=["repair"],
            memory_trace_store={"traces": []},
            relationship_memory={},
            blocked_refs=[],
            provider_name="noop",
        )
        self.assertEqual(merge["eligible_candidate_trace_refs"], [])
        self.assertEqual(merge["cue_provider_audit"]["provider_name"], "noop")

    def test_deleted_trace_blocked_from_expression_candidates(self):
        trace_store = {
            "traces": [
                {
                    "trace_id": "memory-trace-deleted-001",
                    "lifecycle_state": "deleted",
                    "content_summary": "coffee preference episode",
                    "live_trace_origin": "live_dialogue_turn",
                },
                {
                    "trace_id": "memory-trace-active-001",
                    "lifecycle_state": "active",
                    "content_summary": "coffee preference episode",
                    "live_trace_origin": "live_dialogue_turn",
                },
            ]
        }
        provider = local_full_text_cue_candidate_provider(
            cue_terms=["coffee"],
            memory_trace_store=trace_store,
        )
        self.assertEqual(len(provider["candidate_trace_refs"]), 1)
        merge = merge_cue_candidates(
            cue_terms=["coffee"],
            memory_trace_store=trace_store,
            relationship_memory={},
            blocked_refs=[
                "runtime/state/memory/memory_trace_store.json#memory-trace-deleted-001"
            ],
            provider_name="local_full_text",
        )
        self.assertEqual(len(merge["eligible_candidate_trace_refs"]), 1)
        self.assertNotIn(
            "runtime/state/memory/memory_trace_store.json#memory-trace-deleted-001",
            merge["eligible_candidate_trace_refs"],
        )

    def test_build_memory_retrieval_frame_with_noop_matches_baseline_shape(self):
        frame = build_memory_retrieval_frame(
            run_id="u4-noop",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="你还记得吗？",
            cue_provider_name="noop",
        )
        self.assertIn("cue_provider_audit", frame)
        self.assertEqual(frame["cue_provider_audit"]["provider_name"], "noop")
        guardrails = frame["recall_to_expression_profile"]["expression_guardrails"]
        self.assertIn("provider_hits_are_not_facts", guardrails)

    def test_pattern_separation_scope_keeps_relationship_hits_separate(self):
        frame_a = build_memory_retrieval_frame(
            run_id="u4-scope-a",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="你喜欢什么？",
            relationship_memory={
                "shared_memory_refs": ["runtime/state/memory/relationship_memory.json#person-a"],
                "relationship_scope": "person_a",
            },
            cue_provider_name="noop",
        )
        frame_b = build_memory_retrieval_frame(
            run_id="u4-scope-b",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="你喜欢什么？",
            relationship_memory={
                "shared_memory_refs": ["runtime/state/memory/relationship_memory.json#person-b"],
                "relationship_scope": "person_b",
            },
            cue_provider_name="noop",
        )
        self.assertNotEqual(
            frame_a["relationship_memory_hits"],
            frame_b["relationship_memory_hits"],
        )


if __name__ == "__main__":
    unittest.main()