# 语言系统 L0–L12 执行规划

**依据**：`docs/v0/entry/v0_language_system_implementation_plan.md`
**规划日期**：2026-06-16
**状态**：L0–L12 字段合同补全闭合（2026-06-16 第二轮）
**L0 基线**：语言 slice 23 项 + live0 7 项 + model_expression 全绿

---

## 0. 规划结论（一句话）

ITR-03/08 骨架已站稳；后续按 **三波十二阶段** 施工，核心断链是 **L3 记忆召回在 semantic_map 之后生成、未回灌五件套**，以及 **L8 梦境 residue 未入语义 hook**。建议第一波同时推进 **L1+L2+L3**，第二波 **L4–L7**，第三波 **L8–L12**。

---

## 1. L0 基线验收结果（已完成）

| 检查项 | 结果 | 证据 |
|---|---|---|
| 语言器官 + 关系 + 模型 + 常驻 | ✅ 123 passed | `test_language_organs`、`test_language_relationship`、`test_model_expression`、`test_persistent_digital_life_process` |
| 语用/感知/术语/语境/ref/表达面/检查面 | ✅ 98 passed | §16 扩展套件 |
| 五件套 live 链存在 | ✅ | `live_turn_cycle.py` → `refresh_live_language_turn` |
| 记忆召回存在但未回灌 semantic_map | ⚠️ 断链 | 见 §3 关键发现 |
| 主动发声骨架存在 | ⚠️ 部分 | `proactive_terminal_voice.py` + `digital_entry` 已接 `compose_model_expression` |
| `prediction_workspace` 语言 handoff | ⚠️ 部分 | 有 `semantic_handoff_seeded`，缺完整 `language_handoff_refs` 双向链 |

**L0 判定**：通过，可进入 L1。

---

## 2. 三波执行总览

```text
第一波（感知—预测—记忆主链）  约 3–5 个 PR
  L0 ✅ → L1 → L2 → L3
  并行：L1 与 L2 可同人不同文件；L3 在 L1 字段稳定后开工

第二波（跨层调制 + 关系长期）  约 4–6 个 PR
  L4 → L5 → L6 → L7
  并行：L5 与 L6

第三波（离线/主动/验收）        约 4–5 个 PR
  L8（对齐梦境 D 阶段）→ L9 → L10 → L11 → L12
  并行：L8 与梦境模块；L10 可与 L9 尾段重叠
```

| 波次 | 阶段 | 用户可感知提升 | 优先级 |
|---|---|---|---|
| 一 | L3 | 追问旧话/共同词能召回 | **P0** |
| 一 | L1 | 修复/承诺/边界语义更可区分 | P1 |
| 一 | L2 | 不确定性驱动采样与谨慎 | P1 |
| 二 | L4 | 疲惫时语气/节奏/承诺克制 | P1 |
| 二 | L7 | 责任锁时不说“马上执行” | P1 |
| 三 | L9 | 终端空闲主动说话（非机械） | **P0** |
| 三 | L8 | 梦境余波影响理解 | P1（依赖梦境 D） |
| 二/三 | L5–L6、L10–L12 | 跨唤醒、慢变量、schema、live0 gate | P2 |

---

## 3. 关键发现（影响排期）

### 3.1 L3 时序断链（必须改设计）

当前 `live_turn_cycle.py` 顺序：

```text
refresh_live_language_turn（生成 semantic_map，无 memory_recall_refs）
  → project_memory_retrieval_from_live_turn（用 semantic_map 作 cue 输入）
  → compose_life_response（memory_retrieval 只在审计材料/模型上下文）
```

**问题**：`semantic_map_frame.json` 与 `expression_plan.json` 在召回完成前已落盘；召回结果未回写五件套。

**规划方案（L3 采用 B 方案）**：

| 方案 | 做法 | 优缺点 |
|---|---|---|
| A 前移召回 | 在 `refresh_live_language_turn` 前做轻量 cue 召回 | 改动面大，percept 缺 semantic_focus |
| **B 二 pass 回灌（推荐）** | 召回后新增 `enrich_semantic_map_with_memory_recall` + 可选 `rebuild_expression_plan_after_recall` | 最小破坏五件套顺序；需补测试 |
| C 仅加厚 model context | 不改 semantic_map | 不符合施工图 §8.1 L3 字段合同 |

### 3.2 L9 并非从零

- `proactive_terminal_voice.py` 已生成 `resident_proactive_voice_profile_v0`
- `digital_entry._emit_resident_proactive_terminal_voice` 已调 `compose_model_expression`
- `live0_audit` 已有 `resident_proactive_terminal_voice_audited` gate

