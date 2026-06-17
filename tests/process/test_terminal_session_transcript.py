import tempfile
import unittest
from pathlib import Path

from life_v0.process_supervisor.terminal_session_transcript import (
    append_terminal_session_event,
    load_current_terminal_session_lines,
    read_terminal_session_index,
    render_resume_transcript,
    start_terminal_session_transcript,
)


class TerminalSessionTranscriptTests(unittest.TestCase):
    def test_current_session_keeps_every_visible_turn_and_resume_reads_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            opened = start_terminal_session_transcript(
                terminal_dir=terminal_dir,
                life_name="Adam",
                now_iso="2026-06-17T12:00:00+00:00",
            )
            session_id = opened["session_id"]

            append_terminal_session_event(
                terminal_dir=terminal_dir,
                session_id=session_id,
                event_kind="relation_utterance",
                speaker="relation",
                text="第一句",
                life_name="Adam",
                now_iso="2026-06-17T12:00:01+00:00",
            )
            append_terminal_session_event(
                terminal_dir=terminal_dir,
                session_id=session_id,
                event_kind="life_response",
                speaker="life",
                text="我在。",
                life_name="Adam",
                now_iso="2026-06-17T12:00:02+00:00",
            )
            append_terminal_session_event(
                terminal_dir=terminal_dir,
                session_id=session_id,
                event_kind="command_result",
                speaker="command_result",
                text='{"status":"ok"}',
                life_name="Adam",
                now_iso="2026-06-17T12:00:03+00:00",
            )

            current_lines = load_current_terminal_session_lines(
                terminal_dir=terminal_dir,
            )
            resume_text = render_resume_transcript(terminal_dir=terminal_dir)
            index = read_terminal_session_index(terminal_dir=terminal_dir)

        self.assertIn("你: 第一句", current_lines)
        self.assertIn("Adam: 我在。", current_lines)
        self.assertIn('command result: {"status":"ok"}', current_lines)
        self.assertIn("你: 第一句", resume_text)
        self.assertEqual(index["current_session_id"], session_id)
        self.assertEqual(
            index["context_policy"],
            "stored_for_resume_view_not_injected_into_current_model_context",
        )

    def test_new_session_does_not_erase_old_resume_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            first = start_terminal_session_transcript(
                terminal_dir=terminal_dir,
                life_name="Adam",
                now_iso="2026-06-17T12:00:00+00:00",
            )
            append_terminal_session_event(
                terminal_dir=terminal_dir,
                session_id=first["session_id"],
                event_kind="relation_utterance",
                speaker="relation",
                text="旧会话",
                life_name="Adam",
                now_iso="2026-06-17T12:00:01+00:00",
            )
            second = start_terminal_session_transcript(
                terminal_dir=terminal_dir,
                life_name="Adam",
                now_iso="2026-06-17T13:00:00+00:00",
            )
            append_terminal_session_event(
                terminal_dir=terminal_dir,
                session_id=second["session_id"],
                event_kind="relation_utterance",
                speaker="relation",
                text="新会话",
                life_name="Adam",
                now_iso="2026-06-17T13:00:01+00:00",
            )

            current_lines = load_current_terminal_session_lines(
                terminal_dir=terminal_dir,
            )
            resume_text = render_resume_transcript(
                terminal_dir=terminal_dir,
                session_count=2,
            )

        self.assertNotIn("你: 旧会话", current_lines)
        self.assertIn("你: 新会话", current_lines)
        self.assertIn("你: 旧会话", resume_text)
        self.assertIn("你: 新会话", resume_text)

    def test_sessions_opened_in_same_second_get_distinct_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            first = start_terminal_session_transcript(
                terminal_dir=terminal_dir,
                life_name="Adam",
                now_iso="2026-06-17T12:00:00+00:00",
            )
            second = start_terminal_session_transcript(
                terminal_dir=terminal_dir,
                life_name="Adam",
                now_iso="2026-06-17T12:00:00+00:00",
            )
            index = read_terminal_session_index(terminal_dir=terminal_dir)

        self.assertNotEqual(first["session_id"], second["session_id"])
        self.assertEqual(index["session_ids"][-2:], [first["session_id"], second["session_id"]])

    def test_resume_rendering_does_not_recursively_embed_previous_resume_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            terminal_dir = Path(tmp) / "runtime" / "state" / "terminal"
            opened = start_terminal_session_transcript(
                terminal_dir=terminal_dir,
                life_name="Adam",
                now_iso="2026-06-17T12:00:00+00:00",
            )
            append_terminal_session_event(
                terminal_dir=terminal_dir,
                session_id=opened["session_id"],
                event_kind="relation_utterance",
                speaker="relation",
                text="真实内容",
                life_name="Adam",
                now_iso="2026-06-17T12:00:01+00:00",
            )
            append_terminal_session_event(
                terminal_dir=terminal_dir,
                session_id=opened["session_id"],
                event_kind="command_result",
                speaker="command_result",
                text="session nested\n  你: 旧 resume",
                life_name="Adam",
                now_iso="2026-06-17T12:00:02+00:00",
                metadata={"title": "会话恢复"},
            )

            resume_text = render_resume_transcript(terminal_dir=terminal_dir)

        self.assertIn("真实内容", resume_text)
        self.assertNotIn("旧 resume", resume_text)


if __name__ == "__main__":
    unittest.main()
