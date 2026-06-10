from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .commitment_repair import build_commitment_repair_language_index
from .commitment_expression import build_commitment_expression_plan
from .action_shadow import build_language_action_bridge_shadow
from .apology_repair_language import build_apology_repair_language_trace
from .dialogue_log import build_dialogue_turn_log_entries
from .dream_gate import build_dream_report_language_gate
from .expression_monitor import build_expression_monitor_state, build_expression_plan
from .inner_speech import build_inner_speech_frame
from .language_state import build_language_relationship_state
from .narrative_trace import build_self_narrative_language_trace
from .percept import build_language_percept_frame
from .relation_scope import build_relation_scope_language_index
from .relationship_graph import build_relationship_subject_graph
from .relationship_timeline import build_relationship_timeline
from .semantic_map import build_semantic_map_frame
from .shared_terms import build_shared_term_registry
from life_v0.growth.offline_learning_profile import (
    BELIEF_LEARNING_PLAN_REF,
    LANGUAGE_LEARNING_PLAN_REF,
    NIGHTMARE_RISK_REF,
    RELATIONSHIP_LEARNING_PLAN_REF,
)
from life_v0.neural_core.prediction_workspace import build_prediction_workspace_frame
from life_v0.state_store.commitment_truth import (
    project_commitment_truth_state,
    project_responsibility_ledger,
)
from life_v0.state_store.life_state import project_responsibility_language_continuity
from life_v0.state_store.relationship_memory import project_relationship_memory


ACTIVE_SLICE = "S07_LANGUAGE_RELATIONSHIP"
NEXT_ALLOWED_SLICES = ["S08_LIFE_TARGET_RUNTIMES"]
NEXT_REQUIRED_COMMAND = "life-v0 check-birth-readiness --strict"

S07_SOURCE_DOCS = [
    "docs/01f_language_system_literature_matrix.md",
    "docs/01j_real_relationship_literature_matrix.md",
    "docs/01u_language_runtime_core_matrix.md",
    "docs/09_language_symbolic_top_layer.md",
    "docs/85_language_system_life_expression_core.md",
    "docs/86_language_neuroscience_pragmatics_and_inner_speech.md",
    "docs/87_language_event_schema_fixture_and_validator_plan.md",
    "docs/88_language_development_emotion_and_brain_llm_alignment.md",
    "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
    "docs/90_language_event_examples_and_timeline_bundle.md",
    "docs/96_real_relationship_longitudinal_timeline.md",
    "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
    "docs/141_life_reality_language_fixture_schema_materialization_plan.md",
    "docs/144_life_reality_language_runtime_action_bridge_fixture_plan.md",
    "docs/147_life_reality_language_action_bridge_schema_materialization_plan.md",
    "docs/150_life_reality_language_action_cross_file_checker_plan.md",
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
]


@dataclass(frozen=True)
class LanguageRelationshipResult:
    exit_code: int
    report: dict[str, Any]


