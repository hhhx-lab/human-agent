from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Mapping

from life_v0.process_supervisor.model_expression import (
    _chat_completion_endpoint,
    _extract_chat_content,
    _model_expression_headers,
    _model_expression_skip_reason,
    _post_openai_compatible_chat_completion,
    _timeout_seconds,
)
from life_v0.runtime_config import DigitalLifeRuntimeConfig, load_digital_life_runtime_config

EXIT_DREAM_SEMANTIC_CONSOLIDATION_REF = (
    "runtime/state/dream/exit_dream_semantic_consolidation.json"
)

ExitDreamSemanticConsolidationTransport = Callable[
    [str, Mapping[str, str], dict[str, Any], float],
    dict[str, Any],
]

SOURCE_DOC_REFS = [
    "docs/v0/entry/v0_dream_module_implementation_plan.md",
    "docs/real—live0/08_dream_sleep_offline_life.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def resolve_exit_dream_episode_summaries(
    *,
    run_id: str,
    generated_at: str,
    dialogue_turns: list[dict[str, Any]],
    rule_based_episode_summaries: list[dict[str, Any]],
    dream_dir: Path | None = None,
    write_json: Callable[[Path, dict[str, Any]], None] | None = None,
    transport: ExitDreamSemanticConsolidationTransport | None = None,
    runtime_config: DigitalLifeRuntimeConfig | None = None,
    repo_root: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    config = runtime_config or load_digital_life_runtime_config(
        repo_root=repo_root,
        environ=environ,
    )
    audit = _base_audit(
        run_id=run_id,
        generated_at=generated_at,
        dialogue_turn_count=len(dialogue_turns),
        rule_based_episode_count=len(rule_based_episode_summaries),
    )
    model_episodes, model_audit = _try_model_semantic_consolidation(
        run_id=run_id,
        generated_at=generated_at,
        dialogue_turns=dialogue_turns,
        runtime_config=config,
        transport=transport,
    )
    audit.update(model_audit)
    if model_episodes:
        audit["consolidation_mode"] = "model_semantic"
        audit["episode_summary_count"] = len(model_episodes)
        episodes = model_episodes
    else:
        audit["consolidation_mode"] = "rule_based_fallback"
        audit["episode_summary_count"] = len(rule_based_episode_summaries)
        episodes = [
            {**episode, "consolidation_mode": "rule_based_fallback"}
            for episode in rule_based_episode_summaries
        ]
    if dream_dir is not None:
        dream_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = dream_dir / "exit_dream_semantic_consolidation.json"
        audit["exit_dream_semantic_consolidation_ref"] = (
            EXIT_DREAM_SEMANTIC_CONSOLIDATION_REF
        )
        if write_json is not None:
            write_json(artifact_path, audit)
        else:
            artifact_path.write_text(
                json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    return episodes, audit


def _try_model_semantic_consolidation(
    *,
    run_id: str,
    generated_at: str,
    dialogue_turns: list[dict[str, Any]],
    runtime_config: DigitalLifeRuntimeConfig,
    transport: ExitDreamSemanticConsolidationTransport | None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    audit: dict[str, Any] = {
        "model_status": "skipped",
        "model_skip_reason": None,
        "model_error": None,
        "session_narrative_summary": "",
        "relationship_theme_tags": [],
    }
    if not dialogue_turns:
        audit["model_skip_reason"] = "no_dialogue_turns"
        return [], audit

    skip_reason = None if transport is not None else _model_expression_skip_reason(
        runtime_config
    )
    if skip_reason:
        audit["model_skip_reason"] = skip_reason
        return [], audit

    endpoint = _chat_completion_endpoint(runtime_config.model_base_url)
    request_payload = _build_semantic_consolidation_payload(
        runtime_config=runtime_config,
        run_id=run_id,
        generated_at=generated_at,
        dialogue_turns=dialogue_turns,
    )
    try:
        api_response = (transport or _post_openai_compatible_chat_completion)(
            endpoint,
            _model_expression_headers(runtime_config),
            request_payload,
            _timeout_seconds(runtime_config),
        )
        raw_text, finish_reason = _extract_chat_content(api_response)
        audit["model_finish_reason"] = finish_reason
        if not raw_text:
            audit["model_status"] = "empty_response"
            audit["model_skip_reason"] = "empty_model_response"
            return [], audit
        parsed = _parse_model_consolidation_output(raw_text)
        episodes = _normalize_model_episodes(
            parsed=parsed,
            dialogue_turns=dialogue_turns,
        )
        if not episodes:
            audit["model_status"] = "invalid_output"
            audit["model_skip_reason"] = "model_output_missing_episode_summaries"
            return [], audit
        audit["model_status"] = "applied"
        audit["session_narrative_summary"] = str(
            parsed.get("session_narrative_summary") or ""
        )[:480]
        audit["relationship_theme_tags"] = _string_list(
            parsed.get("relationship_theme_tags")
        )
        return episodes, audit
    except Exception as exc:  # pragma: no cover - network variance
        audit["model_status"] = "failed"
        audit["model_error"] = str(exc)[:240]
        audit["model_skip_reason"] = "model_request_failed"
        return [], audit


def _build_semantic_consolidation_payload(
    *,
    runtime_config: DigitalLifeRuntimeConfig,
    run_id: str,
    generated_at: str,
    dialogue_turns: list[dict[str, Any]],
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": runtime_config.model_name,
        "messages": [
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "schema_version": "exit_dream_semantic_consolidation_input_v1",
                        "run_id": run_id,
                        "generated_at": generated_at,
                        "task": "offline_exit_dream_episode_consolidation",
                        "boundary": (
                            "internal_consolidation_structured_output_not_spoken_language"
                        ),
                        "output_contract": {
                            "schema_version": (
                                "exit_dream_semantic_consolidation_output_v1"
                            ),
                            "required_fields": [
                                "session_narrative_summary",
                                "episode_summaries",
                            ],
                            "episode_summaries_item_fields": [
                                "source_line_indices",
                                "summary",
                                "semantic_key",
                                "salience_hint",
                                "consolidation_rationale",
                            ],
                            "salience_hint_values": [
                                "salient_core",
                                "retrievable_context",
                                "deep_sediment",
                            ],
                        },
                        "instructions": {
                            "merge_duplicate_or_near_duplicate_turns": True,
                            "preserve_relationship_identity_and_memory_intent": True,
                            "do_not_emit_fixed_wake_questions": True,
                            "do_not_promote_dream_content_to_fact_memory": True,
                        },
                        "dialogue_turns": _dialogue_turn_payload(dialogue_turns),
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ),
            }
        ],
        "stream": False,
    }
    if runtime_config.model_temperature is not None:
        payload["temperature"] = runtime_config.model_temperature
    if runtime_config.model_max_output_tokens is not None:
        payload["max_tokens"] = runtime_config.model_max_output_tokens
    return payload


def _dialogue_turn_payload(
    dialogue_turns: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    payload: list[dict[str, Any]] = []
    for index, turn in enumerate(dialogue_turns, start=1):
        utterance = str(turn.get("utterance") or turn.get("text") or "").strip()
        if not utterance:
            continue
        payload.append(
            {
                "line_index": index,
                "source_ref": (
                    f"runtime/state/language/dialogue_turn_log.jsonl#line-{index}"
                ),
                "event_role": turn.get("event_role"),
                "utterance": utterance[:240],
            }
        )
    return payload


def _parse_model_consolidation_output(raw_text: str) -> dict[str, Any]:
    stripped = raw_text.strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", stripped, flags=re.S)
    if fence_match:
        stripped = fence_match.group(1)
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        object_match = re.search(r"\{.*\}", stripped, flags=re.S)
        if not object_match:
            return {}
        payload = json.loads(object_match.group(0))
    return payload if isinstance(payload, dict) else {}


def _normalize_model_episodes(
    *,
    parsed: dict[str, Any],
    dialogue_turns: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    raw_episodes = parsed.get("episode_summaries")
    if not isinstance(raw_episodes, list):
        return []
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(raw_episodes, start=1):
        if not isinstance(item, dict):
            continue
        line_indices = _line_indices(item.get("source_line_indices"))
        if not line_indices:
            continue
        primary_line = line_indices[0]
        turn = _turn_at_line(dialogue_turns, primary_line)
        summary = str(item.get("summary") or "").strip()
        if not summary:
            continue
        semantic_key = str(item.get("semantic_key") or f"model_episode_{index}")[:64]
        salience_hint = _normalize_salience_hint(item.get("salience_hint"))
        source_refs = [
            f"runtime/state/language/dialogue_turn_log.jsonl#line-{line}"
            for line in line_indices
        ]
        normalized.append(
            {
                "episode_id": f"exit-dialogue-episode-{index:04d}",
                "source_ref": source_refs[0],
                "source_refs": source_refs,
                "event_role": turn.get("event_role") if turn else None,
                "summary": summary[:160],
                "semantic_key": semantic_key,
                "salience_hint": salience_hint,
                "consolidation_mode": "model_semantic",
                "consolidation_rationale": str(
                    item.get("consolidation_rationale") or ""
                )[:160],
            }
        )
    return normalized


def _base_audit(
    *,
    run_id: str,
    generated_at: str,
    dialogue_turn_count: int,
    rule_based_episode_count: int,
) -> dict[str, Any]:
    return {
        "schema_version": "exit_dream_semantic_consolidation_audit_v1",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "object_kind": "ExitDreamSemanticConsolidationAudit",
        "dialogue_turn_count": dialogue_turn_count,
        "rule_based_episode_count": rule_based_episode_count,
        "consolidation_mode": "pending",
        "model_status": "pending",
        "boundary": "internal_consolidation_not_spoken_output",
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def _turn_at_line(
    dialogue_turns: list[dict[str, Any]],
    line_index: int,
) -> dict[str, Any]:
    if line_index < 1 or line_index > len(dialogue_turns):
        return {}
    turn = dialogue_turns[line_index - 1]
    return turn if isinstance(turn, dict) else {}


def _line_indices(value: Any) -> list[int]:
    if not isinstance(value, list):
        return []
    indices: list[int] = []
    for item in value:
        try:
            parsed = int(item)
        except (TypeError, ValueError):
            continue
        if parsed > 0:
            indices.append(parsed)
    return indices


def _normalize_salience_hint(value: Any) -> str:
    hint = str(value or "retrievable_context")
    if hint in {"salient_core", "retrievable_context", "deep_sediment"}:
        return hint
    return "retrievable_context"


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]