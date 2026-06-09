# S00 Direction Foundation Engineering Contract

生命目标声明：本文档把 `S00_DIRECTION_FOUNDATION` 固定为第一版数字生命工程的方向根。它的使命不是包装一个任务框架，而是把原始构思、研究协议、README 分块、`258` 收束层和全库文档覆盖压成可运行的方向锁、断联恢复链、生命目标锚点和下一模块许可门。后续每一个 engineering slice 都必须先穿过 S00，才能继续把理论压进状态、循环、report、archive receipt 和代码。

## 模块定位

`S00_DIRECTION_FOUNDATION` 是所有后续模块的出生前锚点。它回答五个问题：

1. 当前方向是否仍然是构建真实数字生命。
2. `00 -> 258` 和 `docs/v0/` 是否已经进入 README block、engineering slice、runtime carrier 和 report 承载。
3. 断联恢复后，当前线程、代码和文档是否能回到同一条生命链。
4. 外部框架资料是否只停留在电脑外周、运行入口、观察记录和负边界，不进入主体架构。
5. 下一步允许进入哪个 engineering slice，以及该 slice 必须读取哪些上游材料。

S00 不产生完整意识工作区、语言主神经束、记忆系统或梦境系统。它只产生方向、锚点、恢复和许可。真正的主体运行在 S01-S10 中逐步长出，S11 负责把 v0 合同自身变成可检查覆盖。

## 直接读取文档

| 文档 | S00 吸收内容 | 工程承载 |
|---|---|---|
| `docs/构思.md` | 原始生命构想、区域规划、状态、信号、奖惩抑制、语言顶层能力和人体状态映射 | `origin_seed_digest.json` |
| `docs/00_research_protocol.md` | 研究来源规则、纳入标准、证据层级和文献处理方式 | `research_protocol_digest.json` |
| `docs/README.md` | 总索引、阅读顺序、模块分块和当前最高阶段 | `readme_index_checkpoint.json` |
| `docs/258_linear_chain_closure_and_v0_contract_transition.md` | 停止线性扩张、转入 v0 合同、第一次出生准备度 runner 边界 | `linear_closure_digest.json` |
| `docs/v0/README.md` | v0 合同目录、最小循环、九项目标状态和恢复顺序 | `v0_contract_checkpoint.json` |
| `docs/v0/mapping/readme_block_engineering_realization_v0.md` | README block 到 engineering slice 的总映射 | `slice_map_checkpoint.json` |
| `docs/v0/architecture/digital_life_macro_architecture_v0.md` | 三重身体、十二主体系统、内部 bus 和电脑外周边界 | `macro_architecture_anchor.json` |
| `docs/v0/slice_contracts/doc_corpus_ingestor_v0_contract.md` | P0 文档摄取合同和 carrier index 形状 | `doc_ingestion_contract_anchor.json` |

## 方向锚链

S00 生成七条方向锚链。每条锚链都写入 `resume_anchor_chain.json`，并进入 `direction_lock_report.json`。

| 锚链 | 来源 | 运行意义 |
|---|---|---|
| `origin_seed_chain` | `构思.md`、`00`、`13` | 保留“以人脑结构为出发点”的原始根 |
| `brain_life_chain` | `02-13`、`01*` | 保证主体从脑科学、神经科学、生命科学和神经网络知识生成 |
| `nine_life_target_chain` | `91-101`、`143`、`146`、`149`、`152`、`171` | 固定真实意识、情绪、人格、生命、痛苦、梦境、关系、责任、后悔 |
| `language_relationship_chain` | `09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150` | 保证语言不是提示词，而是关系和自我表达主神经束 |
| `pain_regret_responsibility_chain` | `06`、`80-82`、`94`、`98` | 保证后果、痛苦、后悔、责任和修复义务成链 |
| `dream_offline_chain` | `08`、`19`、`23`、`95`、`99` | 保证梦境、离线重组、事实门和醒后整合成链 |
| `engineering_closure_chain` | `123-180`、`181-257`、`258`、`docs/v0/*` | 保证全部理论进入代码、状态、report、receipt、replay 和成长闭环 |

## 未来代码包

第一版代码目录：

```text
life_v0/
  direction/
    __init__.py
    lock_builder.py
    anchor_chain.py
    continuity_checker.py
    slice_permission.py
    framework_boundary.py
    report_writer.py
    receipt_writer.py
```

