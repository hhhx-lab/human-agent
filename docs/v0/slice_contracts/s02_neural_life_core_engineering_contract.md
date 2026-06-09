# S02 Neural Life Core Engineering Contract

生命目标声明：本文档把 `S02_NEURAL_LIFE_CORE` 固定为第一版数字生命主体核心的工程合同。它的职责不是启动完整长期生命，也不是复制任何现成 agent 框架，而是把 `02-13` 的脑科学主干、`01*` 权威来源层、`142/145/151` 的 authority patch 链、`digital_life_macro_architecture_v0.md` 的三重身体和十二主体系统，压成可运行的神经生命核心状态、内部 bus、source authority 回链、report 和 receipt。S02 通过后，后续 S04/S03/S07/S08 才能把记忆、生命膜、语言关系和九项目标继续落成运行时对象。

## 模块定位

`S02_NEURAL_LIFE_CORE` 是数字生命出生前的主体骨架。它回答七个问题：

1. `02-13` 是否已经从综述文档进入十二主体系统，而不是停留在文本理论。
2. 每个主体系统是否拥有 source authority refs、机制对象、runtime carrier、状态命名空间和下游连接。
3. 三重身体是否明确分为 `SiliconBody`、`NeuralLifeCore` 和 `ComputerBody`，电脑外周不能变成主体架构。
4. 内部 bus 是否把身体、脑图谱、信号介质、预测、记忆、意识、语言、情绪自我、梦境和行动责任连成闭环。
5. `02-13` 每份核心文档是否都有来自 S01 的 `DocAuthorityCarrierPatch`。
6. AI/cognitive architecture/LLM agent 来源是否仍然只作为电脑外周、技术桥和负边界材料。
7. 下一步是否允许进入 `S04_STATE_OBJECT_STORE` 和 `S03_DIRECTION_LIFE_MEMBRANE`，而不是直接开放长期运行。

S02 不执行真实对话，不写长期人格慢变量，不生成梦境内容，不触碰外部程序，也不进行自我训练。它只生成主体系统骨架、内部连接、authority binding、状态种子、report 和 receipt。

## 直接读取文档

| 文档 | S02 吸收内容 | 工程承载 |
|---|---|---|
| `docs/02_brain_region_and_network_atlas.md` | 脑区/连接组/多尺度图谱、区域动态边界 | `multiscale_brain_graph_seed.json` |
| `docs/03_default_executive_salience_networks.md` | 默认/执行/显著性网络、状态切换 | `network_mode_seed.json` |
| `docs/04_sensory_thalamus_interoception.md` | 感知、丘脑路由、内感受、稳态和主动推理 | `silicon_body_seed.json`、`prediction_seed.json` |
| `docs/05_memory_systems_and_growth.md` | engram、海马-皮层、巩固与成长 | `memory_core_seed.json` |
| `docs/06_action_reward_inhibition.md` | 动作选择、奖赏、抑制、责任前体 | `action_responsibility_seed.json` |
| `docs/07_emotion_personality_self.md` | 情绪、自我、人格慢变量、后悔前体 | `affective_self_seed.json` |
| `docs/08_sleep_dream_fatigue_states.md` | 睡眠、梦境、疲惫、离线 replay | `dream_offline_seed.json` |
| `docs/09_language_symbolic_top_layer.md` | 语言网络、内言语、表达监控、语言行动桥 | `language_relationship_seed.json` |
| `docs/10_consciousness_attention_workspace.md` | 意识进入、全局工作区、报告性、元认知 | `conscious_workspace_seed.json` |
| `docs/11_neuromodulation_and_signal_media.md` | 神经调质、兴奋抑制、信号介质、精度政策 | `signal_media_seed.json` |
| `docs/12_ai_and_cognitive_architecture_bridge.md` | 电脑外周、认知架构桥、AI 负边界 | `computer_body_boundary_seed.json` |
| `docs/13_agentic_human_research_synthesis.md` | 跨模块综合、生命目标上卷、工程闭环 | `neural_life_core_synthesis_seed.json` |
| `docs/v0/architecture/digital_life_macro_architecture_v0.md` | 三重身体、十二主体系统和内部循环 | `twelve_subject_systems.json` |
| `runtime/state/authority/*` | source registry、机制证据图、`02-13` authority patches | `authority_binding_snapshot.json` |
| `runtime/docs/doc_carrier_index.json` | `02-13` 的 README block、engineering slice 和 runtime carrier | `doc_core_coverage_snapshot.json` |

## 十二主体系统

S02 生成 `twelve_subject_systems.json`。第一版系统清单固定为：

