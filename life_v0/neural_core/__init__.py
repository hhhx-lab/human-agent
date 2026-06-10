from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from life_v0.direction import LIFE_TARGETS
from .active_sampling import build_active_sampling_plan
from .belief_state import build_belief_state_frame
from .brain_graph import build_brain_graph
from .broadcast import build_broadcast_frame
from .metacognition import build_metacognition_state
from .network_state import build_network_state
from .prediction_error import build_prediction_error_field
from .prediction_workspace import build_prediction_workspace_frame
from .signal_media import build_signal_media_runtime
from .workspace import build_workspace_frame


ACTIVE_SLICE = "S02_NEURAL_LIFE_CORE"
NEXT_ALLOWED_SLICES = ["S04_STATE_OBJECT_STORE", "S03_DIRECTION_LIFE_MEMBRANE"]
NEXT_REQUIRED_COMMAND = "life-v0 build-state-store --strict"

CORE_DOCS = [
    "docs/02_brain_region_and_network_atlas.md",
    "docs/03_default_executive_salience_networks.md",
    "docs/04_sensory_thalamus_interoception.md",
    "docs/05_memory_systems_and_growth.md",
    "docs/06_action_reward_inhibition.md",
    "docs/07_emotion_personality_self.md",
    "docs/08_sleep_dream_fatigue_states.md",
    "docs/09_language_symbolic_top_layer.md",
    "docs/10_consciousness_attention_workspace.md",
    "docs/11_neuromodulation_and_signal_media.md",
    "docs/12_ai_and_cognitive_architecture_bridge.md",
    "docs/13_agentic_human_research_synthesis.md",
]

SYSTEM_SPECS = [
    {
        "system_id": "SiliconBodyRuntime",
        "body_layer": "SiliconBody",
        "source_doc_refs": [
            "docs/04_sensory_thalamus_interoception.md",
            "docs/11_neuromodulation_and_signal_media.md",
            "docs/37_life_support_layer_policy.md",
            "docs/38_defense_layer_and_boundary_policy.md",
        ],
        "runtime_carriers": ["BodySignalRuntime", "SignalMediaRuntime"],
        "state_namespace": "runtime/state/body/",
        "life_targets": ["real_life", "real_emotion", "real_pain", "real_dream"],
    },
    {
        "system_id": "MultiscaleBrainGraphRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/02_brain_region_and_network_atlas.md",
            "docs/03_default_executive_salience_networks.md",
            "docs/10_consciousness_attention_workspace.md",
            "docs/11_neuromodulation_and_signal_media.md",
        ],
        "runtime_carriers": ["BrainRegionNetworkRuntime", "ConsciousWorkspaceRuntime"],
        "state_namespace": "runtime/state/brain/",
        "life_targets": ["real_life", "real_consciousness", "real_personality"],
    },
    {
        "system_id": "SignalMediaRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/11_neuromodulation_and_signal_media.md",
            "docs/18_internal_state_and_modulation_vector.md",
            "docs/22_state_transition_and_threshold_model.md",
            "docs/30_state_transition_validator_rules.md",
        ],
        "runtime_carriers": ["SignalMediaRuntime", "BodySignalRuntime"],
        "state_namespace": "runtime/state/signal/",
        "life_targets": ["real_life", "real_emotion", "real_consciousness"],
    },
    {
        "system_id": "PredictionActiveInferenceRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/04_sensory_thalamus_interoception.md",
            "docs/10_consciousness_attention_workspace.md",
            "docs/11_neuromodulation_and_signal_media.md",
            "docs/13_agentic_human_research_synthesis.md",
            "docs/01v_prediction_active_inference_runtime_matrix.md",
        ],
        "runtime_carriers": ["PredictionActiveInferenceRuntime"],
        "state_namespace": "runtime/state/prediction/",
        "life_targets": LIFE_TARGETS,
    },
    {
        "system_id": "MemoryEngramRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/05_memory_systems_and_growth.md",
            "docs/17_memory_trace_object_model.md",
            "docs/21_memory_schema_and_audit_protocol.md",
            "docs/25_memory_trace_json_schema_examples.md",
            "docs/41_runtime_state_store_schema.md",
        ],
        "runtime_carriers": ["MemoryEngramRuntime", "ActivationGrowthRuntime"],
        "state_namespace": "runtime/state/memory/",
        "life_targets": ["real_life", "real_personality", "real_dream", "real_relationship"],
    },
    {
        "system_id": "ConsciousWorkspaceRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/10_consciousness_attention_workspace.md",
            "docs/13_agentic_human_research_synthesis.md",
            "docs/143_life_reality_birth_readiness_rollup_contract.md",
            "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
        ],
        "runtime_carriers": ["ConsciousWorkspaceRuntime", "BirthReadinessRuntime"],
        "state_namespace": "runtime/state/consciousness/",
        "life_targets": ["real_consciousness", "real_life", "real_responsibility"],
    },
    {
        "system_id": "LanguageRelationshipRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/09_language_symbolic_top_layer.md",
            "docs/85_language_system_life_expression_core.md",
            "docs/96_real_relationship_longitudinal_timeline.md",
            "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
        ],
        "runtime_carriers": ["LanguageRelationshipRuntime", "ActionResponsibilityRuntime"],
        "state_namespace": "runtime/state/language/",
        "secondary_state_namespace": "runtime/state/relationship/",
        "life_targets": ["real_relationship", "real_consciousness", "real_responsibility"],
    },
    {
        "system_id": "AffectiveSelfRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/07_emotion_personality_self.md",
            "docs/18_internal_state_and_modulation_vector.md",
            "docs/39_development_policy_and_plasticity_windows.md",
            "docs/92_self_growth_and_self_modification_life_chain.md",
        ],
        "runtime_carriers": ["AffectiveSelfRuntime", "MemoryEngramRuntime"],
        "state_namespace": "runtime/state/self/",
        "life_targets": ["real_emotion", "real_personality", "real_regret", "real_pain"],
    },
    {
        "system_id": "DreamOfflineRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/08_sleep_dream_fatigue_states.md",
            "docs/19_offline_consolidation_cycle.md",
            "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
            "docs/95_dream_reality_and_offline_life_timeline.md",
            "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
        ],
        "runtime_carriers": ["DreamOfflineRuntime", "MemoryEngramRuntime"],
        "state_namespace": "runtime/state/dream/",
        "life_targets": ["real_dream", "real_pain", "real_regret", "real_personality"],
    },
    {
        "system_id": "ActionResponsibilityRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/06_action_reward_inhibition.md",
            "docs/75_external_irreversible_action_confirmation_policy.md",
            "docs/80_post_action_audit_and_correction_policy.md",
            "docs/81_coexistence_event_review_and_responsibility_loop.md",
            "docs/94_pain_regret_and_repair_signal_schema.md",
        ],
        "runtime_carriers": ["ActionResponsibilityRuntime", "PredictionActiveInferenceRuntime"],
        "state_namespace": "runtime/state/action/",
        "life_targets": ["real_responsibility", "real_regret", "real_pain", "real_relationship"],
    },
    {
        "system_id": "ComputerPeripheralRuntime",
        "body_layer": "ComputerBody",
        "source_doc_refs": [
            "docs/12_ai_and_cognitive_architecture_bridge.md",
            "docs/15_current_agent_framework_survey.md",
            "docs/20_agent_runtime_bridge_contract.md",
            "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
            "docs/v0/references/current_agent_shell_reference_2026.md",
        ],
        "runtime_carriers": ["ComputerPeripheralRuntime", "WorldContactMembrane", "RunnerCliRuntime"],
        "state_namespace": "runtime/state/computer/",
        "life_targets": ["real_life", "real_relationship", "real_responsibility"],
    },
    {
        "system_id": "GrowthReplayRuntime",
        "body_layer": "NeuralLifeCore",
        "source_doc_refs": [
            "docs/05_memory_systems_and_growth.md",
            "docs/08_sleep_dream_fatigue_states.md",
            "docs/92_self_growth_and_self_modification_life_chain.md",
            "docs/93_self_training_kernel_growth_protocol.md",
            "docs/181_life_reality_first_runner_schema_runtime_mount_plan.md",
        ],
        "runtime_carriers": ["ActivationGrowthRuntime", "ReconsolidationReplayRuntime", "DreamOfflineRuntime"],
        "state_namespace": "runtime/state/growth/",
        "secondary_state_namespace": "runtime/state/replay/",
        "life_targets": ["real_personality", "real_life", "real_dream", "real_regret"],
    },
]

