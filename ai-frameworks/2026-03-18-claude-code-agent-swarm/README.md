# Claude Code Agent 与 Agent 蜂群 - 深度研究报告

> 📊 **研究概况**
> - 研究模式: 深度
> - 检索轮数: 8 轮 (Context7 5 轮 + Exa 3 轮)
> - 参考来源: 16 个
> - 生成日期: 2026-03-18

## 📋 执行摘要

Claude Code 已从单一 AI 编码助手演进为完整的多智能体协作平台。其架构分为三层：**单 Agent 核心**（基于 agentic loop 的工具调用引擎）、**Subagent 委派机制**（在独立上下文窗口中运行的专用子代理）、以及 **Agent Teams/Swarm 蜂群模式**（Leader + Workers 的多智能体协调系统）。Agent SDK 提供了 Python/TypeScript 编程接口，让开发者可以将 Claude Code 的全部能力嵌入到自定义应用和 CI/CD 流水线中。蜂群模式采用"控制平面 + 数据平面"分离的设计理念，通过 TeammateTool 实现代理间通信、任务分配和 Git Worktree 隔离，报告团队在大型项目上可获得 5-10x 开发效率提升。

**核心要点**：
- Claude Code 的 Agent 核心是一个基于工具调用的自主循环（agentic loop），支持 Read/Write/Edit/Bash/Grep/Glob 等原生工具
- Subagent 在独立上下文窗口运行，支持自定义 system prompt、工具访问权限和模型选择
- Agent Teams（蜂群模式）采用 Leader + Workers 架构，通过 Mailbox 系统和共享 Task List 协调
- Agent SDK 提供 `query()` 流式 API，支持 Hooks、动态权限、自定义工具等企业级功能
- 每个 Teammate 运行在独立 Git Worktree 中，避免代码冲突

## 📂 文档导航

| 文档 | 内容 | 预计阅读 |
|------|------|--------|
| [详细分析](02-detailed-analysis.md) | 完整技术架构研究 | 12 分钟 |
| [代码示例](03-code-examples.md) | Agent SDK 与蜂群实战代码 | 8 分钟 |
| [参考来源](99-references.md) | 完整引用列表 | 参考 |

## 🎯 快速导航

- 想了解三层架构演进？→ [详细分析 - 架构演进](02-detailed-analysis.md#一架构演进从单-agent-到蜂群)
- 想了解 Subagent 机制？→ [详细分析 - Subagent](02-detailed-analysis.md#二subagent-子代理机制)
- 想了解蜂群模式？→ [详细分析 - Agent Teams](02-detailed-analysis.md#三agent-teams-蜂群模式)
- 想了解 Agent SDK？→ [详细分析 - Agent SDK](02-detailed-analysis.md#四agent-sdk-编程接口)
- 想看代码示例？→ [代码示例](03-code-examples.md)

---
*Research Skill v4.0 生成 | 2026-03-18*
