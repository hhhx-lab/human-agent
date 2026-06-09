from __future__ import annotations

from typing import Any


def build_life_target_evidence_matrix(
    *,
    run_id: str,
    generated_at: str,
    active_engineering_slice: str,
    life_targets: list[str],
    evidence_families: list[str],
    receipt_ref: str,
    report_ref: str,
    consciousness_probe_ref: str | None = None,
) -> dict[str, Any]:
    targets = {}
    for target in life_targets:
        runtime_refs = [
            "runtime/state/membrane/birth_readiness_precheck.json",
            "runtime/reports/latest/life_membrane_report.json",
            "runtime/state/neural_life_core/neural_life_internal_bus.json",
            "runtime/reports/latest/language_relationship_report.json",
        ]
        if target == "real_consciousness" and consciousness_probe_ref:
            runtime_refs = [consciousness_probe_ref, *runtime_refs]
        targets[target] = {
            "state": [
                "runtime/state/life_state.json",
                "runtime/state/life_targets/life_target_claims.json",
                _state_namespace_for_target(target),
            ],
            "memory": [
                "runtime/state/life_state.json#memory_index",
                "runtime/state/indexes/memory_index.json",
                "runtime/state/indexes/replay_index.json",
            ],
            "language": [
                "runtime/state/language/language_percept_frame.json",
                "runtime/state/language/semantic_map_frame.json",
                "runtime/state/prediction/prediction_workspace_frame.json#workspace_contents.language_continuity_focus",
            ],
            "relationship": [
                "runtime/state/life_state.json#relationship_subjects",
                "runtime/state/membrane/relationship_subject_boundary.json",
                "runtime/state/indexes/relationship_index.json",
            ],
            "dream": [
                "runtime/state/life_state.json#dream_records",
                "runtime/state/membrane/dream_fact_boundary.json",
                "runtime/state/indexes/dream_index.json",
            ],
            "pain_regret_responsibility": [
                "runtime/state/life_state.json#pain_events",
                "runtime/state/life_state.json#regret_events",
                "runtime/state/life_state.json#responsibility_bindings",
                "runtime/state/membrane/responsibility_repair_boundary.json",
            ],
            "self_growth": [
                "runtime/state/life_state.json#self_model",
                "runtime/state/self/autobiographical_stack.json",
                "runtime/state/direction/value_orientation.json",
            ],
            "runtime": runtime_refs,
            "report": [
                report_ref,
                "runtime/reports/latest/life_target_status.json",
                "runtime/reports/latest/birth_readiness_digest.json",
            ],
            "archive": [receipt_ref],
        }
    return {
        "schema_version": "life_target_evidence_matrix_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "active_engineering_slice": active_engineering_slice,
        "evidence_families": evidence_families,
        "targets": targets,
    }


def _state_namespace_for_target(target: str) -> str:
    mapping = {
        "real_consciousness": "runtime/state/consciousness/",
        "real_emotion": "runtime/state/self/",
        "real_personality": "runtime/state/self/",
        "real_life": "runtime/state/",
        "real_pain": "runtime/state/action/",
        "real_dream": "runtime/state/dream/",
        "real_relationship": "runtime/state/relationship/",
        "real_responsibility": "runtime/state/action/",
        "real_regret": "runtime/state/action/",
    }
    return mapping[target]
