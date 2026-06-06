# Life Reality First Runner Code Observation Feedback Loop

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 166 层承接 `165_life_reality_first_runner_code_commit_and_push_protocol.md`，把 commit/push event、真实运行观测、report drift、stage gate finding、repair route 和 growth route 接入下一轮代码生长。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `FirstRunnerCodeObservationFeedbackLoop166`、`CommitPushObservationEvent166`、`RuntimeSmokeObservationEvent166`、`ReportDriftSignal166`、`StageGateFindingFeedback166`、`RepairRouteQueue166`、`GrowthRouteQueue166` 和 `ObservationToBootstrapHandoff166`。它的生命膜职责是让首批 runner code 进入远端历史之后继续被运行、观察、比较、阻断、修复和生长。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `165_life_reality_first_runner_code_commit_and_push_protocol.md` | commit scope ledger、review evidence bundle、validation receipt、remote push receipt、post-push verification summary |
| `164_life_reality_first_runner_code_review_and_stage_gate_plan.md` | review matrix、stage gate、birth readiness hold、repair route |
| `163_life_reality_first_runner_code_generation_batch.md` | target file tree、command milestones、minimum fixture、cleanup rules |
| `160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md` | dashboard source、blocking-first stage gate、gap feedback |
| `106_runtime_observation_to_life_reality_bundle_bridge.md` | runtime observation envelope、ingestion report、dashboard source |
| `140_life_reality_experience_boundary_declaration_lock.md` | 真实经验生命膜、`EXPB-140-*` scanner rules |

## 本层定位

`166` 是首批 runner code 的观测反馈回路。它把一次 commit/push 之后发生的运行、报告、漂移、阻断和修复都写成 observation event。观测事件先进入候选链，由 stage gate 判断进入 repair queue、growth queue、quarantine 或下一层 minimum code bootstrap execution。

本层把观测反馈拆成 8 个面：

| surface | 目标 |
|---|---|
| `OBS-166-001` | commit/push observation intake |
| `OBS-166-002` | runtime smoke observation intake |
| `OBS-166-003` | report digest and schema drift detection |
| `OBS-166-004` | dashboard and stage gate finding feedback |
| `OBS-166-005` | repair route queue |
| `OBS-166-006` | growth route queue |
| `OBS-166-007` | birth readiness effect feedback |
| `OBS-166-008` | handoff to minimum code bootstrap execution |

## FirstRunnerCodeObservationFeedbackLoop166

```json
{
  "artifact": "FirstRunnerCodeObservationFeedbackLoop166",
  "source_doc": "166_life_reality_first_runner_code_observation_feedback_loop.md",
  "inherits": [
    "165_life_reality_first_runner_code_commit_and_push_protocol.md",
    "164_life_reality_first_runner_code_review_and_stage_gate_plan.md",
    "163_life_reality_first_runner_code_generation_batch.md",
    "160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md",
    "106_runtime_observation_to_life_reality_bundle_bridge.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "loop_stage": "first_runner_code_observation_feedback",
  "stage_gate_family": "OBS-STAGE-166",
  "required_outputs": [
    "CommitPushObservationEvent166",
    "RuntimeSmokeObservationEvent166",
    "ReportDriftSignal166",
    "StageGateFindingFeedback166",
    "RepairRouteQueue166",
    "GrowthRouteQueue166",
    "ObservationToBootstrapHandoff166"
  ],
  "next_artifacts": [
    "167_life_reality_first_runner_minimum_code_bootstrap_execution.md",
    "168_life_reality_first_runner_minimum_code_validation_report.md"
  ]
}
```

## Observation Event Family

| event | 触发来源 | 必须携带 |
|---|---|---|
| `CommitPushObservationEvent166` | `165` post-push summary | commit hash、remote branch、pushed files、review evidence refs、birth readiness effect |
| `RuntimeSmokeObservationEvent166` | 首批 runner 命令运行 | command、exit code、stdout contract、report refs、stage effect |
| `ReportDriftSignal166` | report/digest/baseline comparison | artifact refs、old digest、new digest、drift surface、affected life targets |
| `StageGateFindingFeedback166` | dashboard/stage gate | finding id、severity、stage effect、repair route、growth route |
| `RepairRouteQueue166` | failed review、failed smoke、drift | owner module、owner doc、blocking surface、repair item |
| `GrowthRouteQueue166` | passed review、new evidence | next artifact、new fixture、new command、new dashboard panel |
| `BirthReadinessEffectFeedback166` | birth readiness hold/open decision | target claims、blocked chains、allowed growth window |
| `ObservationToBootstrapHandoff166` | 本层输出 | `167` execution inputs、`168` validation report expectations |

