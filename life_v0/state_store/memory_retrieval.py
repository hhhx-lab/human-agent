from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from .cue_candidate_provider import (
    local_full_text_cue_candidate_provider,
    noop_cue_candidate_provider,
)
from .hippocampal_cue_index import (
    apply_hippocampal_cue_weight_decay,
    build_hippocampal_cue_index,
)
from .memory_expression_material_chain import build_memory_expression_material_chain
from .memory_trace_store import apply_retrieval_salience_delta


MEMORY_RETRIEVAL_FRAME_REF = "runtime/state/memory/memory_retrieval_frame.json"

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/41_runtime_state_store_schema.md",
    "docs/v0/shared_contracts/life_state_store_v0_schema.md",
    "docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def build_memory_retrieval_frame(
    *,
    run_id: str,
    generated_at: str,
    cue_sources: dict[str, Any] | None = None,
    external_utterance: str | None = None,
    semantic_map: dict[str, Any] | None = None,
    language_percept: dict[str, Any] | None = None,
    engram_index: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    life_schema_map: dict[str, Any] | None = None,
    pattern_completion_frame: dict[str, Any] | None = None,
    dialogue_memory_summary: dict[str, Any] | None = None,
    life_state: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    memory_validator_report: dict[str, Any] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    web_dream_learning_state: dict[str, Any] | None = None,
    cue_provider_name: str = "noop",
    source_doc_refs: list[str] | None = None,
) -> dict[str, Any]:
    cue_terms = _cue_terms(
        cue_sources=cue_sources,
        external_utterance=external_utterance,
        semantic_map=semantic_map,
        language_percept=language_percept,
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
    )
    tiered_recall = _tiered_recall(
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
        memory_trace_store=memory_trace_store,
    )
    activated_refs = _activated_refs(
        cue_terms=cue_terms,
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
        responsibility_loop_state=responsibility_loop_state,
        state_merge_guard=state_merge_guard,
    )
    relationship_hits = _relationship_hits(
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
    )
    autobiographical_hits = _autobiographical_hits(autobiographical_stack)
    schema_memory_hits = _schema_memory_hits(life_schema_map)
    pattern_completion_hits = _pattern_completion_hits(pattern_completion_frame)
    autobiographical_repair_hits = _autobiographical_responsibility_repair_hits(
        autobiographical_stack
    )
    autobiographical_repair_profile = (
        _autobiographical_responsibility_repair_profile(
            autobiographical_stack,
            autobiographical_repair_hits,
        )
    )
    dream_residue_hits = _dream_residue_hits(
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
    )
    exit_dream_next_wake_governance = _exit_dream_next_wake_governance(
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
        state_merge_guard=state_merge_guard,
    )
    responsibility_hits = _responsibility_hits(
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        life_state=life_state,
        responsibility_loop_state=responsibility_loop_state,
        autobiographical_repair_hits=autobiographical_repair_hits,
    )
    blocked_refs = _blocked_or_quarantined_refs(
        engram_index,
        life_state,
        memory_validator_report=memory_validator_report,
    )
    cue_merge = merge_cue_candidates(
        cue_terms=cue_terms,
        memory_trace_store=memory_trace_store,
        relationship_memory=relationship_memory,
        blocked_refs=blocked_refs,
        provider_name=cue_provider_name,
    )
    cue_terms = _dedupe(cue_terms + _string_list(cue_merge.get("merged_cue_terms")))
    provider_candidate_refs = _string_list(cue_merge.get("eligible_candidate_trace_refs"))
    activated_refs = _dedupe(activated_refs + provider_candidate_refs)
    cue_activation_profile = _cue_activation_profile(
        cue_terms=cue_terms,
        tiered_recall=tiered_recall,
        activated_refs=activated_refs,
        relationship_hits=relationship_hits,
        autobiographical_hits=autobiographical_hits,
        schema_memory_hits=schema_memory_hits,
        pattern_completion_hits=pattern_completion_hits,
        autobiographical_repair_hits=autobiographical_repair_hits,
        dream_residue_hits=dream_residue_hits,
        responsibility_hits=responsibility_hits,
        blocked_refs=blocked_refs,
        exit_dream_governance=exit_dream_next_wake_governance,
    )
    live_memory_trace_hits = _string_list(
        (engram_index or {}).get("live_memory_trace_refs")
    )
    reconstructive_recall_profile = _reconstructive_recall_profile(
        pattern_completion_frame=pattern_completion_frame,
        cue_terms=cue_terms,
        live_memory_trace_hits=live_memory_trace_hits,
    )
    memory_phenomenology_profile = _memory_phenomenology_profile(
        external_utterance=external_utterance,
        live_memory_trace_hits=live_memory_trace_hits,
        relationship_hits=relationship_hits,
        autobiographical_hits=autobiographical_hits,
        schema_memory_hits=schema_memory_hits,
        pattern_completion_hits=pattern_completion_hits,
        activated_refs=activated_refs,
        blocked_refs=blocked_refs,
        memory_trace_store=memory_trace_store,
        dream_residue_hits=dream_residue_hits,
        reconstructive_recall_profile=reconstructive_recall_profile,
    )
    recall_to_expression_profile = _recall_to_expression_profile(
        cue_activation_profile=cue_activation_profile,
        reconstruction_inputs=_reconstruction_inputs(
            cue_terms=cue_terms,
            tiered_recall=tiered_recall,
            relationship_hits=relationship_hits,
            autobiographical_hits=autobiographical_hits,
            schema_memory_hits=schema_memory_hits,
            pattern_completion_hits=pattern_completion_hits,
            autobiographical_repair_hits=autobiographical_repair_hits,
            dream_residue_hits=dream_residue_hits,
            responsibility_hits=responsibility_hits,
        ),
        activated_refs=activated_refs,
        relationship_hits=relationship_hits,
        autobiographical_hits=autobiographical_hits,
        autobiographical_repair_hits=autobiographical_repair_hits,
        dream_residue_hits=dream_residue_hits,
        responsibility_hits=responsibility_hits,
        schema_memory_hits=schema_memory_hits,
        pattern_completion_hits=pattern_completion_hits,
        live_memory_trace_hits=live_memory_trace_hits,
        blocked_refs=blocked_refs,
        exit_dream_governance=exit_dream_next_wake_governance,
        phenomenology_profile=memory_phenomenology_profile,
    )
    memory_expression_material_chain = build_memory_expression_material_chain(
        memory_retrieval_frame={
            "cue_terms": cue_terms,
            "memory_phenomenology_profile": memory_phenomenology_profile,
            "reconstructive_recall_profile": reconstructive_recall_profile,
            "recall_to_expression_profile": recall_to_expression_profile,
        },
        pattern_completion_frame=pattern_completion_frame,
        dream_reentry_refs=_dream_reentry_refs(
            dream_residue_hits=dream_residue_hits,
            exit_dream_governance=exit_dream_next_wake_governance,
        ),
        memory_hygiene_refs=_memory_hygiene_refs(memory_trace_store),
        web_dream_refs=_web_dream_refs(memory_trace_store),
        structured_wake_question_candidates=_structured_wake_question_candidates(
            memory_trace_store=memory_trace_store,
            web_dream_learning_state=web_dream_learning_state,
        ),
    )
    recall_to_expression_profile = _apply_expression_material_chain_to_recall_profile(
        recall_to_expression_profile,
        memory_expression_material_chain=memory_expression_material_chain,
    )
    source_docs = _dedupe(_string_list(source_doc_refs) + SOURCE_DOC_REFS)
    return {
        "schema_version": "memory_retrieval_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "retrieval_mode": "cue_driven_reconstructive_recall",
        "retrieval_frame_ref": MEMORY_RETRIEVAL_FRAME_REF,
        "cue_sources": _cue_source_summary(
            cue_sources=cue_sources,
            external_utterance=external_utterance,
            semantic_map=semantic_map,
            language_percept=language_percept,
        ),
        "cue_terms": cue_terms,
        "cue_fingerprint": _fingerprint(cue_terms),
        "activated_engram_refs": activated_refs,
        "relationship_memory_hits": relationship_hits,
        "autobiographical_hits": autobiographical_hits,
        "schema_memory_hits": schema_memory_hits,
        "pattern_completion_hits": pattern_completion_hits,
        "autobiographical_responsibility_repair_hits": (
            autobiographical_repair_hits
        ),
        "autobiographical_responsibility_repair_profile": (
            autobiographical_repair_profile
        ),
        "dream_residue_hits": dream_residue_hits,
        "exit_dream_next_wake_governance": exit_dream_next_wake_governance,
        "responsibility_hits": responsibility_hits,
        "tiered_recall": tiered_recall,
        "cue_activation_profile": cue_activation_profile,
        "recall_to_expression_profile": recall_to_expression_profile,
        "reconstruction_inputs": _reconstruction_inputs(
            cue_terms=cue_terms,
            tiered_recall=tiered_recall,
            relationship_hits=relationship_hits,
            autobiographical_hits=autobiographical_hits,
            schema_memory_hits=schema_memory_hits,
            pattern_completion_hits=pattern_completion_hits,
            autobiographical_repair_hits=autobiographical_repair_hits,
            dream_residue_hits=dream_residue_hits,
            responsibility_hits=responsibility_hits,
        ),
        "blocked_or_quarantined_refs": blocked_refs,
        "cue_provider_audit": cue_merge.get("cue_provider_audit"),
        "memory_phenomenology_profile": memory_phenomenology_profile,
        "reconstructive_recall_profile": reconstructive_recall_profile,
        "memory_expression_material_chain": memory_expression_material_chain,
        "cue_provider_candidate_trace_refs": provider_candidate_refs,
        "memory_validator_report_ref": (
            "runtime/state/memory/memory_validator_report.json"
            if memory_validator_report
            else None
        ),
        "writeback_candidates": _writeback_candidates(
            activated_refs=activated_refs,
            blocked_refs=blocked_refs,
            exit_dream_governance=exit_dream_next_wake_governance,
        ),
        "consumer_refs": [
            "runtime/state/language/model_expression_state.json#model_expression_context_summary",
            "runtime/reports/latest/dialogue_writeback_bundle.json#memory_retrieval_writeback_refs",
            "runtime/state/life_state.json#memory_index.memory_retrieval_refs",
            "runtime/state/consciousness/workspace_frame.json#memory_retrieval_refs",
        ],
        "source_doc_refs": source_docs,
    }


