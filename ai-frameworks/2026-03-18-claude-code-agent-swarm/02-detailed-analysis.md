# 详细分析

## 一、架构演进：从单 Agent 到蜂群

### 1.1 技术定位

Claude Code 是 Anthropic 的官方终端 AI 编码工具，经历了三个架构阶段 [[1]](https://medium.com/@devikanekkalapu7/inside-claude-codes-multi-agent-architecture-17cc162d5d7c)：

```
Stage 1: 单 Agent       → 一个 AI 助手 + 工具集
Stage 2: Subagent 委派   → 主 Agent 派生专用子代理
Stage 3: Agent Teams     → Leader + Workers 协作蜂群
```

### 1.2 单 Agent 核心架构

Claude Code 的基础是一个 **agentic loop**（自主循环）引擎 [[2]](https://platform.claude.com/docs/en/agent-sdk/overview)：

```
用户输入 → LLM 推理 → 工具选择 → 工具执行 → 结果反馈 → LLM 推理 → ... → 最终输出
```

内置工具集包括：

| 工具类别 | 工具名称 | 功能 |
|---------|---------|------|
| 文件操作 | Read, Write, Edit | 读取、创建、编辑文件 |
| 搜索 | Glob, Grep | 文件名匹配、内容搜索 |
| 执行 | Bash | Shell 命令执行 |
| 笔记本 | NotebookEdit | Jupyter Notebook 编辑 |
| 网络 | WebFetch, WebSearch | 网页获取和搜索 |
| 代理 | Agent | 派生子代理 |

每次工具调用都经过权限检查，由用户配置的 permission mode 控制（default / acceptEdits / plan / bypassPermissions）。

---

## 二、Subagent 子代理机制

### 2.1 核心概念

Subagent 是运行在**独立上下文窗口**中的专用 AI 助手。每个 Subagent 拥有 [[3]](https://code.claude.com/docs/en/sub-agents)：

- **独立上下文窗口**：不共享主对话的历史记录，避免上下文污染
- **自定义 System Prompt**：针对特定任务的角色定义
- **受限工具访问**：只能使用被授权的工具子集
- **独立权限控制**：可以使用不同的 permission mode
- **模型选择**：可以路由到不同模型（sonnet/opus/haiku）以控制成本

### 2.2 内置 Subagent 类型

| 类型 | 用途 | 可用工具 |
|------|------|--------|
| `general-purpose` | 复杂多步任务 | 全部工具 |
| `Explore` | 快速代码库探索 | 除 Agent/Edit/Write 外的全部工具 |
| `Plan` | 架构设计和实现规划 | 除 Agent/Edit/Write 外的全部工具 |
| `claude-code-guide` | Claude Code 使用指南查询 | Glob, Grep, Read, WebFetch, WebSearch |

### 2.3 自定义 Subagent

开发者可以通过两种方式定义自定义 Subagent [[3]](https://code.claude.com/docs/en/sub-agents)：

**方式一：Markdown 文件**（放置在 `.claude/agents/` 目录）

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
```

**方式二：CLI 动态定义**

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

### 2.4 SubagentStart Hook

通过 Hook 机制，可以在 Subagent 启动时注入额外上下文 [[4]](https://code.claude.com/docs/en/hooks)：

```json
{
  "hooks": {
    "SubagentStart": [{
      "matcher": "security-reviewer",
      "command": "echo '{\"additionalContext\": \"Follow OWASP Top 10 guidelines\"}'"
    }]
  }
}
```

### 2.5 Subagent 调度策略

Claude 会根据以下因素自动选择是否使用 Subagent：
- 任务复杂度和预计步骤数
- 是否需要保护主对话上下文窗口
- 是否需要并行探索多个方向
- 任务描述是否匹配某个 Subagent 的 description

---

## 三、Agent Teams 蜂群模式

### 3.1 概述

Agent Teams（又称 Swarm Mode）于 2026 年 2 月随 Claude Opus 4.6 正式发布，是 Claude Code 从单助手向多智能体协作平台的关键跃迁 [[5]](https://help.apiyi.com/en/claude-code-swarm-mode-multi-agent-guide-en.html)。

启用方式：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 3.2 架构设计：Leader + Workers

蜂群模式采用经典的 **Leader-Worker** 架构 [[6]](https://decodeclaude.com/teams-and-swarms/)：

```
                    ┌─────────────┐
                    │  Team Lead  │ ← 主 Claude Code 会话
                    │ (控制平面)   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼────┐ ┌────▼─────┐
        │ Worker A  │ │Worker B│ │ Worker C │
        │ API 重构  │ │ 测试   │ │  文档    │
        │ (Worktree)│ │(Worktree)│(Worktree)│
        └───────────┘ └────────┘ └──────────┘
```

**核心设计原则：控制平面与数据平面分离** [[6]](https://decodeclaude.com/teams-and-swarms/)

- **控制平面**（Leader）：审批、权限、策略、取消、关闭、健康检查
- **数据平面**（Workers）：消息、代码 diff、建议、实现工作

Leader 是唯一拥有"副作用决策权"的节点。Workers 是具有"有限自主权"的执行引擎。

### 3.3 TeammateTool 核心工具集

蜂群模式由一组工具组成 [[7]](https://gist.github.com/sorrycc/4702f258f3d505495f4d5d984576a08d)：

| 工具 | 功能 |
|------|------|
| **TeamCreateTool** | 创建新团队（1:1 绑定一个 Task List） |
| **TeamDeleteTool** | 清理团队目录、Worktree 和 Task List |
| **SendMessageTool** | 代理间通信：DM、广播、关闭请求/响应 |
| **TaskCreate** | 创建任务到共享 Task List |
| **TaskUpdate** | 更新任务状态、建立依赖关系 |
| **TaskList** | 查看所有任务和整体进度 |

### 3.4 通信机制：Mailbox 系统

代理间通过 Mailbox 系统通信 [[8]](https://code.claude.com/docs/en/agent-teams)：

- **点对点消息（DM）**：`SendMessage` 发送到特定 Teammate
- **广播（Broadcast）**：发送到所有 Teammate（慎用，会增加成本）
- **空闲通知**：Teammate 完成后自动通知 Leader
- **自动消息投递**：系统自动管理消息队列

### 3.5 Git Worktree 隔离

每个 Teammate 在独立的 Git Worktree 中工作 [[5]](https://help.apiyi.com/en/claude-code-swarm-mode-multi-agent-guide-en.html)：

```
main-repo/
├── .claude/worktrees/
│   ├── worker-api/      ← Worker A 的独立工作区
│   ├── worker-tests/    ← Worker B 的独立工作区
│   └── worker-docs/     ← Worker C 的独立工作区
```

- 每个 Worker 在独立分支上工作
- 测试通过后自动合并
- 消除并行开发的代码冲突

### 3.6 上下文与共享

每个 Teammate 启动时 [[8]](https://code.claude.com/docs/en/agent-teams)：

- ✅ 加载与常规会话相同的项目上下文（CLAUDE.md、MCP servers、Skills）
- ✅ 接收 Leader 的 spawn prompt
- ❌ **不会**获得 Leader 的对话历史
- 通过 Mailbox 和 Task List 实现信息共享

### 3.7 Subagent vs Agent Teams 对比

| 维度 | Subagent | Agent Teams |
|------|----------|-------------|
| 拓扑 | Hub-and-Spoke（中心辐射） | Mesh（网格） |
| 通信 | 仅与主 Agent 单向返回结果 | 代理间可直接通信 |
| 协作 | 隔离执行，结果回报 | 共享 Task List，协同工作 |
| 持久性 | 任务完成即销毁 | 可持续存活直到团队解散 |
| 适用场景 | 单一研究/验证任务 | 大型多模块并行开发 |
| Token 消耗 | 1-2x | 约 7x（plan mode） |

[[9]](https://medium.com/@jiten.p.oswal/the-switch-got-flipped-a-technical-deep-dive-into-anthropics-agent-teams-9e1093446f09)

---

## 四、Agent SDK 编程接口

### 4.1 概述

Claude Agent SDK 是官方 Python/TypeScript SDK，允许开发者以编程方式使用 Claude Code 的全部能力 [[10]](https://platform.claude.com/docs/en/agent-sdk/overview)：

```
pip install claude-agent-sdk        # Python
npm install @anthropic-ai/claude-agent-sdk  # TypeScript
```

### 4.2 核心 API：query()

`query()` 是流式异步函数，返回 Claude 工作过程中的消息流 [[10]](https://platform.claude.com/docs/en/agent-sdk/overview)：

```python
async for message in query(
    prompt="Find and fix bugs in auth.py",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Bash"],
        permission_mode="acceptEdits",
    ),
):
    # AssistantMessage: Claude 的推理和工具调用
    # ResultMessage: 最终结果
```

### 4.3 权限模式

| 模式 | 行为 |
|------|------|
| `default` | 标准权限行为，需要用户审批 |
| `acceptEdits` | 自动审批文件编辑 |
| `plan` | 规划模式，不执行任何操作 |
| `bypassPermissions` | 绕过所有权限检查（谨慎使用） |

支持会话中途动态切换 [[11]](https://platform.claude.com/docs/en/agent-sdk/permissions)：

```python
q = query(prompt="...", options=ClaudeAgentOptions(permission_mode="default"))
await q.set_permission_mode("acceptEdits")  # 动态切换
```

### 4.4 Hooks 系统

Agent SDK 支持基于正则匹配的 Hook 机制 [[12]](https://platform.claude.com/docs/en/agent-sdk/hooks)：

```python
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Write|Edit|Delete", hooks=[file_security_hook]),
            HookMatcher(matcher="^mcp__", hooks=[mcp_audit_hook]),
            HookMatcher(hooks=[global_logger]),  # 匹配所有工具
        ]
    }
)
```

Hook 类型：
- **PreToolUse**：工具执行前触发，可拦截或修改参数
- **PostToolUse**：工具执行后触发，可审计或过滤结果
- **SubagentStart**：子代理启动时触发，可注入上下文

### 4.5 GTVR 执行模式

Agent SDK 推荐的执行模式是 **GTVR**（Gather → Take Action → Verify → Repeat）[[13]](https://mcpmarket.com/tools/skills/claude-agent-sdk-python-automation)：

```
1. Gather: 收集信息（Read, Grep, Glob）
2. Take Action: 执行操作（Edit, Write, Bash）
3. Verify: 验证结果（运行测试、检查输出）
4. Repeat: 如有问题，重复上述步骤
```

---

## 五、最佳实践

### 5.1 Subagent 使用建议

1. **探索性任务优先委派**：代码库调研、依赖分析、模式搜索
2. **模型降级控制成本**：探索任务用 `sonnet`/`haiku`，关键实现用 `opus`
3. **明确工具约束**：只读任务限制为 `Read, Grep, Glob`，不给予 `Edit/Write`
4. **利用 SubagentStart Hook**：注入安全策略、编码规范等上下文

### 5.2 蜂群模式使用建议

1. **适合场景**：大型重构、多模块 feature、全面测试覆盖、并行 Code Review
2. **团队规模**：支持 2-16 个 Agent，推荐 3-5 个
3. **任务拆分**：按模块/职责划分，确保低耦合
4. **成本意识**：蜂群模式约消耗单会话 7x Token，评估 ROI 后使用
5. **广播慎用**：Broadcast 消息会发送给所有成员，尽量使用点对点 DM

### 5.3 Agent SDK 生产部署建议

1. **最小权限原则**：为每个 Agent 配置最小工具集和权限
2. **Hook 审计**：使用 PreToolUse Hook 记录所有工具调用
3. **动态权限**：初始受限，根据执行阶段逐步放开
4. **CI/CD 集成**：自动化 PR Review、测试生成、文档更新

---

## 六、常见陷阱

| 陷阱 | 后果 | 解决方案 |
|------|------|--------|
| 蜂群任务耦合度过高 | Workers 频繁通信，效率反降 | 按模块拆分，降低依赖 |
| Subagent 上下文过载 | 响应质量下降 | 限制任务范围，分多个 Subagent |
| bypassPermissions 滥用 | 安全风险 | 仅在可信 CI 环境使用 |
| 忽略 Token 成本 | 账单飙升 | 探索任务用 haiku/sonnet |
| Broadcast 过度使用 | 每个成员都消耗 Token 处理 | 优先使用 SendMessage 点对点 |
