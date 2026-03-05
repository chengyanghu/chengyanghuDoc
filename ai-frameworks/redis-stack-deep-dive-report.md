# Redis Stack 深度研究报告

> 📊 **研究概况**
> - 研究模式: 深度
> - 检索轮数: 8 轮 (web_fetch 官方文档)
> - 参考来源: 12 个
> - 生成日期: 2026-03-05

---

## 1) TL;DR（核心要点）

1. **Redis Stack 是 Redis OSS 的增强发行版**，捆绑了 RedisJSON、RediSearch、RedisTimeSeries、RedisBloom 四大模块，提供 JSON 文档、全文/向量检索、时序数据、概率数据结构等能力。[[1]](https://redis.io/about/about-stack/)

2. **Redis 作为向量数据库（Vector Database）已正式 GA**，支持 FLAT、HNSW、SVS-VAMANA 三种向量索引类型，向量可存储在 Hash 或 JSON 文档中，配合元数据字段实现混合检索（Hybrid Search）。[[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/)

3. **混合检索通过 pre-filter + KNN 范式实现**：查询语法为 `"(filter_expr)=>[KNN k @vector $blob]" DIALECT 2`，Redis 内部自动选择 Batches 或 Ad-hoc Brute Force 模式以优化延迟。[[3]](https://redis.io/docs/latest/develop/ai/search-and-query/query/combined/)

4. **性能基准显示 Redis 在向量检索领域领先**：在 recall ≥ 0.98 的条件下，Redis 吞吐量比第二名高 62%（低维数据集），比 pgvector 高 9.5 倍，比 MongoDB Atlas Search 高 11 倍。[[4]](https://redis.io/blog/benchmarking-results-for-vector-databases/)

5. **Redis 在 RAG 架构中可同时承担三个角色**：向量知识库、语义缓存（Semantic Cache）、LLM 会话管理器（Session Manager），减少基础设施复杂度。[[5]](https://redis.io/docs/latest/develop/get-started/rag/)

6. **RedisVL（Redis Vector Library）是官方推荐的 Python 高级客户端**，封装了向量存储、搜索、语义缓存等 AI 工作流，与 TensorFlow/PyTorch/HuggingFace 等框架集成。[[6]](https://redis.io/docs/latest/develop/ai/redisvl/)

7. **时序数据能力（TimeSeries）原生支持** retention、aggregation、compaction rules 和多时序跨标签查询，适用于 IoT/监控/金融等场景。[[7]](https://redis.io/docs/latest/develop/data-types/timeseries/)

8. **概率数据结构涵盖 6 种类型**：HyperLogLog、Bloom Filter、Cuckoo Filter、t-digest、Top-K、Count-Min Sketch，用于基数估算、频率统计、百分位计算等。[[8]](https://redis.io/docs/latest/develop/data-types/probabilistic/)

---

## 2) Redis Stack 能力地图

### 组件总览

| 组件 | 解决的问题 | 典型命令/API | 来源 |
|------|-----------|-------------|------|
| **RedisJSON** | 存储/查询 JSON 文档，支持 JSONPath 嵌套访问 | `JSON.SET`, `JSON.GET`, `JSON.ARRAPPEND`, `JSON.NUMINCRBY` | [[9]](https://redis.io/docs/latest/develop/data-types/json/) |
| **RediSearch (Redis Query Engine)** | 全文检索、二级索引、向量相似度搜索（VSS）、地理空间查询、聚合 | `FT.CREATE`, `FT.SEARCH`, `FT.AGGREGATE`, `FT.DROPINDEX` | [[10]](https://redis.io/docs/latest/develop/ai/search-and-query/) |
| **RedisTimeSeries** | 时序数据采集、存储、聚合、降采样压缩 | `TS.CREATE`, `TS.ADD`, `TS.RANGE`, `TS.MRANGE`, `TS.CREATERULE` | [[7]](https://redis.io/docs/latest/develop/data-types/timeseries/) |
| **RedisBloom (Probabilistic)** | 概率数据结构：去重、基数、频率、百分位 | `BF.ADD`, `CF.ADD`, `TOPK.ADD`, `CMS.INCRBY`, `TDIGEST.ADD` | [[8]](https://redis.io/docs/latest/develop/data-types/probabilistic/) |
| **RedisInsight** | 可视化管理工具：数据浏览、Workbench CLI、Profiler、内存分析、慢查询 | GUI 工具 | [[1]](https://redis.io/about/about-stack/) |

### 与 Redis OSS 的关系

Redis Stack = **Redis OSS 核心** + **模块扩展（RediSearch + RedisJSON + RedisTimeSeries + RedisBloom）**+ **RedisInsight 开发工具**。[[1]](https://redis.io/about/about-stack/)

- **Redis Stack Server**：不含 RedisInsight，适合生产部署，可作为 Redis OSS 的直接替换（drop-in replacement）。
- **Redis Stack**：含 Redis Stack Server + RedisInsight，适合开发调试。
- **许可证**：双许可 RSALv2 + SSPL（自 2022 年 11 月起）。[[1]](https://redis.io/about/about-stack/)

### Redis Query Engine 核心能力

Redis Query Engine 提供以下搜索能力，支持在 Hash 和 JSON 文档上创建增量索引（incremental indexing）：[[10]](https://redis.io/docs/latest/develop/ai/search-and-query/)

- **全文检索（Full-text Search）**：支持 stemming、停用词、前缀/模糊匹配
- **向量相似度搜索（Vector Similarity Search, VSS）**：KNN 和 Range 查询
- **二级索引（Secondary Index）**：数值范围、Tag 精确匹配、地理空间
- **聚合（Aggregation）**：GROUPBY、REDUCE、APPLY、SORTBY
- **组合查询（Combined Queries）**：AND / OR / NOT 逻辑运算 + pre-filter KNN

---

## 3) 向量/混合检索深挖

### 3.1 核心概念

**向量字段（Vector Field）**：在 `FT.CREATE` 定义 schema 时声明，关键属性包括：[[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/)

| 属性 | 说明 |
|------|------|
| `TYPE` | 向量数据类型：`FLOAT32`、`FLOAT64`、`FLOAT16`、`BFLOAT16`、`INT8`、`UINT8` |
| `DIM` | 向量维度（必须与查询向量维度严格一致） |
| `DISTANCE_METRIC` | 距离度量：`L2`（欧氏距离）、`IP`（内积）、`COSINE`（余弦距离） |

**存储方式**：
- **Hash**：向量以 raw bytes（`np.float32.tobytes()`）存储，通过 `HSET` 写入。
- **JSON**：向量以 JSON 浮点数组存储，通过 `JSON.SET` 写入；支持多值索引（multi-value indexing，v2.6.1+）。[[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/)

### 3.2 索引类型

| 索引类型 | 适用场景 | 关键可调参数 | 来源 |
|---------|---------|-------------|------|
| **FLAT** | 小数据集（< 1M 向量），需要精确搜索 | 无额外参数 | [[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#flat-index) |
| **HNSW** | 大数据集（> 1M 向量），允许近似以换取性能 | `M`(默认 16)、`EF_CONSTRUCTION`(默认 200)、`EF_RUNTIME`(默认 10)、`EPSILON`(默认 0.01) | [[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#hnsw-index) |
| **SVS-VAMANA** | Intel 硬件优化，支持压缩（LVQ/LeanVec），内存更低 | `GRAPH_MAX_DEGREE`(默认 32)、`COMPRESSION`、`SEARCH_WINDOW_SIZE`(默认 10) | [[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#svs-vamana-index) |

**HNSW 参数调优要点**：
- `M` 值越大 → 精度越高，但内存和构建时间增加
- `EF_CONSTRUCTION` 越大 → 构建质量越高，构建时间越长
- `EF_RUNTIME` 越大 → 搜索精度越高，延迟越大
- 这些参数可在查询时通过 `PARAMS` 覆盖 [[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#runtime-query-parameters)

### 3.3 查询范式

#### a) KNN 向量搜索

```
FT.SEARCH <index> "(*)=>[KNN <k> @<vector_field> $blob]"
  PARAMS 2 blob <binary_vector>
  SORTBY __<vector_field>_score
  DIALECT 2
```

- `(*)` 表示不做 pre-filter，搜索全量向量
- 必须指定 `DIALECT 2`（向量搜索从 dialect 2 起支持）
- 默认 `LIMIT 0 10`，若 k > 10 需显式指定 `LIMIT 0 <k>`
[[11]](https://redis.io/docs/latest/develop/ai/search-and-query/query/vector-search/)

#### b) 向量范围查询（Vector Range Query）

```
FT.SEARCH <index>
  "@vector:[VECTOR_RANGE <radius> $blob]=>{$YIELD_DISTANCE_AS: dist}"
  PARAMS 2 blob <binary_vector>
  SORTBY dist
  DIALECT 2
```

适用场景：异常检测、欺诈识别等不确定最近邻数量的场景。[[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#vector-range-queries)

#### c) 混合检索（Hybrid Search / Pre-filter + KNN）

```
FT.SEARCH <index>
  "(@price:[500 1000] @condition:{new})=>[KNN 10 @vector $blob AS score]"
  PARAMS 2 blob <binary_vector>
  SORTBY score
  DIALECT 2
```

**关键原理**：`=>` 箭头左侧为过滤表达式（支持 Tag/Numeric/Text/Geo），右侧为 KNN。Redis 内部自动选择优化策略：[[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#how-filtering-works)

| 模式 | 机制 | 何时触发 |
|------|------|---------|
| **Batches** | 分批从向量索引取候选，逐批过滤直到满足 k 个 | 过滤后剩余文档较多时 |
| **Ad-hoc Brute Force** | 先过滤出满足条件的文档，再逐一计算向量距离 | 过滤后剩余文档较少时 |

可通过 `HYBRID_POLICY` 参数手动指定：`BATCHES` 或 `ADHOC_BF`。[[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#filter-mode)

### 3.4 注意事项

1. **维度一致性**：查询向量维度必须与索引定义的 `DIM` 严格一致，否则报错。[[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/)
2. **Hash 存储向量必须是 bytes**，而 JSON 存储向量是浮点数组，两者不可混用。[[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#store-and-update-vectors)
3. **COSINE 距离范围 [0, 2]**，L2 距离无上界，设计 Range Query 时需注意。[[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#important-notes)
4. **集群环境优化**：可用 `$SHARD_K_RATIO` (0.1-1.0) 控制每个分片返回的候选数量比例，平衡精度与性能。[[11]](https://redis.io/docs/latest/develop/ai/search-and-query/query/vector-search/#cluster-optimization)
5. **多线程 Query Engine**：Redis 新版 Query Engine 使用 producer-consumer 模式，单分片可通过多线程实现 16 倍吞吐提升。[[4]](https://redis.io/blog/benchmarking-results-for-vector-databases/)

---

## 4) 落地场景（≥ 6 个，按优先级排序）

### 场景 1：LLM 语义缓存（Semantic Cache）⭐⭐⭐⭐⭐

**业务问题**：LLM API 调用成本高、延迟大（数百毫秒到数秒）；相似问题重复调用浪费资源。

**数据形态**：`{question_text, question_embedding, answer_text, model_version, created_at, tenant_id}`

**Redis Stack 能力组合**：
- **RedisJSON**：存储问答对的完整文档
- **RediSearch (VECTOR + TAG + NUMERIC)**：向量索引做语义相似度匹配，TAG 做租户/模型版本隔离，NUMERIC 做时间过滤
- **Redis TTL (EXPIRE)**：原生键过期实现缓存淘汰

**关键设计点**：
- 索引 schema：`VECTOR(HNSW, DIM=1536, COSINE)` + `TAG(tenant_id)` + `TAG(model_version)` + `NUMERIC(created_at)`
- 查询路径：`"(@tenant_id:{t1} @model_version:{v2})=>[KNN 1 @embedding $blob AS dist]" DIALECT 2`，当 dist < 阈值时命中缓存
- 更新/删除：TTL 自动淘汰 + 模型版本变更时通过 TAG 过滤隔离
- 扩展：按 key prefix 分租户（`cache:{tenant}:{id}`）

**风险/指标**：
- 命中率（Hit Rate）：需监控并调整相似度阈值
- 模型版本切换导致向量空间不一致 → 按 model_version TAG 隔离
- 引用：语义缓存是 Redis RAG 架构中的官方推荐角色 [[5]](https://redis.io/docs/latest/develop/get-started/rag/)

---

### 场景 2：RAG 知识库检索 ⭐⭐⭐⭐⭐

**业务问题**：企业内部文档（FAQ、政策、产品手册）需要被 LLM 准确引用，传统关键词搜索召回不足。

**数据形态**：`{doc_id, chunk_text, chunk_embedding, source_file, department, doc_version, updated_at}`

**Redis Stack 能力组合**：
- **RedisJSON**：存储文档 chunk 及元数据
- **RediSearch**：VECTOR（语义检索）+ TEXT（全文检索 fallback）+ TAG（部门/来源过滤）+ NUMERIC（版本/时间过滤）

**关键设计点**：
- 索引 schema：
  ```
  FT.CREATE idx:rag ON JSON PREFIX 1 doc:
    SCHEMA $.chunk_embedding AS embedding VECTOR HNSW 6 TYPE FLOAT32 DIM 1536 DISTANCE_METRIC COSINE
    $.chunk_text AS chunk_text TEXT
    $.department AS department TAG
    $.doc_version AS doc_version NUMERIC
  ```
- 混合检索：先按部门/版本过滤，再做 KNN top-5
- 更新策略：文档更新时删除旧 chunk keys → 重新 embedding → 写入新 keys
- 与 LangChain/LlamaIndex 集成：RedisVL 或原生 redis-py 均支持 [[5]](https://redis.io/docs/latest/develop/get-started/rag/) [[6]](https://redis.io/docs/latest/develop/ai/redisvl/)

**风险/指标**：
- 召回质量：用 RAGAS 等框架评估 [[12]](https://redis.io/docs/latest/develop/ai/)
- chunk 大小与 overlap 影响检索效果（推测/建议：建议 400-600 token，overlap 50-100 token，需实测验证）
- 大规模文档（> 10M chunks）的内存成本

---

### 场景 3：电商/推荐 — 相似商品检索 ⭐⭐⭐⭐

**业务问题**：用户浏览商品时，实时展示"相似推荐"；需要在价格、品类等维度做过滤。

**数据形态**：`{product_id, title, description, image_embedding, category, price, brand, in_stock}`

**Redis Stack 能力组合**：
- **RedisJSON**：存储商品文档
- **RediSearch**：VECTOR（图片/文本 embedding 相似度）+ TAG（category/brand）+ NUMERIC（price）+ TEXT（title 全文检索）

**关键设计点**：
- 混合查询示例：`"(@category:{electronics} @price:[100 500])=>[KNN 20 @image_embedding $blob]" DIALECT 2`
- 实时性：商品上下架通过 `JSON.SET` / `JSON.DEL` 即时更新索引（增量索引）
- 多租户电商平台：key prefix 分店铺（`product:{shop_id}:{product_id}`）

**风险/指标**：
- 商品频繁更新导致索引重建开销 → Redis 增量索引自动处理 [[10]](https://redis.io/docs/latest/develop/ai/search-and-query/)
- 向量维度影响内存：1M 商品 × 768 维 × 4 字节 ≈ 3 GB（推测，需根据实际评估）
- 引用：Redis 官方提供 redis-product-search 示例 [[12]](https://redis.io/docs/latest/develop/ai/)

---

### 场景 4：日志/监控/指标 — 时序分析 ⭐⭐⭐⭐

**业务问题**：系统指标（CPU/内存/QPS）、IoT 传感器数据需要实时采集、聚合、告警。

**数据形态**：`{timestamp, metric_name, value, labels: {host, region, service}}`

**Redis Stack 能力组合**：
- **RedisTimeSeries**：原生时序数据类型，支持 retention、aggregation（avg/min/max/sum）、compaction rules、跨时序标签查询

**关键设计点**：
- 创建时序键并设置 retention 和 labels：
  ```
  TS.CREATE cpu:host1 RETENTION 86400000 LABELS host host1 region us-east service api
  ```
- 降采样 compaction：`TS.CREATERULE cpu:host1 cpu:host1:hourly AGGREGATION avg 3600000`
- 跨标签聚合查询：`TS.MRANGE - + FILTER region=us-east GROUPBY service REDUCE avg`
- 支持 NaN 值表示缺失数据（Redis 8.6+）[[7]](https://redis.io/docs/latest/develop/data-types/timeseries/)

**风险/指标**：
- 高频写入（每秒百万级）的内存压力 → 使用 retention + compaction 控制
- 与 Prometheus/Grafana 集成需要适配层（推测/建议：可用 RedisTimeSeries 的 Grafana 数据源插件，需验证兼容性）

---

### 场景 5：混合检索（关键词 + 语义）⭐⭐⭐⭐

**业务问题**：纯语义检索可能漏掉精确关键词匹配；纯关键词检索缺乏语义理解。需要两者结合。

**数据形态**：`{doc_id, title, content, content_embedding, tags, publish_date}`

**Redis Stack 能力组合**：
- **RediSearch**：TEXT（全文检索 BM25 评分）+ VECTOR（语义检索 cosine 距离）在同一索引中共存

**关键设计点**：
- **方案 A — Pre-filter 混合**：先用关键词/Tag 过滤，再做 KNN
  ```
  FT.SEARCH idx "(@content:machine learning @tags:{AI})=>[KNN 10 @embedding $blob]" DIALECT 2
  ```
- **方案 B — 两阶段融合**（推测/建议）：分别执行 FT.SEARCH 全文检索和 KNN 向量检索，在应用层做 RRF（Reciprocal Rank Fusion）。Redis 原生不支持 RRF，需应用层实现。
- 引用：Redis 官方 Combined Queries 文档明确支持 pre-filter + KNN [[3]](https://redis.io/docs/latest/develop/ai/search-and-query/query/combined/)

**风险/指标**：
- BM25 和向量距离的评分尺度不同，融合时需要归一化
- Pre-filter 过于严格可能导致 KNN 候选不足

---

### 场景 6：企业架构集成 — AI Agent 会话管理 + 上下文工程 ⭐⭐⭐

**业务问题**：AI Agent 需要存储和检索多轮对话历史，实现上下文感知的对话；同时需要与 RAG 知识库、语义缓存共存。

**数据形态**：`{session_id, turn_index, user_message, assistant_message, turn_embedding, timestamp, user_id}`

**Redis Stack 能力组合**：
- **RedisJSON**：存储会话记录文档
- **RediSearch (VECTOR + TAG + NUMERIC)**：按 session_id 检索，按语义相似度检索历史相关对话
- **Redis Streams / Lists**：维护对话的时序顺序
- **Redis TTL**：会话过期清理

**关键设计点**：
- 单一 Redis 实例同时承担：会话存储（Session Manager）+ 语义缓存 + RAG 知识库 → 减少运维复杂度
- 向量检索历史对话：从长对话中语义召回最相关的 K 轮，而非简单截断
- Redis 官方提供 LangGraph + Redis 集成示例 [[12]](https://redis.io/docs/latest/develop/ai/)
- Redis University 提供 "Context Engineering with Redis & LangChain" 课程 [[12]](https://redis.io/docs/latest/develop/ai/)

**风险/指标**：
- 长对话的 embedding 存储内存成本
- 会话隔离（tenant_id / user_id TAG 过滤）

---

### 场景 7（附加）：实时欺诈/异常检测 ⭐⭐⭐

**业务问题**：交易请求到达时，需要毫秒级判断其是否与已知欺诈模式相似。

**数据形态**：`{transaction_embedding, merchant_category, amount, geo_location, timestamp}`

**Redis Stack 能力组合**：
- **RediSearch**：Vector Range Query（不确定命中数量）+ NUMERIC/TAG 过滤 + GEO 过滤
- **RedisBloom (Bloom Filter)**：快速判断交易 ID 是否已处理（去重）
- **RedisTimeSeries**：记录每用户/每商户的交易频率指标

**关键设计点**：
- 使用 Vector Range Query 而非 KNN：`"@embedding:[VECTOR_RANGE 0.3 $blob]"` — 在指定半径内查找所有相似欺诈模式 [[2]](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/#vector-range-queries)
- 适合实时场景：Redis 端到端延迟 < 1ms [[4]](https://redis.io/blog/benchmarking-results-for-vector-databases/)

---

## 5) 选型决策清单

### 何时选择 Redis Stack

| 场景特征 | Redis Stack 优势 | 来源 |
|---------|-----------------|------|
| 已有 Redis 基础设施 | 直接升级，无需引入新组件 | [[1]](https://redis.io/about/about-stack/) |
| 需要极低延迟（< 10ms） | 内存存储 + 多线程 Query Engine | [[4]](https://redis.io/blog/benchmarking-results-for-vector-databases/) |
| 缓存 + 检索合一 | 同一实例兼做缓存和向量/全文检索 | [[5]](https://redis.io/docs/latest/develop/get-started/rag/) |
| 多种数据模型共存 | JSON + 向量 + 时序 + 概率结构一站式 | [[1]](https://redis.io/about/about-stack/) |
| 实时更新、增量索引 | 数据写入即自动索引，无需 ETL | [[10]](https://redis.io/docs/latest/develop/ai/search-and-query/) |
| 数据集 < 10M 向量 | 内存可控，性能显著优于磁盘方案 | [[4]](https://redis.io/blog/benchmarking-results-for-vector-databases/) |

### 何时不适合

| 场景特征 | 局限性 | 替代建议 |
|---------|--------|---------|
| 纯向量超大规模（> 100M 向量） | 全内存成本高（推测） | Milvus / Qdrant（磁盘索引）|
| 复杂多阶段召回/排序管线 | Redis 不支持原生 RRF、多路召回排序 | Elasticsearch + 自定义排序管线 |
| 需要强 ACID 事务 | Redis 事务为乐观锁，非严格 ACID | PostgreSQL + pgvector |
| 需要持久化为第一优先级 | Redis 以内存为主，RDB/AOF 有数据窗口 | 传统关系型数据库 |
| 向量维度极高（> 4096） + 需要最优压缩 | SVS-VAMANA 压缩仅限 Intel 硬件优化 | 专用 ANN 引擎 |

### 决策清单

| 决策维度 | 评估问题 | Redis Stack 适合的答案 |
|---------|---------|----------------------|
| **数据规模** | 向量总数？ | < 10M（HNSW）或 < 1M（FLAT） |
| **延迟目标** | P99 延迟要求？ | < 10ms |
| **召回要求** | 能否接受近似？ | 可以（HNSW recall ≥ 0.98） |
| **写入频率** | 实时/批量？ | 实时增量索引 ✓ |
| **是否需要 TTL** | 数据需要自动过期？ | ✓ 原生支持 |
| **混合过滤** | 需要 metadata + 向量联合查询？ | ✓ pre-filter + KNN |
| **多租户** | 需要数据隔离？ | TAG 过滤 + key prefix |
| **可观测性** | 需要慢查询/内存分析？ | RedisInsight Profiler + Slowlog |
| **已有基础设施** | 是否已部署 Redis？ | 已有 → 强烈推荐 |
| **成本模型** | 内存预算充足？ | 每 1M 向量 × 768 维 ≈ 3GB |

---

## 6) 落地蓝图

### Blueprint A：LLM 语义缓存（Semantic Cache）

#### 数据模型

```json
{
  "question": "如何重置密码？",
  "question_embedding": [0.12, -0.34, ...],  // DIM=1536, FLOAT32
  "answer": "您可以在设置页面点击'重置密码'...",
  "model_name": "gpt-4",
  "model_version": "v2",
  "tenant_id": "tenant_001",
  "created_at": 1709625600,
  "hit_count": 0
}
```

Key 格式：`semcache:{tenant_id}:{hash_id}`

#### 索引设计

```
FT.CREATE idx:semcache ON JSON PREFIX 1 semcache:
  SCHEMA
    $.question_embedding AS embedding VECTOR HNSW 10
      TYPE FLOAT32 DIM 1536 DISTANCE_METRIC COSINE M 16 EF_CONSTRUCTION 200
    $.tenant_id AS tenant_id TAG
    $.model_version AS model_version TAG
    $.created_at AS created_at NUMERIC SORTABLE
    $.question AS question TEXT
```

#### 查询路径

**步骤 1 — 语义匹配**：
```
FT.SEARCH idx:semcache
  "(@tenant_id:{tenant_001} @model_version:{v2})=>[KNN 1 @embedding $blob AS dist]"
  PARAMS 2 blob <query_embedding_bytes>
  RETURN 3 dist question answer
  SORTBY dist
  DIALECT 2
```

**步骤 2 — 阈值判断**（应用层）：
- 若 `dist < 0.15`（cosine distance）→ 缓存命中，直接返回 answer
- 若 `dist >= 0.15` → 缓存未命中，调用 LLM → 将新问答对写入 Redis

#### 更新/淘汰策略

| 策略 | 实现方式 |
|------|---------|
| **TTL 过期** | `EXPIRE semcache:{tenant}:{id} 86400`（24h） |
| **模型版本隔离** | 切换模型版本时，旧版本数据通过 TAG 过滤自动失效；可定期批量清理 |
| **LRU 淘汰** | Redis `maxmemory-policy allkeys-lru` 作为兜底 |
| **命中计数** | `JSON.NUMINCRBY semcache:{id} $.hit_count 1`，定期清理低命中条目 |

#### 最小可行 PoC 步骤

1. **部署 Redis Stack**：Docker `redis/redis-stack:latest`
2. **定义索引**：执行上述 `FT.CREATE`
3. **Embedding 服务**：用 sentence-transformers 或 OpenAI API 生成 1536 维向量
4. **写入测试数据**：`JSON.SET` 写入 100 条 FAQ 问答对
5. **查询测试**：用 redis-py 执行混合 KNN 查询，验证命中逻辑
6. **集成 LLM 调用链**：在应用层实现 cache-check → LLM-call → cache-write 流程
7. **监控**：RedisInsight Slowlog + `FT.INFO` 查看索引状态

---

### Blueprint B：RAG 检索服务

#### 数据模型

```json
{
  "chunk_id": "doc_policy_001_chunk_003",
  "source_doc": "employee_policy_v3.pdf",
  "chunk_text": "员工年假从第二年起每年增加一天...",
  "chunk_embedding": [0.05, -0.22, ...],  // DIM=1536, FLOAT32
  "department": "HR",
  "doc_version": 3,
  "page_number": 12,
  "updated_at": 1709625600
}
```

Key 格式：`rag:{department}:{chunk_id}`

#### 索引设计

```
FT.CREATE idx:rag ON JSON PREFIX 1 rag:
  SCHEMA
    $.chunk_embedding AS embedding VECTOR HNSW 10
      TYPE FLOAT32 DIM 1536 DISTANCE_METRIC COSINE M 24 EF_CONSTRUCTION 300
    $.chunk_text AS chunk_text TEXT WEIGHT 2.0
    $.department AS department TAG
    $.doc_version AS doc_version NUMERIC SORTABLE
    $.source_doc AS source_doc TAG
    $.updated_at AS updated_at NUMERIC SORTABLE
```

注意：`M=24` 和 `EF_CONSTRUCTION=300` 相比默认值更高，因为 RAG 对召回质量要求较高。

#### 查询路径

**路径 1 — 纯语义检索**：
```
FT.SEARCH idx:rag
  "(@department:{HR})=>[KNN 5 @embedding $blob AS dist]"
  PARAMS 2 blob <query_embedding_bytes>
  RETURN 4 dist chunk_text source_doc page_number
  SORTBY dist
  LIMIT 0 5
  DIALECT 2
```

**路径 2 — 混合检索（关键词 + 语义）**：
```
FT.SEARCH idx:rag
  "(@chunk_text:年假 @department:{HR})=>[KNN 5 @embedding $blob AS dist]"
  PARAMS 2 blob <query_embedding_bytes>
  RETURN 4 dist chunk_text source_doc page_number
  SORTBY dist
  LIMIT 0 5
  DIALECT 2
```

**路径 3 — 版本过滤**：
```
FT.SEARCH idx:rag
  "(@doc_version:[3 3] @department:{HR})=>[KNN 5 @embedding $blob AS dist]"
  ...
```

#### 更新/淘汰策略

| 策略 | 实现方式 |
|------|---------|
| **文档版本更新** | 新版本 chunks 用新 key 写入 → 更新 doc_version → 查询时按最新版本过滤 → 定期清理旧版本 keys |
| **增量更新** | 修改单个 chunk：`JSON.SET rag:{dept}:{chunk_id} $.chunk_text <new_text>` + 更新 embedding |
| **批量重建** | 文档大改时：删除旧 prefix keys → pipeline 批量写入新 chunks |
| **内存管理** | 监控 `FT.INFO idx:rag` 的 `num_docs` 和 `num_records`，设置 maxmemory 告警 |

#### 最小可行 PoC 步骤

1. **部署 Redis Stack**：同上
2. **文档预处理**：PDF/Markdown → 分 chunk（400-600 tokens, overlap 50-100）
3. **Embedding 生成**：批量生成 chunk embeddings
4. **Pipeline 批量写入**：redis-py Pipeline 一次写入数千 chunks
5. **创建索引**：执行 `FT.CREATE`
6. **端到端测试**：用户问题 → embedding → FT.SEARCH → top-5 chunks → 拼接 prompt → LLM 生成
7. **集成框架**：接入 LangChain/LlamaIndex 的 Redis VectorStore
8. **质量评估**：用 RAGAS 框架评估 faithfulness / answer relevancy / context precision

---

## 7) 风险与治理

### 7.1 权限隔离 / 多租户

| 风险 | 缓解措施 |
|------|---------|
| 租户数据混访 | key prefix 隔离（`{tenant}:doc:xxx`）+ TAG 字段过滤 + Redis ACL 按 key pattern 授权 |
| 索引交叉 | 每租户独立索引（`idx:{tenant}:rag`）或共享索引 + 必带 `@tenant_id:{xxx}` 过滤 |
| 推测/建议 | Redis ACL 支持按 key pattern 限制访问（`~tenant_001:*`），需验证是否覆盖 FT.SEARCH 的索引级权限 |

### 7.2 数据泄露风险

| 风险 | 缓解措施 |
|------|---------|
| 向量反推原始数据 | 向量 embedding 通常不可逆，但需防止 chunk_text 明文泄露 → Redis ACL + 网络隔离 |
| RedisInsight 暴露 | 限制 RedisInsight 仅内网访问，开启认证 |
| 传输加密 | 启用 TLS（Redis 6.0+ 原生支持） |

### 7.3 模型版本导致向量空间不一致

| 风险 | 缓解措施 |
|------|---------|
| 新旧 embedding 模型向量空间不兼容 | **TAG 隔离**：`model_version` 字段标记每条数据使用的模型版本，查询时必带版本过滤 |
| 模型升级需要全量重建 | 蓝绿部署：新索引并行构建 → 切换查询路由 → 清理旧索引 |
| 维度变化 | 新模型维度不同时必须建新索引（DIM 不可变） |

### 7.4 成本与容量（内存/索引）

| 指标 | 估算方法 |
|------|---------|
| 向量存储 | `向量数 × 维度 × 字节宽度`。例：1M × 1536 × 4B = **~5.7 GB** |
| HNSW 索引开销 | 约为向量存储的 1.5-2 倍（含图结构） |
| JSON 元数据 | 取决于字段数量和文本长度 |
| 总内存预算 | 建议按向量数据 × 3-4 倍估算总内存需求 |
| 推测/建议 | 超过 10M 向量时建议做集群分片（Redis Cluster），需基准测试验证 |

### 7.5 可观测性

| 观测维度 | 实现方式 | 来源 |
|---------|---------|------|
| **慢查询** | RedisInsight Slowlog 工具 / `SLOWLOG GET` | [[1]](https://redis.io/about/about-stack/) |
| **索引健康** | `FT.INFO <index>` → num_docs, indexing_failures, bytes_per_record | [[10]](https://redis.io/docs/latest/develop/ai/search-and-query/) |
| **缓存命中率** | 应用层统计：cache_hit / (cache_hit + cache_miss) |  |
| **查询延迟** | Redis Profiler（RedisInsight）或 `redis-cli --latency` | [[1]](https://redis.io/about/about-stack/) |
| **召回质量** | RAGAS 框架离线评估 context_precision / faithfulness | [[12]](https://redis.io/docs/latest/develop/ai/) |
| **内存使用** | RedisInsight Memory Analysis 或 `INFO memory` | [[1]](https://redis.io/about/about-stack/) |

---

## 参考资料清单

### 官方文档

1. [Redis Stack - About](https://redis.io/about/about-stack/) - Redis Stack 概述、组件、许可证
2. [Vector Search Concepts](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/) - 向量索引、搜索、过滤完整参考
3. [Combined Queries](https://redis.io/docs/latest/develop/ai/search-and-query/query/combined/) - 混合查询语法（AND/OR/NOT/pre-filter KNN）
4. [Benchmarking Results for Vector Databases](https://redis.io/blog/benchmarking-results-for-vector-databases/) - Redis 向量性能基准
5. [RAG Quick Start](https://redis.io/docs/latest/develop/get-started/rag/) - Redis 在 RAG 中的角色（向量库/语义缓存/会话管理）
6. [RedisVL Overview](https://redis.io/docs/latest/develop/ai/redisvl/) - Redis Vector Library Python 客户端
7. [TimeSeries Data Type](https://redis.io/docs/latest/develop/data-types/timeseries/) - 时序数据结构完整文档
8. [Probabilistic Data Structures](https://redis.io/docs/latest/develop/data-types/probabilistic/) - 概率数据结构概述
9. [JSON Data Type](https://redis.io/docs/latest/develop/data-types/json/) - JSON 文档存储与查询
10. [Redis Query Engine](https://redis.io/docs/latest/develop/ai/search-and-query/) - 搜索与查询引擎概述
11. [Vector Search Query](https://redis.io/docs/latest/develop/ai/search-and-query/query/vector-search/) - KNN/Range 向量查询详细指南
12. [Redis for AI Overview](https://redis.io/docs/latest/develop/ai/) - AI 生态整合、教程、课程汇总

### 生态资源

13. [Vector Database Quick Start](https://redis.io/docs/latest/develop/get-started/vector-database/) - 完整 Python 代码示例（embedding + 索引 + 搜索）
14. [Redis AI Resources GitHub](https://github.com/redis-developer/redis-ai-resources) - RAG/向量搜索 Notebook 集合
15. [Redis Product Search](https://github.com/redis-developer/redis-product-search) - 电商产品搜索示例
16. [LangGraph + Redis](https://github.com/redis-developer/langgraph-redis/tree/main/examples) - AI Agent 集成示例

### 客户端库

17. [redis-py](https://redis-py.readthedocs.io/en/stable/) - Python 客户端
18. [Jedis](https://github.com/redis/jedis) - Java 客户端
19. [NRedisStack](https://github.com/redis/NRedisStack) - .NET 客户端
20. [node_redis](https://github.com/redis/node-redis) - Node.js 客户端

---

*Research Skill v4.0 生成 | 2026-03-05*
*检索统计: web_fetch 共 8 轮，12+ 官方来源*
