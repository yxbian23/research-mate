# Course Learning Workflow

三种模式的详细工作流程定义。

---

## Phase 0: PDF 预分析（大型文件）

**触发条件**: PDF 页数 > 30 页

当处理大型 PDF 时，在正式处理前先执行预分析阶段。

### 步骤

1. **检测文件大小**
   ```bash
   # 使用 pdf_preprocessor.py 分析
   python ~/.claude/skills/course-learning/scripts/pdf_preprocessor.py <pdf_path>
   ```

2. **获取结构信息**
   - 总页数和估算 token 数
   - 目录结构（如有）
   - 章节边界
   - 内容密集页面（公式/表格多）

3. **确定分块策略**
   ```python
   # 根据模式选择分块配置
   MODE_CONFIGS = {
       "summary": {"chunk_size": 10, "overlap": 2},
       "homework": {"chunk_size": 5, "overlap": 2},
       "review": {"chunk_size": 15, "overlap": 2},
   }
   ```

4. **创建处理计划**
   ```bash
   # 生成分块计划
   python ~/.claude/skills/course-learning/scripts/chunk_manager.py <pdf_path> <mode>
   ```

### 输出

```json
{
    "total_pages": 67,
    "total_chunks": 7,
    "chunks": [
        {"id": 0, "pages": "1-10", "read": "1-12", "tokens": 8500},
        {"id": 1, "pages": "11-20", "read": "9-22", "tokens": 9200},
        ...
    ]
}
```

### 检查点

- [ ] PDF 结构分析完成
- [ ] 分块计划生成
- [ ] 预估 token 在限制内

---

## 1. Summary Workflow (--summary)

### Phase 1.0: 分块检测

**任务**: 检测是否需要分块处理

```
如果 PDF 页数 > 30:
    1. 执行 Phase 0 预分析
    2. 进入分块处理模式
否则:
    直接进入 Phase 1.1
```

### Phase 1.1: 文件准备（含分块处理）

**任务**: 读取并解析讲义 PDF

#### 标准模式（≤30 页）

```
输入: /course ./CSCI5350/2025R2/ --summary lecture3.pdf

步骤:
1. 验证路径存在
2. 使用 Read tool 读取 PDF
3. 提取文本内容和结构
4. 识别讲义元数据（标题、日期、讲师）
```

#### 分块模式（>30 页）

```
输入: /course ./ENGG5202/ --summary "Lecture 2.pdf"  # 67 页

步骤:
1. 执行 Phase 0 获取分块计划
2. 初始化 PageTracker
3. 对每个分块执行:
   a. 读取当前块页面（含重叠页）
   b. 提取关键概念和定义
   c. 记录概念→页码映射
   d. 生成块摘要作为下一块的上下文
4. 合并所有块的处理结果
```

**分块处理示例**:
```python
from page_tracker import create_tracker

tracker = create_tracker("lecture.pdf")

for chunk in chunk_plan.chunks:
    tracker.start_chunk(chunk.chunk_id)

    # 读取块内容（含重叠）
    content = read_pdf_pages(chunk.overlap_start, chunk.overlap_end)

    # 提取概念并记录
    for concept in extract_concepts(content):
        tracker.add_concept(
            name=concept.name,
            page_num=concept.page,
            category=concept.type
        )

    # 生成块摘要传递给下一块
    summary = generate_chunk_summary(content)
    tracker.end_chunk(summary)

# 合并引用
tracker.merge_references()
```

**检查点**:
- [ ] PDF 成功读取（或分块读取完成）
- [ ] 内容结构识别完成
- [ ] 页码映射建立
- [ ] 分块模式：所有块处理完成
- [ ] 分块模式：跨块引用已合并

### Phase 1.2: 内容分析

**任务**: 分析讲义结构和核心概念

```
分析维度:
1. 主题层级结构（章节、小节）
2. 核心概念列表
3. 关键定理/公式
4. 示例和应用
5. 与其他讲义的关联
```

**输出**: 内容大纲

```markdown
# Lecture 3 内容大纲

## 主要主题
1. [主题1]
   - 概念: [...]
   - 定理: [...]
2. [主题2]
   - ...

## 关键术语
- [术语1] (English Term)
- [术语2] (English Term)

## 关联
- 前置: Lecture 2 - [内容]
- 后续: Lecture 4 - [内容]
```

### Phase 1.3: 总结生成

**任务**: 生成结构化的中英双语总结

**格式要求**:

