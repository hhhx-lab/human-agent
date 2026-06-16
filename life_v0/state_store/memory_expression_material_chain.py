from __future__ import annotations

from typing import Any

SOURCE_DOC_REFS = [
    "docs/v0/entry/v0_memory_recall_to_expression_contract.md",
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]

MEMORY_EXPRESSION_MATERIAL_CHAIN_REF = (
    "runtime/state/memory/memory_retrieval_frame.json#memory_expression_material_chain"
)


def build_memory_expression_material_chain(
    *,
    memory_retrieval_frame: dict[str, Any] | None,
    pattern_completion_frame: dict[str, Any] | None = None,
    dream_reentry_refs: list[str] | None = None,
    memory_hygiene_refs: list[str] | None = None,
    web_dream_refs: list[str] | None = None,
    structured_wake_question_candidates: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    frame = memory_retrieval_frame or {}
    phenomenology = frame.get("memory_phenomenology_profile") or {}
    reconstructive = frame.get("reconstructive_recall_profile") or {}
    recall_profile = frame.get("recall_to_expression_profile") or {}
    fragments = _reconstruction_fragments(pattern_completion_frame, reconstructive)
    chain_steps = [
        _chain_step(
            step_id="cue_extraction",
            passed=bool(frame.get("cue_terms")),
            evidence_refs=_string_list(frame.get("cue_terms"))[:6],
        ),
        _chain_step(
            step_id="hippocampal_activation",
            passed=bool(reconstructive.get("hippocampal_activation_count")),
            evidence_refs=_string_list(reconstructive.get("reconstruction_fragment_refs"))[:6],
        ),
        _chain_step(
            step_id="reconstructive_fragment_assembly",
            passed=bool(fragments),
            evidence_refs=[
                str(fragment.get("trace_ref"))
                for fragment in fragments
                if fragment.get("trace_ref")
            ][:6],
        ),
        _chain_step(
            step_id="recall_to_expression_profile",
            passed=bool(recall_profile.get("expression_source_refs"))
            or bool(fragments),
            evidence_refs=_string_list(recall_profile.get("expression_source_refs"))[:6],
        ),
        _chain_step(
            step_id="phenomenology_grounding",
            passed=bool(phenomenology.get("expression_material_grounded")),
            evidence_refs=[
                str(phenomenology.get("recall_phenomenology") or ""),
                str(phenomenology.get("recall_strength_score") or ""),
            ],
        ),
    ]
    tip_gate = _tip_of_tongue_expression_gate(
        phenomenology=phenomenology,
        fragments=fragments,
        recall_profile=recall_profile,
    )
    chain_closed = all(step["passed"] for step in chain_steps[:4]) or bool(
        fragments and tip_gate.get("expression_release_posture") != "withhold_pending_reconstruction"
    )
    offline_material_refs = _dedupe(
        _string_list(dream_reentry_refs)
        + _string_list(memory_hygiene_refs)
        + _string_list(web_dream_refs)
    )
    wake_candidates = [
        candidate
        for candidate in (structured_wake_question_candidates or [])
        if isinstance(candidate, dict)
    ]
    return {
        "schema_version": "memory_expression_material_chain_v0",
        "chain_ref": MEMORY_EXPRESSION_MATERIAL_CHAIN_REF,
        "chain_closed": chain_closed,
        "chain_steps": chain_steps,
        "reconstruction_fragment_count": len(fragments),
        "tip_of_tongue_gate": tip_gate,
        "expression_release_posture": tip_gate.get("expression_release_posture"),
        "expression_material_audit_boundary": (
            "chain_audits_structured_material_not_spoken_template"
        ),
        "dream_reentry_refs": _string_list(dream_reentry_refs),
        "memory_hygiene_refs": _string_list(memory_hygiene_refs),
        "web_dream_refs": _string_list(web_dream_refs),
        "structured_wake_question_candidates": wake_candidates,
        "expression_guardrails": {
            "no_fixed_response": True,
            "no_dream_fact_promotion": True,
            "model_generated_only": True,
        },
        "offline_expression_material_refs": offline_material_refs,
        "consumer_refs": [
            "runtime/state/language/model_expression_state.json#model_expression_context_summary",
            "runtime/reports/latest/dialogue_writeback_bundle.json#memory_retrieval_writeback_refs",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _tip_of_tongue_expression_gate(
    *,
    phenomenology: dict[str, Any],
    fragments: list[dict[str, Any]],
    recall_profile: dict[str, Any],
) -> dict[str, Any]:
    risk = str(phenomenology.get("tip_of_tongue_risk") or "baseline")
    recall_strength = float(phenomenology.get("recall_strength_score") or 0)
    uncertain = bool(phenomenology.get("uncertain_boundary_active"))
    recall_question = phenomenology.get("recall_phenomenology") in {
        "uncertain",
        "partial",
    }
    live_source_refs = [
        ref
        for ref in _string_list(recall_profile.get("expression_source_refs"))
        if "memory_trace_store" in ref or "memory-trace-" in ref
    ]
    block = (
        risk in {"elevated", "moderate"}
        and recall_strength < 0.45
        and not fragments
    ) or (
        uncertain
        and recall_question
        and not fragments
        and not live_source_refs
    )
    if block:
        return {
            "gate_status": "blocked",
            "expression_release_posture": "withhold_pending_reconstruction",
            "block_reason": "tip_of_tongue_or_uncertain_without_reconstruction_fragments",
            "tip_of_tongue_risk": risk,
            "recall_strength_score": recall_strength,
            "requires_silent_or_uncertain_expression_route": True,
        }
    if risk == "moderate" and not fragments:
        return {
            "gate_status": "cautious",
            "expression_release_posture": "release_with_uncertainty_boundary",
            "block_reason": None,
            "tip_of_tongue_risk": risk,
            "recall_strength_score": recall_strength,
            "requires_silent_or_uncertain_expression_route": False,
        }
    return {
        "gate_status": "open",
        "expression_release_posture": "release_with_source_boundary",
        "block_reason": None,
        "tip_of_tongue_risk": risk,
        "recall_strength_score": recall_strength,
        "requires_silent_or_uncertain_expression_route": False,
    }


def _reconstruction_fragments(
    pattern_completion_frame: dict[str, Any] | None,
    reconstructive_recall_profile: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    fragments: list[dict[str, Any]] = []
    reconstructive = (pattern_completion_frame or {}).get("reconstructive_completion") or {}
    if isinstance(reconstructive, dict):
        for fragment in reconstructive.get("reconstruction_fragments", []):
            if isinstance(fragment, dict):
                fragments.append(fragment)
    for candidate in (pattern_completion_frame or {}).get("completion_candidates", []):
        if not isinstance(candidate, dict):
            continue
        for fragment in candidate.get("reconstruction_fragments", []):
            if isinstance(fragment, dict):
                fragments.append(fragment)
    if not fragments:
        for ref in _string_list(
            (reconstructive_recall_profile or {}).get("reconstruction_fragment_refs")
        ):
            fragments.append({"trace_ref": ref})
    return fragments


def _chain_step(
    *,
    step_id: str,
    passed: bool,
    evidence_refs: list[str],
) -> dict[str, Any]:
    return {
        "step_id": step_id,
        "passed": passed,
        "evidence_refs": _dedupe(_string_list(evidence_refs)),
    }


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [str(value)] if value else []


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result