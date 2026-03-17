<div align="center">

**English** | [中文](README_CN.md)

# ResearchMate

**One-click Claude Code toolkit for AI researchers**

*Your config + 6 curated tools in one repo. One-click deploy. Customize freely. Auto-sync upstream.*

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
- Works with any combination: no Claude/Codex, either one, or both installed

## Configuration

### API Keys

Edit `~/.research-mate/.env` to configure API keys:

| Key | Required? | Purpose |
|-----|-----------|---------|
| `ANTHROPIC_API_KEY` | For auto-review | GitHub Actions PR auto-review via Claude |
| `OPENAI_API_KEY` | For ARIS | Cross-model adversarial review (Codex MCP) |
| `LLM_API_KEY` | For ARIS | LLM-chat MCP (DeepSeek / Kimi / MiniMax) |
| `LLM_API_BASE` | With LLM_API_KEY | API base URL for LLM-chat |
| `MINIMAX_API_KEY` | For ARIS | MiniMax-chat MCP |
| `HF_TOKEN` | For models | Hugging Face model downloads |
| `WANDB_API_KEY` | For tracking | Weights & Biases experiment tracking |

> When running via `curl | bash`, the API key prompt is skipped automatically.
> Configure keys afterwards as described below.

### Post-Install Setup

If you skipped API key configuration during install (e.g., via `curl | bash`):

```bash
# 1. Edit .env and add your keys
vim ~/.research-mate/.env

# 2. Re-run setup to register MCP servers
cd ~/.research-mate && ./setup.sh
```

`setup.sh` is idempotent — it reads `.env`, detects newly added keys, and registers the corresponding MCP servers (LLM-chat, MiniMax) without affecting existing config.

Alternatively, register MCP servers manually:

```bash
# LLM-chat MCP (requires LLM_API_KEY in .env)
claude mcp add llm-chat -s user -- python3 ~/.research-mate/third-party/aris/mcp-servers/llm-chat/server.py

# MiniMax MCP (requires MINIMAX_API_KEY in .env)
claude mcp add minimax-chat -s user -- python3 ~/.research-mate/third-party/aris/mcp-servers/minimax-chat/server.py
```

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

| Feature | Type | Source | Description |
|---------|------|--------|-------------|
| `/idea-discovery` | Skill | ARIS | Literature survey → brainstorm → novelty check → GPU pilot |
| `/research-pipeline` | Skill | ARIS | End-to-end: idea → implement → review → submit |
| `/autoresearch` | Skill | config | Karpathy-style autonomous ML experiments |
| `/autoresearch-loop` | Skill | config | Domain-agnostic autonomous optimization loop |
| `/implement-paper` | Command | config | Extract algorithms from papers → PyTorch code |
| `/analyze-paper` | Command | config | Deep analysis of AI papers → structured report |
| Codex / LLM-chat / MiniMax | MCP | ARIS | Cross-model adversarial review |

### Paper Writing

| Feature | Type | Source | Description |
|---------|------|--------|-------------|
| `/paper-writing` | Skill | ARIS | Narrative → outline → figures → LaTeX → PDF |
| `/paper-plan` `/paper-write` `/paper-figure` `/paper-compile` | Skill | ARIS | Individual paper pipeline stages |
| `/auto-paper-improvement-loop` | Skill | ARIS | Autonomous review → fix → recompile (2 rounds) |
| `/academic-paper` | Skill | academic-research | 12-agent writing system + bilingual abstracts |
| `/research-paper-workflow` | Skill | config | Paper structure, LaTeX best practices |
| `/ai-research-slides` | Skill | config | Paper analysis → academic presentation |
| 19 format templates | Skill | scientific-skills | Nature / Science / NeurIPS / ICLR... |

### Literature Review & Peer Review

| Feature | Type | Source | Description |
|---------|------|--------|-------------|
| `/auto-review-loop` | Skill | ARIS | 4-round GPT adversarial review |
| `/research-review` | Skill | ARIS | Deep critical review via Codex MCP |
| `/deep-research` | Skill | academic-research | 13-agent PRISMA literature review |
| `/academic-paper-reviewer` | Skill | academic-research | 7-agent peer review (0-100 scoring) |
| `/academic-pipeline` | Skill | academic-research | 10-stage orchestrator with integrity checks |
| `/review-paper` | Command | config | Generate ICLR/ICML/NeurIPS review comments |

### Experiment Management & Training

| Feature | Type | Source | Description |
|---------|------|--------|-------------|
| `/run-experiment` | Skill | ARIS | Remote GPU deployment + monitoring |
| `/train` | Command | config | GPU check → config validation → launch training |
| `/debug-cuda` | Command | config | CUDA memory / device issue diagnosis |
| `/ablation` | Command | config | Ablation study design and comparison tables |
| `/eval-model` | Command | config | Standard benchmark evaluation (FID/MMLU/VQA) |
| `/benchmark` | Command | config | Run standard ML benchmarks |
| `/experiment-management` | Skill | config | wandb/tensorboard + hydra config management |
| `/gpu-optimization` | Skill | config | Mixed precision, gradient accumulation, parallelism |
| `/pytorch-patterns` | Skill | config | Model architecture, DDP/FSDP, checkpointing |
| `/dataset-processing` | Skill | config | Large-scale data loading, augmentation, streaming |

### Code Review & Quality

| Feature | Type | Source | Description |
|---------|------|--------|-------------|
| `/review-loop` | Command | claude-review-loop | Codex independent review after task completion |
| `/code-review` | Command | config | Code quality and security review |
| `/test-coverage` | Command | config | Test coverage analysis (80%+ target) |
| `/refactor-clean` | Command | config | Dead code identification and safe removal |
| code-reviewer | Agent | config | Code quality review specialist |
| security-reviewer | Agent | config | Security vulnerability detection |

### Scientific Data Access

175 production-ready skills covering 250+ scientific databases and APIs (PubMed, ChEMBL, UniProt, COSMIC, SEC EDGAR, and more). 19 journal/conference paper format templates.

### Office Documents

Skills for PDF, DOCX, PPTX, and XLSX creation, editing, and analysis.

### Maintenance

| Feature | Type | Description |
|---------|------|-------------|
| `/sync-upstream` | Claude Code command | Sync third-party tools with upstream from within Claude |
| `/add-tool` | Claude Code command | Add new third-party tool from within Claude |
| `/research-mate-update` | Claude Code command | Pull latest changes + re-run setup |
| `sync-upstream.sh` | Shell script | Manual sync (all or single tool) |
| `add-tool.sh` | Shell script | Manual add new tool via git subtree |

### Statistics

| Type | Count | Sources |
|------|-------|---------|
| **Skills** | 230+ | config: 24, ARIS: 27, academic: 4, scientific: 175 |
| **Commands** | 25 | config: 23, review-loop: 2 |
| **Agents** | 7 | config |
| **MCP Servers** | 3 | ARIS: Codex, LLM-chat, MiniMax |
| **Rules** | 13 | config |
| **Contexts** | 4 | config |

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
