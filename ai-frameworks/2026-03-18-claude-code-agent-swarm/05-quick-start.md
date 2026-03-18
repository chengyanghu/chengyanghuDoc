# Claude Code 多 Agent 与蜂群模式 - 快速实操指南

> 只讲怎么做，不讲为什么。复制粘贴即可用。

---

## 一、Subagent（零配置，开箱即用）

### 直接在对话中说

```text
use a subagent to search the codebase for all database queries

用 subagent 帮我检查这个项目的安全漏洞
```

Claude 自动派生子代理，完事回报结果，不需要任何配置。

---

## 二、自定义 Subagent

### 第1步：建目录

```bash
# 项目级（当前项目用）
mkdir -p .claude/agents

# 全局（所有项目用）
mkdir -p ~/.claude/agents
```

### 第2步：建文件

创建 `.claude/agents/reviewer.md`：

```markdown
---
name: reviewer
description: Reviews code changes for bugs and security issues
tools: Read, Grep, Glob
model: sonnet
---
You are a code reviewer. Check for bugs, security issues, and bad patterns.
Give specific file:line references.
```

搞定。Claude 检测到相关任务会自动调用。

### 或者用 CLI 一次性定义（不建文件）

```bash
claude --agents '{
  "reviewer": {
    "description": "Reviews code for bugs",
    "prompt": "You are a code reviewer. Find bugs and security issues.",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  }
}'
```

### 或者用交互命令

```text
/agents
```

跟着提示走就行。

---

## 三、蜂群模式（Agent Teams）

### 第1步：激活

**三选一**：

```bash
# 方式A：环境变量（临时）
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

```bash
# 方式B：settings.json（永久）
# macOS: ~/Library/Application Support/Claude Code/settings.json
# Linux: ~/.config/Claude Code/settings.json
# Windows: %APPDATA%/Claude Code/settings.json
```

写入：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

```bash
# 方式C：项目级 .claude/settings.json
```

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 第2步：选显示模式（可选）

```bash
# 默认 auto，不用管
# 想要分屏看所有 agent 同时干活：先装 tmux，在 tmux 里跑 claude
tmux
claude

# 或者强制在一个终端里跑
claude --teammate-mode in-process
```

### 第3步：开干

直接跟 Claude 说想要什么团队：

```text
Create an agent team:
- "backend" handles API implementation
- "frontend" handles React components
- "tester" writes tests

Task: build a user profile page with GET/PUT /api/profile
```

Claude 自动创团队、分任务、建 worktree、开始干活。

### 常用团队操作命令

```text
# 给某个 teammate 发消息
message backend "add input validation to the profile endpoint"

# 广播（慎用，烧钱）
broadcast "switch database from MySQL to PostgreSQL"

# 看任务进度
show task list

# 在 in-process 模式下切换查看不同 teammate
Shift+Down

# 收工
wrap up the team, commit all changes and merge worktrees
```

---

## 四、Agent SDK（代码调用）

### 安装

```bash
pip install claude-agent-sdk          # Python
npm install @anthropic-ai/claude-agent-sdk  # TypeScript
```

### 最简用法

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for msg in query(
        prompt="Fix bugs in src/auth.py",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Bash"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(msg, "result"):
            print(msg.result)

asyncio.run(main())
```

### 并行跑多个 Agent

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def run(name, prompt, tools):
    async for msg in query(
        prompt=prompt,
        options=ClaudeAgentOptions(allowed_tools=tools, permission_mode="acceptEdits"),
    ):
        if hasattr(msg, "result"):
            return f"[{name}] {msg.result}"

async def main():
    results = await asyncio.gather(
        run("审计", "Audit src/ for security issues", ["Read", "Glob", "Grep"]),
        run("测试", "Write tests for src/services/", ["Read", "Write", "Bash"]),
        run("文档", "Generate docs for src/routes/", ["Read", "Write", "Glob"]),
    )
    for r in results:
        print(r)

asyncio.run(main())
```

---

## 五、速查

| 要做什么 | 怎么做 |
|---------|--------|
| 用子代理 | 对话中说 "use a subagent to..." |
| 建自定义子代理 | `.claude/agents/xxx.md` 写 YAML frontmatter |
| 临时子代理 | `claude --agents '{...}'` |
| 激活蜂群 | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
| 分屏看 | `tmux` 里跑 claude |
| 不分屏 | `claude --teammate-mode in-process` |
| 建团队 | "Create an agent team..." |
| 发消息 | "message xxx ..." |
| 广播 | "broadcast ..." |
| 看进度 | "show task list" |
| 解散 | "wrap up the team" |
| SDK 调用 | `pip install claude-agent-sdk` → `query()` |

---

## 参考

- [官方 Agent Teams 文档](https://code.claude.com/docs/en/agent-teams)
- [官方 Sub-agents 文档](https://code.claude.com/docs/en/sub-agents)
- [官方 Agent SDK 文档](https://platform.claude.com/docs/en/agent-sdk/overview)
