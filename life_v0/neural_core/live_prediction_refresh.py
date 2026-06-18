from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from .active_sampling import build_active_sampling_plan, compute_efe_score
from .belief_state import build_belief_state_frame, refresh_belief_confidence_from_live_turn
from .prediction_error import (
    build_prediction_error_field,
    refresh_prediction_error_from_live_turn,
)
from .signal_media import build_signal_media_runtime, refresh_signal_media_from_integrator


SOURCE_DOC_REFS = [
    "docs/v0/动力学升级/05_网络状态与认知预测.md",
    "docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md",
]

SIGNAL_MEDIA_REF = "runtime/state/signal/signal_media_runtime.json"
BELIEF_STATE_REF = "runtime/state/prediction/belief_state_frame.json"
PREDICTION_ERROR_REF = "runtime/state/prediction/prediction_error_field.json"
ACTIVE_SAMPLING_REF = "runtime/state/prediction/active_sampling_plan.json"


def is_prediction_refresh_enabled(environ: Mapping[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return _parse_bool(env.get("DIGITAL_LIFE_PREDICTION_REFRESH"), False)


@dataclass(frozen=True)
class PredictionStackRefreshResult:
    signal_media_runtime: dict[str, Any]
    belief_state: dict[str, Any]
    prediction_error_field: dict[str, Any]
    active_sampling_plan: dict[str, Any]
    applied: bool


def project_prediction_stack_from_live_turn(
    *,
    run_id: str,
    generated_at: str,
    turn_counter: int,
    signal_media_runtime: dict[str, Any] | None,
    belief_state: dict[str, Any] | None,
    prediction_error_field: dict[str, Any] | None,
    active_sampling_plan: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
    semantic_map: dict[str, Any] | None,
    core_affect_vector: dict[str, Any] | None,
    body_integrator: dict[str, Any] | None,
    body_resource_budget: dict[str, Any] | None,
    network_state: dict[str, Any] | None,
    offline_learning_cumulative_profile: dict[str, Any] | None = None,
    language_continuity: dict[str, Any] | None = None,
) -> PredictionStackRefreshResult:
    language_percept = language_percept or {}
    semantic_map = semantic_map or {}
    core_affect_vector = core_affect_vector or {}
    body_integrator = body_integrator or {}
    body_resource_budget = body_resource_budget or {}
    network_state = network_state or {}

    repair_profile = _resolve_queue_e_profile(
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
    )

    signal_media_runtime = refresh_signal_media_from_integrator(
        signal_media_runtime=signal_media_runtime,
        run_id=run_id,
        generated_at=generated_at,
        body_integrator=body_integrator,
        core_affect_vector=core_affect_vector,
        body_resource_budget=body_resource_budget,
        network_state=network_state,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        queue_e_repair_modulation_profile=repair_profile,
    )
    if not signal_media_runtime:
        signal_media_runtime = build_signal_media_runtime(
            run_id=run_id,
            generated_at=generated_at,
            network_state=network_state,
            body_resource_budget=body_resource_budget,
            core_affect_vector=core_affect_vector,
            offline_learning_cumulative_profile=offline_learning_cumulative_profile,
            queue_e_repair_modulation_profile=repair_profile,
        )

    belief_state = refresh_belief_confidence_from_live_turn(
        belief_state=belief_state,
        run_id=run_id,
        generated_at=generated_at,
        signal_media_runtime=signal_media_runtime,
        language_percept=language_percept,
        semantic_map=semantic_map,
        language_continuity=language_continuity,
        queue_e_repair_modulation_profile=repair_profile,
    )
    if not belief_state:
        belief_state = build_belief_state_frame(
            run_id=run_id,
            generated_at=generated_at,
            signal_media_runtime=signal_media_runtime,
            language_continuity=language_continuity,
            queue_e_repair_modulation_profile=repair_profile,
        )

    prediction_error_field = refresh_prediction_error_from_live_turn(
        prediction_error_field=prediction_error_field,
        run_id=run_id,
        generated_at=generated_at,
        turn_counter=turn_counter,
        belief_state=belief_state,
        signal_media_runtime=signal_media_runtime,
        language_percept=language_percept,
        semantic_map=semantic_map,
        body_integrator=body_integrator,
        queue_e_repair_modulation_profile=repair_profile,
    )
    if not prediction_error_field:
        prediction_error_field = build_prediction_error_field(
            run_id=run_id,
            generated_at=generated_at,
            belief_state=belief_state,
            signal_media_runtime=signal_media_runtime,
            queue_e_repair_modulation_profile=repair_profile,
        )

    active_sampling_plan = build_active_sampling_plan(
        run_id=run_id,
        generated_at=generated_at,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        signal_media_runtime=signal_media_runtime,
        queue_e_repair_modulation_profile=repair_profile,
        semantic_map=semantic_map,
        body_integrator=body_integrator,
        turn_counter=turn_counter,
    )
    if active_sampling_plan and not active_sampling_plan.get("efe_score"):
        active_sampling_plan["efe_score"] = compute_efe_score(
            signal_media_runtime=signal_media_runtime,
            semantic_map=semantic_map,
            body_integrator=body_integrator,
            repair_profile=repair_profile,
        )

    return PredictionStackRefreshResult(
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        applied=True,
    )


def maybe_run_prediction_refresh_hook(
    *,
    state_dir: Path,
    run_id: str,
    generated_at: str,
    turn_counter: int,
    signal_media_runtime: dict[str, Any] | None,
    belief_state: dict[str, Any] | None,
    prediction_error_field: dict[str, Any] | None,
    active_sampling_plan: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
    semantic_map: dict[str, Any] | None,
    core_affect_vector: dict[str, Any] | None,
    body_resource_budget: dict[str, Any] | None,
    network_state: dict[str, Any] | None,
    offline_learning_cumulative_profile: dict[str, Any] | None,
    write_json: Callable[[Path, dict[str, Any]], None],
    environ: Mapping[str, str] | None = None,
) -> PredictionStackRefreshResult:
    if not is_prediction_refresh_enabled(environ):
        return PredictionStackRefreshResult(
            signal_media_runtime=signal_media_runtime or {},
            belief_state=belief_state or {},
            prediction_error_field=prediction_error_field or {},
            active_sampling_plan=active_sampling_plan or {},
            applied=False,
        )

    body_integrator = _read_json(state_dir / "body" / "body_integrator_state.json")
    refreshed = project_prediction_stack_from_live_turn(
        run_id=run_id,
        generated_at=generated_at,
        turn_counter=turn_counter,
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        language_percept=language_percept,
        semantic_map=semantic_map,
        core_affect_vector=core_affect_vector,
        body_integrator=body_integrator,
        body_resource_budget=body_resource_budget,
        network_state=network_state,
        offline_learning_cumulative_profile=offline_learning_cumulative_profile,
    )

    signal_dir = state_dir / "signal"
    prediction_dir = state_dir / "prediction"
    write_json(signal_dir / "signal_media_runtime.json", refreshed.signal_media_runtime)
    write_json(prediction_dir / "belief_state_frame.json", refreshed.belief_state)
    write_json(prediction_dir / "prediction_error_field.json", refreshed.prediction_error_field)
    write_json(prediction_dir / "active_sampling_plan.json", refreshed.active_sampling_plan)
    return refreshed


def _resolve_queue_e_profile(
    *,
    signal_media_runtime: dict[str, Any] | None,
    belief_state: dict[str, Any] | None,
    prediction_error_field: dict[str, Any] | None,
    active_sampling_plan: dict[str, Any] | None,
) -> dict[str, Any]:
    for source in (
        active_sampling_plan,
        prediction_error_field,
        belief_state,
        signal_media_runtime,
    ):
        if not isinstance(source, dict):
            continue
        profile = source.get("queue_e_repair_modulation_profile")
        if isinstance(profile, dict) and profile:
            return json.loads(json.dumps(profile))
    return {}


def _parse_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}