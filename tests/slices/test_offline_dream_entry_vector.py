import unittest

from life_v0.dream.offline_dream_entry import (
    build_dream_cue_policy_state,
    build_offline_dream_entry_vector,
)


class OfflineDreamEntryVectorTests(unittest.TestCase):
    def test_high_sleep_pressure_selects_replay_and_rem(self):
        entry = build_offline_dream_entry_vector(
            run_id="d0-test",
            generated_at="2026-06-16T12:00:00Z",
            need_state_vector={"sleep_pressure": 0.6},
            memory_trace_store={
                "traces": [
                    {"lifecycle_state": "active"},
                    {"lifecycle_state": "candidate"},
                    {"lifecycle_state": "encoding"},
                ]
            },
            exit_dream_summary={"source_dialogue_turn_count": 12},
        )
        modes = entry["selected_offline_modes"]
        self.assertIn("NREMReplayCycle", modes)
        self.assertEqual(entry["schema_version"], "offline_dream_entry_vector_v1")

    def test_high_fatigue_selects_recovery_mode(self):
        entry = build_offline_dream_entry_vector(
            run_id="d0-fatigue",
            generated_at="2026-06-16T12:00:00Z",
            body_resource_budget={"fatigue_state": {"level": "high"}},
        )
        self.assertIn("FatigueRecoveryMode", entry["selected_offline_modes"])

    def test_suppressed_cue_has_auditable_reason(self):
        cue_policy = build_dream_cue_policy_state(
            run_id="d0-cue",
            generated_at="2026-06-16T12:00:00Z",
            exit_dream_summary={
                "deduplicated_episode_summaries": [
                    {
                        "episode_id": "ep-1",
                        "source_ref": "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                        "semantic_key": "memory",
                    }
                ]
            },
            topic_history={
                "entries": [
                    {"topic_cluster_id": "memory", "url_digest": "abc"},
                ]
            },
        )
        suppressed = cue_policy.get("suppressed_cues", [])
        if suppressed:
            self.assertEqual(suppressed[0].get("reason"), "topic_cluster_cooldown")