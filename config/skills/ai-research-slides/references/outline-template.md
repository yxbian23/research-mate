# AI Research Slides Outline Template

AI 研究论文分析的标准大纲格式。

## Outline Format

```markdown
# AI Research Paper Analysis

**Paper**: [论文标题]
**Venue**: [会议/期刊, 年份]
**Authors**: [作者列表]
**Analysis Depth**: [quick/standard/detailed]
**Language**: [zh/en]
**Generated**: YYYY-MM-DD HH:mm

---

<STYLE_INSTRUCTIONS>
[样式指令块]
</STYLE_INSTRUCTIONS>

---

[幻灯片内容]
```

---

## Section 1: TLDR (Slide 1)

```markdown
## Slide 1 of N

**Type**: Cover
**Section**: 1-TLDR
**Filename**: 01-slide-tldr.png

// NARRATIVE GOAL
一句话概括论文核心：问题、方法、结果

// KEY CONTENT
Headline: [论文标题]
Sub-headline: [TLDR 一句话总结，≤50字]
Venue: [会议/期刊 年份]
Authors: [主要作者]

// VISUAL
Clean cover with prominent title, TLDR as subtitle, venue badge

// LAYOUT
Layout: paper-title
```

---

## Section 2: 核心故事与贡献 (Slides 2-4)

### 2a: 问题与动机

```markdown
## Slide 2 of N

**Type**: Content
**Section**: 2-核心故事
**Filename**: 02-slide-motivation.png

// NARRATIVE GOAL
阐述问题的重要性和现有方法的不足

// KEY CONTENT
Headline: 问题与动机
Sub-headline: 为什么这个问题重要？
Body:
- [现有方法局限1]
- [现有方法局限2]
- [这个问题为什么难]

// VISUAL
Left: 现有方法的问题展示
Right: 理想状态/目标

// LAYOUT
Layout: split-screen
```

### 2b: 核心洞察

```markdown
## Slide 3 of N

**Type**: Content
**Section**: 2-核心故事
**Filename**: 03-slide-insight.png

// NARRATIVE GOAL
揭示论文的核心 insight，为什么这个方法能 work

// KEY CONTENT
Headline: 核心洞察
Sub-headline: [一句话总结 key insight]
Body:
- 关键观察：[观察内容]
- 技术洞察：[洞察内容]
- 解决思路：[思路描述]

// VISUAL
Central diagram showing the key insight, with annotations

// LAYOUT
Layout: hub-spoke
```

### 2c: 主要贡献

```markdown
## Slide 4 of N

**Type**: Content
**Section**: 2-核心故事
**Filename**: 04-slide-contributions.png

// NARRATIVE GOAL
明确列出论文的主要贡献

// KEY CONTENT
Headline: 主要贡献
Body:
1. **[贡献类型]**: [具体描述]
2. **[贡献类型]**: [具体描述]
3. **[贡献类型]**: [具体描述]
(Optional) 4. **[贡献类型]**: [具体描述]

// VISUAL
Numbered list with icons, each contribution clearly separated

// LAYOUT
Layout: contributions
```

---

## Section 3: 相关工作与区别 (Slides 5-6)

### 3a: 相关工作概览

```markdown
## Slide 5 of N

**Type**: Content
**Section**: 3-相关工作
**Filename**: 05-slide-related-work.png

// NARRATIVE GOAL
定位论文在研究领域中的位置

// KEY CONTENT
Headline: 相关工作
Sub-headline: 研究领域全景
Body:
**方向A**: [Work1], [Work2] - [简述]
**方向B**: [Work3], [Work4] - [简述]
**方向C**: [Work5], [Work6] - [简述]

// VISUAL
Hub-spoke or matrix showing research landscape

// LAYOUT
Layout: hub-spoke
```

### 3b: 关键区别

```markdown
## Slide 6 of N

**Type**: Content
**Section**: 3-相关工作
**Filename**: 06-slide-comparison.png

// NARRATIVE GOAL
突出本工作与 prior work 的核心区别

// KEY CONTENT
Headline: 与现有工作的区别
Body:
| 方面 | Prior Work | 本工作 |
|------|-----------|--------|
| [维度1] | [描述] | [描述] |
| [维度2] | [描述] | [描述] |
| [维度3] | [描述] | [描述] |

// VISUAL
Comparison table or binary split view

// LAYOUT
Layout: comparison-matrix
```

