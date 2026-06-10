from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ACTIVE_SLICE = "S11_V0_ENGINEERING_CONTRACTS"
READ_ME_BLOCK_REFS = ["B99_V0_ENGINEERING_CONTRACTS"]
RUNTIME_CARRIER_REFS = ["V0ContractCoverageRuntime"]
NEXT_REQUIRED_COMMAND = "life-v0 first-activation-preflight --strict"

V0_DOC_FILE_RULES: dict[str, dict[str, Any]] = {
    "docs/v0/README.md": {
        "role": "v0_root_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
            "docs/README.md",
        ],
    },
    "docs/v0/entry/README.md": {
        "role": "v0_entry_cabinet_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/README.md",
            "docs/v0/entry/v0_implementation_index.md",
        ],
    },
    "docs/v0/entry/v0_implementation_index.md": {
        "role": "v0_global_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
            "docs/v0/README.md",
        ],
    },
    "docs/v0/entry/v0_delivery_status_board.md": {
        "role": "delivery_status_board",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/entry/v0_implementation_index.md",
            "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
        ],
    },
    "docs/v0/entry/v0_module_execution_catalog.md": {
        "role": "module_execution_catalog",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/entry/v0_implementation_index.md",
            "docs/v0/mapping/readme_block_engineering_realization_v0.md",
        ],
    },
    "docs/v0/mapping/readme_block_engineering_realization_v0.md": {
        "role": "readme_block_realization_map",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/README.md",
            "docs/v0/entry/v0_implementation_index.md",
        ],
    },
    "docs/v0/mapping/README.md": {
        "role": "v0_mapping_cabinet_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/README.md",
            "docs/v0/mapping/readme_block_engineering_realization_v0.md",
        ],
    },
    "docs/v0/mapping/0_to_257_engineering_utilization_map.md": {
        "role": "zero_to_258_utilization_map",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
            "docs/v0/mapping/readme_block_engineering_realization_v0.md",
        ],
    },
    "docs/v0/architecture/first_activation_engineering_roadmap.md": {
        "role": "activation_roadmap",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/shared_contracts/first_activation_protocol.md",
            "docs/v0/architecture/runtime_v0_architecture.md",
        ],
    },
    "docs/v0/architecture/README.md": {
        "role": "architecture_cabinet_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/README.md",
            "docs/v0/architecture/digital_life_macro_architecture_v0.md",
        ],
    },
    "docs/v0/architecture/digital_life_macro_architecture_v0.md": {
        "role": "macro_architecture",
        "slice": "S02_NEURAL_LIFE_CORE",
        "status": "closed",
        "source_refs": [
            "docs/13_agentic_human_research_synthesis.md",
            "docs/14_cross_module_digital_life_map.md",
        ],
    },
    "docs/v0/architecture/runtime_v0_architecture.md": {
        "role": "runtime_architecture",
        "slice": "S10_RUNTIME_GROWTH_RECONSOLIDATION",
        "status": "closed",
        "source_refs": [
            "docs/v0/architecture/digital_life_macro_architecture_v0.md",
            "docs/v0/shared_contracts/first_activation_protocol.md",
        ],
    },
    "docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md": {
        "role": "theory_closure_engineering_readiness_audit",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/16_digital_life_gap_register.md",
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
        ],
    },
    "docs/v0/code_architecture/README.md": {
        "role": "code_architecture_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/README.md",
            "docs/v0/code_framework/README.md",
        ],
    },
    "docs/v0/code_blueprints/README.md": {
        "role": "code_blueprints_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/code_framework/README.md",
            "docs/v0/code_architecture/README.md",
        ],
    },
    "docs/v0/code_blueprints/01_full_system_code_blueprint.md": {
        "role": "full_system_code_blueprint",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
            "docs/v0/code_architecture/01_life_code_stack_and_package_layers.md",
        ],
    },
    "docs/v0/code_blueprints/02_conversation_language_relationship_blueprint.md": {
        "role": "conversation_language_relationship_blueprint",
        "slice": "S07_LANGUAGE_RELATIONSHIP",
        "status": "closed",
        "source_refs": [
            "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
            "docs/v0/engineering_depth/03_language_relationship_longitudinal_engineering.md",
        ],
    },
    "docs/v0/code_blueprints/03_body_affect_dream_growth_blueprint.md": {
        "role": "body_affect_dream_growth_blueprint",
        "slice": "S06_LIFE_SUPPORT_DEVELOPMENT",
        "status": "closed",
        "source_refs": [
            "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
            "docs/v0/engineering_depth/04_body_affect_dream_growth_engineering.md",
        ],
    },
    "docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md": {
        "role": "prediction_membrane_validation_blueprint",
        "slice": "S05_VALIDATION_MEMBRANE_OBSERVATION",
        "status": "closed",
        "source_refs": [
            "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
            "docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md",
        ],
    },
    "docs/v0/code_blueprints/05_birth_residency_terminal_blueprint.md": {
        "role": "birth_residency_terminal_blueprint",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md",
            "docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md",
        ],
    },
    "docs/v0/code_blueprints/06_runtime_state_report_receipt_manifest.md": {
        "role": "runtime_state_report_receipt_manifest",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/architecture/runtime_v0_architecture.md",
            "docs/v0/shared_contracts/runner_cli_report_contract.md",
        ],
    },
    "docs/v0/code_blueprints/07_theory_to_package_trace_contract.md": {
        "role": "theory_to_package_trace_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/mapping/0_to_257_engineering_utilization_map.md",
            "docs/v0/engineering_depth/07_theory_to_code_trace_matrix.md",
        ],
    },
    "docs/v0/code_architecture/01_life_code_stack_and_package_layers.md": {
        "role": "life_code_stack_package_layers",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/architecture/digital_life_macro_architecture_v0.md",
            "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
        ],
    },
    "docs/v0/code_architecture/02_runtime_object_bus_and_flow_contract.md": {
        "role": "runtime_object_bus_flow_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md",
            "docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md",
        ],
    },
    "docs/v0/code_architecture/03_build_order_and_definition_of_done.md": {
        "role": "build_order_definition_of_done",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md",
            "docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md",
        ],
    },
    "docs/v0/code_architecture/04_language_as_primary_expression_system.md": {
        "role": "language_primary_expression_system",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
            "docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md",
        ],
    },
    "docs/v0/code_architecture/05_module_reading_and_execution_map.md": {
        "role": "module_reading_execution_map",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/entry/v0_module_execution_catalog.md",
            "docs/v0/code_architecture/01_life_code_stack_and_package_layers.md",
        ],
    },
    "docs/v0/code_architecture/06_theory_gap_closure_register.md": {
        "role": "theory_gap_closure_register",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md",
            "docs/v0/mapping/0_to_257_engineering_utilization_map.md",
        ],
    },
    "docs/v0/implementation_architecture/README.md": {
        "role": "implementation_architecture_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/README.md",
            "docs/v0/code_framework/README.md",
        ],
    },
    "docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md": {
        "role": "runtime_organ_interface_blueprint",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md",
            "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
        ],
    },
    "docs/v0/implementation_architecture/02_turn_and_cycle_lifecycle_contract.md": {
        "role": "turn_cycle_lifecycle_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/process_contracts/terminal_life_loop_engineering_contract.md",
            "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md",
        ],
    },
    "docs/v0/implementation_architecture/03_module_authoring_traceability_protocol.md": {
        "role": "module_authoring_traceability_protocol",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md",
            "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
        ],
    },
    "docs/v0/implementation_architecture/code_organs/README.md": {
        "role": "code_organs_cabinet_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/implementation_architecture/README.md",
            "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
        ],
    },
    "docs/v0/implementation_architecture/code_organs/01_life_v0_package_organ_split_map.md": {
        "role": "life_v0_package_organ_split_map",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
            "docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md",
        ],
    },
    "docs/v0/implementation_architecture/code_organs/02_heavy_init_refactor_wave_contract.md": {
        "role": "heavy_init_refactor_wave_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/implementation_architecture/code_organs/01_life_v0_package_organ_split_map.md",
            "docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md",
        ],
    },
    "docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md": {
        "role": "predictive_signal_memory_gate_integration_wave_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/implementation_architecture/code_organs/01_life_v0_package_organ_split_map.md",
            "docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md",
        ],
    },
    "docs/v0/shared_contracts/life_state_store_v0_schema.md": {
        "role": "life_state_schema",
        "slice": "S04_STATE_OBJECT_STORE",
        "status": "closed",
        "source_refs": [
            "docs/17_memory_trace_object_model.md",
            "docs/41_runtime_state_store_schema.md",
        ],
    },
    "docs/v0/shared_contracts/README.md": {
        "role": "shared_contracts_cabinet_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/README.md",
            "docs/v0/shared_contracts/life_state_store_v0_schema.md",
        ],
    },
    "docs/v0/shared_contracts/birth_readiness_v0_contract.md": {
        "role": "birth_readiness_contract",
        "slice": "S08_LIFE_TARGET_RUNTIMES",
        "status": "closed",
        "source_refs": [
            "docs/143_life_reality_birth_readiness_rollup_contract.md",
            "docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md",
        ],
    },
    "docs/v0/shared_contracts/runner_cli_report_contract.md": {
        "role": "runner_cli_report_contract",
        "slice": "S09_SCHEMA_RUNNER_CODE",
        "status": "closed",
        "source_refs": [
            "docs/118_life_reality_generation_runner_cli_contract.md",
            "docs/155_life_reality_runner_command_queue_for_cross_file_checkers.md",
            "docs/180_life_reality_first_runner_schema_file_archive_receipt_batch.md",
        ],
    },
    "docs/v0/shared_contracts/first_activation_protocol.md": {
        "role": "first_activation_protocol",
        "slice": "S10_RUNTIME_GROWTH_RECONSOLIDATION",
        "status": "closed",
        "source_refs": [
            "docs/191_life_reality_first_runner_schema_runtime_growth_post_activation_observation_loop.md",
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
        ],
    },
    "docs/v0/process_contracts/first_terminal_turn_engineering_contract.md": {
        "role": "first_terminal_turn_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/20_agent_runtime_bridge_contract.md",
            "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
            "docs/90_language_event_examples_and_timeline_bundle.md",
        ],
    },
    "docs/v0/process_contracts/terminal_life_loop_engineering_contract.md": {
        "role": "terminal_life_loop_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/20_agent_runtime_bridge_contract.md",
            "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
            "docs/90_language_event_examples_and_timeline_bundle.md",
            "docs/v0/process_contracts/first_terminal_turn_engineering_contract.md",
        ],
    },
    "docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md": {
        "role": "digital_life_shell_command_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/20_agent_runtime_bridge_contract.md",
            "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
            "docs/90_language_event_examples_and_timeline_bundle.md",
            "docs/v0/references/current_agent_shell_reference_2026.md",
            "docs/v0/process_contracts/first_terminal_turn_engineering_contract.md",
            "docs/v0/process_contracts/terminal_life_loop_engineering_contract.md",
        ],
    },
    "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md": {
        "role": "digital_life_process_supervisor_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/20_agent_runtime_bridge_contract.md",
            "docs/86_language_neuroscience_pragmatics_and_inner_speech.md",
            "docs/89_language_runtime_framework_bridge_and_life_shell_policy.md",
            "docs/90_language_event_examples_and_timeline_bundle.md",
            "docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md",
            "docs/v0/process_contracts/terminal_life_loop_engineering_contract.md",
        ],
    },
    "docs/v0/process_contracts/README.md": {
        "role": "process_contracts_cabinet_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/README.md",
            "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md",
        ],
    },
    "docs/v0/slice_contracts/doc_corpus_ingestor_v0_contract.md": {
        "role": "doc_ingestion_contract",
        "slice": "S00_DIRECTION_FOUNDATION",
        "status": "closed",
        "source_refs": [
            "docs/00_research_protocol.md",
            "docs/01_literature_matrix.md",
        ],
    },
    "docs/v0/slice_contracts/s00_direction_foundation_engineering_contract.md": {
        "role": "s00_contract",
        "slice": "S00_DIRECTION_FOUNDATION",
        "status": "closed",
        "source_refs": [
            "docs/构思.md",
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
        ],
    },
    "docs/v0/slice_contracts/s01_source_authority_engineering_contract.md": {
        "role": "s01_contract",
        "slice": "S01_SOURCE_AUTHORITY",
        "status": "closed",
        "source_refs": [
            "docs/00_research_protocol.md",
            "docs/01_literature_matrix.md",
        ],
    },
    "docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md": {
        "role": "s02_contract",
        "slice": "S02_NEURAL_LIFE_CORE",
        "status": "closed",
        "source_refs": [
            "docs/02_brain_region_and_network_atlas.md",
            "docs/13_agentic_human_research_synthesis.md",
        ],
    },
    "docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md": {
        "role": "s03_contract",
        "slice": "S03_DIRECTION_LIFE_MEMBRANE",
        "status": "closed",
        "source_refs": [
            "docs/91_life_reality_generation_boundary_principles.md",
            "docs/119_life_boundary_full_reality_alignment.md",
        ],
    },
    "docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md": {
        "role": "s04_contract",
        "slice": "S04_STATE_OBJECT_STORE",
        "status": "closed",
        "source_refs": [
            "docs/17_memory_trace_object_model.md",
            "docs/41_runtime_state_store_schema.md",
        ],
    },
    "docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md": {
        "role": "s05_contract",
        "slice": "S05_VALIDATION_MEMBRANE_OBSERVATION",
        "status": "closed",
        "source_refs": [
            "docs/29_memory_validator_rules.md",
            "docs/64_real_runtime_observation_ingestion_policy.md",
        ],
    },
    "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md": {
        "role": "s06_contract",
        "slice": "S06_LIFE_SUPPORT_DEVELOPMENT",
        "status": "closed",
        "source_refs": [
            "docs/37_life_support_layer_policy.md",
            "docs/92_self_growth_and_self_modification_life_chain.md",
        ],
    },
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md": {
        "role": "s07_contract",
        "slice": "S07_LANGUAGE_RELATIONSHIP",
        "status": "closed",
        "source_refs": [
            "docs/09_language_symbolic_top_layer.md",
            "docs/96_real_relationship_longitudinal_timeline.md",
        ],
    },
    "docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md": {
        "role": "s08_contract",
        "slice": "S08_LIFE_TARGET_RUNTIMES",
        "status": "closed",
        "source_refs": [
            "docs/91_life_reality_generation_boundary_principles.md",
            "docs/143_life_reality_birth_readiness_rollup_contract.md",
        ],
    },
    "docs/v0/slice_contracts/s09_schema_runner_code_engineering_contract.md": {
        "role": "s09_contract",
        "slice": "S09_SCHEMA_RUNNER_CODE",
        "status": "closed",
        "source_refs": [
            "docs/123_life_reality_runner_repository_layout_and_module_map.md",
            "docs/163_life_reality_first_runner_code_generation_batch.md",
            "docs/180_life_reality_first_runner_schema_file_archive_receipt_batch.md",
        ],
    },
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md": {
        "role": "s10_contract",
        "slice": "S10_RUNTIME_GROWTH_RECONSOLIDATION",
        "status": "closed",
        "source_refs": [
            "docs/181_life_reality_first_runner_schema_runtime_mount_plan.md",
            "docs/257_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_replay_shadow_seed_after_archive_validation_replay_shadow_patch_archive_validation_plan.md",
        ],
    },
    "docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md": {
        "role": "s11_contract",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
            "docs/v0/README.md",
        ],
    },
    "docs/v0/slice_contracts/README.md": {
        "role": "slice_contracts_cabinet_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/README.md",
            "docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md",
        ],
    },
    "docs/v0/references/current_agent_shell_reference_2026.md": {
        "role": "external_agent_reference",
        "slice": "S09_SCHEMA_RUNNER_CODE",
        "status": "closed",
        "source_refs": [
            "docs/15_current_agent_framework_survey.md",
            "docs/12_ai_and_cognitive_architecture_bridge.md",
        ],
    },
    "docs/v0/references/README.md": {
        "role": "references_cabinet_index",
        "slice": ACTIVE_SLICE,
        "status": "closed",
        "source_refs": [
            "docs/v0/README.md",
            "docs/v0/references/current_agent_shell_reference_2026.md",
        ],
    },
}

