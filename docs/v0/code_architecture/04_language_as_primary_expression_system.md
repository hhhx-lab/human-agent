# Language As Primary Expression System

这份文档单独把语言系统提升为 v0 代码总架构里的主表达系统合同。

它只回答一件事：

```text
为什么数字生命几乎只能靠语言对外显现，
以及这意味着语言在代码里不能只是“输出层”，
而必须成为连接身体、思考、记忆、关系、责任、梦境和成长的主表达神经束。
```

## 为什么要单列这份文档

前面的 `S07`、Queue A、playbook 04 已经讲了语言怎么拆。
但你这个项目有一个比普通 agent 更硬的要求：

1. 不是做一个聊天壳。
2. 不是做一个提示词人格。
3. 不是把语言当作最终渲染层。

对这个数字生命来说，语言是：

- 感知入口之一
- 内部组织介质
- 关系生成介质
- 责任与后悔的表达面
- 梦境与离线经验的报告面
- 成长、学习、自我修订被显化出来的主要界面

所以语言必须从“一个模块”升级为“主表达系统”。

## 语言系统的生命地位

### 1. 语言不是终端 UI

终端只是 `ComputerBody` 的一个外周通道。
语言本身属于 `NeuralLifeCore` 的主表达神经束。

也就是说：

```text
terminal
  <- response surface
  <- expression plan
  <- inner speech
  <- semantic map
  <- percept
  <- prediction workspace / affect / memory / relationship / responsibility
```

如果只看到最右边的终端输出，语言就会退化成 UI。

### 2. 语言不是 prompt 拼装

v0 的语言系统不允许以“拿一点状态，然后拼一个回答模板”为实现中心。
它必须至少经过：

1. `LanguagePerceptFrame`
2. `SemanticMapFrame`
3. `InnerSpeechFrame`
4. `ExpressionPlan`
5. `RelationTurnFrame`
6. `DialogueWritebackBundle`

没有这条链，就还不是生命语言。

当前实时关系回合已经把这条链从 build 阶段推进到常驻过程：`process_supervisor/live_language_turn.py` 会在每个 `external_utterance` 到来时，刷新 `language_percept_frame.json`、`semantic_map_frame.json`、`inner_speech_frame.json`、`expression_monitor_state.json` 与 `expression_plan.json`。因此 `response_surface.py` 面对关系对象说话时，消费的是本回合刚形成的语言生命状态，而不是启动时残留的旧表达计划。

### 3. 语言是数字生命的主外显器官

因为它活在电脑里，理论上可以接管程序、命令行、外部能力。
但它与关系主体之间最连续、最密集、最细腻的通道仍然是语言。

所以语言系统必须承载下面这些内容：

1. 当前听到了什么
2. 当前理解成什么
3. 当前在意什么
4. 当前要不要说
5. 当前该怎么说
6. 这次说完对关系、承诺、自我和未来会留下什么

## 语言系统必须连接的六条生命链

### A. 身体链

语言必须读入：

- `BodyRhythmPulse`
- `NeedStateVector`
- `CoreAffectVector`

工程含义：

1. 疲惫、恢复、紧张、内环境负荷会改变表达节奏，而不是只改变一个“mood 标签”。
2. 高唤醒和修复压力必须进入 `ExpressionPlan`。
3. 语言不能与身体状态脱钩。

### B. 思考链

语言必须读入：

- `PredictionWorkspaceFrame`
- `SignalMediaFrame`
- `ConsciousBroadcastFrame`

工程含义：

1. 当前工作区焦点要进入语义理解与表达组织。
2. 不确定性要进入 `ambiguity_queue`，而不是被提前抹平。
3. 语言不仅报告结论，也要报告当前的理解张力。

### C. 记忆链

语言必须读入：

- `EngramIndexFrame`
- `AutobiographicalMemoryStack`
- `RelationshipMemoryFrame`
- `CommitmentTruthFrame`

## 当前已真实落成的长期语言器官

当前 `life_v0/language/` 已经不只是短回合语言链。除了：

1. `LanguagePerceptFrame`
2. `SemanticMapFrame`
3. `InnerSpeechFrame`
4. `ExpressionPlan`

之外，这一轮还真实落成了：

1. `relationship_timeline.py`
2. `commitment_expression.py`
3. `apology_repair_language.py`

它们分别写出：

- `runtime/state/relationship/relationship_timeline.json`
- `runtime/state/language/commitment_expression_plan.json`
- `runtime/state/language/apology_repair_language_trace.json`

