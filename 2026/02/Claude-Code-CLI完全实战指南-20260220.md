# Claude Code CLI 完全实战指南 - 2026年2月

## 📋 概述

Claude Code 是 Anthropic 官方推出的本地命令行工具，通过自然语言交互实现智能编码辅助。本指南聚焦**本地CLI版本**的核心指令体系、进阶功能（MCP/Skill/Agent）与实战技巧，所有内容配备可直接执行的示例代码。

> **📎 参考来源**: [[1]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/README.md) [[2]](https://code.claude.com/docs/en/features-overview)

---

## ✨ 核心指令体系

### 1. Slash 命令（/前缀）

Slash 命令是 Claude Code 的主要交互方式，用于触发预定义的工作流和功能。

#### 1.1 会话管理类

**`/clear` - 清除上下文**

清空当前会话的所有对话历史，释放上下文窗口。

```bash
# 使用场景：切换项目或任务时
/clear

# 效果：重置对话历史，但保留配置（MCP、Skill等）
```

> **📎 参考来源**: [[3]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md)

**`/help` - 查看可用命令**

```bash
# 查看所有可用的 slash 命令
/help

# 查看特定命令的详细说明
/help plan
```

**其他常用会话命令**：
- `/sessions` - 查看历史会话列表
- `/exit` 或 `/quit` - 退出当前会话

#### 1.2 开发工作流类

**`/plan` - 生成实现计划**

```bash
# 为功能开发生成详细计划
/plan "添加用户认证系统，支持 JWT"

# 输出结构：
# 1. 需求分析
# 2. 技术选型
# 3. 实现步骤
# 4. 测试策略
# 5. 潜在风险
```

> **📎 参考来源**: [[4]](https://github.com/affaan-m/everything-claude-code/blob/main/examples/rust-api-CLAUDE.md)

**`/tdd` - 测试驱动开发**

```bash
# 启动 TDD 工作流（自动识别测试框架）
/tdd

# 流程：
# 1. 编写测试用例
# 2. 运行测试（失败）
# 3. 实现功能代码
# 4. 运行测试（通过）
# 5. 重构优化
```

**`/code-review` - 代码审查**

```bash
# 审查未提交的代码变更
/code-review

# 检查维度：
# - 安全漏洞（SQL注入、XSS、硬编码密钥）
# - 代码质量（命名、复杂度、重复代码）
# - 最佳实践（错误处理、类型安全）
```

> **📎 参考来源**: [[7]](https://context7.com/affaan-m/everything-claude-code/llms.txt)

**`/verify` - 全面验证**

```bash
# 执行构建、测试、安全扫描全流程
/verify

# 等同于执行：
# npm run build && npm test && npm audit
# 或
# cargo build && cargo test && cargo clippy
```

### 2. 感叹号命令（!前缀）

**`!` 后跟反引号 - 嵌入式命令执行**

在 Slash 命令内部动态执行 Bash 命令并插入输出结果。

```bash
# 在自定义命令中使用（.claude/commands/review-changes.md）
---
description: 审查 Git 变更文件
allowed-tools: Bash(git:*), Read
---

当前变更的文件列表：
!`git diff --name-only`

请逐一审查每个文件的：
- 代码质量
- 潜在 Bug
- 安全风险
```

**工作原理**：
1. Claude 执行 `git diff --name-only` 获取文件列表
2. 将输出结果动态插入到命令上下文
3. 基于实际文件列表执行后续操作

> **📎 参考来源**: [[1]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/README.md) [[2]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md)

### 3. @ 符号 - 文件引用

**`@` 后跟文件路径 - 读取文件内容**

```bash
# 在对话中直接引用文件内容
请审查 @src/api/auth.ts 的安全性

# 在自定义命令中使用（.claude/commands/review-file.md）
---
description: 审查指定文件
argument-hint: [file-path]
---

审查文件 @$1 的：
- 代码规范
- 性能优化点
- 潜在问题
```

**动态参数引用**：
- `@$1` - 第一个命令行参数指定的文件
- `@$2` - 第二个参数
- `@$ARGUMENTS` - 所有参数

> **📎 参考来源**: [[3]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md)

### 4. # 符号 - 记忆与持久化（推测功能）

**注意**：`#` 符号的具体功能在官方文档中未明确说明，根据 CLI 工具惯例，可能用于：
- 会话标记（`#tag` 标记重要对话）
- 记忆点设置（保存关键决策）
- 注释（在命令文件中）

**推荐做法**：
```bash
# 在 YAML frontmatter 中作为注释
---
# 这是命令配置
description: 部署应用
---

# 或在对话中尝试
# checkpoint: 完成认证模块开发
```

---

## 💡 进阶功能深度教程

### 1. MCP（Model Context Protocol）集成

#### 1.1 什么是 MCP？

MCP 是 Claude Code 连接外部服务的标准协议，允许 Claude 访问数据库、API、文件系统等外部资源。

#### 1.2 配置 MCP 服务器

**全局配置**（`~/.config/claude-code/settings.json`）：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/projects"]
    },
    "database": {
      "command": "python",
      "args": ["/path/to/db-server.py"],
      "env": {
        "DB_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

> **📎 参考来源**: [[9]](https://code.claude.com/docs/en/plugins-reference) [[10]](https://code.claude.com/docs/en/mcp)

**插件内 MCP 配置**（`.claude/plugin.json`）：

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "API_KEY": "${API_KEY}"
      },
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**关键变量**：
- `${CLAUDE_PLUGIN_ROOT}` - 插件安装目录的绝对路径
- `${VAR}` - 引用环境变量

#### 1.3 MCP 访问控制

**白名单模式**（仅允许特定服务器）：

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "sentry" },
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverUrl": "https://mcp.company.com/*" }
  ]
}
```

**黑名单模式**（阻止危险服务器）：

```json
{
  "deniedMcpServers": [
    { "serverName": "dangerous-server" },
    { "serverCommand": ["npx", "-y", "untrusted-package"] },
    { "serverUrl": "https://*.malicious.com/*" }
  ]
}
```

> **📎 参考来源**: [[10]](https://code.claude.com/docs/en/mcp)

#### 1.4 实战示例：集成 GitHub MCP

```bash
# 1. 安装 GitHub MCP 服务器
npm install -g @modelcontextprotocol/server-github

# 2. 配置环境变量
export GITHUB_TOKEN="ghp_your_token_here"

# 3. 添加到 settings.json（见上方配置）

# 4. 重启 Claude Code 并验证
claude

# 5. 在对话中使用
> 列出我在 GitHub 上的所有仓库
> 查看 repo-name 的最新 PR
> 创建一个 issue："修复登录 bug"
```

### 2. Skills（技能）系统

#### 2.1 Skill 的两种类型

**Knowledge Skill（知识型）**：
- 提供参考文档和指导原则
- 按需加载，不常驻内存
- 文件名：`SKILL.md`

**Task Skill（任务型）**：
- 可直接调用的工作流
- 支持参数传递
- 通过 Slash 命令触发

#### 2.2 创建自定义 Skill

**目录结构**：
```
.claude/
└── skills/
    └── api-guidelines/
        └── SKILL.md
```

**Knowledge Skill 示例**（`.claude/skills/api-guidelines/SKILL.md`）：

```markdown
---
name: api-guidelines
description: 公司 API 设计规范
---

# API 设计规范

## RESTful 原则

1. **资源命名**：使用复数名词
   - ✅ `/api/users`
   - ❌ `/api/user`

2. **HTTP 方法**：
   - GET - 查询
   - POST - 创建
   - PUT - 完整更新
   - PATCH - 部分更新
   - DELETE - 删除

3. **状态码**：
   - 200 - 成功
   - 201 - 创建成功
   - 400 - 请求参数错误
   - 401 - 未认证
   - 403 - 无权限
   - 404 - 资源不存在
   - 500 - 服务器错误

## 响应格式

```json
{
  "success": true,
  "data": { /* 实际数据 */ },
  "error": null,
  "timestamp": "2026-02-20T10:00:00Z"
}
```

## 认证

使用 JWT Bearer Token：
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
```

> **📎 参考来源**: [[12]](https://code.claude.com/docs/en/skills)

**Task Skill 示例**（`.claude/skills/deploy/SKILL.md`）：

```yaml
---
name: deploy
description: 部署应用到生产环境
context: fork
disable-model-invocation: true
---

执行部署流程：

1. **运行测试套件**
   ```bash
   npm test
   ```

2. **构建生产版本**
   ```bash
   npm run build
   ```

3. **推送到部署目标**
   ```bash
   git push production main
   ```

4. **验证部署**
   - 访问 https://app.example.com/health
   - 检查日志：`kubectl logs -f deployment/app`
```

#### 2.3 Skill 与 MCP 组合

MCP 提供数据连接，Skill 提供使用指导：

```markdown
---
name: database-queries
description: 数据库查询模式
---

# 数据库查询最佳实践

## 常用查询模式

### 1. 用户认证
```sql
SELECT id, email, hashed_password
FROM users
WHERE email = $1 AND deleted_at IS NULL;
```

### 2. 分页查询
```sql
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT $1 OFFSET $2;
```

### 3. 关联查询
```sql
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id;
```

## 注意事项
- ✅ 使用参数化查询（$1, $2）防止 SQL 注入
- ✅ 为常查字段添加索引
- ❌ 避免 SELECT *
- ❌ 避免 N+1 查询问题
```

> **📎 参考来源**: [[13]](https://code.claude.com/docs/en/features-overview)

### 3. Agent Teams（多智能体协作）

#### 3.1 Agent 的基本概念

Agent 是独立的 Claude 实例，拥有：
- 独立的上下文和记忆
- 特定的角色和职责
- 可配置的工具访问权限

#### 3.2 创建 Agent

**Agent 配置文件**（`.claude/agents/security-reviewer.md`）：

```markdown
---
agent_name: security-reviewer
task_number: 1
enabled: true
dependencies: []
---

# Security Reviewer Agent

## 职责
审查代码的安全问题，包括：
- 注入攻击风险（SQL/XSS/Command）
- 认证授权缺陷
- 敏感信息泄露
- 加密和哈希使用

## 审查清单

### 1. 输入验证
- [ ] 所有用户输入已验证
- [ ] 使用白名单而非黑名单
- [ ] 文件上传有类型和大小限制

### 2. 认证与授权
- [ ] 密码使用 bcrypt/argon2 哈希
- [ ] JWT 有过期时间和刷新机制
- [ ] API 端点有权限检查

### 3. 数据保护
- [ ] 敏感数据已加密存储
- [ ] HTTPS 强制启用
- [ ] 无硬编码密钥

## 输出格式

```markdown
## 安全审查报告

### 高危问题
1. [文件:行号] 问题描述
   - 风险等级：Critical
   - 修复建议：...

### 中危问题
...

### 建议改进
...
```
```

> **📎 参考来源**: [[15]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/examples/example-settings.md)

#### 3.3 启动 Agent Team

**使用 Task Tool 启动**：

```json
{
  "subagent_type": "general-purpose",
  "description": "安全审查代码变更",
  "prompt": "你是一个安全审查专家。请审查当前的代码变更，重点关注：\n1. SQL注入风险\n2. XSS漏洞\n3. 认证绕过\n4. 敏感信息泄露\n\n对每个问题提供：\n- 文件和行号\n- 风险等级（Critical/High/Medium/Low）\n- 具体修复建议"
}
```

#### 3.4 多 Agent 协作模式

**并行审查模式**：

```bash
# 同时启动多个专业 Agent
/multi-execute

# Agent 1: 安全审查
# Agent 2: 性能分析
# Agent 3: 代码风格检查

# 各自独立工作，最后汇总结果
```

**流水线模式**：

```markdown
---
agent_name: database-implementation
task_number: 4.2
coordinator_session: team-leader
dependencies: ["Task 3.5: API 定义", "Task 4.1: 数据模型设计"]
---

# 数据库实现 Agent

等待依赖任务完成后：
1. 创建数据库迁移文件
2. 添加性能索引
3. 编写约束测试
4. 更新 README 文档

完成后向 coordinator 'team-leader' 报告。
```

> **📎 参考来源**: [[18]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/SKILL.md)

#### 3.5 Agent 状态管理

**Agent 状态文件**（`.claude/multi-agent-swarm.local.md`）：

```yaml
---
agent_name: frontend-developer
task_number: 2
pr_number: 1234
coordinator_session: main-coordinator
enabled: true
dependencies: ["Task 1"]
additional_instructions: "使用 React 18 和 TypeScript"
---

# 前端开发任务

## 当前状态
- 已完成：组件基础结构
- 进行中：状态管理实现
- 待处理：单元测试

## 与其他 Agent 的交互
- 依赖 Backend Agent (Task 1) 提供的 API 规范
- 产出供 Testing Agent (Task 3) 使用的组件
```

---

## 🔧 高阶技巧与避坑指南

### 1. 指令组合联动

#### 1.1 标准开发工作流

```bash
# 步骤 1：规划
/plan "添加订单退款功能，集成 Stripe"

# 步骤 2：TDD 开发
/tdd

# 步骤 3：代码审查
/code-review

# 步骤 4：安全扫描
/security-scan

# 步骤 5：全面验证
/verify
```

> **📎 参考来源**: [[4]](https://github.com/affaan-m/everything-claude-code/blob/main/examples/rust-api-CLAUDE.md) [[5]](https://github.com/affaan-m/everything-claude-code/blob/main/examples/django-api-CLAUDE.md)

#### 1.2 多语言项目适配

```bash
# Python 项目
/python-review  # Python 特定审查
/security-scan  # Django 安全审计

# Rust 项目
/code-review    # Rust 代码审查
/verify         # cargo build + clippy + test

# 自动识别项目类型并调整工作流
```

### 2. 上下文高效管理

#### 2.1 何时使用 `/clear`

**✅ 适合清空的场景**：
- 切换到完全不同的项目
- 完成一个功能模块，开始新模块
- 上下文窗口接近限制（对话过长）

**❌ 不适合清空的场景**：
- 仍在同一功能的不同文件间工作
- 需要引用之前的讨论或决策
- 调试阶段（保留错误追踪历史）

#### 2.2 减少上下文消耗技巧

```bash
# 1. 使用文件引用而非粘贴代码
# ❌ 粘贴整个文件内容
# ✅ 使用 @ 引用
请优化 @src/utils/parser.ts

# 2. 使用 Skill 存储常用知识
# ❌ 每次重复解释项目规范
# ✅ 创建 .claude/skills/project-conventions/SKILL.md

# 3. 使用 Agent 并行处理
# ❌ 在主会话中逐个处理多个文件
# ✅ 启动多个 Agent 并行审查
```

### 3. 常见问题排查

#### 3.1 Slash 命令不生效

**症状**：输入 `/command` 无反应或未出现在 `/help` 中。

**排查步骤**：

```bash
# 1. 检查文件位置和权限
ls -la .claude/commands/my-command.md
chmod 644 .claude/commands/my-command.md

# 2. 检查 YAML frontmatter 语法
head -n 20 .claude/commands/my-command.md

# 3. 重启 Claude Code（带调试模式）
claude --debug

# 4. 查看错误日志
~/.config/claude-code/logs/
```

> **📎 参考来源**: [[17]](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/testing-strategies.md)

#### 3.2 参数替换失败

**症状**：`$1` 或 `$ARGUMENTS` 未被实际值替换。

```bash
# 1. 验证语法
grep '\$1' .claude/commands/my-command.md
grep '\$ARGUMENTS' .claude/commands/my-command.md

# 2. 测试简单示例
cat > .claude/commands/test-args.md <<EOF
---
description: 测试参数
argument-hint: [arg1] [arg2]
---

参数 1: \$1
参数 2: \$2
所有参数: \$ARGUMENTS
EOF

# 3. 调用测试
/test-args foo bar
# 预期输出：
# 参数 1: foo
# 参数 2: bar
# 所有参数: foo bar
```

#### 3.3 Bash 命令执行失败

**症状**：使用 `!`command`` 时命令未执行。

```bash
# 1. 检查 allowed-tools 配置
grep "allowed-tools" .claude/commands/my-command.md

# 必须包含：allowed-tools: Bash(command:*) 或 Bash

# 2. 验证命令语法
grep '!`' .claude/commands/my-command.md

# 正确格式：!`git status`
# 错误格式：!(git status) 或 !git status

# 3. 测试命令是否在系统中可用
which git
git --version
```

#### 3.4 MCP 服务器连接失败

**症状**：Claude 无法访问配置的 MCP 服务器。

```bash
# 1. 检查服务器进程
ps aux | grep mcp-server

# 2. 验证配置文件语法
cat ~/.config/claude-code/settings.json | jq .

# 3. 检查环境变量
echo $GITHUB_TOKEN
echo $API_KEY

# 4. 手动启动服务器测试
npx -y @modelcontextprotocol/server-github

# 5. 查看 Claude Code 日志
tail -f ~/.config/claude-code/logs/mcp-*.log
```

### 4. 隐藏提效技巧

#### 4.1 使用 Hooks 自动化

**Post-Edit Hook**（代码修改后自动检查）：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "eslint --fix $FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

#### 4.2 CLAUDE.md 设置项目规则

在项目根目录创建 `CLAUDE.md`：

```markdown
# 项目约定

## 代码风格
- 使用 TypeScript strict 模式
- 函数命名：驼峰式（camelCase）
- 类命名：帕斯卡式（PascalCase）
- 缩进：2 空格

## 禁止操作
- ❌ 不要使用 `any` 类型
- ❌ 不要在生产代码中使用 `console.log`
- ❌ 不要提交包含 `TODO` 的代码

## 提交规范
格式：`<type>(<scope>): <subject>`
类型：feat/fix/docs/style/refactor/test/chore
```

> **📎 参考来源**: [[13]](https://code.claude.com/docs/en/features-overview)

#### 4.3 Python 最佳实践集成

```python
# 在 .claude/skills/python-patterns/SKILL.md 中定义

# ✅ 使用 None 和创建新列表
def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# ✅ 使用 isinstance
if isinstance(obj, list):
    process(obj)

# ✅ 使用 is 比较 None
if value is None:
    process()

# ✅ 显式导入
from os.path import join, exists

# ✅ 具体异常处理
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
```

> **📎 参考来源**: [[6]](https://github.com/affaan-m/everything-claude-code/blob/main/skills/python-patterns/SKILL.md)

---

## 🚀 端到端实战案例

### 场景：为 Web 应用添加用户认证系统

#### 前置准备

```bash
# 1. 确保项目初始化
cd my-web-app
git init

# 2. 配置 GitHub MCP（用于 issue 管理）
# 编辑 ~/.config/claude-code/settings.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "ghp_xxx" }
    }
  }
}

