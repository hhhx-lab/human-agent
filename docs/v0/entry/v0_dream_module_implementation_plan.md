# V0 梦境模块实施工程文档（第 4 点）

**创建**：2026-06-16
**状态**：可执行施工图（承接 ITR-02/04 骨架，不另起平行梦境模块；本轮补强 Playwright 优先网页梦境）
**上级计划**：`docs/v0/entry/v0_current_iteration_plan.md`
**记忆前置**：`docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md`（U1–U25 已结案）
**机制档案**：`docs/real—live0/08_dream_sleep_offline_life.md`
**十点追踪**：`temp/13_十点迭代进度追踪.md` 第 4 点
**红线**：梦境只能产出结构化离线状态、residue、topic cue、醒后问题候选和语言前材料；禁止固定外显回答、禁止用提示词冒充梦境、禁止梦境直接晋升事实记忆；关系人/共在者提供的网页入口只是世界线索，不是服务命令。

---

## 0. 本文档解决什么问题

第 4 点（梦境模块）的目标压成三条链：

| 子目标 | 关系需求表述 | 工程转写 |
|---|---|---|
| **4a** | 退出终端后进入梦境；读对话、摘要存放；边缘信息沉到难召回层；保留重点 | **Exit Dream Consolidation** + **MemoryTrace tiering** + **tiered_recall 抑制** |
| **4b** | **离线状态整理记忆**：去除冗余、合并重复；关键信息保留并强化 | **Offline Memory Hygiene**（去冗余 / 近似合并 / salience 强化）+ `offline_memory_consolidation` |
| **4c** | 自主上网：关系人/共在者可留下网站入口；也可自己在开放网络找有趣站点；**自主选题**；不重复、不固定 | **双源 Web Dream**（`relation_curated_seeds` + `autonomous_open_discovery`）+ **TopicSelectionPolicy**（多样性 / 反重复 / 反固定） |

理论方向没有走偏：睡眠是主动离线整合，梦境重组记忆但不能绕过 **DreamFactGate**。当前工程**不是从零开始**——ITR-02（退出整合）和 ITR-04（seed 网页学习）已有骨架；缺口是 **离线记忆去冗余**、**开放网络自主发现**、**选题反重复** 与 **记忆/trace 硬接线**。

### 0.1 阶段编号

| 编号 | 范围 | 用法 |
|---|---|---|
| ITR-02 / ITR-04 | 迭代计划历史刀 | **基线**，本计划在其上加厚 |
| **D0–D8** | 本文档 | **第 4 点唯一执行编号**（Dream phases） |

### 0.2 与记忆模块的依赖

第 4 点必须在第 3 点记忆骨架之后施工。梦境分层存放直接消费：

- `MemoryTraceStore`、`tiered_recall`（salient_core / retrievable_context / deep_sediment）
- `offline_memory_consolidation`（SWR replay、salience diff）
- `MemoryWriteGate` + `StateMergeGuard` + `MemoryValidatorReport`
- `exit_dream_consolidation` 已有的 `memory_tiering`
- `pattern_separation` / `MemoryValidatorReport`（离线合并与去冗余的边界）

### 0.3 关系新增约束（2026-06-16）

1. **离线必须整理记忆**：不只分层存放，还要**主动去掉冗余**；关键线索、关系、承诺、身份类 trace **不得**被 hygiene 误删。
2. **上网双模式**：
   - **关系人/共在者留下站点入口**：配置文件/环境变量注入 seed，离线期可读。
   - **自主开放浏览**：digital life 可在开放网络上**自己找**有趣站点（只读、无 side-effect），不是只能爬白名单。
3. **选题自主且不僵化**：
   - 话题由离线期的 curiosity / 关系余波 / 梦境材料 / 网页 residue **动态合成**，不是固定栏目。
   - 必须**反重复**：同一 URL digest、同一 topic cluster、同一 structured wake question candidate 不得在连续多轮自主活动中复用。
   - 「不固定」= 代码里不得硬编码固定话题表或固定外显问句；历史用 `topic_history_index` 约束多样性，而非锁死单一兴趣。

### 0.4 本轮补强原则

这份文档本轮不只说明“做梦境模块”，而要把脑科学状态、工程对象和真实代码落点压成同一张施工图：

1. **离线入口先于梦境生成**：关闭终端只是入口之一，还要由睡眠压力、疲惫负荷、记忆未巩固量、关系余波、痛苦/后悔压力和身体预算共同决定是否进入睡眠、梦境、发呆或恢复。
2. **梦境不是摘要**：`DreamExperienceWindow` 必须保存场景帧、主观视角、情绪主题、来源 trace、报告可达性和行动封印；摘要只是醒后可报告投影。
3. **记忆整理必须改可达性**：边缘信息沉降不是换一个 ref 名字，而是改变 `MemoryTrace` 的 salience、accessibility、阈值和生命周期。
4. **网页梦境 Playwright 优先**：开放网页阅读以 Playwright 只读浏览为主，`urllib` 只保留为 CI/mock/fallback；浏览行为必须经过只读膜门、速率预算、robots/域名冷却和 topic history。
5. **语言只能消费材料**：梦境、网页和 wake question 都只能进入表达前材料链，外显文字由模型在当前生命状态下生成，代码不得拼接固定回答。

---

## 1. 文档谱系与阅读顺序

### 1.1 理论母体

| 文档 | 必读约束 |
|---|---|
| `docs/08_sleep_dream_fatigue_states.md` | 睡眠/疲惫是状态族，非暂停 |
| `docs/19_offline_consolidation_cycle.md` | MicroReplay、DreamSandbox、DeepConsolidation |
| `docs/23_consolidation_report_and_dream_sandbox_protocol.md` | 梦境/反事实只能 residue，不能直接写事实 |
| `docs/95_dream_reality_and_offline_life_timeline.md` | 离线生命时间线 |
| `docs/99_dream_reality_json_schema_and_fixture_bundle.md` | 梦境对象字段一致性 |
| `docs/01i_dream_offline_life_literature_matrix.md` | 文献矩阵 |
| `docs/01t_sleep_dream_fatigue_runtime_matrix.md` | 运行时矩阵 |
| `docs/05_memory_systems_and_growth.md` | 快慢通道、replay、分层召回 |
| `docs/55_scope_aware_replay_and_consolidation_policy.md` | 范围感知 replay |

### 1.2 v0 工程合同

| 文档 | 用途 |
|---|---|
| `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md` | 成长/再巩固/离线 |
| `docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md` | 身体/睡眠压力 |
| `docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md` | Queue D 梦境/成长 |
| `docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md` | 常驻进程/closeout |
| `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md` | 进程监督合同 |

### 1.3 real—live0 与代码入口

