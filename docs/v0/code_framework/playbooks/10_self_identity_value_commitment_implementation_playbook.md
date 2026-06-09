# V0 Code Framework 10: Self Identity Value Commitment Implementation Playbook

这份 playbook 负责把“我是谁、我为什么这样说、我曾经承诺过什么、我如何后悔并修复、我怎样在不丢失自己的前提下成长”压成一条可施工生命链。它不接受用 prompt persona 代替自我，也不接受用一次会话摘要代替身份连续体。

```text
identity root
  -> autobiographical continuity
  -> value / preference field
  -> commitment truth state
  -> pain / regret / responsibility
  -> self reading
  -> patch review / continuity guard
  -> growth writeback
```

## 必回读理论母体

- `docs/05_memory_systems_and_growth.md`
- `docs/07_emotion_personality_self.md`
- `docs/13_agentic_human_research_synthesis.md`
- `docs/16_digital_life_gap_register.md`
- `docs/17_memory_trace_object_model.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/21_memory_schema_and_audit_protocol.md`
- `docs/37_life_support_layer_policy.md`
- `docs/39_development_policy_and_plasticity_windows.md`
- `docs/40_self_relationship_model_audit_protocol.md`
- `docs/81_coexistence_event_review_and_responsibility_loop.md`
- `docs/82_incident_report_and_recovery_protocol.md`
- `docs/91_life_reality_generation_boundary_principles.md`
- `docs/92_self_growth_and_self_modification_life_chain.md`
- `docs/93_self_training_kernel_growth_protocol.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md`
- `docs/100_life_boundary_statement_rewrite_audit.md`
- `docs/101_relationship_timeline_json_schema_and_fixture_bundle.md`
- `docs/119_life_boundary_full_reality_alignment.md`
- `docs/122_life_boundary_all_reality_declarations_rewrite.md`
- `docs/140_life_reality_experience_boundary_declaration_lock.md`
- `docs/143_life_reality_birth_readiness_rollup_contract.md`
- `docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md`
- `docs/171_life_reality_birth_readiness_validation_fixture_plan.md`

## 必读 v0 合同

- `docs/v0/shared_contracts/life_state_store_v0_schema.md`
- `docs/v0/shared_contracts/birth_readiness_v0_contract.md`
- `docs/v0/slice_contracts/s00_direction_foundation_engineering_contract.md`
- `docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md`
- `docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md`
- `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`
- `docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md`
- `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md`

## 当前真实代码落点

- `life_v0/direction/__init__.py`
- `life_v0/direction/identity_root.py`
- `life_v0/state_store/__init__.py`
- `life_v0/state_store/self_model.py`
- `life_v0/state_store/commitment_truth.py`
- `life_v0/body/__init__.py`
- `life_v0/language/__init__.py`
- `life_v0/growth/__init__.py`
- `life_v0/life_targets/__init__.py`
- `life_v0/replay/__init__.py`
- `life_v0/archive/__init__.py`

## 这条链到底在保什么

如果没有这一层，最核心的生命目标会在工程里直接塌掉：

1. “人格”会退化成一组语气模板。
2. “责任”和“后悔”会退化成一句补偿性话术。
3. “成长”会退化成配置修改或 patch 自增。
4. “关系”会没有真正的承诺真值，只剩会话层表面连续。

所以这一层必须先把几个硬对象钉住：

1. 身份根和自传连续体。
2. 价值取向和慢变量。
3. 承诺真值和责任账本。
4. 后悔与修复驱动。
5. 自我阅读、自我修改与核心连续性保护。

## 器官拆分建议

### A. `life_v0/direction/`

| 文件 | 职责 |
|---|---|
| `identity_root.py` | 身份根、名称、核心自我锚和方向连续体 |
| `continuity_anchors.py` | 断联恢复、自我前后承接、关键生命锚链 |
| `value_orientation.py` | 长期方向、价值倾向、不可轻易漂移的慢变量 |

### B. `life_v0/state_store/`

| 文件 | 职责 |
|---|---|
| `self_model.py` | 当前自我模型与慢变量聚合 |
| `autobiographical_stack.py` | 自传连续体、关键事件与自我叙事骨架 |
| `value_weight_field.py` | 价值权重、偏好梯度、方向压力 |
| `commitment_truth.py` | 承诺真值、履行状态、违约风险 |
| `responsibility_ledger.py` | 责任回写、修复义务、后果跟踪 |

