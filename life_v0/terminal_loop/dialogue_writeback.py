from __future__ import annotations

from typing import Any


def build_dialogue_writeback_bundle(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    dialogue_event_refs: list[str],
    self_narrative_writeback_refs: list[str],
    relationship_writeback_refs: list[str],
    commitment_writeback_refs: list[str],
    replay_cue_refs: list[str],
    terminal_state_refs: list[str],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "dialogue_writeback_bundle_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "writeback_bundle_id": f"dialogue-writeback-{run_id}",
        "dialogue_event_refs": dialogue_event_refs,
        "self_narrative_writeback_refs": self_narrative_writeback_refs,
        "relationship_writeback_refs": relationship_writeback_refs,
        "commitment_writeback_refs": commitment_writeback_refs,
        "replay_cue_refs": replay_cue_refs,
        "terminal_state_refs": terminal_state_refs,
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }
