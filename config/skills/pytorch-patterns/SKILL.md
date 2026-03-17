---
name: pytorch-patterns
description: Use this skill when implementing deep learning models with PyTorch. Covers model architecture design, custom layers, mixed precision training, distributed training (DDP/FSDP), gradient checkpointing, and checkpointing.
---

# PyTorch Development Patterns

This skill provides comprehensive guidance for professional PyTorch development, from model design to distributed training.

## When to Activate

- Implementing new neural network architectures
- Setting up training pipelines
- Optimizing training efficiency
- Debugging model issues
- Implementing custom layers or loss functions

## Model Architecture Patterns

### Base Model Template

```python
import torch
import torch.nn as nn
from typing import Optional, Dict, Any

class BaseModel(nn.Module):
    """Base class for all models with common functionality."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self._build_model()

    def _build_model(self):
        """Override in subclass to build architecture."""
        raise NotImplementedError

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass - override in subclass."""
        raise NotImplementedError

    def get_num_params(self, non_embedding: bool = True) -> int:
        """Count parameters."""
        n_params = sum(p.numel() for p in self.parameters())
        if non_embedding and hasattr(self, 'embedding'):
            n_params -= self.embedding.weight.numel()
        return n_params

    @classmethod
    def from_pretrained(cls, path: str, **kwargs):
        """Load pretrained model."""
        checkpoint = torch.load(path, map_location='cpu')
        config = checkpoint['config']
        model = cls(config, **kwargs)
        model.load_state_dict(checkpoint['model'])
        return model

    def save_pretrained(self, path: str):
        """Save model checkpoint."""
        torch.save({
            'config': self.config,
            'model': self.state_dict(),
        }, path)
```

### Transformer Block Pattern

```python
class TransformerBlock(nn.Module):
    """Standard transformer block with pre-norm."""

    def __init__(
        self,
        dim: int,
        num_heads: int,
        mlp_ratio: float = 4.0,
        dropout: float = 0.0,
        attention_dropout: float = 0.0,
    ):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = nn.MultiheadAttention(
            dim, num_heads,
            dropout=attention_dropout,
            batch_first=True
        )
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim, int(dim * mlp_ratio)),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(int(dim * mlp_ratio), dim),
            nn.Dropout(dropout),
        )

    def forward(
        self,
        x: torch.Tensor,
        attn_mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        # Pre-norm attention
        x = x + self.attn(
            self.norm1(x), self.norm1(x), self.norm1(x),
            attn_mask=attn_mask
        )[0]
        # Pre-norm MLP
        x = x + self.mlp(self.norm2(x))
        return x
```

## Custom Layers

### Adaptive Layer Normalization

```python
class AdaLN(nn.Module):
    """Adaptive Layer Normalization for conditioning."""

    def __init__(self, dim: int, cond_dim: int):
        super().__init__()
        self.norm = nn.LayerNorm(dim, elementwise_affine=False)
        self.proj = nn.Linear(cond_dim, dim * 2)

    def forward(self, x: torch.Tensor, cond: torch.Tensor) -> torch.Tensor:
        scale, shift = self.proj(cond).chunk(2, dim=-1)
        return self.norm(x) * (1 + scale) + shift
```

### RMS Normalization

```python
class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization."""

    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rms = torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * rms * self.weight
```

## Custom Loss Functions

### Focal Loss

```python
class FocalLoss(nn.Module):
    """Focal loss for imbalanced classification."""

    def __init__(self, alpha: float = 1.0, gamma: float = 2.0):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(
        self,
        inputs: torch.Tensor,
        targets: torch.Tensor
    ) -> torch.Tensor:
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        return focal_loss.mean()
```

### Contrastive Loss (InfoNCE)

```python
class InfoNCELoss(nn.Module):
    """InfoNCE contrastive loss for representation learning."""

    def __init__(self, temperature: float = 0.07):
        super().__init__()
        self.temperature = temperature

    def forward(
        self,
        query: torch.Tensor,  # (B, D)
        positive: torch.Tensor,  # (B, D)
        negatives: Optional[torch.Tensor] = None,  # (B, N, D) or None for in-batch
    ) -> torch.Tensor:
        # Normalize embeddings
        query = F.normalize(query, dim=-1)
        positive = F.normalize(positive, dim=-1)

        # Positive similarity
        pos_sim = (query * positive).sum(dim=-1, keepdim=True) / self.temperature

        if negatives is None:
            # In-batch negatives
            neg_sim = query @ positive.T / self.temperature
        else:
            negatives = F.normalize(negatives, dim=-1)
            neg_sim = (query.unsqueeze(1) @ negatives.transpose(-1, -2)).squeeze(1)
            neg_sim = neg_sim / self.temperature

        # InfoNCE loss
        logits = torch.cat([pos_sim, neg_sim], dim=-1)
        labels = torch.zeros(query.size(0), dtype=torch.long, device=query.device)
        return F.cross_entropy(logits, labels)
```

## Mixed Precision Training

