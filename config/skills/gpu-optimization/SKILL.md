---
name: gpu-optimization
description: Use this skill when optimizing GPU training efficiency. Covers memory optimization, mixed precision, gradient accumulation, model parallelism (TP/PP/DP), DeepSpeed, and FSDP integration.
---

# GPU Optimization

This skill provides comprehensive guidance for optimizing GPU training efficiency and handling large models.

## When to Activate

- Training runs out of GPU memory
- Need to scale training to multiple GPUs
- Optimizing training throughput
- Implementing model parallelism
- Using DeepSpeed or FSDP

## Memory Optimization Techniques

### 1. Mixed Precision Training

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    optimizer.zero_grad()

    # Forward pass in fp16/bf16
    with autocast(dtype=torch.bfloat16):
        outputs = model(batch["input"])
        loss = criterion(outputs, batch["target"])

    # Backward pass with scaling
    scaler.scale(loss).backward()

    # Unscale for gradient clipping
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

    # Optimizer step
    scaler.step(optimizer)
    scaler.update()
```

### 2. Gradient Checkpointing

```python
from torch.utils.checkpoint import checkpoint, checkpoint_sequential

class CheckpointedTransformer(nn.Module):
    def __init__(self, num_layers: int, dim: int):
        super().__init__()
        self.layers = nn.ModuleList([
            TransformerBlock(dim) for _ in range(num_layers)
        ])
        self.gradient_checkpointing = False

    def enable_gradient_checkpointing(self):
        self.gradient_checkpointing = True

    def forward(self, x):
        if self.gradient_checkpointing and self.training:
            # Checkpoint every layer
            for layer in self.layers:
                x = checkpoint(layer, x, use_reentrant=False)
        else:
            for layer in self.layers:
                x = layer(x)
        return x

# Or checkpoint sequential blocks
x = checkpoint_sequential(self.layers, segments=4, input=x)
```

### 3. Gradient Accumulation

```python
accumulation_steps = 4
optimizer.zero_grad()

for i, batch in enumerate(dataloader):
    # Forward pass
    with autocast():
        outputs = model(batch["input"])
        loss = criterion(outputs, batch["target"])
        loss = loss / accumulation_steps  # Normalize loss

    # Backward pass
    scaler.scale(loss).backward()

    # Update only every N steps
    if (i + 1) % accumulation_steps == 0:
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
```

### 4. Memory-Efficient Attention

```python
# Flash Attention (via PyTorch 2.0+)
from torch.nn.functional import scaled_dot_product_attention

# Automatically uses flash attention when available
output = scaled_dot_product_attention(query, key, value, is_causal=True)

# Or use xFormers
from xformers.ops import memory_efficient_attention
output = memory_efficient_attention(query, key, value)
```

### 5. Activation Offloading

```python
import torch
from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import (
    checkpoint_wrapper,
    offload_wrapper,
)

# Wrap layers with offloading
model = checkpoint_wrapper(model, offload_to_cpu=True)
```

## Distributed Data Parallel (DDP)

### Basic DDP Setup

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler

def setup(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

def cleanup():
    dist.destroy_process_group()

def train(rank, world_size, config):
    setup(rank, world_size)

    # Create model on correct device
    model = MyModel().to(rank)
    model = DDP(model, device_ids=[rank])

    # Distributed sampler
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    loader = DataLoader(dataset, sampler=sampler, batch_size=config.batch_size)

    for epoch in range(config.epochs):
        sampler.set_epoch(epoch)  # Important for shuffling

        for batch in loader:
            # Training step
            pass

    cleanup()

# Launch
import torch.multiprocessing as mp
mp.spawn(train, args=(world_size, config), nprocs=world_size, join=True)
```

## Fully Sharded Data Parallel (FSDP)

### Basic FSDP

```python
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP,
    MixedPrecision,
    BackwardPrefetch,
    ShardingStrategy,
)
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy

# Mixed precision policy
mixed_precision_policy = MixedPrecision(
    param_dtype=torch.bfloat16,
    reduce_dtype=torch.bfloat16,
    buffer_dtype=torch.bfloat16,
)

# Auto wrap policy for transformers
auto_wrap_policy = functools.partial(
    transformer_auto_wrap_policy,
    transformer_layer_cls={TransformerBlock},
)

# Create FSDP model
model = FSDP(
    model,
    sharding_strategy=ShardingStrategy.FULL_SHARD,  # or SHARD_GRAD_OP, NO_SHARD
    mixed_precision=mixed_precision_policy,
    auto_wrap_policy=auto_wrap_policy,
    backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
    device_id=torch.cuda.current_device(),
)
```

### FSDP Checkpointing

```python
from torch.distributed.fsdp import StateDictType, FullStateDictConfig

# Full state dict (for saving/loading complete model)
with FSDP.state_dict_type(
    model,
    StateDictType.FULL_STATE_DICT,
    FullStateDictConfig(offload_to_cpu=True, rank0_only=True),
):
    state_dict = model.state_dict()
    if rank == 0:
        torch.save(state_dict, "checkpoint.pt")

# Sharded state dict (for resuming training)
with FSDP.state_dict_type(model, StateDictType.SHARDED_STATE_DICT):
    state_dict = model.state_dict()
    torch.save(state_dict, f"checkpoint_rank{rank}.pt")
```

## DeepSpeed Integration