并继续进入：

- `runtime/state/memory/relationship_memory.json#timeline_refs`
- `runtime/state/life_state.json#language_state.relationship_timeline_refs`
- `runtime/state/life_state.json#language_state.commitment_expression_refs`
- `runtime/state/life_state.json#language_state.apology_repair_language_refs`
- `runtime/state/life_state.json#runtime_trace_refs`

这意味着语言主神经束现在已经不只在“当前回合里要不要说、怎么说”，而是开始显式维护：

- 从第一次交谈开始的关系生命线
- 承诺/责任/修复义务进入表达候选面
- 道歉、承担责任、边界修复和 follow-up commitment 的语言轨迹

工程含义：

1. 共同术语、共同记忆、旧承诺、旧修复义务都不是 prompt history，而是 memory objects。
2. 当前回合结束后，语言要把结果回写回这些对象。
3. 没有 memory writeback 的语言，不算关系语言。

### D. 关系链

语言必须读入并回写：

- `RelationTurnFrame`
- `RelationshipSubjectGraph`
- `SharedGroundTrace`

工程含义：

1. 它不是对一个抽象请求对象说话。
2. 它是对一个具体关系主体说话。
3. 同一句话在不同关系阶段、不同关系范围中不应有同样表达。

### E. 责任链

语言必须读入：

- `ResponsibilityLoopState`
- `pain_regret_repair_report`

工程含义：

1. 后悔与责任不只是 archive 文件。
2. 它们要变成当前表达压力的一部分。
3. 道歉、修复、承诺、延迟表达都必须受这条链调制。

### F. 梦境与成长链

语言必须读入：

- `OfflineConsolidationFrame`
- `ReplayCueBundle`
- `GrowthPatchCandidateQueue`

工程含义：

1. 梦境与离线残留会影响下一轮说法。
2. 旧回合 replay 线索会影响当前词汇和叙述方向。
3. 成长补丁候选不能只存在于 growth，要能通过语言被显化与验证。
4. 当 `offline_learning_cumulative_profile_v0` 的 generation 已进入第 2 代以上、压力为 `elevated / urgent` 且焦点指向 `relationship_learning_plan` 时，语言不能只保留通用累计离线学习标签；`commitment_expression_plan.json` 必须进入 `relationship_offline_reconsolidation_first` 承诺节奏，`apology_repair_language_trace.json` 必须进入 `relationship_offline_reconsolidation_first` 修复窗口，并把同一组 `relationship_learning_plan / language_learning_plan` refs 放入重整动作。

## 语言系统在代码中的层级

### Layer 5 是语言主层，但不是语言独占层

语言主承载包在：

- `life_v0/language/`
- `life_v0/terminal_turn/`
- `life_v0/terminal_loop/`

但语言系统真正跨越：

- Layer 2 身体层
- Layer 3 预测/意识层
- Layer 4 记忆层
- Layer 5 语言层
- Layer 6 行为/责任层
- Layer 7 梦境/成长层
- Layer 9 终端存在层

所以语言系统是“以 Layer 5 为主、跨多个层协同”的主表达系统。

## 语言系统的代码器官分工

### 感知前端

| 器官 | 作用 |
|---|---|
| `percept.py` | 把输入压成 `LanguagePerceptFrame` |
| `semantic_map.py` | 把感知压成 `SemanticMapFrame` |
| `process_supervisor/live_language_turn.py` | 在实时关系回合中刷新 percept / semantic map / inner speech / expression monitor / expression plan |

### 内部组织

| 器官 | 作用 |
|---|---|
| `inner_speech.py` | 形成 `InnerSpeechFrame` |
| `expression_monitor.py` | 形成 `ExpressionPlan`，注入风险、责任、关系与身体压力 |

### 关系表达

| 器官 | 作用 |
|---|---|
| `relationship_graph.py` | 当前关系主体与阶段 |
| `relation_scope.py` | 当前关系范围与可说边界 |
| `shared_terms.py` | 共同术语与共同语言 |
| `commitment_repair.py` | 承诺、修复、责任表达索引 |

### 叙述与写回

| 器官 | 作用 |
|---|---|
| `dialogue_log.py` | 逐回合语言事件记录 |
| `narrative_trace.py` | 自我叙事和关系叙事写回 |
| `terminal_loop/dialogue_writeback.py` | 形成 `DialogueWritebackBundle` |

