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
