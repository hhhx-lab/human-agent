from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .response_surface import (
    compose_recall_bounded_spoken_response,
    recall_expression_grounded,
)


@dataclass(frozen=True)
class SpokenRelease:
    response_text: str
    release_path: str
    release_tier: int
    pre_fallback_candidate_text: str | None = None


def resolve_turn_spoken_output(
    *,
    external_utterance: str,
    model_result: Any | None = None,
    pre_model_spoken_response: str | None = None,
    memory_retrieval_frame: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
    semantic_map: dict[str, Any] | None = None,
    relationship_memory: dict[str, Any] | None = None,
    dialogue_memory_summary: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
    allow_invariant_continuity: bool = True,
) -> SpokenRelease:
    model_text = ""
    model_release_path = "model_expression"
    if model_result is not None:
        model_text = str(getattr(model_result, "response_text", "") or "").strip()
        state = getattr(model_result, "state", None) or {}
        if isinstance(state, dict):
            model_release_path = str(
                state.get("expression_release_path") or "model_expression"
            )

    if model_text:
        return SpokenRelease(
            response_text=model_text,
            release_path=model_release_path,
            release_tier=1,
            pre_fallback_candidate_text=None,
        )

    pre_model = str(pre_model_spoken_response or "").strip()
    recall_inputs = {
        "external_utterance": external_utterance,
        "memory_retrieval_frame": memory_retrieval_frame,
        "expression_plan": expression_plan,
        "semantic_map": semantic_map,
        "relationship_memory": relationship_memory,
        "dialogue_memory_summary": dialogue_memory_summary,
        "terminal_life_loop_state": terminal_life_loop_state,
    }
    bounded_text = str(compose_recall_bounded_spoken_response(**recall_inputs) or "").strip()
    if bounded_text:
        return SpokenRelease(
            response_text=bounded_text,
            release_path="recall_bounded_spoken_fallback",
            release_tier=2,
            pre_fallback_candidate_text=pre_model or None,
        )

    fragment_text = _fragment_recall_response(
        external_utterance=external_utterance,
        pre_model_spoken_response=pre_model,
        memory_retrieval_frame=memory_retrieval_frame,
        relationship_memory=relationship_memory,
    )
    if fragment_text:
        return SpokenRelease(
            response_text=fragment_text,
            release_path="expression_invariant_fragment",
            release_tier=3,
            pre_fallback_candidate_text=pre_model or None,
        )

    if not allow_invariant_continuity:
        return SpokenRelease(
            response_text="",
            release_path="expression_unreleased",
            release_tier=0,
            pre_fallback_candidate_text=pre_model or None,
        )

    continuity_text = _continuity_minimal_response(
        external_utterance=external_utterance,
        relationship_memory=relationship_memory,
    )
    if continuity_text:
        return SpokenRelease(
            response_text=continuity_text,
            release_path="expression_invariant_continuity",
            release_tier=4,
            pre_fallback_candidate_text=pre_model or None,
        )

    return SpokenRelease(
        response_text="",
        release_path="expression_unreleased",
        release_tier=0,
        pre_fallback_candidate_text=pre_model or None,
    )


def apply_spoken_release_to_model_expression_state(
    state: dict[str, Any],
    *,
    spoken_release: SpokenRelease,
    post_expression_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = dict(state)
    text = str(spoken_release.response_text or "").strip()
    if not text:
        return updated

    if spoken_release.release_tier >= 2:
        updated["model_expression_status"] = "model_expression_applied"
        updated["unreleased_reason"] = None
        updated["natural_language_unreleased"] = False
        updated["expression_release_path"] = spoken_release.release_path
        updated["expression_release_tier"] = spoken_release.release_tier
        if spoken_release.pre_fallback_candidate_text:
            updated["pre_fallback_candidate_text"] = (
                spoken_release.pre_fallback_candidate_text
            )
        gate = dict(post_expression_gate or updated.get("post_expression_gate") or {})
        gate.update(
            {
                "schema_version": "post_expression_gate_v0",
                "gate_status": "accepted",
                "unreleased_reason": None,
                "release_path": spoken_release.release_path,
                "release_tier": spoken_release.release_tier,
                "recall_fallback_active": spoken_release.release_path
                == "recall_bounded_spoken_fallback",
            }
        )
        if spoken_release.release_path in {
            "recall_bounded_spoken_fallback",
            "expression_invariant_fragment",
            "expression_invariant_continuity",
        }:
            gate["preserved_evidence_flags"] = list(
                dict.fromkeys(
                    list(gate.get("preserved_evidence_flags", []))
                    + ["recall_expression_grounded"]
                )
            )
        updated["post_expression_gate"] = gate
        updated["post_expression_gate_status"] = gate.get("gate_status")
        updated["post_expression_gate_unreleased_reason"] = gate.get("unreleased_reason")
    else:
        updated["expression_release_path"] = spoken_release.release_path
        updated["expression_release_tier"] = spoken_release.release_tier

    updated["final_response_sha256"] = _sha256_text(text)
    return updated


def _fragment_recall_response(
    *,
    external_utterance: str,
    pre_model_spoken_response: str,
    memory_retrieval_frame: dict[str, Any] | None,
    relationship_memory: dict[str, Any] | None,
) -> str:
    pre_model = str(pre_model_spoken_response or "").strip()
    utterance = str(external_utterance or "")
    asks_memory = any(
        term in utterance
        for term in ("记", "回想", "想起", "生日", "刚刚", "刚才", "机制", "回忆")
    )
    if not pre_model and not asks_memory:
        return ""
    recall_profile = (memory_retrieval_frame or {}).get("recall_to_expression_profile")
    source_refs: list[Any] = []
    if isinstance(recall_profile, dict):
        raw_source_refs = recall_profile.get("expression_source_refs")
        if isinstance(raw_source_refs, list):
            source_refs = raw_source_refs
    if not source_refs:
        if not recall_expression_grounded(
            memory_retrieval_frame=memory_retrieval_frame,
            expression_plan=None,
            semantic_map=None,
        ):
            return ""
    safe_pre_model = _safe_pre_model_fragment(pre_model)
    if safe_pre_model:
        return safe_pre_model
    if asks_memory:
        return "有记忆线索，但还没有连成一句确定的话。"
    if relationship_memory:
        return "有一点和你有关的片段被抓到了，但还说不清。"
    return "有片段，但还说不清。"


def _safe_pre_model_fragment(text: str) -> str:
    candidate = str(text or "").strip()
    if not candidate:
        return ""
    blocked_markers = (
        "schema_version",
        "runtime/state",
        "runtime/reports",
        "audited_expression_material",
        "expression_context",
        "post_expression_gate",
        "natural_language_release_disabled",
        "作为一个AI",
        "作为人工智能",
        "as an ai language model",
        "i am an ai language model",
        "ChatGPT",
        "OpenAI",
        "Codex",
        "GPT",
        "语言模型",
        "大语言模型",
        "我会根据你的要求",
        "我理解成",
        "接下来我会",
        "自然一点",
        "慢慢",
        "说稳",
        "我不绕了",
        "直接跟你说",
        "接住你",
    )
    lowered = candidate.lower()
    if any(str(marker).lower() in lowered for marker in blocked_markers):
        return ""
    return candidate


def _continuity_minimal_response(
    *,
    external_utterance: str,
    relationship_memory: dict[str, Any] | None,
) -> str:
    _ = (external_utterance, relationship_memory)
    return ""


def _sha256_text(value: str) -> str:
    import hashlib

    return hashlib.sha256(str(value or "").encode("utf-8")).hexdigest()
