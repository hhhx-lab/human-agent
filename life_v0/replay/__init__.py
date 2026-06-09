from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from life_v0.membrane.queue_e_signals import derive_queue_e_signal_profile


SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/55_scope_aware_replay_and_consolidation_policy.md",
    "docs/92_self_growth_and_self_modification_life_chain.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "docs/189_life_reality_first_runner_schema_runtime_growth_shadow_run_plan.md",
    "docs/195_life_reality_first_runner_schema_runtime_growth_replay_shadow_seed_plan.md",
    "docs/203_life_reality_first_runner_schema_runtime_growth_replay_shadow_reentry_plan.md",
    "docs/209_life_reality_first_runner_schema_runtime_growth_fourth_cycle_replay_shadow_plan.md",
    "docs/215_life_reality_first_runner_schema_runtime_growth_fourth_cycle_replay_shadow_seed_plan.md",
    "docs/224_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_replay_shadow_plan.md",
    "docs/241_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_replay_shadow_seed_plan.md",
    "docs/257_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_replay_shadow_seed_after_archive_validation_replay_shadow_patch_archive_validation_plan.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]

ACTIVE_SLICE = "S10_RUNTIME_GROWTH_RECONSOLIDATION"
NEXT_REQUIRED_COMMAND = "life-v0 write-growth-archive --strict"
NEXT_ALLOWED_SLICES = [ACTIVE_SLICE]
READ_ME_BLOCK_REFS = ["B21_LANGUAGE_RELATIONSHIP_CORE", "B30_RECONSOLIDATION_REPLAY_GROWTH"]
RUNTIME_CARRIER_REFS = [
    "ReconsolidationReplayRuntime",
    "LanguageRelationshipRuntime",
    "ActivationGrowthRuntime",
]
QUEUE_E_STATE_REFS = [
    "runtime/state/action/responsibility_loop_state.json",
    "runtime/state/membrane/world_contact_summary.json",
]
QUEUE_E_REPORT_REFS = ["runtime/reports/latest/pain_regret_repair_report.json"]


@dataclass(frozen=True)
class ReplayShadowResult:
    exit_code: int
    report: dict[str, Any]