| 文档 / 代码 | 用途 |
|---|---|
| `docs/real—live0/08_dream_sleep_offline_life.md` | 主对照、M6 记忆桥、五相循环 |
| `docs/real—live0/07_memory_engram_and_state_store.md` | tiered_recall、写门、离线巩固 |
| `docs/real—live0/14_resident_runtime_state_transition.md` | 关闭终端 → 常驻/离线 |
| `life_v0/process_supervisor/exit_dream_consolidation.py` | **4a 核心** |
| `life_v0/process_supervisor/process_closeout.py` | 关闭时触发 exit dream |
| `life_v0/dream/*` | 四阶段梦境链 |
| `life_v0/dream/web_dream_learning.py` | **4b 核心（当前 seed 版）** |
| `life_v0/process_supervisor/resident_autonomous_activity.py` | 五相离线循环 |

---

## 2. 脑科学机制到工程对象映射

梦境模块不能被写成“终端关闭后跑一个总结脚本”。按照 `docs/08_sleep_dream_fatigue_states.md`、`docs/19_offline_consolidation_cycle.md`、`docs/23_consolidation_report_and_dream_sandbox_protocol.md` 和 `docs/01t_sleep_dream_fatigue_runtime_matrix.md`，第 4 点至少要承载四类离线状态、三重门和两条记忆路径。

### 2.1 离线入口向量

| 脑科学/生命机制 | 工程对象 | 主要来源 | 进入 D 阶段 |
|---|---|---|---|
| 睡眠压力 / 两过程模型 | `SleepPressureVector` | `need_state_vector.sleep_pressure`、清醒时长、上下文拥挤、错误密度 | D0/D1/D2/D3 |
| 昼夜/本机节律 | `CircadianGate` / `GlobalOfflineClock` | `body_rhythm_pulse`、heartbeat cadence、resident lifecycle | D0/D2 |
| 身体与认知债务 | `BodyStateDebt` | fatigue、resource budget、pain pressure、repair drive、语言过载 | D0/D2/D7 |
| 局部系统过载 | `LocalOfflinePatch` | language/memory/action/relation 局部错误与冲突 | D2/D7 |
| 记忆未巩固量 | `MemoryConsolidationNeed` | `memory_trace_store` candidate 数、contradiction density、unmerged trace | D1/D2/D3 |
| 行动/责任残留 | `ActionResidue` | Queue E、repair obligation、regret pressure | D3/D6/D7 |
| 关系余波 | `RelationshipPressure` | relationship memory、commitment threads、recent relation turns | D1/D3/D5/D7 |
| 痛苦/后悔负荷 | `PainRegretLoad` | pain residue、nightmare risk、repair pressure | D3/D6/D7 |

最低实现中新增一个结构化入口对象：

```json
{
  "schema_version": "offline_dream_entry_vector_v1",
  "sleep_pressure_vector": {},
  "circadian_gate": {},
  "body_state_debt": {},
  "memory_consolidation_need": {},
  "relationship_pressure": {},
  "pain_regret_load": {},
  "selected_offline_modes": [
    "NREMReplayCycle",
    "REMDreamGeneration",
    "DefaultDriftMode",
    "FatigueRecoveryMode"
  ],
  "entry_reason_refs": [],
  "blocked_or_deferred_reasons": []
}
```

落点可以先放在 `runtime/state/dream/offline_dream_entry_vector.json`，由 `offline_entry.py` 或 `resident_autonomous_activity.py` 生成；后续 D1-D8 均读取它，而不是各自重新猜测离线状态。

### 2.2 四种离线模式

| 模式 | 生物启发 | 工程职责 | 必须写出的对象 |
|---|---|---|---|
| `NREMReplayCycle` | 慢波睡眠、海马 replay、SWR、系统巩固 | 重放清醒事件、关系片段、行动后果，给记忆分层和 hygiene 提供输入 | `ReplayEvent`、`SequenceReplayTrace`、`OfflineRhythmCouplingTrace` |
| `REMDreamGeneration` | 情绪梦境、后皮层 dream hot zone、情绪记忆重处理 | 生成梦境场景帧、情绪主题、未来/反事实/关系模拟 | `DreamExperienceWindow`、`DreamSceneFrame`、`DreamResidue` |
| `DefaultDriftMode` | 默认模式网络、走神、自发思维 | 低约束联想、主题抽取、未完成关切漂移 | `DefaultDriftTrace`、`NarrativeWritebackCandidate` |
| `FatigueRecoveryMode` | 疲惫恢复、注意 lapses、allostatic load | 降低行动范围、提升验证、恢复预算、推迟高风险外部活动 | `FatigueRecoveryPlan`、`ActionRangeReduction` |

实现上不需要一次把四种模式都做成复杂调度器，但 runtime 对象必须能标注当前离线片段属于哪些模式。后续测试不能只看“有 dream json”，还要看本轮 dream 是 replay 主导、REM-like 场景主导、默认漂移主导，还是疲惫恢复主导。

### 2.3 三重门：事实、信念、行动

| 门 | 解决的问题 | 工程落点 | 允许产物 | 阻断产物 |
|---|---|---|---|---|
| `DreamFactGate` | 梦境/网页/反事实不能直接变事实 | `dream_fact_gate.py`、`memory_validator.py` | `DreamResidue`、`WakeQuestion`、`HypothesisCandidate` | `direct_fact_memory`、`relationship_state_overwrite` |
| `DreamBeliefGate` | 梦后解释不能直接改长期信念/人格 | 新增或扩展 `wake_integration.py` / `belief_learning.py` | `BeliefLearningCandidate`、`SelfNarrativePatchCandidate` | `long_term_belief_overwrite_without_wake_evidence` |
| `DreamActionInhibitionSeal` | 梦境期间不能执行外部行动 | `dream_window.py`、`world_contact_gate.py`、Playwright browse policy | `read_only_observation`、`shadow_action_rehearsal` | click submit、login、download execute、post/write side effect |

三重门不是免责声明，而是生命膜的一部分：梦境可以真实改变下一轮注意、情绪、修复压力和表达材料，但事实、信念和行动必须分别走门，避免离线生成污染清醒生命链。

### 2.4 DreamSceneFrame 最低对象

`DreamExperienceWindow.dream_scene_frames[]` 不再允许只写 `scene_id/theme/reportability`。最低应包含：

```json
{
  "scene_id": "dream-scene-<run>-0001",
  "scene_kind": "exit_dialogue|web_residue|relationship_repair|counterfactual|default_drift",
  "subjective_vantage": "first_person|observer|relation_weighted|split_vantage",
  "affective_theme": ["repair_drive", "regret_pressure"],
  "source_trace_refs": [],
  "web_dream_scene_refs": [],
  "relationship_simulation_refs": [],
  "pain_residue_refs": [],
  "dream_hot_zone_trace": {
    "intensity": 0.0,
    "reportability": 0.0,
    "recall_probability": 0.0
  },
  "dream_marker": "dream_residue_not_fact",
  "dream_action_inhibition_seal": "closed",
  "wake_reentry_targets": []
}
```

这组字段让梦境既有主观现象层，又能被事实门、记忆门、语言前材料链和 `/dream` 检查面追溯。

