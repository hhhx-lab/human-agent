import tempfile
import unittest
from io import StringIO
from pathlib import Path

from life_v0.process_supervisor.terminal_input import (
    TerminalLineBuffer,
    build_terminal_input_profile,
    write_terminal_input_profile,
)


class TerminalInputTests(unittest.TestCase):
    def test_terminal_line_buffer_supports_editing_without_polluting_turn_text(self):
        editor = TerminalLineBuffer()
        for char in "helol":
            result = editor.feed(char)
            self.assertFalse(result.submitted)
        self.assertEqual(editor.text, "helol")
        editor.feed("\x7f")
        editor.feed("\x7f")
        for char in "lo":
            editor.feed(char)
        self.assertEqual(editor.text, "hello")
        editor.feed("\x1b")
        editor.feed("[")
        editor.feed("D")
        self.assertEqual(editor.text, "hello")
        result = editor.feed("\n")
        self.assertTrue(result.submitted)
        self.assertEqual(result.line, "hello")
        self.assertEqual(editor.text, "")

    def test_terminal_line_buffer_ctrl_u_and_ctrl_d_boundaries(self):
        editor = TerminalLineBuffer()
        for char in "temporary":
            editor.feed(char)
        clear_result = editor.feed("\x15")
        self.assertFalse(clear_result.submitted)
        self.assertEqual(editor.text, "")
        eof_result = editor.feed("\x04")
        self.assertTrue(eof_result.eof)

    def test_terminal_input_profile_records_editing_and_idle_voice_policy(self):
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
            self.assertEqual(
                written["line_editing"]["backspace"],
                "delete_previous_character",
            )
            self.assertTrue(
                written["idle_voice_policy"]["release_only_when_input_buffer_empty"]
            )
            self.assertTrue(
                written["relation_turn_boundary"][
                    "slash_commands_bypass_relation_inbox"
                ]
            )
            self.assertTrue((terminal_dir / "terminal_input_profile.json").exists())


if __name__ == "__main__":
    unittest.main()
