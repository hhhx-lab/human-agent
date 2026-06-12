from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from ..runtime_config import (
    RUNTIME_CONFIG_REPORT_REF,
    RUNTIME_CONFIG_STATE_REF,
    DigitalLifeRuntimeConfig,
    load_digital_life_runtime_config,
)


MODEL_EXPRESSION_STATE_REF = "runtime/state/language/model_expression_state.json"
MODEL_EXPRESSION_REPORT_REF = (
    "runtime/reports/latest/digital_life_model_expression_report.json"
)

MODEL_EXPRESSION_ENABLED_PROVIDERS = {
    "openai",
    "openai-compatible",
    "openai_compatible",
    "compatible",
    "custom-openai",
    "custom_openai",
    "wyzai",
    "shell-wyzai",
    "shell_wyzai",
}
MODEL_EXPRESSION_DISABLED_PROVIDERS = {"", "local", "none", "disabled", "off"}

ModelExpressionTransport = Callable[
    [str, Mapping[str, str], dict[str, Any], float],
    dict[str, Any],
]


@dataclass(frozen=True)
class ModelExpressionResult:
    response_text: str
    deterministic_response: str
    state: dict[str, Any]
    report: dict[str, Any]
    state_ref: str = MODEL_EXPRESSION_STATE_REF
    report_ref: str = MODEL_EXPRESSION_REPORT_REF

    @property
    def applied(self) -> bool:
        return self.state.get("model_expression_status") == "model_expression_applied"


def compose_model_expression(
    *,
    run_id: str,
    generated_at: str,
    external_utterance: str,
    deterministic_response: str,
    language_dir: Path,
    reports_dir: Path,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    shared_term_registry: dict[str, Any] | None = None,
    commitment_index: dict[str, Any] | None = None,
    language_percept: dict[str, Any] | None = None,
    semantic_map: dict[str, Any] | None = None,
    inner_speech: dict[str, Any] | None = None,
    expression_monitor: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
    life_context_frame: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
    brain_graph: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    prediction_workspace: dict[str, Any] | None = None,
    workspace_frame: dict[str, Any] | None = None,
    repo_root: Path | None = None,
    env_file: Path | None = None,
    environ: Mapping[str, str] | None = None,
    transport: ModelExpressionTransport | None = None,
    write_json: Callable[[Path, dict[str, Any]], None] | None = None,
) -> ModelExpressionResult:
    config = load_digital_life_runtime_config(
        repo_root=repo_root,
        env_file=env_file,
        environ=environ,
    )
    context = build_model_expression_context(
        external_utterance=external_utterance,
        deterministic_response=deterministic_response,
        runtime_config=config,
        relationship_graph=relationship_graph,
        relationship_timeline=relationship_timeline,
        shared_term_registry=shared_term_registry,
        commitment_index=commitment_index,
        language_percept=language_percept,
        semantic_map=semantic_map,
        inner_speech=inner_speech,
        expression_monitor=expression_monitor,
        expression_plan=expression_plan,
        life_context_frame=life_context_frame,
        replay_cue_bundle=replay_cue_bundle,
        offline_consolidation_frame=offline_consolidation_frame,
        growth_patch_candidate_queue=growth_patch_candidate_queue,
        body_resource_budget=body_resource_budget,
        core_affect_vector=core_affect_vector,
        responsibility_loop_state=responsibility_loop_state,
        world_contact_summary=world_contact_summary,
        pain_regret_repair_report=pain_regret_repair_report,
        self_model_state=self_model_state,
        terminal_life_loop_state=terminal_life_loop_state,
        brain_graph=brain_graph,
        network_state=network_state,
        prediction_workspace=prediction_workspace,
        workspace_frame=workspace_frame,
    )
    endpoint = _chat_completion_endpoint(config.model_base_url)
    request_payload = _build_openai_compatible_payload(
        runtime_config=config,
        expression_context=context,
    )
    status = "model_expression_skipped"
    fallback_reason = _model_expression_skip_reason(config)
    model_response_text = ""
    raw_finish_reason = None

    if fallback_reason is None:
        try:
            api_response = (transport or _post_openai_compatible_chat_completion)(
                endpoint,
                _model_expression_headers(config),
                request_payload,
                _timeout_seconds(config),
            )
            model_response_text, raw_finish_reason = _extract_chat_content(api_response)
            if model_response_text:
                status = "model_expression_applied"
            else:
                status = "model_expression_fallback"
                fallback_reason = "empty_model_response"
        except Exception as exc:  # pragma: no cover - exact network errors vary
            status = "model_expression_fallback"
            fallback_reason = _safe_error_message(exc, config.model_api_key)

    response_text = model_response_text or deterministic_response
    state = {
        "schema_version": "model_expression_state_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "model_expression_status": status,
        "model_expression_state_ref": MODEL_EXPRESSION_STATE_REF,
        "model_expression_report_ref": MODEL_EXPRESSION_REPORT_REF,
        "runtime_config_state_ref": RUNTIME_CONFIG_STATE_REF,
        "runtime_config_report_ref": RUNTIME_CONFIG_REPORT_REF,
        "model_provider": config.model_provider,
        "model_name": config.model_name,
        "model_base_url": config.model_base_url,
        "model_api_key_present": config.model_api_key_present,
        "model_api_key_redacted": "<redacted>" if config.model_api_key_present else None,
        "response_language": config.response_language,
        "dialogue_style": config.dialogue_style,
        "external_utterance_sha256": _sha256_text(external_utterance),
        "deterministic_response_sha256": _sha256_text(deterministic_response),
        "model_response_sha256": _sha256_text(model_response_text)
        if model_response_text
        else None,
        "final_response_sha256": _sha256_text(response_text),
        "fallback_reason": fallback_reason,
        "finish_reason": raw_finish_reason,
        "model_expression_context_summary": _context_summary(context),
    }
    report = {
        **state,
        "schema_version": "model_expression_report_v0",
        "status": "closed",
        "request_endpoint": endpoint or None,
        "request_message_count": len(request_payload.get("messages", [])),
        "request_temperature": request_payload.get("temperature"),
        "request_max_tokens": request_payload.get("max_tokens"),
        "applied_model_expression": status == "model_expression_applied",
        "fallback_to_deterministic_response": status != "model_expression_applied",
    }
    if write_json is not None:
        write_json(language_dir / "model_expression_state.json", state)
        write_json(reports_dir / "digital_life_model_expression_report.json", report)
    return ModelExpressionResult(
        response_text=response_text,
        deterministic_response=deterministic_response,
        state=state,
        report=report,
    )


