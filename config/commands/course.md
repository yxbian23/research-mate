---
description: 课程学习助手 - 讲义总结、作业辅助、考试复习。支持中英双语总结、LaTeX 作业解答、完整复习指南。
---

# Course Command

CUHK 博士生课程学习辅助命令，支持三种模式：
- **--summary**: 讲义总结（中英双语）
- **--homework**: 作业辅助（LaTeX + 中文注释）
- **--review**: 复习文档生成

---

## 使用语法

```bash
/course <path> --summary [files...]    # 总结讲义
/course <path> --homework <file>       # 作业辅助
/course <path> --review                # 生成复习文档
```

---

## Mode 1: Summary (--summary)

### 用法

```bash
# 总结单个讲义
/course ./CSCI5350/2025R2/ --summary lecture3.pdf

# 总结多个讲义
/course ./CSCI5350/2025R2/ --summary lecture1.pdf lecture2.pdf lecture3.pdf

# 总结目录下所有讲义
/course ./CSCI5350/2025R2/ --summary all

# 指定输出语言
/course ./ENGG5202/ --summary "Lecture 1.pdf" --lang zh    # 中文为主（默认）
/course ./ENGG5202/ --summary "Lecture 1.pdf" --lang en    # 英文为主
```

### 输出

- `summary_lecture[X].md` - 结构化的讲义总结

### 输出格式特点

- 中文表述为主，英文术语辅助
- 每个概念: "纳什均衡 (Nash Equilibrium)"
- 配有示例和来源页码
- 术语对照表

---

## Mode 2: Homework (--homework)

### 用法

```bash
# 基本用法
/course ./CSCI5350/ --homework hw1.pdf

# 指定参考讲义范围
/course ./CSCI5350/ --homework assignment1.pdf --lectures 2025R2/

# 指定输出目录
/course ./CSCI5350/ --homework hw1.pdf --output ./solutions/
```

### 输出

- `hw[X]_solution.tex` - LaTeX 格式的英文解答
- `hw[X]_annotation.md` - 中文详细注释文档

### 关键特性

1. **类人写作风格**: 避免 AI 检测
   - 结构有变化
   - 自然过渡语
   - 简单步骤适度省略

2. **交叉验证**: 关键结果用多种方法验证

3. **基于讲义**: 仅使用讲义中的定理和方法

4. **详细注释**: 中文解释思路和易错点

### 学术诚信提醒

**本工具仅用于学习参考，严禁直接提交 AI 生成的作业。**

使用者必须：
- 理解并验证所有解答
- 用自己的方式重新表述
- 遵守课程学术诚信政策

---

## Mode 3: Review (--review)

### 用法

```bash
# 基本用法 - 生成整个课程的复习文档
/course ./ENGG5202/ --review

# 指定学期
/course ./CSCI5350/2025R2/ --review

# 指定复习重点
/course ./CSCI5350/ --review --focus midterm    # 期中重点
/course ./CSCI5350/ --review --focus final      # 期末重点
/course ./CSCI5350/ --review --focus all        # 全部内容（默认）
```

### 输出

- `review_[COURSE_CODE].md` - 完整的课程复习指南

### 复习文档内容

1. **课程概览**: 结构、重点章节、考试范围
2. **分章节详解**:
   - 核心概念（中英对照）
   - 重要定理/公式
   - 典型例题（带详解）
   - 易错点
3. **综合练习**: 章节综合题、历年真题
4. **快速复习**: 公式速查表、概念卡片、考前清单
5. **术语表**: 完整中英术语对照

---

## 支持的课程结构

### Pattern A: 按学期组织

```
CSCI5350/
├── 2024R2/
│   ├── lecture1.pdf
│   ├── lecture2.pdf
│   ├── hw1.pdf
│   └── hw2.pdf
└── 2025R2/
    ├── lecture1.pdf
    └── assignment1.pdf
```

### Pattern B: 扁平结构

```
ENGG5202/
├── ENGG 5202_Lecture 1 Introduction.pdf
├── ENGG 5202_Lecture 2 Decision Tree.pdf
├── ENGG 5202_TA_Decision Tree.pdf
└── ...
```

---

## 可选参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--lang` | 输出语言: `zh` / `en` | `zh` |
| `--lectures` | 指定参考讲义目录 | 自动检测 |
| `--output` | 输出目录 | 当前目录 |
| `--focus` | 复习重点: `midterm` / `final` / `all` | `all` |
| `--depth` | 详细程度: `brief` / `standard` / `detailed` | `standard` |
| `--pages` | 指定页范围（如 `1-30`） | 全部 |
| `--chunk-size` | 自定义分块大小（页数） | 模式默认 |
| `--full` | 强制完整处理（禁用分块） | `false` |

---

## 大型 PDF 处理

当 PDF 页数超过 30 页时，自动启用分块处理模式：

### 自动分块

```bash
# 67 页的讲义会自动分块处理
/course ./ENGG5202/ --summary "ENGG 5202_Lecture 2 Decision Tree.pdf"
```

处理流程：
1. 预分析 PDF 结构（页数、目录、章节边界）
2. 根据模式选择分块策略（summary: 10页/块）
3. 逐块读取和处理（每块含 2 页重叠上下文）
4. 合并结果并维护准确的页码引用

### 指定页范围

```bash
# 只处理第 1-30 页
/course ./ENGG5202/ --summary "Lecture 2.pdf" --pages 1-30

# 处理第 31-67 页
/course ./ENGG5202/ --summary "Lecture 2.pdf" --pages 31-67
```

### 自定义分块

```bash
# 使用 8 页为一块
/course ./ENGG5202/ --summary "Lecture 2.pdf" --chunk-size 8
```

### 强制完整处理

```bash
# 禁用分块（注意：可能导致上下文溢出）
/course ./ENGG5202/ --summary "Lecture 2.pdf" --full
```

### 分块策略

| 模式 | 默认块大小 | 重叠 | 说明 |
|------|-----------|------|------|
| summary | 10 页 | 2 页 | 平衡覆盖和精度 |
| homework | 5 页 | 2 页 | 精确定位相关内容 |
| review | 15 页 | 2 页 | 完整章节上下文 |

详细说明见 `~/.claude/skills/course-learning/CHUNKING.md`

---

## 示例

### 示例 1: 总结 Game Theory 讲义

```bash
/course ./CSCI5350/2025R2/ --summary lecture3.pdf
```

输出 `summary_lecture3.md`:
- 本讲核心概念：纳什均衡、混合策略等
- 每个概念中英对照并配示例
- 重要定理和公式
- 与其他讲义的关联

### 示例 2: 完成 Pattern Recognition 作业

```bash
/course ./ENGG5202/ --homework "Assignment 1.pdf"
```

输出:
- `Assignment1_solution.tex`: LaTeX 解答
- `Assignment1_annotation.md`: 中文注释

### 示例 3: 准备期末复习

```bash
/course ./CSCI5350/2025R2/ --review --focus final
```

输出 `review_CSCI5350.md`:
- 考试重点章节
- 核心公式速查
- 典型例题详解
- 考前 checklist

---

## Related Skills

- `course-learning/` - 完整的课程学习技能包

## Related Agents

- `course-assistant` - 课程学习助手 Agent

## Related Rules

- `academic-integrity.md` - 学术诚信规范
