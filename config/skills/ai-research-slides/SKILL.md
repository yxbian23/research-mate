---
name: ai-research-slides
description: 为 AI 研究论文生成专业的分析演示文稿。按照标准化的学术分析框架，从 TLDR 到 Limitation 全面解读论文。适用于论文阅读汇报、组会分享、研究讨论等场景。
---

# AI Research Paper Slide Generator

将 AI 研究论文转换为结构化的分析演示文稿，专为深度理解和分享设计。

## Usage

```bash
/ai-research-slides path/to/paper.pdf
/ai-research-slides path/to/paper.pdf --lang zh
/ai-research-slides path/to/paper.pdf --style academic-paper
/ai-research-slides path/to/paper.pdf --depth detailed
/ai-research-slides path/to/paper.pdf --outline-only
```

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/generate-slides.py` | Generate AI slides via Gemini API (Python) |
| `scripts/merge-to-pptx.ts` | Merge slides into PowerPoint |
| `scripts/merge-to-pdf.ts` | Merge slides into PDF |
| `scripts/detect-figures.ts` | Auto-detect figures/tables in PDF |
| `scripts/extract-figure.ts` | Extract figure from PDF page |
| `scripts/apply-template.ts` | Apply figure container template |

## Options

| Option | Description |
|--------|-------------|
| `--style <name>` | Visual style (default: `academic-paper`) |
| `--lang <code>` | Output language: `zh` (中文), `en` (English) |
| `--depth <level>` | Analysis depth: `quick` (快速), `standard` (标准), `detailed` (详细) |
| `--outline-only` | Generate outline only, skip image generation |

## 标准分析框架 (7 Sections)

每份 AI 研究论文分析按以下 **7 个核心部分** 组织：

### Section 1: TLDR (1 slide)
**目标**：一句话总结论文核心

| 要素 | 说明 |
|------|------|
| 问题 | 论文要解决什么问题？ |
| 方法 | 用什么方法解决？ |
| 结果 | 取得了什么效果？ |
| 格式 | 一句话，不超过 50 字 |

**Layout**: `title-hero` 或 `key-stat`

---

### Section 2: 核心故事与贡献 (2-3 slides)
**目标**：讲清楚论文的核心故事线

| Slide | 内容 |
|-------|------|
| 2a: 问题与动机 | 为什么这个问题重要？现有方法有什么不足？ |
| 2b: 核心洞察 | 论文的关键 insight 是什么？为什么这个 idea 能 work？ |
| 2c: 主要贡献 | 明确列出 2-4 个贡献点（technical contribution, empirical contribution, etc.） |

**Layout**: `split-screen`, `contributions`, `bullet-list`

---

### Section 3: 相关工作与区别 (1-2 slides)
**目标**：定位论文在研究领域中的位置

| 要素 | 说明 |
|------|------|
| 领域分类 | 相关工作属于哪几个方向？ |
| 代表工作 | 每个方向 2-3 个代表性工作 |
| 关键区别 | 本工作与 prior work 的核心区别是什么？ |
| 创新点 | 本工作填补了什么 gap？ |

**Layout**: `comparison-matrix`, `hub-spoke`, `binary-comparison`

---

### Section 4: Method 方法详解 (3-5 slides)
**目标**：清晰呈现技术方案

| Slide | 内容 |
|-------|------|
| 4a: 整体框架 | Pipeline/Architecture 总览图 |
| 4b-4d: 核心模块 | 每个关键模块的详细设计 |
| 4e: 数据流程 | 数据处理、格式、制作流程 |

**重点关注**：
- 模型输入输出格式
- Loss function 设计
- 核心算法伪代码（如有）
- 数据处理 pipeline

**Layout**: `methods-diagram`, `linear-progression`, `hierarchical-layers`

**IMAGE_SOURCE**: 优先从论文提取架构图 (`Source: extract`)

---

### Section 5: 实现细节 (2-3 slides)
**目标**：提供可复现的技术细节

| Slide | 内容 |
|-------|------|
| 5a: 训练配置 | 训练流程、超参数、优化器、学习率策略 |
| 5b: 推理配置 | 推理流程、推理超参数、加速技术 |
| 5c: 数据与规模 | 模型架构参数量、数据集规模、计算资源 |

**必须包含的信息**（如论文提供）：

```
训练配置:
- Optimizer: [AdamW/Adam/SGD]
- Learning Rate: [初始值, schedule]
- Batch Size: [per GPU, total]
- Training Steps/Epochs: [数量]
- GPU/TPU: [型号 × 数量]
- Training Time: [小时/天]

