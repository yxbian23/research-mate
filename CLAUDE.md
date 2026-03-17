# ResearchMate

AI researcher's one-click Claude Code toolkit.

## Structure

- `config/` — Claude Code config (agents, rules, commands, skills, contexts, settings.json.template)
- `third-party/` — 6 curated tools (git subtree, independently syncable)
- `install.sh` — `curl | bash` remote installer (supports `--claude-path` / `--codex-path`)
- `setup.sh` — Local setup (idempotent, cross-platform)
- `sync-upstream.sh` — Manual upstream sync
- `add-tool.sh` — Add new third-party tool

## Third-party Tools

| Directory | Upstream | Purpose |
|-----------|----------|---------|
| `third-party/aris/` | wanshuiyin/Auto-claude-code-research-in-sleep | ML research automation |
| `third-party/autoresearch/` | karpathy/autoresearch | Autonomous ML experiments |
| `third-party/pi-autoresearch/` | davebcn87/pi-autoresearch | Domain-agnostic optimization loop |
| `third-party/claude-review-loop/` | hamelsmu/claude-review-loop | Codex code review |
| `third-party/academic-research-skills/` | Imbad0202/academic-research-skills | Academic workflow |
| `third-party/claude-scientific-skills/` | K-Dense-AI/claude-scientific-skills | Scientific databases |

## Daily Operations

- Edit config: `config/` → symlink takes effect immediately
- Edit third-party: `third-party/` → symlink takes effect immediately → commit to this repo
- Sync upstream: `./sync-upstream.sh [tool-name]` or `/sync-upstream` in Claude Code
- Add tool: `./add-tool.sh <name> <url> [branch]` or `/add-tool` in Claude Code
- Update: `git pull && ./setup.sh` or `/research-mate-update` in Claude Code

## Notes

- Do not edit `~/.claude/` files directly (they are symlinks)
- `settings.json.template` → `~/.claude/settings.json` (global hooks & plugins)
- `settings.local.json.template` → `.claude/settings.local.json` (project-level env & permissions)
- `.env` is gitignored (contains API keys)
