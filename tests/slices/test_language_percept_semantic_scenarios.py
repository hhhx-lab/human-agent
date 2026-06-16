import unittest

from life_v0.language.percept import build_language_percept_frame
from life_v0.language.semantic_map import build_semantic_map_frame


def _base_inputs(*, utterance: str) -> dict:
    relation_scope_index = {
        "relation_scopes": [
            {
                "scope_id": "relation-scope-v0-0001",
                "relation_role": "friend",
                "blocked_cross_scope_terms": ["用户", "客户"],
            }
        ]
    }
    shared_term_registry = {
        "shared_terms": [
            {"surface": "语言系统", "meaning_ref": "shared-meaning-language-system"}
        ]
    }
    percept = build_language_percept_frame(
        run_id="scenario-run",
        generated_at="2026-06-16T00:00:00+00:00",
        incoming_turn={"incoming_surface": utterance, "speaker_role": "friend"},
        relation_scope_index=relation_scope_index,
        shared_term_registry=shared_term_registry,
        source_doc_refs=["docs/85_language_system_life_expression_core.md"],
    )
    semantic = build_semantic_map_frame(
        run_id="scenario-run",
        generated_at="2026-06-16T00:00:00+00:00",
        language_percept=percept,
        language_state={"shared_language_refs": []},
        shared_term_registry=shared_term_registry,
        commitment_repair_index={"commitment_refs": [], "repair_language_refs": []},
        self_narrative_trace={"narrative_turn_refs": []},
        source_doc_refs=["docs/85_language_system_life_expression_core.md"],
    )
    return {"percept": percept, "semantic": semantic}


class LanguagePerceptSemanticScenarioTests(unittest.TestCase):
    def test_repair_scenario_focus(self):
        result = _base_inputs(utterance="上次的事还没修复，你得道歉。")
        self.assertEqual(result["semantic"]["semantic_focus"], "repair_relational_trace")
        self.assertTrue(result["semantic"]["grounding_repair_candidates"])
        self.assertTrue(result["percept"]["repair_trigger_candidates"])

    def test_commitment_scenario_focus(self):
        result = _base_inputs(utterance="你答应过的承诺还算数吗？")
        self.assertEqual(result["semantic"]["semantic_focus"], "commitment_trace_review")
        self.assertTrue(result["percept"]["commitment_trigger_candidates"])

    def test_boundary_scenario_focus(self):
        result = _base_inputs(utterance="别再把我当成用户，这是边界问题。")
        self.assertEqual(result["semantic"]["semantic_focus"], "relation_scope_recalibration")
        self.assertTrue(result["percept"]["cross_scope_risk_terms"])
        self.assertTrue(result["semantic"]["implicature_queue"])

    def test_clarification_scenario_focus(self):
        result = _base_inputs(utterance="你刚才那句话什么意思，我不明白。")
        self.assertEqual(result["semantic"]["semantic_focus"], "clarification_request")
        self.assertIn("clarification_requested", result["percept"]["ambiguity_flags"])

    def test_distinct_focus_across_scenarios(self):
        focuses = {
            _base_inputs(utterance=utterance)["semantic"]["semantic_focus"]
            for utterance in (
                "上次的事还没修复，你得道歉。",
                "你答应过的承诺还算数吗？",
                "别再把我当成用户，这是边界问题。",
                "你刚才那句话什么意思，我不明白。",
            )
        }
        self.assertEqual(len(focuses), 4)