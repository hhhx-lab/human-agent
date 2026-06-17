from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from life_v0.tools.sanitize_relationship_memory import sanitize_runtime_memory_files


class SanitizeRelationshipMemoryToolTests(unittest.TestCase):
    def test_sanitizes_relationship_and_dialogue_observed_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "runtime" / "state"
            memory_dir = state_dir / "memory"
            memory_dir.mkdir(parents=True)
            relationship_path = memory_dir / "relationship_memory.json"
            dialogue_path = memory_dir / "dialogue_memory_summary.json"
            relationship_path.write_text(
                json.dumps(
                    {
                        "schema_version": "relationship_memory_v0",
                        "relation_person_profile": {
                            "observed_names": ["何剑宝", "哪一种吗", "ChatGPT"]
                        },
                        "relationship_theme_tags": ["digital_life"],
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            dialogue_path.write_text(
                json.dumps(
                    {
                        "schema_version": "dialogue_memory_summary_v0",
                        "relation_person_profile": {
                            "observed_names": ["GPT", "阿宝"]
                        },
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )

            report = sanitize_runtime_memory_files(state_dir=state_dir)
            relationship = json.loads(relationship_path.read_text(encoding="utf-8"))
            dialogue = json.loads(dialogue_path.read_text(encoding="utf-8"))

        self.assertEqual(report["sanitized_file_count"], 2)
        self.assertEqual(
            relationship["relation_person_profile"]["observed_names"],
            ["何剑宝"],
        )
        self.assertEqual(
            dialogue["relation_person_profile"]["observed_names"],
            ["阿宝"],
        )
        self.assertEqual(relationship["relationship_theme_tags"], ["digital_life"])


if __name__ == "__main__":
    unittest.main()