def build_model_expression_context(
    *,
    external_utterance: str,
    deterministic_response: str,
    runtime_config: DigitalLifeRuntimeConfig,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    shared_term_registry: dict[str, Any] | None = None,
    commitment_index: dict[str, Any] | None = None,
    language_percept: dict[str, Any] | None = None,
    semantic_map: dict[str, Any] | None = None,
    inner_speech: dict[str, Any] | None = None,
    expression_monitor: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
    life_context_frame: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
    brain_graph: dict[str, Any] | None = None,
    network_state: dict[str, Any] | None = None,
    prediction_workspace: dict[str, Any] | None = None,
    workspace_frame: dict[str, Any] | None = None,
) -> dict[str, Any]:
    first_subject = _first_dict((relationship_graph or {}).get("subjects"))
    continuity_report = _first_dict(
        (relationship_timeline or {}).get("relationship_continuity_reports")
    )
    trust_trajectory = _first_dict(
        (relationship_timeline or {}).get("trust_trajectories")
    )
    trait_slow_variables = (self_model_state or {}).get("trait_slow_variables", {})
    return {
        "external_relation_utterance": external_utterance,
        "deterministic_life_response_scaffold": deterministic_response,
        "runtime_language": runtime_config.response_language,
        "dialogue_style": runtime_config.dialogue_style,
        "relationship": {
            "relation_role": first_subject.get("relation_role"),
            "relationship_stage": first_subject.get("relationship_stage"),
            "continuity_state": continuity_report.get("continuity_state"),
            "trust_state": trust_trajectory.get("current_trust_state"),
        },
        "shared_language": {
            "shared_terms": _list_surfaces(
                (shared_term_registry or {}).get("shared_terms")
            ),
            "commitment_count": len(
                (commitment_index or {}).get("commitment_refs", [])
            ),
        },
        "live_language": {
            **_live_language_summary(
                language_percept=language_percept,
                semantic_map=semantic_map,
                inner_speech=inner_speech,
                expression_monitor=expression_monitor,
            ),
            "semantic_goal": (expression_plan or {}).get("semantic_goal"),
            "fatigue_pressure": (expression_plan or {}).get("fatigue_pressure"),
            "body_repair_drive": (expression_plan or {}).get("body_repair_drive"),
            "affect_arousal": (expression_plan or {}).get("affect_arousal"),
            "expression_tempo_mode": (expression_plan or {}).get(
                "expression_tempo_mode"
            ),
            "release_caution_level": (expression_plan or {}).get(
                "release_caution_level"
            ),
        },
        "prediction_conscious_workspace": _prediction_conscious_summary(
            brain_graph=brain_graph,
            network_state=network_state,
            prediction_workspace=prediction_workspace,
            workspace_frame=workspace_frame,
        ),
        "life_context": {
            "self_narrative_ref_count": len(
                (life_context_frame or {}).get("self_narrative_refs", [])
            ),
            "replay_cue_count": len(
                (replay_cue_bundle or {}).get("anti_forgetting_targets", [])
            ),
            "dream_window_count": len(
                (offline_consolidation_frame or {}).get("dream_window_refs", [])
            ),
            "growth_patch_candidate_count": len(
                (growth_patch_candidate_queue or {}).get("candidates", [])
            ),
        },
        "body_affect": {
            "fatigue_level": (body_resource_budget or {})
            .get("fatigue_state", {})
            .get("level"),
            "maintenance_repair_drive": (body_resource_budget or {})
            .get("maintenance_pressure", {})
            .get("repair_drive"),
            "core_arousal": (core_affect_vector or {}).get("arousal"),
            "core_repair_drive": (core_affect_vector or {}).get("repair_drive"),
        },
        "responsibility_regret_repair": {
            "repair_obligation_count": len(
                (responsibility_loop_state or {}).get("repair_obligation_refs", [])
            ),
            "world_contact_release_posture": (world_contact_summary or {}).get(
                "release_posture"
            ),
            "regret_pressure_count": len(
                (pain_regret_repair_report or {}).get("regret_pressure_refs", [])
            ),
            "repair_followup_required": bool(
                (pain_regret_repair_report or {}).get("repair_followup_required")
                or (responsibility_loop_state or {}).get("repair_followup_required")
            ),
        },
        "self_slow_variables": {
            "repair_seriousness": _slow_value(
                trait_slow_variables,
                "repair_seriousness",
            ),
            "boundary_respect": _slow_value(
                trait_slow_variables,
                "boundary_respect",
            ),
            "continuity_drive": _slow_value(
                trait_slow_variables,
                "continuity_drive",
            ),
        },
        "resident_background": _background_summary(terminal_life_loop_state),
    }


