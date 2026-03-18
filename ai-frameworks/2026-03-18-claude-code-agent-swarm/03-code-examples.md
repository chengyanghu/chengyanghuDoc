# 代码示例

## 1. Agent SDK 基础：自动修复 Bug

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def main():
    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")


asyncio.run(main())
```

**说明**: 使用 `query()` 流式 API，配置 Read/Edit/Glob 工具，自动审批文件编辑。 [[1]](https://platform.claude.com/docs/en/agent-sdk/quickstart)

---

## 2. Agent SDK：只读代码审查

```python
async for message in query(
    prompt="Review this code for best practices",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep"],  # 只读工具
    ),
):
    if hasattr(message, "result"):
        print(message.result)
```

**关键点**: 只给 Read/Glob/Grep 工具，Agent 无法修改任何文件。 [[2]](https://platform.claude.com/docs/en/agent-sdk/overview)

---

## 3. Agent SDK：动态权限切换

```python
async def main():
    q = query(
        prompt="Help me refactor this code",
        options=ClaudeAgentOptions(permission_mode="default"),
    )

    # 分析阶段完成后，放开编辑权限
    await q.set_permission_mode("acceptEdits")

    async for message in q:
        if hasattr(message, "result"):
            print(message.result)
```

**说明**: 先以受限模式分析，确认安全后切换到 acceptEdits 模式。 [[3]](https://platform.claude.com/docs/en/agent-sdk/permissions)

---

## 4. Agent SDK：Hook 安全审计

```python
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            # 拦截文件修改操作
            HookMatcher(matcher="Write|Edit|Delete", hooks=[file_security_hook]),
            # 审计所有 MCP 工具调用
            HookMatcher(matcher="^mcp__", hooks=[mcp_audit_hook]),
            # 全局日志
            HookMatcher(hooks=[global_logger]),
        ]
    }
)
```

**关键点**: 使用正则匹配不同工具类别，分别应用安全策略。 [[4]](https://platform.claude.com/docs/en/agent-sdk/hooks)

---

## 5. 自定义 Subagent：安全审查员

创建文件 `.claude/agents/security-reviewer.md`：

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
- Insecure data handling

Provide specific line references and suggested fixes.
```

**使用方式**: Claude 会在检测到代码安全审查需求时自动调用此 Subagent。 [[5]](https://code.claude.com/docs/en/best-practices)

---

## 6. CLI 动态定义多 Subagent

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

**说明**: 通过 `--agents` JSON 参数一次性定义多个专用 Subagent。 [[6]](https://code.claude.com/docs/en/sub-agents)

---

## 7. 启用蜂群模式并创建团队

**步骤 1：启用**

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**步骤 2：自然语言创建团队**

```text
Create an agent team to refactor the payment module. Spawn three teammates:
one for the API layer, one for the database migrations, one for test coverage.
Have them coordinate through the shared task list.
```

**说明**: Leader 自动创建三个 Teammate，每个在独立 Worktree 中工作，通过共享 Task List 协调。 [[7]](https://code.claude.com/docs/en/agent-teams)

---

## 8. 多 Agent 协作：Box 文档处理（Agent SDK）

```typescript
// src/config/agents.ts
function readSkill(skillDir: string): string {
  const skillPath = join(PROJECT_ROOT, ".claude", "skills", skillDir, "SKILL.md");
  return readFileSync(skillPath, "utf-8");
}

const agents = {
  explorer: {
    description: "Explores Box folder structure",
    prompt: readSkill("explorer"),
    tools: ["Read", "Bash"],
  },
  extractor: {
    description: "Extracts structured data from documents",
    prompt: readSkill("extractor"),
    tools: ["Read", "Bash", "Write"],
  },
  assembler: {
    description: "Creates summary spreadsheet",
    prompt: readSkill("xlsx"),
    tools: ["Read", "Write", "Bash"],
  },
};
```

**说明**: 真实生产案例——多个专用 Agent 协作处理 Box 云存储中的文档。 [[8]](https://blog.box.com/building-multi-agent-system-claude-agent-sdk-and-box)

---

## 常见问题代码

### 问题：蜂群模式下 Broadcast 滥用

❌ 错误写法：
```text
broadcast "I've finished my task" to all teammates
```

✅ 正确写法：
```text
message team-lead "API refactor complete, all tests passing. Ready for review."
```

**原因**: Broadcast 会让每个 Teammate 都消耗 Token 处理消息，点对点 DM 更高效。 [[7]](https://code.claude.com/docs/en/agent-teams)