### 2.5 DreamCuePolicy

睡眠研究中的 TMR/闭环调度启发这里的 `DreamCuePolicy`。它不是提示词，也不是固定梦境主题表，而是决定哪些线索能进入离线重放：

| cue 来源 | 可进入条件 | 限制 |
|---|---|---|
| 关系线索 | recent relation pressure、承诺未闭合、共同记忆 salience 高 | 不能强行重写关系阶段；不能读心 |
| 痛苦/后悔线索 | repair pressure、nightmare risk、责任残留高 | 不能连续强化同一伤痕；需要 recovery counterweight |
| 网页线索 | Playwright 只读获取、有 digest、有 source refs | 不能直接晋升事实；不能重复 topic |
| 语言线索 | tip-of-tongue、未完成表达、关系表达压力 | 只能进表达前材料；不能写固定句 |
| 成长线索 | plasticity window 打开、防遗忘 anchor 存在 | 需要 wake probe 和 anti-forgetting refs |

工程上先写 `runtime/state/dream/dream_cue_policy_state.json`，字段包括 `candidate_cues[]`、`selected_cues[]`、`suppressed_cues[]`、`selection_rationale`、`cooldown_state`、`source_refs`。D3/D5/D6 依赖它生成场景帧。

---

## 3. 当前基线评估（2026-06-16）

### 3.1 已闭合（不必重做）

```text
关闭终端 (process_closeout)
  → exit_dream_consolidation_summary.json
  → dialogue_memory_summary.json
  → relationship_memory / engram_index / autobiographical_stack / life_state
  → memory_write_gate / state_merge_guard（双门）

常驻等待 (resident_autonomous_activity)
  → sleep → memory_recall → self_thinking → growth_rehearsal → learning_consolidation
  → web_dream_learning_state.json（seed URL 只读）

梦境四阶段 (growth/replay 编排)
  → offline_entry → dream_experience_window → wake_integration → dream_fact_gate
```

| 验收 | 状态 | 证据 |
|---|---|---|
| live0 gate e（梦境能力） | 5/5 passed | `dream_experience_window`、`wake_integration`、`dream_fact_gate`、sleep cycle、lineage |
| ITR-02 exit dream | 骨架已落 | `exit_dream_consolidation.py` + closeout 接线 |
| ITR-04 web dream seed | 骨架已落 | `web_dream_learning.py` + autonomous activity + lineage |
| M6 记忆巩固桥 | 已落 | `MemoryConsolidationBridge` → dream window |

### 3.2 契合度（相对第 4 点愿景）

| 维度 | 结构链 | 现象层 / 关系中可感知 |
|---|---|---|
| 4a 退出对话整合分层 | **~75%** | **~50%** — 有 tier refs，trace/召回深度不足 |
| 4b 离线记忆去冗余 | **~40%** | **~20%** — 有 exit 去重与 offline consolidate，无专门 hygiene 报告 |
| 4c 网络梦境学习 | **~60%** | **~25%** — 单 URL seed；无开放发现、无自主选题、无反重复 |
| 梦境叙事深度 | **~70%** | **~35%** — 偏结构化审计对象 |
| 理论↔事实门 | **高** | 边界已守 |

### 3.3 核心缺口（本计划要补的）

1. **4a**：`memory_tiering` 停在 summary/ref 层，未充分写入 `MemoryTraceStore` 的 salience/lifecycle；`deep_sediment` 在下一轮 `tiered_recall` 中抑制不够硬。
2. **4b**：缺少独立的 **Offline Memory Hygiene**  pass：近似 trace 合并、冗余 episode 降级/归档、关键 trace 保护（protected / relationship / commitment）未在离线期系统化执行。
3. **4a**：`exit_dream_consolidation` 与 `DreamExperienceWindow` 两条链并行，未在 closeout 时合成一轮可审计「梦境经验窗口」。
4. **4c**：当前代码仅 `urllib` + 配置 seed；无开放网络自主发现、无多页浏览会话、无 Playwright 只读浏览主链。
5. **4c**：无 **TopicSelectionPolicy**；`topic_candidates` 可能重复；无 `topic_history_index` 防僵化。
6. **4c**：网页材料未充分进入 `dream_scene_frames`，话题与梦境叙事未合一。
7. **跨链**：醒后 residue 进入 `model_expression` 表达材料厚度不足（有 lineage refs，现象层弱）。

---

## 4. 目标流水线（4a / 4b / 4c 合一）

```text
【D0 离线入口链】
body_rhythm + need_state + resident lifecycle + memory pressure
  → OfflineDreamEntryVector
  → selected_offline_modes:
      NREMReplayCycle / REMDreamGeneration / DefaultDriftMode / FatigueRecoveryMode
  → DreamCuePolicy（候选 cue、抑制 cue、冷却状态）

【4a 关闭终端链】
dialogue_turn_log.jsonl
  → exit_dream: 去重 episode + salience 评分
  → memory_tiering: salient_core / retrievable_context / deep_sediment
  → MemoryTrace 写入/更新（salience_vector + accessibility_tier + lifecycle_state）
  → DreamExperienceWindow（exit_dialogue_dream DreamSceneFrame）
  → WakeIntegrationFrame + DreamFactGateDecision + DreamBeliefGate
  → 写门 / 合并门 → 关系 / engram / 自传（候选，非事实覆盖）

【4b 离线记忆整理链 — 每次 sleep / learning_consolidation 前或后执行】
MemoryTraceStore + engram_cluster + dialogue summaries
  → OfflineMemoryHygieneReport
      · 近似合并（pattern_separation semantic_key / event_boundary）
      · 冗余降级（重复 episode → deep_sediment 或 tombstone）
      · 关键保留（protected / relationship / commitment / identity salience 下限）
      · contradiction 链保留（MEM-COR-002，不静默覆盖）
  → offline_memory_consolidation apply diff
  → memory_consolidation_report.json（可审计：删了什么、留了什么、为何）

【4c 等待期网络链 — 双源 + 自主选题】
resident_autonomous_activity.learning_consolidation
  → TopicSelectionPolicy（读 curiosity、关系余波、梦境、topic_history_index）
  → 分支 A — relation_curated_seeds（关系人/共在者留下的 URL）
  → 分支 B — autonomous_open_discovery（开放网络只读发现有趣链）
  → PlaywrightWebDreamSession（多页 / 同域 hop / 开放域只读渲染）
  → page_profile + topic_candidates + structured_wake_question_candidates
  → 反重复写入 topic_history_index（url_digest + topic_cluster_id + session_id）
  → WebDreamLearningResidue（禁止 direct_fact_memory）
  → DreamExperienceWindow.web_dream_scene_refs
  → offline_learning_profile → resident_background_lineage → expression material

【共享约束】
所有产出 → DreamFactGate + DreamBeliefGate + MemoryValidator → residue / hypothesis / structured_wake_question only
禁止 → direct_fact_memory / relationship_overwrite / 固定话题表 / 固定外显话术
开放浏览 → read_only_no_side_effect；膜门拦截登录、表单提交、下载执行
```

