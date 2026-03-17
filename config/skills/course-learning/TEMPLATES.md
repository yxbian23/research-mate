# Course Learning Templates

输出文档的标准模板。

---

## 1. Summary Template (总结模板)

```markdown
# Lecture [X]: [讲义标题]

**课程**: [COURSE_CODE] - [课程名称]
**来源**: [文件名]
**日期**: [讲义日期]
**总结日期**: [生成日期]

---

## 本讲概览

[2-3 句话概述本讲核心内容和学习目标]

**前置知识**: [需要先掌握的内容，来自哪些 Lecture]

**关键词**: `[keyword1]`, `[keyword2]`, `[keyword3]`

---

## 核心内容

### 1. [主题1 中文] ([English Topic])

#### 概念介绍

[概念的详细解释，中文为主]

> **定义** ([Definition Name])
>
> [正式的数学或技术定义]

**直观理解**: [用简单的语言解释这个概念]

#### 关键性质

1. **[性质1名称]**: [描述]
2. **[性质2名称]**: [描述]

#### 示例

**例 1.1**: [例题描述]

> **解答**:
>
> [详细解答过程]
>
> *来源: Page [X]*

---

### 2. [主题2 中文] ([English Topic])

[同上结构...]

---

## 重要定理与公式

### 定理 [X.X]: [定理名称] ([Theorem English Name])

**陈述**:

$$
[LaTeX 公式]
$$

**条件**: [定理适用的条件]

**直观理解**: [定理的含义]

**证明思路**: [证明的关键步骤，可选]

**应用**: [何时使用这个定理]

*来源: Page [X]*

---

### 公式 [X.X]: [公式名称]

$$
[LaTeX 公式]
$$

其中:
- $[变量1]$: [含义]
- $[变量2]$: [含义]

**使用场景**: [何时使用]

---

## 公式速查表

| 名称 | 公式 | 条件 | 页码 |
|------|------|------|------|
| [名称1] | $[formula]$ | [条件] | P.[X] |
| [名称2] | $[formula]$ | [条件] | P.[X] |

---

## 术语对照表

| 中文 | English | 定义简述 |
|------|---------|---------|
| [术语1] | [Term 1] | [简短定义] |
| [术语2] | [Term 2] | [简短定义] |

---

## 与其他内容的关联

### 前序关联
- **Lecture [X]**: [相关内容及如何关联]

### 后续关联
- **Lecture [Y]**: [本讲内容如何为后续内容奠定基础]

---

## 学习检查

完成本讲学习后，应能回答：

1. [ ] [检查问题1]?
2. [ ] [检查问题2]?
3. [ ] [检查问题3]?

---

*本总结基于 [文件名] 生成，仅供学习参考*
```

---

## 2. Homework Solution Template (作业解答模板)

### 2.1 LaTeX 解答模板 (hw_solution.tex)

```latex
\documentclass[11pt,a4paper]{article}

% 基本包
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{hyperref}

% 定理环境
\theoremstyle{definition}
\newtheorem{problem}{Problem}
\newtheorem*{solution}{Solution}

% 常用命令
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\E}{\mathbb{E}}
\newcommand{\Var}{\mathrm{Var}}
\DeclareMathOperator*{\argmax}{argmax}
\DeclareMathOperator*{\argmin}{argmin}

\title{[COURSE_CODE] Homework [X] Solutions}
\author{[Student Name] \\ [Student ID]}
\date{\today}

\begin{document}
\maketitle

% ========== Problem 1 ==========
\begin{problem}[XX points]
[题目重述，可选]
\end{problem}

\begin{solution}
[解答内容]

% 对于证明题
We first show that [要证明的内容].

Consider [设定]. By [定理/定义名称], we have
\[
[公式]
\]

Since [条件], it follows that [结论].

% 对于计算题
Given [已知条件], we need to find [目标].

From [来源], the formula is:
\[
[公式]
\]

Substituting the values:
\begin{align*}
[变量] &= [表达式] \\
       &= [计算步骤] \\
       &= [结果]
\end{align*}

Therefore, [最终答案].
\end{solution}

\newpage

% ========== Problem 2 ==========
\begin{problem}[XX points]
[题目]
\end{problem}

\begin{solution}
[解答]
\end{solution}

% 继续其他题目...

\end{document}
```

