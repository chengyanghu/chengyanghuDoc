# Claude Code CLI 实战配置指南 - 2026年02月

## 📋 概述

本指南聚焦于Claude Code CLI的实用配置和命令操作，去除理论介绍，直接提供可复制使用的配置示例和命令清单。

> **📎 参考来源**: [[1]](https://github.com/anthropics/claude-code) [[2]](https://code.claude.com/docs/en/settings)

---

## ⚙️ 核心配置文件

### settings.json 配置

**文件位置**: `~/.claude/settings.json` 或项目根目录 `.claude/settings.json`

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs"
  ]
}
```

> **📎 参考来源**: [[2]](https://code.claude.com/docs/en/settings)

**配置说明**:
- **permissions.allow**: 白名单命令，Claude可直接执行
- **permissions.deny**: 黑名单规则，禁止访问敏感文件和命令
- **env**: 环境变量设置
- **companyAnnouncements**: 团队公告，每次启动时显示

---

## 🔌 MCP Server 配置

### 基础 MCP 配置

**文件位置**: `~/.claude/settings.json` 或独立文件 `.mcp.json`

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    },
    "database-tools": {
      "command": "node",
      "args": ["./servers/db-server.js"],
      "env": {
        "DB_HOST": "localhost",
        "DB_USER": "username",
        "DB_PASSWORD": "password"
      }
    }
  }
}
```

> **📎 参考来源**: [[3]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/mcp-integration/references/tool-usage.md) [[4]](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/development-tools/mcp-expert.md)

### 独立 MCP 配置文件

**方式1: 在 settings.json 中引用外部文件**

```json
{
  "mcpServers": "./.mcp.json"
}
```

**方式2: 直接创建 .mcp.json**

```json
{
  "serverType": "stdio",
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
  "env": {
    "API_KEY": "${SECURE_API_KEY}"
  }
}
```

> **📎 参考来源**: [[5]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/references/manifest-reference.md) [[6]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/commands/create-plugin.md)

### 常用 MCP 服务配置模板

```json
{
  "mcpServers": {
    "GitHub Integration MCP": {
      "command": "npx",
      "args": ["-y", "github-mcp@latest"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here",
        "GITHUB_API_URL": "https://api.github.com",
        "RATE_LIMIT_REQUESTS": "5000"
      }
    },
    "AWS Integration MCP": {
      "command": "npx",
      "args": ["-y", "mcp-aws@latest"],
      "env": {
        "AWS_REGION": "us-east-1",
        "AWS_ACCESS_KEY_ID": "your-access-key",
        "AWS_SECRET_ACCESS_KEY": "your-secret-key"
      }
    }
  }
}
```

> **📎 参考来源**: [[7]](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/development-tools/mcp-expert.md)

**环境变量设置**:

```bash
# GitHub integration
export GITHUB_TOKEN="your-github-token"
export GITHUB_REPO="username/repository"

# Database integration
export DB_HOST="localhost"
export DB_USER="username"
export DB_PASSWORD="password"

# AWS integration
export AWS_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
```

> **📎 参考来源**: [[8]](https://github.com/davila7/claude-code-templates/blob/main/docu/docs/components/mcps.md)

---

## 🎣 Hooks 配置

### PreToolUse Hook - 过滤测试输出

**用途**: 在Bash命令执行前预处理输出，减少token消耗

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/filter-test-output.sh"
          }
        ]
      }
    ]
  }
}
```

> **📎 参考来源**: [[9]](https://code.claude.com/docs/en/costs)

### SessionStart Hook - 自动加载环境

**用途**: 会话启动时自动执行环境配置（如激活conda环境）

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

> **📎 参考来源**: [[10]](https://code.claude.com/docs/en/settings)

---

## ⌨️ 键盘快捷键配置

**文件位置**: `~/.claude/keybindings.json`

```json
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

