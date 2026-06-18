from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from life_v0.neural_core.broadcast import project_broadcast_frame_from_live_turn
from life_v0.neural_core.workspace import (
    apply_workspace_topk,
    is_workspace_topk_enabled,
    maybe_apply_workspace_topk_to_frame,
    resolve_workspace_k,
)
from life_v0.process_supervisor.pre_expression_consciousness_refresh import (
    refresh_pre_expression_consciousness,
)
from life_v0.replay import append_workspace_evictions_to_replay_cue_bundle


class WorkspaceTopKTests(unittest.TestCase):
    def test_disabled_by_default(self):
        self.assertFalse(is_workspace_topk_enabled({}))

    def test_high_fatigue_reduces_k(self):
        low_k = resolve_workspace_k(cognitive_bandwidth=0.8, fatigue_load=0.1)
        high_k = resolve_workspace_k(cognitive_bandwidth=0.8, fatigue_load=0.9)
        self.assertGreater(low_k, high_k)

    def test_apply_workspace_topk_evicts_lower_salience(self):
        candidates = [
            {"explanation_id": "exp-low", "focus": "background_noise", "salience_score": 0.2},
            {"explanation_id": "exp-high", "focus": "repair_commitment", "salience_score": 0.4},
            {"explanation_id": "exp-mid", "focus": "relationship_continuity", "salience_score": 0.35},
        ]
        result = apply_workspace_topk(candidates, k=2)
        winner_ids = [item["explanation_id"] for item in result.winners]
        evicted_ids = [item["explanation_id"] for item in result.evicted]
        self.assertEqual(len(result.winners), 2)
        self.assertIn("exp-high", winner_ids)
        self.assertIn("exp-low", evicted_ids)

    def test_broadcast_primary_secondary_from_topk(self):
        workspace_frame = {
            "schema_version": "workspace_frame_v0",
            "candidate_explanations": [
                {"explanation_id": "exp-1", "focus": "repair_commitment", "salience_score": 0.9},
                {"explanation_id": "exp-2", "focus": "relationship_continuity", "salience_score": 0.7},
            ],
            "workspace_topk_applied": True,
            "workspace_topk": {
                "k": 2,
                "evicted_candidate_refs": ["exp-3"],
                "suppressed_candidates": [
                    {"explanation_id": "exp-3", "focus": "dream_residue"},
                ],
            },
            "broadcast_targets": ["LanguageRelationshipRuntime"],
        }
        broadcast = project_broadcast_frame_from_live_turn(
            broadcast_frame={},
            generated_at="2026-06-17T01:00:00Z",
            workspace_frame=workspace_frame,
            run_id="topk-broadcast",
        )
        self.assertEqual(broadcast["primary_broadcast"]["explanation_id"], "exp-1")
        self.assertEqual(broadcast["secondary_broadcast"]["explanation_id"], "exp-2")
        self.assertEqual(broadcast["workspace_topk_k"], 2)
        self.assertIn("exp-3", broadcast["suppressed_content_refs"])

    def test_evicted_candidates_append_to_replay_bundle(self):
        updated = append_workspace_evictions_to_replay_cue_bundle(
            {"schema_version": "replay_cue_bundle_v0", "dream_entry_candidates": []},
            evicted_candidates=[
                {"explanation_id": "exp-evicted", "focus": "dream_residue"},
            ],
            generated_at="2026-06-17T02:00:00Z",
            run_id="replay-run",
        )
        self.assertTrue(updated["workspace_topk_replay_applied"])
        self.assertTrue(updated["dream_entry_candidates"])
        self.assertTrue(updated["anti_forgetting_targets"])

    def test_pre_expression_refresh_applies_topk_when_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_dir = Path(tmp)
            for sub in (
                "consciousness",
                "neural_life_core",
                "memory",
                "prediction",
                "language",
                "signal",
                "body",
                "replay",
            ):
                (state_dir / sub).mkdir(parents=True)

            (state_dir / "prediction" / "prediction_workspace_frame.json").write_text(
                json.dumps(
                    {
                        "workspace_contents": {
                            "candidate_explanations": [
                                {"explanation_id": "exp-1", "focus": "repair_commitment"},
                                {"explanation_id": "exp-2", "focus": "relationship_continuity"},
                                {"explanation_id": "exp-3", "focus": "dream_residue"},
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "body" / "body_integrator_state.json").write_text(
                json.dumps(
                    {
                        "continuous": {
                            "cognitive_bandwidth": 0.35,
                            "allostatic_load": 0.2,
                        }
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "signal" / "signal_media_runtime.json").write_text(
                json.dumps({"modulation_vector": {"fatigue_load": 0.75}}),
                encoding="utf-8",
            )
            (state_dir / "replay" / "replay_cue_bundle.json").write_text(
                json.dumps({"schema_version": "replay_cue_bundle_v0"}),
                encoding="utf-8",
            )

            def write_json(path: Path, payload: dict) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload), encoding="utf-8")

            import os

            old = os.environ.get("DIGITAL_LIFE_WORKSPACE_TOPK")
            os.environ["DIGITAL_LIFE_WORKSPACE_TOPK"] = "1"
            try:
                result = refresh_pre_expression_consciousness(
                    state_dir=state_dir,
                    run_id="topk-pre-expression",
                    generated_at="2026-06-17T03:00:00Z",
                    live_turn_focus="repair_commitment",
                    write_json=write_json,
                )
            finally:
                if old is None:
                    os.environ.pop("DIGITAL_LIFE_WORKSPACE_TOPK", None)
                else:
                    os.environ["DIGITAL_LIFE_WORKSPACE_TOPK"] = old

            self.assertTrue(result.workspace_frame.get("workspace_topk_applied"))
            self.assertLessEqual(
                len(result.workspace_frame.get("candidate_explanations", [])),
                2,
            )
            self.assertIsNotNone(result.broadcast_frame.get("primary_broadcast"))
            replay_bundle = json.loads(
                (state_dir / "replay" / "replay_cue_bundle.json").read_text(encoding="utf-8")
            )
            if result.workspace_frame.get("workspace_topk", {}).get("evicted_count"):
                self.assertTrue(replay_bundle.get("workspace_topk_replay_applied"))

    def test_maybe_apply_noop_when_disabled(self):
        frame = maybe_apply_workspace_topk_to_frame(
            {
                "candidate_explanations": [
                    {"explanation_id": "exp-1", "focus": "repair"},
                    {"explanation_id": "exp-2", "focus": "dream"},
                ]
            },
            environ={"DIGITAL_LIFE_WORKSPACE_TOPK": "0"},
        )
        self.assertFalse(frame.get("workspace_topk_applied"))


if __name__ == "__main__":
    unittest.main()