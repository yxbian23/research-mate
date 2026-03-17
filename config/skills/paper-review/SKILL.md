---
name: paper-review
description: AI 顶会论文审稿知识库。包含 ICLR/ICML/NeurIPS/CVPR/ECCV/ICCV 的审稿标准、评分体系、常见表达和伦理准则。用于辅助审稿人撰写专业、建设性的审稿意见。
---

# Paper Review Skill

专业论文审稿知识库，辅助审稿人撰写高质量审稿意见。

**重要**: 本 skill 仅用于辅助审稿人组织思路，所有审稿意见必须基于审稿人的独立判断，严禁直接提交 AI 生成内容。

---

## 各会议评分标准

### ICLR (International Conference on Learning Representations)

**Rating Scale (1-10)**:
| Score | Label | 描述 |
|-------|-------|------|
| 10 | Award quality | Top 2%，开创性工作 |
| 8 | Strong Accept | Top 10%，优秀贡献 |
| 6 | Weak Accept | 高于门槛，可以接收 |
| 5 | Borderline | 边缘，优缺点相当 |
| 3 | Weak Reject | 低于门槛，需要改进 |
| 1 | Strong Reject | 明显问题，不适合该会议 |

**Confidence Scale (1-5)**:
| Score | 描述 |
|-------|------|
| 5 | 该领域专家，非常熟悉相关工作 |
| 4 | 熟悉该领域，理解论文细节 |
| 3 | 了解大部分内容，但有些部分不确定 |
| 2 | 对该领域了解有限 |
| 1 | 几乎不了解该领域 |

**特点**: 公开审稿，作者可回复，审稿人需参与讨论

---

### ICML (International Conference on Machine Learning)

**Rating Scale**:
| Score | Label | 描述 |
|-------|-------|------|
| 10 | Top 5% | 必须接收 |
| 9 | Top 15% | 强接收 |
| 7-8 | Top 30% | 接收 |
| 6 | Top 50% | 边缘接收 |
| 5 | Borderline | 边缘拒绝 |
| 4 | Reject | 拒绝 |
| 1-3 | Strong Reject | 强拒 |

**特点**: 双盲审稿，Area Chair 协调

---

### NeurIPS (Neural Information Processing Systems)

**Rating Scale (1-10)**:
| Score | 描述 |
|-------|------|
| 9-10 | Top 2%，突破性工作 |
| 7-8 | Strong Accept，优秀 |
| 6 | Weak Accept，可接收 |
| 5 | Borderline，边缘 |
| 4 | Weak Reject，略低于门槛 |
| 1-3 | Strong Reject，明显问题 |

**特点**:
- 双盲审稿
- 要求 Broader Impact 和 Limitations 章节
- Author response 阶段

---

### CVPR/ICCV/ECCV (计算机视觉顶会)

**Rating Scale (CVPR/ICCV)**:
| Score | Label | 描述 |
|-------|-------|------|
| 5 | Strong Accept | 优秀，应该接收 |
| 4 | Accept | 可以接收 |
| 3 | Borderline | 边缘 |
| 2 | Reject | 应该拒绝 |
| 1 | Strong Reject | 强烈拒绝 |

**ECCV 特点**:
- 使用 CMT 系统
- 两轮审稿 (部分投稿)
- 欧洲时区

---

## 评审维度详解

### 1. Novelty（新颖性）

**评估问题**:
- 核心 idea 是否新颖？
- 与现有工作的区别是否显著？
- 是否仅是现有方法的简单组合？

**等级标准**:
| 等级 | 描述 | 表达方式 |
|------|------|---------|
| 高 | 全新问题定义或方法范式 | "first to...", "novel paradigm", "fundamentally new" |
| 中 | 显著改进现有方法 | "interesting extension", "non-trivial improvement" |
| 低 | 增量式改进 | "incremental", "straightforward extension" |
| 无 | 已有方法 | "essentially the same as", "lacks novelty" |

**常见表达**:
```
高新颖性:
- "This paper introduces a fundamentally new perspective on..."
- "To the best of my knowledge, this is the first work to..."
- "The proposed formulation opens up new research directions."

中等新颖性:
- "While the individual components are known, their combination is novel."
- "The paper provides interesting insights into..."
- "The extension to [new setting] is non-trivial."

低新颖性:
- "The approach is similar to [prior work], with the main difference being..."
- "The contribution seems incremental over [citation]."
- "I'm not convinced the technical novelty is sufficient for [venue]."
```