# 3. 创建 API 规范 Skill
mkdir -p .claude/skills/api-conventions
# 编辑 .claude/skills/api-conventions/SKILL.md（参考前文示例）

# 4. 启动 Claude Code
claude
```

#### 步骤 1：需求规划

```bash
用户> /plan "添加用户认证系统，支持邮箱登录、JWT token、密码重置功能"

Claude> 📋 实现计划：用户认证系统

## 技术选型
- 后端：Express.js + TypeScript
- 数据库：PostgreSQL + Prisma ORM
- 认证：JWT（access token 15分钟，refresh token 7天）
- 密码：bcrypt 哈希（salt rounds: 12）
- 邮件：Nodemailer + SendGrid

## 实现步骤

### 阶段 1：数据模型（2-3h）
1.1 创建 User 表结构
1.2 创建 RefreshToken 表
1.3 创建 PasswordReset 表
1.4 编写 Prisma migrations

### 阶段 2：核心认证逻辑（3-4h）
2.1 用户注册接口
2.2 用户登录接口
2.3 Token 刷新接口
2.4 登出接口
2.5 认证中间件

### 阶段 3：密码管理（2-3h）
3.1 忘记密码接口
3.2 重置密码接口
3.3 修改密码接口

### 阶段 4：测试与安全（2-3h）
4.1 单元测试（Jest）
4.2 集成测试
4.3 安全审计
4.4 性能测试

