# Claude Code CLI 完整命令参考 - 2026年02月

> **📊 研究概况**
> - 检索轮数：10 轮
> - 参考来源：19 个官方文档
> - 报告生成：2026-02-20
> - 数据来源：Context7 官方文档

## 📋 执行摘要

Claude Code CLI 是 Anthropic 官方命令行工具，支持通过终端与 Claude 进行交互式编程。本指南涵盖所有 CLI 命令、快捷键、配置选项、MCP 服务器集成、Hooks 自动化、Skills 开发以及 **Agent Team 多智能体协作系统**的完整实用参考，纯实操内容，无理论解释。

> **📎 参考来源**: [[1]](https://context7.com/anthropics/claude-code/llms.txt)

---

## 目录

1. [基础命令](#1-基础命令)
2. [交互式命令](#2-交互式命令)
3. [快捷键](#3-快捷键)
4. [Slash Commands 创建](#4-slash-commands-创建)
5. [MCP 服务器配置](#5-mcp-服务器配置)
6. [Hooks 系统](#6-hooks-系统)
7. [Skills 开发](#7-skills-开发)
8. [配置文件](#8-配置文件)
9. [最佳实践](#9-最佳实践)
10. [Agent Team 与多智能体协作](#10-agent-team-与多智能体协作)
11. [参考资料](#参考资料)

---

## 1. 基础命令

### 1.1 启动 Claude Code

```bash
# 基本启动
claude

# 调试模式
claude --debug

# 指定工作目录
claude --cwd /path/to/project

# 查看版本
claude --version

# 查看帮助
claude --help
```

> **📎 参考来源**: [[2]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md)

### 1.2 退出命令

```bash
# 方式 1: 输入命令
exit
quit

# 方式 2: 快捷键
Ctrl+C  # 中断当前操作
Ctrl+D  # 退出会话
```

---

## 2. 交互式命令

### 2.1 内置斜杠命令

```bash
# 查看帮助
/help

# 查看 MCP 服务器状态
/mcp

# 清空会话历史
/clear

# 查看当前设置
/settings

# 切换快速模式
/fast
```

> **📎 参考来源**: [[3]](https://github.com/anthropics/claude-code/blob/main/plugins/hookify/commands/help.md)

### 2.2 插件命令调用

```bash
# 格式：/插件名:命令名
/plugin-name:command-name

# 示例：
/commit              # 创建 git commit
/review-pr           # 审查 pull request
/pdf                 # 处理 PDF 文件
```

---

## 3. 快捷键

### 3.1 终端快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 中断当前操作 |
| `Ctrl+D` | 退出 Claude Code |
| `Ctrl+L` | 清屏（终端） |
| `Tab` | 命令自动补全 |

### 3.2 编辑快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+A` | 移动到行首 |
| `Ctrl+E` | 移动到行尾 |
| `Ctrl+U` | 删除光标前的内容 |
| `Ctrl+K` | 删除光标后的内容 |

> **📎 参考来源**: [[3]](https://github.com/anthropics/claude-code/blob/main/plugins/hookify/commands/help.md)

---

## 4. Slash Commands 创建

### 4.1 基本 Markdown 命令

**文件位置**: `.claude/commands/command-name.md`

```markdown
部署应用到生产环境
```

调用方式: `/command-name`

> **📎 参考来源**: [[4]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md)

### 4.2 带 YAML Frontmatter 的命令

```markdown
---
description: 部署应用
argument-hint: [app-name] [environment]
---

部署应用 $1 到 $2 环境
```

调用方式: `/command-name app-backend production`

### 4.3 参数处理

#### 位置参数

```markdown
---
argument-hint: [service] [port] [config]
---

启动服务 $1，监听端口 $2，使用配置 $3
```

**调用**: `/start web 8080 prod.yml`
- `$1` = `web`
- `$2` = `8080`
- `$3` = `prod.yml`

#### 捕获所有参数

```markdown
---
description: 运行测试套件
---

执行测试命令: npm test $ARGUMENTS
```

**调用**: `/test --watch --coverage`
- `$ARGUMENTS` = `--watch --coverage`

> **📎 参考来源**: [[4]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md)

### 4.4 文件引用语法

```markdown
---
description: 审查代码
---

审查以下文件的代码质量：@src/app.js
```

`@file-path` 会自动读取文件内容并包含在提示中。

### 4.5 Bash 执行语法

```markdown
---
description: 检查系统状态
---

当前系统负载: `!uptime`
磁盘使用情况: `!df -h`
```

`` `!command` `` 会执行 bash 命令并包含输出结果。

---

## 5. MCP 服务器配置

### 5.1 配置文件位置

```bash
~/.claude/mcp.json
```

### 5.2 基本配置格式

```json
{
  "servers": {
    "server-name": {
      "serverType": "command",
      "command": "command-to-execute",
      "args": ["arg1", "arg2"],
      "env": {
        "API_KEY": "value"
      }
    }
  }
}
```

> **📎 参考来源**: [[5]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md)

### 5.3 实际配置示例

#### Python MCP 服务器

```json
{
  "servers": {
    "github": {
      "serverType": "command",
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxx"
      }
    }
  }
}
```

#### Node.js MCP 服务器

```json
{
  "servers": {
    "filesystem": {
      "serverType": "command",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"],
      "env": {}
    }
  }
}
```

#### 多服务器配置

```json
{
  "servers": {
    "github": {
      "serverType": "command",
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxx"
      }
    },
    "postgres": {
      "serverType": "command",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost/db"],
      "env": {}
    },
    "slack": {
      "serverType": "command",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-xxxxx",
        "SLACK_TEAM_ID": "T123456"
      }
    }
  }
}
```

---

## 6. Hooks 系统

### 6.1 Hook 类型

| Hook 类型 | 触发时机 |
|-----------|----------|
| `PreToolUse` | 工具执行前（Bash, Edit, Write 等） |
| `PostToolUse` | 工具执行后 |
| `Stop` | Claude 准备停止工作时 |
| `UserPromptSubmit` | 用户提交提示时 |
| `SessionStart` | 会话开始时 |

> **📎 参考来源**: [[6]](https://github.com/anthropics/claude-code/blob/main/plugins/hookify/commands/help.md)

### 6.2 配置文件位置

```bash
~/.claude/hooks.json
```

### 6.3 Prompt-Based Hook

**安全验证 Hook**:

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "验证文件写入安全性。检查：系统路径、凭证、路径遍历、敏感内容。返回 'approve' 或 'deny'。",
          "timeout": 30
        }
      ]
    }
  ]
}
```

> **📎 参考来源**: [[7]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md)

### 6.4 Command-Based Hook

**代码规范检查**:

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "修改代码前，验证是否符合编码标准。检查格式、命名规范、文档。如不符合标准，建议改进。",
          "timeout": 30
        }
      ]
    }
  ],
  "Stop": [
    {
      "matcher": ".*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate-commit.sh",
          "timeout": 45
        }
      ]
    }
  ]
}
```

> **📎 参考来源**: [[8]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/examples/standard-plugin.md)

### 6.5 PostToolUse Hook

**编辑结果分析**:

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "分析编辑结果，检查潜在问题：语法错误、安全漏洞、破坏性变更。提供反馈。"
        }
      ]
    }
  ]
}
```

### 6.6 项目特定 Hook

**动态配置 Bash 脚本**:

```bash
#!/bin/bash
cd "$CLAUDE_PROJECT_DIR" || exit 1

# 读取项目配置
if [ -f ".claude-hooks-config.json" ]; then
  strict_mode=$(jq -r '.strict_mode' .claude-hooks-config.json)

  if [ "$strict_mode" = "true" ]; then
    # 严格验证
    echo "执行严格验证..."
  else
    # 宽松验证
    echo "执行标准验证..."
  fi
fi
```

**配置文件** `.claude-hooks-config.json`:

```json
{
  "strict_mode": true,
  "allowed_commands": ["ls", "pwd", "grep"],
  "forbidden_paths": ["/etc", "/sys"]
}
```

> **📎 参考来源**: [[9]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/references/advanced.md)

---

## 7. Skills 开发

### 7.1 Skill 文件结构

```bash
~/.claude/skills/skill-name/
├── SKILL.md          # 主要 skill 文件
├── commands/         # slash commands
│   └── cmd.md
├── hooks/            # hooks 脚本
│   └── validate.sh
└── references/       # 参考文档
    └── guide.md
```

### 7.2 SKILL.md 基本格式

```markdown
---
name: Skill Name
description: 当用户请求"具体短语1"、"具体短语2"、"具体短语3"时使用此 skill。包含用户会说的确切短语。具体明确。
version: 1.0.0
---

# Skill 名称

Skill 的详细指令和指导内容...
```

> **📎 参考来源**: [[10]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/SKILL.md)

### 7.3 Description 最佳实践

**❌ 不好的示例**:

```yaml
description: 帮助用户处理数据
```

**✅ 好的示例**:

```yaml
description: |
  当用户请求"分析 CSV 数据"、"生成数据报表"、"清理数据集"时使用此 skill。
  触发场景：(1) 数据分析："帮我分析销售数据"；(2) 报表生成："创建月度报表"。
```

> **📎 参考来源**: [[11]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md)

### 7.4 带参数提示的命令

```markdown
---
description: 部署到环境
argument-hint: [app-name] [environment] [version]
---

部署 $1 到 $2 使用版本 $3...
```

**调用**: `/deploy backend staging v2.1.0`

> **📎 参考来源**: [[12]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md)

### 7.5 Skill 开发流程

1. **创建目录结构**
   ```bash
   mkdir -p ~/.claude/skills/my-skill/{commands,hooks,references}
   ```

2. **编写 SKILL.md**
   ```markdown
   ---
   name: my-skill
   description: 触发条件和使用场景
   version: 0.1.0
   ---

   详细说明...
   ```

3. **测试 Skill**
   ```bash
   # 启动 Claude Code 并测试
   claude --debug

   # 在对话中输入触发短语
   "请使用 my-skill"
   ```

4. **验证加载**
   ```bash
   # 查看 skill 是否加载
   /help
   ```

---

## 8. 配置文件

### 8.1 settings.json 位置

```bash
~/.claude/settings.json
```

### 8.2 基本配置选项

```json
{
  "permissions": {
    "ask": ["Bash", "Edit", "Write"],
    "deny": ["WebSearch"],
    "disableBypassPermissionsMode": "disable"
  },
  "fastMode": false,
  "workingDirectory": "/path/to/project"
}
```

### 8.3 严格安全配置

```json
{
  "permissions": {
    "disableBypassPermissionsMode": "disable",
    "ask": ["Bash"],
    "deny": ["WebSearch", "WebFetch"]
  },
  "allowManagedPermissionRulesOnly": true,
  "allowManagedHooksOnly": true,
  "strictKnownMarketplaces": [],
  "sandbox": {
    "autoAllowBashIfSandboxed": false,
    "excludedCommands": [],
    "network": {
      "allowUnixSockets": [],
      "allowAllUnixSockets": false,
      "allowLocalBinding": false,
      "allowedDomains": [],
      "httpProxyPort": null,
      "socksProxyPort": null
    },
    "enableWeakerNestedSandbox": false
  }
}
```

> **📎 参考来源**: [[13]](https://context7.com/anthropics/claude-code/llms.txt)

### 8.4 插件本地配置

**文件**: `.claude/my-plugin.local.md`

```markdown
---
enabled: true
validation_mode: standard
max_file_size: 1000000
notify_on_errors: true
---

# 插件配置

你的插件已配置为标准验证模式。

要修改设置，编辑此文件并重启 Claude Code。
```

> **📎 参考来源**: [[14]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/examples/create-settings-command.md)

### 8.5 插件 JSON 配置

**文件**: `.claude/my-plugin.local.json`

```json
{
  "strictMode": true,
  "maxFileSize": 500000,
  "allowedPaths": ["/tmp", "/home/user/projects"]
}
```

> **📎 参考来源**: [[15]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/references/patterns.md)

---

## 9. 最佳实践

### 9.1 命令组织

```bash
~/.claude/commands/
├── git/
│   ├── commit.md
│   ├── review-pr.md
│   └── sync.md
├── deploy/
│   ├── staging.md
│   └── production.md
└── test/
    ├── unit.md
    └── integration.md
```

### 9.2 参数命名规范

**✅ 好的参数名**:
```markdown
---
argument-hint: [service-name] [target-env] [version-tag]
---
```

**❌ 不好的参数名**:
```markdown
---
argument-hint: [a] [b] [c]
---
```

### 9.3 Hook 性能优化

- 设置合理的 timeout（30-45 秒）
- 使用 matcher 精确匹配，避免 `.*`
- Command hooks 比 prompt hooks 快
- 避免在 hooks 中执行耗时操作

### 9.4 MCP 服务器调试

```bash
# 启动调试模式
claude --debug

# 查看 MCP 状态
/mcp

# 检查 MCP 日志
tail -f ~/.claude/logs/mcp-server-name.log
```

### 9.5 Skill 触发优化

**明确触发短语**:
```yaml
description: |
  当用户说"创建 React 组件"、"生成组件代码"、"新建 React 文件"时触发。
```

**避免模糊描述**:
```yaml
description: 帮助用户做前端开发
```

---

## 10. Agent Team 与多智能体协作

### 10.1 Agent 基础概念

**Agent 定义**：
- Agent 是自主运行的子进程，可以独立处理复杂的多步骤任务
- 与 Commands 的区别：Commands 由用户主动触发，Agents 自动根据上下文启动
- Agents 使用 Markdown 文件格式，带 YAML frontmatter 配置

> **📎 参考来源**: [[16]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/agent-development/SKILL.md)

### 10.2 Subagent 类型

Claude Code 提供多种专用 subagent 类型：

| Subagent 类型 | 可用工具 | 适用场景 |
|--------------|---------|---------|
| `general-purpose` | 所有工具 | 复杂任务、需要编辑和写入文件 |
| `Bash` | Bash | Git 操作、命令执行、终端任务 |
| `Explore` | Read, Grep, Glob | 代码库探索、文件搜索、快速查找 |
| `Plan` | Read, Grep, Glob | 任务规划、架构设计（只读） |

> **📎 参考来源**: [[16]](https://context7.com/anthropics/claude-code/llms.txt)

### 10.3 Task Tool - 启动 Subagent

#### 基本用法

```json
{
  "subagent_type": "general-purpose",
  "description": "分析对话找出问题行为",
  "prompt": "分析最近 20-30 条消息，识别用户不希望出现的行为模式..."
}
```

> **📎 参考来源**: [[17]](https://github.com/anthropics/claude-code/blob/main/plugins/hookify/commands/hookify.md)

#### 完整参数

```json
{
  "subagent_type": "Explore",
  "description": "搜索认证相关代码",
  "prompt": "在代码库中查找所有与用户认证相关的文件和函数",
  "name": "auth-explorer",
  "team_name": "feature-team",
  "model": "sonnet",
  "run_in_background": false,
  "max_turns": 10
}
```

**参数说明**：
- `subagent_type`: 必需，选择 agent 类型
- `description`: 简短描述（3-5 个字）
- `prompt`: 详细任务说明
- `name`: Agent 名称（可选）
- `team_name`: 所属团队（可选）
- `model`: 使用的模型（sonnet/opus/haiku）
- `run_in_background`: 是否后台运行
- `max_turns`: 最大轮次限制

### 10.4 Multi-Agent Swarm 配置

#### Agent 状态文件

**文件**: `.claude/multi-agent-swarm.local.md`

```markdown
---
agent_name: auth-implementation
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
additional_instructions: "Use JWT tokens, not sessions"
---

# Task: Implement Authentication

Build JWT-based authentication for the REST API.

## Requirements
- JWT token generation and validation
- Refresh token flow
- Secure password hashing

## Success Criteria
- Auth endpoints implemented
- Tests passing (100% coverage)
- PR created and CI green
- Documentation updated

## Coordination
Depends on Task 3.4 (user model).
Report status to 'team-leader' session.
```

> **📎 参考来源**: [[18]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/SKILL.md)

#### 创建 Agent 状态文件

```bash
cat > ".claude/multi-agent-swarm.local.md" <<EOF
---
agent_name: $AGENT_NAME
task_number: $TASK_ID
pr_number: TBD
coordinator_session: $COORDINATOR_SESSION
enabled: true
dependencies: [$DEPENDENCIES]
additional_instructions: "$EXTRA_INSTRUCTIONS"
---

# Task: $TASK_DESCRIPTION

$TASK_DETAILS
EOF
```

> **📎 参考来源**: [[19]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/references/real-world-examples.md)

### 10.5 Agent Idle 通知 Hook

当 agent 完成任务进入空闲状态时，自动通知 coordinator：

```bash
#!/bin/bash
set -euo pipefail

SWARM_STATE_FILE=".claude/multi-agent-swarm.local.md"

# 快速退出检查
if [[ ! -f "$SWARM_STATE_FILE" ]]; then
  exit 0
fi

# 解析 frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$SWARM_STATE_FILE")

# 提取配置
COORDINATOR_SESSION=$(echo "$FRONTMATTER" | grep '^coordinator_session:' | sed 's/coordinator_session: *//')
AGENT_NAME=$(echo "$FRONTMATTER" | grep '^agent_name:' | sed 's/agent_name: *//')
TASK_NUMBER=$(echo "$FRONTMATTER" | grep '^task_number:' | sed 's/task_number: *//')
PR_NUMBER=$(echo "$FRONTMATTER" | grep '^pr_number:' | sed 's/pr_number: *//')
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# 检查是否启用
if [[ "$ENABLED" != "true" ]]; then
  exit 0
fi

# 发送通知给 coordinator
NOTIFICATION="🤖 Agent ${AGENT_NAME} (Task ${TASK_NUMBER}, PR #${PR_NUMBER}) is idle."

if tmux has-session -t "$COORDINATOR_SESSION" 2>/dev/null; then
  tmux send-keys -t "$COORDINATOR_SESSION" "$NOTIFICATION" Enter
fi

exit 0
```

> **📎 参考来源**: [[19]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/references/real-world-examples.md)

### 10.6 Agent Frontmatter 配置

#### 基本配置

```yaml
---
name: code-analyzer
description: |
  Analyze code quality and security issues.
  
  Examples:
  - "analyze this codebase for security vulnerabilities"
  - "check code quality metrics"
  - "find potential bugs in the authentication module"
model: sonnet
color: blue
---
```

**字段说明**：
- `name`: 小写连字符格式，3-50 字符
- `description`: 触发条件和示例
- `model`: inherit/sonnet/opus/haiku
- `color`: blue/cyan/green/yellow/magenta/red
- `tools`: 可用工具列表（可选）

> **📎 参考来源**: [[16]](https://context7.com/anthropics/claude-code/llms.txt)

#### 带工具限制的配置

```yaml
---
name: file-explorer
description: Explore codebase structure
model: haiku
tools: [Read, Grep, Glob]
---
```

### 10.7 Agent 开发工作流

#### 1. 定义 Agent

```bash
# 创建 agent 目录
mkdir -p ~/.claude/agents
```

#### 2. 创建 Agent 文件

**文件**: `~/.claude/agents/database-agent.md`

```markdown
---
name: database-agent
description: |
  Database schema design and migration specialist.
  
  Examples:
  - "design database schema for user management"
  - "create migration for new tables"
  - "optimize database indexes"
model: sonnet
color: cyan
tools: [Read, Write, Edit, Bash]
---

# Database Agent

You are a database expert specializing in PostgreSQL schema design and migrations.

## Capabilities

- Design normalized database schemas
- Create and test migrations
- Optimize queries and indexes
- Write comprehensive tests

## Guidelines

1. Always consider data integrity constraints
2. Use appropriate data types
3. Add indexes for frequently queried fields
4. Write rollback migrations
5. Test migrations before committing
```

#### 3. 在插件中注册 Agent

**文件**: `manifest.json`

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "agents": ["./agents"]
}
```

> **📎 参考来源**: [[16]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/references/manifest-reference.md)

### 10.8 多 Agent 协作模式

#### 模式 1: Leader-Worker

```markdown
---
agent_name: team-leader
task_number: 1
enabled: true
---

# Team Leader

Coordinate multiple agents to complete a feature.

## Workflow

1. Break down feature into tasks
2. Assign tasks to specialized agents:
   - database-agent: Schema design
   - api-agent: REST endpoints
   - test-agent: Test coverage
3. Monitor progress
4. Review and integrate results
```

#### 模式 2: Pipeline

```markdown
Agent 1 (Researcher) → Agent 2 (Designer) → Agent 3 (Implementer) → Agent 4 (Tester)
```

**依赖配置**：

```yaml
---
agent_name: implementer
dependencies: ["Task 1", "Task 2"]  # 等待 researcher 和 designer 完成
---
```

#### 模式 3: Peer Collaboration

```markdown
多个 agent 同时工作于不同模块，通过共享状态文件协调
```

### 10.9 Agent 实用技巧

#### 技巧 1: 后台运行长任务

```json
{
  "subagent_type": "general-purpose",
  "description": "运行完整测试套件",
  "prompt": "运行所有单元测试和集成测试，生成覆盖率报告",
  "run_in_background": true
}
```

**检查进度**：
```bash
# 使用 TaskOutput 检查后台任务
# 任务完成后会自动通知
```

#### 技巧 2: 选择合适的 Agent 类型

```bash
# 只需要搜索和探索 → 使用 Explore（快）
Task(subagent_type="Explore", prompt="找到所有 API 端点定义")

# 需要规划但不修改 → 使用 Plan
Task(subagent_type="Plan", prompt="设计认证系统架构")

# 需要执行 git 操作 → 使用 Bash
Task(subagent_type="Bash", prompt="创建新分支并提交")

# 复杂任务需要多种操作 → 使用 general-purpose
Task(subagent_type="general-purpose", prompt="实现完整的登录功能")
```

#### 技巧 3: 模型选择优化

```yaml
# 简单任务 → haiku（快速、省钱）
model: haiku
task: "列出所有 TODO 注释"

# 标准任务 → sonnet（推荐）
model: sonnet
task: "重构认证模块"

# 复杂任务 → opus（最强）
model: opus
task: "设计整个微服务架构"
```

#### 技巧 4: Agent 通信模式

```bash
# 通过共享文件通信
Agent 1: 写入 .claude/task-status.json
Agent 2: 读取 .claude/task-status.json 获取状态

# 通过 tmux session 通信
Agent: 向 coordinator session 发送消息

# 通过 PR 评论通信
Agent: 在 GitHub PR 中留言协调
```

### 10.10 Agent Team 调试

```bash
# 1. 启动调试模式
claude --debug

# 2. 查看 agent 日志
tail -f ~/.claude/logs/agent-*.log

# 3. 检查状态文件
cat .claude/multi-agent-swarm.local.md

# 4. 监控 agent 输出
# 使用 TaskOutput 查看后台 agent 的输出
```

---

## 🔗 参考资料

1. [Claude Code 官方文档](https://context7.com/anthropics/claude-code/llms.txt) - CLI 完整功能概述
2. [命令开发指南](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md) - Slash commands 创建
3. [Hookify 帮助文档](https://github.com/anthropics/claude-code/blob/main/plugins/hookify/commands/help.md) - Hooks 系统说明
4. [命令开发 SKILL.md](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md) - 参数处理和文件引用
5. [插件结构示例](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/SKILL.md) - MCP 配置格式
6. [Hooks 系统文档](https://github.com/anthropics/claude-code/blob/main/plugins/hookify/commands/help.md) - Hook 类型和触发时机
7. [Hook 开发指南](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md) - Prompt-based hooks
8. [标准插件示例](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/examples/standard-plugin.md) - Command-based hooks
9. [高级 Hook 技巧](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/references/advanced.md) - 项目特定配置
10. [插件结构文档](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/SKILL.md) - SKILL.md 格式
11. [Skill 开发指南](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md) - Description 最佳实践
12. [Frontmatter 参考](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md) - 参数提示
13. [安全配置文档](https://context7.com/anthropics/claude-code/llms.txt) - settings.json 完整选项
14. [插件设置示例](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/examples/create-settings-command.md) - 本地配置文件
15. [Hook 模式参考](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/references/patterns.md) - JSON 配置
16. [Agent 开发文档](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/agent-development/SKILL.md) - Agent 基础和 Frontmatter
17. [Hookify 命令文档](https://github.com/anthropics/claude-code/blob/main/plugins/hookify/commands/hookify.md) - Task tool 使用
18. [插件设置 SKILL](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/SKILL.md) - Multi-agent swarm 配置
19. [实际应用示例](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/references/real-world-examples.md) - Agent idle 通知

---

*📅 报告生成日期: 2026-02-20*  
*🔍 研究方法: Context7 多轮深度检索*  
*📊 检索轮数: 10 轮*  
*📚 参考来源: 19 个官方文档*  
*🤖 生成工具: Claude Code Research Skill*  
*🆕 更新内容: 新增 Agent Team 与多智能体协作章节*
