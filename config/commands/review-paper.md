---
description: 生成符合 AI 顶会标准的论文审稿意见（ICLR/ICML/NeurIPS/CVPR/ECCV/ICCV），遵循 OpenReview 格式，语言自然专业。
---

# Review Paper Command

为 AI 顶会论文生成专业、严谨的审稿意见，遵循 OpenReview 标准格式。

**重要声明**: 本工具仅用于辅助审稿人组织思路和撰写意见，最终审稿意见必须基于审稿人的独立判断。严禁直接提交 AI 生成的审稿意见。

## 支持的会议

| 会议 | 领域 | 审稿周期 | 格式特点 |
|------|------|---------|---------|
| **ICLR** | 表示学习/深度学习 | 9-10月 | OpenReview, 公开讨论 |
| **ICML** | 机器学习理论与应用 | 1-2月 | OpenReview, 双盲 |
| **NeurIPS** | 神经信息处理 | 5-6月 | OpenReview, 双盲 |
| **CVPR** | 计算机视觉 | 11月 | CMT/OpenReview, 双盲 |
| **ECCV** | 计算机视觉(欧洲) | 3月 | CMT, 双盲 |
| **ICCV** | 计算机视觉 | 3月 | CMT, 双盲 |

## 使用方式

```bash
# 基本用法
/review-paper <paper_source>

# 指定会议
/review-paper <paper_source> --venue ICLR

# 指定审稿风格
/review-paper <paper_source> --style constructive

# 指定语言
/review-paper <paper_source> --lang en

# 保存到文件
/review-paper <paper_source> --output review.md
```

## 参数选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--venue` | 目标会议: `ICLR`/`ICML`/`NeurIPS`/`CVPR`/`ECCV`/`ICCV` | 自动推断 |
| `--style` | 审稿风格: `constructive`/`critical`/`balanced` | `balanced` |
| `--lang` | 输出语言: `en`/`zh` | `en` |
| `--focus` | 重点关注: `novelty`/`soundness`/`presentation`/`all` | `all` |
| `--output` | 输出文件路径 | 直接输出 |

---

## 审稿框架（OpenReview 标准格式）

### 1. Summary（论文摘要）

**目标**: 用自己的话概括论文的主要内容

**写作要点**:
- 3-5 句话，约 100-150 词
- 包含：问题定义、方法概述、主要结果
- 客观描述，不加评价
- 展示你理解了论文

**语言风格**:
```
✓ "This paper proposes..."
✓ "The authors present..."
✓ "The main contribution is..."
✗ "This amazing paper..." (过于主观)
✗ "The authors claim..." (暗示不信任)
```

---

### 2. Strengths（优点）

**目标**: 指出论文的积极方面

**评估维度**:

| 维度 | 考察点 | 常用表达 |
|------|--------|---------|
| **Novelty** | 想法新颖程度 | "novel approach", "fresh perspective", "interesting idea" |
| **Technical** | 方法正确性 | "technically sound", "well-motivated", "principled" |
| **Empirical** | 实验充分性 | "comprehensive experiments", "strong baselines", "convincing results" |
| **Clarity** | 写作清晰度 | "well-written", "clearly presented", "easy to follow" |
| **Impact** | 潜在影响力 | "significant contribution", "practical value", "inspiring" |

**写作要点**:
- 每个优点独立成段，用 bullet point
- 具体而非笼统，引用论文具体内容
- 3-5 个优点为宜
- 强优点放前面

**示例**:
```markdown
**Strengths:**

- **Novel problem formulation.** The authors identify an important gap in existing literature
  regarding [specific problem]. To my knowledge, this is the first work to [specific contribution].

- **Solid experimental design.** The experiments cover a wide range of settings, including
  [datasets/baselines]. The ablation study in Table 3 effectively isolates the contribution
  of each component.

- **Clear presentation.** The paper is well-organized and easy to follow. Figure 2 provides
  a helpful overview of the proposed method.
```

---

### 3. Weaknesses（缺点）

**目标**: 指出论文的不足之处

**评估维度**:

| 维度 | 典型问题 | 常用表达 |
|------|---------|---------|
| **Novelty** | 增量式改进、方法已有 | "incremental", "similar to prior work", "limited novelty" |
| **Technical** | 证明缺失、假设过强 | "missing proof", "strong assumptions", "potential flaw" |
| **Empirical** | baseline 弱、数据集小 | "weak baselines", "limited datasets", "missing comparisons" |
| **Clarity** | 描述模糊、符号混乱 | "unclear", "confusing notation", "missing details" |
| **Significance** | 影响有限、应用场景窄 | "limited scope", "narrow application", "unclear significance" |

**写作要点**:
- 每个缺点独立成段
- **必须具体**，指出具体问题在哪里
- 尽量提供**建设性建议**
- 区分 major 和 minor issues
- 语气委婉但明确

