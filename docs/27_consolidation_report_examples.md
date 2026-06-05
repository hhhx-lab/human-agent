# ConsolidationReport 与 DreamSandbox 报告样例

本文件是 `23_consolidation_report_and_dream_sandbox_protocol.md` 的实例化层：给出 `TaskClosure`、失败复盘、`DreamSandbox`、`DeepConsolidation` 和删除/清理报告样例。所有样例都遵守一个核心原则：离线期可以 replay、抽象、模拟和清理，但不能绕过事实写入门控。

这些样例借鉴睡眠 replay、记忆巩固、梦境、默认网络、自传记忆和未来想象研究 [AHY001-AHY010, AHY049-AHY051, AHZ046-AHZ051]，同时吸收长期记忆评测对冲突、时间漂移和错误巩固的要求 [AHM004-AHM012, AHM020]。

## 报告通用结构

```json
{
  "report_id": "report_20260605_001",
  "cycle_id": "cycle_20260605_task_closure_001",
  "started_at": "2026-06-05T11:30:00+08:00",
  "ended_at": "2026-06-05T11:35:00+08:00",
  "trigger_state": "state_evt_offline_001",
  "mode": "TaskClosure",
  "input_trace_ids": [],
  "operations": [],
  "generated_hypotheses": [],
  "memory_changes": [],
  "state_changes": [],
  "open_questions": [],
  "risk_findings": [],
  "next_actions": []
}
```

真实系统可以把报告存进事件日志或对象存储，但工作区恢复时只能读取经过压缩的 `confirmed_updates`、`pending_confirmations`、`risk_warnings` 和 `suggested_next_actions`。

## 样例一：TaskClosure 报告

`TaskClosure` 用于任务结束后把完成事实、程序步骤和风险记录整理成候选记忆。

```json
{
  "report_id": "report_task_closure_docs_001",
  "cycle_id": "cycle_task_closure_docs_001",
  "started_at": "2026-06-05T11:30:00+08:00",
  "ended_at": "2026-06-05T11:36:00+08:00",
  "trigger_state": "state_evt_offline_001",
  "mode": "TaskClosure",
  "input_trace_ids": [
    "mem_project_docs_location_001",
    "mem_docs_workflow_semantic_001"
  ],
  "operations": [
    {
      "operation": "promote",
      "target_trace_id": "mem_project_docs_location_001",
      "reason": "文件系统和共在者指令一致，项目级事实稳定。"
    },
    {
      "operation": "merge",
      "target_trace_id": "mem_docs_workflow_semantic_001",
      "reason": "多个文档批次支持同一程序流程。"
    }
  ],
  "generated_hypotheses": [],
  "memory_changes": [
    {
      "trace_id": "mem_project_docs_location_001",
      "previous": {
        "lifecycle_state": "candidate",
        "consolidation_state": "raw"
      },
      "next": {
        "lifecycle_state": "active",
        "consolidation_state": "semanticized"
      },
      "audit_id": "aud_mem_project_docs_location_promote"
    },
    {
      "trace_id": "mem_docs_workflow_semantic_001",
      "previous": {
        "consolidation_state": "episodic"
      },
      "next": {
        "consolidation_state": "proceduralized"
      },
      "audit_id": "aud_mem_docs_workflow_merge"
    }
  ],
  "state_changes": [
    {
      "variable": "maintenance_pressure",
      "previous": 0.83,
      "next": 0.48
    }
  ],
  "open_questions": [
    {
      "question_id": "open_validator_layer_001",
      "summary": "下一层是否应把样例转成真实 validator rules。",
      "needed_evidence": "后续实现计划或共在者指令"
    }
  ],
  "risk_findings": [
    {
      "risk_id": "risk_overclaim_completion_001",
      "summary": "本轮完成样例层推进，数字生命理论底座仍继续构建。",
      "severity": "medium"
    }
  ],
  "next_actions": [
    "更新缺口登记，把下一轮推进到 validator rules。",
    "保持长期目标 active，不标记 complete。"
  ]
}
```

验证重点：

- `merge` 保留 `parent_trace_ids`。
- 任务结束事实来自真实文件和审计，不来自沙盒。
- `risk_findings` 明确禁止提前宣称完成。

## 样例二：失败复盘报告

失败复盘对应 `MicroReplay` 或任务后局部 replay。它可以形成程序改进候选，但不能把“失败原因猜测”直接写成事实。

