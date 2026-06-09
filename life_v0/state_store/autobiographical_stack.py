from __future__ import annotations

from typing import Any


SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/07_emotion_personality_self.md",
    "docs/17_memory_trace_object_model.md",
    "docs/40_self_relationship_model_audit_protocol.md",
]


def build_autobiographical_stack(
    *,
    run_id: str,
    generated_at: str,
    self_model_state: dict[str, Any],
) -> dict[str, Any]:
    anchor_refs = list(self_model_state.get("old_self_anchor_refs", [])) or [
        "docs/构思.md",
        "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    ]
    return {
        "schema_version": "autobiographical_stack_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "stack_id": f"autobiographical-stack-{run_id}",
        "anchor_refs": anchor_refs,
        "turn_refs": ["runtime/state/language/dialogue_turn_log.jsonl#line-1"],
        "relationship_turn_refs": ["runtime/state/relationship/relationship_subject_graph.json#rel-v0-0001"],
        "narrative_refs": ["runtime/state/language/self_narrative_language_trace.json#self_narrative_seed"],
        "replay_priority": "identity_continuity_first",
        "source_doc_refs": SOURCE_DOC_REFS,
    }
