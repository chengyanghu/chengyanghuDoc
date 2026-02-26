# OpenCode 研究报告

## 一、OpenCode 上手指南

### 1.1 安装方法

| 平台 | 安装命令 |
|------|---------|
| **通用（推荐）** | `curl -fsSL https://opencode.ai/install \| bash` |
| **macOS** | `brew install opencode` |
| **Windows** | `choco install opencode` 或 `npm install -g opencode-ai` |
| **Linux** | `paru -S opencode-bin` (Arch) 或下载二进制 |

### 1.2 快速配置流程

1. 运行 `opencode`
2. 执行 `/connect` 命令连接 AI 提供商
3. 选择模型：OpenCode Zen（官方精选）或自定义 API Key
4. 进入项目目录，运行 `/init` 初始化项目

### 1.3 核心使用方式

- **Ask 模式**：询问代码库问题
- **Plan 模式**：分析项目结构，制定实现计划
- **Build 模式**：执行代码修改
- **AGENTS.md**：在项目根目录创建此文件，帮助 AI 理解项目结构

### 1.4 支持的 AI 提供商

OpenCode 支持 **75+** AI 模型提供商，包括 [[1]](https://opencode.ai/docs/)：
- OpenAI (GPT-4/4o)
- Anthropic (Claude)
- Google Gemini
- AWS Bedrock
- Azure OpenAI
- Ollama (本地模型)
- Moonshot AI (Kimi)

---

## 二、OpenCode vs Claude Code 核心对比

### 2.1 基本信息对比

| 维度 | OpenCode | Claude Code |
|------|---------|-------------|
| **开源性质** | MIT 开源 [[2]](https://www.builder.io/blog/opencode-vs-claude-code) | 专有 |
| **开发团队** | Anomaly (SST 团队) [[2]](https://www.builder.io/blog/opencode-vs-claude-code) | Anthropic |
| **GitHub Stars** | 48K+ (2026年1月) [[3]](https://morphllm.com/comparisons/opencode-vs-claude-code) | 47K+ |
| **许可证** | MIT | Proprietary |

### 2.2 模型支持

| 维度 | OpenCode | Claude Code |
|------|---------|-------------|
| **模型支持** | 75+ 提供商 [[1]](https://opencode.ai/docs/) | 仅 Anthropic 模型 |
| **本地模型** | 支持 Ollama [[4]](https://www.sourceboxai.com/blog/the-basics-how-to-install-and-use-opencode) | 不支持 |
| **模型切换** | 可按任务切换提供商 | 自动在 Haiku/Sonnet/Opus 间切换 |

### 2.3 定价模式

| 维度 | OpenCode | Claude Code |
|------|---------|-------------|
| **工具费用** | 免费（MIT） | 免费（CLI） |
| **模型费用** | 自带 API Key，按需付费 | Pro $20/月，Max $100/月 |
| **订阅方案** | OpenCode Black $200/月（企业版）[[5]](https://thomas-wiegold.com/blog/i-switched-from-claude-code-to-opencode/) | 订阅制，含 API 调用 |

### 2.4 核心功能对比

| 功能 | OpenCode | Claude Code |
|------|---------|-------------|
| **IDE 集成** | VS Code / Cursor / Zed / Windsurf | 官方插件 |
| **MCP 支持** | ✅ (stdio, SSE, OAuth) [[5]](https://thomas-wiegold.com/blog/i-switched-from-claude-code-to-opencode/) | ✅ (stdio, HTTP, OAuth) |
| **Checkpoints** | Git-based /undo 和 /redo | 自动工作区快照 |
| **多会话** | 原生多会话 | 命名会话、分支 |

---

## 三、性能与架构对比

### 3.1 性能表现

根据 Benchmark 测试 [[3]](https://morphllm.com/comparisons/opencode-vs-claude-code)：

| 指标 | OpenCode | Claude Code |
|------|---------|-------------|
| **任务完成速度** | 较慢（默认运行完整测试套件） | 快 45%，优化低延迟 |
| **测试生成数量** | 94 个测试 | 73 个测试 |
| **SWE-bench 得分** | 取决于所用模型 | Opus 4.5 达 80.9% |

### 3.2 架构差异

- **Claude Code**：垂直整合方案，Tight integration with ripgrep 和 LSP
- **OpenCode**：水平灵活性方案，基于 OpenTUI 框架 [[5]](https://thomas-wiegold.com/blog/i-switched-from-claude-code-to-opencode/)

---

## 四、优缺点分析

### OpenCode 优势
- ✅ **灵活性高**：支持 75+ 提供商，可按任务切换模型
- ✅ **隐私优先**：支持本地模型（Ollama），敏感代码不出本地
- ✅ **成本可控**：自带 API Key，按需付费，无订阅压力
- ✅ **开源透明**：MIT 许可证，社区活跃
- ✅ **多 IDE 支持**：Cursor、Windsurf 等新兴编辑器

### OpenCode 劣势
- ⚠️ 生态成熟度较低，偶有 Bug
- ⚠️ 配置相对复杂，需要选择提供商
- ⚠️ 安全漏洞历史：CVE-2026-22812（已修复）[[5]](https://thomas-wiegold.com/blog/i-switched-from-claude-code-to-opencode/)

### Claude Code 优势
- ✅ **开箱即用**：订阅制体验，无缝集成
- ✅ **性能优化**：低延迟，LSP 导航约 50ms
- ✅ **稳定性高**：企业级质量，版本发布规范
- ✅ **顶级模型**：独家访问 Opus 4.5

### Claude Code 劣势
- ❌ 仅支持 Anthropic 模型
- ❌ 订阅制成本较高
- ❌ 2026年1月起限制第三方工具使用 OAuth [[5]](https://thomas-wiegold.com/blog/i-switched-from-claude-code-to-opencode/)

---

## 五、选择建议

| 场景 | 推荐 | 理由 |
|------|-----|------|
| 需要多提供商切换 | OpenCode | 75+ 提供商，按需选择 |
| 预算有限 | OpenCode + Zen | 工具免费，模型按量计费 |
| 追求极致性能 | Claude Code (Opus) | 80.9% SWE-bench 得分 |
| 企业/团队使用 | Claude Code | 稳定可靠，企业级支持 |
| 隐私敏感项目 | OpenCode + Ollama | 完全本地运行 |
| Vim/Neovim 用户 | OpenCode | 终端工作流优先 |
| 快速原型开发 | 两者皆可 | 核心功能已趋同 |

> **关键发现**：当使用相同的底层模型时，OpenCode 与 Claude Code 的代码输出质量几乎相同 [[3]](https://morphllm.com/comparisons/opencode-vs-claude-code)。

---

## 六、2026 年最新动态

- Anthropic 于 2026年1月9日 阻止第三方工具使用 Claude 订阅 OAuth 令牌 [[5]](https://thomas-wiegold.com/blog/i-switched-from-claude-code-to-opencode/)
- OpenCode GitHub Stars 在5天内增长 3,610 颗 [[3]](https://morphllm.com/comparisons/opencode-vs-claude-code)
- 预计2026年 40% 的应用将采用 AI 代理 [[3]](https://morphllm.com/comparisons/opencode-vs-claude-code)

---

## 参考来源

- [1] OpenCode Official Docs: https://opencode.ai/docs/
- [2] Builder.io Comparison: https://www.builder.io/blog/opencode-vs-claude-code
- [3] Morph LLM Comparison: https://morphllm.com/comparisons/opencode-vs-claude-code
- [4] SourceBox AI Guide: https://www.sourceboxai.com/blog/the-basics-how-to-install-and-use-opencode
- [5] Thomas Wiegold Blog: https://thomas-wiegold.com/blog/i-switched-from-claude-code-to-opencode/
- [6] DataCamp Comparison: https://www.datacamp.com/blog/opencode-vs-claude-code
- [7] Byteiota Analysis: https://byteiota.com/opencode-vs-claude-code-2026-battle-guide-48k-vs-47k/