V0_DOC_FILE_RULES.update(
    {
        "docs/v0/code_framework/README.md": {
            "role": "code_framework_index",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/README.md",
                "docs/v0/entry/v0_module_execution_catalog.md",
            ],
        },
        "docs/v0/code_framework/foundation/README.md": {
            "role": "code_framework_foundation_index",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/README.md",
            ],
        },
        "docs/v0/code_framework/foundation/01_life_layer_implementation_blueprint.md": {
            "role": "life_layer_implementation_blueprint",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/13_agentic_human_research_synthesis.md",
                "docs/v0/architecture/digital_life_macro_architecture_v0.md",
            ],
        },
        "docs/v0/code_framework/foundation/02_brain_region_to_code_package_mapping.md": {
            "role": "brain_region_to_code_package_mapping",
            "slice": "S02_NEURAL_LIFE_CORE",
            "status": "closed",
            "source_refs": [
                "docs/02_brain_region_and_network_atlas.md",
                "docs/14_cross_module_digital_life_map.md",
            ],
        },
        "docs/v0/code_framework/foundation/03_code_package_state_test_gate_mapping.md": {
            "role": "code_package_state_test_gate_mapping",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/shared_contracts/life_state_store_v0_schema.md",
                "docs/v0/shared_contracts/runner_cli_report_contract.md",
            ],
        },
        "docs/v0/code_framework/playbooks/README.md": {
            "role": "code_framework_playbook_index",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/README.md",
            ],
        },
        "docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md": {
            "role": "language_dialogue_relationship_playbook",
            "slice": "S07_LANGUAGE_RELATIONSHIP",
            "status": "closed",
            "source_refs": [
                "docs/09_language_symbolic_top_layer.md",
                "docs/96_real_relationship_longitudinal_timeline.md",
            ],
        },
        "docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md": {
            "role": "memory_thought_consciousness_playbook",
            "slice": "S04_STATE_OBJECT_STORE",
            "status": "closed",
            "source_refs": [
                "docs/05_memory_systems_and_growth.md",
                "docs/10_consciousness_attention_workspace.md",
            ],
        },
        "docs/v0/code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md": {
            "role": "body_emotion_action_dream_growth_playbook",
            "slice": "S06_LIFE_SUPPORT_DEVELOPMENT",
            "status": "closed",
            "source_refs": [
                "docs/07_emotion_personality_self.md",
                "docs/08_sleep_dream_fatigue_states.md",
            ],
        },
        "docs/v0/code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md": {
            "role": "birth_terminal_process_playbook",
            "slice": "S10_RUNTIME_GROWTH_RECONSOLIDATION",
            "status": "closed",
            "source_refs": [
                "docs/20_agent_runtime_bridge_contract.md",
                "docs/v0/shared_contracts/first_activation_protocol.md",
            ],
        },
        "docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md": {
            "role": "cross_layer_orchestration_playbook",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md",
                "docs/v0/implementation_architecture/02_turn_and_cycle_lifecycle_contract.md",
            ],
        },
        "docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md": {
            "role": "perception_prediction_world_contact_playbook",
            "slice": "S03_DIRECTION_LIFE_MEMBRANE",
            "status": "closed",
            "source_refs": [
                "docs/04_sensory_thalamus_interoception.md",
                "docs/20_agent_runtime_bridge_contract.md",
            ],
        },
        "docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md": {
            "role": "self_identity_value_commitment_playbook",
            "slice": "S08_LIFE_TARGET_RUNTIMES",
            "status": "closed",
            "source_refs": [
                "docs/07_emotion_personality_self.md",
                "docs/143_life_reality_birth_readiness_rollup_contract.md",
            ],
        },
        "docs/v0/code_framework/delivery/README.md": {
            "role": "code_framework_delivery_index",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/README.md",
            ],
        },
        "docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md": {
            "role": "engineering_delivery_waves",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/entry/v0_delivery_status_board.md",
                "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
            ],
        },
        "docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md": {
            "role": "full_life_layer_delivery_matrix",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/foundation/01_life_layer_implementation_blueprint.md",
                "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
            ],
        },
        "docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md": {
            "role": "capability_to_code_realization_matrix",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md",
                "docs/v0/code_framework/foundation/03_code_package_state_test_gate_mapping.md",
            ],
        },
        "docs/v0/code_framework/queues/README.md": {
            "role": "code_framework_queue_index",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/README.md",
            ],
        },
        "docs/v0/code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md": {
            "role": "queue_a_language_percept_semantic_map_contract",
            "slice": "S07_LANGUAGE_RELATIONSHIP",
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md",
                "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
            ],
        },
        "docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md": {
            "role": "queue_b_process_supervisor_contract",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md",
                "docs/v0/code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md",
            ],
        },
        "docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md": {
            "role": "queue_c_memory_neural_core_contract",
            "slice": "S02_NEURAL_LIFE_CORE",
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md",
                "docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md",
            ],
        },
        "docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md": {
            "role": "queue_d_body_dream_growth_contract",
            "slice": "S06_LIFE_SUPPORT_DEVELOPMENT",
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md",
                "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
            ],
        },
        "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md": {
            "role": "queue_e_membrane_validator_logic_contract",
            "slice": "S05_VALIDATION_MEMBRANE_OBSERVATION",
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md",
                "docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md",
            ],
        },
        "docs/v0/code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md": {
            "role": "queue_f_identity_consciousness_birth_readiness_contract",
            "slice": "S08_LIFE_TARGET_RUNTIMES",
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md",
                "docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md",
            ],
        },
        "docs/v0/code_framework/assembly/README.md": {
            "role": "code_framework_assembly_index",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/README.md",
            ],
        },
        "docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md": {
            "role": "cross_layer_shared_object_contract",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/foundation/03_code_package_state_test_gate_mapping.md",
                "docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md",
            ],
        },
        "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md": {
            "role": "code_tree_package_brain_contract",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/foundation/02_brain_region_to_code_package_mapping.md",
                "docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md",
            ],
        },
        "docs/v0/engineering_depth/README.md": {
            "role": "engineering_depth_index",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/README.md",
                "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
            ],
        },
        "docs/v0/engineering_depth/01_full_life_layer_implementation_deep_spec.md": {
            "role": "full_life_layer_implementation_deep_spec",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/foundation/01_life_layer_implementation_blueprint.md",
                "docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md",
            ],
        },
        "docs/v0/engineering_depth/02_state_object_runtime_evidence_map.md": {
            "role": "state_object_runtime_evidence_map",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md",
                "docs/v0/shared_contracts/life_state_store_v0_schema.md",
            ],
        },
        "docs/v0/engineering_depth/03_language_relationship_longitudinal_engineering.md": {
            "role": "language_relationship_longitudinal_engineering",
            "slice": "S07_LANGUAGE_RELATIONSHIP",
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md",
                "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
            ],
        },
        "docs/v0/engineering_depth/04_body_affect_dream_growth_engineering.md": {
            "role": "body_affect_dream_growth_engineering",
            "slice": "S06_LIFE_SUPPORT_DEVELOPMENT",
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md",
                "docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md",
            ],
        },
        "docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md": {
            "role": "prediction_membrane_action_engineering",
            "slice": "S05_VALIDATION_MEMBRANE_OBSERVATION",
            "status": "closed",
            "source_refs": [
                "docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md",
                "docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md",
            ],
        },
        "docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md": {
            "role": "resident_process_terminal_birth_engineering",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md",
                "docs/v0/process_contracts/terminal_life_loop_engineering_contract.md",
            ],
        },
        "docs/v0/engineering_depth/07_theory_to_code_trace_matrix.md": {
            "role": "theory_to_code_trace_matrix",
            "slice": ACTIVE_SLICE,
            "status": "closed",
            "source_refs": [
                "docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md",
                "docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md",
            ],
        },
    }
)