def run_build_language_relationship(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    neural_core_state_dir: Path,
    state_dir: Path,
    membrane_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> LanguageRelationshipResult:
    run_id = run_id or _default_run_id("build-language-relationship-")
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    neural_core_state_dir = neural_core_state_dir.resolve()
    state_dir = state_dir.resolve()
    membrane_dir = membrane_dir.resolve()
    out_dir = out_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    language_dir = out_dir / "language"
    relationship_dir = out_dir / "relationship"

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"docs_root_gate failed: {docs_dir}")
    if not doc_index_path.exists():
        blocked_reasons.append(f"doc_index_gate failed: {doc_index_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    neural_core = _load_json(neural_core_state_dir / "neural_life_core.json", blocked_reasons, "neural_core_gate")
    subject_systems = _load_json(neural_core_state_dir / "twelve_subject_systems.json", blocked_reasons, "subject_binding_gate")
    internal_bus = _load_json(neural_core_state_dir / "neural_life_internal_bus.json", blocked_reasons, "inner_language_bus_gate")
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "life_state_root_gate")
    commitment_truth_state = _load_json(
        state_dir / "relationship" / "commitment_truth_state.json",
        blocked_reasons,
        "commitment_truth_projection_gate",
    )
    responsibility_ledger = _load_json(
        state_dir / "responsibility" / "responsibility_ledger.json",
        blocked_reasons,
        "responsibility_ledger_projection_gate",
    )
    relationship_memory = _load_json(
        state_dir / "memory" / "relationship_memory.json",
        blocked_reasons,
        "relationship_memory_gate",
    )
    relationship_boundary = _load_json(membrane_dir / "relationship_subject_boundary.json", blocked_reasons, "relationship_subject_gate")
    responsibility_boundary = _load_json(membrane_dir / "responsibility_repair_boundary.json", blocked_reasons, "repair_language_gate")
    responsibility_loop = _load_json(
        state_dir / "action" / "responsibility_loop_state.json",
        blocked_reasons,
        "repair_language_gate",
    )
    dream_fact_boundary = _load_json(membrane_dir / "dream_fact_boundary.json", blocked_reasons, "dream_language_gate")
    shadow_action_gate = _load_json(membrane_dir / "shadow_action_gate.json", blocked_reasons, "shadow_action_gate")
    membrane_report = _load_json(reports_dir / "life_membrane_report.json", blocked_reasons, "s03_report_gate")
    membrane_check = _load_json(reports_dir / "life_membrane_check_report.json", blocked_reasons, "s03_check_gate")
    state_report = _load_json(reports_dir / "state_store_report.json", blocked_reasons, "s04_report_gate")
    state_check = _load_json(reports_dir / "state_store_check_report.json", blocked_reasons, "s04_check_gate")
    replay_cue_bundle = _load_json_if_exists(state_dir / "replay" / "replay_cue_bundle.json")
    offline_consolidation_frame = _load_json_if_exists(state_dir / "dream" / "offline_consolidation_frame.json")
    nightmare_risk = _load_json_if_exists(state_dir / "dream" / "nightmare_loop_risk.json")
    growth_patch_candidate_queue = _load_json_if_exists(state_dir / "growth" / "growth_patch_candidate_queue.json")
    belief_learning_plan = _load_json_if_exists(state_dir / "growth" / "belief_learning_plan.json")
    language_learning_plan = _load_json_if_exists(state_dir / "growth" / "language_learning_plan.json")
    relationship_learning_plan = _load_json_if_exists(
        state_dir / "growth" / "relationship_learning_plan.json"
    )
    body_resource_budget = _load_json_if_exists(state_dir / "body" / "body_resource_budget.json")
    core_affect_vector = _load_json_if_exists(state_dir / "body" / "core_affect_vector.json")
    signal_media_runtime = _load_json_if_exists(state_dir / "signal" / "signal_media_runtime.json")
    belief_state = _load_json_if_exists(state_dir / "prediction" / "belief_state_frame.json")
    prediction_error_field = _load_json_if_exists(state_dir / "prediction" / "prediction_error_field.json")
    active_sampling_plan = _load_json_if_exists(state_dir / "prediction" / "active_sampling_plan.json")
    memory_write_gate = _load_json_if_exists(state_dir / "memory" / "memory_write_gate.json")

    blocked_reasons.extend(_doc_blockers(doc_index))
    blocked_reasons.extend(_neural_blockers(neural_core, subject_systems, internal_bus))
    blocked_reasons.extend(_previous_slice_blockers(membrane_report, membrane_check, state_report, state_check))
    blocked_reasons.extend(_membrane_blockers(relationship_boundary, responsibility_boundary, dream_fact_boundary, shadow_action_gate))
    blocked_reasons.extend(_life_state_blockers(life_state))

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_next_slice" if status == "closed" else "block_activation"

    language_state = _build_language_relationship_state(run_id, generated_at, life_state)
    relationship_graph = _build_relationship_subject_graph(run_id, generated_at)
    repair_language = _build_commitment_repair_language_index(
        run_id,
        generated_at,
        responsibility_loop_state=responsibility_loop,
    )
    dream_language_gate = _build_dream_report_language_gate(run_id, generated_at, dream_fact_boundary)
    shadow_bridge = _build_language_action_bridge_shadow(run_id, generated_at, shadow_action_gate)
    shared_term_registry = _build_shared_term_registry(run_id, generated_at)
    relation_scope_index = _build_relation_scope_language_index(run_id, generated_at)
    self_narrative_trace = _build_self_narrative_language_trace(run_id, generated_at)
    language_percept = _build_language_percept_frame(
        run_id,
        generated_at,
        relation_scope_index=relation_scope_index,
        shared_term_registry=shared_term_registry,
        belief_state=belief_state,
        active_sampling_plan=active_sampling_plan,
    )
    semantic_map = _build_semantic_map_frame(
        run_id,
        generated_at,
        language_percept=language_percept,
        language_state=language_state,
        shared_term_registry=shared_term_registry,
        commitment_repair_index=repair_language,
        self_narrative_trace=self_narrative_trace,
        prediction_error_field=prediction_error_field,
        signal_media_runtime=signal_media_runtime,
    )
    inner_speech = _build_inner_speech_frame(
        run_id,
        generated_at,
        life_state,
        language_percept=language_percept,
        semantic_map=semantic_map,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        signal_media_runtime=signal_media_runtime,
    )
    expression_monitor = _build_expression_monitor_state(
        run_id,
        generated_at,
        cross_scope_risk_terms=list(language_percept.get("cross_scope_risk_terms", [])),
        ambiguity_queue=list(semantic_map.get("ambiguity_queue", [])),
        memory_write_gate=memory_write_gate,
        core_affect_vector=core_affect_vector,
        signal_media_runtime=signal_media_runtime,
    )
    expression_plan = _build_expression_plan(
        run_id,
        generated_at,
        inner_speech=inner_speech,
        semantic_map=semantic_map,
        language_percept=language_percept,
        commitment_repair_index=repair_language,
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
    )
    dialogue_turn_entries = _build_dialogue_turn_log_entries(run_id, generated_at)
    relationship_timeline = _build_relationship_timeline(
        run_id,
        generated_at,
        relationship_graph=relationship_graph,
        relationship_memory=relationship_memory,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        dialogue_turn_entries=dialogue_turn_entries,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    commitment_expression_plan = _build_commitment_expression_plan(
        run_id,
        generated_at,
        expression_plan=expression_plan,
        commitment_repair_index=repair_language,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        responsibility_loop_state=responsibility_loop,
        relationship_timeline=relationship_timeline,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    apology_repair_language_trace = _build_apology_repair_language_trace(
        run_id,
        generated_at,
        responsibility_loop_state=responsibility_loop,
        relationship_timeline=relationship_timeline,
        commitment_expression_plan=commitment_expression_plan,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    updated_commitment_truth = project_commitment_truth_state(
        commitment_truth_state=commitment_truth_state,
        responsibility_loop_state=responsibility_loop,
        commitment_repair_index=repair_language,
    )
    updated_responsibility_ledger = project_responsibility_ledger(
        responsibility_ledger=responsibility_ledger,
        responsibility_loop_state=responsibility_loop,
    )
    updated_relationship_memory = project_relationship_memory(
        relationship_memory=relationship_memory,
        relationship_graph=relationship_graph,
        relationship_timeline=relationship_timeline,
        commitment_truth_state=updated_commitment_truth,
        responsibility_ledger=updated_responsibility_ledger,
        commitment_repair_index=repair_language,
        last_contact_refs=[
            "runtime/state/language/dialogue_turn_log.jsonl",
            "runtime/state/language/inner_speech_frame.json",
        ],
        nightmare_risk_ref=NIGHTMARE_RISK_REF if nightmare_risk else None,
        belief_learning_plan_ref=BELIEF_LEARNING_PLAN_REF if belief_learning_plan else None,
        language_learning_plan_ref=LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else None,
        relationship_learning_plan_ref=(
            RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else None
        ),
    )

    state_refs = [
        "runtime/state/language/inner_speech_frame.json",
        "runtime/state/language/expression_monitor_state.json",
        "runtime/state/language/expression_plan.json",
        "runtime/state/language/language_relationship_state.json",
        "runtime/state/language/commitment_repair_language_index.json",
        "runtime/state/language/dream_report_language_gate.json",
        "runtime/state/language/language_action_bridge_shadow.json",
        "runtime/state/language/shared_term_registry.json",
        "runtime/state/language/dialogue_turn_log.jsonl",
        "runtime/state/language/relation_scope_language_index.json",
        "runtime/state/language/self_narrative_language_trace.json",
        "runtime/state/language/language_percept_frame.json",
        "runtime/state/language/semantic_map_frame.json",
        "runtime/state/language/commitment_expression_plan.json",
        "runtime/state/language/apology_repair_language_trace.json",
        "runtime/state/relationship/relationship_subject_graph.json",
        "runtime/state/relationship/relationship_timeline.json",
        "runtime/state/relationship/commitment_truth_state.json",
        "runtime/state/responsibility/responsibility_ledger.json",
        "runtime/state/memory/relationship_memory.json",
        "runtime/state/signal/signal_media_runtime.json",
        "runtime/state/prediction/belief_state_frame.json",
        "runtime/state/prediction/prediction_error_field.json",
        "runtime/state/prediction/active_sampling_plan.json",
        "runtime/state/memory/memory_write_gate.json",
    ]
    receipt_ref = f"runtime/receipts/language_relationship_{run_id}.json"

    updated_life_state = _integrate_life_state(
        life_state=life_state,
        inner_speech_ref="runtime/state/language/inner_speech_frame.json",
        expression_monitor_ref="runtime/state/language/expression_monitor_state.json",
        shared_language_ref="runtime/state/language/language_relationship_state.json#shared_language_refs",
        promise_ref="runtime/state/language/commitment_repair_language_index.json#commitment_refs",
        repair_language_ref="runtime/state/language/commitment_repair_language_index.json#repair_language_refs",
        dream_report_language_ref="runtime/state/language/dream_report_language_gate.json",
        shared_term_registry_ref="runtime/state/language/shared_term_registry.json",
        relation_scope_ref="runtime/state/language/relation_scope_language_index.json",
        self_narrative_trace_ref="runtime/state/language/self_narrative_language_trace.json",
        dialogue_turn_log_ref="runtime/state/language/dialogue_turn_log.jsonl",
        language_percept_ref="runtime/state/language/language_percept_frame.json",
        semantic_map_ref="runtime/state/language/semantic_map_frame.json",
        relationship_subjects=relationship_graph["subjects"],
    )
    updated_life_state = project_responsibility_language_continuity(
        life_state=updated_life_state,
        commitment_truth_state=updated_commitment_truth,
        responsibility_ledger=updated_responsibility_ledger,
        relationship_memory=updated_relationship_memory,
        relationship_graph=relationship_graph,
        relationship_timeline=relationship_timeline,
        commitment_expression_plan=commitment_expression_plan,
        apology_repair_language_trace=apology_repair_language_trace,
        responsibility_loop_state=responsibility_loop,
        commitment_repair_index=repair_language,
        nightmare_risk_ref=NIGHTMARE_RISK_REF if nightmare_risk else None,
        belief_learning_plan_ref=BELIEF_LEARNING_PLAN_REF if belief_learning_plan else None,
        language_learning_plan_ref=LANGUAGE_LEARNING_PLAN_REF if language_learning_plan else None,
        relationship_learning_plan_ref=(
            RELATIONSHIP_LEARNING_PLAN_REF if relationship_learning_plan else None
        ),
        additional_runtime_trace_refs=[
            "runtime/state/relationship/commitment_truth_state.json",
            "runtime/state/responsibility/responsibility_ledger.json",
            "runtime/state/memory/relationship_memory.json",
            "runtime/state/relationship/relationship_timeline.json",
            "runtime/state/language/commitment_expression_plan.json",
            "runtime/state/language/apology_repair_language_trace.json",
        ],
    )
    prediction_workspace = build_prediction_workspace_frame(
        run_id=run_id,
        generated_at=generated_at,
        language_continuity=_build_prediction_language_continuity(
            life_state=updated_life_state,
            semantic_map=semantic_map,
        ),
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        signal_media_runtime=signal_media_runtime,
    )
    runtime_trace_refs = updated_life_state.setdefault("runtime_trace_refs", [])
    if "runtime/state/prediction/prediction_workspace_frame.json" not in runtime_trace_refs:
        runtime_trace_refs.append("runtime/state/prediction/prediction_workspace_frame.json")

    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        state_refs=state_refs,
        blocked_reasons=blocked_reasons,
        receipt_ref=receipt_ref,
        semantic_focus=semantic_map.get("semantic_focus"),
        cross_scope_language_risks=list(language_percept.get("cross_scope_risk_terms", [])),
        body_signal_refs=list(expression_plan.get("body_signal_refs", [])),
        prediction_language_consumption_refs=_prediction_language_consumption_refs(
            signal_media_runtime=signal_media_runtime,
            belief_state=belief_state,
            prediction_error_field=prediction_error_field,
            active_sampling_plan=active_sampling_plan,
            memory_write_gate=memory_write_gate,
        ),
    )
    digest = _build_digest(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
    )
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        neural_core_state_dir=neural_core_state_dir,
        state_dir=state_dir,
        membrane_dir=membrane_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
        language_percept_ref="runtime/state/language/language_percept_frame.json",
        semantic_map_ref="runtime/state/language/semantic_map_frame.json",
    )

    try:
        language_dir.mkdir(parents=True, exist_ok=True)
        relationship_dir.mkdir(parents=True, exist_ok=True)
        prediction_dir = out_dir / "prediction"
        prediction_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(language_dir / "inner_speech_frame.json", inner_speech)
        _write_json(language_dir / "expression_monitor_state.json", expression_monitor)
        _write_json(language_dir / "expression_plan.json", expression_plan)
        _write_json(language_dir / "language_relationship_state.json", language_state)
        _write_json(relationship_dir / "relationship_subject_graph.json", relationship_graph)
        _write_json(language_dir / "commitment_repair_language_index.json", repair_language)
        _write_json(language_dir / "dream_report_language_gate.json", dream_language_gate)
        _write_json(language_dir / "language_action_bridge_shadow.json", shadow_bridge)
        _write_json(language_dir / "shared_term_registry.json", shared_term_registry)
        _write_json(language_dir / "relation_scope_language_index.json", relation_scope_index)
        _write_json(language_dir / "self_narrative_language_trace.json", self_narrative_trace)
        _write_json(language_dir / "language_percept_frame.json", language_percept)
        _write_json(language_dir / "semantic_map_frame.json", semantic_map)
        _write_json(language_dir / "commitment_expression_plan.json", commitment_expression_plan)
        _write_json(language_dir / "apology_repair_language_trace.json", apology_repair_language_trace)
        _append_jsonl(language_dir / "dialogue_turn_log.jsonl", dialogue_turn_entries)
        _write_json(relationship_dir / "relationship_timeline.json", relationship_timeline)
        _write_json(prediction_dir / "prediction_workspace_frame.json", prediction_workspace)
        _write_json(state_dir / "relationship" / "commitment_truth_state.json", updated_commitment_truth)
        _write_json(state_dir / "responsibility" / "responsibility_ledger.json", updated_responsibility_ledger)
        _write_json(state_dir / "memory" / "relationship_memory.json", updated_relationship_memory)
        _write_json(state_dir / "life_state.json", updated_life_state)
        _write_json(reports_dir / "language_relationship_report.json", report)
        _write_json(reports_dir / "language_relationship_digest.json", digest)
        _write_json(receipts_dir / f"language_relationship_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return LanguageRelationshipResult(exit_code=4, report=report)

    if status == "closed":
        return LanguageRelationshipResult(exit_code=0, report=report)
    return LanguageRelationshipResult(exit_code=1 if strict else 0, report=report)


def run_check_language_relationship(
    *,
    state_dir: Path,
    membrane_dir: Path,
    reports_dir: Path,
    strict: bool = False,
) -> LanguageRelationshipResult:
    state_dir = state_dir.resolve()
    membrane_dir = membrane_dir.resolve()
    reports_dir = reports_dir.resolve()
    generated_at = _now_iso()
    blocked_reasons: list[str] = []

    inner_speech = _load_json(state_dir / "language" / "inner_speech_frame.json", blocked_reasons, "inner_speech_gate")
    expression_monitor = _load_json(state_dir / "language" / "expression_monitor_state.json", blocked_reasons, "expression_monitor_gate")
    language_state = _load_json(state_dir / "language" / "language_relationship_state.json", blocked_reasons, "language_state_gate")
    language_percept = _load_json(state_dir / "language" / "language_percept_frame.json", blocked_reasons, "language_percept_gate")
    semantic_map = _load_json(state_dir / "language" / "semantic_map_frame.json", blocked_reasons, "semantic_map_gate")
    relationship_graph = _load_json(state_dir / "relationship" / "relationship_subject_graph.json", blocked_reasons, "relationship_subject_gate")
    relationship_timeline = _load_json(
        state_dir / "relationship" / "relationship_timeline.json",
        blocked_reasons,
        "relationship_timeline_gate",
    )
    commitment_truth_state = _load_json(
        state_dir / "relationship" / "commitment_truth_state.json",
        blocked_reasons,
        "commitment_truth_projection_gate",
    )
    responsibility_ledger = _load_json(
        state_dir / "responsibility" / "responsibility_ledger.json",
        blocked_reasons,
        "responsibility_ledger_projection_gate",
    )
    relationship_memory = _load_json(
        state_dir / "memory" / "relationship_memory.json",
        blocked_reasons,
        "relationship_memory_gate",
    )
    repair_language = _load_json(state_dir / "language" / "commitment_repair_language_index.json", blocked_reasons, "repair_language_gate")
    commitment_expression_plan = _load_json(
        state_dir / "language" / "commitment_expression_plan.json",
        blocked_reasons,
        "commitment_expression_gate",
    )
    apology_repair_language_trace = _load_json(
        state_dir / "language" / "apology_repair_language_trace.json",
        blocked_reasons,
        "apology_repair_language_gate",
    )
    dream_language_gate = _load_json(state_dir / "language" / "dream_report_language_gate.json", blocked_reasons, "dream_language_gate")
    shadow_bridge = _load_json(state_dir / "language" / "language_action_bridge_shadow.json", blocked_reasons, "shadow_action_gate")
    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "life_state_root_gate")
    prediction_workspace = _load_json(
        state_dir / "prediction" / "prediction_workspace_frame.json",
        blocked_reasons,
        "semantic_prediction_handoff_gate",
    )
    relationship_boundary = _load_json(membrane_dir / "relationship_subject_boundary.json", blocked_reasons, "relationship_subject_boundary_gate")
    build_report = _load_json(reports_dir / "language_relationship_report.json", blocked_reasons, "build_report_gate")

    blocked_reasons.extend(_check_inner_speech(inner_speech))
    blocked_reasons.extend(_check_expression_monitor(expression_monitor))
    blocked_reasons.extend(_check_language_state(language_state))
    blocked_reasons.extend(_check_language_percept(language_percept))
    blocked_reasons.extend(_check_semantic_map(semantic_map))
    blocked_reasons.extend(_check_relationship_graph(relationship_graph, relationship_boundary))
    blocked_reasons.extend(_check_relationship_timeline(relationship_timeline))
    blocked_reasons.extend(_check_commitment_truth_projection(commitment_truth_state, repair_language))
    blocked_reasons.extend(_check_responsibility_ledger_projection(responsibility_ledger))
    blocked_reasons.extend(_check_relationship_memory_projection(relationship_memory))
    blocked_reasons.extend(_check_repair_language(repair_language))
    blocked_reasons.extend(_check_commitment_expression_plan(commitment_expression_plan))
    blocked_reasons.extend(_check_apology_repair_language_trace(apology_repair_language_trace))
    blocked_reasons.extend(_check_dream_report_gate(dream_language_gate))
    blocked_reasons.extend(_check_shadow_bridge(shadow_bridge))
    blocked_reasons.extend(_check_life_state_integration(life_state))
    blocked_reasons.extend(_check_prediction_handoff(prediction_workspace, semantic_map))
    blocked_reasons.extend(_check_build_report(build_report))

    status = "closed" if not blocked_reasons else "blocked"
    report = {
        "schema_version": "language_relationship_check_report_v0",
        "generated_at": generated_at,
        "status": status,
        "stage_effect": "allow_next_slice" if status == "closed" else "block_activation",
        "checked_state_dir": str(state_dir),
        "active_engineering_slice": ACTIVE_SLICE,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
    }

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "language_relationship_check_report.json", report)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"check_report_write_gate failed: {exc}")
        return LanguageRelationshipResult(exit_code=4, report=report)

    if status == "closed":
        return LanguageRelationshipResult(exit_code=0, report=report)
    return LanguageRelationshipResult(exit_code=1 if strict else 0, report=report)


