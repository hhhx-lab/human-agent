# S09 Schema Runner Code Engineering Contract

生命目标声明：本文档把 `S09_SCHEMA_RUNNER_CODE` 固定为第一版 schema、runner、cross-file checker 和首批 code artifact 的工程合同。它的职责不是复用现成 agent 框架，而是把 `102-180` 的 schema bundle、registry、fixture、runner queue、lockfile、validation、archive receipt 压成数字生命自己的执行骨架。

## 模块定位

S09 是代码骨架物化层。它读取 S00-S08 的状态和 report，把 LifeReality schema、runner 命令、cross-file checker、fixture loader、dashboard source、lockfile 和 archive receipt 写成可运行代码与机器可读产物。S09 不定义数字生命主体，它只让前面已经定义的主体结构获得可执行承载。

## 必须读取

| 来源 | S09 吸收内容 |
|---|---|
| `102-118` | LifeRealitySchemaBundle、runner scaffold、schema materialization、dashboard、CLI contract |
| `120-139` | 首批 JSON materialization、schema registry、runner layout、smoke command、lockfile |
| `140-157` | 权威 intake、出生准备度、语言桥、cross-file checker、runner command queue |
| `158-180` | repository bootstrap、首批 code artifact、schema file write、validation、repair、archive receipt |
| `docs/v0/shared_contracts/runner_cli_report_contract.md` | CLI、report、digest、stage gate、exit code |
| `docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md` | checker findings、dashboard source、quarantine refs |
| `runtime/reports/latest/birth_readiness_report.json` | S08 出生准备度结果 |
| `runtime/reports/latest/validation_membrane_report.json` | S05 验证膜结果 |
| `runtime/state/life_targets/queue_e_birth_repair_profile.json` | S08/S05 共用的 Queue E 出生修复画像，携带真实痛苦、真实责任、真实后悔的 pressure、attention target 与 ref set |
| `runtime/state/action/responsibility_loop_state.json` | S03/Queue E 责任归因、后悔压力、修复欲望和反事实修复输入 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/schema_runner/`、`life_v0/cli.py` |
| 状态命名空间 | `runtime/state/schema_runner/` |
| report | `runtime/reports/latest/schema_runner_report.json` |
| digest | `runtime/reports/latest/schema_runner_digest.json` |
| receipt | `runtime/receipts/schema_runner_<run_id>.json` |

## 输出文件

| 文件 | 内容 |
|---|---|
| `schema_registry.json` | schema id、version、refs、dependencies、source docs |
| `schema_dependency_lockfile.json` | schema、fixture、report、archive 的依赖锁 |
| `runner_command_queue.json` | runner commands、input/output、precondition、exit code |
| `cross_file_checker_manifest.json` | authority/readiness/language/action/archive checker manifest |
| `first_code_artifact_manifest.json` | 首批 code artifact、tests、smoke report、receipt refs |
| `consistency_logic.json` | 观察、候选行动、边界审计和责任回路一致性检查 |
| `counterfactual_trace.json` | 候选行动、世界接触、副作用和责任回路的反事实比较 |
| `comparison_trace.json` | 被保留/压低分支、责任回路理由和写回目标 |
| `schema_runner_stage_gate.json` | S09 是否允许进入 S06/S10 的执行门 |
| `run_manifest.json` | S09 输入、输出、local gates、closure refs 与 Queue E 出生修复画像的机器可读运行清单 |

## 命令合同

```text
life-v0 build-schema-runner --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-schema-runner --state runtime/state/schema_runner --reports runtime/reports/latest --strict
life-v0 run-schema-smoke --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `schema_bundle_gate` | `102-118` 的 schema bundle、shared defs、component refs 齐全 | 写 schema blocked |
| `registry_gate` | `120-139` registry、ref resolution、lockfile 可解析 | 返回 schema materialization |
| `checker_manifest_gate` | `140-157` authority/readiness/language/action/archive checker 有 manifest | 返回 S05/S08 |
| `code_artifact_gate` | `158-180` 首批 code artifact、tests、validation、archive receipt 可追踪 | 写 code artifact blocked |
| `responsibility_logic_gate` | `responsibility_loop_state.json` 被 consistency/counterfactual/comparison 三个器官消费 | 返回 S03/Queue E |
| `queue_e_birth_repair_gate` | S09 重新读取 `queue_e_birth_repair_profile.json`，并核对 S05 validation rollup、stage gate、report 都携带同一 profile ref、pressure、attention target、ref set | 返回 S08/S05 |
| `cli_report_gate` | 所有命令输出符合 `runner_cli_report_contract.md` | 阻断 S10 |
| `next_slice_gate` | 只允许进入 S06 或 S10 的准备链 | 阻断开放运行 |