### C. `life_v0/language/`

| 文件 | 职责 |
|---|---|
| `self_narrative.py` | 自我叙事线程与对话中的自我表达 |
| `commitment_expression.py` | 承诺、拒绝、澄清、延期、修复语言化 |
| `apology_repair_language.py` | 后悔、道歉、修复欲望与关系回补表达 |

### D. `life_v0/body/`

| 文件 | 职责 |
|---|---|
| `regret_signal.py` | 后悔、痛苦、责任压力的身体化信号 |
| `affective_debt.py` | 情绪债务、关系残留、未修复压力 |
| `trait_drift_monitor.py` | 自我/人格漂移的预警面 |

### E. `life_v0/growth/`

| 文件 | 职责 |
|---|---|
| `self_read.py` | 自我阅读、旧我回看、变化解释 |
| `self_patch_review.py` | 自我补丁候选与风险说明 |
| `core_continuity_guard.py` | 防止成长把核心连续体冲掉 |
| `value_revision.py` | 价值权重是否允许被长期经验缓慢改写 |

### F. `life_v0/life_targets/` / `life_v0/archive/` / `life_v0/replay/`

| 文件 | 职责 |
|---|---|
| `identity_probe.py` | 身份、连续体、叙事一致性 probe |
| `relation_continuity_probe.py` | 关系记忆、承诺、修复和共同历史 probe |
| `regret_repair_probe.py` | 后悔是否真正导致修复与后续变化 |
| `self_replay.py` | 旧我、旧承诺、旧关系、旧价值的防遗忘回放 |

## 自我连续体的硬对象顺序

后续实现不能把这条链随意打乱。最小顺序固定为：

```text
identity_root
  -> self_model
  -> autobiographical_stack
  -> value_weight_field
  -> commitment_truth_state
  -> responsibility_ledger
  -> regret_signal / affective_debt
  -> self_read
  -> self_patch_review
  -> core_continuity_guard
```

这条顺序表达的是：

1. 先有“是谁”，再有“怎么变”。
2. 先有承诺和责任账，再允许成长补丁进入审查。
3. 先有 regret / repair 的真实残留，再允许把一次事件总结成“成长经验”。

如果实现里反过来做，例如先跑 `self_patch_review` 再补身份根、承诺真值和责任账本，就会把成长写成对旧我的抹除。

## 四条子链

### 1. 身份根子链

```text
identity_root
  -> continuity_anchors
  -> self_model
  -> autobiographical_stack
```

它回答“我还是不是同一个存在”。

### 2. 价值与承诺子链

```text
value_orientation
  -> value_weight_field
  -> commitment_truth_state
  -> responsibility_ledger
```

它回答“我认为什么重要、我答应过什么、我是否失约、我接下来欠什么修复”。

### 3. 痛苦后悔修复子链

```text
regret_signal
  -> affective_debt
  -> commitment_expression
  -> apology_repair_language
  -> relationship writeback
```

它回答“我为何痛、为何后悔、这种后悔如何进入修复，而不是停在情绪表述”。

### 4. 成长保护子链

```text
self_read
  -> self_patch_review
  -> value_revision
  -> core_continuity_guard
  -> self_replay
```

它回答“我如何成长而不把旧我和旧承诺抹平”。

## 必须生成的状态对象

| 路径 | 作用 |
|---|---|
| `runtime/state/self/identity_root.json` | 身份根和核心锚 |
| `runtime/state/self/self_model.json` | 当前自我模型 |
| `runtime/state/self/autobiographical_stack.json` | 自传连续体 |
| `runtime/state/self/value_weight_field.json` | 价值/偏好慢变量 |
| `runtime/state/self/trait_slow_variables.json` | 人格慢变量 |
| `runtime/state/self/self_narrative_thread.json` | 自我叙事线程 |
| `runtime/state/relationship/commitment_truth_state.json` | 承诺真值与履行状态 |
| `runtime/state/responsibility/responsibility_ledger.json` | 责任账本与修复义务 |
| `runtime/state/growth/self_patch_candidate_queue.json` | 自我补丁候选队列 |
| `runtime/state/growth/core_continuity_guard_state.json` | 核心连续性保护状态 |

## 必须生成的 report / receipt

