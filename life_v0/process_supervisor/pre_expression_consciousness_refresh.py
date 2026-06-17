from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from ..neural_core.broadcast import project_broadcast_frame_from_live_turn
from ..neural_core.metacognition import project_metacognition_state_from_live_turn
from ..neural_core.workspace import project_workspace_frame_from_live_turn


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