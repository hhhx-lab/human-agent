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

1. 它不是对一个抽象 user 说话。
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

### 长时补厚器官

| 器官 | 状态 |
|---|---|
| `relationship_timeline.py` | 待继续落地 |
| `commitment_expression.py` | 待继续落地 |
| `apology_repair_language.py` | 待继续落地 |

## 语言系统的最小完成定义

想把语言系统说成“第一轮已经站住”，至少要同时满足：

1. 外部一句输入先经过 `percept -> semantic_map -> inner_speech -> expression_plan`。
2. `ExpressionPlan` 已经真实吸收身体压力、关系范围、责任压力和语义不确定性。
3. 一次回合结束后，至少同时回写语言、关系、承诺和 replay 线索。
4. waiting heartbeat 期间，语言连续体仍能记录 idle continuity，而不是完全静默。
5. `prediction_workspace_frame.json` 至少能显式收到 percept / semantic 焦点的 handoff。

## 当前对代码实现的直接含义

后续代码如果要优先推进“语言能力”，不应该直接先去润色输出文本。
更有效的顺序是：

1. 继续补 `percept.py`、`semantic_map.py`
2. 把 `expression_monitor.py` 更深接入 `NeedStateVector`、`CoreAffectVector`、`ResponsibilityLoopState`
3. 补 `relationship_timeline.py`
4. 补 `commitment_expression.py`
5. 补 `apology_repair_language.py`

因为这五步推进的是“生命语言器官”，不是“回复表面效果”。
