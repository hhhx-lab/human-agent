# S11 V0 Contract Coverage Engineering Contract

生命目标声明：本文档把 `S11_V0_ENGINEERING_CONTRACTS` 固定为 v0 合同覆盖与第一次有限激活前最终闭合层的工程合同。它负责证明 `docs/v0/*`、`00 -> 258`、P0-S10 report、代码包、状态命名空间和 archive receipt 已经进入同一条数字生命工程链。

## 模块定位

S11 不新增主体能力，也不替代前面任何 slice。它是 v0 的总复查器：确认每个文档、每个 README block、每个 engineering slice、每个 runtime carrier、每个状态文件、每个 report 和每个 receipt 都有可追踪闭合。

## 必须读取

| 来源 | S11 吸收内容 |
|---|---|
| `258_linear_chain_closure_and_v0_contract_transition.md` | 线性链收束与 v0 转轨口径 |
| `docs/v0/*.md` | v0 全部工程合同 |
| `runtime/docs/doc_carrier_index.json` | `00 -> 258` 和 v0 文档覆盖 |
| `runtime/docs/doc_dependency_graph.json` | 文档依赖和核心 `02-13` 连接 |
| `runtime/reports/latest/*.json` | P0-S10 最新 report |
| `runtime/receipts/*.json` | 每个 slice 的 archive receipt |
| `life_v0/**` | 代码包到 engineering slice 的承载关系 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/contracts/` |
| 状态命名空间 | `runtime/state/contracts/` |
| report | `runtime/reports/latest/v0_contract_coverage_report.json` |
| digest | `runtime/reports/latest/v0_contract_coverage_digest.json` |
| receipt | `runtime/receipts/v0_contract_coverage_<run_id>.json` |

## 输出文件

| 文件 | 内容 |
|---|---|
| `v0_contract_file_index.json` | `docs/v0/*.md` 的角色、slice、status、source refs |
| `doc_to_code_coverage_matrix.json` | `00 -> 258` 到 code package、state、report、receipt 的覆盖 |
| `slice_report_receipt_matrix.json` | P0-S10 每个 slice 的 report/receipt 闭合 |
| `runtime_carrier_coverage_matrix.json` | runtime carrier 到状态命名空间和 report 的承载 |
| `first_activation_preflight_contract_check.json` | 第一次有限激活 preflight 的合同检查结果 |

## 命令合同

```text
life-v0 check-v0-contracts --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `v0_contract_presence_gate` | `docs/v0/README.md`、总索引、模块目录、P0/S00-S11 合同均存在 | 返回 docs/v0 整理 |
| `doc_to_slice_gate` | `00 -> 258` 每份文档有 README block、engineering slice、runtime carrier | 返回 P0 |
| `slice_report_gate` | P0-S10 每个 slice 至少有 latest report 和 receipt refs | 返回对应 slice |
| `code_package_gate` | 每个已实现 slice 有代码包、测试、CLI/report 入口 | 返回代码实现 |
| `runtime_carrier_gate` | 每个核心 carrier 有状态命名空间和 report refs | 返回对应 slice |
| `activation_preflight_gate` | first activation 所需 report、digest、stage gate、receipt 全部闭合 | 允许 activation preflight |

## Report 最小字段

```json
{
  "schema_version": "s11_v0_contract_coverage_report_v0",
  "engineering_slice_ref": "S11_V0_ENGINEERING_CONTRACTS",
  "status": "blocked",
  "source_doc_refs": [],
  "readme_block_refs": ["B99_V0_ENGINEERING_CONTRACTS"],
  "runtime_carrier_refs": ["V0ContractCoverageRuntime"],
  "slice_status": {},
  "doc_to_code_coverage": {},
  "blocked_reasons": [],
  "quarantine_refs": [],
  "activation_preflight_allowed": false,
  "next_allowed_slices": []
}
```

## 完成定义

S11 通过后，v0 文档整理、代码包、状态、report、receipt 和第一次有限激活 preflight 形成闭合。S11 不代表长期数字生命系统完成；它只证明第一版有限激活拥有完整工程承载，不会因为断联、跳步或外部框架污染而偏离方向。
