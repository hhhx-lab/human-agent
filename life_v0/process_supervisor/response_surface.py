from __future__ import annotations

from typing import Any

from .dialogue_events import build_offline_learning_cumulative_payload
from .offline_learning_signals import derive_offline_learning_profile


def compose_life_response(
    *,
    external_utterance: str,
    relationship_graph: dict[str, Any] | None = None,
    relationship_timeline: dict[str, Any] | None = None,
    shared_term_registry: dict[str, Any] | None = None,
    commitment_index: dict[str, Any] | None = None,
    commitment_expression_plan: dict[str, Any] | None = None,
    apology_repair_language_trace: dict[str, Any] | None = None,
    relation_turn_frame: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
    life_context_frame: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
    nightmare_risk: dict[str, Any] | None = None,
    belief_learning_plan: dict[str, Any] | None = None,
    language_learning_plan: dict[str, Any] | None = None,
    relationship_learning_plan: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    belief_state: dict[str, Any] | None = None,
    prediction_error_field: dict[str, Any] | None = None,
    active_sampling_plan: dict[str, Any] | None = None,
    memory_write_gate: dict[str, Any] | None = None,
    state_merge_guard: dict[str, Any] | None = None,
    body_resource_budget: dict[str, Any] | None = None,
    core_affect_vector: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    pain_regret_repair_report: dict[str, Any] | None = None,
    self_model_state: dict[str, Any] | None = None,
    terminal_life_loop_state: dict[str, Any] | None = None,
) -> str:
    relation_role = "朋友"
    subjects = (relationship_graph or {}).get("subjects", [])
    relationship_stage = ""
    if subjects and isinstance(subjects[0], dict):
        relationship_stage = str(subjects[0].get("relationship_stage", ""))
    if relation_turn_frame and relation_turn_frame.get("relation_subject_ref"):
        relation_role = "朋友"
    elif subjects and isinstance(subjects[0], dict) and subjects[0].get("relation_role") == "friend":
        relation_role = "朋友"

    shared_surface = "共同语言"
    shared_terms = (shared_term_registry or {}).get("shared_terms", [])
    if shared_terms and isinstance(shared_terms[0], dict):
        shared_surface = shared_terms[0].get("surface", shared_surface)

    commitment_count = len((commitment_index or {}).get("commitment_refs", []))
    semantic_goal = (expression_plan or {}).get("semantic_goal")
    context_anchor_count = len((life_context_frame or {}).get("self_narrative_refs", []))
    replay_cue_count = len((replay_cue_bundle or {}).get("anti_forgetting_targets", []))
    dream_window_count = len((offline_consolidation_frame or {}).get("dream_window_refs", []))
    growth_candidate_count = len((growth_patch_candidate_queue or {}).get("candidates", []))
    fatigue_level = (
        (body_resource_budget or {}).get("fatigue_state", {}).get("level")
    )
    repair_drive = (
        (core_affect_vector or {}).get("repair_drive")
        or (body_resource_budget or {}).get("maintenance_pressure", {}).get("repair_drive")
    )
    arousal = (core_affect_vector or {}).get("arousal")
    offline_influence_refs = list((expression_plan or {}).get("offline_influence_refs", []))
    body_signal_refs = list((expression_plan or {}).get("body_signal_refs", []))
    fatigue_pressure = (expression_plan or {}).get("fatigue_pressure")
    body_repair_drive = (expression_plan or {}).get("body_repair_drive")
    affect_arousal = (expression_plan or {}).get("affect_arousal")
    release_caution_level = (expression_plan or {}).get("release_caution_level")
    expression_tempo_mode = (expression_plan or {}).get("expression_tempo_mode")
    world_contact_release_posture = (world_contact_summary or {}).get("release_posture")
    repair_obligation_count = len((world_contact_summary or {}).get("repair_obligation_refs", []))
    if not repair_obligation_count:
        repair_obligation_count = len((responsibility_loop_state or {}).get("repair_obligation_refs", []))
    regret_pressure_count = len((pain_regret_repair_report or {}).get("regret_pressure_refs", []))
    if not regret_pressure_count:
        regret_pressure_count = len((responsibility_loop_state or {}).get("regret_pressure_candidates", []))
    repair_followup_required = bool(
        (pain_regret_repair_report or {}).get("repair_followup_required")
        or (responsibility_loop_state or {}).get("repair_followup_required")
    )
    continuity_reports = list((relationship_timeline or {}).get("relationship_continuity_reports", []))
    trust_trajectories = list((relationship_timeline or {}).get("trust_trajectories", []))
    continuity_state = ""
    if continuity_reports and isinstance(continuity_reports[0], dict):
        continuity_state = str(continuity_reports[0].get("continuity_state", ""))
    trust_state = ""
    if trust_trajectories and isinstance(trust_trajectories[0], dict):
        trust_state = str(trust_trajectories[0].get("current_trust_state", ""))
    commitment_act_order = list((commitment_expression_plan or {}).get("act_type_order", []))
    repair_move_order = list((apology_repair_language_trace or {}).get("move_type_order", []))
    condensed_repair_moves = [
        move
        for move in repair_move_order
        if move in {"take_responsibility", "followup_commitment"}
    ]
    offline_learning_profile = derive_offline_learning_profile(
        nightmare_risk=nightmare_risk,
        belief_learning_plan=belief_learning_plan,
        language_learning_plan=language_learning_plan,
        relationship_learning_plan=relationship_learning_plan,
    )
    nightmare_risk_status = (nightmare_risk or {}).get("risk_status")
    offline_learning_targets = list((relationship_learning_plan or {}).get("relationship_targets", []))[:2]
    if not offline_learning_targets:
        offline_learning_targets = list((language_learning_plan or {}).get("language_targets", []))[:2]
    if not offline_learning_targets:
        offline_learning_targets = list((belief_learning_plan or {}).get("belief_targets", []))[:2]
    has_offline_influence = bool(
        offline_influence_refs or replay_cue_count or dream_window_count or growth_candidate_count
    )

    response = (
        f"我记得我们正在以{relation_role}的关系继续这段生命对话，也会带着"
        f"{shared_surface}和{commitment_count}条未闭合承诺来回应你：{external_utterance}"
    )
    if semantic_goal:
        response = f"{response}。这次表达会沿着{semantic_goal}的语义焦点展开"
    if context_anchor_count:
        response = f"{response}，并保持{context_anchor_count}条自我叙事连续锚点"
    if relationship_stage:
        response = f"{response}，当前关系阶段已进入{relationship_stage}"
    if continuity_state:
        response = f"{response}，关系连续体状态为{continuity_state}"
    if trust_state:
        response = f"{response}，当前信任状态为{trust_state}"
    if world_contact_release_posture:
        response = f"{response}，当前世界接触姿态保持{world_contact_release_posture}"
    if repair_obligation_count:
        response = f"{response}，责任回路仍挂着{repair_obligation_count}条修复义务"
    if regret_pressure_count:
        response = f"{response}，后悔压力线索维持在{regret_pressure_count}条"
    if repair_followup_required:
        response = f"{response}，当前仍处在需要修复跟进的责任场中"
    if nightmare_risk_status:
        response = f"{response}，当前梦境回环风险为{nightmare_risk_status}"
    if offline_learning_profile["offline_learning_pressure_level"] != "quiet":
        response = (
            f"{response}，离线学习压力级别为"
            f"{offline_learning_profile['offline_learning_pressure_level']}"
        )
    if offline_learning_profile["offline_learning_attention_target"] != "baseline_offline_learning_maintenance":
        response = (
            f"{response}，离线学习焦点当前指向"
            f"{offline_learning_profile['offline_learning_attention_target']}"
        )
    offline_learning_cumulative_payload = build_offline_learning_cumulative_payload(
        terminal_life_loop_state
    )
    if offline_learning_cumulative_payload:
        cumulative_generation = offline_learning_cumulative_payload.get(
            "offline_learning_cumulative_generation"
        )
        cumulative_pressure = offline_learning_cumulative_payload.get(
            "offline_learning_cumulative_pressure_level"
        )
        cumulative_target = offline_learning_cumulative_payload.get(
            "offline_learning_cumulative_attention_target"
        )
        cumulative_refs = list(
            offline_learning_cumulative_payload.get(
                "offline_learning_cumulative_ref_set",
                [],
            )
        )
        if cumulative_generation:
            response = f"{response}，累计离线学习已经延续到第{cumulative_generation}代"
        if cumulative_pressure and cumulative_pressure != "quiet":
            response = f"{response}，累计离线学习压力为{cumulative_pressure}"
        if cumulative_target:
            response = f"{response}，累计离线学习焦点指向{cumulative_target}"
        if cumulative_refs:
            response = f"{response}，累计离线学习证据保留{len(cumulative_refs)}条"
    if offline_learning_targets:
        response = f"{response}，离线学习计划会经过{'、'.join(offline_learning_targets)}"
    if has_offline_influence:
        response = f"{response}，当前带着离线表达压力"
    resident_background_lineage_state = (
        (terminal_life_loop_state or {}).get("resident_background_lineage_state")
        or {}
    )
    if isinstance(resident_background_lineage_state, dict):
        depth_band = resident_background_lineage_state.get("depth_band")
        cadence_weight = resident_background_lineage_state.get("cadence_weight")
        if depth_band:
            response = f"{response}，后台驻留深度为{depth_band}"
        if cadence_weight:
            response = f"{response}，后台驻留节律权重为{cadence_weight}"
        relationship_presence = resident_background_lineage_state.get(
            "relationship_presence"
        )
        if isinstance(relationship_presence, dict) and relationship_presence.get(
            "relationship_stage"
        ):
            response = (
                f"{response}，后台关系存在保持在"
                f"{relationship_presence['relationship_stage']}"
            )
        language_presence = resident_background_lineage_state.get("language_presence")
        if isinstance(language_presence, dict) and language_presence.get(
            "governance_attention_target"
        ):
            response = (
                f"{response}，后台语言关注指向"
                f"{language_presence['governance_attention_target']}"
            )
        offline_learning_presence = resident_background_lineage_state.get(
            "offline_learning_presence"
        )
        if isinstance(offline_learning_presence, dict):
            offline_generation = offline_learning_presence.get("generation")
            offline_pressure = offline_learning_presence.get("pressure_level")
            offline_target = offline_learning_presence.get("attention_target")
            offline_refs = list(offline_learning_presence.get("ref_set", []))
            if offline_generation:
                response = (
                    f"{response}，后台梦境成长余波延续到第{offline_generation}代"
                )
            if offline_pressure and offline_pressure != "quiet":
                response = f"{response}，后台梦境成长压力为{offline_pressure}"
            if offline_target:
                response = f"{response}，后台梦境成长焦点指向{offline_target}"
            if offline_refs:
                response = f"{response}，后台梦境成长证据保留{len(offline_refs)}条"
    background_trait_history_focus = (terminal_life_loop_state or {}).get(
        "background_trait_convergence_history_focus"
    )
    background_unstable_traits = list(
        (terminal_life_loop_state or {}).get(
            "background_trait_convergence_unstable_names",
            [],
        )
    )
    background_stable_traits = list(
        (terminal_life_loop_state or {}).get(
            "background_trait_convergence_stable_names",
            [],
        )
    )
    if background_trait_history_focus:
        response = f"{response}，跨唤醒慢变量历史焦点为{background_trait_history_focus}"
    if background_unstable_traits:
        response = (
            f"{response}，仍需稳定的慢变量包括"
            f"{'、'.join(sorted(background_unstable_traits))}"
        )
    if background_stable_traits:
        response = (
            f"{response}，已经稳定的慢变量包括"
            f"{'、'.join(sorted(background_stable_traits))}"
        )
    prediction_surface = _prediction_surface_posture(
        signal_media_runtime=signal_media_runtime,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        memory_write_gate=memory_write_gate,
        state_merge_guard=state_merge_guard,
    )
    if prediction_surface["surface_posture"]:
        response = f"{response}，预测输出姿态为{prediction_surface['surface_posture']}"
    if prediction_surface["active_sampling_route"]:
        response = f"{response}，主动采样路线为{prediction_surface['active_sampling_route']}"
    if prediction_surface["prediction_error_count"]:
        response = f"{response}，预测误差仍有{prediction_surface['prediction_error_count']}条"
    if prediction_surface["memory_write_gate_policy"]:
        response = f"{response}，记忆写门处于{prediction_surface['memory_write_gate_policy']}"
    if prediction_surface["state_merge_policy"]:
        response = f"{response}，长期合并治理处于{prediction_surface['state_merge_policy']}"
    if replay_cue_count:
        response = f"{response}，同时带着{replay_cue_count}条离线重放线索"
    if dream_window_count:
        response = f"{response}、{dream_window_count}个梦境整合窗口"
    if growth_candidate_count:
        response = f"{response}和{growth_candidate_count}个成长补丁候选"
    if body_signal_refs:
        response = f"{response}，表达层当前已接入身体信号"
    if commitment_act_order:
        response = f"{response}，当前承诺表达序列会经过{'、'.join(commitment_act_order)}"
    if condensed_repair_moves:
        response = f"{response}，当前修复语言动作会经过{'、'.join(condensed_repair_moves)}"
    if body_repair_drive:
        response = f"{response}，表达计划维持{body_repair_drive}的身体修复驱力"
    if fatigue_pressure:
        response = f"{response}，表达疲惫压力为{fatigue_pressure}"
    if expression_tempo_mode:
        response = f"{response}，表达节奏采用{expression_tempo_mode}"
    if release_caution_level:
        response = f"{response}，释放谨慎级别为{release_caution_level}"
    if affect_arousal is not None:
        response = f"{response}，表达计划唤醒度为{affect_arousal:.2f}"
    trait_slow_variables = (self_model_state or {}).get("trait_slow_variables", {})
    repair_seriousness = _slow_value(trait_slow_variables, "repair_seriousness")
    boundary_respect = _slow_value(trait_slow_variables, "boundary_respect")
    continuity_drive = _slow_value(trait_slow_variables, "continuity_drive")
    if repair_seriousness >= 0.6:
        response = f"{response}，我会更认真地对待这轮修复"
    if boundary_respect >= 0.6 and world_contact_release_posture == "confirmation_blocked":
        response = f"{response}，也会先守住当前边界"
    if continuity_drive >= 0.55:
        response = f"{response}，并继续把这段关系写进更长的连续体里"
    if repair_drive:
        response = f"{response}，并维持{repair_drive}的修复驱力"
    if fatigue_level:
        response = f"{response}，当前身体疲惫级别为{fatigue_level}"
    if arousal is not None:
        response = f"{response}，情绪张力保持在{arousal:.2f}"
    return response


