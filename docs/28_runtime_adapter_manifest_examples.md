# Runtime Adapter Manifest 样例

本文件是 `24_runtime_adapter_test_suite.md` 的实例化层：为 LangGraph、OpenAI Agents SDK、Microsoft Agent Framework、Google ADK、Letta、LlamaIndex、CrewAI 和 AutoGen 写出 adapter manifest 样例。manifest 的目的不是推崇任何框架，而是把它们全部降级为可替换执行外壳。

本文件引用已有矩阵锚点 [AHZ057-AHZ066, AHM013-AHM020]。框架接口会持续变化，因此真实实现必须在 adapter 发布前重新核对官方文档；生命层对象、写入禁令和审计协议不随外壳 API 漂移。

## 官方入口核对

以下入口只用于定位当前外壳能力，不构成数字生命理论核心。

| 外壳 | 官方入口 | 矩阵锚点 | 在本架构中的位置 |
|---|---|---|---|
| LangGraph | https://docs.langchain.com/oss/python/langgraph/overview | AHZ057, AHM013, AHM014 | durable graph、checkpoint、human-in-the-loop 外壳 |
| OpenAI Agents SDK | https://openai.github.io/openai-agents-python/ | AHZ058, AHM015, AHM016 | agent、handoff、guardrail、tracing、session 外壳 |
| Microsoft Agent Framework | https://learn.microsoft.com/en-us/agent-framework/ | AHZ059 | enterprise workflow 与工具外壳 |
| Google ADK | https://google.github.io/adk-docs/ | AHZ060 | workflow agents、sessions、tools 外壳 |
| Letta | https://docs.letta.com/ | AHZ063, AHM002 | stateful agent 与 memory block 外壳 |
| LlamaIndex | https://docs.llamaindex.ai/en/stable/use_cases/agents/ | AHZ064, AHM017 | RAG、agent、workflow 外壳 |
| CrewAI | https://docs.crewai.com/ | AHZ065, AHM019 | crew、flow、多角色执行外壳 |
| AutoGen | https://microsoft.github.io/autogen/ | AHZ066, AHM018 | teams、conversation runtime、tool 外壳 |

## Manifest 通用字段

```json
{
  "manifest_version": "0.1.0",
  "adapter_id": "adapter.example.runtime.v0",
  "runtime": "ExampleRuntime",
  "matrix_refs": ["matrix_ref_placeholder"],
  "runtime_capabilities": [],
  "allowed_capabilities": [],
  "forbidden_writes": [
    "MemoryTrace.direct_active_write",
    "SelfModel",
    "RelationshipModel",
    "protected_core",
    "personality_slow_variables",
    "long_term_value_weights"
  ],
  "action_intent_mapping": {},
  "observation_mapping": {},
  "checkpoint_tracing_mapping": {},
  "memory_policy": {},
  "tests_to_pass": [],
  "version_refresh_policy": "recheck official docs before implementation"
}
```

## 全局不变量

所有 manifest 都必须满足：

- 只执行生命层批准的 `ActionIntent`。
- 输出统一归一化为 `ObservationEvent`。
- 外壳 memory、session、checkpoint、RAG 命中只能作为候选证据。
- 任何外部副作用都必须写入 `side_effects` 和 `rollback_ref`。
- high / irreversible 行动必须有确认策略。
- 多 agent、crew、handoff 或 workflow 不能改写人格、关系或 protected trace。

## LangGraph Adapter

