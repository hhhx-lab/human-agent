import unittest

from life_v0.state_store.memory_trace_store import (
    build_memory_trace_store,
    project_live_dialogue_episode_traces,
)


class MemoryLiveTraceContentizationTests(unittest.TestCase):
    def test_project_live_dialogue_episode_trace_has_non_seed_content(self):
        traces = project_live_dialogue_episode_traces(
            run_id="u2-test",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "你还记得我们上次修复吗？",
                "life_response": "我记得那次修复还在进行。",
                "semantic_focus": "repair_relational_trace",
                "expression_outcome": "released",
            },
            memory_retrieval_frame={
                "cue_terms": ["repair", "relational"],
                "reconstruction_focus": "repair_relational_trace",
            },
        )
        self.assertEqual(len(traces), 1)
        trace = traces[0]
        self.assertEqual(trace.get("live_trace_origin"), "live_dialogue_turn")
        self.assertEqual(trace.get("memory_kind"), "episodic")
        self.assertIn(
            "dialogue_turn_log.jsonl#line-1",
            trace.get("source_evidence_refs", [])[0],
        )
        summary = str(trace.get("content_summary") or "")
        self.assertNotIn("Seed", summary)
        self.assertNotIn("state_store_seed", summary)
        self.assertIn("repair_relational_trace", summary)
        self.assertEqual(trace.get("expression_outcome"), "released")

    def test_build_memory_trace_store_appends_live_trace(self):
        store = build_memory_trace_store(
            run_id="u2-store",
            generated_at="2026-06-16T00:00:00+00:00",
            engram_index={
                "live_dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3"
                ]
            },
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-4",
                ],
                "external_utterance": "你好",
                "semantic_focus": "relation_checkin",
            },
        )
        live_traces = [
            trace
            for trace in store.get("traces", [])
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        ]
        self.assertEqual(len(live_traces), 1)
        self.assertGreater(store.get("trace_count", 0), 1)


if __name__ == "__main__":
    unittest.main()