---

### 2. Technical Soundness（技术正确性）

**评估问题**:
- 方法是否正确？证明是否严谨？
- 假设是否合理？是否明确说明？
- 实验设计是否正确？

**常见问题类型**:
| 问题类型 | 示例 | 严重程度 |
|---------|------|---------|
| 证明错误 | 定理证明有漏洞 | Major |
| 假设过强 | 假设在实际中不成立 | Major |
| 实验设置不当 | 数据泄露、不公平对比 | Major |
| 细节缺失 | 关键参数未说明 | Minor |
| 符号混乱 | 符号定义不一致 | Minor |

**表达方式**:
```
发现问题:
- "I believe there is an issue in the proof of Theorem 1..."
- "The assumption in Section 3.2 seems too strong because..."
- "The experimental setup may have potential data leakage..."

不确定:
- "I may have missed something, but it seems like..."
- "Could the authors clarify how [X] is handled?"
- "Unless I misunderstand, the derivation in Eq. (5) assumes..."
```

---

### 3. Empirical Evaluation（实验评估）

**评估问题**:
- Baseline 是否合理且足够？
- 数据集是否有代表性？
- 消融实验是否充分？
- 结果是否统计显著？

**Baseline 评估标准**:
| 等级 | 描述 |
|------|------|
| 优 | 包含最新 SOTA 方法，公平对比 |
| 良 | 包含主要 baseline，但缺少部分最新工作 |
| 中 | Baseline 较弱或过时 |
| 差 | 明显缺失重要 baseline |

**常见表达**:
```
Baseline 问题:
- "The recent work [X] addresses a very similar problem but is not compared."
- "Some baselines are from 2019, and more recent methods should be included."
- "It would be helpful to compare with [specific method] which is SOTA on [dataset]."

消融不足:
- "The ablation study is incomplete. Specifically, the effect of [X] is not studied."
- "It's unclear which component contributes most to the improvement."

统计显著性:
- "Are the improvements statistically significant? Error bars would be helpful."
- "The variance across runs should be reported."
```

---

### 4. Presentation（论文呈现）

**评估问题**:
- 写作是否清晰流畅？
- 图表是否信息丰富？
- 组织结构是否合理？

**常见表达**:
```
正面:
- "The paper is well-written and easy to follow."
- "Figure 2 provides a clear overview of the method."
- "The notation is consistent throughout."

负面:
- "The paper could benefit from better organization."
- "Some parts are hard to follow, particularly Section 3.2."
- "The notation is inconsistent between Sections 2 and 3."

建议:
- "A figure illustrating the pipeline would help readers understand the method."
- "Consider moving [X] to the appendix to make room for [Y]."
```

---

### 5. Significance（重要性）

**评估问题**:
- 解决的问题是否重要？
- 方法是否有广泛适用性？
- 对领域发展是否有推动作用？

**常见表达**:
```
高重要性:
- "This addresses a fundamental problem in..."
- "The results could have significant impact on [application]."
- "I expect this work to inspire follow-up research."

中等重要性:
- "While the problem is somewhat niche, the solution is elegant."
- "The contribution is solid, though the scope is limited."

低重要性:
- "The practical impact seems limited given [constraint]."
- "It's unclear who would benefit from this method."
```

---

## 自然语言表达库

### 开场白（Summary 开头）

```
✓ "This paper proposes..."
✓ "This work presents..."
✓ "The authors introduce..."
✓ "This submission addresses..."
✓ "The paper tackles the problem of..."

✗ "This amazing paper..." (过于热情)
✗ "The authors claim..." (暗示不信任)
✗ "This paper attempts to..." (暗示失败)
```

### 表达优点

```
强肯定:
- "A key strength of this work is..."
- "I particularly appreciate..."
- "The most compelling aspect is..."
- "This is a significant contribution because..."

中等肯定:
- "The paper does a good job of..."
- "I found [X] to be interesting."
- "The approach is reasonable and well-motivated."

弱肯定:
- "On the positive side,..."
- "One merit of the paper is..."
```

### 表达缺点

