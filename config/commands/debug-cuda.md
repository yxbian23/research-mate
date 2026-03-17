---
description: Debug CUDA and GPU issues - diagnose memory problems, device errors, synchronization issues, and distributed training bugs with actionable solutions.
---

# Debug CUDA Command

This command diagnoses and resolves CUDA, GPU memory, and distributed training issues.

## What This Command Does

1. **Analyze Error** - Parse CUDA error messages and stack traces
2. **Diagnose Root Cause** - Identify the underlying issue
3. **Suggest Fixes** - Provide actionable solutions
4. **Verify Fix** - Confirm the issue is resolved

## When to Use

Use `/debug-cuda` when:
- Getting CUDA out of memory (OOM) errors
- Encountering device mismatch errors
- Facing NCCL/distributed training failures
- Seeing NaN/Inf in training
- Training hangs or deadlocks

## Common Error Categories

### 1. Out of Memory (OOM)
```
RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB
```

**Solutions checked:**
- Reduce batch size
- Enable gradient checkpointing
- Use mixed precision (fp16/bf16)
- Clear cache between steps
- Use memory-efficient attention

### 2. Device Mismatch
```
RuntimeError: Expected all tensors to be on the same device
```

**Solutions checked:**
- Verify model device placement
- Check input tensor devices
- Ensure consistent `.to(device)` calls

### 3. NCCL Errors
```
RuntimeError: NCCL error: unhandled system error
```

**Solutions checked:**
- Network configuration
- NCCL environment variables
- GPU topology
- Timeout settings

### 4. Synchronization Errors
```
CUDA error: device-side assert triggered
```

**Solutions checked:**
- Enable CUDA_LAUNCH_BLOCKING
- Check tensor shapes
- Validate loss computation

## Example Usage

```
User: /debug-cuda
RuntimeError: CUDA out of memory. Tried to allocate 4.00 GiB (GPU 0; 24.00 GiB total capacity; 21.50 GiB already allocated)

Agent:
# CUDA Debug Report

## Error Analysis
- **Type**: Out of Memory (OOM)
- **GPU**: 24GB VRAM
- **Requested**: 4GB
- **Available**: 2.5GB
- **Utilization**: 89.6%

## Memory Breakdown
```
Model parameters: 14.2 GB
Gradients: 14.2 GB (if not gradient checkpointing)
Optimizer states: 28.4 GB (Adam)
Activations: ~8 GB (estimated)
Total: ~65 GB (exceeds 24GB)
```

## Root Cause
Adam optimizer requires 2x model size for momentum/variance states.
Combined with gradients and activations, exceeds GPU memory.

## Recommended Solutions (priority order)

### 1. Enable Gradient Checkpointing (saves ~30% memory)
```python
model.gradient_checkpointing_enable()
```

### 2. Use Mixed Precision (saves ~50% memory)
```python
from torch.cuda.amp import autocast, GradScaler
scaler = GradScaler()
with autocast():
    output = model(input)
    loss = criterion(output, target)
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

### 3. Reduce Batch Size with Gradient Accumulation
```python
accumulation_steps = 4
for i, batch in enumerate(dataloader):
    loss = model(batch) / accumulation_steps
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### 4. Use Memory-Efficient Optimizer
```python
# 8-bit Adam
import bitsandbytes as bnb
optimizer = bnb.optim.Adam8bit(model.parameters(), lr=1e-4)
```

### 5. Use DeepSpeed ZeRO
```python
# ZeRO Stage 2 partitions optimizer states
deepspeed_config = {
    "zero_optimization": {"stage": 2}
}
```

## Quick Memory Check
```python
print(f"Allocated: {torch.cuda.memory_allocated()/1e9:.2f} GB")
print(f"Reserved: {torch.cuda.memory_reserved()/1e9:.2f} GB")
torch.cuda.empty_cache()
```

**Implement solution 1 first?** (yes/no/try another)
```

## Debug Utilities

### Memory Profiler
```python
import torch
from torch.cuda import memory_stats

def print_memory_stats():
    stats = memory_stats()
    print(f"Allocated: {stats['allocated_bytes.all.current']/1e9:.2f} GB")
    print(f"Peak: {stats['allocated_bytes.all.peak']/1e9:.2f} GB")
```

### Device Checker
```python
def check_model_device(model):
    devices = set()
    for p in model.parameters():
        devices.add(str(p.device))
    print(f"Model devices: {devices}")
```

### CUDA Error Locator
```bash
CUDA_LAUNCH_BLOCKING=1 python train.py
```

## Environment Variables

```bash
# Debugging
export CUDA_LAUNCH_BLOCKING=1
export TORCH_DISTRIBUTED_DEBUG=DETAIL
export NCCL_DEBUG=INFO

# Memory
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

## Related Commands

- `/train` - Start training with proper config
- `/eval-model` - Evaluate after fixing issues