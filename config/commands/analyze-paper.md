---
description: 深度分析 AI 研究论文，支持多种来源（PDF、arXiv、项目主页、公众号、HTML 等），输出结构化 Markdown 分析报告。
---

# Analyze Paper Command

对 AI 研究论文进行深度分析，按照标准化的 7 部分学术分析框架输出结构化 Markdown 报告。

## 支持的输入格式

| 格式 | 示例 | 处理方式 |
|------|------|---------|
| **arXiv URL** | `https://arxiv.org/abs/2401.00001` | WebFetch 获取页面 + 下载 PDF |
| **arXiv PDF** | `https://arxiv.org/pdf/2401.00001.pdf` | 直接下载并解析 PDF |
| **本地 PDF** | `/path/to/paper.pdf` | Read tool 读取 PDF |
| **项目主页** | `https://project-page.github.io/` | WebFetch 抓取页面内容 |
| **GitHub Repo** | `https://github.com/org/repo` | WebFetch + 读取 README |
| **公众号文章** | 微信公众号链接 | WebFetch 抓取文章内容 |
| **HTML 页面** | 任意 HTML URL | WebFetch 抓取并解析 |
| **Markdown 文件** | `/path/to/notes.md` | Read tool 读取 |

## 使用方式

```bash
# arXiv 论文
/analyze-paper https://arxiv.org/abs/2401.00001

# 本地 PDF
/analyze-paper /path/to/paper.pdf

# 项目主页
/analyze-paper https://omnivideo.github.io/

# 指定深度
/analyze-paper <source> --depth detailed

# 指定语言
/analyze-paper <source> --lang zh

# 同时分析多个来源（论文+项目主页+代码）
/analyze-paper <pdf> --with <project_page> --with <github_repo>
```

## 参数选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--depth` | 分析深度: `quick` / `standard` / `detailed` | `standard` |
| `--lang` | 输出语言: `zh` (中文) / `en` (English) | `zh` |
| `--with` | 补充来源（可多次使用） | - |
| `--focus` | 重点关注: `method` / `experiment` / `reproduce` | 全面分析 |

---

## 分析框架（7 个核心部分）

### Part 1: TLDR（一句话总结）

**目标**: 用一句话概括论文核心

**输出格式**:
```markdown
## TLDR

**[论文标题]** ([会议/期刊 年份])

> 一句话总结：[问题] + [方法] + [结果]，不超过 50 字

**关键词**: `keyword1`, `keyword2`, `keyword3`
```

**分析要点**:
- 论文要解决什么问题？
- 用什么方法解决？
- 取得了什么效果？

---

### Part 2: 核心故事与贡献

**目标**: 讲清楚论文的核心故事线

**输出格式**:
```markdown
## 核心故事与贡献

### 2.1 问题与动机
- 为什么这个问题重要？
- 现有方法有什么不足？
- 这个问题的挑战是什么？

### 2.2 核心洞察 (Key Insight)
- 论文的关键 insight 是什么？
- 为什么这个 idea 能 work？
- 与之前方法的本质区别？

### 2.3 主要贡献
1. **[贡献1类型]**: [具体描述]
2. **[贡献2类型]**: [具体描述]
3. **[贡献3类型]**: [具体描述]

> 贡献类型: Technical Contribution / Empirical Contribution / Theoretical Contribution / Dataset/Benchmark / System/Tool
```

---

### Part 3: 相关工作与定位

**目标**: 定位论文在研究领域中的位置

**输出格式**:
```markdown
## 相关工作与定位

### 3.1 领域分类
| 方向 | 代表工作 | 主要思路 |
|------|---------|---------|
| [方向1] | Work A, Work B | [简述] |
| [方向2] | Work C, Work D | [简述] |

### 3.2 与 Prior Work 的关键区别

| 对比维度 | 本工作 | Prior Work |
|---------|--------|-----------|
| [维度1] | [本文做法] | [之前做法] |
| [维度2] | [本文做法] | [之前做法] |

### 3.3 本工作填补的 Gap
- [Gap 1]
- [Gap 2]
```

---

### Part 4: 方法详解 (Method)

**目标**: 清晰呈现技术方案

**输出格式**:
```markdown
## 方法详解

### 4.1 整体框架
```
[Pipeline/Architecture 文字描述或 ASCII 图]
Input → Module A → Module B → Output
```

### 4.2 核心模块

#### Module A: [名称]
- **功能**: [做什么]
- **输入/输出**: [格式和维度]
- **关键设计**: [技术细节]

#### Module B: [名称]
...

### 4.3 关键公式

**[公式名称]** (Equation X):
$$
[LaTeX 公式]
$$
- 含义: [公式含义解释]
- 实现要点: [代码实现时的注意事项]

### 4.4 Loss Function
$$
\mathcal{L} = \mathcal{L}_1 + \lambda \mathcal{L}_2
$$
- $\mathcal{L}_1$: [含义]
- $\mathcal{L}_2$: [含义]
- $\lambda$: [取值和作用]

### 4.5 数据流程
1. 数据预处理: [描述]
2. 训练数据格式: [描述]
3. 数据增强: [如有]
```

