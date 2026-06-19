import unittest
from pathlib import Path

from life_v0.process_supervisor.terminal_layout import MessageRenderSpec
from life_v0.process_supervisor.terminal_scroll import (
    count_conversation_display_lines,
    resolve_conversation_max_scroll,
    scroll_conversation_by_lines,
)
from life_v0.process_supervisor.terminal_tui_runtime import ConversationModel
from life_v0.process_supervisor.resident_lifecycle import send_resident_relation_turn
from life_v0.process_supervisor.terminal_ui import resolve_relation_turn_display_text
from life_v0.process_supervisor.terminal_command_palette import (
    build_palette_items,
    resolve_palette_action,
)


class _FakePane:
    def __init__(self) -> None:
        self.vertical_scroll = 0
        self.render_info = None


class DialogueScrollAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terminal_dir = Path("runtime/state/terminal")

    def test_twenty_messages_remain_scrollable(self):
        model = ConversationModel(width=72)
        for index in range(20):
            model.append_message(
                MessageRenderSpec(
                    speaker="relation" if index % 2 == 0 else "life",
                    text=f"第{index + 1}轮：这是一条用于滚动测试的对话内容，长度足够占多行。",
                    life_name="Adam",
                )
            )
        pane = _FakePane()
        content_lines = count_conversation_display_lines(model, width=72)
        self.assertGreaterEqual(content_lines, 60)
        max_scroll = resolve_conversation_max_scroll(
            pane=pane,
            conversation=model,
            terminal_height=28,
            width=72,
        )
        self.assertGreater(max_scroll, 20)
        model.scroll_to_end = False
        scroll_conversation_by_lines(
            pane=pane,
            conversation=model,
            delta=-max_scroll,
            terminal_height=28,
            width=72,
        )
        self.assertEqual(pane.vertical_scroll, 0)
        scroll_conversation_by_lines(
            pane=pane,
            conversation=model,
            delta=max_scroll,
            terminal_height=28,
            width=72,
        )
        self.assertEqual(pane.vertical_scroll, max_scroll)

    def test_twenty_round_live_dialogue_returns_visible_text(self):
        prompts = [
            "第1轮：你好。",
            "第2轮：记得上一句吗？",
            "第3轮：说一个短句。",
            "第4轮：继续。",
            "第5轮：嗯。",
            "第6轮：再说一句。",
            "第7轮：好的。",
            "第8轮：随便聊聊。",
            "第9轮：我在测试滚动。",
            "第10轮：过半了。",
            "第11轮：还能看到吗？",
            "第12轮：继续测试。",
            "第13轮：快结束了。",
            "第14轮：再说点。",
            "第15轮：快完成了。",
            "第16轮：快十七了。",
            "第17轮：继续。",
            "第18轮：倒数第二轮。",
            "第19轮：最后一轮前。",
            "第20轮：最后一轮，请简短回复。",
        ]
        replies: list[str] = []
        for utterance in prompts:
            turn_result = send_resident_relation_turn(
                terminal_dir=self.terminal_dir,
                utterance=utterance,
                wait_timeout_seconds=90.0,
            )
            response_event = turn_result.state.get("response_event") or {}
            response = resolve_relation_turn_display_text(
                utterance=utterance,
                response_text=str(turn_result.state.get("response_text") or ""),
                send_status=str(turn_result.state.get("send_status") or ""),
                output_status=str(response_event.get("status") or ""),
            )
            self.assertTrue(response.strip(), msg=utterance)
            replies.append(response.strip())
        self.assertEqual(len(replies), 20)

    def test_palette_slash_commands_resolve(self):
        items = build_palette_items(
            slash_commands=(
                ("/status", "状态"),
                ("/resume", "恢复"),
                ("/help", "帮助"),
            )
        )
        self.assertGreaterEqual(len(items), 3)
        slash_items = [item for item in items if str(item.action).startswith("slash:")]
        self.assertGreaterEqual(len(slash_items), 3)
        kind, payload = resolve_palette_action(slash_items[0])
        self.assertEqual(kind, "slash")
        self.assertTrue(str(payload).startswith("/"))


if __name__ == "__main__":
    unittest.main()