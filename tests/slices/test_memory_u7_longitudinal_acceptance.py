import unittest

from life_v0.language.pragmatic_inference import detect_memory_feedback_from_utterance
from life_v0.state_store.memory_retrieval import (
    build_memory_retrieval_frame,
    project_memory_retrieval_from_live_turn,
)
from life_v0.state_store.memory_trace_store import (
    apply_post_expression_reconsolidation,
    build_memory_trace_store,
)


class MemoryU7LongitudinalAcceptanceTests(unittest.TestCase):
    def test_recall_without_source_keeps_uncertain_boundary(self):
        frame = build_memory_retrieval_frame(
            run_id="u7-uncertain",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="你还记得 X 吗？",
        )
        profile = frame.get("recall_to_expression_profile") or {}
        self.assertIn(
            profile.get("closure_status"),
            {"uncertain", "partial", "closed", "withhold_pending_reconstruction"},
        )
        hooks = profile.get("post_expression_reconsolidation_hooks") or []
        self.assertIn("uncertain_recall_remains_hypothesis_or_silent_trace", hooks)

    def test_correction_state_machine_triggers(self):
        store = build_memory_trace_store(
            run_id="u7-correct",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "上次你说我喜欢茶",
                "semantic_focus": "tea_preference",
            },
        )
        feedback = detect_memory_feedback_from_utterance(
            "你记错了，是咖啡。",
            dialogue_turn_ref="runtime/state/language/dialogue_turn_log.jsonl#line-3",
        )
        result = apply_post_expression_reconsolidation(
            store,
            feedback_event=feedback,
            run_id="u7-correct",
            generated_at="2026-06-16T01:00:00+00:00",
            relationship_memory={},
            state_merge_guard={},
            exclude_dialogue_turn_ref="runtime/state/language/dialogue_turn_log.jsonl#line-3",
        )
        self.assertEqual(
            result["memory_reconsolidation_report"]["feedback_event_type"],
            "correction",
        )

    def test_live_trace_enters_recall_expression_refs(self):
        trace_store = build_memory_trace_store(
            run_id="u7-recall",
            generated_at="2026-06-16T00:00:00+00:00",
            engram_index={
                "live_memory_trace_refs": [
                    "runtime/state/memory/memory_trace_store.json#memory-trace-live"
                ]
            },
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-5",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-6",
                ],
                "external_utterance": "我们上次聊过什么？",
                "semantic_focus": "shared_history",
            },
        )
        live_refs = [
            trace["trace_id"]
            for trace in trace_store.get("traces", [])
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        ]
        engram_index = {
            "live_memory_trace_refs": [
                f"runtime/state/memory/memory_trace_store.json#{trace_id}"
                for trace_id in live_refs
            ]
        }
        frame = project_memory_retrieval_from_live_turn(
            memory_retrieval_frame=None,
            run_id="u7-recall",
            generated_at="2026-06-16T00:00:00+00:00",
            external_utterance="我们上次聊过什么？",
            semantic_map={"semantic_focus": "shared_history"},
            language_percept={},
            engram_index=engram_index,
            relationship_memory={},
            autobiographical_stack={},
            dialogue_memory_summary={},
            life_state={},
            responsibility_loop_state={},
            state_merge_guard={},
            memory_trace_store=trace_store,
        )
        source_refs = frame["recall_to_expression_profile"].get(
            "expression_source_refs"
        ) or []
        self.assertTrue(source_refs)


if __name__ == "__main__":
    unittest.main()