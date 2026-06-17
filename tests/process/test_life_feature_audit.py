import json
import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.life_feature_audit import build_life_feature_audit


class LifeFeatureAuditTests(unittest.TestCase):
    def test_audit_reports_enabled_disabled_and_stale_disabled_features(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_root = Path(tmp) / "runtime" / "state"
            reports = Path(tmp) / "runtime" / "reports" / "latest"
            for directory in [
                state_root / "terminal",
                state_root / "dream",
                state_root / "memory",
                state_root / "body",
                state_root / "consciousness",
                state_root / "language",
                state_root / "relationship",
                state_root / "self",
                state_root / "growth",
                reports,
            ]:
                directory.mkdir(parents=True, exist_ok=True)

            def write(path: Path, payload: dict) -> None:
                path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            write(
                state_root / "terminal" / "resident_autonomous_activity_state.json",
                {
                    "schema_version": "resident_autonomous_activity_state_v0",
                    "status": "active",
                    "activity_count": 15,
                    "last_activity_kind": "learning_consolidation",
                    "covered_activity_kinds": [
                        "sleep",
                        "memory_recall",
                        "self_thinking",
                        "growth_rehearsal",
                        "learning_consolidation",
                    ],
                    "cycle_coverage_complete": True,
                },
            )
            write(
                state_root / "dream" / "web_dream_learning_state.json",
                {"schema_version": "web_dream_learning_state_v1", "status": "disabled"},
            )
            write(
                state_root / "dream" / "exit_dream_consolidation_summary.json",
                {
                    "schema_version": "exit_dream_consolidation_summary_v0",
                    "status": "closed",
                    "source_dialogue_turn_count": 8,
                },
            )
            write(
                state_root / "memory" / "dialogue_memory_summary.json",
                {
                    "schema_version": "dialogue_memory_summary_v0",
                    "status": "closed",
                    "source_dialogue_turn_count": 8,
                },
            )
            for relative in [
                "memory/memory_retrieval_frame.json",
                "memory/relationship_memory.json",
                "memory/engram_index.json",
                "relationship/relationship_timeline.json",
                "self/self_model.json",
                "self/resident_self_thinking_state.json",
                "terminal/terminal_life_loop_state.json",
                "body/core_affect_vector.json",
                "body/need_state_vector.json",
                "body/body_resource_budget.json",
                "body/body_rhythm_pulse.json",
                "consciousness/workspace_frame.json",
                "language/semantic_map_frame.json",
                "language/language_percept_frame.json",
                "language/inner_speech_frame.json",
            ]:
                write(state_root / relative, {"schema_version": relative, "status": "closed"})

            audit = build_life_feature_audit(
                state_dir=state_root,
                reports_dir=reports,
                environ={
                    "DIGITAL_LIFE_WEB_DREAM_LEARNING_ENABLED": "true",
                    "DIGITAL_LIFE_WEB_DREAM_URLS": "https://example.test",
                },
            )

            by_id = {item["feature_id"]: item for item in audit["features"]}
            self.assertEqual(audit["overall_status"], "active_with_warnings")
            self.assertEqual(by_id["autonomous_activity_cycle"]["status"], "enabled")
            self.assertEqual(by_id["exit_dream_memory_summary"]["status"], "enabled")
            self.assertEqual(by_id["web_dream_learning"]["status"], "enabled")
            self.assertEqual(
                by_id["web_dream_learning"]["last_runtime_status"],
                "disabled",
            )
            self.assertIn(
                "stale_disabled_state_overridden_by_effective_config",
                by_id["web_dream_learning"]["warnings"],
            )
            self.assertEqual(by_id["body_inner_environment"]["status"], "enabled")
            self.assertEqual(by_id["consciousness_workspace"]["status"], "enabled")