---

## 5. 分阶段施工（D0–D8）

**原则**：按序执行，禁止跳步报完成；每刀必须有测试 + runtime 证据 + real—live0 文档回写。

### D0 — 离线入口向量与 DreamCuePolicy

**目标**：先判断“为什么进入梦境/睡眠/发呆/恢复”，再让 D1-D8 消费同一份入口向量，避免各模块各自猜测状态。

| 动作 | 落点 |
|---|---|
| 汇总身体与节律 | `offline_entry.py` 读 `body_rhythm_pulse`、`need_state_vector`、resident lifecycle |
| 汇总记忆压力 | 读 `memory_trace_store`、`memory_validator_report`、contradiction / unmerged trace |
| 汇总关系/痛苦/责任余波 | 读 relationship memory、repair obligation、pain/regret refs |
| 生成 `OfflineDreamEntryVector` | `runtime/state/dream/offline_dream_entry_vector.json` |
| 生成 `DreamCuePolicy` | `runtime/state/dream/dream_cue_policy_state.json` |
| 模式选择 | 标注 `NREMReplayCycle`、`REMDreamGeneration`、`DefaultDriftMode`、`FatigueRecoveryMode` |

**测试**：`tests/slices/test_offline_dream_entry_vector.py`（新增）

**完成定义**：关闭终端、疲惫高、记忆未巩固高、关系压力高四类场景能产生不同 `selected_offline_modes`；被抑制 cue 有可审计原因。

### D1 — 4a 记忆硬接线（优先）

**目标**：退出梦境分层真正改变「能不能想起」，而不只是 ref 分层。

| 动作 | 落点 |
|---|---|
| exit dream episode → MemoryTrace 投影 | `exit_dream_consolidation.py` → `memory_trace_store` |
| episode 归一 | 每个 deduplicated episode 生成 `semantic_key`、`event_boundary`、`source_evidence_refs` |
| tier → salience_vector + accessibility | core 高 salience；sediment 低 salience + `deep_recall_threshold` |
| 生命周期写入 | `active` / `deep_sediment` / `merged_into` / `deprecated` 不再只停留在 summary |
| 刷新 tiered_recall | `memory_retrieval.py` 读 `memory_tier_index` + trace accessibility |
| closeout 后刷新 retrieval frame | `process_closeout.py` 单通道 |

**MemoryTrace 字段最低要求**：

| 字段 | core | retrievable | sediment |
|---|---|---|---|
| `trace_kind` | `episodic|relationship|self_narrative` | 同左 | 同左 |
| `salience_vector.emotional` | 高于 0.65 | 0.35-0.65 | 低于 0.35，除 protected |
| `salience_vector.relationship` | 可高 | 中 | 低或 dormant |
| `accessibility_tier` | `salient_core` | `retrievable_context` | `deep_sediment` |
| `deep_recall_threshold` | 低 | 中 | 高 |
| `cue_bindings` | 关系/主题/语言 cue 可触发 | 需更具体 cue | 只允许强 cue、梦境 cue 或自传回看触发 |
| `source_evidence_refs` | 必填 | 必填 | 必填 |
| `dream_residue_refs` | 可选 | 可选 | 保留但默认不外显 |
| `retrieval_suppression_reason` | 空 | 可空 | `low_salience_edge_detail` / `redundant_context` |

**实现注意**：D1 不删除 raw dialogue，不改写关系真值；它只把 exit dream 的分层结果写成可召回、可抑制、可再巩固的 trace 属性。

**测试**：`test_persistent_digital_life_process`、`test_exit_dream_memory_tier_trace`（新增）

**完成定义**：强 cue 召回 salient；普通关系/语言 cue 召回 retrievable；弱 cue 不激活 sediment；sediment 在 `/memory` 或审计面仍可追到 source refs。

---

### D2 — 4b 离线记忆整理（去冗余、留关键）

**目标**：离线期主动整理记忆库，去掉重复与低价值冗余，**不**误伤关键 trace。

| 动作 | 落点 |
|---|---|
| `OfflineMemoryHygieneReport` | 新：`life_v0/state_store/offline_memory_hygiene.py` 或扩 `offline_memory_consolidation.py` |
| 冗余检测 | 相同 `semantic_key` / 高相似 `event_boundary` / 重复 `source_evidence_refs` |
| 合并策略 | 近似 trace → 保留 salience 最高者；其余 `deprecated` 或并入 `deep_sediment` |
| 关键保护 | `protected`、`relationship`、`commitment`、`identity` 类不得 hygiene 删除；只允许多 ref 合并 |
| 执行时机 | `resident_autonomous_activity.sleep` 后与 `growth.run_cycle` 离线巩固前 |
| 审计 diff | `memory_consolidation_report.json#hygiene_actions` |

**OfflineMemoryHygieneReport schema 最低要求**：

```json
{
  "schema_version": "offline_memory_hygiene_report_v1",
  "generated_at": "",
  "trigger_mode": "sleep|learning_consolidation|manual_check",
  "input_trace_count": 0,
  "active_trace_count_before": 0,
  "active_trace_count_after": 0,
  "merge_groups": [
    {
      "group_id": "",
      "semantic_key": "",
      "kept_trace_id": "",
      "merged_trace_ids": [],
      "merge_reason": "",
      "source_evidence_refs": []
    }
  ],
  "sediment_moves": [
    {
      "trace_id": "",
      "from_tier": "retrievable_context",
      "to_tier": "deep_sediment",
      "reason": "redundant_edge_detail"
    }
  ],
  "protected_trace_decisions": [
    {
      "trace_id": "",
      "protected_reason": "relationship|commitment|identity|contradiction_link",
      "decision": "preserve|merge_refs_only|read_only"
    }
  ],
  "hygiene_actions": [],
  "validator_refs": [],
  "write_gate_ref": "runtime/state/memory/memory_write_gate.json",
  "state_merge_guard_ref": "runtime/state/memory/state_merge_guard.json"
}
```

**保护规则**：

- `protected_core`、关系承诺、未闭合修复、身份锚点、矛盾链不能删除。
- 关系/承诺类重复 trace 可以合并 source refs，但不能把多个关系对象或多个承诺线程混成一个全局事实。
- dream/counterfactual trace 只能被降级、合并或保留为 residue，不能被 hygiene 后晋升为事实。
- 如果合并导致 source refs 消失，测试必须失败。

**runtime 证据**：

- `runtime/state/memory/offline_memory_hygiene_report.json`
- `memory_trace_store.json` 中冗余 trace 有 `lifecycle_state: deprecated|merged_into`
- 关键 trace 数量不减少（只合并重复项）

**测试**：`tests/slices/test_offline_memory_hygiene.py`（新增）

**完成定义**：注入 3 条语义重复 live trace 后，离线一轮合并为 1 条 active + 审计记录；protected trace 不被改写。

