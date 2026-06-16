import unittest

from life_v0.language.pragmatic_inference import detect_memory_feedback_from_utterance
from life_v0.state_store.memory_trace_store import (
    apply_post_expression_reconsolidation,
    build_memory_trace_store,
    project_live_dialogue_episode_traces,
)


class MemoryReconsolidationFeedbackTests(unittest.TestCase):
    def _seed_store_with_live_trace(self) -> dict:
        return build_memory_trace_store(
            run_id="u3-seed",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "你记得我喜欢咖啡吗？",
                "semantic_focus": "coffee_preference",
                "expression_outcome": "released",
            },
        )

    def test_detect_memory_feedback_correction(self):
        feedback = detect_memory_feedback_from_utterance(
            "你记错了，我不喜欢咖啡。",
            dialogue_turn_ref="runtime/state/language/dialogue_turn_log.jsonl#line-3",
        )
        self.assertEqual(feedback["event_type"], "correction")

    def test_correction_deprecates_old_trace_and_creates_new(self):
        store = self._seed_store_with_live_trace()
        old_trace = [
            trace
            for trace in store["traces"]
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        ][0]
        old_trace_id = old_trace["trace_id"]
        feedback = {
            "event_type": "correction",
            "trigger_event_ref": "runtime/state/language/dialogue_turn_log.jsonl#line-3",
        }
        result = apply_post_expression_reconsolidation(
            store,
            feedback_event=feedback,
            run_id="u3-correct",
            generated_at="2026-06-16T01:00:00+00:00",
            relationship_memory={},
            state_merge_guard={},
            exclude_dialogue_turn_ref="runtime/state/language/dialogue_turn_log.jsonl#line-3",
        )
        updated = result["memory_trace_store"]
        report = result["memory_reconsolidation_report"]
        deprecated = [
            trace
            for trace in updated["traces"]
            if trace.get("trace_id") == old_trace_id
        ][0]
        self.assertEqual(deprecated["lifecycle_state"], "deprecated")
        self.assertTrue(deprecated["contradiction_links"])
        self.assertEqual(report["feedback_event_type"], "correction")
        self.assertIn(
            f"runtime/state/memory/memory_trace_store.json#{old_trace_id}",
            report["old_trace_refs"],
        )
        self.assertTrue(report["new_trace_refs"])
        self.assertTrue(report["contradiction_links"])
        self.assertTrue(report.get("mem_cor_002_satisfied"))

    def test_confirmation_strengthens_trace(self):
        store = self._seed_store_with_live_trace()
        old_trace = [
            trace
            for trace in store["traces"]
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        ][0]
        old_confidence = float(old_trace.get("confidence") or 0)
        result = apply_post_expression_reconsolidation(
            store,
            feedback_event={
                "event_type": "confirmation",
                "trigger_event_ref": "runtime/state/language/dialogue_turn_log.jsonl#line-4",
            },
            run_id="u3-confirm",
            generated_at="2026-06-16T02:00:00+00:00",
        )
        updated_trace = [
            trace
            for trace in result["memory_trace_store"]["traces"]
            if trace.get("trace_id") == old_trace["trace_id"]
        ][0]
        self.assertGreater(float(updated_trace["confidence"]), old_confidence)


if __name__ == "__main__":
    unittest.main()