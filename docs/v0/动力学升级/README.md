# 动力学升级方案（Dynamics Upgrade）— 修订版

本目录定义 live0 从 **schema 器官** 到 **数值积分 + 竞争加厚** 的**增量**路线。

## 版本说明

| 版本 | 日期 | 变化 |
|------|------|------|
| v0.1 | 初稿 | 偏大刀阔斧（新包、主状态取代、全量 L0/L1/L2） |
| **v0.2** | 修订 | 对照理论/工程/代码审计；**加厚现有器官**，ITR-09 微段 |

## 必读顺序（修订后）

| 顺序 | 文档 | 内容 |
|------|------|------|
| **0** | [00_现状审计与增量原则.md](./00_现状审计与增量原则.md) | **先读**：已有代码、禁止重开、真实缺口 |
| 1 | [00_总纲_动力学巅峰架构.md](./00_总纲_动力学巅峰架构.md) | 总架构、对齐矩阵、诚实边界 |
| 2 | [13_实施波次_测试与Gate.md](./13_实施波次_测试与Gate.md) | ITR-09-A~F 微段、flag、验收 |
| 3 | 分模块 `01`–`12` | 按实施波次选读 |

## 理论 + 工程双锚

| 类型 | 文档 |
|------|------|
| 宏架构 | `docs/v0/architecture/digital_life_macro_architecture_v0.md` |
| 对象总线 | `docs/v0/code_architecture/02_runtime_object_bus_and_flow_contract.md` |
| 回合生命周期 | `docs/v0/implementation_architecture/02_turn_and_cycle_lifecycle_contract.md` |
| 预测深消费波 | `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md` |
| 增量施工 | `docs/v0/package_specs/03_incremental_package_delivery_protocol.md` |
| 当前迭代 | `docs/v0/entry/v0_current_iteration_plan.md` |
| 记忆结案 | `docs/real—live0/07_memory_engram_and_state_store.md`（U1–U25） |
| 机制追踪 | `docs/real—live0/00_reading_map_and_traceability.md` |

## 一句话定位

```text
动力学升级 ≠ 新 digital life
动力学升级 = 在 resident_turn_writeback / idle_strategy / memory U 链上
              补：连续积分、预测栈刷新、检索轻量改写、工作区 top-K
```

## 诚实边界

- `at_biological_human_parity` 恒为 `false`
- `engineering_rubric` 满分 ≠ 人脑 parity
- 72h 无 LLM 实验 = 审计夹具，非 merge gate