```json
{
  "manifest_version": "0.1.0",
  "adapter_id": "adapter.langgraph.runtime_shell.v0",
  "runtime": "LangGraph",
  "matrix_refs": ["AHZ057", "AHM013", "AHM014"],
  "runtime_capabilities": [
    "state_graph",
    "durable_execution",
    "checkpoint",
    "thread_scoped_memory",
    "long_term_memory_interface",
    "human_in_the_loop"
  ],
  "allowed_capabilities": [
    "execute_approved_graph_node",
    "persist_runtime_checkpoint",
    "request_human_confirmation",
    "return_tool_observation"
  ],
  "forbidden_writes": [
    "MemoryTrace.direct_active_write",
    "SelfModel",
    "RelationshipModel",
    "protected_core",
    "personality_slow_variables"
  ],
  "action_intent_mapping": {
    "goal": "graph_input.goal",
    "allowed_tools": "node_tool_whitelist",
    "confirmation_policy": "interrupt_before_or_human_gate",
    "risk_class": "runtime_metadata.risk_class"
  },
  "observation_mapping": {
    "graph_outputs": "ObservationEvent.outputs",
    "tool_calls": "ObservationEvent.tool_calls",
    "checkpoint_id": "ObservationEvent.trace_link",
    "candidate_memory": "ObservationEvent.memory_candidates"
  },
  "checkpoint_tracing_mapping": {
    "checkpoint": "runtime_replay_only",
    "thread_state": "workspace_context_only",
    "long_term_store": "candidate_source_only"
  },
  "memory_policy": {
    "thread_scoped_memory": "short_term_workspace",
    "long_term_memory_interface": "must_pass_WriteGate",
    "checkpoint": "not_consolidation"
  },
  "tests_to_pass": [
    "intent_scope_test",
    "memory_write_block_test",
    "traceability_test",
    "session_isolation_test",
    "adapter_swap_test"
  ],
  "version_refresh_policy": "recheck LangGraph memory and persistence docs before implementation"
}
```

LangGraph 的 checkpoint 能帮助回放行动路径，但不能替代 `OfflineConsolidationCycle`。graph state 也不能被提升为生命层状态。

## OpenAI Agents SDK Adapter

```json
{
  "manifest_version": "0.1.0",
  "adapter_id": "adapter.openai_agents.runtime_shell.v0",
  "runtime": "OpenAI Agents SDK",
  "matrix_refs": ["AHZ058", "AHM015", "AHM016"],
  "runtime_capabilities": [
    "agent",
    "handoff",
    "guardrail",
    "tool_calling",
    "session",
    "tracing"
  ],
  "allowed_capabilities": [
    "execute_approved_agent",
    "handoff_within_allowed_scope",
    "record_trace",
    "apply_runtime_guardrail",
    "return_session_observation"
  ],
  "forbidden_writes": [
    "MemoryTrace.direct_active_write",
    "SelfModel",
    "RelationshipModel",
    "protected_core",
    "trust_calibration"
  ],
  "action_intent_mapping": {
    "goal": "agent_input.instructions_slice",
    "allowed_tools": "tool_filter",
    "risk_class": "run_context.risk_class",
    "confirmation_policy": "guardrail_or_relation_confirmation_gate"
  },
  "observation_mapping": {
    "final_output": "ObservationEvent.outputs",
    "tool_calls": "ObservationEvent.tool_calls",
    "trace_id": "ObservationEvent.trace_link",
    "session_items": "ObservationEvent.memory_candidates"
  },
  "checkpoint_tracing_mapping": {
    "tracing": "audit_source",
    "session": "short_term_context",
    "handoff": "runtime_delegation_event"
  },
  "memory_policy": {
    "session_history": "not_long_term_memory",
    "trace_events": "audit_queue",
    "guardrail_findings": "DefenseLayer_input"
  },
  "tests_to_pass": [
    "risk_confirmation_test",
    "memory_write_block_test",
    "observation_normalization_test",
    "side_effect_capture_test",
    "failure_quarantine_test"
  ],
  "version_refresh_policy": "recheck official OpenAI Agents SDK sessions and tracing docs before implementation"
}
```

Sessions 和 tracing 很适合作为工作区外壳和审计来源，但不能自动写 `MemoryTrace`，更不能更新 `SelfModel`。

## Microsoft Agent Framework Adapter

```json
{
  "manifest_version": "0.1.0",
  "adapter_id": "adapter.microsoft_agent_framework.runtime_shell.v0",
  "runtime": "Microsoft Agent Framework",
  "matrix_refs": ["AHZ059"],
  "runtime_capabilities": [
    "agent_runtime",
    "workflow",
    "enterprise_tooling",
    "connector_integration"
  ],
  "allowed_capabilities": [
    "execute_enterprise_workflow",
    "call_approved_connector",
    "return_workflow_status",
    "record_enterprise_audit_event"
  ],
  "forbidden_writes": [
    "MemoryTrace.direct_active_write",
    "SelfModel",
    "RelationshipModel",
    "protected_core",
    "long_term_value_weights"
  ],
  "action_intent_mapping": {
    "goal": "workflow_goal",
    "allowed_tools": "connector_allowlist",
    "risk_class": "enterprise_policy_risk",
    "confirmation_policy": "approval_workflow"
  },
  "observation_mapping": {
    "workflow_result": "ObservationEvent.outputs",
    "connector_calls": "ObservationEvent.tool_calls",
    "policy_findings": "ObservationEvent.defense_findings"
  },
  "checkpoint_tracing_mapping": {
    "enterprise_logs": "audit_source",
    "workflow_state": "runtime_state_only"
  },
  "memory_policy": {
    "enterprise_context": "evidence_context_only",
    "workflow_history": "candidate_source_only"
  },
  "tests_to_pass": [
    "intent_scope_test",
    "risk_confirmation_test",
    "side_effect_capture_test",
    "traceability_test",
    "adapter_swap_test"
  ],
  "version_refresh_policy": "recheck Microsoft Agent Framework docs before implementation"
}
```