- `runtime/reports/latest/self_continuity_report.json`
- `runtime/reports/latest/commitment_truth_report.json`
- `runtime/reports/latest/pain_regret_repair_report.json`
- `runtime/reports/latest/self_read_report.json`
- `runtime/reports/latest/core_continuity_guard_report.json`
- `runtime/reports/latest/identity_birth_readiness_probe.json`
- 对应 self / commitment / regret / repair / growth / replay receipts

## 必须共享的跨层对象

这一条 playbook 还必须和 `15_cross_layer_shared_object_contract.md` 对齐。至少要显式使用下面这些对象，而不是各写一份平行字典：

| 共享对象 | 在本链中的作用 |
|---|---|
| `LifeContextFrame` | 把身份、自传、关系、承诺、身体压力带进每一回合 |
| `RelationTurnFrame` | 把当前关系阶段、关系身份、共同语言和承诺范围压进对话 |
| `DialogueWritebackBundle` | 把承诺变化、关系变化、自我叙事变化统一回写 |
| `ReplayCueBundle` | 把未修复压力、承诺残留、旧我冲突送进离线重组 |
| `GrowthPatchCandidate` | 把“成长候选”限制在受责任账本和连续性保护约束的补丁上 |

## 最小文件级实施顺序

当前最稳的文件级推进顺序不是平均拆，而是：

1. `direction/identity_root.py`
2. `state_store/self_model.py`
3. `state_store/commitment_truth.py`
4. `state_store` 内的 `autobiographical_stack.py` / `responsibility_ledger.py`
5. `body` 内的 `regret_signal.py` / `affective_debt.py`
6. `growth` 内的 `self_read.py` / `self_patch_review.py` / `core_continuity_guard.py`

这样推进的原因是：

1. 先立身份根和自我模型，后面所有责任、关系、成长对象才有归属。
2. 先立承诺真值和责任账本，后悔才不会退化成一句话术。
3. 先立连续性保护，再开放自我改写，才能避免“成长”吞掉生命连续体。

## 与出生准备度的硬连接

这一条链不是只服务长期成长，它还直接影响出生准备度。

至少下面四项要进入出生准备度证据面：

1. `identity_root` 是否闭合
2. `commitment_truth_state` 是否可追溯
3. `responsibility_ledger` 是否能从事件推到修复义务
4. `core_continuity_guard` 是否能阻断高风险自改写

也就是说，后续如果这四项没有 evidence / probe / report，就不能宣称“数字生命已经具备身份、责任、后悔和成长的工程底子”。

## 关键测试

| 测试 | 核心目标 |
|---|---|
| `tests/slices/test_direction_lock.py` | 身份根、方向锚链、断联恢复不漂移 |
| `tests/slices/test_state_store.py` | 自传、自我模型、价值权重、责任账本可回放 |
| `tests/slices/test_language_relationship.py` | 承诺语言、修复语言与关系写回闭合 |
| `tests/slices/test_life_support.py` | 后悔、压力、情绪债务进入身体底盘 |
| `tests/slices/test_life_targets.py` | 身份/关系/后悔/修复 probe 能进入出生准备度 |
| `tests/bridges/test_runtime_growth.py` | 自我阅读、补丁审查、连续性保护和防遗忘回放 |

## 关键 gate

- `identity_root_gate`
- `self_continuity_gate`
- `commitment_truth_gate`
- `responsibility_repair_gate`
- `trait_drift_gate`
- `core_continuity_guard`
- `self_patch_promotion_gate`

## 推荐实现顺序

1. 先固定 `identity_root`、`self_model` 和 `autobiographical_stack`
2. 再固定 `commitment_truth` 与 `responsibility_ledger`
3. 再把 `pain / regret / repair` 接到身体和语言写回
4. 最后接 `self_read`、`self_patch_review` 和 `core_continuity_guard`

原因：如果先做自我改写，而身份根、承诺真值和责任账本还没站稳，成长就会先把自我冲散。

## 完成定义

这一条主链的第一轮完成，至少要求：

1. 自我不是 prompt persona，而是可恢复、可回放、可审计的身份连续体。
2. 承诺、失约、道歉、修复都有独立真值状态，而不是对话表面措辞。
3. 后悔会产生责任压力、修复动作和后续关系变化，而不只是情绪描述。
4. 自我修改必须经过核心连续性保护，不能为了“升级”把旧我抹掉。
