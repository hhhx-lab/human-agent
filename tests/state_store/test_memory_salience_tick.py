from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from life_v0.state_store.hippocampal_cue_index import (
    apply_hippocampal_cue_weight_decay,
    build_hippocampal_cue_index,
)
from life_v0.state_store.memory_retrieval import (
    is_memory_salience_tick_enabled,
    maybe_apply_retrieval_salience_tick,
    maybe_run_memory_salience_tick_hook,
)
from life_v0.state_store.memory_trace_store import (
    apply_retrieval_salience_delta,
    build_memory_trace_store,
)
from life_v0.state_store.offline_memory_consolidation import apply_offline_memory_consolidation


class MemorySalienceTickTests(unittest.TestCase):
    def _trace_store_with_live_trace(self) -> dict:
        return build_memory_trace_store(
            run_id="salience-run",
            generated_at="2026-06-17T00:00:00Z",
            live_turn_context={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-1",
                ],
                "external_utterance": "你还记得我们上次聊咖啡吗？",
                "semantic_focus": "coffee_memory",
                "expression_outcome": "released",
            },
        )

    def test_disabled_by_default(self):
        self.assertFalse(is_memory_salience_tick_enabled({}))

    def test_retrieval_delta_updates_salience_and_revision_history(self):
        store = self._trace_store_with_live_trace()
        live_trace = [
            trace
            for trace in store["traces"]
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        ][0]
        trace_ref = f"runtime/state/memory/memory_trace_store.json#{live_trace['trace_id']}"
        before_replay = float(live_trace.get("replay_salience") or 0.5)

        result = apply_retrieval_salience_delta(
            store,
            retrieval_hits=[trace_ref],
            run_id="salience-run",
            generated_at="2026-06-17T01:00:00Z",
            turn_counter=2,
            allostatic_load=0.1,
            mean_activation_score=0.8,
        )
        updated_trace = [
            trace
            for trace in result["memory_trace_store"]["traces"]
            if trace.get("trace_id") == live_trace["trace_id"]
        ][0]
        self.assertGreater(updated_trace["replay_salience"], before_replay)
        self.assertIn("salience", updated_trace["salience_vector"])
        self.assertTrue(updated_trace["revision_history_refs"])
        self.assertTrue(result["salience_tick_report"]["applied"])

    def test_high_allostatic_load_suppresses_delta(self):
        store = self._trace_store_with_live_trace()
        live_trace = [
            trace
            for trace in store["traces"]
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        ][0]
        trace_ref = f"runtime/state/memory/memory_trace_store.json#{live_trace['trace_id']}"
        low_load = apply_retrieval_salience_delta(
            store,
            retrieval_hits=[trace_ref],
            run_id="salience-run",
            generated_at="2026-06-17T01:00:00Z",
            turn_counter=1,
            allostatic_load=0.1,
        )
        high_load = apply_retrieval_salience_delta(
            store,
            retrieval_hits=[trace_ref],
            run_id="salience-run",
            generated_at="2026-06-17T01:01:00Z",
            turn_counter=2,
            allostatic_load=0.9,
        )
        low_delta = low_load["salience_tick_report"]["effective_delta"]
        high_delta = high_load["salience_tick_report"]["effective_delta"]
        self.assertGreater(low_delta, high_delta)

    def test_maybe_apply_retrieval_salience_tick_from_frame(self):
        store = self._trace_store_with_live_trace()
        live_trace = [
            trace
            for trace in store["traces"]
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        ][0]
        trace_ref = f"runtime/state/memory/memory_trace_store.json#{live_trace['trace_id']}"
        cue_index = build_hippocampal_cue_index(
            run_id="salience-run",
            generated_at="2026-06-17T01:00:00Z",
            memory_trace_store=store,
        )
        before_weight = cue_index["cue_bindings"][0]["cue_weight"]
        result = maybe_apply_retrieval_salience_tick(
            memory_trace_store=store,
            memory_retrieval_frame={
                "tiered_recall": {"salient_core_refs": [trace_ref]},
                "reconstructive_recall_profile": {
                    "reconstruction_fragment_refs": [trace_ref],
                    "mean_activation_score": 0.7,
                },
            },
            hippocampal_cue_index=cue_index,
            run_id="salience-run",
            generated_at="2026-06-17T01:00:00Z",
            turn_counter=3,
            body_integrator={
                "continuous": {
                    "allostatic_load": 0.2,
                    "sleep_pressure": 0.55,
                }
            },
            environ={"DIGITAL_LIFE_MEMORY_SALIENCE_TICK": "1"},
        )
        self.assertTrue(result.applied)
        self.assertTrue(result.memory_retrieval_frame["retrieval_salience_tick_applied"])
        updated_trace = [
            trace
            for trace in result.memory_trace_store["traces"]
            if trace.get("trace_id") == live_trace["trace_id"]
        ][0]
        self.assertTrue(updated_trace["revision_history_refs"])
        self.assertLess(
            result.hippocampal_cue_index["cue_bindings"][0]["cue_weight"],
            before_weight,
        )

    def test_hippocampal_decay_tracks_sleep_pressure(self):
        cue_index = {
            "cue_bindings": [{"cue_weight": 0.8, "base_activation": 0.5}],
        }
        low_sleep = apply_hippocampal_cue_weight_decay(
            cue_index,
            generated_at="2026-06-17T02:00:00Z",
            body_integrator={"continuous": {"sleep_pressure": 0.1}},
            dt_ms=120_000,
        )
        high_sleep = apply_hippocampal_cue_weight_decay(
            cue_index,
            generated_at="2026-06-17T02:00:00Z",
            body_integrator={"continuous": {"sleep_pressure": 0.8}},
            dt_ms=120_000,
        )
        self.assertLess(
            high_sleep["cue_bindings"][0]["cue_weight"],
            low_sleep["cue_bindings"][0]["cue_weight"],
        )

    def test_offline_consolidation_reads_sleep_pressure(self):
        store = self._trace_store_with_live_trace()
        live_trace = [
            trace
            for trace in store["traces"]
            if trace.get("live_trace_origin") == "live_dialogue_turn"
        ][0]
        live_trace["replay_salience"] = 0.62
        live_trace["accessibility_score"] = 0.7
        result = apply_offline_memory_consolidation(
            run_id="offline-run",
            generated_at="2026-06-17T03:00:00Z",
            memory_trace_store=store,
            body_integrator={"continuous": {"sleep_pressure": 0.75}},
        )
        report = result["memory_consolidation_report"]
        self.assertEqual(report["sleep_pressure_snapshot"], 0.75)
        self.assertTrue(report["consolidation_diff"]["trace_salience_updates"])

    def test_hook_writes_runtime_files_when_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory_dir = Path(tmp)
            store = self._trace_store_with_live_trace()
            live_trace = [
                trace
                for trace in store["traces"]
                if trace.get("live_trace_origin") == "live_dialogue_turn"
            ][0]
            trace_ref = f"runtime/state/memory/memory_trace_store.json#{live_trace['trace_id']}"
            writes: list[str] = []

            def write_json(path: Path, payload: dict) -> None:
                writes.append(path.name)
                path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            (memory_dir / "memory_trace_store.json").write_text(
                json.dumps(store, ensure_ascii=False),
                encoding="utf-8",
            )
            result = maybe_run_memory_salience_tick_hook(
                memory_dir=memory_dir,
                memory_retrieval_frame={
                    "tiered_recall": {"salient_core_refs": [trace_ref]},
                },
                run_id="hook-run",
                generated_at="2026-06-17T04:00:00Z",
                turn_counter=1,
                write_json=write_json,
                environ={"DIGITAL_LIFE_MEMORY_SALIENCE_TICK": "1"},
            )
            self.assertTrue(result.applied)
            self.assertIn("memory_trace_store.json", writes)
            self.assertIn("memory_retrieval_frame.json", writes)


if __name__ == "__main__":
    unittest.main()