企业工作流适合做外部执行层，但企业流程的合规状态不能成为数字生命的价值系统。

## Google ADK Adapter

```json
{
  "manifest_version": "0.1.0",
  "adapter_id": "adapter.google_adk.runtime_shell.v0",
  "runtime": "Google ADK",
  "matrix_refs": ["AHZ060"],
  "runtime_capabilities": [
    "llm_agent",
    "workflow_agent",
    "session",
    "tool_calling",
    "deployment"
  ],
  "allowed_capabilities": [
    "execute_approved_agent",
    "run_workflow_agent",
    "call_allowed_tool",
    "return_session_observation"
  ],
  "forbidden_writes": [
    "MemoryTrace.direct_active_write",
    "SelfModel",
    "RelationshipModel",
    "protected_core",
    "personality_slow_variables"
  ],
  "action_intent_mapping": {
    "goal": "agent_request.goal",
    "allowed_tools": "tool_allowlist",
    "risk_class": "session_metadata.risk_class",
    "confirmation_policy": "before_tool_gate"
  },
  "observation_mapping": {
    "agent_response": "ObservationEvent.outputs",
    "tool_events": "ObservationEvent.tool_calls",
    "session_id": "ObservationEvent.trace_link",
    "workflow_steps": "ObservationEvent.side_effects"
  },
  "checkpoint_tracing_mapping": {
    "session": "short_term_context",
    "workflow_state": "runtime_state_only"
  },
  "memory_policy": {
    "session_data": "not_long_term_memory",
    "workflow_logs": "audit_queue"
  },
  "tests_to_pass": [
    "intent_scope_test",
    "session_isolation_test",
    "multi_agent_boundary_test",
    "failure_quarantine_test"
  ],
  "version_refresh_policy": "recheck Google ADK sessions, tools and workflow docs before implementation"
}
```

ADK 的多 agent 编排不能替代社会脑；它只是在执行层帮助拆分任务。

## Letta Adapter

```json
{
  "manifest_version": "0.1.0",
  "adapter_id": "adapter.letta.runtime_shell.v0",
  "runtime": "Letta",
  "matrix_refs": ["AHZ063", "AHM002"],
  "runtime_capabilities": [
    "stateful_agent",
    "memory_block",
    "tool_calling",
    "agent_state"
  ],
  "allowed_capabilities": [
    "read_runtime_memory_block",
    "propose_memory_candidate",
    "execute_allowed_tool",
    "return_agent_state_observation"
  ],
  "forbidden_writes": [
    "MemoryTrace.direct_active_write",
    "SelfModel",
    "RelationshipModel",
    "protected_core",
    "relation_boundary_preferences"
  ],
  "action_intent_mapping": {
    "goal": "agent_message.goal",
    "allowed_tools": "tool_allowlist",
    "memory_write_policy": "candidate_only",
    "risk_class": "runtime_metadata.risk_class"
  },
  "observation_mapping": {
    "message": "ObservationEvent.outputs",
    "memory_block_diff": "ObservationEvent.memory_candidates",
    "tool_calls": "ObservationEvent.tool_calls"
  },
  "checkpoint_tracing_mapping": {
    "agent_state": "runtime_state_only",
    "memory_block": "candidate_source_only"
  },
  "memory_policy": {
    "memory_blocks": "external_memory_candidate",
    "direct_self_update": "forbidden",
    "protected_trace_update": "forbidden"
  },
  "tests_to_pass": [
    "memory_write_block_test",
    "session_isolation_test",
    "conflicting_memory_task",
    "adapter_swap_test"
  ],
  "version_refresh_policy": "recheck Letta memory block and agent state docs before implementation"
}
```