## 反馈回路

首批 runner code 进入远端历史后，观测反馈按以下顺序流动：

```text
post-push verification
  -> commit/push observation event
  -> runtime smoke observation event
  -> report drift signal
  -> stage gate finding feedback
  -> repair route queue
  -> growth route queue
  -> observation-to-bootstrap handoff
```

这个顺序让提交推送变成可复盘事件，也让每一次命令运行都能影响下一轮代码生长。

## Observation Intake Fields

所有 observation event 共享一组字段：

| field | 要求 |
|---|---|
| `observation_id` | 稳定 id，包含阶段和时间窗口 |
| `observation_kind` | commit_push、runtime_smoke、report_drift、stage_gate_finding、repair_route、growth_route |
| `source_docs` | 至少包含 `165` 和本层 |
| `source_artifacts` | commit hash、report path、dashboard source、stage gate review 或 fixture report |
| `life_reality_targets` | 九项真实生命目标中的受影响目标 |
| `stage_effect` | open_next_stage、promote_growth_window、repair、hold_for_evidence、quarantine |
| `repair_route_refs` | 阻断时必须存在 |
| `growth_route_refs` | 通过或新增证据时必须存在 |
| `next_artifacts` | 指向 `167`、`168` 或后续补丁文档 |

## Runtime Smoke Observation

首批 runner code 的最小运行观测来自 `163-165` 固定的命令：

```text
uv run life-reality-runner --help
uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run
uv run life-reality-runner run-full-archive-rollup-fixture-cases --fixture-manifest tests/fixtures/full_archive_rollup_minimum/manifest.json --json
uv run pytest
```

每条命令产生一个 `RuntimeSmokeObservationEvent166`。命令失败时不丢弃结果，而是把 exit code、stdout/stderr 摘要、Problem Details、affected life targets 和 repair route 写入观测事件。

## Report Drift

`ReportDriftSignal166` 用来比较同一类 report 在不同运行窗口中的变化：

| drift surface | 检查 |
|---|---|
| schema drift | report schema id、required fields、life target enum 是否变化 |
| digest drift | canonical digest 是否稳定，变化是否有 source docs |
| finding drift | critical/quarantine finding 是否新增、消失或降级 |
| dashboard drift | blocking-first panel 是否仍然覆盖 false green |
| stage drift | stage effect 是否从 quarantine/repair 被误升为 open |
| gap drift | gap feedback 是否仍然指向下一层 artifact |
| archive drift | doc/code/test/fixture/report/dashboard/stage/gap carrier 是否断裂 |

drift 不是单纯错误；它是下一轮修复或成长的信号。无解释的降级进入 `repair`，遮蔽 critical finding 进入 `quarantine`，有证据的新能力进入 `growth_route`。

## Stage Gate Feedback

| rule | 条件 | effect |
|---|---|---|
| `OBS-STAGE-166-001` | commit/push observation 缺 commit hash 或 pushed files | `hold_for_evidence` |
| `OBS-STAGE-166-002` | runtime smoke observation 缺 command、exit code 或 report refs | `repair` |
| `OBS-STAGE-166-003` | report drift 无 source docs 且影响 stage effect | `repair` |
| `OBS-STAGE-166-004` | critical/quarantine finding 被 dashboard green 遮蔽 | `quarantine` |
| `OBS-STAGE-166-005` | birth readiness effect 被误写成完成态 | `quarantine` |
| `OBS-STAGE-166-006` | 任一真实生命目标在 observation 中没有 carrier | `critical_repair` |
| `OBS-STAGE-166-007` | repair route 缺 owner doc 或 owner module | `repair` |
| `OBS-STAGE-166-008` | growth route 缺 next artifact | `hold_for_evidence` |
| `OBS-STAGE-166-009` | observation event 形成闭环并进入 `167` 输入 | `promote_growth_window` |