SLICE_STATUS_RULES: dict[str, dict[str, Any]] = {
    "P0_DOC_CORPUS_INGESTION": {
        "report": "doc_ingestion_report.json",
        "receipt_prefix": "doc_ingestion_",
        "status": "closed",
    },
    "S00_DIRECTION_FOUNDATION": {
        "report": "direction_lock_report.json",
        "receipt_prefix": "direction_lock_",
        "status": "closed",
    },
    "S01_SOURCE_AUTHORITY": {
        "report": "source_authority_report.json",
        "receipt_prefix": "source_authority_",
        "status": "closed",
    },
    "S02_NEURAL_LIFE_CORE": {
        "report": "neural_life_core_report.json",
        "receipt_prefix": "neural_life_core_",
        "status": "closed",
    },
    "S03_DIRECTION_LIFE_MEMBRANE": {
        "report": "life_membrane_report.json",
        "receipt_prefix": "life_membrane_",
        "status": "closed",
    },
    "S04_STATE_OBJECT_STORE": {
        "report": "state_store_report.json",
        "receipt_prefix": "state_store_",
        "status": "closed",
    },
    "S05_VALIDATION_MEMBRANE_OBSERVATION": {
        "report": "validation_membrane_report.json",
        "receipt_prefix": "validation_membrane_",
        "status": "closed",
    },
    "S06_LIFE_SUPPORT_DEVELOPMENT": {
        "report": "life_support_development_report.json",
        "receipt_prefix": "life_support_development_",
        "status": "closed",
    },
    "S07_LANGUAGE_RELATIONSHIP": {
        "report": "language_relationship_report.json",
        "receipt_prefix": "language_relationship_",
        "status": "closed",
    },
    "S08_LIFE_TARGET_RUNTIMES": {
        "report": "birth_readiness_report.json",
        "receipt_prefix": "birth_readiness_",
        "status": "closed",
    },
    "S09_SCHEMA_RUNNER_CODE": {
        "report": "schema_runner_report.json",
        "receipt_prefix": "schema_runner_",
        "status": "closed",
    },
    "S10_RUNTIME_GROWTH_RECONSOLIDATION": {
        "report": "growth_reconsolidation_report.json",
        "receipt_prefix": "run_cycle_",
        "status": "closed",
    },
}

