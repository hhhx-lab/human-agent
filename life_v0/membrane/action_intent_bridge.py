from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/06_action_reward_inhibition.md",
    "docs/09_language_symbolic_top_layer.md",
    "docs/20_agent_runtime_bridge_contract.md",
    "docs/144_life_reality_language_runtime_action_bridge_fixture_plan.md",
    "docs/147_life_reality_language_action_bridge_schema_materialization_plan.md",
    "docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md",
]


def build_action_intent_queue(
    *,
    run_id: str,
    generated_at: str,
    action_candidate_set: dict[str, Any],
    expression_plan: dict[str, Any],
    relation_turn_frame: dict[str, Any],
    shadow_action_gate: dict[str, Any],
) -> dict[str, Any]:
    semantic_goal = expression_plan.get("semantic_goal") or "continuity_hold"
    relation_role = relation_turn_frame.get("relation_role") or "relationship_subject"
    action_intents: list[dict[str, Any]] = []
    for index, candidate in enumerate(action_candidate_set.get("candidate_actions", []), start=1):
        world_contact_mode = candidate.get("world_contact_mode", "shadow_only")
        side_effect_level = _side_effect_level(world_contact_mode)
        action_intents.append(
            {
                "action_intent_id": f"action-intent-{run_id}-{index:04d}",
                "action_candidate_ref": "runtime/state/action/action_candidate_set.json",
                "action_kind": candidate.get("action_kind", "shadow_hold"),
                "semantic_goal": candidate.get("semantic_goal", semantic_goal),
                "relation_scope_ref": "runtime/state/terminal/relation_turn_frame.json",
                "relation_role": relation_role,
                "language_origin_ref": "runtime/state/language/expression_plan.json",
                "world_contact_mode": world_contact_mode,
                "side_effect_level": side_effect_level,
                "requires_confirmation": side_effect_level == "external_irreversible"
                and world_contact_mode == "external_release",
                "responsibility_projection": list(action_candidate_set.get("responsibility_projection", [])),
                "blocked_action_classes": list(shadow_action_gate.get("blocked_action_classes", [])),
                "source_doc_refs": SOURCE_DOC_REFS,
            }
        )

    return {
        "schema_version": "action_intent_queue_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "action_intent_queue_id": f"action-intent-queue-{run_id}",
        "queue_status": "shadow_review",
        "action_intents": action_intents,
        "world_contact_needed": bool(action_candidate_set.get("world_contact_needed")),
        "input_refs": {
            "action_candidate_set_ref": "runtime/state/action/action_candidate_set.json",
            "expression_plan_ref": "runtime/state/language/expression_plan.json",
            "relation_turn_frame_ref": "runtime/state/terminal/relation_turn_frame.json",
            "shadow_action_gate_ref": "runtime/state/membrane/shadow_action_gate.json",
        },
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def check_action_intent_queue(queue: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if queue.get("schema_version") != "action_intent_queue_v0":
        reasons.append("action_intent_provenance_gate schema mismatch")
    for field in ["action_intent_queue_id", "queue_status", "action_intents", "input_refs", "source_doc_refs"]:
        if not queue.get(field):
            reasons.append(f"action_intent_provenance_gate missing {field}")
    for intent in queue.get("action_intents", []):
        for field in [
            "action_intent_id",
            "action_candidate_ref",
            "action_kind",
            "language_origin_ref",
            "world_contact_mode",
            "side_effect_level",
        ]:
            if not intent.get(field):
                reasons.append(f"action_intent_provenance_gate intent missing {field}")
    return reasons


def _side_effect_level(world_contact_mode: str) -> str:
    if world_contact_mode == "review_before_release":
        return "external_reversible"
    if world_contact_mode == "external_release":
        return "external_irreversible"
    return "none"
