import unittest

from life_v0.process_supervisor.terminal_ui import (
    extract_life_response_text,
    render_dialogue_box,
)


class TerminalUiTests(unittest.TestCase):
    def test_dialogue_rendering_uses_transcript_style_not_ascii_box(self):
        rendered = render_dialogue_box("Adam", "第一行\n第二行", width=60)

        self.assertTrue(rendered.startswith("Adam\n"))
        self.assertIn("  第一行", rendered)
        self.assertIn("  第二行", rendered)
        self.assertNotIn("+---", rendered)
        self.assertNotIn("| ", rendered)
        self.assertEqual(extract_life_response_text(rendered), "第一行\n第二行")


if __name__ == "__main__":
    unittest.main()