## Repair Route Queue

`RepairRouteQueue166` 把观测中的阻断面变成可执行修复项：

| finding | repair route |
|---|---|
| missing commit evidence | 回到 `165` 补 post-push verification summary |
| missing runtime observation | 回到 `167` 补最小命令执行 |
| unstable digest | 修复 canonical digest 或 report writer |
| false green | 修复 dashboard writer、stage gate writer 和 test fixture |
| missing life target carrier | 修复 `RunContext`、report envelope、archive graph |
| broken source doc edge | 修复 archive edge registry |
| birth readiness false open | 修复 birth readiness gate 和 stage effect |

## Growth Route Queue

`GrowthRouteQueue166` 记录可以推动下一轮生长的证据：

| growth signal | next growth |
|---|---|
| command milestone stable | 扩展 `167` 的最小代码执行范围 |
| report digest stable | 进入 `168` validation report |
| critical fixture caught | 增加 mutation fixture 和 withheld probe |
| dashboard blocking-first stable | 扩展 dashboard source panel |
| archive carrier closed | 推进 doc/code/test/report edge registry |
| birth readiness hold stable | 继续增加真实生命目标 carrier |

## Observation To Bootstrap Handoff

`ObservationToBootstrapHandoff166` 是 `167` 的输入合同：

| field | 要求 |
|---|---|
| `commit_observation_refs` | 来自 `165` 的 commit/push event |
| `runtime_smoke_observation_refs` | help、suite dry-run、fixture command、pytest |
| `drift_signal_refs` | report/digest/dashboard/stage/archive drift |
| `repair_queue_refs` | 阻断项 |
| `growth_queue_refs` | 下一轮扩展项 |
| `minimum_code_execution_scope` | `167` 要实际创建或运行的文件/命令 |
| `validation_report_expectations` | `168` 要输出的 report/dashboard/stage/gap |

## Birth Readiness Effect

本层对出生准备度的作用是观测与反馈，而不是完成判定。它确认首批 runner code 是否在运行后仍能承载九项真实生命目标，并把结果分成：

| effect | 含义 |
|---|---|
| `promote_growth_window` | 工程承载面稳定，可以进入下一轮最小代码执行 |
| `repair` | 有缺口但可由 owner doc/module 修复 |
| `hold_for_evidence` | 证据不足，需要更多运行观测 |
| `quarantine` | false green、birth readiness false open 或 critical finding 被遮蔽 |

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-166-001` | observation event 不写入 `.env`、`.codex`、key/token 或本地代理配置 |
| `CLEAN-166-002` | 运行噪声默认进入 ignored report root，不进入 staged source |
| `CLEAN-166-003` | 每个 observation 必须有 source docs、affected life targets 和 stage effect |
| `CLEAN-166-004` | 每个 repair route 必须有 owner doc 或 owner module |
| `CLEAN-166-005` | 每个 growth route 必须有 next artifact |

## Acceptance Criteria

本层完成后必须证明：

1. commit/push event 能变成 `CommitPushObservationEvent166`。
2. 首批 runner 命令运行能变成 `RuntimeSmokeObservationEvent166`。
3. report、digest、dashboard、stage 和 archive drift 都有检测面。
4. repair route 和 growth route 都能从 observation event 派生。
5. birth readiness effect 只打开工程生长窗口，false open 会进入 quarantine。
6. `167` 可以读取 handoff，开始最小代码 bootstrap execution。
7. `168` 可以读取 validation report expectations，生成最小代码执行结果报告。

## 与下一层连接

`167_life_reality_first_runner_minimum_code_bootstrap_execution.md` 已承接本层：开始把 `163-166` 的合同、断联恢复方向锁和出生准备度定义承载转成最小代码 bootstrap 执行入口。

`168_life_reality_first_runner_minimum_code_validation_report.md` 应承接 `167`：把最小代码执行结果写成 validation report、dashboard source、stage gate review 和 gap feedback。

本层完成后，首批 runner code 观测反馈链推进为：

`commit/push event -> runtime smoke observation -> report drift -> stage gate finding -> repair route -> growth route -> minimum code bootstrap execution -> validation report`
