from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from life_v0.digital_entry import _handle_resident_terminal_utterance
from life_v0.process_supervisor.terminal_inspection_compose import (
    COMPOSITE_CATEGORIES,
    build_composite_state_inspection,
)
from tests.helpers.life_v0_bootstrap import (
    DigitalLifeRuntimeEnvIsolationMixin,
    build_runtime_paths,
)


class TerminalInspectionComposeTests(DigitalLifeRuntimeEnvIsolationMixin, unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    def test_live_runtime_composite_categories_build_without_error(self):
        terminal_dir = self.repo_root / "runtime" / "state" / "terminal"
        if not terminal_dir.exists():
            self.skipTest("live runtime terminal dir missing")
        for category in sorted(COMPOSITE_CATEGORIES):
            inspection = build_composite_state_inspection(
                terminal_dir=terminal_dir,
                category=category,
            )
            self.assertEqual(inspection.get("category"), category)
            self.assertNotIn("error", inspection)
            payload = inspection.get(category)
            self.assertIsInstance(payload, dict)

    def test_me_slash_renders_human_text_not_raw_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (terminal_dir / "resident_lifecycle_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "resident_lifecycle_state_v0",
                        "status": "background_active",
                        "life_name": "Adam",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (terminal_dir / "terminal_life_loop_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "terminal_life_loop_state_v0",
                        "life_name": "Adam",
                        "current_mode": "restored_waiting_for_external_turn",
                        "next_required_action": "await_next_external_relation_turn",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/me",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                    record_terminal_transcript=False,
                )
            rendered = stdout.getvalue()
            self.assertIsNone(exit_code)
            self.assertIn("我是谁：", rendered)
            self.assertIn("生命名:", rendered)
            self.assertNotIn('"schema_version"', rendered)

    def test_turn_inspection_exposes_expression_release_tier(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (terminal_dir / "terminal_life_loop_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "terminal_life_loop_state_v0",
                        "life_name": "Adam",
                        "current_mode": "restored_waiting_for_external_turn",
                        "next_required_action": "await_next_external_relation_turn",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (paths["state_root"] / "language").mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "language" / "model_expression_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "model_expression_state_v0",
                        "expression_release_path": "recall_bounded_spoken_fallback",
                        "expression_release_tier": 2,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/turn",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                    record_terminal_transcript=False,
                )
            rendered = stdout.getvalue()
            self.assertIsNone(exit_code)
            self.assertIn("表达门:", rendered)
            self.assertIn("2", rendered)

    def test_memory_slash_json_flag_emits_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build_runtime_paths(Path(tmp))
            terminal_dir = paths["terminal_state"]
            terminal_dir.mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory").mkdir(parents=True, exist_ok=True)
            (paths["state_root"] / "memory" / "relationship_memory.json").write_text(
                json.dumps(
                    {
                        "schema_version": "relationship_memory_v0",
                        "relation_person_profile": {"observed_names": ["测试用户"]},
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = _handle_resident_terminal_utterance(
                    terminal_dir=terminal_dir,
                    utterance="/memory --json",
                    life_name="Adam",
                    say_timeout_seconds=0.1,
                    record_terminal_transcript=False,
                )
            rendered = stdout.getvalue()
            self.assertIsNone(exit_code)
            self.assertIn('"category": "memory"', rendered)
            self.assertIn('"schema_version"', rendered)


if __name__ == "__main__":
    unittest.main()
