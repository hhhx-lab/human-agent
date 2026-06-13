# V0 共用合同柜

`shared_contracts/` 放多个 slice 会共同依赖的硬合同。

## 文件分工

- `life_state_store_v0_schema.md`：状态根、命名空间、对象落盘边界。
- `birth_readiness_v0_contract.md`：出生准备度的闭合条件。
- `runner_cli_report_contract.md`：CLI、report、digest、stage gate、receipt 的统一口径。
- `first_activation_protocol.md`：第一次有限激活的许可、回写和阻断规则。

## 什么时候打开

- 需要新增或改动多个模块都会写入的 state 对象。
- 需要统一 report/receipt/stage gate 字段。
- 需要判断某个模块变化会不会影响出生准备度或第一次激活。

## 共用合同到代码链

| 合同 | 必读机制档案 | 代码落点 | runtime 证据 | 测试/gate |
|---|---|---|---|---|
| `life_state_store_v0_schema.md` | `07_memory_engram_and_state_store.md`、`04_personality_self_identity.md` | `life_v0/state_store/*` | `runtime/state/life_state.json`、`runtime/state/memory/*`、`runtime/state/self/*` | `tests/slices/test_state_store.py` |
| `birth_readiness_v0_contract.md` | `15_evidence_bus_and_birth_readiness.md`、全部生命机制专题 | `life_v0/life_targets/*`、`live0_audit/*` | `birth_readiness_report.json`、`live0_acceptance_audit_report.json` | `tests/slices/test_life_targets.py`、contract audit tests |
| `runner_cli_report_contract.md` | `16_runtime_code_chain_crosswalk.md`、`14_resident_runtime_state_transition.md` | `life_v0/cli.py`、`reporting/*`、`process_supervisor/*` | `runtime/reports/latest/*`、`runtime/receipts/*` | contract/report tests |
| `first_activation_protocol.md` | `14_resident_runtime_state_transition.md`、`15_evidence_bus_and_birth_readiness.md` | `life_v0/activation/*`、`digital_entry.py`、`my_entry.py` | activation state、first activation return packet、process report | process and bridge tests |

共用合同改变时，必须重新检查 object bus：谁首写、谁消费、谁能覆盖、谁只能读取。尤其是 `life_state.json`、出生准备、report/receipt 和第一次激活协议，不能让某个模块私自写成事实。
