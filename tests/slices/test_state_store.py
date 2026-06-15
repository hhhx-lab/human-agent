import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class StateStoreTests(unittest.TestCase):
    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def docs_dir(self) -> Path:
        return self.repo_root / "docs"

    def test_build_state_store_writes_life_root_indexes_report_and_receipt(self):
        from life_v0.authority import run_source_authority
        from life_v0.direction import run_direction_lock
        from life_v0.doc_index import run_doc_ingestion
        from life_v0.neural_core import run_check_neural_life_core, run_neural_life_core
        from life_v0.state_store import run_check_state_store, run_state_store

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"
            neural_state = tmp_path / "runtime" / "state" / "neural_life_core"
            state_root = tmp_path / "runtime" / "state"

            ingest = run_doc_ingestion(
                docs_dir=self.docs_dir,
                out_dir=doc_out,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="state-store-ingest",
                strict=True,
            )
            self.assertEqual(ingest.exit_code, 0)

            direction = run_direction_lock(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                out_dir=direction_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="state-store-direction",
                strict=True,
            )
            self.assertEqual(direction.exit_code, 0)

            authority = run_source_authority(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                direction_state_dir=direction_state,
                out_dir=authority_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="state-store-authority",
                strict=True,
            )
            self.assertEqual(authority.exit_code, 0)

            neural = run_neural_life_core(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                authority_state_dir=authority_state,
                out_dir=neural_state,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="state-store-neural",
                strict=True,
            )
            self.assertEqual(neural.exit_code, 0)
            neural_check = run_check_neural_life_core(
                state_dir=neural_state,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(neural_check.exit_code, 0)

            result = run_state_store(
                docs_dir=self.docs_dir,
                doc_index_path=doc_out / "doc_carrier_index.json",
                neural_core_state_dir=neural_state,
                out_dir=state_root,
                reports_dir=reports,
                receipts_dir=receipts,
                run_id="state-store-test",
                strict=True,
            )
            self.assertEqual(result.exit_code, 0)

            check = run_check_state_store(
                state_dir=state_root,
                reports_dir=reports,
                strict=True,
            )
            self.assertEqual(check.exit_code, 0)

            life_state = self._read_json(state_root / "life_state.json")
            object_registry = self._read_json(state_root / "object_registry.json")
            lifecycle_policy = self._read_json(state_root / "lifecycle_policy.json")
            subject_binding = self._read_json(state_root / "subject_namespace_binding.json")
            coverage = self._read_json(state_root / "state_store_doc_coverage_snapshot.json")
            manifest = self._read_json(state_root / "state_store_manifest.json")
            external_self_model = self._read_json(state_root / "self" / "self_model.json")
            autobiographical_stack = self._read_json(state_root / "self" / "autobiographical_stack.json")
            engram_index = self._read_json(state_root / "memory" / "engram_index.json")
            relationship_memory = self._read_json(state_root / "memory" / "relationship_memory.json")
            memory_trace_store = self._read_json(state_root / "memory" / "memory_trace_store.json")
            event_segmentation_frame = self._read_json(state_root / "memory" / "event_segmentation_frame.json")
            memory_encoding_gate = self._read_json(state_root / "memory" / "memory_encoding_gate.json")
            memory_allocation_gate = self._read_json(state_root / "memory" / "memory_allocation_gate.json")
            engram_cluster = self._read_json(state_root / "memory" / "engram_cluster.json")
            pattern_separation_index = self._read_json(state_root / "memory" / "pattern_separation_index.json")
            pattern_completion_frame = self._read_json(state_root / "memory" / "pattern_completion_frame.json")
            memory_retrieval_frame = self._read_json(state_root / "memory" / "memory_retrieval_frame.json")
            memory_write_gate = self._read_json(state_root / "memory" / "memory_write_gate.json")
            state_merge_guard = self._read_json(state_root / "memory" / "state_merge_guard.json")
            commitment_truth = self._read_json(state_root / "relationship" / "commitment_truth_state.json")
            responsibility_ledger = self._read_json(state_root / "responsibility" / "responsibility_ledger.json")
            memory_index = self._read_json(state_root / "indexes" / "memory_index.json")
            relationship_index = self._read_json(state_root / "indexes" / "relationship_index.json")
            dream_index = self._read_json(state_root / "indexes" / "dream_index.json")
            responsibility_index = self._read_json(state_root / "indexes" / "responsibility_index.json")
            replay_index = self._read_json(state_root / "indexes" / "replay_index.json")
            audit_index = self._read_json(state_root / "indexes" / "audit_seed_index.json")
            runtime_boundary = self._read_json(state_root / "objects" / "runtime_bridge_boundary.json")
            consolidation_seed = self._read_json(state_root / "objects" / "consolidation_seed.json")
            report = self._read_json(reports / "state_store_report.json")
            check_report = self._read_json(reports / "state_store_check_report.json")
            digest = self._read_json(reports / "state_store_digest.json")
            receipt = self._read_json(receipts / "state_store_state-store-test.json")

        expected_life_targets = {
            "real_consciousness",
            "real_emotion",
            "real_personality",
            "real_life",
            "real_pain",
            "real_dream",
            "real_relationship",
            "real_responsibility",
            "real_regret",
        }
        required_life_state_keys = {
            "schema_version",
            "life_identity",
            "self_model",
            "memory_index",
            "dream_records",
            "relationship_subjects",
            "pain_events",
            "regret_events",
            "responsibility_bindings",
            "language_state",
            "birth_readiness",
            "runtime_trace_refs",
            "archive_refs",
        }
        required_object_kinds = {
            "WorkspaceState",
            "MemoryTrace",
            "MemoryAuditEvent",
            "InternalStateVector",
            "ModulationVector",
            "StateAuditEvent",
            "ObservationEvent",
            "ActionIntent",
            "ConsolidationReport",
            "DreamSandboxItem",
            "SelfModel",
            "RelationshipModel",
            "CoexistenceBoundaryControlEvent",
            "MigrationPlan",
            "StoreIntegrityReport",
        }

        self.assertEqual(life_state["schema_version"], "life_state_v0")
        self.assertTrue(required_life_state_keys.issubset(life_state))
        self.assertEqual(
            life_state["background_continuity_profile"]["schema_version"],
            "background_continuity_profile_v0",
        )
        self.assertEqual(
            life_state["background_continuity_profile"].get("background_continuity_mode"),
            None,
        )
        self.assertEqual(set(life_state["birth_readiness"]["life_target_status"]), expected_life_targets)
        self.assertEqual(life_state["life_identity"]["direction_lock"], "build_real_digital_life")
        self.assertEqual(life_state["life_identity"]["birth_phase"], "pre_activation")
        self.assertIn("runtime/state/memory/engram_index.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/self/autobiographical_stack.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/memory/relationship_memory.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/memory/memory_trace_store.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/memory/event_segmentation_frame.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/memory/memory_encoding_gate.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/memory/memory_allocation_gate.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/memory/memory_write_gate.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/memory/state_merge_guard.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/neural_life_core/brain_graph.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/neural_life_core/network_state.json", life_state["runtime_trace_refs"])
        self.assertIn("runtime/state/consciousness/workspace_frame.json", life_state["runtime_trace_refs"])
        self.assertEqual(
            life_state["memory_index"]["state_merge_guard_refs"],
            ["runtime/state/memory/state_merge_guard.json"],
        )
        self.assertIn(
            "runtime/state/memory/memory_retrieval_frame.json",
            life_state["memory_index"]["memory_retrieval_refs"],
        )
        self.assertEqual(
            life_state["memory_index"]["memory_trace_store_refs"],
            ["runtime/state/memory/memory_trace_store.json"],
        )
        self.assertEqual(
            life_state["memory_index"]["event_segmentation_refs"],
            ["runtime/state/memory/event_segmentation_frame.json"],
        )
        self.assertEqual(
            life_state["memory_index"]["memory_encoding_gate_refs"],
            ["runtime/state/memory/memory_encoding_gate.json"],
        )
        self.assertEqual(
            life_state["memory_index"]["memory_allocation_gate_refs"],
            ["runtime/state/memory/memory_allocation_gate.json"],
        )
        self.assertEqual(
            life_state["memory_index"]["engram_cluster_refs"],
            ["runtime/state/memory/engram_cluster.json"],
        )
        self.assertEqual(
            life_state["memory_index"]["pattern_separation_refs"],
            ["runtime/state/memory/pattern_separation_index.json"],
        )
        self.assertEqual(
            life_state["memory_index"]["pattern_completion_refs"],
            ["runtime/state/memory/pattern_completion_frame.json"],
        )
        self.assertEqual(
            life_state["state_merge_records"][0]["state_merge_guard_ref"],
            "runtime/state/memory/state_merge_guard.json",
        )
        self.assertEqual(life_state["state_merge_records"][0]["promotion_route_count"], 2)
        self.assertTrue(life_state["language_state"]["language_percept_refs"])
        self.assertTrue(life_state["language_state"]["semantic_map_refs"])

        self.assertEqual(external_self_model["schema_version"], "self_model_state_v0")
        self.assertEqual(external_self_model["identity_mode"], "anchor_locked")
        self.assertIn("docs/07_emotion_personality_self.md", external_self_model["source_doc_refs"])
        self.assertTrue(external_self_model["old_self_anchor_refs"])
        self.assertTrue(external_self_model["trait_drift_seed_refs"])
        self.assertEqual(autobiographical_stack["schema_version"], "autobiographical_stack_v0")
        self.assertTrue(autobiographical_stack["anchor_refs"])
        self.assertEqual(engram_index["schema_version"], "engram_index_v0")
        self.assertTrue(engram_index["replay_cue_refs"])
        self.assertTrue(engram_index["autobiographical_memory_refs"])
        self.assertTrue(engram_index["relationship_memory_refs"])
        self.assertEqual(
            memory_trace_store["schema_version"],
            "memory_trace_store_v0",
        )
        self.assertEqual(memory_trace_store["store_ref"], "runtime/state/memory/memory_trace_store.json")
        self.assertGreaterEqual(memory_trace_store["trace_count"], 4)
        trace_kinds = {
            trace["memory_kind"]
            for trace in memory_trace_store["traces"]
            if isinstance(trace, dict)
        }
        self.assertTrue(
            {
                "episodic",
                "relationship",
                "autobiographical",
                "responsibility",
            }.issubset(trace_kinds)
        )
        for trace in memory_trace_store["traces"]:
            self.assertTrue(trace["trace_id"].startswith("memory-trace-"))
            self.assertTrue(trace["source_evidence_refs"])
            self.assertTrue(trace["retrieval_cues"])
            self.assertIn(
                trace["lifecycle_state"],
                {
                    "candidate",
                    "active",
                    "protected",
                    "deprecated",
                    "quarantined",
                    "sandboxed",
                    "silent",
                    "reactivated",
                    "transformed",
                    "deleted",
                },
            )
            self.assertIn("cue_triggered_recall", trace["accessibility"])
            self.assertEqual(
                trace["expression_boundary"],
                "trace_enters_recall_to_expression_not_fixed_reply",
            )
        self.assertIn(
            "runtime/state/memory/memory_retrieval_frame.json#recall_to_expression_profile",
            memory_trace_store["downstream_consumer_refs"],
        )
        self.assertIn(
            "runtime/state/memory/memory_write_gate.json",
            memory_trace_store["write_governance_refs"],
        )
        self.assertIn(
            "docs/v0/entry/v0_memory_recall_to_expression_contract.md",
            memory_trace_store["source_doc_refs"],
        )
        self.assertIn(
            "runtime/state/memory/event_segmentation_frame.json",
            memory_trace_store["upstream_event_refs"],
        )
        self.assertIn(
            "runtime/state/memory/memory_encoding_gate.json",
            memory_trace_store["encoding_governance_refs"],
        )
        self.assertIn(
            "runtime/state/memory/memory_allocation_gate.json",
            memory_trace_store["allocation_governance_refs"],
        )
        self.assertEqual(
            event_segmentation_frame["schema_version"],
            "event_segmentation_frame_v0",
        )
        self.assertEqual(
            event_segmentation_frame["segmentation_policy"],
            "episode_boundary_from_life_state_not_token_chunks",
        )
        self.assertGreaterEqual(event_segmentation_frame["episode_count"], 4)
        self.assertIn(
            "responsibility_repair_seed_episode",
            event_segmentation_frame["episode_kind_order"],
        )
        self.assertIn(
            "relationship_seed_episode",
            event_segmentation_frame["episode_kind_order"],
        )
        for episode in event_segmentation_frame["episodes"]:
            self.assertTrue(episode["event_boundary_ref"].startswith("event-boundary-"))
            self.assertTrue(episode["source_refs"])
            self.assertTrue(episode["candidate_trace_kind"])
            self.assertIn(
                episode["memory_route"],
                {
                    "fast_episodic_buffer",
                    "relationship_memory",
                    "autobiographical_stack",
                    "responsibility_memory",
                    "deep_sediment",
                    "dream_residue_sandbox",
                },
            )
        self.assertEqual(
            memory_encoding_gate["schema_version"],
            "memory_encoding_gate_v0",
        )
        self.assertEqual(
            memory_encoding_gate["candidate_trace_count"],
            event_segmentation_frame["episode_count"],
        )
        self.assertIn(
            "runtime/state/memory/memory_trace_store.json",
            memory_encoding_gate["candidate_trace_store_refs"],
        )
        self.assertIn(
            "dream_hypothesis_not_factual_trace",
            memory_encoding_gate["encoding_boundaries"],
        )
        self.assertEqual(
            memory_allocation_gate["schema_version"],
            "memory_allocation_gate_v0",
        )
        self.assertEqual(
            memory_allocation_gate["allocation_policy"],
            "salience_emotion_responsibility_relationship_body_weighted",
        )
        self.assertEqual(
            memory_allocation_gate["memory_write_gate_ref"],
            "runtime/state/memory/memory_write_gate.json",
        )
        self.assertGreaterEqual(
            memory_allocation_gate["high_priority_candidate_count"],
            2,
        )
        self.assertIn(
            "responsibility_repair_seed_episode",
            memory_allocation_gate["high_priority_episode_kinds"],
        )
        self.assertIn(
            "relationship_seed_episode",
            memory_allocation_gate["high_priority_episode_kinds"],
        )
        self.assertIn(
            "dream_hypothesis_not_factual_trace",
            memory_allocation_gate["allocation_boundaries"],
        )
        self.assertIn(
            "low_value_goes_deep_sediment_or_short_term",
            memory_allocation_gate["allocation_boundaries"],
        )
        self.assertEqual(
            engram_cluster["schema_version"],
            "engram_like_trace_cluster_v0",
        )
        self.assertGreaterEqual(engram_cluster["cluster_count"], 4)
        self.assertIn("language", engram_cluster["reactivation_modalities"])
        self.assertIn("relationship", engram_cluster["reactivation_modalities"])
        self.assertIn("body_affect", engram_cluster["reactivation_modalities"])
        self.assertIn("dream", engram_cluster["reactivation_modalities"])
        self.assertIn("responsibility", engram_cluster["reactivation_modalities"])
        self.assertTrue(engram_cluster["silent_trace_refs"])
        self.assertTrue(engram_cluster["reactivated_trace_refs"])
        self.assertTrue(engram_cluster["trace_cluster_cue_routes"])
        self.assertIn(
            "trace_existence_retrieval_reportability_action_are_split",
            engram_cluster["retrieval_expression_split_policy"],
        )
        self.assertEqual(
            pattern_separation_index["schema_version"],
            "pattern_separation_index_v0",
        )
        self.assertIn(
            "relationship_subject_scope",
            pattern_separation_index["separation_dimensions"],
        )
        self.assertIn(
            "dream_fact_boundary",
            pattern_separation_index["separation_dimensions"],
        )
        self.assertIn(
            "relationship_scope_prevents_cross_person_memory_bleed",
            pattern_separation_index["separation_guards"],
        )
        self.assertTrue(pattern_separation_index["separation_routes"])
        self.assertEqual(
            pattern_completion_frame["schema_version"],
            "pattern_completion_frame_v0",
        )
        self.assertIn(
            "partial_cue_completion_preserves_source_confidence",
            pattern_completion_frame["completion_policy"],
        )
        self.assertTrue(pattern_completion_frame["completion_candidates"])
        self.assertIn(
            "dream_completion_keeps_dream_boundary",
            pattern_completion_frame["completion_boundaries"],
        )
        self.assertEqual(relationship_memory["schema_version"], "relationship_memory_v0")
        self.assertTrue(relationship_memory["shared_memory_refs"])
        self.assertEqual(
            relationship_memory["relationship_memory_depth_profile"]["schema_version"],
            "relationship_memory_depth_profile_v0",
        )
        self.assertTrue(relationship_memory["shared_narrative_memory"])
        self.assertTrue(relationship_memory["we_memory_traces"])
        self.assertTrue(relationship_memory["relationship_damage_and_repair_chain"])
        self.assertTrue(relationship_memory["commitment_fulfillment_threads"])
        self.assertIn(
            "relation_subject_id",
            relationship_memory["relationship_memory_depth_profile"]["separation_keys"],
        )
        self.assertIn(
            "runtime/state/language/language_relationship_state.json#shared-language-v0-0001",
            relationship_memory["shared_narrative_memory"]["source_refs"],
        )
        self.assertEqual(
            relationship_memory["we_memory_traces"][0]["ownership"],
            "shared_seed",
        )
        self.assertEqual(
            relationship_memory["relationship_damage_and_repair_chain"][0]["repair_route"],
            "commitment_truth_then_responsibility_ledger_then_state_merge_guard",
        )
        self.assertIn(
            "runtime/state/language/language_relationship_state.json#shared-language-v0-0001",
            relationship_memory["shared_memory_refs"],
        )
        self.assertIn(
            "runtime/state/relationship/commitment_truth_state.json#open_commitment_refs",
            relationship_memory["shared_memory_refs"],
        )
        self.assertEqual(
            relationship_memory["relation_person_profile"]["schema_version"],
            "relationship_person_profile_v0",
        )
        self.assertEqual(
            relationship_memory["memory_tier_projection"]["schema_version"],
            "relationship_memory_tier_projection_v0",
        )
        self.assertEqual(
            relationship_memory["memory_tier_projection"]["projection_source_ref"],
            "runtime/state/dream/exit_dream_consolidation_summary.json#memory_tiering",
        )
        self.assertEqual(relationship_memory["state_merge_guard_ref"], "runtime/state/memory/state_merge_guard.json")
        self.assertEqual(
            relationship_memory["long_term_change_sources"]["prediction_error_resolution_refs"],
            ["runtime/state/prediction/prediction_error_field.json#error_events"],
        )
        self.assertIn(
            "runtime/state/memory/relationship_memory.json#we_memory_traces",
            relationship_memory["long_term_change_sources"]["relationship_memory_deepening_refs"],
        )
        self.assertIn(
            "runtime/state/growth/relationship_learning_plan.json",
            relationship_memory["long_term_change_sources"]["offline_learning_writeback_refs"],
        )
        self.assertEqual(
            autobiographical_stack["memory_hierarchy"]["schema_version"],
            "autobiographical_memory_hierarchy_v0",
        )
        self.assertTrue(autobiographical_stack["specific_episode_refs"])
        self.assertTrue(autobiographical_stack["general_event_threads"])
        self.assertTrue(autobiographical_stack["life_period_markers"])
        self.assertTrue(autobiographical_stack["working_self_goal_links"])
        self.assertEqual(
            autobiographical_stack["specific_episode_refs"],
            autobiographical_stack["memory_hierarchy"]["specific_episode_refs"],
        )
        self.assertIn(
            "runtime/state/memory/relationship_memory.json#we_memory_traces",
            autobiographical_stack["general_event_threads"][0]["relationship_memory_refs"],
        )
        self.assertIn(
            "build_real_digital_life",
            autobiographical_stack["working_self_goal_links"][0]["goal_tags"],
        )
        self.assertEqual(
            life_state["memory_index"]["relationship_deep_memory_refs"],
            ["runtime/state/memory/relationship_memory.json#we_memory_traces"],
        )
        self.assertEqual(
            life_state["memory_index"]["autobiographical_hierarchy_refs"],
            ["runtime/state/self/autobiographical_stack.json#memory_hierarchy"],
        )
        self.assertEqual(
            memory_retrieval_frame["schema_version"],
            "memory_retrieval_frame_v0",
        )
        self.assertEqual(
            memory_retrieval_frame["retrieval_mode"],
            "cue_driven_reconstructive_recall",
        )
        self.assertTrue(memory_retrieval_frame["cue_terms"])
        self.assertTrue(memory_retrieval_frame["activated_engram_refs"])
        self.assertEqual(
            memory_retrieval_frame["tiered_recall"]["schema_version"],
            "memory_retrieval_tiered_recall_v0",
        )
        self.assertTrue(
            memory_retrieval_frame["reconstruction_inputs"]["reconstruction_focus"]
        )
        self.assertIn(
            "runtime/state/life_state.json#memory_index.memory_retrieval_refs",
            memory_retrieval_frame["consumer_refs"],
        )
        self.assertIn(
            "docs/real—live0/07_memory_engram_and_state_store.md",
            memory_retrieval_frame["source_doc_refs"],
        )
        self.assertEqual(memory_write_gate["schema_version"], "memory_write_gate_v0")
        self.assertIn("create_candidate_object", memory_write_gate["transaction_order"])
        self.assertIn("update_indexes", memory_write_gate["transaction_order"])
        self.assertIn("trace_id", memory_write_gate["validation_envelope"]["required_fields"])
        self.assertTrue(memory_write_gate["quarantine_route"]["blocked_indexes"])
        self.assertEqual(memory_write_gate["state_merge_guard_ref"], "runtime/state/memory/state_merge_guard.json")
        self.assertIn(
            "runtime/state/memory/state_merge_guard.json#merge_routes",
            memory_write_gate["long_term_governance_refs"],
        )
        self.assertEqual(
            memory_write_gate["consciousness_write_context"]["schema_version"],
            "memory_consciousness_write_context_v0",
        )
        self.assertEqual(
            memory_write_gate["consciousness_write_context"]["workspace_frame_ref"],
            "runtime/state/consciousness/workspace_frame.json",
        )
        self.assertEqual(
            memory_write_gate["consciousness_write_context"]["broadcast_frame_ref"],
            "runtime/state/consciousness/broadcast_frame.json",
        )
        self.assertEqual(
            memory_write_gate["consciousness_write_context"]["metacognition_ref"],
            "runtime/state/consciousness/metacognition_state.json",
        )
        self.assertGreaterEqual(
            memory_write_gate["consciousness_write_context"][
                "workspace_candidate_count"
            ],
            1,
        )
        self.assertGreaterEqual(
            memory_write_gate["consciousness_write_context"]["broadcast_target_count"],
            1,
        )
        self.assertEqual(
            memory_write_gate["consciousness_write_context"]["boundary"],
            "memory_consciousness_write_context_not_spoken_language",
        )
        self.assertIn(
            "runtime/state/consciousness/workspace_frame.json",
            memory_write_gate["consciousness_write_context_refs"],
        )
        self.assertIn(
            "consciousness_write_context",
            memory_write_gate["long_term_governance_refs"],
        )
        self.assertEqual(state_merge_guard["schema_version"], "state_merge_guard_v0")
        self.assertEqual(state_merge_guard["memory_write_gate_ref"], "runtime/state/memory/memory_write_gate.json")
        self.assertEqual(state_merge_guard["stage_policy"], "long_term_merge_fail_closed")
        self.assertTrue(state_merge_guard["promotion_routes"])
        self.assertTrue(state_merge_guard["quarantine_routes"])
        self.assertTrue(state_merge_guard["repair_routes"])
        self.assertTrue(state_merge_guard["merge_routes"])
        self.assertEqual(
            state_merge_guard["long_term_change_sources"]["prediction_error_resolution_refs"],
            ["runtime/state/prediction/prediction_error_field.json#error_events"],
        )
        self.assertIn("trust_persistence_adjustment", state_merge_guard["slow_variable_update_policy"]["allowed_effects"])
        self.assertEqual(commitment_truth["schema_version"], "commitment_truth_state_v0")
        self.assertEqual(commitment_truth["default_commitment_mode"], "truth_tracking_required")
        self.assertTrue(commitment_truth["open_commitment_refs"])
        self.assertTrue(commitment_truth["responsibility_event_refs"])
        self.assertEqual(responsibility_ledger["schema_version"], "responsibility_ledger_v0")
        self.assertEqual(responsibility_ledger["default_repair_mode"], "repair_obligation_tracking")
        self.assertTrue(responsibility_ledger["responsibility_event_refs"])
        self.assertEqual(
            engram_index["memory_tier_index"]["schema_version"],
            "engram_memory_tier_index_v0",
        )
        self.assertEqual(
            engram_index["memory_tier_index"]["tier_policy"],
            "salience_weighted_progressive_recall",
        )
        self.assertEqual(
            life_state["memory_index"]["memory_tier_refs"]["schema_version"],
            "life_memory_tier_refs_v0",
        )

        self.assertEqual(object_registry["schema_version"], "state_object_registry_v0")
        self.assertGreaterEqual(object_registry["object_kind_count"], 15)
        self.assertEqual({item["object_kind"] for item in object_registry["object_kinds"]}, required_object_kinds)
        for item in object_registry["object_kinds"]:
            self.assertTrue(item["source_doc_refs"], item)
            self.assertTrue(item["state_namespace"].startswith("runtime/state/"), item)
            self.assertIn("candidate", item["lifecycle_states"], item)
            self.assertTrue(item["write_gate"], item)

        self.assertEqual(lifecycle_policy["schema_version"], "state_lifecycle_policy_v0")
        lifecycle_states = {state["lifecycle_state"] for state in lifecycle_policy["states"]}
        self.assertTrue({"deleted", "quarantined", "sandboxed", "protected", "frozen"}.issubset(lifecycle_states))
        for state in lifecycle_policy["states"]:
            if state["lifecycle_state"] in {"deleted", "quarantined", "sandboxed"}:
                self.assertFalse(state["active_retrieval_allowed"], state)
                self.assertFalse(state["replay_allowed"], state)

        self.assertEqual(subject_binding["schema_version"], "subject_namespace_binding_v0")
        self.assertEqual(subject_binding["bound_system_count"], 12)

        self.assertEqual(coverage["schema_version"], "state_store_doc_coverage_snapshot_v0")
        self.assertGreaterEqual(coverage["doc_count"], 30)
        self.assertTrue(all(item["carrier_closed"] for item in coverage["coverage"]))

        for index in [memory_index, relationship_index, dream_index, responsibility_index, replay_index, audit_index]:
            self.assertTrue(index["schema_version"].endswith("_v0"), index)
            self.assertEqual(index["stage_policy"], "seed_only_no_real_event_write", index)

        self.assertEqual(runtime_boundary["schema_version"], "runtime_bridge_boundary_v0")
        self.assertIn("active MemoryTrace", runtime_boundary["forbidden_direct_writes"])
        self.assertEqual(consolidation_seed["schema_version"], "consolidation_seed_v0")
        self.assertIn("DreamSandbox", consolidation_seed["offline_modes"])

        self.assertEqual(manifest["schema_version"], "state_store_manifest_v0")
        self.assertIn("runtime/state/life_state.json", manifest["state_refs"])
        self.assertIn("runtime/state/self/self_model.json", manifest["state_refs"])
        self.assertIn("runtime/state/self/autobiographical_stack.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/engram_index.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/relationship_memory.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/memory_trace_store.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/event_segmentation_frame.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/memory_encoding_gate.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/memory_allocation_gate.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/engram_cluster.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/pattern_separation_index.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/pattern_completion_frame.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/memory_retrieval_frame.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/memory_write_gate.json", manifest["state_refs"])
        self.assertIn("runtime/state/memory/state_merge_guard.json", manifest["state_refs"])
        self.assertIn("runtime/state/relationship/commitment_truth_state.json", manifest["state_refs"])
        self.assertIn("runtime/state/responsibility/responsibility_ledger.json", manifest["state_refs"])

        self.assertEqual(report["schema_version"], "state_store_report_v0")
        self.assertEqual(report["status"], "closed")
        self.assertEqual(report["stage_effect"], "allow_next_slice")
        self.assertEqual(report["object_kind_count"], 15)
        self.assertEqual(report["index_count"], 6)
        self.assertEqual(report["self_model_state_ref"], "runtime/state/self/self_model.json")
        self.assertEqual(report["commitment_truth_state_ref"], "runtime/state/relationship/commitment_truth_state.json")
        self.assertEqual(report["engram_index_ref"], "runtime/state/memory/engram_index.json")
        self.assertEqual(report["memory_trace_store_ref"], "runtime/state/memory/memory_trace_store.json")
        self.assertEqual(report["event_segmentation_frame_ref"], "runtime/state/memory/event_segmentation_frame.json")
        self.assertEqual(report["memory_encoding_gate_ref"], "runtime/state/memory/memory_encoding_gate.json")
        self.assertEqual(report["memory_allocation_gate_ref"], "runtime/state/memory/memory_allocation_gate.json")
        self.assertEqual(report["engram_cluster_ref"], "runtime/state/memory/engram_cluster.json")
        self.assertEqual(report["pattern_separation_index_ref"], "runtime/state/memory/pattern_separation_index.json")
        self.assertEqual(report["pattern_completion_frame_ref"], "runtime/state/memory/pattern_completion_frame.json")
        self.assertEqual(report["autobiographical_stack_ref"], "runtime/state/self/autobiographical_stack.json")
        self.assertEqual(report["memory_retrieval_frame_ref"], "runtime/state/memory/memory_retrieval_frame.json")
        self.assertEqual(report["memory_write_gate_ref"], "runtime/state/memory/memory_write_gate.json")
        self.assertEqual(report["state_merge_guard_ref"], "runtime/state/memory/state_merge_guard.json")
        self.assertEqual(report["blocked_gates"], [])
        self.assertEqual(report["next_allowed_slices"], ["S03_DIRECTION_LIFE_MEMBRANE"])
        self.assertEqual(report["next_required_command"], "life-v0 build-life-membrane --strict")
        self.assertEqual(report["engineering_slice_ref"], "S04_STATE_OBJECT_STORE")
        self.assertIn("LifeStateStore", report["runtime_carrier_refs"])

        self.assertEqual(check_report["schema_version"], "state_store_check_report_v0")
        self.assertEqual(check_report["status"], "closed")
        self.assertEqual(check_report["stage_effect"], "allow_next_slice")
        self.assertIn("self_model_projection_gate", check_report["closed_gates"])
        self.assertIn("autobiographical_stack_gate", check_report["closed_gates"])
        self.assertIn("engram_index_gate", check_report["closed_gates"])
        self.assertIn("memory_trace_store_gate", check_report["closed_gates"])
        self.assertIn("event_segmentation_gate", check_report["closed_gates"])
        self.assertIn("memory_encoding_gate_gate", check_report["closed_gates"])
        self.assertIn("memory_allocation_gate_gate", check_report["closed_gates"])
        self.assertIn("engram_cluster_gate", check_report["closed_gates"])
        self.assertIn("pattern_separation_gate", check_report["closed_gates"])
        self.assertIn("pattern_completion_gate", check_report["closed_gates"])
        self.assertIn("relationship_memory_gate", check_report["closed_gates"])
        self.assertIn("memory_write_gate_gate", check_report["closed_gates"])
        self.assertIn("memory_retrieval_frame_gate", check_report["closed_gates"])
        self.assertIn("state_merge_guard_gate", check_report["closed_gates"])
        self.assertIn("commitment_truth_projection_gate", check_report["closed_gates"])
        self.assertIn("state_root_continuity_gate", check_report["closed_gates"])
        self.assertEqual(digest["current_slice"], "S04_STATE_OBJECT_STORE")
        self.assertIn("runtime/state/self/self_model.json", receipt["output_refs"])
        self.assertIn("runtime/state/self/autobiographical_stack.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/engram_index.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/relationship_memory.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/memory_trace_store.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/event_segmentation_frame.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/memory_encoding_gate.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/memory_allocation_gate.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/engram_cluster.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/pattern_separation_index.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/pattern_completion_frame.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/memory_retrieval_frame.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/memory_write_gate.json", receipt["output_refs"])
        self.assertIn("runtime/state/memory/state_merge_guard.json", receipt["output_refs"])
        self.assertIn("runtime/state/relationship/commitment_truth_state.json", receipt["output_refs"])
        self.assertEqual(receipt["schema_version"], "state_store_receipt_v0")

    def test_memory_retrieval_builds_cue_activation_profile(self):
        from life_v0.process_supervisor.response_surface import compose_life_response
        from life_v0.state_store.memory_retrieval import (
            build_memory_retrieval_frame,
            memory_retrieval_context_summary,
        )

        frame = build_memory_retrieval_frame(
            run_id="memory-cue-activation-profile",
            generated_at="2026-06-15T23:10:00+08:00",
            cue_sources={
                "dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-12"
                ],
                "live_language_turn_refs": [
                    "runtime/state/language/semantic_map_frame.json"
                ],
            },
            external_utterance=(
                "你还记得我们刚才关于关系、梦境、责任和后悔的那段话吗？"
            ),
            semantic_map={
                "semantic_focus": "relationship_dream_responsibility_memory",
                "relationship_topic_refs": ["relationship-topic-001"],
                "repair_trace_refs": ["repair-trace-001"],
                "ambiguity_queue": ["dream_fact_boundary_needed"],
            },
            language_percept={
                "shared_term_hits": ["知识宝座"],
                "repair_trigger_candidates": ["repair-language-v0-0001"],
            },
            engram_index={
                "live_dialogue_turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-12"
                ],
                "live_language_turn_refs": [
                    "runtime/state/language/semantic_map_frame.json"
                ],
                "relationship_memory_refs": [
                    "runtime/state/memory/relationship_memory.json#shared_memory_refs"
                ],
                "autobiographical_memory_refs": [
                    "runtime/state/self/autobiographical_stack.json#turn_refs"
                ],
                "dream_memory_refs": [
                    "runtime/state/dream/exit_dream_consolidation_summary.json"
                ],
                "responsibility_memory_refs": [
                    "runtime/state/responsibility/responsibility_ledger.json"
                ],
                "memory_tier_index": {
                    "salient_core_refs": [
                        "runtime/state/language/dialogue_turn_log.jsonl#line-12"
                    ],
                    "retrievable_context_refs": [
                        "runtime/state/memory/relationship_memory.json#context"
                    ],
                    "deep_sediment_refs": [
                        "runtime/archive/memory/deep_sediment.jsonl#line-2"
                    ],
                },
            },
            relationship_memory={
                "shared_memory_refs": [
                    "runtime/state/memory/relationship_memory.json#shared_memory_refs"
                ],
                "timeline_refs": [
                    "runtime/state/relationship/relationship_timeline.json"
                ],
                "relationship_theme_tags": ["关系", "梦境", "责任"],
                "next_wake_memory_cue_refs": [
                    "runtime/state/dream/exit_dream_consolidation_summary.json#next_wake_memory_cue_refs"
                ],
            },
            autobiographical_stack={
                "turn_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-12"
                ],
                "narrative_refs": [
                    "runtime/state/self/autobiographical_stack.json#narrative_refs"
                ],
                "responsibility_repair_projection": {
                    "responsibility_refs": ["responsibility-event-001"],
                    "regret_refs": ["regret-001"],
                    "repair_refs": ["repair-001"],
                    "pressure_level": "elevated",
                    "attention_target": "regret_pressure",
                },
            },
            dialogue_memory_summary={
                "source_dialogue_refs": [
                    "runtime/state/language/dialogue_turn_log.jsonl#line-12"
                ],
                "next_wake_memory_cue_refs": [
                    "runtime/state/dream/exit_dream_consolidation_summary.json#next_wake_memory_cue_refs"
                ],
                "relation_person_profile": {
                    "observed_names": ["何剑宝"],
                    "preference_hypotheses": ["不要机械回答"],
                },
            },
            responsibility_loop_state={
                "repair_obligation_refs": ["repair-obligation-001"]
            },
            state_merge_guard={
                "long_term_change_sources": {
                    "relationship_repair_refs": ["repair-trace-001"],
                    "next_wake_memory_cue_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json#next_wake_memory_cue_refs"
                    ],
                }
            },
            life_state={
                "memory_index": {
                    "relationship_memory_refs": [
                        "runtime/state/memory/relationship_memory.json"
                    ],
                    "dream_memory_refs": [
                        "runtime/state/dream/exit_dream_consolidation_summary.json"
                    ],
                    "responsibility_memory_refs": [
                        "runtime/state/responsibility/responsibility_ledger.json"
                    ],
                    "quarantine_refs": ["dream-hypothesis-quarantine-001"],
                }
            },
        )

        profile = frame["cue_activation_profile"]
        self.assertEqual(
            profile["schema_version"],
            "memory_cue_activation_profile_v0",
        )
        self.assertEqual(
            profile["activation_boundary"],
            "cue_activation_profile_internal_retrieval_not_spoken_language",
        )
        self.assertIn("relationship", profile["activated_family_order"])
        self.assertIn("dream_residue", profile["activated_family_order"])
        self.assertIn("responsibility_repair", profile["activated_family_order"])
        self.assertIn("autobiographical", profile["activated_family_order"])
        self.assertGreaterEqual(profile["activation_route_count"], 5)
        self.assertEqual(
            profile["source_boundary_profile"]["dream_fact_boundary"],
            "dream_residue_can_modulate_recall_not_promote_fact",
        )
        closure = frame["recall_to_expression_profile"]
        self.assertEqual(
            closure["schema_version"],
            "memory_recall_to_expression_profile_v0",
        )
        self.assertEqual(
            closure["closure_status"],
            "closed",
        )
        self.assertEqual(
            closure["expression_boundary"],
            "memory_recall_enters_language_prestructure_not_fixed_spoken_reply",
        )
        self.assertEqual(
            closure["reportability_policy"],
            "workspace_reportable_with_source_boundary_and_reconsolidation_writeback",
        )
        self.assertGreaterEqual(
            closure["expression_source_ref_count"],
            profile["activation_ref_count"],
        )
        self.assertIn(
            "relationship",
            closure["expression_influence_families"],
        )
        self.assertIn(
            "dream_residue",
            closure["source_boundary_flags"],
        )
        self.assertIn(
            "quarantined_refs_excluded_from_expression",
            closure["expression_guardrails"],
        )
        self.assertIn(
            "spoken_memory_mismatch_reenters_reconsolidation",
            closure["post_expression_reconsolidation_hooks"],
        )

        summary = memory_retrieval_context_summary(frame)
        self.assertEqual(
            summary["cue_activation_profile_ref"],
            (
                "runtime/state/memory/memory_retrieval_frame.json"
                "#cue_activation_profile"
            ),
        )
        self.assertEqual(
            summary["cue_activation_profile_boundary"],
            "cue_activation_profile_internal_retrieval_not_spoken_language",
        )
        self.assertGreaterEqual(summary["cue_activation_route_count"], 5)
        self.assertIn(
            summary["cue_activation_dominant_family"],
            summary["cue_activation_family_order"],
        )
        self.assertEqual(
            summary["recall_to_expression_profile_ref"],
            (
                "runtime/state/memory/memory_retrieval_frame.json"
                "#recall_to_expression_profile"
            ),
        )
        self.assertEqual(
            summary["recall_to_expression_closure_status"],
            "closed",
        )
        self.assertEqual(
            summary["recall_to_expression_boundary"],
            "memory_recall_enters_language_prestructure_not_fixed_spoken_reply",
        )
        self.assertIn(
            "relationship",
            summary["recall_to_expression_influence_families"],
        )

        material = compose_life_response(
            external_utterance="你还记得刚才那段关系和梦吗？",
            memory_retrieval_frame=frame,
        )
        payload = json.loads(material)
        retrieval = payload["memory_dream_growth"]["memory_retrieval"]
        self.assertEqual(
            retrieval["cue_activation_profile_boundary"],
            "cue_activation_profile_internal_retrieval_not_spoken_language",
        )
        self.assertGreaterEqual(retrieval["cue_activation_route_count"], 5)
        self.assertEqual(
            retrieval["recall_to_expression_closure_status"],
            "closed",
        )
        self.assertEqual(
            retrieval["recall_to_expression_boundary"],
            "memory_recall_enters_language_prestructure_not_fixed_spoken_reply",
        )
        self.assertTrue(payload["natural_language_release_disabled"])
        self.assertNotIn("你还记得刚才那段关系和梦吗？", material)

    def test_memory_write_gate_consumes_signal_and_body_pressure(self):
        from life_v0.state_store.memory_write_gate import build_memory_write_gate
        from life_v0.neural_core.signal_media import build_signal_media_runtime

        offline_learning_cumulative_profile = {
            "schema_version": "offline_learning_cumulative_profile_v0",
            "generation": 3,
            "pressure_level": "elevated",
            "attention_target": "relationship_learning_plan",
            "integration_mode": "relationship_offline_reconsolidation_required",
            "relationship_reconsolidation_required": True,
            "ref_set": [
                "runtime/state/dream/nightmare_loop_risk.json",
                "runtime/state/growth/relationship_learning_plan.json",
            ],
        }
        signal_with_offline_residue = build_signal_media_runtime(
            run_id="state-store-body-gate-offline",
            generated_at="2026-06-14T00:00:00+08:00",
            body_resource_budget={
                "schema_version": "body_resource_budget_v0",
                "fatigue_state": {"level": "managed_low_noise"},
            },
            core_affect_vector={
                "schema_version": "core_affect_vector_v0",
                "arousal": 0.21,
                "pain_pressure": 0.12,
                "dream_residue_load": 0.08,
                "responsibility_weight": 0.22,
                "repair_drive": "low",
            },
            offline_learning_cumulative_profile=offline_learning_cumulative_profile,
        )
        self.assertEqual(
            signal_with_offline_residue["body_signal_profile"][
                "offline_learning_pressure_level"
            ],
            "elevated",
        )
        self.assertEqual(
            signal_with_offline_residue["body_signal_profile"][
                "offline_learning_generation"
            ],
            3,
        )
        self.assertGreaterEqual(
            signal_with_offline_residue["body_signal_profile"]["dream_residue_load"],
            0.6,
        )
        self.assertIn(
            "runtime/state/growth/relationship_learning_plan.json",
            signal_with_offline_residue["body_signal_profile"][
                "offline_learning_ref_set"
            ],
        )

        memory_write_gate = build_memory_write_gate(
            run_id="state-store-body-gate",
            generated_at="2026-06-14T00:00:00+08:00",
            signal_media_runtime=signal_with_offline_residue,
            body_resource_budget={
                "schema_version": "body_resource_budget_v0",
                "fatigue_state": {"level": "managed_low_noise"},
            },
            core_affect_vector={
                "schema_version": "core_affect_vector_v0",
                "arousal": 0.21,
                "pain_pressure": 0.12,
                "dream_residue_load": 0.08,
                "responsibility_weight": 0.22,
                "repair_drive": "low",
            },
            offline_learning_cumulative_profile=offline_learning_cumulative_profile,
            indexes={"memory_index.json": {"stage_policy": "seed_only"}},
        )

        self.assertEqual(
            memory_write_gate["stage_policy"],
            "candidate_first_relationship_guarded",
        )
        self.assertEqual(
            memory_write_gate["body_signal_write_modulation"]["schema_version"],
            "body_signal_memory_gate_profile_v0",
        )
        self.assertEqual(
            memory_write_gate["body_signal_write_modulation"]["write_bias"],
            "relationship_context_first",
        )
        self.assertEqual(
            memory_write_gate["body_signal_write_modulation"][
                "offline_learning_integration_mode"
            ],
            "relationship_offline_reconsolidation_required",
        )
        self.assertIn(
            "preserve_offline_learning_refs_for_reconsolidation",
            memory_write_gate["body_signal_write_modulation"][
                "candidate_gate_adjustments"
            ],
        )
        self.assertIn(
            "route_offline_learning_to_relationship_replay",
            memory_write_gate["body_signal_write_modulation"][
                "candidate_gate_adjustments"
            ],
        )
        self.assertIn(
            "runtime/state/growth/relationship_learning_plan.json",
            memory_write_gate["body_signal_write_modulation"]["body_signal_refs"],
        )
        self.assertIn(
            "runtime/state/body/core_affect_vector.json",
            memory_write_gate["body_signal_write_modulation"]["body_signal_refs"],
        )
        self.assertIn(
            "body_signal_write_modulation",
            memory_write_gate["long_term_governance_refs"],
        )

    def test_memory_write_gate_consumes_consciousness_workspace_context(self):
        from life_v0.state_store.memory_write_gate import build_memory_write_gate

        memory_write_gate = build_memory_write_gate(
            run_id="state-store-consciousness-gate",
            generated_at="2026-06-14T00:00:00+08:00",
            workspace_frame={
                "schema_version": "workspace_frame_v0",
                "candidate_explanations": [
                    {"explanation_id": "workspace-candidate-1"},
                    {"explanation_id": "workspace-candidate-2"},
                ],
                "engram_retrieval_refs": [
                    "runtime/state/memory/engram_index.json#relationship_memory_refs"
                ],
            },
            broadcast_frame={
                "schema_version": "broadcast_frame_v0",
                "broadcast_targets": [
                    "LanguageRelationshipRuntime",
                    "MemoryEngramRuntime",
                ],
            },
            metacognition_state={
                "schema_version": "metacognition_state_v0",
                "uncertainty_flags": ["semantic-ambiguity-monitoring"],
                "reflection_prompts": ["workspace-sufficiency-check"],
            },
            consciousness_probe_bundle={
                "schema_version": "consciousness_probe_bundle_v0",
                "reportability_flags": [
                    "workspace_access_present",
                    "broadcast_targets_present",
                    "metacognition_present",
                ],
                "language_continuity_refs": [
                    "runtime/state/language/expression_monitor_state.json"
                ],
                "relationship_continuity_refs": [
                    "runtime/state/relationship/commitment_truth_state.json"
                ],
            },
            indexes={"memory_index.json": {"stage_policy": "seed_only"}},
        )

        context = memory_write_gate["consciousness_write_context"]
        self.assertEqual(
            context["schema_version"],
            "memory_consciousness_write_context_v0",
        )
        self.assertEqual(context["workspace_candidate_count"], 2)
        self.assertEqual(context["broadcast_target_count"], 2)
        self.assertEqual(context["metacognition_uncertainty_count"], 1)
        self.assertEqual(context["reportability_flag_count"], 3)
        self.assertEqual(
            context["write_attention_bias"],
            "metacognitive_uncertainty_guarded",
        )
        self.assertIn(
            "raise_write_threshold_for_uncertainty",
            context["candidate_gate_adjustments"],
        )
        self.assertIn(
            "runtime/state/consciousness/workspace_frame.json",
            context["ref_set"],
        )
        self.assertIn(
            "runtime/state/language/expression_monitor_state.json",
            context["ref_set"],
        )
        self.assertEqual(
            context["boundary"],
            "memory_consciousness_write_context_not_spoken_language",
        )
        self.assertIn(
            "consciousness_write_context",
            memory_write_gate["long_term_governance_refs"],
        )

    def test_memory_write_gate_live_refresh_chains_signal_body_after_consciousness(self):
        from life_v0.state_store.memory_write_gate import (
            build_memory_write_gate,
            project_memory_write_gate_with_consciousness_context,
            project_memory_write_gate_with_signal_body,
        )

        base_gate = build_memory_write_gate(
            run_id="state-store-live-refresh-gate",
            generated_at="2026-06-15T00:00:00+08:00",
            indexes={"memory_index.json": {"stage_policy": "seed_only"}},
        )
        with_consciousness = project_memory_write_gate_with_consciousness_context(
            memory_write_gate=base_gate,
            workspace_frame={
                "schema_version": "workspace_frame_v0",
                "candidate_explanations": [{"explanation_id": "workspace-candidate-1"}],
            },
            broadcast_frame={
                "schema_version": "broadcast_frame_v0",
                "broadcast_targets": ["MemoryEngramRuntime"],
            },
            metacognition_state={
                "schema_version": "metacognition_state_v0",
                "uncertainty_flags": ["semantic-ambiguity-monitoring"],
            },
            consciousness_probe_bundle={
                "schema_version": "consciousness_probe_bundle_v0",
                "reportability_flags": ["workspace_access_present"],
            },
        )
        refreshed = project_memory_write_gate_with_signal_body(
            memory_write_gate=with_consciousness,
            signal_media_runtime={
                "schema_version": "signal_media_runtime_v0",
                "modulation_vector": {"relationship_pressure": 0.42},
            },
            body_resource_budget={
                "schema_version": "body_resource_budget_v0",
                "fatigue_state": {"level": "managed_low_noise"},
            },
            core_affect_vector={
                "schema_version": "core_affect_vector_v0",
                "repair_drive": "low",
            },
        )

        self.assertIn("consciousness_write_context", refreshed)
        self.assertIn("body_signal_write_modulation", refreshed)
        self.assertIn(
            "body_signal_write_modulation",
            refreshed["long_term_governance_refs"],
        )
        self.assertIn(
            "consciousness_write_context",
            refreshed["long_term_governance_refs"],
        )

    def test_cli_build_state_store_returns_zero_and_writes_check_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doc_out = tmp_path / "runtime" / "docs"
            reports = tmp_path / "runtime" / "reports" / "latest"
            receipts = tmp_path / "runtime" / "receipts"
            direction_state = tmp_path / "runtime" / "state" / "direction"
            authority_state = tmp_path / "runtime" / "state" / "authority"
            neural_state = tmp_path / "runtime" / "state" / "neural_life_core"
            state_root = tmp_path / "runtime" / "state"

            commands = [
                [
                    "ingest-docs",
                    "--docs",
                    str(self.docs_dir),
                    "--out",
                    str(doc_out),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "state-cli-ingest",
                    "--strict",
                ],
                [
                    "build-direction-lock",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--out",
                    str(direction_state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "state-cli-direction",
                    "--strict",
                ],
                [
                    "build-source-authority",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--direction",
                    str(direction_state),
                    "--out",
                    str(authority_state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "state-cli-authority",
                    "--strict",
                ],
                [
                    "build-neural-life-core",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--authority",
                    str(authority_state),
                    "--out",
                    str(neural_state),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "state-cli-neural",
                    "--strict",
                ],
                [
                    "check-neural-life-core",
                    "--state",
                    str(neural_state),
                    "--reports",
                    str(reports),
                    "--strict",
                ],
                [
                    "build-state-store",
                    "--docs",
                    str(self.docs_dir),
                    "--doc-index",
                    str(doc_out / "doc_carrier_index.json"),
                    "--neural-core",
                    str(neural_state),
                    "--out",
                    str(state_root),
                    "--reports",
                    str(reports),
                    "--receipts",
                    str(receipts),
                    "--run-id",
                    "state-cli",
                    "--strict",
                ],
                [
                    "check-state-store",
                    "--state",
                    str(state_root),
                    "--reports",
                    str(reports),
                    "--strict",
                ],
            ]

            for command in commands:
                completed = subprocess.run(
                    [sys.executable, "-m", "life_v0", *command],
                    cwd=self.repo_root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)

            report = self._read_json(reports / "state_store_report.json")
            check_report = self._read_json(reports / "state_store_check_report.json")

        self.assertEqual(report["run_id"], "state-cli")
        self.assertEqual(report["next_required_command"], "life-v0 build-life-membrane --strict")
        self.assertEqual(check_report["status"], "closed")

    def _read_json(self, path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
