import tempfile
import unittest
from io import StringIO
from pathlib import Path

from life_v0.process_supervisor.terminal_input import (
    build_file_reference_completion_items,
    build_slash_completion_items,
    build_terminal_completion_state,
    build_terminal_input_profile,
    render_terminal_completion_popup,
    write_terminal_input_profile,
)


class TerminalInputTests(unittest.TestCase):
    def test_terminal_input_profile_records_prompt_toolkit_as_only_interactive_reader(self):
        stream = StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            profile = build_terminal_input_profile(
                input_stream=stream,
                idle_voice_interval_seconds=12.5,
                mode_override="test_editable_line_buffer",
            )
            written = write_terminal_input_profile(
                terminal_dir=terminal_dir,
                profile=profile,
            )

            self.assertEqual(
                written["schema_version"],
                "terminal_input_profile_v0",
            )
            self.assertEqual(written["input_mode"], "test_editable_line_buffer")
            self.assertEqual(written["terminal_framework"], "prompt_toolkit")
            self.assertEqual(written["self_built_input_reader"], "removed")
            self.assertEqual(
                written["prompt_toolkit_experience"]["input_box"],
                "bottom_composer_with_prompt_prefix_and_cursor_index",
            )
            self.assertTrue(written["prompt_toolkit_experience"]["mouse_support"])
            self.assertTrue(
                written["prompt_toolkit_experience"]["enable_history_search"]
            )
            self.assertEqual(
                written["prompt_toolkit_experience"]["complete_style"],
                "MULTI_COLUMN",
            )
            self.assertEqual(
                written["prompt_toolkit_experience"]["cursor_shape"],
                "BLINKING_BEAM",
            )
            self.assertEqual(
                written["line_editing"]["backspace"],
                "prompt_toolkit_native_delete_previous_character",
            )
            self.assertEqual(
                written["line_editing"]["left_right_arrows"],
                "prompt_toolkit_native_cursor_navigation",
            )
            self.assertEqual(
                written["line_editing"]["up_down_arrows"],
                "completion_selection_when_menu_open_else_history",
            )
            self.assertEqual(
                written["line_editing"]["redraw_strategy"],
                "prompt_toolkit_layout_renderer",
            )
            self.assertTrue(
                written["idle_voice_policy"]["release_only_when_prompt_submits_empty_line"]
            )
            self.assertTrue(
                written["relation_turn_boundary"][
                    "slash_commands_bypass_relation_inbox"
                ]
            )
            self.assertTrue(written["slash_command_completion"]["enabled"])
            self.assertEqual(written["slash_command_completion"]["selection"], "up_down_arrows")
            self.assertEqual(written["slash_command_completion"]["confirm"], "enter")
            self.assertEqual(written["file_reference_completion"]["trigger"], "@")
            self.assertEqual(written["file_reference_completion"]["selection"], "up_down_arrows")
            self.assertEqual(written["file_reference_completion"]["confirm"], "enter")
            self.assertEqual(
                written["default_state_visibility"],
                "hidden_until_slash_command",
            )
            self.assertTrue((terminal_dir / "terminal_input_profile.json").exists())

    def test_self_built_terminal_reader_is_not_exported(self):
        import life_v0.process_supervisor.terminal_input as terminal_input

        self.assertFalse(hasattr(terminal_input, "TerminalLineBuffer"))
        self.assertFalse(hasattr(terminal_input, "read_interactive_line_with_idle_voice"))

    def test_slash_completion_items_filter_commands_for_tui_popup(self):
        items = build_slash_completion_items(
            "/m",
            slash_commands=[
                ("/memory", "记忆、召回、写门"),
                ("/dream", "梦境、离线整合"),
                ("/state", "生命状态"),
                ("/exit", "离开终端"),
            ],
        )

        self.assertEqual([item.label for item in items], ["/memory"])
        self.assertEqual(items[0].detail, "记忆、召回、写门")

        state = build_terminal_completion_state(
            "/",
            slash_commands=[
                ("/memory", "记忆、召回、写门"),
                ("/dream", "梦境、离线整合"),
                ("/state", "生命状态"),
                ("/exit", "离开终端"),
            ],
        )
        rendered = render_terminal_completion_popup(state)
        self.assertIn("/memory", rendered)
        self.assertIn("/dream", rendered)
        self.assertIn("/state", rendered)
        self.assertIn("/exit", rendered)

    def test_file_reference_completion_indexes_repo_files_and_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "life_v0" / "process_supervisor").mkdir(parents=True)
            (root / "life_v0" / "process_supervisor" / "terminal_input.py").write_text(
                "",
                encoding="utf-8",
            )
            (root / "docs" / "v0").mkdir(parents=True)
            (root / "runtime" / "state").mkdir(parents=True)
            (root / "runtime" / "state" / "local.json").write_text(
                "",
                encoding="utf-8",
            )
            (root / ".env").write_text("SECRET=1", encoding="utf-8")
            (root / ".env.example").write_text("SECRET=", encoding="utf-8")

            items = build_file_reference_completion_items(
                "@",
                repo_root=root,
            )

        labels = [item.label for item in items]
        self.assertIn("life_v0/process_supervisor/", labels)
        self.assertIn("life_v0/process_supervisor/terminal_input.py", labels)
        self.assertIn(".env.example", labels)
        self.assertNotIn(".env", labels)
        self.assertNotIn("runtime/state/local.json", labels)

    def test_completion_state_uses_current_at_token_inside_sentence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "v0").mkdir(parents=True)
            (root / "docs" / "v0" / "entry.md").write_text("", encoding="utf-8")

            state = build_terminal_completion_state(
                "你看一下 @docs/v",
                cursor_index=len("你看一下 @docs/v"),
                repo_root=root,
                slash_commands=[("/memory", "记忆")],
            )

        self.assertIsNotNone(state)
        self.assertEqual(state.trigger, "@")
        self.assertEqual(state.query, "docs/v")
        self.assertIn("docs/v0/", [item.label for item in state.items])


if __name__ == "__main__":
    unittest.main()