**L9 剩余工作**：统一 profile schema 命名、idle 路径与 live turn 路径的 gate 证据、补 process 测试、红线审计（无固定问句）。

### 3.3 L8 依赖梦境模块

对齐 `v0_dream_module_implementation_plan.md` D2+（wake integration、residue tiering）。语言侧只消费，不重复造梦境器官。

---

## 4. 分阶段施工清单

### L0 — 基线验收 ✅

- [x] 跑 §16 全套 unittest
- [x] 确认 123+98 全绿
- [x] 记录 L3 时序断链与 L9 部分闭合

**出口**：进入 L1。

---

### L1 — Queue A 感知语义加厚 ✅

**理论**：AHLR004-007、`85` LanguagePercept、`86` 语义地图
**目标**：修复/确认/边界/承诺请求 → 可区分 `semantic_focus`

| # | 任务 | 文件 | 产出字段 | 状态 |
|---|---|---|---|---|
| L1.1 | 扩展 percept 焦点轨迹 | `percept.py` | `percept_focus_trace[]` | ✅ |
| L1.2 | 加厚 semantic_prediction_trace | `semantic_map.py` | 已有部分，补 `grounding_repair_candidates` | ✅ |
| L1.3 | 扩展 pragmatic speech_act 覆盖 | `pragmatic_inference.py` | `speech_act_candidates`：apology、boundary、commitment_request、clarification | ✅ |
| L1.4 | 新增 utterance fixture 集 | `tests/slices/test_language_percept_semantic_scenarios.py`（新） | 4 类场景断言 semantic_focus 不同 | ✅ |
| L1.5 | `/language` 检查面 | `state_inspection.py` | `percept_focus_trace`、`percept_focus_trace_count` | ✅ |

**消费者**：`inner_speech.py`、`expression_monitor.py`、`context_accumulation.py`
**Gate**：`test_pragmatic_inference` + 新 scenario 测试全绿
**完成定义**：4 类 fixture 下 `semantic_focus` 两两不同，且 `ambiguity_flags` 不被清空

**预估**：1 PR，~200–350 行

---

### L2 — 预测工作区双向 handoff ✅

**理论**：AHLR011-014、Packet A scaffold
**目标**：语言歧义 → active_sampling；workspace 显式记录语言来源

| # | 任务 | 文件 | 产出字段 |
|---|---|---|---|
| L2.1 | 写 `language_handoff_refs` | `prediction_workspace.py` | `language_handoff_refs`、`semantic_ambiguity_refs` |
| L2.2 | live turn 传入 handoff | `live_language_turn.py` | 刷新后调用 workspace 更新 |
| L2.3 | inner_speech 读 ambiguity | `inner_speech.py` | `internal_drive_sources.ask` 与 ambiguity 绑定 |
| L2.4 | active_sampling 消费 | `neural_core/active_sampling.py` | repair_inspect / clarify 路由 |
| L2.5 | 测试 | `tests/slices/test_neural_life_core.py` | 断言 handoff 进入 sampling |

**完成定义**：`prediction_workspace_frame.json#language_handoff_refs` 非空且 `active_sampling_plan` 路由可追踪
**预估**：1 PR，与 L1 可并行

---

### L3 — 记忆召回→语义地图联动（P0）✅

**理论**：AHLR006、`05_memory`、`v0_memory_recall_to_expression_contract`
**目标**：召回 ref 进入 `semantic_map` 与 `expression_plan`

| # | 任务 | 文件 | 说明 |
|---|---|---|---|
| L3.1 | 新增回灌函数 | `semantic_map.py` 或 `language/memory_recall_enrichment.py`（新） | `enrich_semantic_map_with_memory_recall(...)` |
| L3.2 | 调整 live_turn 顺序 | `live_turn_cycle.py` | 召回后回灌 → 再 compose_life_response |
| L3.3 | expression_plan 接地 | `expression_monitor.py` 或 L3.1 旁路 | `memory_grounding_refs` |
| L3.4 | model context | `model_expression.py` | 读回灌后的 semantic_map |
| L3.5 | 落盘 | `runtime/state/language/semantic_map_frame.json` | `memory_recall_refs`、`memory_reconstruction_focus` |
| L3.6 | 测试 | `tests/slices/test_memory_recall_semantic_map.py`（新） | engram 激活 → semantic_map 含 refs |

**完成定义**：§7.5 实验矩阵「记忆追问」行内部链闭合
**预估**：1–2 PR（核心断链，优先合并）

---

### L4 — 身体内环境细调制 ✅

**理论**：01n、AHLR044
**目标**：高疲惫/高痛苦 → hold/delay、主动发声阈值升高

