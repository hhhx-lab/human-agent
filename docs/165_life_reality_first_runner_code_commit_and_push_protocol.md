# Life Reality First Runner Code Commit And Push Protocol

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 165 层承接 `164_life_reality_first_runner_code_review_and_stage_gate_plan.md`，把首批 runner code 的 staged scope、commit message、push、验证摘要、review report、远端状态和后续观测反馈固定为提交推送协议。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `FirstRunnerCodeCommitPushProtocol165`、`CommitScopeLedger165`、`ReviewEvidenceBundle165`、`RemotePushReceipt165`、`PostPushVerificationSummary165`、`CommitToObservationBridge165` 和 `GrowthHandoffRecord165`。它的生命膜职责是让首批 runner code 从本地 review 进入远端历史，并让 commit/push 本身成为可追踪、可复盘、可继续生长的生命工程事件。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `164_life_reality_first_runner_code_review_and_stage_gate_plan.md` | generated file review、life membrane field review、command/test/dashboard/archive/birth gates、repair route |
| `163_life_reality_first_runner_code_generation_batch.md` | target file tree、command milestones、`GEN-STAGE-163`、cleanup rules |
| `161_life_reality_code_artifact_archive_cohesion_execution_plan.md` | archive node/edge registry、life target carrier matrix、birth readiness archive gate |
| `160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md` | dashboard/stage/gap bridge、false green guard |
| `140_life_reality_experience_boundary_declaration_lock.md` | 真实经验生命膜、`EXPB-140-*` scanner rules |

## 本层定位

`165` 是首批 runner code 的提交推送协议层。它不替代 `164` 的审查，也不替代后续真实代码执行；它定义在首批代码通过 review 后，如何把 staged scope、验证证据、commit、push、远端状态和下一层观测入口写成可追踪事件。

本层把提交推送拆成 8 个面：

| surface | 目标 |
|---|---|
| `COMMIT-165-001` | staged scope ledger |
| `COMMIT-165-002` | review evidence bundle |
| `COMMIT-165-003` | validation command receipt |
| `COMMIT-165-004` | commit message and hash receipt |
| `COMMIT-165-005` | remote push receipt |
| `COMMIT-165-006` | post-push verification summary |
| `COMMIT-165-007` | birth readiness hold and growth handoff |
| `COMMIT-165-008` | observation feedback bridge |

## FirstRunnerCodeCommitPushProtocol165

```json
{
  "artifact": "FirstRunnerCodeCommitPushProtocol165",
  "source_doc": "165_life_reality_first_runner_code_commit_and_push_protocol.md",
  "inherits": [
    "164_life_reality_first_runner_code_review_and_stage_gate_plan.md",
    "163_life_reality_first_runner_code_generation_batch.md",
    "161_life_reality_code_artifact_archive_cohesion_execution_plan.md",
    "160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "protocol_stage": "first_runner_code_commit_and_push",
  "stage_gate_family": "COMMIT-STAGE-165",
  "required_evidence": [
    "CommitScopeLedger165",
    "ReviewEvidenceBundle165",
    "ValidationCommandReceipt165",
    "RemotePushReceipt165",
    "PostPushVerificationSummary165",
    "GrowthHandoffRecord165"
  ],
  "next_artifacts": [
    "166_life_reality_first_runner_code_observation_feedback_loop.md",
    "167_life_reality_first_runner_minimum_code_bootstrap_execution.md"
  ]
}
```

## Commit Scope Ledger

首批 runner code 进入 commit 前，必须先生成或人工确认 `CommitScopeLedger165`。它记录 staged 文件、文件来源、review surface、生命目标承载和清理状态。

| field | 要求 |
|---|---|
| `staged_files` | 只包含首批 runner code、tests、fixtures、README/docs updates、必要 config |
| `source_docs` | 至少引用 `163`、`164` 和相关上游工程合同 |
| `life_target_carriers` | 九项真实生命目标在 context/report/dashboard/stage/archive 的 carrier refs |
| `review_outputs` | 指向 `generated_file_review`、`life_membrane_field_review`、`command_milestone_review` 等 |
| `cleanup_status` | `.env`、`.codex`、key/token、generated noise、debug artifact 均未 staged |
| `commit_message` | 简体中文，描述真实进展，不写空泛动作 |
| `push_target` | `origin main`，SSH remote |