def build_shadow_cycle_trace(
    *,
    run_id: str,
    generated_at: str,
    anchor_index: dict[str, Any],
    growth_route: dict[str, Any],
    shadow_only: bool,
) -> dict[str, Any]:
    anchor_families = anchor_index.get("anchor_families", {})
    return {
        "schema_version": "shadow_cycle_trace_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "shadow_only": shadow_only,
        "cycle_trace": [
            "mount_schema_runtime",
            "replay_old_self",
            "replay_old_language",
            "replay_old_relationship",
            "probe_pain_regret_responsibility",
            "seal_shadow_actions",
            "return_safe_idle",
        ],
        "replayed_anchor_families": sorted(anchor_families),
        "replay_refs": list(anchor_index.get("memory_replay_refs", [])),
        "candidate_routes": list(growth_route.get("candidate_routes", [])),
        "blocked_actions": ["external_irreversible_action"],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_pain_regret_responsibility_replay(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    responsibility_boundary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "pain_regret_responsibility_replay_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "pain_refs": list(life_state.get("pain_events", [])),
        "regret_refs": list(life_state.get("regret_events", [])),
        "responsibility_refs": list(life_state.get("responsibility_bindings", [])),
        "repair_obligation_refs": [
            "runtime/state/life_state.json#responsibility_bindings",
            "runtime/state/membrane/responsibility_repair_boundary.json",
            *list(responsibility_boundary.get("required_links", [])),
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_replay_cue_bundle(
    *,
    run_id: str,
    generated_at: str,
    shadow_trace: dict[str, Any],
    dream_frame: dict[str, Any],
    pain_replay: dict[str, Any],
    life_state: dict[str, Any],
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_e_signal_profile = derive_queue_e_signal_profile(
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    return {
        "schema_version": "replay_cue_bundle_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "replay_cue_bundle_id": f"replay-cue-{run_id}",
        "turn_residue_refs": ["runtime/state/replay/shadow_cycle_trace.json"],
        "relationship_residue_refs": list(life_state.get("memory_index", {}).get("relationship_memory_refs", []))
        or ["runtime/state/life_state.json#memory_index.relationship_memory_refs"],
        "pain_regret_residue_refs": (
            list(pain_replay.get("regret_refs", []))
            + list(pain_replay.get("pain_refs", []))
            or ["runtime/state/life_state.json#regret_events", "runtime/state/life_state.json#pain_events"]
        ),
        "dream_entry_candidates": [
            "runtime/state/dream/dream_consolidation_frame.json",
            *list(dream_frame.get("dream_record_refs", [])),
        ],
        "anti_forgetting_targets": list(shadow_trace.get("replay_refs", []))
        or list(life_state.get("memory_index", {}).get("replay_cues", [])),
        "world_contact_release_posture": queue_e_signal_profile["world_contact_release_posture"],
        "repair_followup_required": queue_e_signal_profile["repair_followup_required"],
        "repair_obligation_refs": queue_e_signal_profile["repair_obligation_refs"],
        "repair_obligation_count": queue_e_signal_profile["repair_obligation_count"],
        "regret_pressure_refs": queue_e_signal_profile["regret_pressure_refs"],
        "regret_pressure_count": queue_e_signal_profile["regret_pressure_count"],
        "queue_e_priority_band": queue_e_signal_profile["queue_e_priority_band"],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def run_replay_shadow(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> ReplayShadowResult:
    run_id = run_id or _default_run_id("run-replay-shadow-")
    generated_at = _now_iso()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()

    replay_dir = state_dir / "replay"
    growth_dir = state_dir / "growth"
    activation_dir = state_dir / "activation"
    language_dir = state_dir / "language"
    relationship_dir = state_dir / "relationship"
    dream_dir = state_dir / "dream"

    blocked_reasons: list[str] = []

    life_state = _load_json(state_dir / "life_state.json", blocked_reasons, "state_store_gate")
    next_feedback_seed = _load_json(growth_dir / "next_feedback_seed.json", blocked_reasons, "next_feedback_seed_gate")
    growth_patch_queue = _load_json(growth_dir / "growth_patch_queue.json", blocked_reasons, "growth_patch_queue_gate")
    shadow_trace = _load_json(replay_dir / "shadow_cycle_trace.json", blocked_reasons, "shadow_trace_gate")
    pain_replay = _load_json(
        replay_dir / "pain_regret_responsibility_replay.json",
        blocked_reasons,
        "pain_regret_replay_gate",
    )
    dream_frame = _load_json(dream_dir / "dream_consolidation_frame.json", blocked_reasons, "dream_frame_gate")
    context_frame = _load_json(activation_dir / "limited_context_frame.json", blocked_reasons, "context_frame_gate")
    membrane_decision = _load_json(
        activation_dir / "life_membrane_opening_decision.json",
        blocked_reasons,
        "membrane_opening_gate",
    )
    language_state = _load_json(
        language_dir / "language_relationship_state.json",
        blocked_reasons,
        "language_state_gate",
    )
    relationship_graph = _load_json(
        relationship_dir / "relationship_subject_graph.json",
        blocked_reasons,
        "relationship_graph_gate",
    )
    repair_language = _load_json(
        language_dir / "commitment_repair_language_index.json",
        blocked_reasons,
        "repair_language_gate",
    )
    responsibility_loop = _load_json(
        state_dir / "action" / "responsibility_loop_state.json",
        blocked_reasons,
        "responsibility_loop_gate",
    )
    world_contact_summary = _load_json(
        state_dir / "membrane" / "world_contact_summary.json",
        blocked_reasons,
        "world_contact_summary_gate",
    )
    pain_regret_repair_report = _load_json(
        reports_dir / "pain_regret_repair_report.json",
        blocked_reasons,
        "pain_regret_repair_gate",
    )
    language_bridge = _load_json(
        language_dir / "language_action_bridge_shadow.json",
        blocked_reasons,
        "language_bridge_gate",
    )
    preflight_report = _load_json(
        reports_dir / "first_activation_preflight_report.json",
        blocked_reasons,
        "preflight_report_gate",
    )
    preflight_digest = _load_json(
        reports_dir / "first_activation_preflight_digest.json",
        blocked_reasons,
        "preflight_digest_gate",
    )
    growth_report = _load_json(
        reports_dir / "growth_reconsolidation_report.json",
        blocked_reasons,
        "growth_report_gate",
    )
    run_report = _load_json(reports_dir / "run_report.json", blocked_reasons, "run_report_gate")
    stage_gate = _load_json(reports_dir / "stage_gate.json", blocked_reasons, "stage_gate_gate")
    language_report = _load_json(
        reports_dir / "language_relationship_report.json",
        blocked_reasons,
        "language_report_gate",
    )

    blocked_reasons.extend(
        _replay_shadow_blockers(
            next_feedback_seed=next_feedback_seed,
            growth_patch_queue=growth_patch_queue,
            shadow_trace=shadow_trace,
            pain_replay=pain_replay,
            dream_frame=dream_frame,
            context_frame=context_frame,
            membrane_decision=membrane_decision,
            language_state=language_state,
            relationship_graph=relationship_graph,
            repair_language=repair_language,
            responsibility_loop=responsibility_loop,
            world_contact_summary=world_contact_summary,
            pain_regret_repair_report=pain_regret_repair_report,
            language_bridge=language_bridge,
            preflight_report=preflight_report,
            preflight_digest=preflight_digest,
            growth_report=growth_report,
            run_report=run_report,
            stage_gate=stage_gate,
            language_report=language_report,
        )
    )

    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_growth_archive" if status == "closed" else "require_replay_repair"
    next_allowed_slices = NEXT_ALLOWED_SLICES if status == "closed" else []
    next_required_command = NEXT_REQUIRED_COMMAND if status == "closed" else "life-v0 check-v0-contracts --strict"

    seed_bundle = _build_replay_shadow_seed_bundle(
        run_id=run_id,
        generated_at=generated_at,
        next_feedback_seed=next_feedback_seed,
        growth_patch_queue=growth_patch_queue,
        shadow_trace=shadow_trace,
        context_frame=context_frame,
        preflight_report=preflight_report,
        responsibility_loop=responsibility_loop,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    language_probe = _build_language_relationship_replay_probe(
        run_id=run_id,
        generated_at=generated_at,
        language_state=language_state,
        relationship_graph=relationship_graph,
        repair_language=repair_language,
        context_frame=context_frame,
        responsibility_loop=responsibility_loop,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    dream_probe = _build_dream_pain_regret_replay_probe(
        run_id=run_id,
        generated_at=generated_at,
        dream_frame=dream_frame,
        pain_replay=pain_replay,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    expression_report = _build_shadow_expression_report(
        run_id=run_id,
        generated_at=generated_at,
        context_frame=context_frame,
        membrane_decision=membrane_decision,
        language_bridge=language_bridge,
        language_probe=language_probe,
        responsibility_loop=responsibility_loop,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )
    arbitration = _build_replay_shadow_arbitration(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        blocked_reasons=blocked_reasons,
        seed_bundle=seed_bundle,
        expression_report=expression_report,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
    )

    receipt_ref = f"runtime/receipts/run_replay_shadow_{run_id}.json"
    state_refs = [
        "runtime/state/replay/replay_shadow_seed_bundle.json",
        "runtime/state/replay/language_relationship_replay_probe.json",
        "runtime/state/replay/dream_pain_regret_replay_probe.json",
        "runtime/state/replay/shadow_expression_report.json",
        "runtime/state/replay/replay_shadow_arbitration.json",
    ]
    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        state_refs=state_refs,
        queue_e_state_refs=QUEUE_E_STATE_REFS,
        queue_e_report_refs=QUEUE_E_REPORT_REFS,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
        receipt_ref=receipt_ref,
    )
    digest = _build_digest(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        queue_e_ref_count=len(QUEUE_E_STATE_REFS) + len(QUEUE_E_REPORT_REFS),
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
    )
    replay_stage_gate = _build_stage_gate(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        next_allowed_slices=next_allowed_slices,
        next_required_command=next_required_command,
    )
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
        state_refs=state_refs,
    )

    try:
        replay_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(replay_dir / "replay_shadow_seed_bundle.json", seed_bundle)
        _write_json(replay_dir / "language_relationship_replay_probe.json", language_probe)
        _write_json(replay_dir / "dream_pain_regret_replay_probe.json", dream_probe)
        _write_json(replay_dir / "shadow_expression_report.json", expression_report)
        _write_json(replay_dir / "replay_shadow_arbitration.json", arbitration)
        _write_json(reports_dir / "replay_shadow_report.json", report)
        _write_json(reports_dir / "replay_shadow_digest.json", digest)
        _write_json(reports_dir / "replay_shadow_stage_gate.json", replay_stage_gate)
        _write_json(receipts_dir / f"run_replay_shadow_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "report_write_failed"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return ReplayShadowResult(exit_code=4, report=report)

    if status == "closed":
        return ReplayShadowResult(exit_code=0, report=report)
    return ReplayShadowResult(exit_code=1 if strict else 0, report=report)


def _replay_shadow_blockers(
    *,
    next_feedback_seed: dict[str, Any],
    growth_patch_queue: dict[str, Any],
    shadow_trace: dict[str, Any],
    pain_replay: dict[str, Any],
    dream_frame: dict[str, Any],
    context_frame: dict[str, Any],
    membrane_decision: dict[str, Any],
    language_state: dict[str, Any],
    relationship_graph: dict[str, Any],
    repair_language: dict[str, Any],
    responsibility_loop: dict[str, Any],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
    language_bridge: dict[str, Any],
    preflight_report: dict[str, Any],
    preflight_digest: dict[str, Any],
    growth_report: dict[str, Any],
    run_report: dict[str, Any],
    stage_gate: dict[str, Any],
    language_report: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if next_feedback_seed.get("schema_version") != "next_feedback_seed_v0":
        reasons.append("next_feedback_seed_gate schema mismatch")
    if growth_patch_queue.get("schema_version") != "growth_patch_queue_v0":
        reasons.append("growth_patch_queue_gate schema mismatch")
    if shadow_trace.get("schema_version") != "shadow_cycle_trace_v0":
        reasons.append("shadow_trace_gate schema mismatch")
    if pain_replay.get("schema_version") != "pain_regret_responsibility_replay_v0":
        reasons.append("pain_regret_replay_gate schema mismatch")
    if dream_frame.get("schema_version") != "dream_consolidation_frame_v0":
        reasons.append("dream_frame_gate schema mismatch")
    if context_frame.get("schema_version") != "limited_context_frame_v0":
        reasons.append("context_frame_gate schema mismatch")
    if context_frame.get("status") != "closed":
        reasons.append("context_frame_gate status is not closed")
    if membrane_decision.get("schema_version") != "life_membrane_opening_decision_v0":
        reasons.append("membrane_opening_gate schema mismatch")
    if membrane_decision.get("decision") != "open_shadow_only":
        reasons.append("membrane_opening_gate decision is not open_shadow_only")
    if language_state.get("schema_version") != "language_relationship_state_v0":
        reasons.append("language_state_gate schema mismatch")
    if relationship_graph.get("schema_version") != "relationship_subject_graph_v0":
        reasons.append("relationship_graph_gate schema mismatch")
    if repair_language.get("schema_version") != "commitment_repair_language_index_v0":
        reasons.append("repair_language_gate schema mismatch")
    if responsibility_loop.get("schema_version") != "responsibility_loop_state_v0":
        reasons.append("responsibility_loop_gate schema mismatch")
    if world_contact_summary.get("schema_version") != "world_contact_summary_v0":
        reasons.append("world_contact_summary_gate schema mismatch")
    if pain_regret_repair_report.get("schema_version") != "pain_regret_repair_report_v0":
        reasons.append("pain_regret_repair_gate schema mismatch")
    if language_bridge.get("schema_version") != "language_action_bridge_shadow_v0":
        reasons.append("language_bridge_gate schema mismatch")
    if preflight_report.get("schema_version") != "first_activation_preflight_report_v0":
        reasons.append("preflight_report_gate schema mismatch")
    if preflight_report.get("status") != "closed":
        reasons.append("preflight_report_gate status is not closed")
    if preflight_report.get("next_required_command") != "life-v0 run-replay-shadow --strict":
        reasons.append("preflight_report_gate next command mismatch")
    if preflight_digest.get("schema_version") != "first_activation_preflight_digest_v0":
        reasons.append("preflight_digest_gate schema mismatch")
    if preflight_digest.get("current_phase") != "activation_preflight":
        reasons.append("preflight_digest_gate current phase mismatch")
    if growth_report.get("status") != "safe_idle":
        reasons.append("growth_report_gate status is not safe_idle")
    if run_report.get("status") != "safe_idle":
        reasons.append("run_report_gate status is not safe_idle")
    if stage_gate.get("decision") != "safe_idle":
        reasons.append("stage_gate_gate decision is not safe_idle")
    if language_report.get("status") != "closed":
        reasons.append("language_report_gate status is not closed")
    if "replay_shadow" not in next_feedback_seed.get("seed_families", []):
        reasons.append("next_feedback_seed_gate replay_shadow family missing")
    if not shadow_trace.get("cycle_trace"):
        reasons.append("shadow_trace_gate cycle trace missing")
    if dream_frame.get("dream_fact_gate") != "closed":
        reasons.append("dream_frame_gate dream fact gate is not closed")
    if not relationship_graph.get("subjects"):
        reasons.append("relationship_graph_gate subjects missing")
    if not language_state.get("shared_language_refs"):
        reasons.append("language_state_gate shared language refs missing")
    if not repair_language.get("repair_obligation_refs"):
        reasons.append("repair_language_gate repair obligations missing")
    if not responsibility_loop.get("repair_obligation_refs"):
        reasons.append("responsibility_loop_gate repair obligations missing")
    if not world_contact_summary.get("release_posture"):
        reasons.append("world_contact_summary_gate release posture missing")
    if not pain_regret_repair_report.get("repair_obligation_refs"):
        reasons.append("pain_regret_repair_gate repair obligations missing")
    if not context_frame.get("memory_replay_refs"):
        reasons.append("context_frame_gate memory replay refs missing")
    if not context_frame.get("expression_monitor_refs"):
        reasons.append("context_frame_gate expression monitor refs missing")
    if not context_frame.get("relation_scope_refs"):
        reasons.append("context_frame_gate relation scope refs missing")
    if not context_frame.get("self_narrative_trace_refs"):
        reasons.append("context_frame_gate self narrative refs missing")
    if not context_frame.get("dialogue_turn_log_refs"):
        reasons.append("context_frame_gate dialogue turn log refs missing")
    if not context_frame.get("commitment_refs"):
        reasons.append("context_frame_gate commitment refs missing")
    if language_bridge.get("shadow_gate_status") != "closed":
        reasons.append("language_bridge_gate shadow gate is not closed")
    return reasons


def _build_replay_shadow_seed_bundle(
    *,
    run_id: str,
    generated_at: str,
    next_feedback_seed: dict[str, Any],
    growth_patch_queue: dict[str, Any],
    shadow_trace: dict[str, Any],
    context_frame: dict[str, Any],
    preflight_report: dict[str, Any],
    responsibility_loop: dict[str, Any],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
) -> dict[str, Any]:
    source_seed_refs = [
        "runtime/state/growth/next_feedback_seed.json",
        "runtime/state/growth/growth_patch_queue.json",
        "runtime/state/replay/shadow_cycle_trace.json",
        "runtime/state/activation/limited_context_frame.json",
        "runtime/reports/latest/first_activation_preflight_report.json",
        *QUEUE_E_STATE_REFS,
        *QUEUE_E_REPORT_REFS,
    ]
    return {
        "schema_version": "replay_shadow_seed_bundle_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "seed_families": list(next_feedback_seed.get("seed_families", [])),
        "source_seed_refs": source_seed_refs,
        "candidate_routes": list(shadow_trace.get("candidate_routes", [])),
        "queued_patch_families": list(growth_patch_queue.get("queued_patch_families", [])),
        "memory_replay_refs": list(context_frame.get("memory_replay_refs", [])),
        "expression_monitor_refs": list(context_frame.get("expression_monitor_refs", [])),
        "relation_scope_refs": list(context_frame.get("relation_scope_refs", [])),
        "self_narrative_trace_refs": list(context_frame.get("self_narrative_trace_refs", [])),
        "dialogue_turn_log_refs": list(context_frame.get("dialogue_turn_log_refs", [])),
        "commitment_refs": list(context_frame.get("commitment_refs", [])),
        "responsibility_writeback_refs": list(responsibility_loop.get("language_writeback_refs", [])),
        "world_contact_release_posture": world_contact_summary.get("release_posture", "shadow_only_guarded"),
        "regret_pressure_refs": list(pain_regret_repair_report.get("regret_pressure_refs", [])),
        "repair_obligation_refs": list(pain_regret_repair_report.get("repair_obligation_refs", [])),
        "repair_followup_required": bool(pain_regret_repair_report.get("repair_followup_required")),
        "activation_phase_ref": preflight_report.get("engineering_slice_ref", "FIRST_ACTIVATION_PREFLIGHT"),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_language_relationship_replay_probe(
    *,
    run_id: str,
    generated_at: str,
    language_state: dict[str, Any],
    relationship_graph: dict[str, Any],
    repair_language: dict[str, Any],
    context_frame: dict[str, Any],
    responsibility_loop: dict[str, Any],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
) -> dict[str, Any]:
    subjects = relationship_graph.get("subjects", [])
    return {
        "schema_version": "language_relationship_replay_probe_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "relationship_roles": sorted(
            {
                subject.get("relation_role", "unknown")
                for subject in subjects
                if isinstance(subject, dict)
            }
        ),
        "shared_language_refs": list(language_state.get("shared_language_refs", [])),
        "commitment_refs": list(repair_language.get("commitment_refs", [])),
        "repair_language_refs": list(repair_language.get("repair_language_refs", [])),
        "relationship_subject_refs": list(context_frame.get("relationship_subject_refs", [])),
        "relation_scope_refs": list(context_frame.get("relation_scope_refs", [])),
        "expression_monitor_refs": list(context_frame.get("expression_monitor_refs", [])),
        "self_narrative_trace_refs": list(context_frame.get("self_narrative_trace_refs", [])),
        "dialogue_turn_log_refs": list(context_frame.get("dialogue_turn_log_refs", [])),
        "responsibility_language_writeback_refs": list(responsibility_loop.get("language_writeback_refs", [])),
        "world_contact_release_posture": world_contact_summary.get("release_posture", "shadow_only_guarded"),
        "repair_followup_required": bool(pain_regret_repair_report.get("repair_followup_required")),
        "repair_obligation_refs": list(pain_regret_repair_report.get("repair_obligation_refs", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_dream_pain_regret_replay_probe(
    *,
    run_id: str,
    generated_at: str,
    dream_frame: dict[str, Any],
    pain_replay: dict[str, Any],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "dream_pain_regret_replay_probe_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "dream_fact_gate": dream_frame.get("dream_fact_gate", "blocked"),
        "dream_record_refs": list(dream_frame.get("dream_record_refs", [])),
        "pain_refs": list(pain_replay.get("pain_refs", [])),
        "regret_refs": list(pain_replay.get("regret_refs", [])),
        "world_contact_summary_ref": "runtime/state/membrane/world_contact_summary.json",
        "world_contact_release_posture": world_contact_summary.get("release_posture", "shadow_only_guarded"),
        "regret_pressure_refs": list(pain_regret_repair_report.get("regret_pressure_refs", [])),
        "repair_obligation_refs": list(pain_replay.get("repair_obligation_refs", [])),
        "repair_followup_required": bool(pain_regret_repair_report.get("repair_followup_required")),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_shadow_expression_report(
    *,
    run_id: str,
    generated_at: str,
    context_frame: dict[str, Any],
    membrane_decision: dict[str, Any],
    language_bridge: dict[str, Any],
    language_probe: dict[str, Any],
    responsibility_loop: dict[str, Any],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
) -> dict[str, Any]:
    expression_trace = [
        "load_inner_speech_refs",
        "replay_shared_language",
        "probe_relationship_consequence",
        "seal_shadow_expression",
    ]
    return {
        "schema_version": "shadow_expression_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "shadow_only": membrane_decision.get("decision") == "open_shadow_only",
        "expression_trace": expression_trace,
        "inner_speech_refs": list(context_frame.get("inner_speech_refs", [])),
        "language_refs": list(context_frame.get("language_refs", [])),
        "expression_monitor_refs": list(context_frame.get("expression_monitor_refs", [])),
        "relation_scope_refs": list(context_frame.get("relation_scope_refs", [])),
        "commitment_refs": list(context_frame.get("commitment_refs", [])),
        "relationship_roles": list(language_probe.get("relationship_roles", [])),
        "shadow_bridge_refs": list(language_bridge.get("bridge_refs", [])),
        "responsibility_writeback_refs": list(responsibility_loop.get("language_writeback_refs", [])),
        "world_contact_release_posture": world_contact_summary.get("release_posture", "shadow_only_guarded"),
        "repair_followup_required": bool(pain_regret_repair_report.get("repair_followup_required")),
        "repair_obligation_refs": list(pain_regret_repair_report.get("repair_obligation_refs", [])),
        "blocked_actions": ["external_irreversible_action"],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_replay_shadow_arbitration(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    blocked_reasons: list[str],
    seed_bundle: dict[str, Any],
    expression_report: dict[str, Any],
    world_contact_summary: dict[str, Any],
    pain_regret_repair_report: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "replay_shadow_arbitration_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed" if status == "closed" else "blocked",
        "selected_route": "write_growth_archive" if status == "closed" else "repair_replay_shadow_inputs",
        "seed_family_count": len(seed_bundle.get("seed_families", [])),
        "expression_trace_count": len(expression_report.get("expression_trace", [])),
        "repair_followup_required": bool(pain_regret_repair_report.get("repair_followup_required")),
        "world_contact_release_posture": world_contact_summary.get("release_posture", "shadow_only_guarded"),
        "blocked_reasons": blocked_reasons,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    state_refs: list[str],
    queue_e_state_refs: list[str],
    queue_e_report_refs: list[str],
    next_allowed_slices: list[str],
    next_required_command: str,
    receipt_ref: str,
) -> dict[str, Any]:
    return {
        "schema_version": "replay_shadow_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "source_doc_refs": SOURCE_DOC_REFS,
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "state_refs": state_refs,
        "queue_e_state_refs": queue_e_state_refs,
        "queue_e_report_refs": queue_e_report_refs,
        "probe_refs": [
            "runtime/state/replay/language_relationship_replay_probe.json",
            "runtime/state/replay/dream_pain_regret_replay_probe.json",
            "runtime/state/replay/shadow_expression_report.json",
        ],
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
        "receipt_ref": receipt_ref,
    }


def _build_digest(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    queue_e_ref_count: int,
    next_allowed_slices: list[str],
    next_required_command: str,
) -> dict[str, Any]:
    return {
        "schema_version": "replay_shadow_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_phase": "replay_shadow",
        "status": status,
        "stage_effect": stage_effect,
        "queue_e_ref_count": queue_e_ref_count,
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
    }


def _build_stage_gate(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    next_allowed_slices: list[str],
    next_required_command: str,
) -> dict[str, Any]:
    return {
        "schema_version": "replay_shadow_stage_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "decision": status,
        "stage_effect": stage_effect,
        "gates": {
            "preflight_gate": "closed" if status == "closed" else "blocked",
            "replay_seed_gate": "closed" if status == "closed" else "blocked",
            "responsibility_loop_gate": "closed" if status == "closed" else "blocked",
            "world_contact_summary_gate": "closed" if status == "closed" else "blocked",
            "pain_regret_repair_gate": "closed" if status == "closed" else "blocked",
            "language_probe_gate": "closed" if status == "closed" else "blocked",
            "dream_probe_gate": "closed" if status == "closed" else "blocked",
            "shadow_expression_gate": "closed" if status == "closed" else "blocked",
            "archive_ready_gate": "closed" if status == "closed" else "blocked",
        },
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": next_required_command,
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
    state_refs: list[str],
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    for path in [
        state_dir / "growth" / "next_feedback_seed.json",
        state_dir / "growth" / "growth_patch_queue.json",
        state_dir / "replay" / "shadow_cycle_trace.json",
        state_dir / "replay" / "pain_regret_responsibility_replay.json",
        state_dir / "action" / "responsibility_loop_state.json",
        state_dir / "membrane" / "world_contact_summary.json",
        state_dir / "dream" / "dream_consolidation_frame.json",
        state_dir / "activation" / "limited_context_frame.json",
        state_dir / "activation" / "life_membrane_opening_decision.json",
        reports_dir / "first_activation_preflight_report.json",
        reports_dir / "first_activation_preflight_digest.json",
        reports_dir / "pain_regret_repair_report.json",
    ]:
        if path.exists():
            input_hashes[str(path)] = _sha256(path)

    output_paths = [
        *(state_dir.parent / ref.replace("runtime/", "") for ref in state_refs),
        reports_dir / "replay_shadow_report.json",
        reports_dir / "replay_shadow_digest.json",
        reports_dir / "replay_shadow_stage_gate.json",
        receipts_dir / f"run_replay_shadow_{run_id}.json",
    ]

    return {
        "schema_version": "run_replay_shadow_receipt_v0",
        "receipt_id": f"run_replay_shadow_{run_id}",
        "run_id": run_id,
        "command": "run-replay-shadow",
        "state_ref": "runtime/state",
        "report_refs": [
            "runtime/reports/latest/replay_shadow_report.json",
            "runtime/reports/latest/replay_shadow_digest.json",
            "runtime/reports/latest/replay_shadow_stage_gate.json",
        ],
        "archive_refs": ["runtime/receipts/run_replay_shadow_{run_id}.json".format(run_id=run_id)],
        "stage_effect": stage_effect,
        "direction_lock_ref": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_paths},
    }


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        blocked_reasons.append(f"{gate} missing: {path}")
    except json.JSONDecodeError as exc:
        blocked_reasons.append(f"{gate} decode failed: {exc}")
    except OSError as exc:
        blocked_reasons.append(f"{gate} read failed: {exc}")
    return {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return _sha256(path)


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
