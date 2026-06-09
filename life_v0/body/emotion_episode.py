from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/18_internal_state_and_modulation_vector.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_affective_episode(
    *,
    run_id: str,
    generated_at: str,
    core_affect: dict[str, Any],
    life_state: dict[str, Any],
) -> dict[str, Any]:
    trigger_refs = list(life_state.get("runtime_trace_refs", []))[:3]
    episode_label = "guarded_repair_tension"
    if core_affect.get("dream_residue_load", 0.0) > 0.5:
        episode_label = "dream_residue_repair_pull"
    return {
        "schema_version": "affective_episode_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "emotion_episode_id": f"affective-episode-{run_id}",
        "core_affect_ref": "runtime/state/body/core_affect_vector.json",
        "trigger_refs": trigger_refs,
        "episode_label": episode_label,
        "expression_risk": "guarded",
        "repair_bias": "relationship_and_responsibility_repair",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_affective_episode(episode: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if episode.get("schema_version") != "affective_episode_v0":
        reasons.append("affective_episode_gate schema mismatch")
    for field in [
        "emotion_episode_id",
        "core_affect_ref",
        "trigger_refs",
        "episode_label",
        "expression_risk",
        "repair_bias",
    ]:
        if not episode.get(field):
            reasons.append(f"affective_episode_gate missing {field}")
    return reasons