### 2.2 中文注释模板 (hw_annotation.md)

```markdown
# [COURSE_CODE] Homework [X] 解答注释

**作业文件**: [文件名]
**生成日期**: [日期]

---

## 作业总览

**题目数量**: [X] 题
**总分**: [X] 分
**涉及内容**: Lecture [X] - Lecture [Y]

### 题目分布
| 题号 | 分值 | 类型 | 主要考点 |
|------|------|------|---------|
| 1 | [X] | [证明/计算/分析] | [考点] |
| 2 | [X] | [...] | [...] |

---

## 各题详解

### Problem 1

#### 题目理解

[用自己的话描述题目要求什么]

**关键信息提取**:
- 已知: [已知条件1], [已知条件2]
- 求: [目标]
- 约束: [如有]

#### 解题思路

**第一反应**: [看到题目的第一想法]

**思路演进**:
1. [想法1] → [为什么行/不行]
2. [想法2] → [最终采用的方法]

**核心 insight**: [解这道题的关键洞察]

#### 关键步骤详解

**步骤 1**: [步骤描述]

为什么这样做: [原因解释]

对应讲义: Lecture [X], Page [Y]

**步骤 2**: [步骤描述]

[继续解释...]

#### 易错点

1. **[易错点1]**: [描述]
   - 正确做法: [...]
   - 错误做法: [...]

2. **[易错点2]**: [描述]

#### 验证

**验证方法**: [使用的验证方法]

**验证结果**: [验证是否通过]

#### 相关知识点

- [知识点1]: Lecture [X], Page [Y]
- [知识点2]: Lecture [X], Page [Y]

---

### Problem 2

[同上结构...]

---

## 综合笔记

### 本次作业核心收获

1. [收获1]
2. [收获2]

### 需要复习的内容

- [ ] [内容1]
- [ ] [内容2]

### 拓展思考

[可选：题目的变形、推广等]

---

*本注释仅供学习参考，请确保理解后独立完成作业*
```

---

## 3. Review Document Template (复习文档模板)

```markdown
# [COURSE_CODE] 课程复习指南

**课程名称**: [课程全名]
**学期**: [20XX-20XX 学年 第X学期]
**生成日期**: [日期]

---

## Part 1: 课程概览

### 1.1 课程结构

| 章节 | 主题 | 讲义 | 重要程度 |
|------|------|------|---------|
| Ch.1 | [主题] | Lec 1-2 | ★★★ |
| Ch.2 | [主题] | Lec 3-4 | ★★☆ |
| ... | ... | ... | ... |

### 1.2 章节依赖关系

```
Ch.1 Introduction
    ↓
Ch.2 [Topic] ← Ch.3 [Topic]
    ↓
Ch.4 [Topic]
    ↓