---

## Section 4: Method 方法详解 (Slides 7-11)

### 4a: 方法总览

```markdown
## Slide 7 of N

**Type**: Content
**Section**: 4-Method
**Filename**: 07-slide-method-overview.png

// NARRATIVE GOAL
展示方法的整体框架

// KEY CONTENT
Headline: 方法框架
Sub-headline: [方法名称] Overview
Body:
- 输入: [描述]
- 输出: [描述]
- 核心模块: [模块1], [模块2], [模块3]

// VISUAL
Pipeline/Architecture diagram from paper

// LAYOUT
Layout: methods-diagram

// IMAGE_SOURCE
Source: extract
Figure: Figure [N]
Page: [N]
Caption: [图注]
```

### 4b-4d: 核心模块

```markdown
## Slide 8 of N

**Type**: Content
**Section**: 4-Method
**Filename**: 08-slide-module-a.png

// NARRATIVE GOAL
详细解释核心模块 A

// KEY CONTENT
Headline: [模块名称]
Sub-headline: [一句话描述功能]
Body:
- 输入: [格式, 维度]
- 设计要点:
  - [要点1]
  - [要点2]
- 输出: [格式, 维度]

// VISUAL
Module diagram with annotations

// LAYOUT
Layout: split-screen
```

### 4e: 数据流程

```markdown
## Slide 11 of N

**Type**: Content
**Section**: 4-Method
**Filename**: 11-slide-data-pipeline.png

// NARRATIVE GOAL
展示数据处理流程

// KEY CONTENT
Headline: 数据处理流程
Body:
**原始数据**: [来源, 规模]
**预处理**:
1. [步骤1]
2. [步骤2]
3. [步骤3]
**数据格式**: [最终格式描述]

// VISUAL
Linear flow diagram: Raw → Process → Format

// LAYOUT
Layout: linear-progression
```

---

## Section 5: 实现细节 (Slides 12-14)

### 5a: 训练配置

```markdown
## Slide 12 of N

**Type**: Content
**Section**: 5-实现细节
**Filename**: 12-slide-training.png

// NARRATIVE GOAL
提供可复现的训练配置

// KEY CONTENT
Headline: 训练配置
Body:
| 配置 | 值 |
|------|------|
| Optimizer | [AdamW] |
| Learning Rate | [1e-4, cosine decay] |
| Batch Size | [32 × 8 GPUs] |
| Training Steps | [100K] |
| Hardware | [8 × A100 80GB] |
| Training Time | [~24 hours] |

// VISUAL
Clean table with key training hyperparameters

// LAYOUT
Layout: dashboard
```

### 5b: 推理配置

```markdown
## Slide 13 of N

**Type**: Content
**Section**: 5-实现细节
**Filename**: 13-slide-inference.png

// NARRATIVE GOAL
提供推理配置和性能指标

// KEY CONTENT
Headline: 推理配置
Body:
| 配置 | 值 |
|------|------|
| Batch Size | [1] |
| Inference Steps | [50] |
| Latency | [~2s per sample] |
| Memory | [~16GB] |
| Acceleration | [Flash Attention, FP16] |

// VISUAL
Dashboard showing inference metrics

// LAYOUT
Layout: dashboard
```

### 5c: 模型规模

```markdown
## Slide 14 of N

**Type**: Content
**Section**: 5-实现细节
**Filename**: 14-slide-model-scale.png

// NARRATIVE GOAL
展示模型和数据规模

// KEY CONTENT
Headline: 模型与数据规模
Body:
**模型规模**:
- Total Params: [X B]
- Architecture: [描述]

**数据规模**:
- Training Data: [X samples / X tokens]
- Validation Data: [X samples]

// VISUAL
Key statistics with large numbers highlighted

// LAYOUT
Layout: bento-grid
```

---

## Section 6: 实验分析 (Slides 15-19)

