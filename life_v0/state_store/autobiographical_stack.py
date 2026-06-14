from __future__ import annotations

import json
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


def project_autobiographical_stack_from_live_turn(
    *,
    autobiographical_stack: dict[str, Any],
    generated_at: str,
    run_id: str | None = None,
    dialogue_turn_refs: list[str] | None = None,
    live_language_turn_refs: list[str] | None = None,
    self_narrative_trace: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    engram_index: dict[str, Any] | None = None,
    trigger_ref: str | None = None,
) -> dict[str, Any]:
    updated = _seed_missing_autobiographical_stack(
        autobiographical_stack,
        generated_at,
        run_id,
        self_model_state,
    )
    self_narrative_trace = self_narrative_trace or {}
    self_model_state = self_model_state or {}
    relationship_graph = relationship_graph or {}
    relationship_timeline = relationship_timeline or {}
    engram_index = engram_index or {}

    updated["generated_at"] = generated_at
    if run_id and not updated.get("run_id"):
        updated["run_id"] = run_id
    updated["status"] = "closed"
    updated["turn_refs"] = _dedupe(
        list(updated.get("turn_refs", [])) + list(dialogue_turn_refs or [])
    )
    updated["live_language_turn_refs"] = _dedupe(
        list(updated.get("live_language_turn_refs", []))
        + list(live_language_turn_refs or [])
    )
    updated["narrative_refs"] = _dedupe(
        list(updated.get("narrative_refs", []))
        + ["runtime/state/language/self_narrative_language_trace.json"]
        + list(self_narrative_trace.get("narrative_turn_refs", []))
    )

    subject_refs = [
        f"runtime/state/relationship/relationship_subject_graph.json#{subject.get('relationship_id')}"
        for subject in relationship_graph.get("subjects", [])
        if isinstance(subject, dict) and subject.get("relationship_id")
    ]
    updated["relationship_turn_refs"] = _dedupe(
        list(updated.get("relationship_turn_refs", []))
        + subject_refs
        + ["runtime/state/relationship/relationship_timeline.json"]
        + list(relationship_timeline.get("dialogue_turn_refs", []))
    )

    trait_slow_variables = self_model_state.get("trait_slow_variables", {})
    if isinstance(trait_slow_variables, dict):
        trait_names = sorted(trait_slow_variables)
        updated["trait_slow_variable_names"] = _dedupe(
            list(updated.get("trait_slow_variable_names", [])) + trait_names
        )
        updated["trait_slow_variable_refs"] = _dedupe(
            list(updated.get("trait_slow_variable_refs", []))
            + [
                f"runtime/state/self/self_model.json#trait_slow_variables.{name}"
                for name in trait_names
            ]
        )
        growth_projection = _growth_self_modification_projection(
            self_model_state=self_model_state,
            trait_slow_variables=trait_slow_variables,
        )
        if growth_projection["growth_ref_count"]:
            updated["growth_self_modification_projection"] = growth_projection
            updated["growth_self_modification_refs"] = _dedupe(
                list(updated.get("growth_self_modification_refs", []))
                + list(growth_projection["growth_refs"])
            )
            updated["growth_self_modification_trait_refs"] = _dedupe(
                list(updated.get("growth_self_modification_trait_refs", []))
                + list(growth_projection["trait_refs"])
            )
            updated["replay_priority"] = (
                "identity_growth_reconsolidation_first"
                if growth_projection["trait_count"]
                else updated.get("replay_priority", "identity_continuity_first")
            )

    graph_subject = next(
        (
            subject
            for subject in relationship_graph.get("subjects", [])
            if isinstance(subject, dict)
        ),
        {},
    )
    if graph_subject.get("relationship_stage"):
        updated["last_relationship_stage"] = graph_subject["relationship_stage"]
        updated["last_relationship_stage_ref"] = (
            "runtime/state/relationship/relationship_subject_graph.json#"
            f"{graph_subject.get('relationship_id', 'rel-v0-0001')}.relationship_stage"
        )

    updated["engram_index_refs"] = _dedupe(
        list(updated.get("engram_index_refs", []))
        + ["runtime/state/memory/engram_index.json"]
        + list(engram_index.get("live_dialogue_turn_refs", []))[-4:]
    )
    updated["autobiographical_update_refs"] = _dedupe(
        list(updated.get("autobiographical_update_refs", []))
        + [
            ref
            for ref in [
                trigger_ref,
                "runtime/state/language/dialogue_turn_log.jsonl",
                "runtime/state/language/self_narrative_language_trace.json",
                "runtime/state/memory/engram_index.json",
            ]
            if ref
        ]
    )
    updated["last_projected_from_live_turn_ref"] = (
        list(dialogue_turn_refs or [])[-1] if dialogue_turn_refs else None
    )
    updated["source_doc_refs"] = _dedupe(
        list(updated.get("source_doc_refs", [])) + SOURCE_DOC_REFS
    )
    return updated


