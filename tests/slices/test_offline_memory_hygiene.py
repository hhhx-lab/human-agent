import unittest

from life_v0.state_store.offline_memory_hygiene import apply_offline_memory_hygiene


class OfflineMemoryHygieneTests(unittest.TestCase):
    def test_duplicate_traces_merge_to_one_active(self):
        traces = [
            {
                "trace_id": "trace-a",
                "event_boundary": "same-event",
                "content_summary": "hello",
                "salience_vector": {"emotional": 0.2},
                "source_evidence_refs": ["ref-1"],
                "lifecycle_state": "active",
            },
            {
                "trace_id": "trace-b",
                "event_boundary": "same-event",
                "content_summary": "hello",
                "salience_vector": {"emotional": 0.15},
                "source_evidence_refs": ["ref-2"],
                "lifecycle_state": "active",
            },
            {
                "trace_id": "trace-c",
                "event_boundary": "same-event",
                "content_summary": "hello",
                "salience_vector": {"emotional": 0.1},
                "source_evidence_refs": ["ref-3"],
                "lifecycle_state": "active",
            },
        ]
        report, updated = apply_offline_memory_hygiene(
            memory_trace_store={"traces": traces},
            generated_at="2026-06-16T12:00:00Z",
            trigger_mode="sleep",
        )
        active = [
            trace
            for trace in updated["traces"]
            if trace.get("lifecycle_state") not in {"merged_into", "deprecated"}
        ]
        self.assertEqual(len(active), 1)
        self.assertEqual(len(report["merge_groups"]), 1)
        kept_refs = active[0]["source_evidence_refs"]
        self.assertIn("ref-1", kept_refs)
        self.assertIn("ref-2", kept_refs)

    def test_protected_relationship_trace_not_merged(self):
        traces = [
            {
                "trace_id": "rel-a",
                "memory_kind": "relationship",
                "event_boundary": "rel-event",
                "content_summary": "friend",
                "salience_vector": {"relationship": 0.9},
                "source_evidence_refs": ["rel-ref-1"],
                "lifecycle_state": "active",
            },
            {
                "trace_id": "rel-b",
                "memory_kind": "relationship",
                "event_boundary": "rel-event",
                "content_summary": "friend",
                "salience_vector": {"relationship": 0.8},
                "source_evidence_refs": ["rel-ref-2"],
                "lifecycle_state": "active",
            },
        ]
        report, updated = apply_offline_memory_hygiene(
            memory_trace_store={"traces": traces},
            generated_at="2026-06-16T12:00:00Z",
        )
        protected = report["protected_trace_decisions"]
        self.assertTrue(any(item["decision"] == "preserve" for item in protected))
        active = [
            trace
            for trace in updated["traces"]
            if trace.get("lifecycle_state") not in {"merged_into", "deprecated"}
        ]
        self.assertEqual(len(active), 2)