### 6a: 主实验结果

```markdown
## Slide 15 of N

**Type**: Content
**Section**: 6-实验分析
**Filename**: 15-slide-main-results.png

// NARRATIVE GOAL
展示主要实验结果和 SOTA 对比

// KEY CONTENT
Headline: 主实验结果
Sub-headline: [在XX基准上达到 SOTA]
Body:
| Method | Metric1 | Metric2 | Metric3 |
|--------|---------|---------|---------|
| Baseline1 | X.X | X.X | X.X |
| Baseline2 | X.X | X.X | X.X |
| **Ours** | **X.X (+Δ)** | **X.X (+Δ)** | **X.X** |

// VISUAL
Results table from paper with best results highlighted

// LAYOUT
Layout: results-chart

// IMAGE_SOURCE
Source: extract
Figure: Table [N]
Page: [N]
Caption: [表注]
```

### 6b: 效果分析

```markdown
## Slide 16 of N

**Type**: Content
**Section**: 6-实验分析
**Filename**: 16-slide-analysis.png

// NARRATIVE GOAL
分析结果背后的原因

// KEY CONTENT
Headline: 效果分析
Sub-headline: 为什么我们的方法更好？
Body:
- **主要提升**: [哪个指标提升最多, +X%]
- **原因分析**:
  - [原因1]
  - [原因2]
- **边界情况**: [哪些情况下表现一般]

// VISUAL
Annotated chart or comparison visualization

// LAYOUT
Layout: split-screen
```

### 6c: 定性结果

```markdown
## Slide 17 of N

**Type**: Content
**Section**: 6-实验分析
**Filename**: 17-slide-qualitative.png

// NARRATIVE GOAL
展示定性对比结果

// KEY CONTENT
Headline: 定性对比
Body:
Grid showing: Input | Baseline | Ours | GT
[描述可以观察到什么]

// VISUAL
2x4 or 3x4 comparison grid from paper

// LAYOUT
Layout: qualitative-grid

// IMAGE_SOURCE
Source: extract
Figure: Figure [N]
Page: [N]
Caption: [图注]
```

### 6d: 消融实验

```markdown
## Slide 18 of N

**Type**: Content
**Section**: 6-实验分析
**Filename**: 18-slide-ablation.png

// NARRATIVE GOAL
展示各组件的贡献

// KEY CONTENT
Headline: 消融实验
Sub-headline: 每个组件的贡献
Body:
| 配置 | Metric | Δ |
|------|--------|-----|
| Full | X.X | - |
| w/o A | X.X | -Y.Y |
| w/o B | X.X | -Y.Y |
| w/o C | X.X | -Y.Y |

**结论**: [组件X贡献最大, 组件Y与Z有协同效应]

// VISUAL
Ablation table with delta columns

// LAYOUT
Layout: results-chart

// IMAGE_SOURCE
Source: extract
Figure: Table [N]
Page: [N]
Caption: [表注]
```

### 6e: 失败案例 (Optional)

```markdown
## Slide 19 of N

**Type**: Content
**Section**: 6-实验分析
**Filename**: 19-slide-failure-cases.png

// NARRATIVE GOAL
诚实展示方法的失败情况

// KEY CONTENT
Headline: 失败案例分析
Body:
**Case 1**: [描述]
- 原因: [分析]

**Case 2**: [描述]
- 原因: [分析]

// VISUAL
Side-by-side showing failure cases with annotations

// LAYOUT
Layout: qualitative-grid
```

---

## Section 7: 总结与展望 (Slides 20-21)

### 7a: 工作总结

```markdown
## Slide 20 of N

**Type**: Content
**Section**: 7-总结展望
**Filename**: 20-slide-summary.png

// NARRATIVE GOAL
总结评价这项工作

// KEY CONTENT
Headline: 工作总结
Body:
**整体评价**:
- ✅ 创新性: [评价]
- ✅ 实用性: [评价]
- ✅ 完整性: [评价]
- [可选] ❌ 不足: [评价]

**可复现性**: [是否开源, 细节是否充足]

// VISUAL
Summary card with evaluation points

// LAYOUT
Layout: bullet-list
```

