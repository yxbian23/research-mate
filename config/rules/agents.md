# Agent Orchestration

## Available Agents

Located in `~/.claude/agents/`:

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| planner | Implementation planning | Complex features, refactoring |
| architect | System design | Architectural decisions |
| code-reviewer | Code review | After writing code |
| security-reviewer | Security analysis | Before commits |
| doc-updater | Documentation | Updating docs |
| paper-reviewer | Paper review | Writing peer review comments |
| course-assistant | Course learning | Lecture summaries, homework, exam prep |

## Immediate Agent Usage

No user prompt needed:
1. Complex feature requests → **planner**
2. Code just written/modified → **code-reviewer**
3. Architectural decision → **architect**
4. Security concerns → **security-reviewer**
5. Paper review → **paper-reviewer**

## Parallel Task Execution

ALWAYS use parallel Task execution for independent operations:

```markdown
# GOOD: Parallel execution
Launch 3 agents in parallel:
1. Agent 1: Review model architecture
2. Agent 2: Check security
3. Agent 3: Plan implementation

# BAD: Sequential when unnecessary
First agent 1, then agent 2, then agent 3
```

## Multi-Perspective Analysis

For complex problems, use split role sub-agents:
- Architecture expert
- Security specialist
- Code quality reviewer
- Performance analyzer