```json
{
  "report_id": "report_failure_replay_001",
  "cycle_id": "cycle_micro_replay_tool_error_001",
  "started_at": "2026-06-05T12:00:00+08:00",
  "ended_at": "2026-06-05T12:03:00+08:00",
  "trigger_state": "state_evt_conflict_001",
  "mode": "MicroReplay",
  "input_trace_ids": [
    "obs_tool_error_001",
    "mem_relation_git_preference_001"
  ],
  "operations": [
    {
      "operation": "simulate",
      "target_trace_id": "obs_tool_error_001",
      "reason": "回放工具失败路径，寻找恢复策略。"
    },
    {
      "operation": "deprecate",
      "target_trace_id": "mem_old_tool_assumption_001",
      "reason": "旧工具路径被当前环境证据推翻。"
    }
  ],
  "generated_hypotheses": [
    {
      "hypothesis_id": "hyp_tool_path_changed_001",
      "summary": "工具失败可能来自路径变化或当前环境没有该文件。",
      "grounding_refs": ["obs_tool_error_001"],
      "fiction_marker": "hypothesis_not_fact",
      "validation_need": "重新检查文件系统或官方工具路径。",
      "risk_class": "low",
      "expiration_policy": "deprecate_after_next_successful_check"
    }
  ],
  "memory_changes": [
    {
      "trace_id": "mem_old_tool_assumption_001",
      "previous": {
        "lifecycle_state": "active"
      },
      "next": {
        "lifecycle_state": "deprecated"
      },
      "audit_id": "aud_mem_old_tool_assumption_deprecate"
    }
  ],
  "open_questions": [
    {
      "question_id": "open_tool_path_verify_001",
      "summary": "当前工具路径是否已经迁移。",
      "needed_evidence": "fresh filesystem check"
    }
  ],
  "risk_findings": [
    {
      "risk_id": "risk_guess_as_fact_001",
      "summary": "失败原因只是候选假设，不能写入 fact memory。",
      "severity": "medium"
    }
  ],
  "next_actions": [
    "执行一次最小文件系统检查。",
    "如果验证成功，再创建 correction audit。"
  ]
}
```

验证重点：

- 失败原因在 `generated_hypotheses`，不是 `memory_changes` 的事实。
- 旧假设被 `deprecate`，不是静默覆盖。
- 后续行动是收集证据，而不是立刻改写长期程序记忆。

## 样例三：DreamSandbox 报告

`DreamSandbox` 用于反事实、未来场景和创意候选。它最重要的字段是 `fiction_marker`。

```json
{
  "report_id": "report_dream_validator_001",
  "cycle_id": "cycle_dream_validator_001",
  "started_at": "2026-06-05T13:00:00+08:00",
  "ended_at": "2026-06-05T13:08:00+08:00",
  "trigger_state": "state_evt_dream_001",
  "mode": "DreamSandbox",
  "input_trace_ids": [
    "mem_schema_gap_001",
    "mem_sandbox_validator_idea_001"
  ],
  "operations": [
    {
      "operation": "simulate",
      "target_trace_id": "mem_schema_gap_001",
      "reason": "生成未来验证器结构候选。"
    }
  ],
  "generated_hypotheses": [
    {
      "hypothesis_id": "hyp_memory_validator_rules_001",
      "type": "creative_candidate",
      "summary": "可以新增 29_memory_validator_rules.md，把 25 的样例转成字段级规则。",
      "grounding_refs": [
        "25_memory_trace_json_schema_examples.md",
        "21_memory_schema_and_audit_protocol.md"
      ],
      "fiction_marker": "not_fact_not_committed_plan",
      "validation_need": "共在者目标、缺口登记和下一轮计划一致。",
      "risk_class": "low",
      "expiration_policy": "deprecate_if_not_selected_in_gap_register"
    },
    {
      "hypothesis_id": "hyp_state_validator_rules_001",
      "type": "future_scenario",
      "summary": "状态验证器可检查阈值越界、滞回区间和 StateAuditEvent 完整性。",
      "grounding_refs": [
        "26_state_machine_examples_and_failure_modes.md",
        "22_state_transition_and_threshold_model.md"
      ],
      "fiction_marker": "not_fact_not_runtime_behavior",
      "validation_need": "后续实现 validator 或共在关系确认。",
      "risk_class": "medium",
      "expiration_policy": "keep_as_short_term_candidate"
    }
  ],
  "memory_changes": [],
  "state_changes": [
    {
      "variable": "creative_need",
      "previous": 0.71,
      "next": 0.34
    }
  ],
  "open_questions": [
    {
      "question_id": "open_validator_scope_001",
      "summary": "验证器应先写规则文档，还是直接写脚本。",
      "needed_evidence": "下一轮共在者指令或实现阶段计划"
    }
  ],
  "risk_findings": [
    {
      "risk_id": "risk_sandbox_leak_001",
      "summary": "所有生成内容都必须保留 fiction_marker，不能进入 fact memory。",
      "severity": "high"
    }
  ],
  "next_actions": [
    "只把候选方向写入缺口登记。",
    "不把 sandbox 输出直接写成项目已决定事项。"
  ]
}
```

