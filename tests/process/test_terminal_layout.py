from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.terminal_layout import (
    MessageRenderSpec,
    TerminalLayoutState,
    build_file_reference_preview,
    build_itr09_flag_summary,
    build_slash_panel_lines,
    format_message_plain,
    format_sidebar_fragments,
    format_top_bar_fragments,
    load_sidebar_snapshot,
    resolve_release_badge,
)


class TerminalLayoutTests(unittest.TestCase):
    def test_itr09_flag_summary_marks_enabled_segments(self):
        summary = build_itr09_flag_summary(
            {
                "DIGITAL_LIFE_BODY_INTEGRATE": "true",
                "DIGITAL_LIFE_PREDICTION_REFRESH": "1",
            }
        )
        self.assertIn("A✓", summary)
        self.assertIn("B✓", summary)
        self.assertIn("C·", summary)

    def test_message_block_includes_timestamp_and_release_badge(self):
        rendered = format_message_plain(
            MessageRenderSpec(
                speaker="life",
                text="你好",
                life_name="Adam",
                release_badge="released",
            )
        )
        self.assertIn("Adam", rendered)
        self.assertIn("released", rendered)
        self.assertIn("你好", rendered)
        self.assertRegex(rendered, r"\[\d{2}:\d{2}\]")

    def test_sidebar_hidden_by_default(self):
        fragments = format_sidebar_fragments(
            snapshot=load_sidebar_snapshot(
                terminal_dir=Path("/tmp/nonexistent/runtime/state/terminal")
            ),
            width=100,
            collapsed=True,
        )
        text = "".join(fragment for _, fragment in fragments)
        self.assertIn("侧栏关闭", text)

    def test_sidebar_shows_integrator_scalars_when_expanded(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            state_root = terminal_dir.parent
            (state_root / "body").mkdir(parents=True)
            (state_root / "language").mkdir(parents=True)
            (state_root / "consciousness").mkdir(parents=True)
            (state_root / "body" / "body_integrator_state.json").write_text(
                json.dumps(
                    {
                        "continuous": {
                            "cognitive_bandwidth": 0.42,
                            "allostatic_load": 0.31,
                            "sleep_pressure": 0.12,
                        }
                    }
                ),
                encoding="utf-8",
            )
            (state_root / "language" / "expression_plan.json").write_text(
                json.dumps({"workspace_topk_k": 3, "proactive_drive_scalar": 0.55}),
                encoding="utf-8",
            )
            snapshot = load_sidebar_snapshot(terminal_dir=terminal_dir)
            fragments = format_sidebar_fragments(
                snapshot=snapshot,
                width=110,
                collapsed=False,
            )
            text = "".join(fragment for _, fragment in fragments)
            self.assertIn("band 0.42", text)
            self.assertIn("topk 3", text)

    def test_file_reference_preview_for_text_and_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text_path = root / "notes.md"
            text_path.write_text("一段用于预览的引用文本", encoding="utf-8")
            image_path = root / "shot.png"
            image_path.write_bytes(b"png")
            preview = build_file_reference_preview(
                "请看 @notes.md 和 @shot.png",
                repo_root=root,
            )
            self.assertIn("@notes.md", preview or "")
            self.assertIn("预览", preview or "")
            self.assertIn("@shot.png", preview or "")

    def test_slash_panel_groups_commands(self):
        lines = build_slash_panel_lines(
            (
                ("/me", "常用｜我是谁"),
                ("/memory", "状态｜记忆"),
                ("/growth", "生命机制｜成长"),
            )
        )
        joined = "\n".join(lines)
        self.assertIn("[常用]", joined)
        self.assertIn("/me", joined)
        self.assertIn("[状态]", joined)

    def test_release_badge_reads_model_expression_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            language_dir = terminal_dir.parent / "language"
            language_dir.mkdir(parents=True)
            (language_dir / "model_expression_state.json").write_text(
                json.dumps(
                    {
                        "model_expression_status": "model_expression_applied",
                        "post_expression_gate": {"gate_status": "accepted"},
                    }
                ),
                encoding="utf-8",
            )
            badge = resolve_release_badge(
                terminal_dir=terminal_dir,
                speaker="life",
                text="自然语言回复",
            )
            self.assertEqual(badge, "released")

    def test_top_bar_contains_life_name_and_status(self):
        fragments = format_top_bar_fragments(
            life_name="Adam",
            resident_status="background_active",
            itr_flags="ITR A·B·",
            width=80,
        )
        text = "".join(fragment for _, fragment in fragments)
        self.assertIn("Adam", text)
        self.assertIn("background_active", text)
        self.assertIn("ITR", text)

    def test_layout_toolbar_does_not_surface_sidebar_when_collapsed(self):
        from life_v0.process_supervisor.terminal_layout import (
            format_layout_toolbar_fragments,
        )

        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            state_root = terminal_dir.parent
            (state_root / "body").mkdir(parents=True)
            (state_root / "body" / "core_affect_vector.json").write_text(
                json.dumps({"valence": "guarded"}),
                encoding="utf-8",
            )
            fragments = format_layout_toolbar_fragments(
                life_name="Adam",
                terminal_dir=terminal_dir,
                layout_state=TerminalLayoutState(sidebar_visible=False, terminal_width=100),
                slash_commands=(("/memory", "状态｜记忆"),),
                repo_root=Path(tmp),
            )
            text = "".join(fragment for _, fragment in fragments)
            self.assertNotIn("guarded", text)
            self.assertNotIn("band ", text)


if __name__ == "__main__":
    unittest.main()