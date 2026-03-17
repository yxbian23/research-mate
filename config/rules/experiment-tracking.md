# Experiment Tracking Rules

## Mandatory Logging

### ALWAYS Log These Items

Every experiment MUST record:

1. **Configuration** - Full hyperparameter config
2. **Seeds** - All random seeds used
3. **Git Commit** - Code version
4. **Environment** - Python, PyTorch, CUDA versions
5. **Hardware** - GPU type and count

```python
def log_experiment_metadata(config):
    """Log mandatory experiment metadata."""
    import subprocess
    import platform

    wandb.config.update({
        # Full config
        "config": config,

        # Code version
        "git_commit": subprocess.getoutput("git rev-parse HEAD"),
        "git_branch": subprocess.getoutput("git rev-parse --abbrev-ref HEAD"),
        "git_dirty": subprocess.getoutput("git status --porcelain") != "",

        # Environment
        "python_version": platform.python_version(),
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda,

        # Hardware
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A",
        "gpu_count": torch.cuda.device_count(),
    })
```

## Metric Logging Standards

### Log Training Metrics

ALWAYS log at regular intervals:

```python
def log_training_step(step, loss, lr, grad_norm=None):
    """Log training metrics."""
    metrics = {
        "train/loss": loss,
        "train/lr": lr,
        "train/step": step,
    }
    if grad_norm is not None:
        metrics["train/grad_norm"] = grad_norm

    wandb.log(metrics, step=step)
```

### Log Validation Metrics

ALWAYS log validation after each eval:

```python
def log_validation(step, metrics):
    """Log validation metrics."""
    wandb.log({
        f"val/{k}": v for k, v in metrics.items()
    }, step=step)
```

### Log with Proper Step

ALWAYS use global step, not epoch:

```python
# CORRECT - use global step
wandb.log({"loss": loss}, step=global_step)

# WRONG - inconsistent x-axis
wandb.log({"loss": loss})  # Auto-increments
```

## Checkpoint Rules

### Save Best and Last

ALWAYS save both best model and last checkpoint:

```python
class CheckpointManager:
    def __init__(self, save_dir, metric_name="val_loss", mode="min"):
        self.save_dir = Path(save_dir)
        self.metric_name = metric_name
        self.mode = mode
        self.best_value = float('inf') if mode == "min" else float('-inf')

    def save(self, model, optimizer, scheduler, epoch, step, metrics):
        # Always save last
        self._save_checkpoint(
            model, optimizer, scheduler, epoch, step,
            self.save_dir / "last.pt"
        )

        # Save best if improved
        current = metrics[self.metric_name]
        is_best = (self.mode == "min" and current < self.best_value) or \
                  (self.mode == "max" and current > self.best_value)

        if is_best:
            self.best_value = current
            self._save_checkpoint(
                model, optimizer, scheduler, epoch, step,
                self.save_dir / "best.pt"
            )
            print(f"New best {self.metric_name}: {current:.4f}")
```

### Log Checkpoints as Artifacts

ALWAYS log important checkpoints to wandb:

```python
def log_checkpoint_artifact(checkpoint_path, name="model"):
    """Log checkpoint as wandb artifact."""
    artifact = wandb.Artifact(
        name=f"{name}-{wandb.run.id}",
        type="model",
    )
    artifact.add_file(checkpoint_path)
    wandb.log_artifact(artifact)
```

## Naming Conventions

### Run Naming

Use descriptive, searchable run names:

```python
def create_run_name(config):
    """Create descriptive run name."""
    return f"{config.model_name}-lr{config.lr}-bs{config.batch_size}-{config.seed}"

# Example: llama7b-lr1e4-bs32-42
```

### Tagging

ALWAYS tag experiments for filtering:

```python
wandb.init(
    project="my-project",
    name=run_name,
    tags=[
        "baseline",           # Experiment type
        f"model:{config.model_name}",  # Model
        f"dataset:{config.dataset}",   # Dataset
        "v1",                 # Version
    ]
)
```

## Experiment Organization

### Project Structure

Organize experiments by project:

```
wandb projects:
- project-baselines     # Initial experiments
- project-ablations     # Ablation studies
- project-final         # Final results for paper
```

### Group Related Runs

Group related experiments:

```python
wandb.init(
    project="my-project",
    group="ablation-lr",  # Groups related runs
    job_type="train",     # train, eval, sweep
)
```

## Reproducibility Requirements

### Save Config to File

ALWAYS save config alongside checkpoint:

```python
def save_experiment(save_dir, config, model, results):
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    # Save config
    with open(save_dir / "config.yaml", "w") as f:
        yaml.dump(asdict(config), f)

    # Save results
    with open(save_dir / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Save model
    torch.save(model.state_dict(), save_dir / "model.pt")
```

### Document Deviations

ALWAYS note any deviations from standard config:

```python
wandb.config.update({
    "notes": "Reduced batch size due to memory constraints",
    "deviations": ["batch_size: 16 -> 8"],
})
```

## Tracking Checklist

Before starting experiment:
- [ ] wandb initialized with proper project/name/tags
- [ ] Full config logged
- [ ] Git commit logged
- [ ] Environment logged

During training:
- [ ] Loss logged every N steps
- [ ] Validation metrics logged after each eval
- [ ] Learning rate logged
- [ ] Gradient norm logged (optional)

After training:
- [ ] Best checkpoint saved and logged as artifact
- [ ] Final results logged
- [ ] Run marked as finished

For paper:
- [ ] Results can be reproduced from logged config
- [ ] Checkpoint artifacts available
- [ ] All hyperparameters documented
