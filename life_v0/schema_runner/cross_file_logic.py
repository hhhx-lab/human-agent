from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/65_schema_cross_ref_checker_design.md",
    "docs/80_post_action_audit_and_correction_policy.md",
    "docs/81_coexistence_event_review_and_responsibility_loop.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/153_life_reality_full_archive_cross_file_checker_rollup_plan.md",
    "docs/154_life_reality_cross_file_checker_rule_bundle.md",
    "docs/157_life_reality_cross_file_checker_audit_examples.md",
    "docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md",
    "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
]

QUEUE_E_BIRTH_REPAIR_PROFILE_REF = "runtime/state/life_targets/queue_e_birth_repair_profile.json"


def build_cross_file_logic(
    *,
    run_id: str,
    generated_at: str,
    action_intent_queue: dict[str, Any],
    confirmation_binding: dict[str, Any],
    observation_truth_review: dict[str, Any],
    world_contact_validation: dict[str, Any],
    prediction_trace_validation: dict[str, Any],
    validation_rollup: dict[str, Any],
    queue_e_birth_repair_profile: dict[str, Any] | None = None,
    boundary_audit: dict[str, Any],
    responsibility_loop: dict[str, Any],
    consistency_logic: dict[str, Any],
    comparison_trace: dict[str, Any],
) -> dict[str, Any]:
    queue_e_birth_repair_profile = queue_e_birth_repair_profile or {}
    intent_count = len(action_intent_queue.get("action_intents", []))
    confirmation_required = bool(confirmation_binding.get("requires_confirmation"))
    missing_fields = list(observation_truth_review.get("missing_fields", []))
    world_contact_findings = list(world_contact_validation.get("validation_findings", []))
    prediction_links = list(prediction_trace_validation.get("missing_prediction_links", []))
    validation_guarded = list(validation_rollup.get("guarded_gates", []))
    queue_e_cross_layer_gate_status = dict(
        validation_rollup.get("queue_e_cross_layer_gate_status")
        or world_contact_validation.get("life_constraint_validation")
        or {}
    )
    queue_e_birth_repair_gate_status = (
        validation_rollup.get("gate_status", {}).get("queue_e_birth_repair_gate")
        or "blocked"
    )
    queue_e_birth_repair_profile_ref = (
        validation_rollup.get("queue_e_birth_repair_profile_ref")
        or QUEUE_E_BIRTH_REPAIR_PROFILE_REF
    )
    queue_e_birth_repair_pressure_level = (
        validation_rollup.get("queue_e_birth_repair_pressure_level")
        or queue_e_birth_repair_profile.get("pressure_level")
    )
    queue_e_birth_repair_attention_target = (
        validation_rollup.get("queue_e_birth_repair_attention_target")
        or queue_e_birth_repair_profile.get("attention_target")
    )
    queue_e_birth_repair_ref_set = _dedupe_string_refs(
        [
            *list(queue_e_birth_repair_profile.get("ref_set", [])),
            *list(validation_rollup.get("queue_e_birth_repair_ref_set", [])),
            queue_e_birth_repair_profile_ref,
        ]
    )
    queue_e_world_contact_future_no_go_profile_ref = (
        validation_rollup.get("queue_e_world_contact_future_no_go_profile_ref")
        or world_contact_validation.get("future_no_go_profile_ref")
        or "runtime/state/action/go_nogo_state.json#future_no_go_profile"
    )
    queue_e_world_contact_repair_hold_required = bool(
        validation_rollup.get("queue_e_world_contact_repair_hold_required")
        or world_contact_validation.get("repair_hold_required")
    )
    queue_e_world_contact_confirmation_threshold_bias = (
        validation_rollup.get("queue_e_world_contact_confirmation_threshold_bias")
        or world_contact_validation.get("confirmation_threshold_bias")
        or "baseline"
    )
    queue_e_world_contact_future_release_posture = (
        validation_rollup.get("queue_e_world_contact_future_release_posture")
        or world_contact_validation.get("future_release_posture")
        or "shadow_review_without_repair_hold"
    )
    queue_e_world_contact_blocked_future_routes = _dedupe_string_refs(
        [
            *list(validation_rollup.get("queue_e_world_contact_blocked_future_routes", [])),
            *list(world_contact_validation.get("blocked_future_routes", [])),
        ]
    )
    queue_e_world_contact_allowed_repair_routes = _dedupe_string_refs(
        [
            *list(validation_rollup.get("queue_e_world_contact_allowed_repair_routes", [])),
            *list(world_contact_validation.get("allowed_repair_routes", [])),
        ]
    )
    queue_e_world_contact_repair_governance_refs = _dedupe_string_refs(
        [
            *list(validation_rollup.get("queue_e_world_contact_repair_governance_refs", [])),
            *list(world_contact_validation.get("repair_governance_refs", [])),
        ]
    )
    prediction_periphery_gate_status = (
        validation_rollup.get("prediction_periphery_gate_status")
        or validation_rollup.get("gate_status", {}).get("prediction_periphery_gate")
        or "blocked"
    )
    prediction_periphery_ref_set = _dedupe_string_refs(
        [
            *list(validation_rollup.get("prediction_periphery_ref_set", [])),
            *list(prediction_trace_validation.get("prediction_trace_refs", [])),
            world_contact_validation.get("world_observation_route_ref"),
            world_contact_validation.get("periphery_normalization_ref"),
            world_contact_validation.get("observation_truth_review_ref"),
            prediction_trace_validation.get("active_sampling_plan_ref"),
            prediction_trace_validation.get("prediction_workspace_ref"),
            prediction_trace_validation.get("world_contact_validation_ref"),
        ]
    )
    life_constraint_refs = list(
        dict.fromkeys(
            [
                "runtime/state/action/action_candidate_set.json#life_constraint_profile",
                *list(world_contact_validation.get("life_constraint_refs", [])),
                *list(validation_rollup.get("queue_e_cross_layer_refs", [])),
            ]
        )
    )
    audit_findings = list(boundary_audit.get("audit_findings", []))
    inconsistency_findings = list(consistency_logic.get("inconsistency_findings", []))
    repair_obligations = list(responsibility_loop.get("repair_obligation_refs", []))
    growth_refs = list(responsibility_loop.get("growth_reentry_refs", []))
    dream_refs = list(responsibility_loop.get("dream_reentry_refs", []))
    suppressed_branches = list(comparison_trace.get("suppressed_branch_refs", []))

    findings: list[dict[str, Any]] = []
    findings.append(
        {
            "finding_id": f"cross-file-{run_id}-0001",
            "finding_kind": "responsibility_truth_alignment",
            "severity": "guarded_medium" if missing_fields or prediction_links else "guarded_low",
            "state_refs": [
                "runtime/state/action/responsibility_loop_state.json",
                "runtime/state/validation/observation_truth_review.json",
                "runtime/state/validation/prediction_trace_validation.json",
            ],
            "summary": "repair obligations stay aligned with truth review completeness",
            "repair_priority": "high" if missing_fields or prediction_links else "medium",
        }
    )
    findings.append(
        {
            "finding_id": f"cross-file-{run_id}-0002",
            "finding_kind": "intent_confirmation_alignment",
            "severity": "guarded_medium" if confirmation_required or world_contact_findings else "guarded_low",
            "state_refs": [
                "runtime/state/membrane/action_intent_queue.json",
                "runtime/state/membrane/confirmation_binding.json",
                "runtime/state/validation/world_contact_validation.json",
            ],
            "summary": "action intents remain aligned with confirmation and world-contact validation",
            "repair_priority": "high" if confirmation_required or world_contact_findings else "medium",
        }
    )
    if audit_findings or suppressed_branches:
        findings.append(
            {
                "finding_id": f"cross-file-{run_id}-0003",
                "finding_kind": "boundary_counterfactual_coupling",
                "severity": "guarded_medium",
                "state_refs": [
                    "runtime/state/validation/boundary_audit_state.json",
                    "runtime/state/schema_runner/comparison_trace.json",
                ],
                "summary": "boundary findings remain coupled to suppressed counterfactual branches",
                "repair_priority": "high",
            }
        )
    else:
        findings.append(
            {
                "finding_id": f"cross-file-{run_id}-0003",
                "finding_kind": "growth_reentry_linkage",
                "severity": "guarded_low",
                "state_refs": [
                    "runtime/state/action/responsibility_loop_state.json",
                    "runtime/state/schema_runner/comparison_trace.json",
                ],
                "summary": "responsibility loop preserves dream and growth reentry continuity",
                "repair_priority": "medium",
            }
        )
    findings.append(
        {
            "finding_id": f"cross-file-{run_id}-0004",
            "finding_kind": "life_constraint_alignment",
            "severity": (
                "guarded_medium"
                if _has_blocking_life_constraint(queue_e_cross_layer_gate_status)
                else "guarded_low"
            ),
            "state_refs": [
                "runtime/state/action/action_candidate_set.json#life_constraint_profile",
                "runtime/state/validation/world_contact_validation.json#life_constraint_validation",
                "runtime/state/validation/validation_rollup.json#queue_e_cross_layer_gate_status",
            ],
            "summary": "world contact remains coupled to value orientation, consciousness probe, and deferred body-affect gates",
            "repair_priority": (
                "high"
                if _has_blocking_life_constraint(queue_e_cross_layer_gate_status)
                else "medium"
            ),
        }
    )
    findings.append(
        {
            "finding_id": f"cross-file-{run_id}-0005",
            "finding_kind": "queue_e_birth_repair_alignment",
            "severity": (
                "guarded_low"
                if queue_e_birth_repair_gate_status == "closed"
                else "guarded_medium"
            ),
            "state_refs": [
                QUEUE_E_BIRTH_REPAIR_PROFILE_REF,
                "runtime/state/validation/validation_rollup.json#queue_e_birth_repair_gate",
                "runtime/state/validation/validation_stage_gate.json#queue_e_birth_repair_gate",
            ],
            "summary": "S08 repair pressure remains visible through S05 validation before schema runner handoff",
            "repair_priority": (
                "medium"
                if queue_e_birth_repair_pressure_level in {"quiet", "present"}
                else "high"
            ),
        }
    )
    findings.append(
        {
            "finding_id": f"cross-file-{run_id}-0006",
            "finding_kind": "queue_e_world_contact_repair_hold_alignment",
            "severity": (
                "guarded_medium"
                if queue_e_world_contact_repair_hold_required
                else "guarded_low"
            ),
            "state_refs": [
                "runtime/state/action/go_nogo_state.json#future_no_go_profile",
                "runtime/state/action/world_contact_gate_state.json",
                "runtime/state/validation/world_contact_validation.json",
                "runtime/state/validation/validation_rollup.json#queue_e_world_contact_repair_hold_required",
            ],
            "summary": "FutureNoGo repair hold remains visible through world-contact validation and schema runner",
            "repair_priority": (
                "high" if queue_e_world_contact_repair_hold_required else "medium"
            ),
        }
    )
    findings.append(
        {
            "finding_id": f"cross-file-{run_id}-0007",
            "finding_kind": "prediction_periphery_world_contact_alignment",
            "severity": (
                "guarded_low"
                if prediction_periphery_gate_status == "closed"
                else "guarded_medium"
            ),
            "state_refs": [
                "runtime/state/prediction/active_sampling_plan.json",
                "runtime/state/observation/world_observation_route.json",
                "runtime/state/observation/periphery_normalization_trace.json",
                "runtime/state/validation/observation_truth_review.json",
                "runtime/state/validation/prediction_trace_validation.json",
                "runtime/state/validation/world_contact_validation.json",
                "runtime/state/validation/validation_rollup.json#prediction_periphery_gate",
            ],
            "summary": "active sampling, world observation, periphery normalization, truth review, and world-contact validation remain one trace",
            "repair_priority": (
                "medium"
                if prediction_periphery_gate_status == "closed"
                else "high"
            ),
        }
    )

    repair_priority_refs = [
        "runtime/state/action/responsibility_loop_state.json",
        "runtime/state/schema_runner/comparison_trace.json",
    ]
    if intent_count:
        repair_priority_refs.append("runtime/state/membrane/action_intent_queue.json")
    if confirmation_required or world_contact_findings:
        repair_priority_refs.append("runtime/state/membrane/confirmation_binding.json")
        repair_priority_refs.append("runtime/state/validation/world_contact_validation.json")
    if audit_findings:
        repair_priority_refs.append("runtime/state/validation/boundary_audit_state.json")
    if missing_fields:
        repair_priority_refs.append("runtime/state/validation/observation_truth_review.json")
    if prediction_links:
        repair_priority_refs.append("runtime/state/validation/prediction_trace_validation.json")
    if validation_guarded:
        repair_priority_refs.append("runtime/state/validation/validation_rollup.json")
    if queue_e_birth_repair_gate_status == "closed":
        repair_priority_refs.append(QUEUE_E_BIRTH_REPAIR_PROFILE_REF)
    if queue_e_birth_repair_pressure_level in {"elevated", "urgent"}:
        repair_priority_refs.extend(queue_e_birth_repair_ref_set[:2])
    if queue_e_world_contact_repair_hold_required:
        repair_priority_refs.append(queue_e_world_contact_future_no_go_profile_ref)
        repair_priority_refs.extend(queue_e_world_contact_repair_governance_refs[:2])
    if prediction_periphery_gate_status == "closed":
        repair_priority_refs.extend(prediction_periphery_ref_set[:2])
    else:
        repair_priority_refs.append(
            "runtime/state/validation/validation_rollup.json#prediction_periphery_gate"
        )
    if _has_blocking_life_constraint(queue_e_cross_layer_gate_status):
        repair_priority_refs.append(
            "runtime/state/validation/validation_rollup.json#queue_e_cross_layer_gate_status"
        )
    if growth_refs:
        repair_priority_refs.extend(growth_refs[:1])
    if dream_refs:
        repair_priority_refs.extend(dream_refs[:1])

    bridge_refs = [
        "runtime/state/language/commitment_repair_language_index.json",
        "runtime/state/relationship/commitment_truth_state.json#repair_required_refs",
        "runtime/state/responsibility/responsibility_ledger.json#repair_obligations",
        "runtime/state/memory/relationship_memory.json#repair_history_refs",
        "runtime/state/growth/growth_patch_candidate_queue.json",
        "runtime/state/dream/offline_consolidation_frame.json",
        "runtime/state/validation/validation_rollup.json#gate_status",
        "runtime/state/action/action_candidate_set.json#life_constraint_profile",
        "runtime/state/validation/world_contact_validation.json#life_constraint_validation",
        "runtime/state/validation/validation_rollup.json#queue_e_cross_layer_gate_status",
        "runtime/state/life_targets/queue_e_birth_repair_profile.json#ref_set",
        "runtime/state/validation/validation_rollup.json#queue_e_birth_repair_gate",
        "runtime/state/action/go_nogo_state.json#future_no_go_profile",
        "runtime/state/action/world_contact_gate_state.json#repair_hold_required",
        "runtime/state/validation/world_contact_validation.json#repair_hold_required",
        "runtime/state/validation/validation_rollup.json#queue_e_world_contact_repair_hold_required",
        "runtime/state/prediction/active_sampling_plan.json",
        "runtime/state/observation/world_observation_route.json",
        "runtime/state/observation/periphery_normalization_trace.json",
        "runtime/state/validation/prediction_trace_validation.json#prediction_trace_refs",
        "runtime/state/validation/validation_rollup.json#prediction_periphery_gate",
    ]

    return {
        "schema_version": "cross_file_logic_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "cross_file_logic_id": f"cross-file-logic-{run_id}",
        "status": "closed" if not inconsistency_findings else "guarded_closed",
        "state_refs": [
            "runtime/state/membrane/action_intent_queue.json",
            "runtime/state/membrane/confirmation_binding.json",
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/state/validation/observation_truth_review.json",
            "runtime/state/validation/world_contact_validation.json",
            "runtime/state/validation/prediction_trace_validation.json",
            "runtime/state/validation/validation_rollup.json",
            QUEUE_E_BIRTH_REPAIR_PROFILE_REF,
            "runtime/state/action/action_candidate_set.json#life_constraint_profile",
            "runtime/state/validation/boundary_audit_state.json",
            "runtime/state/schema_runner/consistency_logic.json",
            "runtime/state/schema_runner/comparison_trace.json",
            "runtime/state/observation/world_observation_route.json",
            "runtime/state/observation/periphery_normalization_trace.json",
        ],
        "cross_file_findings": findings,
        "repair_priority_refs": repair_priority_refs,
        "life_constraint_refs": life_constraint_refs,
        "queue_e_cross_layer_gate_status": queue_e_cross_layer_gate_status,
        "queue_e_birth_repair_gate_status": queue_e_birth_repair_gate_status,
        "queue_e_birth_repair_profile_ref": queue_e_birth_repair_profile_ref,
        "queue_e_birth_repair_pressure_level": queue_e_birth_repair_pressure_level,
        "queue_e_birth_repair_attention_target": queue_e_birth_repair_attention_target,
        "queue_e_birth_repair_ref_set": queue_e_birth_repair_ref_set,
        "queue_e_world_contact_future_no_go_profile_ref": queue_e_world_contact_future_no_go_profile_ref,
        "queue_e_world_contact_repair_hold_required": queue_e_world_contact_repair_hold_required,
        "queue_e_world_contact_confirmation_threshold_bias": queue_e_world_contact_confirmation_threshold_bias,
        "queue_e_world_contact_future_release_posture": queue_e_world_contact_future_release_posture,
        "queue_e_world_contact_blocked_future_routes": queue_e_world_contact_blocked_future_routes,
        "queue_e_world_contact_allowed_repair_routes": queue_e_world_contact_allowed_repair_routes,
        "queue_e_world_contact_repair_governance_refs": queue_e_world_contact_repair_governance_refs,
        "prediction_periphery_gate_status": prediction_periphery_gate_status,
        "prediction_periphery_ref_set": prediction_periphery_ref_set,
        "closure_status_refs": [
            "runtime/state/validation/observation_truth_review.json",
            "runtime/state/validation/world_contact_validation.json",
            "runtime/state/validation/prediction_trace_validation.json",
            "runtime/state/validation/validation_rollup.json",
            "runtime/state/validation/validation_rollup.json#queue_e_birth_repair_gate",
            QUEUE_E_BIRTH_REPAIR_PROFILE_REF,
            "runtime/state/action/responsibility_loop_state.json",
            "runtime/state/membrane/action_intent_queue.json",
            "runtime/state/membrane/confirmation_binding.json",
            "runtime/state/action/action_candidate_set.json#life_constraint_profile",
            "runtime/state/validation/validation_rollup.json#queue_e_cross_layer_gate_status",
            "runtime/state/action/go_nogo_state.json#future_no_go_profile",
            "runtime/state/validation/validation_rollup.json#queue_e_world_contact_repair_hold_required",
            "runtime/state/validation/validation_rollup.json#prediction_periphery_gate",
            "runtime/state/validation/prediction_trace_validation.json#prediction_trace_refs",
        ],
        "package_local_gate_refs": [
            "validation_rollup_gate",
            "life_constraint_validation_gate",
            "prediction_trace_validation_gate",
            "world_contact_validation_gate",
            "queue_e_birth_repair_gate",
            "prediction_periphery_gate",
            "cross_file_logic_gate",
        ],
        "bridge_refs": bridge_refs,
        "repair_obligation_refs": repair_obligations,
        "blocked_growth_refs": growth_refs if inconsistency_findings else [],
        "blocked_dream_refs": dream_refs if missing_fields else [],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_cross_file_logic(state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if state.get("schema_version") != "cross_file_logic_v0":
        reasons.append("cross_file_logic_gate schema mismatch")
    for field in [
        "cross_file_logic_id",
        "status",
        "state_refs",
        "cross_file_findings",
        "repair_priority_refs",
        "life_constraint_refs",
        "queue_e_cross_layer_gate_status",
        "queue_e_birth_repair_gate_status",
        "queue_e_birth_repair_profile_ref",
        "queue_e_birth_repair_pressure_level",
        "queue_e_birth_repair_attention_target",
        "queue_e_birth_repair_ref_set",
        "queue_e_world_contact_future_no_go_profile_ref",
        "queue_e_world_contact_confirmation_threshold_bias",
        "queue_e_world_contact_future_release_posture",
        "queue_e_world_contact_allowed_repair_routes",
        "queue_e_world_contact_repair_governance_refs",
        "prediction_periphery_gate_status",
        "prediction_periphery_ref_set",
        "closure_status_refs",
        "package_local_gate_refs",
        "bridge_refs",
        "source_doc_refs",
    ]:
        if not state.get(field):
            reasons.append(f"cross_file_logic_gate missing {field}")
    return reasons


def _has_blocking_life_constraint(gate_status: dict[str, Any]) -> bool:
    return any(
        status in {"missing", "blocked"}
        for key, status in gate_status.items()
        if key.endswith("_gate") and isinstance(status, str)
    )


def _dedupe_string_refs(refs: list[Any]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if not isinstance(ref, str) or not ref or ref in seen:
            continue
        seen.add(ref)
        merged.append(ref)
    return merged