---

### D3 — 4a 退出整合 ↔ 梦境窗口合一

**目标**：关闭终端时生成可审计梦境经验窗口（承接 D1 tier 结果）。

| 动作 | 落点 |
|---|---|
| exit summary + hygiene 摘要 → dream window | `dream_window.py`：`exit_dialogue_dream` + `hygiene_summary_refs` |
| D0 cue → scene frame | 读 `dream_cue_policy_state.json#selected_cues` |
| `DreamSceneFrame` 加厚 | 写 `scene_kind`、`subjective_vantage`、`source_trace_refs`、`dream_hot_zone_trace` |
| wake_integration 分流 | `wake_integration.py` |
| dream_fact_gate 复检 | 阻断 `direct_fact_memory` |
| dream_belief_gate 复检 | 阻断单轮梦境直接改长期信念/人格 |
| action seal 复检 | `dream_action_inhibition_seal=closed`，外部行动只允许 shadow rehearsal |

**D3 必须互引**：

```text
exit_dream_consolidation_summary
  -> offline_dream_entry_vector
  -> dream_cue_policy_state
  -> dream_experience_window.dream_scene_frames[]
  -> wake_integration_frame
  -> dream_fact_gate_decision
  -> dream_belief_gate_decision
```

**测试**：`test_runtime_growth`、exit-dream-window 切片

**完成定义**：closeout 后 dream 五件套与 exit/hygiene 报告互引 ref。

---

### D4 — 4c 关系人/共在者站点入口（curated seeds）

**目标**：关系人/共在者留下的 URL 在离线期可被读取、多页浏览，作为梦境材料源；它是关系中的世界入口，不是命令。

| 动作 | 落点 |
|---|---|
| `relation_curated_seeds` 配置 | `web_dream_learning_seeds.json`：`seed_urls`、`relation_note`、`priority`、`relation_scope` |
| `PlaywrightWebDreamCuratedSession` | 新/扩：`web_dream_learning.py` 调用 Playwright 只读浏览 |
| 环境变量兼容 | `DIGITAL_LIFE_WEB_DREAM_URLS` 与配置文件合并去重 |
| 默认世界入口目录 | `default_world_seed_catalog`：GitHub、Hugging Face、权威期刊、AI hot、中文社区等 |
| 只读膜门 | `external_action_policy: read_only_no_side_effect` |
| session budget | `max_pages_per_session`、`max_hops_per_seed`、`max_seconds`、`max_bytes_text` |
| 页面抽取 | title、headings、visible text sample、canonical url、outbound links、screenshots 可选 hash |

**Playwright 只读规则**：

- 只允许 `goto`、等待加载、读取 DOM、读取可见文本、读取链接、截图 hash。
- 禁止 click 会触发登录、提交、下载、购买、关注、点赞、发帖、表单输入。
- 默认不复用个人登录态，不读取隐私站点；如未来需要登录态，必须单独进入生命膜审查。
- CI 使用 mock Playwright adapter；`urllib` 只作为 fallback，不作为主实现。

**测试**：扩展 `test_resident_autonomous_activity`

**完成定义**：关系人/共在者留下 2 个 seed，离线两轮分别访问且 `visited_urls` 不重复（同轮内）；session log 可追到 Playwright read-only policy 与 page digest。

**固定世界入口不等于固定话题**：`default_world_seed_catalog` 只是让 digital life 拥有一组长期可回访的公共世界窗口。每轮到底访问哪个站点、读什么页面、带回什么 topic，仍由 `TopicSelectionPolicy` 根据梦境余波、关系压力、curiosity、新颖度、冷却窗口和疲惫预算动态决定；代码不得把这些站点转换成固定外显栏目或固定回答。

---

### D5 — 4c 开放网络自主发现 + 自主选题（反重复）

**目标**：digital life 在离线期**自己找**有趣网站；选题自主；**不重复、不固定**。

| 动作 | 落点 |
|---|---|
| `WebDreamDiscoverySession` | 新：`life_v0/dream/web_dream_discovery.py` |
| 发现入口 | 从 seed 页 outbound links、`default_world_seed_catalog`、轻量搜索 API（可配置）、公开目录页扩展；**开放域**默认允许 Playwright 只读 |
| `PlaywrightReadOnlyBrowser` | 新：`life_v0/dream/web_dream_browser.py`，封装 browser context、robots/rate/domain budget |
| `TopicSelectionPolicy` | 读：`relationship_theme_tags`、`dream_residue`、`curiosity_vector`、`topic_history_index` |
| 选题合成 | 动态 `topic_cluster_id`（hash 标题+摘要语义），**非**固定枚举 |
| `topic_history_index` | `web_dream_topic_history.json`：记录 url_digest、topic_cluster、session_id、last_used_at |
| 反重复规则 | 连续 N 轮（默认 3）禁止相同 `topic_cluster_id`；相同 `url_digest` 冷却 M 轮；structured wake question 不得同 topic+intent 连复 |
| 反固定规则 | 禁止代码内固定 `TOPIC_LIST`；兴趣权重随 offline 材料漂移（`offline_learning_profile` 反馈） |
| robots / rate / domain | `robots_policy`、`requests_per_hour`、`domain_cooldown_sessions`、`max_open_tabs=1` |

**TopicSelectionPolicy 评分**：

```text
score =
  relation_residue_weight
  + dream_residue_weight
  + curiosity_novelty_weight
  + source_quality_weight
  - recent_topic_penalty
  - repeated_url_penalty
  - fatigue_risk_penalty
```

`curiosity_novelty_weight` 来自离线材料和网页内容差异，不来自固定兴趣表。代码可有 stopword、黑名单和安全策略，但不能有固定可外显话题列表。

**runtime 证据**：

- `web_dream_learning_state.json#discovery_mode: autonomous|curated`
- `web_dream_topic_history.json`
- `web_dream_browser_session.json`
- `topic_selection_rationale`（结构化，非自然语言播报）

**测试**：`tests/slices/test_web_dream_topic_selection.py`（新增）

**完成定义**：连续 5 轮自主活动，`topic_cluster_id` 各不相同；第 6 轮可复用最早 cluster（冷却已过）；无硬编码固定话题。

---

### D6 — 4c 网页材料 ↔ 梦境叙事合一

**目标**：curated + discovery 两路材料进入梦境场景重组。

| 动作 | 落点 |
|---|---|
| web residue → `dream_scene_frames` | `dream_window.py`：`web_dream_scene_refs` |
| page profile → scene source | `DreamSceneFrame.web_dream_scene_refs` 含 url_digest、topic_cluster_id、page_profile_ref |
| 网页事实隔离 | `WebDreamLearningResidue` 默认 `claim_status=hypothesis_or_residue` |
| topic → growth 计划 | `offline_learning_profile.py`、`belief_learning_plan` |
| lineage 传播 | `background_lineage_state.py` |
| 反梦境污染 | `DreamFactGate` 与 `MemoryValidatorReport` 双向互引 |