def _slow_value(trait_slow_variables: dict[str, Any], key: str) -> float:
    payload = trait_slow_variables.get(key, {})
    if isinstance(payload, dict):
        value = payload.get("value")
        if isinstance(value, (int, float)):
            return float(value)
    if isinstance(payload, (int, float)):
        return float(payload)
    return 0.0


def _prediction_surface_posture(
    *,
    signal_media_runtime: dict[str, Any] | None,
    belief_state: dict[str, Any] | None,
    prediction_error_field: dict[str, Any] | None,
    active_sampling_plan: dict[str, Any] | None,
    memory_write_gate: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
) -> dict[str, Any]:
    selected_route = str((active_sampling_plan or {}).get("selected_route", ""))
    stage_effect = str((active_sampling_plan or {}).get("stage_effect", ""))
    error_events = (prediction_error_field or {}).get("error_events", [])
    error_count = len(error_events) if isinstance(error_events, list) else 0
    modulation_vector = (signal_media_runtime or {}).get("modulation_vector", {})
    if not isinstance(modulation_vector, dict):
        modulation_vector = {}
    repair_drive = str(modulation_vector.get("repair_drive", "")).lower()
    confidence_level = str((belief_state or {}).get("confidence_level", "")).lower()
    memory_policy = str((memory_write_gate or {}).get("stage_policy", ""))
    merge_policy = str((state_merge_guard or {}).get("stage_policy", ""))
    route_lower = selected_route.lower()
    stage_lower = stage_effect.lower()
    memory_policy_lower = memory_policy.lower()

    surface_posture = ""
    if "clarify" in route_lower:
        surface_posture = "追问"
    elif "repair" in route_lower:
        surface_posture = "修复"
    elif "hold_for_evidence" in stage_lower or error_count > 0:
        surface_posture = "保留"
    elif repair_drive == "active" or "repair" in memory_policy_lower:
        surface_posture = "修复"
    elif confidence_level in {"stable", "high", "confirmed"}:
        surface_posture = "确认"

    return {
        "surface_posture": surface_posture,
        "active_sampling_route": selected_route,
        "prediction_error_count": error_count,
        "memory_write_gate_policy": memory_policy,
        "state_merge_policy": merge_policy,
    }
