from __future__ import annotations

import hashlib
from typing import Any

LANGUAGE_PERCEPT_REF = "runtime/state/language/language_percept_frame.json"
VISUAL_OBSERVATION_REF = "runtime/state/observation/visual_observation.json"
WORLD_CONTACT_SUMMARY_REF = "runtime/state/membrane/world_contact_summary.json"
RESPONSIBILITY_LOOP_STATE_REF = "runtime/state/action/responsibility_loop_state.json"
WORLD_OBSERVATION_ROUTE_REF = "runtime/state/observation/world_observation_route.json"
PERIPHERY_NORMALIZATION_REF = (
    "runtime/state/observation/periphery_normalization_trace.json"
)
SIGNAL_MEDIA_RUNTIME_REF = "runtime/state/signal/signal_media_runtime.json"

SOURCE_DOC_REFS = [
    "docs/17_memory_trace_object_model.md",
    "docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md",
    "docs/real—live0/07_memory_engram_and_state_store.md",
]


def collect_cross_modal_source_evidence(
    *,
    language_percept: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    world_observation_route: dict[str, Any] | None = None,
    periphery_normalization_trace: dict[str, Any] | None = None,
    visual_observation: dict[str, Any] | None = None,
    action_outcome_refs: list[str] | None = None,
    percept_frame_present: bool = False,
    world_contact_present: bool = False,
    visual_percept_present: bool = False,
) -> dict[str, Any]:
    cross_modal_refs: list[str] = []
    evidence_modalities: list[str] = []

    if percept_frame_present or language_percept:
        cross_modal_refs.append(LANGUAGE_PERCEPT_REF)
        evidence_modalities.append("language_percept")
        percept_cues = _string_list((language_percept or {}).get("percept_cue_refs"))
        cross_modal_refs.extend(percept_cues)

    if world_contact_present or world_contact_summary:
        cross_modal_refs.append(WORLD_CONTACT_SUMMARY_REF)
        evidence_modalities.append("world_contact")
        contact_refs = _string_list(
            (world_contact_summary or {}).get("contact_event_refs")
        ) + _string_list((world_contact_summary or {}).get("observation_refs"))
        cross_modal_refs.extend(contact_refs)

    responsibility = responsibility_loop_state or {}
    repair_refs = _string_list(responsibility.get("repair_obligation_refs"))
    action_refs = _string_list(responsibility.get("action_outcome_refs"))
    if repair_refs or action_refs:
        cross_modal_refs.append(RESPONSIBILITY_LOOP_STATE_REF)
        evidence_modalities.append("action_responsibility")
        cross_modal_refs.extend(repair_refs + action_refs)

    cross_modal_refs.extend(_string_list(action_outcome_refs))
    if action_outcome_refs:
        evidence_modalities.append("action_outcome")

    signal_media = signal_media_runtime or {}
    body_signal_profile = signal_media.get("body_signal_profile") or {}
    visual_refs = _string_list(body_signal_profile.get("visual_channel_refs")) + _string_list(
        body_signal_profile.get("visual_observation_refs")
    )
    if signal_media or visual_refs or visual_percept_present:
        cross_modal_refs.append(SIGNAL_MEDIA_RUNTIME_REF)
        evidence_modalities.append("signal_media")
        cross_modal_refs.extend(visual_refs)

    observation = world_observation_route or {}
    observation_refs = _string_list(observation.get("observation_refs")) + _string_list(
        observation.get("visual_scene_refs")
    )
    if observation_refs or visual_percept_present:
        cross_modal_refs.append(WORLD_OBSERVATION_ROUTE_REF)
        evidence_modalities.append("visual_percept")
        cross_modal_refs.extend(observation_refs)

    visual = visual_observation or {}
    if visual:
        cross_modal_refs.append(VISUAL_OBSERVATION_REF)
        if visual.get("encoder_available"):
            evidence_modalities.append("visual_percept")
            embedding_ref = visual.get("visual_embedding_ref")
            if embedding_ref:
                cross_modal_refs.append(str(embedding_ref))
        elif visual.get("status") == "degraded":
            cross_modal_refs.append(f"{VISUAL_OBSERVATION_REF}#degraded")

    periphery = periphery_normalization_trace or {}
    promoted = _string_list(periphery.get("promoted_channels"))
    visual_channels = [channel for channel in promoted if "visual" in channel.lower()]
    if periphery or visual_channels:
        cross_modal_refs.append(PERIPHERY_NORMALIZATION_REF)
        if visual_channels:
            evidence_modalities.append("visual_percept")
        cross_modal_refs.extend(
            [f"{PERIPHERY_NORMALIZATION_REF}#{channel}" for channel in visual_channels]
        )

    if world_contact_summary:
        cross_modal_refs.extend(
            _string_list(world_contact_summary.get("active_sampling_expected_observation_refs"))
        )

    cross_modal_refs = _dedupe(cross_modal_refs)
    evidence_modalities = _dedupe(evidence_modalities)
    feature_bundle = build_cross_modal_feature_bundle(
        language_percept=language_percept,
        world_contact_summary=world_contact_summary,
        signal_media_runtime=signal_media_runtime,
        world_observation_route=world_observation_route,
        periphery_normalization_trace=periphery_normalization_trace,
        responsibility_loop_state=responsibility_loop_state,
        visual_observation=visual_observation,
        evidence_modalities=evidence_modalities,
        cross_modal_evidence_refs=cross_modal_refs,
    )
    return {
        "schema_version": "cross_modal_source_evidence_v0",
        "cross_modal_evidence_refs": cross_modal_refs,
        "evidence_modalities": evidence_modalities,
        "evidence_modal_count": len(evidence_modalities),
        "first_class_modalities_present": bool(evidence_modalities),
        "cross_modal_feature_bundle": feature_bundle,
        "source_boundary": "cross_modal_refs_are_evidence_not_recall_answers",
        "consumer_refs": [
            "runtime/state/memory/memory_trace_store.json#source_evidence_refs",
            "runtime/state/memory/memory_trace_store.json#cross_modal_feature_bundle",
            "runtime/state/memory/memory_retrieval_frame.json#memory_phenomenology_profile",
        ],
        "source_doc_refs": SOURCE_DOC_REFS,
    }


