# CLI 封装供 Agent 高效使用 — 2026

## 1. 为什么 CLI 有时优于 MCP？

这是 2026 年出现的重要反直觉洞见：

**实践发现**（来自 Eugene Petrenko，AI工具工程师）：
> "我没有为 Agent 构建任何自定义集成，也没有先写 MCP Server。我只是安装了一个设计良好的 CLI，带有 `--help`、良好的错误信息和可预测的行为。Agent 自己就开始用了。"

[[1]](https://jonnyzzz.com/blog/2026/02/20/cli-tools-for-ai-agents/)

**CLI vs MCP 的权衡**：

| 维度 | MCP | CLI |
|------|-----|-----|
| **Token 成本** | 高（工具定义持续占用system prompt）| 低（仅在调用时产生stdout）|
| **开发成本** | 需要专门服务器 | 直接复用已有CLI |
| **调试体验** | 抽象层多，难调 | bash历史可回溯 |
| **组合能力** | 有限 | Unix管道天然支持 |
| **适用条件** | Agent无shell访问 | Agent有shell访问 |
| **生态集成** | 标准化，跨平台 | 环境依赖 |

**结论**：两者不是替代关系，而是互补——MCP 适合跨平台标准集成，CLI 适合有 shell 访问权限的 Agent 本地高效操作。

---

## 2. 哪些企业系统最适合封装成 CLI 供 Agent 使用

### 一类：已有成熟 CLI，Agent 可直接使用

| 系统 | CLI工具 | Agent可做的事 |
|------|---------|-------------|
| **Git/GitHub** | `gh`, `git` | PR管理、Issue追踪、代码审查 |
| **Kubernetes** | `kubectl`, `helm` | Pod管理、部署、扩缩容 |
| **云平台** | `aws`, `gcloud`, `az` | 资源创建、监控、费用分析 |
| **数据库** | `psql`, `mysql`, `redis-cli` | 查询、备份、性能分析 |
| **CI/CD** | `gh run`, `argocd` | 触发部署、查看日志 |
| **监控** | `promtool`, `logcli` | 指标查询、日志检索 |
| **基础设施即代码** | `terraform`, `pulumi` | Plan/Apply/State管理 |

### 二类：需要自己封装成 CLI 的系统

| 系统类型 | 封装价值 | 示例 |
|----------|----------|------|
| **ERP系统** | SAP/Oracle API太复杂，CLI简化接口 | `erp query --type po --status pending` |
| **内部审批系统** | OA系统API不友好 | `oa approve --id REQ-001 --comment "已审核"` |
| **数据平台** | 复杂查询接口 | `dataplatform run --query "日活用户" --date yesterday` |
| **安全合规** | 合规检查脚本化 | `compliance check --scope finance --standard SOX` |

---

## 3. 为 Agent 设计 CLI 的 8 条黄金法则

来自 ["Writing CLI Tools That AI Agents Actually Want to Use"](https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no)：

### 法则1：输出必须机器可读
```bash
# ❌ 人类友好但Agent难解析
echo "✅ 部署成功！应用已在 3 个节点上运行"

# ✅ 结构化输出
echo '{"status": "success", "replicas": 3, "endpoint": "https://app.example.com"}'
# 或加 --json flag 切换格式
```

### 法则2：退出码语义化
```bash
# 0 = 成功，1 = 业务错误，2 = 参数错误，3 = 网络错误
# Agent 可以根据退出码决定重试策略
```

### 法则3：幂等性设计
```bash
# Agent 可能因失败重试，操作必须安全重复
deploy --app myapp --image v1.2.3  # 重复执行结果相同
```

### 法则4：dry-run 模式
```bash
# 让 Agent 先"演习"，再实际执行
deploy --dry-run   # 显示会做什么，但不实际执行
```

### 法则5：详细的帮助文档
```bash
# --help 输出是 Agent 的"API文档"
erp --help
# Usage: erp <command> [options]
# Commands:
#   query    查询ERP数据
#   create   创建记录（需审批权限）
# Examples:
#   erp query --type invoice --status pending --limit 10
```

### 法则6：错误信息可操作化
```bash
# ❌ 模糊错误
Error: Permission denied

# ✅ 可操作的错误
Error: 缺少 ERP 只读权限 (ERP_READONLY_ROLE)
建议操作: 联系 IT 申请权限，工单模板: https://it.company.com/erp-access
```

### 法则7：支持 stdin/stdout 管道
```bash
# Agent 喜欢管道组合
erp query --type po | jq '.[] | select(.amount > 10000)' | approval submit
```

### 法则8：添加 AGENTS.md 说明文件
```markdown
# AGENTS.md（放在工具根目录）
## erp CLI - Agent 使用指南

### 认证
运行前设置：export ERP_API_KEY=xxx

### 常用工作流
1. 查询待审批PO：erp query --type po --status pending
2. 批量审批：erp approve --ids $(erp query --type po --status pending --format ids)

### 注意事项
- create/delete 操作会写入生产数据库，请先 --dry-run
- 大量查询请加 --limit，默认100条
```

---

## 4. 值得关注的 Agent CLI 框架

### Axe（Go实现，Unix哲学）
- 用 TOML 定义单一目标 Agent，像 Unix 程序一样可组合
- 触发方式：管道、git hooks、cron、终端
- 哲学：**每个Agent做一件事，做好**
[[2]](https://github.com/jrswab/axe)

```toml
# agent.toml
[agent]
name = "code-reviewer"
model = "claude-opus-4-6"
skill = "skills/code-review.md"
max_tokens = 4096

[input]
from = "stdin"  # git hook 传入 diff

[output]
format = "json"
```

### Goose（Block出品，开源）
- 本地优先的 AI Agent，CLI + 桌面双模式
- 通过 MCP Extensions 扩展能力
- 支持 Recipes（可复用任务模板）
- 多 LLM 提供商支持

---

## 5. 实战：将内部系统封装成 Agent 友好的 CLI

```python
#!/usr/bin/env python3
# erp-cli.py — ERP系统Agent友好封装示例

import click
import json
import sys

@click.group()
def cli():
    """ERP系统CLI - 为AI Agent优化的接口"""
    pass

@cli.command()
@click.option('--type', 'doc_type', required=True, help='文档类型: po/invoice/expense')
@click.option('--status', default='pending', help='状态过滤')
@click.option('--limit', default=20, help='返回数量上限')
@click.option('--format', 'fmt', default='json', type=click.Choice(['json', 'ids', 'table']))
@click.option('--dry-run', is_flag=True, help='仅显示查询计划，不执行')
def query(doc_type, status, limit, fmt, dry_run):
    """查询ERP记录"""
    if dry_run:
        click.echo(json.dumps({"dry_run": True, "query": {"type": doc_type, "status": status, "limit": limit}}))
        sys.exit(0)

    try:
        results = erp_client.query(doc_type, status, limit)
        if fmt == 'json':
            click.echo(json.dumps(results))
        elif fmt == 'ids':
            click.echo('\n'.join(r['id'] for r in results))
        sys.exit(0)
    except PermissionError as e:
        click.echo(json.dumps({
            "error": str(e),
            "code": "PERMISSION_DENIED",
            "action": "申请权限: https://it.company.com/erp-access"
        }), err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
```