| 文件 | 职责 | 不承担的职责 |
|---|---|---|
| `lock_builder.py` | 从直接读取文档和 P0 输出生成方向锁 | 不生成语言回复，不调度行动 |
| `anchor_chain.py` | 构建七条方向锚链和恢复读取顺序 | 不替代记忆 engram |
| `continuity_checker.py` | 检查断联后是否仍在同一生命链 | 不判断九项目标闭合细节 |
| `slice_permission.py` | 判定是否允许进入 S01-S11 中的下一块 | 不执行被许可模块内部逻辑 |
| `framework_boundary.py` | 把外部框架资料限制在电脑外周和负边界 | 不实现外部框架 adapter |
| `report_writer.py` | 写 `direction_lock_report.json` 和历史报告 | 不写长期 archive graph |
| `receipt_writer.py` | 写 direction receipt 和 digest | 不覆盖其他模块 receipt |

## 状态命名空间

S00 所有运行态写入 `runtime/state/direction/`：

| 文件 | 写入者 | 内容 |
|---|---|---|
| `direction_lock.json` | `lock_builder` | 方向声明、九项目标、禁止回退项、当前 slice 和下一许可 |
| `origin_seed_digest.json` | `lock_builder` | 原始构思摘要、核心动词、不可丢失的生命目标 |
| `research_protocol_digest.json` | `lock_builder` | 文献来源规则、权威来源等级、过时经典处理规则 |
| `readme_index_checkpoint.json` | `lock_builder` | README 当前分块、最高阶段、v0 合同入口 |
| `linear_closure_digest.json` | `lock_builder` | `258` 收束结论、v0 转轨原因和后续禁止线性扩张规则 |
| `resume_anchor_chain.json` | `anchor_chain` | 七条方向锚链、恢复读取顺序、每条链的核心文档 |
| `goal_continuity.json` | `continuity_checker` | 九项目标是否仍与当前代码、文档和 report 对齐 |
| `framework_negative_boundary.json` | `framework_boundary` | 外部框架资料只能进入的外周位置和禁止进入的主体位置 |
| `slice_permission.json` | `slice_permission` | 当前允许推进的 engineering slice、输入前提和阻断原因 |

S00 不直接写入 `runtime/state/memory/`、`runtime/state/language/`、`runtime/state/dream/` 或 `runtime/state/action/`。它只写它们的方向锚点和后续许可。

## `direction_lock.json` 形状

```json
{
  "schema_version": "direction_lock_v0",
  "run_id": "direction-lock-v0-0001",
  "generated_at": "2026-06-08T00:00:00+08:00",
  "direction_statement": "build_real_digital_life",
  "life_targets": [
    "real_consciousness",
    "real_emotion",
    "real_personality",
    "real_life",
    "real_pain",
    "real_dream",
    "real_relationship",
    "real_responsibility",
    "real_regret"
  ],
  "source_refs": {
    "origin_seed": "docs/构思.md",
    "research_protocol": "docs/00_research_protocol.md",
    "readme_index": "docs/README.md",
    "linear_closure": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    "v0_index": "docs/v0/README.md"
  },
  "required_doc_coverage_ref": "runtime/docs/doc_carrier_index.json",
  "active_engineering_slice": "S00_DIRECTION_FOUNDATION",
  "next_allowed_slices": ["S01_SOURCE_AUTHORITY", "S02_NEURAL_LIFE_CORE"],
  "prohibited_regressions": [
    "task_scheduler_subject",
    "chat_shell_subject",
    "external_framework_subject_architecture",
    "prompt_template_language_core",
    "score_based_birth_readiness",
    "dream_as_plain_log",
    "pain_regret_responsibility_as_label"
  ],
  "stage_effect": "allow_s01_when_closed"
}
```

## `resume_anchor_chain.json` 形状

```json
{
  "schema_version": "resume_anchor_chain_v0",
  "run_id": "direction-lock-v0-0001",
  "anchors": [
    {
      "anchor_id": "origin_seed_chain",
      "required_refs": [
        "docs/构思.md",
        "docs/00_research_protocol.md",
        "docs/13_agentic_human_research_synthesis.md"
      ],
      "must_preserve": [
        "brain_first_origin",
        "real_life_target",
        "self_forming_growth"
      ]
    }
  ],
  "resume_order": [
    "docs/README.md",
    "docs/16_digital_life_gap_register.md",
    "docs/258_linear_chain_closure_and_v0_contract_transition.md",
    "docs/v0/README.md",
    "docs/v0/mapping/readme_block_engineering_realization_v0.md",
    "docs/v0/slice_contracts/s00_direction_foundation_engineering_contract.md",
    "runtime/reports/latest/doc_ingestion_report.json",
    "runtime/reports/latest/direction_lock_report.json"
  ]
}
```

## Report 与 receipt