```markdown
# Lecture X: [讲义标题]

**课程**: [COURSE_CODE]
**来源**: [文件名]
**总结日期**: [日期]

---

## 概览

[1-2 段概述本讲主要内容]

---

## 核心内容

### 1. [主题1 中文名] ([English Name])

#### 1.1 基本概念

**[概念名称]** (Concept Name)

[概念解释，中文为主]

**定义**: [正式定义]

**直观理解**: [通俗解释]

**示例**:
> [具体例子]
>
> 来源: Lecture 3, Page 12

#### 1.2 关键定理

**定理 X.X** ([Theorem Name])

$$
[LaTeX 公式]
$$

**含义**: [定理的直观解释]

**应用场景**: [何时使用这个定理]

---

## 重点公式汇总

| 公式名称 | 公式 | 适用条件 | 来源 |
|---------|------|---------|------|
| [名称] | $[formula]$ | [条件] | Page X |

---

## 术语表

| 中文术语 | 英文术语 | 定义 |
|---------|---------|------|
| 纳什均衡 | Nash Equilibrium | [定义] |

---

## 与其他讲义的关联

- **前置知识**: [Lecture X 内容]
- **后续应用**: [Lecture Y 内容]
```

### Phase 1.4: 质量检查

**检查清单**:
- [ ] 所有核心概念已覆盖
- [ ] 中英文术语对照正确
- [ ] 每个重要概念有示例
- [ ] 来源页码标注完整
- [ ] 公式 LaTeX 语法正确

---

## 2. Homework Workflow (--homework)

### Phase 2.1: 题目解析

**任务**: 解析作业要求

```
输入: /course ./CSCI5350/ --homework hw1.pdf

步骤:
1. 读取作业 PDF
2. 识别题目结构（题号、分值）
3. 提取每道题的要求
4. 识别题目类型（证明/计算/分析）
```

**输出**: 题目清单

```markdown
# Homework 1 题目解析

## 题目列表
1. [Q1] (20 pts) - 证明题: 纳什均衡存在性
2. [Q2] (15 pts) - 计算题: 混合策略均衡
3. [Q3] (15 pts) - 分析题: 博弈树

## 相关讲义
- Q1: Lecture 2-3
- Q2: Lecture 3
- Q3: Lecture 4
```

### Phase 2.2: 相关内容检索

**任务**: 从讲义中检索相关内容

```
对每道题:
1. 识别关键概念
2. 在讲义中搜索相关定理、公式、示例
3. 提取可用于解答的材料
4. 标记讲义来源
```

**检索策略**:
- 使用 Grep 搜索关键术语
- 使用 Read 读取相关讲义页面
- 建立题目→讲义内容的映射

### Phase 2.3: 解答构建

**任务**: 构建解答框架并生成详细步骤

**解答原则**:
1. **基于讲义**: 只使用讲义中提到的定理和方法
2. **步骤完整**: 每一步推导都要清晰
3. **不跳步**: 不省略关键中间步骤
4. **标注来源**: 引用的定理标注讲义来源

**解答结构**:
```
对于证明题:
1. 明确要证明的命题
2. 列出将使用的定理/引理
3. 分步骤进行证明
4. 每步都有清晰的理由
5. 最后总结证毕

对于计算题:
1. 明确已知条件
2. 确定计算方法
3. 分步骤计算
4. 验证结果合理性
5. 给出最终答案
```

### Phase 2.4: 类人写作

**任务**: 以自然、类人的风格撰写解答

**关键技巧** (详见 [writing-style.md](references/writing-style.md)):

1. **结构变化**: 不要每道题结构完全相同
2. **自然过渡**: 使用自然的连接词
   - "首先考虑..."
   - "不难发现..."
   - "由定义可得..."
   - "因此..."
3. **简单步骤可省略**: 显然的步骤不需要展开
4. **个人风格**: 偶尔使用 "We observe that..." 而非 "It can be observed that..."

**禁止**:
- 完全对称的结构
- 过于正式的模板语言
- 每步都详细解释显而易见的内容
- "Let's break this down step by step" 等 AI 特征表达

### Phase 2.5: 交叉验证

**任务**: 验证关键结果的正确性

**验证方法** (详见 [cross-validation.md](references/cross-validation.md)):

1. **数值验证**: 用不同方法重新计算
2. **边界检验**: 检查边界情况是否合理
3. **维度分析**: 确保公式维度正确
4. **反例检验**: 尝试找反例（如找不到则增强信心）
5. **特例验证**: 用简单特例验证一般结论

**验证记录**:
```markdown
## 验证记录

### Q2 结果验证
- 方法1 (混合策略计算): p* = 1/3, q* = 2/3
- 方法2 (最佳响应交叉): p* = 1/3, q* = 2/3
- 边界检验: 当 p→0 或 p→1 时，结果退化合理
- 结论: ✓ 结果通过验证
```

### Phase 2.6: 输出生成