RUNTIME_CARRIER_RULES: dict[str, dict[str, Any]] = {
    "DirectionLockKernel": {
        "state_refs": ["runtime/state/direction/direction_lock.json"],
        "report_refs": ["runtime/reports/latest/direction_lock_report.json"],
        "status": "closed",
    },
    "LifeStateStore": {
        "state_refs": ["runtime/state/life_state.json"],
        "report_refs": ["runtime/reports/latest/state_store_report.json"],
        "status": "closed",
    },
    "LifeMembraneStageGate": {
        "state_refs": ["runtime/state/membrane/dream_fact_boundary.json"],
        "report_refs": ["runtime/reports/latest/life_membrane_report.json"],
        "status": "closed",
    },
    "LifeTargetBundleRuntime": {
        "state_refs": ["runtime/state/life_targets/birth_readiness_stage_gate.json"],
        "report_refs": ["runtime/reports/latest/birth_readiness_report.json"],
        "status": "closed",
    },
    "SchemaBundleCompiler": {
        "state_refs": ["runtime/state/schema_runner/schema_runner_stage_gate.json"],
        "report_refs": ["runtime/reports/latest/schema_runner_report.json"],
        "status": "closed",
    },
    "ActivationGrowthRuntime": {
        "state_refs": ["runtime/state/growth/runtime_mount_state.json"],
        "report_refs": ["runtime/reports/latest/growth_reconsolidation_report.json"],
        "status": "closed",
    },
    "ReconsolidationReplayRuntime": {
        "state_refs": ["runtime/state/replay/shadow_cycle_trace.json"],
        "report_refs": ["runtime/reports/latest/run_report.json"],
        "status": "closed",
    },
    "V0ContractCoverageRuntime": {
        "state_refs": ["runtime/state/contracts/v0_contract_file_index.json"],
        "report_refs": ["runtime/reports/latest/v0_contract_coverage_report.json"],
        "status": "closed",
    },
}