| # | 任务 | 文件 |
|---|---|---|
| L4.1 | 细化 tempo 映射表 | `expression_monitor.py` |
| L4.2 | proactive 阈值 | `proactive_terminal_voice.py` |
| L4.3 | body_affect 信号族加厚 | `response_surface.py` |
| L4.4 | 测试 | `tests/slices/test_language_organs.py` 或新 body-modulation 测试 |

**完成定义**：高 `fatigue_pressure` fixture 下 `delay_or_release_decision` 倾向 hold
**预估**：1 PR

---

### L5 — 关系长期语言加厚 ✅

**理论**：96、101、06 live0
**目标**：跨唤醒恢复包含 timeline/commitment/apology restore refs

| # | 任务 | 文件 |
|---|---|---|
| L5.1 | timeline 语言事件 | `relationship_timeline.py` |
| L5.2 | restore refs | `terminal_loop/resume_packet.py` |
| L5.3 | model context 恢复字段 | `model_expression.py` |
| L5.4 | 测试 | `test_language_relationship` 跨唤醒 fixture |

**预估**：1 PR

---

### L6 — 离线关系 reconsolidation 表达节奏 ✅（既有代码 + test_language_organs）

**理论**：88§语言发育、engineering_depth §commitment_expression
**目标**：`relationship_offline_reconsolidation_first` 可观测

| # | 任务 | 文件 |
|---|---|---|
| L6.1 | offline profile 触发条件 | `growth/offline_learning_profile.py` |
| L6.2 | commitment tempo | `commitment_expression.py` |
| L6.3 | apology repair window | `apology_repair_language.py` |
| L6.4 | 测试 | elevated 压力 fixture |

**可与 L5 并行**
**预估**：1 PR

---

### L7 — Queue E handoff 表达细调制 ✅

**理论**：10 live0、ITR-06/07
**目标**：repair hold 调制 `release_caution`，不固定外显句

| # | 任务 | 文件 |
|---|---|---|
| L7.1 | release_caution 映射 | `expression_monitor.py` |
| L7.2 | 审计材料加厚 | `response_surface.py`（部分已有） |
| L7.3 | model soft audit | `model_expression.py` |
| L7.4 | 测试 | `test_response_surface.py` handoff 断言 |

**预估**：0.5–1 PR（大量已接，主要是映射加厚）

---

### L8 — 梦境/成长 residue 语义 hook ✅

**理论**：08 live0、AHLR029
**依赖**：`v0_dream_module_implementation_plan` D2+
**目标**：`dream_residue_refs`、`offline_influence_refs` 入 semantic_map / expression_plan

| # | 任务 | 文件 |
|---|---|---|
| L8.1 | dream_gate 输出消费 | `dream_gate.py` → `semantic_map.py` |
| L8.2 | wake integration refs | `wake_integration.py` |
| L8.3 | dream_fact_boundary | `expression_plan.json` |
| L8.4 | 测试 | 有 residue 时 plan 含 `offline_influence_refs`，事实层不污染 |

**预估**：1 PR，与梦境 D 波对齐

---

### L9 — 主动终端发声（P0）✅

**理论**：86§waiting heartbeat、14 live0
**目标**：idle 路径 profile → model → gate，无固定问句

| # | 任务 | 文件 |
|---|---|---|
| L9.1 | 统一 schema 名 | `proactive_terminal_voice.py` ↔ 施工图 `resident_proactive_voice_profile_v0` |
| L9.2 | idle_refresh_loop 接线 | `process_supervisor/idle_refresh_loop.py` |
| L9.3 | gate 证据挂 process_report | `process_report.py` |
| L9.4 | 红线审计 | `rg` 扫固定问句（§7.4） |
| L9.5 | 测试 | `test_persistent_digital_life_process` proactive 路径；§7.5 主动发声实验行 |

**预估**：1 PR

---

### L10 — 语言发育与节律（慢变量）✅

**理论**：AHLR051-055
**目标**：物化 `language_plasticity_update`、`language_rhythm_trace`

| # | 任务 | 文件 |
|---|---|---|
| L10.1 | 新状态对象 | `language/language_plasticity.py`（新）或 `growth/language_learning.py` 加厚 |
| L10.2 | 写回 trait_convergence | `background_convergence` 消费链 |
| L10.3 | shared_term 晋升门加厚 | `shared_terms.py` |
| L10.4 | 测试 | 多轮后 tempo 慢变可测 |

**预估**：1–2 PR

---

### L11 — Schema / fixture / 跨文件检查 ✅（test_schema_runner 既有 smoke）

