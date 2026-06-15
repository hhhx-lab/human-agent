import json
import tempfile
import unittest
from pathlib import Path

from life_v0.language.percept import build_language_percept_frame
from life_v0.language.percept_input import resolve_incoming_turn_for_language_build
from life_v0.language.relation_scope import build_relation_scope_language_index
from life_v0.language.shared_terms import build_shared_term_registry


class PerceptInputTests(unittest.TestCase):
    def _base_inputs(self) -> dict:
        source_doc_refs = ["docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md"]
        return {
            "relation_scope_index": build_relation_scope_language_index(
                run_id="percept-input-test",
                generated_at="2026-06-15T00:00:00+00:00",
                source_doc_refs=source_doc_refs,
            ),
            "shared_term_registry": build_shared_term_registry(
                run_id="percept-input-test",
                generated_at="2026-06-15T00:00:00+00:00",
                source_doc_refs=source_doc_refs,
            ),
            "commitment_repair_index": {
                "repair_obligation_refs": ["repair-obligation-001"],
                "commitment_refs": ["commitment-v0-0001"],
            },
        }

    def test_resolve_prefers_dialogue_turn_log_external_utterance(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "runtime" / "state"
            language_dir = state_dir / "language"
            language_dir.mkdir(parents=True, exist_ok=True)
            dialogue_log = language_dir / "dialogue_turn_log.jsonl"
            dialogue_log.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "schema_version": "dialogue_turn_event_v0",
                                "turn_id": "life-turn-001",
                                "event_role": "digital_life_turn",
                                "utterance": "我会先确认关系语境。",
                            },
                            ensure_ascii=False,
                        ),
                        json.dumps(
                            {
                                "schema_version": "dialogue_turn_event_v0",
                                "turn_id": "external-turn-002",
                                "event_role": "external_relation_turn",
                                "relation_role": "friend",
                                "utterance": "你还记得我们共同语言里的修复约定吗？",
                            },
                            ensure_ascii=False,
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            inputs = self._base_inputs()
            resolved = resolve_incoming_turn_for_language_build(
                state_dir=state_dir,
                **inputs,
            )

        self.assertEqual(resolved["percept_input_mode"], "dialogue_turn_log")
        self.assertEqual(
            resolved["incoming_turn"]["incoming_surface"],
            "你还记得我们共同语言里的修复约定吗？",
        )

    def test_resolve_bootstraps_from_relationship_evidence_without_fixture_sentence(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "runtime" / "state"
            inputs = self._base_inputs()
            resolved = resolve_incoming_turn_for_language_build(
                state_dir=state_dir,
                **inputs,
            )
            percept = build_language_percept_frame(
                run_id="percept-input-test",
                generated_at="2026-06-15T00:00:00+00:00",
                incoming_turn=resolved["incoming_turn"],
                relation_scope_index=inputs["relation_scope_index"],
                shared_term_registry=inputs["shared_term_registry"],
                source_doc_refs=[
                    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md"
                ],
            )

        self.assertEqual(
            resolved["percept_input_mode"],
            "relationship_evidence_bootstrap",
        )
        self.assertNotIn(
            "还记得吗",
            resolved["incoming_turn"]["incoming_surface"],
        )
        self.assertIn("共同语言", percept["shared_term_hits"])
        self.assertTrue(percept["repair_trigger_candidates"])


if __name__ == "__main__":
    unittest.main()