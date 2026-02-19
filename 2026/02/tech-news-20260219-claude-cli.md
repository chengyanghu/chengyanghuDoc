# Claude Code CLI 命令使用教程

**发布日期**: 2026-02-19

## 概述

Claude Code 是 Anthropic 官方推出的命令行工具，它是一个具备智能代码理解能力的终端助手，可以通过自然语言命令帮助开发者快速构建功能、调试问题、导航代码库和自动化任务。

## 核心特性

### 1. 基本命令结构

Claude Code 使用斜杠命令（Slash Commands）系统，命令文件采用 Markdown 格式，可选 YAML 前置元数据：

```markdown
---
description: 命令简要描述
argument-hint: [参数1] [参数2]
allowed-tools: Read, Bash(git:*)
---

命令提示内容：
- 参数: $1, $2, 或 $ARGUMENTS
- 文件: @path/to/file
- Bash: !`command here`
```

### 2. 常用配置字段

YAML 前置元数据支持的字段：
- **description**: 命令简要描述
- **allowed-tools**: 允许使用的工具（如 Read, Write）
- **model**: 指定模型（如 sonnet）
- **argument-hint**: 参数提示

### 3. Git 工作流命令示例

**仓库状态总结命令**:
```markdown
---
description: 总结 Git 仓库状态
allowed-tools: Bash(git:*)
---

仓库状态摘要：

**当前分支:** !`git branch --show-current`

**状态:** !`git status --short`

**最近提交:** !`git log --oneline -5`

**远程状态:** !`git fetch && git status -sb`

提供：
- 变更摘要
- 建议的下一步操作
- 任何警告或问题
```

使用方式：
```bash
> /git-status
```

### 4. 部署工作流

**初始化部署**:
创建 `.claude/deployment-state.local.md` 文件来持久化部署状态，记录：
- 当前 Git 分支
- 最新 commit hash
- 时间戳
- 部署状态

**智能部署条件分支**:
根据分支类型、测试结果、目标环境自动调整部署流程：
- main/master 分支：需要批准
- feature 分支：显示目标警告
- hotfix：快速通道处理

### 5. 最佳实践

**提交工作流**:
- 开发时使用 `/commit` 创建结构化提交
- 准备分享时使用 `/commit-push-pr` 推送并创建 PR
- 定期运行 `/clean_gone` 清理已删除的远程分支

**依赖检查**:
命令执行前验证必需工具（git, jq, node），提供清晰的错误信息和安装链接。

**命令编写技巧**:
- 从简单结构开始，单一职责
- 逐步添加复杂性，每次增加新功能后测试
- 使用描述性名称明确命令用途
- 始终用 `argument-hint` 记录参数
- 在注释中提供使用示例
- 考虑错误处理（缺失参数或文件）

## 参考链接

- [Claude Code 官方 GitHub](https://github.com/anthropics/claude-code)
- [命令开发文档](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/README.md)
- [工作流参考](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/advanced-workflows.md)

## 总结

Claude Code 通过自然语言命令和可扩展的斜杠命令系统，将 AI 能力深度集成到终端工作流中。无论是 Git 操作、代码分析还是自动化部署，都能通过简洁的命令快速完成，极大提升开发效率。

---

*本文档由 Context7 检索并整理，数据来源：Anthropic Claude Code 官方文档*
