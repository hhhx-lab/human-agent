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
    relationship_timeline_writeback_refs: list[str],
    commitment_writeback_refs: list[str],
    commitment_expression_writeback_refs: list[str],
    apology_repair_writeback_refs: list[str],
    responsibility_writeback_refs: list[str],
    life_state_writeback_refs: list[str],
    replay_cue_refs: list[str],
    terminal_state_refs: list[str],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    background_trait_convergence_refs: list[str] | None = None,
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
        "relationship_timeline_writeback_refs": relationship_timeline_writeback_refs,
        "commitment_writeback_refs": commitment_writeback_refs,
        "commitment_expression_writeback_refs": commitment_expression_writeback_refs,
        "apology_repair_writeback_refs": apology_repair_writeback_refs,
        "responsibility_writeback_refs": responsibility_writeback_refs,
        "life_state_writeback_refs": life_state_writeback_refs,
        "replay_cue_refs": replay_cue_refs,
        "terminal_state_refs": terminal_state_refs,
        "background_trait_convergence_refs": list(
            background_trait_convergence_refs or []
        ),
        "source_doc_refs": source_doc_refs,
        "readme_block_refs": readme_block_refs,
        "runtime_carrier_refs": runtime_carrier_refs,
    }
