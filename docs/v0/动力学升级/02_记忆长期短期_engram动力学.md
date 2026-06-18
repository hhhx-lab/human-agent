# 02 · 记忆机制（长期 / 短期 / Engram 动力学）

> **修订 v0.2** · 记忆 U1–U25 已 `engineering_complete` — **扩展，不重建**

## §修订摘要

| 已有资产 | `hippocampal_cue_index.activate_*`、`memory_retrieval._cue_activation_profile`、`apply_post_expression_reconsolidation`、`offline_memory_consolidation`、U13 重构召回 |
| 禁止重开 | cue 管、双写门、`engram_activation_graph` 平行库 |
| 增量改法 | `memory_trace_store` 增 salience/cue_weight 积分；检索轻量 delta；sleep 读 integrator |
| ITR 段 | **ITR-09-C**（在 A/B 之后） |

## 1. 理论锚点

- `docs/real—live0/07_memory_engram_and_state_store.md`
- `docs/05_memory_systems_and_growth.md`
- `docs/01q_memory_engram_consolidation_matrix.md`
- 核心：**线索触发、重构、再巩固**；召回 ≠ 写入

## 2. 现状 vs 动力学峰值

| 能力 | schema 现状 | 动力学峰值 | 生物人脑 |
|------|-------------|------------|----------|
| 分层召回 | tiered_recall 有 | + 激活竞争 | 极高 |
| 模式分离/补全 | 有帧 | + 图竞争抑制 | 高 |
| 再巩固 | 文档有，动态弱 | **检索即修改** | 极高 |
| 短期记忆 | 高激活隐式 | 显式 STM 子图 | 高 |
| 长期沉积 | 层级有 | 可及性衰减曲线 | 极高 |
| 睡眠巩固 | offline_consolidation | batch replay 合并 | 高 |
| 写门/事实边界 | **高** | **保持** | 高 |

**总评：** 重构性召回 中→**高**；再巩固 低→**中高**

## 3. 核心：在 MemoryTrace 上加厚（非新图模块）

**落点：** 扩展 `life_v0/state_store/memory_trace_store.py` + `hippocampal_cue_index.py`（修订：取消独立 `engram_activation_graph.py`）

每个 `MemoryTrace` / engram 节点新增/加厚字段：

```python
@dataclass
class EngramNode:
    trace_id: str
    activation: float          # 0..1
    decay_rate: float          # λ
    salience: float
    emotional_tag: float       # -1..1
    last_retrieved_at: str | None
    last_reconsolidated_at: str | None
    tier: Literal["stm", "core", "context", "sediment"]
    cue_weights: dict[str, float]
    source_refs: list[str]     # 审计不变
```

### 3.1 短期 vs 长期

```text
STM  = { node | activation > θ_stm OR age < T_stm }
LTM  = engram_index 中已晋升节点
沉积 = tier == sediment AND accessibility < θ_access
```

**不是两个库**，是同一图上的 **时间尺度分离**（符合理论「快索引-慢结构」）。

### 3.2 Spreading Activation（召回）

```text
输入 cue_terms → 种子节点激活 = 1.0
for hop in 1..H:
  邻居激活 += w_edge * activation(seed) * exp(-λ * Δt)
抑制:
  相似但不同 scope 的节点互相抑制（pattern_separation）
输出:
  top-N 节点 → memory_retrieval_frame.activated_refs
```

替代纯 `_cue_terms` 字符串匹配；保留 cue 匹配为 **种子初始化**。

### 3.3 再巩固（Reconsolidation on Retrieval）

每次 `project_memory_retrieval_from_live_turn` 成功激活节点：

```text
for node in activated:
  Δsalience = η * emotional_tag * prediction_error
  node.salience += Δsalience
  node.narrative_fragment = reconstruct(node, current_workspace, source_refs)
  append revision_history_refs
  node.last_reconsolidated_at = now
```

**约束：**

- `narrative_fragment` 变更必须保留 `source_refs`
- 梦境来源 trace 不得晋升 fact（DreamFactGate 不变）
- 高 `allostatic_load` 时 η 降低（防错误固化，AHB015）

### 3.4 可及性衰减与沉积

```text
accessibility(node, t) = salience * exp(-λ * (t - last_retrieved_at))

sleep tick:
  for node in batch_sample:
    if accessibility < θ_sediment:
      node.tier = sediment
    elif replay_merge_success:
      node.tier = core
      cortical_transfer_candidate = true
```

对接现有 `cortical_memory_transfer.py`、`offline_memory_consolidation.py`。

### 3.5 写入强度（编码）

```text
encoding_strength = (
  α1 * emotional_arousal
  + α2 * prediction_error
  + α3 * encoding_gain(cardiac_phase)
  - α4 * allostatic_load
  - α5 * body_state_debt
)
```

`memory_encoding_gate` / `memory_write_gate` 读 `encoding_strength`，非仅 episode 计数。

## 4. 与现有文件关系

| 现有 | 角色变化 |
|------|----------|
| `memory_retrieval.py` | 召回 orchestrator；检索成功调 `apply_retrieval_salience_delta` |
| `memory_trace_store.py` | 持久化节点字段扩展 |
| `engram_index.py` | 投影索引，非主动力学 |
| `hippocampal_cue_index.py` | cue_weights 初始化 |
| `pattern_separation.py` | 抑制矩阵 |
| `pattern_completion.py` | 部分线索补全触发激活 |
| `memory_write_gate.py` | 读 encoding_strength |
| `state_merge_guard.py` | 不变 |
| `resident_turn_writeback.py` | 回合末 graph.sync_to_store() |

## 5. 用户上下文与记忆的交界

- `context_accumulation_window` 持有 **STM 子图 ref 列表**，非全文堆叠
- 对话摘要进入 engram 节点，不单独维护平行「摘要库」
- `@文件` 引用生成 `observation_trace` 节点，经 TruthGate 后入图

## 6. Runtime 证据

| 文件 | 证明 |
|------|------|
| `runtime/state/memory/memory_trace_store.json` | salience/cue_weight 加厚 |
| `runtime/state/memory/memory_retrieval_frame.json` | 含 activation_scores |
| `runtime/state/memory/reconsolidation_event.jsonl` | 每次检索改写审计 |
| `runtime/state/memory/memory_longitudinal_profile.json` | 月级曲线 |

## 7. 测试 Gate

- `test_spreading_activation_from_cue`
- `test_pattern_separation_inhibits_cross_scope`
- `test_reconsolidation_changes_salience_with_audit`
- `test_high_load_suppresses_encoding`
- `test_sleep_migrates_tiers`
- `test_dream_trace_blocked_from_fact_promotion`（回归）
- 147+ memory tests 全绿

## 8. human_brain_alignment 预期

| 维度 | schema | 动力学后 |
|------|--------|----------|
| cue_reconstructive_recall | ~65% | ~82% |
| phenomenology_grounding | ~55% | ~72% |
| sleep_replay_selection | ~60% | ~78% |

仍 `at_biological_human_parity: false`；诚实估计封顶 ~82%（process live turn tier）。