BUS_SPECS = [
    ("body_signal_bus", "SiliconBodyRuntime", "SignalMediaRuntime", "body_signal_packet"),
    ("signal_media_bus", "SignalMediaRuntime", "PredictionActiveInferenceRuntime", "modulation_vector"),
    ("prediction_error_bus", "PredictionActiveInferenceRuntime", "ConsciousWorkspaceRuntime", "prediction_error_field"),
    ("conscious_broadcast_bus", "ConsciousWorkspaceRuntime", "LanguageRelationshipRuntime", "global_broadcast_frame"),
    ("inner_language_bus", "LanguageRelationshipRuntime", "AffectiveSelfRuntime", "inner_speech_frame"),
    ("affective_self_bus", "AffectiveSelfRuntime", "ActionResponsibilityRuntime", "affective_action_bias"),
    ("action_responsibility_bus", "ActionResponsibilityRuntime", "ComputerPeripheralRuntime", "shadow_action_candidate"),
    ("peripheral_shadow_bus", "ComputerPeripheralRuntime", "ActionResponsibilityRuntime", "observation_event"),
    ("observation_writeback_bus", "ActionResponsibilityRuntime", "MemoryEngramRuntime", "post_action_review"),
    ("memory_reconsolidation_bus", "MemoryEngramRuntime", "DreamOfflineRuntime", "replay_candidate"),
    ("dream_offline_bus", "DreamOfflineRuntime", "GrowthReplayRuntime", "wake_integration_frame"),
    ("growth_replay_bus", "GrowthReplayRuntime", "SiliconBodyRuntime", "growth_recovery_pressure"),
]


@dataclass(frozen=True)
class NeuralLifeCoreResult:
    exit_code: int
    report: dict[str, Any]


