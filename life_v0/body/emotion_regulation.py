from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/07_emotion_personality_self.md",
    "docs/39_development_policy_and_plasticity_windows.md",
    "docs/94_pain_regret_and_repair_signal_schema.md",
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
]


def build_emotion_regulation_loop(
    *,
    run_id: str,
    generated_at: str,
    episode: dict[str, Any],
    recovery_path: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "emotion_regulation_loop_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "emotion_regulation_id": f"emotion-regulation-{run_id}",
        "episode_ref": "runtime/state/body/affective_episode.json",
        "regulation_mode": "hold_then_articulate",
        "suppression_cost": 0.18,
        "expression_delay_required": episode.get("expression_risk") == "guarded",
        "recovery_route_refs": ["runtime/state/body/recovery_path.json"],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_emotion_regulation_loop(regulation: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if regulation.get("schema_version") != "emotion_regulation_loop_v0":
        reasons.append("emotion_regulation_gate schema mismatch")
    for field in [
        "emotion_regulation_id",
        "episode_ref",
        "regulation_mode",
        "suppression_cost",
        "recovery_route_refs",
    ]:
        if field not in regulation or regulation.get(field) in ("", []):
            reasons.append(f"emotion_regulation_gate missing {field}")
    return reasons
