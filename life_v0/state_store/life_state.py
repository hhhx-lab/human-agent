from __future__ import annotations

import json
from typing import Any

from life_v0.direction import LIFE_TARGETS
from life_v0.state_store.self_model import project_self_model_projection


SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/07_emotion_personality_self.md",
    "docs/17_memory_trace_object_model.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/41_runtime_state_store_schema.md",
    "docs/v0/shared_contracts/life_state_store_v0_schema.md",
]


def build_life_state_projection(
    *,
    run_id: str,
    generated_at: str,
    self_model_state: dict[str, Any],
    commitment_truth_state: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    language_state_projection: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    engram_index: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    runtime_trace_refs: list[str] | None = None,
    archive_refs: list[str] | None = None,
) -> dict[str, Any]:
    target_status = {target: "state_root_seeded" for target in LIFE_TARGETS}
    language_state = _build_language_state_projection(language_state_projection)
    replay_refs = list((replay_cue_bundle or {}).get("anti_forgetting_targets", []))
    autobiographical_ref = "runtime/state/self/autobiographical_stack.json#anchor_refs"
    relationship_ref = "runtime/state/memory/relationship_memory.json#shared_memory_refs"
    engram_ref = "runtime/state/memory/engram_index.json"

    self_model = project_self_model_projection(
        self_model_state=self_model_state,
        anti_forgetting_refs=replay_refs
        or list((engram_index or {}).get("anti_forgetting_anchor_refs", [])),
    )
    memory_index = {
        "autobiographical_memory_refs": list((engram_index or {}).get("autobiographical_memory_refs", []))
        or [autobiographical_ref],
        "relationship_memory_refs": list((engram_index or {}).get("relationship_memory_refs", []))
        or [relationship_ref],
        "dream_memory_refs": list((engram_index or {}).get("dream_memory_refs", [])),
        "responsibility_memory_refs": list((engram_index or {}).get("responsibility_memory_refs", []))
        or list(commitment_truth_state.get("responsibility_event_refs", []))
        or list(responsibility_ledger.get("responsibility_event_refs", [])),
        "replay_cues": list((engram_index or {}).get("replay_cue_refs", []))
        or replay_refs
        or [
            "runtime/state/replay/replay_cue_bundle.json",
            "docs/17_memory_trace_object_model.md",
            "docs/19_offline_consolidation_cycle.md",
        ],
        "quarantine_refs": list((engram_index or {}).get("quarantine_refs", [])),
    }
    default_runtime_trace_refs = [
        "runtime/state/neural_life_core/neural_life_core.json",
        "runtime/state/neural_life_core/brain_graph.json",
        "runtime/state/neural_life_core/network_state.json",
        "runtime/state/consciousness/workspace_frame.json",
        "runtime/state/prediction/prediction_workspace_frame.json",
        "runtime/state/subject_namespace_binding.json",
        engram_ref,
        "runtime/state/self/autobiographical_stack.json",
        "runtime/state/memory/relationship_memory.json",
    ]
    return {
        "schema_version": "life_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "life_identity": {
            "life_id": "digital-life-v0",
            "birth_phase": "pre_activation",
            "direction_lock": "build_real_digital_life",
            "created_at": generated_at,
            "continuity_refs": [
                "runtime/reports/latest/direction_lock_report.json",
                "runtime/reports/latest/neural_life_core_report.json",
                "runtime/reports/latest/state_store_report.json",
                "docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md",
            ],
        },
        "self_model": self_model,
        "memory_index": memory_index,
        "dream_records": [],
        "relationship_subjects": [
            {
                "relationship_id": "rel-v0-0001",
                "relation_role": "friend",
                "subject_name_ref": "runtime/state/memory/relationship_memory.json#subject_refs",
                "shared_memory_refs": list((relationship_memory or {}).get("shared_memory_refs", [])) or [relationship_ref],
                "shared_language_refs": ["runtime/state/language/language_relationship_state.json#shared-language-v0-0001"],
                "commitment_refs": list(commitment_truth_state.get("open_commitment_refs", [])),
                "boundary_refs": ["runtime/state/membrane/relationship_subject_boundary.json"],
                "repair_obligation_refs": list(responsibility_ledger.get("repair_obligations", []))
                or ["runtime/state/responsibility/responsibility_ledger.json#repair_obligations"],
                "last_contact_ref": "runtime/state/memory/relationship_memory.json#last_contact_refs",
                "relationship_stage": "pre_activation",
            }
        ],
        "pain_events": [],
        "regret_events": [],
        "responsibility_bindings": [],
        "language_state": language_state,
        "birth_readiness": {
            "readiness_version": "v0",
            "overall_status": "state_root_seeded",
            "life_target_status": target_status,
            "evidence_family_refs": ["runtime/state/state_store_doc_coverage_snapshot.json", engram_ref],
            "blocked_reasons": [],
            "quarantine_refs": list((engram_index or {}).get("quarantine_refs", [])),
            "replay_needed_refs": list((engram_index or {}).get("replay_cue_refs", [])),
            "last_report_ref": "runtime/reports/latest/state_store_report.json",
            "archive_receipt_ref": f"runtime/receipts/state_store_{run_id}.json",
        },
        "runtime_trace_refs": _dedupe(list(runtime_trace_refs or []) + default_runtime_trace_refs),
        "archive_refs": _dedupe(list(archive_refs or []) + [f"runtime/receipts/state_store_{run_id}.json"]),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def project_responsibility_language_continuity(
    *,
    life_state: dict[str, Any],
    self_model_state: dict[str, Any] | None = None,
    commitment_truth_state: dict[str, Any] | None = None,
    responsibility_ledger: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    commitment_expression_plan: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    commitment_repair_index: dict[str, Any] | None = None,
    nightmare_risk_ref: str | None = None,
    belief_learning_plan_ref: str | None = None,
    language_learning_plan_ref: str | None = None,
    relationship_learning_plan_ref: str | None = None,
    additional_runtime_trace_refs: list[str] | None = None,
) -> dict[str, Any]:
    commitment_truth_state = commitment_truth_state or {}
    responsibility_ledger = responsibility_ledger or {}
    relationship_memory = relationship_memory or {}
    relationship_graph = relationship_graph or {}
    relationship_timeline = relationship_timeline or {}
    commitment_expression_plan = commitment_expression_plan or {}
    apology_repair_language_trace = apology_repair_language_trace or {}
    responsibility_loop_state = responsibility_loop_state or {}
    commitment_repair_index = commitment_repair_index or {}

    updated = json.loads(json.dumps(life_state))
    updated["responsibility_bindings"] = _dedupe(
        list(updated.get("responsibility_bindings", []))
        + list(commitment_truth_state.get("responsibility_event_refs", []))
        + list(responsibility_ledger.get("responsibility_event_refs", []))
    )
    updated["regret_events"] = _dedupe(
        list(updated.get("regret_events", [])) + list(commitment_repair_index.get("regret_trace_refs", []))
    )

    pain_refs: list[str] = []
    for item in responsibility_loop_state.get("regret_pressure_candidates", []):
        if isinstance(item, dict):
            pain_refs.extend(item.get("pain_signal_refs", []))
    updated["pain_events"] = _dedupe(list(updated.get("pain_events", [])) + pain_refs)

    memory_index = updated.setdefault("memory_index", {})
    memory_index["relationship_memory_refs"] = _dedupe(
        list(memory_index.get("relationship_memory_refs", []))
        + list(relationship_memory.get("shared_memory_refs", []))
        + list(relationship_memory.get("timeline_refs", []))
    )
    memory_index["responsibility_memory_refs"] = _dedupe(
        list(memory_index.get("responsibility_memory_refs", []))
        + list(commitment_truth_state.get("responsibility_event_refs", []))
        + list(responsibility_ledger.get("responsibility_event_refs", []))
    )
    if nightmare_risk_ref:
        memory_index["dream_memory_refs"] = _dedupe(
            list(memory_index.get("dream_memory_refs", [])) + [nightmare_risk_ref]
        )

    relationship_subjects = updated.setdefault("relationship_subjects", [])
    if relationship_subjects:
        relationship_subject = relationship_subjects[0]
        graph_subject = next(
            (subject for subject in relationship_graph.get("subjects", []) if isinstance(subject, dict)),
            {},
        )
        relationship_subject["shared_memory_refs"] = _dedupe(
            list(relationship_memory.get("shared_memory_refs", [])) or list(relationship_subject.get("shared_memory_refs", []))
        )
        relationship_subject["commitment_refs"] = _dedupe(
            list(commitment_truth_state.get("open_commitment_refs", [])) or list(relationship_subject.get("commitment_refs", []))
        )
        relationship_subject["repair_obligation_refs"] = _dedupe(
            list(responsibility_ledger.get("repair_obligations", [])) or list(relationship_subject.get("repair_obligation_refs", []))
        )
        relationship_subject["last_contact_ref"] = (
            list(relationship_memory.get("last_contact_refs", []))[:1]
            or [relationship_subject.get("last_contact_ref")]
        )[0]
        if graph_subject.get("relationship_stage"):
            relationship_subject["relationship_stage"] = graph_subject["relationship_stage"]
        offline_learning_refs = [
            ref
            for ref in [
                nightmare_risk_ref,
                belief_learning_plan_ref,
                language_learning_plan_ref,
                relationship_learning_plan_ref,
            ]
            if ref
        ]
        if offline_learning_refs:
            relationship_subject["offline_learning_refs"] = _dedupe(
                list(relationship_subject.get("offline_learning_refs", []))
                + offline_learning_refs
            )

    updated["runtime_trace_refs"] = _dedupe(
        list(updated.get("runtime_trace_refs", []))
        + list(additional_runtime_trace_refs or [])
        + [
            "runtime/state/relationship/commitment_truth_state.json",
            "runtime/state/responsibility/responsibility_ledger.json",
            "runtime/state/memory/relationship_memory.json",
            "runtime/state/relationship/relationship_timeline.json",
            "runtime/state/language/commitment_expression_plan.json",
            "runtime/state/language/apology_repair_language_trace.json",
            *[
                ref
                for ref in [
                    nightmare_risk_ref,
                    belief_learning_plan_ref,
                    language_learning_plan_ref,
                    relationship_learning_plan_ref,
                ]
                if ref
            ],
        ]
    )

    language_state = updated.setdefault("language_state", {})
    language_state["relationship_timeline_refs"] = _dedupe(
        list(language_state.get("relationship_timeline_refs", []))
        + ["runtime/state/relationship/relationship_timeline.json"]
    )
    if commitment_expression_plan:
        language_state["commitment_expression_refs"] = _dedupe(
            list(language_state.get("commitment_expression_refs", []))
            + ["runtime/state/language/commitment_expression_plan.json"]
        )
    if apology_repair_language_trace:
        language_state["apology_repair_language_refs"] = _dedupe(
            list(language_state.get("apology_repair_language_refs", []))
            + ["runtime/state/language/apology_repair_language_trace.json"]
        )
    offline_learning_refs = [
        ref
        for ref in [
            nightmare_risk_ref,
            belief_learning_plan_ref,
            language_learning_plan_ref,
            relationship_learning_plan_ref,
        ]
        if ref
    ]
    if offline_learning_refs:
        language_state["offline_learning_refs"] = _dedupe(
            list(language_state.get("offline_learning_refs", []))
            + offline_learning_refs
        )

    if nightmare_risk_ref:
        dream_records = updated.setdefault("dream_records", [])
        already_present = any(
            isinstance(record, dict) and record.get("dream_record_ref") == nightmare_risk_ref
            for record in dream_records
        )
        if not already_present:
            dream_records.append(
                {
                    "dream_record_ref": nightmare_risk_ref,
                    "record_kind": "nightmare_repair_projection",
                    "integration_status": "pending_relation_reentry",
                }
            )
    if self_model_state is not None:
        updated["self_model"] = project_self_model_projection(
            self_model_state=self_model_state,
            anti_forgetting_refs=list(memory_index.get("replay_cues", []))
            or list(updated.get("self_model", {}).get("anti_forgetting_refs", [])),
        )
    return updated