```python
from torch.cuda.amp import autocast, GradScaler

def train_with_amp(model, dataloader, optimizer, criterion):
    """Training loop with automatic mixed precision."""
    scaler = GradScaler()

    for batch in dataloader:
        optimizer.zero_grad()

        # Forward pass with autocast
        with autocast():
            outputs = model(batch['input'])
            loss = criterion(outputs, batch['target'])

        # Backward pass with gradient scaling
        scaler.scale(loss).backward()

        # Gradient clipping (optional, unscale first)
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        # Optimizer step
        scaler.step(optimizer)
        scaler.update()
```

## Distributed Training (DDP)

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler

def setup_ddp(rank: int, world_size: int):
    """Initialize distributed training."""
    dist.init_process_group(
        backend='nccl',
        init_method='env://',
        world_size=world_size,
        rank=rank
    )
    torch.cuda.set_device(rank)

def cleanup_ddp():
    """Clean up distributed training."""
    dist.destroy_process_group()

def train_ddp(rank: int, world_size: int, config: dict):
    """Main training function for DDP."""
    setup_ddp(rank, world_size)

    # Create model and move to GPU
    model = MyModel(config).to(rank)
    model = DDP(model, device_ids=[rank])

    # Create distributed sampler
    train_sampler = DistributedSampler(
        train_dataset,
        num_replicas=world_size,
        rank=rank,
        shuffle=True
    )
    train_loader = DataLoader(
        train_dataset,
        batch_size=config['batch_size'],
        sampler=train_sampler,
        num_workers=4,
        pin_memory=True
    )

    # Training loop
    for epoch in range(config['epochs']):
        train_sampler.set_epoch(epoch)  # Important for shuffling
        for batch in train_loader:
            # Training step
            pass

    cleanup_ddp()

# Launch with torchrun
# torchrun --nproc_per_node=4 train.py
```

## Gradient Checkpointing

```python
from torch.utils.checkpoint import checkpoint

class CheckpointedModel(nn.Module):
    """Model with gradient checkpointing for memory efficiency."""

    def __init__(self, num_layers: int, dim: int):
        super().__init__()
        self.layers = nn.ModuleList([
            TransformerBlock(dim) for _ in range(num_layers)
        ])
        self.use_checkpoint = False

    def enable_gradient_checkpointing(self):
        self.use_checkpoint = True

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            if self.use_checkpoint and self.training:
                x = checkpoint(layer, x, use_reentrant=False)
            else:
                x = layer(x)
        return x
```

## Checkpoint Management

```python
def save_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: Any,
    epoch: int,
    step: int,
    loss: float,
    path: str,
):
    """Save training checkpoint."""
    checkpoint = {
        'epoch': epoch,
        'step': step,
        'loss': loss,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'scheduler_state_dict': scheduler.state_dict() if scheduler else None,
        'rng_state': torch.get_rng_state(),
        'cuda_rng_state': torch.cuda.get_rng_state_all(),
    }
    torch.save(checkpoint, path)
    print(f"Saved checkpoint to {path}")

def load_checkpoint(
    path: str,
    model: nn.Module,
    optimizer: Optional[torch.optim.Optimizer] = None,
    scheduler: Optional[Any] = None,
) -> dict:
    """Load training checkpoint."""
    checkpoint = torch.load(path, map_location='cpu')

    model.load_state_dict(checkpoint['model_state_dict'])

    if optimizer and 'optimizer_state_dict' in checkpoint:
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    if scheduler and checkpoint.get('scheduler_state_dict'):
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

    # Restore RNG state for reproducibility
    if 'rng_state' in checkpoint:
        torch.set_rng_state(checkpoint['rng_state'])
    if 'cuda_rng_state' in checkpoint:
        torch.cuda.set_rng_state_all(checkpoint['cuda_rng_state'])

    return checkpoint
```

## Weight Initialization

```python
def init_weights(module: nn.Module, std: float = 0.02):
    """Initialize weights for transformer models."""
    if isinstance(module, nn.Linear):
        nn.init.normal_(module.weight, mean=0.0, std=std)
        if module.bias is not None:
            nn.init.zeros_(module.bias)
    elif isinstance(module, nn.Embedding):
        nn.init.normal_(module.weight, mean=0.0, std=std)
    elif isinstance(module, nn.LayerNorm):
        nn.init.ones_(module.weight)
        nn.init.zeros_(module.bias)

# Apply initialization
model.apply(lambda m: init_weights(m, std=0.02))
```

## Performance Tips

1. **Use torch.compile** (PyTorch 2.0+)
   ```python
   model = torch.compile(model, mode='reduce-overhead')
   ```

2. **Enable cuDNN benchmark**
   ```python
   torch.backends.cudnn.benchmark = True
   ```

3. **Use channels_last memory format**
   ```python
   model = model.to(memory_format=torch.channels_last)
   x = x.to(memory_format=torch.channels_last)
   ```

4. **Disable gradient computation for validation**
   ```python
   with torch.no_grad():
       outputs = model(inputs)
   ```

5. **Use pin_memory in DataLoader**
   ```python
   DataLoader(..., pin_memory=True, num_workers=4)
   ```

## Best Practices

1. Always use `torch.no_grad()` for inference
2. Clear GPU cache periodically: `torch.cuda.empty_cache()`
3. Use `model.eval()` for evaluation
4. Profile with `torch.profiler`
5. Use deterministic algorithms for reproducibility
6. Implement proper checkpoint saving/loading
7. Use gradient clipping for training stability
8. Monitor GPU memory usage
