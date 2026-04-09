# Copilot Cowork 能力深度解析 — 2026-04-09

> **用途**：培训素材补充——深入理解 Cowork 的具体能力、技能体系、操作边界和实战技巧
> **配合**：[培训聚焦文档](https://github.com/chengyanghu/chengyanghuDoc/blob/main/ai-frameworks/2026-04-09-copilot-cowork-training-focus.md) | [深度研究报告](https://github.com/chengyanghu/chengyanghuDoc/blob/main/ai-frameworks/2026-04-09-copilot-cowork.md)

---

## 一、13 个内置技能（官方完整列表）

Cowork 有 **13 个明确的内置技能**，按需自动调用：

| # | 技能名称 | 涉及应用 | 能做什么 |
|---|---------|----------|----------|
| 1 | **Word** | Word | 创建、编辑 Word 文档 |
| 2 | **Excel** | Excel | 创建电子表格、处理数据、生成报告、自动化计算 |
| 3 | **PowerPoint** | PowerPoint | 创建演示文稿，保持原有模板格式 |
| 4 | **PDF** | — | 生成 PDF 文件 |
| 5 | **Email** | Outlook | 起草、回复、转发邮件（含附件） |
| 6 | **Scheduling** | Outlook | 安排会议、发送会议邀请 |
| 7 | **Calendar Management** | Outlook | 管理日历事件、优化日程安排 |
| 8 | **Meetings** | Teams/Outlook | 会议准备、会议记录处理 |
| 9 | **Daily Briefing** | 跨应用 | 生成每日简报（邮件、会议、待办摘要） |
| 10 | **Enterprise Search** | M365 全域 | 跨组织搜索文件、人员、信息 |
| 11 | **Communications** | 跨应用 | 起草利益相关方沟通文件 |
| 12 | **Deep Research** | 跨应用+网络 | 跨多源深度研究并编译综合分析 |
| 13 | **Adaptive Cards** | Teams/Copilot | 生成结构化布局的卡片式响应 |

---

## 二、每个技能的详细能力

### 邮件技能（Email）

**能做**：起草/回复/转发邮件（含附件）、批量起草、嵌入工作流
**审批**：发送前必须用户审批，可直接编辑后发送

```
❌ "帮我写封邮件给张经理"
✅ "帮我写封邮件给张经理，汇报Q1销售数据，附上上周的Excel报表，语气正式"
```

### 日历与排程（Scheduling + Calendar Management）

**能做**：创建事件、分析日程冲突、预留专注时间、建议改期、发送邀请
**审批**：创建/修改/发送邀请前需确认

```
❌ "整理我的日程"
✅ "分析我下周的日程，找出可以取消或改期的会议，周二和周四上午各预留2小时专注时间"
```

### 文档创建（Word / Excel / PowerPoint / PDF）

**能做**：从零创建、基于模板创建（保持格式）、跨文档操作（Excel→PPT）、数据处理和图表
**存储**：文档创建后保存在 OneDrive

```
❌ "做个PPT"
✅ "基于上周的销售Excel，创建季度汇报PPT：1)趋势图 2)区域对比 3)下季度预测，使用公司标准模板"
```

### Teams 沟通

**能做**：在指定频道/聊天发消息、嵌入工作流通知

### 企业搜索（Enterprise Search）

**能做**：跨 M365 全域搜索文件/人员/邮件/Teams消息/SharePoint
**限制**：只搜索你有权限的内容

### 深度研究（Deep Research）

**能做**：跨多源收集信息、编译综合分析、公司研究（财报/监管/市场）

### 每日简报（Daily Briefing）

**能做**：汇总今日邮件/会议/待办、会议智能摘要、**支持定时自动运行**

### 自适应卡片（Adaptive Cards）

**能做**：结构化卡片响应、数据展示（表格/列表/按钮）、交互式布局

---

## 三、高级能力

### 定时任务（Scheduled Prompts）

支持自动运行：每日简报、每周报告、定期数据更新。

### 自定义技能（Custom Skills）

最多 **20 个**自定义技能：
1. OneDrive 中创建 `/Documents/Cowork/Skills/{技能名}/SKILL.md`
2. 用 Markdown 描述指令和规则
3. Cowork 自动识别并调用

### 上下文附件

可主动附加邮件、文件、日历事件作为 Cowork 的工作上下文。

### 模型选择

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **Auto Mode**（默认） | 系统自动选择 | 推荐大多数情况 |
| **Claude 4.6** | Sonnet | 快速响应、日常任务 |
| **Opus 4.6** | Opus | 复杂推理、深度分析 |

### 中途干预

- 执行中追加新要求 → 不暂停现有任务，融入计划
- 随时修改方向或取消
- 可同时 **10+ 任务并行运行**

---

## 四、明确的能力边界

### 生态边界

| 不能做 | 说明 |
|--------|------|
| 访问本地电脑 | 不能操作本地文件和应用 |
| 第三方系统 | 不能连接 Salesforce、SAP、Slack 等 |
| 网页浏览 | 不能自由访问任意网站 |
| 安装软件 | 不能在设备上安装程序 |

### 操作边界

| 不能做 | 说明 |
|--------|------|
| 删除邮件/文件 | 破坏性操作受限 |
| 代理他人 | 只能以你的身份操作 |
| 绕过权限 | 只访问你有权限的内容 |
| 修改系统设置 | 不能更改 M365 管理设置 |

### 认知边界

| 不能做 | 说明 |
|--------|------|
| 理解公司政治 | 不知道哪个会议不能取消 |
| 判断优先级含义 | 不知道"紧急"在你公司意味着什么 |
| 理解隐性知识 | 不知道客户特殊偏好 |

### 技术边界

| 限制 | 详情 |
|------|------|
| 输入长度 | 单条最多 **16,000 字符** |
| 语言 | 英文为主，中文有限 |
| 准确性 | 可能不准确，需人工审核 |
| 上下文 | 跨会话可能丢失 |

---

## 五、Copilot Cowork vs Claude Cowork 对比

| 维度 | Copilot Cowork (Microsoft) | Claude Cowork (Anthropic) |
|------|---------------------------|--------------------------|
| 运行位置 | 云端（M365 租户） | 本地（桌面沙箱） |
| 访问范围 | M365 生态 | 本地文件 + 38+ 连接器 |
| 数据保护 | 企业 M365 合规 | 本地沙箱隔离 |
| 目标用户 | 企业团队 | 个人/开发者 |
| 第三方集成 | 仅 M365 | MCP 连接器广泛集成 |

**一句话**：同一个"大脑"（Claude），不同的"身体"——一个在公司云端，一个在个人电脑。

---

## 六、Prompt 实战指南

### 核心原则

> 你不是在"提问"，而是在"写工单"。

1. **描述结果，不描述步骤**
2. **给约束，不给长文** — `"正式语气、200字以内、必须包含交付日期"`
3. **要求迭代** — `"先给初步发现，确认后再深入"`
4. **给检查点** — `"每步完成后暂停让我确认"`

### 7 个预置模板

| 模板 | 功能 | 适合谁 |
|------|------|--------|
| Catch me up | 追赶进度 | 休假回来/早晨开工 |
| Organize my inbox | 整理收件箱 | 邮件多的人 |
| Organize my week | 优化日程 | 会议多的人 |
| Prep for a meeting | 会议准备 | 所有人 |
| Plan an event | 规划活动 | 行政/项目管理 |
| Prepare for my 1:1 | 一对一准备 | 管理者 |
| Research a company | 公司研究 | 市场/销售/BD |

### 按岗位 Prompt 库

**行政/助理**
```
"Organize my week: 取消无议程会议，高优会议预留准备时间，周五下午不排会"
"每天8:30自动生成日报：今日会议、待回复邮件、昨日未完成事项"
```

**市场/销售**
```
"Research [竞品]: 近6个月产品发布、定价变化、媒体报道，整理成Excel"
"Prep for meeting with [客户]: 整理往来邮件和提案，生成简报和PPT"
```

**项目管理**
```
"收集[项目]的Teams消息和邮件，生成本周进展周报"
"Prepare for my 1:1 with [下属]: 整理TA最近的邮件、会议、交付物"
```

---

## 七、能力成熟度模型

| 阶段 | 时间 | 目标 | 活动 |
|------|------|------|------|
| Level 1 观察者 | 1-2周 | 了解概念 | 只用 Catch me up、Research |
| Level 2 尝试者 | 3-4周 | 单技能使用 | 创建文档、用预置模板 |
| Level 3 实践者 | 2-3月 | 多技能组合 | 自写 Prompt、设置定时任务 |
| Level 4 专家 | 3月+ | 标准化推广 | 创建自定义技能、指导同事 |

---

## 八、已知问题

| 问题 | 应对 |
|------|------|
| 跨会话丢失上下文 | 新会话附加必要文件 |
| PPT 模板不完美 | 生成后在 PPT 中微调 |
| 最新数据未索引 | 重要数据手动附加 |
| 中文效果有限 | Prompt 用英文，产出指定中文 |
| 复杂 Excel 公式 | 简单处理为主，复杂手动 |
| 批准后不可撤回 | 审批前逐字检查 |

---

## 九、培训视频

| 视频 | 时长 | 适合 |
|------|------|------|
| [Meet Copilot Cowork](https://www.youtube.com/watch?v=j8rHJsM3fxQ) (微软官方) | 1'49" | 培训开场 |
| [Here's What It Can Actually Do](https://www.youtube.com/watch?v=sxTQuFLobgk) (Scott Brant) | 15'57" | 深入理解 |
| [Copilot Cowork Walkthrough](https://www.youtube.com/watch?v=3jewNNMCxA8) (John Savill) | 18'25" | IT/高级用户 |

---

## 参考来源

| # | 来源 | URL |
|---|------|-----|
| 1 | Copilot Cowork FAQ | https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-faq |
| 2 | Responsible AI FAQ | https://learn.microsoft.com/en-us/microsoft-365/copilot/responsible-ai/cowork-responsible-ai-faq |
| 3 | Responsible AI Overview | https://learn.microsoft.com/en-us/microsoft-365/copilot/responsible-ai/cowork-responsible-ai-overview |
| 4 | Walkthrough - Rob Quickenden | https://robquickenden.blog/2026/04/copilot-cowork-walkthrough/ |
| 5 | 官方视频 | https://www.youtube.com/watch?v=j8rHJsM3fxQ |
| 6 | Enterprise Limitations - AGAT | https://agatsoftware.com/blog/microsoft-copilot-cowork-ai-agent-limitations/ |
| 7 | Explained - FindSkill.ai | https://findskill.ai/blog/copilot-cowork-explained/ |
| 8 | Prompt 指南 - Rephrase | https://rephrase-it.com/blog/copilot-cowork-claude-in-microsoft-365-2026-how-i-prompt-ai- |
| 9 | Use Cowork - Microsoft Learn | https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/use-cowork |
