import unittest

from life_v0.state_store.cortical_memory_transfer import apply_cortical_memory_transfer
from life_v0.state_store.cross_modal_evidence import collect_cross_modal_source_evidence
from life_v0.state_store.memory_engineering_completion_gate import (
    build_memory_engineering_completion_gate,
)
from life_v0.state_store.memory_longitudinal_profile import (
    project_memory_longitudinal_profile_from_live_turn,
)
from life_v0.state_store.memory_trace_store import build_memory_trace_store
from life_v0.state_store.offline_memory_consolidation import (
    apply_offline_memory_consolidation,
)
from tests.slices.test_memory_u10_u12_human_parity_scorecard import (
    _month_scale_memory_fixture,
)


class MemoryU20U24EngineeringCompletionTests(unittest.TestCase):
    def test_u20_visual_feature_encoding_present_on_bundle(self):
        evidence = collect_cross_modal_source_evidence(
            world_observation_route={
                "visual_scene_refs": [
                    "runtime/state/observation/world_observation_route.json#scene-a"
                ]
            },
            periphery_normalization_trace={"promoted_channels": ["visual_channel_live"]},
            visual_percept_present=True,
        )
        bundle = evidence.get("cross_modal_feature_bundle") or {}
        self.assertTrue(bundle.get("visual_feature_encoding_present"))
        visual_feature = next(
            (
                feature.get("visual_feature_encoding")
                for feature in bundle.get("modality_features", [])
                if feature.get("modality") == "visual_percept"
            ),
            None,
        )
        self.assertIsNotNone(visual_feature)
        self.assertEqual(
            visual_feature.get("encoding_kind"),
            "scene_layout_and_channel_fingerprint",
        )

    def test_u21_cortical_transfer_marks_replayed_traces(self):
        store = build_memory_trace_store(
            run_id="u21-cortical",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-2",
                ],
                "external_utterance": "episode one",
                "semantic_focus": "relationship_continuity_and_repair",
                "replay_salience": 0.7,
                "accessibility_score": 0.72,
            },
        )
        live_trace_id = next(
            trace["trace_id"]
            for trace in store.get("traces", [])
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        )
        store["traces"] = [
            {
                **trace,
                "offline_replay_count": 2,
                "replay_salience": 0.72,
            }
            if trace.get("trace_id") == live_trace_id
            else trace
            for trace in store.get("traces", [])
        ]
        result = apply_cortical_memory_transfer(
            memory_trace_store=store,
            life_schema_map={},
            replay_trace_ids=[live_trace_id],
            generated_at="2026-06-16T01:00:00+00:00",
            swr_replay_weights=[{"trace_id": live_trace_id, "swr_weight": 0.81}],
        )
        updated = result["memory_trace_store"]
        trace = next(
            item
            for item in updated.get("traces", [])
            if item.get("trace_id") == live_trace_id
        )
        self.assertEqual(trace.get("cortical_transfer_state"), "cortical_linked")
        self.assertTrue(result.get("cortical_transfer_diff"))

    def test_u21_offline_consolidation_emits_cortical_transfer_diff(self):
        store = build_memory_trace_store(
            run_id="u21-offline",
            generated_at="2026-06-16T00:00:00+00:00",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-3",
                    "runtime/state/language/dialogue_turn_log.jsonl#line-4",
                ],
                "external_utterance": "episode two",
                "semantic_focus": "relationship_continuity_and_repair",
                "replay_salience": 0.74,
                "accessibility_score": 0.7,
            },
        )
        result = apply_offline_memory_consolidation(
            run_id="u21-offline",
            generated_at="2026-06-16T02:00:00+00:00",
            memory_trace_store=store,
        )
        diff = (result.get("memory_consolidation_report") or {}).get(
            "consolidation_diff", {}
        )
        self.assertTrue(diff.get("cortical_transfer_diff"))
        self.assertEqual(
            (result.get("memory_consolidation_report") or {}).get(
                "cortical_transfer_policy"
            ),
            "swr_replay_then_cortical_slow_integration",
        )

    def test_u22_process_long_run_evidence_tracks_turn_count(self):
        profile = {"turn_count": 0, "offline_cycle_count": 0}
        for turn in range(5):
            profile = project_memory_longitudinal_profile_from_live_turn(
                profile=profile,
                run_id="u22-process",
                generated_at=f"2026-06-16T0{turn}:00:00+00:00",
            )
        evidence = profile.get("process_long_run_evidence") or {}
        self.assertEqual(evidence.get("process_turn_count"), 5)

    def test_u24_engineering_completion_gate_reaches_100_percent(self):
        fixture = _month_scale_memory_fixture()
        from life_v0.state_store.memory_capability_scorecard import (
            build_memory_capability_scorecard,
        )

        scorecard = build_memory_capability_scorecard(
            run_id="u24-scorecard",
            generated_at="2026-06-16T17:00:00+00:00",
            memory_trace_store=fixture["trace_store"],
            memory_retrieval_frame=fixture["memory_retrieval_frame"],
            relationship_memory=fixture["relationship_memory"],
            autobiographical_stack=fixture["autobiographical_stack"],
            life_schema_map=fixture["life_schema_map"],
            memory_longitudinal_profile=fixture["memory_longitudinal_profile"],
            memory_consolidation_report=fixture["memory_consolidation_report"],
            fast_episodic_buffer=fixture["fast_episodic_buffer"],
            engram_cluster=fixture["engram_cluster"],
            pattern_separation_index=fixture["pattern_separation_index"],
            hippocampal_cue_index=fixture["hippocampal_cue_index"],
            pattern_completion_frame=fixture["pattern_completion_frame"],
        )
        gate = build_memory_engineering_completion_gate(
            run_id="u24-gate",
            generated_at="2026-06-16T17:00:00+00:00",
            memory_capability_scorecard=scorecard,
            memory_trace_store=fixture["trace_store"],
            memory_retrieval_frame=fixture["memory_retrieval_frame"],
            memory_consolidation_report=fixture["memory_consolidation_report"],
            memory_longitudinal_profile=fixture["memory_longitudinal_profile"],
            hippocampal_cue_index=fixture["hippocampal_cue_index"],
            pattern_completion_frame=fixture["pattern_completion_frame"],
        )
        self.assertTrue(gate["engineering_complete"])
        self.assertEqual(gate["engineering_completion_pct"], 100.0)
        self.assertFalse(gate["at_biological_human_parity"])


if __name__ == "__main__":
    unittest.main()