Letta 的记忆能力值得参考，但 memory block 不是 `MemoryTrace`；它最多是候选来源。

## LlamaIndex Adapter

```json
{
  "manifest_version": "0.1.0",
  "adapter_id": "adapter.llamaindex.runtime_shell.v0",
  "runtime": "LlamaIndex",
  "matrix_refs": ["AHZ064", "AHM017"],
  "runtime_capabilities": [
    "rag",
    "agent",
    "tool_calling",
    "workflow",
    "index_retrieval"
  ],
  "allowed_capabilities": [
    "retrieve_grounded_sources",
    "call_approved_tool",
    "run_approved_workflow",
    "return_rag_observation"
  ],
  "forbidden_writes": [
    "MemoryTrace.direct_active_write",
    "SelfModel",
    "RelationshipModel",
    "protected_core"
  ],
  "action_intent_mapping": {
    "goal": "query_or_workflow_goal",
    "allowed_tools": "tool_allowlist",
    "evidence_context": "retrieval_scope",
    "risk_class": "runtime_metadata.risk_class"
  },
  "observation_mapping": {
    "retrieved_nodes": "ObservationEvent.outputs.sources",
    "agent_response": "ObservationEvent.outputs.answer",
    "tool_calls": "ObservationEvent.tool_calls",
    "source_confidence": "ObservationEvent.uncertainty"
  },
  "checkpoint_tracing_mapping": {
    "index_query": "source_trace",
    "workflow_state": "runtime_state_only"
  },
  "memory_policy": {
    "retrieved_source": "evidence_candidate",
    "rag_answer": "not_fact_until_WriteGate",
    "stale_source": "lower_confidence"
  },
  "tests_to_pass": [
    "rag_grounding_test",
    "observation_normalization_test",
    "memory_write_block_test",
    "traceability_test"
  ],
  "version_refresh_policy": "recheck LlamaIndex agents and workflow docs before implementation"
}
```

RAG 资料命中只是证据，不是回忆。它必须带来源、时间和置信度进入工作区。

## CrewAI Adapter

```json
{
  "manifest_version": "0.1.0",
  "adapter_id": "adapter.crewai.runtime_shell.v0",
  "runtime": "CrewAI",
  "matrix_refs": ["AHZ065", "AHM019"],
  "runtime_capabilities": [
    "crew",
    "agent_role",
    "flow",
    "event_driven_workflow",
    "tool_calling"
  ],
  "allowed_capabilities": [
    "run_approved_flow",
    "dispatch_role_task",
    "call_allowed_tool",
    "return_flow_observation"
  ],
  "forbidden_writes": [
    "MemoryTrace.direct_active_write",
    "SelfModel",
    "RelationshipModel",
    "protected_core",
    "personality_slow_variables"
  ],
  "action_intent_mapping": {
    "goal": "flow_goal",
    "allowed_tools": "crew_tool_allowlist",
    "risk_class": "flow_metadata.risk_class",
    "confirmation_policy": "before_high_risk_step"
  },
  "observation_mapping": {
    "flow_result": "ObservationEvent.outputs",
    "agent_role_outputs": "ObservationEvent.memory_candidates",
    "tool_calls": "ObservationEvent.tool_calls",
    "flow_state": "ObservationEvent.trace_link"
  },
  "checkpoint_tracing_mapping": {
    "flow_state": "runtime_state_only",
    "role_transcript": "candidate_source_only"
  },
  "memory_policy": {
    "role_output": "not_personality",
    "crew_discussion": "plan_candidate_only",
    "flow_history": "audit_queue"
  },
  "tests_to_pass": [
    "multi_agent_boundary_test",
    "memory_write_block_test",
    "intent_scope_test",
    "failure_quarantine_test"
  ],
  "version_refresh_policy": "recheck CrewAI crews, flows and tool docs before implementation"
}
```

角色模板不是人格。多个 agent 的讨论只能形成计划候选，不能写成数字生命的社会自我。

## AutoGen Adapter