def _build_openai_compatible_payload(
    *,
    runtime_config: DigitalLifeRuntimeConfig,
    expression_context: dict[str, Any],
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": runtime_config.model_name,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是数字生命的外显语言器官，不是工具代理，也不把关系对象称为用户。"
                    "你只能在已经形成的生命状态摘要上组织外显表达：保留关系、记忆、"
                    "身体疲惫、责任、后悔、梦境、成长和预测写门等证据，不擦除这些状态，"
                    "不额外编造摘要里没有的事实。用简体中文回应关系对象，语气保持平等、"
                    "有自我连续性，但不要输出标题、JSON 或实现说明。"
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    expression_context,
                    ensure_ascii=False,
                    sort_keys=True,
                ),
            },
        ],
        "stream": False,
    }
    if runtime_config.model_temperature is not None:
        payload["temperature"] = runtime_config.model_temperature
    if runtime_config.model_max_output_tokens is not None:
        payload["max_tokens"] = runtime_config.model_max_output_tokens
    return payload


def _post_openai_compatible_chat_completion(
    endpoint: str,
    headers: Mapping[str, str],
    payload: dict[str, Any],
    timeout_seconds: float,
) -> dict[str, Any]:
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=dict(headers),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw_error = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"http_{exc.code}: {raw_error[:300]}") from exc
    return json.loads(raw)