Ch.5 [Topic] ← Ch.6 [Topic]
```

### 1.3 考试重点

根据历年考试和作业分布，重点关注：

1. **高频考点** (★★★)
   - [考点1]
   - [考点2]

2. **中频考点** (★★☆)
   - [考点3]
   - [考点4]

3. **基础内容** (★☆☆)
   - [考点5]

---

## Part 2: 分章节详解

### Chapter 1: [章节名称]

**对应讲义**: Lecture 1-2
**重要程度**: ★★★

#### 1.1 核心概念

##### [概念1 中文] (English Term)

**定义**: [正式定义]

**直观理解**: [通俗解释]

**关键性质**:
1. [性质1]
2. [性质2]

**常见误区**: [误区描述]

##### [概念2 中文] (English Term)

[同上结构...]

#### 1.2 重要定理

##### 定理 1.1: [定理名称]

$$
[定理公式]
$$

**条件**: [适用条件]

**理解**: [直观解释]

**典型应用**: [应用场景]

**证明要点**: [可选，证明的关键步骤]

#### 1.3 关键公式

| 公式名 | 公式 | 使用条件 |
|--------|------|---------|
| [名称1] | $[formula]$ | [条件] |
| [名称2] | $[formula]$ | [条件] |

#### 1.4 典型例题

**例题 1.1** [难度: ★★☆]

[题目描述]

<details>
<summary>查看解答</summary>

**解答**:

[详细解答过程]

**关键点**: [这道题的关键在于...]

</details>

**例题 1.2** [难度: ★★★]

[继续...]

#### 1.5 易错点汇总

| 易错点 | 错误做法 | 正确做法 |
|--------|---------|---------|
| [易错点1] | [错误] | [正确] |
| [易错点2] | [错误] | [正确] |

---

### Chapter 2: [章节名称]

[同上结构...]

---

## Part 3: 综合练习

### 3.1 章节综合题

**综合题 1**: [题目，综合 Ch.1-2 内容]

<details>
<summary>提示</summary>
[提示内容]
</details>

<details>
<summary>解答</summary>
[详细解答]
</details>

### 3.2 历年考题精选

#### 20XX Midterm Q1

[题目]

<details>
<summary>解答</summary>
[解答]
</details>

---

## Part 4: 考前快速复习

### 4.1 公式速查表

#### Chapter 1 公式

| 公式 | 用途 |
|------|------|
| $[formula1]$ | [用途] |
| $[formula2]$ | [用途] |

#### Chapter 2 公式

[继续...]

### 4.2 关键概念卡片

<div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">

**[概念名称]** (English)

一句话定义: [定义]

关键点: [要点]

</div>

[更多概念卡片...]

### 4.3 考前 Checklist

- [ ] Ch.1: [核心内容] 掌握
- [ ] Ch.1: [关键公式] 记住
- [ ] Ch.2: [核心内容] 掌握
- [ ] ...
- [ ] 历年真题: 至少做过一遍
- [ ] 错题: 复习过易错点

---

## Part 5: 完整术语表

| 中文术语 | English Term | 定义 | 首次出现 |
|---------|--------------|------|---------|
| [术语1] | [Term 1] | [定义] | Lec 1 |
| [术语2] | [Term 2] | [定义] | Lec 2 |
| ... | ... | ... | ... |

---

## 附录

### A. 讲义索引

| 讲义 | 主题 | 关键内容 |
|------|------|---------|
| Lec 1 | [主题] | [内容] |
| ... | ... | ... |

### B. 参考资料

- 教材: [教材名称]
- 参考书: [参考书名称]
- 在线资源: [如有]

---

*本复习指南基于 [COURSE_CODE] 课程材料生成，仅供学习参考*
```

---

## 4. 中英术语对照表模板

```markdown
# [COURSE_CODE] 中英术语对照表

| 中文术语 | English Term | 缩写 | 定义 | 首次出现 |
|---------|--------------|------|------|---------|
| 纳什均衡 | Nash Equilibrium | NE | 所有玩家都采用最佳响应策略的状态 | Lec 2 |
| 帕累托最优 | Pareto Optimality | PO | 不存在帕累托改进的状态 | Lec 3 |
| 占优策略 | Dominant Strategy | - | 无论对手如何行动都是最佳的策略 | Lec 2 |
| 混合策略 | Mixed Strategy | - | 在纯策略上的概率分布 | Lec 3 |
| 支付矩阵 | Payoff Matrix | - | 记录各策略组合下各玩家收益的矩阵 | Lec 1 |
| 博弈树 | Game Tree | - | 表示序贯博弈的树形结构 | Lec 4 |
| 子博弈完美均衡 | Subgame Perfect Equilibrium | SPE | 在每个子博弈中都是纳什均衡的策略 | Lec 5 |
```

---

## 模板使用说明

1. **根据实际内容填充**: 模板中的 `[...]` 需要替换为实际内容
2. **保持格式一致**: 同一文档中保持相同的格式风格
3. **适当调整**: 根据课程特点可适当调整模板结构
4. **LaTeX 检查**: 生成后检查所有 LaTeX 公式能正常渲染