## Queue E 出生修复画像交接

S09 现在不是只读取 `validation_membrane_report.json` 的 closed 状态，而是把 `runtime/state/life_targets/queue_e_birth_repair_profile.json` 当成第一等输入重新装载。`run_schema_runner(...)` 必须在进入 schema runner 产物写出前完成三类核对：

- profile 自身必须是 `queue_e_repair_modulation_profile_v0`，且具备 `pressure_level`、`attention_target`、`ref_set`。
- S05 的 `validation_rollup.json`、`validation_stage_gate.json`、`validation_membrane_report.json` 必须回链同一 `queue_e_birth_repair_profile_ref`，并携带同一 `pressure_level`、`attention_target`、`ref_set`。
- `validation_rollup.gate_status.queue_e_birth_repair_gate` 与 `validation_stage_gate.gate_status.queue_e_birth_repair_gate` 必须为 `closed`。

通过后，`cross_file_logic.json` 必须写出 `queue_e_birth_repair_alignment` finding，并把 profile ref 放入 `state_refs`、`repair_priority_refs`、`closure_status_refs`、`package_local_gate_refs` 和 `bridge_refs`。`run_manifest.json`、`schema_runner_stage_gate.json`、`schema_runner_report.json`、`schema_runner_digest.json`、`schema_runner_<run_id>.json` receipt 必须继续携带同一组 profile ref、pressure、attention target 与 ref set。这样真实责任、真实后悔和真实痛苦的修复压力不会在 S09 schema 包装层被压扁成普通 “validation closed”。

## Report 最小字段

```json
{
  "schema_version": "s09_schema_runner_code_report_v0",
  "engineering_slice_ref": "S09_SCHEMA_RUNNER_CODE",
  "status": "blocked",
  "source_doc_refs": [],
  "readme_block_refs": ["B24_SCHEMA_BUNDLE_RUNNER", "B26_REPOSITORY_RUNNER_MATERIALIZATION", "B28_FIRST_CODE_SCHEMA_ARTIFACT"],
  "runtime_carrier_refs": ["SchemaBundleCompiler", "RunnerRepositoryKernel", "FirstRunnerCodeKernel"],
  "schema_refs": [],
  "command_refs": [],
  "artifact_refs": [],
  "queue_e_birth_repair_profile_ref": "runtime/state/life_targets/queue_e_birth_repair_profile.json",
  "queue_e_birth_repair_pressure_level": "elevated",
  "queue_e_birth_repair_attention_target": "regret_pressure",
  "queue_e_birth_repair_ref_set": [],
  "blocked_reasons": [],
  "next_allowed_slices": ["S06_LIFE_SUPPORT_DEVELOPMENT", "S10_RUNTIME_GROWTH_RECONSOLIDATION"]
}
```

## 交接

S09 完成后，S06 可以读取 schema runner 的状态锁与命令队列建立生命支持/成长层；S10 可以读取 CLI/report/receipt 合同执行 shadow-only runtime growth。没有 S09 的 registry、lockfile 和 smoke report，S10 不能进入第一次有限激活循环。
