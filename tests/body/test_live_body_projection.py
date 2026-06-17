from __future__ import annotations

import unittest

from life_v0.body.live_body_projection import (
    body_presence_digest,
    project_body_rhythm_pulse_from_live_turn,
    project_need_state_from_live_turn,
)
from life_v0.process_supervisor.resident_turn_writeback import (
    _append_world_contact_episode_to_autobiographical_stack,
)


class LiveBodyProjectionTests(unittest.TestCase):
    def test_live_turn_updates_body_rhythm_pulse(self):
        pulse = project_body_rhythm_pulse_from_live_turn(
            body_rhythm_pulse={},
            generated_at="2026-06-17T00:00:00Z",
            run_id="body-live-test",
            live_turn_focus="relational_checkin",
            core_affect_vector={"arousal": 0.4},
            body_resource_budget={
                "fatigue_state": {"level": "managed_low_noise"},
                "energy_state": {"level": "baseline"},
            },
            external_utterance="你好",
        )
        self.assertEqual(pulse["rhythm_state"], "live_dialogue_engaged")
        self.assertEqual(pulse["generated_at"], "2026-06-17T00:00:00Z")
        self.assertEqual(pulse["live_turn_focus"], "relational_checkin")

    def test_body_presence_digest_includes_world_contact(self):
        digest = body_presence_digest(
            body_rhythm_pulse={"rhythm_state": "live_dialogue_engaged"},
            body_resource_budget={"fatigue_state": {"level": "managed_low_noise"}},
            core_affect_vector={"arousal": 0.5},
            world_contact_summary={
                "release_posture": "shadow_only_guarded",
                "contact_kind": "shadow_observation",
            },
        )
        self.assertEqual(digest["world_contact_posture"], "shadow_only_guarded")
        self.assertEqual(digest["rhythm_state"], "live_dialogue_engaged")

    def test_need_state_social_readiness_engaged_on_live_utterance(self):
        need = project_need_state_from_live_turn(
            need_state_vector={},
            generated_at="2026-06-17T00:00:00Z",
            run_id="need-live-test",
            external_utterance="继续聊",
        )
        self.assertEqual(need["social_readiness"], "dialogic_live_engaged")

    def test_world_contact_episode_appended_to_autobiographical_stack(self):
        stack = _append_world_contact_episode_to_autobiographical_stack(
            {},
            world_contact_summary={
                "release_posture": "shadow_only_guarded",
                "contact_kind": "shadow_observation",
            },
            generated_at="2026-06-17T00:00:00Z",
            live_turn_focus="relational_checkin",
        )
        episodes = stack.get("world_contact_episodes", [])
        self.assertEqual(len(episodes), 1)
        self.assertIn("世界接触", episodes[0]["episode_digest"])


if __name__ == "__main__":
    unittest.main()