> **📎 参考来源**: [[11]](https://code.claude.com/docs/en/keybindings)

**说明**:
- 修改后自动生效，无需重启
- `null` 值表示禁用该快捷键
- `context` 指定快捷键生效的上下文环境

---

## 📝 自定义 Slash 命令

### 命令文件结构

**文件位置**: `~/.claude/commands/your-command.md`

```markdown
---
description: Deploy application to environment
argument-hint: [app-name] [environment] [version]
allowed-tools: Bash(kubectl:*), Bash(helm:*), Read
model: sonnet
---

Deploy $1 to $2 environment using version $3

Pre-deployment checks:
- Verify $2 configuration
- Check cluster status: !`kubectl cluster-info`
- Validate version $3 exists

Proceed with deployment following deployment runbook.
```

> **📎 参考来源**: [[12]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md) [[13]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/README.md)

### YAML Frontmatter 配置项

| 配置项 | 说明 | 示例 |
|-------|------|------|
| `description` | 命令简短描述（显示在/help中） | `Review code for security issues` |
| `argument-hint` | 参数提示 | `[app-name] [environment]` |
| `allowed-tools` | 允许使用的工具 | `Bash(git:*), Read, Edit` |
| `model` | 指定模型 | `sonnet`, `opus`, `haiku` |
| `disable-model-invocation` | 禁止自动调用（仅手动执行） | `true` / `false` |

> **📎 参考来源**: [[14]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md) [[15]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md)

### 命令内变量和功能

- **参数引用**: `$1`, `$2`, `$ARGUMENTS`（所有参数）
- **文件引用**: `@path/to/file`（读取文件内容）
- **执行命令**: `!`命令内容`` （嵌入bash命令输出）

### 内置帮助子命令模板

```bash
if [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
  echo "Command Help"
  echo ""
  echo "USAGE:"
  echo "  /command [subcommand] [args]"
  echo ""
  echo "SUBCOMMANDS:"
  echo "  init [name]       Initialize new configuration"
  echo "  deploy [env]      Deploy to environment"
  echo "  status            Show current status"
  echo "  rollback          Rollback last deployment"
  echo "  help              Show this help"
  echo ""
  echo "EXAMPLES:"
  echo "  /command init my-project"
  echo "  /command deploy staging"
  echo ""
  echo "For detailed help on a subcommand:"
  echo "  /command [subcommand] --help"
  exit 0
fi
```

> **📎 参考来源**: [[16]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/documentation-patterns.md)

---

## 🛠️ 常用 CLI 命令

### 重置配置和认证

```bash
# 清除认证信息（强制重新登录）
rm -rf ~/.config/claude-code/auth.json
claude

# 重置所有用户设置
rm ~/.claude.json
rm -rf ~/.claude/

# 重置项目特定设置
rm -rf .claude/
rm .mcp.json
```

> **📎 参考来源**: [[17]](https://code.claude.com/docs/en/troubleshooting)

### 内置命令快捷键

| 命令 | 说明 |
|-----|------|
| `/help` | 显示帮助信息和可用命令 |
| `/clear` | 清除当前会话历史 |
| `/commit` | 创建Git提交 |
| `/fast` | 切换快速模式（更快输出） |

---

## 📂 目录结构

```
~/.claude/                      # 用户级配置目录
├── settings.json               # 全局设置
├── keybindings.json            # 键盘快捷键
├── commands/                   # 自定义命令
│   ├── deploy.md
│   └── security-check.md
└── hooks/                      # Hook脚本
    └── filter-test-output.sh

.claude/                        # 项目级配置目录
├── settings.json               # 项目特定设置
└── commands/                   # 项目特定命令
    └── project-specific.md

.mcp.json                       # MCP配置（项目级）
```

---

## 💡 实用技巧

### 1. 分层配置优先级

配置加载顺序（后者覆盖前者）：
1. 全局配置: `~/.claude/settings.json`
2. 项目配置: `./.claude/settings.json`
3. 环境变量: `CLAUDE_*` 前缀的变量

### 2. 权限控制最佳实践

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Read(src/**)",
      "Edit(src/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Read(.env*)",
      "Read(secrets/**)",
      "Edit(package-lock.json)"
    ]
  }
}
```

**原则**:
- 使用白名单限定安全操作
- 黑名单阻止敏感文件访问和危险命令
- 使用通配符简化配置

### 3. 环境变量使用技巧

**在MCP配置中引用项目路径**:

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/server.js",
  "env": {
    "DB_URL": "${DB_URL}",
    "API_KEY": "${SECURE_API_KEY}"
  }
}
```

**预定义变量**:
- `${CLAUDE_PLUGIN_ROOT}`: 插件根目录
- `$CLAUDE_ENV_FILE`: 环境配置文件路径

### 4. Schema 自动补全

在配置文件开头添加 schema 引用，启用编辑器自动补全：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```

---

## 🔗 参考资料汇总

1. [GitHub - anthropics/claude-code](https://github.com/anthropics/claude-code) - Claude Code 官方仓库
2. [Claude Code Docs - Settings](https://code.claude.com/docs/en/settings) - 设置配置文档
3. [MCP Tool Usage Guide](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/mcp-integration/references/tool-usage.md) - MCP工具使用指南
4. [Claude Code Templates - MCP Expert](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/development-tools/mcp-expert.md) - MCP配置模板
5. [Manifest Reference](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/references/manifest-reference.md) - 插件清单参考
6. [Create Plugin Guide](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/commands/create-plugin.md) - 插件创建指南
7. [MCP Integration Templates](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/development-tools/mcp-expert.md) - MCP集成模板
8. [MCP Environment Variables](https://github.com/davila7/claude-code-templates/blob/main/docu/docs/components/mcps.md) - MCP环境变量配置
9. [Claude Code Docs - Costs](https://code.claude.com/docs/en/costs) - 成本优化（Hooks示例）
10. [Settings - SessionStart Hook](https://code.claude.com/docs/en/settings) - 会话启动Hook
11. [Keybindings Documentation](https://code.claude.com/docs/en/keybindings) - 键盘快捷键配置
12. [Frontmatter Reference](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md) - 命令前置配置参考
13. [Command Development README](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/README.md) - 命令开发指南
14. [Command Frontmatter Fields](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md) - 配置项详解
15. [Command Development Skill](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md) - 命令开发技能文档
16. [Documentation Patterns](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/documentation-patterns.md) - 文档化模式
17. [Troubleshooting Guide](https://code.claude.com/docs/en/troubleshooting) - 故障排除指南

---

*📅 整理日期: 2026-02-20*
*📦 数据来源: Context7官方文档 + Anthropic Claude Code仓库*
*🔗 所有引用链接已在正文中标注*
