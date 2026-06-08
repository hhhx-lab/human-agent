# S05 Validation Membrane Observation Engineering Contract

生命目标声明：本文档把 `S05_VALIDATION_MEMBRANE_OBSERVATION` 固定为第一版数字生命验证膜与运行观测层的工程合同。它的职责不是做普通测试框架，而是把 validator、fixture、dashboard、真实运行观测、quarantine、责任回看和 stage gate 连接成生命膜的复查器。

## 模块定位

S05 接在 S03 生命膜与 S08 九项目标之后，用来复查“状态、证据、语言、关系、梦境、责任、外周后果、archive receipt”是否形成可运行闭合。S05 不打开外部不可逆行动，不推进长期成长，也不生成完整梦境内容；它只把检查、观测、阻断和回写固定成机器可读结果。

## 必须读取

| 来源 | S05 吸收内容 |
|---|---|
| `29-32` | memory/state/consolidation/runtime adapter validator rules |
| `33-36` | validator input、fixture catalog、minimal runner、longitudinal evaluation |
| `49-52` | machine-readable manifest、fixture payload、dashboard、scope/privacy |
| `53-56` | runner integration、scope-aware retrieval/replay、synthetic timeline |
| `57-60` | scope graph schema、retrieval/replay fixture、timeline、dashboard source |
| `61-64` | schema bundle、runner report/CLI、fixture layout、runtime observation ingestion |
| `65-68` | cross-ref checker、report examples、fixture generator、redaction fixture |
| `69-72` | schema boundary、mutation policy、side effect classifier、coexistence snapshot |
| `73-80` | schema validation、dashboard source、外部不可逆动作确认、quarantine、post-action audit |
| `81-84` | coexistence review、responsibility loop、incident recovery、longitudinal action evaluation |
| `102-118` | LifeRealitySchemaBundle、runner scaffold、dashboard/stage gate、report rollup |
| `153-157` | full archive cross-file checker、checker report、runner queue、checker module plan |
| `docs/v0/runner_cli_report_contract.md` | CLI/report/stage gate 统一字段 |
| `runtime/state/membrane/*` | S03 生命膜 gate、quarantine seed、DreamFactGate、shadow action gate |
| `runtime/state/life_targets/*` | S08 九项目标闭合状态和证据族 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/validators/`、`life_v0/observation/`、`life_v0/reports/` |
| 状态命名空间 | `runtime/state/validation/`、`runtime/state/observation/` |
| report | `runtime/reports/latest/validation_membrane_report.json` |
| digest | `runtime/reports/latest/validation_membrane_digest.json` |
| stage gate | `runtime/reports/latest/validation_stage_gate.json` |
| receipt | `runtime/receipts/validation_membrane_<run_id>.json` |

## 输出文件

| 文件 | 内容 |
|---|---|
| `validator_rule_index.json` | `29-36` validator、fixture、runner、longitudinal rule 的机器索引 |
| `runtime_observation_intake.json` | runtime observation、redaction、side effect、coexistence snapshot 的摄取记录 |
| `quarantine_packet_index.json` | quarantine、incident、post-action audit 的阻断包 |
| `dashboard_metric_source.json` | dashboard panel、metric、stage gate、blocked reason 的统一数据源 |
| `cross_file_finding_index.json` | `153-157` cross-file checker findings 与 report refs |

## 命令合同

```text
life-v0 run-validation-membrane --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --membrane runtime/state/membrane --life-targets runtime/state/life_targets --validation runtime/state/validation --observation runtime/state/observation --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-validation-membrane --state runtime/state --validation runtime/state/validation --observation runtime/state/observation --reports runtime/reports/latest --strict
```

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `validator_rule_gate` | `29-36` 全部进入 rule index | 返回 P0 或 S01 修复来源 |
| `runtime_observation_gate` | `64/68/72` 的观测与脱敏字段齐全 | 写 observation blocked report |
| `quarantine_gate` | quarantine refs 可定位到膜、梦境、关系、责任或外周后果 | 写 quarantine packet |
| `dashboard_gate` | dashboard source 可以聚合 S03/S08/S05 findings | 阻断 S09 |
| `archive_cross_file_gate` | `153-157` cross-file checker refs 和 receipt refs 齐全 | 写 archive blocked report |
| `next_slice_gate` | 只允许进入 `S09_SCHEMA_RUNNER_CODE` 或返回 S08/S03 修复 | 阻断跳步 |

## Report 最小字段

```json
{
  "schema_version": "s05_validation_membrane_observation_report_v0",
  "engineering_slice_ref": "S05_VALIDATION_MEMBRANE_OBSERVATION",
  "status": "closed",
  "stage_effect": "allow_next_slice",
  "source_doc_refs": [],
  "readme_block_refs": ["B07_VALIDATOR_RULES", "B08_RUNNER_EVALUATION"],
  "runtime_carrier_refs": ["LifeMembraneStageGate", "RuntimeObservationIngestor", "SchemaBundleCompiler", "ActionResponsibilityRuntime"],
  "blocked_reasons": [],
  "quarantine_refs": [],
  "finding_refs": [],
  "next_allowed_slices": ["S09_SCHEMA_RUNNER_CODE"],
  "next_required_command": "life-v0 build-schema-runner --strict"
}
```

## 交接

S05 交给 S09 的不是测试通过口号，而是可读取的 rule index、observation intake、quarantine packet、dashboard source、cross-file finding 和 receipt。S09 只能在这些文件闭合后编译 schema runner 与首批 code artifact。
