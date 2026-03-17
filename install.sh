#!/usr/bin/env bash
# ResearchMate — One-line installer (macOS + Linux)
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/yxbian23/research-mate/main/install.sh | bash
#   curl -fsSL ... | bash -s -- --claude-path /path/to/claude
#   curl -fsSL ... | bash -s -- --claude-path /path/to/claude --codex-path /path/to/codex
set -euo pipefail

INSTALL_DIR="${HOME}/.research-mate"
REPO_URL="https://github.com/yxbian23/research-mate.git"

# Parse arguments
export CLAUDE_BIN="" CODEX_BIN=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --claude-path) CLAUDE_BIN="$2"; shift 2 ;;
        --codex-path)  CODEX_BIN="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# Auto-detect if not specified
if [[ -z "$CLAUDE_BIN" ]]; then
    CLAUDE_BIN="$(command -v claude 2>/dev/null || true)"
fi
if [[ -z "$CODEX_BIN" ]]; then
    CODEX_BIN="$(command -v codex 2>/dev/null || true)"
fi

echo ""
echo "  ResearchMate Installer"
echo "  ======================"
if [[ -n "$CLAUDE_BIN" ]]; then
    echo "  Claude: $CLAUDE_BIN"
else
    echo "  Claude: not found (will auto-install)"
fi
if [[ -n "$CODEX_BIN" ]]; then
    echo "  Codex:  $CODEX_BIN"
else
    echo "  Codex:  not found (will auto-install)"
fi
echo ""

# Check git
if ! command -v git >/dev/null; then
    case "$(uname -s)" in
        Darwin*) echo "Error: git is required. Install with: xcode-select --install" ;;
        Linux*)  echo "Error: git is required. Install with: sudo apt install git (or your package manager)" ;;
        *)       echo "Error: git is required. Please install git first." ;;
    esac
    exit 1
fi

# Clone or update
if [[ -d "$INSTALL_DIR" ]]; then
    echo "  Updating existing installation..."
    cd "$INSTALL_DIR" && git pull --ff-only
else
    echo "  Cloning to ${INSTALL_DIR}..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Run setup (CLAUDE_BIN and CODEX_BIN are exported)
cd "$INSTALL_DIR"
chmod +x setup.sh sync-upstream.sh add-tool.sh
exec ./setup.sh