def project_memory_retrieval_from_live_turn(
    *,
    memory_retrieval_frame: dict[str, Any] | None,
    run_id: str,
    generated_at: str,
    external_utterance: str,
    semantic_map: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    responsibility_loop_state: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
    memory_validator_report: dict[str, Any] | None = None,
    life_schema_map: dict[str, Any] | None = None,
    pattern_completion_frame: dict[str, Any] | None = None,
    memory_trace_store: dict[str, Any] | None = None,
    memory_feedback_event: dict[str, Any] | None = None,
    web_dream_learning_state: dict[str, Any] | None = None,
    cue_provider_name: str = "noop",
    live_language_turn_refs: list[str] | None = None,
    dialogue_turn_refs: list[str] | None = None,
) -> dict[str, Any]:
    previous = memory_retrieval_frame or {}
    if web_dream_learning_state is None:
        prior_candidates = (
            (previous.get("memory_expression_material_chain") or {}).get(
                "structured_wake_question_candidates"
            )
            or []
        )
        if prior_candidates:
            web_dream_learning_state = {
                "structured_wake_question_candidates": prior_candidates,
            }
    cue_sources = {
        "previous_retrieval_frame_ref": (
            MEMORY_RETRIEVAL_FRAME_REF if previous else None
        ),
        "live_language_turn_refs": list(live_language_turn_refs or []),
        "dialogue_turn_refs": list(dialogue_turn_refs or []),
        "semantic_map_ref": "runtime/state/language/semantic_map_frame.json"
        if semantic_map
        else None,
        "language_percept_ref": "runtime/state/language/language_percept_frame.json"
        if language_percept
        else None,
    }
    frame = build_memory_retrieval_frame(
        run_id=run_id,
        generated_at=generated_at,
        cue_sources=cue_sources,
        external_utterance=external_utterance,
        semantic_map=semantic_map,
        language_percept=language_percept,
        engram_index=engram_index,
        relationship_memory=relationship_memory,
        autobiographical_stack=autobiographical_stack,
        life_schema_map=life_schema_map,
        pattern_completion_frame=pattern_completion_frame,
        dialogue_memory_summary=dialogue_memory_summary,
        life_state=life_state,
        responsibility_loop_state=responsibility_loop_state,
        state_merge_guard=state_merge_guard,
        memory_validator_report=memory_validator_report,
        memory_trace_store=memory_trace_store,
        web_dream_learning_state=web_dream_learning_state,
        cue_provider_name=cue_provider_name,
    )
    if memory_feedback_event and memory_feedback_event.get("event_type"):
        recall_profile = frame.get("recall_to_expression_profile")
        if isinstance(recall_profile, dict):
            hooks = _string_list(recall_profile.get("post_expression_reconsolidation_hooks"))
            route = f"post_expression_{memory_feedback_event['event_type']}_reconsolidation"
            recall_profile["post_expression_reconsolidation_hooks"] = _dedupe(
                hooks + [route, "correction_updates_contradiction_links"]
            )
            recall_profile["reconsolidation_route"] = route
            recall_profile["reconsolidation_trigger_event_ref"] = (
                memory_feedback_event.get("trigger_event_ref")
            )
    frame["previous_retrieval_fingerprint"] = previous.get("cue_fingerprint")
    frame["previous_activated_ref_count"] = len(
        _string_list(previous.get("activated_engram_refs"))
    )
    frame["live_language_turn_refs"] = list(live_language_turn_refs or [])
    frame["dialogue_turn_refs"] = list(dialogue_turn_refs or [])
    frame["last_external_utterance_sha256"] = _sha256(external_utterance)
    return frame