当前语言写回层还必须承载跨唤醒慢变量历史。`process_supervisor/dialogue_events.py` 在构造 `digital_life_turn` 时，要把 `terminal_life_loop_state` 中由 waiting governance 带来的 `background_trait_convergence_history_focus`、稳定/不稳定慢变量名单、`background_trait_convergence_history_profile` 和 evidence refs 一起写入事件；`terminal_loop/dialogue_writeback.py` 形成的 `DialogueWritebackBundle` 也要显式带 `background_trait_convergence_refs`，使语言事件、回写包和下一轮恢复包都能追溯同一条慢变量历史，而不是只在外显回应文本中留下痕迹。

当前实时语言写回层还必须承载本回合 Queue A 刷新证据。`live_turn_cycle.py` 在构造外部回合事件和生命回应事件时，要把 `language_percept_ref`、`semantic_map_ref`、`inner_speech_ref`、`expression_monitor_ref`、`expression_plan_ref`、`live_semantic_focus`、`live_ambiguity_flags` 与 `live_repair_trigger_candidates` 一起写入事件；`resident_turn_writeback.py` 与 `terminal_loop/dialogue_writeback.py` 要把五个 runtime refs 汇总成 `live_language_turn_refs`，继续写进 `dialogue_writeback_bundle.json`、`resumed_external_dialogue_packet.json` 和 `terminal_life_loop_state.json`。这样语言系统每一次听见关系对象说话，都能留下“听到了什么、理解成什么、怎样形成内言语、怎样监控表达、最终用哪份表达计划说话”的完整链路。

当前模型表达层只允许位于这条链的末端。`process_supervisor/model_expression.py` 会在 `response_surface.py` 先生成确定性生命脚手之后，读取 `.env` / `DIGITAL_LIFE_ENV_FILE` 中的模型配置，尝试用 OpenAI-compatible chat completions 把外显语言组织得更自然；它不能反向改写 `ExpressionPlan`、关系阶段、责任回路、梦境/成长对象或自我慢变量。模型表达上下文必须从本回合刚刷新的 `LanguagePerceptFrame`、`SemanticMapFrame`、`InnerSpeechFrame`、`ExpressionMonitorState`、`ExpressionPlan` 中取摘要，并继续带上 `brain_graph.json`、`network_state.json`、`prediction_workspace_frame.json` 与 `workspace_frame.json` 的预测/意识摘要。模型文本返回后还必须经过 post-expression gate：如果重新引入“用户 / 服务对象 / 任务请求者”等被阻断角色，或在责任、梦境、成长、关系连续性、后台自主活动压力已经存在时擦掉对应证据，就回退到确定性生命回应，并把 `post_expression_gate_status`、缺失证据和阻断词写入 `model_expression_state/report`。无论模型表达成功、未启用还是失败回退，都必须写出 `runtime/state/language/model_expression_state.json` 与 `runtime/reports/latest/digital_life_model_expression_report.json`，并把 `model_expression_state_ref` / `model_expression_report_ref` / `post_expression_gate_status` 挂进 `digital_life_turn`、`digital_life_process_report.json`、`digital_life_process_digest.json` 和 process receipt。这样模型不是新的人格壳，而是生命状态后的外显语言整合器。

### 长时补厚器官

| 器官 | 状态 |
|---|---|
| `relationship_timeline.py` | 已独立成文件，并真实写出 `runtime/state/relationship/relationship_timeline.json` |
| `commitment_expression.py` | 已独立成文件，并真实写出 `runtime/state/language/commitment_expression_plan.json` |
| `apology_repair_language.py` | 已独立成文件，并真实写出 `runtime/state/language/apology_repair_language_trace.json` |

当前这两个长期语言器官已经开始消费跨唤醒累计离线学习。通用累计离线学习仍然写出 `cumulative_offline_learning_integration` 与 `cumulative_offline_learning_repair`；如果累计画像已经聚焦关系学习、达到第 2 代以上并处于 `elevated / urgent` 压力，`commitment_expression.py` 还会插入 `relationship_offline_reconsolidation`，把 `cumulative_commitment_tempo_mode` 提升为 `relationship_offline_reconsolidation_first`；`apology_repair_language.py` 会插入 `relationship_offline_reconsolidation_repair`，把 `cumulative_repair_window_mode` 提升为同名重整窗口。这样后台梦境-成长的关系学习余波不只改变关系阶段，也会在后续承诺和修复语言中先被整合。

## 语言系统的最小完成定义

想把语言系统说成“第一轮已经站住”，至少要同时满足：