### 7b: Limitations & Future Work

```markdown
## Slide 21 of N

**Type**: Back Cover
**Section**: 7-总结展望
**Filename**: 21-slide-limitations.png

// NARRATIVE GOAL
指出局限性和未来方向

// KEY CONTENT
Headline: Limitations & Future Work
Body:
**Limitations**:
1. [论文提到的局限1]
2. [论文提到的局限2]
3. [你发现的问题]

**Future Directions**:
1. [方向1]: [描述]
2. [方向2]: [描述]
3. [方向3]: [描述]

// VISUAL
Two-column: Left=Limitations, Right=Future Work

// LAYOUT
Layout: two-columns
```

---

## IMAGE_SOURCE 规则

### 自动映射规则

| 图表类型 | 映射到 Section | Source |
|---------|---------------|--------|
| Architecture/Pipeline | 4-Method | `extract` |
| Main Results Table | 6-实验分析 | `extract` |
| Ablation Table | 6-实验分析 | `extract` |
| Qualitative Comparison | 6-实验分析 | `extract` |
| Training Curves | 5-实现细节 | `extract` |
| Conceptual Illustration | 2-核心故事 | `generate` |
| Related Work Diagram | 3-相关工作 | `generate` |

### IMAGE_SOURCE Format

```markdown
// IMAGE_SOURCE
Source: extract | generate
Figure: Figure 2 | Table 1
Page: 4
Caption: [原始图注]
```

---

## Depth Level 幻灯片分配

| Section | Quick (8-10) | Standard (12-18) | Detailed (20-28) |
|---------|--------------|------------------|------------------|
| 1. TLDR | 1 | 1 | 1 |
| 2. 核心故事 | 1 | 2-3 | 3-4 |
| 3. 相关工作 | 1 | 1-2 | 2 |
| 4. Method | 2 | 3-5 | 5-7 |
| 5. 实现细节 | 1 | 2-3 | 3-4 |
| 6. 实验分析 | 1-2 | 2-4 | 4-6 |
| 7. 总结展望 | 1 | 1-2 | 2 |

---

## STYLE_INSTRUCTIONS Template

```markdown
<STYLE_INSTRUCTIONS>
Design Aesthetic: Clean academic presentation style with emphasis on clarity, information hierarchy, and technical precision.

Background:
  Color: White (#FFFFFF)
  Texture: Subtle grid or clean white

Typography:
  Primary Font: Bold sans-serif for headlines (similar to Inter Bold)
  Secondary Font: Regular sans-serif for body (similar to Inter Regular)
  Code Font: Monospace for code/equations (similar to JetBrains Mono)

Color Palette:
  Primary Text: Dark Blue (#1C2833) - headlines, emphasis
  Body Text: Dark Gray (#2C3E50) - body text
  Background: White (#FFFFFF) - slide background
  Accent 1: Royal Blue (#2E86AB) - highlights, links
  Accent 2: Coral (#E85D75) - important callouts, warnings
  Accent 3: Green (#27AE60) - positive results, checkmarks
  Accent 4: Orange (#F39C12) - neutral highlights
  Table Header: Light Blue (#EBF5FB) - table header background
  Table Alt Row: Light Gray (#F8F9F9) - alternating row background

Visual Elements:
  - Diagrams: Clean lines, consistent arrow styles, labeled components
  - Tables: Alternating rows, header row highlighted, best values bold
  - Charts: Minimal gridlines, direct labels, clear legends
  - Code blocks: Rounded corners, syntax highlighting
  - Icons: Simple line icons, consistent stroke width

Style Rules:
  Do:
    - Use clear visual hierarchy (headline > subheadline > body)
    - Highlight key numbers and results with accent colors
    - Keep slides uncluttered with ample whitespace
    - Use consistent spacing and alignment
    - Show comparisons side-by-side when possible

  Don't:
    - Overcrowd slides with too much text
    - Use decorative elements that don't convey information
    - Mix too many colors (stick to the palette)
    - Use small font sizes that are hard to read
    - Add unnecessary animations or effects
</STYLE_INSTRUCTIONS>
```
