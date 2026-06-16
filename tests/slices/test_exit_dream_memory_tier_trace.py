import unittest

from life_v0.state_store.memory_retrieval import merge_cue_candidates
from life_v0.state_store.memory_trace_store import (
    merge_exit_dream_traces_into_store,
    project_exit_dream_episode_traces,
)


class ExitDreamMemoryTierTraceTests(unittest.TestCase):
    def _summary(self) -> dict:
        return {
            "deduplicated_episode_summaries": [
                {
                    "episode_id": "ep-core",
                    "source_ref": "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "semantic_key": "identity_name",
                    "summary": "我叫小明",
                    "event_role": "external_relation_turn",
                },
                {
                    "episode_id": "ep-sediment",
                    "source_ref": "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                    "semantic_key": "low_context",
                    "summary": "嗯",
                    "event_role": "external_relation_turn",
                },
            ],
            "memory_tiering": {
                "salient_core_episode_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ],
                "retrievable_context_episode_refs": [],
                "deep_sediment_episode_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2"
                ],
            },
        }

    def test_exit_dream_projects_trace_tiers(self):
        traces = project_exit_dream_episode_traces(
            run_id="d1-test",
            generated_at="2026-06-16T12:00:00Z",
            exit_dream_summary=self._summary(),
        )
        self.assertEqual(len(traces), 2)
        by_ref = {
            ref: trace
            for trace in traces
            for ref in trace.get("source_evidence_refs", [])
            if "dialogue_turn_log.jsonl#line-" in ref
        }
        core = by_ref["runtime/state/language/dialogue_turn_log.jsonl#line-1"]
        sediment = by_ref["runtime/state/language/dialogue_turn_log.jsonl#line-2"]
        self.assertEqual(core["accessibility_tier"], "salient_core")
        self.assertEqual(sediment["accessibility_tier"], "deep_sediment")
        self.assertEqual(
            sediment.get("retrieval_suppression_reason"),
            "low_salience_edge_detail",
        )

    def test_sediment_trace_suppressed_for_weak_cue(self):
        traces = project_exit_dream_episode_traces(
            run_id="d1-suppress",
            generated_at="2026-06-16T12:00:00Z",
            exit_dream_summary=self._summary(),
        )
        store = merge_exit_dream_traces_into_store(
            memory_trace_store={"traces": []},
            exit_dream_traces=traces,
            generated_at="2026-06-16T12:00:00Z",
        )
        sediment_id = next(
            trace["trace_id"]
            for trace in traces
            if trace["accessibility_tier"] == "deep_sediment"
        )
        merge = merge_cue_candidates(
            cue_terms=["x"],
            memory_trace_store=store,
            relationship_memory={},
            blocked_refs=[],
        )
        eligible = merge["eligible_candidate_trace_refs"]
        self.assertNotIn(
            f"runtime/state/memory/memory_trace_store.json#{sediment_id}",
            eligible,
        )