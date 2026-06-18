import unittest

from life_v0.process_supervisor.terminal_stream_bridge import stream_session


class TerminalStreamBridgeTests(unittest.TestCase):
    def test_stream_session_collects_live_deltas(self):
        deltas: list[str] = []

        with stream_session(on_delta=deltas.append) as sink:
            sink.emit_start()
            sink.emit_delta("你")
            sink.emit_delta("好")
            sink.emit_complete("你好")

        self.assertEqual(deltas, ["你", "好"])
        self.assertTrue(sink.saw_live_deltas)


if __name__ == "__main__":
    unittest.main()