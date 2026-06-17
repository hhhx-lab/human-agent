import json
import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.resident_turn_writeback import (
    _extract_observed_names_from_turns,
    _merge_observed_names_into_relationship_memory,
)


class ResidentTurnWritebackMemoryTests(unittest.TestCase):
    def test_extracts_relation_person_name_from_current_and_recent_external_turns(self):
        with tempfile.TemporaryDirectory() as tmp:
            dialogue_log = Path(tmp) / "runtime" / "state" / "language" / "dialogue_turn_log.jsonl"
            dialogue_log.parent.mkdir(parents=True)
            dialogue_log.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "speaker": "external",
                                "utterance": "我的名字是何剑宝，记住这个。",
                            },
                            ensure_ascii=False,
                        ),
                        json.dumps(
                            {
                                "speaker": "life",
                                "utterance": "我会记住。",
                            },
                            ensure_ascii=False,
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            names = _extract_observed_names_from_turns(
                dialogue_dir=dialogue_log,
                external_utterance="你可以叫我阿宝。",
            )

        self.assertEqual(names, ["阿宝", "何剑宝"])

    def test_observed_name_merges_into_relationship_memory_cues(self):
        relationship_memory = {
            "schema_version": "relationship_memory_v0",
            "relation_person_profile": {
                "schema_version": "relationship_person_profile_v0",
                "observed_names": ["何剑宝"],
                "profile_source_refs": [],
            },
            "relationship_theme_tags": [],
            "next_wake_cues": [],
        }

        merged = _merge_observed_names_into_relationship_memory(
            relationship_memory,
            observed_names=["何剑宝", "阿宝"],
        )

        profile = merged["relation_person_profile"]
        self.assertEqual(profile["observed_names"], ["何剑宝", "阿宝"])
        self.assertIn("relation_person_identity_memory", merged["relationship_theme_tags"])
        self.assertIn("remember_relation_person_name:何剑宝", merged["next_wake_cues"])
        self.assertIn("remember_relation_person_name:阿宝", merged["next_wake_cues"])

    def test_rejects_noisy_observed_names(self):
        names = _extract_observed_names_from_turns(
            dialogue_dir=Path("/nonexistent/dialogue_turn_log.jsonl"),
            external_utterance="你是哪一种吗？我是 ChatGPT。",
        )
        self.assertEqual(names, [])

    def test_merge_sanitizes_existing_polluted_names(self):
        relationship_memory = {
            "schema_version": "relationship_memory_v0",
            "relation_person_profile": {
                "schema_version": "relationship_person_profile_v0",
                "observed_names": ["何剑宝", "哪一种吗", "ChatGPT"],
                "profile_source_refs": [],
            },
            "relationship_theme_tags": [],
            "next_wake_cues": [],
        }
        merged = _merge_observed_names_into_relationship_memory(
            relationship_memory,
            observed_names=[],
        )
        self.assertEqual(
            merged["relation_person_profile"]["observed_names"],
            ["何剑宝"],
        )


if __name__ == "__main__":
    unittest.main()
