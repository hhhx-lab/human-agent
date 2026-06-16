import unittest

from life_v0.state_store.life_schema_map import project_life_schema_map_from_live_turn
from life_v0.state_store.memory_allocation_gate import build_memory_allocation_gate
from life_v0.state_store.memory_trace_store import (
    build_fast_episodic_buffer,
    build_memory_trace_store,
)
from life_v0.state_store.event_segmentation import build_event_segmentation_frame


class MemoryFastSlowChannelTests(unittest.TestCase):
    def test_fast_episodic_buffer_indexes_recent_live_traces(self):
        store = build_memory_trace_store(
            run_id="u5-fast",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "第一轮",
                "semantic_focus": "topic_alpha",
            },
        )
        store = build_memory_trace_store(
            run_id="u5-fast",
            generated_at="2026-06-16T00:01:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-4",
                ],
                "external_utterance": "第二轮",
                "semantic_focus": "topic_beta",
            },
            existing_memory_trace_store=store,
        )
        buffer = store.get("fast_episodic_buffer") or {}
        self.assertGreaterEqual(buffer.get("entry_count", 0), 2)
        self.assertTrue(buffer.get("trace_refs"))

    def test_schema_promotion_after_repeated_episodes(self):
        traces = []
        for index in range(3):
            traces.append(
                {
                    "trace_id": f"memory-trace-live-{index}",
                    "live_trace_origin": "live_dialogue_turn",
                    "lifecycle_state": "active",
                    "semantic_focus": "relationship_continuity_and_repair",
                    "content_summary": (
                        "Live relation episode centered on relationship_continuity_and_repair"
                    ),
                }
            )
        schema_map = project_life_schema_map_from_live_turn(
            life_schema_map=None,
            run_id="u5-schema",
            generated_at="2026-06-16T00:00:00+00:00",
            memory_trace_store={"traces": traces},
        )
        promoted = schema_map.get("last_promoted_schema_ids") or []
        self.assertFalse(promoted)
        schema_map = project_life_schema_map_from_live_turn(
            life_schema_map=schema_map,
            run_id="u5-schema",
            generated_at="2026-06-16T00:01:00+00:00",
            memory_trace_store={"traces": traces},
            memory_longitudinal_profile={"turn_count": 21},
        )
        promoted = schema_map.get("last_promoted_schema_ids") or []
        self.assertTrue(promoted)
        self.assertIn("schema_evidence_counts", schema_map)

    def test_allocation_gate_replay_priority_vector_prioritizes_live_trace(self):
        event_segmentation = build_event_segmentation_frame(
            run_id="u5-replay",
            generated_at="2026-06-16T00:00:00+00:00",
        )
        trace_store = build_memory_trace_store(
            run_id="u5-replay",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-9",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-10",
                ],
                "external_utterance": "repair now",
                "semantic_focus": "repair_relational_trace",
            },
        )
        allocation_gate = build_memory_allocation_gate(
            run_id="u5-replay",
            generated_at="2026-06-16T00:00:00+00:00",
            event_segmentation_frame=event_segmentation,
            memory_trace_store=trace_store,
            core_affect_vector={"repair_drive": 0.8},
        )
        vector = allocation_gate.get("replay_priority_vector") or []
        self.assertTrue(vector)
        live_entries = [
            item
            for item in vector
            if item.get("episode_kind") == "live_dialogue_episode"
        ]
        self.assertTrue(live_entries)


if __name__ == "__main__":
    unittest.main()