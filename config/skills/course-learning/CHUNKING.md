# PDF Chunking System

大型 PDF 文件的智能分块处理策略。

---

## 概述

当 PDF 页数超过 30 页时，`/course` 命令自动启用分块模式。分块系统通过以下方式确保大型文件的有效处理：

1. **预分析**：快速扫描 PDF 获取结构信息
2. **智能分块**：根据模式和内容密度确定最优分块
3. **重叠处理**：保持跨块上下文连续性
4. **引用追踪**：维护准确的页码引用

---

## 分块策略

### 各模式默认配置

| 模式 | 基础块大小 | 重叠页数 | 最大 Token | 适用场景 |
|------|-----------|---------|-----------|---------|
| `summary` | 10 页 | 2 页 | 30,000 | 需要广泛覆盖的讲义总结 |
| `homework` | 5 页 | 2 页 | 25,000 | 需要精确定位的作业辅助 |
| `review` | 15 页 | 2 页 | 35,000 | 需要完整上下文的复习 |

### 分块策略选择依据

1. **Summary 模式 (10 页)**
   - 需要理解整体结构
   - 概念可能跨多页展开
   - 适度的块大小平衡覆盖和处理

2. **Homework 模式 (5 页)**
   - 需要精确定位相关内容
   - 小块便于快速找到相关定理
   - 更高的处理精度

3. **Review 模式 (15 页)**
   - 需要完整的章节上下文
   - 综合多个概念的关联
   - 大块减少上下文切换

---

## 重叠机制

### 为什么需要重叠

- 概念可能在页面边界被分割
- 定理的证明可能跨越多页
- 上下文信息帮助理解当前内容

### 重叠策略

```
Chunk 1: Pages 1-10  (read: 1-12)
Chunk 2: Pages 11-20 (read: 9-22)
Chunk 3: Pages 21-30 (read: 19-32)
...
```

每个块：
- **核心范围**：需要处理的主要页面
- **读取范围**：包含前后各 2 页重叠

### 重叠处理规则

1. **首块**：无前向重叠
2. **末块**：无后向重叠
3. **中间块**：前后各 2 页重叠

---

## 使用方法

### 自动模式（推荐）

```bash
# 自动检测是否需要分块
/course ./ENGG5202/ --summary "Lecture 2.pdf"
```

### 指定页范围

```bash
# 只处理特定页范围
/course ./ENGG5202/ --summary "Lecture 2.pdf" --pages 1-30
```

### 自定义块大小

```bash
# 使用自定义块大小
/course ./ENGG5202/ --summary "Lecture 2.pdf" --chunk-size 8
```

### 强制完整处理

```bash
# 禁用分块（注意：可能导致上下文溢出）
/course ./ENGG5202/ --summary "Lecture 2.pdf" --full
```

---

## 处理流程

### Phase 0: 预分析

```python
# 运行预分析脚本
python pdf_preprocessor.py <pdf_path>

# 输出
{
    "total_pages": 67,
    "estimated_tokens": 45000,
    "chapter_boundaries": [1, 15, 32, 48],
    "content_dense_pages": [12, 13, 25, 26, 45]
}
```

### Phase 1: 分块处理

对每个块执行：

1. **读取**：读取当前块页面（含重叠）
2. **提取**：提取关键概念和定义
3. **记录**：记录概念→页码映射
4. **总结**：生成块摘要传递给下一块

### Phase 2: 合并

1. **合并引用**：去重和合并跨块引用
2. **生成术语表**：汇总所有概念
3. **生成输出**：合并所有块的处理结果

---

## 页码引用规范

### 引用格式

```markdown
**来源**: Page 15
**来源**: Pages 15-17
**来源**: Lecture 2, Pages 15, 23, 45
```

### 引用追踪

使用 `page_tracker.py` 维护：

```python
tracker = create_tracker("lecture.pdf")

# 添加概念引用
tracker.add_concept(
    name="纳什均衡",
    english_name="Nash Equilibrium",
    page_num=15,
    category="definition",
    section="2.3 Equilibrium Concepts"
)

# 生成术语表
glossary = tracker.generate_glossary()
```

---

## 边界情况处理

### 1. 跨页概念

