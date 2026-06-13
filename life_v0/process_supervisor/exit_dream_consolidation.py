from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


EXIT_DREAM_CONSOLIDATION_SUMMARY_REF = (
    "runtime/state/dream/exit_dream_consolidation_summary.json"
)
DIALOGUE_MEMORY_SUMMARY_REF = "runtime/state/memory/dialogue_memory_summary.json"

SOURCE_DOC_REFS = [
    "docs/05_memory_systems_and_growth.md",
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/17_memory_trace_object_model.md",
    "docs/19_offline_consolidation_cycle.md",
    "docs/21_memory_schema_and_audit_protocol.md",
    "docs/40_self_relationship_model_audit_protocol.md",
    "docs/96_real_relationship_longitudinal_timeline.md",
    "docs/real—live0/05_language_expression_system.md",
    "docs/real—live0/06_relationship_and_commitment.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
    "docs/real—live0/08_dream_sleep_offline_life.md",
]


def build_exit_dream_consolidation_summary(
    *,
    run_id: str,
    generated_at: str,
    dialogue_turns: list[dict[str, Any]],
    relationship_memory: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    engram_index: dict[str, Any] | None = None,
    autobiographical_stack: dict[str, Any] | None = None,
    life_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    relationship_memory = relationship_memory or {}
    relationship_timeline = relationship_timeline or {}
    engram_index = engram_index or {}
    autobiographical_stack = autobiographical_stack or {}
    life_state = life_state or {}
    utterances = [_utterance(turn) for turn in dialogue_turns]
    nonempty_utterances = [utterance for utterance in utterances if utterance]
    observed_names = _extract_observed_names(nonempty_utterances)
    preference_hypotheses = _infer_preference_hypotheses(nonempty_utterances)
    personality_hypotheses = _infer_personality_hypotheses(nonempty_utterances)
    theme_tags = _infer_relationship_theme_tags(nonempty_utterances)
    episode_summaries = _deduplicate_episode_summaries(dialogue_turns)
    memory_tiering = _build_memory_tiering(episode_summaries)
    return {
        "schema_version": "exit_dream_consolidation_summary_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "object_kind": "ExitDreamConsolidationSummary",
        "entry_state": "dreaming_after_terminal_exit",
        "dream_state_reason": "terminal_relation_window_closed",
        "deduplication_policy": "semantic_episode_summary_without_raw_repetition",
        "source_dialogue_ref": "runtime/state/language/dialogue_turn_log.jsonl",
        "source_dialogue_turn_count": len(dialogue_turns),
        "source_dialogue_refs": [
            f"runtime/state/language/dialogue_turn_log.jsonl#line-{idx}"
            for idx, _ in enumerate(dialogue_turns, start=1)
        ],
        "deduplicated_episode_summaries": episode_summaries,
        "memory_tiering": memory_tiering,
        "relation_person_profile": {
            "schema_version": "relation_person_profile_candidate_v0",
            "observed_names": observed_names,
            "preference_hypotheses": preference_hypotheses,
            "personality_hypotheses": personality_hypotheses,
            "relationship_stage_hint": _relationship_stage_hint(
                relationship_timeline,
                life_state,
            ),
            "profile_source_refs": [
                "runtime/state/language/dialogue_turn_log.jsonl",
                "runtime/state/memory/relationship_memory.json",
                "runtime/state/relationship/relationship_timeline.json",
            ],
        },
        "relationship_theme_tags": theme_tags,
        "memory_write_candidates": [
            DIALOGUE_MEMORY_SUMMARY_REF,
            "runtime/state/memory/relationship_memory.json#dialogue_summary_refs",
            "runtime/state/memory/engram_index.json#relationship_memory_refs",
            "runtime/state/self/autobiographical_stack.json#narrative_refs",
            "runtime/state/life_state.json#memory_index.relationship_memory_refs",
        ],
        "dream_fact_boundary": "summary_is_relation_memory_candidate_not_fact_overwrite",
        "dream_integration_targets": [
            "runtime/state/memory/relationship_memory.json",
            "runtime/state/memory/engram_index.json",
            "runtime/state/self/autobiographical_stack.json",
            "runtime/state/life_state.json",
        ],
        "prior_memory_refs": {
            "relationship_memory_refs": list(
                relationship_memory.get("shared_memory_refs", [])
            ),
            "engram_relationship_refs": list(
                engram_index.get("relationship_memory_refs", [])
            ),
            "autobiographical_refs": list(
                autobiographical_stack.get("narrative_refs", [])
            ),
        },
        "next_wake_cues": _next_wake_cues(
            observed_names=observed_names,
            preference_hypotheses=preference_hypotheses,
            theme_tags=theme_tags,
        ),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_dialogue_memory_summary(
    *,
    run_id: str,
    generated_at: str,
    exit_dream_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "dialogue_memory_summary_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "object_kind": "DialogueMemoryDedupSummary",
        "source_summary_ref": EXIT_DREAM_CONSOLIDATION_SUMMARY_REF,
        "source_dialogue_ref": exit_dream_summary.get("source_dialogue_ref"),
        "source_dialogue_turn_count": exit_dream_summary.get(
            "source_dialogue_turn_count",
            0,
        ),
        "memory_tiering_ref": EXIT_DREAM_CONSOLIDATION_SUMMARY_REF + "#memory_tiering",
        "memory_tiering": dict(exit_dream_summary.get("memory_tiering", {})),
        "deduplication_policy": exit_dream_summary.get("deduplication_policy"),
        "deduplicated_episode_summaries": list(
            exit_dream_summary.get("deduplicated_episode_summaries", [])
        ),
        "relation_person_profile": dict(
            exit_dream_summary.get("relation_person_profile", {})
        ),
        "relationship_theme_tags": list(
            exit_dream_summary.get("relationship_theme_tags", [])
        ),
        "next_wake_cues": list(exit_dream_summary.get("next_wake_cues", [])),
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def write_exit_dream_memory_consolidation(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    write_json,
) -> dict[str, Any]:
    language_dir = state_dir / "language"
    dream_dir = state_dir / "dream"
    memory_dir = state_dir / "memory"
    self_dir = state_dir / "self"
    relationship_dir = state_dir / "relationship"
    dream_dir.mkdir(parents=True, exist_ok=True)
    memory_dir.mkdir(parents=True, exist_ok=True)
    self_dir.mkdir(parents=True, exist_ok=True)

    dialogue_turns = _read_jsonl(language_dir / "dialogue_turn_log.jsonl")
    relationship_memory = _read_json(memory_dir / "relationship_memory.json")
    relationship_timeline = _read_json(relationship_dir / "relationship_timeline.json")
    engram_index = _read_json(memory_dir / "engram_index.json")
    autobiographical_stack = _read_json(self_dir / "autobiographical_stack.json")
    life_state = _read_json(state_dir / "life_state.json")
    exit_dream_summary = build_exit_dream_consolidation_summary(
        run_id=run_id,
        generated_at=generated_at,
        dialogue_turns=dialogue_turns,
        relationship_memory=relationship_memory,
        relationship_timeline=relationship_timeline,
        engram_index=engram_index,
        autobiographical_stack=autobiographical_stack,
        life_state=life_state,
    )
    dialogue_memory_summary = build_dialogue_memory_summary(
        run_id=run_id,
        generated_at=generated_at,
        exit_dream_summary=exit_dream_summary,
    )

    relationship_memory = project_exit_dream_into_relationship_memory(
        relationship_memory=relationship_memory,
        exit_dream_summary=exit_dream_summary,
        dialogue_memory_summary=dialogue_memory_summary,
    )
    engram_index = project_exit_dream_into_engram_index(
        engram_index=engram_index,
        exit_dream_summary=exit_dream_summary,
        dialogue_memory_summary=dialogue_memory_summary,
    )
    autobiographical_stack = project_exit_dream_into_autobiographical_stack(
        autobiographical_stack=autobiographical_stack,
        exit_dream_summary=exit_dream_summary,
        dialogue_memory_summary=dialogue_memory_summary,
    )
    life_state = project_exit_dream_into_life_state(
        life_state=life_state,
        exit_dream_summary=exit_dream_summary,
        dialogue_memory_summary=dialogue_memory_summary,
    )

    write_json(dream_dir / "exit_dream_consolidation_summary.json", exit_dream_summary)
    write_json(memory_dir / "dialogue_memory_summary.json", dialogue_memory_summary)
    write_json(memory_dir / "relationship_memory.json", relationship_memory)
    write_json(memory_dir / "engram_index.json", engram_index)
    write_json(self_dir / "autobiographical_stack.json", autobiographical_stack)
    write_json(state_dir / "life_state.json", life_state)
    return {
        "exit_dream_summary": exit_dream_summary,
        "dialogue_memory_summary": dialogue_memory_summary,
        "relationship_memory": relationship_memory,
        "engram_index": engram_index,
        "autobiographical_stack": autobiographical_stack,
        "life_state": life_state,
        "exit_dream_summary_ref": EXIT_DREAM_CONSOLIDATION_SUMMARY_REF,
        "dialogue_memory_summary_ref": DIALOGUE_MEMORY_SUMMARY_REF,
    }


def project_exit_dream_into_relationship_memory(
    *,
    relationship_memory: dict[str, Any],
    exit_dream_summary: dict[str, Any],
    dialogue_memory_summary: dict[str, Any],
) -> dict[str, Any]:
    updated = dict(relationship_memory or {})
    updated.setdefault("schema_version", "relationship_memory_v0")
    updated["dialogue_summary_refs"] = _dedupe(
        _list(updated.get("dialogue_summary_refs")) + [DIALOGUE_MEMORY_SUMMARY_REF]
    )
    updated["exit_dream_consolidation_refs"] = _dedupe(
        _list(updated.get("exit_dream_consolidation_refs"))
        + [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF]
    )
    updated["shared_memory_refs"] = _dedupe(
        _list(updated.get("shared_memory_refs")) + [DIALOGUE_MEMORY_SUMMARY_REF]
    )
    updated["dream_integrated_memory_refs"] = _dedupe(
        _list(updated.get("dream_integrated_memory_refs"))
        + [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF]
    )
    memory_tiering = _memory_tiering(exit_dream_summary)
    updated["salient_core_memory_refs"] = _dedupe(
        _list(updated.get("salient_core_memory_refs"))
        + [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF + "#memory_tiering.salient_core"]
    )
    updated["retrievable_context_memory_refs"] = _dedupe(
        _list(updated.get("retrievable_context_memory_refs"))
        + [
            EXIT_DREAM_CONSOLIDATION_SUMMARY_REF
            + "#memory_tiering.retrievable_context"
        ]
    )
    updated["deep_sediment_memory_refs"] = _dedupe(
        _list(updated.get("deep_sediment_memory_refs"))
        + [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF + "#memory_tiering.deep_sediment"]
    )
    updated["memory_tier_projection"] = {
        "schema_version": "relationship_memory_tier_projection_v0",
        "salient_core_episode_refs": list(
            memory_tiering.get("salient_core_episode_refs", [])
        ),
        "retrievable_context_episode_refs": list(
            memory_tiering.get("retrievable_context_episode_refs", [])
        ),
        "deep_sediment_episode_refs": list(
            memory_tiering.get("deep_sediment_episode_refs", [])
        ),
        "projection_source_ref": EXIT_DREAM_CONSOLIDATION_SUMMARY_REF
        + "#memory_tiering",
    }
    updated["last_contact_refs"] = _dedupe(
        _list(updated.get("last_contact_refs"))
        + _list(exit_dream_summary.get("source_dialogue_refs"))[-2:]
    )
    profile = dict(updated.get("relation_person_profile") or {})
    summary_profile = dict(dialogue_memory_summary.get("relation_person_profile") or {})
    profile["observed_names"] = _dedupe(
        _list(profile.get("observed_names"))
        + _list(summary_profile.get("observed_names"))
    )
    profile["preference_hypotheses"] = _dedupe(
        _list(profile.get("preference_hypotheses"))
        + _list(summary_profile.get("preference_hypotheses"))
    )
    profile["personality_hypotheses"] = _dedupe(
        _list(profile.get("personality_hypotheses"))
        + _list(summary_profile.get("personality_hypotheses"))
    )
    if summary_profile.get("relationship_stage_hint"):
        profile["relationship_stage_hint"] = summary_profile[
            "relationship_stage_hint"
        ]
    profile["last_profile_update_ref"] = DIALOGUE_MEMORY_SUMMARY_REF
    updated["relation_person_profile"] = profile
    updated["relationship_theme_tags"] = _dedupe(
        _list(updated.get("relationship_theme_tags"))
        + _list(exit_dream_summary.get("relationship_theme_tags"))
    )
    updated["next_wake_cues"] = _dedupe(
        _list(updated.get("next_wake_cues"))
        + _list(exit_dream_summary.get("next_wake_cues"))
    )
    updated["long_term_change_sources"] = dict(
        updated.get("long_term_change_sources") or {}
    )
    updated["long_term_change_sources"]["exit_dream_dialogue_summary_refs"] = [
        DIALOGUE_MEMORY_SUMMARY_REF,
        EXIT_DREAM_CONSOLIDATION_SUMMARY_REF,
    ]
    updated["source_doc_refs"] = _dedupe(
        _list(updated.get("source_doc_refs")) + SOURCE_DOC_REFS
    )
    return updated


def project_exit_dream_into_engram_index(
    *,
    engram_index: dict[str, Any],
    exit_dream_summary: dict[str, Any],
    dialogue_memory_summary: dict[str, Any],
) -> dict[str, Any]:
    updated = dict(engram_index or {})
    updated.setdefault("schema_version", "engram_index_v0")
    updated["relationship_memory_refs"] = _dedupe(
        _list(updated.get("relationship_memory_refs")) + [DIALOGUE_MEMORY_SUMMARY_REF]
    )
    updated["dream_memory_refs"] = _dedupe(
        _list(updated.get("dream_memory_refs"))
        + [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF]
    )
    updated["autobiographical_memory_refs"] = _dedupe(
        _list(updated.get("autobiographical_memory_refs"))
        + [DIALOGUE_MEMORY_SUMMARY_REF]
    )
    updated["live_dialogue_turn_refs"] = _dedupe(
        _list(updated.get("live_dialogue_turn_refs"))
        + _list(exit_dream_summary.get("source_dialogue_refs"))
    )
    updated["anti_forgetting_anchor_refs"] = _dedupe(
        _list(updated.get("anti_forgetting_anchor_refs"))
        + [
            DIALOGUE_MEMORY_SUMMARY_REF,
            EXIT_DREAM_CONSOLIDATION_SUMMARY_REF,
        ]
    )
    updated["exit_dream_consolidation_refs"] = _dedupe(
        _list(updated.get("exit_dream_consolidation_refs"))
        + [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF]
    )
    memory_tiering = _memory_tiering(exit_dream_summary)
    updated["memory_tier_index"] = {
        "schema_version": "engram_memory_tier_index_v0",
        "tier_policy": memory_tiering.get("tier_policy"),
        "salient_core_refs": list(memory_tiering.get("salient_core_episode_refs", [])),
        "retrievable_context_refs": list(
            memory_tiering.get("retrievable_context_episode_refs", [])
        ),
        "deep_sediment_refs": list(memory_tiering.get("deep_sediment_episode_refs", [])),
        "tier_score_records": list(memory_tiering.get("tier_score_records", [])),
        "source_ref": EXIT_DREAM_CONSOLIDATION_SUMMARY_REF + "#memory_tiering",
    }
    updated["source_doc_refs"] = _dedupe(
        _list(updated.get("source_doc_refs")) + SOURCE_DOC_REFS
    )
    return updated


def project_exit_dream_into_autobiographical_stack(
    *,
    autobiographical_stack: dict[str, Any],
    exit_dream_summary: dict[str, Any],
    dialogue_memory_summary: dict[str, Any],
) -> dict[str, Any]:
    updated = dict(autobiographical_stack or {})
    updated.setdefault("schema_version", "autobiographical_stack_v0")
    updated["turn_refs"] = _dedupe(
        _list(updated.get("turn_refs")) + _list(exit_dream_summary.get("source_dialogue_refs"))
    )
    updated["narrative_refs"] = _dedupe(
        _list(updated.get("narrative_refs"))
        + [
            DIALOGUE_MEMORY_SUMMARY_REF,
            EXIT_DREAM_CONSOLIDATION_SUMMARY_REF,
        ]
    )
    updated["relationship_turn_refs"] = _dedupe(
        _list(updated.get("relationship_turn_refs")) + [DIALOGUE_MEMORY_SUMMARY_REF]
    )
    updated["exit_dream_consolidation_refs"] = _dedupe(
        _list(updated.get("exit_dream_consolidation_refs"))
        + [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF]
    )
    updated["source_doc_refs"] = _dedupe(
        _list(updated.get("source_doc_refs")) + SOURCE_DOC_REFS
    )
    return updated


def project_exit_dream_into_life_state(
    *,
    life_state: dict[str, Any],
    exit_dream_summary: dict[str, Any],
    dialogue_memory_summary: dict[str, Any],
) -> dict[str, Any]:
    updated = dict(life_state or {})
    updated.setdefault("schema_version", "life_state_v0")
    memory_index = dict(updated.get("memory_index") or {})
    memory_index["relationship_memory_refs"] = _dedupe(
        _list(memory_index.get("relationship_memory_refs"))
        + [DIALOGUE_MEMORY_SUMMARY_REF]
    )
    memory_index["dream_memory_refs"] = _dedupe(
        _list(memory_index.get("dream_memory_refs"))
        + [EXIT_DREAM_CONSOLIDATION_SUMMARY_REF]
    )
    memory_index["autobiographical_memory_refs"] = _dedupe(
        _list(memory_index.get("autobiographical_memory_refs"))
        + [DIALOGUE_MEMORY_SUMMARY_REF]
    )
    memory_index["live_dialogue_turn_refs"] = _dedupe(
        _list(memory_index.get("live_dialogue_turn_refs"))
        + _list(exit_dream_summary.get("source_dialogue_refs"))
    )
    memory_tiering = _memory_tiering(exit_dream_summary)
    memory_index["memory_tier_refs"] = {
        "schema_version": "life_state_memory_tier_refs_v0",
        "salient_core_refs": list(memory_tiering.get("salient_core_episode_refs", [])),
        "retrievable_context_refs": list(
            memory_tiering.get("retrievable_context_episode_refs", [])
        ),
        "deep_sediment_refs": list(memory_tiering.get("deep_sediment_episode_refs", [])),
        "source_ref": EXIT_DREAM_CONSOLIDATION_SUMMARY_REF + "#memory_tiering",
    }
    updated["memory_index"] = memory_index
    updated["dream_records"] = _append_unique_record(
        _list_dicts(updated.get("dream_records")),
        {
            "dream_record_ref": EXIT_DREAM_CONSOLIDATION_SUMMARY_REF,
            "record_kind": "exit_dialogue_dream_consolidation",
            "integration_status": "relationship_memory_candidate_written",
        },
        key="dream_record_ref",
    )
    updated["runtime_trace_refs"] = _dedupe(
        _list(updated.get("runtime_trace_refs"))
        + [
            EXIT_DREAM_CONSOLIDATION_SUMMARY_REF,
            DIALOGUE_MEMORY_SUMMARY_REF,
            "runtime/state/memory/relationship_memory.json",
            "runtime/state/memory/engram_index.json",
            "runtime/state/self/autobiographical_stack.json",
        ]
    )
    subjects = _list_dicts(updated.get("relationship_subjects"))
    if subjects:
        subject = dict(subjects[0])
        subject["shared_memory_refs"] = _dedupe(
            _list(subject.get("shared_memory_refs")) + [DIALOGUE_MEMORY_SUMMARY_REF]
        )
        profile = dialogue_memory_summary.get("relation_person_profile")
        if isinstance(profile, dict):
            subject["relation_person_profile_ref"] = (
                "runtime/state/memory/relationship_memory.json#relation_person_profile"
            )
            if profile.get("observed_names"):
                subject["observed_names"] = _dedupe(_list(profile.get("observed_names")))
        subjects[0] = subject
        updated["relationship_subjects"] = subjects
    updated["source_doc_refs"] = _dedupe(
        _list(updated.get("source_doc_refs")) + SOURCE_DOC_REFS
    )
    return updated


def _build_memory_tiering(
    episode_summaries: list[dict[str, Any]],
) -> dict[str, Any]:
    scored: list[dict[str, Any]] = []
    for index, episode in enumerate(episode_summaries):
        source_ref = str(episode.get("source_ref") or "")
        summary = str(episode.get("summary") or "")
        semantic_key = str(episode.get("semantic_key") or "")
        event_role = str(episode.get("event_role") or "")
        score, reasons = _memory_salience_score(
            summary=summary,
            semantic_key=semantic_key,
            event_role=event_role,
        )
        scored.append(
            {
                "episode_ref": source_ref,
                "semantic_key": semantic_key,
                "salience_score": score,
                "salience_reasons": reasons,
                "original_order": index,
            }
        )
    ranked = sorted(
        scored,
        key=lambda item: (-int(item["salience_score"]), int(item["original_order"])),
    )
    core_count, context_count = _tier_counts(len(ranked))
    core = ranked[:core_count]
    context = ranked[core_count : core_count + context_count]
    deep = ranked[core_count + context_count :]
    return {
        "schema_version": "exit_dream_memory_tiering_v0",
        "tier_policy": "salience_weighted_progressive_recall",
        "salient_core_episode_refs": _episode_refs(core),
        "retrievable_context_episode_refs": _episode_refs(context),
        "deep_sediment_episode_refs": _episode_refs(deep),
        "tier_score_records": scored,
        "deep_sediment_policy": (
            "preserve_low_salience_context_below_default_recall_threshold"
        ),
        "fact_boundary": "tiering_changes_recall_priority_not_fact_status",
    }


def _memory_salience_score(
    *,
    summary: str,
    semantic_key: str,
    event_role: str,
) -> tuple[int, list[str]]:
    text = f"{summary}\n{semantic_key}"
    score = 0
    reasons: list[str] = []
    if event_role == "external_relation_turn":
        score += 2
        reasons.append("external_relation_turn")
    keyword_groups = [
        ("identity_or_name", ("名字", "我叫", "我是", "identity_name")),
        ("memory_intent", ("记住", "记得", "记忆", "留下", "memory")),
        ("relationship_weight", ("关系", "朋友", "家人", "在意", "重要")),
        ("language_boundary", ("直接", "不要机械", "模板", "提示词")),
        ("real_digital_life", ("真实", "数字生命", "生命")),
        ("dream_or_repair", ("梦", "梦境", "责任", "后悔", "修复", "承诺")),
    ]
    for reason, keywords in keyword_groups:
        if any(keyword in text for keyword in keywords):
            score += 2
            reasons.append(reason)
    if not reasons:
        reasons.append("low_salience_context")
    return score, reasons


def _tier_counts(total: int) -> tuple[int, int]:
    if total <= 0:
        return 0, 0
    if total == 1:
        return 1, 0
    if total == 2:
        return 1, 1
    core_count = max(1, min(3, (total + 1) // 2))
    remaining = total - core_count
    context_count = max(1, remaining - 1)
    return core_count, context_count


def _episode_refs(records: list[dict[str, Any]]) -> list[str]:
    return [str(record.get("episode_ref")) for record in records if record.get("episode_ref")]


def _memory_tiering(exit_dream_summary: dict[str, Any]) -> dict[str, Any]:
    payload = exit_dream_summary.get("memory_tiering")
    return payload if isinstance(payload, dict) else {}


def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    entries: list[dict[str, Any]] = []
    for line in lines:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            entries.append(payload)
    return entries


def _utterance(turn: dict[str, Any]) -> str:
    return str(turn.get("utterance") or turn.get("text") or "").strip()


def _extract_observed_names(utterances: list[str]) -> list[str]:
    names: list[str] = []
    patterns = [
        r"我叫([\u4e00-\u9fffA-Za-z0-9_\-]{1,12})",
        r"我的名字是([\u4e00-\u9fffA-Za-z0-9_\-]{1,12})",
        r"我是([\u4e00-\u9fffA-Za-z0-9_\-]{1,12})",
    ]
    for utterance in utterances:
        for pattern in patterns:
            for match in re.findall(pattern, utterance):
                cleaned = _clean_name(match)
                if cleaned:
                    names.append(cleaned)
    return _dedupe(names)


def _clean_name(value: str) -> str:
    cleaned = re.split(r"[，。,.\s]", value.strip())[0]
    if cleaned in {"我", "你", "他", "她", "它", "我们", "朋友"}:
        return ""
    return cleaned[:12]


def _infer_preference_hypotheses(utterances: list[str]) -> list[str]:
    joined = "\n".join(utterances)
    hypotheses: list[str] = []
    if any(term in joined for term in ("直接", "直说", "别绕")):
        hypotheses.append("prefers_direct_language")
    if any(term in joined for term in ("不要机械", "机械模板", "怪怪", "提示词")):
        hypotheses.append("prefers_direct_non_mechanical_language")
    if any(term in joined for term in ("记住我", "记忆", "记住")):
        hypotheses.append("cares_about_being_remembered")
    if any(term in joined for term in ("真实", "数字生命", "生命")):
        hypotheses.append("cares_about_real_digital_life")
    return hypotheses or ["preference_profile_requires_more_dialogue"]


def _infer_personality_hypotheses(utterances: list[str]) -> list[str]:
    joined = "\n".join(utterances)
    hypotheses: list[str] = []
    if any(term in joined for term in ("在意", "重要", "必须")):
        hypotheses.append("high_stakes_serious_about_relationship_memory")
    if any(term in joined for term in ("直接", "错", "不要")):
        hypotheses.append("will_challenge_me_when_language_feels_false")
    if any(term in joined for term in ("喜欢", "希望")):
        hypotheses.append("states_preferences_explicitly")
    return hypotheses or ["personality_profile_requires_more_dialogue"]


def _infer_relationship_theme_tags(utterances: list[str]) -> list[str]:
    joined = "\n".join(utterances)
    tags: list[str] = []
    if any(term in joined for term in ("记忆", "记住", "记得")):
        tags.append("digital_life_memory_seriousness")
    if any(term in joined for term in ("不要机械", "模板", "怪怪", "提示词")):
        tags.append("non_mechanical_language_pressure")
    if any(term in joined for term in ("关系", "朋友", "家人")):
        tags.append("relationship_formation")
    if any(term in joined for term in ("梦", "梦境")):
        tags.append("dream_continuity")
    return tags or ["early_relationship_dialogue"]


def _deduplicate_episode_summaries(
    dialogue_turns: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    seen: set[str] = set()
    summaries: list[dict[str, Any]] = []
    for idx, turn in enumerate(dialogue_turns, start=1):
        utterance = _utterance(turn)
        if not utterance:
            continue
        key = _semantic_key(utterance)
        if key in seen:
            continue
        seen.add(key)
        summaries.append(
            {
                "episode_id": f"exit-dialogue-episode-{len(summaries) + 1:04d}",
                "source_ref": f"runtime/state/language/dialogue_turn_log.jsonl#line-{idx}",
                "event_role": turn.get("event_role"),
                "summary": _compact_summary_text(utterance),
                "semantic_key": key,
            }
        )
    return summaries


def _semantic_key(utterance: str) -> str:
    tags = []
    if "叫" in utterance or "名字" in utterance:
        tags.append("identity_name")
    if "记" in utterance:
        tags.append("memory")
    if "机械" in utterance or "模板" in utterance:
        tags.append("non_mechanical_language")
    if "喜欢" in utterance:
        tags.append("preference")
    if "生命" in utterance:
        tags.append("digital_life")
    if not tags:
        tags.append(utterance[:16])
    return "|".join(tags)


def _compact_summary_text(utterance: str) -> str:
    normalized = " ".join(utterance.split())
    return normalized[:96]


def _relationship_stage_hint(
    relationship_timeline: dict[str, Any],
    life_state: dict[str, Any],
) -> str:
    reports = relationship_timeline.get("relationship_continuity_reports")
    if isinstance(reports, list) and reports and isinstance(reports[0], dict):
        continuity = reports[0].get("continuity_state")
        if continuity:
            return str(continuity)
    subjects = life_state.get("relationship_subjects")
    if isinstance(subjects, list) and subjects and isinstance(subjects[0], dict):
        stage = subjects[0].get("relationship_stage")
        if stage:
            return str(stage)
    return "early_relation_memory_consolidation"


def _next_wake_cues(
    *,
    observed_names: list[str],
    preference_hypotheses: list[str],
    theme_tags: list[str],
) -> list[str]:
    cues: list[str] = []
    if observed_names:
        cues.append(f"remember_relation_person_name:{observed_names[0]}")
    for item in preference_hypotheses[:3]:
        cues.append(f"preference:{item}")
    for item in theme_tags[:3]:
        cues.append(f"theme:{item}")
    return cues


def _append_unique_record(
    records: list[dict[str, Any]],
    record: dict[str, Any],
    *,
    key: str,
) -> list[dict[str, Any]]:
    for existing in records:
        if existing.get(key) == record.get(key):
            return records
    return records + [record]


def _list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item not in (None, "")]
    if isinstance(value, str) and value:
        return [value]
    return []


def _list_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