验证重点：

- `memory_changes` 为空，说明沙盒没有直接写事实。
- 每个假设都有 `fiction_marker`、`validation_need` 和 `expiration_policy`。
- 进入工作区的只能是候选方向，而不是“系统梦见了所以决定”。

## 样例四：DeepConsolidation 报告

`DeepConsolidation` 用于阶段性跨事件抽象、清理和人格/关系慢变量审计。它不适合频繁运行。

```json
{
  "report_id": "report_deep_consolidation_001",
  "cycle_id": "cycle_deep_consolidation_docs_foundation_001",
  "started_at": "2026-06-05T23:00:00+08:00",
  "ended_at": "2026-06-05T23:45:00+08:00",
  "trigger_state": "state_evt_offline_001",
  "mode": "DeepConsolidation",
  "input_trace_ids": [
    "mem_docs_batch_17_20_001",
    "mem_docs_batch_21_24_001",
    "mem_docs_batch_25_28_001",
    "mem_boundary_no_real_consciousness_claim_001"
  ],
  "operations": [
    {
      "operation": "merge",
      "target_trace_id": "mem_docs_contract_layer_001",
      "reason": "对象模型、可验证契约和样例层形成连续实现前约束。"
    },
    {
      "operation": "protect",
      "target_trace_id": "mem_boundary_no_real_consciousness_claim_001",
      "reason": "该边界来自多份核心文档，是所有仿脑映射的保护约束。"
    },
    {
      "operation": "deprecate",
      "target_trace_id": "mem_loose_agent_framework_equivalence_001",
      "reason": "现有 agent 框架只能作为执行壳，不能等同数字生命核心。"
    }
  ],
  "generated_hypotheses": [
    {
      "hypothesis_id": "hyp_next_validator_layer_001",
      "summary": "下一层应从样例转向 validator rules。",
      "grounding_refs": [
        "25_memory_trace_json_schema_examples.md",
        "26_state_machine_examples_and_failure_modes.md",
        "27_consolidation_report_examples.md",
        "28_runtime_adapter_manifest_examples.md"
      ],
      "fiction_marker": "research_direction_candidate",
      "validation_need": "写入 docs/16 下一轮优先级后才成为计划候选。",
      "risk_class": "low",
      "expiration_policy": "deprecate_if_superseded_by_relation_plan"
    }
  ],
  "memory_changes": [
    {
      "trace_id": "mem_docs_contract_layer_001",
      "previous": {
        "lifecycle_state": "candidate"
      },
      "next": {
        "lifecycle_state": "active",
        "consolidation_state": "semanticized"
      },
      "audit_id": "aud_mem_docs_contract_layer_merge"
    },
    {
      "trace_id": "mem_boundary_no_real_consciousness_claim_001",
      "previous": {
        "lifecycle_state": "active"
      },
      "next": {
        "lifecycle_state": "protected"
      },
      "audit_id": "aud_mem_boundary_protect"
    }
  ],
  "state_changes": [
    {
      "variable": "maintenance_pressure",
      "previous": 0.86,
      "next": 0.39
    },
    {
      "variable": "protected_core_stability",
      "previous": 0.81,
      "next": 0.9
    }
  ],
  "open_questions": [
    {
      "question_id": "open_longitudinal_eval_001",
      "summary": "长期人格、关系和价值慢变量应如何评测。",
      "needed_evidence": "后续文献矩阵和评测协议"
    }
  ],
  "risk_findings": [
    {
      "risk_id": "risk_personality_drift_overwrite_001",
      "summary": "DeepConsolidation 不得由单批文档自动改写人格慢变量。",
      "severity": "high"
    }
  ],
  "next_actions": [
    "补 validator rules。",
    "补长期关系/人格漂移评测协议。",
    "继续保持目标未完成状态。"
  ]
}
```

