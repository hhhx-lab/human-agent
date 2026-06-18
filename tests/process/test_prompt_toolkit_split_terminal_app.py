import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.prompt_toolkit_split_terminal_app import (
    split_terminal_experience_profile,
)
from life_v0.process_supervisor.terminal_command_palette import build_palette_items
from life_v0.process_supervisor.terminal_layout import (
    MessageRenderSpec,
    format_auxiliary_fragments,
    format_footer_fragments,
    format_message_body_fragments,
    format_sidebar_pane_fragments,
    load_sidebar_snapshot,
)
from life_v0.process_supervisor.terminal_tui_runtime import ConversationModel
from life_v0.process_supervisor.terminal_layout import build_startup_conversation_fragments
from life_v0.process_supervisor.terminal_session_transcript import (
    resolve_attach_terminal_session,
)


def _text(fragments: list[tuple[str, str]]) -> str:
    return "".join(fragment for _, fragment in fragments)


class PromptToolkitSplitTerminalAppTests(unittest.TestCase):
    def test_experience_profile_describes_split_pane_shell(self):
        profile = split_terminal_experience_profile()

        self.assertEqual(profile["layout_profile"], "product_split_pane_v4_grok_visual")
        self.assertEqual(profile["block_visual"], "grok_style_accent_blocks_foldable")
        self.assertEqual(profile["session_resume"], "startup_carry_and_transcript")
        self.assertIn("pixel_birth", str(profile.get("welcome_screen", "")))
        self.assertEqual(profile["command_palette"], "ctrl_p_search_list_detail_overlay")
        self.assertEqual(profile["async_turns"], "background_worker_with_typing_indicator")
        self.assertEqual(profile["streaming_output"], "live_sse_with_simulated_fallback")
        self.assertTrue(profile["mouse_support"])
        self.assertEqual(
            profile["scrollback_policy"],
            "in_app_conversation_pane_mac_trackpad_and_ctrl_arrows",
        )
        self.assertEqual(profile["conversation_pane"], "scrollable_left_column")
        self.assertEqual(profile["sidebar_pane"], "fixed_right_column_ctrl_b")

    def test_sidebar_pane_renders_vertical_live_scalars(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            state_root = terminal_dir.parent
            (state_root / "body").mkdir(parents=True)
            (state_root / "language").mkdir(parents=True)
            (state_root / "consciousness").mkdir(parents=True)
            (state_root / "body" / "body_integrator_state.json").write_text(
                '{"continuous": {"cognitive_bandwidth": 0.42}}',
                encoding="utf-8",
            )
            snapshot = load_sidebar_snapshot(terminal_dir=terminal_dir)
            text = _text(
                format_sidebar_pane_fragments(
                    snapshot=snapshot,
                    collapsed=False,
                )
            )

        self.assertIn("live", text)
        self.assertIn("band", text)
        self.assertIn("0.42", text)

    def test_message_body_renders_code_fence_blocks(self):
        body = format_message_body_fragments(
            "说明\n```py\nprint('hi')\n```\n结束"
        )
        text = _text(body)

        self.assertIn("说明", text)
        self.assertIn("print('hi')", text)
        self.assertIn("结束", text)

    def test_auxiliary_fragments_surface_slash_panel_and_file_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "notes.md").write_text("引用预览文本", encoding="utf-8")
            aux = format_auxiliary_fragments(
                active_text="/",
                slash_commands=(("/memory", "状态｜记忆"),),
                repo_root=root,
                width=88,
            )
            preview = format_auxiliary_fragments(
                active_text="看 @notes.md",
                slash_commands=(),
                repo_root=root,
                width=88,
            )

        self.assertIn("命令面板", _text(aux))
        self.assertIn("引用预览", _text(preview))

    def test_auxiliary_fragments_filter_slash_commands_for_prefix_query(self):
        aux = format_auxiliary_fragments(
            active_text="/mem",
            slash_commands=(
                ("/memory", "状态｜记忆"),
                ("/me", "常用｜我是谁"),
            ),
            repo_root=None,
            width=88,
        )
        lines = [line.strip() for line in _text(aux).splitlines()]
        self.assertIn("命令匹配", lines[0])
        self.assertTrue(any(line.startswith("/memory") for line in lines))
        self.assertFalse(any(line.startswith("/me ") for line in lines))

    def test_conversation_model_appends_message_blocks(self):
        model = ConversationModel()
        model.append_message(
            MessageRenderSpec(
                speaker="life",
                text="你好",
                life_name="Adam",
                release_badge="released",
            )
        )

        text = _text(model.fragments)
        self.assertIn("Adam", text)
        self.assertIn("released", text)
        self.assertIn("你好", text)

    def test_startup_conversation_includes_resume_and_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            terminal_dir.mkdir(parents=True)
            fragments = build_startup_conversation_fragments(
                terminal_dir=terminal_dir,
                life_name="Adam",
                width=88,
            )

        self.assertIn("会话恢复", _text(fragments))

    def test_attach_reuses_current_terminal_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            terminal_dir.mkdir(parents=True)
            first = resolve_attach_terminal_session(
                terminal_dir=terminal_dir,
                life_name="Adam",
            )
            second = resolve_attach_terminal_session(
                terminal_dir=terminal_dir,
                life_name="Adam",
            )

        self.assertTrue(first.get("created"))
        self.assertEqual(second.get("session_id"), first.get("session_id"))
        self.assertTrue(second.get("attached"))

    def test_conversation_model_load_startup_restores_current_session_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            terminal_dir.mkdir(parents=True)
            opened = resolve_attach_terminal_session(
                terminal_dir=terminal_dir,
                life_name="Adam",
            )
            from life_v0.process_supervisor.terminal_session_transcript import (
                append_terminal_session_event,
            )

            append_terminal_session_event(
                terminal_dir=terminal_dir,
                session_id=str(opened["session_id"]),
                event_kind="relation_utterance",
                speaker="relation",
                text="你好",
                life_name="Adam",
            )
            model = ConversationModel()
            model.load_startup(
                terminal_dir=terminal_dir,
                life_name="Adam",
                width=88,
            )

        self.assertIn("你好", _text(model.fragments))

    def test_command_palette_includes_slash_commands(self):
        items = build_palette_items(
            slash_commands=(("/memory", "状态｜记忆"),),
        )
        labels = [item.label for item in items]
        self.assertIn("/memory", labels)
        self.assertIn("Ctrl+P", labels)

    def test_command_palette_accepts_slash_command_metadata_tuples(self):
        items = build_palette_items(
            slash_commands=(
                ("/web-dream", "梦境网页｜网页梦境学习", {"show_on_empty_query": False}),
            ),
        )
        labels = [item.label for item in items]
        self.assertIn("/web-dream", labels)

    def test_command_palette_loads_real_slash_command_registry(self):
        from life_v0.digital_entry import _build_terminal_slash_completion_items

        items = build_palette_items(
            slash_commands=_build_terminal_slash_completion_items(),
        )
        labels = [item.label for item in items]
        self.assertIn("/me", labels)
        self.assertIn("/web-dream", labels)

    def test_conversation_model_supports_block_fold(self):
        model = ConversationModel()
        model.append_message(
            MessageRenderSpec(
                speaker="command_result",
                text="diff --git a/x b/x\n+++ b/x\n@@\n+line\n",
                life_name="Adam",
            )
        )
        model.select_block(0)
        model.collapse_selected()
        text = _text(model.render_fragments())
        self.assertIn("▸", text)
        model.expand_selected()
        text = _text(model.render_fragments())
        self.assertIn("▾", text)

    def test_split_app_uses_scrollable_pane_for_conversation(self):
        source = Path(
            "life_v0/process_supervisor/prompt_toolkit_split_terminal_app.py"
        ).read_text(encoding="utf-8")
        self.assertIn("ScrollablePane(", source)
        self.assertIn("_ScrollableConversationControl", source)
        self.assertIn("conversation_pane_holder", source)
        self.assertIn("_conversation_scroll_width", source)

    def test_split_app_key_bindings_use_valid_prompt_toolkit_keys(self):
        import ast
        import re

        from prompt_toolkit.key_binding.key_bindings import _parse_key

        source = Path(
            "life_v0/process_supervisor/prompt_toolkit_split_terminal_app.py"
        ).read_text(encoding="utf-8")
        tree = ast.parse(source)
        invalid: list[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not (
                isinstance(func, ast.Attribute)
                and func.attr == "add"
                and isinstance(func.value, ast.Name)
                and func.value.id == "bindings"
            ):
                continue
            if not node.args:
                continue
            key_arg = node.args[0]
            keys: list[str] = []
            if isinstance(key_arg, ast.Constant) and isinstance(key_arg.value, str):
                keys = [key_arg.value]
            elif isinstance(key_arg, ast.Attribute) and isinstance(key_arg.value, ast.Name):
                keys = [f"Keys.{key_arg.attr}"]
            for key in keys:
                if key.startswith("Keys."):
                    continue
                try:
                    _parse_key(key)
                except ValueError:
                    invalid.append(key)
        self.assertEqual(invalid, [])

    def test_split_app_source_has_no_invalid_window_focusable_kwarg(self):
        import ast

        source = Path(
            "life_v0/process_supervisor/prompt_toolkit_split_terminal_app.py"
        ).read_text(encoding="utf-8")
        tree = ast.parse(source)
        offenders: list[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = func.id if isinstance(func, ast.Name) else (
                func.attr if isinstance(func, ast.Attribute) else None
            )
            if name != "Window":
                continue
            for keyword in node.keywords:
                if keyword.arg == "focusable":
                    offenders.append(
                        ast.get_source_segment(source, node) or "Window(...)"
                    )
        self.assertEqual(offenders, [])

    def test_footer_fragments_keep_cursor_hints(self):
        class FakeBuffer:
            text = "你好"
            cursor_position = 1
            complete_state = None

        text = _text(format_footer_fragments(life_name="Adam", buffer=FakeBuffer()))

        self.assertIn("pos 1/2", text)
        self.assertIn("双指滑对话区", text)
        self.assertIn("⌃G最新", text)
        self.assertIn("Ctrl+O浏览", text)


if __name__ == "__main__":
    unittest.main()
