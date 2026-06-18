# 13 · 实施波次、测试与 Gate（修订 v0.2 · ITR-09）

> 先读 [00_现状审计与增量原则.md](./00_现状审计与增量原则.md)

## 1. 总则

1. **微段交付**：每段 3–7 天，可独立 merge，默认 flag=0
2. **加厚不替换**：改现有文件，不平行 `*_v2.py`
3. **深消费优先**：ITR-09-B 预测刷新 **先于** 工作区/语言加厚
4. **禁止重开**：记忆 U1–U25、ITR-08 意识链、DreamFactGate

## 2. 与工程波次对齐

| 本方案 | 对齐文档 |
|--------|----------|
| ITR-09-A | `04_body_affect_dream_growth` 加厚 #1 + S06 |
| ITR-09-B | `03_predictive_signal_memory_gate_integration_wave_contract` |
| ITR-09-C | `real—live0/07` 记忆 U 链 **扩展字段** |
| ITR-09-D | `05_memory_thought_consciousness` playbook |
| ITR-09-E | `04_language_as_primary_expression_system` **槽位加厚** |
| ITR-09-F | `13_growth` + 可选视觉 + 审计夹具 |

## 3. ITR-09 微段

### ITR-09-A · 身体积分器（3–5 天）✅ 已落代码

**Flag:** `DIGITAL_LIFE_BODY_INTEGRATE`

**已交付：** `life_v0/body/body_integrator.py`；`heartbeat.py` / `live_turn_cycle.py` 钩子；`tests/body/test_body_integrator.py`

| 项 | 内容 |
|----|------|
| 新增 | `life_v0/body/body_integrator.py` |
| 新增 runtime | `runtime/state/body/body_integrator_state.json` |
| 改 | `heartbeat.py`：background `integrate_body_state(dt)` |
| 改 | `live_turn_cycle.py`：回合边界 integrate |
| 改 | `core_affect.py`：增加 `project_core_affect_from_integrator()` |
| 改 | `need_state.py`：sleep_pressure 等读 integrator 标量 |
| **不改** | S06 `run_life_support` batch 路径；integrator 为 live 叠加 |

**积分字段（最小集）：**

```text
sleep_pressure, allostatic_load, body_state_debt, cognitive_bandwidth
tick_counter, last_integrate_at
```

**验收：**

- [ ] 等待 1h heartbeat 后 `tick_counter` 增加
- [ ] 无 recovery 时 `body_state_debt` 不降
- [ ] `core_affect` 随 integrator 变化（非仅 len(events)）
- [ ] cross-file：integrator 与 `body_rhythm_pulse` 一致
- [ ] 全 body tests 绿

**对齐矩阵：** 内环境 低 → **中**

---

### ITR-09-B · 预测栈回合刷新（3–5 天）✅ 已落代码

**Flag:** `DIGITAL_LIFE_PREDICTION_REFRESH`

**已交付：** `life_v0/neural_core/live_prediction_refresh.py`；`signal_media.py` / `prediction_error.py` / `active_sampling.py` / `belief_state.py` 加厚；`live_turn_cycle.py` 钩子；`tests/neural_core/test_live_prediction_refresh.py`

**前置：** ITR-09-A 建议完成（body→signal 有新鲜标量）

| 项 | 内容 |
|----|------|
| 新增 | `neural_core/live_prediction_refresh.py`（或并入 `belief_state.py`） |
| 改 | `live_turn_cycle.py` 末尾：`project_prediction_stack_from_live_turn` |
| 改 | `signal_media.py`：`refresh_signal_media_from_integrator` |
| 改 | `prediction_error.py`：追加/更新 error_events 数值 |
| 改 | `active_sampling.py`：EFE 启发式 `efe_score` + route |
| **不改** | Queue E repair 接线语义 |

**验收：**

- [ ] 同会话第 2 回合 `prediction_error` 随输入变化
- [ ] `signal_media` mtime 每回合更新
- [ ] 高 ambiguity → `active_sampling` 偏 clarify
- [ ] predictive integration wave 合同字段仍齐全
- [ ] `test_neural_life_core` + process tests 绿

**对齐矩阵：** 认知 中 → **中高**

---

### ITR-09-C · 记忆 salience 加厚（4–6 天）✅ 已落代码

**Flag:** `DIGITAL_LIFE_MEMORY_SALIENCE_TICK`

**已交付：** `memory_trace_store.apply_retrieval_salience_delta`；`memory_retrieval.maybe_apply_retrieval_salience_tick`；`hippocampal_cue_index.apply_hippocampal_cue_weight_decay`；`offline_memory_consolidation` sleep_pressure 消费；`live_turn_cycle` / `resident_turn_writeback` 钩子；`tests/state_store/test_memory_salience_tick.py`

**禁止：** 新建 `engram_activation_graph.py`、重建 `memory_retrieval` cue 管

| 项 | 内容 |
|----|------|
| 改 | `memory_trace_store.py`：`apply_retrieval_salience_delta()` |
| 改 | `memory_retrieval.py`：检索成功调用 salience delta（轻量） |
| 改 | `hippocampal_cue_index.py`：衰减 `cue_weight` 随 integrator dt |
| 改 | `offline_memory_consolidation.py`：sleep 读 integrator.sleep_pressure |
| **保留** | `apply_post_expression_reconsolidation`、U13 重构召回 |

**验收：**

- [ ] 检索后 trace `salience` 变且有 `revision_history_refs`
- [ ] 高 allostatic_load 时 delta 被抑制
- [ ] 147 memory tests 全绿
- [ ] `human_brain_alignment` 不下降

