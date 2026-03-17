#!/usr/bin/env bash
# ResearchMate — Sync upstream third-party tools
# Usage: ./sync-upstream.sh [tool-name]
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"

# Tool registry (bash 3.x compatible)
get_tool_info() {
    case "$1" in
        aris)                    echo "https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git main" ;;
        autoresearch)            echo "https://github.com/karpathy/autoresearch.git master" ;;
        pi-autoresearch)         echo "https://github.com/davebcn87/pi-autoresearch.git main" ;;
        claude-review-loop)      echo "https://github.com/hamelsmu/claude-review-loop.git main" ;;
        academic-research-skills) echo "https://github.com/Imbad0202/academic-research-skills.git main" ;;
        claude-scientific-skills) echo "https://github.com/K-Dense-AI/claude-scientific-skills.git main" ;;
        *) return 1 ;;
    esac
}

ALL_TOOLS="aris autoresearch pi-autoresearch claude-review-loop academic-research-skills claude-scientific-skills"

sync_tool() {
    local name="$1"
    local info
    info="$(get_tool_info "$name")" || { echo "Unknown tool: $name"; return 1; }
    local url="${info% *}"
    local branch="${info#* }"
    local prefix="third-party/${name}"

    echo "--- Syncing ${name} (${branch}) ---"

    if [[ ! -d "$prefix" ]]; then
        echo "  Warning: ${prefix} not found, skipping."
        return 0
    fi

    if git subtree pull --prefix="$prefix" "$url" "$branch" --squash -m "chore: sync upstream ${name}" 2>&1; then
        echo "  Done."
    else
        echo "  Warning: sync failed (possible conflict). Resolve manually."
        return 1
    fi
}

if [[ $# -gt 0 ]]; then
    tool="$1"
    sync_tool "$tool"
else
    echo "=== Syncing all upstream tools ==="
    failed=""
    for tool in $ALL_TOOLS; do
        sync_tool "$tool" || failed="$failed $tool"
    done

    echo ""
    if [[ -n "$failed" ]]; then
        echo "Failed:$failed"
        echo "Resolve conflicts manually, then commit."
        exit 1
    else
        echo "All tools synced successfully."
    fi
fi
