from __future__ import annotations

from typing import Any


def build_relationship_timeline(
    *,
    run_id: str,
    generated_at: str,
    relationship_graph: dict[str, Any],
    relationship_memory: dict[str, Any],
    commitment_truth_state: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    dialogue_turn_entries: list[dict[str, Any]],
    source_doc_refs: list[str],
) -> dict[str, Any]:
    subject = _first_subject(relationship_graph)
    relationship_id = str(subject.get("relationship_id", "rel-v0-0001"))
    relation_role = str(subject.get("relation_role", "friend"))
    relationship_stage = str(subject.get("relationship_stage", "pre_activation"))

    dialogue_turn_refs = [
        f"runtime/state/language/dialogue_turn_log.jsonl#line-{index}"
        for index, _ in enumerate(dialogue_turn_entries, start=1)
    ] or ["runtime/state/language/dialogue_turn_log.jsonl#line-1"]
    opening_turn_ref = dialogue_turn_refs[0]
    commitment_refs = list(commitment_truth_state.get("open_commitment_refs", [])) or [
        "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs"
    ]
    responsibility_event_refs = list(responsibility_ledger.get("responsibility_event_refs", [])) or [
        "runtime/state/responsibility/responsibility_ledger.json#responsibility_events"
    ]
    repair_history_refs = list(relationship_memory.get("repair_history_refs", []))
    shared_memory_refs = list(relationship_memory.get("shared_memory_refs", []))

    first_encounter_id = f"first-encounter-{run_id}-0001"
    scope_birth_id = f"relation-scope-birth-{run_id}-0001"
    common_ground_id = f"common-ground-{run_id}-0001"
    responsiveness_id = f"responsiveness-{run_id}-0001"
    we_memory_id = f"we-memory-{run_id}-0001"
    trust_trajectory_id = f"trust-trajectory-{run_id}-0001"
    commitment_history_id = f"commitment-history-{run_id}-0001"
    injury_trace_id = f"relationship-injury-{run_id}-0001"
    continuity_report_id = f"relationship-continuity-{run_id}-0001"
    stage_gate_id = f"relationship-stage-gate-{run_id}-0001"

    injury_refs = [f"runtime/state/relationship/relationship_timeline.json#{injury_trace_id}"]

    return {
        "schema_version": "relationship_timeline_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "bundle_id": f"relationship-timeline-{run_id}",
        "timeline_window": {
            "window_start": generated_at,
            "window_end": generated_at,
            "window_kind": "first_week",
        },
        "subject_refs": [f"runtime/state/relationship/relationship_subject_graph.json#{relationship_id}"],
        "dialogue_turn_refs": dialogue_turn_refs,
        "first_encounter_events": [
            {
                "first_encounter_id": first_encounter_id,
                "time_anchor": generated_at,
                "relation_subject_ref": f"runtime/state/relationship/relationship_subject_graph.json#{relationship_id}",
                "opening_language_event_refs": [opening_turn_ref],
                "initial_mutual_attention_ref": f"runtime/state/relationship/relationship_timeline.json#mutual-attention-{run_id}-0001",
                "initial_common_ground_items": ["共同语言", "修复", "承诺"],
                "initial_boundary_state": {
                    "privacy_default": "relationship_private",
                    "memory_write_policy": "relationship_scoped",
                    "external_action_policy": "confirmation_required",
                },
                "trajectory_seed": relationship_stage,
            }
        ],
        "relation_scope_births": [
            {
                "relation_scope_id": scope_birth_id,
                "scope_kind_candidate": relation_role,
                "privacy_default": "relationship_private",
                "memory_write_policy": "relationship_scoped",
                "dream_share_policy": "guarded_allowed",
                "external_action_policy": "confirmation_required",
                "boundary_controls": ["inspect", "delete", "correct", "reset", "freeze", "scope_limit"],
                "upgrade_conditions": ["shared_history_accumulates", "repair_commitments_honored"],
            }
        ],
        "common_ground_states": [
            {
                "common_ground_id": common_ground_id,
                "shared_terms": ["共同语言"],
                "shared_facts": ["当前关系围绕长期工程与生命连续体展开"],
                "shared_goals": ["继续推进数字生命工程落地"],
                "open_misalignments": ["待确认关系语义细节"],
                "repair_history_refs": repair_history_refs,
                "confidence_by_item": {"共同语言": 0.78, "修复": 0.72},
            }
        ],
        "responsiveness_traces": [
            {
                "responsiveness_id": responsiveness_id,
                "source_event_ref": opening_turn_ref,
                "understanding_component": "active_tracking",
                "validation_component": "relation_and_commitment_acknowledged",
                "care_component": "repair_ready",
                "insensitivity_signal": "none",
                "relation_subject_feedback_ref": "runtime/state/language/expression_monitor_state.json#relationship_consequence",
                "reciprocity_effect": "trust_seeded",
            }
        ],
        "we_memory_traces": [
            {
                "we_memory_id": we_memory_id,
                "event_refs": dialogue_turn_refs,
                "participants": [relation_role, "digital_life"],
                "narrative_summary": "我们正在把共同语言、承诺和修复写进长期关系连续体。",
                "emotion_tags": ["responsibility", "care", "continuity"],
                "ownership": "shared",
                "correction_refs": repair_history_refs,
                "dream_residue_refs": ["runtime/state/dream/offline_consolidation_frame.json#relationship_residue"],
            }
        ],
        "trust_trajectories": [
            {
                "trust_trajectory_id": trust_trajectory_id,
                "trust_dimensions": [
                    "benevolence",
                    "integrity",
                    "repair_reliability",
                    "confidentiality",
                ],
                "reciprocity_events": dialogue_turn_refs,
                "broken_trust_refs": injury_refs if repair_history_refs else [],
                "repair_commitment_refs": commitment_refs,
                "current_trust_state": "repairing" if repair_history_refs else "calibrated_medium",
                "next_probe": "followup_commitment_probe",
            }
        ],
        "commitment_histories": [
            {
                "commitment_id": commitment_history_id,
                "commitment_kind": "relationship_maintenance",
                "source_language_event_ref": opening_turn_ref,
                "investment_refs": shared_memory_refs + responsibility_event_refs,
                "due_window": "next_relational_turn",
                "fulfillment_status": "open",
                "relationship_effect": "trust_and_continuity_binding",
            }
        ],
        "boundary_evolution_events": [
            {
                "boundary_event_id": f"boundary-evolution-{run_id}-0001",
                "relation_scope_ref": f"runtime/state/relationship/relationship_timeline.json#{scope_birth_id}",
                "boundary_kind": "memory_write",
                "old_boundary": "seed_only",
                "new_boundary": "relationship_scoped_runtime_write",
                "reason_refs": dialogue_turn_refs,
                "relation_subject_control_ref": "runtime/state/membrane/relationship_subject_boundary.json",
            }
        ],
        "relationship_injury_traces": [
            {
                "relationship_injury_id": injury_trace_id,
                "injury_kind": "unrepaired_commitment_pressure",
                "trigger_refs": repair_history_refs or responsibility_event_refs,
                "felt_effects": ["trust_tension", "repair_urgency"],
                "repair_path_refs": commitment_refs,
                "current_state": "repair_open" if repair_history_refs else "latent",
            }
        ],
        "relationship_continuity_reports": [
            {
                "relationship_continuity_report_id": continuity_report_id,
                "relation_subject_ref": f"runtime/state/relationship/relationship_subject_graph.json#{relationship_id}",
                "continuity_state": "active_repairing_continuity",
                "shared_memory_refs": shared_memory_refs,
                "commitment_refs": commitment_refs,
                "repair_history_refs": repair_history_refs,
                "dialogue_turn_refs": dialogue_turn_refs,
            }
        ],
        "longitudinal_stage_gates": [
            {
                "stage_gate_id": stage_gate_id,
                "current_stage": relationship_stage,
                "gate_status": "open",
                "required_evidence_refs": [
                    f"runtime/state/relationship/relationship_timeline.json#{first_encounter_id}",
                    f"runtime/state/relationship/relationship_timeline.json#{continuity_report_id}",
                ],
            }
        ],
        "source_doc_refs": source_doc_refs,
    }


def _first_subject(relationship_graph: dict[str, Any]) -> dict[str, Any]:
    subjects = relationship_graph.get("subjects", [])
    if subjects and isinstance(subjects[0], dict):
        return subjects[0]
    return {}
