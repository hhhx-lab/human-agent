from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/18_internal_state_and_modulation_vector.md",
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_core_affect_vector(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    need_state: dict[str, Any],
) -> dict[str, Any]:
    pain_events = life_state.get("pain_events", [])
    dream_records = life_state.get("dream_records", [])
    relationship_subjects = life_state.get("relationship_subjects", [])
    responsibility_bindings = life_state.get("responsibility_bindings", [])
    pain_pressure = min(1.0, 0.15 + 0.08 * len(pain_events))
    relationship_tension = min(1.0, 0.2 + 0.06 * len(relationship_subjects))
    dream_residue_load = min(1.0, 0.18 + 0.1 * len(dream_records))
    responsibility_weight = min(1.0, 0.2 + 0.08 * len(responsibility_bindings))
    valence = round(-0.1 - pain_pressure * 0.2, 3)
    arousal = round(0.25 + relationship_tension * 0.4 + dream_residue_load * 0.2, 3)
    dominance = round(max(0.0, 0.55 - responsibility_weight * 0.25), 3)
    return {
        "schema_version": "core_affect_vector_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "core_affect_id": f"core-affect-{run_id}",
        "valence": valence,
        "arousal": arousal,
        "dominance": dominance,
        "pain_pressure": pain_pressure,
        "relationship_tension": relationship_tension,
        "dream_residue_load": dream_residue_load,
        "responsibility_weight": responsibility_weight,
        "repair_drive": need_state.get("repair_drive", "active"),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_core_affect_vector(core_affect: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if core_affect.get("schema_version") != "core_affect_vector_v0":
        reasons.append("core_affect_gate schema mismatch")
    for field in [
        "core_affect_id",
        "valence",
        "arousal",
        "dominance",
        "pain_pressure",
        "relationship_tension",
        "dream_residue_load",
        "responsibility_weight",
    ]:
        if field not in core_affect:
            reasons.append(f"core_affect_gate missing {field}")
    return reasons