推理配置:
- Inference Steps: [数量]
- Batch Size: [推理批大小]
- Latency: [每样本耗时]

模型规模:
- Total Parameters: [参数量]
- Architecture: [模型架构细节]
- Data Scale: [数据集大小]
```

**Layout**: `dashboard`, `two-columns`, `bento-grid`

---

### Section 6: 实验分析 (3-5 slides)
**目标**：深度分析实验结果

| Slide | 内容 |
|-------|------|
| 6a: 主实验结果 | 与 baseline 的对比，state-of-the-art 性能 |
| 6b: 效果分析 | 为什么本方法更好？定量/定性分析 |
| 6c: 合理性验证 | 实验设置是否合理？评估指标是否恰当？ |
| 6d: 消融实验 | 每个组件的贡献，设计选择的验证 |
| 6e: 失败案例 | 方法在哪些情况下表现不好？ |

**分析要点**：
- 数值对比要标注 **提升幅度**（如 +2.3%）
- 分析结果背后的**原因**，不只是报数
- 关注**边界情况**和**失败案例**

**Layout**: `results-chart`, `qualitative-grid`, `comparison-matrix`

**IMAGE_SOURCE**: 结果表格和对比图优先提取 (`Source: extract`)

---

### Section 7: 总结与展望 (1-2 slides)
**目标**：评价工作质量，指出未来方向

| Slide | 内容 |
|-------|------|
| 7a: 工作总结 | 整体评价：创新性、实用性、完整性 |
| 7b: Limitations & Future Work | 论文的局限性，可能的改进方向 |

**评价维度**：

| 维度 | 考察点 |
|------|--------|
| 创新性 | Idea 的新颖程度，技术贡献 |
| 实用性 | 是否能落地？计算成本如何？ |
| 完整性 | 实验是否充分？消融是否完整？ |
| 可复现性 | 是否开源？细节是否充足？ |
| 写作质量 | 论文是否清晰易懂？ |

**Future Work 分析**：
- 论文自己提到的 limitation
- 你发现的潜在问题
- 可能的改进方向
- 与其他工作结合的机会

**Layout**: `bullet-list`, `two-columns`, `bridge`

---

## Depth Levels

| Level | 中文 | 幻灯片数量 | 适用场景 |
|-------|------|-----------|----------|
| `quick` | 快速 | 8-10 slides | 快速过论文，5分钟分享 |
| `standard` | 标准 | 12-18 slides | 组会汇报，15分钟讲解 |
| `detailed` | 详细 | 20-28 slides | 深度分析，30分钟以上 |

### Slide Distribution by Depth

| Section | Quick | Standard | Detailed |
|---------|-------|----------|----------|
| 1. TLDR | 1 | 1 | 1 |
| 2. 核心故事 | 1 | 2-3 | 3 |
| 3. 相关工作 | 1 | 1-2 | 2 |
| 4. Method | 2 | 3-4 | 5 |
| 5. 实现细节 | 1 | 2-3 | 3 |
| 6. 实验分析 | 1-2 | 3-4 | 5 |
| 7. 总结展望 | 1 | 1-2 | 2 |

---

## Workflow

### Step 1: 论文内容提取

1. **保存论文**：将 PDF 保存为 `source-paper.pdf`
2. **提取文本**：
   ```bash
   python -m markitdown source-paper.pdf > paper-content.md
   ```
3. **检测图表**：
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/detect-figures.ts --pdf source-paper.pdf --output figures.json
   ```