### DeepSpeed Config

```json
{
  "train_batch_size": 256,
  "gradient_accumulation_steps": 4,
  "fp16": {
    "enabled": true,
    "loss_scale": 0,
    "initial_scale_power": 16
  },
  "zero_optimization": {
    "stage": 2,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    },
    "allgather_partitions": true,
    "reduce_scatter": true,
    "overlap_comm": true
  },
  "gradient_clipping": 1.0,
  "optimizer": {
    "type": "AdamW",
    "params": {
      "lr": 1e-4,
      "betas": [0.9, 0.999],
      "weight_decay": 0.01
    }
  }
}
```

### DeepSpeed Training

```python
import deepspeed

def main():
    # Initialize DeepSpeed
    model = MyModel()
    model_engine, optimizer, _, _ = deepspeed.initialize(
        model=model,
        model_parameters=model.parameters(),
        config="deepspeed_config.json",
    )

    for batch in dataloader:
        # Forward pass
        outputs = model_engine(batch["input"])
        loss = criterion(outputs, batch["target"])

        # Backward pass (handled by DeepSpeed)
        model_engine.backward(loss)

        # Optimizer step (handled by DeepSpeed)
        model_engine.step()
```

### ZeRO Stages

```
ZeRO-1: Optimizer state partitioning
ZeRO-2: + Gradient partitioning
ZeRO-3: + Parameter partitioning (most memory efficient)
```

```json
// ZeRO Stage 3
{
  "zero_optimization": {
    "stage": 3,
    "offload_param": {
      "device": "cpu",
      "pin_memory": true
    },
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    },
    "stage3_gather_16bit_weights_on_model_save": true
  }
}
```

## Model Parallelism

### Tensor Parallelism (TP)

```python
# Using Megatron-LM style
class ColumnParallelLinear(nn.Module):
    """Linear layer with column-parallel weight."""

    def __init__(self, in_features, out_features, world_size, rank):
        super().__init__()
        self.out_features_per_partition = out_features // world_size
        self.weight = nn.Parameter(
            torch.randn(self.out_features_per_partition, in_features)
        )

    def forward(self, x):
        # Each GPU computes part of output
        return F.linear(x, self.weight)

class RowParallelLinear(nn.Module):
    """Linear layer with row-parallel weight."""

    def __init__(self, in_features, out_features, world_size, rank):
        super().__init__()
        self.in_features_per_partition = in_features // world_size
        self.weight = nn.Parameter(
            torch.randn(out_features, self.in_features_per_partition)
        )

    def forward(self, x):
        # Input is split, compute partial output, then all-reduce
        output = F.linear(x, self.weight)
        dist.all_reduce(output)
        return output
```

### Pipeline Parallelism (PP)

```python
from torch.distributed.pipeline.sync import Pipe

# Split model into stages
class Stage1(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(...)

    def forward(self, x):
        return self.layers(x)

class Stage2(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(...)

    def forward(self, x):
        return self.layers(x)

# Create pipeline
model = nn.Sequential(Stage1(), Stage2())
model = Pipe(model, chunks=8)  # Micro-batches
```

## Memory Profiling

### Track Memory Usage

```python
def log_memory(stage: str):
    """Log GPU memory usage."""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1e9
        reserved = torch.cuda.memory_reserved() / 1e9
        max_allocated = torch.cuda.max_memory_allocated() / 1e9
        print(f"[{stage}] Allocated: {allocated:.2f}GB, "
              f"Reserved: {reserved:.2f}GB, Max: {max_allocated:.2f}GB")

# Use in training
log_memory("before forward")
output = model(input)
log_memory("after forward")
loss.backward()
log_memory("after backward")
```

### PyTorch Profiler

```python
from torch.profiler import profile, ProfilerActivity, tensorboard_trace_handler

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
    on_trace_ready=tensorboard_trace_handler("./log/profiler"),
    record_shapes=True,
    profile_memory=True,
    with_stack=True,
) as prof:
    for step, batch in enumerate(dataloader):
        output = model(batch)
        loss.backward()
        optimizer.step()
        prof.step()
```

## Optimization Checklist

### Memory Reduction
- [ ] Enable mixed precision (bf16/fp16)
- [ ] Enable gradient checkpointing
- [ ] Use gradient accumulation
- [ ] Enable memory-efficient attention
- [ ] Reduce batch size if needed
- [ ] Use CPU offloading for optimizer states

### Speed Optimization
- [ ] Use torch.compile()
- [ ] Enable cuDNN benchmark
- [ ] Use DataLoader with num_workers > 0
- [ ] Use pin_memory=True
- [ ] Minimize CPU-GPU transfers
- [ ] Use non-blocking transfers

### Scaling
- [ ] Start with DDP for multi-GPU
- [ ] Use FSDP for large models
- [ ] Consider DeepSpeed for very large models
- [ ] Profile before optimizing

## Common Memory Estimates

| Model Size | Parameters | FP32 Memory | FP16 Memory | Training Memory* |
|------------|------------|-------------|-------------|------------------|
| 1B | 1B | 4GB | 2GB | ~20GB |
| 7B | 7B | 28GB | 14GB | ~100GB |
| 13B | 13B | 52GB | 26GB | ~200GB |
| 70B | 70B | 280GB | 140GB | ~1TB |

*Training memory includes gradients, optimizer states, activations