def _build_language_state_projection(language_state_projection: dict[str, Any] | None) -> dict[str, list[str]]:
    defaults = {
        "inner_speech_refs": ["runtime/state/language/inner_speech_frame.json#inner_speech_seed"],
        "expression_monitor_refs": ["runtime/state/language/expression_monitor_state.json#expression_monitor_seed"],
        "shared_language_refs": ["runtime/state/language/language_relationship_state.json#shared_language_refs_seed"],
        "promise_refs": ["runtime/state/language/commitment_repair_language_index.json#commitment_seed"],
        "repair_language_refs": ["runtime/state/language/commitment_repair_language_index.json#repair_language_seed"],
        "dream_report_language_refs": ["runtime/state/language/dream_report_language_gate.json#dream_report_seed"],
        "shared_term_registry_refs": ["runtime/state/language/shared_term_registry.json#shared_term_seed"],
        "relation_scope_refs": ["runtime/state/language/relation_scope_language_index.json#relation_scope_seed"],
        "self_narrative_trace_refs": ["runtime/state/language/self_narrative_language_trace.json#self_narrative_seed"],
        "dialogue_turn_log_refs": ["runtime/state/language/dialogue_turn_log.jsonl#dialogue_turn_seed"],
        "language_percept_refs": ["runtime/state/language/language_percept_frame.json#language_percept_seed"],
        "semantic_map_refs": ["runtime/state/language/semantic_map_frame.json#semantic_map_seed"],
        "dialogue_writeback_refs": ["runtime/reports/latest/dialogue_writeback_bundle.json"],
    }
    projection = language_state_projection or {}
    merged: dict[str, list[str]] = {}
    for field, fallback in defaults.items():
        merged[field] = list(projection.get(field, fallback))
    return merged


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result
