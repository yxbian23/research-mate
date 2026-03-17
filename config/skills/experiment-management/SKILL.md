---
name: experiment-management
description: Use this skill when setting up ML experiment infrastructure. Covers wandb/tensorboard integration, hydra/omegaconf configuration management, experiment reproducibility, and results visualization.
---

# Experiment Management

This skill provides comprehensive guidance for managing machine learning experiments systematically.

## When to Activate

- Setting up experiment tracking
- Configuring hyperparameters with hydra/omegaconf
- Ensuring experiment reproducibility
- Analyzing and visualizing results
- Comparing multiple experiments

## Weights & Biases (wandb) Integration

### Basic Setup

```python
import wandb

# Initialize wandb run
wandb.init(
    project="my-research-project",
    name="exp-001-baseline",
    config={
        "learning_rate": 1e-4,
        "batch_size": 32,
        "epochs": 100,
        "model": "resnet50",
    },
    tags=["baseline", "v1"],
    notes="Initial baseline experiment",
)

# Access config
config = wandb.config
lr = config.learning_rate
```

### Logging Metrics

```python
# Log scalar metrics
wandb.log({
    "train/loss": train_loss,
    "train/accuracy": train_acc,
    "val/loss": val_loss,
    "val/accuracy": val_acc,
    "epoch": epoch,
    "lr": optimizer.param_groups[0]['lr'],
})

# Log with step
wandb.log({"loss": loss}, step=global_step)

# Log histograms
wandb.log({"gradients": wandb.Histogram(gradients)})

# Log images
wandb.log({"samples": [wandb.Image(img) for img in images]})

# Log tables
table = wandb.Table(columns=["id", "prediction", "target"])
for i, (pred, target) in enumerate(zip(predictions, targets)):
    table.add_data(i, pred, target)
wandb.log({"predictions": table})
```

### Model Checkpointing

```python
# Save model artifact
artifact = wandb.Artifact(
    name=f"model-{wandb.run.id}",
    type="model",
    description="Trained model checkpoint",
)
artifact.add_file("model.pt")
wandb.log_artifact(artifact)

# Load model artifact
artifact = wandb.use_artifact("model-abc123:latest")
artifact_dir = artifact.download()
model.load_state_dict(torch.load(f"{artifact_dir}/model.pt"))
```

### Hyperparameter Sweeps

```python
# sweep_config.yaml
sweep_config = {
    "method": "bayes",  # or "random", "grid"
    "metric": {"name": "val/loss", "goal": "minimize"},
    "parameters": {
        "learning_rate": {"distribution": "log_uniform_values", "min": 1e-5, "max": 1e-2},
        "batch_size": {"values": [16, 32, 64]},
        "optimizer": {"values": ["adam", "sgd"]},
    },
}

# Create sweep
sweep_id = wandb.sweep(sweep_config, project="my-project")

# Run sweep agent
def train():
    wandb.init()
    config = wandb.config
    # Training code using config
    wandb.finish()

wandb.agent(sweep_id, train, count=50)
```

## Hydra Configuration Management

### Basic Setup

```yaml
# config/config.yaml
defaults:
  - model: resnet50
  - dataset: imagenet
  - optimizer: adam
  - _self_

training:
  epochs: 100
  batch_size: 32
  seed: 42

logging:
  wandb_project: "my-project"
  log_every: 100
```

```yaml
# config/model/resnet50.yaml
name: resnet50
num_classes: 1000
pretrained: true
```

```yaml
# config/optimizer/adam.yaml
name: adam
lr: 1e-4
weight_decay: 0.01
betas: [0.9, 0.999]
```

### Using Hydra in Code

```python
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg: DictConfig):
    # Print resolved config
    print(OmegaConf.to_yaml(cfg))

    # Access config values
    lr = cfg.optimizer.lr
    epochs = cfg.training.epochs

    # Create model
    model = create_model(cfg.model)

    # Training
    train(model, cfg)

if __name__ == "__main__":
    main()
```

### Command Line Overrides

```bash
# Override single value
python train.py training.epochs=200

# Override nested value
python train.py optimizer.lr=1e-3

# Switch config groups
python train.py model=vit optimizer=sgd

# Multi-run (sweep)
python train.py --multirun optimizer.lr=1e-3,1e-4,1e-5
```

### OmegaConf Resolvers

```python
from omegaconf import OmegaConf

# Custom resolver
OmegaConf.register_new_resolver("mul", lambda x, y: x * y)

# In config.yaml:
# effective_batch_size: ${mul:${batch_size},${num_gpus}}
```

## TensorBoard Integration

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter(log_dir=f"runs/{exp_name}")

# Log scalars
writer.add_scalar("Loss/train", train_loss, epoch)
writer.add_scalar("Loss/val", val_loss, epoch)

# Log multiple scalars
writer.add_scalars("Loss", {"train": train_loss, "val": val_loss}, epoch)

