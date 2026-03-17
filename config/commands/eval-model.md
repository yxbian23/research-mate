---
description: Evaluate ML models on standard benchmarks - supports vision (FID/IS/LPIPS), LLM (MMLU/HumanEval), and VLM evaluation with automatic report generation.
---

# Eval Model Command

This command runs comprehensive model evaluation on standard benchmarks and generates detailed evaluation reports.

## What This Command Does

1. **Load Model** - Load checkpoint with proper configuration
2. **Select Benchmarks** - Choose appropriate evaluation suite
3. **Run Evaluation** - Execute benchmarks with proper settings
4. **Generate Report** - Create comprehensive evaluation report

## When to Use

Use `/eval-model` when:
- Evaluating a trained model checkpoint
- Running standard benchmarks for paper
- Comparing model versions
- Validating model quality before deployment

## Supported Benchmarks

### Vision Generation Models
| Metric | Description | Lower/Higher Better |
|--------|-------------|---------------------|
| FID | Frechet Inception Distance | Lower |
| IS | Inception Score | Higher |
| LPIPS | Learned Perceptual Similarity | Lower |
| CLIP Score | Text-image alignment | Higher |
| Aesthetic Score | Visual quality | Higher |

### Large Language Models
| Benchmark | Description |
|-----------|-------------|
| MMLU | Multitask accuracy |
| HellaSwag | Commonsense reasoning |
| ARC | Science QA |
| WinoGrande | Coreference resolution |
| HumanEval | Code generation |
| GSM8K | Math reasoning |
| TruthfulQA | Factual accuracy |

### Vision-Language Models
| Benchmark | Description |
|-----------|-------------|
| VQAv2 | Visual QA |
| GQA | Compositional reasoning |
| TextVQA | OCR understanding |
| MMBench | Multimodal understanding |
| SEED-Bench | Generative comprehension |
| MME | Comprehensive multimodal |

## Example Usage

```
User: /eval-model checkpoints/model-best.pt on imagenet

Agent:
# Model Evaluation Report

## Model Info
- Checkpoint: checkpoints/model-best.pt
- Architecture: DiT-XL/2
- Parameters: 675M
- Training steps: 400K

## Evaluation: ImageNet-256

### Generation Quality
| Metric | Score | Reference |
|--------|-------|-----------|
| FID-50K | 2.27 | DiT paper: 2.27 |
| IS | 278.24 | DiT paper: 278.24 |
| Precision | 0.83 | - |
| Recall | 0.57 | - |

### Generation Speed
- Samples/sec: 12.4 (batch=16)
- Steps: 250 (DDPM)

### Sample Analysis
- High quality: 89%
- Artifacts detected: 3%
- Mode coverage: Good

## Recommendations
✓ FID matches paper, model correctly implemented
⚠ Recall slightly low, consider more CFG scales
```

## Evaluation Configuration

```yaml
eval:
  model_path: checkpoints/model-best.pt
  benchmarks:
    - name: fid
      dataset: imagenet
      num_samples: 50000
    - name: is
      num_samples: 50000
  device: cuda
  precision: fp16
  batch_size: 64
```

## Evaluation Script Examples

### FID Evaluation
```python
from cleanfid import fid

score = fid.compute_fid(
    gen_folder="generated_samples/",
    dataset_name="imagenet",
    mode="clean",
    num_workers=8,
)
print(f"FID: {score:.2f}")
```

### LLM Evaluation with lm-eval
```bash
lm_eval --model hf \
    --model_args pretrained=./checkpoint \
    --tasks mmlu,hellaswag,arc_easy,arc_challenge \
    --batch_size 8 \
    --output_path results/
```

### VLM Evaluation
```python
from lmms_eval import evaluator

results = evaluator.simple_evaluate(
    model="llava",
    model_args="pretrained=./checkpoint",
    tasks=["vqav2", "gqa", "textvqa"],
)
```

## Report Format

```markdown
# Evaluation Report: [Model Name]

## Summary
| Benchmark | Score | Baseline | Delta |
|-----------|-------|----------|-------|
| ... | ... | ... | ... |

## Detailed Results
[Per-benchmark breakdown]

## Failure Analysis
[Common error patterns]

## Comparison
[vs baselines and SOTA]

## Artifacts
- samples/: Generated samples
- results/: Raw evaluation outputs
- plots/: Visualization
```

## Important Notes

1. **Reproducibility**: Always report seed and evaluation settings
2. **Sample Count**: Use standard counts (50K for FID)
3. **Baseline**: Compare against published numbers
4. **Hardware**: Report GPU type for speed benchmarks

## Related Commands

- `/train` - Train models
- `/benchmark` - Run specific benchmarks
- `/ablation` - Compare model variants