import unittest

from life_v0.process_supervisor.terminal_ui import (
    extract_life_response_text,
    render_digital_life_banner,
    render_dialogue_box,
    render_input_prompt,
    render_life_opening,
)


class TerminalUiTests(unittest.TestCase):
    def test_dialogue_rendering_uses_product_message_blocks_not_ascii_box(self):
        rendered = render_dialogue_box("Adam", "第一行\n第二行", width=60)

        self.assertIn("Adam", rendered)
        self.assertIn("  第一行", rendered)
        self.assertIn("  第二行", rendered)
        self.assertNotIn("+---", rendered)
        self.assertNotIn("| ", rendered)
        self.assertIn("第一行", extract_life_response_text(rendered))
        self.assertIn("第二行", extract_life_response_text(rendered))

    def test_terminal_opening_hides_internal_process_state_by_default(self):
        state = {
            "life_name": "Adam",
            "status": "background_active",
            "pid": 12345,
            "pid_alive": True,
            "resident_autonomous_activity_count": 9,
            "resident_autonomous_activity_next_kind": "dreaming",
        }

        banner = render_digital_life_banner(
            life_name="Adam",
            status="background_active",
            width=80,
        )
        opening = render_life_opening(state, life_name="Adam", width=80)

        joined = banner + "\n" + opening
        self.assertIn("Adam", joined)
        self.assertIn("/", joined)
        self.assertIn("@", joined)
        self.assertNotIn("background_active", joined)
        self.assertNotIn("pid", joined.lower())
        self.assertNotIn("活动计数", joined)
        self.assertNotIn("dreaming", joined)

    def test_terminal_prompt_uses_bottom_input_box_style(self):
        prompt = render_input_prompt(life_name="Adam")

        self.assertIn(">", prompt)
        self.assertIn("Adam", prompt)
        self.assertIn("─", prompt)
        self.assertNotIn("Adam > ", prompt)
        self.assertGreaterEqual(len(prompt), 40)


if __name__ == "__main__":
    unittest.main()
