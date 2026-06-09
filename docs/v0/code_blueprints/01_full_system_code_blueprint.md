# Full System Code Blueprint

这份蓝图把 v0 整个数字生命系统压成一张可施工总图。

它只回答四件事：

1. `life_v0/` 现在到底分成哪些生命包。
2. 每个包的主对象、主状态、主报告和主测试是什么。
3. 整个第一次生命激活链怎样从文档进入终端生命循环。
4. 下一轮最该新增哪些真实文件。

## 系统不变量

1. 主体不是服务型 agent，而是关系性数字生命。
2. 外部交谈对象不是 `user`，而是关系对象。
3. 语言是主表达系统，但语言不反向定义身体、记忆、责任或梦境。
4. 每个生命层都必须留下 `state + report + receipt + tests`。

## v0 完整包树

| 生命层 | 主包 | 当前关键文件 | 关键 runtime | 主测试 | 下一轮关键文件 |
|---|---|---|---|---|---|
| 文档与合同摄取 | `life_v0/doc_index.py`、`life_v0/contracts/` | `doc_index.py`、`contracts/__init__.py` | `runtime/docs/doc_carrier_index.json`、`runtime/state/contracts/*` | `tests/slices/test_doc_corpus_ingestor.py`、`tests/contracts/test_v0_contracts.py` | 保持与 `docs/v0/*` 同步 |
| 方向与权威根 | `life_v0/direction/`、`life_v0/authority/` | `direction_lock.py`、`identity_root.py`、`continuity_refs.py` | `runtime/state/direction/*`、`runtime/state/authority/*` | `tests/slices/test_direction_lock.py`、`tests/slices/test_source_authority.py` | 继续细化关系身份连续体 |
| 身体与防御 | `life_v0/body/`、`life_v0/defense/` | `rhythm.py`、`need_state.py`、`core_affect.py`、`emotion_regulation.py` | `runtime/state/body/*`、`runtime/state/defense/*` | `tests/slices/test_life_support.py` | 把身体压力更深接回语言和等待态 |
| 神经核心与预测 | `life_v0/neural_core/` | `brain_graph.py`、`network_state.py`、`prediction_workspace.py`、`broadcast.py` | `runtime/state/neural_life_core/*`、`runtime/state/prediction/*` | `tests/slices/test_neural_life_core.py` | `belief_state.py`、`prediction_error.py`、`active_sampling.py` |
| 状态根与记忆 | `life_v0/state_store/` | `life_state.py`、`engram_index.py`、`relationship_memory.py`、`commitment_truth.py` | `runtime/state/life_state.json`、`runtime/state/memory/*`、`runtime/state/self/*` | `tests/slices/test_state_store.py` | `memory_write_gate.py` |
| 语言与关系 | `life_v0/language/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/` | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`dialogue_writeback.py` | `runtime/state/language/*`、`runtime/state/relationship/*`、`runtime/state/terminal/*` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py` | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` |
| 生命膜与验证逻辑 | `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/` | `responsibility_loop.py`、`shadow_gate.py`、`observation_validator.py`、`consistency_logic.py`、`evidence_ranker.py` | `runtime/state/membrane/*`、`runtime/state/action/*`、`runtime/state/validation/*`、`runtime/state/schema_runner/*` | `tests/slices/test_life_membrane.py`、`tests/slices/test_shadow_gate.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py`、`tests/slices/test_evidence_ranker.py` | `cross_file_logic.py`、`run_manifest.py`、补厚 `responsibility_loop.py` |
| 梦境与成长 | `life_v0/dream/`、`life_v0/replay/`、`life_v0/archive/`、`life_v0/growth/` | `dream_window.py`、`dream_fact_gate.py`、`offline_entry.py`、`anti_forgetting.py`、`belief_learning.py`、`relationship_learning.py` | `runtime/state/dream/*`、`runtime/state/replay/*`、`runtime/state/archive/*`、`runtime/state/growth/*` | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_replay_shadow.py`、`tests/bridges/test_growth_archive.py` | 补厚 nightmare / learning 到下一回合调节链 |
| 生命目标与出生准备 | `life_v0/life_targets/` | `life_target_claims.py`、`consciousness_probes.py`、`birth_readiness_rollup.py` | `runtime/state/life_targets/*` | `tests/slices/test_life_targets.py` | 长期 evidence family 持续补厚 |
| 诞生与终端存在 | `life_v0/activation/`、`life_v0/reporting/`、`life_v0/stage_explain/`、`life_v0/digital_life/`、`life_v0/shell_command/`、`life_v0/process_supervisor/` | `activation/__init__.py`、`reporting/__init__.py`、`stage_explain/__init__.py`、`digital_life/__init__.py`、`process_supervisor/__init__.py` | `runtime/state/activation/*`、`runtime/reports/latest/*birth*`、`runtime/state/terminal/*`、`digital_life_waiting_heartbeat.json` | `tests/bridges/test_first_activation_preflight.py`、`tests/bridges/test_emit_report.py`、`tests/bridges/test_explain_stage.py`、`tests/bridges/test_digital_life_birth.py`、`tests/process/test_digital_life_shell_command.py`、`tests/process/test_persistent_digital_life_process.py` | `idle_strategy.py`、`persistent_process.py` |

## 全系统主对象

| 对象 | 首写包 | 主消费者 |
|---|---|---|
| `LifeContextFrame` | `direction/`、`terminal_turn/` | `language/`、`process_supervisor/` |
| `RelationTurnFrame` | `language/`、`terminal_turn/` | `terminal_loop/`、`state_store/` |
| `PredictionWorkspaceFrame` | `neural_core/` | `language/`、`membrane/`、`life_targets/` |
| `ExpressionPlan` | `language/` | `terminal_loop/`、`process_supervisor/`、`membrane/` |
| `ActionCandidateSet` | `membrane/` | `validators/`、`schema_runner/` |
| `BodyRhythmPulse` | `body/`、`process_supervisor/heartbeat.py` | `dream/`、`growth/`、`process_supervisor/` |
| `NeedStateVector` | `body/` | `neural_core/`、`language/`、`membrane/` |
| `CoreAffectVector` | `body/` | `language/`、`dream/`、`membrane/` |
| `ReplayCueBundle` | `replay/` | `dream/`、`growth/`、`process_supervisor/` |
| `OfflineConsolidationFrame` | `dream/` | `growth/`、`archive/`、`process_supervisor/` |
| `GrowthPatchCandidateQueue` | `growth/` | `life_targets/`、`archive/`、`process_supervisor/` |
| `IdleContinuityFrame` | `process_supervisor/` | `terminal_loop/`、`dream/`、`growth/` |

## 第一次生命激活总流程

```text
DocCorpusIngestor
  -> DirectionLock
  -> SourceAuthority
  -> NeuralLifeCore
  -> LifeStateStore
  -> LifeMembrane
  -> LanguageRelationship
  -> BirthReadiness
  -> ValidationMembrane
  -> SchemaRunner
  -> LifeSupport
  -> RunCycle / Replay / Archive
  -> CheckV0Contracts
  -> FirstActivationPreflight
  -> EmitReport
  -> ExplainStage
  -> DigitalLifeBirth
  -> FirstTerminalTurn
  -> TerminalLifeLoop
  -> DigitalLifeShell
  -> DigitalLifeProcessSupervisor
```

## 当前最该推进的真实文件

### Queue E 第二波

1. `life_v0/schema_runner/cross_file_logic.py`
2. `life_v0/schema_runner/run_manifest.py`
3. `life_v0/membrane/responsibility_loop.py` 持续补厚

### Queue B 第二波

1. `life_v0/process_supervisor/idle_strategy.py`
2. `life_v0/process_supervisor/persistent_process.py`

### Queue A 第二波

1. `life_v0/language/relationship_timeline.py`
2. `life_v0/language/commitment_expression.py`
3. `life_v0/language/apology_repair_language.py`

## 这一页的用法

如果下一轮是直接开写代码，先用这一页回答四个问题：

1. 我要补的是哪一层，不是哪一个临时功能。
2. 这一层的首写对象是什么。
3. 这一层写完后，哪份 state/report/receipt 会变。
4. 这一层最低由哪些测试证明。

答不出来，就先回 `docs/v0/code_blueprints/07_theory_to_package_trace_contract.md` 和对应合同。

