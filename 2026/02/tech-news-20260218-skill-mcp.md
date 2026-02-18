# Claude Code Skill与MCP集成

**日期**: 2026-02-18

## 概述

Skill和MCP是Claude Code的两个核心扩展机制。Skill提供高级工作流和领域知识，MCP提供与外部系统的标准化连接。两者结合实现强大的自动化能力。

## 什么是Skill

- **定义**：Claude Code的模块化扩展包，提供专业领域的工作流和知识
- **作用**：把通用AI助手转化为领域专家
- **触发方式**：通过斜杠命令（如`/docx`、`/pdf`）或自动触发
- **包含内容**：
  - 工作流程指导
  - 参考文档和模板
  - 可执行脚本
  - 资源文件

## 什么是MCP

- **定义**：Model Context Protocol，连接LLM与外部系统的开放协议
- **架构**：客户端-服务器模式
  - **MCP Host**：Claude Code等AI应用
  - **MCP Client**：维持连接的客户端
  - **MCP Server**：提供工具和数据的服务端
- **功能**：
  - 工具调用（Tool Calls）
  - 资源访问（Resources）
  - 提示词管理（Prompts）

## Skill与MCP如何协同

### 分层架构

```
用户请求
   ↓
Skill层（工作流编排）
   ↓
MCP层（工具和数据访问）
   ↓
外部系统（GitHub、数据库、API）
```

### 集成模式

**模式1：Skill调用MCP工具**
- Skill定义工作流程
- MCP提供具体工具实现
- 例如：`/mcp-builder` skill使用`github` MCP完成代码上传

**模式2：多MCP编排**
- 一个Skill可以协调多个MCP服务
- 例如：财务报告skill同时使用ERP MCP + SharePoint MCP

**模式3：Skill中配置MCP**
- 在skill的配置文件中定义MCP服务器
- 支持stdio（本地）和SSE（远程）两种类型

## 配置示例

### 在Skill中集成多个MCP服务

```json
{
  "github": {
    "type": "sse",
    "url": "https://mcp.github.com/sse"
  },
  "jira": {
    "type": "sse",
    "url": "https://mcp.jira.com/sse"
  }
}
```

### MCP服务器配置

```json
{
  "serverType": "stdio",
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
  "env": {
    "API_KEY": "${API_KEY}"
  }
}
```

## 实际应用场景

### 场景1：技术文档生成
```
用户：生成API文档
  ↓
/docx skill激活
  ↓
context7 MCP检索代码示例
  ↓
生成Word文档
```

### 场景2：自动化发布
```
用户：发布新版本
  ↓
自定义release skill
  ↓
github MCP创建release
  ↓
slack MCP发送通知
```

### 场景3：数据分析报告
```
用户：生成月度报告
  ↓
/monthly-financial-closing skill
  ↓
ERP MCP获取数据
  ↓
生成Excel和PPT
```

## 开发建议

### 何时创建Skill
- 重复性工作流程
- 需要领域专业知识
- 涉及多步骤操作
- 团队共享使用

### 何时创建MCP服务
- 连接外部API或数据库
- 标准化系统交互
- 需要权限管理
- 跨多个skill使用

### 最佳实践
1. **Skill专注工作流**：不要实现具体工具逻辑
2. **MCP专注接口**：提供稳定的工具定义
3. **分离关注点**：Skill编排，MCP执行
4. **错误处理**：两层都要有完善的错误处理
5. **文档完善**：清晰说明如何使用

## 技术优势

| 特性 | Skill | MCP |
|------|-------|-----|
| **可复用性** | 工作流可复用 | 工具可复用 |
| **扩展性** | 添加新skill | 添加新服务器 |
| **安全性** | 权限配置 | 认证和授权 |
| **性能** | 减少重复规划 | 标准化调用 |

## 参考

- [Claude Code官方文档](https://github.com/anthropics/claude-code)
- [MCP协议规范](https://modelcontextprotocol.io)
- [Microsoft MCP服务器](https://github.com/microsoft/mcp)

---
*通过Context7检索 | Claude Code生成*
