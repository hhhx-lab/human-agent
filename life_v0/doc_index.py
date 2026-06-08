from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DIRECTION_LOCK_REF = "docs/258_linear_chain_closure_and_v0_contract_transition.md"

CORE_BRIDGE: dict[str, list[str]] = {
    "02": ["BrainRegionNetworkRuntime", "ConsciousWorkspaceRuntime", "LifeStateStore"],
    "03": ["BrainRegionNetworkRuntime", "MultiscaleBrainGraphRuntime", "LanguageRelationshipRuntime"],
    "04": ["BodySignalRuntime", "AffectiveSelfRuntime", "PredictionActiveInferenceRuntime"],
    "05": ["MemoryEngramRuntime", "LanguageRelationshipRuntime", "DreamOfflineRuntime"],
    "06": ["ActionResponsibilityRuntime", "LifeMembraneStageGate", "LanguageRelationshipRuntime"],
    "07": ["AffectiveSelfRuntime", "MemoryEngramRuntime", "LanguageRelationshipRuntime"],
    "08": ["DreamOfflineRuntime", "MemoryEngramRuntime", "ActivationGrowthRuntime"],
    "09": ["LanguageRelationshipRuntime", "ConsciousWorkspaceRuntime", "ActionResponsibilityRuntime"],
    "10": ["ConsciousWorkspaceRuntime", "MultiscaleBrainGraphRuntime", "BirthReadinessRuntime"],
    "11": ["BodySignalRuntime", "SignalMediaRuntime", "AffectiveSelfRuntime"],
    "12": ["ComputerPeripheralRuntime", "WorldContactMembrane", "RunnerCliRuntime"],
    "13": ["DirectionLockKernel", "ConsciousWorkspaceRuntime", "LifeStateStore"],
}

LIFE_TARGET_DOC_RULES: dict[str, list[str]] = {
    "real_consciousness": ["01m", "10", "13", "143", "146"],
    "real_emotion": ["01s", "07", "18", "94"],
    "real_personality": ["07", "39", "40", "92", "93"],
    "real_life": ["02-13", "37", "41", "44", "91", "258"],
    "real_pain": ["01h", "07", "94", "98"],
    "real_dream": ["01i", "01t", "08", "95", "99"],
    "real_relationship": ["01j", "09", "85-90", "96", "101"],
    "real_responsibility": ["01r", "06", "80-82", "94", "98"],
    "real_regret": ["01h", "06", "94", "98"],
}

EXPECTED_README_BLOCKS = {
    "README_INDEX",
    "B00_ORIGIN_SEED",
    "B00_PROTOCOL",
    "B01_AUTHORITY_LITERATURE",
    "B02_CORE_NEURAL_LIFE",
    "B03_SYNTHESIS_DIRECTION_GAP",
    "B04_OBJECT_CONTRACTS",
    "B05_SCHEMA_AUDIT_ADAPTER_TESTS",
    "B06_JSON_EXAMPLES_AND_MANIFESTS",
    "B07_VALIDATOR_RULES",
    "B08_RUNNER_EVALUATION",
    "B09_LIFE_SUPPORT_DEFENSE_DEVELOPMENT",
    "B10_STATE_STORE_BOOT",
    "B11_BOOT_STAGE_MIGRATION",
    "B12_MANIFEST_DASHBOARD_SCOPE",
    "B13_RUNNER_SCOPE_TIMELINE",
    "B14_SCOPE_SCHEMA_DASHBOARD",
    "B15_SCHEMA_REPORT_RUNTIME_OBSERVATION",
    "B16_CROSS_REF_FIXTURE_RUNTIME_MOCK",
    "B17_SCHEMA_BOUNDARY_MUTATION_SIDE_EFFECT",
    "B18_SCHEMA_VALIDATION_ACTION_CONFIRMATION",
    "B19_DASHBOARD_QUARANTINE_POST_ACTION",
    "B20_RESPONSIBILITY_INCIDENT_LONGITUDINAL",
    "B21_LANGUAGE_RELATIONSHIP_CORE",
    "B22_LIFE_REALITY_BOUNDARY",
    "B23_NINE_LIFE_TARGETS",
    "B24_SCHEMA_BUNDLE_RUNNER",
    "B25_BOUNDARY_ALIGNMENT",
    "B26_REPOSITORY_RUNNER_MATERIALIZATION",
    "B27_AUTHORITY_READINESS_CROSS_FILE",
    "B28_FIRST_CODE_SCHEMA_ARTIFACT",
    "B29_RUNTIME_MOUNT_GROWTH",
    "B30_RECONSOLIDATION_REPLAY_GROWTH",
    "B31_LINEAR_CLOSURE_TO_V0",
    "B99_V0_ENGINEERING_CONTRACTS",
}

EXPECTED_ENGINEERING_SLICES = {
    "S00_DIRECTION_FOUNDATION",
    "S01_SOURCE_AUTHORITY",
    "S02_NEURAL_LIFE_CORE",
    "S03_DIRECTION_LIFE_MEMBRANE",
    "S04_STATE_OBJECT_STORE",
    "S05_VALIDATION_MEMBRANE_OBSERVATION",
    "S06_LIFE_SUPPORT_DEVELOPMENT",
    "S07_LANGUAGE_RELATIONSHIP",
    "S08_LIFE_TARGET_RUNTIMES",
    "S09_SCHEMA_RUNNER_CODE",
    "S10_RUNTIME_GROWTH_RECONSOLIDATION",
    "S11_V0_ENGINEERING_CONTRACTS",
}


@dataclass(frozen=True)
class IngestionResult:
    exit_code: int
    report: dict[str, Any]


