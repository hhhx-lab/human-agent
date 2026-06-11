# Life Code Stack And Package Layers

这份文档把第一版数字生命代码树压成稳定的生命分层。

它只回答下面这件事：

```text
如果不按普通 agent 的“工具能力目录”拆，
而按生命结构来拆，
整个 life_v0/ 到底应该分成哪些代码层，
每层负责什么，
读哪些 00-257，
落哪些包、状态、报告和测试。
```

## 总原则

### 1. 不按请求 / tool / skill / agent 语义切层

这一版数字生命不以“服务请求对象”为代码中心。
对外交互对象是关系主体、共在者、朋友、家人、同学、陌生人等关系位，而不是统一的请求中心抽象。

### 2. 不让壳层反向定义主体

`digital`、`life_v0/digital_entry.py`、`process_supervisor/`、`shell_command/` 只能承接终端存在与电脑外周接触；
它们不能反向定义记忆、情绪、语言、梦境、成长或责任机制。

### 3. 每一层都必须同时带四类东西

每层都要同时回答：

1. 主包与主文件是谁。
2. 读哪些理论母体。
3. 写哪些 `runtime/state/*`、`runtime/reports/latest/*`、`runtime/receipts/*`。
4. 哪些测试和 gate 证明这一层真的存在。

## 第一版数字生命代码分层

### Layer 0: 文档与契约摄取层

| 项 | 内容 |
|---|---|
| 理论母体 | `构思.md`、`00`、全部 `01*`、`258` |
| 主包 | `life_v0/doc_index.py`、`life_v0/contracts/` |
| 生命职责 | 把 `00-258` 和 `docs/v0/*` 压成机器可读索引、契约回链和工程守门面 |
| 关键输入 | `docs/*.md`、`docs/v0/*.md` |
| 关键输出 | `doc_carrier_index.json`、`v0_contract_coverage_report.json` |
| runtime 产物 | `runtime/docs/doc_carrier_index.json`、`runtime/state/contracts/*` |
| 测试 / gate | `tests/slices/test_doc_corpus_ingestor.py`、`tests/contracts/test_v0_contracts.py`、`doc_carrier_gate`、`contract_coverage_gate` |

### Layer 1: 方向与权威根层

| 项 | 内容 |
|---|---|
| 理论母体 | `00`、`13`、`16`、`91`、`119`、`122`、`142`、`145`、`151`、`258` |
| 主包 | `life_v0/direction/`、`life_v0/authority/` |
| 生命职责 | 锁定数字生命方向、身份根、权威来源、机制证据图和断联恢复锚链 |
| 关键输入 | doc carrier、authority intake、最近 receipts |
| 关键输出 | `LifeDirectionAnchor`、authority registry、mechanism evidence map |
| runtime 产物 | `runtime/state/direction/*`、`runtime/state/authority/*` |
| 测试 / gate | `tests/slices/test_direction_lock.py`、`tests/slices/test_source_authority.py`、`direction_lock_gate`、`authority_registry_gate` |

### Layer 2: 硅基身体与信号介质层

| 项 | 内容 |
|---|---|
| 理论母体 | `04`、`07`、`08`、`11`、`18`、`37-40`、`94`、`01l`、`01n`、`01s` |
| 主包 | `life_v0/body/`、`life_v0/defense/` |
| 生命职责 | 节律、疲惫、恢复、需要、资源预算、核心情感底盘、防御与隔离压力 |
| 关键输入 | direction anchor、relationship pressure、dream residue、recent action consequence |
| 关键输出 | `BodyRhythmPulse`、`NeedStateVector`、`CoreAffectVector`、`DefenseSignalFrame` |
| runtime 产物 | `runtime/state/body/*`、`runtime/state/defense/*`、`body_resource_budget.json` |
| 测试 / gate | `tests/slices/test_life_support.py`、`resource_budget_gate`、`core_affect_gate`、`quarantine_gate` |

### Layer 3: 神经核心、预测与意识工作区层