def _seed_missing_autobiographical_stack(
    autobiographical_stack: dict[str, Any],
    generated_at: str,
    run_id: str | None,
    self_model_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if autobiographical_stack:
        return json.loads(json.dumps(autobiographical_stack))
    resolved_run_id = run_id or "resident-turn-writeback"
    self_model_state = self_model_state or {}
    anchor_refs = list(self_model_state.get("old_self_anchor_refs", [])) or [
        "docs/构思.md",
        "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    ]
    return {
        "schema_version": "autobiographical_stack_v0",
        "run_id": resolved_run_id,
        "generated_at": generated_at,
        "status": "closed",
        "stack_id": f"autobiographical-stack-{resolved_run_id}",
        "anchor_refs": anchor_refs,
        "turn_refs": [],
        "relationship_turn_refs": [],
        "narrative_refs": [],
        "replay_priority": "identity_continuity_first",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _growth_self_modification_projection(
    *,
    self_model_state: dict[str, Any],
    trait_slow_variables: dict[str, Any],
) -> dict[str, Any]:
    trait_names: list[str] = []
    trait_refs: list[str] = []
    growth_refs: list[str] = []
    pressure_levels: list[str] = []
    attention_targets: list[str] = []
    waiting_postures: list[str] = []
    boundaries: list[str] = []
    for name, payload in trait_slow_variables.items():
        if not isinstance(payload, dict):
            continue
        if not payload.get("growth_self_modification_update_mode"):
            continue
        trait_name = str(name)
        trait_names.append(trait_name)
        trait_refs.append(
            f"runtime/state/self/self_model.json#trait_slow_variables.{trait_name}"
        )
        growth_refs.extend(_string_list(payload.get("evidence_refs")))
        pressure_levels.extend(
            _string_list(payload.get("background_growth_self_modification_pressure_level"))
        )
        attention_targets.extend(
            _string_list(payload.get("background_growth_self_modification_attention_target"))
        )
        waiting_postures.extend(
            _string_list(payload.get("background_growth_self_modification_waiting_posture"))
        )
        boundaries.extend(
            _string_list(payload.get("background_growth_self_modification_boundary"))
        )
    growth_refs = _dedupe(
        growth_refs + _string_list(self_model_state.get("growth_window_refs"))
    )
    return {
        "schema_version": "autobiographical_growth_self_modification_projection_v0",
        "trait_names": _dedupe(trait_names),
        "trait_refs": _dedupe(trait_refs),
        "trait_count": len(_dedupe(trait_names)),
        "growth_refs": growth_refs,
        "growth_ref_count": len(growth_refs),
        "pressure_level": _first(pressure_levels),
        "attention_target": _first(attention_targets),
        "waiting_posture": _first(waiting_postures),
        "boundary": _first(boundaries),
        "projection_boundary": "autobiographical_growth_evidence_not_spoken_language",
    }


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _first(items: list[str]) -> str | None:
    deduped = _dedupe(items)
    return deduped[0] if deduped else None


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
