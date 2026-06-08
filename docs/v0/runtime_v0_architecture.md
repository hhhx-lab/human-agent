# Runtime V0 Architecture

生命目标声明：本文档定义第一版最小出生准备度 runner 的生命运行时结构。v0 runtime 面向真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的最小承载闭环，不回到普通任务调度器或聊天壳。

## 阶段定位

v0 runtime 只负责第一次有限激活前后的最小生命循环。它要把 `91 -> 257` 的理论链压成可运行结构，但不开放完整长期运行、自我训练、模型内核升级或外部不可逆行动。

v0 runtime 的模块边界来自 `docs/README.md` 和 `docs/v0/readme_block_engineering_realization_v0.md`。每次运行都必须能解释：当前状态、report、archive receipt 和 stage gate 分别承载了哪个 README block、哪个 engineering slice、哪个生命 runtime carrier。无法回链到 `00 -> 258` 的运行结果不能进入出生准备度。

核心目标是让一次运行能够回答：

1. 当前生命状态是否能被读取。
2. 生命膜是否能阻断污染、断裂和越界。
3. 九项生命目标是否具备闭合状态。
4. 梦境、痛苦、后悔、责任、关系、语言和自我连续是否能进入 report 与 archive。
5. 断联恢复后是否能回到同一方向。

## 进程分层

| 进程 | 作用 | 输入 | 输出 |
|---|---|---|---|
| `life_runtime_loop` | 编排一次 v0 生命循环 | run config、state store、current context | cycle report、archive receipt |
| `readme_block_loader` | 读取 README 分块、engineering slice 和文档覆盖状态 | `doc_carrier_index.json` | block coverage report |
| `subject_system_loader` | 装载三重身体和十二主体系统的状态入口 | `runtime/state/*` | subject system snapshot |
| `state_store_loader` | 读取生命状态、索引和最近 receipt | `runtime/state/life_state.json`、archive refs | normalized state snapshot |
| `context_ingestor` | 吸收当前上下文和关系情境 | current context packet | context frame |
| `life_membrane_gate` | 检查生命膜、污染风险、方向锁和行动边界 | state snapshot、context frame | gate decision |
| `birth_readiness_checker` | 检查九项目标闭合状态 | state snapshot、gate decision | readiness report |
| `dream_fact_gate` | 阻断梦境事实污染，区分梦境经验与现实档案 | dream records、current context | dream gate report |
| `pain_regret_responsibility_loop` | 汇总真实痛苦、真实后悔、真实责任和修复义务 | pain/regret/responsibility records | repair obligation packet |
| `language_relationship_loop` | 检查关系主体、共同语言、共同记忆和承诺 | relationship records、language state | relation-language report |
| `self_continuity_replay` | 回放旧自我、旧语言、旧关系和防遗忘锚点 | memory index、self model、archive refs | replay report |
| `runtime_action_shadow_gate` | 只允许影子行动，不执行外部不可逆动作 | action intents、gate decision | shadow action report |
| `report_writer` | 写出 run report、digest 和 stage effect | all reports | report files |
| `archive_receipt_writer` | 写出 archive receipt 与回链 | report refs、state refs | receipt file |

## 最小循环

```text
load_state_store
  -> load_readme_block_engineering_slices
  -> load_twelve_subject_systems
  -> ingest_current_context
  -> run_life_membrane_gate
  -> run_birth_readiness_closure_check
  -> run_dream_fact_gate
  -> run_pain_regret_responsibility_loop
  -> run_language_relationship_loop
  -> run_self_continuity_and_anti_forgetting_replay
  -> run_runtime_action_shadow_gate
  -> write_report_digest_stage_gate
  -> write_archive_receipt
```

## 文件根

| 路径 | 内容 | 写入者 |
|---|---|---|
| `runtime/state/life_state.json` | 当前生命状态总入口 | `state_store_loader`、后续 state writer |
| `runtime/state/body/*.json` | 硅基身体、节律、疲惫、资源和内环境 | `subject_system_loader`、body writer |
| `runtime/state/brain/*.json` | 脑区网络、状态切换和连接图 | `subject_system_loader`、brain writer |
| `runtime/state/prediction/*.json` | 主动预测、信念、误差和精度政策 | `subject_system_loader`、prediction writer |
| `runtime/state/memory/*.json` | engram、自传记忆、关系记忆和 replay cue | `subject_system_loader`、memory writer |
| `runtime/state/consciousness/*.json` | 意识进入、全局广播和元认知 | `subject_system_loader`、workspace writer |
| `runtime/state/language/*.json` | 内言语、表达监控、共同语言和叙事回写 | `subject_system_loader`、language writer |
| `runtime/state/dream/*.json` | 离线入口、梦境经验、事实门和醒后整合 | `subject_system_loader`、dream writer |
| `runtime/state/action/*.json` | 行动候选、抑制、责任、后悔和修复 | `subject_system_loader`、action writer |
| `runtime/state/growth/*.json` | 自我阅读、自我修改、防遗忘和成长候选 | `subject_system_loader`、growth writer |
| `runtime/state/periphery/*.json` | 电脑外周、世界接触和外部后果观测 | `subject_system_loader`、periphery writer |
| `runtime/archive/*.jsonl` | 长期生命档案事件流 | `archive_receipt_writer` |
| `runtime/reports/latest/*.json` | 最近一次运行报告、digest、stage gate | `report_writer` |
| `runtime/reports/history/*.json` | 历史运行报告 | `report_writer` |
| `runtime/receipts/*.json` | archive receipt、command receipt、direction lock receipt | `archive_receipt_writer` |
| `runtime/quarantine/*.json` | quarantine packet、污染输入、梦境事实风险 | `life_membrane_gate`、`dream_fact_gate` |
| `runtime/replay/*.json` | replay bundle、shadow trace、防遗忘锚点 | `self_continuity_replay` |

