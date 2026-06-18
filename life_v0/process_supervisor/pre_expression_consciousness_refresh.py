from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from ..neural_core.broadcast import project_broadcast_frame_from_live_turn
from ..neural_core.metacognition import project_metacognition_state_from_live_turn
from ..neural_core.workspace import (
    maybe_apply_workspace_topk_to_frame,
    project_workspace_frame_from_live_turn,
)
from ..replay import append_workspace_evictions_to_replay_cue_bundle


@dataclass(frozen=True)
class PreExpressionConsciousnessRefresh:
    workspace_frame: dict[str, Any]
    broadcast_frame: dict[str, Any]
    metacognition_state: dict[str, Any]


def refresh_pre_expression_consciousness(
    *,
    state_dir: Path,
    run_id: str,
    generated_at: str,
    live_turn_focus: str | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    expression_monitor: dict[str, Any] | None = None,
    live_language_turn_refs: list[str] | None = None,
    dialogue_turn_refs: list[str] | None = None,
    write_json: Callable[[Path, dict[str, Any]], None] | None = None,
) -> PreExpressionConsciousnessRefresh:
    consciousness_dir = state_dir / "consciousness"
    consciousness_dir.mkdir(parents=True, exist_ok=True)
    neural_dir = state_dir / "neural_life_core"
    memory_dir = state_dir / "memory"
    prediction_dir = state_dir / "prediction"

    workspace_frame = _read_json_if_exists(
        consciousness_dir / "workspace_frame.json",
        {},
    )
    broadcast_frame = _read_json_if_exists(
        consciousness_dir / "broadcast_frame.json",
        {},
    )
    metacognition_state = _read_json_if_exists(
        consciousness_dir / "metacognition_state.json",
        {},
    )
    prediction_workspace = _read_json_if_exists(
        prediction_dir / "prediction_workspace_frame.json",
        {},
    )
    prediction_error_field = _read_json_if_exists(
        prediction_dir / "prediction_error_field.json",
        {},
    )
    signal_media_runtime = _read_json_if_exists(state_dir / "signal" / "signal_media_runtime.json", {})
    body_integrator = _read_json_if_exists(state_dir / "body" / "body_integrator_state.json", {})
    network_state = _read_json_if_exists(neural_dir / "network_state.json", {})
    engram_index = _read_json_if_exists(memory_dir / "engram_index.json", {})

    updated_workspace = project_workspace_frame_from_live_turn(
        workspace_frame=workspace_frame,
        generated_at=generated_at,
        run_id=run_id,
        prediction_workspace=prediction_workspace,
        network_state=network_state,
        engram_index=engram_index,
        live_dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        live_turn_focus=live_turn_focus,
    )
    updated_workspace = maybe_apply_workspace_topk_to_frame(
        updated_workspace,
        body_integrator=body_integrator,
        signal_media_runtime=signal_media_runtime,
        memory_retrieval_frame=memory_retrieval_frame,
        prediction_error_field=prediction_error_field,
        live_turn_focus=live_turn_focus,
    )
    if updated_workspace.get("workspace_topk_applied") and write_json is not None:
        topk_meta = updated_workspace.get("workspace_topk") or {}
        evicted = list(topk_meta.get("suppressed_candidates") or [])
        if evicted:
            replay_dir = state_dir / "replay"
            replay_dir.mkdir(parents=True, exist_ok=True)
            replay_cue_bundle = append_workspace_evictions_to_replay_cue_bundle(
                _read_json_if_exists(replay_dir / "replay_cue_bundle.json", {}),
                evicted_candidates=evicted,
                generated_at=generated_at,
                run_id=run_id,
            )
            write_json(replay_dir / "replay_cue_bundle.json", replay_cue_bundle)
    updated_broadcast = project_broadcast_frame_from_live_turn(
        broadcast_frame=broadcast_frame,
        generated_at=generated_at,
        workspace_frame=updated_workspace,
        run_id=run_id,
        live_dialogue_turn_refs=dialogue_turn_refs,
        live_language_turn_refs=live_language_turn_refs,
        live_turn_focus=live_turn_focus,
    )
    updated_metacognition = project_metacognition_state_from_live_turn(
        metacognition_state=metacognition_state,
        generated_at=generated_at,
        broadcast_frame=updated_broadcast,
        workspace_frame=updated_workspace,
        run_id=run_id,
        memory_retrieval_frame=memory_retrieval_frame,
        expression_monitor_state=expression_monitor,
        live_turn_focus=live_turn_focus,
        repair_closeout_state=_read_json_if_exists(
            state_dir / "language" / "repair_closeout_state.json",
            {},
        ),
    )

    if write_json is not None:
        write_json(consciousness_dir / "workspace_frame.json", updated_workspace)
        write_json(consciousness_dir / "broadcast_frame.json", updated_broadcast)
        write_json(consciousness_dir / "metacognition_state.json", updated_metacognition)

    return PreExpressionConsciousnessRefresh(
        workspace_frame=updated_workspace,
        broadcast_frame=updated_broadcast,
        metacognition_state=updated_metacognition,
    )


def _read_json_if_exists(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return fallback
    try:
        import json

        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return fallback
    return payload if isinstance(payload, dict) else fallback