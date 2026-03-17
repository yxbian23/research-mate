# AI Research Paper Analysis Framework

专为 AI/ML 研究论文设计的深度分析框架。

## 1. TLDR 分析

### 一句话总结公式

```
[方法名] 通过 [核心技术/洞察] 解决了 [问题]，在 [基准] 上达到了 [结果]。
```

**示例**：
- "GPT-4V 通过统一视觉和语言的 next token prediction 训练，实现了强大的多模态理解能力"
- "DDPM 通过迭代去噪的扩散过程，首次在图像生成质量上超越 GAN"

### TLDR 质量检查

- [ ] 不超过 50 字
- [ ] 包含问题、方法、结果三要素
- [ ] 非专业人士能理解大意
- [ ] 突出了核心创新点

---

## 2. 核心故事分析

### 2.1 问题与动机

| 分析维度 | 问题 |
|---------|------|
| 问题定义 | 论文要解决的具体问题是什么？ |
| 重要性 | 为什么这个问题重要？谁在乎？ |
| 现有局限 | 之前的方法哪里不行？ |
| 差距 (Gap) | 理想状态和现实之间的差距是什么？ |

### 2.2 核心洞察 (Key Insight)

**核心问题**：这篇论文的 "Aha moment" 是什么？

分析角度：
- 技术洞察：发现了什么技术规律或原理？
- 经验洞察：从实验/数据中发现了什么？
- 类比洞察：从其他领域借鉴了什么思路？

**判断标准**：
- 这个 insight 是否 non-trivial？
- 其他人为什么没想到？
- 这个 insight 能否泛化到其他问题？

### 2.3 贡献点分类

| 贡献类型 | 说明 | 示例 |
|---------|------|------|
| Technical | 新的算法、架构、损失函数 | Transformer attention, Diffusion process |
| Empirical | 新的实验发现、benchmark | Scaling laws, Emergent abilities |
| System | 工程系统、优化技术 | FlashAttention, vLLM |
| Dataset | 新数据集、标注 | ImageNet, LAION-5B |
| Application | 新的应用场景 | GPT for code, CLIP for zero-shot |

---

## 3. 相关工作分析

### 3.1 领域定位矩阵

```
                    方法复杂度
                 低 ←——————→ 高
        ↑    |  [简单方法]  |  [复杂方法]  |
效果    |    |  Baseline   |  SOTA       |
        ↓    |  [本工作?]  |  [Prior]    |
```

### 3.2 相关工作分类模板

```markdown
| 方向 | 代表工作 | 核心思路 | 局限性 |
|------|---------|---------|--------|
| 方向A | [Work1, Work2] | [简述] | [为什么不够好] |
| 方向B | [Work3, Work4] | [简述] | [为什么不够好] |
| 方向C | [Work5, Work6] | [简述] | [为什么不够好] |
```

### 3.3 与 Prior Work 对比

**关键区别分析表**：

| 对比维度 | Prior Work | 本工作 | 优势 |
|---------|------------|--------|------|
| 核心方法 | | | |
| 数据需求 | | | |
| 计算成本 | | | |
| 适用范围 | | | |
| 性能表现 | | | |

---

## 4. Method 分析框架

### 4.1 整体框架分析

```
输入 → [模块1] → [模块2] → [模块3] → 输出
         ↓          ↓          ↓
      [Loss1]    [Loss2]    [Loss3]
```

**必答问题**：
- 输入是什么格式？
- 输出是什么格式？
- 有几个主要模块？
- 各模块如何连接？
- 训练目标/Loss 是什么？

### 4.2 核心模块分析模板

对每个关键模块：

```markdown
## 模块名称

**功能**：这个模块做什么？

**输入输出**：
- Input: [格式, 维度]
- Output: [格式, 维度]

**核心设计**：
- [设计决策1]: [原因]
- [设计决策2]: [原因]

**与 Prior Work 的区别**：
- 之前: [旧方法]
- 现在: [新方法]
- 优势: [为什么更好]
```

### 4.3 数据处理流程