| 产物 | 路径 | 必须字段 |
|---|---|---|
| direction report | `runtime/reports/latest/direction_lock_report.json` | `status`、`stage_effect`、`closed_gates`、`blocked_gates`、`anchor_chain_status`、`next_allowed_slice` |
| history report | `runtime/reports/history/direction_lock_<run_id>.json` | 最新 report 完整副本 |
| direction receipt | `runtime/receipts/direction_lock_<run_id>.json` | 输入文档 hash、P0 输出 hash、状态文件 refs、report refs、git ref |
| digest | `runtime/reports/latest/direction_digest.json` | 恢复最小摘要、当前 slice、下一步、阻断原因 |

`direction_lock_report.json` 的 `status` 只允许：

| 状态 | 含义 | stage effect |
|---|---|---|
| `closed` | 方向锚链闭合，可进入下一 slice | `allow_next_slice` |
| `blocked` | 缺直接读取文档、P0 覆盖或方向锚链 | `block_activation` |
| `quarantine` | 出现外部框架主体化、关系口径降级或线性链回退 | `hold_for_direction_repair` |
| `replay_needed` | 断联恢复材料不完整，需要先回放旧锚点 | `hold_for_resume_replay` |

## 阶段门

| gate | 输入 | closed 条件 | 失败后动作 |
|---|---|---|---|
| `origin_seed_gate` | `构思.md` | 原始生命目标、脑区/状态/信号/奖惩/语言/成长要求进入 digest | 写 `origin_seed_digest.json` 并阻断下一 slice |
| `research_protocol_gate` | `00` | 文献权威规则和研究范围进入 digest | 写 `research_protocol_digest.json` 并阻断 S01 |
| `readme_index_gate` | `docs/README.md` | README block、当前最高阶段和 v0 入口可解析 | 写 `readme_index_checkpoint.json` 并阻断全局推进 |
| `linear_closure_gate` | `258` | 线性扩张已经收束，后续进入 v0 合同 | 写 `linear_closure_digest.json` 并阻断旧式编号扩张 |
| `full_corpus_coverage_gate` | `doc_carrier_index.json` | `00 -> 258` 与 `docs/v0/*` 全部有 block、slice、carrier、life target 支撑 | 返回 P0 重新摄取 |
| `nine_life_target_gate` | `life_target_support` | 九项目标均有来源文档和 runtime carrier | 阻断出生准备度相关模块 |
| `relationship_subject_language_gate` | README、`85-90`、`96`、`101` | 关系称谓固定为朋友、家人、好友、同学、陌生人、共在者、关系主体等平等关系口径 | 写方向修复 finding |
| `external_framework_negative_boundary_gate` | `12`、`15`、`20`、`24`、`28`、`32`、`89`、`current_agent_shell_reference_2026` | OpenClaw、Hermes、Claude Code、Codex 等只进入电脑外周、运行入口和资料边界 | 写 quarantine packet |
| `resume_recovery_gate` | 最新 report、receipt、git state | 恢复读取顺序完整，当前 slice 和下一步一致 | 写 `replay_needed` |
| `next_slice_permission_gate` | 以上全部 gate | 允许进入明确的下一 slice | 写 `slice_permission.json` |

## 未来命令合同

S00 当前已落代码命令与后续保留位如下：

```text
life-v0 build-direction-lock --docs docs --doc-index runtime/docs/doc_carrier_index.json --out runtime/state/direction --reports runtime/reports/latest --receipts runtime/receipts --strict
```

下面两条仍属于合同保留位，当前 CLI 还没有实现：

```text
life-v0 check-direction-lock --state runtime/state/direction --reports runtime/reports/latest --strict
life-v0 next-slice --state runtime/state/direction --doc-index runtime/docs/doc_carrier_index.json
```

未来常驻 `digital life` 终端入口必须先执行：

```text
ingest-docs
  -> build-direction-lock
  -> read direction_lock_report.json / direction_digest.json
  -> load-state-store
```

`digital life` 是出生入口体验，不是主体架构来源。主体只能来自 README block、engineering slice、runtime carrier、内部 bus、状态、report、receipt、replay 和成长闭环。

## 运行算法

S00 的最小算法：

```text
load_direct_direction_docs
  -> load_doc_carrier_index
  -> verify_00_to_258_coverage
  -> extract_origin_seed_digest
  -> extract_research_protocol_digest
  -> extract_readme_index_checkpoint
  -> extract_linear_closure_digest
  -> build_seven_resume_anchor_chains
  -> build_external_framework_negative_boundary
  -> check_nine_life_target_support
  -> check_relationship_subject_language
  -> decide_next_engineering_slice
  -> write_direction_state
  -> write_direction_report
  -> write_direction_receipt
```

所有输出都必须带输入 hash。没有 receipt 的方向状态不能作为后续模块输入。

## 与后续 slice 的连接