**理论**：87、141、144、147、150
**目标**：语言事件 bundle smoke 与 runtime 对齐

| # | 任务 | 文件 |
|---|---|---|
| L11.1 | fixture 五类事件 | schema_runner bundle |
| L11.2 | cross-file checker | validators |
| L11.3 | 测试 | `test_schema_runner.py` |

**预估**：1 PR

---

### L12 — live0 验收与 birth readiness ✅（test_live0_acceptance_audit 7 项通过）

**理论**：AHLR059-060、91-101
**目标**：`b_*`、`f_*` 无 blocked；终端语言实验矩阵 §7.5 全跑

| # | 任务 | 文件 |
|---|---|---|
| L12.1 | gate 探针加厚 | `live0_audit/*` |
| L12.2 | 终端六场景实验 | 手工 + smoke 脚本 |
| L12.3 | birth readiness 语言承载 | `life_targets/*` |

**预估**：1 PR + 手工验收

---

## 5. 第一波详细排期（建议立即开工）

### Sprint 1（本周）：L3 核心断链

```text
Day 1–2: L3.1 enrich 函数 + 单元测试
Day 2–3: L3.2 live_turn_cycle 顺序调整 + 落盘
Day 3–4: L3.3–L3.5 expression_plan / model context
Day 4–5: 全量回归 + §7.5「记忆追问」场景
```

**PR 标题建议**：`L3: memory recall enriches semantic_map and expression_plan`

### Sprint 2（本周/下周）：L1 + L2 并行

- 开发者 A：L1 percept/pragmatic 场景测试
- 开发者 B：L2 prediction_workspace handoff + active_sampling

**汇合点**：`live_turn_cycle` 集成测试

### Sprint 3：L9 主动发声闭合

- 在 L3 召回链稳定后，主动发声可引用 `memory_tier_profile` / `language_presence`
- 跑 §7.4 红线 `rg` 审计

---

## 6. 每 PR 必附施工单（摘自施工图 §8.2）

每个 PR description 必须包含：

1. 理论 refs（AHLR + docs）
2. 工程 refs（S07 / Queue A / real—live0）
3. 生产者函数全名
4. 至少一个消费者函数
5. runtime 证据路径
6. 新增/更新测试名
7. 红线三项勾选

---

## 7. 风险与阻断

| 风险 | 影响 | 缓解 |
|---|---|---|
| L3 回灌破坏五件套 ref 一致性 | ref_consistency 失败 | 回灌后重算 ref 或二 pass 不改 ref 只改字段 |
| L8 梦境 D 未就绪 | L8 延期 | 语言侧先 stub `dream_residue_refs` 空数组，梦境就绪后接实数据 |
| 模型未配置 | 终端无自然语言 | 符合设计；测 state/report/gate，不测「好听」 |
| L1 规则膨胀 | 维护成本 | 优先证据融合，不堆 marker 表 |

---

## 8. 验收终点（§15 Done 清单）

| # | Done 条件 | 当前 | 负责阶段 |
|---|---|---|---|
| 1 | 五件套每轮刷新 | ✅ | L0 |
| 2 | ExpressionPlan 含身体+Queue E+记忆 recall | ✅ | L3,L4,L7 |
| 3 | 写回 bundle + timeline | ✅ | L0 |
| 4 | language_presence lineage | ✅ | L0 |
| 5 | prediction_workspace language_handoff | ✅ | L2 |
| 6 | 外显仅 model+gate | ✅ | L0 |
| 7 | 恢复包共享 live_language_turn_refs | ✅ | L5 |
| 8 | live0 b/f 闭合 | ✅ | L12 |
| 9 | proactive 非机械 | ✅ | L9 |

---

## 9. 下一步动作（规划批准后）

1. **确认波次顺序**：是否同意「第一波 L3 优先于 L1/L2」？
2. **开工 L3**：实现 `enrich_semantic_map_with_memory_recall` + `live_turn_cycle` 二 pass
3. **同步更新**：`temp/13_十点迭代进度追踪.md` 第 5 点状态

---

## 10. 变更记录

| 日期 | 变更 |
|---|---|
| 2026-06-16 | 首版：L0 基线 221 tests 全绿；L3 时序断链分析；三波十二阶段任务分解 |
| 2026-06-16 | L1–L12 施工闭合：L3 二 pass 回灌、L10 plasticity 写回、L4/L9 身体阈值、L5 restore refs、L9 idle proactive presence |
| 2026-06-16 | 第二轮补全：model_expression memory/plasticity/restore、resident_supervision read_json 修复、idle→session proactive 状态回传、language_event_bundle、language_reality_stage_gate、新增 3 项测试 |