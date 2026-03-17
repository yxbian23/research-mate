---
name: autoresearch
description: Autonomous ML research loop inspired by Karpathy's autoresearch. Agent modifies code, trains on single GPU, evaluates metric, keeps or discards, repeats indefinitely. Use when asked to "run autoresearch", "autonomous training loop", or "overnight experiments".
---

# Autoresearch — Autonomous ML Experiment Loop

Adapted from [karpathy/autoresearch](https://github.com/karpathy/autoresearch). Give an AI agent a GPU, let it experiment autonomously overnight.

## Core Concept

The agent modifies training code → trains for a fixed time budget → checks if metric improved → keeps or discards → repeats. The human sleeps, the agent researches.

## Quick Start

To set up autoresearch in the current project:

1. **Copy the reference implementation** (optional, for new projects):
   ```bash
   cp third-party/autoresearch/prepare.py ./
   cp third-party/autoresearch/train.py ./
   cp third-party/autoresearch/pyproject.toml ./
   uv run prepare.py  # one-time data setup
   ```

2. Or **adapt to your existing project** — you need:
   - A training script that trains for a fixed time and outputs a metric
   - A clear metric to optimize (e.g., val_loss, val_bpb, accuracy)

## Setup

1. **Agree on a run tag** with the user (e.g., `mar17`).
2. **Create branch**: `git checkout -b autoresearch/<tag>`
3. **Read source files** to fully understand the codebase.
4. **Initialize results.tsv** with header: `commit\tval_bpb\tmemory_gb\tstatus\tdescription`
5. **Run baseline**: execute the training script as-is, record results.

## The Experiment Loop

**LOOP FOREVER:**

1. Look at git state and past results in results.tsv.
2. Modify the training script with an experimental idea.
3. `git commit` the change.
4. Run: `uv run train.py > run.log 2>&1` (redirect all output).
5. Read results: `grep "^val_bpb:\|^peak_vram_mb:" run.log`
6. If empty → crash. Run `tail -n 50 run.log` for traceback.
7. Log results to results.tsv (do NOT commit this file).
8. If metric improved → keep the commit, advance the branch.
9. If metric equal or worse → `git reset --hard HEAD~1` to revert.

## Rules

- **NEVER STOP.** The user may be asleep. Keep going until manually interrupted.
- **Never ask** "should I continue?" — you are autonomous.
- **Simplicity criterion**: simpler is better. Removing code for equal perf = keep.
- **Crashes**: fix trivial bugs (typos, imports), skip fundamentally broken ideas.
- **Timeout**: if a run exceeds 2x the time budget, kill it and treat as failure.
- **One file**: prefer modifying only the training script to keep diffs reviewable.

## What You CAN Modify

- Model architecture, optimizer, hyperparameters, training loop, batch size, model size.

## What You CANNOT Modify

- Data preparation, evaluation harness, tokenizer, fixed constants.
- Do not install new packages.

## Logging Format (results.tsv)

Tab-separated, 5 columns:
```
commit	val_bpb	memory_gb	status	description
a1b2c3d	0.997900	44.0	keep	baseline
b2c3d4e	0.993200	44.2	keep	increase LR to 0.04
c3d4e5f	1.005000	44.0	discard	switch to GeLU activation
d4e5f6g	0.000000	0.0	crash	double model width (OOM)
```

## Reference

For the complete methodology, see: `third-party/autoresearch/program.md`
For the reference training script: `third-party/autoresearch/train.py`