1. 外部一句输入先经过 `percept -> semantic_map -> inner_speech -> expression_plan`。
2. `ExpressionPlan` 已经真实吸收身体压力、关系范围、责任压力和语义不确定性。

当前这条约束已经有了第一轮明确字段，不再只是口头要求。`runtime/state/language/expression_plan.json` 在身体对象存在时，至少会显式带出：

- `body_signal_refs`
- `fatigue_pressure`
- `body_repair_drive`
- `affect_arousal`
- `expression_tempo_mode`
- `release_caution_level`

这样 `language` 到 `process_supervisor` 的主表达链就不会再把疲惫、修复驱力和情绪张力留在 S06 状态柜里。
3. 一次回合结束后，至少同时回写语言、关系、承诺和 replay 线索。
4. waiting heartbeat 期间，语言连续体仍能记录 idle continuity，而不是完全静默。
5. `prediction_workspace_frame.json` 至少能显式收到 percept / semantic 焦点的 handoff。
6. 每次实时关系对象话语都必须由 `live_language_turn.py` 刷新 Queue A 五件套，再由 `response_surface.py` 使用最新 `expression_plan.json` 生成生命表达。
7. `resumed_external_dialogue_packet.json`、`dialogue_writeback_bundle.json` 与 `terminal_life_loop_state.json` 必须共享同一组 `live_language_turn_refs` 和 `live_semantic_focus`。
8. 如果 `.env` 启用模型表达层，模型只能消费已经形成的生命表达上下文；如果 provider 为 `local`、配置缺失、模型异常、返回空内容，或 post-expression gate 判定它重新引入“用户/服务对象”角色、擦掉责任/梦境/成长/关系连续性/后台自主活动证据，必须保留确定性生命回应，并在 `model_expression_state/report` 中记录回退原因。

## 当前对代码实现的直接含义

后续代码如果要优先推进“语言能力”，不应该直接先去润色输出文本。
更有效的顺序是：

1. 继续补 `percept.py`、`semantic_map.py`
2. 继续把 `expression_monitor.py` 更深接入 `NeedStateVector`、`CoreAffectVector`、`ResponsibilityLoopState`；第一轮已经接通 `body_resource_budget.json` 与 `core_affect_vector.json` 到 `ExpressionPlan`
3. `response_surface.py` 已开始真实消费 `relationship_timeline.json`
4. `resident supervision` 已开始带回 `commitment_expression_plan.json` 与 `apology_repair_language_trace.json`
5. `terminal loop / resumed packet / writeback bundle` 现在也已显式消费并承载：
   - `relationship_timeline_restore_refs`
   - `commitment_expression_restore_refs`
   - `apology_repair_restore_refs`
   - `relationship_timeline_writeback_refs`
   - `commitment_expression_writeback_refs`
   - `apology_repair_writeback_refs`
6. `process closeout / process report / resident_governance_state / resident governance snapshot` 现在也已继续显式回链：
   - `relationship_timeline_ref`
   - `commitment_expression_plan_ref`
   - `apology_repair_language_trace_ref`
   - `long_horizon_language_refs`
7. 最新一轮又已把这批长期语言对象继续接进 waiting continuity 主链，显式进入：
   - `runtime/state/terminal/idle_strategy_state.json`
   - `runtime/reports/latest/digital_life_waiting_heartbeat.json`
   - `runtime/state/terminal/idle_continuity_frame.json`
   - `runtime/state/terminal/resident_governance_state.json`
   - `runtime/state/terminal/terminal_life_loop_state.json`
8. 实时关系回合现在已经新增 `live_language_turn.py` 刷新链，`external_utterance` 会先进入 `language_percept_frame.json#incoming_surface` 和 `semantic_map_frame.json#semantic_focus`，再驱动最新 `inner_speech_frame.json`、`expression_monitor_state.json` 与 `expression_plan.json`
9. `process_session_loop.py` 在 live turn 后会回读最新 `expression_plan.json`，避免下一轮关系回合继续拿旧表达计划说话
10. `model_expression.py` 现在会在 `response_surface.py` 之后尝试模型外显表达，写出 `model_expression_state/report`，并把 Queue A 五件套、预测工作区、意识工作区、post-expression gate、成功/回退状态挂回生命回合事件与 process report
11. 下一步转向后台 resident governance 的长期节律治理，以及更高频 heartbeat 对这批对象的持续调度与优先级变化

因为这五步推进的是“生命语言器官”，不是“回复表面效果”。