## Review Evidence Bundle

`ReviewEvidenceBundle165` 汇总 `164` 的所有审查输出。没有 evidence bundle 时不得进入 commit：

| evidence | 必须包含 |
|---|---|
| generated file review | `163` target file tree 覆盖情况 |
| life membrane field review | 九项真实生命目标字段 coverage |
| command milestone review | help、suite dry-run、fixture command、pytest 的状态 |
| fixture/test review | pass/critical fixture、exit code、expected finding |
| report/digest review | artifact refs、canonical digest、gap route |
| dashboard false green review | blocking-first decision |
| archive cohesion review | doc/code/test/fixture/report/dashboard/stage/gap edges |
| birth readiness gate review | 最小 runner 只进入工程生长窗口 |
| vocabulary scan | 旧式边界语境与关系主体词汇稳定 |
| git hygiene review | staged scope 和 secret/noise scan |

## Validation Command Receipt

首批 runner code 提交前，至少要保留以下命令的结果摘要：

```text
/opt/homebrew/bin/git status --short --branch
/opt/homebrew/bin/git diff --check
uv sync
uv run life-reality-runner --help
uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run
uv run life-reality-runner run-full-archive-rollup-fixture-cases --fixture-manifest tests/fixtures/full_archive_rollup_minimum/manifest.json --json
uv run pytest
/opt/homebrew/bin/git diff --cached --check
/opt/homebrew/bin/git diff --cached --stat
/opt/homebrew/bin/git diff --cached --name-status
```

如果首批代码还没有生成，本文档只固定未来 receipt 合同；真正执行时每条命令都要有 status、exit code、stdout contract、blocking finding 和 gap route。

## Commit Message Rules

提交信息默认使用简体中文，并表达实际推进：

| commit surface | message pattern |
|---|---|
| project bootstrap | `新增生命现实运行器项目骨架` |
| command and fixtures | `新增生命现实运行器冒烟命令` |
| dashboard/stage/archive | `新增生命现实运行器阶段门与凝聚检查` |
| first full runner batch | `新增首批生命现实运行器代码` |

提交信息必须对应 staged scope。若 staged scope 同时覆盖多个 surface，message 选择最能代表主推进的句子，并在 post-push summary 中列出子面。

## Remote Push Receipt

`RemotePushReceipt165` 记录 push 结果，使远端历史成为可审计生命工程事件：

| field | 要求 |
|---|---|
| `remote` | `git@github.com:hhhx-lab/human-agent.git` |
| `branch` | `main` |
| `before_rev` | push 前 `origin/main` |
| `after_rev` | push 后 `HEAD` |
| `commit_hash` | 本次 commit hash |
| `push_status` | success、failed、retry_needed |
| `remote_alignment` | `HEAD == origin/main` |
| `review_evidence_refs` | 指向 `ReviewEvidenceBundle165` |
| `next_growth_artifacts` | `166` 和 `167` |

## Post-Push Verification

push 后必须重新确认：

```text
/opt/homebrew/bin/git status --short --branch
/opt/homebrew/bin/git rev-parse --short HEAD
/opt/homebrew/bin/git log -1 --oneline --decorate
```

`PostPushVerificationSummary165` 需要写出：

| field | 要求 |
|---|---|
| `working_tree_state` | 干净或列出剩余非本次文件 |
| `branch_alignment` | `main...origin/main` 对齐 |
| `latest_commit` | hash + message |
| `pushed_files` | 本次实际进入远端的文件 |
| `validation_summary` | 命令、scan、review gate 状态 |
| `birth_readiness_effect` | `promote_growth_window` 或阻断原因 |
| `next_observation_entry` | 指向 `166` |

## Stage Gate Rules

