# 1. 礼来与 NVIDIA 合作基线 (Benchmark)

## 1.1 合作时间线

| 时间 | 事件 | 关键细节 |
|------|------|---------|
| 2025-10-28 | LillyPod 发布 | 全球首个 DGX B300 系统的 NVIDIA DGX SuperPOD，由 1,016 颗 Blackwell Ultra GPU 构建 [[1]](https://blogs.nvidia.com/?p=86280) |
| 2025-10-28 | NVIDIA GTC 大会亮相 | 宣布为制药企业全资运营的最大最强 AI 工厂 [[2]](https://lilly.gcs-web.com/news-releases/news-release-details/lilly-partners-nvidia-build-industrys-most-powerful-ai) |
| 2026-01-12 | 联合创新实验室发布 | J.P. Morgan Healthcare Conference 宣布，双方联合投资最高 **10 亿美元**（5 年期）[[3]](https://investor.lilly.com/node/53651/pdf) |
| 2026-02-26 | LillyPod 正式上线 | 全球药企最强 AI 工厂开始运行 [[4]](https://blogs.nvidia.com/blog/lilly-ai-factory-live/) |
| 2026-04-12 | BioNeMo 平台深化 | 扩展至 Thermo Fisher、TetraScience 等合作伙伴 [[5]](https://finance.via.news/corporate-finance/nvidia-s-bionemo-platform-secures-eli-lilly-partnership-as-biotech-ai) |

## 1.2 合作模式

| 维度 | 详情 |
|------|------|
| **合作形态** | 联合创新实验室（Co-Innovation Lab）+ 自建 AI 工厂（LillyPod） |
| **投资规模** | 双方联合最高 10 亿美元 / 5 年 [[3]](https://investor.lilly.com/node/53651/pdf) |
| **实验室选址** | 美国南旧金山（South San Francisco） |
| **所有权** | LillyPod 为礼来全资拥有运营；联合实验室为合资模式 |
| **人员构成** | 多学科科学家、AI 研究人员、工程师联合团队 |

## 1.3 核心技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **GPU 硬件** | NVIDIA Blackwell Ultra (B300) | 1,016 颗 GPU，DGX SuperPOD 架构 |
| **下一代架构** | NVIDIA Vera Rubin | 联合实验室规划的下一代计算架构 [[3]](https://investor.lilly.com/node/53651/pdf) |
| **AI 平台** | NVIDIA BioNeMo | 预训练生物医学模型、分子生成、蛋白质结构预测工具集 [[5]](https://finance.via.news/corporate-finance/nvidia-s-bionemo-platform-secures-eli-lilly-partnership-as-biotech-ai) |
| **集群管理** | DGX SuperPOD | 端到端超算集群管理和调度 |
| **互联网络** | NVLink / InfiniBand | 高速 GPU 间和节点间通信 |
| **软件框架** | CUDA + PyTorch 生态 | 标准 AI/ML 研发栈 |

## 1.4 覆盖的药物研发场景

| 场景 | 说明 |
|------|------|
| **分子识别与优化** | 利用基础模型（Foundation Model）加速小分子和生物制剂的发现 [[2]](https://lilly.gcs-web.com/news-releases/news-release-details/lilly-partners-nvidia-build-industrys-most-powerful-ai) |
| **分子验证** | AI 辅助的候选分子验证流程 |
| **蛋白质结构预测** | BioNeMo 平台提供的结构预测工具 |
| **物理 AI / 分子模拟** | 将物理模拟与 AI 结合加速分子动力学研究 [[4]](https://blogs.nvidia.com/blog/lilly-ai-factory-live/) |
| **制造优化** | AI 在药物制造流程中的应用 [[2]](https://lilly.gcs-web.com/news-releases/news-release-details/lilly-partners-nvidia-build-industrys-most-powerful-ai) |
| **医学影像** | 基于 AI 的医学影像分析 |
| **Agentic AI** | 企业级 AI Agent 应用于研发全流程 [[4]](https://blogs.nvidia.com/blog/lilly-ai-factory-live/) |
| **机器人与自动化** | 机器人和物理 AI 加速药物发现和生产规模化 [[3]](https://investor.lilly.com/node/53651/pdf) |

## 1.5 对中国市场的启示

礼来-NVIDIA 合作为中国本土替代方案设定了以下基准：

1. **算力规模**: 千卡级 GPU 集群，支持大规模基础模型训练
2. **端到端平台**: 不只是芯片，需要从硬件到软件的完整解决方案
3. **药物研发专用工具**: 类 BioNeMo 的预训练生物模型和工具链
4. **集群交付能力**: 类 DGX SuperPOD 的整机交付和运维能力
5. **投资规模**: 亿级美元量级的长期合作承诺