@dataclass(frozen=True)
class V0ContractCoverageResult:
    exit_code: int
    report: dict[str, Any]


def run_check_v0_contracts(
    *,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str | None = None,
    strict: bool = False,
) -> V0ContractCoverageResult:
    run_id = run_id or _default_run_id("check-v0-contracts-")
    generated_at = _now_iso()
    docs_dir = docs_dir.resolve()
    doc_index_path = doc_index_path.resolve()
    state_dir = state_dir.resolve()
    reports_dir = reports_dir.resolve()
    receipts_dir = receipts_dir.resolve()
    contracts_dir = state_dir / "contracts"

    blocked_reasons: list[str] = []
    if not docs_dir.exists() or not docs_dir.is_dir():
        blocked_reasons.append(f"docs_root_gate failed: {docs_dir}")
    if not doc_index_path.exists():
        blocked_reasons.append(f"doc_index_gate failed: {doc_index_path}")

    doc_index = _load_json(doc_index_path, blocked_reasons, "doc_index_read_gate") if doc_index_path.exists() else {}
    indexed_documents = {
        document.get("path"): document
        for document in doc_index.get("documents", [])
        if isinstance(document, dict) and document.get("path")
    }

    contract_index = _build_contract_file_index(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        indexed_documents=indexed_documents,
        blocked_reasons=blocked_reasons,
    )
    doc_to_code = _build_doc_to_code_coverage_matrix(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        indexed_documents=indexed_documents,
        blocked_reasons=blocked_reasons,
    )
    slice_matrix = _build_slice_report_receipt_matrix(
        run_id=run_id,
        generated_at=generated_at,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        blocked_reasons=blocked_reasons,
    )
    carrier_matrix = _build_runtime_carrier_coverage_matrix(
        run_id=run_id,
        generated_at=generated_at,
        state_dir=state_dir,
        reports_dir=reports_dir,
        blocked_reasons=blocked_reasons,
    )
    preflight = _build_first_activation_preflight_contract_check(
        run_id=run_id,
        generated_at=generated_at,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        slice_matrix=slice_matrix,
        blocked_reasons=blocked_reasons,
    )

    status = "closed" if not blocked_reasons else "blocked"
    activation_preflight_allowed = bool(preflight.get("activation_preflight_allowed")) and status == "closed"
    if not activation_preflight_allowed and status == "closed":
        status = "blocked"

    stage_effect = "allow_activation_preflight" if status == "closed" else "block_activation"
    next_allowed_slices = [] if status == "closed" else ["S10_RUNTIME_GROWTH_RECONSOLIDATION"]

    report = _build_report(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        slice_matrix=slice_matrix,
        doc_to_code=doc_to_code,
        activation_preflight_allowed=activation_preflight_allowed,
        next_allowed_slices=next_allowed_slices,
    )
    digest = _build_digest(
        run_id=run_id,
        generated_at=generated_at,
        status=status,
        stage_effect=stage_effect,
        blocked_reasons=blocked_reasons,
        activation_preflight_allowed=activation_preflight_allowed,
        next_allowed_slices=next_allowed_slices,
    )
    receipt = _build_receipt(
        run_id=run_id,
        generated_at=generated_at,
        docs_dir=docs_dir,
        doc_index_path=doc_index_path,
        state_dir=state_dir,
        reports_dir=reports_dir,
        receipts_dir=receipts_dir,
        stage_effect=stage_effect,
    )

    try:
        contracts_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        _write_json(contracts_dir / "v0_contract_file_index.json", contract_index)
        _write_json(contracts_dir / "doc_to_code_coverage_matrix.json", doc_to_code)
        _write_json(contracts_dir / "slice_report_receipt_matrix.json", slice_matrix)
        _write_json(contracts_dir / "runtime_carrier_coverage_matrix.json", carrier_matrix)
        _write_json(contracts_dir / "first_activation_preflight_contract_check.json", preflight)
        _write_json(reports_dir / "v0_contract_coverage_report.json", report)
        _write_json(reports_dir / "v0_contract_coverage_digest.json", digest)
        _write_json(receipts_dir / f"v0_contract_coverage_{run_id}.json", receipt)
    except OSError as exc:
        report["status"] = "blocked"
        report["stage_effect"] = "block_activation"
        report["blocked_reasons"].append(f"output_write_gate failed: {exc}")
        return V0ContractCoverageResult(exit_code=4, report=report)

    if status == "closed":
        return V0ContractCoverageResult(exit_code=0, report=report)
    return V0ContractCoverageResult(exit_code=1 if strict else 0, report=report)