# Log histograms
for name, param in model.named_parameters():
    writer.add_histogram(f"params/{name}", param, epoch)
    if param.grad is not None:
        writer.add_histogram(f"grads/{name}", param.grad, epoch)

# Log images
img_grid = torchvision.utils.make_grid(images)
writer.add_image("samples", img_grid, epoch)

# Log model graph
writer.add_graph(model, sample_input)

# Log hyperparameters
writer.add_hparams(
    {"lr": lr, "batch_size": bs},
    {"val_loss": val_loss, "val_acc": val_acc}
)

writer.close()
```

## Reproducibility

### Seed Everything

```python
import random
import numpy as np
import torch

def seed_everything(seed: int):
    """Set all random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # For deterministic behavior
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    # Set environment variable
    os.environ['PYTHONHASHSEED'] = str(seed)

# Use in training
seed_everything(cfg.training.seed)
```

### Log Environment Info

```python
import subprocess
import sys

def log_environment():
    """Log environment information for reproducibility."""
    env_info = {
        "python_version": sys.version,
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "cudnn_version": torch.backends.cudnn.version(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A",
        "git_commit": subprocess.getoutput("git rev-parse HEAD"),
        "git_branch": subprocess.getoutput("git rev-parse --abbrev-ref HEAD"),
    }
    return env_info

# Log to wandb
wandb.config.update({"environment": log_environment()})
```

### Configuration Checksums

```python
import hashlib
from omegaconf import OmegaConf

def config_hash(cfg: DictConfig) -> str:
    """Generate hash of configuration for experiment ID."""
    config_str = OmegaConf.to_yaml(cfg, sort_keys=True)
    return hashlib.md5(config_str.encode()).hexdigest()[:8]

# Use in experiment naming
exp_name = f"{cfg.model.name}_{config_hash(cfg)}"
```

## Experiment Organization

### Directory Structure

```
experiments/
├── configs/
│   ├── config.yaml
│   ├── model/
│   ├── optimizer/
│   └── dataset/
├── outputs/                    # Hydra outputs
│   └── 2024-01-15/
│       └── 14-30-00/
│           ├── .hydra/
│           ├── train.log
│           └── checkpoints/
├── wandb/                      # W&B local files
├── results/
│   └── exp-001/
│       ├── metrics.json
│       ├── predictions.csv
│       └── figures/
└── scripts/
    ├── train.py
    └── evaluate.py
```

### Experiment Registry

```python
import json
from datetime import datetime
from pathlib import Path

class ExperimentRegistry:
    """Track all experiments."""

    def __init__(self, registry_path: str = "experiments/registry.json"):
        self.registry_path = Path(registry_path)
        self.registry = self._load()

    def _load(self):
        if self.registry_path.exists():
            return json.loads(self.registry_path.read_text())
        return {}

    def _save(self):
        self.registry_path.write_text(json.dumps(self.registry, indent=2))

    def register(self, exp_id: str, config: dict, notes: str = ""):
        self.registry[exp_id] = {
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "notes": notes,
            "status": "running",
        }
        self._save()

    def complete(self, exp_id: str, metrics: dict):
        self.registry[exp_id]["status"] = "completed"
        self.registry[exp_id]["metrics"] = metrics
        self._save()
```

## Results Analysis

### Compare Experiments

```python
import pandas as pd
import wandb

api = wandb.Api()

# Get runs from project
runs = api.runs("username/project-name")

# Convert to DataFrame
data = []
for run in runs:
    row = {
        "name": run.name,
        "state": run.state,
        **run.config,
        **run.summary._json_dict,
    }
    data.append(row)

df = pd.DataFrame(data)

# Filter and sort
best_runs = df[df["state"] == "finished"].sort_values("val_loss").head(10)
print(best_runs[["name", "lr", "batch_size", "val_loss", "val_acc"]])
```

### Generate Comparison Table

```python
def generate_latex_table(experiments: list[dict]) -> str:
    """Generate LaTeX table from experiments."""
    headers = ["Model", "LR", "Batch", "Val Loss", "Val Acc"]

    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Experiment comparison}",
        "\\begin{tabular}{" + "l" * len(headers) + "}",
        "\\toprule",
        " & ".join(headers) + " \\\\",
        "\\midrule",
    ]

    for exp in experiments:
        row = [
            exp["model"],
            f"{exp['lr']:.0e}",
            str(exp["batch_size"]),
            f"{exp['val_loss']:.4f}",
            f"{exp['val_acc']:.2%}",
        ]
        lines.append(" & ".join(row) + " \\\\")

    lines.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ])

    return "\n".join(lines)
```

## Best Practices

1. **Version control configs** alongside code
2. **Use meaningful experiment names** with timestamps
3. **Log everything** needed for reproduction
4. **Automate sweep** for hyperparameter search
5. **Tag experiments** for easy filtering
6. **Save checkpoints** at regular intervals
7. **Document failed experiments** too
8. **Use config inheritance** to avoid duplication
9. **Set seeds deterministically** for reproducibility
10. **Archive completed experiments** periodically