## 潜在风险
- 时区处理（Token 过期时间）
- 邮件发送失败重试机制
- 并发 Token 刷新竞态条件
```

#### 步骤 2：启动 Agent Team

```bash
用户> 使用多个 Agent 并行实现不同模块

Claude> 正在启动 Agent Team...

# Agent 1: Database Schema Designer
任务：设计并实现数据库模型

# Agent 2: API Developer
任务：实现 RESTful API 端点

# Agent 3: Security Reviewer
任务：审查安全问题

# Agent 4: Test Engineer
任务：编写测试用例

所有 Agent 已启动，开始并行工作...
```

#### 步骤 3：TDD 开发（以注册接口为例）

```bash
用户> /tdd

Claude> 🧪 启动 TDD 工作流

# 步骤 1：编写测试用例
# 文件：tests/auth/register.test.ts

import request from 'supertest';
import app from '../../src/app';

describe('POST /api/auth/register', () => {
  it('应成功注册新用户', async () => {
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'SecurePass123!',
        name: 'Test User'
      });

    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.user).toHaveProperty('id');
    expect(response.body.data.user.email).toBe('test@example.com');
    expect(response.body.data).toHaveProperty('accessToken');
  });

  it('应拒绝重复邮箱', async () => {
    // 第一次注册
    await request(app).post('/api/auth/register').send({
      email: 'duplicate@example.com',
      password: 'SecurePass123!',
      name: 'User 1'
    });

    // 第二次注册相同邮箱
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'duplicate@example.com',
        password: 'AnotherPass456!',
        name: 'User 2'
      });

    expect(response.status).toBe(400);
    expect(response.body.success).toBe(false);
    expect(response.body.error.code).toBe('EMAIL_ALREADY_EXISTS');
  });

  it('应验证密码强度', async () => {
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'weak@example.com',
        password: '123',  // 弱密码
        name: 'Weak User'
      });

    expect(response.status).toBe(400);
    expect(response.body.error.code).toBe('WEAK_PASSWORD');
  });
});

