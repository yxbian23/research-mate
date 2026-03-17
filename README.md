<div align="center">

# ResearchMate

**One-click Claude Code toolkit for AI researchers**

*Your config + 6 curated third-party tools. Unified management. One-click deploy. Auto-sync upstream.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)]()
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)]()

[Quick Start](#quick-start) · [Integrated Tools](#integrated-tools) · [Feature Catalog](#feature-catalog) · [Usage Guide](#usage-guide)

</div>

---

## Why ResearchMate?

| Pain point | Status quo | ResearchMate |
|------------|-----------|--------------|
| Reconfigure Claude on every new machine | Manual copy, no version control | **One command** sets up everything |
| Want to use multiple community tools | Installed separately, scattered | **6 tools unified** in one repo |
| Community tool gets updated | Fork and manually merge | **GitHub Actions auto-sync** + Claude review |
| Customized a tool, can't sync anymore | Locked out of upstream | **git subtree** -- edit freely, still mergeable |
| Dependency setup takes many steps | Read each README step by step | **Auto-detect** platform, deps, MCP registration |

## Architecture

```
 ResearchMate
 ├── config/                          Your Claude Code config
 │   ├── 7 agents                     (architect, code-reviewer, planner, ...)
 │   ├── 13 rules                     (gpu-safety, ml-coding-style, security, ...)
 │   ├── 25 commands                  (/train, /plan, /review-paper, ...)
 │   ├── 24 skills                    (pytorch-patterns, experiment-management, ...)
 │   ├── 4 contexts                   (research, training, review, dev)
 │   └── settings.json.template
 │
 ├── third-party/                     6 curated tools (git subtree, auto-sync)
 │   ├── Auto-claude-code-research-in-sleep (ARIS)/  27 skills, 3 MCP servers — AI research automation
 │   ├── autoresearch/                program.md + train.py — Autonomous ML iteration on single GPU
 │   ├── pi-autoresearch/             1 skill, 1 extension — Domain-agnostic autonomous optimization loop
 │   ├── claude-review-loop/          2 commands, 1 stop hook — Automated Codex code review
 │   ├── academic-research-skills/    4 skills (13+12+7-agent systems) — Full academic workflow
 │   └── claude-scientific-skills/    175 scientific data source skills — Scientific database access
 │
 ├── install.sh          curl | bash one-liner
 ├── setup.sh            Local setup (idempotent)
 ├── sync-upstream.sh    Manual upstream sync
 └── add-tool.sh         Add new third-party tool
```

## Quick Start

**Supported platforms**: macOS (Homebrew) and Linux (apt / dnf / pacman). `setup.sh` auto-detects your platform.

### One-line install

```bash
curl -fsSL https://raw.githubusercontent.com/yxbian23/research-mate/main/install.sh | bash
```

### Custom binary paths (common on Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/yxbian23/research-mate/main/install.sh | bash -s -- \
  --claude-path /path/to/claude \
  --codex-path /path/to/codex
```

### Or clone manually

```bash
git clone https://github.com/yxbian23/research-mate.git ~/.research-mate
cd ~/.research-mate && ./setup.sh
```

The setup script automatically:
- Checks and reports all dependency status
- Backs up existing `~/.claude/` config (nothing is lost)
- Symlinks config files to `~/.claude/`
- Installs all skills with conflict detection and priority resolution
- Registers MCP servers (Codex, LLM-chat, MiniMax)
- Installs Claude Code plugins (document-skills, huggingface-skills)
- Prompts for API key configuration

## Key Features

| Feature | How it works |
|---------|-------------|
| **One-click install** | `curl \| bash` -- auto-detects platform, Claude path, dependencies |
| **6 curated tools** | Hand-picked third-party tools in one repo, all pre-configured |
| **Auto upstream sync** | GitHub Actions runs weekly + Claude Haiku reviews changes + auto-merge |
| **Free to customize** | Edit any third-party code; git subtree keeps upstream merges clean |
| **Priority conflict resolution** | Same-name skills auto-resolved: your config > ARIS > academic > scientific |
| **Symlink, not copy** | Edit repo files, changes take effect instantly -- no reinstall needed |

## Integrated Tools

### Auto-claude-code-research-in-sleep (ARIS) -- AI Research Automation Engine
> [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) ![GitHub stars](https://img.shields.io/github/stars/wanshuiyin/Auto-claude-code-research-in-sleep?style=flat-square)

27 skills, 3 MCP servers (Codex, LLM-chat, MiniMax). Highlights: cross-model adversarial review (Claude + GPT), idea discovery pipeline, 4-round auto review loop, end-to-end research pipeline.

### autoresearch -- Autonomous ML Experiments
> [karpathy/autoresearch](https://github.com/karpathy/autoresearch) ![GitHub stars](https://img.shields.io/github/stars/karpathy/autoresearch?style=flat-square)

Andrej Karpathy's framework: give an AI agent a single GPU, let it modify code, train, evaluate, keep-or-discard, repeat. Single-file constraint keeps scope auditable.

### pi-autoresearch -- Domain-Agnostic Optimization Loop
> [davebcn87/pi-autoresearch](https://github.com/davebcn87/pi-autoresearch) ![GitHub stars](https://img.shields.io/github/stars/davebcn87/pi-autoresearch?style=flat-square)

Not limited to ML -- optimize any quantifiable metric (build speed, bundle size, test performance). Persistent state across sessions via `autoresearch.jsonl`.

### academic-research-skills -- Academic Workflow System
> [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) ![GitHub stars](https://img.shields.io/github/stars/Imbad0202/academic-research-skills?style=flat-square)

4 skills: deep-research (13-agent PRISMA literature review), academic-paper (12-agent writing system), paper-reviewer (7-agent peer review), academic-pipeline (10-stage orchestrator).

### claude-review-loop -- Automated Code Review
> [hamelsmu/claude-review-loop](https://github.com/hamelsmu/claude-review-loop) ![GitHub stars](https://img.shields.io/github/stars/hamelsmu/claude-review-loop?style=flat-square)

2 commands, 1 stop hook. Triggers Codex for independent review after development. Provides third-party perspective on code quality with iterative feedback loops.

### claude-scientific-skills -- Scientific Data Access
> [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) ![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/claude-scientific-skills?style=flat-square)

175 production-ready skills accessing 250+ data sources (PubMed, ChEMBL, UniProt, COSMIC, SEC EDGAR, and more). 19 journal/conference paper format templates.

## Feature Catalog

### Research Automation

`/idea-discovery` `/research-pipeline` `/novelty-check` `/autoresearch` `/autoresearch-loop` `/run-experiment` `/monitor-experiment` `/analyze-results` `/implement-paper` `/analyze-paper` -- MCP: Codex, LLM-chat.

### Paper Writing

`/paper-writing` `/paper-plan` `/paper-write` `/paper-figure` `/paper-compile` `/auto-paper-improvement-loop` -- plus skills: academic-paper (12-agent system), research-paper-workflow, ai-research-slides. 19 format templates (Nature, Science, NeurIPS, ICLR, ...).

### Literature Review & Peer Review

`/auto-review-loop` `/research-review` `/review-paper` -- plus skills: deep-research (13-agent PRISMA), academic-paper-reviewer (7-agent, 0-100 scoring), academic-pipeline (10-stage orchestrator with integrity checks).

### Experiment Management & Training

`/train` `/checkpoint` `/debug-cuda` `/ablation` `/eval-model` `/benchmark` -- plus skills: experiment-management (wandb/tensorboard + hydra), gpu-optimization (mixed precision, gradient accumulation, model parallelism), pytorch-patterns (DDP/FSDP), dataset-processing.

### Code Review & Quality

`/review-loop` `/code-review` `/test-coverage` `/refactor-clean` -- plus agents: code-reviewer, security-reviewer. Stop hook auto-triggers Codex review on session end.

### Scientific Data Access

175 skills covering 250+ scientific databases and APIs. Ready to query from within Claude Code.

### Office Documents

Skills for PDF, DOCX, PPTX, and XLSX creation, editing, and analysis.

### Maintenance

In-Claude commands: `/sync-upstream` `/add-tool` `/research-mate-update`. Shell scripts: `sync-upstream.sh` `add-tool.sh`.

## Dependencies

`setup.sh` auto-detects your platform and provides install hints.

| Dependency | Required? | macOS | Linux (apt) |
|-----------|-----------|-------|-------------|
| Git | Yes | `xcode-select --install` | `sudo apt install git` |
| Node.js | Yes | `brew install node` | `sudo apt install nodejs npm` |
| Claude Code | Recommended | `npm i -g @anthropic-ai/claude-code` | same |
| Codex CLI | For ARIS | `npm i -g @openai/codex` | same |
| jq | For review-loop | `brew install jq` | `sudo apt install jq` |
| LaTeX | For paper writing | `brew install --cask mactex` | `sudo apt install texlive-full` |
| Python 3 | For literature search | `brew install python` | `sudo apt install python3 python3-pip` |
| uv | For autoresearch | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | same |
| PyTorch | For autoresearch | `pip install torch` | same |

> Fedora (`dnf`) and Arch (`pacman`) are also supported -- `setup.sh` detects them automatically.

## Usage Guide

### Edit your config

```bash
# Edit files in config/ -- symlinks make changes take effect immediately
vim ~/.research-mate/config/rules/my-new-rule.md
git add . && git commit -m "feat: add new rule" && git push
```

### Customize third-party tools

```bash
# Edit directly -- changes are instant, and upstream merges still work
vim ~/.research-mate/third-party/aris/skills/auto-review-loop/SKILL.md
git add . && git commit -m "feat: customize ARIS review loop" && git push
```

### Sync upstream updates

```
# In Claude Code:
/sync-upstream

# Or via shell:
./sync-upstream.sh            # sync all tools
./sync-upstream.sh aris       # sync one tool

# Automatic: GitHub Actions checks weekly, Claude Haiku reviews, auto-merge
```

### Add a new tool

```
# In Claude Code:
/add-tool

# Or via shell:
./add-tool.sh <name> <git-url> [branch]
```

### Update ResearchMate itself

```
# In Claude Code:
/research-mate-update

# Or via shell:
cd ~/.research-mate && git pull && ./setup.sh
```

## Comparison

| Capability | everything-claude-code | dot-claude | starter-kit | **ResearchMate** |
|-----------|:---:|:---:|:---:|:---:|
| Store your own config | ~ | ✅ | ~ | ✅ |
| Integrate multiple third-party tools | ❌ | ❌ | ❌ | ✅ (6 tools) |
| Independent upstream sync per tool | ❌ | ❌ | ~ (one only) | ✅ |
| Local edits still mergeable with upstream | ❌ | N/A | ✅ | ✅ |
| One-click new machine deploy | ✅ | ✅ | ~ | ✅ |
| AI researcher workflows | ❌ | ❌ | ❌ | ✅ |
| Claude auto-reviews sync PRs | ❌ | ❌ | ❌ | ✅ |
| In-Claude maintenance commands | ❌ | ❌ | ❌ | ✅ |

## Design Principles

1. **One-click > Multi-step** -- Everything configurable in a single command, no manual steps
2. **Symlink > Copy** -- Edit repo files, instant effect, no reinstall
3. **Your config > Third-party** -- Same-name conflicts always resolve in favor of your config
4. **Auto > Manual** -- Upstream sync, conflict detection, dependency checks are all automated
5. **Backup > Overwrite** -- Existing config is backed up to `~/.claude/backup/`, nothing is lost

## License

[MIT](LICENSE)

## Acknowledgments

Built on top of these excellent projects:

- [autoresearch](https://github.com/karpathy/autoresearch) by [@karpathy](https://github.com/karpathy)
- [pi-autoresearch](https://github.com/davebcn87/pi-autoresearch) by [@davebcn87](https://github.com/davebcn87)
- [Auto-claude-code-research-in-sleep (ARIS)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) by [@wanshuiyin](https://github.com/wanshuiyin)
- [claude-review-loop](https://github.com/hamelsmu/claude-review-loop) by [@hamelsmu](https://github.com/hamelsmu)
- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) by [@Imbad0202](https://github.com/Imbad0202)
- [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) by [@K-Dense-AI](https://github.com/K-Dense-AI)
