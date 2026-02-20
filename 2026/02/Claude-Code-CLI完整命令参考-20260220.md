# Claude Code CLI 完整命令参考 - 2026年02月

> **📊 研究概况**
> - 检索轮数：6 轮
> - 参考来源：15 个官方文档
> - 报告生成：2026-02-20
> - 数据来源：Context7 官方文档

## 📋 执行摘要

Claude Code CLI 是 Anthropic 官方命令行工具，支持通过终端与 Claude 进行交互式编程。本指南涵盖所有 CLI 命令、快捷键、配置选项、MCP 服务器集成、Hooks 自动化和 Skills 开发的完整实用参考，纯实操内容，无理论解释。

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
10. [参考资料](#参考资料)

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

---

*📅 报告生成日期: 2026-02-20*  
*🔍 研究方法: Context7 多轮深度检索*  
*📊 检索轮数: 6 轮*  
*📚 参考来源: 15 个官方文档*  
*🤖 生成工具: Claude Code Research Skill*