# 步骤 2：运行测试（预期失败）
npm test -- register.test.ts

✗ 应成功注册新用户 (未实现)
✗ 应拒绝重复邮箱 (未实现)
✗ 应验证密码强度 (未实现)

# 步骤 3：实现功能代码
# 文件：src/controllers/auth.controller.ts

import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { prisma } from '../db';
import { validatePassword } from '../utils/validators';

export async function register(req, res) {
  try {
    const { email, password, name } = req.body;

    // 验证密码强度
    if (!validatePassword(password)) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'WEAK_PASSWORD',
          message: '密码必须至少8位，包含大小写字母和数字'
        }
      });
    }

    // 检查邮箱是否已存在
    const existingUser = await prisma.user.findUnique({
      where: { email }
    });

    if (existingUser) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'EMAIL_ALREADY_EXISTS',
          message: '该邮箱已被注册'
        }
      });
    }

    // 哈希密码
    const hashedPassword = await bcrypt.hash(password, 12);

    // 创建用户
    const user = await prisma.user.create({
      data: {
        email,
        hashedPassword,
        name
      }
    });

    // 生成 JWT
    const accessToken = jwt.sign(
      { userId: user.id },
      process.env.JWT_SECRET!,
      { expiresIn: '15m' }
    );

    const refreshToken = jwt.sign(
      { userId: user.id },
      process.env.JWT_REFRESH_SECRET!,
      { expiresIn: '7d' }
    );

    // 保存 refresh token
    await prisma.refreshToken.create({
      data: {
        userId: user.id,
        token: refreshToken,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    });

    res.status(201).json({
      success: true,
      data: {
        user: {
          id: user.id,
          email: user.email,
          name: user.name
        },
        accessToken,
        refreshToken
      }
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({
      success: false,
      error: {
        code: 'INTERNAL_ERROR',
        message: '服务器错误'
      }
    });
  }
}

# 步骤 4：再次运行测试
npm test -- register.test.ts

✓ 应成功注册新用户
✓ 应拒绝重复邮箱
✓ 应验证密码强度

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total

# 步骤 5：重构优化（按需）
```

#### 步骤 4：安全审查

```bash
用户> /security-scan

Claude> 🔒 执行安全扫描...

## 安全审查报告

### ✅ 通过项
- [√] 密码使用 bcrypt 哈希（salt rounds: 12）
- [√] JWT 有过期时间
- [√] 环境变量管理敏感信息
- [√] SQL 查询使用参数化（Prisma ORM）

### ⚠️ 警告项
1. **缺少速率限制**
   - 文件：src/routes/auth.routes.ts
   - 风险：暴力破解攻击
   - 建议：添加 express-rate-limit
   ```typescript
   import rateLimit from 'express-rate-limit';
   
   const authLimiter = rateLimit({
     windowMs: 15 * 60 * 1000, // 15分钟
     max: 5, // 限制5次请求
     message: '请求过于频繁，请稍后再试'
   });
   
   router.post('/register', authLimiter, register);
   router.post('/login', authLimiter, login);
   ```

2. **JWT Secret 强度未验证**
   - 文件：.env
   - 建议：使用至少32字节的随机密钥
   ```bash
   # 生成安全密钥
   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
   ```

### 📋 建议改进
1. 添加 HTTPS 强制重定向
2. 实现 CSRF 保护（如使用 cookie 存储 token）
3. 添加登录审计日志
4. 实现账户锁定机制（多次失败登录后）
```

#### 步骤 5：代码审查与提交

```bash
用户> /code-review

Claude> 📝 代码审查中...

## 审查结果

### 优点
- 代码结构清晰，职责分离合理
- 错误处理完善
- 测试覆盖率高（87%）

### 需要改进
1. **auth.controller.ts:45** - 错误日志包含敏感信息
   ```typescript
   // ❌ 不要记录完整的错误对象（可能包含密码）
   console.error('Registration error:', error);
   
   // ✅ 只记录安全信息
   console.error('Registration error:', error.message);
   ```

2. **validators.ts:12** - 密码规则应该可配置
   ```typescript
   // ✅ 从配置读取
   const PASSWORD_MIN_LENGTH = process.env.PASSWORD_MIN_LENGTH || 8;
   ```

所有问题已修复，准备提交。

用户> 创建 Git 提交

Claude> 
git add src/ tests/
git commit -m "feat(auth): 实现用户注册和登录功能

- 添加用户注册接口（邮箱验证、密码哈希）
- 添加用户登录接口（JWT 生成）
- 实现 Token 刷新机制
- 添加单元测试和集成测试
- 通过安全审查

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"

✓ 提交成功
```

#### 步骤 6：验证与部署

```bash
用户> /verify

Claude> ✅ 执行全面验证...

1. 构建检查
   npm run build
   ✓ TypeScript 编译成功

2. 代码质量
   npm run lint
   ✓ ESLint 检查通过

3. 测试套件
   npm test
   ✓ 15/15 测试通过

4. 安全审计
   npm audit
   ✓ 0 个漏洞

5. 性能测试
   npm run test:performance
   ✓ 注册接口响应时间: 245ms (目标 <500ms)
   ✓ 登录接口响应时间: 189ms (目标 <500ms)

✅ 所有验证通过，可以部署！
```

---

## 🔗 参考资料汇总

1. [Claude Code - Command Development](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/README.md) - Slash 命令开发指南
2. [Claude Code - Frontmatter Reference](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md) - YAML 配置参考
3. [Claude Code - Skill Development](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md) - Skill 开发文档
4. [Everything Claude Code - Rust API Example](https://github.com/affaan-m/everything-claude-code/blob/main/examples/rust-api-CLAUDE.md) - Rust 项目工作流
5. [Everything Claude Code - Django API Example](https://github.com/affaan-m/everything-claude-code/blob/main/examples/django-api-CLAUDE.md) - Python/Django 工作流
6. [Everything Claude Code - Python Patterns](https://github.com/affaan-m/everything-claude-code/blob/main/skills/python-patterns/SKILL.md) - Python 最佳实践
7. [Everything Claude Code - LLMs.txt](https://context7.com/affaan-m/everything-claude-code/llms.txt) - 代码审查工具
8. [Everything Claude Code - README](https://github.com/affaan-m/everything-claude-code/blob/main/README.md) - 完整命令列表
9. [Claude Code - Plugins Reference](https://code.claude.com/docs/en/plugins-reference) - 插件开发参考
10. [Claude Code - MCP Documentation](https://code.claude.com/docs/en/mcp) - MCP 集成指南
11. [Claude Code - Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) - 插件市场配置
12. [Claude Code - Skills Documentation](https://code.claude.com/docs/en/skills) - Skills 系统文档
13. [Claude Code - Features Overview](https://code.claude.com/docs/en/features-overview) - 功能组合模式
14. [Claude Code - Hookify Command](https://github.com/anthropics/claude-code/blob/main/plugins/hookify/commands/hookify.md) - Agent 启动示例
15. [Claude Code - Agent Settings Example](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/examples/example-settings.md) - Agent 配置示例
16. [Claude Code - Conversation Analyzer](https://github.com/anthropics/claude-code/blob/main/plugins/hookify/agents/conversation-analyzer.md) - 分析输出格式
17. [Claude Code - Testing Strategies](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/references/testing-strategies.md) - 调试技巧
18. [Claude Code - Plugin Settings](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/SKILL.md) - Agent 状态管理

---

*📅 整理日期: 2026-02-20*  
*📦 数据来源: Context7 官方文档 + Everything Claude Code 社区*  
*🔗 所有引用链接已在正文中标注*