### Step 2: 深度内容分析

按照 7 个部分逐一分析论文内容：

**分析清单**：
- [ ] TLDR 一句话总结
- [ ] 问题动机和核心 insight
- [ ] 主要贡献（2-4 点）
- [ ] 相关工作分类和区别
- [ ] 方法框架和核心模块
- [ ] 训练/推理配置信息
- [ ] 主实验结果和消融实验
- [ ] Limitations 和 Future Work

### Step 3: 生成大纲

1. 根据 `--depth` 确定幻灯片数量
2. 按照 7 个部分组织内容
3. 自动填充 `// IMAGE_SOURCE` 元数据
4. 保存为 `outline.md`

### Step 4: 用户确认

**使用 AskUserQuestion 确认**：
- 大纲结构是否合适
- 是否需要调整深度
- 语言偏好（如果未指定）

### Step 5: 图表提取与生成

1. **提取论文图表**（`Source: extract` 的幻灯片）：
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/extract-figure.ts \
     --pdf source-paper.pdf \
     --page <page-number> \
     --output figures/figure-<N>.png
   ```

2. **应用模板**：
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/apply-template.ts \
     --figure figures/figure-<N>.png \
     --title "<slide-headline>" \
     --caption "Figure <N>: <caption-text>" \
     --output <NN>-slide-<slug>.png
   ```

### Step 6: AI 生成幻灯片

使用 Gemini API 生成非提取类幻灯片：

```bash
python ${SKILL_DIR}/scripts/generate-slides.py <slide-deck-dir> --model gemini-3-pro-image-preview
```

### Step 7: 合并输出

```bash
npx -y bun ${SKILL_DIR}/scripts/merge-to-pptx.ts <slide-deck-dir>
npx -y bun ${SKILL_DIR}/scripts/merge-to-pdf.ts <slide-deck-dir>
```

---

## Outline Template

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
Design Aesthetic: Clean academic style with emphasis on clarity and information hierarchy

