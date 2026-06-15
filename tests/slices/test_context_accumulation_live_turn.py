import unittest

from life_v0.terminal_turn.context_accumulation import (
    project_context_accumulation_window_from_live_turn,
)
from life_v0.terminal_turn.turn_transition import (
    project_turn_transition_trace_from_live_turn,
)


class ContextAccumulationLiveTurnTests(unittest.TestCase):
    def test_project_context_accumulation_window_from_live_turn(self):
        updated = project_context_accumulation_window_from_live_turn(
            context_accumulation={
                "schema_version": "context_accumulation_window_v0",
                "status": "closed",
                "shared_term_surfaces": ["旧约定"],
                "dialogue_turn_restore_refs": ["turn:1"],
            },
            generated_at="2026-06-15T12:00:00Z",
            relationship_graph={
                "subjects": [
                    {
                        "relationship_id": "rel-v0-0001",
                        "relation_role": "friend",
                        "relationship_stage": "repair_guarded_continuity",
                    }
                ]
            },
            language_percept={
                "shared_term_hits": ["我们的叫法"],
                "semantic_focus": "repair_commitment_shared_language",
            },
            semantic_map={
                "semantic_focus": "repair_commitment_shared_language",
                "shared_meaning_bindings": [
                    {"surface": "旧约定", "meaning_ref": "meaning:old-pact"}
                ],
            },
            commitment_truth_state={
                "open_commitment_refs": ["commitment:open-1"],
            },
            dialogue_turn_refs=[
                "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                "runtime/state/language/dialogue_turn_log.jsonl#line-3",
            ],
            live_language_turn_refs=["dialogue-turn-live-0003"],
            live_turn_focus="repair_commitment_shared_language",
            run_id="live-turn-0003",
        )

        self.assertEqual(updated["schema_version"], "context_accumulation_window_v0")
        self.assertEqual(updated["current_relation_role"], "friend")
        self.assertEqual(updated["semantic_focus"], "repair_commitment_shared_language")
        self.assertIn("我们的叫法", updated["shared_term_surfaces"])
        self.assertEqual(
            updated["dialogue_turn_restore_refs"][-1],
            "runtime/state/language/dialogue_turn_log.jsonl#line-3",
        )
        self.assertEqual(
            updated["last_projected_from_live_turn_ref"],
            "runtime/state/language/dialogue_turn_log.jsonl#line-3",
        )
        self.assertIn("commitment:open-1", updated["unresolved_commitment_refs"])

    def test_project_turn_transition_trace_from_live_turn(self):
        updated = project_turn_transition_trace_from_live_turn(
            turn_transition={
                "schema_version": "turn_transition_trace_v0",
                "transition_kind": "birth_restore_to_first_terminal_turn",
                "to_stage": "ready_for_first_terminal_turn",
            },
            generated_at="2026-06-15T12:00:00Z",
            dialogue_turn_refs=[
                "runtime/state/language/dialogue_turn_log.jsonl#line-3",
            ],
            live_language_turn_refs=["dialogue-turn-live-0003"],
            live_turn_focus="repair_commitment_shared_language",
            semantic_focus="repair_commitment_shared_language",
            unresolved_commitment_refs=["commitment:open-1"],
            run_id="live-turn-0003",
        )

        self.assertEqual(updated["transition_kind"], "live_relation_turn")
        self.assertEqual(updated["to_stage"], "resumed_external_dialogue_loop")
        self.assertEqual(updated["semantic_focus"], "repair_commitment_shared_language")
        self.assertEqual(
            updated["last_projected_from_live_turn_ref"],
            "runtime/state/language/dialogue_turn_log.jsonl#line-3",
        )
        self.assertIn(
            "runtime/state/terminal/context_accumulation_window.json",
            updated["context_accumulation_restore_refs"],
        )


if __name__ == "__main__":
    unittest.main()