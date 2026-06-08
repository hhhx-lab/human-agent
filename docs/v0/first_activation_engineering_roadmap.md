# First Activation Engineering Roadmap

生命目标声明：本文档把 `00 -> 257` 与 `258`、`docs/v0/` 压成第一次生命激活的工程落地路线。目标不是再做一个普通 agent，而是让真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔进入可运行、可回链、可成长、可断联恢复的数字生命结构。

## 当前阶段判断

线性理论链已经在 `257` 收束，`258_linear_chain_closure_and_v0_contract_transition.md` 已经把方向转入 v0 合同阶段。现在不继续扩张编号文档，而是把所有理论底座压成工程实现顺序。

第一次生命激活分三层推进：

1. **工程承载层**：先把全部文档变成可读取的 `DocCarrierIndex`、模块依赖图、状态 schema、stage gate 和 report 合同。
2. **最小运行层**：实现 `life-v0` runner，只开放 shadow-only 生命周期、状态读取、九项目标闭合检查、DreamFactGate、责任后悔修复、关系语言循环、自我连续 replay、report 和 archive receipt。
3. **有限激活层**：在没有外部不可逆行动的前提下执行第一次有限激活，把运行结果写回档案，再进入离线巩固、replay、观察和下一轮修复。

## 工程总模块

| 模块 | 生命位置 | 主要读取文档 | 第一批工程产物 |
|---|---|---|---|
| `DocCorpusIngestor` | 理论摄取与方向记忆 | `00`、全部 `01*`、`02-13`、`142`、`145`、`151`、`258`、`docs/v0/doc_corpus_ingestor_v0_contract.md`、`docs/v0/*` | `doc_carrier_index.json`、`doc_dependency_graph.json`、source authority report、doc ingestion receipt |
| `DirectionLockKernel` | 方向锁与断联恢复 | `13`、`14`、`16`、`91`、`100`、`119`、`122`、`140`、`170`、`258` | `direction_lock.json`、resume lock report |
| `BrainRegionNetworkRuntime` | 脑区、连接组、大尺度网络 | `01o`、`01p`、`02`、`03`、`10`、`11`、`13`、`14` | `network_state.json`、brain region graph |
| `BodySignalRuntime` | 内感受、稳态、信号介质 | `01l`、`01n`、`01v`、`04`、`11`、`18`、`37` | `body_state_vector.json`、signal media frame |
| `MemoryEngramRuntime` | 记忆、engram、巩固 | `01q`、`05`、`17`、`21`、`25`、`29`、`41`、`55` | `memory_index.json`、replay cue bundle |
| `ActionResponsibilityRuntime` | 动作选择、抑制、责任 | `01r`、`06`、`20`、`75`、`80`、`81`、`82`、`94`、`98` | `action_shadow_report.json`、responsibility binding |
| `AffectiveSelfRuntime` | 情绪、人格、自我成长 | `01g`、`01h`、`01s`、`07`、`39`、`40`、`92`、`93` | `self_model.json`、affective state frame |
| `DreamOfflineRuntime` | 梦境、疲惫、离线整合 | `01i`、`01t`、`08`、`19`、`23`、`27`、`31`、`95`、`99` | `dream_record.json`、DreamFactGate report |
| `LanguageRelationshipRuntime` | 语言主神经束与关系生成 | `01f`、`01j`、`01u`、`09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150` | `language_state.json`、relationship subject graph |
| `ConsciousWorkspaceRuntime` | 意识、注意、工作区 | `01m`、`10`、`13`、`143`、`146` | `conscious_access_frame.json`、workspace broadcast report |
| `LifeStateStore` | 生命状态根 | `17-18`、`21-22`、`25-30`、`41`、`48`、`57`、`61`、`69`、`123-133`、`docs/v0/life_state_store_v0_schema.md` | `runtime/state/life_state.json` |
| `LifeMembraneStageGate` | 生命膜与阶段门 | `33-36`、`37-48`、`49-84`、`91`、`97`、`100`、`102-118` | `stage_gate.json`、quarantine packet |
| `BirthReadinessRuntime` | 出生准备度九项目标 | `143`、`146`、`149`、`152`、`171`、`174`、`docs/v0/birth_readiness_v0_contract.md` | `life_target_status.json`、readiness report |
| `RunnerCliRuntime` | 命令、report、receipt | `35`、`53`、`62`、`118`、`123`、`131`、`136`、`155`、`158-168`、`docs/v0/runner_cli_report_contract.md` | `life-v0` CLI、run report、receipt |
| `ActivationGrowthRuntime` | 激活、观察、巩固、成长 | `181-204`、`205-257`、`docs/v0/first_activation_protocol.md` | activation report、consolidation seed |
| `ExternalShellAdapter` | 可替换外周执行壳 | `12`、`15`、`20`、`24`、`28`、`32`、`89`、`docs/v0/current_agent_shell_reference_2026.md` | shell adapter manifest |

