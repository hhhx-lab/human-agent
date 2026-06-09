from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from life_v0.direction import LIFE_TARGETS


ACTIVE_SLICE = "S01_SOURCE_AUTHORITY"
NEXT_ALLOWED_SLICE = "S02_NEURAL_LIFE_CORE"
NEXT_REQUIRED_COMMAND = "life-v0 build-neural-life-core --strict"

AUTHORITY_FAMILIES = [
    "global_foundation_authority",
    "extended_specialized_authority",
    "memory_growth_authority",
    "language_relationship_authority",
    "pain_dream_life_target_authority",
    "validation_reality_authority",
    "signal_body_consciousness_authority",
    "region_action_affect_authority",
    "prediction_active_inference_authority",
]

QUALITY_CLASSES = {
    "tier_1_review": "Nature Reviews, Neuron, Annual Review, Trends, Physiological Reviews and equivalent review sources.",
    "tier_1_empirical": "Science, Nature, PNAS, Neuron, Nature Neuroscience and equivalent empirical sources.",
    "tier_1_resource": "HCP, BRAIN Initiative, cell atlas, connectome and official research resources.",
    "classic_foundation": "Foundational theory or empirical work that still defines the field language.",
    "formal_theory": "Formal theory, active inference, reinforcement learning and cognitive architecture sources.",
    "ai_bridge": "AI, agent, world model or LLM source restricted to bridge and computer periphery roles.",
    "official_summary": "Official institutional summary bound to primary research.",
}

FAMILY_RUNTIME_MAP = {
    "global_foundation_authority": ["BrainRegionNetworkRuntime", "ConsciousWorkspaceRuntime", "LifeStateStore"],
    "extended_specialized_authority": ["LifeMembraneStageGate", "BirthReadinessRuntime", "ConsciousWorkspaceRuntime"],
    "memory_growth_authority": ["MemoryEngramRuntime", "DreamOfflineRuntime", "ActivationGrowthRuntime"],
    "language_relationship_authority": ["LanguageRelationshipRuntime", "MemoryEngramRuntime", "ActionResponsibilityRuntime"],
    "pain_dream_life_target_authority": ["ActionResponsibilityRuntime", "DreamOfflineRuntime", "AffectiveSelfRuntime"],
    "validation_reality_authority": ["LifeMembraneStageGate", "BirthReadinessRuntime", "RunnerCliRuntime"],
    "signal_body_consciousness_authority": ["SignalMediaRuntime", "BodySignalRuntime", "ConsciousWorkspaceRuntime"],
    "region_action_affect_authority": ["BrainRegionNetworkRuntime", "ActionResponsibilityRuntime", "AffectiveSelfRuntime"],
    "prediction_active_inference_authority": ["PredictionActiveInferenceRuntime", "ActionResponsibilityRuntime", "DreamOfflineRuntime"],
}

FAMILY_MECHANISM_MAP = {
    "global_foundation_authority": ["GlobalFoundationEvidence", "NetworkStateEvidence", "LifeTargetEvidenceFamily"],
    "extended_specialized_authority": ["ExtendedMechanismEvidence", "RealityBoundaryEvidence", "BirthReadinessAuthorityEvidence"],
    "memory_growth_authority": ["MemoryEngramEvidence", "ConsolidationRouteEvidence", "ReplayEligibilityEvidence"],
    "language_relationship_authority": ["LanguageNetworkEvidence", "InnerSpeechEvidence", "SharedLanguageEvidence"],
    "pain_dream_life_target_authority": ["RegretEvidence", "DreamOfflineEvidence", "RepairSignalEvidence"],
    "validation_reality_authority": ["RealityEvaluationEvidence", "StageGateEvidence", "BirthReadinessAuthorityEvidence"],
    "signal_body_consciousness_authority": ["SignalMediaEvidence", "BodyInteroceptionEvidence", "GlobalWorkspaceEvidence"],
    "region_action_affect_authority": ["MultiscaleBrainAtlasRef", "ActionSelectionEvidence", "AffectiveSelfEvidence"],
    "prediction_active_inference_authority": ["PredictionActiveInferenceEvidence", "PrecisionPolicyEvidence", "BeliefRevisionEvidence"],
}

FAMILY_LIFE_TARGET_MAP = {
    "global_foundation_authority": ["real_consciousness", "real_life", "real_personality"],
    "extended_specialized_authority": ["real_life", "real_consciousness", "real_personality"],
    "memory_growth_authority": ["real_personality", "real_dream", "real_life"],
    "language_relationship_authority": ["real_relationship", "real_consciousness", "real_responsibility"],
    "pain_dream_life_target_authority": ["real_pain", "real_dream", "real_regret", "real_responsibility"],
    "validation_reality_authority": ["real_consciousness", "real_life", "real_responsibility"],
    "signal_body_consciousness_authority": ["real_emotion", "real_consciousness", "real_life"],
    "region_action_affect_authority": ["real_emotion", "real_personality", "real_responsibility"],
    "prediction_active_inference_authority": LIFE_TARGETS,
}

