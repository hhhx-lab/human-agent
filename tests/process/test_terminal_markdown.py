import unittest

from life_v0.process_supervisor.terminal_markdown import format_markdown_body_fragments


class TerminalMarkdownTests(unittest.TestCase):
    def test_markdown_renders_heading_list_link_and_code(self):
        text = "# 标题\n- 条目\n阅读 [文档](docs/a.md)\n```py\nprint(1)\n```"
        rendered = "".join(fragment for _, fragment in format_markdown_body_fragments(text))

        self.assertIn("标题", rendered)
        self.assertIn("条目", rendered)
        self.assertIn("文档", rendered)
        self.assertIn("docs/a.md", rendered)
        self.assertIn("print(1)", rendered)


if __name__ == "__main__":
    unittest.main()