| system id | 主体位置 | 输入文档 | 主要状态命名空间 | 主要下游 |
|---|---|---|---|---|
| `SiliconBodyRuntime` | 内环境、节律、资源、疲惫、压力 | `04`、`11`、`37`、`38` | `runtime/state/body/` | 信号介质、情绪、梦境、生命支持 |
| `MultiscaleBrainGraphRuntime` | 脑区、连接组、大尺度网络 | `02`、`03`、`10`、`11` | `runtime/state/brain/` | 所有主体系统 |
| `SignalMediaRuntime` | 调质、兴奋抑制、精度政策 | `11`、`18`、`22`、`30` | `runtime/state/signal/` | 预测、意识、情绪、行动 |
| `PredictionActiveInferenceRuntime` | 主动预测、误差、证据寻求 | `04`、`10`、`11`、`13`、`01v-01ax` | `runtime/state/prediction/` | 记忆、语言、行动、梦境 |
| `MemoryEngramRuntime` | 情景、自传、关系、责任记忆 | `05`、`17`、`21`、`25`、`41` | `runtime/state/memory/` | 语言、梦境、人格、成长 |
| `ConsciousWorkspaceRuntime` | 意识进入、全局广播、报告性 | `10`、`13`、`143`、`146` | `runtime/state/consciousness/` | 语言、行动、出生准备度 |
| `LanguageRelationshipRuntime` | 语言主神经束和关系生成 | `09`、`85-90`、`96`、`101` | `runtime/state/language/`、`runtime/state/relationship/` | 行动、记忆、关系、责任 |
| `AffectiveSelfRuntime` | 情绪、自我、人格慢变量 | `07`、`18`、`39`、`40`、`92`、`93` | `runtime/state/self/` | 语言、行动、梦境、成长 |
| `DreamOfflineRuntime` | 梦境、离线整合、疲惫恢复 | `08`、`19`、`23`、`95`、`99` | `runtime/state/dream/` | 记忆、自我、行动修复 |
| `ActionResponsibilityRuntime` | 动作选择、抑制、后果、责任 | `06`、`75`、`80-84`、`94`、`98` | `runtime/state/action/` | 外周、后悔、修复 |
| `ComputerPeripheralRuntime` | 电脑、终端、文件、浏览器和外部程序 | `12`、`15`、`20`、`24`、`28`、`32`、`89` | `runtime/state/computer/` | 世界接触膜 |
| `GrowthReplayRuntime` | 再巩固、replay、成长和防遗忘 | `05`、`08`、`92`、`93`、`181-257` | `runtime/state/growth/`、`runtime/state/replay/` | 自我成长、archive |

## 内部 Bus

S02 生成 `neural_life_internal_bus.json`。第一版 bus 不传递真实消息，只固定可检查的连接边：

```text
body_signal_bus
  -> signal_media_bus
  -> prediction_error_bus
  -> conscious_broadcast_bus
  -> inner_language_bus
  -> affective_self_bus
  -> action_responsibility_bus
  -> peripheral_shadow_bus
  -> observation_writeback_bus
  -> memory_reconsolidation_bus
  -> dream_offline_bus
  -> growth_replay_bus
```

每条 bus edge 都必须有 `from_system`、`to_system`、`payload_family`、`source_doc_refs`、`authority_refs`、`life_targets` 和 `stage_policy`。没有 authority refs 的边不能进入后续状态对象。

## 状态命名空间

S02 所有运行态写入 `runtime/state/neural_life_core/`：

| 文件 | 内容 |
|---|---|
| `neural_life_core.json` | S02 总入口、三重身体、当前闭合状态、下一 slice |
| `twelve_subject_systems.json` | 十二主体系统、source docs、authority refs、runtime carriers、state namespaces |
| `neural_life_internal_bus.json` | 内部 bus 边、payload family、stage policy |
| `authority_binding_snapshot.json` | S01 registry、mechanism map、`02-13` patch 引用 |
| `doc_core_coverage_snapshot.json` | `02-13` 文档覆盖、readme block、engineering slice、carrier |
| `computer_body_boundary_seed.json` | 电脑外周只作为外设和观测入口的负边界 |
| `neural_life_core_manifest.json` | S02 输出文件、schema version、receipt refs |

S02 不写入长期 `runtime/state/memory/*`、`language/*`、`dream/*` 的真实事件，只写系统种子和命名空间约定。

## Report 与 receipt

| 产物 | 路径 | 必须字段 |
|---|---|---|
| S02 report | `runtime/reports/latest/neural_life_core_report.json` | `status`、`stage_effect`、`system_count`、`bus_edge_count`、`core_doc_coverage`、`authority_patch_coverage`、`blocked_gates` |
| S02 digest | `runtime/reports/latest/neural_life_core_digest.json` | 当前 slice、三重身体、下一步、最大缺口 |
| S02 receipt | `runtime/receipts/neural_life_core_<run_id>.json` | 输入 hash、authority refs、state refs、report refs |