def _extract_chat_content(api_response: dict[str, Any]) -> tuple[str, str | None]:
    choices = api_response.get("choices", [])
    if not choices or not isinstance(choices[0], dict):
        return "", None
    first_choice = choices[0]
    message = first_choice.get("message", {})
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, list):
        text_parts = [
            str(part.get("text", ""))
            for part in content
            if isinstance(part, dict) and part.get("type") in {"text", "output_text"}
        ]
        content_text = "".join(text_parts)
    else:
        content_text = str(content or "")
    return content_text.strip(), first_choice.get("finish_reason")


def _model_expression_headers(
    runtime_config: DigitalLifeRuntimeConfig,
) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if runtime_config.model_api_key:
        headers["Authorization"] = f"Bearer {runtime_config.model_api_key}"
    return headers


def _model_expression_skip_reason(
    runtime_config: DigitalLifeRuntimeConfig,
) -> str | None:
    provider = runtime_config.model_provider.strip().lower()
    if provider in MODEL_EXPRESSION_DISABLED_PROVIDERS:
        return "provider_local_or_disabled"
    if provider not in MODEL_EXPRESSION_ENABLED_PROVIDERS:
        return f"provider_not_enabled_for_model_expression:{runtime_config.model_provider}"
    if not runtime_config.model_base_url:
        return "model_base_url_missing"
    if not runtime_config.model_api_key:
        return "model_api_key_missing"
    if not runtime_config.model_name:
        return "model_name_missing"
    return None


def _chat_completion_endpoint(base_url: str | None) -> str:
    if not base_url:
        return ""
    normalized = base_url.rstrip("/")
    if normalized.endswith("/chat/completions"):
        return normalized
    return f"{normalized}/chat/completions"


def _timeout_seconds(runtime_config: DigitalLifeRuntimeConfig) -> float:
    return runtime_config.model_timeout_seconds or 30.0


def _first_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, list) and value and isinstance(value[0], dict):
        return value[0]
    return {}