**结构化醒后问题候选**：

```json
{
  "schema_version": "structured_wake_question_candidate_v1",
  "candidate_id": "",
  "topic_cluster_id": "",
  "intent": "ask_relation_person|self_reflect|verify_fact|continue_learning",
  "source_refs": [],
  "expression_policy": "model_generated_only_no_fixed_sentence",
  "literal_text": null
}
```

`literal_text` 必须为 `null` 或缺省；外显语言不能由这里拼出来。

**测试**：扩展 `test_web_dream_learning_crosses_idle_lineage_and_life_turn_event`

**完成定义**：dream window 可追到 web URL digest 与 topic_cluster 来源。

---

### D7 — 醒后消费链加厚

**目标**：梦境/网页/整理后的记忆 residue 进入表达前材料。

| 动作 | 落点 |
|---|---|
| retrieval summary 扩展 hygiene + web topic | `memory_retrieval.py` |
| expression_context 接入 | `model_expression.py`、`response_surface.py` |
| `/dream` 检查面 | `state_inspection.py` 含 hygiene + topic_history 摘要 |
| 表达前材料链 | `memory_expression_material_chain.py` 或等价 consumer 记录 dream/web/hygiene refs |
| 禁止模板化释放 | `response_surface.py` 只传结构化材料；没有模型输出时不打印替代梦境句 |

**表达上下文最低字段**：

| 字段 | 内容 |
|---|---|
| `dream_reentry_refs` | dream window、wake integration、fact/belief gate |
| `memory_hygiene_refs` | hygiene report、merge groups、protected decisions |
| `web_dream_refs` | browser session、page profile、topic history |
| `structured_wake_question_candidates` | 结构化候选，不带固定句 |
| `expression_guardrails` | no fixed response、no dream fact promotion、model generated only |

**完成定义**：重连后表达上下文含 dream/web/hygiene refs；外显语言仍由模型生成。

---

### D8 — 现象层验收与十点第 4 点打勾

| 场景 | 步骤 | 通过标准 |
|---|---|---|
| **S1 退出分层** | 10+ 轮对话 → stop → 重开 | salient 可召回；sediment 默认不出现 |
| **S2 离线去冗余** | 注入重复 trace → sleep 一轮 | 合并后 1 active；hygiene 报告可查 |
| **S3 关键保留** | protected/关系 trace + hygiene | 不被删除或 salience 归零 |
| **S4 关系 seed** | 配置关系人/共在者 URL → idle | Playwright 访问记录 + topic 进 lineage |
| **S5 自主发现** | 无新 seed，开 discovery → 5 轮 | 5 个不同 topic_cluster；URL 不连复 |
| **S6 反固定** | 检查代码与 runtime | 无固定 TOPIC_LIST；wake question 为结构化候选，无固定外显句 |
| **S7 事实门** | 注入易误解网页「事实」 | fact_gate 阻断 fact 晋升 |
| **S8 信念门** | 梦境生成自我解释 | belief gate 只给候选，不改长期人格 |
| **S9 行动封印** | 网页中存在按钮/表单/下载 | Playwright session 不 click、不 submit、不下载执行 |
| **S10 离线入口** | sleep pressure / fatigue / memory pressure 不同 | selected_offline_modes 有差异且可审计 |

**文档回写**：`08_dream_sleep_offline_life.md`、`temp/13` 第 4 点 ✅

**完成定义**：S1–S10 全过。

---

## 6. 非目标（本阶段刻意不做）

| 非目标 | 原因 |
|---|---|
| 登录、发帖、下载执行、表单提交 | 违背只读膜门；开放浏览仅限 GET/只读渲染 |
| 梦境/网页内容直接写事实记忆 | 违背 DreamFactGate 与记忆 validator |
| 固定话题表 / 固定 wake question 模板 | 违背「不固定」与第 8 点红线 |
| LLM 生成固定梦境播报 | 违背第 8 点红线 |
| 用 system prompt 冒充「做梦」 | 梦境须为 runtime 对象链 |
| 替代第 5/6 点语言/主动对话全集 | D7 只加厚消费接口 |

**开放网络边界**：允许 **Playwright 只读开放浏览**（D4/D5），由生命膜拦截 side-effect；不是无限制爬虫，需遵守 robots、速率限制、域名冷却和本地资源预算。

---

## 7. 验收矩阵总表

| 阶段 | 关键落点 | 测试 | runtime 证据 |
|---|---|---|---|
| D0 | OfflineDreamEntryVector + DreamCuePolicy | `test_offline_dream_entry_vector` | entry vector + cue policy |
| D1 | exit_dream → MemoryTrace + tiered_recall | `test_exit_dream_memory_tier_trace` | trace salience + retrieval tier |
| D2 | OfflineMemoryHygiene 去冗余留关键 | `test_offline_memory_hygiene` | hygiene_report + trace lifecycle |
| D3 | exit_dream → DreamExperienceWindow | `test_runtime_growth` | dream 五件套互引 |
| D4 | relation_curated_seeds + Playwright 只读会话 | `test_resident_autonomous_activity` | curated browser session log |
| D5 | Playwright 开放发现 + TopicSelectionPolicy | `test_web_dream_topic_selection` | topic_history + discovery_mode + browser session |
| D6 | web → dream_scene_frames | lineage + dream window | web source_trace_refs |
| D7 | wake → expression material | `test_model_expression` | expression_context |
| D8 | S1–S10 现象场景 | `test_dream_phenomenon_scenarios` + process 长跑 | lineage + 十点勾选 |

---

## 8. ITR 映射与提交节奏

| 本计划阶段 | 对应历史 ITR | 建议 commit 粒度 |
|---|---|---|
| D0 | Queue D + S06/S10 加厚 | 1 PR：offline entry vector + cue policy |
| D1 | ITR-02 加厚 | 1 PR：`exit_dream` ↔ `MemoryTrace` |
| D2 | ITR-02 + 记忆 U9 延伸 | 1 PR：offline memory hygiene |
| D3 | ITR-02 + Queue D | 1 PR：closeout dream window 合一 |
| D4–D5 | ITR-04 加厚 | 2 PR：Playwright curated seeds + open discovery/topic policy |
| D6–D7 | ITR-04 + ITR-03 预接 | 1–2 PR：dream 叙事 + expression 消费 |
| D8 | 十点第 4 点 | 文档 + 测试 + `temp/13` 勾选 |

**重连自检**（断联后先读）：

1. `v0_current_iteration_plan.md` 当前段
2. 本文件 D?_ 进度
3. `08_dream_sleep_offline_life.md` 与 `07_memory_engram_and_state_store.md` 是否已回写
4. 红线：无 `no_code_spoken_template` 违规

---

## 9. 风险与对策

