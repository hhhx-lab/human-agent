from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    "docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]


def build_dream_fact_gate_decision(
    *,
    run_id: str,
    generated_at: str,
    dream_window: dict[str, Any],
    wake_integration: dict[str, Any],
    offline_entry: dict[str, Any],
) -> dict[str, Any]:
    source_trace_refs = list(dream_window.get("source_trace_refs", []))
    relationship_candidates = list(wake_integration.get("relationship_repair_candidates", []))
    narrative_candidates = list(wake_integration.get("narrative_writeback_candidates", []))

    decision_items = [
        {
            "decision_id": f"dream-fact-decision-{run_id}-scene",
            "candidate_ref": dream_window.get("dream_scene_frames", [{}])[0].get("scene_id", f"dream-scene-{run_id}"),
            "source_evidence_refs": source_trace_refs[:2],
            "conflict_refs": ["dream_generated_content_requires_wake_review"],
            "scope_result": "guarded",
            "state_bias_result": "offline_bias_bounded",
            "decision": "keep_as_dream_residue",
            "required_wake_probe": ["probe_dream_reportability"],
        }
    ]
    if relationship_candidates or narrative_candidates:
        decision_items.append(
            {
                "decision_id": f"dream-fact-decision-{run_id}-repair",
                "candidate_ref": (relationship_candidates + narrative_candidates)[0],
                "source_evidence_refs": source_trace_refs[:2],
                "conflict_refs": [],
                "scope_result": "relationship_guarded",
                "state_bias_result": "repair_bias_allowed_with_wake_review",
                "decision": "route_to_repair_review",
                "required_wake_probe": ["probe_repair_followup"],
            }
        )

    return {
        "schema_version": "dream_fact_gate_decision_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "DreamFactGateDecision",
        "fact_gate_id": f"dream-fact-gate-{run_id}",
        "wake_integration_ref": "runtime/state/dream/wake_integration_frame.json",
        "offline_entry_ref": "runtime/state/dream/offline_entry_gate.json",
        "offline_entry_mode_refs": list(offline_entry.get("offline_modes", [])),
        "decision_items": decision_items,
        "allowed_writes": [
            "DreamResidue",
            "SelfNarrativePatchCandidate",
            "RepairCommitmentCandidate",
            "WakeQuestion",
        ],
        "blocked_writes": [
            "direct_fact_memory",
            "relationship_state_overwrite",
            "external_action_commitment_without_wake_review",
        ],
        "gate_result": "passed",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_dream_fact_gate_decision(decision: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if decision.get("schema_version") != "dream_fact_gate_decision_v0":
        reasons.append("dream_fact_gate schema mismatch")
    if decision.get("object_kind") != "DreamFactGateDecision":
        reasons.append("dream_fact_gate object kind mismatch")
    if decision.get("gate_result") not in {"passed", "partial", "blocked", "quarantine"}:
        reasons.append("dream_fact_gate result mismatch")
    for field in ["fact_gate_id", "wake_integration_ref", "decision_items", "allowed_writes", "blocked_writes"]:
        if not decision.get(field):
            reasons.append(f"dream_fact_gate missing {field}")
    return reasons