---

### Part 5: 实现细节

**目标**: 提供可复现的技术细节

**输出格式**:
```markdown
## 实现细节

### 5.1 模型配置

| 配置项 | 值 |
|--------|-----|
| 模型架构 | [架构名称] |
| 参数量 | [X]B / [X]M |
| Hidden Dim | [值] |
| Layers | [值] |
| Heads | [值] |

### 5.2 训练配置

| 配置项 | 值 |
|--------|-----|
| Optimizer | [AdamW/Adam/SGD] |
| Learning Rate | [值] + [schedule] |
| Batch Size | [per GPU] × [GPUs] = [total] |
| Training Steps | [值] |
| Warmup | [值] |
| Weight Decay | [值] |
| Gradient Clipping | [值] |
| Mixed Precision | [bf16/fp16/fp32] |

### 5.3 计算资源

| 资源 | 配置 |
|------|------|
| GPU 型号 | [型号] × [数量] |
| 训练时间 | [时间] |
| 显存占用 | [值] GB/GPU |

### 5.4 推理配置

| 配置项 | 值 |
|--------|-----|
| Inference Steps | [值] |
| Batch Size | [值] |
| Latency | [值] ms/sample |

### 5.5 数据集

| 数据集 | 规模 | 用途 |
|--------|------|------|
| [Dataset A] | [规模] | 训练 |
| [Dataset B] | [规模] | 评估 |
```

---

### Part 6: 实验分析

**目标**: 深度分析实验结果

**输出格式**:
```markdown
## 实验分析

### 6.1 主实验结果

| Method | Metric1 | Metric2 | Metric3 |
|--------|---------|---------|---------|
| Baseline A | X.XX | X.XX | X.XX |
| Baseline B | X.XX | X.XX | X.XX |
| **Ours** | **X.XX** (+Y.Y%) | **X.XX** (+Y.Y%) | **X.XX** |

**结果分析**:
- [为什么本方法更好？]
- [在哪些指标上提升最大？为什么？]

### 6.2 消融实验

| 配置 | Metric | 结论 |
|------|--------|------|
| w/o Component A | X.XX (↓Y.Y) | [Component A 的作用] |
| w/o Component B | X.XX (↓Y.Y) | [Component B 的作用] |
| Full Model | X.XX | - |

**关键发现**:
- [哪个组件贡献最大？]
- [设计选择的验证结论]

### 6.3 定性分析
- **成功案例**: [描述]
- **失败案例**: [描述]
- **边界情况**: [描述]

### 6.4 实验设置合理性评估
- [ ] Baseline 选择是否合理？
- [ ] 评估指标是否恰当？
- [ ] 数据集是否有代表性？
- [ ] 统计显著性是否充分？
```

---

### Part 7: 总结与展望

**目标**: 评价工作质量，指出未来方向

**输出格式**:
```markdown
## 总结与展望

### 7.1 工作评价

| 维度 | 评分 | 说明 |
|------|------|------|
| 创新性 | ⭐⭐⭐⭐☆ | [评价] |
| 实用性 | ⭐⭐⭐☆☆ | [评价] |
| 完整性 | ⭐⭐⭐⭐☆ | [评价] |
| 可复现性 | ⭐⭐⭐⭐⭐ | [评价] |
| 写作质量 | ⭐⭐⭐⭐☆ | [评价] |

### 7.2 Limitations（论文提到的）
1. [Limitation 1]
2. [Limitation 2]

### 7.3 Limitations（我发现的）
1. [额外发现的问题 1]
2. [额外发现的问题 2]

### 7.4 Future Work 方向
1. **[方向1]**: [描述]
2. **[方向2]**: [描述]
3. **[方向3]**: [描述]

### 7.5 可复现性资源

| 资源 | 状态 | 链接 |
|------|------|------|
| 官方代码 | ✅/❌ | [link] |
| 预训练模型 | ✅/❌ | [link] |
| 数据集 | ✅/❌ | [link] |
| Demo | ✅/❌ | [link] |
```

---

## 深度级别