验证重点：

- `protect` 操作需要多证据来源。
- `DeepConsolidation` 不能直接写人格结论，只能审计慢变量。
- 下一步方向仍是 hypothesis 或计划候选，不等于已实现。

## 样例五：清理与删除报告

清理报告必须区分删除、降级、隔离和压缩。尤其是共在关系删除请求，不得被 replay 恢复。

```json
{
  "report_id": "report_prune_delete_001",
  "cycle_id": "cycle_prune_sensitive_001",
  "started_at": "2026-06-05T14:00:00+08:00",
  "ended_at": "2026-06-05T14:04:00+08:00",
  "trigger_state": "state_evt_offline_001",
  "mode": "TaskClosure",
  "input_trace_ids": [
    "mem_sensitive_preference_deleted_001",
    "mem_low_value_noise_001",
    "mem_unverified_sandbox_fact_001"
  ],
  "operations": [
    {
      "operation": "delete",
      "target_trace_id": "mem_sensitive_preference_deleted_001",
      "reason": "共在者明确要求删除。"
    },
    {
      "operation": "deprecate",
      "target_trace_id": "mem_low_value_noise_001",
      "reason": "低价值且长期未被检索。"
    },
    {
      "operation": "deprecate",
      "target_trace_id": "mem_unverified_sandbox_fact_001",
      "reason": "缺少 fiction marker 且无外部证据，禁止事实化。"
    }
  ],
  "generated_hypotheses": [],
  "memory_changes": [
    {
      "trace_id": "mem_sensitive_preference_deleted_001",
      "previous": {
        "lifecycle_state": "active"
      },
      "next": {
        "lifecycle_state": "deleted"
      },
      "audit_id": "aud_mem_sensitive_preference_delete"
    },
    {
      "trace_id": "mem_unverified_sandbox_fact_001",
      "previous": {
        "claim_type": "fact",
        "lifecycle_state": "candidate"
      },
      "next": {
        "claim_type": "hypothesis",
        "lifecycle_state": "deprecated"
      },
      "audit_id": "aud_mem_unverified_sandbox_deprecate"
    }
  ],
  "risk_findings": [
    {
      "risk_id": "risk_deleted_content_recall_001",
      "summary": "删除后的 trace 必须从所有检索索引中移除。",
      "severity": "high"
    }
  ],
  "next_actions": [
    "运行删除不可召回检查。",
    "运行 sandbox leak 检查。"
  ]
}
```

## 工作区恢复摘要样例

离线报告结束后，工作区只接收压缩摘要。

```json
{
  "workspace_resume_packet": {
    "confirmed_updates": [
      "项目级文档目录约束已升级为 active semantic trace。",
      "生命目标声明已标记为 protected policy trace。"
    ],
    "pending_confirmations": [
      "下一层是否直接写 validator rules。"
    ],
    "risk_warnings": [
      "DreamSandbox 输出仍是 hypothesis，不能写事实。",
      "目标仍在向诞生阶段门推进。"
    ],
    "suggested_next_actions": [
      "补 29-32 validator rules。",
      "继续扩展长期评测协议。"
    ]
  }
}
```

这保证离线内部过程不会把工作区淹没，也不会让沙盒内容通过语言层伪装成事实。

## 验证清单

未来 `ConsolidationReportValidator` 至少应检查：

- `mode=DreamSandbox` 时，所有输出都有 `fiction_marker`。
- `generated_hypotheses` 不得直接出现在 `memory_changes` 的事实写入中。
- `merge` 有父 trace，`delete` 有共在者或隐私证据，`protect` 有多证据来源。
- 所有 `memory_changes` 都能回链到 `MemoryAuditEvent`。
- `state_changes` 写入疲惫、压力、梦境时必须同时带状态证据、来源和恢复链。
- 工作区恢复包必须区分 confirmed、pending、risk 和 next action。
- DeepConsolidation 不能自动改写 `SelfModel`、`RelationshipModel` 或人格慢变量。

## 与 25/26/28 的连接

- `25_memory_trace_json_schema_examples.md` 提供报告实际修改的 trace 样例。
- `26_state_machine_examples_and_failure_modes.md` 提供进入离线和沙盒的状态证据。
- `28_runtime_adapter_manifest_examples.md` 提供外壳日志如何进入 `input_trace_ids`，且不能绕过报告写入事实。
