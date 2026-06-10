from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from ..language.expression_monitor import (
    build_expression_monitor_state,
    build_expression_plan,
)
from ..language.inner_speech import build_inner_speech_frame
from ..language.percept import build_language_percept_frame
from ..language.semantic_map import build_semantic_map_frame


LANGUAGE_PERCEPT_REF = "runtime/state/language/language_percept_frame.json"
SEMANTIC_MAP_REF = "runtime/state/language/semantic_map_frame.json"
INNER_SPEECH_REF = "runtime/state/language/inner_speech_frame.json"
EXPRESSION_MONITOR_REF = "runtime/state/language/expression_monitor_state.json"
EXPRESSION_PLAN_REF = "runtime/state/language/expression_plan.json"


@dataclass(frozen=True)
class LiveLanguageTurnState:
    language_percept: dict[str, Any]
    semantic_map: dict[str, Any]
    inner_speech: dict[str, Any]
    expression_monitor: dict[str, Any]
    expression_plan: dict[str, Any]
    language_percept_ref: str
    semantic_map_ref: str
    inner_speech_ref: str
    expression_monitor_ref: str
    expression_plan_ref: str


def refresh_live_language_turn(
    *,
    run_id: str,
    generated_at: str,
    external_utterance: str,
    language_dir: Path,
    state_dir: Path,
    relation_scope_index: dict[str, Any],
    shared_term_registry: dict[str, Any],
    language_state: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    life_state: dict[str, Any],
    source_doc_refs: list[str],
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    write_json: Callable[[Path, dict[str, Any]], None],
) -> LiveLanguageTurnState:
    speaker_role = _active_relation_role(relation_scope_index)
    language_percept = build_language_percept_frame(
        run_id=run_id,
        generated_at=generated_at,
        incoming_turn={
            "incoming_surface": external_utterance,
            "speaker_role": speaker_role,
        },
        relation_scope_index=relation_scope_index,
        shared_term_registry=shared_term_registry,
        source_doc_refs=source_doc_refs,
        belief_state=belief_state,
        active_sampling_plan=active_sampling_plan,
    )
    semantic_map = build_semantic_map_frame(
        run_id=run_id,
        generated_at=generated_at,
        language_percept=language_percept,
        language_state=language_state,
        shared_term_registry=shared_term_registry,
        commitment_repair_index=commitment_repair_index,
        self_narrative_trace=self_narrative_trace,
        source_doc_refs=source_doc_refs,
        prediction_error_field=prediction_error_field,
        signal_media_runtime=signal_media_runtime,
    )
    inner_speech = build_inner_speech_frame(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        source_doc_refs=source_doc_refs,
        language_percept=language_percept,
        semantic_map=semantic_map,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        signal_media_runtime=signal_media_runtime,
    )
    expression_monitor = build_expression_monitor_state(
        run_id=run_id,
        generated_at=generated_at,
        source_doc_refs=source_doc_refs,
        cross_scope_risk_terms=list(language_percept.get("cross_scope_risk_terms", [])),
        ambiguity_queue=list(semantic_map.get("ambiguity_queue", [])),
        memory_write_gate=memory_write_gate,
        core_affect_vector=core_affect_vector,
        signal_media_runtime=signal_media_runtime,
    )
    expression_plan = build_expression_plan(
        run_id=run_id,
        generated_at=generated_at,
        inner_speech=inner_speech,
        semantic_map=semantic_map,
        language_percept=language_percept,
        commitment_repair_index=commitment_repair_index,
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
        source_doc_refs=source_doc_refs,
    )

    language_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)
    write_json(language_dir / "language_percept_frame.json", language_percept)
    write_json(language_dir / "semantic_map_frame.json", semantic_map)
    write_json(language_dir / "inner_speech_frame.json", inner_speech)
    write_json(language_dir / "expression_monitor_state.json", expression_monitor)
    write_json(language_dir / "expression_plan.json", expression_plan)

    return LiveLanguageTurnState(
        language_percept=language_percept,
        semantic_map=semantic_map,
        inner_speech=inner_speech,
        expression_monitor=expression_monitor,
        expression_plan=expression_plan,
        language_percept_ref=LANGUAGE_PERCEPT_REF,
        semantic_map_ref=SEMANTIC_MAP_REF,
        inner_speech_ref=INNER_SPEECH_REF,
        expression_monitor_ref=EXPRESSION_MONITOR_REF,
        expression_plan_ref=EXPRESSION_PLAN_REF,
    )


def _active_relation_role(relation_scope_index: dict[str, Any]) -> str:
    relation_scopes = relation_scope_index.get("relation_scopes", [])
    if relation_scopes and isinstance(relation_scopes[0], dict):
        relation_role = str(relation_scopes[0].get("relation_role", "")).strip()
        if relation_role:
            return relation_role
    return "friend"
