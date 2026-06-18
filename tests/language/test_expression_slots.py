from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from life_v0.language.expression_monitor import (
    apply_expression_slots_from_live_state,
    compute_proactive_drive_scalar,
    expression_plan_slots_summary,
    is_expression_slots_enabled,
    maybe_append_episodic_speech_ref,
)
from life_v0.process_supervisor.model_expression import (
    _model_visible_expression_context,
    build_model_expression_context,
)
from life_v0.process_supervisor.proactive_terminal_voice import (
    build_resident_proactive_terminal_event,
)
from life_v0.process_supervisor.terminal_inspection_compose import (
    _build_express_inspection,
)
class ExpressionSlotsTests(unittest.TestCase):
    def test_disabled_by_default(self):
        self.assertFalse(is_expression_slots_enabled({}))

    def test_apply_expression_slots_projects_workspace_and_body_scalars(self):
        plan = {
            "schema_version": "expression_plan_v0",
            "semantic_goal": "relationship_repair",
            "fatigue_pressure": "baseline",
        }
        updated = apply_expression_slots_from_live_state(
            expression_plan=plan,
            workspace_frame={
                "candidate_explanations": [
                    {
                        "explanation_id": "exp-primary",
                        "focus": "repair_commitment",
                        "salience_score": 0.9,
                    },
                    {
                        "explanation_id": "exp-secondary",
                        "focus": "relationship_continuity",
                        "salience_score": 0.7,
                    },
                ],
                "workspace_topk": {"k": 2},
            },
            broadcast_frame={
                "primary_broadcast": {
                    "explanation_id": "exp-primary",
                    "focus": "repair_commitment",
                },
                "secondary_broadcast": {
                    "explanation_id": "exp-secondary",
                    "focus": "relationship_continuity",
                },
            },
            body_integrator={
                "continuous": {
                    "cognitive_bandwidth": 0.71,
                    "allostatic_load": 0.22,
                    "sleep_pressure": 0.18,
                }
            },
            network_state={
                "dominant_network": "default_mode_network",
                "active_networks": [
                    {
                        "network_id": "default_mode_network",
                        "mode": "background_self_narrative",
                    }
                ],
            },
            environ={"DIGITAL_LIFE_EXPRESSION_SLOTS": "true"},
        )
        self.assertTrue(updated["expression_slots_applied"])
        self.assertEqual(updated["workspace_primary_focus"], "repair_commitment")
        self.assertEqual(updated["workspace_topk_k"], 2)
        self.assertEqual(updated["cognitive_bandwidth_scalar"], 0.71)
        self.assertEqual(updated["workspace_broadcast_primary_ref"], "exp-primary")
        self.assertEqual(updated["dmn_network_mode"], "background_self_narrative")
        self.assertTrue(updated["dmn_network_dominant"])
        self.assertIsNotNone(updated["proactive_drive_scalar"])

    def test_model_expression_context_uses_slots_when_enabled(self):
        runtime = type(
            "Cfg",
            (),
            {"response_language": "zh-CN", "dialogue_style": "relationship"},
        )()
        expression_plan = {
            "expression_slots_applied": True,
            "semantic_goal": "relationship_repair",
            "workspace_primary_focus": "repair_commitment",
            "workspace_topk_k": 2,
            "cognitive_bandwidth_scalar": 0.71,
            "allostatic_load_scalar": 0.22,
            "workspace_broadcast_primary_ref": "exp-primary",
            "fatigue_pressure": "baseline",
            "release_caution_level": "baseline",
            "repair_pressure": 1,
        }
        with mock.patch(
            "life_v0.process_supervisor.model_expression.is_expression_slots_enabled",
            return_value=True,
        ):
            context = build_model_expression_context(
                external_utterance="你好",
                audited_expression_material='{"schema_version":"audited_v0"}',
                runtime_config=runtime,
                relationship_graph={
                    "subjects": [{"relation_role": "friend", "relationship_stage": "warm"}]
                },
                relationship_timeline={
                    "relationship_continuity_reports": [
                        {"continuity_state": "stable"}
                    ],
                    "trust_trajectories": [{"current_trust_state": "trusted"}],
                },
                expression_plan=expression_plan,
            )
        self.assertTrue(context.get("expression_slots_mode"))
        self.assertEqual(
            context["expression_plan_slots"]["workspace_primary_focus"],
            "repair_commitment",
        )
        self.assertEqual(context["relationship"]["relation_role"], "friend")
        self.assertEqual(context["relationship"]["repair_pressure"], 1)

        visible = _model_visible_expression_context(context)
        self.assertNotIn("prediction_conscious_workspace", visible)
        self.assertIn("expression_plan_slots", visible)
        self.assertNotIn("conscious_self_summary", visible)
        self.assertNotIn("body_affect", visible)

    def test_proactive_drive_scalar_from_integrator_and_dmn(self):
        high_drive = compute_proactive_drive_scalar(
            body_integrator={
                "continuous": {
                    "cognitive_bandwidth": 0.9,
                    "sleep_pressure": 0.05,
                    "allostatic_load": 0.1,
                }
            },
            network_state={
                "dominant_network": "default_mode_network",
                "active_networks": [
                    {"network_id": "default_mode_network", "mode": "background_self_narrative"}
                ],
            },
        )
        low_drive = compute_proactive_drive_scalar(
            body_integrator={
                "continuous": {
                    "cognitive_bandwidth": 0.3,
                    "sleep_pressure": 0.9,
                    "allostatic_load": 0.8,
                }
            },
            network_state={"dominant_network": "executive_workspace_network", "active_networks": []},
            expression_plan={"fatigue_pressure": "critical", "release_caution_level": "elevated"},
        )
        self.assertGreater(high_drive, low_drive)

    def test_episodic_speech_append_on_gate_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            language_dir = Path(tmp)
            appended = maybe_append_episodic_speech_ref(
                language_dir=language_dir,
                utterance_ref="runtime/state/language/dialogue_turn_log.jsonl#turn-0001",
                expression_plan={"semantic_goal": "relationship_repair"},
                gate_status="accepted",
                generated_at="2026-06-17T03:00:00Z",
                environ={"DIGITAL_LIFE_EXPRESSION_SLOTS": "true"},
            )
            self.assertTrue(appended)
            lines = (language_dir / "episodic_speech_memory.jsonl").read_text(
                encoding="utf-8"
            ).splitlines()
            self.assertEqual(len(lines), 1)
            payload = json.loads(lines[0])
            self.assertEqual(payload["gate_status"], "accepted")
            self.assertIn("turn-0001", payload["utterance_ref"])

    def test_express_inspection_shows_slots(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "terminal"
            state_root = terminal_dir.parent
            language_dir = state_root / "language"
            language_dir.mkdir(parents=True)
            terminal_dir.mkdir(parents=True)
            plan = {
                "semantic_goal": "relationship_repair",
                "expression_slots_applied": True,
                "workspace_primary_focus": "repair_commitment",
                "workspace_topk_k": 2,
                "cognitive_bandwidth_scalar": 0.71,
                "allostatic_load_scalar": 0.22,
                "workspace_broadcast_primary_ref": "exp-primary",
                "proactive_drive_scalar": 0.62,
                "dmn_network_mode": "background_self_narrative",
            }
            (language_dir / "expression_plan.json").write_text(
                json.dumps(plan, ensure_ascii=False),
                encoding="utf-8",
            )
            (language_dir / "expression_monitor_state.json").write_text(
                json.dumps({"delay_or_release_decision": "release_guarded_expression"}),
                encoding="utf-8",
            )
            (language_dir / "model_expression_state.json").write_text(
                json.dumps({"model_expression_status": "model_expression_applied"}),
                encoding="utf-8",
            )
            inspection = _build_express_inspection(terminal_dir=terminal_dir)
            express = inspection["express"]
            self.assertTrue(express["expression_slots_applied"])
            self.assertEqual(express["workspace_primary_focus"], "repair_commitment")
            self.assertEqual(express["workspace_topk_k"], 2)

    def test_proactive_terminal_event_records_drive_when_slots_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_root = Path(tmp) / "runtime" / "state"
            terminal_dir = state_root / "terminal"
            language_dir = state_root / "language"
            body_dir = state_root / "body"
            neural_dir = state_root / "neural_life_core"
            for path in (terminal_dir, language_dir, body_dir, neural_dir):
                path.mkdir(parents=True)
            (language_dir / "expression_plan.json").write_text(
                json.dumps({"release_caution_level": "baseline"}),
                encoding="utf-8",
            )
            (body_dir / "body_integrator_state.json").write_text(
                json.dumps(
                    {
                        "continuous": {
                            "cognitive_bandwidth": 0.85,
                            "sleep_pressure": 0.1,
                            "allostatic_load": 0.12,
                        }
                    }
                ),
                encoding="utf-8",
            )
            (neural_dir / "network_state.json").write_text(
                json.dumps(
                    {
                        "dominant_network": "default_mode_network",
                        "active_networks": [
                            {
                                "network_id": "default_mode_network",
                                "mode": "background_self_narrative",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.dict(
                os.environ, {"DIGITAL_LIFE_EXPRESSION_SLOTS": "true"}, clear=False
            ):
                event = build_resident_proactive_terminal_event(
                    terminal_dir=terminal_dir,
                    life_name="Adam",
                    now_iso=lambda: "2026-06-17T04:00:00Z",
                )
            profile = event["proactive_voice_profile"]
            self.assertIsNotNone(event.get("proactive_drive_scalar"))
            self.assertIsNotNone(profile.get("proactive_drive_scalar"))
            self.assertEqual(profile.get("body_integrator_ref"), "runtime/state/body/body_integrator_state.json")

    def test_expression_plan_slots_summary_filters_applied_only(self):
        self.assertEqual(expression_plan_slots_summary({}), {})
        summary = expression_plan_slots_summary(
            {
                "expression_slots_applied": True,
                "workspace_primary_focus": "repair_commitment",
                "cognitive_bandwidth_scalar": 0.71,
                "ignored_field": "x",
            }
        )
        self.assertEqual(summary["workspace_primary_focus"], "repair_commitment")
        self.assertNotIn("ignored_field", summary)


if __name__ == "__main__":
    unittest.main()