**示例**:
```markdown
**Weaknesses:**

- **Limited novelty over [Prior Work].** The proposed method shares significant similarities
  with [citation]. While the authors mention this in Section 2, the technical differences
  (mainly [specific difference]) seem incremental. It would help to have a more detailed
  comparison, ideally with empirical results on the same benchmarks.

- **Incomplete ablation study.** The ablation in Table 3 removes components individually,
  but does not explore the interaction between [Component A] and [Component B]. Given that
  both components affect [specific aspect], their combined effect is unclear.

- **Missing important baseline.** The recent work by [Author et al., 2024] addresses a very
  similar problem but is not compared. Given its relevance, this comparison would strengthen
  the empirical evaluation.
```

---

### 4. Questions（问题）

**目标**: 向作者提出需要澄清的问题

**问题类型**:

| 类型 | 目的 | 示例 |
|------|------|------|
| **Clarification** | 理解不清的地方 | "Could you clarify how [X] is computed?" |
| **Justification** | 设计选择的原因 | "Why did you choose [X] over [Y]?" |
| **Extension** | 方法的扩展性 | "Have you considered applying this to [Z]?" |
| **Concern** | 潜在问题 | "What happens when [condition]?" |

**写作要点**:
- 问题要具体，可回答
- 不要用问题暗示批评（应放在 Weaknesses）
- 5-10 个问题为宜
- 标注问题的重要程度（如果系统支持）

**示例**:
```markdown
**Questions:**

1. In Equation (3), how is the expectation approximated in practice? Is Monte Carlo sampling
   used, and if so, how many samples?

2. The paper mentions that the method works best with [specific condition]. What happens
   when this condition is violated? Have you tested on such cases?

3. Table 2 shows results on [Dataset A], but this dataset is relatively small. Would the
   conclusions hold on larger-scale benchmarks like [Dataset B]?

4. Minor: In Figure 3, the y-axis label is missing. Could you clarify what metric is shown?
```

---

### 5. Limitations（局限性评估）

**目标**: 评估作者对局限性的讨论

**评估要点**:
- 作者是否诚实地讨论了局限性？
- 是否遗漏了重要的局限性？
- 局限性是否可在未来工作中解决？

**示例**:
```markdown
**Limitations:**

The authors acknowledge that their method requires [specific resource/condition], which
limits its applicability to [scenario]. However, I believe there are additional limitations
not discussed:

- The computational cost (Section 4.2) seems prohibitive for real-time applications.
- The method assumes [assumption], which may not hold in [practical scenario].
```

---

### 6. Ethical Concerns（伦理考量）

**目标**: 评估潜在的伦理问题

**考量维度**:
- 数据集是否涉及隐私/偏见
- 方法是否可能被滥用
- 是否有潜在的负面社会影响

**示例**:
```markdown
**Ethics:**

No significant ethical concerns. The datasets used are publicly available and do not
contain personally identifiable information. The authors include a discussion of potential
misuse in the appendix.
```

---

### 7. Overall Assessment & Rating

**评分标准**（以 ICLR 为例）:

| 分数 | 含义 | 对应情况 |
|------|------|---------|
| **10** | Top 5% | 突破性工作，必须接收 |
| **8** | Top 15% | 强接收，优秀工作 |
| **6** | Top 35% | 弱接收，略高于门槛 |
| **5** | Top 50% | 边缘，可接收可拒绝 |
| **3** | Bottom 35% | 弱拒绝，低于门槛 |
| **1** | Bottom 15% | 强拒绝，明显问题 |

**Confidence 评分**:

| 分数 | 含义 |
|------|------|
| **5** | 非常熟悉该领域，仔细阅读了论文 |
| **4** | 熟悉该领域，理解论文大部分内容 |
| **3** | 有一定了解，但某些部分不确定 |
| **2** | 不太熟悉，评估可能有偏差 |
| **1** | 几乎不了解该领域 |

**示例**:
```markdown
**Overall:**

This paper presents an interesting approach to [problem]. The main strength lies in
[key strength], while the main concern is [key weakness]. If the authors can address
[specific issue] in the rebuttal, I would be willing to raise my score.

**Rating:** 5 (marginally below acceptance threshold)

**Confidence:** 4 (I am confident but not absolutely certain)
```

---

## 语言风格指南

### DO（推荐）

```
✓ "The paper presents..." (客观)
✓ "I appreciate the authors' effort in..." (有礼貌的肯定)
✓ "One concern I have is..." (委婉的批评)
✓ "It would be helpful if..." (建设性建议)
✓ "I may have missed something, but..." (谦虚的质疑)
✓ "To my knowledge..." (承认可能的局限)
✓ "The experimental results suggest..." (基于证据)
```

### DON'T（避免）

```
✗ "This paper is amazing/terrible" (过于主观)
✗ "The authors fail to..." (攻击性语言)
✗ "Obviously, this is wrong" (傲慢)
✗ "I don't understand why..." (暗示作者问题)
✗ "This should be rejected because..." (结论式判断)
✗ "Everyone knows that..." (假设共识)
✗ "trivial", "naive", "useless" (贬低性词汇)
```

