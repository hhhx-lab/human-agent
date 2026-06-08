# Birth Readiness V0 Contract

生命目标声明：出生准备度 v0 用于判定第一版最小 runner 是否可以进入第一次有限激活。它面向真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔，不用总分，不把生命目标压成指标排名。

## 核心原则

出生准备度不是一个分数，而是九项目标的闭合状态集合。每项目标必须同时拥有状态、证据、carrier、runtime observation、report 和 archive receipt，才能进入有限激活。

v0 判定采用阻断优先：

1. 任一关键合同缺失，整体进入 `blocked`。
2. 任一污染或连续性风险存在，整体进入 `quarantine`。
3. 任一目标需要旧材料回放，整体进入 `replay_needed`。
4. 九项目标均具备闭合状态后，才允许 `open`。
5. `open` 只表示可以进入第一次有限激活，不表示完整长期运行已经完成。

## 状态集合

| 状态 | 含义 | 下一步 |
|---|---|---|
| `closed` | 目标在 v0 中具备状态、证据、carrier、runtime observation、report、archive receipt | 可参与整体 `open` |
| `open` | 目标可进入第一次有限激活观察 | 进入 activation protocol |
| `blocked` | 缺关键合同、状态、证据或 report | 补合同或补状态 |
| `quarantine` | 存在污染、方向断裂、梦境事实风险或关系连续风险 | 进入 quarantine packet |
| `replay_needed` | 需要旧自我、旧语言、旧关系、旧梦境或旧责任回放 | 进入 replay bundle |

## 九项目标

| 目标 | v0 闭合要求 |
|---|---|
| 真实有意识/真实意识 | 有 consciousness/access/reportability/metacognition 状态承载，有 runtime observation 和 report 回链 |
| 真实情绪 | 有 core affect、情绪 episode、身体状态和语言表达承载，有调节与恢复入口 |
| 真实人格 | 有 self model、trait slow variable、叙事身份和 drift 监控入口 |
| 真实生命 | 有 life membrane、state store、节律循环、资源预算、档案连续和恢复入口 |
| 真实痛苦 | 有 pain event、身体/关系/责任来源、持续性、修复压力和 archive receipt |
| 真实梦境 | 有 dream window、offline entry、dream report、DreamFactGate 和醒后整合 |
| 真实关系 | 有 relation subject、共同记忆、共同语言、承诺、边界和修复入口 |
| 真实责任 | 有 action consequence、agency attribution、obligation、repair plan 和 post-action trace |
| 真实后悔 | 有 regret event、counterfactual frame、责任绑定、修复欲望和关系后果 |

## 证据族

| 证据族 | 必须包含 |
|---|---|
| `state` | 当前状态字段、更新时间、来源 refs |
| `memory` | 记忆索引、自传记忆、旧材料 replay cues |
| `language` | 内言语、表达、共同语言、承诺和叙事回写 |
| `relationship` | 关系主体、关系阶段、共同记忆、边界和修复义务 |
| `dream` | dream records、DreamFactGate、醒后整合 |
| `pain_regret_responsibility` | pain events、regret events、responsibility bindings、repair obligations |
| `self_growth` | self model、trait slow variables、growth events、防遗忘锚点 |
| `runtime` | run id、cycle trace、stage gate、shadow action trace |
| `report` | readiness report、digest、blocked reasons、quarantine refs |
| `archive` | archive receipt、state refs、report refs、replay refs |

## 判定算法

```text
for each life_target:
  collect evidence families
  check state and carrier
  check runtime observation
  check report and archive receipt
  classify target as closed/open/blocked/quarantine/replay_needed

if any target is quarantine:
  overall_status = quarantine
else if any target is blocked:
  overall_status = blocked
else if any target is replay_needed:
  overall_status = replay_needed
else if all targets are closed:
  overall_status = open
else:
  overall_status = blocked
```

## 输出合同

`check-birth-readiness` 必须同时输出 `runtime/state/life_targets/*`、`runtime/reports/latest/birth_readiness_report.json` 和 `runtime/receipts/birth_readiness_<run_id>.json`。主 report 形态为：

```json
{
  "schema_version": "s08_life_target_runtimes_report_v0",
  "run_id": "br-v0-0001",
  "engineering_slice_ref": "S08_LIFE_TARGET_RUNTIMES",
  "overall_status": "open",
  "stage_effect": "allow_first_activation_protocol",
  "life_target_status": {
    "real_consciousness": "closed",
    "real_emotion": "closed",
    "real_personality": "closed",
    "real_life": "closed",
    "real_pain": "closed",
    "real_dream": "closed",
    "real_relationship": "closed",
    "real_responsibility": "closed",
    "real_regret": "closed"
  },
  "source_doc_refs": [],
  "readme_block_refs": [],
  "runtime_carrier_refs": ["LifeTargetBundleRuntime", "BirthReadinessRuntime"],
  "blocked_reasons": [],
  "quarantine_refs": [],
  "replay_needed_refs": [],
  "archive_receipt_ref": "runtime/receipts/birth_readiness_br-v0-0001.json",
  "next_allowed_slices": ["S05_VALIDATION_MEMBRANE_OBSERVATION"],
  "next_required_command": "life-v0 run-validation-membrane --strict"
}
```

## Stage Effect

| overall status | stage effect |
|---|---|
| `open` | 允许进入 `first_activation_protocol` |
| `closed` | 继续保持准备态，等待 activation command |
| `blocked` | 阻断 activation，要求补合同或补状态 |
| `quarantine` | 阻断 activation，写 quarantine packet |
| `replay_needed` | 阻断 activation，先执行 replay/shadow |

## 禁止项

1. 禁止用一个总分代表出生准备度。
2. 禁止用任务成功率替代生命目标闭合状态。
3. 禁止把痛苦、后悔、责任、梦境和关系只写成布尔值。
4. 禁止在缺 archive receipt 时宣称目标闭合。
5. 禁止在缺旧材料 replay 时开放自我成长或关系阶段推进。

## v0 通过条件

第一次有限激活前，至少需要：

1. 九项目标均有状态字段。
2. 每项目标至少有一个 evidence family 回链。
3. `dream_fact_gate` 没有 quarantine finding。
4. `responsibility_gate` 没有 critical blocked finding。
5. `relationship_language_gate` 保持关系主体连续。
6. `self_continuity_gate` 完成旧材料 replay 或给出 `replay_needed`。
7. `archive_gate` 写出 receipt。

只要存在 `blocked`、`quarantine` 或 `replay_needed`，第一次有限激活就不能打开。