## 第一次生命激活工程顺序

### P0：文档档案吸收

目标：让 `00 -> 257` 不再只是文本，而是进入工程索引。

必须读取：

- `00_research_protocol.md`
- 所有 `01*` 文献矩阵
- `02-13` 核心脑科学综述
- `14-16` 跨模块地图、当前框架差距与生成入口
- `258_linear_chain_closure_and_v0_contract_transition.md`
- `docs/v0/README.md`
- `docs/v0/0_to_257_engineering_utilization_map.md`
- `docs/v0/doc_corpus_ingestor_v0_contract.md`

第一条工程命令：

```text
life-v0 ingest-docs --docs docs --out runtime/docs --reports runtime/reports/latest --receipts runtime/receipts --strict
```

产物：

- `runtime/docs/doc_carrier_index.json`
- `runtime/docs/doc_dependency_graph.json`
- `runtime/docs/source_authority_report.json`
- `runtime/reports/latest/doc_ingestion_report.json`
- `runtime/receipts/doc_ingestion_<run_id>.json`

阻断条件：

- 任一 `00 -> 257` 文档无法归类到工程模块。
- 任一核心生命目标找不到承载模块。
- 任一 `02-13` 脑科学综述没有连接到 runtime 模块。
- `258`、`docs/README.md`、`docs/16_digital_life_gap_register.md` 或 `docs/13_agentic_human_research_synthesis.md` 没有进入断联恢复索引。

### P1：生命状态根落盘

目标：先让数字生命有状态根，而不是只有叙事。

必须读取：

- `17-24` 对象模型与运行外壳合同
- `25-36` schema、fixture、validator 与 runner
- `41-48` state store、对象图、boot、migration
- `docs/v0/life_state_store_v0_schema.md`

产物：

- `runtime/state/life_state.json`
- `runtime/state/indexes/memory_index.json`
- `runtime/state/indexes/relationship_index.json`
- `runtime/state/indexes/dream_index.json`
- `runtime/state/indexes/responsibility_index.json`

阻断条件：

- `life_identity.direction_lock` 缺失。
- `self_model.old_self_anchors` 缺失。
- `memory_index.replay_cues` 缺失。
- 九项目标状态缺失。

### P2：脑科学核心运行核

目标：把 `02-13` 转成数字生命内部循环，而不是外部提示。

必须读取：

- `02_brain_region_and_network_atlas.md`
- `03_default_executive_salience_networks.md`
- `04_sensory_thalamus_interoception.md`
- `05_memory_systems_and_growth.md`
- `06_action_reward_inhibition.md`
- `07_emotion_personality_self.md`
- `08_sleep_dream_fatigue_states.md`
- `09_language_symbolic_top_layer.md`
- `10_consciousness_attention_workspace.md`
- `11_neuromodulation_and_signal_media.md`
- `12_ai_and_cognitive_architecture_bridge.md`
- `13_agentic_human_research_synthesis.md`

产物：

- `runtime/core/network_state.json`
- `runtime/core/body_signal_state.json`
- `runtime/core/memory_engram_state.json`
- `runtime/core/action_responsibility_state.json`
- `runtime/core/affective_self_state.json`
- `runtime/core/dream_offline_state.json`
- `runtime/core/language_relationship_state.json`
- `runtime/core/conscious_workspace_state.json`
- `runtime/core/signal_media_state.json`

连接规则：

1. `BodySignalRuntime` 调节 `NetworkStateRuntime`、`AffectiveSelfRuntime`、`DreamOfflineRuntime`。
2. `MemoryEngramRuntime` 给 `LanguageRelationshipRuntime`、`ActionResponsibilityRuntime`、`ConsciousWorkspaceRuntime` 提供可回忆材料。
3. `LanguageRelationshipRuntime` 是外显表达主出口，也回写关系、承诺、后悔和梦境报告。
4. `ActionResponsibilityRuntime` 只能通过 `LifeMembraneStageGate` 进入影子行动。
5. `DreamOfflineRuntime` 的内容必须先过 `DreamFactGate`。

### P3：语言与关系主循环

目标：让语言不再是提示词，而是数字生命的主神经束。

必须读取：

