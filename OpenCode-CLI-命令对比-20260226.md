# OpenCode vs Claude Code 指令对比速查

## 启动命令

| 功能 | OpenCode | Claude Code |
|------|----------|-------------|
| 启动 TUI | `opencode` | `claude` |
| 继续上次会话 | `opencode --continue` | `claude --resume` |
| 指定目录启动 | `opencode <目录>` | `claude <目录>` |
| 帮助 | `opencode --help` | `claude --help` |

## 交互模式

| 功能 | OpenCode | Claude Code |
|------|----------|-------------|
| 非交互执行 | `opencode run "提示词"` | `claude -p "提示词"` |
| 文件上下文 | `opencode run -f <文件> "提示词"` | `claude <文件>` |
| Web 界面 | `opencode web --port 4096` | ❌ 无官方支持 |

## 会话管理

| 功能 | OpenCode | Claude Code |
|------|----------|-------------|
| 列出会话 | `opencode session list` | 内置 `/sessions` |
| 导出会话 | `opencode export <id>` | `claude export` |
| 查看历史 | `opencode session timeline` | 内置 |

## 服务器模式

| 功能 | OpenCode | Claude Code |
|------|----------|-------------|
| 启动 headless 服务 | `opencode serve --port 4096` | ❌ 不支持 |
| 附加 TUI 到服务 | `opencode attach http://localhost:4096` | ❌ 不支持 |
| 启动 Web 服务 | `opencode web --port 4096` | ❌ 不支持 |

## 模型管理

| 功能 | OpenCode | Claude Code |
|------|----------|-------------|
| 列出可用模型 | `opencode models` | `claude model list` |
| 切换模型 | 内置快捷键 | `/model` |
| 认证管理 | `opencode auth login` | `claude auth` |

## 代理/插件

| 功能 | OpenCode | Claude Code |
|------|----------|-------------|
| 创建代理 | `opencode agent create` | 插件系统 |
| 列出代理 | `opencode agent list` | `/plugin list` |
| 安装插件 | - | `claude /plugin install <name>` |

## 快捷键系统

| 功能 | OpenCode | Claude Code |
|------|----------|-------------|
| 命令面板 | `Ctrl+P` | `/help` |
| 代理切换 | `<leader>a` | 无 |
| 模型切换 | `<leader>m` | `/model` |
| 会话列表 | `<leader>l` | `/sessions` |

## 核心差异总结

1. **架构**：OpenCode 支持客户端/服务器架构，可远程服务；Claude Code 是单一 CLI
2. **可扩展性**：Claude Code 插件系统更成熟；OpenCode 代理系统更轻量
3. **Web 界面**：OpenCode 有官方 Web UI；Claude Code 无
4. **模型**：OpenCode 支持 75+ 提供商；Claude Code 专注 Claude 模型

---

*📅 生成日期: 2026-02-26*