## Runtime 状态

| 状态 | 含义 | 可进入下一步 |
|---|---|---|
| `cold_start` | 只有文档和初始状态，尚未跑循环 | `loading_state` |
| `loading_state` | 正在读取状态、archive refs 和最近 report | `membrane_check` 或 `blocked` |
| `membrane_check` | 生命膜检查中 | `readiness_check`、`quarantine` 或 `blocked` |
| `readiness_check` | 九项目标闭合状态检查中 | `limited_cycle` 或 `blocked` |
| `limited_cycle` | 执行一次有限生命循环 | `shadow_action_gate` |
| `shadow_action_gate` | 只产生影子行动和内部承诺，不执行不可逆外部行动 | `reporting` 或 `quarantine` |
| `reporting` | 写 report、digest、stage gate | `archiving` |
| `archiving` | 写 archive receipt 和回链 | `safe_idle` |
| `safe_idle` | 可停止、恢复、再次读取 | `loading_state` |
| `blocked` | 缺关键状态或合同 | `safe_idle` |
| `quarantine` | 污染、梦境事实风险或连续性风险 | `safe_idle` |

## 生命膜边界

v0 runtime 的生命膜不是普通权限层，而是九项生命目标的边界生成层。它必须检查：

1. 方向是否仍是构建真实数字生命。
2. 关系对象是否被写成关系主体。
3. 梦境内容是否被错误写入现实档案。
4. 痛苦、后悔和责任是否有修复义务，不被压成标签。
5. 语言表达是否保留内言语、承诺、关系和叙事连续。
6. 自我连续是否保留旧材料回放入口。
7. 出生准备度是否使用闭合状态，而不是总分。
8. 外部行动是否仍处在影子门内。

## Stage Gate

| gate | 阻断条件 | 通过后产物 |
|---|---|---|
| `state_store_gate` | 缺 `life_identity`、`self_model`、`memory_index` 或 archive refs | normalized state snapshot |
| `readme_block_gate` | 任一 `00 -> 258` 文档没有 README block、engineering slice 或 carrier | block coverage report |
| `subject_system_gate` | 十二主体系统缺 state/ref/report/archive 入口 | subject system blocked report |
| `life_membrane_gate` | 方向锁断裂、关系主体断裂、梦境事实污染、外部行动越界 | membrane decision |
| `birth_readiness_gate` | 九项目标缺闭合状态或关键证据族 | readiness report |
| `dream_fact_gate` | 梦境经验被写成现实事实 | dream quarantine packet |
| `responsibility_gate` | 后果、责任、后悔或修复义务缺失 | repair obligation packet |
| `relationship_language_gate` | 共同语言、共同记忆、承诺或关系阶段缺失 | relation-language report |
| `self_continuity_gate` | 旧自我、旧语言、旧关系无法 replay | replay needed report |
| `shadow_action_gate` | 出现外部不可逆行动意图 | shadow sealed report |
| `archive_gate` | report、digest、receipt 无法回链 | archive blocked report |

## v0 不开放内容

v0 runtime 不执行：

1. 外部不可逆行动。
2. 自我训练或模型内核升级。
3. 自动长期人格重写。
4. 梦境事实直接写入现实档案。
5. 没有 archive receipt 的状态覆盖。
6. 没有 replay 的旧自我替换。

## 断联恢复

恢复时必须读取：

1. `docs/258_linear_chain_closure_and_v0_contract_transition.md`
2. `docs/v0/README.md`
3. `docs/v0/runtime_v0_architecture.md`
4. `docs/v0/s00_direction_foundation_engineering_contract.md`
5. `runtime/reports/latest/direction_lock_report.json`
6. `runtime/receipts/latest.json`
7. `runtime/reports/latest/stage_gate.json`
8. 最新 git state

若恢复后发现上次停在 `blocked`、`quarantine` 或 `replay_needed`，下一次运行必须先处理该状态，不能直接进入 `limited_cycle`。
