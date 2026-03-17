# GPU Safety Rules

## Memory Management (CRITICAL)

### Check GPU Memory Before Training

ALWAYS verify GPU memory before starting:

```python
def check_gpu_memory():
    """Check if sufficient GPU memory is available."""
    if torch.cuda.is_available():
        free_memory = torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated()
        print(f"Free GPU memory: {free_memory / 1e9:.2f} GB")
        return free_memory
    return 0
```

### Clear Cache Regularly

CLEAR GPU cache when switching between large operations:

```python
# After evaluation, before next training epoch
torch.cuda.empty_cache()
gc.collect()
```

### Detach Tensors for Logging

ALWAYS detach tensors before storing:

```python
# WRONG - keeps computation graph, leaks memory
loss_history.append(loss)

# CORRECT - detaches and moves to CPU
loss_history.append(loss.detach().cpu().item())
```

## Gradient Safety

### Zero Gradients Properly

ALWAYS zero gradients before backward:

```python
# CORRECT - explicit zero
optimizer.zero_grad()
loss.backward()
optimizer.step()

# ALSO CORRECT - zero in forward
for batch in dataloader:
    optimizer.zero_grad()  # MUST be before forward or backward
    outputs = model(batch)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
```

### Gradient Clipping

ALWAYS use gradient clipping for training stability:

```python
# After backward, before step
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

### Check for NaN Gradients

MONITOR for NaN gradients:

```python
def check_gradients(model):
    """Check for NaN or Inf gradients."""
    for name, param in model.named_parameters():
        if param.grad is not None:
            if torch.isnan(param.grad).any():
                raise ValueError(f"NaN gradient in {name}")
            if torch.isinf(param.grad).any():
                raise ValueError(f"Inf gradient in {name}")
```

## CUDA Error Handling

### Synchronize for Error Detection

Use CUDA synchronization when debugging:

```python
# For debugging CUDA errors
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

# Explicit sync
torch.cuda.synchronize()
```

### Handle Device Mismatch

ALWAYS check tensor devices:

```python
def to_device(batch: dict, device: torch.device) -> dict:
    """Move batch to device safely."""
    return {
        k: v.to(device) if isinstance(v, torch.Tensor) else v
        for k, v in batch.items()
    }

# Verify model and data on same device
assert next(model.parameters()).device == inputs.device
```

## Mixed Precision Safety

### Use GradScaler Correctly

ALWAYS use GradScaler with AMP:

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    optimizer.zero_grad()

    with autocast():
        outputs = model(batch)
        loss = outputs.loss

    # Scale loss and backward
    scaler.scale(loss).backward()

    # Unscale for gradient clipping
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

    # Step with scaler
    scaler.step(optimizer)
    scaler.update()
```

### Handle NaN Loss with Scaler

GradScaler handles NaN automatically, but monitor:

```python
if scaler.get_scale() < 1.0:
    print("Warning: GradScaler scale is very low, possible numerical issues")
```

## Distributed Training Safety

### Initialize Properly

ALWAYS initialize distributed before creating model:

```python
import torch.distributed as dist

def setup_distributed(rank, world_size):
    dist.init_process_group(
        backend='nccl',
        init_method='env://',
        world_size=world_size,
        rank=rank
    )
    torch.cuda.set_device(rank)

def cleanup_distributed():
    dist.destroy_process_group()
```

### Synchronize Metrics

ALWAYS synchronize metrics across ranks:

```python
def all_reduce_mean(tensor):
    """Average tensor across all ranks."""
    dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
    tensor /= dist.get_world_size()
    return tensor
```

## Checkpointing Safety

### Save Complete State

ALWAYS save complete training state:

```python
def save_checkpoint(path, model, optimizer, scheduler, epoch, step):
    torch.save({
        'epoch': epoch,
        'step': step,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'scheduler_state_dict': scheduler.state_dict(),
        'rng_state': torch.get_rng_state(),
        'cuda_rng_state': torch.cuda.get_rng_state_all(),
    }, path)
```

### Load Safely

HANDLE missing keys gracefully:

```python
def load_checkpoint(path, model, strict=False):
    checkpoint = torch.load(path, map_location='cpu')
    missing, unexpected = model.load_state_dict(
        checkpoint['model_state_dict'],
        strict=strict
    )
    if missing:
        print(f"Missing keys: {missing}")
    if unexpected:
        print(f"Unexpected keys: {unexpected}")
    return checkpoint
```

## Safety Checklist

Before training:
- [ ] GPU memory checked
- [ ] Devices verified (model and data on same device)
- [ ] Gradient clipping configured
- [ ] Checkpoint saving configured
- [ ] NaN monitoring in place
- [ ] Mixed precision scaler initialized (if using AMP)
- [ ] Distributed training properly initialized (if multi-GPU)

During training:
- [ ] Gradients zeroed before backward
- [ ] Loss detached before logging
- [ ] Periodic cache clearing
- [ ] Checkpoints saved regularly