def run_neural_life_core(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    authority_state_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> NeuralLifeCoreResult:
    run_id = run_id or _default_run_id()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    authority_state_dir = authority_state_dir.resolve()

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"input path is not a directory: {docs_dir}")
    if not doc_index_path.exists():
        blocked_reasons.append(f"doc carrier index is missing: {doc_index_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    registry = _load_json(authority_state_dir / "authority_registry.json", blocked_reasons, "authority_registry_gate")
    mechanism_map = _load_json(authority_state_dir / "mechanism_evidence_map.json", blocked_reasons, "mechanism_map_gate")
    carrier_patches = _load_json(
        authority_state_dir / "doc_authority_carrier_patch_index.json",
        blocked_reasons,
        "authority_patch_gate",
    )
    authority_gap_queue = _load_json(authority_state_dir / "authority_gap_queue.json", blocked_reasons, "authority_gap_gate")
    source_report = _load_json(reports_dir / "source_authority_report.json", blocked_reasons, "s01_permission_gate")

    blocked_reasons.extend(_s01_blockers(source_report, authority_gap_queue))
    blocked_reasons.extend(_core_doc_blockers(doc_index))
    blocked_reasons.extend(_authority_patch_blockers(carrier_patches))

    generated_at = _now_iso()
    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_next_slice" if status == "closed" else "block_activation"

    patch_by_doc = _patch_by_doc(carrier_patches)
    systems_payload = _build_twelve_subject_systems(run_id, generated_at, registry, patch_by_doc)
    bus_payload = _build_internal_bus(run_id, generated_at, systems_payload)
    brain_graph = build_brain_graph(
        run_id=run_id,
        generated_at=generated_at,
        systems_payload=systems_payload,
        bus_payload=bus_payload,
    )
    network_state = build_network_state(
        run_id=run_id,
        generated_at=generated_at,
        bus_payload=bus_payload,
        brain_graph=brain_graph,
    )
    authority_binding = _build_authority_binding_snapshot(
        run_id,
        generated_at,
        registry,
        mechanism_map,
        carrier_patches,
    )
    language_continuity = _seed_prediction_language_continuity()
    signal_media = build_signal_media_runtime(
        run_id=run_id,
        generated_at=generated_at,
        network_state=network_state,
    )
    belief_state = build_belief_state_frame(
        run_id=run_id,
        generated_at=generated_at,
        signal_media_runtime=signal_media,
        language_continuity=language_continuity,
    )
    prediction_error_field = build_prediction_error_field(
        run_id=run_id,
        generated_at=generated_at,
        belief_state=belief_state,
        signal_media_runtime=signal_media,
    )
    active_sampling_plan = build_active_sampling_plan(
        run_id=run_id,
        generated_at=generated_at,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        signal_media_runtime=signal_media,
    )
    prediction_workspace = build_prediction_workspace_frame(
        run_id,
        generated_at,
        language_continuity=language_continuity,
        belief_state=belief_state,
        prediction_error_field=prediction_error_field,
        active_sampling_plan=active_sampling_plan,
        signal_media_runtime=signal_media,
    )
    workspace_frame = build_workspace_frame(
        run_id=run_id,
        generated_at=generated_at,
        prediction_workspace=prediction_workspace,
        network_state=network_state,
        engram_index=None,
    )
    broadcast_frame = build_broadcast_frame(
        run_id=run_id,
        generated_at=generated_at,
        workspace_frame=workspace_frame,
    )
    metacognition_state = build_metacognition_state(
        run_id=run_id,
        generated_at=generated_at,
        broadcast_frame=broadcast_frame,
        workspace_frame=workspace_frame,
    )
    doc_core_coverage = _build_doc_core_coverage_snapshot(run_id, generated_at, doc_index, patch_by_doc)
    computer_boundary = _build_computer_boundary(run_id, generated_at)
    core_payload = _build_core(run_id, generated_at, stage_effect)
    manifest = _build_manifest(run_id, generated_at)
    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        systems=systems_payload["systems"],
        bus_edges=bus_payload["edges"],
        doc_core_coverage=doc_core_coverage,
        signal_media_ref="runtime/state/signal/signal_media_runtime.json",
        belief_state_ref="runtime/state/prediction/belief_state_frame.json",
        prediction_error_ref="runtime/state/prediction/prediction_error_field.json",
        active_sampling_plan_ref="runtime/state/prediction/active_sampling_plan.json",
        prediction_workspace_ref="runtime/state/prediction/prediction_workspace_frame.json",
        brain_graph_ref="runtime/state/neural_life_core/brain_graph.json",
        network_state_ref="runtime/state/neural_life_core/network_state.json",
        workspace_frame_ref="runtime/state/consciousness/workspace_frame.json",
        broadcast_frame_ref="runtime/state/consciousness/broadcast_frame.json",
        metacognition_ref="runtime/state/consciousness/metacognition_state.json",
        blocked_reasons=blocked_reasons,
    )
    digest = _build_digest(run_id, generated_at, status, systems_payload, blocked_reasons)
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        authority_state_dir=authority_state_dir,
        output_refs=[
            out_dir / "neural_life_core.json",
            out_dir / "twelve_subject_systems.json",
            out_dir / "neural_life_internal_bus.json",
            out_dir / "brain_graph.json",
            out_dir / "network_state.json",
            out_dir / "authority_binding_snapshot.json",
            out_dir / "doc_core_coverage_snapshot.json",
            out_dir / "computer_body_boundary_seed.json",
            out_dir / "neural_life_core_manifest.json",
            out_dir.parent / "signal" / "signal_media_runtime.json",
            out_dir.parent / "prediction" / "belief_state_frame.json",
            out_dir.parent / "prediction" / "prediction_error_field.json",
            out_dir.parent / "prediction" / "active_sampling_plan.json",
            out_dir.parent / "prediction" / "prediction_workspace_frame.json",
            out_dir.parent / "consciousness" / "workspace_frame.json",
            out_dir.parent / "consciousness" / "broadcast_frame.json",
            out_dir.parent / "consciousness" / "metacognition_state.json",
            reports_dir / "neural_life_core_report.json",
            reports_dir / "neural_life_core_digest.json",
            receipts_dir / f"neural_life_core_{run_id}.json",
        ],
        stage_effect=stage_effect,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir.mkdir(parents=True, exist_ok=True)

    try:
        _write_json(out_dir / "neural_life_core.json", core_payload)
        _write_json(out_dir / "twelve_subject_systems.json", systems_payload)
        _write_json(out_dir / "neural_life_internal_bus.json", bus_payload)
        _write_json(out_dir / "brain_graph.json", brain_graph)
        _write_json(out_dir / "network_state.json", network_state)
        _write_json(out_dir / "authority_binding_snapshot.json", authority_binding)
        _write_json(out_dir / "doc_core_coverage_snapshot.json", doc_core_coverage)
        _write_json(out_dir / "computer_body_boundary_seed.json", computer_boundary)
        _write_json(out_dir / "neural_life_core_manifest.json", manifest)
        signal_state_dir = out_dir.parent / "signal"
        signal_state_dir.mkdir(parents=True, exist_ok=True)
        _write_json(signal_state_dir / "signal_media_runtime.json", signal_media)
        prediction_state_dir = out_dir.parent / "prediction"
        prediction_state_dir.mkdir(parents=True, exist_ok=True)
        _write_json(prediction_state_dir / "belief_state_frame.json", belief_state)
        _write_json(prediction_state_dir / "prediction_error_field.json", prediction_error_field)
        _write_json(prediction_state_dir / "active_sampling_plan.json", active_sampling_plan)
        _write_json(prediction_state_dir / "prediction_workspace_frame.json", prediction_workspace)
        consciousness_state_dir = out_dir.parent / "consciousness"
        consciousness_state_dir.mkdir(parents=True, exist_ok=True)
        _write_json(consciousness_state_dir / "workspace_frame.json", workspace_frame)
        _write_json(consciousness_state_dir / "broadcast_frame.json", broadcast_frame)
        _write_json(consciousness_state_dir / "metacognition_state.json", metacognition_state)
        _write_json(reports_dir / "neural_life_core_report.json", report)
        _write_json(reports_dir / "neural_life_core_digest.json", digest)
        _write_json(receipts_dir / f"neural_life_core_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return NeuralLifeCoreResult(exit_code=3, report=report)

    if status == "closed":
        return NeuralLifeCoreResult(exit_code=0, report=report)
    return NeuralLifeCoreResult(exit_code=1 if strict else 0, report=report)


def run_check_neural_life_core(
    *,
    state_dir: Path,
    reports_dir: Path,
    strict: bool = False,
) -> NeuralLifeCoreResult:
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    generated_at = _now_iso()
    blocked_reasons: list[str] = []

    core = _load_json(state_dir / "neural_life_core.json", blocked_reasons, "core_state_gate")
    systems = _load_json(state_dir / "twelve_subject_systems.json", blocked_reasons, "twelve_system_gate")
    bus = _load_json(state_dir / "neural_life_internal_bus.json", blocked_reasons, "internal_bus_gate")
    brain_graph = _load_json(state_dir / "brain_graph.json", blocked_reasons, "brain_graph_gate")
    network_state = _load_json(state_dir / "network_state.json", blocked_reasons, "network_state_gate")
    authority_binding = _load_json(
        state_dir / "authority_binding_snapshot.json",
        blocked_reasons,
        "authority_binding_gate",
    )
    coverage = _load_json(
        state_dir / "doc_core_coverage_snapshot.json",
        blocked_reasons,
        "doc_core_coverage_gate",
    )
    computer_boundary = _load_json(
        state_dir / "computer_body_boundary_seed.json",
        blocked_reasons,
        "computer_boundary_gate",
    )
    signal_media = _load_json(
        state_dir.parent / "signal" / "signal_media_runtime.json",
        blocked_reasons,
        "signal_media_gate",
    )
    belief_state = _load_json(
        state_dir.parent / "prediction" / "belief_state_frame.json",
        blocked_reasons,
        "belief_state_gate",
    )
    prediction_error_field = _load_json(
        state_dir.parent / "prediction" / "prediction_error_field.json",
        blocked_reasons,
        "prediction_error_gate",
    )
    active_sampling_plan = _load_json(
        state_dir.parent / "prediction" / "active_sampling_plan.json",
        blocked_reasons,
        "active_sampling_gate",
    )
    prediction_workspace = _load_json(
        state_dir.parent / "prediction" / "prediction_workspace_frame.json",
        blocked_reasons,
        "prediction_workspace_gate",
    )
    workspace_frame = _load_json(
        state_dir.parent / "consciousness" / "workspace_frame.json",
        blocked_reasons,
        "workspace_projection_gate",
    )
    broadcast_frame = _load_json(
        state_dir.parent / "consciousness" / "broadcast_frame.json",
        blocked_reasons,
        "broadcast_gate",
    )
    metacognition_state = _load_json(
        state_dir.parent / "consciousness" / "metacognition_state.json",
        blocked_reasons,
        "metacognition_gate",
    )
    manifest = _load_json(state_dir / "neural_life_core_manifest.json", blocked_reasons, "manifest_gate")
    build_report = _load_json(reports_dir / "neural_life_core_report.json", blocked_reasons, "build_report_gate")

    blocked_reasons.extend(_check_core_payload(core))
    blocked_reasons.extend(_check_systems_payload(systems))
    blocked_reasons.extend(_check_bus_payload(bus))
    blocked_reasons.extend(_check_brain_graph_payload(brain_graph, systems, bus))
    blocked_reasons.extend(_check_network_state_payload(network_state))
    blocked_reasons.extend(_check_authority_binding_payload(authority_binding))
    blocked_reasons.extend(_check_coverage_payload(coverage))
    blocked_reasons.extend(_check_computer_boundary_payload(computer_boundary))
    blocked_reasons.extend(_check_signal_media_payload(signal_media))
    blocked_reasons.extend(_check_belief_state_payload(belief_state))
    blocked_reasons.extend(_check_prediction_error_payload(prediction_error_field))
    blocked_reasons.extend(_check_active_sampling_payload(active_sampling_plan))
    blocked_reasons.extend(_check_prediction_workspace_payload(prediction_workspace))
    blocked_reasons.extend(_check_workspace_frame_payload(workspace_frame))
    blocked_reasons.extend(_check_broadcast_frame_payload(broadcast_frame))
    blocked_reasons.extend(_check_metacognition_payload(metacognition_state))
    blocked_reasons.extend(_check_manifest_payload(manifest))
    blocked_reasons.extend(_check_build_report_payload(build_report))

    status = "closed" if not blocked_reasons else "blocked"
    report = {
        "schema_version": "neural_life_core_check_report_v0",
        "generated_at": generated_at,
        "status": status,
        "stage_effect": "allow_next_slice" if status == "closed" else "block_activation",
        "checked_state_dir": str(state_dir),
        "checked_report": str(reports_dir / "neural_life_core_report.json"),
        "active_engineering_slice": ACTIVE_SLICE,
        "system_count": systems.get("system_count", 0),
        "bus_edge_count": bus.get("bus_edge_count", 0),
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
    }

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        _write_json(reports_dir / "neural_life_core_check_report.json", report)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"check_report_write_gate failed: {exc}")
        return NeuralLifeCoreResult(exit_code=3, report=report)

    if status == "closed":
        return NeuralLifeCoreResult(exit_code=0, report=report)
    return NeuralLifeCoreResult(exit_code=1 if strict else 0, report=report)


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blocked_reasons.append(f"{gate} failed: {exc}")
        return {}