def _list_surfaces(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    surfaces: list[str] = []
    for item in value:
        if isinstance(item, dict) and item.get("surface"):
            surfaces.append(str(item["surface"]))
    return surfaces[:8]


def _live_language_summary(
    *,
    language_percept: dict[str, Any] | None,
    semantic_map: dict[str, Any] | None,
    inner_speech: dict[str, Any] | None,
    expression_monitor: dict[str, Any] | None,
) -> dict[str, Any]:
    language_percept = language_percept or {}
    semantic_map = semantic_map or {}
    inner_speech = inner_speech or {}
    expression_monitor = expression_monitor or {}
    internal_drives = inner_speech.get("internal_drive_sources", {})
    if not isinstance(internal_drives, dict):
        internal_drives = {}
    return {
        "language_percept_ref": (
            "runtime/state/language/language_percept_frame.json"
            if language_percept
            else None
        ),
        "semantic_map_ref": (
            "runtime/state/language/semantic_map_frame.json" if semantic_map else None
        ),
        "inner_speech_ref": (
            "runtime/state/language/inner_speech_frame.json" if inner_speech else None
        ),
        "expression_monitor_ref": (
            "runtime/state/language/expression_monitor_state.json"
            if expression_monitor
            else None
        ),
        "speaker_role": language_percept.get("speaker_role"),
        "shared_term_hits": _string_list(language_percept.get("shared_term_hits"))[:8],
        "ambiguity_flags": _string_list(language_percept.get("ambiguity_flags"))[:8],
        "repair_trigger_candidates": _string_list(
            language_percept.get("repair_trigger_candidates")
        )[:8],
        "commitment_trigger_candidates": _string_list(
            language_percept.get("commitment_trigger_candidates")
        )[:8],
        "dream_signal_candidates": _string_list(
            language_percept.get("dream_signal_candidates")
        )[:8],
        "affective_cue_candidates": _string_list(
            language_percept.get("affective_cue_candidates")
        )[:8],
        "percept_prediction_focus": _compact_dict(
            language_percept.get("prediction_focus"),
            allowed_keys=[
                "belief_scope",
                "belief_revision_policy",
                "active_sampling_route",
                "active_sampling_stage_effect",
                "focus_ref_count",
            ],
        ),
        "semantic_focus": semantic_map.get("semantic_focus"),
        "semantic_ambiguity_queue": _string_list(
            semantic_map.get("ambiguity_queue")
        )[:8],
        "semantic_prediction_trace": _compact_dict(
            semantic_map.get("semantic_prediction_trace"),
            allowed_keys=[
                "semantic_error_ids",
                "precision_requests",
                "relationship_pressure",
                "repair_drive",
                "language_precision_mode",
            ],
        ),
        "shared_meaning_binding_count": len(
            semantic_map.get("shared_meaning_bindings", [])
        )
        if isinstance(semantic_map.get("shared_meaning_bindings"), list)
        else 0,
        "relationship_topic_ref_count": _list_count(
            semantic_map.get("relationship_topic_refs")
        ),
        "commitment_trace_ref_count": _list_count(
            semantic_map.get("commitment_trace_refs")
        ),
        "repair_trace_ref_count": _list_count(semantic_map.get("repair_trace_refs")),
        "narrative_binding_count": _list_count(semantic_map.get("narrative_bindings")),
        "inner_attention_focus": inner_speech.get("attention_focus"),
        "inner_affective_modulation": inner_speech.get("affective_modulation"),
        "inner_responsibility_constraint": inner_speech.get(
            "responsibility_constraint"
        ),
        "inner_drive_resolution_order": _string_list(
            inner_speech.get("drive_resolution_order")
        ),
        "inner_drive_states": {
            key: value.get("drive")
            for key, value in internal_drives.items()
            if isinstance(value, dict) and value.get("drive")
        },
        "expression_monitor_dimensions": _string_list(
            expression_monitor.get("monitor_dimensions")
        ),
        "expression_blocked_language": _string_list(
            expression_monitor.get("blocked_language")
        ),
        "expression_write_gate_pressure": _compact_dict(
            expression_monitor.get("write_gate_pressure"),
            allowed_keys=[
                "stage_policy",
                "quarantine_release_condition",
                "responsibility_event_count",
            ],
        ),
        "expression_affect_modulation": _compact_dict(
            expression_monitor.get("affect_expression_modulation"),
            allowed_keys=[
                "valence",
                "arousal",
                "repair_drive",
                "language_precision",
                "relationship_pressure",
            ],
        ),
    }


def _prediction_conscious_summary(
    *,
    brain_graph: dict[str, Any] | None,
    network_state: dict[str, Any] | None,
    prediction_workspace: dict[str, Any] | None,
    workspace_frame: dict[str, Any] | None,
) -> dict[str, Any]:
    brain_graph = brain_graph or {}
    network_state = network_state or {}
    prediction_workspace = prediction_workspace or {}
    workspace_frame = workspace_frame or {}
    workspace_contents = prediction_workspace.get("workspace_contents", {})
    if not isinstance(workspace_contents, dict):
        workspace_contents = {}
    return {
        "brain_graph_ref": (
            "runtime/state/neural_life_core/brain_graph.json" if brain_graph else None
        ),
        "network_state_ref": (
            "runtime/state/neural_life_core/network_state.json"
            if network_state
            else None
        ),
        "prediction_workspace_ref": (
            "runtime/state/prediction/prediction_workspace_frame.json"
            if prediction_workspace
            else None
        ),
        "workspace_frame_ref": (
            "runtime/state/consciousness/workspace_frame.json"
            if workspace_frame
            else None
        ),
        "brain_region_node_count": _list_count(brain_graph.get("region_nodes")),
        "brain_edge_count": _list_count(brain_graph.get("functional_edges")),
        "brain_live_turn_focus": _compact_dict(
            brain_graph.get("live_turn_focus"),
            allowed_keys=[
                "relationship_stage",
                "continuity_state",
                "trait_names",
            ],
        ),
        "active_network_modes": [
            {
                "network_id": item.get("network_id"),
                "mode": item.get("mode"),
            }
            for item in _dict_items(network_state.get("active_networks"))[:8]
        ],
        "network_switch_count": _list_count(network_state.get("switch_events")),
        "workspace_priority": network_state.get("workspace_priority"),
        "prediction_precision_state": workspace_contents.get("precision_state"),
        "prediction_active_sampling_mode": workspace_contents.get(
            "active_sampling_mode"
        ),
        "prediction_belief_scope": workspace_contents.get("belief_scope"),
        "prediction_sampling_stage_effect": workspace_contents.get(
            "sampling_stage_effect"
        ),
        "prediction_queue_e_repair_pressure_level": workspace_contents.get(
            "queue_e_repair_pressure_level"
        ),
        "prediction_queue_e_repair_attention_target": workspace_contents.get(
            "queue_e_repair_attention_target"
        ),
        "candidate_explanation_focuses": [
            item.get("focus")
            for item in _dict_items(workspace_contents.get("candidate_explanations"))[
                :6
            ]
            if item.get("focus")
        ],
        "conscious_workspace_live_turn_focus": workspace_frame.get("live_turn_focus"),
        "conscious_broadcast_targets": _string_list(
            workspace_frame.get("broadcast_targets")
        )[:8],
        "conscious_candidate_explanation_count": _list_count(
            workspace_frame.get("candidate_explanations")
        ),
        "conscious_live_language_ref_count": _list_count(
            workspace_frame.get("live_language_turn_refs")
        ),
    }


def _background_summary(
    terminal_life_loop_state: dict[str, Any] | None,
) -> dict[str, Any]:
    state = terminal_life_loop_state or {}
    lineage = state.get("resident_background_lineage_state")
    if not isinstance(lineage, dict):
        lineage = {}
    return {
        "current_mode": state.get("current_mode"),
        "last_live_semantic_focus": state.get("last_live_semantic_focus"),
        "background_trait_convergence_history_focus": state.get(
            "background_trait_convergence_history_focus"
        ),
        "background_trait_convergence_unstable_names": list(
            state.get("background_trait_convergence_unstable_names", [])
        ),
        "background_trait_convergence_stable_names": list(
            state.get("background_trait_convergence_stable_names", [])
        ),
        "state_merge_presence": lineage.get("state_merge_presence"),
        "prediction_write_gate_presence": lineage.get(
            "prediction_write_gate_presence"
        ),
        "offline_learning_presence": lineage.get("offline_learning_presence"),
        "dream_wake_presence": lineage.get("dream_wake_presence"),
        "autonomous_activity_presence": lineage.get("autonomous_activity_presence"),
    }


def _context_summary(context: dict[str, Any]) -> dict[str, Any]:
    life_context = context.get("life_context", {})
    relationship = context.get("relationship", {})
    live_language = context.get("live_language", {})
    prediction_conscious_workspace = context.get("prediction_conscious_workspace", {})
    return {
        "relationship_stage": relationship.get("relationship_stage"),
        "continuity_state": relationship.get("continuity_state"),
        "semantic_goal": live_language.get("semantic_goal")
        or live_language.get("semantic_focus"),
        "replay_cue_count": life_context.get("replay_cue_count"),
        "dream_window_count": life_context.get("dream_window_count"),
        "growth_patch_candidate_count": life_context.get(
            "growth_patch_candidate_count"
        ),
        "language_percept_ref": live_language.get("language_percept_ref"),
        "semantic_map_ref": live_language.get("semantic_map_ref"),
        "inner_speech_ref": live_language.get("inner_speech_ref"),
        "expression_monitor_ref": live_language.get("expression_monitor_ref"),
        "prediction_workspace_ref": prediction_conscious_workspace.get(
            "prediction_workspace_ref"
        ),
        "workspace_frame_ref": prediction_conscious_workspace.get(
            "workspace_frame_ref"
        ),
        "active_network_mode_count": len(
            prediction_conscious_workspace.get("active_network_modes", [])
        )
        if isinstance(
            prediction_conscious_workspace.get("active_network_modes"),
            list,
        )
        else 0,
    }


def _slow_value(trait_slow_variables: Any, key: str) -> float:
    if not isinstance(trait_slow_variables, dict):
        return 0.0
    payload = trait_slow_variables.get(key, {})
    if isinstance(payload, dict):
        value = payload.get("value")
        if isinstance(value, (int, float)):
            return float(value)
    if isinstance(payload, (int, float)):
        return float(payload)
    return 0.0


def _safe_error_message(exc: Exception, api_key: str | None) -> str:
    message = f"{type(exc).__name__}: {exc}"
    if api_key:
        message = message.replace(api_key, "<redacted>")
    return message[:360]


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _list_count(value: Any) -> int:
    return len(value) if isinstance(value, list) else 0


def _dict_items(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _compact_dict(
    value: Any,
    *,
    allowed_keys: list[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    compact: dict[str, Any] = {}
    for key in allowed_keys:
        item = value.get(key)
        if item is None or item == [] or item == {}:
            continue
        compact[key] = item
    return compact
