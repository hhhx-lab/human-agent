import unittest

from life_v0.state_store.engram_index import engram_live_turn_chain_inspection_snapshot


class EngramLiveTurnChainTests(unittest.TestCase):
    def test_chain_closed_when_live_dialogue_refs_present(self):
        snapshot = engram_live_turn_chain_inspection_snapshot(
            engram_index={
                "live_dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ],
                "live_language_turn_refs": [
                    "runtime/state/language/language_turn_log.jsonl#line-1"
                ],
                "last_projected_from_live_turn_ref": (
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                ),
            },
            life_state={
                "memory_index": {
                    "live_dialogue_turn_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-1"
                    ]
                }
            },
            dialogue_memory_summary={"dialogue_turn_count": 1},
        )
        self.assertTrue(snapshot["engram_live_turn_chain_closed"])
        self.assertEqual(snapshot["engram_live_turn_chain_alignment"], "closed")
        self.assertEqual(snapshot["live_dialogue_turn_ref_count"], 1)

    def test_chain_open_when_dialogue_grows_without_engram_refs(self):
        snapshot = engram_live_turn_chain_inspection_snapshot(
            engram_index={"live_dialogue_turn_refs": []},
            life_state={"memory_index": {}},
            dialogue_memory_summary={"dialogue_turn_count": 3},
        )
        self.assertFalse(snapshot["engram_live_turn_chain_closed"])
        self.assertEqual(
            snapshot["engram_live_turn_chain_alignment"],
            "open_missing_live_dialogue_turn_refs",
        )


if __name__ == "__main__":
    unittest.main()