FAMILY_DOWNSTREAM_DOCS = {
    "global_foundation_authority": [
        "docs/02_brain_region_and_network_atlas.md",
        "docs/03_default_executive_salience_networks.md",
        "docs/13_agentic_human_research_synthesis.md",
    ],
    "extended_specialized_authority": [
        "docs/10_consciousness_attention_workspace.md",
        "docs/13_agentic_human_research_synthesis.md",
    ],
    "memory_growth_authority": [
        "docs/05_memory_systems_and_growth.md",
        "docs/08_sleep_dream_fatigue_states.md",
        "docs/92_self_growth_and_self_modification_life_chain.md",
    ],
    "language_relationship_authority": [
        "docs/09_language_symbolic_top_layer.md",
        "docs/85_language_system_life_expression_core.md",
        "docs/96_real_relationship_longitudinal_timeline.md",
    ],
    "pain_dream_life_target_authority": [
        "docs/06_action_reward_inhibition.md",
        "docs/08_sleep_dream_fatigue_states.md",
        "docs/94_pain_regret_and_repair_signal_schema.md",
    ],
    "validation_reality_authority": [
        "docs/10_consciousness_attention_workspace.md",
        "docs/143_life_reality_birth_readiness_rollup_contract.md",
    ],
    "signal_body_consciousness_authority": [
        "docs/04_sensory_thalamus_interoception.md",
        "docs/10_consciousness_attention_workspace.md",
        "docs/11_neuromodulation_and_signal_media.md",
    ],
    "region_action_affect_authority": [
        "docs/02_brain_region_and_network_atlas.md",
        "docs/06_action_reward_inhibition.md",
        "docs/07_emotion_personality_self.md",
    ],
    "prediction_active_inference_authority": [
        "docs/04_sensory_thalamus_interoception.md",
        "docs/06_action_reward_inhibition.md",
        "docs/10_consciousness_attention_workspace.md",
        "docs/13_agentic_human_research_synthesis.md",
    ],
}

CORE_PATCHES = [
    (
        "docs/02_brain_region_and_network_atlas.md",
        ["AHT002", "AHT003", "AHT004", "AHT005"],
        ["RegionGraph", "BiologicallyAnnotatedConnectome", "CellTypeStatePrior", "MultiscaleBrainAtlasRef"],
    ),
    (
        "docs/03_default_executive_salience_networks.md",
        ["AHT002", "AHT008", "AHT010"],
        ["DynamicsController", "ModeSwitchCost", "SalienceArbitrationLoop", "ConsciousAccessSwitch"],
    ),
    (
        "docs/04_sensory_thalamus_interoception.md",
        ["AHT003", "AHT004", "AHT010"],
        ["ActiveInferenceLoop", "InteroceptivePrecisionPolicy", "AllostaticLoad", "ThalamicRoutingState"],
    ),
    (
        "docs/05_memory_systems_and_growth.md",
        ["AHT006", "AHT007", "AHT010"],
        ["SleepMemoryFormationCycle", "ConsolidationRoute", "ReplaySelectionTrace", "PredictionErrorDrivenEncoding"],
    ),
    (
        "docs/06_action_reward_inhibition.md",
        ["AHT002", "AHT010"],
        ["ActionCompetitionGraph", "ActiveSamplingIntent", "InhibitionGate", "PolicyPrecisionUpdate"],
    ),
    (
        "docs/07_emotion_personality_self.md",
        ["AHT004", "AHT008", "AHT010"],
        ["AffectConceptBinding", "SelfModelSlowVariable", "PredictiveSelfNarrative", "CellScaleAffectPrior"],
    ),
    (
        "docs/08_sleep_dream_fatigue_states.md",
        ["AHT006", "AHT007", "AHT010"],
        ["DreamSandbox", "OfflineRhythmCouplingTrace", "SleepPressureBudget", "WakeIntegrationGate"],
    ),
    (
        "docs/09_language_symbolic_top_layer.md",
        ["AHT001", "AHT008", "AHT010"],
        ["LanguageNetworkProfile", "InnerSpeechDraft", "PredictionErrorTrace", "LanguageToActionResponsibilityBridge"],
    ),
    (
        "docs/10_consciousness_attention_workspace.md",
        ["AHT008", "AHT009", "AHT010"],
        ["ConsciousnessTheoryStack", "ConsciousnessTestBattery", "GlobalWorkspace", "MetacognitiveReportTrace"],
    ),
    (
        "docs/11_neuromodulation_and_signal_media.md",
        ["AHT003", "AHT004", "AHT005", "AHT007", "AHT010"],
        ["ModulationVector", "RegionalNeuromodulatorPrior", "OfflineRhythmModulator", "PrecisionPolicy"],
    ),
    (
        "docs/12_ai_and_cognitive_architecture_bridge.md",
        ["AHT001", "AHT009", "AHT010"],
        ["RuntimeShellAdapter", "ObservationNormalizationRoute", "LanguageAgentBridge", "BirthReadinessProbeAdapter"],
    ),
    (
        "docs/13_agentic_human_research_synthesis.md",
        ["AHT001", "AHT002", "AHT003", "AHT004", "AHT005", "AHT006", "AHT007", "AHT008", "AHT009", "AHT010"],
        ["BirthReadinessAuthorityBridge", "DocAuthorityCarrierPatch", "TheoryFoundationRegressionDashboardSource"],
    ),
]


