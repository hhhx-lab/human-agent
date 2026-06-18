import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.prompt_toolkit_terminal_app import (
    TerminalIdleVoicePolicy,
    _TerminalCompleter,
    _bottom_toolbar,
    _confirm_selected_completion_or_submit,
    _format_bottom_toolbar,
    _format_right_prompt,
    _move_completion_selection_or_history,
    _prompt_prefix,
    _session_experience_profile,
    prompt_toolkit_available,
)
from life_v0.process_supervisor.terminal_layout import TerminalLayoutState


def _toolbar_text(toolbar) -> str:
    if isinstance(toolbar, list):
        return "".join(fragment for _, fragment in toolbar)
    return "".join(fragment for _, fragment in toolbar)


class PromptToolkitTerminalAppTests(unittest.TestCase):
    def test_prompt_toolkit_dependency_is_available_for_mature_tui_input(self):
        if not prompt_toolkit_available():
            self.skipTest("prompt_toolkit is installed in the project environment")
        self.assertTrue(prompt_toolkit_available())

    def test_completer_uses_existing_slash_and_file_reference_rules(self):
        if not prompt_toolkit_available():
            self.skipTest("prompt_toolkit is installed in the project environment")
        from prompt_toolkit.document import Document

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "v0").mkdir(parents=True)
            (root / "docs" / "v0" / "entry.md").write_text("", encoding="utf-8")
            completer = _TerminalCompleter(
                slash_commands=(("/memory", "记忆"), ("/dream", "梦境")),
                repo_root=root,
            )

            slash = list(
                completer.get_completions(
                    Document("/m", cursor_position=2),
                    complete_event=None,
                )
            )
            file_refs = list(
                completer.get_completions(
                    Document("看 @docs/v", cursor_position=len("看 @docs/v")),
                    complete_event=None,
                )
            )

        self.assertEqual([item.text for item in slash], ["/memory"])
        self.assertIn("@docs/v0/", [item.text for item in file_refs])

    def test_slash_completer_exposes_full_grouped_command_list_to_arrow_selection(self):
        if not prompt_toolkit_available():
            self.skipTest("prompt_toolkit is installed in the project environment")
        from prompt_toolkit.document import Document

        commands = tuple(
            (f"/cmd-{index}", f"常用｜第 {index} 个命令")
            for index in range(1, 15)
        )
        completer = _TerminalCompleter(
            slash_commands=commands,
            repo_root=Path.cwd(),
        )

        completions = list(
            completer.get_completions(
                Document("/", cursor_position=1),
                complete_event=None,
            )
        )

        self.assertEqual(len(completions), 14)
        self.assertEqual(completions[-1].text, "/cmd-14")
        self.assertIn("常用", str(completions[0].display_meta_text))
        self.assertIn("第 1 个命令", str(completions[0].display_meta_text))

    def test_arrow_keys_select_completion_and_enter_confirms_it_before_submit(self):
        if not prompt_toolkit_available():
            self.skipTest("prompt_toolkit is installed in the project environment")
        from prompt_toolkit.buffer import Buffer
        from prompt_toolkit.completion import Completion
        from prompt_toolkit.document import Document
        from prompt_toolkit.buffer import CompletionState

        buffer = Buffer()
        buffer.document = Document("/", cursor_position=1)
        buffer.complete_state = CompletionState(
            buffer.document,
            completions=[
                Completion("/memory", start_position=-1),
                Completion("/dream", start_position=-1),
            ],
        )

        self.assertTrue(_move_completion_selection_or_history(buffer, direction="down"))
        self.assertEqual(buffer.text, "/memory")
        self.assertTrue(_move_completion_selection_or_history(buffer, direction="down"))
        self.assertEqual(buffer.text, "/dream")
        self.assertTrue(_move_completion_selection_or_history(buffer, direction="up"))
        self.assertEqual(buffer.text, "/memory")
        self.assertTrue(_confirm_selected_completion_or_submit(buffer))
        self.assertEqual(buffer.text, "/memory")
        self.assertIsNone(buffer.complete_state)

    def test_arrow_key_can_open_completion_synchronously_before_async_menu_arrives(self):
        if not prompt_toolkit_available():
            self.skipTest("prompt_toolkit is installed in the project environment")
        from prompt_toolkit.buffer import Buffer
        from prompt_toolkit.document import Document

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "v0").mkdir(parents=True)
            completer = _TerminalCompleter(
                slash_commands=(("/memory", "记忆"), ("/dream", "梦境")),
                repo_root=root,
            )
            slash_buffer = Buffer()
            slash_buffer.document = Document("/", cursor_position=1)
            at_buffer = Buffer()
            at_buffer.document = Document("引用 @docs/v", cursor_position=len("引用 @docs/v"))

            self.assertTrue(
                _move_completion_selection_or_history(
                    slash_buffer,
                    direction="down",
                    completer=completer,
                )
            )
            self.assertEqual(slash_buffer.text, "/memory")
            self.assertTrue(_confirm_selected_completion_or_submit(slash_buffer))
            self.assertEqual(slash_buffer.text, "/memory")

            self.assertTrue(
                _move_completion_selection_or_history(
                    at_buffer,
                    direction="down",
                    completer=completer,
                )
            )
            self.assertIn("@docs/v0/", at_buffer.text)
            self.assertTrue(_confirm_selected_completion_or_submit(at_buffer))
            self.assertIn("@docs/v0/", at_buffer.text)

    def test_enter_without_completion_submits_current_line(self):
        if not prompt_toolkit_available():
            self.skipTest("prompt_toolkit is installed in the project environment")
        from prompt_toolkit.buffer import Buffer
        from prompt_toolkit.document import Document

        buffer = Buffer()
        submitted: list[str] = []
        buffer.accept_handler = lambda b: submitted.append(b.text) or True
        buffer.document = Document("你好", cursor_position=2)

        self.assertFalse(_confirm_selected_completion_or_submit(buffer))
        self.assertEqual(submitted, ["你好"])

    def test_default_toolbar_does_not_surface_internal_life_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            state_root = terminal_dir.parent
            (state_root / "body").mkdir(parents=True)
            (state_root / "consciousness").mkdir(parents=True)
            (state_root / "body" / "core_affect_vector.json").write_text(
                '{"valence":"guarded"}',
                encoding="utf-8",
            )
            (state_root / "consciousness" / "workspace_frame.json").write_text(
                '{"status":"active"}',
                encoding="utf-8",
            )

            toolbar = _bottom_toolbar(
                terminal_dir=terminal_dir,
                life_name="Adam",
                layout_state=TerminalLayoutState(sidebar_visible=False, terminal_width=100),
                slash_commands=(("/memory", "状态｜记忆"),),
                repo_root=Path(tmp),
            )
            text = _toolbar_text(toolbar)

        self.assertIn("Adam", text)
        self.assertNotIn("情绪", text)
        self.assertNotIn("guarded", text)
        self.assertNotIn("band 0.", text)

    def test_toolbar_reports_cursor_index_for_mid_line_editing(self):
        class FakeBuffer:
            text = "连续输入三个字"
            cursor_position = 4
            complete_state = None

        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            terminal_dir.mkdir(parents=True)
            toolbar = _format_bottom_toolbar(
                life_name="Adam",
                buffer=FakeBuffer(),
                terminal_dir=terminal_dir,
                layout_state=TerminalLayoutState(sidebar_visible=False, terminal_width=100),
                slash_commands=(),
                repo_root=Path(tmp),
            )
            text = _toolbar_text(toolbar)

        self.assertIn("pos 4/7", text)
        self.assertIn("Enter发送", text)
        self.assertIn("Ctrl+P命令", text)

    def test_toolbar_reports_remaining_completion_count_when_menu_has_more_rows(self):
        class FakeCompletionState:
            completions = [object() for _ in range(20)]

        class FakeBuffer:
            text = "/"
            cursor_position = 1
            complete_state = FakeCompletionState()

        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            terminal_dir.mkdir(parents=True)
            toolbar = _format_bottom_toolbar(
                life_name="Adam",
                buffer=FakeBuffer(),
                terminal_dir=terminal_dir,
                layout_state=TerminalLayoutState(sidebar_visible=False, terminal_width=100),
                slash_commands=(),
                repo_root=Path(tmp),
            )
            text = _toolbar_text(toolbar)

        self.assertIn("↑↓ 选择", text)
        self.assertIn("还有 6 个，继续输入筛选", text)

    def test_prompt_prefix_and_right_prompt_make_input_box_visible(self):
        class FakeBuffer:
            text = "连续输入三个字"
            cursor_position = 4
            complete_state = None

        prompt_text = _toolbar_text(_prompt_prefix("Adam"))
        right_text = _toolbar_text(_format_right_prompt(buffer=FakeBuffer()))

        self.assertIn("╭─ Adam", prompt_text)
        self.assertIn("╰─›", prompt_text)
        self.assertIn("pos 4/7", right_text)

    def test_prompt_toolkit_experience_profile_enables_mature_terminal_feel(self):
        profile = _session_experience_profile()

        self.assertEqual(profile["layout_profile"], "product_split_pane_v4_grok_visual")
        self.assertTrue(profile["mouse_support"])
        self.assertEqual(
            profile["scrollback_policy"],
            "in_app_conversation_pane_mac_trackpad_and_ctrl_arrows",
        )
        self.assertGreaterEqual(profile["session_replay_line_limit"], 400)
        self.assertTrue(profile["enable_history_search"])
        self.assertTrue(profile["show_frame"])
        self.assertEqual(profile["complete_style"], "COLUMN")
        self.assertEqual(profile["cursor_shape"], "BLINKING_BEAM")
        self.assertGreaterEqual(profile["reserve_space_for_menu"], 14)
        self.assertEqual(profile["sidebar_toggle"], "ctrl_b")
        self.assertEqual(profile["message_blocks"], "timestamp_speaker_badge_body")

    def test_idle_voice_policy_releases_only_after_empty_idle_interval(self):
        timeline = [0.0]

        def now():
            return timeline[0]

        policy = TerminalIdleVoicePolicy(interval_seconds=10.0, now_fn=now)

        timeline[0] = 4.0
        self.assertFalse(policy.should_release(active_text=""))

        timeline[0] = 11.0
        self.assertTrue(policy.should_release(active_text=""))

        timeline[0] = 15.0
        self.assertFalse(policy.should_release(active_text=""))

        timeline[0] = 22.0
        self.assertFalse(policy.should_release(active_text="正在输入"))

        timeline[0] = 33.0
        self.assertTrue(policy.should_release(active_text=""))


if __name__ == "__main__":
    unittest.main()