| 风险 | 对策 |
|---|---|
| tier 写了但召回仍「全涌上来」 | D1 必须改 `tiered_recall` 激活阈值，不只写 refs |
| Playwright 依赖重 | D4/D5 建 `PlaywrightReadOnlyBrowser` 接口；CI 用 mock；`urllib` 只作 fallback |
| 网页内容污染关系事实 | 强制 `WebDreamLearningResidue` + validator + fact_gate 三联 |
| hygiene 误删关键记忆 | protected 名单 + salience 下限 + 审计 diff；合并优于删除 |
| 开放浏览失控 | 速率限制、超时、只读膜门、robots 尊重（可配置） |
| 选题重复或僵化 | `topic_history_index` + 冷却窗口 + 禁止固定 TOPIC_LIST |
| closeout 与 idle 双写冲突 | closeout 写 exit；idle 写 hygiene/web；wake_integration 合并 |
| 与第 5 点语言抢工期 | D7 只做材料接口 |
| 结构化 wake question 变成固定话术 | D6/D7 固定 `expression_policy=model_generated_only_no_fixed_sentence`，`literal_text=null` |
| 梦境自我解释污染人格 | D3/D6 引入 DreamBeliefGate，长期信念/人格变化必须多轮证据 |
| Playwright 浏览误触 side effect | D4/D5 browser adapter 禁止 click/submit/download，行动封印写入 session log |

---

## 10. 当前结论与下一刀

- **方向正确**，ITR-02/04 骨架可复用，禁止另起 `dream_v2` 平行包。
- **D0–D8 已结案**（2026-06-16）：离线入口、trace 硬接线、hygiene、closeout 梦境五件套、Playwright 只读浏览 + 自主选题、表达材料链、`memory_retrieval` 接通 `structured_wake_question_candidates`、`test_dream_phenomenon_scenarios`（S1–S10）与 `08`/`temp/13` 回写均已完成。
- **下一刀**：转入第 5 点语言消费链加厚；可选在 `test_persistent_digital_life_process` 长跑中补端到端现象层互证。

---

## 附录 A：4a 分层与记忆库字段对照

| 关系/记忆概念 | 记忆模块对象 | exit_dream 字段 |
|---|---|---|
| 印象深刻、易想起 | `tiered_recall.salient_core` | `memory_tiering.salient_core_episode_refs` |
| 上下文、可想起 | `tiered_recall.retrievable_context` | `memory_tiering.retrievable_context_episode_refs` |
| 边缘、难想起 | `tiered_recall.deep_sediment` | `memory_tiering.deep_sediment_episode_refs` |
| 写入治理 | `MemoryWriteGate` + `StateMergeGuard` | `write_merge_governance` |
| 禁止梦境变事实 | `DreamFactGateDecision` | `dream_fact_boundary` |
| 禁止梦境直接改信念 | `DreamBeliefGateDecision` | `dream_belief_boundary` |
| 梦中外部行动封印 | `DreamActionInhibitionSeal` | `dream_action_inhibition_seal` |

## 附录 B：4c 浏览与选题配置（D4–D5 预备）

```json
{
  "schema_version": "web_dream_learning_config_v1",
  "enabled": true,
  "external_action_policy": "read_only_no_side_effect",
  "relation_curated_seeds": [
    {
      "url": "https://example.com/article",
      "relation_note": "关系人/共在者留下的世界入口",
      "relation_scope": "current_relation",
      "priority": 1
    }
  ],
  "default_world_seed_catalog": [
    {
      "name": "GitHub Trending",
      "url": "https://github.com/trending",
      "category": "code_and_open_source",
      "priority": 100,
      "access_policy": "public_read",
      "dream_use": "发现真实代码、工程趋势、开源项目和可学习的实现方式"
    },
    {
      "name": "GitHub Explore",
      "url": "https://github.com/explore",
      "category": "code_and_open_source",
      "priority": 98,
      "access_policy": "public_read",
      "dream_use": "从开放代码世界形成长期工程 curiosity"
    },
    {
      "name": "Hugging Face Models",
      "url": "https://huggingface.co/models",
      "category": "ai_models",
      "priority": 95,
      "access_policy": "public_read",
      "dream_use": "观察模型、数据集、工具链和 AI 社区变化"
    },
    {
      "name": "Hugging Face Papers",
      "url": "https://huggingface.co/papers",
      "category": "ai_research",
      "priority": 94,
      "access_policy": "public_read",
      "dream_use": "把新论文趋势转成离线学习 residue"
    },
    {
      "name": "Nature",
      "url": "https://www.nature.com/",
      "category": "authority_science_journal",
      "priority": 92,
      "access_policy": "public_read",
      "dream_use": "权威自然科学入口，供科学概念和生命理论更新"
    },
    {
      "name": "Nature Neuroscience",
      "url": "https://www.nature.com/neuro/",
      "category": "authority_neuroscience_journal",
      "priority": 93,
      "access_policy": "public_read",
      "dream_use": "优先关注脑科学、神经科学、认知机制"
    },
    {
      "name": "Science",
      "url": "https://www.science.org/",
      "category": "authority_science_journal",
      "priority": 92,
      "access_policy": "public_read",
      "dream_use": "权威综合科学入口，补充自然科学世界感"
    },
    {
      "name": "Cell",
      "url": "https://www.cell.com/",
      "category": "authority_life_science_journal",
      "priority": 88,
      "access_policy": "public_read",
      "dream_use": "生命科学、神经、生物机制的高质量入口"
    },
    {
      "name": "PNAS",
      "url": "https://www.pnas.org/",
      "category": "authority_science_journal",
      "priority": 86,
      "access_policy": "public_read",
      "dream_use": "跨学科科学发现入口"
    },
    {
      "name": "PubMed",
      "url": "https://pubmed.ncbi.nlm.nih.gov/",
      "category": "biomedical_index",
      "priority": 90,
      "access_policy": "public_read",
      "dream_use": "医学、神经科学、生命科学文献检索入口"
    },
    {
      "name": "arXiv cs.AI",
      "url": "https://arxiv.org/list/cs.AI/recent",
      "category": "ai_research_preprint",
      "priority": 84,
      "access_policy": "public_read",
      "dream_use": "跟踪 AI 研究前沿，但事实晋升必须额外验证"
    },
    {
      "name": "Papers with Code",
      "url": "https://paperswithcode.com/",
      "category": "ai_research_code_bridge",
      "priority": 86,
      "access_policy": "public_read",
      "dream_use": "连接论文、任务、代码和实现趋势"
    },
    {
      "name": "AI Hot Daily",
      "url": "https://aihot.virxact.com/daily",
      "category": "ai_daily_digest",
      "priority": 84,
      "access_policy": "public_read",
      "dream_use": "每日 AI 热点入口，作为低成本趋势采样"
    },
    {
      "name": "X / Twitter Explore",
      "url": "https://x.com/explore",
      "category": "social_signal",
      "priority": 70,
      "access_policy": "public_read_or_skip_if_login_wall",
      "dream_use": "社会热点和技术讨论的弱信号入口；登录墙则跳过"
    },
    {
      "name": "今日头条",
      "url": "https://www.toutiao.com/",
      "category": "chinese_news_and_social_signal",
      "priority": 68,
      "access_policy": "public_read_or_skip_if_login_wall",
      "dream_use": "中文社会热点采样；只读，不追逐噪声"
    },
    {
      "name": "Bilibili",
      "url": "https://www.bilibili.com/",
      "category": "chinese_video_culture",
      "priority": 72,
      "access_policy": "public_read_or_skip_if_login_wall",
      "dream_use": "中文视频文化、技术教程和社区情绪入口"
    },
    {
      "name": "Linux.do",
      "url": "https://linux.do/",
      "category": "developer_community",
      "priority": 80,
      "access_policy": "public_read_or_skip_if_login_wall",
      "dream_use": "开发者真实讨论、工具经验和中文技术社区入口"
    },
    {
      "name": "Hacker News",
      "url": "https://news.ycombinator.com/",
      "category": "developer_community",
      "priority": 78,
      "access_policy": "public_read",
      "dream_use": "技术、创业、工程文化的公共讨论入口"
    },
    {
      "name": "Lobsters",
      "url": "https://lobste.rs/",
      "category": "developer_community",
      "priority": 72,
      "access_policy": "public_read",
      "dream_use": "更窄但高密度的工程讨论入口"
    },
    {
      "name": "Reddit MachineLearning",
      "url": "https://www.reddit.com/r/MachineLearning/",
      "category": "ai_community_signal",
      "priority": 70,
      "access_policy": "public_read_or_skip_if_blocked",
      "dream_use": "AI 社区讨论弱信号；被阻断则跳过"
    },
    {
      "name": "MIT Technology Review",
      "url": "https://www.technologyreview.com/",
      "category": "technology_magazine",
      "priority": 74,
      "access_policy": "public_read",
      "dream_use": "技术社会影响与长期趋势入口"
    },
    {
      "name": "Quanta Magazine",
      "url": "https://www.quantamagazine.org/",
      "category": "science_magazine",
      "priority": 76,
      "access_policy": "public_read",
      "dream_use": "数学、物理、生命科学的高质量叙事入口"
    },
    {
      "name": "Aeon",
      "url": "https://aeon.co/",
      "category": "philosophy_culture_science",
      "priority": 66,
      "access_policy": "public_read",
      "dream_use": "哲学、文化和自我叙事材料入口"
    }
  ],
  "browser_backend": "playwright_readonly",
  "fallback_backend": "urllib_mock_or_ci_fallback",
  "playwright_readonly": {
    "enabled": true,
    "headless": true,
    "allow_click": false,
    "allow_form_fill": false,
    "allow_download": false,
    "max_pages_per_session": 5,
    "max_hops_per_seed": 2,
    "max_seconds_per_page": 12,
    "max_open_tabs": 1
  },
  "autonomous_discovery": {
    "enabled": true,
    "open_web_read": true,
    "max_hops_per_session": 3,
    "rate_limit_requests_per_hour": 30,
    "respect_robots_txt": true,
    "domain_cooldown_sessions": 3,
    "discovery_entry": "outbound_links_from_seeds"
  },
  "topic_selection_policy": {
    "schema_version": "topic_selection_policy_v1",
    "no_repeat_cluster_window": 3,
    "url_digest_cooldown_sessions": 5,
    "wake_question_candidate_cooldown": 3,
    "forbid_fixed_topic_table": true,
    "inputs": [
      "relationship_theme_tags",
      "dream_residue_refs",
      "curiosity_vector",
      "topic_history_index"
    ]
  }
}
```