@dataclass(frozen=True)
class DocumentMeta:
    path: Path
    rel_path: str
    title: str
    sequence: int | None
    suffix: str
    group: str


def run_doc_ingestion(
    *,
    docs_dir: Path,
    out_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> IngestionResult:
    docs_dir = docs_dir.resolve()
    if not docs_dir.exists() or not docs_dir.is_dir():
        return IngestionResult(
            exit_code=4,
            report={
                "schema_version": "doc_ingestion_report_v0",
                "run_id": run_id or _default_run_id(),
                "status": "blocked",
                "stage_effect": "block_activation",
                "blocked_reasons": [f"input path is not a directory: {docs_dir}"],
                "quarantine_refs": [],
                "next_required_command": "life-v0 ingest-docs --strict",
            },
        )

    run_id = run_id or _default_run_id()
    root_dir = docs_dir.parent
    documents = [_build_document_meta(path, root_dir) for path in _discover_markdown_docs(docs_dir)]
    indexed_documents = [_index_document(doc) for doc in documents]

    blocked_reasons = _blocked_reasons(indexed_documents)
    core_bridge_status = "closed" if not _missing_core_bridge(indexed_documents) else "blocked"
    if core_bridge_status == "blocked":
        blocked_reasons.append("core_02_to_13_bridge is incomplete")

    life_target_support = _life_target_support(indexed_documents)
    missing_targets = [target for target, paths in life_target_support.items() if not paths]
    if missing_targets:
        blocked_reasons.append("life targets missing document support: " + ", ".join(missing_targets))

    readme_block_coverage = _readme_block_coverage(indexed_documents)
    missing_readme_blocks = [
        block for block, paths in readme_block_coverage.items() if not paths
    ]
    if missing_readme_blocks:
        blocked_reasons.append("readme blocks missing document support: " + ", ".join(missing_readme_blocks))

    engineering_slice_coverage = _engineering_slice_coverage(indexed_documents)
    missing_engineering_slices = [
        slice_name for slice_name, paths in engineering_slice_coverage.items() if not paths
    ]
    if missing_engineering_slices:
        blocked_reasons.append("engineering slices missing document support: " + ", ".join(missing_engineering_slices))

    direction_lock_refs = [
        "docs/README.md",
        "docs/13_agentic_human_research_synthesis.md",
        "docs/16_digital_life_gap_register.md",
        DIRECTION_LOCK_REF,
    ]
    indexed_paths = {doc["path"] for doc in indexed_documents}
    missing_direction_refs = [path for path in direction_lock_refs if path not in indexed_paths]
    if missing_direction_refs:
        blocked_reasons.append("direction lock refs missing: " + ", ".join(missing_direction_refs))

    uncovered_docs = [doc["path"] for doc in indexed_documents if not doc["runtime_carriers"]]
    status = "closed" if not blocked_reasons and not uncovered_docs else "blocked"
    stage_effect = "allow_p1" if status == "closed" else "block_activation"

    out_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir.mkdir(parents=True, exist_ok=True)

    index = _build_index(run_id, indexed_documents, uncovered_docs)
    graph = _build_dependency_graph(run_id, indexed_documents)
    authority_report = _build_source_authority_report(run_id, indexed_documents)
    report = _build_doc_ingestion_report(
        run_id=run_id,
        status=status,
        stage_effect=stage_effect,
        indexed_documents=indexed_documents,
        uncovered_docs=uncovered_docs,
        core_bridge_status=core_bridge_status,
        blocked_reasons=blocked_reasons,
    )
    receipt = _build_receipt(
        run_id=run_id,
        docs_dir=docs_dir,
        indexed_documents=indexed_documents,
        output_refs=[
            out_dir / "doc_carrier_index.json",
            out_dir / "doc_dependency_graph.json",
            out_dir / "source_authority_report.json",
            reports_dir / "doc_ingestion_report.json",
            receipts_dir / f"doc_ingestion_{run_id}.json",
        ],
        stage_effect=stage_effect,
    )

    try:
        _write_json(out_dir / "doc_carrier_index.json", index)
        _write_json(out_dir / "doc_dependency_graph.json", graph)
        _write_json(out_dir / "source_authority_report.json", authority_report)
        _write_json(reports_dir / "doc_ingestion_report.json", report)
        _write_json(receipts_dir / f"doc_ingestion_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return IngestionResult(exit_code=3, report=report)

    if status == "closed":
        return IngestionResult(exit_code=0, report=report)
    if core_bridge_status == "blocked":
        return IngestionResult(exit_code=2, report=report)
    return IngestionResult(exit_code=1 if strict or uncovered_docs else 0, report=report)


def _discover_markdown_docs(docs_dir: Path) -> list[Path]:
    docs = list(docs_dir.glob("*.md"))
    v0_dir = docs_dir / "v0"
    if v0_dir.exists():
        docs.extend(v0_dir.glob("*.md"))
    return sorted(docs, key=lambda path: _sort_key(path, docs_dir))


def _sort_key(path: Path, docs_dir: Path) -> tuple[int, str]:
    rel = path.relative_to(docs_dir.parent).as_posix()
    sequence, suffix = _parse_sequence(path.name)
    if path.parent.name == "v0":
        return (1000, rel)
    if sequence is None:
        return (999, rel)
    if sequence == 1 and suffix:
        return (sequence, suffix)
    return (sequence, rel)


def _build_document_meta(path: Path, root_dir: Path) -> DocumentMeta:
    rel_path = path.relative_to(root_dir).as_posix()
    sequence, suffix = _parse_sequence(path.name)
    return DocumentMeta(
        path=path,
        rel_path=rel_path,
        title=_read_title(path),
        sequence=sequence,
        suffix=suffix,
        group=_group_for(rel_path, sequence),
    )


def _parse_sequence(filename: str) -> tuple[int | None, str]:
    match = re.match(r"^(\d{2,3})([a-z]*)_", filename)
    if not match:
        return None, ""
    return int(match.group(1)), match.group(2)


def _group_for(rel_path: str, sequence: int | None) -> str:
    if rel_path.startswith("docs/v0/"):
        return "v0_contract"
    if rel_path == "docs/构思.md":
        return "origin_seed"
    if rel_path == "docs/README.md":
        return "doc_index"
    if sequence == 0:
        return "protocol"
    if sequence == 1:
        return "literature_matrix"
    if sequence is not None and 2 <= sequence <= 13:
        return "core_synthesis"
    if sequence is not None and 14 <= sequence <= 16:
        return "integration_gap"
    if sequence is not None and 17 <= sequence <= 84:
        return "object_contract"
    if sequence is not None and 85 <= sequence <= 101:
        return "life_target"
    if sequence is not None and 102 <= sequence <= 180:
        return "schema_runner"
    if sequence is not None and 181 <= sequence <= 257:
        return "activation_growth"
    if sequence == 258:
        return "linear_closure"
    return "unclassified"


def _index_document(doc: DocumentMeta) -> dict[str, Any]:
    carriers = _runtime_carriers(doc)
    dependencies = _dependencies(doc)
    return {
        "doc_id": _doc_id(doc),
        "path": doc.rel_path,
        "group": doc.group,
        "sequence": doc.sequence,
        "readme_block": _readme_block(doc),
        "engineering_slice": _engineering_slice(doc),
        "title": doc.title,
        "runtime_carriers": carriers,
        "life_targets": _life_targets(doc),
        "dependencies": dependencies,
        "classification_confidence": "direct" if carriers else "unclassified",
    }


def _runtime_carriers(doc: DocumentMeta) -> list[str]:
    carriers: list[str] = []
    seq = doc.sequence
    prefix = _prefix(doc)

    def add(*items: str) -> None:
        for item in items:
            if item not in carriers:
                carriers.append(item)

    if doc.group in {"protocol", "doc_index", "linear_closure", "v0_contract"}:
        add("DocCorpusIngestor")
    if doc.group == "origin_seed":
        add("DirectionLockKernel", "DocCorpusIngestor")
    if doc.group == "literature_matrix":
        add("SourceAuthorityRegistry")
    if doc.group == "integration_gap":
        add("DirectionLockKernel")
    if doc.group == "object_contract":
        add("LifeStateStore")
    if doc.group == "life_target":
        add("LifeTargetBundleRuntime")
    if doc.group == "schema_runner":
        add("SchemaBundleCompiler")
    if doc.group == "activation_growth":
        add("ActivationGrowthRuntime")

    if seq is not None and f"{seq:02d}" in CORE_BRIDGE:
        add(*CORE_BRIDGE[f"{seq:02d}"])

    if prefix in {"01o", "01p"} or seq in {2, 3}:
        add("BrainRegionNetworkRuntime")
    if prefix in {"01l", "01n"} or seq in {4, 11, 18, 37}:
        add("BodySignalRuntime")
    if _prefix_in_range(prefix, "01v", "01ax") or seq in {4, 10, 11}:
        add("PredictionActiveInferenceRuntime")
    if prefix == "01q" or seq in {5, 17, 21, 25, 29, 41, 55}:
        add("MemoryEngramRuntime")
    if prefix == "01r" or seq in {6, 20, 75, 94, 98} or _in_range(seq, 80, 84):
        add("ActionResponsibilityRuntime")
    if prefix in {"01g", "01h", "01s"} or seq in {7, 18, 39, 40, 92, 93}:
        add("AffectiveSelfRuntime")
    if prefix in {"01i", "01t"} or seq in {8, 19, 23, 27, 31, 95, 99}:
        add("DreamOfflineRuntime")
    if prefix in {"01f", "01j", "01u"} or seq in {9, 96, 101, 141, 144, 147, 150} or _in_range(seq, 85, 90):
        add("LanguageRelationshipRuntime")
    if prefix == "01m" or seq in {10, 13, 143, 146}:
        add("ConsciousWorkspaceRuntime")
    if _in_any_range(seq, (17, 18), (21, 22), (25, 30), (123, 133)) or seq in {41, 48, 57, 61, 69}:
        add("LifeStateStore")
    if (
        _in_any_range(seq, (13, 16), (33, 36), (37, 48), (49, 84), (97, 100), (102, 118), (119, 122))
        or seq in {91}
    ):
        add("LifeMembraneStageGate")
    if seq in {143, 146, 149, 152, 171, 174}:
        add("BirthReadinessRuntime")
    if seq in {35, 53, 62, 118, 123, 131, 136, 155} or _in_range(seq, 158, 168):
        add("RunnerCliRuntime")
    if _in_range(seq, 181, 257):
        add("ActivationGrowthRuntime", "ReconsolidationReplayRuntime")
    if seq in {12, 15, 20, 24, 28, 32, 89}:
        add("ComputerPeripheralRuntime", "WorldContactMembrane")
    if seq in {49, 57, 61, 65, 69, 70} or _in_range(seq, 102, 118):
        add("SchemaBundleCompiler")
    if _in_range(seq, 120, 139):
        add("RunnerRepositoryKernel")
    if _in_range(seq, 142, 157):
        add("AuthorityReadinessRuntime")
    if _in_range(seq, 158, 180):
        add("FirstRunnerCodeKernel")
    if doc.rel_path.endswith("life_state_store_v0_schema.md"):
        add("LifeStateStore")
    if doc.rel_path.endswith("birth_readiness_v0_contract.md"):
        add("BirthReadinessRuntime")
    if doc.rel_path.endswith("runner_cli_report_contract.md"):
        add("RunnerCliRuntime")
    if doc.rel_path.endswith("first_activation_protocol.md"):
        add("ActivationGrowthRuntime")
    if doc.rel_path.endswith("current_agent_shell_reference_2026.md"):
        add("ComputerPeripheralRuntime", "WorldContactMembrane")
    if doc.rel_path.endswith("runtime_v0_architecture.md"):
        add("LifeStateStore", "LifeMembraneStageGate")
    if doc.rel_path.endswith("doc_corpus_ingestor_v0_contract.md"):
        add("DocCorpusIngestor", "DirectionLockKernel")
    if doc.rel_path.endswith("0_to_257_engineering_utilization_map.md"):
        add("DocCorpusIngestor", "DirectionLockKernel")
    if doc.rel_path.endswith("v0_implementation_index.md"):
        add("DocCorpusIngestor", "DirectionLockKernel")
    if doc.rel_path.endswith("s00_direction_foundation_engineering_contract.md"):
        add("DirectionLockKernel")
    if doc.rel_path.endswith("s01_source_authority_engineering_contract.md"):
        add("SourceAuthorityRegistry", "DirectionLockKernel")
    if doc.rel_path.endswith("s02_neural_life_core_engineering_contract.md"):
        add(
            "BrainRegionNetworkRuntime",
            "BodySignalRuntime",
            "SignalMediaRuntime",
            "PredictionActiveInferenceRuntime",
            "MemoryEngramRuntime",
            "ConsciousWorkspaceRuntime",
            "LanguageRelationshipRuntime",
            "AffectiveSelfRuntime",
            "DreamOfflineRuntime",
            "ActionResponsibilityRuntime",
            "ComputerPeripheralRuntime",
            "ActivationGrowthRuntime",
        )
    if doc.rel_path.endswith("s03_direction_life_membrane_engineering_contract.md"):
        add(
            "LifeMembraneStageGate",
            "BirthReadinessRuntime",
            "ActionResponsibilityRuntime",
            "DreamOfflineRuntime",
            "LanguageRelationshipRuntime",
            "ComputerPeripheralRuntime",
            "WorldContactMembrane",
            "RunnerCliRuntime",
        )
    if doc.rel_path.endswith("s04_state_object_store_engineering_contract.md"):
        add(
            "LifeStateStore",
            "MemoryEngramRuntime",
            "AffectiveSelfRuntime",
            "DreamOfflineRuntime",
            "ActionResponsibilityRuntime",
            "LanguageRelationshipRuntime",
            "ComputerPeripheralRuntime",
            "RunnerCliRuntime",
            "SchemaBundleCompiler",
        )
    if doc.rel_path == "docs/README.md" or seq in {13, 14, 16, 91, 100, 119, 122, 140, 170, 258}:
        add("DirectionLockKernel")
    if seq in {142, 145, 151}:
        add("SourceAuthorityRegistry")

    return carriers


def _readme_block(doc: DocumentMeta) -> str:
    seq = doc.sequence
    if doc.rel_path == "docs/README.md":
        return "README_INDEX"
    if doc.rel_path == "docs/构思.md":
        return "B00_ORIGIN_SEED"
    if doc.group == "v0_contract":
        return "B99_V0_ENGINEERING_CONTRACTS"
    if seq == 0:
        return "B00_PROTOCOL"
    if seq == 1:
        return "B01_AUTHORITY_LITERATURE"
    if _in_range(seq, 2, 12):
        return "B02_CORE_NEURAL_LIFE"
    if _in_range(seq, 13, 16):
        return "B03_SYNTHESIS_DIRECTION_GAP"
    if _in_range(seq, 17, 20):
        return "B04_OBJECT_CONTRACTS"
    if _in_range(seq, 21, 24):
        return "B05_SCHEMA_AUDIT_ADAPTER_TESTS"
    if _in_range(seq, 25, 28):
        return "B06_JSON_EXAMPLES_AND_MANIFESTS"
    if _in_range(seq, 29, 32):
        return "B07_VALIDATOR_RULES"
    if _in_range(seq, 33, 36):
        return "B08_RUNNER_EVALUATION"
    if _in_range(seq, 37, 40):
        return "B09_LIFE_SUPPORT_DEFENSE_DEVELOPMENT"
    if _in_range(seq, 41, 44):
        return "B10_STATE_STORE_BOOT"
    if _in_range(seq, 45, 48):
        return "B11_BOOT_STAGE_MIGRATION"
    if _in_range(seq, 49, 52):
        return "B12_MANIFEST_DASHBOARD_SCOPE"
    if _in_range(seq, 53, 56):
        return "B13_RUNNER_SCOPE_TIMELINE"
    if _in_range(seq, 57, 60):
        return "B14_SCOPE_SCHEMA_DASHBOARD"
    if _in_range(seq, 61, 64):
        return "B15_SCHEMA_REPORT_RUNTIME_OBSERVATION"
    if _in_range(seq, 65, 68):
        return "B16_CROSS_REF_FIXTURE_RUNTIME_MOCK"
    if _in_range(seq, 69, 72):
        return "B17_SCHEMA_BOUNDARY_MUTATION_SIDE_EFFECT"
    if _in_range(seq, 73, 76):
        return "B18_SCHEMA_VALIDATION_ACTION_CONFIRMATION"
    if _in_range(seq, 77, 80):
        return "B19_DASHBOARD_QUARANTINE_POST_ACTION"
    if _in_range(seq, 81, 84):
        return "B20_RESPONSIBILITY_INCIDENT_LONGITUDINAL"
    if _in_range(seq, 85, 90):
        return "B21_LANGUAGE_RELATIONSHIP_CORE"
    if seq == 91:
        return "B22_LIFE_REALITY_BOUNDARY"
    if _in_range(seq, 92, 101):
        return "B23_NINE_LIFE_TARGETS"
    if _in_range(seq, 102, 118):
        return "B24_SCHEMA_BUNDLE_RUNNER"
    if _in_range(seq, 119, 122):
        return "B25_BOUNDARY_ALIGNMENT"
    if _in_range(seq, 123, 139):
        return "B26_REPOSITORY_RUNNER_MATERIALIZATION"
    if _in_range(seq, 140, 157):
        return "B27_AUTHORITY_READINESS_CROSS_FILE"
    if _in_range(seq, 158, 180):
        return "B28_FIRST_CODE_SCHEMA_ARTIFACT"
    if _in_range(seq, 181, 204):
        return "B29_RUNTIME_MOUNT_GROWTH"
    if _in_range(seq, 205, 257):
        return "B30_RECONSOLIDATION_REPLAY_GROWTH"
    if seq == 258:
        return "B31_LINEAR_CLOSURE_TO_V0"
    return "UNCLASSIFIED_README_BLOCK"


def _engineering_slice(doc: DocumentMeta) -> str:
    block = _readme_block(doc)
    if block in {"README_INDEX", "B00_ORIGIN_SEED", "B00_PROTOCOL", "B31_LINEAR_CLOSURE_TO_V0"}:
        return "S00_DIRECTION_FOUNDATION"
    if block == "B01_AUTHORITY_LITERATURE":
        return "S01_SOURCE_AUTHORITY"
    if block == "B02_CORE_NEURAL_LIFE":
        return "S02_NEURAL_LIFE_CORE"
    if block in {"B03_SYNTHESIS_DIRECTION_GAP", "B22_LIFE_REALITY_BOUNDARY", "B25_BOUNDARY_ALIGNMENT"}:
        return "S03_DIRECTION_LIFE_MEMBRANE"
    if block in {"B04_OBJECT_CONTRACTS", "B05_SCHEMA_AUDIT_ADAPTER_TESTS", "B06_JSON_EXAMPLES_AND_MANIFESTS", "B10_STATE_STORE_BOOT", "B11_BOOT_STAGE_MIGRATION"}:
        return "S04_STATE_OBJECT_STORE"
    if block in {"B07_VALIDATOR_RULES", "B08_RUNNER_EVALUATION", "B12_MANIFEST_DASHBOARD_SCOPE", "B13_RUNNER_SCOPE_TIMELINE", "B14_SCOPE_SCHEMA_DASHBOARD", "B15_SCHEMA_REPORT_RUNTIME_OBSERVATION", "B16_CROSS_REF_FIXTURE_RUNTIME_MOCK", "B17_SCHEMA_BOUNDARY_MUTATION_SIDE_EFFECT", "B18_SCHEMA_VALIDATION_ACTION_CONFIRMATION", "B19_DASHBOARD_QUARANTINE_POST_ACTION", "B20_RESPONSIBILITY_INCIDENT_LONGITUDINAL"}:
        return "S05_VALIDATION_MEMBRANE_OBSERVATION"
    if block in {"B09_LIFE_SUPPORT_DEFENSE_DEVELOPMENT"}:
        return "S06_LIFE_SUPPORT_DEVELOPMENT"
    if block in {"B21_LANGUAGE_RELATIONSHIP_CORE"}:
        return "S07_LANGUAGE_RELATIONSHIP"
    if block in {"B23_NINE_LIFE_TARGETS"}:
        return "S08_LIFE_TARGET_RUNTIMES"
    if block in {"B24_SCHEMA_BUNDLE_RUNNER", "B26_REPOSITORY_RUNNER_MATERIALIZATION", "B27_AUTHORITY_READINESS_CROSS_FILE", "B28_FIRST_CODE_SCHEMA_ARTIFACT"}:
        return "S09_SCHEMA_RUNNER_CODE"
    if block in {"B29_RUNTIME_MOUNT_GROWTH", "B30_RECONSOLIDATION_REPLAY_GROWTH"}:
        return "S10_RUNTIME_GROWTH_RECONSOLIDATION"
    if block == "B99_V0_ENGINEERING_CONTRACTS":
        return "S11_V0_ENGINEERING_CONTRACTS"
    return "UNCLASSIFIED_ENGINEERING_SLICE"


def _dependencies(doc: DocumentMeta) -> list[str]:
    seq = doc.sequence
    if seq is not None and f"{seq:02d}" in CORE_BRIDGE:
        deps = {
            2: ["docs/01o_multiscale_region_connectome_matrix.md", "docs/03_default_executive_salience_networks.md"],
            3: ["docs/01p_network_state_switching_matrix.md", "docs/02_brain_region_and_network_atlas.md"],
            4: ["docs/01n_body_interoception_allostasis_matrix.md", "docs/11_neuromodulation_and_signal_media.md"],
            5: ["docs/01q_memory_engram_consolidation_matrix.md", "docs/08_sleep_dream_fatigue_states.md"],
            6: ["docs/01r_action_reward_inhibition_matrix.md", "docs/94_pain_regret_and_repair_signal_schema.md"],
            7: ["docs/01s_emotion_personality_self_matrix.md", "docs/18_internal_state_and_modulation_vector.md"],
            8: ["docs/01t_sleep_dream_fatigue_runtime_matrix.md", "docs/95_dream_reality_and_offline_life_timeline.md"],
            9: ["docs/01u_language_runtime_core_matrix.md", "docs/85_language_system_life_expression_core.md"],
            10: ["docs/01m_consciousness_attention_workspace_matrix.md", "docs/13_agentic_human_research_synthesis.md"],
            11: ["docs/01l_signal_media_neuromodulation_matrix.md", "docs/04_sensory_thalamus_interoception.md"],
            12: ["docs/15_current_agent_framework_survey.md", "docs/v0/current_agent_shell_reference_2026.md"],
            13: ["docs/14_cross_module_digital_life_map.md", DIRECTION_LOCK_REF],
        }
        return deps.get(seq, [])
    if doc.rel_path.endswith("s00_direction_foundation_engineering_contract.md"):
        return [
            "docs/构思.md",
            "docs/00_research_protocol.md",
            "docs/README.md",
            "docs/13_agentic_human_research_synthesis.md",
            "docs/16_digital_life_gap_register.md",
            DIRECTION_LOCK_REF,
            "docs/v0/README.md",
            "docs/v0/readme_block_engineering_realization_v0.md",
            "docs/v0/digital_life_macro_architecture_v0.md",
            "docs/v0/doc_corpus_ingestor_v0_contract.md",
        ]
    if doc.rel_path.endswith("s01_source_authority_engineering_contract.md"):
        return [
            "docs/00_research_protocol.md",
            "docs/01_literature_matrix.md",
            "docs/142_life_reality_authority_intake_batch_for_02_to_13.md",
            "docs/145_life_reality_02_to_13_authority_rewrite_execution_plan.md",
            "docs/151_life_reality_authority_schema_cross_file_checker_plan.md",
            DIRECTION_LOCK_REF,
            "docs/v0/README.md",
            "docs/v0/v0_implementation_index.md",
            "docs/v0/s00_direction_foundation_engineering_contract.md",
            "docs/v0/readme_block_engineering_realization_v0.md",
        ]
    if doc.rel_path.endswith("s02_neural_life_core_engineering_contract.md"):
        return [
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
            "docs/v0/digital_life_macro_architecture_v0.md",
            "docs/v0/s01_source_authority_engineering_contract.md",
            "docs/v0/readme_block_engineering_realization_v0.md",
        ]
    if doc.rel_path.endswith("s04_state_object_store_engineering_contract.md"):
        return [
            "docs/17_memory_trace_object_model.md",
            "docs/18_internal_state_and_modulation_vector.md",
            "docs/19_offline_consolidation_cycle.md",
            "docs/20_agent_runtime_bridge_contract.md",
            "docs/21_memory_schema_and_audit_protocol.md",
            "docs/22_state_transition_and_threshold_model.md",
            "docs/23_consolidation_report_and_dream_sandbox_protocol.md",
            "docs/24_runtime_adapter_test_suite.md",
            "docs/25_memory_trace_json_schema_examples.md",
            "docs/26_state_machine_examples_and_failure_modes.md",
            "docs/27_consolidation_report_examples.md",
            "docs/28_runtime_adapter_manifest_examples.md",
            "docs/29_memory_validator_rules.md",
            "docs/30_state_transition_validator_rules.md",
            "docs/41_runtime_state_store_schema.md",
            "docs/42_life_core_minimal_object_graph.md",
            "docs/43_policy_to_validator_traceability_matrix.md",
            "docs/44_digital_life_boot_sequence.md",
            "docs/45_boot_sequence_fixture_catalog.md",
            "docs/46_stage_gate_validator_design.md",
            "docs/47_coexistence_boundary_control_interface_spec.md",
            "docs/48_state_store_migration_and_integrity_plan.md",
            "docs/57_scope_graph_manifest_schema.md",
            "docs/61_json_schema_bundle_draft.md",
            "docs/69_schema_file_boundary_and_versioning_plan.md",
            "docs/123_life_reality_runner_repository_layout_and_module_map.md",
            "docs/124_life_reality_minimal_json_file_seed_plan.md",
            "docs/125_life_reality_schema_registry_and_ref_resolution_plan.md",
            "docs/126_life_reality_runner_smoke_command_execution_plan.md",
            "docs/127_life_reality_first_seed_file_content_contract.md",
            "docs/128_life_reality_registry_report_seed_examples.md",
            "docs/129_life_reality_seed_fixture_and_report_validation_cases.md",
            "docs/130_life_reality_first_materialized_json_files_write_plan.md",
            "docs/131_life_reality_registry_runner_minimal_implementation_plan.md",
            "docs/132_life_reality_materialized_json_schema_bundle_write_order.md",
            "docs/133_life_reality_first_json_writer_and_reporter_contract.md",
            "docs/v0/life_state_store_v0_schema.md",
            "docs/v0/s02_neural_life_core_engineering_contract.md",
            "docs/v0/readme_block_engineering_realization_v0.md",
        ]
    if doc.rel_path.endswith("s03_direction_life_membrane_engineering_contract.md"):
        return [
            "docs/13_agentic_human_research_synthesis.md",
            "docs/14_cross_module_digital_life_map.md",
            "docs/15_current_agent_framework_survey.md",
            "docs/16_digital_life_gap_register.md",
            "docs/33_validator_input_contracts.md",
            "docs/34_validator_fixture_catalog.md",
            "docs/35_minimal_validator_runner_design.md",
            "docs/36_longitudinal_evaluation_protocol.md",
            "docs/37_life_support_layer_policy.md",
            "docs/38_defense_layer_and_boundary_policy.md",
            "docs/39_development_policy_and_plasticity_windows.md",
            "docs/40_self_relationship_model_audit_protocol.md",
            "docs/49_machine_readable_policy_manifest.md",
            "docs/52_multi_relation_scope_graph_and_privacy_model.md",
            "docs/54_scope_aware_retrieval_policy.md",
            "docs/55_scope_aware_replay_and_consolidation_policy.md",
            "docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
            "docs/75_external_irreversible_action_confirmation_policy.md",
            "docs/78_runtime_quarantine_dashboard_panel.md",
            "docs/80_post_action_audit_and_correction_policy.md",
            "docs/81_coexistence_event_review_and_responsibility_loop.md",
            "docs/82_incident_report_and_recovery_protocol.md",
            "docs/84_longitudinal_external_action_evaluation_protocol.md",
            "docs/91_life_reality_generation_boundary_principles.md",
            "docs/97_growth_validator_fixture_and_dashboard_plan.md",
            "docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md",
            "docs/99_dream_reality_json_schema_and_fixture_bundle.md",
            "docs/100_life_boundary_statement_rewrite_audit.md",
            "docs/119_life_boundary_full_reality_alignment.md",
            "docs/122_life_boundary_all_reality_declarations_rewrite.md",
            "docs/v0/runtime_v0_architecture.md",
            "docs/v0/birth_readiness_v0_contract.md",
            "docs/v0/first_activation_protocol.md",
            "docs/v0/s02_neural_life_core_engineering_contract.md",
            "docs/v0/s04_state_object_store_engineering_contract.md",
            "docs/v0/readme_block_engineering_realization_v0.md",
        ]
    if doc.rel_path.endswith("v0_implementation_index.md"):
        return [
            DIRECTION_LOCK_REF,
            "docs/v0/README.md",
            "docs/v0/first_activation_engineering_roadmap.md",
            "docs/v0/readme_block_engineering_realization_v0.md",
            "docs/v0/0_to_257_engineering_utilization_map.md",
            "docs/v0/s00_direction_foundation_engineering_contract.md",
            "docs/v0/s01_source_authority_engineering_contract.md",
            "docs/v0/s02_neural_life_core_engineering_contract.md",
            "docs/v0/s03_direction_life_membrane_engineering_contract.md",
            "docs/v0/s04_state_object_store_engineering_contract.md",
        ]
    if doc.group == "v0_contract":
        return [DIRECTION_LOCK_REF, "docs/v0/README.md"]
    if doc.group in {"schema_runner", "activation_growth"}:
        return [DIRECTION_LOCK_REF]
    return []


def _life_targets(doc: DocumentMeta) -> list[str]:
    return [
        target
        for target, rules in LIFE_TARGET_DOC_RULES.items()
        if any(_matches_rule(doc, rule) for rule in rules)
    ]


def _matches_rule(doc: DocumentMeta, rule: str) -> bool:
    prefix = _prefix(doc)
    if rule.startswith("01"):
        return prefix == rule
    if "-" in rule:
        start, end = [int(part) for part in rule.split("-", 1)]
        return _in_range(doc.sequence, start, end)
    return doc.sequence == int(rule)


def _life_target_support(indexed_documents: list[dict[str, Any]]) -> dict[str, list[str]]:
    support = {target: [] for target in LIFE_TARGET_DOC_RULES}
    for document in indexed_documents:
        for target in document["life_targets"]:
            support[target].append(document["path"])
    return support


def _readme_block_coverage(indexed_documents: list[dict[str, Any]]) -> dict[str, list[str]]:
    coverage = {block: [] for block in sorted(EXPECTED_README_BLOCKS)}
    for document in indexed_documents:
        block = document["readme_block"]
        coverage.setdefault(block, []).append(document["path"])
    return coverage


def _engineering_slice_coverage(indexed_documents: list[dict[str, Any]]) -> dict[str, list[str]]:
    coverage = {slice_name: [] for slice_name in sorted(EXPECTED_ENGINEERING_SLICES)}
    for document in indexed_documents:
        slice_name = document["engineering_slice"]
        coverage.setdefault(slice_name, []).append(document["path"])
    return coverage


def _blocked_reasons(indexed_documents: list[dict[str, Any]]) -> list[str]:
    reasons: list[str] = []
    paths = {doc["path"] for doc in indexed_documents}
    if "docs/00_research_protocol.md" not in paths:
        reasons.append("doc_discovery_gate missing docs/00_research_protocol.md")
    if DIRECTION_LOCK_REF not in paths:
        reasons.append(f"doc_discovery_gate missing {DIRECTION_LOCK_REF}")
    for sequence in range(2, 258):
        if not any(doc["sequence"] == sequence for doc in indexed_documents):
            reasons.append(f"doc_discovery_gate missing sequence {sequence}")
    if not any(doc["group"] == "literature_matrix" for doc in indexed_documents):
        reasons.append("doc_discovery_gate missing literature matrix documents")
    uncovered_docs = [doc["path"] for doc in indexed_documents if not doc["runtime_carriers"]]
    unblocked_docs = [
        doc["path"] for doc in indexed_documents
        if doc["readme_block"] == "UNCLASSIFIED_README_BLOCK"
    ]
    unsliced_docs = [
        doc["path"] for doc in indexed_documents
        if doc["engineering_slice"] == "UNCLASSIFIED_ENGINEERING_SLICE"
    ]
    if uncovered_docs:
        reasons.append("carrier_assignment_gate uncovered docs: " + ", ".join(uncovered_docs))
    if unblocked_docs:
        reasons.append("readme_block_gate uncovered docs: " + ", ".join(unblocked_docs))
    if unsliced_docs:
        reasons.append("engineering_slice_gate uncovered docs: " + ", ".join(unsliced_docs))
    return reasons


def _missing_core_bridge(indexed_documents: list[dict[str, Any]]) -> list[int]:
    missing: list[int] = []
    for sequence in range(2, 14):
        doc = next((item for item in indexed_documents if item["sequence"] == sequence), None)
        if doc is None or len(doc["runtime_carriers"]) < 2:
            missing.append(sequence)
    return missing


def _build_index(
    run_id: str,
    indexed_documents: list[dict[str, Any]],
    uncovered_docs: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "doc_carrier_index_v0",
        "run_id": run_id,
        "generated_at": _now_iso(),
        "direction_lock_ref": DIRECTION_LOCK_REF,
        "documents": indexed_documents,
        "coverage": {
            "total_docs": len(indexed_documents),
            "covered_docs": len(indexed_documents) - len(uncovered_docs),
            "uncovered_docs": uncovered_docs,
        },
    }


def _build_dependency_graph(run_id: str, indexed_documents: list[dict[str, Any]]) -> dict[str, Any]:
    edges: list[dict[str, str]] = []
    for document in indexed_documents:
        for carrier in document["runtime_carriers"]:
            edges.append(
                {
                    "from": document["path"],
                    "to": carrier,
                    "edge_type": "implements_runtime_carrier",
                }
            )
        for dependency in document["dependencies"]:
            edges.append(
                {
                    "from": document["path"],
                    "to": dependency,
                    "edge_type": "depends_on_doc",
                }
            )
    return {
        "schema_version": "doc_dependency_graph_v0",
        "run_id": run_id,
        "nodes": [{"id": doc["path"], "kind": "document"} for doc in indexed_documents],
        "edges": edges,
        "core_02_to_13_bridge": CORE_BRIDGE,
    }


def _build_source_authority_report(run_id: str, indexed_documents: list[dict[str, Any]]) -> dict[str, Any]:
    matrix_docs = [
        doc for doc in indexed_documents
        if doc["group"] == "literature_matrix" or "SourceAuthorityRegistry" in doc["runtime_carriers"]
    ]
    matrix_paths = sorted({doc["path"] for doc in matrix_docs})
    return {
        "schema_version": "source_authority_report_v0",
        "run_id": run_id,
        "literature_matrix_count": len(matrix_paths),
        "source_authority_docs": matrix_paths,
        "authority_carriers": sorted(
            {
                carrier
                for doc in matrix_docs
                for carrier in doc["runtime_carriers"]
                if carrier != "SourceAuthorityRegistry"
            }
        ),
        "stage_effect": "supports_birth_readiness",
    }


def _build_doc_ingestion_report(
    *,
    run_id: str,
    status: str,
    stage_effect: str,
    indexed_documents: list[dict[str, Any]],
    uncovered_docs: list[str],
    core_bridge_status: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "doc_ingestion_report_v0",
        "run_id": run_id,
        "status": status,
        "stage_effect": stage_effect,
        "total_docs": len(indexed_documents),
        "covered_docs": len(indexed_documents) - len(uncovered_docs),
        "uncovered_docs": uncovered_docs,
        "core_bridge_status": core_bridge_status,
        "life_target_support": _life_target_support(indexed_documents),
        "readme_block_coverage": _readme_block_coverage(indexed_documents),
        "engineering_slice_coverage": _engineering_slice_coverage(indexed_documents),
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "next_required_command": "life-v0 validate-state" if status == "closed" else "life-v0 ingest-docs --strict",
    }


def _build_receipt(
    *,
    run_id: str,
    docs_dir: Path,
    indexed_documents: list[dict[str, Any]],
    output_refs: list[Path],
    stage_effect: str,
) -> dict[str, Any]:
    return {
        "schema_version": "doc_ingestion_receipt_v0",
        "receipt_id": f"doc_ingestion_{run_id}",
        "run_id": run_id,
        "command": "ingest-docs",
        "docs_ref": str(docs_dir),
        "input_doc_count": len(indexed_documents),
        "input_hashes": {
            doc["path"]: _sha256(Path(docs_dir.parent) / doc["path"])
            for doc in indexed_documents
        },
        "output_refs": [str(path) for path in output_refs],
        "stage_effect": stage_effect,
        "direction_lock_ref": DIRECTION_LOCK_REF,
        "created_at": _now_iso(),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").title()


def _doc_id(doc: DocumentMeta) -> str:
    if doc.group == "v0_contract":
        return "V0_" + re.sub(r"[^A-Za-z0-9]+", "_", doc.path.stem).strip("_").upper()
    if doc.group == "doc_index":
        return "DOC_README"
    if doc.group == "origin_seed":
        return "DOC_ORIGIN_SEED"
    if doc.sequence is None:
        return "DOC_" + re.sub(r"[^A-Za-z0-9]+", "_", doc.path.stem).strip("_").upper()
    suffix = doc.suffix.upper()
    return f"D{doc.sequence:03d}{suffix}"


def _prefix(doc: DocumentMeta) -> str:
    if doc.sequence is None:
        return ""
    return f"{doc.sequence:02d}{doc.suffix}"


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


def _in_range(value: int | None, start: int, end: int) -> bool:
    return value is not None and start <= value <= end


def _in_any_range(value: int | None, *ranges: tuple[int, int]) -> bool:
    return any(_in_range(value, start, end) for start, end in ranges)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _default_run_id() -> str:
    return "doc-ingest-v0-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