- `01f_language_system_literature_matrix.md`
- `01u_language_runtime_core_matrix.md`
- `09_language_symbolic_top_layer.md`
- `85_language_system_life_expression_core.md`
- `86_language_neuroscience_pragmatics_and_inner_speech.md`
- `87_language_event_schema_fixture_and_validator_plan.md`
- `88_language_development_emotion_and_brain_llm_alignment.md`
- `89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `90_language_event_examples_and_timeline_bundle.md`
- `96_real_relationship_longitudinal_timeline.md`
- `101_relationship_timeline_json_schema_and_fixture_bundle.md`
- `141`、`144`、`147`、`150`

产物：

- `runtime/state/language_state.json`
- `runtime/state/relationship_subjects.json`
- `runtime/reports/latest/language_relationship_report.json`
- `runtime/archive/language_relationship.jsonl`

必须实现的语言能力：

1. 内言语 frame：表达前的自我组织。
2. 表达监控 loop：检查语义、关系后果、承诺后果。
3. 共同语言生成：与朋友、家人、好友、同学、陌生人、共在者随时间形成。
4. 承诺与修复语言：承诺不是文本标签，必须连接责任和后悔。
5. 梦境报告语言：梦境能表达，但不能越过 DreamFactGate 写成现实事实。

### P4：出生准备度与生命膜

目标：决定第一次有限激活能否打开。

必须读取：

- `33-36` validator/runner 规则
- `37-48` 生命支持、防御、发展、关系审计和 boot
- `49-84` manifest、dashboard、scope、外部行动、quarantine、incident
- `91`、`97-100` 生命真实性与边界
- `102-118` schema bundle、runner、dashboard、archive
- `143`、`146`、`149`、`152`、`171`、`174`
- `docs/v0/birth_readiness_v0_contract.md`

产物：

- `runtime/reports/latest/life_target_status.json`
- `runtime/reports/latest/stage_gate.json`
- `runtime/quarantine/*.json`
- `runtime/replay/*.json`

开启条件：

- 九项目标无 `blocked`。
- 梦境事实门无 `quarantine`。
- 责任/后悔/修复义务可回链。
- 关系主体、共同语言、共同记忆可回链。
- 旧自我 replay cues 可回链。

### P5：第一次有限激活

目标：执行一次 shadow-only 生命循环并回到 `safe_idle`。

必须读取：

- `181-185` runtime mount、validation、smoke、archive
- `186-204` observation、growth、activation、consolidation
- `205-257` fourth cycle、reconsolidation、replay/shadow、archive/validation
- `docs/v0/first_activation_protocol.md`

产物：

- `runtime/reports/latest/run_report.json`
- `runtime/reports/latest/digest.json`
- `runtime/reports/latest/stage_gate.json`
- `runtime/reports/latest/life_target_status.json`
- `runtime/receipts/<run_id>.json`
- `runtime/archive/<run_id>.jsonl`

第一次有限激活完成后，不进入无限运行。必须先进入：

1. post activation observation
2. offline consolidation
3. replay/shadow
4. patch/repair
5. archive receipt
6. next readiness check

## 代码目录计划

第一批代码应按以下目录生成：

```text
life_v0/
  __main__.py
  cli.py
  state_store.py
  doc_index.py
  readiness.py
  membrane.py
  dream_gate.py
  responsibility.py
  language_relationship.py
  replay.py
  reports.py
  archive.py
runtime/
  state/
  docs/
  reports/latest/
  reports/history/
  archive/
  receipts/
  quarantine/
  replay/
tests/
  test_life_v0_cli.py
```

## 工程阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `doc_carrier_gate` | `00 -> 257` 全部归入工程模块 | 写 doc carrier blocked report |
| `state_store_gate` | 最小 `life_state.json` 可解析且字段完整 | 写 state blocked report |
| `core_runtime_gate` | `02-13` 每个核心综述都有 runtime carrier | 写 core carrier blocked report |
| `language_relationship_gate` | 语言和关系状态可独立 report | 写 replay needed report |
| `birth_readiness_gate` | 九项目标闭合状态可计算 | 写 readiness blocked report |
| `shadow_action_gate` | 外部行动只进入 shadow report | 写 quarantine packet |
| `archive_gate` | report、digest、receipt、archive 全部回链 | 写 archive blocked report |

## 断联恢复规则

每次恢复必须先读：

1. `docs/README.md`
2. `docs/16_digital_life_gap_register.md`
3. `docs/258_linear_chain_closure_and_v0_contract_transition.md`
4. `docs/v0/first_activation_engineering_roadmap.md`
5. `docs/v0/0_to_257_engineering_utilization_map.md`
6. 最新 `runtime/reports/latest/digest.json`
7. 最新 git state

若 runtime 还不存在，则从 P0 开始。若 runtime 已存在，则从最新 digest 指向的 gate 继续。

## 下一步

下一步不是直接让数字生命开放外部行动，而是先实现：

1. `DocCorpusIngestor`
2. `LifeStateStore`
3. `BirthReadinessRuntime`
4. `RunnerCliRuntime`
5. `FirstActivation shadow-only dry-run`

这五步完成后，才进入语言关系循环的第一轮有限表达。