**任务**: 生成最终输出文件

**文件 1: hw_solution.tex**
```latex
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry}
\geometry{margin=1in}

\title{Homework 1 Solutions}
\author{[Student Name]}
\date{\today}

\begin{document}
\maketitle

\section*{Problem 1}

[解答内容]

\section*{Problem 2}

[解答内容]

\end{document}
```

**文件 2: hw_annotation.md**
```markdown
# Homework 1 解答注释

## 总体思路
[作业整体分析]

## 各题详解

### Problem 1 注释

**题目理解**: [题目要求什么]

**解题思路**: [思考过程]

**关键步骤**:
1. [步骤1 为什么这样做]
2. [步骤2 为什么这样做]

**易错点**:
- [易错点1]
- [易错点2]

**相关讲义**: Lecture 3, Pages 15-18
```

---

## 3. Review Workflow (--review)

### Phase 3.1: 课程扫描

**任务**: 扫描并索引课程文件夹

```
输入: /course ./ENGG5202/ --review

步骤:
1. 使用 Glob 列出所有 PDF 文件
2. 分类: 讲义 / 作业 / TA材料 / 考试
3. 按讲次排序
4. 建立文件索引
```

**输出**: 课程索引

```markdown
# ENGG5202 课程索引

## 讲义 (12)
- Lecture 1: Introduction (ENGG 5202_Lecture 1 Introduction.pdf)
- Lecture 2: Decision Tree (ENGG 5202_Lecture 2 Decision Tree.pdf)
- ...

## TA 材料 (6)
- TA Session 1: Decision Tree (ENGG 5202_TA_Decision Tree.pdf)
- ...

## 作业 (4)
- HW1, HW2, HW3, HW4

## 考试 (2)
- Midterm, Final
```

### Phase 3.2: 内容提取

**任务**: 从所有文件中提取关键内容

```
对每个讲义:
1. 读取 PDF
2. 提取主题、概念、定理、公式
3. 建立知识点列表
4. 标记重要程度
```

**重要程度标准**:
- ★★★ 核心定理、多次出现
- ★★☆ 重要概念、常见应用
- ★☆☆ 辅助内容、特殊情况

### Phase 3.3: 知识组织

**任务**: 按主题组织知识点

```
组织结构:
1. 按课程章节分组
2. 建立概念间的依赖关系
3. 识别跨章节的联系
4. 确定复习顺序
```

**知识图谱**:
```
Introduction
    ↓
Decision Tree ← Entropy (Information Theory)
    ↓
Ensemble Methods
    ↓
SVM ← Kernel Methods
    ↓
Neural Networks ← Backpropagation
```

### Phase 3.4: 复习文档生成

**任务**: 生成完整的复习指南

**文档结构** (详见 [TEMPLATES.md](TEMPLATES.md)):

```markdown
# [COURSE_CODE] 课程复习指南

## Part 1: 课程概览
- 课程结构
- 重点章节
- 考试范围

## Part 2: 分章节详解
### Chapter X: [章节名]
- 核心概念 (中英对照)
- 重要定理/公式
- 典型例题 (带详解)
- 易错点

## Part 3: 综合练习
- 章节综合题
- 期中/期末样题

## Part 4: 快速复习
- 公式速查表
- 关键概念卡片
- 考前 checklist

## Part 5: 术语表
- 中英文术语对照完整表
```

### Phase 3.5: 练习题生成

**任务**: 生成复习练习题

**练习题来源**:
1. 讲义中的例题（改编）
2. 作业题（变形）
3. TA 材料中的练习
4. 历年考试题

**每道题包含**:
- 题目描述
- 难度标记
- 详细解答
- 相关知识点

### Phase 3.6: 质量检查

**检查清单**:
- [ ] 覆盖所有讲义内容
- [ ] 概念→公式→例题 完整
- [ ] 术语表覆盖所有重要术语
- [ ] 易错点来自实际作业/考试
- [ ] 快速复习部分可在 30 分钟内浏览完

---

## 通用质量标准

### 内容质量
- 准确性: 与讲义内容一致
- 完整性: 覆盖所有重要内容
- 清晰性: 表述清楚易懂
- 实用性: 对学习有实际帮助

### 格式质量
- Markdown 语法正确
- LaTeX 公式可渲染
- 表格对齐美观
- 代码块格式正确

### 学术诚信
- 不编造内容
- 标注来源
- 对不确定处说明
- 鼓励独立思考

---

## 附录：分块处理详细说明

详见 [CHUNKING.md](CHUNKING.md) 获取完整的分块处理文档，包括：

- 各模式分块策略
- 重叠机制原理
- 页码引用规范
- 边界情况处理
- 脚本使用说明
