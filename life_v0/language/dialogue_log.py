from __future__ import annotations

from pathlib import Path
from typing import Any


def build_dialogue_turn_log_entries(
    *,
    run_id: str,
    generated_at: str,
    source_doc_refs: list[str],
) -> list[dict[str, Any]]:
    return [
        {
            "schema_version": "dialogue_turn_event_v0",
            "run_id": run_id,
            "generated_at": generated_at,
            "turn_id": "dialogue-turn-v0-0001",
            "relation_role": "friend",
            "shared_term_refs": ["runtime/state/language/shared_term_registry.json#shared-term-v0-0001"],
            "commitment_refs": ["runtime/state/language/commitment_repair_language_index.json#commitment-v0-0001"],
            "expression_monitor_ref": "runtime/state/language/expression_monitor_state.json",
            "narrative_trace_ref": "runtime/state/language/self_narrative_language_trace.json",
            "source_doc_refs": source_doc_refs,
        }
    ]


def collect_dialogue_turn_refs(path: Path, blocked_reasons: list[str]) -> list[str]:
    try:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError as exc:
        blocked_reasons.append(f"dialogue_turn_restore_gate failed: {exc}")
        return []
    return [f"runtime/state/language/dialogue_turn_log.jsonl#line-{idx}" for idx, _ in enumerate(lines, start=1)]
