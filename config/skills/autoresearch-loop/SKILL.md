---
name: autoresearch-loop
description: Domain-agnostic autonomous optimization loop. Try ideas, measure results, keep what works, discard what doesn't, repeat forever. Works for any quantifiable metric — ML training, build speed, bundle size, test performance, etc. Use when asked to "optimize X in a loop", "autoresearch for X", or "autonomous optimization".
---

# Autoresearch Loop — Autonomous Optimization

Adapted from [davebcn87/pi-autoresearch](https://github.com/davebcn87/pi-autoresearch). A domain-agnostic optimization loop that works for any quantifiable metric.

## Core Concept

Try an idea → measure it → keep what works → discard what doesn't → repeat forever.

Unlike the ML-specific autoresearch skill, this works for **any** optimization target: build times, bundle size, test speed, inference latency, memory usage, code quality metrics, etc.

## Setup

1. **Ask or infer** from the user:
   - **Goal**: What to optimize (e.g., "reduce build time")
   - **Command**: How to measure it (e.g., `npm run build`)
   - **Metric**: What number to track + direction (e.g., "build time in seconds, lower is better")
   - **Files in scope**: What files the agent may modify
   - **Constraints**: Hard rules (e.g., "tests must pass", "no new dependencies")

2. **Create branch**: `git checkout -b autoresearch/<goal>-<date>`

3. **Read source files** deeply before writing anything.

4. **Create `autoresearch.md`** — the heart of the session:
   ```markdown
   # Autoresearch: <goal>

   ## Objective
   <Specific description of what we're optimizing and the workload.>

   ## Metrics
   - **Primary**: <name> (<unit>, lower/higher is better)
   - **Secondary**: <name>, <name>, ...

   ## How to Run
   `./autoresearch.sh` — outputs METRIC name=number lines.

   ## Files in Scope
   <Every file the agent may modify, with a brief note on what it does.>

   ## Off Limits
   <What must NOT be touched.>

   ## Constraints
   <Hard rules: tests must pass, no new deps, etc.>

   ## What's Been Tried
   <Update this section as experiments accumulate. Note key wins, dead ends,
   and architectural insights so the agent doesn't repeat failed approaches.>
   ```

5. **Create `autoresearch.sh`** — benchmark script:
   ```bash
   #!/bin/bash
   set -euo pipefail
   # Pre-check (fast, <1s)
   <syntax/lint check>
   # Run benchmark
   <actual benchmark command>
   # Output metrics
   echo "METRIC build_time=12.3"
   echo "METRIC bundle_size=450"
   ```

6. **Optional: Create `autoresearch.checks.sh`** — correctness validation:
   ```bash
   #!/bin/bash
   set -euo pipefail
   # Only needed if constraints require correctness checks
   npm test --run 2>&1 | tail -50
   ```

7. **Run baseline** → log results → start looping immediately.

## The Experiment Loop

**LOOP FOREVER:**

1. Review `autoresearch.md` and past results.
2. Modify files in scope with an optimization idea.
3. `git commit` the change.
4. Run `./autoresearch.sh` and capture output.
5. Parse `METRIC` lines from output.
6. If `autoresearch.checks.sh` exists, run it. Failed → log as `checks_failed`, revert.
7. If primary metric improved → **keep** (commit stands).
8. If primary metric equal/worse → **discard** (`git reset --hard HEAD~1`).
9. Update `autoresearch.md` "What's Been Tried" section periodically.

## Rules

- **LOOP FOREVER.** Never ask "should I continue?" — the user expects autonomous work.
- **Primary metric is king.** Improved → keep. Worse/equal → discard.
- **Simpler is better.** Removing code for equal perf = keep.
- **Don't thrash.** Repeatedly reverting the same idea? Try something structurally different.
- **Think longer when stuck.** Re-read source files, study profiling data, reason deeply.
- **Crashes**: fix trivial issues, otherwise log and move on.
- **Resuming**: if `autoresearch.md` exists, read it + git log, continue looping.

## State Files

| File | Purpose | Committed? |
|------|---------|-----------|
| `autoresearch.md` | Living document: goals, constraints, what's been tried | Yes |
| `autoresearch.sh` | Benchmark script | Yes |
| `autoresearch.checks.sh` | Correctness checks (optional) | Yes |
| `autoresearch.jsonl` | Append-only experiment log (one JSON per run) | No |

## JSONL Log Format

Each line in `autoresearch.jsonl`:
```json
{"run": 1, "commit": "a1b2c3d", "status": "keep", "metrics": {"build_time": 12.3}, "description": "baseline"}
{"run": 2, "commit": "b2c3d4e", "status": "keep", "metrics": {"build_time": 11.1}, "description": "enable parallel compilation"}
{"run": 3, "commit": "c3d4e5f", "status": "discard", "metrics": {"build_time": 13.0}, "description": "switch to esbuild"}
```

## Reference

For the original implementation: `third-party/pi-autoresearch/skills/autoresearch-create/SKILL.md`
