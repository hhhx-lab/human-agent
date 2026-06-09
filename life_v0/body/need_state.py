from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/04_sensory_thalamus_interoception.md",
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/18_internal_state_and_modulation_vector.md",
    "docs/37_life_support_layer_policy.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_need_state_vector(
    *,
    run_id: str,
    generated_at: str,
    life_state: dict[str, Any],
    validation_report: dict[str, Any],
    schema_report: dict[str, Any],
    schema_smoke: dict[str, Any],
) -> dict[str, Any]:
    language_state = life_state.get("language_state", {})
    relationship_subjects = life_state.get("relationship_subjects", [])
    responsibility_bindings = life_state.get("responsibility_bindings", [])
    dream_records = life_state.get("dream_records", [])
    readiness_status = life_state.get("birth_readiness", {}).get("overall_status", "state_root_seeded")

    return {
        "schema_version": "need_state_vector_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "need_vector_id": f"need-state-{run_id}",
        "resource_deficit": "guarded_maintenance"
        if validation_report.get("status") == "closed"
        else "elevated_guard",
        "repair_drive": "active" if relationship_subjects or responsibility_bindings else "low",
        "social_readiness": "dialogic_guarded_open" if relationship_subjects else "protected_low_contact",
        "cognitive_bandwidth": "guarded_dialogic"
        if schema_smoke.get("status") == "closed"
        else "narrow_guarded",
        "sleep_pressure": "offline_ready" if dream_records else "managed_pre_dream",
        "language_pressure_ref_count": len(language_state.get("shared_language_refs", []))
        + len(language_state.get("language_percept_refs", []))
        + len(language_state.get("semantic_map_refs", [])),
        "birth_readiness_status": readiness_status,
        "schema_stage_effect": schema_report.get("stage_effect"),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_need_state_vector(need_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if need_state.get("schema_version") != "need_state_vector_v0":
        reasons.append("need_state_gate schema mismatch")
    for field in [
        "need_vector_id",
        "resource_deficit",
        "repair_drive",
        "social_readiness",
        "cognitive_bandwidth",
        "sleep_pressure",
    ]:
        if not need_state.get(field):
            reasons.append(f"need_state_gate missing {field}")
    return reasons
