# Add Tool

Add a new third-party tool to ResearchMate via git subtree.

## Usage

When the user runs `/add-tool`, do the following:

1. Identify the ResearchMate repo location by checking where `~/.claude/agents` symlink points to, then navigate to its parent's parent directory (the repo root).
2. Ask the user for:
   - **name**: Short name for the tool (e.g., `my-tool`)
   - **git URL**: The upstream repository URL
   - **branch**: Branch to track (default: `main`)
3. Run `./add-tool.sh <name> <git-url> [branch]` from the repo root.
4. After adding, remind the user to:
   - Update `sync-upstream.sh` with the new tool's registry entry
   - Update `setup.sh` if the tool has skills/commands to install
   - Run `./setup.sh` to activate the new tool
5. Optionally, help the user make these updates automatically.

## Example

```
User: /add-tool
Claude: What's the tool name, git URL, and branch?
User: my-tool https://github.com/user/repo.git main
Claude: [runs ./add-tool.sh and guides next steps]
```
