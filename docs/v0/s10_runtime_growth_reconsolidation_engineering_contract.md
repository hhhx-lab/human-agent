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
| `docs/v0/first_activation_protocol.md` | 第一次有限激活入口、允许动作、禁止动作、回写和回滚 |
| `docs/v0/runner_cli_report_contract.md` | `run-cycle`、stage gate、receipt、exit code |
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
| `dream_consolidation_frame.json` | offline dream consolidation、DreamFactGate、醒后整合 |
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
| `reconsolidation_gate` | patch/archive/validation/replay 边完整 | 写 reconsolidation blocked |
| `archive_gate` | run report、digest、stage gate、receipt、archive edge 同时写出 | 写 archive blocked |
| `safe_idle_gate` | cycle 完成后回到可恢复 safe idle | 阻断第二次激活 |

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