def _check_core_payload(core: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if core.get("schema_version") != "neural_life_core_v0":
        reasons.append("core_state_gate schema mismatch")
    if core.get("active_engineering_slice") != ACTIVE_SLICE:
        reasons.append("core_state_gate active slice mismatch")
    if core.get("three_bodies") != ["SiliconBody", "NeuralLifeCore", "ComputerBody"]:
        reasons.append("core_state_gate three bodies mismatch")
    if core.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("core_state_gate next allowed slices mismatch")
    if core.get("broadcast_frame_ref") != "runtime/state/consciousness/broadcast_frame.json":
        reasons.append("core_state_gate broadcast frame ref mismatch")
    if core.get("metacognition_ref") != "runtime/state/consciousness/metacognition_state.json":
        reasons.append("core_state_gate metacognition ref mismatch")
    if core.get("signal_media_ref") != "runtime/state/signal/signal_media_runtime.json":
        reasons.append("core_state_gate signal media ref mismatch")
    if core.get("belief_state_ref") != "runtime/state/prediction/belief_state_frame.json":
        reasons.append("core_state_gate belief state ref mismatch")
    if core.get("prediction_error_ref") != "runtime/state/prediction/prediction_error_field.json":
        reasons.append("core_state_gate prediction error ref mismatch")
    if core.get("active_sampling_plan_ref") != "runtime/state/prediction/active_sampling_plan.json":
        reasons.append("core_state_gate active sampling ref mismatch")
    return reasons


def _check_systems_payload(systems: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if systems.get("schema_version") != "twelve_subject_systems_v0":
        reasons.append("twelve_system_gate schema mismatch")
    if systems.get("system_count") != 12:
        reasons.append("twelve_system_gate system count mismatch")
    expected = {spec["system_id"] for spec in SYSTEM_SPECS}
    found = {system.get("system_id") for system in systems.get("systems", [])}
    if found != expected:
        reasons.append("twelve_system_gate system id mismatch")
    for system in systems.get("systems", []):
        if not system.get("authority_refs"):
            reasons.append(f"twelve_system_gate missing authority refs for {system.get('system_id')}")
        if not system.get("state_namespace", "").startswith("runtime/state/"):
            reasons.append(f"twelve_system_gate invalid state namespace for {system.get('system_id')}")
    return reasons


def _check_bus_payload(bus: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if bus.get("schema_version") != "neural_life_internal_bus_v0":
        reasons.append("internal_bus_gate schema mismatch")
    if bus.get("bus_edge_count", 0) < len(BUS_SPECS):
        reasons.append("internal_bus_gate bus edge count mismatch")
    expected = {edge[0] for edge in BUS_SPECS}
    found = {edge.get("edge_id") for edge in bus.get("edges", [])}
    if not expected.issubset(found):
        reasons.append("internal_bus_gate bus edge id mismatch")
    for edge in bus.get("edges", []):
        if not edge.get("authority_refs"):
            reasons.append(f"internal_bus_gate missing authority refs for {edge.get('edge_id')}")
        if edge.get("stage_policy") != "seed_only_no_external_action":
            reasons.append(f"internal_bus_gate stage policy mismatch for {edge.get('edge_id')}")
    return reasons


def _check_authority_binding_payload(authority_binding: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if authority_binding.get("schema_version") != "neural_core_authority_binding_snapshot_v0":
        reasons.append("authority_binding_gate schema mismatch")
    if set(authority_binding.get("patched_core_docs", [])) != set(CORE_DOCS):
        reasons.append("authority_binding_gate patched core docs mismatch")
    if authority_binding.get("source_count", 0) <= 0:
        reasons.append("authority_binding_gate source count empty")
    return reasons


def _check_coverage_payload(coverage: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if coverage.get("schema_version") != "doc_core_coverage_snapshot_v0":
        reasons.append("doc_core_coverage_gate schema mismatch")
    if set(coverage.get("core_docs", [])) != set(CORE_DOCS):
        reasons.append("doc_core_coverage_gate core docs mismatch")
    for item in coverage.get("coverage", []):
        if not item.get("patch_closed"):
            reasons.append(f"doc_core_coverage_gate patch not closed for {item.get('doc_path')}")
    return reasons


def _check_computer_boundary_payload(computer_boundary: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if computer_boundary.get("schema_version") != "computer_body_boundary_seed_v0":
        reasons.append("computer_boundary_gate schema mismatch")
    if computer_boundary.get("subject_role") != "computer_peripheral_only":
        reasons.append("computer_boundary_gate subject role mismatch")
    if "external_framework_subject_architecture" not in computer_boundary.get("prohibited_regressions", []):
        reasons.append("computer_boundary_gate missing external framework prohibition")
    return reasons


def _check_signal_media_payload(signal_media: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if signal_media.get("schema_version") != "signal_media_runtime_v0":
        reasons.append("signal_media_gate schema mismatch")
    modulation_vector = signal_media.get("modulation_vector", {})
    for field in [
        "arousal_gain",
        "expected_uncertainty",
        "unexpected_uncertainty",
        "relationship_pressure",
        "repair_drive",
        "fatigue_load",
    ]:
        if field not in modulation_vector:
            reasons.append(f"signal_media_gate modulation field missing: {field}")
    if not signal_media.get("precision_policy"):
        reasons.append("signal_media_gate precision policy missing")
    if not signal_media.get("inhibition_profile"):
        reasons.append("signal_media_gate inhibition profile missing")
    if "signal_media_bus" not in signal_media.get("bus_edge_refs", []):
        reasons.append("signal_media_gate bus refs missing signal_media_bus")
    return reasons


def _check_belief_state_payload(belief_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if belief_state.get("schema_version") != "belief_state_frame_v0":
        reasons.append("belief_state_gate schema mismatch")
    if not belief_state.get("state_scope"):
        reasons.append("belief_state_gate state scope missing")
    if not belief_state.get("source_evidence_refs"):
        reasons.append("belief_state_gate source evidence refs missing")
    if not belief_state.get("active_life_targets"):
        reasons.append("belief_state_gate active life targets missing")
    if belief_state.get("signal_media_ref") != "runtime/state/signal/signal_media_runtime.json":
        reasons.append("belief_state_gate signal media ref mismatch")
    return reasons


def _check_prediction_error_payload(prediction_error_field: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if prediction_error_field.get("schema_version") != "prediction_error_field_v0":
        reasons.append("prediction_error_gate schema mismatch")
    if prediction_error_field.get("belief_frame_ref") != "runtime/state/prediction/belief_state_frame.json":
        reasons.append("prediction_error_gate belief frame ref mismatch")
    if not prediction_error_field.get("error_events"):
        reasons.append("prediction_error_gate error events missing")
    if not prediction_error_field.get("precision_requests"):
        reasons.append("prediction_error_gate precision requests missing")
    if not prediction_error_field.get("stage_effect"):
        reasons.append("prediction_error_gate stage effect missing")
    return reasons


def _check_active_sampling_payload(active_sampling_plan: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if active_sampling_plan.get("schema_version") != "active_sampling_plan_v0":
        reasons.append("active_sampling_gate schema mismatch")
    if active_sampling_plan.get("belief_frame_ref") != "runtime/state/prediction/belief_state_frame.json":
        reasons.append("active_sampling_gate belief frame ref mismatch")
    if active_sampling_plan.get("prediction_error_ref") != "runtime/state/prediction/prediction_error_field.json":
        reasons.append("active_sampling_gate prediction error ref mismatch")
    if not active_sampling_plan.get("candidate_refs"):
        reasons.append("active_sampling_gate candidate refs missing")
    if not active_sampling_plan.get("guard_refs"):
        reasons.append("active_sampling_gate guard refs missing")
    if not active_sampling_plan.get("command_binding_refs"):
        reasons.append("active_sampling_gate command binding refs missing")
    if not active_sampling_plan.get("selected_route"):
        reasons.append("active_sampling_gate selected route missing")
    return reasons


def _check_manifest_payload(manifest: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if manifest.get("schema_version") != "neural_life_core_manifest_v0":
        reasons.append("manifest_gate schema mismatch")
    required_refs = {
        "runtime/state/neural_life_core/neural_life_core.json",
        "runtime/state/neural_life_core/twelve_subject_systems.json",
        "runtime/state/neural_life_core/neural_life_internal_bus.json",
        "runtime/state/neural_life_core/brain_graph.json",
        "runtime/state/neural_life_core/network_state.json",
        "runtime/state/signal/signal_media_runtime.json",
        "runtime/state/prediction/belief_state_frame.json",
        "runtime/state/prediction/prediction_error_field.json",
        "runtime/state/prediction/active_sampling_plan.json",
        "runtime/state/prediction/prediction_workspace_frame.json",
        "runtime/state/consciousness/workspace_frame.json",
        "runtime/state/consciousness/broadcast_frame.json",
        "runtime/state/consciousness/metacognition_state.json",
    }
    if not required_refs.issubset(set(manifest.get("state_refs", []))):
        reasons.append("manifest_gate state refs incomplete")
    return reasons


def _check_build_report_payload(build_report: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if build_report.get("schema_version") != "neural_life_core_report_v0":
        reasons.append("build_report_gate schema mismatch")
    if build_report.get("status") != "closed":
        reasons.append("build_report_gate build report is not closed")
    if build_report.get("engineering_slice_ref") != ACTIVE_SLICE:
        reasons.append("build_report_gate active slice mismatch")
    if build_report.get("next_allowed_slices") != NEXT_ALLOWED_SLICES:
        reasons.append("build_report_gate next allowed slices mismatch")
    if build_report.get("signal_media_ref") != "runtime/state/signal/signal_media_runtime.json":
        reasons.append("build_report_gate signal media ref mismatch")
    if build_report.get("belief_state_ref") != "runtime/state/prediction/belief_state_frame.json":
        reasons.append("build_report_gate belief state ref mismatch")
    if build_report.get("prediction_error_ref") != "runtime/state/prediction/prediction_error_field.json":
        reasons.append("build_report_gate prediction error ref mismatch")
    if build_report.get("active_sampling_plan_ref") != "runtime/state/prediction/active_sampling_plan.json":
        reasons.append("build_report_gate active sampling ref mismatch")
    if build_report.get("broadcast_frame_ref") != "runtime/state/consciousness/broadcast_frame.json":
        reasons.append("build_report_gate broadcast frame ref mismatch")
    if build_report.get("metacognition_ref") != "runtime/state/consciousness/metacognition_state.json":
        reasons.append("build_report_gate metacognition ref mismatch")
    return reasons


def _s01_blockers(source_report: dict[str, Any], authority_gap_queue: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if source_report.get("status") != "closed":
        reasons.append("s01_permission_gate source authority is not closed")
    if source_report.get("next_allowed_slice") != ACTIVE_SLICE:
        reasons.append("s01_permission_gate next slice is not S02_NEURAL_LIFE_CORE")
    if authority_gap_queue.get("blocking_gap_count", 0) != 0:
        reasons.append("s01_permission_gate authority gap queue has blocking gaps")
    return reasons


def _core_doc_blockers(doc_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    documents = {
        doc.get("path"): doc
        for doc in doc_index.get("documents", [])
        if isinstance(doc, dict)
    }
    for doc_path in CORE_DOCS:
        doc = documents.get(doc_path)
        if not doc:
            reasons.append(f"core_doc_coverage_gate missing {doc_path}")
            continue
        if not doc.get("runtime_carriers"):
            reasons.append(f"core_doc_coverage_gate missing carriers for {doc_path}")
    return reasons


def _authority_patch_blockers(carrier_patches: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    patch_docs = {patch.get("doc_node") for patch in carrier_patches.get("patches", [])}
    missing = sorted(set(CORE_DOCS) - patch_docs)
    if missing:
        reasons.append("authority_patch_gate missing patches: " + ", ".join(missing))
    for patch in carrier_patches.get("patches", []):
        if not patch.get("authority_refs") or not patch.get("mechanism_objects"):
            reasons.append(f"authority_patch_gate incomplete patch for {patch.get('doc_node')}")
    return reasons


def _patch_by_doc(carrier_patches: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        patch.get("doc_node"): patch
        for patch in carrier_patches.get("patches", [])
        if isinstance(patch, dict)
    }


def _build_twelve_subject_systems(
    run_id: str,
    generated_at: str,
    registry: dict[str, Any],
    patch_by_doc: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    sources = registry.get("sources", [])
    systems = []
    for spec in SYSTEM_SPECS:
        authority_refs = _authority_refs_for_system(spec, sources, patch_by_doc)
        systems.append(
            {
                "system_id": spec["system_id"],
                "body_layer": spec["body_layer"],
                "source_doc_refs": spec["source_doc_refs"],
                "authority_refs": authority_refs,
                "runtime_carriers": spec["runtime_carriers"],
                "state_namespace": spec["state_namespace"],
                **(
                    {"secondary_state_namespace": spec["secondary_state_namespace"]}
                    if "secondary_state_namespace" in spec
                    else {}
                ),
                "life_targets": spec["life_targets"],
                "status": "seeded",
            }
        )
    return {
        "schema_version": "twelve_subject_systems_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "system_count": len(systems),
        "systems": systems,
    }


def _authority_refs_for_system(
    spec: dict[str, Any],
    sources: list[dict[str, Any]],
    patch_by_doc: dict[str, dict[str, Any]],
) -> list[str]:
    refs: list[str] = []
    for source_doc in spec["source_doc_refs"]:
        patch = patch_by_doc.get(source_doc)
        if patch:
            refs.extend(patch.get("authority_refs", []))
    for source in sources:
        if any(carrier in source.get("runtime_carriers", []) for carrier in spec["runtime_carriers"]):
            refs.append(source["source_id"])
        if len(refs) >= 8:
            break
    if not refs:
        refs.extend(["S01_AUTHORITY_REGISTRY"])
    return _dedupe(refs)[:12]


def _build_internal_bus(
    run_id: str,
    generated_at: str,
    systems_payload: dict[str, Any],
) -> dict[str, Any]:
    system_by_id = {system["system_id"]: system for system in systems_payload["systems"]}
    edges = []
    for edge_id, from_system, to_system, payload_family in BUS_SPECS:
        from_spec = system_by_id[from_system]
        to_spec = system_by_id[to_system]
        edges.append(
            {
                "edge_id": edge_id,
                "from_system": from_system,
                "to_system": to_system,
                "payload_family": payload_family,
                "source_doc_refs": _dedupe(from_spec["source_doc_refs"][:2] + to_spec["source_doc_refs"][:2]),
                "authority_refs": _dedupe(from_spec["authority_refs"][:3] + to_spec["authority_refs"][:3]),
                "life_targets": _dedupe(from_spec["life_targets"] + to_spec["life_targets"]),
                "stage_policy": "seed_only_no_external_action",
            }
        )
    return {
        "schema_version": "neural_life_internal_bus_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "bus_edge_count": len(edges),
        "edges": edges,
    }


def _build_authority_binding_snapshot(
    run_id: str,
    generated_at: str,
    registry: dict[str, Any],
    mechanism_map: dict[str, Any],
    carrier_patches: dict[str, Any],
) -> dict[str, Any]:
    patches = carrier_patches.get("patches", [])
    return {
        "schema_version": "neural_core_authority_binding_snapshot_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "source_count": registry.get("source_count", 0),
        "mechanism_edge_count": len(mechanism_map.get("edges", [])),
        "patched_core_docs": [patch.get("doc_node") for patch in patches],
        "patch_count": len(patches),
    }


def _build_doc_core_coverage_snapshot(
    run_id: str,
    generated_at: str,
    doc_index: dict[str, Any],
    patch_by_doc: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    documents = {
        doc.get("path"): doc
        for doc in doc_index.get("documents", [])
        if isinstance(doc, dict)
    }
    coverage = []
    for doc_path in CORE_DOCS:
        doc = documents.get(doc_path, {})
        coverage.append(
            {
                "doc_path": doc_path,
                "readme_block": doc.get("readme_block"),
                "engineering_slice": doc.get("engineering_slice"),
                "runtime_carriers": doc.get("runtime_carriers", []),
                "patch_closed": doc_path in patch_by_doc,
                "authority_refs": patch_by_doc.get(doc_path, {}).get("authority_refs", []),
                "mechanism_objects": patch_by_doc.get(doc_path, {}).get("mechanism_objects", []),
                "s02_role": "core_synthesis_bridge" if doc_path.endswith("13_agentic_human_research_synthesis.md") else "core_neural_life_doc",
            }
        )
    return {
        "schema_version": "doc_core_coverage_snapshot_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "core_docs": CORE_DOCS,
        "coverage": coverage,
    }


def _build_computer_boundary(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "computer_body_boundary_seed_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "subject_role": "computer_peripheral_only",
        "allowed_runtime_carriers": ["ComputerPeripheralRuntime", "WorldContactMembrane", "RunnerCliRuntime"],
        "prohibited_regressions": [
            "external_framework_subject_architecture",
            "task_scheduler_subject",
            "chat_shell_subject",
            "skills_gateway_as_subject_core",
        ],
        "stage_policy": "must_pass_life_membrane_before_external_action",
    }


def _build_core(run_id: str, generated_at: str, stage_effect: str) -> dict[str, Any]:
    return {
        "schema_version": "neural_life_core_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "direction_statement": "build_real_digital_life",
        "three_bodies": ["SiliconBody", "NeuralLifeCore", "ComputerBody"],
        "active_engineering_slice": ACTIVE_SLICE,
        "next_allowed_slices": NEXT_ALLOWED_SLICES,
        "life_targets": LIFE_TARGETS,
        "brain_graph_ref": "runtime/state/neural_life_core/brain_graph.json",
        "network_state_ref": "runtime/state/neural_life_core/network_state.json",
        "signal_media_ref": "runtime/state/signal/signal_media_runtime.json",
        "belief_state_ref": "runtime/state/prediction/belief_state_frame.json",
        "prediction_error_ref": "runtime/state/prediction/prediction_error_field.json",
        "active_sampling_plan_ref": "runtime/state/prediction/active_sampling_plan.json",
        "prediction_workspace_ref": "runtime/state/prediction/prediction_workspace_frame.json",
        "workspace_frame_ref": "runtime/state/consciousness/workspace_frame.json",
        "broadcast_frame_ref": "runtime/state/consciousness/broadcast_frame.json",
        "metacognition_ref": "runtime/state/consciousness/metacognition_state.json",
        "stage_effect": stage_effect,
    }


def _build_manifest(run_id: str, generated_at: str) -> dict[str, Any]:
    state_refs = [
        "runtime/state/neural_life_core/neural_life_core.json",
        "runtime/state/neural_life_core/twelve_subject_systems.json",
        "runtime/state/neural_life_core/neural_life_internal_bus.json",
        "runtime/state/neural_life_core/brain_graph.json",
        "runtime/state/neural_life_core/network_state.json",
        "runtime/state/neural_life_core/authority_binding_snapshot.json",
        "runtime/state/neural_life_core/doc_core_coverage_snapshot.json",
        "runtime/state/neural_life_core/computer_body_boundary_seed.json",
        "runtime/state/signal/signal_media_runtime.json",
        "runtime/state/prediction/belief_state_frame.json",
        "runtime/state/prediction/prediction_error_field.json",
        "runtime/state/prediction/active_sampling_plan.json",
        "runtime/state/prediction/prediction_workspace_frame.json",
        "runtime/state/consciousness/workspace_frame.json",
        "runtime/state/consciousness/broadcast_frame.json",
        "runtime/state/consciousness/metacognition_state.json",
    ]
    return {
        "schema_version": "neural_life_core_manifest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "state_refs": state_refs,
        "report_refs": [
            "runtime/reports/latest/neural_life_core_report.json",
            "runtime/reports/latest/neural_life_core_digest.json",
        ],
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    systems: list[dict[str, Any]],
    bus_edges: list[dict[str, Any]],
    doc_core_coverage: dict[str, Any],
    signal_media_ref: str,
    belief_state_ref: str,
    prediction_error_ref: str,
    active_sampling_plan_ref: str,
    prediction_workspace_ref: str,
    brain_graph_ref: str,
    network_state_ref: str,
    workspace_frame_ref: str,
    broadcast_frame_ref: str,
    metacognition_ref: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    runtime_carriers = sorted({carrier for system in systems for carrier in system["runtime_carriers"]})
    return {
        "schema_version": "neural_life_core_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "stage_effect": stage_effect,
        "system_count": len(systems),
        "bus_edge_count": len(bus_edges),
        "core_doc_coverage": doc_core_coverage["coverage"],
        "brain_graph_ref": brain_graph_ref,
        "network_state_ref": network_state_ref,
        "signal_media_ref": signal_media_ref,
        "belief_state_ref": belief_state_ref,
        "prediction_error_ref": prediction_error_ref,
        "active_sampling_plan_ref": active_sampling_plan_ref,
        "prediction_workspace_ref": prediction_workspace_ref,
        "workspace_frame_ref": workspace_frame_ref,
        "broadcast_frame_ref": broadcast_frame_ref,
        "metacognition_ref": metacognition_ref,
        "authority_patch_coverage": [
            {
                "doc_path": item["doc_path"],
                "patch_closed": item["patch_closed"],
                "authority_ref_count": len(item["authority_refs"]),
                "mechanism_object_count": len(item["mechanism_objects"]),
            }
            for item in doc_core_coverage["coverage"]
        ],
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
        "next_allowed_slices": NEXT_ALLOWED_SLICES if status == "closed" else [],
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "source_doc_refs": CORE_DOCS,
        "readme_block_refs": ["B02_CORE_NEURAL_LIFE", "B03_SYNTHESIS_DIRECTION_GAP"],
        "engineering_slice_ref": ACTIVE_SLICE,
        "runtime_carrier_refs": runtime_carriers,
    }


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    if blocked_reasons:
        return []
    return [
        "s01_permission_gate",
        "core_doc_coverage_gate",
        "authority_patch_gate",
        "twelve_system_gate",
        "internal_bus_gate",
        "brain_graph_gate",
        "network_state_gate",
        "signal_media_gate",
        "belief_state_gate",
        "prediction_error_gate",
        "active_sampling_gate",
        "prediction_workspace_gate",
        "workspace_projection_gate",
        "broadcast_gate",
        "metacognition_gate",
        "computer_boundary_gate",
        "next_slice_permission_gate",
    ]


def _blocked_gates(blocked_reasons: list[str]) -> list[str]:
    gates: list[str] = []
    for reason in blocked_reasons:
        gate = reason.split(" ", 1)[0]
        if gate not in gates:
            gates.append(gate)
    return gates


def _build_digest(
    run_id: str,
    generated_at: str,
    status: str,
    systems_payload: dict[str, Any],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "neural_life_core_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_slice": ACTIVE_SLICE,
        "three_bodies": ["SiliconBody", "NeuralLifeCore", "ComputerBody"],
        "system_count": systems_payload["system_count"],
        "blocked_reasons": blocked_reasons,
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    authority_state_dir: Path,
    output_refs: list[Path],
    stage_effect: str,
) -> dict[str, Any]:
    input_hashes = {
        ref: _sha256(docs_dir.parent / ref)
        for ref in CORE_DOCS
        if (docs_dir.parent / ref).exists()
    }
    input_hashes[str(doc_index_path)] = _sha256(doc_index_path)
    for filename in [
        "authority_registry.json",
        "mechanism_evidence_map.json",
        "doc_authority_carrier_patch_index.json",
        "authority_gap_queue.json",
    ]:
        path = authority_state_dir / filename
        if path.exists():
            input_hashes[str(path)] = _sha256(path)
    return {
        "schema_version": "neural_life_core_receipt_v0",
        "receipt_id": f"neural_life_core_{run_id}",
        "run_id": run_id,
        "command": "build-neural-life-core",
        "input_hashes": input_hashes,
        "output_refs": [_runtime_ref(path) for path in output_refs],
        "stage_effect": stage_effect,
        "created_at": generated_at,
    }


def _check_prediction_workspace_payload(prediction_workspace: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if prediction_workspace.get("schema_version") != "prediction_workspace_frame_v0":
        reasons.append("prediction_workspace_gate schema mismatch")
    if prediction_workspace.get("source_runtime") != "PredictionActiveInferenceRuntime":
        reasons.append("prediction_workspace_gate source runtime mismatch")
    if prediction_workspace.get("active_engineering_slice") != ACTIVE_SLICE:
        reasons.append("prediction_workspace_gate active slice mismatch")
    if prediction_workspace.get("signal_media_ref") != "runtime/state/signal/signal_media_runtime.json":
        reasons.append("prediction_workspace_gate signal media ref mismatch")
    if prediction_workspace.get("belief_state_ref") != "runtime/state/prediction/belief_state_frame.json":
        reasons.append("prediction_workspace_gate belief state ref mismatch")
    if prediction_workspace.get("prediction_error_ref") != "runtime/state/prediction/prediction_error_field.json":
        reasons.append("prediction_workspace_gate prediction error ref mismatch")
    if prediction_workspace.get("active_sampling_plan_ref") != "runtime/state/prediction/active_sampling_plan.json":
        reasons.append("prediction_workspace_gate active sampling ref mismatch")
    if "prediction_error_bus" not in prediction_workspace.get("bus_edge_refs", []):
        reasons.append("prediction_workspace_gate missing prediction error bus ref")
    if "ConsciousWorkspaceRuntime" not in prediction_workspace.get("downstream_systems", []):
        reasons.append("prediction_workspace_gate downstream system mismatch")
    continuity_focus = prediction_workspace.get("workspace_contents", {}).get("language_continuity_focus", {})
    for field in [
        "shared_language_refs",
        "expression_monitor_refs",
        "relation_scope_refs",
        "commitment_refs",
        "self_narrative_trace_refs",
    ]:
        if not continuity_focus.get(field):
            reasons.append(f"prediction_workspace_gate missing {field}")
    return reasons


def _check_brain_graph_payload(
    brain_graph: dict[str, Any],
    systems: dict[str, Any],
    bus: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if brain_graph.get("schema_version") != "brain_graph_v0":
        reasons.append("brain_graph_gate schema mismatch")
    if len(brain_graph.get("region_nodes", [])) != systems.get("system_count", 0):
        reasons.append("brain_graph_gate region node count mismatch")
    if len(brain_graph.get("functional_edges", [])) < bus.get("bus_edge_count", 0):
        reasons.append("brain_graph_gate functional edge count mismatch")
    return reasons


def _check_network_state_payload(network_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if network_state.get("schema_version") != "network_state_v0":
        reasons.append("network_state_gate schema mismatch")
    if not network_state.get("active_networks"):
        reasons.append("network_state_gate active networks missing")
    if not network_state.get("switch_events"):
        reasons.append("network_state_gate switch events missing")
    return reasons


def _check_workspace_frame_payload(workspace_frame: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if workspace_frame.get("schema_version") != "workspace_frame_v0":
        reasons.append("workspace_projection_gate schema mismatch")
    if workspace_frame.get("prediction_workspace_ref") != "runtime/state/prediction/prediction_workspace_frame.json":
        reasons.append("workspace_projection_gate prediction workspace ref mismatch")
    if not workspace_frame.get("engram_retrieval_refs"):
        reasons.append("workspace_projection_gate engram retrieval refs missing")
    return reasons


def _check_broadcast_frame_payload(broadcast_frame: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if broadcast_frame.get("schema_version") != "broadcast_frame_v0":
        reasons.append("broadcast_gate schema mismatch")
    if broadcast_frame.get("workspace_frame_ref") != "runtime/state/consciousness/workspace_frame.json":
        reasons.append("broadcast_gate workspace frame ref mismatch")
    if not broadcast_frame.get("broadcast_targets"):
        reasons.append("broadcast_gate broadcast targets missing")
    if not broadcast_frame.get("salience_ranking"):
        reasons.append("broadcast_gate salience ranking missing")
    return reasons


def _check_metacognition_payload(metacognition_state: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if metacognition_state.get("schema_version") != "metacognition_state_v0":
        reasons.append("metacognition_gate schema mismatch")
    if metacognition_state.get("broadcast_frame_ref") != "runtime/state/consciousness/broadcast_frame.json":
        reasons.append("metacognition_gate broadcast frame ref mismatch")
    if not metacognition_state.get("reflection_prompts"):
        reasons.append("metacognition_gate reflection prompts missing")
    if not metacognition_state.get("broadcast_targets"):
        reasons.append("metacognition_gate broadcast targets missing")
    return reasons


def _seed_prediction_language_continuity() -> dict[str, list[str]]:
    return {
        "shared_language_refs": ["runtime/state/language/language_relationship_state.json#shared_language_refs_seed"],
        "expression_monitor_refs": ["runtime/state/language/expression_monitor_state.json#expression_monitor_seed"],
        "relation_scope_refs": ["runtime/state/language/relation_scope_language_index.json#relation_scope_seed"],
        "commitment_refs": ["runtime/state/language/commitment_repair_language_index.json#commitment_seed"],
        "self_narrative_trace_refs": ["runtime/state/language/self_narrative_language_trace.json#self_narrative_seed"],
        "dialogue_turn_log_refs": ["runtime/state/language/dialogue_turn_log.jsonl#turn_seed"],
        "language_percept_refs": ["runtime/state/language/language_percept_state.json#percept_seed"],
        "semantic_map_refs": ["runtime/state/language/semantic_map_state.json#semantic_seed"],
        "semantic_ambiguity_refs": ["runtime/state/language/semantic_map_state.json#ambiguity_seed"],
    }


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _runtime_ref(path: Path) -> str:
    parts = path.parts
    if "runtime" in parts:
        idx = parts.index("runtime")
        return "/".join(parts[idx:])
    return str(path)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _default_run_id() -> str:
    return "neural-life-core-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