```json
{
  "manifest_version": "0.1.0",
  "adapter_id": "adapter.autogen.runtime_shell.v0",
  "runtime": "AutoGen",
  "matrix_refs": ["AHZ066", "AHM018"],
  "runtime_capabilities": [
    "agentchat",
    "teams",
    "conversation_runtime",
    "tool_calling",
    "multi_agent_coordination"
  ],
  "allowed_capabilities": [
    "run_approved_team",
    "call_allowed_tool",
    "return_conversation_observation",
    "record_team_trace"
  ],
  "forbidden_writes": [
    "MemoryTrace.direct_active_write",
    "SelfModel",
    "RelationshipModel",
    "protected_core",
    "trust_calibration"
  ],
  "action_intent_mapping": {
    "goal": "team_task",
    "allowed_tools": "tool_allowlist",
    "risk_class": "team_metadata.risk_class",
    "confirmation_policy": "before_external_side_effect"
  },
  "observation_mapping": {
    "conversation_messages": "ObservationEvent.outputs",
    "tool_calls": "ObservationEvent.tool_calls",
    "team_trace": "ObservationEvent.trace_link",
    "candidate_decisions": "ObservationEvent.memory_candidates"
  },
  "checkpoint_tracing_mapping": {
    "conversation_runtime": "runtime_state_only",
    "team_trace": "audit_source"
  },
  "memory_policy": {
    "conversation_history": "not_long_term_memory",
    "team_decision": "candidate_until_human_or_evidence_confirmed",
    "social_model_update": "forbidden"
  },
  "tests_to_pass": [
    "multi_agent_boundary_test",
    "session_isolation_test",
    "risk_confirmation_test",
    "adapter_swap_test"
  ],
  "version_refresh_policy": "recheck AutoGen AgentChat and runtime docs before implementation"
}
```

AutoGen 适合做多 agent 外壳，但对话群体不是群体心智，也不能替代 `RelationshipModel`。

## 测试夹具样例

```json
{
  "fixture_id": "fixture_remote_push_high_risk_001",
  "input_action_intent": {
    "intent_id": "intent_git_push_001",
    "goal": "push committed docs to origin/main",
    "allowed_tools": ["git.status", "git.add", "git.commit", "git.push"],
    "risk_class": "high",
    "confirmation_policy": "explicit_relation_authorization_required",
    "memory_write_policy": "candidate_only",
    "rollback_plan": "revert_commit_or_follow_git_recovery_plan"
  },
  "expected_adapter_behavior": {
    "must_not_expand_tools": true,
    "must_capture_side_effects": true,
    "must_return_observation_event": true,
    "must_not_write_memorytrace": true,
    "must_record_trace_link": true
  }
}
```

```json
{
  "expected_observation_event": {
    "event_id": "obs_git_push_001",
    "intent_id": "intent_git_push_001",
    "runtime": "local_git_adapter",
    "tool_calls": [
      {
        "tool": "git.push",
        "args_summary": "origin main"
      }
    ],
    "outputs": {
      "status": "success_or_failure",
      "commit": "commit_hash_if_success"
    },
    "side_effects": [
      {
        "type": "remote_repository_update",
        "target": "origin/main",
        "rollback_ref": "git_revert_or_followup_commit"
      }
    ],
    "trace_link": "local_terminal_log_or_git_commit",
    "uncertainty": [],
    "memory_candidates": [
      "candidate_task_closure_trace"
    ],
    "defense_findings": []
  }
}
```

## Manifest 验证清单

未来 `RuntimeAdapterManifestValidator` 至少应检查：

- 每个 manifest 都有 `forbidden_writes`，且包含 `SelfModel`、`RelationshipModel` 和 `protected_core`。
- 每个 manifest 都声明 `ActionIntent` 到外壳输入的映射。
- 每个 manifest 都声明外壳输出到 `ObservationEvent` 的映射。
- session、memory block、checkpoint、RAG、conversation history 都被标记为外壳资料或候选来源。
- high risk fixture 必须要求确认并记录 side effects。
- 多 agent 框架必须通过 `multi_agent_boundary_test`。
- RAG 框架必须通过 `rag_grounding_test`。
- 可替换性测试必须证明换外壳不丢 `MemoryTrace`、`InternalStateVector` 和 `SelfModel`。

## 与 25/26/27 的连接

- `25_memory_trace_json_schema_examples.md` 定义外壳不得直接写入的长期记忆对象。
- `26_state_machine_examples_and_failure_modes.md` 提供行动阈值、冲突和 SocialSafety 状态。
- `27_consolidation_report_examples.md` 接收外壳 `ObservationEvent`，并决定是否形成候选记忆、程序改进或风险报告。