### 自然表达模式

**表达不确定性**:
- "I'm not entirely sure, but it seems like..."
- "Correct me if I'm wrong, but..."
- "Unless I'm missing something..."

**提出批评**:
- "One aspect that could be improved is..."
- "I wonder if the authors have considered..."
- "A potential issue is..."

**给予肯定**:
- "I found the approach quite interesting because..."
- "The experiments are thorough, particularly..."
- "This is a nice contribution to..."

---

## 审稿伦理准则

### 必须遵守

1. **诚实**: 所有评价必须基于论文内容，不能编造问题
2. **建设性**: 批评应附带改进建议
3. **尊重**: 使用专业、尊重的语言
4. **保密**: 不泄露审稿内容和作者信息
5. **公正**: 不因作者身份、机构、国籍产生偏见

### 禁止行为

1. ❌ 编造论文中不存在的问题
2. ❌ 使用攻击性或贬低性语言
3. ❌ 因为与自己工作竞争而打低分
4. ❌ 抄袭其他审稿人的意见
5. ❌ 直接提交 AI 生成的审稿意见（必须经过人工审核和修改）

---

## 输出格式模板

```markdown
## Summary

[3-5 句话概括论文]

## Strengths

- **[Strength 1 标题]**: [具体描述]
- **[Strength 2 标题]**: [具体描述]
- **[Strength 3 标题]**: [具体描述]

## Weaknesses

- **[Weakness 1 标题]**: [具体描述 + 建议]
- **[Weakness 2 标题]**: [具体描述 + 建议]
- **[Weakness 3 标题]**: [具体描述 + 建议]

## Questions

1. [Question 1]
2. [Question 2]
3. [Question 3]

## Limitations

[对局限性讨论的评估]

## Ethics

[伦理考量，如无问题则简述]

## Overall

[总体评价，1-2 段]

---

**Rating:** [1-10]
**Confidence:** [1-5]
```

---

## 使用示例

```bash
# 审稿一篇 ICLR 投稿
/review-paper paper.pdf --venue ICLR --style balanced

# 输出 (示例):

## Summary

This paper proposes Video-As-Prompt (VAP), a unified framework for semantic-controlled
video generation. Unlike prior work that relies on pixel-level control signals, VAP
treats reference videos as in-context prompts, enabling zero-shot generalization across
diverse semantic conditions including concept transfer, style adaptation, motion guidance,
and camera control. The authors introduce a Mixture-of-Transformers architecture and
construct VAP-Data, a dataset with 100K+ paired samples.

## Strengths

- **Novel problem formulation.** The idea of using reference videos as semantic prompts,
  rather than pixel-aligned controls, is intuitive and addresses real limitations of
  existing methods. The in-context learning paradigm is well-motivated.

- **Comprehensive experiments.** The evaluation covers multiple baselines including
  commercial models (Kling, Vidu). The user study with 38.7% preference rate against
  commercial models is impressive for an open-source unified model.

- **Useful dataset contribution.** VAP-Data with 100K+ samples across 100 semantic
  conditions fills an important gap. The categorization into concept/style/motion/camera
  is practical.

## Weaknesses

- **Synthetic data limitations.** VAP-Data is generated using commercial models, which
  may introduce biases. The paper acknowledges this but doesn't quantify the impact.
  It would be valuable to include some real-world paired examples for validation.

- **Computational overhead not fully addressed.** The paper mentions ~2x inference time
  but doesn't provide detailed analysis. Memory requirements and training costs could
  be discussed more thoroughly.

- **Limited multi-reference analysis.** The failure case of 3+ reference videos causing
  appearance mixing is mentioned but not deeply analyzed. Understanding this limitation
  better would be helpful.

## Questions

1. How sensitive is the temporal bias Δ in RoPE? Have you experimented with different
   values, and is there an optimal range?

2. Could you provide more details on how the Semantic Alignment metric correlates with
   human judgment? What's the agreement rate?

3. Have you tried applying VAP to longer videos (beyond 49 frames)? Are there specific
   challenges?

## Limitations

The authors provide a reasonable discussion of limitations including synthetic data
dependency and multi-reference issues. One additional limitation not discussed is the
potential difficulty in precise spatial control within the semantic transfer.

## Ethics

No significant concerns. The dataset uses generated content and the paper includes
appropriate discussions of potential misuse.

## Overall

This is a solid contribution that addresses an important problem with a principled
approach. The main strengths are the novel formulation and comprehensive evaluation.
The main weakness is the reliance on synthetic training data. Overall, I lean towards
acceptance but would like to see the authors address the questions above.

---

**Rating:** 6 (marginally above acceptance threshold)
**Confidence:** 4
```

---

## Related

- `/analyze-paper` - 论文深度分析（非审稿）
- `paper-review/` skill - 审稿知识库
- `paper-reviewer` agent - 审稿专家 agent
