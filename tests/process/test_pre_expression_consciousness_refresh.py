from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from life_v0.neural_core.metacognition import project_metacognition_state_from_live_turn
from life_v0.process_supervisor.model_expression import _conscious_self_summary
from life_v0.process_supervisor.pre_expression_consciousness_refresh import (
    refresh_pre_expression_consciousness,
)


class PreExpressionConsciousnessRefreshTests(unittest.TestCase):
    def test_refresh_updates_consciousness_frames_before_expression(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_dir = root / "state"
            for sub in (
                "consciousness",
                "neural_life_core",
                "memory",
                "prediction",
                "language",
            ):
                (state_dir / sub).mkdir(parents=True)

            (state_dir / "prediction" / "prediction_workspace_frame.json").write_text(
                json.dumps(
                    {
                        "workspace_contents": {
                            "candidate_explanations": [
                                {
                                    "explanation_id": "semantic-focus-v0-0001",
                                    "focus": "relational_checkin",
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "language" / "repair_closeout_state.json").write_text(
                json.dumps({"closeout_phase": "dormant"}),
                encoding="utf-8",
            )

            def write_json(path: Path, payload: dict) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload), encoding="utf-8")

            result = refresh_pre_expression_consciousness(
                state_dir=state_dir,
                run_id="pre-expression-test",
                generated_at="2026-06-17T00:00:00Z",
                live_turn_focus="relational_checkin",
                memory_retrieval_frame={
                    "reconstruction_focus": "relationship_continuity_reconstruction"
                },
                write_json=write_json,
            )

            self.assertEqual(
                result.broadcast_frame.get("live_turn_focus"),
                "relational_checkin",
            )
            self.assertEqual(
                result.metacognition_state.get("dominant_self_narrative"),
                "continuity_primary",
            )
            self.assertEqual(
                result.workspace_frame.get("generated_at"),
                "2026-06-17T00:00:00Z",
            )

    def test_conscious_self_summary_includes_salience_and_traits(self):
        summary = _conscious_self_summary(
            broadcast_frame={
                "live_turn_focus": "relational_checkin",
                "salience_ranking": [{"focus": "relational_checkin"}],
            },
            metacognition_state={
                "dominant_self_narrative": "continuity_primary",
                "memory_reconstruction_focus": "relationship_continuity_reconstruction",
            },
            self_model_state={
                "trait_slow_variables": {
                    "continuity_drive": 0.8,
                    "boundary_respect": 0.7,
                }
            },
            autobiographical_stack={
                "episodes": [{"episode_digest": "一起继续聊天"}]
            },
            semantic_map={"semantic_focus": "relational_checkin"},
        )
        self.assertEqual(summary["dominant_self_narrative"], "continuity_primary")
        self.assertIn("relational_checkin", summary["salience_focuses"])
        self.assertIn("continuity_drive", summary["trait_slow_variable_names"])

    def test_metacognition_repair_narrative_when_closeout_active(self):
        updated = project_metacognition_state_from_live_turn(
            metacognition_state={},
            generated_at="2026-06-17T00:00:00Z",
            broadcast_frame={"broadcast_targets": ["AffectiveSelfRuntime"]},
            workspace_frame={"broadcast_targets": ["LanguageRelationshipRuntime"]},
            run_id="meta-test",
            live_turn_focus="repair_relational_trace",
            repair_closeout_state={"closeout_phase": "active_repair"},
        )
        self.assertEqual(updated["dominant_self_narrative"], "repair_active")


if __name__ == "__main__":
    unittest.main()