```
委婉批评:
- "One area that could be improved is..."
- "A potential concern is..."
- "I have some reservations about..."
- "One aspect that deserves more attention is..."

中等批评:
- "The paper falls short in..."
- "A weakness of the current version is..."
- "I'm not fully convinced that..."

直接批评（仅用于严重问题）:
- "There appears to be an error in..."
- "The experimental setup is flawed because..."
- "This claim is not supported by the evidence."
```

### 表达不确定

```
- "I may have missed something, but..."
- "Unless I misunderstand,..."
- "Correct me if I'm wrong, but..."
- "I'm not entirely sure about [X], so I'd appreciate clarification."
- "This might be addressed in the appendix, but I couldn't find..."
```

### 提出建议

```
- "It would be helpful if..."
- "The paper would benefit from..."
- "I encourage the authors to..."
- "Consider adding..."
- "One way to strengthen the paper is to..."
```

### 评分陈述

```
弱接收:
- "Overall, I lean towards acceptance, but [concern] should be addressed."
- "The contribution is solid, and I'm inclined to accept."
- "Despite some weaknesses, I believe this paper makes a contribution worth publishing."

边缘:
- "I'm on the fence about this paper."
- "The strengths and weaknesses roughly balance out."
- "My assessment could change depending on the authors' response."

弱拒绝:
- "While the paper has merits, the issues outweigh them."
- "In its current form, I cannot recommend acceptance."
- "The paper needs significant revision before it's ready for publication."
```

---

## 避免 AI 检测的写作技巧

### 1. 使用个人化表达

```
✓ "In my experience with similar methods,..."
✓ "When I ran into a similar problem in my own work,..."
✓ "I found myself confused by..."
✓ "Honestly, I'm not sure about..."
```

### 2. 加入具体细节和位置

```
✓ "In Line 235, the notation changes from x to y without explanation."
✓ "Table 3, row 4 shows an unexpected result..."
✓ "The derivation between Eq. (5) and (6) skips several steps."
```

### 3. 使用口语化连接词

```
✓ "That said,..."
✓ "Having said that,..."
✓ "On a related note,..."
✓ "Speaking of which,..."
```

### 4. 表达情感和反应

```
✓ "I was surprised to see..."
✓ "I found it interesting that..."
✓ "This is a bit disappointing because..."
✓ "I'm curious about..."
```

### 5. 承认自己的局限

```
✓ "I'm not an expert in [specific area], so take my comment with a grain of salt."
✓ "I might be wrong here, but..."
✓ "This is outside my main area of expertise, but..."
```

### 6. 不要过于完美

```
✓ 适当使用缩写: "doesn't", "I'd", "won't"
✓ 偶尔用非正式表达: "a bit", "kind of", "sort of"
✓ 避免过于对称的结构
```

---

## 回复 Rebuttal 的技巧

### 当问题被解决

```
"The authors have addressed my concerns regarding [X]. I'm raising my score to [Y]."
"The additional experiments in the rebuttal are convincing. My main concern is resolved."
```

### 当问题部分解决

```
"I appreciate the authors' response. While [X] is addressed, I still have concerns about [Y]."
"The clarification helps, but I'm not fully convinced because..."
```

### 当问题未解决

```
"Unfortunately, the rebuttal does not address my main concern about [X]."
"I appreciate the effort, but the response doesn't change my assessment because..."
```

---

## 伦理检查清单

审稿前确认：
- [ ] 我没有与作者的利益冲突
- [ ] 我有足够的专业知识评审这篇论文
- [ ] 我会保护论文内容的机密性
- [ ] 我会给出建设性的反馈

审稿中确认：
- [ ] 我的所有批评都基于论文内容，没有编造
- [ ] 我使用了专业、尊重的语言
- [ ] 我对所有论文使用了一致的标准
- [ ] 我考虑了论文的优点和缺点

审稿后确认：
- [ ] 我没有泄露论文内容
- [ ] 我参与了 rebuttal 讨论（如需要）
- [ ] 我的最终评分反映了我的诚实判断

---

## References

- [ICLR 2024 Reviewer Guidelines](https://iclr.cc/Conferences/2024/ReviewerGuide)
- [NeurIPS 2024 Reviewer Tutorial](https://neurips.cc/Conferences/2024/ReviewerGuidelines)
- [How to Write Good Reviews (CVPR)](https://cvpr2022.thecvf.com/node/51)
- [The Art of Reviewing (Yoshua Bengio)](https://yoshuabengio.org/2020/02/26/time-to-rethink-the-publication-process-in-machine-learning/)
