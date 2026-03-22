# API Key Model Restriction & CLI-Anything 研究报告

**日期**: 2026-03-22  
**分类**: ai-frameworks

---

## 📋 核心答案

### 问题1: 为什么 API Key 只能使用特定模型？

API Key 模型限制通常由 **API 提供商的层级体系** 和 **认证方式** 决定。Google Gemini API 使用四层系统，不同层级有不同的模型访问权限。[[1]](https://www.aifreeapi.com/en/posts/gemini-api-key-tiers)

### 问题2: CLI-Anything 是什么？

CLI-Anything 是香港大学数据科学实验室（HKUDS）开发的开源工具，能够自动为任何软件生成 CLI 接口，使 AI Agent 可以控制 GIMP、Blender、LibreOffice 等应用程序。一周内获得 13,000+ GitHub Stars。[[2]](https://github.com/HKUDS/CLI-Anything)

---

## 💡 详细说明

### 一、API Key 模型限制的原因

#### 1.1 Google Gemini API 四层系统

Google Gemini API 采用基于计费历史的四级体系：[[1]](https://www.aifreeapi.com/en/posts/gemini-api-key-tiers)

| 层级 | 条件 | 模型访问 | 速率限制 |
|------|------|----------|----------|
| **Free** | 无需信用卡 | 部分模型，排除实验/预览模型 | 15 RPM, 1,500 RPD |
| **Tier 1** | 启用计费 | 完整生产模型目录 | 150-2,000 RPM |
| **Tier 2** | $250 实际消费 + 30 天 | 高吞吐量模型 | 1,000-4,000 RPM |
| **Tier 3** | $1,000 实际消费 | 企业级配额 | 2,000-4,000+ RPM |

**关键发现**：
- Free 层级限制只能使用 Gemini 模型的子集
- 实验性/预览模型（如 `gemini-3-flash-preview`）可能需要特定层级或特殊权限
- 某些模型变体（如 `gemini-3.1-pro-preview-customtools`）**仅限 Gemini API Key 认证**（即 AI Studio 生成的 Key）[[3]](https://github.com/google-gemini/gemini-cli/issues/22062)

#### 1.2 认证方式影响模型可用性

GitHub Issue #22062 揭示了一个重要发现：[[3]](https://github.com/google-gemini/gemini-cli/issues/22062)

> `gemini-3.1-pro-preview-customtools` 模型变体**仅在通过 Gemini API Key 认证时可用**（即从 Google AI Studio 创建的 API Key）。

这意味着：
- 相同的 Google Cloud 项目，不同的认证方式，可用模型不同
- Vertex AI 认证 vs AI Studio Key 认证 → 模型列表不同

#### 1.3 免费层限制变更

2026 年 1 月起，Google 对 Gemini API 配额进行了重大调整：[[4]](https://discuss.ai.google.dev/t/gemini-api-free-tier-limit-is-0-cannot-use-api-despite-valid-key/114215)

- 多个模型取消了免费日配额
- 用户遇到 `429 RESOURCE_EXHAUSTED` 错误，显示 `limit: 0`
- 解决方案：启用付费账户或切换到仍提供免费层的 `Gemini 2.5 Flash` 模型

#### 1.4 API Key 安全限制

API Key 可以配置三种限制，这些限制也可能影响模型访问：[[1]](https://www.aifreeapi.com/en/posts/gemini-api-key-tiers)

1. **IP 地址限制**：仅允许特定 IP 调用
2. **HTTP Referrer 限制**：仅允许特定域名调用
3. **API 服务限制**：仅允许特定 Google API 调用

---

### 二、CLI-Anything 深度解析

#### 2.1 项目定位

CLI-Anything 的核心理念：[[2]](https://github.com/HKUDS/CLI-Anything)

> "Today's Software Serves Humans. Tomorrow's Users will be Agents."

**问题**：AI Agent 无法可靠地使用 GUI 软件
**方案**：自动分析源代码，生成结构化 CLI 接口

#### 2.2 技术架构

7 阶段自动生成流水线：[[5]](https://pasqualepillitteri.it/en/news/391/cli-anything-software-agent-native-guide)

```
1. Analyze  → 分析源代码，映射 GUI 操作到 API
2. Design   → 设计命令组和状态模型
3. Implement → 构建 Click-based CLI（含 REPL + JSON 输出）
4. Plan Tests → 规划测试规范
5. Write Tests → 实现单元和端到端测试
6. Document → 生成 HARNESS.md 规范文档
7. Package  → 打包发布
```

#### 2.3 为什么选择 CLI？

CLI 作为通用接口的优势：[[5]](https://pasqualepillitteri.it/en/news/391/cli-anything-software-agent-native-guide)

| 特性 | GUI 自动化 | 自定义 API | CLI-Anything |
|------|-----------|-----------|--------------|
| **可靠性** | 脆弱（UI 更新即失效） | 稳定但有限 | 稳定且完整 |
| **速度** | 慢（UI 渲染） | 快 | 快（无 UI 开销） |
| **可组合性** | 低 | 中 | 高（命令可链式调用） |
| **自描述性** | 无 | 需文档 | `--help` 自动发现 |

#### 2.4 支持平台

- **Claude Code**（主要平台）- 完整支持
- OpenCode / OpenClaw / Codex / Qodercli - 工作集成
- Cursor / Windsurf - 即将支持 [[6]](https://www.xugj520.cn/en/archives/cli-anything-ai-agent-tools.html)

#### 2.5 安装与使用

```bash
# Claude Code 安装
/plugin marketplace add HKUDS/CLI-Anything
/plugin install cli-anything

# 为 GIMP 生成 CLI
/cli-anything:cli-anything ./gimp

# 安装生成的 CLI
cd gimp/agent-harness && pip install -e .

# 使用
cli-anything-gimp --json layer add -n "Background" --type solid --color "#1a1a2e"
```

#### 2.6 已生成的 CLI

| 软件 | 类型 | CLI 名称 | 命令数 |
|------|------|----------|--------|
| GIMP | 图像编辑 | `cli-anything-gimp` | 158 |
| Blender | 3D 建模 | `cli-anything-blender` | 208 |
| Inkscape | 矢量图形 | `cli-anything-inkscape` | 202 |
| LibreOffice | 办公套件 | `cli-anything-libreoffice` | - |

#### 2.7 与 MCP 的关系

CLI-Anything 与 Model Context Protocol (MCP) 解决不同问题：[[7]](https://apidog.com/blog/how-to-use-cli-anything/)

- **CLI-Anything**：为 GUI 应用生成 CLI 包装器
- **MCP**：为 AI Agent 提供结构化工具接口

两者可以结合使用：MCP 封装云服务 API，CLI-Anything 封装本地 GUI 应用。

---

## 🔗 参考来源

1. [How to Get Gemini API Keys for All Tiers](https://www.aifreeapi.com/en/posts/gemini-api-key-tiers)
2. [CLI-Anything GitHub Repository](https://github.com/HKUDS/CLI-Anything)
3. [GitHub Issue #22062: Model restricted to Gemini API Key auth](https://github.com/google-gemini/gemini-cli/issues/22062)
4. [Gemini API Free tier limit is 0 discussion](https://discuss.ai.google.dev/t/gemini-api-free-tier-limit-is-0-cannot-use-api-despite-valid-key/114215)
5. [CLI-Anything: How to Make Any Software Controllable by AI](https://pasqualepillitteri.it/en/news/391/cli-anything-software-agent-native-guide)
6. [CLI-Anything: Turn Any Software into AI Agent Tools](https://www.xugj520.cn/en/archives/cli-anything-ai-agent-tools.html)
7. [How to use CLI-Anything: make any software agent-native](https://apidog.com/blog/how-to-use-cli-anything/)