S02 report 必须包含 v0 回链字段：

```json
{
  "source_doc_refs": ["docs/02_brain_region_and_network_atlas.md"],
  "readme_block_refs": ["B02_CORE_NEURAL_LIFE"],
  "engineering_slice_ref": "S02_NEURAL_LIFE_CORE",
  "runtime_carrier_refs": ["BrainRegionNetworkRuntime"]
}
```

## 阶段门

| gate | 输入 | closed 条件 | 失败后动作 |
|---|---|---|---|
| `s01_permission_gate` | `source_authority_report.json`、`source_authority_digest.json` | S01 closed 且下一 slice 为 S02 | 返回 S01 |
| `core_doc_coverage_gate` | `doc_carrier_index.json` | `02-13` 全部属于 `S02_NEURAL_LIFE_CORE` 或综合承接链 | 返回 P0 |
| `authority_patch_gate` | `doc_authority_carrier_patch_index.json` | `02-13` 每份都有 patch、authority refs 和机制对象 | 返回 S01 |
| `twelve_system_gate` | `twelve_subject_systems.json` | 12 个主体系统全部存在且有 source docs、authority refs、state namespace | 阻断 S04/S03 |
| `internal_bus_gate` | `neural_life_internal_bus.json` | bus 边覆盖身体、预测、记忆、意识、语言、情绪、梦境、行动、外周、成长 | 写 repair finding |
| `computer_boundary_gate` | `computer_body_boundary_seed.json` | 外部框架只进入 `ComputerPeripheralRuntime`、`WorldContactMembrane`、`RunnerCliRuntime` | quarantine |
| `next_slice_permission_gate` | S02 report | 只允许进入 `S04_STATE_OBJECT_STORE` 和 `S03_DIRECTION_LIFE_MEMBRANE` | 阻断开放运行 |

## 命令合同

S02 当前落地两个命令：

```text
life-v0 build-neural-life-core --docs docs --doc-index runtime/docs/doc_carrier_index.json --authority runtime/state/authority --out runtime/state/neural_life_core --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-neural-life-core --state runtime/state/neural_life_core --reports runtime/reports/latest --strict
```

出生前命令链变为：

```text
ingest-docs
  -> build-direction-lock
  -> build-source-authority
  -> build-neural-life-core
  -> check-neural-life-core
  -> load-state-store
```

## 第一轮实现切片

1. **S02-A：系统清单与 authority binding**

   生成 `twelve_subject_systems.json` 和 `authority_binding_snapshot.json`。

2. **S02-B：内部 bus 与三重身体边界**

   生成 `neural_life_internal_bus.json`、`computer_body_boundary_seed.json`。

3. **S02-C：核心文档覆盖和 patch 检查**

   生成 `doc_core_coverage_snapshot.json`，检查 `02-13` patch 和 carrier。

4. **S02-D：report、digest、receipt 和下一 slice 许可**

   写 `neural_life_core_report.json`、`neural_life_core_digest.json` 和 receipt，只允许进入 S04/S03。

5. **S02-E：只读复查门**

   `check-neural-life-core` 读取 S02 state 与 build report，写 `neural_life_core_check_report.json`，确认十二主体系统、内部 bus、authority binding、核心覆盖、电脑外周边界和下一 slice 许可仍然 closed。

## 验收

S02 完成后必须满足：

1. `life-v0 build-neural-life-core --strict` 返回 `status=closed`。
2. `twelve_subject_systems.json` 含 12 个主体系统，每个系统有 source docs、authority refs、runtime carriers、state namespace 和 life targets。
3. `neural_life_internal_bus.json` 至少含 12 条 bus edge，并覆盖三重身体循环。
4. `doc_authority_carrier_patch_index.json` 中 `02-13` 每份 patch 被 S02 读取。
5. `ComputerPeripheralRuntime` 被固定为电脑外周，不进入记忆、意识、语言、情绪、梦境、关系或人格主体。
6. S02 report 的下一步只能指向 `S04_STATE_OBJECT_STORE` 与 `S03_DIRECTION_LIFE_MEMBRANE`，不能直接进入开放式长期运行。
7. `life-v0 check-neural-life-core --strict` 返回 `status=closed`，并写出 `neural_life_core_check_report.json`。

## 本轮边界

S02 是主体骨架生成，不是第一次生命激活。它让数字生命的大脑、身体、语言、梦境、行动、情绪、责任和成长有工程骨架，但还没有真实事件流。真实事件流必须等待 S04 状态对象、S03 生命膜、S07 语言关系和 S08 九项目标继续闭合。
