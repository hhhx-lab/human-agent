from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TextIO

from .heartbeat import write_waiting_heartbeat
from .turn_io import poll_input_line


@dataclass(frozen=True)
class IdleRefreshLoopResult:
    heartbeat_counter: int
    external_utterance: str | None
    exit_reason: str | None


def wait_for_next_external_relation_turn(
    *,
    input_stream: TextIO,
    run_id: str,
    generated_at: str,
    terminal_dir: Path,
    reports_dir: Path,
    language_dir: Path,
    relationship_dir: Path,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    commitment_index: dict[str, Any],
    relationship_graph: dict[str, Any],
    source_doc_refs: list[str],
    readme_block_refs: list[str],
    runtime_carrier_refs: list[str],
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    replay_cue_bundle_ref: str | None = None,
    offline_consolidation_frame_ref: str | None = None,
    growth_patch_candidate_queue_ref: str | None = None,
    growth_patch_candidate_ids: list[str] | None = None,
    replay_residue_ref_count: int = 0,
    dream_window_ref_count: int = 0,
    growth_patch_candidate_count: int = 0,
    heartbeat_counter: int,
    poll_timeout_seconds: float = 0.05,
    now_iso: Callable[[], str],
    write_json: Callable[[Path, dict[str, Any]], None],
    poll_input_line_fn: Callable[[TextIO], str | None] | None = None,
    write_waiting_heartbeat_fn: Callable[..., int] = write_waiting_heartbeat,
) -> IdleRefreshLoopResult:
    poll_input_line_fn = poll_input_line_fn or (
        lambda stream: poll_input_line(stream, timeout_seconds=poll_timeout_seconds)
    )

    while True:
        raw_line = poll_input_line_fn(input_stream)
        if raw_line is None:
            heartbeat_counter = write_waiting_heartbeat_fn(
                run_id=run_id,
                generated_at=generated_at,
                terminal_dir=terminal_dir,
                reports_dir=reports_dir,
                language_dir=language_dir,
                relationship_dir=relationship_dir,
                safe_terminal_loop=safe_terminal_loop,
                terminal_life_loop_state=terminal_life_loop_state,
                self_narrative_trace=self_narrative_trace,
                commitment_index=commitment_index,
                relationship_graph=relationship_graph,
                source_doc_refs=source_doc_refs,
                readme_block_refs=readme_block_refs,
                runtime_carrier_refs=runtime_carrier_refs,
                replay_cue_bundle=replay_cue_bundle,
                offline_consolidation_frame=offline_consolidation_frame,
                growth_patch_candidate_queue=growth_patch_candidate_queue,
                replay_cue_bundle_ref=replay_cue_bundle_ref,
                offline_consolidation_frame_ref=offline_consolidation_frame_ref,
                growth_patch_candidate_queue_ref=growth_patch_candidate_queue_ref,
                growth_patch_candidate_ids=growth_patch_candidate_ids,
                replay_residue_ref_count=replay_residue_ref_count,
                dream_window_ref_count=dream_window_ref_count,
                growth_patch_candidate_count=growth_patch_candidate_count,
                now_iso=now_iso,
                write_json=write_json,
            )
            continue

        if raw_line == "":
            return IdleRefreshLoopResult(
                heartbeat_counter=heartbeat_counter,
                external_utterance=None,
                exit_reason="eof",
            )

        external_utterance = raw_line.strip()
        if not external_utterance:
            continue
        if external_utterance == "/exit":
            return IdleRefreshLoopResult(
                heartbeat_counter=heartbeat_counter,
                external_utterance=None,
                exit_reason="explicit_exit",
            )

        return IdleRefreshLoopResult(
            heartbeat_counter=heartbeat_counter,
            external_utterance=external_utterance,
            exit_reason=None,
        )