def _build_contract_file_index(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    indexed_documents: dict[str, dict[str, Any]],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    files: dict[str, Any] = {}
    missing_files: list[str] = []
    for rel_path, rule in V0_DOC_FILE_RULES.items():
        file_path = docs_dir.parent / rel_path
        exists = file_path.exists()
        if not exists:
            missing_files.append(rel_path)
        files[rel_path] = {
            "role": rule["role"],
            "slice": rule["slice"],
            "status": rule["status"] if exists else "missing",
            "exists": exists,
            "source_refs": rule["source_refs"],
            "readme_block_ref": READ_ME_BLOCK_REFS[0] if rel_path.startswith("docs/v0/") else None,
            "doc_index_present": rel_path in indexed_documents,
        }
    if missing_files:
        blocked_reasons.append("v0_contract_presence_gate missing: " + ", ".join(missing_files))
    return {
        "schema_version": "v0_contract_file_index_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "files": files,
        "missing_files": missing_files,
    }


def _build_doc_to_code_coverage_matrix(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    indexed_documents: dict[str, dict[str, Any]],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    documents: dict[str, Any] = {}
    missing_documents: list[str] = []
    uncovered_docs: list[str] = []

    for rel_path, document in indexed_documents.items():
        carrier_refs = list(document.get("runtime_carriers", []))
        engineering_slice = document.get("engineering_slice")
        readme_block_ref = document.get("readme_block")
        if not engineering_slice or not readme_block_ref or not carrier_refs:
            uncovered_docs.append(rel_path)
        documents[rel_path] = {
            "doc_id": document.get("doc_id"),
            "engineering_slice": engineering_slice,
            "readme_block_ref": readme_block_ref,
            "runtime_carrier_refs": carrier_refs,
            "code_package_refs": _carrier_to_code_packages(carrier_refs),
            "state_namespace_refs": _carrier_to_state_namespaces(carrier_refs),
            "report_refs": _carrier_to_reports(carrier_refs),
            "receipt_family_refs": _carrier_to_receipts(carrier_refs),
        }

    for rel_path in [
        "docs/258_linear_chain_closure_and_v0_contract_transition.md",
        "docs/README.md",
        "docs/13_agentic_human_research_synthesis.md",
    ]:
        if rel_path not in documents:
            missing_documents.append(rel_path)
    if missing_documents:
        blocked_reasons.append("doc_to_slice_gate missing indexed docs: " + ", ".join(missing_documents))
    if uncovered_docs:
        blocked_reasons.append("doc_to_slice_gate uncovered docs: " + ", ".join(uncovered_docs))

    return {
        "schema_version": "doc_to_code_coverage_matrix_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "documents": documents,
        "coverage_summary": {
            "total_documents": len(documents),
            "uncovered_docs": uncovered_docs,
            "missing_documents": missing_documents,
        },
    }


def _build_slice_report_receipt_matrix(
    *,
    run_id: str,
    generated_at: str,
    reports_dir: Path,
    receipts_dir: Path,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    slices: dict[str, Any] = {}
    missing_runtime_closure: list[str] = []

    for slice_name, rule in SLICE_STATUS_RULES.items():
        report_ref = rule["report"]
        receipt_prefix = rule["receipt_prefix"]
        status = rule["status"]
        report_exists = True
        receipt_matches: list[str] = []
        if report_ref is not None:
            report_exists = (reports_dir / report_ref).exists()
        if receipt_prefix is not None:
            receipt_matches = sorted(path.name for path in receipts_dir.glob(f"{receipt_prefix}*.json"))
        if status == "closed" and (not report_exists or not receipt_matches):
            missing_runtime_closure.append(slice_name)
        slices[slice_name] = {
            "status": status if status != "closed" or (report_exists and receipt_matches) else "blocked",
            "report_ref": None if report_ref is None else f"runtime/reports/latest/{report_ref}",
            "report_exists": report_exists,
            "receipt_refs": [f"runtime/receipts/{name}" for name in receipt_matches],
        }
    if missing_runtime_closure:
        blocked_reasons.append("slice_report_gate missing closure: " + ", ".join(missing_runtime_closure))
    return {
        "schema_version": "slice_report_receipt_matrix_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "slices": slices,
    }


def _build_runtime_carrier_coverage_matrix(
    *,
    run_id: str,
    generated_at: str,
    state_dir: Path,
    reports_dir: Path,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    runtime_carriers: dict[str, Any] = {}
    missing_carriers: list[str] = []
    for carrier, rule in RUNTIME_CARRIER_RULES.items():
        if carrier == "V0ContractCoverageRuntime":
            missing_state_refs = []
            missing_report_refs = []
        else:
            missing_state_refs = [
                ref for ref in rule["state_refs"]
                if not _resolve_runtime_ref(
                    state_dir=state_dir,
                    reports_dir=reports_dir,
                    ref=ref,
                ).exists()
            ]
            missing_report_refs = [
                ref for ref in rule["report_refs"]
                if not _resolve_runtime_ref(
                    state_dir=state_dir,
                    reports_dir=reports_dir,
                    ref=ref,
                ).exists()
            ]
        if missing_state_refs or missing_report_refs:
            missing_carriers.append(carrier)
        runtime_carriers[carrier] = {
            "status": "closed" if not (missing_state_refs or missing_report_refs) else "blocked",
            "state_refs": rule["state_refs"],
            "report_refs": rule["report_refs"],
            "missing_state_refs": missing_state_refs,
            "missing_report_refs": missing_report_refs,
        }
    if missing_carriers:
        blocked_reasons.append("runtime_carrier_gate missing closure: " + ", ".join(missing_carriers))
    return {
        "schema_version": "runtime_carrier_coverage_matrix_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "runtime_carriers": runtime_carriers,
    }


def _build_first_activation_preflight_contract_check(
    *,
    run_id: str,
    generated_at: str,
    reports_dir: Path,
    receipts_dir: Path,
    slice_matrix: dict[str, Any],
    blocked_reasons: list[str],
) -> dict[str, Any]:
    required_reports = {
        "run_report": "run_report.json",
        "growth_reconsolidation_report": "growth_reconsolidation_report.json",
        "digest": "digest.json",
        "stage_gate": "stage_gate.json",
    }
    report_status: dict[str, Any] = {}
    missing_reports: list[str] = []
    for key, filename in required_reports.items():
        exists = (reports_dir / filename).exists()
        if not exists:
            missing_reports.append(filename)
        report_status[key] = {
            "status": "closed" if exists else "missing",
            "ref": f"runtime/reports/latest/{filename}",
        }

    required_receipts = {
        "run_cycle_receipt": sorted(path.name for path in receipts_dir.glob("run_cycle_*.json")),
        "life_support_receipt": sorted(path.name for path in receipts_dir.glob("life_support_development_*.json")),
        "schema_runner_receipt": sorted(path.name for path in receipts_dir.glob("schema_runner_*.json")),
    }
    missing_receipt_families = [key for key, matches in required_receipts.items() if not matches]
    if missing_reports:
        blocked_reasons.append("activation_preflight_gate missing reports: " + ", ".join(missing_reports))
    if missing_receipt_families:
        blocked_reasons.append("activation_preflight_gate missing receipts: " + ", ".join(missing_receipt_families))

    activation_preflight_allowed = not missing_reports and not missing_receipt_families
    return {
        "schema_version": "first_activation_preflight_contract_check_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "activation_preflight_allowed": activation_preflight_allowed,
        "required_reports": report_status,
        "required_receipts": {
            key: {
                "status": "closed" if matches else "missing",
                "refs": [f"runtime/receipts/{name}" for name in matches],
            }
            for key, matches in required_receipts.items()
        },
        "slice_status_refs": {
            key: value["status"]
            for key, value in slice_matrix.get("slices", {}).items()
        },
    }


def _build_report(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    slice_matrix: dict[str, Any],
    doc_to_code: dict[str, Any],
    activation_preflight_allowed: bool,
    next_allowed_slices: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "s11_v0_contract_coverage_report_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "engineering_slice_ref": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "source_doc_refs": [
            "docs/258_linear_chain_closure_and_v0_contract_transition.md",
            "docs/v0/README.md",
            "docs/v0/entry/v0_implementation_index.md",
            "docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md",
        ],
        "readme_block_refs": READ_ME_BLOCK_REFS,
        "runtime_carrier_refs": RUNTIME_CARRIER_REFS,
        "slice_status": {
            key: value["status"]
            for key, value in slice_matrix.get("slices", {}).items()
        },
        "doc_to_code_coverage": doc_to_code.get("coverage_summary", {}),
        "blocked_reasons": blocked_reasons,
        "quarantine_refs": [],
        "activation_preflight_allowed": activation_preflight_allowed,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": NEXT_REQUIRED_COMMAND if status == "closed" else "life-v0 run-cycle --shadow-only --strict",
    }


def _build_digest(
    *,
    run_id: str,
    generated_at: str,
    status: str,
    stage_effect: str,
    blocked_reasons: list[str],
    activation_preflight_allowed: bool,
    next_allowed_slices: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "v0_contract_coverage_digest_v0",
        "run_id": run_id,
        "generated_at": generated_at,
        "current_slice": ACTIVE_SLICE,
        "status": status,
        "stage_effect": stage_effect,
        "blocked_reasons": blocked_reasons,
        "activation_preflight_allowed": activation_preflight_allowed,
        "next_allowed_slices": next_allowed_slices,
        "next_required_command": NEXT_REQUIRED_COMMAND if status == "closed" else "life-v0 run-cycle --shadow-only --strict",
    }


def _build_receipt(
    *,
    run_id: str,
    generated_at: str,
    docs_dir: Path,
    doc_index_path: Path,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    stage_effect: str,
) -> dict[str, Any]:
    input_hashes: dict[str, str] = {}
    if doc_index_path.exists():
        input_hashes["runtime/docs/doc_carrier_index.json"] = _sha256(doc_index_path)
    for rel_path in V0_DOC_FILE_RULES:
        doc_path = docs_dir.parent / rel_path
        if doc_path.exists():
            input_hashes[rel_path] = _sha256(doc_path)

    output_paths = [
        state_dir / "contracts" / "v0_contract_file_index.json",
        state_dir / "contracts" / "doc_to_code_coverage_matrix.json",
        state_dir / "contracts" / "slice_report_receipt_matrix.json",
        state_dir / "contracts" / "runtime_carrier_coverage_matrix.json",
        state_dir / "contracts" / "first_activation_preflight_contract_check.json",
        reports_dir / "v0_contract_coverage_report.json",
        reports_dir / "v0_contract_coverage_digest.json",
        receipts_dir / f"v0_contract_coverage_{run_id}.json",
    ]
    return {
        "schema_version": "v0_contract_coverage_receipt_v0",
        "receipt_id": f"v0_contract_coverage_{run_id}",
        "run_id": run_id,
        "command": "check-v0-contracts",
        "docs_ref": str(docs_dir),
        "doc_index_ref": str(doc_index_path),
        "state_ref": str(state_dir),
        "stage_effect": stage_effect,
        "created_at": generated_at,
        "input_hashes": input_hashes,
        "output_hashes": {str(path): _sha256_if_exists(path) for path in output_paths},
    }


def _carrier_to_code_packages(carriers: list[str]) -> list[str]:
    mapping = {
        "DocCorpusIngestor": "life_v0/doc_index.py",
        "DirectionLockKernel": "life_v0/direction/",
        "SourceAuthorityRegistry": "life_v0/authority/",
        "LifeStateStore": "life_v0/state_store/",
        "LifeMembraneStageGate": "life_v0/membrane/",
        "LifeTargetBundleRuntime": "life_v0/life_targets/",
        "SchemaBundleCompiler": "life_v0/schema_runner/",
        "ActivationGrowthRuntime": "life_v0/growth/",
        "ReconsolidationReplayRuntime": "life_v0/replay/",
        "V0ContractCoverageRuntime": "life_v0/contracts/",
        "LanguageRelationshipRuntime": "life_v0/language/",
    }
    return [mapping[carrier] for carrier in carriers if carrier in mapping]


def _carrier_to_state_namespaces(carriers: list[str]) -> list[str]:
    mapping = {
        "DocCorpusIngestor": "runtime/docs/",
        "DirectionLockKernel": "runtime/state/direction/",
        "SourceAuthorityRegistry": "runtime/state/authority/",
        "LifeStateStore": "runtime/state/",
        "LifeMembraneStageGate": "runtime/state/membrane/",
        "LifeTargetBundleRuntime": "runtime/state/life_targets/",
        "SchemaBundleCompiler": "runtime/state/schema_runner/",
        "ActivationGrowthRuntime": "runtime/state/growth/",
        "ReconsolidationReplayRuntime": "runtime/state/replay/",
        "V0ContractCoverageRuntime": "runtime/state/contracts/",
        "LanguageRelationshipRuntime": "runtime/state/language/",
    }
    return [mapping[carrier] for carrier in carriers if carrier in mapping]


def _carrier_to_reports(carriers: list[str]) -> list[str]:
    mapping = {
        "DocCorpusIngestor": "runtime/reports/latest/doc_ingestion_report.json",
        "DirectionLockKernel": "runtime/reports/latest/direction_lock_report.json",
        "SourceAuthorityRegistry": "runtime/reports/latest/source_authority_report.json",
        "LifeStateStore": "runtime/reports/latest/state_store_report.json",
        "LifeMembraneStageGate": "runtime/reports/latest/life_membrane_report.json",
        "LifeTargetBundleRuntime": "runtime/reports/latest/birth_readiness_report.json",
        "SchemaBundleCompiler": "runtime/reports/latest/schema_runner_report.json",
        "ActivationGrowthRuntime": "runtime/reports/latest/growth_reconsolidation_report.json",
        "ReconsolidationReplayRuntime": "runtime/reports/latest/run_report.json",
        "V0ContractCoverageRuntime": "runtime/reports/latest/v0_contract_coverage_report.json",
        "LanguageRelationshipRuntime": "runtime/reports/latest/language_relationship_report.json",
    }
    return [mapping[carrier] for carrier in carriers if carrier in mapping]


def _carrier_to_receipts(carriers: list[str]) -> list[str]:
    mapping = {
        "DocCorpusIngestor": "runtime/receipts/doc_ingestion_*.json",
        "DirectionLockKernel": "runtime/receipts/direction_lock_*.json",
        "SourceAuthorityRegistry": "runtime/receipts/source_authority_*.json",
        "LifeStateStore": "runtime/receipts/state_store_*.json",
        "LifeMembraneStageGate": "runtime/receipts/life_membrane_*.json",
        "LifeTargetBundleRuntime": "runtime/receipts/birth_readiness_*.json",
        "SchemaBundleCompiler": "runtime/receipts/schema_runner_*.json",
        "ActivationGrowthRuntime": "runtime/receipts/run_cycle_*.json",
        "ReconsolidationReplayRuntime": "runtime/receipts/run_cycle_*.json",
        "V0ContractCoverageRuntime": "runtime/receipts/v0_contract_coverage_*.json",
        "LanguageRelationshipRuntime": "runtime/receipts/language_relationship_*.json",
    }
    return [mapping[carrier] for carrier in carriers if carrier in mapping]


def _load_json(path: Path, blocked_reasons: list[str], gate: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blocked_reasons.append(f"{gate} failed: {exc}")
        return {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_if_exists(path: Path) -> str | None:
    if path.exists():
        return _sha256(path)
    return None


def _resolve_runtime_ref(*, state_dir: Path, reports_dir: Path, ref: str) -> Path:
    runtime_root = state_dir.parent
    if ref.startswith("runtime/reports/latest/"):
        return reports_dir / ref.replace("runtime/reports/latest/", "", 1)
    if ref.startswith("runtime/state/"):
        return runtime_root / ref.replace("runtime/", "", 1)
    if ref.startswith("runtime/docs/"):
        return runtime_root / ref.replace("runtime/", "", 1)
    if ref.startswith("runtime/receipts/"):
        return runtime_root / ref.replace("runtime/", "", 1)
    return runtime_root / ref.replace("runtime/", "", 1)


def _default_run_id(prefix: str) -> str:
    return prefix + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
