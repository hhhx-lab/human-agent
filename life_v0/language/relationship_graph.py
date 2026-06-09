from __future__ import annotations


def build_relationship_subject_graph(
    *,
    run_id: str,
    generated_at: str,
    source_doc_refs: list[str],
) -> dict[str, object]:
    subject = {
        "relationship_id": "rel-v0-0001",
        "relation_role": "friend",
        "subject_name_ref": "relation-subject-v0-0001",
        "shared_memory_refs": ["runtime/state/life_state.json#memory_index.relationship_memory_refs"],
        "shared_language_refs": ["runtime/state/language/language_relationship_state.json#shared-language-v0-0001"],
        "commitment_refs": ["runtime/state/language/commitment_repair_language_index.json#commitment-v0-0001"],
        "boundary_refs": ["runtime/state/membrane/relationship_subject_boundary.json"],
        "repair_obligation_refs": ["runtime/state/language/commitment_repair_language_index.json#repair-obligation-v0-0001"],
        "last_contact_ref": "runtime/state/language/inner_speech_frame.json",
        "relationship_stage": "pre_activation",
    }
    return {
        "schema_version": "relationship_subject_graph_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "status": "closed",
        "subjects": [subject],
        "graph_edges": [
            {
                "from": subject["relationship_id"],
                "to": "runtime/state/language/language_relationship_state.json#shared-language-v0-0001",
                "edge_type": "shared_language",
            }
        ],
        "timeline_refs": [
            "docs/96_real_relationship_longitudinal_timeline.md",
            "docs/101_relationship_timeline_json_schema_and_fixture_bundle.md",
        ],
        "source_doc_refs": source_doc_refs,
    }