**问题**：定义在第 10 页开始，第 11 页结束

**解决**：
- 重叠机制确保两个块都能看到完整定义
- 在第一个块记录起始页，合并时保持

### 2. 章节边界

**问题**：块可能在章节中间断开

**解决**：
- 预分析识别章节边界
- 尽量在章节边界处分块
- `respect_boundaries=True` 启用此行为

### 3. 内容密集页

**问题**：某些页面公式/表格密集，token 数高

**解决**：
- 预分析识别 content_dense_pages
- 自动调整块大小避免超限
- 密集页可能单独成块

### 4. 很小的块

**问题**：最后一块可能只有几页

**解决**：
- 如果剩余页数 < 3，合并到前一块
- 确保每块至少有实质内容

---

## 性能优化

### 1. 并行预分析

对于多文件处理，可并行运行预分析：

```bash
# 并行分析多个 PDF
for pdf in *.pdf; do
    python pdf_preprocessor.py "$pdf" --json > "${pdf%.pdf}.json" &
done
wait
```

### 2. 缓存预分析结果

```python
# 检查缓存
cache_path = pdf_path.with_suffix('.analysis.json')
if cache_path.exists():
    metadata = load_cached_analysis(cache_path)
else:
    metadata = analyze_pdf(pdf_path)
    save_analysis(metadata, cache_path)
```

### 3. 增量处理

对于部分更新的 PDF：
- 保存 tracker 状态到 JSON
- 只处理新增/变更的页面
- 合并新旧结果

---

## 脚本说明

### pdf_preprocessor.py

```bash
# 分析 PDF
python pdf_preprocessor.py lecture.pdf

# JSON 输出
python pdf_preprocessor.py lecture.pdf --json
```

输出信息：
- 总页数和 token 估算
- 目录结构
- 章节边界
- 内容密集页

### chunk_manager.py

```bash
# 生成分块计划
python chunk_manager.py lecture.pdf summary

# JSON 输出
python chunk_manager.py lecture.pdf homework --json
```

输出信息：
- 分块配置
- 每块的页范围
- 估算 token 数

### page_tracker.py

```bash
# 创建追踪器
python page_tracker.py create lecture.pdf

# 加载并显示
python page_tracker.py load tracker.json

# 生成术语表
python page_tracker.py glossary tracker.json

# 生成页面索引
python page_tracker.py index tracker.json
```

---

## 最佳实践

### 1. 选择合适的模式

| 任务 | 推荐模式 | 原因 |
|------|---------|------|
| 快速浏览讲义 | summary | 平衡覆盖和精度 |
| 查找特定定理 | homework | 小块快速定位 |
| 考前复习 | review | 完整上下文理解 |

### 2. 调整块大小

- **公式密集**：减小块大小（8-10 页）
- **文字为主**：可增大块大小（15-20 页）
- **图表多**：使用默认（token 估算会自动调整）

### 3. 验证引用

处理完成后检查：
- 所有重要概念都有引用
- 引用页码准确
- 无重复或遗漏

### 4. 监控 Token 使用

```python
# 检查单块是否超限
if chunk.estimated_tokens > 40000:
    print(f"Warning: Chunk {chunk.chunk_id} may be too large")
```

---

## 故障排除

### 问题：上下文仍然溢出

**原因**：块大小仍然太大

**解决**：
1. 使用 `--chunk-size 5` 减小块大小
2. 使用 `--pages` 处理部分内容
3. 检查是否有特别密集的页面

### 问题：跨块内容不连贯

**原因**：上下文传递不充分

**解决**：
1. 检查 chunk_summaries 是否正确保存
2. 增加重叠页数
3. 在块结束时生成更详细的摘要

### 问题：页码引用不准确

**原因**：引用来自重叠区域

**解决**：
1. 使用 page_tracker 统一管理引用
2. 合并时调用 `tracker.merge_references()`
3. 验证引用来自核心范围还是重叠范围

---

## 相关文件

- `scripts/pdf_preprocessor.py` - PDF 预分析
- `scripts/chunk_manager.py` - 分块管理
- `scripts/page_tracker.py` - 页码追踪
- `WORKFLOW.md` - 完整工作流程
- `../course.md` - 命令使用说明
