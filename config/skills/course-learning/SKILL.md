---
name: course-learning
description: CUHK PhD course learning assistant for lecture summarization, homework assistance, and exam review. Triggers on "课程", "作业", "复习", "homework", "review", "lecture", "考试", "/course". Supports bilingual output (Chinese main + English terms) for summaries, LaTeX homework with human-like writing, and comprehensive review documents.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - Task
---

# Course Learning Assistant Skill

为 CUHK 博士生设计的课程学习辅助系统，支持三大核心功能：
1. **课程总结** (--summary) - 中文为主，英文术语辅助
2. **作业辅助** (--homework) - LaTeX 格式，类人写作，交叉验证
3. **考试复习** (--review) - 完整复习文档，每个概念配例子

---

## Quick Start

```bash
# 总结单个讲义
/course ./CSCI5350/2025R2/ --summary lecture3.pdf

# 完成作业
/course ./CSCI5350/ --homework hw1.pdf

# 生成复习文档
/course ./ENGG5202/ --review
```

---

## 学术诚信声明

**本工具仅用于辅助学习，严禁直接提交 AI 生成的作业。**

使用者必须：
1. 理解并验证所有解答
2. 用自己的方式重新表述
3. 标注任何不确定的推导
4. 遵守课程的学术诚信政策

---

## 三种模式概览

### Mode 1: Summary (--summary)

**输入**: 单个或多个讲义 PDF
**输出**: `summary_lectureX.md`

**特点**:
- 中文表述为主
- 重要术语标注英文："纳什均衡 (Nash Equilibrium)"
- 每个概念配示例
- 标注讲义来源页码

**用法**:
```bash
/course ./CSCI5350/2025R2/ --summary lecture3.pdf
/course ./CSCI5350/2025R2/ --summary lecture1.pdf lecture2.pdf lecture3.pdf
/course ./CSCI5350/2025R2/ --summary all  # 总结所有讲义
```

### Mode 2: Homework (--homework)

**输入**: 作业 PDF
**输出**:
- `hw_solution.tex` - LaTeX 格式英文答案
- `hw_annotation.md` - 中文详细注释

**特点**:
- 类人写作风格（避免 AI 检测）
- 交叉验证关键结果
- 不编造，基于讲义内容
- 详细步骤推导

**用法**:
```bash
/course ./CSCI5350/ --homework hw1.pdf
/course ./CSCI5350/ --homework assignment1.pdf --lectures 2025R2/
```

### Mode 3: Review (--review)

**输入**: 课程文件夹
**输出**: `review_[COURSE_CODE].md`

**特点**:
- 完整的课程复习指南
- 中英双语术语表
- 每个概念配例题
- 易错点总结
- 考前快速清单

**用法**:
```bash
/course ./ENGG5202/ --review
/course ./CSCI5350/2025R2/ --review
```

---

## 课程文件夹结构识别

### Pattern A: 按学期组织
```
CSCI5350/
├── 2024R2/
│   ├── lecture1.pdf - lecture10.pdf
│   └── hw1.pdf, hw2.pdf, hw3.pdf
└── 2025R2/
    ├── lecture1.pdf - lecture4.pdf
    └── assignment1.pdf
```

**识别特征**: 子目录命名包含 `20XXR[1-2]` 或 `semester`

### Pattern B: 扁平结构
```
ENGG5202/
├── ENGG 5202_Lecture 1 Introduction.pdf
├── ENGG 5202_Lecture 2 Decision Tree.pdf
├── ENGG 5202_TA_Decision Tree.pdf
└── ...
```

**识别特征**: 所有文件在同一目录，文件名包含 `Lecture X` 或 `TA_`

### 文件类型检测

| 模式 | 检测规则 |
|------|---------|
| 讲义 | `lecture`, `Lecture`, `lec`, `slides` |
| 作业 | `hw`, `homework`, `assignment`, `ps` |
| TA 材料 | `TA_`, `tutorial`, `recitation` |
| 考试 | `exam`, `midterm`, `final`, `quiz` |

---

## 核心工作流程

详见 [WORKFLOW.md](WORKFLOW.md) 获取完整工作流程。

### Summary 流程简述
1. 读取 PDF 内容
2. 识别主题层级结构
3. 提取核心概念
4. 生成中英双语总结
5. 添加示例和来源标注

### Homework 流程简述
1. 解析题目要求
2. 检索相关讲义内容
3. 构建解答框架
4. 生成 LaTeX 解答（类人风格）
5. 交叉验证关键结果
6. 生成中文注释文档

### Review 流程简述
1. 扫描课程文件夹
2. 构建知识图谱
3. 按主题整理内容
4. 生成完整复习指南
5. 添加练习题和快速清单

---

## 输出质量要求

### 总结文档
- [ ] 结构清晰，层级分明
- [ ] 每个概念有中英文术语
- [ ] 每个重要概念配示例
- [ ] 标注来源页码

### 作业解答
- [ ] LaTeX 能正常编译
- [ ] 写作风格自然（非 AI 模板化）
- [ ] 关键计算交叉验证
- [ ] 步骤完整，逻辑清晰
- [ ] 无编造内容

### 复习文档
- [ ] 覆盖所有讲义内容
- [ ] 概念→公式→例题 完整
- [ ] 术语表完备
- [ ] 易错点明确
- [ ] 可用于考前快速复习

---

## 关键参考文件

- [WORKFLOW.md](WORKFLOW.md) - 详细工作流程
- [TEMPLATES.md](TEMPLATES.md) - 输出模板
- [references/writing-style.md](references/writing-style.md) - 类人写作指南
- [references/latex-patterns.md](references/latex-patterns.md) - LaTeX 模板
- [references/cross-validation.md](references/cross-validation.md) - 交叉验证方法

---

## 常用课程代码

| 课程代码 | 课程名称 | 类型 |
|---------|---------|------|
| CSCI5350 | Game-Theoretic and AI-Based Techniques | 博弈论 |
| ENGG5202 | Pattern Recognition | 机器学习 |
| CSCI5160 | Approximation Algorithms | 算法 |
| IERG5154 | Information Theory | 信息论 |
| SEEM5680 | Optimization | 优化 |

---

## 使用限制

1. **学术诚信**: 不直接提交 AI 生成的作业
2. **内容验证**: 所有解答需要人工验证
3. **不编造**: 仅基于提供的讲义内容
4. **标注不确定**: 对不确定的推导必须标注

---

## Related Commands

- `/analyze-paper` - 论文深度分析
- `/implement-paper` - 论文实现

## Related Skills

- `research-paper-workflow/` - 论文写作
- `pdf/` - PDF 处理工具
