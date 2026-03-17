# ResearchMate Update

Update ResearchMate itself and re-run setup to apply changes.

## Usage

When the user runs `/research-mate-update`, do the following:

1. Identify the ResearchMate repo location by checking where `~/.claude/agents` symlink points to, then navigate to its parent's parent directory (the repo root).
2. Run `git pull --ff-only` to get the latest changes.
3. Run `./setup.sh` to re-apply configuration (idempotent).
4. Report what changed: new skills, updated tools, etc.

## Example

```
User: /research-mate-update
Claude: [pulls latest changes and re-runs setup]
  Updated: 3 files changed
  New skills: 2 added from ARIS update
  All configurations re-applied successfully.
```
