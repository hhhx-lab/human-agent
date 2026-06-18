import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.terminal_session_tabs import (
    create_terminal_session_tab,
    cycle_terminal_session_tab,
    format_session_tab_bar_fragments,
    list_terminal_session_tabs,
    switch_terminal_session,
)


class TerminalSessionTabsTests(unittest.TestCase):
    def test_create_and_cycle_terminal_session_tabs(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            terminal_dir.mkdir(parents=True)
            first = create_terminal_session_tab(terminal_dir=terminal_dir, life_name="Adam")
            second = create_terminal_session_tab(terminal_dir=terminal_dir, life_name="Adam")

            tabs = list_terminal_session_tabs(terminal_dir=terminal_dir, limit=5)
            self.assertEqual(len(tabs), 2)
            self.assertTrue(tabs[-1].is_current)
            self.assertEqual(tabs[-1].session_id, second)

            switch_terminal_session(terminal_dir=terminal_dir, session_id=first)
            cycled = cycle_terminal_session_tab(terminal_dir=terminal_dir, direction="next")
            self.assertEqual(cycled, second)

    def test_session_tab_bar_marks_active_tab(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            terminal_dir.mkdir(parents=True)
            create_terminal_session_tab(terminal_dir=terminal_dir, life_name="Adam")
            second = create_terminal_session_tab(terminal_dir=terminal_dir, life_name="Adam")
            rendered = "".join(
                fragment
                for _, fragment in format_session_tab_bar_fragments(
                    terminal_dir=terminal_dir,
                    width=100,
                )
            )
            self.assertIn("2:", rendered)
            self.assertIn(second.replace("terminal-session-", "s")[:6], rendered)


if __name__ == "__main__":
    unittest.main()