```markdown
## 数据 Pipeline

**原始数据**：
- 来源: [数据集名称]
- 规模: [数量]
- 格式: [原始格式]

**预处理步骤**：
1. [步骤1]: [具体操作]
2. [步骤2]: [具体操作]
3. [步骤3]: [具体操作]

**数据增强**：
- [增强方法1]
- [增强方法2]

**最终格式**：
- 训练样本格式: [描述]
- Batch 组织方式: [描述]
```

### 4.4 Loss Function 分析

```markdown
## Loss Design

**总体 Loss**：
L_total = λ1 * L1 + λ2 * L2 + λ3 * L3

**各项 Loss 说明**：

| Loss | 公式 | 作用 | 权重 |
|------|------|------|------|
| L1 | [公式] | [作用] | λ1= |
| L2 | [公式] | [作用] | λ2= |
| L3 | [公式] | [作用] | λ3= |

**设计考量**：
- 为什么选择这些 loss？
- 权重如何确定的？
- 有没有消融证明每个 loss 的必要性？
```

---

## 5. 实现细节清单

### 5.1 训练配置

```markdown
## Training Configuration

| 配置项 | 值 | 备注 |
|-------|------|------|
| **优化器** | | |
| Optimizer | AdamW/Adam/SGD | |
| Learning Rate | | 初始值 |
| LR Schedule | | cosine/linear/constant |
| Weight Decay | | |
| Gradient Clip | | |
| **批次设置** | | |
| Batch Size (per GPU) | | |
| Total Batch Size | | |
| Accumulation Steps | | |
| **训练规模** | | |
| Training Steps | | 或 epochs |
| Warmup Steps | | |
| **硬件** | | |
| GPU Type | | A100/H100/TPU |
| GPU Count | | |
| Training Time | | 小时/天 |
| **其他** | | |
| Mixed Precision | | FP16/BF16 |
| DeepSpeed Stage | | 0/1/2/3 |
| Checkpoint Interval | | |
```

### 5.2 推理配置

```markdown
## Inference Configuration

| 配置项 | 值 | 备注 |
|-------|------|------|
| **基本设置** | | |
| Inference Batch Size | | |
| Inference Steps | | 如适用 |
| **采样参数** | | |
| Temperature | | |
| Top-p | | |
| Top-k | | |
| **加速技术** | | |
| KV Cache | | 是否使用 |
| Flash Attention | | |
| Quantization | | INT8/INT4 |
| **性能指标** | | |
| Latency (per sample) | | ms |
| Throughput | | samples/sec |
| Memory Usage | | GB |
```

### 5.3 模型规模

```markdown
## Model Scale

| 项目 | 值 |
|------|------|
| **参数量** | |
| Total Parameters | |
| Trainable Parameters | |
| **架构详情** | |
| Model Type | |
| Hidden Size | |
| Num Layers | |
| Num Attention Heads | |
| Vocab Size | |
| Max Sequence Length | |
| **数据规模** | |
| Training Data Size | |
| Training Tokens | |
| Validation Data Size | |
```

---

## 6. 实验分析框架

### 6.1 主实验分析

**结果表格模板**：

| Method | Metric1 ↑ | Metric2 ↑ | Metric3 ↓ | Params | FLOPs |
|--------|-----------|-----------|-----------|--------|-------|
| Baseline1 | | | | | |
| Baseline2 | | | | | |
| Prior SOTA | | | | | |
| **Ours** | **XX.X** (+Δ) | **XX.X** (+Δ) | **XX.X** (-Δ) | | |

**分析要点**：
- 最显著的提升在哪个指标？提升多少？
- 与 strongest baseline 比差距多大？
- 计算成本增加了多少？值得吗？

### 6.2 效果分析

| 分析角度 | 问题 |
|---------|------|
| 主要优势 | 哪些场景/数据上提升最明显？ |
| 原因分析 | 为什么在这些场景上更好？ |
| 边界情况 | 哪些情况下优势不明显？ |
| 定性观察 | 从可视化结果能看出什么？ |

### 6.3 实验合理性分析

**检查清单**：