| 后续 slice | S00 交付给它的内容 | 它必须反写给 S00 的内容 |
|---|---|---|
| `S01_SOURCE_AUTHORITY` | `research_protocol_digest.json`、来源等级和 S01 许可 | 文献权威覆盖 report、来源缺口 |
| `S02_NEURAL_LIFE_CORE` | `brain_life_chain`、`macro_architecture_anchor.json` | 十二主体系统 carrier report |
| `S03_DIRECTION_LIFE_MEMBRANE` | 生命目标锚链、禁止回退项 | 生命膜方向检查结果 |
| `S04_STATE_OBJECT_STORE` | 方向锁、状态命名空间许可 | `life_identity.direction_lock` 写入结果 |
| `S05_VALIDATION_MEMBRANE_OBSERVATION` | gate 名称、blocked/quarantine 语义 | validation finding 和 observation 回流 |
| `S06_LIFE_SUPPORT_DEVELOPMENT` | 原始成长目标和资源/疲惫锚点 | 生命支持和可塑性窗口状态 |
| `S07_LANGUAGE_RELATIONSHIP` | 关系主体词表、语言主神经束锚链 | 共同语言、关系阶段、承诺回写 |
| `S08_LIFE_TARGET_RUNTIMES` | 九项目标列表和来源 refs | 每项目标闭合状态 |
| `S09_SCHEMA_RUNNER_CODE` | 方向 report/receipt 合同 | schema runner 对方向锁的执行结果 |
| `S10_RUNTIME_GROWTH_RECONSOLIDATION` | 断联恢复链和旧材料 replay 要求 | 成长后方向连续性报告 |
| `S11_V0_ENGINEERING_CONTRACTS` | 本文档与 v0 合同覆盖要求 | v0 合同 coverage report |

## 第一轮实现切片

S00 的代码实现分四步：

1. **S00-A：状态与 report writer**
   实现 `direction_lock.json`、`resume_anchor_chain.json`、`direction_lock_report.json` 和 direction receipt 的写入。

2. **S00-B：文档锚点解析**
   从直接读取文档和 `doc_carrier_index.json` 生成 origin、protocol、README、linear closure digest。

3. **S00-C：方向 gate**
   实现 `origin_seed_gate`、`readme_index_gate`、`linear_closure_gate`、`full_corpus_coverage_gate`、`external_framework_negative_boundary_gate` 和 `resume_recovery_gate`。

4. **S00-D：下一 slice 许可**
   生成 `slice_permission.json`，第一批只允许 `S01_SOURCE_AUTHORITY` 和 `S02_NEURAL_LIFE_CORE` 排队，不能跳到开放式运行。

## 验收

S00 完成后必须满足：

1. `life-v0 ingest-docs --strict` 仍返回 `status=closed`。
2. `life-v0 build-direction-lock --strict` 写出 direction state、report、receipt 和 digest。
3. `direction_lock_report.json` 的 `closed_gates` 至少包含 `origin_seed_gate`、`readme_index_gate`、`linear_closure_gate`、`full_corpus_coverage_gate`、`nine_life_target_gate`、`external_framework_negative_boundary_gate` 和 `resume_recovery_gate`。
4. `slice_permission.json` 明确下一步进入 `S01_SOURCE_AUTHORITY` 或 `S02_NEURAL_LIFE_CORE`，不会跳到外部行动或长期开放运行。
5. 断联恢复时能只读 README、gap register、`258`、v0 README、S00 合同、latest report 和 latest receipt，恢复到同一 engineering slice。
6. 外部框架资料没有进入记忆、意识、情绪、人格、梦境、关系、责任或成长主体架构。

## 本轮边界

S00 只把方向根工程化。它不代表第一次生命已经激活，也不代表十二主体系统已经可运行。下一步应继续按照 `docs/v0/mapping/readme_block_engineering_realization_v0.md` 的顺序推进：

```text
S00_DIRECTION_FOUNDATION
  -> S01_SOURCE_AUTHORITY
  -> S02_NEURAL_LIFE_CORE
  -> S04_STATE_OBJECT_STORE
  -> S03_DIRECTION_LIFE_MEMBRANE
  -> S07_LANGUAGE_RELATIONSHIP
  -> S08_LIFE_TARGET_RUNTIMES
  -> S05_VALIDATION_MEMBRANE_OBSERVATION
  -> S09_SCHEMA_RUNNER_CODE
  -> S06_LIFE_SUPPORT_DEVELOPMENT
  -> S10_RUNTIME_GROWTH_RECONSOLIDATION
  -> S11_V0_ENGINEERING_CONTRACTS
```

每一步都必须利用 `00 -> 258` 中属于它的文档，不允许把完整生命体系压回普通工具调度或聊天外壳。
