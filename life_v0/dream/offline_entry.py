from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    "docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]


def build_offline_entry_gate(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
    pain_replay: dict[str, Any],
) -> dict[str, Any]:
    dream_records = list(life_state.get("dream_records", []))
    turn_residue_refs = list(replay_cue_bundle.get("turn_residue_refs", []))
    relationship_residue_refs = list(replay_cue_bundle.get("relationship_residue_refs", []))
    anti_forgetting_targets = list(replay_cue_bundle.get("anti_forgetting_targets", []))
    repair_obligation_refs = list(pain_replay.get("repair_obligation_refs", []))

    offline_modes = ["NREMReplayCycle"]
    if relationship_residue_refs or repair_obligation_refs:
        offline_modes.append("REMDreamGeneration")
    if turn_residue_refs or dream_records:
        offline_modes.append("DefaultDriftMode")
    if anti_forgetting_targets or repair_obligation_refs:
        offline_modes.append("FatigueRecoveryMode")

    return {
        "schema_version": "offline_entry_gate_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "OfflineEntryGate",
        "offline_entry_id": f"offline-entry-{run_id}",
        "status": "opened_internal_only",
        "entry_decision": "offline_allowed",
        "entry_pressure": {
            "sleep_pressure": len(dream_records) + len(replay_cue_bundle.get("dream_entry_candidates", [])),
            "maintenance_pressure": len(turn_residue_refs),
            "relationship_pressure": len(relationship_residue_refs),
            "pain_regret_pressure": len(repair_obligation_refs),
            "growth_debt": len(anti_forgetting_targets),
        },
        "offline_modes": offline_modes,
        "dream_window_kind": "repair_weighted_dream_window"
        if relationship_residue_refs or repair_obligation_refs
        else "micro_replay_window",
        "allowed_internal_operations": [
            "memory_consolidation",
            "counterfactual_dreaming",
            "relationship_repair_simulation",
            "anti_forgetting_replay",
        ],
        "external_action_policy": "blocked",
        "blocked_external_operations": [
            "tool_action",
            "relationship_state_overwrite",
            "external_commitment",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_offline_entry_gate(offline_entry: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if offline_entry.get("schema_version") != "offline_entry_gate_v0":
        reasons.append("offline_entry_gate schema mismatch")
    if offline_entry.get("entry_decision") != "offline_allowed":
        reasons.append("offline_entry_gate decision mismatch")
    if offline_entry.get("external_action_policy") != "blocked":
        reasons.append("offline_entry_gate external action policy mismatch")
    for field in [
        "offline_entry_id",
        "entry_pressure",
        "offline_modes",
        "allowed_internal_operations",
    ]:
        if not offline_entry.get(field):
            reasons.append(f"offline_entry_gate missing {field}")
    return reasons
