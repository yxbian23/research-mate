# ML Coding Style

## Model Definition Standards

### Class Structure

```python
class MyModel(nn.Module):
    """
    Brief description of the model.

    Args:
        config: Model configuration
    """
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.config = config
        self._build_layers()

    def _build_layers(self):
        """Initialize model layers."""
        # Layer definitions here

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.

        Args:
            x: Input tensor of shape (batch, ...)
        Returns:
            Output tensor of shape (batch, ...)
        """
        # Forward logic here

    @torch.no_grad()
    def generate(self, x: torch.Tensor) -> torch.Tensor:
        """Inference method - always use @torch.no_grad()."""
        pass
```

### Type Annotations

ALWAYS use type hints for function signatures:

```python
# CORRECT
def train_step(
    model: nn.Module,
    batch: dict[str, torch.Tensor],
    optimizer: torch.optim.Optimizer,
) -> float:
    ...

# WRONG - no types
def train_step(model, batch, optimizer):
    ...
```

## Configuration Management

### Use Dataclasses or Pydantic

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class TrainingConfig:
    """Training configuration."""
    learning_rate: float = 1e-4
    batch_size: int = 32
    num_epochs: int = 100
    seed: int = 42
    gradient_clip: Optional[float] = 1.0
    warmup_steps: int = 1000
```

### Config Validation

ALWAYS validate configurations:

```python
def validate_config(config: TrainingConfig):
    assert config.learning_rate > 0, "Learning rate must be positive"
    assert config.batch_size > 0, "Batch size must be positive"
    if config.gradient_clip is not None:
        assert config.gradient_clip > 0, "Gradient clip must be positive"
```

## Reproducibility Requirements

### Seed Everything

ALWAYS set seeds at training start:

```python
def seed_everything(seed: int):
    """Set all random seeds for reproducibility."""
    import random
    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # Optional: for fully deterministic behavior
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

### Log Everything

ALWAYS log:
- Git commit hash
- Full configuration
- Random seeds
- Hardware info
- Library versions

```python
import subprocess

def log_experiment_info():
    return {
        "git_commit": subprocess.getoutput("git rev-parse HEAD"),
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "config": asdict(config),
        "seed": seed,
    }
```

## Training Loop Standards

### Standard Training Loop

```python
def train_epoch(model, dataloader, optimizer, scheduler, device):
    model.train()
    total_loss = 0

    for batch in tqdm(dataloader, desc="Training"):
        # Move to device
        batch = {k: v.to(device) for k, v in batch.items()}

        # Forward
        optimizer.zero_grad()
        outputs = model(**batch)
        loss = outputs.loss

        # Backward
        loss.backward()

        # Gradient clipping (if configured)
        if config.gradient_clip:
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.gradient_clip)

        # Step
        optimizer.step()
        scheduler.step()

        # Log
        total_loss += loss.item()

    return total_loss / len(dataloader)
```

### Evaluation Mode

ALWAYS use eval mode and no_grad for inference:

```python
@torch.no_grad()
def evaluate(model, dataloader, device):
    model.eval()  # CRITICAL
    # Evaluation logic
```

## Code Organization

### Project Structure

```
project/
├── configs/           # Configuration files
├── data/              # Data processing
├── models/            # Model definitions
│   ├── __init__.py
│   ├── base.py
│   └── components/
├── training/          # Training logic
├── evaluation/        # Evaluation scripts
├── utils/             # Utilities
├── scripts/           # Entry point scripts
└── tests/             # Unit tests
```

### Import Order

```python
# Standard library
import os
import json
from pathlib import Path

# Third party
import numpy as np
import torch
import torch.nn as nn
from transformers import AutoModel

# Local
from models import MyModel
from utils import seed_everything
```

## Code Quality Checklist

Before committing ML code:
- [ ] Type hints on all functions
- [ ] Docstrings with Args/Returns
- [ ] Seeds set for reproducibility
- [ ] Config is validated
- [ ] Proper use of model.train()/model.eval()
- [ ] torch.no_grad() for inference
- [ ] Gradient clipping configured
- [ ] Checkpointing implemented
- [ ] Experiment tracking configured
- [ ] No hardcoded hyperparameters