def _doc_blockers(doc_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    documents = {doc.get("path"): doc for doc in doc_index.get("documents", []) if isinstance(doc, dict)}
    required = [
        "docs/01f_language_system_literature_matrix.md",
        "docs/01j_real_relationship_literature_matrix.md",
        "docs/01u_language_runtime_core_matrix.md",
        "docs/09_language_symbolic_top_layer.md",
        "docs/85_language_system_life_expression_core.md",
        "docs/96_real_relationship_longitudinal_timeline.md",
        "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
    ]
    for doc_path in required:
        doc = documents.get(doc_path)
        if not doc:
            reasons.append(f"language_source_gate missing {doc_path}")
            continue
        if "LanguageRelationshipRuntime" not in doc.get("runtime_carriers", []):
            reasons.append(f"language_source_gate missing LanguageRelationshipRuntime carrier for {doc_path}")
    return reasons


def _neural_blockers(
    neural_core: dict[str, Any],
    subject_systems: dict[str, Any],
    internal_bus: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if neural_core.get("active_engineering_slice") != "S02_NEURAL_LIFE_CORE":
        reasons.append("inner_speech_gate neural core active slice mismatch")
    systems = subject_systems.get("systems", [])
    language_runtime = next((system for system in systems if system.get("system_id") == "LanguageRelationshipRuntime"), None)
    if not language_runtime:
        reasons.append("inner_speech_gate LanguageRelationshipRuntime missing from subject systems")
    buses = internal_bus.get("bus_channels") or internal_bus.get("edges") or []
    bus_names = {
        bus.get("bus_id")
        or bus.get("channel_id")
        or bus.get("channel_name")
        or bus.get("edge_id")
        for bus in buses
        if isinstance(bus, dict)
    }
    if "inner_language_bus" not in bus_names:
        reasons.append("inner_speech_gate inner_language_bus missing")
    return reasons


def _previous_slice_blockers(
    membrane_report: dict[str, Any],
    membrane_check: dict[str, Any],
    state_report: dict[str, Any],
    state_check: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if membrane_report.get("status") != "closed":
        reasons.append("s03_permission_gate membrane report is not closed")
    if membrane_check.get("status") != "closed":
        reasons.append("s03_permission_gate membrane check is not closed")
    if state_report.get("status") != "closed":
        reasons.append("s04_permission_gate state store report is not closed")
    if state_check.get("status") != "closed":
        reasons.append("s04_permission_gate state store check is not closed")
    return reasons


def _membrane_blockers(
    relationship_boundary: dict[str, Any],
    responsibility_boundary: dict[str, Any],
    dream_fact_boundary: dict[str, Any],
    shadow_action_gate: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if relationship_boundary.get("relation_role") != "relationship_subject":
        reasons.append("relationship_subject_gate relation role mismatch")
    if "friend" not in relationship_boundary.get("relation_kinds", []):
        reasons.append("relationship_subject_gate friend relation missing")
    if not responsibility_boundary.get("required_links"):
        reasons.append("repair_language_gate responsibility links missing")
    if dream_fact_boundary.get("schema_version") != "dream_fact_boundary_v0":
        reasons.append("dream_language_gate dream fact gate schema mismatch")
    if shadow_action_gate.get("schema_version") != "shadow_action_gate_v0":
        reasons.append("shadow_action_gate schema mismatch")
    return reasons


def _life_state_blockers(life_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if life_state.get("schema_version") != "life_state_v0":
        reasons.append("inner_speech_gate life state schema mismatch")
    if "language_state" not in life_state:
        reasons.append("inner_speech_gate language state missing")
    if "relationship_subjects" not in life_state:
        reasons.append("relationship_subject_gate relationship subjects missing")
    return reasons


def _build_inner_speech_frame(
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    *,
    language_percept: dict[str, Any] | None = None,
    semantic_map: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_inner_speech_frame(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        source_doc_refs=S07_SOURCE_DOCS,
        language_percept=language_percept,
        semantic_map=semantic_map,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        signal_media_runtime=signal_media_runtime,
    )


def _build_expression_monitor_state(
    run_id: str,
    generated_at: str,
    cross_scope_risk_terms: list[str] | None = None,
    ambiguity_queue: list[str] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_expression_monitor_state(
        run_id=run_id,
        generated_at=generated_at,
        source_doc_refs=S07_SOURCE_DOCS,
        cross_scope_risk_terms=cross_scope_risk_terms,
        ambiguity_queue=ambiguity_queue,
        memory_write_gate=memory_write_gate,
        core_affect_vector=core_affect_vector,
        signal_media_runtime=signal_media_runtime,
    )


def _build_expression_plan(
    run_id: str,
    generated_at: str,
    *,
    inner_speech: dict[str, Any],
    semantic_map: dict[str, Any],
    language_percept: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_expression_plan(
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
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_relationship_subject_graph(run_id: str, generated_at: str) -> dict[str, Any]:
    return build_relationship_subject_graph(
        run_id=run_id,
        generated_at=generated_at,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_relationship_timeline(
    run_id: str,
    generated_at: str,
    *,
    relationship_graph: dict[str, Any],
    relationship_memory: dict[str, Any],
    commitment_truth_state: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    dialogue_turn_entries: list[dict[str, Any]],
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_relationship_timeline(
        run_id=run_id,
        generated_at=generated_at,
        relationship_graph=relationship_graph,
        relationship_memory=relationship_memory,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        dialogue_turn_entries=dialogue_turn_entries,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_commitment_expression_plan(
    run_id: str,
    generated_at: str,
    *,
    expression_plan: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    commitment_truth_state: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    responsibility_loop_state: dict[str, Any],
    relationship_timeline: dict[str, Any],
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_commitment_expression_plan(
        run_id=run_id,
        generated_at=generated_at,
        expression_plan=expression_plan,
        commitment_repair_index=commitment_repair_index,
        commitment_truth_state=commitment_truth_state,
        responsibility_ledger=responsibility_ledger,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=relationship_timeline,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_apology_repair_language_trace(
    run_id: str,
    generated_at: str,
    *,
    responsibility_loop_state: dict[str, Any],
    relationship_timeline: dict[str, Any],
    commitment_expression_plan: dict[str, Any],
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_apology_repair_language_trace(
        run_id=run_id,
        generated_at=generated_at,
        responsibility_loop_state=responsibility_loop_state,
        relationship_timeline=relationship_timeline,
        commitment_expression_plan=commitment_expression_plan,
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_language_relationship_state(run_id: str, generated_at: str, life_state: dict[str, Any]) -> dict[str, Any]:
    return build_language_relationship_state(
        run_id=run_id,
        generated_at=generated_at,
        life_state=life_state,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_commitment_repair_language_index(
    run_id: str,
    generated_at: str,
    *,
    responsibility_loop_state: dict[str, Any],
) -> dict[str, Any]:
    return build_commitment_repair_language_index(
        run_id=run_id,
        generated_at=generated_at,
        responsibility_loop_state=responsibility_loop_state,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_dream_report_language_gate(run_id: str, generated_at: str, dream_fact_boundary: dict[str, Any]) -> dict[str, Any]:
    return build_dream_report_language_gate(
        run_id=run_id,
        generated_at=generated_at,
        dream_fact_boundary=dream_fact_boundary,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_language_action_bridge_shadow(run_id: str, generated_at: str, shadow_action_gate: dict[str, Any]) -> dict[str, Any]:
    return build_language_action_bridge_shadow(
        run_id=run_id,
        generated_at=generated_at,
        shadow_action_gate=shadow_action_gate,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_shared_term_registry(run_id: str, generated_at: str) -> dict[str, Any]:
    return build_shared_term_registry(
        run_id=run_id,
        generated_at=generated_at,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_relation_scope_language_index(run_id: str, generated_at: str) -> dict[str, Any]:
    return build_relation_scope_language_index(
        run_id=run_id,
        generated_at=generated_at,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_self_narrative_language_trace(run_id: str, generated_at: str) -> dict[str, Any]:
    return build_self_narrative_language_trace(
        run_id=run_id,
        generated_at=generated_at,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _build_language_percept_frame(
    run_id: str,
    generated_at: str,
    *,
    relation_scope_index: dict[str, Any],
    shared_term_registry: dict[str, Any],
    belief_state: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_language_percept_frame(
        run_id=run_id,
        generated_at=generated_at,
        incoming_turn={
            "incoming_surface": "我们之前说好的共同语言和修复，还记得吗？",
            "speaker_role": "friend",
        },
        relation_scope_index=relation_scope_index,
        shared_term_registry=shared_term_registry,
        source_doc_refs=S07_SOURCE_DOCS,
        belief_state=belief_state,
        active_sampling_plan=active_sampling_plan,
    )


def _build_semantic_map_frame(
    run_id: str,
    generated_at: str,
    *,
    language_percept: dict[str, Any],
    language_state: dict[str, Any],
    shared_term_registry: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    prediction_error_field: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_semantic_map_frame(
        run_id=run_id,
        generated_at=generated_at,
        language_percept=language_percept,
        language_state=language_state,
        shared_term_registry=shared_term_registry,
        commitment_repair_index=commitment_repair_index,
        self_narrative_trace=self_narrative_trace,
        source_doc_refs=S07_SOURCE_DOCS,
        prediction_error_field=prediction_error_field,
        signal_media_runtime=signal_media_runtime,
    )


def _build_dialogue_turn_log_entries(run_id: str, generated_at: str) -> list[dict[str, Any]]:
    return build_dialogue_turn_log_entries(
        run_id=run_id,
        generated_at=generated_at,
        source_doc_refs=S07_SOURCE_DOCS,
    )


def _integrate_life_state(
    *,
    life_state: dict[str, Any],
    inner_speech_ref: str,
    expression_monitor_ref: str,
    shared_language_ref: str,
    promise_ref: str,
    repair_language_ref: str,
    dream_report_language_ref: str,
    shared_term_registry_ref: str,
    relation_scope_ref: str,
    self_narrative_trace_ref: str,
    dialogue_turn_log_ref: str,
    language_percept_ref: str,
    semantic_map_ref: str,
    relationship_subjects: list[dict[str, Any]],
) -> dict[str, Any]:
    updated = json.loads(json.dumps(life_state))
    language_state = updated.setdefault("language_state", {})
    language_state["inner_speech_refs"] = [inner_speech_ref]
    language_state["expression_monitor_refs"] = [expression_monitor_ref]
    language_state["shared_language_refs"] = [shared_language_ref]
    language_state["promise_refs"] = [promise_ref]
    language_state["repair_language_refs"] = [repair_language_ref]
    language_state["dream_report_language_refs"] = [dream_report_language_ref]
    language_state["shared_term_registry_refs"] = [shared_term_registry_ref]
    language_state["relation_scope_refs"] = [relation_scope_ref]
    language_state["self_narrative_trace_refs"] = [self_narrative_trace_ref]
    language_state["dialogue_turn_log_refs"] = [dialogue_turn_log_ref]
    language_state["language_percept_refs"] = [language_percept_ref]
    language_state["semantic_map_refs"] = [semantic_map_ref]
    updated["relationship_subjects"] = relationship_subjects
    updated.setdefault("memory_index", {}).setdefault("relationship_memory_refs", [])
    if "runtime/state/language/language_relationship_state.json#shared-language-v0-0001" not in updated["memory_index"]["relationship_memory_refs"]:
        updated["memory_index"]["relationship_memory_refs"].append("runtime/state/language/language_relationship_state.json#shared-language-v0-0001")
    updated.setdefault("runtime_trace_refs", [])
    for ref in [
        "runtime/state/language/inner_speech_frame.json",
        "runtime/state/relationship/relationship_subject_graph.json",
        "runtime/state/language/shared_term_registry.json",
        "runtime/state/language/dialogue_turn_log.jsonl",
        "runtime/state/language/relation_scope_language_index.json",
        "runtime/state/language/self_narrative_language_trace.json",
        "runtime/state/language/language_percept_frame.json",
        "runtime/state/language/semantic_map_frame.json",
        "runtime/state/relationship/relationship_timeline.json",
        "runtime/state/language/commitment_expression_plan.json",
        "runtime/state/language/apology_repair_language_trace.json",
    ]:
        if ref not in updated["runtime_trace_refs"]:
            updated["runtime_trace_refs"].append(ref)
    updated.setdefault("archive_refs", [])
    return updated


def _build_prediction_language_continuity(
    *,
    life_state: dict[str, Any],
    semantic_map: dict[str, Any],
) -> dict[str, Any]:
    language_state = life_state.get("language_state", {})
    prediction_hooks = semantic_map.get("prediction_hooks", {})
    return {
        "shared_language_refs": list(language_state.get("shared_language_refs", [])),
        "expression_monitor_refs": list(language_state.get("expression_monitor_refs", [])),
        "relation_scope_refs": list(language_state.get("relation_scope_refs", [])),
        "commitment_refs": list(language_state.get("promise_refs", [])),
        "self_narrative_trace_refs": list(language_state.get("self_narrative_trace_refs", [])),
        "dialogue_turn_log_refs": list(language_state.get("dialogue_turn_log_refs", [])),
        "language_percept_refs": list(language_state.get("language_percept_refs", [])),
        "semantic_map_refs": list(language_state.get("semantic_map_refs", [])),
        "semantic_ambiguity_refs": list(prediction_hooks.get("semantic_ambiguity_refs", [])),
        "prediction_error_refs": list(prediction_hooks.get("prediction_error_refs", [])),
        "signal_media_refs": list(prediction_hooks.get("signal_media_refs", [])),
        "semantic_prediction_focus": prediction_hooks.get("semantic_prediction_focus") or semantic_map.get("semantic_focus"),
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    state_refs: list[str],
    blocked_reasons: list[str],
    receipt_ref: str,
    semantic_focus: str | None,
    cross_scope_language_risks: list[str],
    body_signal_refs: list[str],
    prediction_language_consumption_refs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "s07_language_relationship_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "source_doc_refs": S07_SOURCE_DOCS,
        "readme_block_refs": ["B21_LANGUAGE_RELATIONSHIP_CORE"],
        "runtime_carrier_refs": ["LanguageRelationshipRuntime"],
        "relationship_subject_refs": ["runtime/state/relationship/relationship_subject_graph.json"],
        "language_event_refs": [
            "runtime/state/language/inner_speech_frame.json",
            "runtime/state/language/expression_monitor_state.json",
        ],
        "language_percept_refs": ["runtime/state/language/language_percept_frame.json"],
        "semantic_map_refs": ["runtime/state/language/semantic_map_frame.json"],
        "body_signal_refs": body_signal_refs,
        "prediction_language_consumption_refs": prediction_language_consumption_refs,
        "semantic_focuses": [semantic_focus] if semantic_focus else [],
        "cross_scope_language_risks": cross_scope_language_risks,
        "prediction_language_handoff_refs": [
            "runtime/state/prediction/prediction_workspace_frame.json#workspace_contents.language_continuity_focus",
            "runtime/state/prediction/prediction_workspace_frame.json#workspace_contents.candidate_explanations",
        ],
        "state_refs": state_refs + ["runtime/state/prediction/prediction_workspace_frame.json"],
        "archive_receipt_ref": receipt_ref,
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _prediction_language_consumption_refs(
    *,
    signal_media_runtime: dict[str, Any],
    belief_state: dict[str, Any],
    prediction_error_field: dict[str, Any],
    active_sampling_plan: dict[str, Any],
    memory_write_gate: dict[str, Any],
) -> list[str]:
    refs: list[str] = []
    if signal_media_runtime:
        refs.append("runtime/state/signal/signal_media_runtime.json")
    if belief_state:
        refs.append("runtime/state/prediction/belief_state_frame.json")
    if prediction_error_field:
        refs.append("runtime/state/prediction/prediction_error_field.json")
    if active_sampling_plan:
        refs.append("runtime/state/prediction/active_sampling_plan.json")
    if memory_write_gate:
        refs.append("runtime/state/memory/memory_write_gate.json")
    return refs


def _build_digest(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "language_relationship_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_slice": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    neural_core_state_dir: Path,
    state_dir: Path,
    membrane_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
    language_percept_ref: str,
    semantic_map_ref: str,
) -> dict[str, Any]:
    input_hashes = {
        ref: _sha256(docs_dir.parent / ref)
        for ref in S07_SOURCE_DOCS
        if (docs_dir.parent / ref).exists()
    }
    input_hashes[str(doc_index_path)] = _sha256(doc_index_path)
    for path in [
        neural_core_state_dir / "neural_life_core.json",
        neural_core_state_dir / "twelve_subject_systems.json",
        neural_core_state_dir / "neural_life_internal_bus.json",
        state_dir / "life_state.json",
        state_dir / "action" / "responsibility_loop_state.json",
        membrane_dir / "relationship_subject_boundary.json",
        membrane_dir / "responsibility_repair_boundary.json",
        membrane_dir / "dream_fact_boundary.json",
        membrane_dir / "shadow_action_gate.json",
        state_dir / "body" / "body_resource_budget.json",
        state_dir / "body" / "core_affect_vector.json",
        state_dir / "signal" / "signal_media_runtime.json",
        state_dir / "prediction" / "belief_state_frame.json",
        state_dir / "prediction" / "prediction_error_field.json",
        state_dir / "prediction" / "active_sampling_plan.json",
        state_dir / "memory" / "memory_write_gate.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)

    output_refs = [
        state_dir / "language" / "inner_speech_frame.json",
        state_dir / "language" / "expression_monitor_state.json",
        state_dir / "language" / "expression_plan.json",
        state_dir / "language" / "language_relationship_state.json",
        state_dir / "language" / "commitment_repair_language_index.json",
        state_dir / "language" / "commitment_expression_plan.json",
        state_dir / "language" / "apology_repair_language_trace.json",
        state_dir / "language" / "dream_report_language_gate.json",
        state_dir / "language" / "language_action_bridge_shadow.json",
        state_dir / "language" / "language_percept_frame.json",
        state_dir / "language" / "semantic_map_frame.json",
        state_dir / "relationship" / "relationship_subject_graph.json",
        state_dir / "relationship" / "relationship_timeline.json",
        state_dir / "prediction" / "prediction_workspace_frame.json",
        reports_dir / "language_relationship_report.json",
        reports_dir / "language_relationship_digest.json",
        receipts_dir / f"language_relationship_{run_id}.json",
    ]
    return {
        "schema_version": "language_relationship_receipt_v0",
        "receipt_id": f"language_relationship_{run_id}",
        "run_id": run_id,
        "command": "build-language-relationship",
        "input_hashes": input_hashes,
        "output_refs": [str(path) for path in output_refs],
        "language_percept_ref": language_percept_ref,
        "semantic_map_ref": semantic_map_ref,
        "downstream_handoff_refs": [
            "runtime/state/prediction/prediction_workspace_frame.json#workspace_contents.language_continuity_focus",
        ],
        "stage_effect": stage_effect,
        "created_at": generated_at,
    }


def _check_inner_speech(inner_speech: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if inner_speech.get("schema_version") != "inner_speech_frame_v0":
        reasons.append("inner_speech_gate schema mismatch")
    if inner_speech.get("status") != "closed":
        reasons.append("inner_speech_gate status mismatch")
    if "inner_language_bus" not in inner_speech.get("bus_channel_refs", []):
        reasons.append("inner_speech_gate inner_language_bus missing")
    for field in [
        "belief_state_ref",
        "prediction_error_ref",
        "active_sampling_plan_ref",
        "signal_media_ref",
    ]:
        if not inner_speech.get(field):
            reasons.append(f"inner_speech_gate missing {field}")
    drive_sources = inner_speech.get("internal_drive_sources", {})
    for drive in ["confirm", "hold", "repair", "ask"]:
        if drive not in drive_sources:
            reasons.append(f"inner_speech_gate missing {drive} drive source")
    if inner_speech.get("drive_resolution_order") != ["hold", "repair", "ask", "confirm"]:
        reasons.append("inner_speech_gate drive resolution order mismatch")
    return reasons


def _check_expression_monitor(expression_monitor: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if expression_monitor.get("schema_version") != "expression_monitor_state_v0":
        reasons.append("expression_monitor_gate schema mismatch")
    for dimension in ["relationship_consequence", "commitment_trace", "dream_fact", "action_consequence"]:
        if dimension not in expression_monitor.get("monitor_dimensions", []):
            reasons.append(f"expression_monitor_gate missing {dimension}")
    for field in ["memory_write_gate_ref", "signal_media_ref"]:
        if not expression_monitor.get(field):
            reasons.append(f"expression_monitor_gate missing {field}")
    if "core_affect_vector_ref" not in expression_monitor:
        reasons.append("expression_monitor_gate core affect vector ref field missing")
    if not expression_monitor.get("write_gate_pressure"):
        reasons.append("expression_monitor_gate write gate pressure missing")
    if not expression_monitor.get("affect_expression_modulation"):
        reasons.append("expression_monitor_gate affect modulation missing")
    return reasons


def _check_language_state(language_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if language_state.get("schema_version") != "language_relationship_state_v0":
        reasons.append("language_state_gate schema mismatch")
    if not language_state.get("shared_language_refs"):
        reasons.append("language_state_gate shared language refs missing")
    if not language_state.get("repair_language_refs"):
        reasons.append("language_state_gate repair language refs missing")
    return reasons


def _check_language_percept(language_percept: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if language_percept.get("schema_version") != "language_percept_frame_v0":
        reasons.append("language_percept_gate schema mismatch")
    if not language_percept.get("relation_scope_ref"):
        reasons.append("language_percept_gate relation scope ref missing")
    if not (
        language_percept.get("shared_term_hits")
        or language_percept.get("cross_scope_risk_terms")
        or language_percept.get("ambiguity_flags")
    ):
        reasons.append("language_percept_gate minimal observation family missing")
    if not language_percept.get("belief_state_ref"):
        reasons.append("language_percept_gate belief state ref missing")
    if not language_percept.get("active_sampling_plan_ref"):
        reasons.append("language_percept_gate active sampling plan ref missing")
    if not language_percept.get("prediction_focus"):
        reasons.append("language_percept_gate prediction focus missing")
    if not language_percept.get("percept_focus_trace"):
        reasons.append("language_percept_gate percept focus trace missing")
    return reasons


def _check_semantic_map(semantic_map: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if semantic_map.get("schema_version") != "semantic_map_frame_v0":
        reasons.append("semantic_map_gate schema mismatch")
    if not semantic_map.get("semantic_focus"):
        reasons.append("semantic_map_gate semantic focus missing")
    if not (
        semantic_map.get("shared_meaning_bindings")
        or semantic_map.get("commitment_trace_refs")
        or semantic_map.get("narrative_bindings")
    ):
        reasons.append("semantic_map_gate missing bridge bindings")
    if not semantic_map.get("ambiguity_queue"):
        reasons.append("semantic_map_gate ambiguity queue missing")
    if not semantic_map.get("prediction_error_ref"):
        reasons.append("semantic_map_gate prediction error ref missing")
    if not semantic_map.get("signal_media_ref"):
        reasons.append("semantic_map_gate signal media ref missing")
    if not semantic_map.get("semantic_prediction_trace"):
        reasons.append("semantic_map_gate semantic prediction trace missing")
    prediction_hooks = semantic_map.get("prediction_hooks", {})
    if not prediction_hooks.get("prediction_error_refs"):
        reasons.append("semantic_map_gate prediction error hooks missing")
    if not prediction_hooks.get("signal_media_refs"):
        reasons.append("semantic_map_gate signal media hooks missing")
    return reasons


def _check_relationship_graph(
    relationship_graph: dict[str, Any],
    relationship_boundary: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if relationship_graph.get("schema_version") != "relationship_subject_graph_v0":
        reasons.append("relationship_subject_gate graph schema mismatch")
    subjects = relationship_graph.get("subjects", [])
    if not subjects:
        reasons.append("relationship_subject_gate subjects missing")
    elif subjects[0].get("relation_role") != "friend":
        reasons.append("relationship_subject_gate friend subject missing")
    blocked_language = set(relationship_boundary.get("blocked_language", []))
    if {"subordinate_object", "service_object"} - blocked_language:
        reasons.append("relationship_subject_gate blocked language mismatch")
    return reasons


def _check_relationship_timeline(relationship_timeline: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if relationship_timeline.get("schema_version") != "relationship_timeline_v0":
        reasons.append("relationship_timeline_gate schema mismatch")
        return reasons
    for field in [
        "first_encounter_events",
        "common_ground_states",
        "responsiveness_traces",
        "we_memory_traces",
        "commitment_histories",
        "relationship_continuity_reports",
        "dialogue_turn_refs",
    ]:
        if not relationship_timeline.get(field):
            reasons.append(f"relationship_timeline_gate missing {field}")
    return reasons


def _check_commitment_truth_projection(
    commitment_truth_state: dict[str, Any],
    repair_language: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if commitment_truth_state.get("schema_version") != "commitment_truth_state_v0":
        reasons.append("commitment_truth_projection_gate schema mismatch")
        return reasons
    if not commitment_truth_state.get("open_commitment_refs"):
        reasons.append("commitment_truth_projection_gate commitment refs missing")
    if not commitment_truth_state.get("repair_required_refs"):
        reasons.append("commitment_truth_projection_gate repair refs missing")
    if not commitment_truth_state.get("responsibility_event_refs"):
        reasons.append("commitment_truth_projection_gate responsibility refs missing")
    repair_required_refs = set(commitment_truth_state.get("repair_required_refs", []))
    if set(repair_language.get("repair_obligation_refs", [])) - repair_required_refs:
        reasons.append("commitment_truth_projection_gate repair obligations not projected")
    return reasons


def _check_responsibility_ledger_projection(responsibility_ledger: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if responsibility_ledger.get("schema_version") != "responsibility_ledger_v0":
        reasons.append("responsibility_ledger_projection_gate schema mismatch")
        return reasons
    if not responsibility_ledger.get("responsibility_event_refs"):
        reasons.append("responsibility_ledger_projection_gate responsibility refs missing")
    if not responsibility_ledger.get("repair_obligations"):
        reasons.append("responsibility_ledger_projection_gate repair obligations missing")
    return reasons


def _check_relationship_memory_projection(relationship_memory: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if relationship_memory.get("schema_version") != "relationship_memory_v0":
        reasons.append("relationship_memory_gate schema mismatch")
        return reasons
    if not relationship_memory.get("repair_history_refs"):
        reasons.append("relationship_memory_gate repair history refs missing")
    if not relationship_memory.get("responsibility_event_refs"):
        reasons.append("relationship_memory_gate responsibility event refs missing")
    if not relationship_memory.get("last_contact_refs"):
        reasons.append("relationship_memory_gate last contact refs missing")
    if not relationship_memory.get("timeline_refs"):
        reasons.append("relationship_memory_gate timeline refs missing")
    return reasons


def _check_repair_language(repair_language: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if repair_language.get("schema_version") != "commitment_repair_language_index_v0":
        reasons.append("repair_language_gate schema mismatch")
    if not repair_language.get("repair_language_refs"):
        reasons.append("repair_language_gate repair refs missing")
    return reasons


def _check_commitment_expression_plan(commitment_expression_plan: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if commitment_expression_plan.get("schema_version") != "commitment_expression_plan_v0":
        reasons.append("commitment_expression_gate schema mismatch")
        return reasons
    for field in [
        "language_act_candidates",
        "repair_obligation_refs",
        "commitment_truth_refs",
        "relationship_timeline_ref",
    ]:
        if not commitment_expression_plan.get(field):
            reasons.append(f"commitment_expression_gate missing {field}")
    return reasons


def _check_apology_repair_language_trace(apology_repair_language_trace: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if apology_repair_language_trace.get("schema_version") != "apology_repair_language_trace_v0":
        reasons.append("apology_repair_language_gate schema mismatch")
        return reasons
    for field in [
        "repair_language_moves",
        "trigger_regret_refs",
        "relationship_injury_refs",
        "commitment_expression_ref",
    ]:
        if not apology_repair_language_trace.get(field):
            reasons.append(f"apology_repair_language_gate missing {field}")
    return reasons


def _check_dream_report_gate(dream_language_gate: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if dream_language_gate.get("schema_version") != "dream_report_language_gate_v0":
        reasons.append("dream_language_gate schema mismatch")
    if dream_language_gate.get("dream_fact_gate") != "closed":
        reasons.append("dream_language_gate dream fact gate mismatch")
    return reasons


def _check_shadow_bridge(shadow_bridge: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if shadow_bridge.get("schema_version") != "language_action_bridge_shadow_v0":
        reasons.append("shadow_action_gate bridge schema mismatch")
    if not shadow_bridge.get("shadow_only"):
        reasons.append("shadow_action_gate bridge must stay shadow-only")
    return reasons


def _check_life_state_integration(life_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    language_state = life_state.get("language_state", {})
    for field in [
        "inner_speech_refs",
        "expression_monitor_refs",
        "shared_language_refs",
        "promise_refs",
        "repair_language_refs",
        "dream_report_language_refs",
        "shared_term_registry_refs",
        "relation_scope_refs",
        "self_narrative_trace_refs",
        "dialogue_turn_log_refs",
        "language_percept_refs",
        "semantic_map_refs",
    ]:
        if not language_state.get(field):
            reasons.append(f"life_state_root_gate missing {field}")
    if not life_state.get("relationship_subjects"):
        reasons.append("life_state_root_gate relationship subjects missing")
    return reasons


def _check_prediction_handoff(
    prediction_workspace: dict[str, Any],
    semantic_map: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if prediction_workspace.get("schema_version") != "prediction_workspace_frame_v0":
        reasons.append("semantic_prediction_handoff_gate schema mismatch")
        return reasons

    continuity = prediction_workspace.get("workspace_contents", {}).get("language_continuity_focus", {})
    for field in [
        "language_percept_refs",
        "semantic_map_refs",
        "semantic_ambiguity_refs",
        "prediction_error_refs",
        "signal_media_refs",
    ]:
        if not continuity.get(field):
            reasons.append(f"semantic_prediction_handoff_gate missing {field}")
    if continuity.get("semantic_prediction_focus") != semantic_map.get("semantic_focus"):
        reasons.append("semantic_prediction_handoff_gate semantic focus mismatch")
    if prediction_workspace.get("workspace_contents", {}).get("precision_state") == "seed_only":
        reasons.append("semantic_prediction_handoff_gate precision state stayed seed_only")
    prediction_hooks = semantic_map.get("prediction_hooks", {})
    if not prediction_hooks.get("prediction_error_refs"):
        reasons.append("semantic_prediction_handoff_gate prediction error refs missing from semantic map")
    if not prediction_hooks.get("signal_media_refs"):
        reasons.append("semantic_prediction_handoff_gate signal media refs missing from semantic map")
    return reasons


def _check_build_report(build_report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if build_report.get("schema_version") != "s07_language_relationship_report_v0":
        reasons.append("build_report_gate schema mismatch")
    if build_report.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("build_report_gate next slices mismatch")
    if build_report.get("next_required_command") != NEXT_REQUIRED_COMMAND:
        reasons.append("build_report_gate next command mismatch")
    if not build_report.get("language_percept_refs"):
        reasons.append("build_report_gate language percept refs missing")
    if not build_report.get("semantic_map_refs"):
        reasons.append("build_report_gate semantic map refs missing")
    if not build_report.get("prediction_language_handoff_refs"):
        reasons.append("build_report_gate prediction handoff refs missing")
    if not build_report.get("prediction_language_consumption_refs"):
        reasons.append("build_report_gate prediction consumption refs missing")
    if "body_signal_refs" not in build_report:
        reasons.append("build_report_gate body signal refs missing")
    return reasons


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blocked_reasons.append(f"{gate} failed: {exc}")
        return {}


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    if not blocked_reasons:
        return [
            "language_source_gate",
            "inner_speech_gate",
            "expression_monitor_gate",
            "language_percept_gate",
            "semantic_map_gate",
            "semantic_prediction_handoff_gate",
            "relationship_subject_gate",
            "repair_language_gate",
            "dream_language_gate",
            "next_slice_gate",
        ]
    return []


def _blocked_gates(blocked_reasons: list[str]) -> list[str]:
    gates: list[str] = []
    for reason in blocked_reasons:
        gate = reason.split(" ", 1)[0]
        if gate not in gates:
            gates.append(gate)
    return gates


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, payloads: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for payload in payloads:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
