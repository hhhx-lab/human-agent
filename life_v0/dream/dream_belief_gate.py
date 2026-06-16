from __future__ import annotations

from typing import Any

DREAM_BELIEF_GATE_DECISION_REF = "runtime/state/dream/dream_belief_gate_decision.json"

SOURCE_DOC_REFS = [
    "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
    "docs/v0/entry/v0_dream_module_implementation_plan.md",
    "docs/real—live0/08_dream_sleep_offline_life.md",
]


def build_dream_belief_gate_decision(
    *,
    run_id: str,
    generated_at: str,
    dream_window: dict[str, Any] | None = None,
    wake_integration: dict[str, Any] | None = None,
) -> dict[str, Any]:
    dream_window = dream_window or {}
    wake_integration = wake_integration or {}
    scene_frames = list(dream_window.get("dream_scene_frames", []))
    allowed = [
        "BeliefLearningCandidate",
        "SelfNarrativePatchCandidate",
        "WakeQuestion",
    ]
    blocked = [
        "long_term_belief_overwrite_without_wake_evidence",
        "global_personality_overwrite_from_single_dream",
    ]
    decision_items = []
    for frame in scene_frames:
        if not isinstance(frame, dict):
            continue
        decision_items.append(
            {
                "scene_id": frame.get("scene_id"),
                "decision": "candidate_only",
                "allowed_writes": allowed,
                "blocked_writes": blocked,
                "dream_belief_boundary": "dream_may_propose_belief_candidate_not_overwrite",
            }
        )
    return {
        "schema_version": "dream_belief_gate_decision_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "DreamBeliefGateDecision",
        "status": "closed",
        "allowed_writes": allowed,
        "blocked_writes": blocked,
        "decision_items": decision_items,
        "dream_belief_boundary": "belief_changes_require_multi_cycle_wake_evidence",
        "wake_integration_ref": wake_integration.get("wake_integration_ref")
        or "runtime/state/dream/wake_integration_frame.json",
        "dream_belief_gate_decision_ref": DREAM_BELIEF_GATE_DECISION_REF,
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_dream_belief_gate_decision(payload: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if payload.get("schema_version") != "dream_belief_gate_decision_v1":
        reasons.append("dream_belief_gate schema mismatch")
    if "long_term_belief_overwrite_without_wake_evidence" not in payload.get(
        "blocked_writes", []
    ):
        reasons.append("dream_belief_gate missing blocked overwrite")
    return reasons