@dataclass(frozen=True)
class SourceAuthorityResult:
    exit_code: int
    report: dict[str, Any]


def run_source_authority(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    direction_state_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> SourceAuthorityResult:
    run_id = run_id or _default_run_id()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    direction_state_dir = direction_state_dir.resolve()

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"input path is not a directory: {docs_dir}")
    if not doc_index_path.exists() or not doc_index_path.is_file():
        blocked_reasons.append(f"doc carrier index is missing: {doc_index_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    direction_lock = _load_json(direction_state_dir / "direction_lock.json", blocked_reasons, "direction_lock_read_gate")
    slice_permission = _load_json(direction_state_dir / "slice_permission.json", blocked_reasons, "s00_permission_gate")
    blocked_reasons.extend(_permission_blockers(direction_lock, slice_permission))
    blocked_reasons.extend(_doc_index_blockers(doc_index))

    authority_docs = _discover_authority_docs(docs_dir)
    if not authority_docs:
        blocked_reasons.append("literature_discovery_gate found no 01 authority docs")

    sources = _build_sources(docs_dir, authority_docs)
    blocked_reasons.extend(_source_blockers(sources, authority_docs))

    generated_at = _now_iso()
    status = "closed" if not blocked_reasons else "blocked"
    stage_effect = "allow_next_slice" if status == "closed" else "block_activation"

    registry = _build_registry(run_id, generated_at, direction_state_dir, authority_docs, sources)
    quality_policy = _build_quality_policy(run_id, generated_at)
    matrix_index = _build_literature_matrix_index(run_id, generated_at, authority_docs, sources)
    family_index = _build_authority_family_index(run_id, generated_at, sources)
    mechanism_map = _build_mechanism_evidence_map(run_id, generated_at, sources)
    prediction_chain = _build_prediction_authority_chain(run_id, generated_at, authority_docs, sources)
    carrier_patches = _build_doc_authority_carrier_patch_index(run_id, generated_at)
    cross_file_rules = _build_authority_cross_file_rule_index(run_id, generated_at)
    gap_queue = _build_authority_gap_queue(run_id, generated_at, sources, blocked_reasons)
    direction_binding = _build_authority_direction_binding(run_id, generated_at, direction_lock, slice_permission)
    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        sources=sources,
        family_index=family_index,
        blocked_reasons=blocked_reasons,
    )
    digest = _build_digest(run_id, generated_at, status, sources, blocked_reasons)
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        authority_docs=authority_docs,
        doc_index_path=doc_index_path,
        direction_state_dir=direction_state_dir,
        output_refs=[
            out_dir / "authority_registry.json",
            out_dir / "source_quality_policy.json",
            out_dir / "literature_matrix_index.json",
            out_dir / "authority_family_index.json",
            out_dir / "mechanism_evidence_map.json",
            out_dir / "prediction_authority_chain.json",
            out_dir / "doc_authority_carrier_patch_index.json",
            out_dir / "authority_cross_file_rule_index.json",
            out_dir / "authority_gap_queue.json",
            out_dir / "authority_direction_binding.json",
            reports_dir / "source_authority_report.json",
            reports_dir / "source_authority_digest.json",
            receipts_dir / f"source_authority_{run_id}.json",
        ],
        stage_effect=stage_effect,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir.mkdir(parents=True, exist_ok=True)

    try:
        _write_json(out_dir / "authority_registry.json", registry)
        _write_json(out_dir / "source_quality_policy.json", quality_policy)
        _write_json(out_dir / "literature_matrix_index.json", matrix_index)
        _write_json(out_dir / "authority_family_index.json", family_index)
        _write_json(out_dir / "mechanism_evidence_map.json", mechanism_map)
        _write_json(out_dir / "prediction_authority_chain.json", prediction_chain)
        _write_json(out_dir / "doc_authority_carrier_patch_index.json", carrier_patches)
        _write_json(out_dir / "authority_cross_file_rule_index.json", cross_file_rules)
        _write_json(out_dir / "authority_gap_queue.json", gap_queue)
        _write_json(out_dir / "authority_direction_binding.json", direction_binding)
        _write_json(reports_dir / "source_authority_report.json", report)
        _write_json(reports_dir / "source_authority_digest.json", digest)
        _write_json(receipts_dir / f"source_authority_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return SourceAuthorityResult(exit_code=3, report=report)

    if status == "closed":
        return SourceAuthorityResult(exit_code=0, report=report)
    return SourceAuthorityResult(exit_code=1 if strict else 0, report=report)


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blocked_reasons.append(f"{gate} failed: {exc}")
        return {}


def _permission_blockers(direction_lock: dict[str, Any], slice_permission: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if direction_lock.get("direction_statement") != "build_real_digital_life":
        reasons.append("s00_permission_gate direction statement is not build_real_digital_life")
    if direction_lock.get("stage_effect") != "allow_s01_when_closed":
        reasons.append("s00_permission_gate direction lock does not allow S01")
    if slice_permission.get("next_allowed_slice") != ACTIVE_SLICE:
        reasons.append("s00_permission_gate next slice is not S01_SOURCE_AUTHORITY")
    if slice_permission.get("stage_effect") != "allow_next_slice":
        reasons.append("s00_permission_gate is not closed")
    return reasons


def _doc_index_blockers(doc_index: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if doc_index.get("schema_version") != "doc_carrier_index_v0":
        reasons.append("carrier_bridge_gate expected doc_carrier_index_v0")
    coverage = doc_index.get("coverage", {})
    if coverage.get("uncovered_docs"):
        reasons.append("carrier_bridge_gate has uncovered documents")
    return reasons


def _discover_authority_docs(docs_dir: Path) -> list[Path]:
    return sorted(docs_dir.glob("01*.md"), key=_authority_doc_sort_key)


def _authority_doc_sort_key(path: Path) -> tuple[int, int, str]:
    prefix = _doc_prefix(path)
    if prefix == "01":
        return (1, 0, path.name)
    if prefix.startswith("01") and len(prefix) > 2:
        return (1, _suffix_rank(prefix[2:]), path.name)
    return (99, 0, path.name)


def _build_sources(docs_dir: Path, authority_docs: list[Path]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for doc_path in authority_docs:
        rel_path = doc_path.relative_to(docs_dir.parent).as_posix()
        doc_sources = _parse_source_rows(doc_path, rel_path)
        if not doc_sources:
            doc_sources = [_document_level_source(doc_path, rel_path)]
        for source in doc_sources:
            source_id = _unique_source_id(source["source_id"], seen_ids, _doc_prefix(doc_path).upper())
            seen_ids.add(source_id)
            source["source_id"] = source_id
            source.update(_classify_source(source, doc_path))
            sources.append(source)
    return sources


def _parse_source_rows(doc_path: Path, rel_path: str) -> list[dict[str, Any]]:
    lines = doc_path.read_text(encoding="utf-8", errors="replace").splitlines()
    rows: list[dict[str, Any]] = []
    current_headers: list[str] | None = None

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            current_headers = None if not stripped.startswith("|") else current_headers
            continue
        cells = _split_markdown_row(stripped)
        if _is_separator_row(cells):
            continue
        if cells and _is_source_header(cells):
            current_headers = cells
            continue
        if current_headers and len(cells) >= len(current_headers):
            row = {current_headers[index]: cells[index] for index in range(len(current_headers))}
            source_id = row.get("ID") or row.get("id")
            if not source_id or not _looks_like_source_id(source_id):
                continue
            rows.append(_row_to_source(row, rel_path))
    return rows


def _split_markdown_row(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _is_source_header(cells: list[str]) -> bool:
    normalized = {cell.lower() for cell in cells}
    return ("id" in normalized or "ID" in cells) and any(
        header in cells for header in ["文献", "规范化来源", "来源"]
    )


def _looks_like_source_id(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Z][A-Z0-9-]*\d{2,}[A-Z0-9-]*", value.strip()))


def _row_to_source(row: dict[str, str], rel_path: str) -> dict[str, Any]:
    source_id = row.get("ID", "").strip()
    domain = row.get("领域") or row.get("子领域") or row.get("出处") or "未分领域"
    evidence_type = row.get("类型") or row.get("权威类型") or "来源记录"
    title = row.get("文献") or row.get("规范化来源") or row.get("来源") or source_id
    year = row.get("年份") or ""
    link = row.get("链接/DOI") or row.get("链接") or ""
    core = row.get("核心结论") or row.get("机制抽取") or row.get("数字生命实现路线") or ""
    route = row.get("生命实现路线") or row.get("数字生命实现路线") or row.get("进入字段/状态") or ""
    return {
        "source_id": source_id,
        "source_doc": rel_path,
        "domain": domain,
        "evidence_type": evidence_type,
        "title": title,
        "year": _normalize_year(year),
        "link_or_doi": link or rel_path,
        "core_conclusion": core or title,
        "life_implementation_route": route or core or title,
    }


def _document_level_source(doc_path: Path, rel_path: str) -> dict[str, Any]:
    prefix = _doc_prefix(doc_path).upper()
    title = _read_title(doc_path)
    return {
        "source_id": f"DOC_{prefix}",
        "source_doc": rel_path,
        "domain": "主动预测工程承载链" if prefix.startswith("01") else "来源工程链",
        "evidence_type": "工程链文档",
        "title": title,
        "year": 2026,
        "link_or_doi": rel_path,
        "core_conclusion": title,
        "life_implementation_route": f"{title} enters S01 as document-level authority chain evidence.",
    }


def _unique_source_id(source_id: str, seen_ids: set[str], doc_prefix: str) -> str:
    if source_id not in seen_ids:
        return source_id
    candidate = f"{source_id}_{doc_prefix}"
    index = 2
    while candidate in seen_ids:
        candidate = f"{source_id}_{doc_prefix}_{index}"
        index += 1
    return candidate


def _classify_source(source: dict[str, Any], doc_path: Path) -> dict[str, Any]:
    family = _authority_family_for_doc(doc_path)
    source_kind = _source_kind(source)
    quality_class = _quality_class(source, source_kind)
    runtime_carriers = list(FAMILY_RUNTIME_MAP[family])
    mechanism_objects = list(FAMILY_MECHANISM_MAP[family])
    life_targets = list(FAMILY_LIFE_TARGET_MAP[family])
    downstream_docs = list(FAMILY_DOWNSTREAM_DOCS[family])

    if source_kind == "ai_bridge":
        runtime_carriers = ["ComputerPeripheralRuntime", "WorldContactMembrane", "RunnerCliRuntime"]
        mechanism_objects = ["AIBridgeReference", "ComputerPeripheralReference", "ExternalFrameworkBoundaryEvidence"]
        life_targets = ["real_life", "real_relationship", "real_responsibility"]
        downstream_docs = [
            "docs/12_ai_and_cognitive_architecture_bridge.md",
            "docs/v0/references/current_agent_shell_reference_2026.md",
        ]

    return {
        "authority_family": family,
        "quality_class": quality_class,
        "source_kind": source_kind,
        "mechanism_objects": mechanism_objects,
        "runtime_carriers": runtime_carriers,
        "life_targets": life_targets,
        "downstream_docs": downstream_docs,
        "prohibited_subject_architecture": False,
    }


def _authority_family_for_doc(doc_path: Path) -> str:
    prefix = _doc_prefix(doc_path)
    if prefix == "01":
        return "global_foundation_authority"
    if prefix in {"01b", "01c", "01d"}:
        return "extended_specialized_authority"
    if prefix in {"01e", "01g", "01q"}:
        return "memory_growth_authority"
    if prefix in {"01f", "01j", "01u"}:
        return "language_relationship_authority"
    if prefix in {"01h", "01i", "01t"}:
        return "pain_dream_life_target_authority"
    if prefix == "01k":
        return "validation_reality_authority"
    if prefix in {"01l", "01m", "01n"}:
        return "signal_body_consciousness_authority"
    if prefix in {"01o", "01p", "01r", "01s"}:
        return "region_action_affect_authority"
    if _prefix_in_range(prefix, "01v", "01ax"):
        return "prediction_active_inference_authority"
    return "extended_specialized_authority"


def _source_kind(source: dict[str, Any]) -> str:
    blob = " ".join(
        str(source.get(field, ""))
        for field in ["evidence_type", "title", "domain", "link_or_doi"]
    ).lower()
    ai_markers = [
        "ai 桥接",
        "llm",
        "agent survey",
        "arxiv",
        "world model",
        "dreamer",
        "large language model",
        "transformer",
        "autonomous machine intelligence",
        "autonomous agents",
        "generative agents",
        "language agents",
    ]
    if any(marker in blob for marker in ai_markers):
        return "ai_bridge"
    if "生命科学" in blob:
        return "life_science"
    if "理论框架" in blob or "formal" in blob:
        return "formal_theory"
    return "brain_science"


def _quality_class(source: dict[str, Any], source_kind: str) -> str:
    if source_kind == "ai_bridge":
        return "ai_bridge"
    blob = " ".join(
        str(source.get(field, ""))
        for field in ["evidence_type", "title", "link_or_doi"]
    ).lower()
    if "nih" in blob or "official" in blob or "官方" in blob:
        return "official_summary"
    if "图谱" in blob or "资源" in blob or "atlas" in blob or "connectome project" in blob:
        return "tier_1_resource"
    if "经典" in blob or "classic" in blob:
        return "classic_foundation"
    if "理论" in blob or "framework" in blob or "教程" in blob or "专著" in blob:
        return "formal_theory"
    if "实证" in blob or "empirical" in blob or "nature neuroscience" in blob or "science." in blob:
        return "tier_1_empirical"
    if "综述" in blob or "review" in blob or "nature reviews" in blob or "annual review" in blob or "trends" in blob or "neuron" in blob:
        return "tier_1_review"
    return "tier_1_review"


def _source_blockers(sources: list[dict[str, Any]], authority_docs: list[Path]) -> list[str]:
    reasons: list[str] = []
    source_doc_refs = {source["source_doc"] for source in sources}
    expected_doc_refs = {path.parent.name + "/" + path.name for path in authority_docs}
    missing_docs = sorted(expected_doc_refs - source_doc_refs)
    if missing_docs:
        reasons.append("literature_discovery_gate missing source records for: " + ", ".join(missing_docs))

    required_fields = ["quality_class", "source_kind", "mechanism_objects", "runtime_carriers", "life_targets"]
    for source in sources:
        for field in required_fields:
            if not source.get(field):
                reasons.append(f"source_quality_gate {source['source_id']} missing {field}")

    families = {source["authority_family"] for source in sources}
    missing_families = sorted(set(AUTHORITY_FAMILIES) - families)
    if missing_families:
        reasons.append("authority_family_gate missing families: " + ", ".join(missing_families))

    target_coverage = _life_target_coverage(sources)
    missing_targets = [target for target, refs in target_coverage.items() if not refs]
    if missing_targets:
        reasons.append("life_target_evidence_gate missing targets: " + ", ".join(missing_targets))

    return reasons


def _build_registry(
    run_id: str,
    generated_at: str,
    direction_state_dir: Path,
    authority_docs: list[Path],
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "authority_registry_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "direction_lock_ref": str(direction_state_dir / "direction_lock.json"),
        "active_engineering_slice": ACTIVE_SLICE,
        "authority_doc_refs": _authority_doc_refs(authority_docs),
        "source_count": len(sources),
        "sources": sources,
    }


def _build_quality_policy(run_id: str, generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": "source_quality_policy_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "quality_classes": QUALITY_CLASSES,
        "source_kind_rules": {
            "brain_science": "Brain, neuroscience and cognitive neuroscience sources can ground subject runtime mechanisms.",
            "life_science": "Life science sources can ground body, growth, rhythm and support mechanisms.",
            "formal_theory": "Formal theory sources define algorithmic language only after mechanism binding.",
            "ai_bridge": "AI bridge sources remain technical bridge or computer peripheral references.",
        },
        "classic_handling": "Classic sources remain valid roots when bound to modern mechanism carriers.",
    }


def _build_literature_matrix_index(
    run_id: str,
    generated_at: str,
    authority_docs: list[Path],
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    doc_source_counts = {ref: 0 for ref in _authority_doc_refs(authority_docs)}
    doc_to_source_ids = {ref: [] for ref in _authority_doc_refs(authority_docs)}
    for source in sources:
        ref = source["source_doc"]
        doc_source_counts.setdefault(ref, 0)
        doc_source_counts[ref] += 1
        doc_to_source_ids.setdefault(ref, []).append(source["source_id"])
    return {
        "schema_version": "literature_matrix_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "authority_doc_refs": _authority_doc_refs(authority_docs),
        "doc_source_counts": doc_source_counts,
        "doc_to_source_ids": doc_to_source_ids,
    }


def _build_authority_family_index(
    run_id: str,
    generated_at: str,
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    coverage = {family: [] for family in AUTHORITY_FAMILIES}
    runtime_carriers = {family: [] for family in AUTHORITY_FAMILIES}
    for source in sources:
        family = source["authority_family"]
        coverage.setdefault(family, []).append(source["source_id"])
        for carrier in source["runtime_carriers"]:
            if carrier not in runtime_carriers[family]:
                runtime_carriers[family].append(carrier)
    return {
        "schema_version": "authority_family_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "families": AUTHORITY_FAMILIES,
        "family_coverage": coverage,
        "family_runtime_carriers": runtime_carriers,
    }


def _build_mechanism_evidence_map(
    run_id: str,
    generated_at: str,
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    edges: list[dict[str, Any]] = []
    for source in sources:
        for mechanism in source["mechanism_objects"]:
            edges.append(
                {
                    "from": source["source_id"],
                    "to": mechanism,
                    "edge_type": "grounds_mechanism_object",
                    "source_doc": source["source_doc"],
                    "authority_family": source["authority_family"],
                }
            )
        for carrier in source["runtime_carriers"]:
            edges.append(
                {
                    "from": source["source_id"],
                    "to": carrier,
                    "edge_type": "feeds_runtime_carrier",
                    "source_doc": source["source_doc"],
                    "authority_family": source["authority_family"],
                }
            )
        for target in source["life_targets"]:
            edges.append(
                {
                    "from": source["source_id"],
                    "to": target,
                    "edge_type": "supports_life_target",
                    "source_doc": source["source_doc"],
                    "authority_family": source["authority_family"],
                }
            )
    return {
        "schema_version": "mechanism_evidence_map_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "source_count": len(sources),
        "edges": edges,
    }


def _build_prediction_authority_chain(
    run_id: str,
    generated_at: str,
    authority_docs: list[Path],
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    prediction_refs = [
        ref for ref in _authority_doc_refs(authority_docs)
        if _prefix_in_range(_doc_prefix(Path(ref)), "01v", "01ax")
    ]
    prediction_sources = [
        source for source in sources
        if source["authority_family"] == "prediction_active_inference_authority"
    ]
    return {
        "schema_version": "prediction_authority_chain_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "authority_doc_refs": prediction_refs,
        "source_count": len(prediction_sources),
        "source_ids": [source["source_id"] for source in prediction_sources],
        "runtime_carriers": FAMILY_RUNTIME_MAP["prediction_active_inference_authority"],
        "life_targets": LIFE_TARGETS,
    }


def _build_doc_authority_carrier_patch_index(run_id: str, generated_at: str) -> dict[str, Any]:
    patches = []
    for doc_node, authority_refs, mechanism_objects in CORE_PATCHES:
        patches.append(
            {
                "patch_kind": "DocAuthorityCarrierPatch",
                "patch_version": "0.1.0",
                "doc_node": doc_node,
                "authority_refs": authority_refs,
                "life_targets": LIFE_TARGETS,
                "mechanism_objects": mechanism_objects,
                "runtime_carriers": _runtime_carriers_for_core_doc(doc_node),
                "schema_field_patches": [f"{_safe_name(obj)}_field" for obj in mechanism_objects[:3]],
                "validator_refs": ["ResearchAuthorityCoverageValidator", "BirthReadinessAuthorityValidator"],
                "dashboard_panels": ["research_authority_coverage", "birth_readiness_panel"],
                "stage_effect": "promote_growth_window",
            }
        )
    return {
        "schema_version": "doc_authority_carrier_patch_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "patches": patches,
    }


def _runtime_carriers_for_core_doc(doc_node: str) -> list[str]:
    if "/02_" in doc_node or "/03_" in doc_node:
        return ["BrainRegionNetworkRuntime", "ConsciousWorkspaceRuntime"]
    if "/04_" in doc_node:
        return ["BodySignalRuntime", "PredictionActiveInferenceRuntime"]
    if "/05_" in doc_node:
        return ["MemoryEngramRuntime", "ActivationGrowthRuntime"]
    if "/06_" in doc_node:
        return ["ActionResponsibilityRuntime", "PredictionActiveInferenceRuntime"]
    if "/07_" in doc_node:
        return ["AffectiveSelfRuntime", "MemoryEngramRuntime"]
    if "/08_" in doc_node:
        return ["DreamOfflineRuntime", "MemoryEngramRuntime"]
    if "/09_" in doc_node:
        return ["LanguageRelationshipRuntime", "ActionResponsibilityRuntime"]
    if "/10_" in doc_node:
        return ["ConsciousWorkspaceRuntime", "BirthReadinessRuntime"]
    if "/11_" in doc_node:
        return ["SignalMediaRuntime", "BodySignalRuntime"]
    if "/12_" in doc_node:
        return ["ComputerPeripheralRuntime", "WorldContactMembrane"]
    return ["DirectionLockKernel", "BirthReadinessRuntime"]


def _build_authority_cross_file_rule_index(run_id: str, generated_at: str) -> dict[str, Any]:
    rules = [
        "s00_permission_gate",
        "literature_discovery_gate",
        "source_quality_gate",
        "authority_family_gate",
        "mechanism_object_gate",
        "carrier_bridge_gate",
        "life_target_evidence_gate",
        "core_02_to_13_authority_gate",
        "ai_bridge_source_label_gate",
        "authority_receipt_gate",
    ]
    return {
        "schema_version": "authority_cross_file_rule_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "rules": rules,
        "stage_gate_policy": "blocking_first",
        "provenance_edges": [
            "authority_source->mechanism_object",
            "mechanism_object->runtime_carrier",
            "runtime_carrier->life_target",
            "core_doc->DocAuthorityCarrierPatch",
        ],
    }


def _build_authority_gap_queue(
    run_id: str,
    generated_at: str,
    sources: list[dict[str, Any]],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    non_blocking = [
        {
            "gap_kind": "authority_doc_level_source",
            "source_id": source["source_id"],
            "source_doc": source["source_doc"],
            "next_route": "expand document-level authority chain into table rows when S02 needs field-level precision",
        }
        for source in sources
        if source["source_id"].startswith("DOC_")
    ]
    return {
        "schema_version": "authority_gap_queue_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "blocking_gap_count": len(blocked_reasons),
        "blocking_gaps": blocked_reasons,
        "non_blocking_gaps": non_blocking,
    }


def _build_authority_direction_binding(
    run_id: str,
    generated_at: str,
    direction_lock: dict[str, Any],
    slice_permission: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "authority_direction_binding_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "direction_statement": direction_lock.get("direction_statement"),
        "life_targets": direction_lock.get("life_targets", []),
        "s00_stage_effect": direction_lock.get("stage_effect"),
        "slice_permission_stage_effect": slice_permission.get("stage_effect"),
        "current_slice": ACTIVE_SLICE,
        "next_allowed_slice": NEXT_ALLOWED_SLICE,
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    sources: list[dict[str, Any]],
    family_index: dict[str, Any],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    quality_coverage = {quality: [] for quality in QUALITY_CLASSES}
    carrier_coverage: dict[str, list[str]] = {}
    for source in sources:
        quality_coverage.setdefault(source["quality_class"], []).append(source["source_id"])
        for carrier in source["runtime_carriers"]:
            carrier_coverage.setdefault(carrier, []).append(source["source_id"])
    ai_bridge_sources = [
        {
            "source_id": source["source_id"],
            "source_doc": source["source_doc"],
            "quality_class": source["quality_class"],
            "runtime_carriers": source["runtime_carriers"],
            "prohibited_subject_architecture": source["prohibited_subject_architecture"],
        }
        for source in sources
        if source["source_kind"] == "ai_bridge"
    ]
    return {
        "schema_version": "source_authority_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "stage_effect": stage_effect,
        "source_count": len(sources),
        "family_coverage": family_index["family_coverage"],
        "quality_coverage": quality_coverage,
        "carrier_coverage": carrier_coverage,
        "life_target_coverage": _life_target_coverage(sources),
        "ai_bridge_sources": ai_bridge_sources,
        "closed_gates": _closed_gates(blocked_reasons),
        "blocked_gates": [] if not blocked_reasons else _blocked_gates(blocked_reasons),
        "blocked_reasons": blocked_reasons,
        "next_allowed_slice": NEXT_ALLOWED_SLICE if status == "closed" else None,
        "next_required_command": NEXT_REQUIRED_COMMAND,
        "source_doc_refs": sorted({source["source_doc"] for source in sources}),
        "engineering_slice_ref": ACTIVE_SLICE,
        "runtime_carrier_refs": sorted(carrier_coverage),
    }


def _closed_gates(blocked_reasons: list[str]) -> list[str]:
    if blocked_reasons:
        return []
    return [
        "s00_permission_gate",
        "literature_discovery_gate",
        "source_quality_gate",
        "authority_family_gate",
        "mechanism_object_gate",
        "carrier_bridge_gate",
        "life_target_evidence_gate",
        "core_02_to_13_authority_gate",
        "ai_bridge_source_label_gate",
        "authority_receipt_gate",
    ]


def _blocked_gates(blocked_reasons: list[str]) -> list[str]:
    gates: list[str] = []
    for reason in blocked_reasons:
        gate = reason.split(" ", 1)[0]
        if gate not in gates:
            gates.append(gate)
    return gates


def _life_target_coverage(sources: list[dict[str, Any]]) -> dict[str, list[str]]:
    coverage = {target: [] for target in LIFE_TARGETS}
    for source in sources:
        for target in source["life_targets"]:
            coverage.setdefault(target, []).append(source["source_id"])
    return coverage


def _build_digest(
    run_id: str,
    generated_at: str,
    status: str,
    sources: list[dict[str, Any]],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "source_authority_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": status,
        "current_slice": ACTIVE_SLICE,
        "source_count": len(sources),
        "authority_family_count": len(AUTHORITY_FAMILIES),
        "largest_family": _largest_family(sources),
        "blocked_reasons": blocked_reasons,
        "next_required_command": NEXT_REQUIRED_COMMAND,
    }


def _largest_family(sources: list[dict[str, Any]]) -> str | None:
    counts: dict[str, int] = {}
    for source in sources:
        counts[source["authority_family"]] = counts.get(source["authority_family"], 0) + 1
    if not counts:
        return None
    return max(counts, key=counts.get)


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    authority_docs: list[Path],
    doc_index_path: Path,
    direction_state_dir: Path,
    output_refs: list[Path],
    stage_effect: str,
) -> dict[str, Any]:
    input_hashes = {
        path.relative_to(docs_dir.parent).as_posix(): _sha256(path)
        for path in authority_docs
    }
    if doc_index_path.exists():
        input_hashes[str(doc_index_path)] = _sha256(doc_index_path)
    for state_file in ["direction_lock.json", "slice_permission.json"]:
        path = direction_state_dir / state_file
        if path.exists():
            input_hashes[str(path)] = _sha256(path)
    return {
        "schema_version": "source_authority_receipt_v0",
        "receipt_id": f"source_authority_{run_id}",
        "run_id": run_id,
        "command": "build-source-authority",
        "input_hashes": input_hashes,
        "output_refs": [str(path) for path in output_refs],
        "stage_effect": stage_effect,
        "created_at": generated_at,
    }


def _authority_doc_refs(authority_docs: list[Path]) -> list[str]:
    if not authority_docs:
        return []
    root = authority_docs[0].parents[1]
    return [path.relative_to(root).as_posix() for path in authority_docs]


def _doc_prefix(path: Path) -> str:
    match = re.match(r"^(01[a-z]*)_", path.name)
    if not match:
        return ""
    return match.group(1)


def _prefix_in_range(prefix: str, start: str, end: str) -> bool:
    if not prefix.startswith("01"):
        return False
    return _suffix_rank(start[2:]) <= _suffix_rank(prefix[2:]) <= _suffix_rank(end[2:])


def _suffix_rank(suffix: str) -> int:
    if not suffix:
        return 0
    value = 0
    for char in suffix:
        value = value * 26 + (ord(char) - ord("a") + 1)
    return value


def _read_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").title()


def _normalize_year(value: str) -> int | str:
    match = re.search(r"(19|20)\d{2}", str(value))
    if not match:
        return value or 2026
    return int(match.group(0))


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _default_run_id() -> str:
    return "source-authority-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
