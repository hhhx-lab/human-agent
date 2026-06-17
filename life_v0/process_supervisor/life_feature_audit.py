from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from life_v0.dream.web_dream_learning import (
    build_web_dream_learning_effective_seed_preview,
)


def build_life_feature_audit(
    *,
    state_dir: Path,
    reports_dir: Path,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    state_dir = Path(state_dir)
    reports_dir = Path(reports_dir)
    features = [
        _feature_from_file(
            feature_id="autonomous_activity_cycle",
            label="常驻自主循环",
            path=state_dir / "terminal/resident_autonomous_activity_state.json",
            enabled_when=lambda data: data.get("status") == "active"
            and bool(data.get("cycle_coverage_complete")),
            detail_keys=[
                "activity_count",
                "last_activity_kind",
                "covered_activity_kinds",
                "missing_activity_kinds",
            ],
        ),
        _feature_from_file(
            feature_id="exit_dream_memory_summary",
            label="退出后梦境记忆摘要",
            path=state_dir / "dream/exit_dream_consolidation_summary.json",
            enabled_when=lambda data: data.get("status") == "closed"
            and int(data.get("source_dialogue_turn_count", 0) or 0) > 0,
            detail_keys=["source_dialogue_turn_count", "entry_state"],
        ),
        _feature_from_file(
            feature_id="dialogue_memory_summary",
            label="对话记忆摘要",
            path=state_dir / "memory/dialogue_memory_summary.json",
            enabled_when=lambda data: data.get("status") == "closed"
            and int(data.get("source_dialogue_turn_count", 0) or 0) > 0,
            detail_keys=["source_dialogue_turn_count"],
        ),
        _web_dream_feature(state_dir=state_dir, environ=environ),
        _file_presence_feature(
            "context_update",
            "上下文更新",
            state_dir / "terminal/terminal_life_loop_state.json",
        ),
        _file_presence_feature(
            "emotion_affect",
            "情绪核心向量",
            state_dir / "body/core_affect_vector.json",
        ),
        _file_presence_feature(
            "self_thinking",
            "自我思考",
            state_dir / "self/resident_self_thinking_state.json",
        ),
        _file_presence_feature(
            "consciousness_workspace",
            "意识工作区",
            state_dir / "consciousness/workspace_frame.json",
        ),
        _file_presence_feature(
            "relationship_state",
            "关系状态",
            state_dir / "relationship/relationship_timeline.json",
        ),
        _file_presence_feature(
            "body_inner_environment",
            "身体与内环境",
            state_dir / "body/need_state_vector.json",
            extra_paths=[
                state_dir / "body/body_resource_budget.json",
                state_dir / "body/body_rhythm_pulse.json",
            ],
        ),
        _file_presence_feature(
            "personality_self",
            "性格与自我",
            state_dir / "self/self_model.json",
        ),
        _file_presence_feature(
            "cognition_language",
            "认知与语义地图",
            state_dir / "language/semantic_map_frame.json",
            extra_paths=[state_dir / "language/inner_speech_frame.json"],
        ),
        _file_presence_feature(
            "short_long_memory",
            "长期/短期记忆",
            state_dir / "memory/memory_retrieval_frame.json",
            extra_paths=[
                state_dir / "memory/relationship_memory.json",
                state_dir / "memory/engram_index.json",
            ],
        ),
        _file_presence_feature(
            "vision_perception",
            "感知/视觉外周",
            state_dir / "observation/world_observation.json",
            extra_paths=[
                state_dir / "language/language_percept_frame.json",
                state_dir / "membrane/world_contact_summary.json",
            ],
            allow_partial=True,
        ),
        _feature_from_file(
            feature_id="model_expression",
            label="模型语言表达",
            path=state_dir / "language/model_expression_state.json",
            enabled_when=lambda data: data.get("model_expression_status")
            == "model_expression_applied",
            detail_keys=[
                "model_expression_status",
                "unreleased_reason",
                "post_expression_gate_status",
            ],
        ),
        _feature_from_file(
            feature_id="proactive_voice",
            label="主动发话",
            path=state_dir / "terminal/resident_terminal_proactive_state.json",
            enabled_when=lambda data: data.get("status")
            in {"released_model_expression", "held_internal"},
            detail_keys=["status", "last_focus", "release_count"],
        ),
    ]
    core_feature_ids = {
        "autonomous_activity_cycle",
        "exit_dream_memory_summary",
        "dialogue_memory_summary",
        "web_dream_learning",
        "context_update",
        "emotion_affect",
        "self_thinking",
        "consciousness_workspace",
        "relationship_state",
        "body_inner_environment",
        "personality_self",
        "cognition_language",
        "short_long_memory",
    }
    core_missing = [
        item
        for item in features
        if item["feature_id"] in core_feature_ids and item["status"] == "missing"
    ]
    core_disabled = [
        item
        for item in features
        if item["feature_id"] in core_feature_ids and item["status"] == "disabled"
    ]
    core_partial = [
        item
        for item in features
        if item["feature_id"] in core_feature_ids and item["status"] == "partial"
    ]
    missing = [item for item in features if item["status"] == "missing"]
    disabled = [item for item in features if item["status"] == "disabled"]
    partial = [item for item in features if item["status"] == "partial"]
    warnings = [item for item in features if item.get("warnings")]
    if core_disabled or core_missing or core_partial:
        overall = "incomplete"
    elif warnings:
        overall = "active_with_warnings"
    else:
        overall = "enabled"
    return {
        "schema_version": "life_feature_audit_v1",
        "overall_status": overall,
        "feature_count": len(features),
        "enabled_count": len([item for item in features if item["status"] == "enabled"]),
        "disabled_count": len(disabled),
        "missing_count": len(missing),
        "partial_count": len(partial),
        "core_disabled_count": len(core_disabled),
        "core_missing_count": len(core_missing),
        "core_partial_count": len(core_partial),
        "core_feature_ids": sorted(core_feature_ids),
        "warning_count": len(warnings),
        "features": features,
        "reports_dir": str(reports_dir),
    }


def _web_dream_feature(
    *,
    state_dir: Path,
    environ: Mapping[str, str] | None,
) -> dict[str, Any]:
    preview = build_web_dream_learning_effective_seed_preview(
        state_dir=state_dir,
        environ=environ,
    )
    runtime_state = _read_json(state_dir / "dream/web_dream_learning_state.json")
    enabled = bool(preview.get("enabled"))
    last_status = runtime_state.get("status") or "not_recorded"
    warnings: list[str] = []
    if enabled and last_status == "disabled":
        warnings.append("stale_disabled_state_overridden_by_effective_config")
    return {
        "feature_id": "web_dream_learning",
        "label": "网页梦境学习",
        "status": "enabled" if enabled else "disabled",
        "config_source": preview.get("source"),
        "seed_count": preview.get("seed_count"),
        "last_runtime_status": last_status,
        "warnings": warnings,
        "evidence_refs": [
            "runtime/state/dream/web_dream_learning_state.json",
            "runtime/state/dream/web_dream_learning_seeds.json",
        ],
    }


def _file_presence_feature(
    feature_id: str,
    label: str,
    path: Path,
    *,
    extra_paths: list[Path] | None = None,
    allow_partial: bool = False,
) -> dict[str, Any]:
    paths = [path] + list(extra_paths or [])
    existing = [item for item in paths if item.exists()]
    if len(existing) == len(paths) or (allow_partial and existing):
        status = "enabled"
    elif existing:
        status = "partial"
    else:
        status = "missing"
    return {
        "feature_id": feature_id,
        "label": label,
        "status": status,
        "evidence_refs": [_runtime_ref(item) for item in existing],
        "missing_refs": [_runtime_ref(item) for item in paths if not item.exists()],
        "warnings": [] if status == "enabled" else ["missing_or_partial_evidence"],
    }


def _feature_from_file(
    *,
    feature_id: str,
    label: str,
    path: Path,
    enabled_when,
    detail_keys: list[str],
) -> dict[str, Any]:
    data = _read_json(path)
    if not data:
        return {
            "feature_id": feature_id,
            "label": label,
            "status": "missing",
            "evidence_refs": [],
            "missing_refs": [_runtime_ref(path)],
            "warnings": ["missing_evidence_file"],
        }
    enabled = bool(enabled_when(data))
    details = {key: data.get(key) for key in detail_keys if key in data}
    return {
        "feature_id": feature_id,
        "label": label,
        "status": "enabled" if enabled else "disabled",
        "details": details,
        "evidence_refs": [_runtime_ref(path)],
        "warnings": [] if enabled else ["present_but_not_enabled_by_gate"],
    }


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _runtime_ref(path: Path) -> str:
    parts = path.parts
    if "runtime" in parts:
        index = parts.index("runtime")
        return "/".join(parts[index:])
    return str(path)