def is_memory_salience_tick_enabled(environ: Mapping[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return _parse_bool(env.get("DIGITAL_LIFE_MEMORY_SALIENCE_TICK"), False)


@dataclass(frozen=True)
class MemorySalienceTickResult:
    memory_trace_store: dict[str, Any]
    hippocampal_cue_index: dict[str, Any]
    memory_retrieval_frame: dict[str, Any]
    salience_tick_report: dict[str, Any]
    applied: bool


def maybe_apply_retrieval_salience_tick(
    *,
    memory_trace_store: dict[str, Any] | None,
    memory_retrieval_frame: dict[str, Any] | None,
    hippocampal_cue_index: dict[str, Any] | None,
    run_id: str,
    generated_at: str,
    turn_counter: int | None = None,
    relationship_memory: dict[str, Any] | None = None,
    body_integrator: dict[str, Any] | None = None,
    environ: Mapping[str, str] | None = None,
) -> MemorySalienceTickResult:
    frame = dict(memory_retrieval_frame or {})
    store = json.loads(json.dumps(memory_trace_store or {}))
    cue_index = dict(hippocampal_cue_index or {})
    if not is_memory_salience_tick_enabled(environ):
        return MemorySalienceTickResult(
            memory_trace_store=store,
            hippocampal_cue_index=cue_index,
            memory_retrieval_frame=frame,
            salience_tick_report={},
            applied=False,
        )

    retrieval_hits = _extract_retrieval_salience_hits(frame)
    if not retrieval_hits:
        return MemorySalienceTickResult(
            memory_trace_store=store,
            hippocampal_cue_index=cue_index,
            memory_retrieval_frame=frame,
            salience_tick_report={
                "schema_version": "memory_retrieval_salience_tick_v0",
                "applied": False,
                "reason": "no_retrieval_hits",
            },
            applied=False,
        )

    continuous = (body_integrator or {}).get("continuous") or {}
    allostatic_load = float(continuous.get("allostatic_load", 0.0) or 0.0)
    reconstructive = frame.get("reconstructive_recall_profile") or {}
    mean_activation = reconstructive.get("mean_activation_score")
    if mean_activation is not None:
        mean_activation = float(mean_activation)

    delta_result = apply_retrieval_salience_delta(
        store,
        retrieval_hits=retrieval_hits,
        run_id=run_id,
        generated_at=generated_at,
        turn_counter=turn_counter,
        allostatic_load=allostatic_load,
        mean_activation_score=mean_activation,
    )
    store = delta_result["memory_trace_store"]
    report = delta_result["salience_tick_report"]

    if cue_index:
        cue_index = apply_hippocampal_cue_weight_decay(
            cue_index,
            generated_at=generated_at,
            body_integrator=body_integrator,
        )
    else:
        cue_index = build_hippocampal_cue_index(
            run_id=run_id,
            generated_at=generated_at,
            memory_trace_store=store,
            relationship_memory=relationship_memory,
        )

    frame["retrieval_salience_tick_report"] = report
    frame["retrieval_salience_tick_applied"] = bool(report.get("applied"))
    return MemorySalienceTickResult(
        memory_trace_store=store,
        hippocampal_cue_index=cue_index,
        memory_retrieval_frame=frame,
        salience_tick_report=report,
        applied=bool(report.get("applied")),
    )


def maybe_run_memory_salience_tick_hook(
    *,
    memory_dir: Path,
    memory_retrieval_frame: dict[str, Any] | None,
    run_id: str,
    generated_at: str,
    turn_counter: int | None = None,
    relationship_memory: dict[str, Any] | None = None,
    body_integrator: dict[str, Any] | None = None,
    write_json: Callable[[Path, dict[str, Any]], None],
    environ: Mapping[str, str] | None = None,
) -> MemorySalienceTickResult:
    memory_trace_store = _read_json(memory_dir / "memory_trace_store.json")
    hippocampal_cue_index = _read_json(memory_dir / "hippocampal_cue_index.json")
    result = maybe_apply_retrieval_salience_tick(
        memory_trace_store=memory_trace_store,
        memory_retrieval_frame=memory_retrieval_frame,
        hippocampal_cue_index=hippocampal_cue_index,
        run_id=run_id,
        generated_at=generated_at,
        turn_counter=turn_counter,
        relationship_memory=relationship_memory,
        body_integrator=body_integrator,
        environ=environ,
    )
    if not result.applied:
        return result

    write_json(memory_dir / "memory_trace_store.json", result.memory_trace_store)
    write_json(memory_dir / "hippocampal_cue_index.json", result.hippocampal_cue_index)
    write_json(memory_dir / "memory_retrieval_frame.json", result.memory_retrieval_frame)
    return result


def _extract_retrieval_salience_hits(memory_retrieval_frame: dict[str, Any]) -> list[str]:
    frame = memory_retrieval_frame or {}
    hits: list[str] = []
    reconstructive = frame.get("reconstructive_recall_profile") or {}
    hits.extend(_string_list(reconstructive.get("reconstruction_fragment_refs")))
    tiered = frame.get("tiered_recall") or {}
    hits.extend(_string_list(tiered.get("salient_core_refs")))
    hits.extend(_string_list(tiered.get("retrievable_context_refs")))
    hits.extend(
        ref
        for ref in _string_list(frame.get("activated_engram_refs"))
        if "memory_trace_store.json#" in ref
    )
    return _dedupe(hits)


def memory_retrieval_context_summary(
    memory_retrieval_frame: dict[str, Any] | None,
) -> dict[str, Any]:
    frame = memory_retrieval_frame or {}
    if not frame:
        return {}
    tiered = frame.get("tiered_recall", {})
    reconstruction = frame.get("reconstruction_inputs", {})
    cue_activation = frame.get("cue_activation_profile")
    if not isinstance(cue_activation, dict):
        cue_activation = {}
    recall_to_expression = frame.get("recall_to_expression_profile")
    if not isinstance(recall_to_expression, dict):
        recall_to_expression = {}
    return {
        "memory_retrieval_frame_ref": MEMORY_RETRIEVAL_FRAME_REF,
        "retrieval_mode": frame.get("retrieval_mode"),
        "cue_terms": _string_list(frame.get("cue_terms"))[:12],
        "cue_activation_profile_ref": cue_activation.get("profile_ref"),
        "cue_activation_profile_boundary": cue_activation.get(
            "activation_boundary"
        ),
        "cue_activation_dominant_family": cue_activation.get("dominant_family"),
        "cue_activation_family_order": _string_list(
            cue_activation.get("activated_family_order")
        )[:8],
        "cue_activation_route_count": cue_activation.get(
            "activation_route_count"
        ),
        "cue_activation_match_strength": cue_activation.get(
            "activation_match_strength"
        ),
        "cue_activation_ref_count": cue_activation.get("activation_ref_count"),
        "recall_to_expression_profile_ref": recall_to_expression.get("profile_ref"),
        "recall_to_expression_closure_status": recall_to_expression.get(
            "closure_status"
        ),
        "memory_phenomenology_profile_ref": (
            frame.get("memory_phenomenology_profile") or {}
        ).get("profile_ref"),
        "recall_phenomenology": (
            frame.get("memory_phenomenology_profile") or {}
        ).get("recall_phenomenology"),
        "memory_accessibility_level": (
            frame.get("memory_phenomenology_profile") or {}
        ).get("accessibility_level"),
        "uncertain_boundary_active": (
            frame.get("memory_phenomenology_profile") or {}
        ).get("uncertain_boundary_active"),
        "cross_modal_evidence_ref_count": (
            frame.get("memory_phenomenology_profile") or {}
        ).get("cross_modal_evidence_ref_count"),
        "recall_to_expression_boundary": recall_to_expression.get(
            "expression_boundary"
        ),
        "recall_to_expression_reportability_policy": recall_to_expression.get(
            "reportability_policy"
        ),
        "recall_to_expression_source_ref_count": recall_to_expression.get(
            "expression_source_ref_count"
        ),
        "recall_to_expression_reportable_source_ref_count": (
            recall_to_expression.get("reportable_source_ref_count")
            if recall_to_expression.get("reportable_source_ref_count") is not None
            else _fallback_reportable_source_ref_count(frame)
        ),
        "recall_to_expression_influence_families": _string_list(
            recall_to_expression.get("expression_influence_families")
        )[:8],
        "recall_to_expression_source_boundary_flags": _string_list(
            recall_to_expression.get("source_boundary_flags")
        )[:8],
        "recall_to_expression_guardrails": _string_list(
            recall_to_expression.get("expression_guardrails")
        )[:8],
        "recall_to_expression_guardrail_count": len(
            _string_list(recall_to_expression.get("expression_guardrails"))
        ),
        "live_memory_trace_ref_count": len(
            _string_list(
                (recall_to_expression.get("expression_source_refs") or [])
            )
        ),
        "reconsolidation_route": recall_to_expression.get("reconsolidation_route"),
        "cue_provider_audit_status": (frame.get("cue_provider_audit") or {}).get(
            "provider_status"
        ),
        "cue_provider_name": (frame.get("cue_provider_audit") or {}).get(
            "provider_name"
        ),
        "post_expression_reconsolidation_hooks": _string_list(
            recall_to_expression.get("post_expression_reconsolidation_hooks")
        )[:8],
        "recall_to_expression_post_expression_reconsolidation_hooks": _string_list(
            recall_to_expression.get("post_expression_reconsolidation_hooks")
        )[:8],
        "recall_to_expression_post_expression_reconsolidation_hook_count": len(
            _string_list(
                recall_to_expression.get("post_expression_reconsolidation_hooks")
            )
        ),
        "activated_engram_ref_count": len(
            _string_list(frame.get("activated_engram_refs"))
        ),
        "salient_core_ref_count": len(
            _string_list((tiered or {}).get("salient_core_refs"))
        ),
        "retrievable_context_ref_count": len(
            _string_list((tiered or {}).get("retrievable_context_refs"))
        ),
        "deep_sediment_ref_count": len(
            _string_list((tiered or {}).get("deep_sediment_refs"))
        ),
        "relationship_hit_count": len(
            _string_list(frame.get("relationship_memory_hits"))
        ),
        "autobiographical_hit_count": len(
            _string_list(frame.get("autobiographical_hits"))
        ),
        "schema_memory_hit_count": len(
            _string_list(frame.get("schema_memory_hits"))
        ),
        "pattern_completion_hit_count": len(
            _string_list(frame.get("pattern_completion_hits"))
        ),
        "autobiographical_responsibility_repair_hit_count": len(
            _string_list(frame.get("autobiographical_responsibility_repair_hits"))
        ),
        "autobiographical_repair_pressure_level": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("pressure_level"),
        "autobiographical_repair_attention_target": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("attention_target"),
        "autobiographical_repair_projection_boundary": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("projection_boundary"),
        "autobiographical_repair_retrieval_boundary": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("retrieval_boundary"),
        "autobiographical_repair_boundary": (
            frame.get("autobiographical_responsibility_repair_profile") or {}
        ).get("retrieval_boundary"),
        "dream_residue_hit_count": len(_string_list(frame.get("dream_residue_hits"))),
        "exit_dream_next_wake_cue_ref_count": len(
            _string_list(
                (frame.get("exit_dream_next_wake_governance") or {}).get(
                    "next_wake_memory_cue_refs"
                )
            )
        ),
        "exit_dream_write_gate_ref": (
            frame.get("exit_dream_next_wake_governance") or {}
        ).get("memory_write_gate_ref"),
        "exit_dream_state_merge_guard_ref": (
            frame.get("exit_dream_next_wake_governance") or {}
        ).get("state_merge_guard_ref"),
        "exit_dream_fact_boundary_ref": (
            frame.get("exit_dream_next_wake_governance") or {}
        ).get("dream_fact_boundary_ref"),
        "responsibility_hit_count": len(_string_list(frame.get("responsibility_hits"))),
        "blocked_or_quarantined_ref_count": len(
            _string_list(frame.get("blocked_or_quarantined_refs"))
        ),
        "reconstruction_focus": (reconstruction or {}).get("reconstruction_focus"),
        "memory_expression_material_chain_ref": (
            frame.get("memory_expression_material_chain") or {}
        ).get("chain_ref"),
        "memory_expression_material_chain_closed": (
            frame.get("memory_expression_material_chain") or {}
        ).get("chain_closed"),
        "expression_release_posture": (
            frame.get("memory_expression_material_chain") or {}
        ).get("expression_release_posture"),
        "tip_of_tongue_gate_status": (
            (frame.get("memory_expression_material_chain") or {}).get(
                "tip_of_tongue_gate"
            )
            or {}
        ).get("gate_status"),
        "source_doc_refs": _string_list(frame.get("source_doc_refs"))[:8],
    }


def _apply_expression_material_chain_to_recall_profile(
    recall_profile: dict[str, Any],
    *,
    memory_expression_material_chain: dict[str, Any],
) -> dict[str, Any]:
    updated = dict(recall_profile)
    tip_gate = memory_expression_material_chain.get("tip_of_tongue_gate") or {}
    posture = memory_expression_material_chain.get("expression_release_posture")
    if posture:
        updated["expression_release_posture"] = posture
        updated["memory_expression_material_chain_ref"] = (
            memory_expression_material_chain.get("chain_ref")
        )
    if tip_gate.get("gate_status") == "blocked":
        updated["closure_status"] = "withhold_pending_reconstruction"
        guardrails = _string_list(updated.get("expression_guardrails"))
        updated["expression_guardrails"] = _dedupe(
            guardrails + ["tip_of_tongue_blocks_expression_without_fragments"]
        )
    elif tip_gate.get("gate_status") == "cautious":
        updated["closure_status"] = "uncertain"
        updated["expression_guardrails"] = _dedupe(
            _string_list(updated.get("expression_guardrails"))
            + ["uncertainty_boundary_required_for_partial_recall"]
        )
    return updated


def _fallback_reportable_source_ref_count(frame: dict[str, Any]) -> int:
    source_refs = _dedupe(
        _string_list(frame.get("activated_engram_refs"))
        + _string_list(frame.get("relationship_memory_hits"))
        + _string_list(frame.get("autobiographical_hits"))
        + _string_list(frame.get("autobiographical_responsibility_repair_hits"))
        + _string_list(frame.get("dream_residue_hits"))
        + _string_list(frame.get("responsibility_hits"))
        + _string_list(
            (frame.get("exit_dream_next_wake_governance") or {}).get(
                "next_wake_memory_cue_refs"
            )
        )
    )
    blocked = set(_string_list(frame.get("blocked_or_quarantined_refs")))
    return len([ref for ref in source_refs if ref not in blocked])


def _cue_terms(
    *,
    cue_sources: dict[str, Any] | None,
    external_utterance: str | None,
    semantic_map: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
) -> list[str]:
    terms: list[str] = []
    if isinstance(cue_sources, dict):
        for key, value in cue_sources.items():
            normalized_key = _normalize_cue(str(key))
            if normalized_key:
                terms.append(normalized_key)
            if isinstance(value, str):
                terms.extend(_extract_text_cues(value))
                normalized_value = _normalize_cue(value)
                if normalized_value:
                    terms.append(normalized_value)
            else:
                terms.extend(_string_list(value))
    terms.extend(_extract_text_cues(external_utterance or ""))
    terms.extend(_string_list((semantic_map or {}).get("ambiguity_queue")))
    terms.extend(_string_list((semantic_map or {}).get("relationship_topic_refs")))
    terms.extend(_string_list((semantic_map or {}).get("commitment_trace_refs")))
    terms.extend(_string_list((semantic_map or {}).get("repair_trace_refs")))
    terms.extend(_string_list((language_percept or {}).get("shared_term_hits")))
    terms.extend(_string_list((language_percept or {}).get("repair_trigger_candidates")))
    terms.extend(_string_list((language_percept or {}).get("commitment_trigger_candidates")))
    relation_profile = (relationship_memory or {}).get("relation_person_profile")
    dialogue_profile = (dialogue_memory_summary or {}).get("relation_person_profile")
    if isinstance(relation_profile, dict):
        terms.extend(_valid_observed_names(relation_profile.get("observed_names")))
        terms.extend(_string_list(relation_profile.get("preference_hypotheses")))
    if isinstance(dialogue_profile, dict):
        terms.extend(_valid_observed_names(dialogue_profile.get("observed_names")))
        terms.extend(_string_list(dialogue_profile.get("preference_hypotheses")))
    terms.extend(_string_list((relationship_memory or {}).get("relationship_theme_tags")))
    terms.extend(_string_list((dialogue_memory_summary or {}).get("relationship_theme_tags")))
    terms.extend(_string_list((relationship_memory or {}).get("next_wake_cues")))
    terms.extend(_string_list((dialogue_memory_summary or {}).get("next_wake_cues")))
    terms.extend(
        _string_list((relationship_memory or {}).get("next_wake_memory_cue_refs"))
    )
    terms.extend(
        _string_list((dialogue_memory_summary or {}).get("next_wake_memory_cue_refs"))
    )
    if isinstance(cue_sources, dict):
        terms.extend(_string_list(cue_sources.get("dialogue_turn_refs")))
        terms.extend(_string_list(cue_sources.get("live_language_turn_refs")))
    return _dedupe([_normalize_cue(term) for term in terms if _normalize_cue(term)])[:48]


def _valid_observed_names(value: Any) -> list[str]:
    from .relation_identity_hygiene import sanitize_observed_names

    return sanitize_observed_names(_string_list(value))


def _cue_source_summary(
    *,
    cue_sources: dict[str, Any] | None,
    external_utterance: str | None,
    semantic_map: dict[str, Any] | None,
    language_percept: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "external_utterance_sha256": _sha256(external_utterance or ""),
        "semantic_focus": (semantic_map or {}).get("semantic_focus"),
        "language_percept_ref": (cue_sources or {}).get("language_percept_ref"),
        "semantic_map_ref": (cue_sources or {}).get("semantic_map_ref"),
        "dialogue_turn_refs": _string_list((cue_sources or {}).get("dialogue_turn_refs")),
        "live_language_turn_refs": _string_list((cue_sources or {}).get("live_language_turn_refs")),
        "shared_term_hit_count": len(
            _string_list((language_percept or {}).get("shared_term_hits"))
        ),
        "ambiguity_count": len(_string_list((semantic_map or {}).get("ambiguity_queue"))),
    }


def _tiered_recall(
    *,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    memory_trace_store: dict[str, Any] | None = None,
) -> dict[str, Any]:
    engram_tier = (engram_index or {}).get("memory_tier_index")
    if not isinstance(engram_tier, dict):
        engram_tier = {}
    relationship_tier = (relationship_memory or {}).get("memory_tier_projection")
    if not isinstance(relationship_tier, dict):
        relationship_tier = {}
    dialogue_tier = (dialogue_memory_summary or {}).get("memory_tiering")
    if not isinstance(dialogue_tier, dict):
        dialogue_tier = {}
    life_tier = ((life_state or {}).get("memory_index") or {}).get("memory_tier_refs")
    if not isinstance(life_tier, dict):
        life_tier = {}
    trace_tier_refs = _trace_accessibility_tier_refs(memory_trace_store)
    return {
        "schema_version": "memory_retrieval_tiered_recall_v0",
        "tier_policy": "salient_core_then_context_then_deep_sediment",
        "salient_core_refs": _dedupe(
            _string_list(engram_tier.get("salient_core_refs"))
            + _string_list(relationship_tier.get("salient_core_episode_refs"))
            + _string_list(dialogue_tier.get("salient_core_episode_refs"))
            + _string_list(life_tier.get("salient_core_refs"))
            + trace_tier_refs.get("salient_core_refs", [])
        ),
        "retrievable_context_refs": _dedupe(
            _string_list(engram_tier.get("retrievable_context_refs"))
            + _string_list(relationship_tier.get("retrievable_context_episode_refs"))
            + _string_list(dialogue_tier.get("retrievable_context_episode_refs"))
            + _string_list(life_tier.get("retrievable_context_refs"))
            + trace_tier_refs.get("retrievable_context_refs", [])
        ),
        "deep_sediment_refs": _dedupe(
            _string_list(engram_tier.get("deep_sediment_refs"))
            + _string_list(relationship_tier.get("deep_sediment_episode_refs"))
            + _string_list(dialogue_tier.get("deep_sediment_episode_refs"))
            + _string_list(life_tier.get("deep_sediment_refs"))
            + trace_tier_refs.get("deep_sediment_refs", [])
        ),
        "trace_accessibility_suppression": trace_tier_refs.get(
            "suppression_profile", {}
        ),
        "fact_boundary": "retrieval_priority_does_not_promote_dream_or_hypothesis_to_fact",
    }


def _activated_refs(
    *,
    cue_terms: list[str],
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    responsibility_loop_state: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
) -> list[str]:
    refs = []
    refs.extend(_string_list((engram_index or {}).get("live_dialogue_turn_refs")))
    refs.extend(_string_list((engram_index or {}).get("live_language_turn_refs")))
    refs.extend(_string_list((engram_index or {}).get("relationship_memory_refs")))
    refs.extend(_string_list((engram_index or {}).get("autobiographical_memory_refs")))
    refs.extend(_string_list((relationship_memory or {}).get("shared_memory_refs")))
    refs.extend(_string_list((relationship_memory or {}).get("dialogue_summary_refs")))
    refs.extend(_string_list((relationship_memory or {}).get("next_wake_memory_cue_refs")))
    refs.extend(_string_list((autobiographical_stack or {}).get("turn_refs")))
    refs.extend(_string_list((autobiographical_stack or {}).get("narrative_refs")))
    refs.extend(_string_list((autobiographical_stack or {}).get("next_wake_memory_cue_refs")))
    refs.extend(
        _autobiographical_responsibility_repair_hits(autobiographical_stack)
    )
    refs.extend(_string_list((dialogue_memory_summary or {}).get("source_dialogue_refs")))
    refs.extend(_string_list((dialogue_memory_summary or {}).get("next_wake_memory_cue_refs")))
    refs.extend(_string_list(((life_state or {}).get("memory_index") or {}).get("relationship_memory_refs")))
    refs.extend(_string_list(((life_state or {}).get("memory_index") or {}).get("next_wake_memory_cue_refs")))
    refs.extend(_string_list((responsibility_loop_state or {}).get("repair_obligation_refs")))
    refs.extend(_flatten_change_sources((state_merge_guard or {}).get("long_term_change_sources")))
    if not cue_terms:
        refs.extend(
            [
                "runtime/state/memory/engram_index.json",
                "runtime/state/memory/relationship_memory.json",
            ]
        )
    return _dedupe(refs)[:64]


def _relationship_hits(
    *,
    relationship_memory: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
) -> list[str]:
    return _dedupe(
        _string_list((relationship_memory or {}).get("shared_memory_refs"))
        + _string_list((relationship_memory or {}).get("timeline_refs"))
        + _string_list((relationship_memory or {}).get("dialogue_summary_refs"))
        + (
            ["runtime/state/memory/dialogue_memory_summary.json"]
            if dialogue_memory_summary
            else []
        )
    )[:24]


def _autobiographical_hits(autobiographical_stack: dict[str, Any] | None) -> list[str]:
    return _dedupe(
        _string_list((autobiographical_stack or {}).get("anchor_refs"))
        + _string_list((autobiographical_stack or {}).get("turn_refs"))
        + _string_list((autobiographical_stack or {}).get("narrative_refs"))
        + _string_list((autobiographical_stack or {}).get("relationship_turn_refs"))
    )[:24]


def _schema_memory_hits(life_schema_map: dict[str, Any] | None) -> list[str]:
    schema_map = life_schema_map or {}
    schemas = [
        schema for schema in schema_map.get("schemas", []) if isinstance(schema, dict)
    ]
    schema_root_ref = (
        f"{schema_map.get('schema_map_ref') or 'runtime/state/memory/life_schema_map.json'}#schema_refs"
        if schema_map
        else "runtime/state/memory/life_schema_map.json#schema_refs"
    )
    hits = _dedupe(
        [schema_root_ref]
        + _string_list(schema_map.get("schema_refs"))
        + [
            str(schema.get("schema_ref"))
            for schema in schemas
            if schema.get("schema_ref")
        ]
    )
    dominant_schema_kind = str(schema_map.get("dominant_schema_kind") or "")
    if dominant_schema_kind:
        hits.extend(
            _dedupe(
                [
                    f"runtime/state/memory/life_schema_map.json#schema_kind:{dominant_schema_kind}",
                    f"runtime/state/memory/life_schema_map.json#schema_focus:{schema_map.get('dominant_schema_focus')}",
                ]
            )
        )
    for schema in schemas:
        schema_kind = str(schema.get("schema_kind") or "")
        schema_ref = str(schema.get("schema_ref") or "")
        if not schema_kind and not schema_ref:
            continue
        hits.append(schema_ref or f"runtime/state/memory/life_schema_map.json#schema_kind:{schema_kind}")
        if schema_kind:
            hits.append(f"runtime/state/memory/life_schema_map.json#schema_kind:{schema_kind}")
        focus = str(schema.get("output_focus") or "")
        if focus:
            hits.append(f"runtime/state/memory/life_schema_map.json#schema_focus:{focus}")
    if not hits and schema_map:
        hits.extend(
            [
                "runtime/state/memory/life_schema_map.json#schema_refs",
                "runtime/state/memory/life_schema_map.json",
            ]
        )
    return _dedupe([hit for hit in hits if hit])[:24]


def _pattern_completion_hits(
    pattern_completion_frame: dict[str, Any] | None,
) -> list[str]:
    frame = pattern_completion_frame or {}
    candidates = [
        candidate
        for candidate in frame.get("completion_candidates", [])
        if isinstance(candidate, dict)
    ]
    hits = _dedupe(
        (
            ["runtime/state/memory/pattern_completion_frame.json"]
            if frame
            else []
        )
        + _string_list(frame.get("frame_ref"))
        + [
            str(candidate.get("candidate_ref"))
            for candidate in candidates
            if candidate.get("candidate_ref")
        ]
        + [
            f"runtime/state/memory/pattern_completion_frame.json#candidate_kind:{candidate.get('candidate_kind')}"
            for candidate in candidates
            if candidate.get("candidate_kind")
        ]
        + [
            str(fragment.get("trace_ref"))
            for candidate in candidates
            for fragment in candidate.get("reconstruction_fragments", [])
            if isinstance(fragment, dict) and fragment.get("trace_ref")
        ]
        + [
            str(fragment.get("trace_ref"))
            for fragment in (frame.get("reconstructive_completion") or {}).get(
                "reconstruction_fragments", []
            )
            if isinstance(fragment, dict) and fragment.get("trace_ref")
        ]
    )
    return [hit for hit in hits if hit][:24]


def _autobiographical_responsibility_repair_hits(
    autobiographical_stack: dict[str, Any] | None,
) -> list[str]:
    stack = autobiographical_stack or {}
    projection = stack.get("responsibility_repair_projection")
    if not isinstance(projection, dict):
        projection = {}
    return _dedupe(
        _string_list(stack.get("autobiographical_responsibility_refs"))
        + _string_list(stack.get("autobiographical_regret_refs"))
        + _string_list(stack.get("autobiographical_repair_refs"))
        + _string_list(stack.get("queue_e_repair_refs"))
        + _string_list(projection.get("responsibility_refs"))
        + _string_list(projection.get("regret_refs"))
        + _string_list(projection.get("repair_refs"))
        + _string_list(projection.get("queue_e_repair_refs"))
    )[:32]


def _autobiographical_responsibility_repair_profile(
    autobiographical_stack: dict[str, Any] | None,
    repair_hits: list[str],
) -> dict[str, Any]:
    if not repair_hits:
        return {}
    projection = (autobiographical_stack or {}).get(
        "responsibility_repair_projection"
    )
    if not isinstance(projection, dict):
        projection = {}
    return {
        "schema_version": "memory_retrieval_autobiographical_repair_profile_v0",
        "projection_ref": (
            "runtime/state/self/autobiographical_stack.json"
            "#responsibility_repair_projection"
        ),
        "hit_count": len(repair_hits),
        "responsibility_ref_count": len(
            _string_list(projection.get("responsibility_refs"))
        ),
        "regret_ref_count": len(_string_list(projection.get("regret_refs"))),
        "repair_ref_count": len(_string_list(projection.get("repair_refs"))),
        "queue_e_repair_ref_count": len(
            _string_list(projection.get("queue_e_repair_refs"))
        ),
        "pressure_level": projection.get("pressure_level"),
        "attention_target": projection.get("attention_target"),
        "queue_e_priority_band": projection.get("queue_e_priority_band"),
        "repair_followup_required": bool(
            projection.get("repair_followup_required")
        ),
        "projection_boundary": projection.get(
            "projection_boundary",
            "autobiographical_repair_evidence_not_spoken_language",
        ),
        "retrieval_boundary": (
            "autobiographical_repair_retrieval_not_spoken_language"
        ),
    }


def _dream_residue_hits(
    *,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
) -> list[str]:
    return _dedupe(
        _string_list((engram_index or {}).get("dream_memory_refs"))
        + _string_list((engram_index or {}).get("exit_dream_consolidation_refs"))
        + _string_list((relationship_memory or {}).get("exit_dream_consolidation_refs"))
        + _string_list((relationship_memory or {}).get("dream_integrated_memory_refs"))
        + _string_list((relationship_memory or {}).get("next_wake_memory_cue_refs"))
        + (
            ["runtime/state/memory/dialogue_memory_summary.json"]
            if dialogue_memory_summary
            else []
        )
        + _string_list((dialogue_memory_summary or {}).get("next_wake_memory_cue_refs"))
        + _string_list(((life_state or {}).get("memory_index") or {}).get("dream_memory_refs"))
        + _string_list(((life_state or {}).get("memory_index") or {}).get("next_wake_memory_cue_refs"))
    )[:24]


def _responsibility_hits(
    *,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    responsibility_loop_state: dict[str, Any] | None,
    autobiographical_repair_hits: list[str] | None = None,
) -> list[str]:
    return _dedupe(
        _string_list((engram_index or {}).get("responsibility_memory_refs"))
        + _string_list((relationship_memory or {}).get("responsibility_event_refs"))
        + _string_list(((life_state or {}).get("memory_index") or {}).get("responsibility_memory_refs"))
        + _string_list((responsibility_loop_state or {}).get("repair_obligation_refs"))
        + list(autobiographical_repair_hits or [])
    )[:24]


def _blocked_or_quarantined_refs(
    engram_index: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    *,
    memory_validator_report: dict[str, Any] | None = None,
) -> list[str]:
    validator_guard = (memory_validator_report or {}).get("retrieval_replay_guard")
    if not isinstance(validator_guard, dict):
        validator_guard = {}
    return _dedupe(
        _string_list((engram_index or {}).get("quarantine_refs"))
        + _string_list(((life_state or {}).get("memory_index") or {}).get("quarantine_refs"))
        + _string_list(validator_guard.get("blocked_active_retrieval_refs"))
        + (
            ["runtime/state/memory/memory_validator_report.json#retrieval_replay_guard"]
            if memory_validator_report
            else []
        )
    )


def _reconstruction_inputs(
    *,
    cue_terms: list[str],
    tiered_recall: dict[str, Any],
    relationship_hits: list[str],
    autobiographical_hits: list[str],
    schema_memory_hits: list[str],
    pattern_completion_hits: list[str],
    autobiographical_repair_hits: list[str],
    dream_residue_hits: list[str],
    responsibility_hits: list[str],
) -> dict[str, Any]:
    counts = {
        "cue_count": len(cue_terms),
        "salient_core_count": len(_string_list(tiered_recall.get("salient_core_refs"))),
        "relationship_hit_count": len(relationship_hits),
        "autobiographical_hit_count": len(autobiographical_hits),
        "schema_hit_count": len(schema_memory_hits),
        "pattern_completion_hit_count": len(pattern_completion_hits),
        "autobiographical_responsibility_repair_hit_count": len(
            autobiographical_repair_hits
        ),
        "dream_residue_hit_count": len(dream_residue_hits),
        "responsibility_hit_count": len(responsibility_hits),
    }
    if counts["autobiographical_responsibility_repair_hit_count"]:
        focus = "autobiographical_responsibility_repair_reconstruction"
    elif counts["responsibility_hit_count"]:
        focus = "responsibility_memory_reconstruction"
    elif counts["dream_residue_hit_count"]:
        focus = "dream_residue_relation_reconstruction"
    elif counts["relationship_hit_count"]:
        focus = "relationship_continuity_reconstruction"
    elif counts["autobiographical_hit_count"]:
        focus = "autobiographical_continuity_reconstruction"
    elif counts["pattern_completion_hit_count"]:
        focus = "pattern_completion_reconstructive_recall"
    elif counts["schema_hit_count"]:
        focus = "schema_continuity_reconstruction"
    else:
        focus = "minimal_context_reconstruction"
    return {
        "schema_version": "memory_reconstruction_inputs_v0",
        "reconstruction_focus": focus,
        "reconstruction_counts": counts,
        "source_priority_order": [
            "current_language_cues",
            "salient_core_memory",
            "relationship_memory",
            "autobiographical_memory",
            "schema_memory",
            "pattern_completion_with_source_boundary",
            "responsibility_memory",
            "dream_residue_with_fact_boundary",
            "deep_sediment_context",
        ],
    }


def _writeback_candidates(
    *,
    activated_refs: list[str],
    blocked_refs: list[str],
    exit_dream_governance: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    blocked = set(blocked_refs)
    candidates: list[dict[str, Any]] = []
    for ref in activated_refs[:16]:
        candidates.append(
            {
                "candidate_ref": ref,
                "writeback_route": "memory_write_gate_then_state_merge_guard",
                "candidate_status": "quarantined_source"
                if ref in blocked
                else "retrieval_reconstruction_candidate",
            }
        )
    governance = exit_dream_governance or {}
    for ref in _string_list(governance.get("next_wake_memory_cue_refs"))[:8]:
        candidates.append(
            {
                "candidate_ref": ref,
                "writeback_route": "exit_dream_memory_write_gate_then_state_merge_guard",
                "candidate_status": "next_wake_cue_reactivation_candidate",
                "memory_write_gate_ref": governance.get("memory_write_gate_ref"),
                "state_merge_guard_ref": governance.get("state_merge_guard_ref"),
                "dream_fact_boundary_ref": governance.get("dream_fact_boundary_ref"),
            }
        )
    return candidates


def _reconstructive_recall_profile(
    *,
    pattern_completion_frame: dict[str, Any] | None,
    cue_terms: list[str],
    live_memory_trace_hits: list[str],
) -> dict[str, Any]:
    frame = pattern_completion_frame or {}
    reconstructive = frame.get("reconstructive_completion") or {}
    if not isinstance(reconstructive, dict):
        reconstructive = {}
    fragments = [
        fragment
        for fragment in reconstructive.get("reconstruction_fragments", [])
        if isinstance(fragment, dict)
    ]
    if not fragments:
        for candidate in frame.get("completion_candidates", []):
            if not isinstance(candidate, dict):
                continue
            for fragment in candidate.get("reconstruction_fragments", []):
                if isinstance(fragment, dict):
                    fragments.append(fragment)
    activation_scores = [
        float(fragment.get("activation_score") or 0) for fragment in fragments
    ]
    mean_activation = (
        round(sum(activation_scores) / len(activation_scores), 3)
        if activation_scores
        else 0.0
    )
    return {
        "schema_version": "reconstructive_recall_profile_v0",
        "profile_ref": MEMORY_RETRIEVAL_FRAME_REF + "#reconstructive_recall_profile",
        "completion_mode": reconstructive.get("completion_mode")
        or ("reconstructive_fragment_assembly" if fragments else "ref_only_fallback"),
        "hippocampal_activation_count": int(
            reconstructive.get("hippocampal_activation_count") or len(fragments)
        ),
        "reconstruction_fragment_count": len(fragments),
        "mean_activation_score": mean_activation,
        "reconstruction_fragment_refs": [
            str(fragment.get("trace_ref"))
            for fragment in fragments
            if fragment.get("trace_ref")
        ][:12],
        "cue_terms": _dedupe(_string_list(cue_terms))[:12],
        "live_memory_trace_hit_count": len(live_memory_trace_hits),
        "recall_route": (
            "hippocampal_cue_activation_then_pattern_completion"
            if fragments
            else "structured_ref_fallback"
        ),
        "material_boundary": (
            "fragments_are_pre_expression_reconstruction_not_spoken_answers"
        ),
    }


def _memory_phenomenology_profile(
    *,
    external_utterance: str | None,
    live_memory_trace_hits: list[str],
    relationship_hits: list[str],
    autobiographical_hits: list[str],
    schema_memory_hits: list[str],
    pattern_completion_hits: list[str],
    activated_refs: list[str],
    blocked_refs: list[str],
    memory_trace_store: dict[str, Any] | None,
    dream_residue_hits: list[str],
    reconstructive_recall_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    recall_question = _is_memory_recall_question(external_utterance)
    strengthening_eligible = _is_memory_confirmation_utterance(external_utterance)
    blocked_set = set(blocked_refs)
    reportable_live_hits = [
        ref for ref in live_memory_trace_hits if ref and ref not in blocked_set
    ]
    relationship_hits = _phenomenology_substantive_hits(relationship_hits)
    autobiographical_hits = _phenomenology_substantive_hits(autobiographical_hits)
    schema_memory_hits = _phenomenology_substantive_hits(
        schema_memory_hits, allow_schema_nodes=True
    )
    pattern_completion_hits = _phenomenology_substantive_hits(pattern_completion_hits)
    has_live_grounding = bool(reportable_live_hits)
    has_relationship_grounding = bool(relationship_hits)
    has_autobiographical_grounding = bool(autobiographical_hits)
    has_schema_grounding = bool(schema_memory_hits)
    has_pattern_grounding = bool(pattern_completion_hits)
    grounded = (
        has_live_grounding
        or has_relationship_grounding
        or has_autobiographical_grounding
        or has_schema_grounding
        or has_pattern_grounding
    )
    cross_modal_refs = _live_trace_cross_modal_refs(
        memory_trace_store=memory_trace_store,
        live_memory_trace_hits=reportable_live_hits,
    )
    if recall_question and not grounded:
        recall_phenomenology = "uncertain"
        accessibility_level = "low"
        uncertain_boundary_active = True
        closure_hint = "uncertain"
        source_grounding = "none"
    elif has_live_grounding and len(reportable_live_hits) >= 2:
        recall_phenomenology = "vivid"
        accessibility_level = "high"
        uncertain_boundary_active = False
        closure_hint = "closed"
        source_grounding = "live_trace"
    elif grounded:
        recall_phenomenology = "partial"
        accessibility_level = "medium"
        uncertain_boundary_active = recall_question and not has_live_grounding
        closure_hint = "partial" if uncertain_boundary_active else "closed"
        if has_schema_grounding:
            source_grounding = "schema"
        elif has_relationship_grounding:
            source_grounding = "relationship"
        elif has_autobiographical_grounding:
            source_grounding = "autobiographical"
        else:
            source_grounding = "pattern_completion"
    else:
        recall_phenomenology = "absent"
        accessibility_level = "low"
        uncertain_boundary_active = False
        closure_hint = "open_no_retrievable_expression_material"
        source_grounding = "none"
    dream_residue_modulation = bool(dream_residue_hits)
    reconstructive = reconstructive_recall_profile or {}
    expression_material_grounded = bool(
        reconstructive.get("reconstruction_fragment_count")
        and reconstructive.get("completion_mode") == "reconstructive_fragment_assembly"
    )
    recall_strength_score = _recall_strength_score(
        live_memory_trace_hits=reportable_live_hits,
        memory_trace_store=memory_trace_store,
        phenomenology=recall_phenomenology,
        reconstructive_recall_profile=reconstructive,
    )
    familiarity_score = _familiarity_score(
        memory_trace_store=memory_trace_store,
        live_memory_trace_hits=reportable_live_hits,
    )
    tip_of_tongue_risk = _tip_of_tongue_risk(
        recall_phenomenology=recall_phenomenology,
        recall_strength_score=recall_strength_score,
        uncertain_boundary_active=uncertain_boundary_active,
    )
    return {
        "schema_version": "memory_phenomenology_profile_v0",
        "profile_ref": MEMORY_RETRIEVAL_FRAME_REF + "#memory_phenomenology_profile",
        "recall_phenomenology": recall_phenomenology,
        "accessibility_level": accessibility_level,
        "source_grounding": source_grounding,
        "uncertain_boundary_active": uncertain_boundary_active,
        "strengthening_eligible": strengthening_eligible,
        "dream_residue_modulation": dream_residue_modulation,
        "recall_strength_score": recall_strength_score,
        "familiarity_score": familiarity_score,
        "tip_of_tongue_risk": tip_of_tongue_risk,
        "expression_material_grounded": expression_material_grounded,
        "reconstructive_recall_profile_ref": reconstructive.get("profile_ref"),
        "cross_modal_evidence_ref_count": len(cross_modal_refs),
        "cross_modal_evidence_refs": cross_modal_refs[:8],
        "closure_hint": closure_hint,
        "phenomenology_boundary": (
            "recall_feeling_derived_from_structured_hits_not_fixed_spoken_templates"
        ),
        "activated_ref_count": len(activated_refs),
        "live_trace_hit_count": len(reportable_live_hits),
    }


def _live_trace_cross_modal_refs(
    *,
    memory_trace_store: dict[str, Any] | None,
    live_memory_trace_hits: list[str],
) -> list[str]:
    if not memory_trace_store:
        return []
    hit_ids = {
        ref.rsplit("#", 1)[-1].replace("trace:", "")
        for ref in live_memory_trace_hits
        if ref
    }
    refs: list[str] = []
    for trace in memory_trace_store.get("traces", []):
        if not isinstance(trace, dict):
            continue
        trace_id = str(trace.get("trace_id") or "")
        if trace_id not in hit_ids:
            continue
        refs.extend(_string_list(trace.get("cross_modal_evidence_refs")))
        refs.extend(_string_list(trace.get("source_evidence_refs")))
    return _dedupe(refs)


PHENOMENOLOGY_SEED_MARKERS = (
    "#schema_refs",
    "dialogue_turn_log.jsonl#line-1",
    "self_narrative_seed",
    "shared-language-v0-0001",
    "rel-v0-0001",
    "pre_activation",
)


def _phenomenology_substantive_hits(
    hits: list[str],
    *,
    allow_schema_nodes: bool = False,
) -> list[str]:
    substantive: list[str] = []
    for hit in hits:
        if not hit:
            continue
        if any(marker in hit for marker in PHENOMENOLOGY_SEED_MARKERS):
            continue
        if (
            hit.endswith("life_schema_map.json")
            or hit.endswith("life_schema_map.json#schema_refs")
        ):
            continue
        if allow_schema_nodes and "#schema:" in hit:
            substantive.append(hit)
            continue
        if "memory_trace_store" in hit or "memory-trace-" in hit:
            substantive.append(hit)
            continue
        if allow_schema_nodes and "life-schema-" in hit:
            substantive.append(hit)
            continue
        if hit.startswith("runtime/state/memory/dialogue_memory_summary.json"):
            substantive.append(hit)
            continue
    return _dedupe(substantive)


def _recall_strength_score(
    *,
    live_memory_trace_hits: list[str],
    memory_trace_store: dict[str, Any] | None,
    phenomenology: str,
    reconstructive_recall_profile: dict[str, Any] | None = None,
) -> float:
    reconstructive = reconstructive_recall_profile or {}
    if reconstructive.get("reconstruction_fragment_count"):
        mean_activation = float(reconstructive.get("mean_activation_score") or 0)
        if mean_activation > 0:
            return round(min(0.98, mean_activation / 4.0), 3)
    if phenomenology == "absent":
        return 0.05
    if phenomenology == "uncertain":
        return 0.22
    hit_ids = {
        ref.rsplit("#", 1)[-1].replace("trace:", "")
        for ref in live_memory_trace_hits
        if ref
    }
    scores: list[float] = []
    for trace in (memory_trace_store or {}).get("traces", []):
        if not isinstance(trace, dict):
            continue
        if str(trace.get("trace_id")) not in hit_ids:
            continue
        scores.append(
            float(trace.get("accessibility_score") or 0.55)
            * float(trace.get("replay_salience") or 0.5)
        )
    if scores:
        return round(min(0.98, sum(scores) / len(scores)), 3)
    return {
        "partial": 0.48,
        "vivid": 0.82,
    }.get(phenomenology, 0.3)


def _familiarity_score(
    *,
    memory_trace_store: dict[str, Any] | None,
    live_memory_trace_hits: list[str],
) -> float:
    hit_ids = {
        ref.rsplit("#", 1)[-1].replace("trace:", "")
        for ref in live_memory_trace_hits
        if ref
    }
    values: list[float] = []
    for trace in (memory_trace_store or {}).get("traces", []):
        if not isinstance(trace, dict):
            continue
        if str(trace.get("trace_id")) not in hit_ids:
            continue
        replay_count = int(trace.get("offline_replay_count") or 0)
        salience = float(trace.get("replay_salience") or 0.5)
        values.append(min(0.98, salience + replay_count * 0.04))
    if values:
        return round(sum(values) / len(values), 3)
    return 0.25


def _tip_of_tongue_risk(
    *,
    recall_phenomenology: str,
    recall_strength_score: float,
    uncertain_boundary_active: bool,
) -> str:
    if recall_phenomenology == "partial" and recall_strength_score < 0.45:
        return "elevated"
    if uncertain_boundary_active and recall_strength_score < 0.35:
        return "moderate"
    if recall_phenomenology == "vivid":
        return "low"
    return "baseline"


def is_memory_recall_question(utterance: str | None) -> bool:
    return _is_memory_recall_question(utterance)


def is_memory_confirmation_utterance(utterance: str | None) -> bool:
    return _is_memory_confirmation_utterance(utterance)


def _is_memory_recall_question(utterance: str | None) -> bool:
    text = str(utterance or "").strip().lower()
    if not text:
        return False
    markers = (
        "你还记得",
        "记得吗",
        "还记得",
        "remember",
        "do you remember",
        "recall",
        "我们上次",
        "之前说过",
    )
    return any(marker in text for marker in markers)


def _is_memory_confirmation_utterance(utterance: str | None) -> bool:
    text = str(utterance or "").strip().lower()
    if not text:
        return False
    markers = (
        "没错",
        "对的",
        "是的",
        "你记得对",
        "就是这样",
        "correct",
        "that's right",
        "yes exactly",
    )
    return any(marker in text for marker in markers)


def _recall_to_expression_profile(
    *,
    cue_activation_profile: dict[str, Any],
    reconstruction_inputs: dict[str, Any],
    activated_refs: list[str],
    relationship_hits: list[str],
    autobiographical_hits: list[str],
    schema_memory_hits: list[str],
    pattern_completion_hits: list[str],
    autobiographical_repair_hits: list[str],
    dream_residue_hits: list[str],
    responsibility_hits: list[str],
    live_memory_trace_hits: list[str] | None = None,
    blocked_refs: list[str],
    exit_dream_governance: dict[str, Any],
    phenomenology_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    influence_families = _string_list(
        cue_activation_profile.get("activated_family_order")
    )
    source_refs = _dedupe(
        activated_refs
        + relationship_hits
        + autobiographical_hits
        + schema_memory_hits
        + pattern_completion_hits
        + autobiographical_repair_hits
        + dream_residue_hits
        + responsibility_hits
        + _string_list(live_memory_trace_hits)
        + _string_list(exit_dream_governance.get("next_wake_memory_cue_refs"))
    )
    blocked_set = set(blocked_refs)
    reportable_refs = [
        ref for ref in source_refs if ref and ref not in blocked_set
    ]
    boundary_flags: list[str] = []
    if relationship_hits or "relationship" in influence_families:
        boundary_flags.append("relationship")
    if autobiographical_hits or "autobiographical" in influence_families:
        boundary_flags.append("autobiographical")
    if schema_memory_hits or "schema" in influence_families:
        boundary_flags.append("schema")
    if pattern_completion_hits:
        boundary_flags.append("pattern_completion")
    if autobiographical_repair_hits or responsibility_hits:
        boundary_flags.append("responsibility_repair")
    if dream_residue_hits or "dream_residue" in influence_families:
        boundary_flags.append("dream_residue")
    if blocked_refs:
        boundary_flags.append("quarantine")

    phenomenology = phenomenology_profile or {}
    closure_hint = phenomenology.get("closure_hint")
    if closure_hint:
        closure_status = str(closure_hint)
    elif reportable_refs or influence_families:
        closure_status = "closed"
    else:
        closure_status = "open_no_retrievable_expression_material"
    return {
        "schema_version": "memory_recall_to_expression_profile_v0",
        "profile_ref": (
            MEMORY_RETRIEVAL_FRAME_REF + "#recall_to_expression_profile"
        ),
        "closure_status": closure_status,
        "expression_boundary": (
            "memory_recall_enters_language_prestructure_not_fixed_spoken_reply"
        ),
        "reportability_policy": (
            "workspace_reportable_with_source_boundary_and_reconsolidation_writeback"
        ),
        "dominant_family": cue_activation_profile.get("dominant_family"),
        "activation_match_strength": cue_activation_profile.get(
            "activation_match_strength"
        ),
        "reconstruction_focus": reconstruction_inputs.get(
            "reconstruction_focus"
        ),
        "expression_source_ref_count": len(source_refs),
        "reportable_source_ref_count": len(reportable_refs),
        "expression_source_refs": _dedupe(
            _string_list(live_memory_trace_hits) + pattern_completion_hits + reportable_refs
        )[:12],
        "expression_influence_families": influence_families[:8],
        "schema_memory_ref_count": len(schema_memory_hits),
        "pattern_completion_ref_count": len(pattern_completion_hits),
        "source_boundary_flags": _dedupe(boundary_flags),
        "expression_guardrails": _dedupe(
            [
                "quarantined_refs_excluded_from_expression",
                "validator_excluded_refs_are_not_reportable",
                "dream_residue_requires_fact_boundary",
                "relationship_memory_requires_relation_scope_boundary",
                "responsibility_memory_requires_write_gate_and_state_merge",
                "retrieval_material_not_spoken_template",
                "provider_hits_are_not_facts",
            ]
        ),
        "memory_phenomenology_profile_ref": phenomenology.get("profile_ref"),
        "recall_phenomenology": phenomenology.get("recall_phenomenology"),
        "accessibility_level": phenomenology.get("accessibility_level"),
        "uncertain_boundary_active": phenomenology.get("uncertain_boundary_active"),
        "strengthening_eligible": phenomenology.get("strengthening_eligible"),
        "recall_strength_score": phenomenology.get("recall_strength_score"),
        "familiarity_score": phenomenology.get("familiarity_score"),
        "tip_of_tongue_risk": phenomenology.get("tip_of_tongue_risk"),
        "post_expression_reconsolidation_hooks": [
            "spoken_memory_mismatch_reenters_reconsolidation",
            "correction_updates_contradiction_links",
            "confirmed_recall_strengthens_trace_accessibility",
            "uncertain_recall_remains_hypothesis_or_silent_trace",
        ],
        "consumer_refs": [
            (
                "runtime/state/language/model_expression_state.json"
                "#model_expression_context_summary"
            ),
            (
                "runtime/reports/latest/dialogue_writeback_bundle.json"
                "#memory_retrieval_writeback_refs"
            ),
            (
                "runtime/state/consciousness/workspace_frame.json"
                "#memory_retrieval_refs"
            ),
        ],
    }


def _cue_activation_profile(
    *,
    cue_terms: list[str],
    tiered_recall: dict[str, Any],
    activated_refs: list[str],
    relationship_hits: list[str],
    autobiographical_hits: list[str],
    schema_memory_hits: list[str],
    pattern_completion_hits: list[str],
    autobiographical_repair_hits: list[str],
    dream_residue_hits: list[str],
    responsibility_hits: list[str],
    blocked_refs: list[str],
    exit_dream_governance: dict[str, Any],
) -> dict[str, Any]:
    family_inputs = [
        (
            "relationship",
            relationship_hits,
            _cue_family_matches(
                cue_terms,
                (
                    "关系",
                    "朋友",
                    "家人",
                    "同学",
                    "陌生",
                    "shared",
                    "relation",
                    "relationship",
                ),
            ),
        ),
        (
            "autobiographical",
            autobiographical_hits,
            _cue_family_matches(
                cue_terms,
                (
                    "我",
                    "自传",
                    "经历",
                    "记得",
                    "记忆",
                    "回忆",
                    "turn",
                    "narrative",
                    "autobiographical",
                ),
            ),
        ),
        (
            "responsibility_repair",
            _dedupe(autobiographical_repair_hits + responsibility_hits),
            _cue_family_matches(
                cue_terms,
                (
                    "责任",
                    "后悔",
                    "修复",
                    "道歉",
                    "承担",
                    "regret",
                    "repair",
                    "responsibility",
                ),
            ),
        ),
        (
            "dream_residue",
            dream_residue_hits,
            _cue_family_matches(
                cue_terms,
                (
                    "梦",
                    "梦境",
                    "睡眠",
                    "醒后",
                    "离线",
                    "dream",
                    "wake",
                    "sleep",
                ),
            ),
        ),
        (
            "schema",
            schema_memory_hits,
            _cue_family_matches(
                cue_terms,
                (
                    "schema",
                    "schema map",
                    "life schema",
                    "pattern",
                    "概念",
                    "流程",
                    "价值",
                    "关系模式",
                ),
            ),
        ),
        (
            "pattern_completion",
            pattern_completion_hits,
            _cue_family_matches(
                cue_terms,
                (
                    "补全",
                    "线索",
                    "片段",
                    "pattern",
                    "completion",
                    "cue",
                    "reconstruct",
                ),
            ),
        ),
        (
            "live_turn",
            [
                ref
                for ref in activated_refs
                if "dialogue_turn_log" in ref
                or "language_percept" in ref
                or "semantic_map" in ref
                or "live" in ref
            ],
            _cue_family_matches(
                cue_terms,
                (
                    "dialogue",
                    "live",
                    "turn",
                    "语义",
                    "语言",
                    "刚才",
                    "这段话",
                ),
            ),
        ),
        (
            "deep_sediment",
            _string_list(tiered_recall.get("deep_sediment_refs")),
            _cue_family_matches(
                cue_terms,
                (
                    "沉淀",
                    "底层",
                    "深层",
                    "archive",
                    "sediment",
                    "long",
                ),
            ),
        ),
    ]
    routes: list[dict[str, Any]] = []
    for family, refs, cue_matches in family_inputs:
        family_refs = _dedupe(refs)
        if not family_refs and not cue_matches:
            continue
        routes.append(
            {
                "family": family,
                "cue_match_count": len(cue_matches),
                "cue_matches": cue_matches[:8],
                "ref_count": len(family_refs),
                "top_refs": family_refs[:6],
                "route_reason": _activation_route_reason(family),
            }
        )
    routes.sort(
        key=lambda item: (item["cue_match_count"] + item["ref_count"], item["family"]),
        reverse=True,
    )
    activated_family_order = [str(item["family"]) for item in routes]
    total_signal_count = sum(
        int(item["cue_match_count"]) + int(item["ref_count"]) for item in routes
    )
    activation_ref_count = len(
        _dedupe(
            activated_refs
            + relationship_hits
            + autobiographical_hits
            + autobiographical_repair_hits
            + dream_residue_hits
            + responsibility_hits
            + _string_list(exit_dream_governance.get("next_wake_memory_cue_refs"))
        )
    )
    if total_signal_count >= 18:
        match_strength = "strong"
    elif total_signal_count >= 8:
        match_strength = "moderate"
    elif total_signal_count > 0:
        match_strength = "weak"
    else:
        match_strength = "minimal"
    return {
        "schema_version": "memory_cue_activation_profile_v0",
        "profile_ref": (
            MEMORY_RETRIEVAL_FRAME_REF + "#cue_activation_profile"
        ),
        "activation_boundary": (
            "cue_activation_profile_internal_retrieval_not_spoken_language"
        ),
        "activation_policy": (
            "cue_family_routes_before_reconstructive_recall_writeback"
        ),
        "dominant_family": activated_family_order[0]
        if activated_family_order
        else None,
        "activated_family_order": activated_family_order,
        "activation_route_count": len(routes),
        "activation_match_strength": match_strength,
        "activation_ref_count": activation_ref_count,
        "cue_term_count": len(cue_terms),
        "family_routes": routes[:8],
        "source_boundary_profile": {
            "relationship_boundary": (
                "relationship_memory_modulates_recall_not_role_hierarchy"
            ),
            "autobiographical_boundary": (
                "autobiographical_memory_reconstructs_self_continuity_not_fixed_script"
            ),
            "dream_fact_boundary": (
                "dream_residue_can_modulate_recall_not_promote_fact"
            ),
            "responsibility_boundary": (
                "responsibility_repair_memory_requires_write_gate_and_state_merge"
            ),
            "quarantine_ref_count": len(blocked_refs),
        },
    }


def _cue_family_matches(
    cue_terms: list[str],
    markers: tuple[str, ...],
) -> list[str]:
    matches: list[str] = []
    lowered_markers = [marker.lower() for marker in markers]
    for cue in cue_terms:
        cue_text = str(cue)
        cue_lower = cue_text.lower()
        if any(marker in cue_lower or marker in cue_text for marker in lowered_markers):
            matches.append(cue_text)
    return _dedupe(matches)


def _activation_route_reason(family: str) -> str:
    reasons = {
        "relationship": "relationship_cues_activate_shared_and_timeline_memory",
        "autobiographical": "self_history_cues_activate_turn_and_narrative_memory",
        "responsibility_repair": (
            "repair_and_regret_cues_activate_obligation_memory"
        ),
        "dream_residue": (
            "dream_and_next_wake_cues_activate_bounded_dream_residue"
        ),
        "schema": "schema_recall_activates_persistent_conceptual_and_relation_maps",
        "live_turn": "current_language_cues_bind_live_turn_refs",
        "deep_sediment": "low_access_context_kept_as_deep_recall_material",
    }
    return reasons.get(family, "cue_family_route")


def _exit_dream_next_wake_governance(
    *,
    engram_index: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    autobiographical_stack: dict[str, Any] | None,
    dialogue_memory_summary: dict[str, Any] | None,
    life_state: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
) -> dict[str, Any]:
    memory_index = (life_state or {}).get("memory_index")
    if not isinstance(memory_index, dict):
        memory_index = {}
    change_sources = (state_merge_guard or {}).get("long_term_change_sources")
    if not isinstance(change_sources, dict):
        change_sources = {}
    projection = (state_merge_guard or {}).get("exit_dream_state_merge_projection")
    if not isinstance(projection, dict):
        projection = {}
    next_wake_refs = _dedupe(
        _string_list((relationship_memory or {}).get("next_wake_memory_cue_refs"))
        + _string_list((engram_index or {}).get("next_wake_memory_cue_refs"))
        + _string_list((autobiographical_stack or {}).get("next_wake_memory_cue_refs"))
        + _string_list((dialogue_memory_summary or {}).get("next_wake_memory_cue_refs"))
        + _string_list(memory_index.get("next_wake_memory_cue_refs"))
        + _string_list(change_sources.get("next_wake_memory_cue_refs"))
        + _string_list(projection.get("next_wake_memory_cue_refs"))
    )
    write_gate_ref = (
        (dialogue_memory_summary or {}).get("memory_write_gate_ref")
        or (relationship_memory or {}).get("memory_write_gate_ref")
        or projection.get("memory_write_gate_ref")
    )
    state_merge_ref = (
        (dialogue_memory_summary or {}).get("state_merge_guard_ref")
        or (relationship_memory or {}).get("state_merge_guard_ref")
    )
    if not state_merge_ref and state_merge_guard:
        state_merge_ref = "runtime/state/memory/state_merge_guard.json"
    dream_fact_boundary_ref = (
        (dialogue_memory_summary or {}).get("dream_fact_boundary_ref")
        or _first_string(change_sources.get("dream_fact_boundary_refs"))
    )
    governance_refs = _dedupe(
        _string_list((relationship_memory or {}).get("exit_dream_governance_refs"))
        + _string_list((engram_index or {}).get("memory_write_gate_refs"))
        + _string_list((engram_index or {}).get("state_merge_guard_refs"))
        + _string_list((autobiographical_stack or {}).get("memory_write_gate_refs"))
        + _string_list((autobiographical_stack or {}).get("state_merge_guard_refs"))
        + _string_list(change_sources.get("exit_dream_write_gate_refs"))
        + ([str(write_gate_ref)] if write_gate_ref else [])
        + ([str(state_merge_ref)] if state_merge_ref else [])
        + ([str(dream_fact_boundary_ref)] if dream_fact_boundary_ref else [])
    )
    if not next_wake_refs and not governance_refs:
        return {}
    return {
        "schema_version": "exit_dream_next_wake_governance_v0",
        "memory_write_gate_ref": write_gate_ref,
        "state_merge_guard_ref": state_merge_ref,
        "dream_fact_boundary_ref": dream_fact_boundary_ref,
        "writeback_route": "memory_write_gate_then_state_merge_guard",
        "next_wake_memory_cue_refs": next_wake_refs[:24],
        "governance_refs": governance_refs[:24],
        "candidate_boundary": "reactivate_as_cue_material_not_fixed_language",
    }


def _extract_text_cues(text: str) -> list[str]:
    if not text:
        return []
    chinese_terms = re.findall(r"[\u4e00-\u9fff]{2,8}", text)
    latin_terms = re.findall(r"[A-Za-z][A-Za-z0-9_\-]{2,32}", text)
    special: list[str] = []
    for marker in [
        "记忆",
        "记住",
        "关系",
        "朋友",
        "家人",
        "梦",
        "梦境",
        "责任",
        "后悔",
        "痛苦",
        "语言",
        "真实",
        "生命",
        "不要机械",
        "模板",
    ]:
        if marker in text:
            special.append(marker)
    return special + chinese_terms[:16] + latin_terms[:12]


def _flatten_change_sources(change_sources: Any) -> list[str]:
    if not isinstance(change_sources, dict):
        return []
    refs: list[str] = []
    for value in change_sources.values():
        refs.extend(_string_list(value))
    return refs


def _dream_reentry_refs(
    *,
    dream_residue_hits: list[str],
    exit_dream_governance: dict[str, Any],
) -> list[str]:
    return _dedupe(
        _string_list(dream_residue_hits)
        + _string_list(exit_dream_governance.get("next_wake_memory_cue_refs"))
        + [
            "runtime/state/dream/dream_experience_window.json",
            "runtime/state/dream/wake_integration_frame.json",
            "runtime/state/dream/dream_fact_gate_decision.json",
            "runtime/state/dream/dream_belief_gate_decision.json",
        ]
    )


def _memory_hygiene_refs(memory_trace_store: dict[str, Any] | None) -> list[str]:
    refs = ["runtime/state/memory/offline_memory_hygiene_report.json"]
    last_hygiene = (memory_trace_store or {}).get("last_hygiene_report_ref")
    if last_hygiene:
        refs.append(str(last_hygiene))
    return _dedupe(refs)


def _web_dream_refs(memory_trace_store: dict[str, Any] | None) -> list[str]:
    return _dedupe(
        [
            "runtime/state/dream/web_dream_learning_state.json",
            "runtime/state/dream/web_dream_browser_session.json",
            "runtime/state/dream/web_dream_topic_history.json",
        ]
    )


def _structured_wake_question_candidates(
    *,
    memory_trace_store: dict[str, Any] | None,
    web_dream_learning_state: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    raw_candidates: list[dict[str, Any]] = []
    if web_dream_learning_state:
        raw_candidates.extend(
            item
            for item in web_dream_learning_state.get(
                "structured_wake_question_candidates", []
            )
            if isinstance(item, dict)
        )
        if not raw_candidates:
            raw_candidates.extend(
                item
                for item in web_dream_learning_state.get(
                    "wake_question_candidates", []
                )
                if isinstance(item, dict)
            )
    if memory_trace_store:
        embedded = memory_trace_store.get("structured_wake_question_candidates")
        if isinstance(embedded, list):
            raw_candidates.extend(
                item for item in embedded if isinstance(item, dict)
            )
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for candidate in raw_candidates:
        candidate_id = str(candidate.get("candidate_id") or "")
        if candidate_id:
            if candidate_id in seen_ids:
                continue
            seen_ids.add(candidate_id)
        normalized.append(
            {
                **candidate,
                "literal_text": None,
                "expression_policy": candidate.get("expression_policy")
                or "model_generated_only_no_fixed_sentence",
            }
        )
    return normalized


def _trace_accessibility_tier_refs(
    memory_trace_store: dict[str, Any] | None,
) -> dict[str, Any]:
    salient: list[str] = []
    retrievable: list[str] = []
    sediment: list[str] = []
    suppressed_count = 0
    for trace in (memory_trace_store or {}).get("traces", []):
        if not isinstance(trace, dict):
            continue
        trace_id = str(trace.get("trace_id") or "")
        if not trace_id:
            continue
        ref = f"runtime/state/memory/memory_trace_store.json#{trace_id}"
        tier = str(trace.get("accessibility_tier") or "retrievable_context")
        if tier == "salient_core":
            salient.append(ref)
        elif tier == "deep_sediment":
            sediment.append(ref)
            if trace.get("retrieval_suppression_reason"):
                suppressed_count += 1
        else:
            retrievable.append(ref)
    return {
        "salient_core_refs": _dedupe(salient),
        "retrievable_context_refs": _dedupe(retrievable),
        "deep_sediment_refs": _dedupe(sediment),
        "suppression_profile": {
            "deep_sediment_trace_count": len(sediment),
            "suppressed_trace_count": suppressed_count,
            "activation_policy": "strong_or_dream_cue_required_for_deep_sediment",
        },
    }


def _filter_traces_by_accessibility_tier(
    trace_refs: list[str],
    *,
    memory_trace_store: dict[str, Any] | None,
    cue_terms: list[str],
) -> list[str]:
    traces_by_id = {
        str(trace.get("trace_id")): trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict) and trace.get("trace_id")
    }
    cue_strength = _cue_activation_strength(cue_terms)
    dream_cue = _cue_family_matches(
        cue_terms,
        ("梦", "梦境", "睡眠", "醒后", "离线", "dream", "wake", "offline"),
    )
    eligible: list[str] = []
    for ref in trace_refs:
        trace_id = ref.rsplit("#", 1)[-1]
        trace = traces_by_id.get(trace_id)
        if not trace:
            eligible.append(ref)
            continue
        tier = str(trace.get("accessibility_tier") or "retrievable_context")
        if tier == "salient_core":
            eligible.append(ref)
            continue
        if tier == "retrievable_context":
            if (
                cue_strength >= 1
                or _trace_cue_overlap(trace, cue_terms)
                or _trace_content_overlap(trace, cue_terms)
            ):
                eligible.append(ref)
            continue
        if tier == "deep_sediment":
            if cue_strength >= 2 or dream_cue or _trace_cue_overlap(trace, cue_terms, strong=True):
                eligible.append(ref)
    return _dedupe(eligible)


def _trace_content_overlap(trace: dict[str, Any], cue_terms: list[str]) -> bool:
    haystack = " ".join(
        [
            str(trace.get("content_summary") or ""),
            str(trace.get("utterance_digest") or ""),
            str(trace.get("semantic_focus") or ""),
        ]
    ).lower()
    if not haystack:
        return False
    for cue in cue_terms:
        normalized = _normalize_cue(cue).lower()
        if normalized and normalized in haystack:
            return True
    return False


def _cue_activation_strength(cue_terms: list[str]) -> int:
    strength = 0
    for cue in cue_terms:
        normalized = _normalize_cue(cue)
        if not normalized:
            continue
        if len(normalized) >= 4:
            strength += 1
        if ":" in normalized:
            strength += 1
    return strength


def _trace_cue_overlap(
    trace: dict[str, Any],
    cue_terms: list[str],
    *,
    strong: bool = False,
) -> bool:
    bindings = _string_list(trace.get("cue_bindings")) + _string_list(
        trace.get("retrieval_cues")
    )
    haystack = " ".join(bindings + [_normalize_cue(str(trace.get("semantic_key") or ""))])
    for cue in cue_terms:
        normalized = _normalize_cue(cue)
        if not normalized:
            continue
        if strong and len(normalized) < 4:
            continue
        if normalized in haystack or any(
            token in haystack for token in normalized.split() if len(token) >= 3
        ):
            return True
    return False


def _filter_trace_refs_by_relationship_scope(
    trace_refs: list[str],
    *,
    memory_trace_store: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    blocked_refs: set[str] | list[str],
) -> list[str]:
    blocked = set(_string_list(blocked_refs))
    active_scope = str((relationship_memory or {}).get("relationship_scope") or "")
    active_subject = str(
        (relationship_memory or {}).get("active_relation_subject_id") or ""
    )
    traces_by_id = {
        str(trace.get("trace_id")): trace
        for trace in (memory_trace_store or {}).get("traces", [])
        if isinstance(trace, dict) and trace.get("trace_id")
    }
    eligible: list[str] = []
    for ref in trace_refs:
        if ref in blocked:
            continue
        trace_id = ref.rsplit("#", 1)[-1]
        trace = traces_by_id.get(trace_id)
        if not trace:
            eligible.append(ref)
            continue
        trace_scope = str(trace.get("relationship_scope") or "")
        trace_subject = str(trace.get("relation_subject_id") or "")
        if active_scope and trace_scope and trace_scope != active_scope:
            continue
        if active_subject and trace_subject and trace_subject != active_subject:
            continue
        eligible.append(ref)
    return _dedupe(eligible)


def merge_cue_candidates(
    *,
    cue_terms: list[str],
    memory_trace_store: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
    blocked_refs: list[str],
    provider_name: str = "noop",
) -> dict[str, Any]:
    scope_boundary = str(
        (relationship_memory or {}).get("relationship_scope")
        or "relation_scoped_live_episode"
    )
    provider = (
        local_full_text_cue_candidate_provider
        if provider_name == "local_full_text"
        else noop_cue_candidate_provider
    )
    provider_result = provider(
        cue_terms=cue_terms,
        memory_trace_store=memory_trace_store,
        relationship_memory=relationship_memory,
        scope_boundary=scope_boundary,
    )
    blocked = set(_string_list(blocked_refs))
    eligible_candidate_trace_refs = _filter_trace_refs_by_relationship_scope(
        _string_list(provider_result.get("candidate_trace_refs")),
        memory_trace_store=memory_trace_store,
        relationship_memory=relationship_memory,
        blocked_refs=blocked,
    )
    eligible_candidate_trace_refs = _filter_traces_by_accessibility_tier(
        eligible_candidate_trace_refs,
        memory_trace_store=memory_trace_store,
        cue_terms=cue_terms,
    )
    merged_cue_terms = _dedupe(
        _string_list(provider_result.get("candidate_cue_terms"))
    )
    cue_provider_audit = {
        "provider_name": provider_result.get("provider_name"),
        "provider_status": provider_result.get("provider_status"),
        "scope_boundary": provider_result.get("scope_boundary"),
        "validator_boundary": provider_result.get("validator_boundary"),
        "candidate_trace_ref_count": len(
            _string_list(provider_result.get("candidate_trace_refs"))
        ),
        "eligible_candidate_trace_ref_count": len(eligible_candidate_trace_refs),
        "blocked_candidate_trace_ref_count": len(
            _string_list(provider_result.get("candidate_trace_refs"))
        )
        - len(eligible_candidate_trace_refs),
        "source_boundary": provider_result.get("source_boundary"),
    }
    return {
        "merged_cue_terms": merged_cue_terms,
        "eligible_candidate_trace_refs": eligible_candidate_trace_refs,
        "cue_provider_audit": cue_provider_audit,
    }


def _normalize_cue(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).strip())[:96]


def _fingerprint(values: list[str]) -> str:
    return _sha256("\n".join(values))


def _sha256(value: str) -> str:
    return hashlib.sha256(str(value or "").encode("utf-8")).hexdigest()


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item not in (None, "")]
    if isinstance(value, str) and value:
        return [value]
    return []


def _first_string(value: Any) -> str | None:
    values = _string_list(value)
    return values[0] if values else None


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


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
