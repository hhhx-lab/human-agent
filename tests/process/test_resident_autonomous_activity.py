import json
import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.resident_autonomous_activity import (
    record_resident_autonomous_activity,
)


class ResidentAutonomousActivityTests(unittest.TestCase):
    def test_learning_consolidation_records_configured_web_dream_learning(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "runtime" / "state"
            terminal_dir = state_dir / "terminal"
            dream_dir = state_dir / "dream"
            terminal_dir.mkdir(parents=True)
            dream_dir.mkdir(parents=True)
            (dream_dir / "web_dream_learning_seeds.json").write_text(
                json.dumps(
                    {
                        "schema_version": "web_dream_learning_seeds_v0",
                        "enabled": True,
                        "seed_urls": ["https://example.test/neuroplasticity"],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            calls: list[str] = []

            def fake_fetch(url: str, timeout_seconds: float) -> dict:
                calls.append(url)
                return {
                    "status_code": 200,
                    "final_url": url,
                    "content_type": "text/html",
                    "text": (
                        "<html><head><title>Neuroplasticity and sleep</title></head>"
                        "<body><h1>Memory consolidation during sleep</h1>"
                        "<p>Dreaming can reorganize memory, emotion, and learning.</p>"
                        "</body></html>"
                    ),
                }

            result = None
            for index in range(5):
                result = record_resident_autonomous_activity(
                    terminal_dir=terminal_dir,
                    now_iso=lambda index=index: f"2026-06-13T00:00:0{index}+00:00",
                    web_fetch_url=fake_fetch,
                )

            self.assertEqual(calls, ["https://example.test/neuroplasticity"])
            self.assertIsNotNone(result)
            activity_state = result["activity_state"]
            aggregate_state = result["state"]
            web_state = json.loads(
                (dream_dir / "web_dream_learning_state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(activity_state["activity_kind"], "learning_consolidation")
            self.assertEqual(web_state["status"], "learned")
            self.assertEqual(web_state["page_title"], "Neuroplasticity and sleep")
            self.assertIn("Neuroplasticity and sleep", web_state["topic_candidates"])
            self.assertEqual(
                activity_state["web_dream_learning_state_ref"],
                "runtime/state/dream/web_dream_learning_state.json",
            )
            self.assertEqual(activity_state["web_dream_learning_status"], "learned")
            self.assertIn(
                "runtime/state/dream/web_dream_learning_state.json",
                activity_state["evidence_refs"],
            )
            self.assertEqual(
                aggregate_state["last_web_dream_learning_status"],
                "learned",
            )
            self.assertIn(
                "Neuroplasticity and sleep",
                aggregate_state["last_web_dream_learning_topic_candidates"],
            )
            self.assertIn(
                "wake_question_about:Neuroplasticity and sleep",
                aggregate_state[
                    "last_web_dream_learning_wake_question_candidates"
                ],
            )
            self.assertTrue((dream_dir / "web_dream_learning_log.jsonl").exists())

    def test_web_dream_learning_crosses_idle_lineage_and_life_turn_event(self):
        from life_v0.process_supervisor.background_lineage_state import (
            build_resident_background_lineage_state,
        )
        from life_v0.process_supervisor.dialogue_events import build_life_turn_event
        from life_v0.process_supervisor.idle_strategy import decide_idle_strategy

        autonomous_state = {
            "schema_version": "resident_autonomous_activity_state_v0",
            "status": "active",
            "activity_count": 5,
            "activity_kind_counts": {
                "sleep": 1,
                "memory_recall": 1,
                "self_thinking": 1,
                "growth_rehearsal": 1,
                "learning_consolidation": 1,
            },
            "last_activity_kind": "learning_consolidation",
            "last_activity_at": "2026-06-13T00:00:04+00:00",
            "last_activity_state_ref": (
                "runtime/state/growth/resident_learning_consolidation_state.json"
            ),
            "last_activity_evidence_refs": [
                "runtime/state/dream/web_dream_learning_state.json"
            ],
            "last_web_dream_learning_state_ref": (
                "runtime/state/dream/web_dream_learning_state.json"
            ),
            "last_web_dream_learning_status": "learned",
            "last_web_dream_learning_topic_candidates": [
                "Neuroplasticity and sleep"
            ],
            "last_web_dream_learning_wake_question_candidates": [
                "wake_question_about:Neuroplasticity and sleep"
            ],
            "activity_state_refs": {
                "sleep": "runtime/state/terminal/resident_sleep_cycle_state.json",
                "memory_recall": (
                    "runtime/state/memory/resident_memory_recall_state.json"
                ),
                "self_thinking": (
                    "runtime/state/self/resident_self_thinking_state.json"
                ),
                "growth_rehearsal": (
                    "runtime/state/growth/resident_growth_rehearsal_state.json"
                ),
                "learning_consolidation": (
                    "runtime/state/growth/resident_learning_consolidation_state.json"
                ),
            },
            "current_cycle": [
                "sleep",
                "memory_recall",
                "self_thinking",
                "growth_rehearsal",
                "learning_consolidation",
            ],
            "cycle_phase_index": 4,
            "cycle_phase_count": 5,
            "cycle_completion_count": 1,
            "cycle_coverage_complete": True,
            "covered_activity_kinds": [
                "sleep",
                "memory_recall",
                "self_thinking",
                "growth_rehearsal",
                "learning_consolidation",
            ],
            "missing_activity_kinds": [],
            "next_activity_kind": "sleep",
        }

        idle_state = decide_idle_strategy(
            run_id="web-dream-lineage",
            generated_at="2026-06-13T00:00:05+00:00",
            safe_terminal_loop={},
            terminal_life_loop_state={},
            idle_continuity_frame={},
            replay_cue_bundle={},
            offline_consolidation_frame={},
            growth_patch_candidate_queue={},
            resident_autonomous_activity_state=autonomous_state,
        )
        presence = idle_state["resident_autonomous_activity_presence_profile"]
        self.assertEqual(presence["last_web_dream_learning_status"], "learned")
        self.assertIn(
            "Neuroplasticity and sleep",
            presence["last_web_dream_learning_topic_candidates"],
        )
        self.assertIn(
            "wake_question_about:Neuroplasticity and sleep",
            presence["last_web_dream_learning_wake_question_candidates"],
        )

        lineage = build_resident_background_lineage_state(
            {
                **idle_state,
                "background_lineage_depth_band": "single_carryover",
            },
            governance_phase="waiting_heartbeat_active",
            status="active",
        )
        autonomous_presence = lineage["autonomous_activity_presence"]
        self.assertEqual(
            autonomous_presence["last_web_dream_learning_state_ref"],
            "runtime/state/dream/web_dream_learning_state.json",
        )
        self.assertIn(
            "Neuroplasticity and sleep",
            autonomous_presence["last_web_dream_learning_topic_candidates"],
        )
        self.assertIn(
            "wake_question_about:Neuroplasticity and sleep",
            autonomous_presence[
                "last_web_dream_learning_wake_question_candidates"
            ],
        )

        life_turn = build_life_turn_event(
            turn_id="life-turn-web-dream-learning",
            generated_at="2026-06-13T00:00:06+00:00",
            utterance="继续",
            shared_term_registry={},
            commitment_index={},
            terminal_life_loop_state={
                "resident_background_lineage_state": lineage
            },
        )
        self.assertEqual(
            life_turn["resident_background_lineage_web_dream_learning_status"],
            "learned",
        )
        self.assertIn(
            "Neuroplasticity and sleep",
            life_turn[
                "resident_background_lineage_web_dream_learning_topic_candidates"
            ],
        )
        self.assertIn(
            "wake_question_about:Neuroplasticity and sleep",
            life_turn[
                "resident_background_lineage_web_dream_learning_wake_question_candidates"
            ],
        )
        self.assertIn(
            "runtime/state/dream/web_dream_learning_state.json",
            life_turn["resident_background_lineage_autonomous_activity_refs"],
        )

    def test_learning_consolidation_without_seed_does_not_fetch(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp) / "runtime" / "state"
            terminal_dir = state_dir / "terminal"
            terminal_dir.mkdir(parents=True)

            def forbidden_fetch(url: str, timeout_seconds: float) -> dict:
                raise AssertionError("web fetch should not run without configured seeds")

            for index in range(5):
                result = record_resident_autonomous_activity(
                    terminal_dir=terminal_dir,
                    now_iso=lambda index=index: f"2026-06-13T00:00:0{index}+00:00",
                    web_fetch_url=forbidden_fetch,
                )

            web_state = json.loads(
                (state_dir / "dream" / "web_dream_learning_state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(web_state["status"], "disabled")
            self.assertEqual(result["activity_state"]["web_dream_learning_status"], "disabled")


if __name__ == "__main__":
    unittest.main()