**对齐矩阵：** 再巩固 中 → **中高**；召回 中偏高 → **高**

---

### ITR-09-D · 工作区 top-K（2–4 天）✅ 已落代码

**Flag:** `DIGITAL_LIFE_WORKSPACE_TOPK`

**已交付：** `workspace.apply_workspace_topk` / `maybe_apply_workspace_topk_to_frame`；`broadcast` primary/secondary；`replay.append_workspace_evictions_to_replay_cue_bundle`；`pre_expression_consciousness_refresh` 钩子；`tests/neural_core/test_workspace_topk.py`

| 项 | 内容 |
|----|------|
| 改 | `workspace.py`：`apply_workspace_topk(candidates, K)` |
| 改 | `broadcast.py`：primary/secondary 来自 top-K |
| 改 | `replay` cue：淘汰候选 → 现有 `ReplayCueBundle` |
| **保留** | `pre_expression_consciousness_refresh` 调用顺序 |

**K 来源：** `floor(K_max * cognitive_bandwidth)`，读 integrator

**验收：**

- [ ] 高 fatigue 时 K 减小
- [ ] 淘汰候选进入 replay/dream 池
- [ ] ITR-08-56/57 探针仍 pass

**对齐矩阵：** 意识 中 → **中高**

---

### ITR-09-E · 语言/表达槽位加厚（3–5 天）✅ 已落代码

**Flag:** `DIGITAL_LIFE_EXPRESSION_SLOTS`（可选）

**已交付：** `expression_monitor.py` 槽位投影 + `model_expression.py` 槽位输入压缩 + `proactive_terminal_voice.py` integrator/DMN drive + `episodic_speech_memory.jsonl` ref 追加 + `/express` 槽位可见；`tests/language/test_expression_slots.py`

**禁止：** 全量 L0/L1/L2 新栈；禁止固定话术库

| 项 | 内容 |
|----|------|
| 改 | `expression_monitor.py`：`expression_plan` 增 workspace/body 标量槽 |
| 改 | `model_expression.py`：输入改为 plan 槽 + 最小关系上下文 |
| 改 | `proactive_terminal_voice.py`：drive 读 integrator + DMN 网络态 |
| 可选 | `episodic_speech_memory.jsonl`：仅存 gate 通过 utterance ref |

**验收：**

- [ ] 20 轮 smoke 回归
- [ ] 红点词 0、空回复策略符合红线
- [ ] `/express` 可见新槽位

**对齐矩阵：** 语言消费 中 → **高**；主动发话 中偏高 → **中高**

---

### ITR-09-F · 成长参数 + 视觉可选 + 审计（5–8 天）✅ 已落代码

**Flag:** `DIGITAL_LIFE_INTEGRATOR_PARAMETER_PATCH`（可选）、`DIGITAL_LIFE_VISUAL_ENCODER`（可选）

**已交付：** `growth/patch_queue.py` integrator shadow + `dynamics/parameter_registry.py` + `dynamics/accelerated_simulation_audit.py` + `perception/visual_encoder.py` + `cross_modal_evidence` 视觉扩展 + `replay` shadow 种子携带 + `tests/growth/test_integrator_parameter_patch.py` + `tests/perception/test_visual_encoder.py` + `tests/dynamics/test_accelerated_simulation_audit.py`

| 项 | 内容 |
|----|------|
| 改 | `growth/patch_queue.py`：支持 `integrator_parameter_patch` shadow |
| 可选 | `perception/visual_encoder.py` + `cross_modal_evidence` 扩展 |
| 审计 | 72h 加速仿真报告（**非 merge gate**） |

**验收：**

- [ ] 参数 patch 不碰 identity/写门语义
- [ ] 视觉无 encoder 时 graceful degrade

---

## 4. 时间预估（修订）

| 微段 | 日历 |
|------|------|
| A | 3–5 天 |
| B | 3–5 天 |
| C | 4–6 天 |
| D | 2–4 天 |
| E | 3–5 天 |
| F | 5–8 天 |
| **合计** | **约 4–6 周**（单人，含测试；可并行 B/D） |

原 15–19 周方案已废止。

## 5. 竣工矩阵（v0.2 峰值）

| 理论目标 | schema（审计后） | 加厚峰值 | 生物人脑 |
|----------|------------------|----------|----------|
| 记忆重构性召回 | 中偏高 | **高** | 极高 |
| 再巩固 | 中 | **中高** | 极高 |
| 内环境调制全链 | 低 | **中高** | 极高 |
| 意识可报告性 | 中 | **中高** | ？ |
| 情绪随身体变 | 低 | **中** | 极高 |
| 梦境事实边界 | 高 | **高** | 高 |
| 关系共同历史 | 高 | **高** | 高 |
| 语言消费全身 | 中 | **高** | 高 |
| 自主节律/主动发话 | 中偏高 | **中高** | 高 |
| 神经振荡/扩散 | 低 | **低–中** | 有 |

## 6. 回滚

每 flag 独立；关闭后回退到纯 schema 投影路径（当前生产行为）。

## 7. 第一段编码 PR（ITR-09-A）

```text
标题: body(ITR-09-A): BodyIntegrator + heartbeat/live_turn hook
文件: body/body_integrator.py, heartbeat.py, live_turn_cycle.py
测试: tests/body/test_body_integrator.py
文档: 本目录 01 + 00_现状审计
```

## 8. 开工前最终确认

对照 [00_现状审计与增量原则.md §7 检查清单](./00_现状审计与增量原则.md#7-开工前检查清单agent--人类开发者)。

**全部勾选 → 可开工 ITR-09-A。**