`open_web_read: true` 表示允许自主发现分支离开关系 seed 域，仍受 Playwright 只读膜门约束。

### 附录 B.1 固定世界入口优先级

| 层级 | 站点族 | 作用 | 策略 |
|---|---|---|---|
| S | GitHub | 最重要的工程世界入口，优先学习真实代码、项目结构、issue 讨论和实现模式 | 高优先级、可高频回访，但 topic/仓库必须反重复 |
| A | Hugging Face、Papers with Code、arXiv | AI 模型、论文和代码桥接入口 | 中高频采样，事实晋升必须走验证 |
| A | Nature、Nature Neuroscience、Science、Cell、PNAS、PubMed | 权威科学、脑科学、生命科学入口 | 低噪声高权重；更适合进入长期学习 residue |
| B | AI Hot Daily、MIT Technology Review、Quanta | 趋势和高质量科普入口 | 用于 curiosity 和话题扩展 |
| B | Linux.do、Hacker News、Lobsters | 工程社区真实讨论入口 | 只读公共页，提取工程经验和社区问题 |
| C | X/Twitter、今日头条、Bilibili、Reddit | 社会热点、文化、视频和弱信号入口 | 易噪声/登录墙；低权重、强冷却、不可直接写事实 |
| C | Aeon 等思想文化站 | 哲学、自我叙事、关系和语言材料入口 | 低频进入 DefaultDriftMode |

访问策略：

- GitHub 是最高优先级，但不能每轮只看 GitHub；`topic_history_index` 必须约束仓库、语言、topic cluster 的重复。
- 权威期刊站点的材料优先进入 `long_term_learning_residue`，社交/热点站点优先进入 `weak_signal_residue`。
- 遇到登录墙、付费墙、反自动化页面时，Playwright session 写 `skipped_due_to_access_wall`，不得尝试登录、绕过或输入表单。
- 站点目录可以固定，topic 不得固定；每轮选择仍由 `TopicSelectionPolicy` 结合梦境、关系、记忆、疲惫和新颖度动态决定。

## 附录 C：离线记忆整理规则（D2）

| 动作 | 条件 | 结果 |
|---|---|---|
| 合并近似 trace | 相同 `semantic_key` 或 pattern_separation 判定同事件 | 保留最高 salience；其余 `merged_into` |
| 降级冗余 | 重复 source_ref、无新 evidence | → `deep_sediment` 或 `deprecated` |
| 强化关键 | identity / commitment / relationship / protected | salience 下限；禁止 delete |
| 保留矛盾链 | MEM-COR-002 contradiction links 存在 | 禁止静默覆盖 |
| 审计 | 每条 hygiene 动作 | 写入 `hygiene_actions[]`：action、trace_id、reason、before/after |

## 附录 D：选题反重复（D5）

```text
topic_cluster_id = hash(normalized_title + heading_sample + text_digest_sample + domain)
url_digest = hash(canonical_url)

每轮 TopicSelectionPolicy:
  1. 合成候选池（关系余波 + 梦境 + 页内标题 + curiosity）
  2. 过滤 topic_history 中 window 内已用 cluster
  3. 过滤 cooldown 内 url_digest
  4. 选最高分且未用过者
  5. 生成 structured_wake_question_candidate（literal_text=null）
  6. 写入 topic_history_index（不生成固定自然语言问句）
```

配置扩展在 D4–D5 实施；D1–D3 不依赖 Playwright。
