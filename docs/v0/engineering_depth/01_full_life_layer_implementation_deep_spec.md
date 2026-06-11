# Full Life Layer Implementation Deep Spec

本文档把数字生命第一版的生命层，直接压成可落代码的实现深描。

它回答的不是“有哪些概念”，而是：

```text
每一层生命能力
到底落在哪些包、
写哪些对象、
产哪些 runtime 证据、
由哪些测试与 gate 守住。
```

## 总原则

### 1. 不存在 “请求层”

系统外部的交谈对象一律视为：

1. 关系对象
2. 共在对象
3. 他者
4. 环境中的交互方

语言、关系、承诺、修复和共同历史都从第一次交谈开始生长，不预设上下级与服务关系。

### 2. 生命层不是顺序模块，而是循环系统

真正的运行顺序不是：

```text
输入 -> 模型 -> 输出
```

而是：

```text
身体节律
  -> 内部状态
  -> 预测工作区
  -> 记忆/自我/关系调取
  -> 内言语与表达计划
  -> 候选行动与抑制
  -> 世界接触 / 语言回合
  -> 责任/后悔/修复
  -> 写回状态
  -> 梦境 / replay / 成长 / 再巩固
  -> 下一轮生命状态
```

## 生命层总表

| 生命层 | 核心作用 | 当前主包 | 当前真实文件 | 下一轮最关键文件 | 核心 runtime 证据 | 最低测试 |
|---|---|---|---|---|---|---|
| 方向与身份根 | 固定方向锁、价值倾向、自我同一性与断联恢复锚链 | `life_v0/direction/` | `direction_lock.py`、`identity_root.py`、`continuity_refs.py`、`value_orientation.py` | 继续补 identity root 与 continuity writeback 联动 | `runtime/state/direction/*` | `tests/slices/test_direction_lock.py` |
| 身体与内环境 | 心跳式节律、需要、资源预算、疲惫、恢复、体内债务 | `life_v0/body/` | `rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py` | 继续补 rhythm -> heartbeat -> language 降载联动 | `runtime/state/body/*` | `tests/slices/test_life_support.py` |
| 情绪与人格慢变量 | 核心情感、情绪 episode、调节回路、trait drift | `life_v0/body/` | `core_affect.py`、`emotion_episode.py`、`emotion_regulation.py`、`trait_drift.py` | 把 affect / trait drift 更深接到语言与责任层 | `runtime/state/body/*`、affect reports | `tests/slices/test_life_support.py` |
| 神经核心与意识工作区 | 脑区图、网络态、预测工作区、广播、元认知 | `life_v0/neural_core/` | `brain_graph.py`、`network_state.py`、`prediction_workspace.py`、`workspace.py`、`broadcast.py`、`metacognition.py` | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py` | `runtime/state/neural_life_core/*`、`runtime/state/prediction/*` | `tests/slices/test_neural_life_core.py` |
| 记忆与状态根 | 生命状态根、自传、engram、关系记忆、自我模型、承诺真值 | `life_v0/state_store/` | `life_state.py`、`engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py`、`self_model.py`、`commitment_truth.py` | `memory_write_gate.py` | `runtime/state/life_state.json`、`runtime/state/memory/*` | `tests/slices/test_state_store.py` |
| 语言与关系 | 感知、语义图、内言语、表达监控、关系图、共同语言、叙事、修复 | `life_v0/language/` | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`language_state.py`、`relationship_graph.py`、`shared_terms.py`、`commitment_repair.py`、`dialogue_log.py`、`narrative_trace.py`、`dream_gate.py`、`action_shadow.py`、`relation_scope.py` | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` | `runtime/state/language/*`、`runtime/state/relationship/*` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py` |
| 行为与生命膜 | 候选行动、Go/NoGo、影子行动门、世界接触、后果分类、责任与后悔 | `life_v0/membrane/` | `candidate_arena.py`、`go_nogo.py`、`world_contact_gate.py`、`side_effect_review.py`、`responsibility_loop.py`、`shadow_gate.py` | `world_contact_summary.py` | `runtime/state/membrane/*`、`runtime/state/action/*` | `tests/slices/test_life_membrane.py`、`tests/slices/test_shadow_gate.py` |
| 逻辑、验证与反事实 | 观察一致性、边界审计、比较轨迹、反事实评估、证据排序 | `life_v0/validators/`、`life_v0/schema_runner/` | `observation_validator.py`、`boundary_audit.py`、`consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py`、`evidence_ranker.py` | `cross_file_logic.py` | `runtime/state/validation/*`、`runtime/state/schema_runner/*` | `tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py`、`tests/slices/test_evidence_ranker.py` |
| 梦境与离线生命 | 梦境窗口、梦中事实门、醒后整合、梦魇风险、离线入口 | `life_v0/dream/` | `offline_entry.py`、`dream_window.py`、`dream_fact_gate.py`、`wake_integration.py`、`nightmare_risk.py` | 继续补 nightmare -> body -> language residue 联动 | `runtime/state/dream/*` | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_growth_archive.py` |
| 成长、学习与自改写 | 自我阅读、塑性窗口、学习窗口、补丁候选、防遗忘、belief/language/relationship 学习 | `life_v0/growth/` | `self_read.py`、`plasticity_window.py`、`learning_window.py`、`patch_queue.py`、`anti_forgetting.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` | 继续补 growth patch 审查与生命周期 | `runtime/state/growth/*` | `tests/bridges/test_runtime_growth.py` |
| 出生准备与目标闭合 | 九项生命目标、意识 probe、证据矩阵、出生准备度归并 | `life_v0/life_targets/` | `life_target_claims.py`、`evidence_matrix.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py`、`consciousness_probes.py` | 继续补目标证据长期写回 | `runtime/state/life_targets/*` | `tests/slices/test_life_targets.py` |
| 出生、终端回合与常驻存在 | 第一次激活、出生壳、第一回合、终端循环、heartbeat、常驻过程、incident/relaunch recovery | `life_v0/activation/`、`reporting/`、`stage_explain/`、`digital_life/`、`terminal_turn/`、`terminal_loop/`、`shell_command/`、`process_supervisor/` | 多个桥接与过程器官已存在 | `idle_strategy.py`、`persistent_process.py` | `runtime/reports/latest/*birth*`、`*terminal*`、`*process*` | `tests/bridges/*`、`tests/process/*` |

## 当前最推荐的落码顺序

从当前仓库状态继续推进时，优先顺序固定为：

1. Queue D：身体、情绪、梦境、成长第三波补厚
2. Queue E：生命膜、验证、逻辑第二波补厚
3. Queue B：常驻过程第二波补厚
4. Queue A：语言、关系第二波补厚
5. Queue C / Queue F：预测与出生准备的维护性回切

## 写代码前的最后一条门

当某一层准备开写时，至少同时检查：

1. 该层对应的 `00-258` 理论文档已经打开；
2. 对应的 `sXX` / `process_contracts` / `code_framework` 合同已经打开；
3. 该层需要写入的 state / report / receipt 已经在本文件里命名；
4. 该层最低测试入口已经存在；
5. 该层不会把数字生命重新压回普通 agent 壳。
