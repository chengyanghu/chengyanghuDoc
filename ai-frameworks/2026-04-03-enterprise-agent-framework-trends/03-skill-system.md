# Agent Skill 体系架构设计 — 2026

## 1. 什么是 Agent Skill？

**核心区别**：

```
Tool（工具）     = 单一功能函数，如 send_email()
Skill（技能）    = 封装完整领域知识的模块，如"采购审批流程"
Plugin（插件）   = UI/平台扩展，侧重集成
```

**Skill 解决的问题**：通用模型知道"企业通常怎么做"，但不知道"你们公司具体怎么做"。

> 你们的请假审批阈值、GL编码规则、供应商资质要求、升级标准——这些制度知识无法从公开互联网学到。Skill 就是将这些知识可执行化的容器。

[[1]](https://dev.to/sreeni5018/agent-skills-the-missing-layer-that-makes-ai-agents-enterprise-ready-3gc)

---

## 2. Skill 的解剖结构（Anthropic/Vercel 新兴标准）

每个 Skill 是一个自包含的 Markdown 文件，包含：

```markdown
---
name: procurement-approval          # 机器可读标识
description: |                      # 触发条件描述（供Agent做路由决策）
  当需要处理采购申请、供应商审批、
  PO单创建或采购金额授权时使用
trigger: "采购|PO|供应商审批|purchase"
author: procurement-team
version: 1.2.0
tools:                              # 需要的工具声明
  - erp_query
  - approval_workflow
  - email_notify
---

# 采购审批 Skill

## 金额阈值规则
- < ¥5,000：直属主管审批
- ¥5,000 ~ ¥50,000：部门总监 + 财务BP
- > ¥50,000：CFO + 法务

## 供应商资质要求
1. 营业执照有效期 > 6个月
2. 需在系统内完成供应商注册（ERP编号前缀：VD-）
3. 首次合作需提交银行账户核验

## 操作步骤
1. 调用 `erp_query` 验证申请人预算余额
2. 根据金额确定审批链
3. 调用 `approval_workflow` 创建审批单
4. 调用 `email_notify` 通知相关人员
```

**关键设计原则**：Skill 不是在对话开始时全部加载（避免 context 爆炸），而是由 Agent **按需发现并加载**。
[[2]](https://aiquinta.ai/blog/agent-skills-for-enterprise-ai/)

---

## 3. Skill 体系的分层架构

```
┌─────────────────────────────────────────────────────┐
│  业务 Skill 层（企业定制）                           │
│  采购审批 | 报销流程 | 合同审查 | IT服务台 | 招聘    │
├─────────────────────────────────────────────────────┤
│  领域 Skill 层（行业通用）                           │
│  财务分析 | 法律合规 | 安全审计 | 代码审查 | 数据ETL │
├─────────────────────────────────────────────────────┤
│  能力 Skill 层（技术通用）                           │
│  Web搜索 | 文档生成 | 数据可视化 | 代码执行 | 邮件   │
├─────────────────────────────────────────────────────┤
│  基础 Tool 层（原子操作）                            │
│  HTTP请求 | DB查询 | 文件读写 | Shell执行 | API调用  │
└─────────────────────────────────────────────────────┘
```

---

## 4. Skill 路由机制

Agent 如何决定调用哪个 Skill？三种主流方式：

### 方式1：语义向量路由
```python
# 将用户意图 embedding 后，与 Skill 描述做相似度匹配
user_intent_vec = embed(user_query)
best_skill = max(skills, key=lambda s: cosine_sim(user_intent_vec, s.description_vec))
```

### 方式2：LLM 分类路由（更灵活）
```python
# 将所有 Skill 的 name + description 送给 LLM 做路由决策
router_prompt = f"用户请求：{query}\n\n可用Skill：{skill_catalog}\n\n选择最匹配的Skill："
```

### 方式3：关键词触发（最省token）
```yaml
# 在 Skill frontmatter 中声明 trigger 词
trigger: "采购|PO|供应商|purchase|procurement"
```

**Claude Code 的实现**（本工具即采用此模式）：
- `CLAUDE.md` 定义何时触发哪个 skill
- `Skill tool` 按需加载 skill 文件内容注入上下文
- 精确控制 token 用量

---

## 5. 企业 Skill 体系建设路径

```
Phase 1：工具化（Month 1-2）
  识别高频重复操作 → 封装为 Tool → 验证准确性

Phase 2：技能化（Month 3-4）
  将相关 Tool 组合 + 加入业务规则 → 封装为 Skill
  建立 Skill Registry（内部技能市场）

Phase 3：知识化（Month 5-6）
  将隐性制度知识文字化 → 嵌入 Skill
  建立 Skill 版本管理 + A/B测试机制

Phase 4：生态化（Month 7+）
  跨团队 Skill 共享
  Skill 质量评分与反馈循环
  外部 MCP Server 集成
```

---

## 6. Anthropic 写 Tool 的核心原则

来自 Anthropic 工程团队实战总结：

1. **选对粒度**：不要为每个 API endpoint 建一个 tool，按"用户任务"粒度设计
2. **命名空间隔离**：`db_read` / `db_write` 而非都叫 `database`
3. **返回有意义的上下文**：不只返回结果，附加"为什么"和"下一步建议"
4. **优化 token 效率**：大文件返回摘要+offset分页，而非全文
5. **描述即文档**：Tool 描述是 Agent 的"API文档"，写清楚参数含义和使用示例

[[3]](https://www.anthropic.com/engineering/writing-tools-for-agents)
