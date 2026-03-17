# Sync Upstream

Sync third-party tools with their upstream repositories.

## Usage

When the user runs `/sync-upstream`, do the following:

1. Identify the ResearchMate repo location by checking where `~/.claude/agents` symlink points to, then navigate to its parent's parent directory (the repo root).
2. Ask the user which tool to sync, or sync all:
   - `aris` — ARIS (Auto-claude-code-research-in-sleep)
   - `autoresearch` — Karpathy's autoresearch
   - `pi-autoresearch` — Pi-autoresearch
   - `claude-review-loop` — Claude Review Loop
   - `academic-research-skills` — Academic Research Skills
   - `claude-scientific-skills` — Claude Scientific Skills
   - `all` — Sync everything
3. Run `./sync-upstream.sh [tool-name]` from the repo root.
4. Report the results: which tools were synced, any conflicts that need manual resolution.

## Example

```
User: /sync-upstream
Claude: Which tool would you like to sync? (aris / autoresearch / all / ...)
User: all
Claude: [runs ./sync-upstream.sh and reports results]
```
