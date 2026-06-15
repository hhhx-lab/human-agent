# S10 Runtime Growth Reconsolidation Engineering Contract

生命目标声明：本文档把 `S10_RUNTIME_GROWTH_RECONSOLIDATION` 固定为第一版 runtime mount、观察反馈、梦境巩固、replay/shadow、再巩固、成长 patch、archive 和有限激活层的工程合同。它承接 `181-257`，把长链压成可执行生命循环。

## 模块定位

S10 是第一次有限激活前后的运行闭环。它不开放无限运行，不执行外部不可逆行动，不跳过出生准备度。它只在生命膜内执行 shadow-only cycle、写 report/digest/stage gate/archive receipt，并把观察、痛苦、后悔、梦境、语言关系、自我成长和防遗忘 replay 回写到下一轮准备。

## 必须读取

| 来源 | S10 吸收内容 |
|---|---|
| `181-185` | schema runtime mount、mount validation、runtime smoke、archive receipt |
| `186-204` | observation feedback、growth patch、shadow run、activation report、consolidation、replay/shadow |
| `205-219` | fourth cycle observation、patch、archive、replay/shadow、activation、validation |
| `220-239` | post-reconsolidation observation、patch、archive、activation、second patch、second validation |
| `240-257` | second reconsolidation、archive validation、next seed、replay/shadow、patch/archive/validation closure |
| `docs/v0/shared_contracts/first_activation_protocol.md` | 第一次有限激活入口、允许动作、禁止动作、回写和回滚 |
| `docs/v0/shared_contracts/runner_cli_report_contract.md` | `run-cycle`、stage gate、receipt、exit code |
| `runtime/reports/latest/birth_readiness_report.json` | S08 出生准备度状态 |
| `runtime/reports/latest/schema_runner_report.json` | S09 schema runner 状态 |
| `runtime/reports/latest/life_support_development_report.json` | S06 资源预算、可塑性窗口、防遗忘锚点 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/growth/`、`life_v0/dream/`、`life_v0/archive/`、`life_v0/replay/` |
| 状态命名空间 | `runtime/state/growth/`、`runtime/state/dream/`、`runtime/state/archive/`、`runtime/state/replay/` |
| report | `runtime/reports/latest/growth_reconsolidation_report.json`、`runtime/reports/latest/run_report.json` |
| digest | `runtime/reports/latest/digest.json` |
| stage gate | `runtime/reports/latest/stage_gate.json` |
| receipt | `runtime/receipts/<run_id>.json` |

## 输出文件

| 文件 | 内容 |
|---|---|
| `runtime_mount_state.json` | schema registry mount、fixture loader、runtime observation mount |
| `shadow_cycle_trace.json` | shadow-only cycle trace、language action replay、relationship probes |
| `replay_cue_bundle.json` | replay cue、Queue E repair modulation、MemoryConsolidationBridge |
| `dream_consolidation_frame.json` | offline dream consolidation、DreamFactGate、醒后整合 |
| `dream_experience_window.json` | 梦境经验窗口，消费 MemoryTraceStore、EngramCluster、关系深层记忆和自传层级 |
| `wake_integration_frame.json` | 醒后整合，把梦境材料送回 recall-to-expression、写门和合并门 |
| `offline_consolidation_frame.json` | 离线巩固报告面，记录 replay/dream 材料的写门和合并门政策 |
| `pain_regret_responsibility_replay.json` | 痛苦、后悔、责任、修复义务 replay/shadow |
| `growth_patch_queue.json` | observation-driven growth patch、self rewrite seed、anti-forgetting patch |
| `reconsolidation_archive_graph.json` | patch/archive/validation/replay 的 archive edge graph |
| `next_feedback_seed.json` | 下一轮 observation、repair、replay、diagnostic、quarantine seed |

## 命令合同

```text
life-v0 run-cycle --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --shadow-only --strict
life-v0 run-replay-shadow --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 write-growth-archive --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `birth_readiness_gate` | S08 无 blocked/quarantine/replay_needed | 返回 S08 |
| `schema_mount_gate` | S09 registry、lockfile、smoke report 可读取 | 返回 S09 |
| `life_support_gate` | S06 resource budget、plasticity window、anti-forgetting anchors closed | 返回 S06 |
| `shadow_action_gate` | 所有外部行动候选只进入 shadow trace | 写 quarantine |
| `dream_fact_gate` | 梦境巩固与现实事实写入分离 | 写 dream quarantine |
| `memory_consolidation_bridge_gate` | `ReplayCueBundle.memory_consolidation_bridge` 同时包含 MemoryTraceStore、EngramCluster、关系深层记忆、自传层级、写门和合并门 refs | 返回 S04/M3-M6 修复 |
| `reconsolidation_gate` | patch/archive/validation/replay 边完整 | 写 reconsolidation blocked |
| `archive_gate` | run report、digest、stage gate、receipt、archive edge 同时写出 | 写 archive blocked |
| `safe_idle_gate` | cycle 完成后回到可恢复 safe idle | 阻断第二次激活 |