| 检查项 | 是否满足 | 说明 |
|--------|---------|------|
| Baseline 选择合理 | ☐ | 是否包含 SOTA 方法？ |
| Baseline 实现公平 | ☐ | 是否使用相同的训练设置？ |
| 评估指标恰当 | ☐ | 指标能反映任务目标吗？ |
| 测试集独立 | ☐ | 没有数据泄露？ |
| 统计显著性 | ☐ | 多次实验？标准差？ |
| 计算资源可比 | ☐ | 参数量/FLOPs 是否公平？ |

### 6.4 消融实验分析

**消融实验模板**：

| 配置 | Metric | Δ vs Full |
|------|--------|-----------|
| Full Model | XX.X | - |
| w/o Component A | XX.X | -Y.Y |
| w/o Component B | XX.X | -Y.Y |
| w/o Component C | XX.X | -Y.Y |
| w/o A + B | XX.X | -Y.Y |

**分析要点**：
- 哪个组件贡献最大？
- 各组件是否有协同效应？
- 有没有可以去掉的冗余组件？

### 6.5 失败案例分析

```markdown
## Failure Cases

**失败类型1**：[描述]
- 示例: [具体例子]
- 原因: [分析]
- 可能解决方案: [建议]

**失败类型2**：[描述]
- 示例: [具体例子]
- 原因: [分析]
- 可能解决方案: [建议]
```

---

## 7. 总结与展望分析

### 7.1 工作质量评分

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| **创新性** | ☆☆☆☆☆ | idea 新颖程度 |
| **技术贡献** | ☆☆☆☆☆ | 技术方案的深度 |
| **实验充分性** | ☆☆☆☆☆ | 实验设计和分析 |
| **可复现性** | ☆☆☆☆☆ | 细节和代码 |
| **实用价值** | ☆☆☆☆☆ | 能否落地应用 |
| **写作质量** | ☆☆☆☆☆ | 论文清晰度 |

### 7.2 Limitation 分析

**论文提到的 Limitations**：
1. [Limitation 1]
2. [Limitation 2]

**你发现的潜在问题**：
1. [Problem 1]: [具体描述]
2. [Problem 2]: [具体描述]

**被忽视的方面**：
- 计算成本讨论够充分吗？
- 数据偏见讨论了吗？
- 负面社会影响考虑了吗？

### 7.3 Future Work 方向

| 方向 | 描述 | 难度 | 潜在影响 |
|------|------|------|---------|
| 方向1 | [具体描述] | 低/中/高 | 低/中/高 |
| 方向2 | [具体描述] | 低/中/高 | 低/中/高 |
| 方向3 | [具体描述] | 低/中/高 | 低/中/高 |

**可以结合的其他工作**：
- [Work A] + 本工作 = [可能的方向]
- [Work B] + 本工作 = [可能的方向]

---

## AI 领域特定分析模板

### LLM 论文

```markdown
**额外关注点**：
- Tokenizer: [类型, vocab size]
- Context Length: [最大长度]
- Scaling: [参数量/数据量/计算量]
- Emergent Abilities: [是否观察到涌现能力]
- Safety: [安全性考量]
- RLHF/DPO: [对齐方法]
```

### Vision 论文

```markdown
**额外关注点**：
- Input Resolution: [训练/推理分辨率]
- Backbone: [架构, 预训练权重]
- Data Augmentation: [增强策略]
- Multi-scale: [多尺度处理]
```

### Multimodal 论文

```markdown
**额外关注点**：
- 模态对齐: [如何对齐不同模态]
- Cross-modal Attention: [跨模态交互设计]
- 预训练数据: [图文配对数据来源]
- Modality Gap: [是否讨论模态差距]
```

### Diffusion 论文

```markdown
**额外关注点**：
- Noise Schedule: [噪声调度]
- Sampling Steps: [采样步数]
- Guidance: [CFG scale, 其他引导]
- Latent Space: [是否在 latent 空间]
- Controlability: [可控生成能力]
```

### RL 论文

```markdown
**额外关注点**：
- Environment: [环境设置]
- Reward Design: [奖励函数设计]
- Exploration: [探索策略]
- Sample Efficiency: [样本效率]
- Sim-to-Real: [仿真到现实迁移]
```