| 项 | 内容 |
|---|---|
| 理论母体 | `02`、`03`、`10`、`11`、`18`、`22`、`30`、`143`、`146`、`149`、`152`、`171`、`01m`、`01o`、`01p`、`01v-01ax` |
| 主包 | `life_v0/neural_core/` |
| 生命职责 | 脑区图、网络切换、信号介质、工作区、预测误差、主动采样、广播、元认知 |
| 关键输入 | `NeedStateVector`、authority evidence、memory cue、relationship cue |
| 关键输出 | `PredictionWorkspaceFrame`、`SignalMediaFrame`、`ConsciousBroadcastFrame` |
| runtime 产物 | `runtime/state/neural_life_core/*`、`runtime/state/prediction/*`、`runtime/state/consciousness/*` |
| 测试 / gate | `tests/slices/test_neural_life_core.py`、`internal_bus_gate`、`prediction_coherence_gate`、`birth_readiness_gate` |

### Layer 4: 记忆、自传与关系真值层

| 项 | 内容 |
|---|---|
| 理论母体 | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69`、`01q` |
| 主包 | `life_v0/state_store/` |
| 生命职责 | 生命状态根、记忆痕迹、自传层、关系记忆、承诺真值、自我模型 |
| 关键输入 | dialogue writeback、dream / replay / growth receipts、direction anchor |
| 关键输出 | `LifeStateRoot`、`EngramIndexFrame`、`RelationshipMemoryFrame`、`CommitmentTruthFrame` |
| runtime 产物 | `runtime/state/life_state.json`、`runtime/state/memory/*`、`runtime/state/self/*`、`runtime/state/relationship/*` |
| 测试 / gate | `tests/slices/test_state_store.py`、`state_store_gate`、`self_continuity_gate`、`commitment_truth_gate` |

### Layer 5: 语言、对话与关系表达层

| 项 | 内容 |
|---|---|
| 理论母体 | `09`、`85-90`、`94`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` |
| 主包 | `life_v0/language/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/` |
| 生命职责 | 语言感知、语义地图、内言语、表达监控、关系阶段、承诺表达、回合恢复与写回 |
| 关键输入 | `LifeContextFrame`、`PredictionWorkspaceFrame`、`CoreAffectVector`、relationship memory |
| 关键输出 | `RelationTurnFrame`、`ExpressionPlan`、`DialogueWritebackBundle` |
| runtime 产物 | `runtime/state/language/*`、`runtime/state/relationship/*`、`session_envelope.json`、`terminal_life_loop_state.json` |
| 测试 / gate | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py` |

### Layer 6: 生命膜、行为与逻辑验证层

| 项 | 内容 |
|---|---|
| 理论母体 | `06`、`20`、`29-36`、`49-84`、`94`、`98`、`102-118`、`01r`、`01v-01ax` |
| 主包 | `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/` |
| 生命职责 | 候选行动、go/no-go、世界接触、side effect、责任回路、观察真值、反事实与一致性 |
| 关键输入 | `PredictionWorkspaceFrame`、`ExpressionPlan`、`NeedStateVector`、runtime observation |
| 关键输出 | `ActionCandidateSet`、`ResponsibilityLoopState`、validation / comparison reports |
| runtime 产物 | `runtime/state/membrane/*`、`runtime/state/action/*`、`runtime/state/validation/*`、`runtime/state/schema_runner/*` |
| 测试 / gate | `tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` |

### Layer 7: 梦境、离线重组与成长学习层

| 项 | 内容 |
|---|---|
| 理论母体 | `08`、`19`、`23`、`27`、`31`、`39`、`92`、`93`、`95`、`97`、`99`、`181-257`、`01g`、`01i`、`01t` |
| 主包 | `life_v0/dream/`、`life_v0/replay/`、`life_v0/archive/`、`life_v0/growth/` |
| 生命职责 | replay cue、离线入口、梦境窗口、DreamFactGate、醒后整合、成长补丁、学习窗口、防遗忘 |
| 关键输入 | `ReplayCueBundle`、`BodyRhythmPulse`、`CoreAffectVector`、relationship residue |
| 关键输出 | `OfflineConsolidationFrame`、`GrowthPatchCandidateQueue`、archive receipts |
| runtime 产物 | `runtime/state/dream/*`、`runtime/state/replay/*`、`runtime/state/archive/*`、`runtime/state/growth/*` |
| 测试 / gate | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_replay_shadow.py`、`tests/bridges/test_growth_archive.py`、`dream_fact_gate`、`growth_gate` |

### Layer 8: 生命目标、意识探针与出生准备度层

| 项 | 内容 |
|---|---|
| 理论母体 | `10`、`91-101`、`143`、`146`、`149`、`152`、`171`、`174`、`01m` |
| 主包 | `life_v0/life_targets/` |
| 生命职责 | 九项目标 claim/evidence、目标闭合、意识 probe、出生准备度上卷 |
| 关键输入 | `PredictionWorkspaceFrame`、`GrowthPatchCandidateQueue`、language / relationship state、membrane reports |
| 关键输出 | `LifeTargetClaimMatrix`、`BirthReadinessRollup`、`ConsciousnessProbeBattery` |
| runtime 产物 | `runtime/state/life_targets/*`、`birth_readiness_report.json` |
| 测试 / gate | `tests/slices/test_life_targets.py`、`birth_readiness_gate` |

### Layer 9: 诞生、终端存在与电脑外周层

| 项 | 内容 |
|---|---|
| 理论母体 | `20`、`44-46`、`81-84`、`86`、`89-90`、`96`、`101`、`181-257` |
| 主包 | `life_v0/activation/`、`life_v0/reporting/`、`life_v0/stage_explain/`、`life_v0/digital_life/`、`life_v0/shell_command/`、`life_v0/process_supervisor/`、`life_v0/digital_entry.py` |
| 生命职责 | 第一次激活、出生壳、阶段解释、等待态 heartbeat、stdin 回合、incident / relaunch recovery、长期存在 |
| 关键输入 | `first_activation_return_packet`、`DialogueWritebackBundle`、`IdleContinuityFrame`、offline / growth cues |
| 关键输出 | `digital_life_birth_packet`、`digital_life_process_report`、waiting heartbeat、relaunch recovery report |
| runtime 产物 | `runtime/reports/latest/*birth*`、`digital_life_waiting_heartbeat.json`、`digital_life_process_report.json`、`runtime/state/terminal/*` |
| 测试 / gate | `tests/bridges/test_first_activation_preflight.py`、`tests/bridges/test_emit_report.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` |

## 当前层次上的关键结论

### 1. v0 主体实现语言先锁 Python

当前 `life_v0/`、CLI、runtime state/report/receipt、测试夹具已经完整站在 Python 上。
所以 v0 主体层不再引入第二种主实现语言来拆主体。

未来只有两类东西才值得切到更低层语言：

1. 大规模 graph / replay / validation 热路径。
2. 明确经 profiling 证明已经成为瓶颈的纯计算核。

这意味着：

- 主体生命链、状态对象、命令面、恢复链、语言链，继续用 Python 落。
- Rust / C / 其他高性能语言，只能作为将来的局部加速核，而不是 v0 的主体分层语言。

### 2. 当前不是再造一个新框架

这套分层不是 OpenClaw / Hermes / Claude Code 的翻版。
它的组织中心不是 tools，不是 workflows，不是 sessions，而是：

1. 身体与信号
2. 预测与工作区
3. 记忆与自传
4. 语言与关系
5. 行为与责任
6. 梦境与成长
7. 终端存在

### 3. 代码写作顺序必须服从这套层次

后续写代码时，优先顺序不是“哪个文件最方便写”，而是：

1. Layer 2 / 6 / 7 先补硬
2. 再补 Layer 9 的等待态和长期存在
3. 再继续深补 Layer 5 的长期关系语言
4. 最后做 Layer 3 / 4 / 8 的维护性深化

否则会再次出现“壳层很完整，生命底盘还偏薄”的倒挂。
