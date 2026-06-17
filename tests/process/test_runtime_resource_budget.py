import json
import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.runtime_resource_budget import (
    append_jsonl_with_hot_budget,
    count_jsonl_events_or_latest_counter,
)


class RuntimeResourceBudgetTests(unittest.TestCase):
    def test_hot_jsonl_rotates_to_archive_and_keeps_tail_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "runtime" / "state" / "terminal" / "idle_heartbeat_trace.jsonl"
            archive_dir = Path(tmp) / "runtime" / "archive" / "resource_budget"
            path.parent.mkdir(parents=True)
            with path.open("a", encoding="utf-8") as handle:
                for counter in range(10):
                    handle.write(
                        json.dumps(
                            {
                                "heartbeat_counter": counter + 1,
                                "payload": "x" * 80,
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

            result = append_jsonl_with_hot_budget(
                path,
                {"heartbeat_counter": 11, "payload": "new"},
                max_bytes=200,
                tail_events=3,
                archive_dir=archive_dir,
            )

            self.assertTrue(result["rotated"])
            archived = list(archive_dir.glob("idle_heartbeat_trace.*.jsonl.gz"))
            summaries = list(archive_dir.glob("idle_heartbeat_trace.*.summary.json"))
            self.assertEqual(len(archived), 1)
            self.assertEqual(len(summaries), 1)
            hot_events = [
                json.loads(line)
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(
                [event["heartbeat_counter"] for event in hot_events],
                [8, 9, 10, 11],
            )
            summary = json.loads(summaries[0].read_text(encoding="utf-8"))
            self.assertEqual(summary["observed_event_count"], 10)
            self.assertEqual(summary["preserved_tail_event_count"], 3)
            self.assertEqual(
                count_jsonl_events_or_latest_counter(path, counter_key="heartbeat_counter"),
                11,
            )


if __name__ == "__main__":
    unittest.main()