| 深度 | 描述 | 输出长度 | 适用场景 |
|------|------|---------|---------|
| `quick` | 快速过论文 | ~500 字 | 初筛论文、快速了解 |
| `standard` | 标准分析 | ~1500 字 | 组会分享、论文阅读 |
| `detailed` | 深度分析 | ~3000 字 | 论文复现、深入研究 |

### 各深度的内容覆盖

| Part | Quick | Standard | Detailed |
|------|-------|----------|----------|
| 1. TLDR | ✅ 完整 | ✅ 完整 | ✅ 完整 |
| 2. 核心故事 | 简要 | ✅ 完整 | ✅ 完整 + 深入 |
| 3. 相关工作 | 略 | 简要 | ✅ 完整 |
| 4. 方法详解 | 框架only | 核心模块 | ✅ 全部细节 + 公式 |
| 5. 实现细节 | 略 | 关键配置 | ✅ 全部配置 |
| 6. 实验分析 | 主结果 | 主结果+消融 | ✅ 完整 + 批判分析 |
| 7. 总结展望 | 一句话 | 评价+限制 | ✅ 完整 + 未来方向 |

---

## 输入处理流程

### 1. arXiv 链接
```
输入: https://arxiv.org/abs/2401.00001
处理:
1. WebFetch 获取 arXiv 页面 → 提取标题、作者、摘要
2. 构造 PDF URL: https://arxiv.org/pdf/2401.00001.pdf
3. 下载并用 Read tool 解析 PDF
4. 提取 GitHub 链接（如有）
```

### 2. 项目主页
```
输入: https://project.github.io/
处理:
1. WebFetch 抓取主页内容
2. 提取: 标题、方法描述、示例、链接
3. 查找并下载相关 PDF（如有）
4. 查找 GitHub 代码链接
```

### 3. 公众号文章
```
输入: 微信公众号 URL
处理:
1. WebFetch 抓取文章内容
2. 提取: 标题、正文、图片描述
3. 识别原始论文链接（如有）
4. 补充获取原始论文
```

### 4. GitHub Repo
```
输入: https://github.com/org/repo
处理:
1. WebFetch 获取 README
2. 提取: 项目描述、安装方法、使用示例
3. 查找论文链接
4. 分析代码结构（如需要）
```

### 5. HTML 页面
```
输入: 任意 URL
处理:
1. WebFetch 抓取页面
2. 提取主要文本内容
3. 识别论文/代码链接
4. 必要时补充获取原始资料
```

---

## 示例输出

```markdown
# 论文分析报告

**生成时间**: 2024-01-15 14:30
**分析深度**: standard
**来源**: https://arxiv.org/abs/2401.00001

---

## TLDR

**OmniVideo: Unified Video Understanding and Generation** (CVPR 2024)

> 一句话总结：提出统一的视频理解与生成框架，通过共享 Transformer 架构同时处理视频问答和视频生成任务，在两类任务上都达到 SOTA。

**关键词**: `Video Generation`, `Video Understanding`, `Unified Model`, `Transformer`

---

## 核心故事与贡献

### 2.1 问题与动机
- 现有视频模型通常分别处理理解和生成任务
- 分离的模型无法共享视觉表征，效率低下
- 人类对视频的理解和想象是统一的过程

### 2.2 核心洞察 (Key Insight)
- 视频理解和生成本质上都是序列建模问题
- 通过统一的 token 表示，可以用同一模型处理两类任务
- 关键是设计合适的 visual tokenizer 和训练策略

### 2.3 主要贡献
1. **Technical Contribution**: 提出 OmniVideo 统一框架
2. **Technical Contribution**: 设计高效的视频 tokenizer
3. **Empirical Contribution**: 在 5 个 benchmark 上达到 SOTA

---

[... 后续 Parts 省略 ...]
```

---

## 多来源分析

当使用 `--with` 提供多个来源时：

```bash
/analyze-paper paper.pdf --with https://project.github.io/ --with https://github.com/org/repo
```

**处理策略**:
1. 主来源 (PDF) 作为核心分析对象
2. 项目主页补充：Demo、可视化结果、简化说明
3. GitHub 补充：实际实现细节、issue 中的已知问题

**输出中会标注信息来源**:
```markdown
### 5.2 训练配置
| 配置项 | 值 | 来源 |
|--------|-----|------|
| Batch Size | 32 | 论文 Table 3 |
| Learning Rate | 1e-4 | GitHub README |
| Warmup Steps | 1000 | 代码 config.yaml |
```

---

## Related Commands

- `/implement-paper` - 分析后开始实现
- `/train` - 训练实现的模型
- `/benchmark` - 评估复现结果

## Related Skills

- `paper-slide-deck/` - 生成论文 slides
- `ai-research-slides/` - AI 论文专用 slides
- `research-paper-workflow/` - 论文写作工作流
