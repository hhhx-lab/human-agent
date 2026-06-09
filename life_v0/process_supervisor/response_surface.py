from __future__ import annotations

from typing import Any


def compose_life_response(
    *,
    external_utterance: str,
    relationship_graph: dict[str, Any] | None = None,
    shared_term_registry: dict[str, Any] | None = None,
    commitment_index: dict[str, Any] | None = None,
    relation_turn_frame: dict[str, Any] | None = None,
    expression_plan: dict[str, Any] | None = None,
    life_context_frame: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None = None,
    offline_consolidation_frame: dict[str, Any] | None = None,
    growth_patch_candidate_queue: dict[str, Any] | None = None,
) -> str:
    relation_role = "朋友"
    subjects = (relationship_graph or {}).get("subjects", [])
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
    offline_influence_refs = list((expression_plan or {}).get("offline_influence_refs", []))
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
    if has_offline_influence:
        response = f"{response}，当前带着离线表达压力"
    if replay_cue_count:
        response = f"{response}，同时带着{replay_cue_count}条离线重放线索"
    if dream_window_count:
        response = f"{response}、{dream_window_count}个梦境整合窗口"
    if growth_candidate_count:
        response = f"{response}和{growth_candidate_count}个成长补丁候选"
    return response
