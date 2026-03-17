---
description: Start ML training workflow - check GPU, validate config, set up distributed training, and launch training job with proper experiment tracking.
---

# Train Command

This command helps you set up and launch machine learning training jobs with proper configuration, experiment tracking, and distributed training support.

## What This Command Does

1. **Environment Check** - Verify GPU availability and CUDA setup
2. **Config Validation** - Ensure training config is complete and valid
3. **Experiment Setup** - Initialize wandb/tensorboard logging
4. **Launch Training** - Start training with proper settings

## When to Use

Use `/train` when:
- Starting a new training run
- Setting up distributed training (DDP/FSDP)
- Need to validate training configuration
- Want to ensure proper experiment tracking

## Pre-Training Checklist

Before starting, the command will verify:

### Hardware
- [ ] GPU available and accessible
- [ ] Sufficient GPU memory for model + batch size
- [ ] Multi-GPU setup configured (if applicable)

### Configuration
- [ ] Model architecture specified
- [ ] Dataset path exists and is readable
- [ ] Batch size fits in GPU memory
- [ ] Learning rate and scheduler configured
- [ ] Checkpoint directory writable

### Reproducibility
- [ ] Random seed set
- [ ] Git commit logged
- [ ] Full config saved

## Example Usage

```
User: /train with config.yaml

Agent:
# Training Setup Verification

## Environment Check
✓ GPU: NVIDIA A100-SXM4-80GB
✓ CUDA: 12.1
✓ PyTorch: 2.1.0+cu121
✓ Available Memory: 80GB

## Config Analysis: config.yaml
✓ Model: LLaMA-7B
✓ Dataset: /data/train.jsonl (exists, 1.2M samples)
✓ Batch size: 4 (estimated memory: 32GB)
✓ Gradient accumulation: 8 (effective batch: 32)
✓ Learning rate: 1e-4 with cosine decay
✓ Checkpoints: ./checkpoints/ (writable)

## Experiment Tracking
- Project: llama-finetune
- Run name: llama7b-lr1e4-bs32-20240115
- Tags: ["baseline", "full-finetune"]

## Distributed Training
- Strategy: DDP
- GPUs: 4
- World size: 4

**Ready to launch training?** (yes/no/modify config)
```

## Training Script Template

The command will help generate or validate training scripts like:

```python
import torch
from torch.distributed import init_process_group
from transformers import AutoModelForCausalLM, Trainer

# Reproducibility
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)

# Initialize distributed
init_process_group(backend="nccl")

# Training
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    callbacks=[WandbCallback()],
)

trainer.train()
```

## Important Notes

**CRITICAL**: Always verify:
1. Dataset path is correct and accessible
2. GPU memory is sufficient (use `nvidia-smi`)
3. Checkpoint directory has enough disk space
4. Experiment tracking is properly configured

## Common Training Configurations

### Single GPU
```bash
python train.py --config config.yaml
```

### Multi-GPU (DDP)
```bash
torchrun --nproc_per_node=4 train.py --config config.yaml
```

### Multi-Node
```bash
torchrun --nnodes=2 --nproc_per_node=8 --node_rank=$RANK \
    --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT \
    train.py --config config.yaml
```

## Related Commands

- `/debug-cuda` - Debug CUDA/GPU issues
- `/eval-model` - Evaluate trained model
- `/ablation` - Run ablation studies