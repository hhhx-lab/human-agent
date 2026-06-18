import unittest

from life_v0.process_supervisor.terminal_layout import MessageRenderSpec
from life_v0.process_supervisor.terminal_scroll import (
    apply_conversation_scroll_policy,
    count_conversation_display_lines,
    estimate_conversation_visual_lines,
    resolve_conversation_max_scroll,
    scroll_conversation_by_lines,
)
from life_v0.process_supervisor.terminal_tui_runtime import ConversationModel


class _FakePane:
    def __init__(self, *, render_info=None) -> None:
        self.vertical_scroll = 0
        self.render_info = render_info


class _FakeRenderInfo:
    def __init__(self, *, content_height: int, window_height: int) -> None:
        self.content_height = content_height
        self.window_height = window_height


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

    def test_count_conversation_display_lines_uses_wrapped_fragments(self):
        model = ConversationModel()
        model.width = 20
        model.append_message(
            MessageRenderSpec(
                speaker="life",
                text="这是一段比较长的回复，用来测试换行后的可视行数统计。",
                life_name="Adam",
            )
        )
        self.assertGreater(
            count_conversation_display_lines(model, width=20),
            estimate_conversation_visual_lines(model),
        )

    def test_resolve_conversation_max_scroll_prefers_render_info(self):
        model = ConversationModel()
        pane = _FakePane(
            render_info=_FakeRenderInfo(content_height=120, window_height=30)
        )
        self.assertEqual(
            resolve_conversation_max_scroll(
                pane=pane,
                conversation=model,
                terminal_height=24,
            ),
            90,
        )


if __name__ == "__main__":
    unittest.main()