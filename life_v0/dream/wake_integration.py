from __future__ import annotations

from typing import Any

from life_v0.membrane.queue_e_signals import (
    queue_e_repair_modulation_profile_from_replay_cue_bundle,
)


SOURCE_DOC_REFS = [
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/95_dream_reality_and_offline_life_timeline.md",
    "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
    "docs/real—live0/02_brain_network_and_workspace.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
]


def build_wake_integration_frame(
    *,
    run_id: str,
    generated_at: str,
    dream_window: dict[str, Any],
    replay_cue_bundle: dict[str, Any],
    workspace_frame: dict[str, Any] | None = None,
    broadcast_frame: dict[str, Any] | None = None,
    metacognition_state: dict[str, Any] | None = None,
    consciousness_probe_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    relationship_candidates = list(dream_window.get("relationship_simulation_refs", []))
    repair_profile = queue_e_repair_modulation_profile_from_replay_cue_bundle(
        replay_cue_bundle
    )
    repair_refs = list(repair_profile.get("ref_set", []))
    consciousness_reentry_profile = _consciousness_reentry_profile(
        workspace_frame=workspace_frame or {},
        broadcast_frame=broadcast_frame or {},
        metacognition_state=metacognition_state or {},
        consciousness_probe_bundle=consciousness_probe_bundle or {},
    )
    return {
        "schema_version": "wake_integration_frame_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "object_kind": "WakeIntegrationFrame",
        "wake_integration_id": f"wake-integration-{run_id}",
        "dream_window_ref": "runtime/state/dream/dream_experience_window.json",
        "life_state_targets": [
            "runtime/state/life_state.json#dream_records",
            "runtime/state/life_state.json#memory_index.replay_cues",
        ],
        "core_affect_targets": ["runtime/state/body/core_affect_vector.json"],
        "growth_seed_refs": list(replay_cue_bundle.get("anti_forgetting_targets", [])),
        "dream_fact_gate_ref": "runtime/state/membrane/dream_fact_boundary.json",
        "narrative_writeback_candidates": list(dream_window.get("source_trace_refs", []))[:3],
        "relationship_repair_candidates": relationship_candidates,
        "consciousness_reentry_profile": consciousness_reentry_profile,
        "consciousness_reentry_refs": list(
            consciousness_reentry_profile.get("ref_set", [])
        ),
        "workspace_reentry_targets": [
            "runtime/state/consciousness/workspace_frame.json#candidate_explanations",
            "runtime/state/consciousness/broadcast_frame.json#broadcast_targets",
            "runtime/state/consciousness/metacognition_state.json#reflection_prompts",
        ],
        "queue_e_repair_modulation_profile": repair_profile,
        "queue_e_repair_pressure_level": repair_profile["pressure_level"],
        "queue_e_repair_attention_target": repair_profile["attention_target"],
        "queue_e_repair_ref_set": repair_refs,
        "repair_modulated_wake_targets": [
            "runtime/state/life_state.json#regret_events",
            "runtime/state/life_state.json#relationship_subjects",
            "runtime/state/growth/relationship_learning_plan.json",
        ]
        if repair_profile["pressure_level"] in {"urgent", "elevated"}
        else [],
        "action_candidate_after_wake": ["defer_until_membrane_review"],
        "archive_requirement": "required_before_activation",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _consciousness_reentry_profile(
    *,
    workspace_frame: dict[str, Any],
    broadcast_frame: dict[str, Any],
    metacognition_state: dict[str, Any],
    consciousness_probe_bundle: dict[str, Any],
) -> dict[str, Any]:
    workspace_ref = (
        "runtime/state/consciousness/workspace_frame.json" if workspace_frame else None
    )
    broadcast_ref = (
        "runtime/state/consciousness/broadcast_frame.json" if broadcast_frame else None
    )
    metacognition_ref = (
        "runtime/state/consciousness/metacognition_state.json"
        if metacognition_state
        else None
    )
    probe_ref = (
        "runtime/state/consciousness/consciousness_probe_bundle.json"
        if consciousness_probe_bundle
        else None
    )
    return {
        "schema_version": "wake_consciousness_reentry_profile_v0",
        "workspace_frame_ref": workspace_ref,
        "broadcast_frame_ref": broadcast_ref,
        "metacognition_ref": metacognition_ref,
        "consciousness_probe_ref": probe_ref,
        "workspace_candidate_count": len(
            workspace_frame.get("candidate_explanations", [])
        ),
        "broadcast_target_count": len(broadcast_frame.get("broadcast_targets", [])),
        "metacognition_reflection_count": len(
            metacognition_state.get("reflection_prompts", [])
        ),
        "reportability_flags": list(
            consciousness_probe_bundle.get("reportability_flags", [])
        ),
        "ref_set": [
            ref for ref in [workspace_ref, broadcast_ref, metacognition_ref, probe_ref] if ref
        ],
        "boundary": "wake_consciousness_reentry_not_spoken_language",
    }


def check_wake_integration_frame(wake_integration: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if wake_integration.get("schema_version") != "wake_integration_frame_v0":
        reasons.append("wake_integration_gate schema mismatch")
    for field in [
        "wake_integration_id",
        "dream_window_ref",
        "life_state_targets",
        "core_affect_targets",
        "growth_seed_refs",
        "dream_fact_gate_ref",
        "consciousness_reentry_profile",
        "consciousness_reentry_refs",
        "workspace_reentry_targets",
        "archive_requirement",
    ]:
        if not wake_integration.get(field):
            reasons.append(f"wake_integration_gate missing {field}")
    if "docs/real—live0/02_brain_network_and_workspace.md" not in wake_integration.get("source_doc_refs", []):
        reasons.append("wake_integration_gate missing workspace mechanism doc")
    return reasons