def build_cross_modal_feature_bundle(
    *,
    language_percept: dict[str, Any] | None = None,
    world_contact_summary: dict[str, Any] | None = None,
    signal_media_runtime: dict[str, Any] | None = None,
    world_observation_route: dict[str, Any] | None = None,
    periphery_normalization_trace: dict[str, Any] | None = None,
    responsibility_loop_state: dict[str, Any] | None = None,
    visual_observation: dict[str, Any] | None = None,
    evidence_modalities: list[str] | None = None,
    cross_modal_evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    percept = language_percept or {}
    world = world_contact_summary or {}
    signal = signal_media_runtime or {}
    observation = world_observation_route or {}
    periphery = periphery_normalization_trace or {}
    responsibility = responsibility_loop_state or {}
    modality_features: list[dict[str, Any]] = []
    if "language_percept" in (evidence_modalities or []):
        modality_features.append(
            {
                "modality": "language_percept",
                "feature_kind": "shared_term_and_repair_cues",
                "feature_vector": _feature_hash(
                    _string_list(percept.get("shared_term_hits"))
                    + _string_list(percept.get("repair_trigger_candidates"))
                ),
                "cue_count": len(_string_list(percept.get("shared_term_hits"))),
            }
        )
    if "visual_percept" in (evidence_modalities or []):
        scene_refs = _string_list(observation.get("visual_scene_refs"))
        promoted_channels = _string_list(periphery.get("promoted_channels"))
        visual_channels = [
            channel for channel in promoted_channels if "visual" in channel.lower()
        ]
        visual = visual_observation or {}
        visual_encoding = visual.get("visual_feature_encoding") or {
            "encoding_kind": "scene_layout_and_channel_fingerprint",
            "layout_fingerprint": _feature_hash("|".join(scene_refs)),
            "channel_fingerprint": _feature_hash("|".join(visual_channels)),
            "scene_layout_dims": len(scene_refs),
            "promoted_visual_channel_count": len(visual_channels),
        }
        modality_features.append(
            {
                "modality": "visual_percept",
                "feature_kind": "scene_and_channel_encoding",
                "feature_vector": _feature_hash(
                    scene_refs
                    + promoted_channels
                    + _string_list([visual.get("visual_embedding_ref")])
                ),
                "scene_ref_count": len(scene_refs),
                "visual_feature_encoding": visual_encoding,
                "visual_observation_status": visual.get("status"),
            }
        )
    if "world_contact" in (evidence_modalities or []):
        modality_features.append(
            {
                "modality": "world_contact",
                "feature_kind": "contact_event_encoding",
                "feature_vector": _feature_hash(
                    _string_list(world.get("contact_event_refs"))
                    + _string_list(world.get("observation_refs"))
                ),
                "contact_event_count": len(_string_list(world.get("contact_event_refs"))),
            }
        )
    if "action_responsibility" in (evidence_modalities or []):
        modality_features.append(
            {
                "modality": "action_responsibility",
                "feature_kind": "repair_and_action_outcome_encoding",
                "feature_vector": _feature_hash(
                    _string_list(responsibility.get("repair_obligation_refs"))
                    + _string_list(responsibility.get("action_outcome_refs"))
                ),
                "obligation_count": len(
                    _string_list(responsibility.get("repair_obligation_refs"))
                ),
            }
        )
    if "signal_media" in (evidence_modalities or []):
        body_signal = signal.get("body_signal_profile") or {}
        modality_features.append(
            {
                "modality": "signal_media",
                "feature_kind": "body_signal_channel_encoding",
                "feature_vector": _feature_hash(
                    _string_list(body_signal.get("visual_channel_refs"))
                    + [str(body_signal.get("memory_write_bias") or "")]
                ),
            }
        )
    return {
        "schema_version": "cross_modal_feature_bundle_v0",
        "bundle_id": f"cross-modal-bundle-{_feature_hash('|'.join(evidence_modalities or []))}",
        "modality_feature_count": len(modality_features),
        "modality_features": modality_features,
        "feature_fingerprint": _feature_hash(
            "|".join(_string_list(cross_modal_evidence_refs))
        ),
        "visual_feature_encoding_present": any(
            feature.get("visual_feature_encoding")
            for feature in modality_features
            if feature.get("modality") == "visual_percept"
        ),
        "encoding_boundary": "feature_bundle_is_engram_evidence_not_recall_answer_text",
    }


def _feature_hash(value: str | list[str]) -> str:
    if isinstance(value, list):
        value = "|".join(str(item) for item in value if item)
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:16]


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, tuple):
        return [str(item) for item in value if item]
    if isinstance(value, set):
        return [str(item) for item in sorted(value) if item]
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