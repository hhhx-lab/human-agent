import unittest

from life_v0.state_store.hippocampal_cue_index import (
    activate_hippocampal_cues,
    build_hippocampal_cue_index,
    build_reconstruction_fragments,
)
from life_v0.state_store.human_brain_alignment_assessment import (
    build_human_brain_alignment_assessment,
)
from life_v0.state_store.memory_retrieval import build_memory_retrieval_frame
from life_v0.state_store.memory_trace_store import build_memory_trace_store
from life_v0.state_store.pattern_completion import build_pattern_completion_frame


class MemoryU13ReconstructiveRecallTests(unittest.TestCase):
    def test_hippocampal_cue_activation_returns_weighted_trace_bindings(self):
        store = build_memory_trace_store(
            run_id="u13-hippo",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "我喜欢茶",
                "semantic_focus": "tea_preference",
            },
        )
        cue_index = build_hippocampal_cue_index(
            run_id="u13-hippo",
            generated_at="2026-06-16T00:00:00+00:00",
            memory_trace_store=store,
        )
        activations = activate_hippocampal_cues(
            cue_terms=["tea", "茶", "tea_preference"],
            hippocampal_cue_index=cue_index,
        )
        self.assertTrue(activations)
        self.assertGreater(float(activations[0]["activation_score"]), 0)

    def test_pattern_completion_emits_reconstruction_fragments_not_only_refs(self):
        store = build_memory_trace_store(
            run_id="u13-complete",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-4",
                ],
                "external_utterance": "我们上次聊过咖啡",
                "semantic_focus": "coffee_chat",
            },
        )
        retrieval = build_memory_retrieval_frame(
            run_id="u13-complete",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="你还记得我们上次聊过什么？",
            cue_sources={"external_utterance": "你还记得我们上次聊过什么？"},
            memory_trace_store=store,
        )
        completion = build_pattern_completion_frame(
            run_id="u13-complete",
            generated_at="2026-06-16T00:00:00+00:00",
            memory_retrieval_frame=retrieval,
            memory_trace_store=store,
        )
        reconstructive = completion.get("reconstructive_completion") or {}
        fragments = reconstructive.get("reconstruction_fragments") or []
        self.assertTrue(fragments)
        self.assertEqual(
            reconstructive.get("completion_mode"),
            "reconstructive_fragment_assembly",
        )
        self.assertTrue(fragments[0].get("episode_digest"))
        self.assertIn("material_boundary", fragments[0])

    def test_memory_retrieval_wires_reconstructive_recall_profile(self):
        store = build_memory_trace_store(
            run_id="u13-retrieval",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-5",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-6",
                ],
                "external_utterance": "喜欢茶",
                "semantic_focus": "tea_preference",
            },
        )
        retrieval = build_memory_retrieval_frame(
            run_id="u13-retrieval",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="你还记得我喜欢什么？",
            memory_trace_store=store,
            pattern_completion_frame=build_pattern_completion_frame(
                run_id="u13-retrieval",
                generated_at="2026-06-16T00:00:00+00:00",
                memory_retrieval_frame={
                    "cue_terms": ["tea", "茶", "tea_preference", "记得"],
                },
                memory_trace_store=store,
            ),
        )
        reconstructive = retrieval.get("reconstructive_recall_profile") or {}
        self.assertEqual(
            reconstructive.get("completion_mode"),
            "reconstructive_fragment_assembly",
        )
        self.assertGreaterEqual(reconstructive.get("reconstruction_fragment_count"), 1)
        phenomenology = retrieval.get("memory_phenomenology_profile") or {}
        self.assertTrue(phenomenology.get("expression_material_grounded"))

    def test_human_brain_alignment_stays_below_engineering_rubric_ceiling(self):
        store = build_memory_trace_store(
            run_id="u13-assess",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-7",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-8",
                ],
                "external_utterance": "茶",
                "semantic_focus": "tea_preference",
            },
        )
        completion = build_pattern_completion_frame(
            run_id="u13-assess",
            generated_at="2026-06-16T00:00:00+00:00",
            memory_retrieval_frame={"cue_terms": ["tea", "茶"]},
            memory_trace_store=store,
        )
        retrieval = build_memory_retrieval_frame(
            run_id="u13-assess",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="你还记得吗？",
            memory_trace_store=store,
            pattern_completion_frame=completion,
        )
        assessment = build_human_brain_alignment_assessment(
            run_id="u13-assess",
            generated_at="2026-06-16T00:00:00+00:00",
            memory_trace_store=store,
            memory_retrieval_frame=retrieval,
            pattern_completion_frame=completion,
            hippocampal_cue_index=build_hippocampal_cue_index(
                run_id="u13-assess",
                generated_at="2026-06-16T00:00:00+00:00",
                memory_trace_store=store,
            ),
        )
        self.assertFalse(assessment.get("at_biological_human_parity"))
        self.assertLess(assessment.get("overall_brain_alignment_pct"), 100.0)
        cue_dimension = next(
            item
            for item in assessment.get("dimensions", [])
            if item.get("dimension_id") == "cue_reconstructive_recall"
        )
        self.assertGreater(cue_dimension.get("score_pct"), 40.0)


if __name__ == "__main__":
    unittest.main()