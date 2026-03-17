---
description: Run standard ML benchmarks - vision generation (FID/IS), LLM (MMLU/HumanEval), VLM (VQAv2/MMBench) with standardized evaluation protocols.
---

# Benchmark Command

This command runs standardized benchmarks for machine learning models with proper evaluation protocols.

## What This Command Does

1. **Select Benchmark Suite** - Choose appropriate benchmarks for model type
2. **Configure Evaluation** - Set up standardized parameters
3. **Run Benchmarks** - Execute with proper protocols
4. **Generate Report** - Compare against baselines

## When to Use

Use `/benchmark` when:
- Preparing results for paper submission
- Comparing against state-of-the-art
- Validating model implementation
- Tracking progress during development

## Benchmark Suites

### Vision Generation

| Benchmark | Metric | Standard Config |
|-----------|--------|-----------------|
| ImageNet-256 | FID-50K | 50K samples, ADM protocol |
| ImageNet-512 | FID-50K | 50K samples |
| COCO-30K | FID | 30K samples |
| FFHQ-256 | FID | 50K samples |

```bash
# Standard FID evaluation
python eval_fid.py \
    --model_path checkpoint.pt \
    --dataset imagenet \
    --num_samples 50000 \
    --batch_size 64 \
    --cfg_scale 1.5
```

### Large Language Models

| Benchmark | Task | Metric |
|-----------|------|--------|
| MMLU | Knowledge | Accuracy |
| HellaSwag | Reasoning | Accuracy |
| ARC-C | Science | Accuracy |
| WinoGrande | Coreference | Accuracy |
| GSM8K | Math | Accuracy |
| HumanEval | Code | Pass@k |
| MBPP | Code | Pass@k |

```bash
# Using lm-evaluation-harness
lm_eval --model hf \
    --model_args pretrained=./model,dtype=float16 \
    --tasks mmlu,hellaswag,arc_challenge,winogrande,gsm8k \
    --batch_size 8 \
    --num_fewshot 5 \
    --output_path results/
```

### Vision-Language Models

| Benchmark | Task | Metric |
|-----------|------|--------|
| VQAv2 | Visual QA | Accuracy |
| GQA | Reasoning | Accuracy |
| TextVQA | OCR | Accuracy |
| POPE | Hallucination | F1 |
| MMBench | Multimodal | Accuracy |
| SEED-Bench | Generative | Accuracy |
| MME | Comprehensive | Score |

```bash
# Using lmms-eval
lmms-eval --model llava \
    --model_args pretrained=./checkpoint \
    --tasks vqav2,gqa,textvqa,mmbench \
    --batch_size 1 \
    --output_path results/
```

## Example Usage

```
User: /benchmark llava-v1.5-7b on VLM suite

Agent:
# Benchmark Report: LLaVA-v1.5-7B

## Model Info
- Architecture: LLaVA-v1.5
- LLM: Vicuna-7B
- Vision: CLIP-ViT-L/14-336px
- Training: 558K pretrain + 665K finetune

## VLM Benchmark Results

### Image Understanding
| Benchmark | Score | LLaVA-1.5-7B (paper) | Δ |
|-----------|-------|----------------------|---|
| VQAv2 (test-dev) | 78.5 | 78.5 | ✓ |
| GQA | 62.0 | 62.0 | ✓ |
| VizWiz | 50.0 | 50.0 | ✓ |
| TextVQA | 58.2 | 58.2 | ✓ |

### Multimodal Reasoning
| Benchmark | Score | Paper | Δ |
|-----------|-------|-------|---|
| POPE (accuracy) | 85.9 | 85.9 | ✓ |
| POPE (F1) | 84.1 | - | - |
| MME (perception) | 1510 | 1510 | ✓ |
| MME (cognition) | 348 | 348 | ✓ |

### Comprehensive Benchmarks
| Benchmark | Score | Paper |
|-----------|-------|-------|
| MMBench | 64.3 | 64.3 |
| MMBench-CN | 58.3 | 58.3 |
| SEED-Bench (img) | 66.1 | 66.1 |

## Comparison with SOTA

| Model | VQAv2 | GQA | MME |
|-------|-------|-----|-----|
| **Ours** | 78.5 | 62.0 | 1858 |
| GPT-4V | 77.2 | - | 1927 |
| Qwen-VL-Chat | 78.2 | 57.5 | 1848 |
| InternLM-XC | 79.8 | 63.8 | 1876 |

## Evaluation Details
- Precision: float16
- Batch size: 1
- Temperature: 0 (greedy)
- Max new tokens: 512

**Download full results?** (yes/no)
```

## Benchmark Protocols

### FID Evaluation (Vision)
```python
# ADM protocol (recommended)
from cleanfid import fid

score = fid.compute_fid(
    fdir1="generated/",
    fdir2="imagenet_train/",
    mode="clean",  # Use clean-fid
    num_workers=8,
    batch_size=64,
)
```

### LLM Evaluation
```python
# Standard few-shot
from lm_eval import evaluator

results = evaluator.simple_evaluate(
    model="hf",
    model_args="pretrained=./model",
    tasks=["mmlu", "hellaswag"],
    num_fewshot=5,  # Standard: 5-shot for MMLU
    batch_size=8,
)
```

### VLM Evaluation
```python
# Zero-shot VQA
from lmms_eval import evaluator

results = evaluator.simple_evaluate(
    model="llava",
    model_args="pretrained=./model",
    tasks=["vqav2"],
    batch_size=1,
)
```

## Results Format

### For Paper Submission
```latex
\begin{table}[t]
\centering
\caption{Comparison on VLM benchmarks.}
\begin{tabular}{l|ccc|cc}
\toprule
Method & VQAv2 & GQA & TextVQA & MME$^P$ & MME$^C$ \\
\midrule
LLaVA-1.5-7B & 78.5 & 62.0 & 58.2 & 1510 & 348 \\
\textbf{Ours} & \textbf{79.8} & \textbf{63.5} & \textbf{60.1} & \textbf{1580} & \textbf{365} \\
\bottomrule
\end{tabular}
\end{table}
```

## Important Notes

1. **Reproducibility**: Report exact eval settings
2. **Fair Comparison**: Match baseline conditions
3. **Statistical Variance**: Multiple runs for close results
4. **Version Control**: Note benchmark versions

## Related Commands

- `/eval-model` - Quick model evaluation
- `/ablation` - Component studies
- `/train` - Train models