import unittest

from life_v0.process_supervisor.terminal_layout import MessageRenderSpec
from life_v0.process_supervisor.terminal_scroll import (
    apply_conversation_scroll_policy,
    clamp_conversation_scroll,
    conversation_layout_chrome_lines,
    count_conversation_display_lines,
    estimate_conversation_visual_lines,
    resolve_conversation_content_height,
    resolve_conversation_max_scroll,
    scroll_conversation_by_lines,
)
from life_v0.process_supervisor.terminal_tui_runtime import ConversationModel


class _FakePane:
    def __init__(self, *, render_info=None) -> None:
        self.vertical_scroll = 0
        self.render_info = render_info


class TerminalScrollTests(unittest.TestCase):
    def test_estimate_conversation_visual_lines_counts_blocks(self):
        model = ConversationModel()
        model.append_message(
            MessageRenderSpec(speaker="relation", text="你好\n世界", life_name="Adam")
        )
        model.append_message(
            MessageRenderSpec(speaker="life", text="收到", life_name="Adam")
        )
        self.assertGreaterEqual(estimate_conversation_visual_lines(model), 8)

    def test_apply_conversation_scroll_policy_scrolls_to_end(self):
        model = ConversationModel()
        for index in range(12):
            model.append_message(
                MessageRenderSpec(
                    speaker="life",
                    text=f"reply {index}\nline two",
                    life_name="Adam",
                )
            )
        pane = _FakePane()
        apply_conversation_scroll_policy(
            pane=pane,
            conversation=model,
            terminal_height=24,
            auxiliary_lines=0,
        )
        self.assertGreater(pane.vertical_scroll, 0)

    def test_scroll_conversation_by_lines_disables_follow_end(self):
        model = ConversationModel()
        for index in range(8):
            model.append_message(
                MessageRenderSpec(
                    speaker="life",
                    text=f"line {index}\nsecond",
                    life_name="Adam",
                )
            )
        model.scroll_to_end = True
        pane = _FakePane()
        pane.vertical_scroll = 4
        scroll_conversation_by_lines(
            pane=pane,
            conversation=model,
            delta=-2,
            terminal_height=24,
            auxiliary_lines=0,
        )
        self.assertFalse(model.scroll_to_end)
        self.assertEqual(pane.vertical_scroll, 2)

    def test_count_conversation_display_lines_matches_prompt_toolkit_height(self):
        model = ConversationModel()
        model.width = 20
        model.append_message(
            MessageRenderSpec(
                speaker="life",
                text="这是一段比较长的回复，用来测试换行后的可视行数统计。",
                life_name="Adam",
            )
        )
        self.assertEqual(
            count_conversation_display_lines(model, width=20),
            resolve_conversation_content_height(model, width=20),
        )

    def test_resolve_conversation_max_scroll_does_not_overshoot_content(self):
        model = ConversationModel(width=72)
        for index in range(20):
            model.append_message(
                MessageRenderSpec(
                    speaker="life",
                    text=(
                        f"第{index + 1}轮：这是一条用于滚动测试的对话内容，"
                        "长度足够占多行。"
                    ),
                    life_name="Adam",
                )
            )
        pane = _FakePane()
        max_scroll = resolve_conversation_max_scroll(
            pane=pane,
            conversation=model,
            terminal_height=28,
            auxiliary_lines=0,
            width=72,
        )
        pane.vertical_scroll = max_scroll + 200
        clamp_conversation_scroll(
            pane=pane,
            conversation=model,
            terminal_height=28,
            auxiliary_lines=0,
            width=72,
        )
        self.assertEqual(pane.vertical_scroll, max_scroll)
        self.assertLess(
            max_scroll,
            estimate_conversation_visual_lines(model) * 2,
        )

    def test_conversation_layout_chrome_matches_split_terminal_pane(self):
        self.assertEqual(conversation_layout_chrome_lines(auxiliary_lines=3), 9)


if __name__ == "__main__":
    unittest.main()