Background:
  Color: White (#FFFFFF)
  Texture: Minimal, clean

Typography:
  Primary Font: Bold sans-serif for headlines
  Secondary Font: Regular sans-serif for body text

Color Palette:
  Primary Text: Dark Blue (#1C2833)
  Background: White (#FFFFFF)
  Accent 1: Royal Blue (#2E86AB) - for highlights and emphasis
  Accent 2: Coral (#E85D75) - for important callouts
  Accent 3: Green (#27AE60) - for positive results

Visual Elements:
  - Clean diagrams with consistent styling
  - Tables with alternating row colors
  - Charts with clear labels and legends
  - Code blocks with monospace font

Style Rules:
  Do: Use clear hierarchy, highlight key numbers, show comparisons
  Don't: Overcrowd slides, use decorative elements, sacrifice clarity for style
</STYLE_INSTRUCTIONS>

---

## Slide 1 of N

**Type**: Cover
**Section**: TLDR
**Filename**: 01-slide-tldr.png

// NARRATIVE GOAL
一句话概括论文的核心贡献

// KEY CONTENT
Headline: [论文标题]
Sub-headline: [一句话 TLDR，包含问题-方法-结果]
Venue: [会议/期刊 年份]
Authors: [作者列表]

// VISUAL
Clean title slide with paper title prominent, TLDR as subtitle

// LAYOUT
Layout: paper-title

---

## Slide 2 of N

**Type**: Content
**Section**: 核心故事
**Filename**: 02-slide-motivation.png

// NARRATIVE GOAL
解释问题的重要性和现有方法的不足

// KEY CONTENT
Headline: 问题与动机
Body:
- [现有方法的局限性1]
- [现有方法的局限性2]
- [为什么这个问题重要]

// VISUAL
Split view: left showing problem/limitations, right showing desired outcome

// LAYOUT
Layout: split-screen

---

[... 继续按照 7 个部分生成 ...]
```

---

## Figure Mapping Rules for AI Papers

| 图表类型 | 映射到 | 提取/生成 |
|---------|--------|----------|
| 模型架构图 | Section 4 (Method) | **Extract** |
| 训练流程图 | Section 5 (实现细节) | **Extract** |
| 主实验表格 | Section 6 (实验分析) | **Extract** |
| 消融实验表格 | Section 6 (实验分析) | **Extract** |
| 定性对比图 | Section 6 (实验分析) | **Extract** |
| 数据示例 | Section 4 (Method) | Extract/Generate |
| 概念示意图 | Section 2 (核心故事) | Generate |
| 相关工作对比 | Section 3 (相关工作) | Generate |

---

## Output Structure

```
slide-deck/{paper-slug}/
├── source-paper.pdf          # 原始论文
├── paper-content.md          # 提取的文本
├── figures.json              # 检测到的图表
├── outline.md                # 最终大纲
├── figures/                  # 提取的图表
│   └── figure-{N}.png
├── prompts/                  # 生成提示词
│   └── {NN}-slide-{name}.md
├── slides/                   # 最终幻灯片
│   └── {NN}-slide-{name}.png
├── {paper-slug}.pptx         # 合并的 PPTX
└── {paper-slug}.pdf          # 合并的 PDF
```

---

## Dependencies

与 `paper-slide-deck` 相同，需要：

- **markitdown**: `pip install "markitdown[pptx]"`
- **google-genai**: `pip install google-genai` (或由脚本自动安装)
- **pptxgenjs**: `npm install -g pptxgenjs`
- **playwright**: `npm install -g playwright`
- **sharp**: `npm install -g sharp`
- **pymupdf**: `pip install pymupdf` (PDF 提取备选)

**API Key**: 需要设置 `GOOGLE_API_KEY` 或 `GEMINI_API_KEY` 环境变量

---

## Example Output Summary

```
AI Research Paper Analysis Complete!

Paper: [论文标题]
Venue: [NeurIPS 2024]
Depth: standard
Language: zh
Location: slide-deck/paper-slug/

Slides: 15 total
- 01-slide-tldr.png ✓ TLDR
- 02-slide-motivation.png ✓ 核心故事
- 03-slide-insight.png ✓ 核心故事
- 04-slide-contributions.png ✓ 核心故事
- 05-slide-related-work.png ✓ 相关工作
- 06-slide-method-overview.png ✓ Method (extracted)
- 07-slide-module-a.png ✓ Method
- 08-slide-module-b.png ✓ Method
- 09-slide-training.png ✓ 实现细节
- 10-slide-inference.png ✓ 实现细节
- 11-slide-main-results.png ✓ 实验分析 (extracted)
- 12-slide-analysis.png ✓ 实验分析
- 13-slide-ablation.png ✓ 实验分析 (extracted)
- 14-slide-summary.png ✓ 总结展望
- 15-slide-limitations.png ✓ 总结展望

Outline: outline.md
PPTX: paper-slug.pptx
PDF: paper-slug.pdf
```

---

## Notes

### AI 研究论文分析要点

1. **关注可复现性**：训练配置、超参数、数据处理细节
2. **批判性分析**：不只是复述，要有自己的评价
3. **对比视角**：始终与相关工作对比
4. **实用价值**：这个方法能不能用？成本如何？
5. **未来方向**：不只是论文说的，还有你想到的

### 常见 AI 领域特定内容

| 领域 | 特别关注点 |
|------|-----------|
| LLM | Tokenizer, Context length, Scaling law |
| Vision | 分辨率, 数据增强, Backbone |
| Multimodal | 模态对齐, 跨模态交互 |
| RL | Reward design, Environment setup |
| Diffusion | Noise schedule, Sampling steps |
| GAN | Discriminator design, Training stability |