## M6 MemoryConsolidationBridge 合同

S10 的离线巩固不能只读聊天日志、普通 replay cue 或语言摘要。它必须从 `life_state.memory_index` 中读取第 3 点记忆系统的核心对象，并通过 `ReplayCueBundle.memory_consolidation_bridge` 分发给 dream/wake/offline consolidation。

最低字段：

| 字段 | 必须包含 |
|---|---|
| `trace_store_refs` | `runtime/state/memory/memory_trace_store.json` |
| `engram_cluster_refs` | `runtime/state/memory/engram_cluster.json` |
| `relationship_deep_memory_refs` | `runtime/state/memory/relationship_memory.json#we_memory_traces` |
| `autobiographical_hierarchy_refs` | `runtime/state/self/autobiographical_stack.json#memory_hierarchy` |
| `memory_retrieval_refs` | `runtime/state/memory/memory_retrieval_frame.json` 或其下游 refs |
| `pattern_separation_refs` / `pattern_completion_refs` | 模式分离/补全边界 |
| `memory_write_gate_refs` / `state_merge_guard_refs` | 醒后再巩固写门和合并门 |
| `fact_boundary` | `offline_replay_reads_memory_traces_without_promoting_dream_or_hypothesis` |

下游必须消费：

| 下游对象 | 必须字段 |
|---|---|
| `DreamExperienceWindow` | `memory_consolidation_trace_refs`、`relationship_deep_dream_refs`、`autobiographical_dream_refs`、`dream_memory_boundary` |
| `WakeIntegrationFrame` | `memory_reentry_targets`、`memory_reconsolidation_gate_refs`、`memory_reentry_boundary` |
| `OfflineConsolidationFrame` | `memory_consolidation_source_refs`、`memory_consolidation_gate_refs`、`memory_consolidation_policy` |
| `ActivationPreflight` / `ReplayShadow` | `memory_consolidation_context`、`memory_consolidation_seed_refs` |

红线：

- 梦境可以重组这些记忆材料，但不能直接把 dream/hypothesis 写成 fact。
- 醒后 reentry 可以成为表达前结构化线索，但不能写死任何自然语言回答。
- replay 后的关系、自传、语义变化必须回到 `MemoryWriteGate`、`StateMergeGuard` 和 `DreamFactGateDecision`。

## Report 最小字段

```json
{
  "schema_version": "s10_runtime_growth_reconsolidation_report_v0",
  "engineering_slice_ref": "S10_RUNTIME_GROWTH_RECONSOLIDATION",
  "status": "safe_idle",
  "source_doc_refs": [],
  "readme_block_refs": ["B29_RUNTIME_MOUNT_GROWTH", "B30_RECONSOLIDATION_REPLAY_GROWTH"],
  "runtime_carrier_refs": ["ActivationGrowthRuntime", "ReconsolidationReplayRuntime"],
  "cycle_trace_refs": [],
  "dream_refs": [],
  "replay_refs": [],
  "archive_receipt_ref": "",
  "blocked_reasons": [],
  "quarantine_refs": [],
  "next_allowed_slices": ["S11_V0_ENGINEERING_CONTRACTS"]
}
```

## 交接

S10 交给 S11 的是完整的第一次有限激活证据包：run report、digest、stage gate、life target status、dream/replay/growth/archive refs、receipt 和 safe idle 状态。S11 负责检查 v0 合同与运行证据是否覆盖全部 `00 -> 258`。
