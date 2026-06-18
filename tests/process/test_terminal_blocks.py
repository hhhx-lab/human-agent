import unittest

from life_v0.process_supervisor.terminal_blocks import (
    format_message_block_fragments,
    format_thinking_block_fragments,
)
from life_v0.process_supervisor.terminal_layout import MessageRenderSpec


class TerminalBlocksTests(unittest.TestCase):
    def test_user_prompt_block_uses_accent_and_timestamp(self):
        rendered = "".join(
            fragment
            for _, fragment in format_message_block_fragments(
                MessageRenderSpec(
                    speaker="relation",
                    text="你好",
                    life_name="Adam",
                    timestamp="12:34",
                )
            )
        )

        self.assertIn("›", rendered)
        self.assertNotIn("▌", rendered)
        self.assertIn("[12:34]", rendered)
        self.assertIn("你", rendered)
        self.assertIn("你好", rendered)

    def test_assistant_block_shows_release_badge(self):
        rendered = "".join(
            fragment
            for _, fragment in format_message_block_fragments(
                MessageRenderSpec(
                    speaker="life",
                    text="回复",
                    life_name="Adam",
                    release_badge="released",
                )
            )
        )

        self.assertIn("Adam", rendered)
        self.assertIn("released", rendered)
        self.assertIn("回复", rendered)

    def test_thinking_block_uses_thinking_header(self):
        rendered = "".join(
            fragment for _, fragment in format_thinking_block_fragments(life_name="Adam")
        )

        self.assertIn("thinking", rendered)
        self.assertIn("▌", rendered)

    def test_diff_block_renders_insert_lines(self):
        rendered = "".join(
            fragment
            for _, fragment in format_message_block_fragments(
                MessageRenderSpec(
                    speaker="command_result",
                    text="diff --git a/x b/x\n--- a/x\n+++ b/x\n@@ -1 +1 @@\n-old\n+new\n",
                    life_name="Adam",
                ),
                collapsed=False,
            )
        )

        self.assertIn("Diff", rendered)
        self.assertIn("+new", rendered)

    def test_execute_block_uses_run_header(self):
        rendered = "".join(
            fragment
            for _, fragment in format_message_block_fragments(
                MessageRenderSpec(
                    speaker="command",
                    text="uv run pytest tests/",
                    life_name="Adam",
                )
            )
        )

        self.assertIn("Run", rendered)
        self.assertIn("uv run pytest", rendered)

    def test_collapsed_block_shows_fold_marker(self):
        rendered = "".join(
            fragment
            for _, fragment in format_message_block_fragments(
                MessageRenderSpec(
                    speaker="life",
                    text="line\n" * 12,
                    life_name="Adam",
                ),
                collapsed=True,
            )
        )

        self.assertIn("▸", rendered)
        self.assertIn("expand", rendered)


if __name__ == "__main__":
    unittest.main()