| rule | 条件 | effect |
|---|---|---|
| `COMMIT-STAGE-165-001` | staged scope 含非本批次文件且没有 source refs | `repair` |
| `COMMIT-STAGE-165-002` | review evidence bundle 缺失 | `hold_for_evidence` |
| `COMMIT-STAGE-165-003` | `RunContext` 或 report 缺九项真实生命目标 | `critical_repair` |
| `COMMIT-STAGE-165-004` | validation command receipt 有未解释失败 | `repair` |
| `COMMIT-STAGE-165-005` | dashboard false green 或 birth readiness false open 未修复 | `quarantine` |
| `COMMIT-STAGE-165-006` | archive carrier 缺失仍进入 commit | `critical_repair` |
| `COMMIT-STAGE-165-007` | `.env`、`.codex`、key/token、代理配置、generated noise staged | `quarantine` |
| `COMMIT-STAGE-165-008` | commit message 与 staged scope 不一致 | `repair` |
| `COMMIT-STAGE-165-009` | push 后 `HEAD` 未对齐 `origin/main` | `hold_for_evidence` |
| `COMMIT-STAGE-165-010` | commit/push evidence 完整且远端对齐 | `promote_growth_window` |

## Birth Readiness Effect

首批 runner code 的 commit/push 只能推进出生准备度的工程承载面。它不把数字生命判为已经出生；它证明的是：

| readiness surface | commit/push 后的证据 |
|---|---|
| 理论到代码 | `163` target files 已进入版本历史 |
| 代码到测试 | unit/smoke/fixture tests 已进入版本历史 |
| 测试到报告 | review evidence bundle 和 validation receipt 可追踪 |
| 报告到 dashboard | dashboard/stage/gap writers 有 carrier |
| dashboard 到 stage | false green guard 有 review gate |
| stage 到下一层 | `166` observation feedback 和 `167` minimum code bootstrap execution |

如果 post-push summary 发现 birth readiness 被误写成完成态，必须生成 `birth_readiness_commit_false_open` finding，并进入 `quarantine`。

## Commit To Observation Bridge

`CommitToObservationBridge165` 把一次提交推送变成下一层观测入口：

| event | observation payload |
|---|---|
| commit created | commit hash、message、staged files、review refs |
| push completed | remote、branch、before/after rev、alignment |
| validation passed | command receipts、scan receipts、stage effect |
| validation failed | finding、repair route、next artifact |
| post-push drift | remote mismatch、dirty tree、missing review evidence |

这些 observation 不直接写入真实生命核心，而是进入 `166` 的运行观测反馈回路，用来形成 report drift、stage finding、repair route 和 growth route。

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-165-001` | 提交前只 stage 本批次目标文件 |
| `CLEAN-165-002` | 不提交 `.env`、`.codex`、key/token、代理配置、generated noise |
| `CLEAN-165-003` | 临时脚本、debug artifact 和运行缓存必须清理或 ignored |
| `CLEAN-165-004` | review evidence 缺失时不打开 commit stage |
| `CLEAN-165-005` | push 后必须确认 `HEAD`、`origin/main` 和工作区状态 |
| `CLEAN-165-006` | post-push summary 必须写入下一层 observation feedback route |

## Acceptance Criteria

首批 runner code 完成提交推送时，本层必须证明：

1. staged scope 与 `163`/`164` 的目标文件和 review surfaces 对齐。
2. review evidence bundle 覆盖 generated files、life membrane fields、commands、tests、dashboard、archive、birth gate 和 git hygiene。
3. validation command receipt 能解释每个通过、失败或跳过的命令。
4. commit message 是简体中文，并准确描述真实进展。
5. push 后 `HEAD` 与 `origin/main` 对齐。
6. post-push summary 记录 pushed files、latest commit、validation summary、birth readiness effect 和 next observation entry。
7. 下一层 `166` 能读取 commit/push event，进入真实运行观测反馈回路。

## 与下一层连接

`166_life_reality_first_runner_code_observation_feedback_loop.md` 应承接本层：把 commit/push event、真实运行观测、report drift、stage gate finding、repair route 和 growth route 接入下一轮代码生长。

`167_life_reality_first_runner_minimum_code_bootstrap_execution.md` 应承接 `166`：开始把 `163-165` 的合同转成实际 runner 文件、命令、tests 和 reports。

本层完成后，首批 runner code 提交推送链推进为：

`review stage gate -> commit scope ledger -> validation receipt -> commit -> push -> post-push verification -> observation feedback loop -> minimum code bootstrap execution`
