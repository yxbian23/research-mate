---
description: Design and run ablation studies - systematically vary components, generate comparison tables, and identify contribution of each design choice.
---

# Ablation Command

This command helps design, execute, and analyze ablation studies to understand the contribution of different model components.

## What This Command Does

1. **Design Experiments** - Identify components to ablate
2. **Generate Configs** - Create configuration variants
3. **Run Studies** - Execute experiments systematically
4. **Analyze Results** - Generate comparison tables and insights

## When to Use

Use `/ablation` when:
- Validating design choices in your model
- Preparing ablation tables for paper
- Understanding component contributions
- Optimizing model architecture

## Ablation Study Types

### 1. Component Ablation
Remove or replace individual components:
- Attention mechanism type
- Normalization layer
- Activation function
- Skip connections

### 2. Hyperparameter Sweep
Systematically vary hyperparameters:
- Model size (depth, width)
- Learning rate
- Batch size
- Regularization strength

### 3. Data Ablation
Study data impact:
- Dataset size
- Data augmentation
- Preprocessing choices

### 4. Training Ablation
Vary training procedures:
- Optimizer choice
- Learning rate schedule
- Training duration

## Example Usage

```
User: /ablation for DiT model components

Agent:
# Ablation Study Design: DiT Components

## Research Questions
1. How much does adaLN-Zero contribute vs standard adaLN?
2. What's the impact of patch size on quality vs speed?
3. Is the final linear layer necessary?

## Experiment Matrix

### Experiment 1: Conditioning Mechanism
| Config | Conditioning | Expected Impact |
|--------|--------------|-----------------|
| baseline | adaLN-Zero | - |
| ablation_1a | adaLN (no zero init) | -5-10% FID |
| ablation_1b | cross-attention | +10% FID |
| ablation_1c | concatenation | +20% FID |

### Experiment 2: Patch Size
| Config | Patch Size | Tokens | Speed | Quality |
|--------|-----------|--------|-------|---------|
| p2 | 2 | 16384 | 1x | Best |
| p4 | 4 | 4096 | 4x | Good |
| p8 | 8 | 1024 | 16x | Worse |

### Experiment 3: Architecture Depth vs Width
| Config | Layers | Hidden | Params | FID |
|--------|--------|--------|--------|-----|
| deep_narrow | 28 | 768 | 400M | ? |
| baseline | 28 | 1152 | 675M | 2.27 |
| shallow_wide | 14 | 1600 | 675M | ? |

## Generated Configs

```yaml
# configs/ablation/conditioning/adaln_zero.yaml
model:
  conditioning: adaln_zero
  zero_init: true

# configs/ablation/conditioning/adaln.yaml
model:
  conditioning: adaln
  zero_init: false

# configs/ablation/conditioning/cross_attn.yaml
model:
  conditioning: cross_attention
```

## Execution Plan

```bash
# Run all ablations
for config in configs/ablation/*/*.yaml; do
    python train.py --config $config \
        --steps 100000 \
        --eval_every 10000 \
        --wandb_group "ablation_study"
done
```

## Results Template

| Component | Variant | FID↓ | IS↑ | Training Cost |
|-----------|---------|------|-----|---------------|
| **Conditioning** | | | | |
| | adaLN-Zero (baseline) | 2.27 | 278 | 1x |
| | adaLN | ? | ? | 1x |
| | Cross-attention | ? | ? | 1.2x |
| **Patch Size** | | | | |
| | p=2 (baseline) | 2.27 | 278 | 1x |
| | p=4 | ? | ? | 0.25x |

**Start ablation study?** (yes/all/select experiments)
```

## Ablation Best Practices

### 1. Controlled Variables
- Change ONE thing at a time
- Use same random seed
- Keep compute budget equal

### 2. Statistical Significance
- Run multiple seeds (3-5)
- Report mean ± std
- Use appropriate tests

### 3. Fair Comparisons
- Match parameter count when possible
- Use same training budget
- Identical evaluation protocol

### 4. Reporting
- Include baseline in every table
- Show computational cost
- Explain surprising results

## Results Analysis

```python
import pandas as pd

# Load results
results = pd.read_csv("ablation_results.csv")

# Generate latex table
print(results.to_latex(
    index=False,
    caption="Ablation study results",
    label="tab:ablation"
))

# Statistical test
from scipy import stats
baseline = results[results['config'] == 'baseline']['fid']
ablation = results[results['config'] == 'no_adaln']['fid']
t_stat, p_value = stats.ttest_ind(baseline, ablation)
```

## LaTeX Table Template

```latex
\begin{table}[t]
\centering
\caption{Ablation study on model components.}
\label{tab:ablation}
\begin{tabular}{lcc}
\toprule
Component & FID $\downarrow$ & IS $\uparrow$ \\
\midrule
Full model (baseline) & \textbf{2.27} & \textbf{278.2} \\
\quad w/o adaLN-Zero & 2.89 & 245.1 \\
\quad w/o final layer & 2.45 & 268.3 \\
\bottomrule
\end{tabular}
\end{table}
```

## Related Commands

- `/train` - Run individual experiments
- `/eval-model` - Evaluate each variant
- `/benchmark` - Standard benchmark comparison