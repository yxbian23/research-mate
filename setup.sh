#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="${HOME}/.claude/backup/$(date +%Y%m%d-%H%M%S)"

# ════════════════════════════════════════════
# Claude / Codex binary detection
# ════════════════════════════════════════════
# CLAUDE_BIN / CODEX_BIN can be set by install.sh or environment
if [[ -z "${CLAUDE_BIN:-}" ]]; then
    CLAUDE_BIN="$(command -v claude 2>/dev/null || true)"
fi
if [[ -z "${CODEX_BIN:-}" ]]; then
    CODEX_BIN="$(command -v codex 2>/dev/null || true)"
fi

# ════════════════════════════════════════════
# Platform detection
# ════════════════════════════════════════════
detect_os() {
    case "$(uname -s)" in
        Darwin*) echo "macos" ;;
        Linux*)  echo "linux" ;;
        *)       echo "unknown" ;;
    esac
}

detect_pkg_manager() {
    if command -v brew >/dev/null; then echo "brew"
    elif command -v apt-get >/dev/null; then echo "apt"
    elif command -v dnf >/dev/null; then echo "dnf"
    elif command -v pacman >/dev/null; then echo "pacman"
    else echo "unknown"
    fi
}

sed_inplace() {
    if [[ "$(detect_os)" == "macos" ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

# Generate install hint based on platform
install_hint() {
    local pkg="$1"
    local pm
    pm="$(detect_pkg_manager)"
    case "$pkg" in
        git)
            case "$pm" in
                brew) echo "xcode-select --install" ;;
                apt)  echo "sudo apt install git" ;;
                dnf)  echo "sudo dnf install git" ;;
                pacman) echo "sudo pacman -S git" ;;
                *) echo "install git via your package manager" ;;
            esac ;;
        node|nodejs)
            case "$pm" in
                brew) echo "brew install node" ;;
                apt)  echo "sudo apt install nodejs npm" ;;
                dnf)  echo "sudo dnf install nodejs npm" ;;
                pacman) echo "sudo pacman -S nodejs npm" ;;
                *) echo "https://nodejs.org/" ;;
            esac ;;
        npm)
            echo "comes with node" ;;
        jq)
            case "$pm" in
                brew) echo "brew install jq" ;;
                apt)  echo "sudo apt install jq" ;;
                dnf)  echo "sudo dnf install jq" ;;
                pacman) echo "sudo pacman -S jq" ;;
                *) echo "install jq via your package manager" ;;
            esac ;;
        latexmk)
            case "$pm" in
                brew) echo "brew install --cask mactex" ;;
                apt)  echo "sudo apt install texlive-full" ;;
                dnf)  echo "sudo dnf install texlive-scheme-full" ;;
                pacman) echo "sudo pacman -S texlive-most" ;;
                *) echo "install texlive via your package manager" ;;
            esac ;;
        python3)
            case "$pm" in
                brew) echo "brew install python" ;;
                apt)  echo "sudo apt install python3 python3-pip" ;;
                dnf)  echo "sudo dnf install python3 python3-pip" ;;
                pacman) echo "sudo pacman -S python python-pip" ;;
                *) echo "install python3 via your package manager" ;;
            esac ;;
        claude)
            echo "npm i -g @anthropic-ai/claude-code" ;;
        codex)
            echo "npm i -g @openai/codex" ;;
        *)
            echo "install $pkg" ;;
    esac
}

OS="$(detect_os)"
PKG="$(detect_pkg_manager)"

# ════════════════════════════════════════════
# 0. Check dependencies
# ════════════════════════════════════════════
check_dep() {
    local cmd="$1" required="${2:-true}"
    local hint
    hint="$(install_hint "$cmd")"
    if command -v "$cmd" >/dev/null; then
        echo "  ✓ $cmd"
    elif [[ "$required" == "true" ]]; then
        echo "  ✗ $cmd (required) → $hint"; return 1
    else
        echo "  △ $cmd (optional) → $hint"
    fi
}

echo ""
echo "=== ResearchMate Setup ==="
echo "    Platform: ${OS} (${PKG})"
echo ""
echo "=== Checking dependencies ==="
echo "Core:"
check_dep git
check_dep node
check_dep npm

echo "Recommended:"
if [[ -n "$CLAUDE_BIN" ]]; then
    echo "  ✓ claude ($CLAUDE_BIN)"
else
    echo "  △ claude (optional) → $(install_hint claude)"
fi
if [[ -n "$CODEX_BIN" ]]; then
    echo "  ✓ codex ($CODEX_BIN)"
else
    echo "  △ codex (optional) → $(install_hint codex)"
fi
check_dep jq     false

echo "Paper writing (optional):"
check_dep latexmk false
check_dep python3 false

echo "Autonomous experiments (optional):"
check_dep uv false
echo ""

# ════════════════════════════════════════════
# 1. API key configuration
# ════════════════════════════════════════════
if [[ ! -f "${REPO}/.env" ]]; then
    cp "${REPO}/.env.template" "${REPO}/.env"
    echo "=== API Key Configuration ==="
    echo "Keys are used for GitHub Actions auto-review & ARIS cross-model review."
    echo "You can configure them later in .env. Press Enter to skip."
    echo ""
    read -rp "ANTHROPIC_API_KEY (for Claude review): " ANTHROPIC_KEY
    if [[ -n "$ANTHROPIC_KEY" ]]; then
        sed_inplace "s|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=${ANTHROPIC_KEY}|" "${REPO}/.env"
        echo "  Note: Also add ANTHROPIC_API_KEY to GitHub repo Settings → Secrets"
        echo "  to enable auto-review on sync PRs."
    fi
    echo ""
fi

mkdir -p "${HOME}/.claude" "${HOME}/.claude/skills/learned"

# ════════════════════════════════════════════
# 2. Backup existing config
# ════════════════════════════════════════════
backup_if_exists() {
    local target="$1"
    if [[ (-d "$target" || -f "$target") && ! -L "$target" ]]; then
        mkdir -p "$BACKUP_DIR"
        mv "$target" "${BACKUP_DIR}/$(basename "$target")"
        echo "  Backed up: $(basename "$target") → $BACKUP_DIR/"
    fi
}

# Backup settings.json if not generated by us
if [[ -f "${HOME}/.claude/settings.json" ]]; then
    if ! grep -q '"_generated_by": "ResearchMate"' "${HOME}/.claude/settings.json" 2>/dev/null; then
        backup_if_exists "${HOME}/.claude/settings.json"
    fi
fi

# ════════════════════════════════════════════
# 3. Symlink config directories
# ════════════════════════════════════════════
echo "=== Installing config ==="
for dir in agents rules commands contexts; do
    backup_if_exists "${HOME}/.claude/${dir}"
    ln -sfn "${REPO}/config/${dir}" "${HOME}/.claude/${dir}"
    echo "  ✓ ${dir}/"
done

# ════════════════════════════════════════════
# 4. Install skills (with conflict detection)
# ════════════════════════════════════════════
echo "=== Installing skills ==="
SKILL_REGISTRY=$(mktemp)
CONFLICT_LOG=$(mktemp)
SKILL_COUNT=0
trap "rm -f '$SKILL_REGISTRY' '$CONFLICT_LOG'" EXIT

register_skill() {
    local name="$1" source="$2" from="$3"
    if grep -q "^${name}|" "$SKILL_REGISTRY" 2>/dev/null; then
        local existing
        existing=$(grep "^${name}|" "$SKILL_REGISTRY" | head -1 | cut -d'|' -f2)
        echo "$name: skipped $from (already from $existing)" >> "$CONFLICT_LOG"
        return 1
    fi
    echo "${name}|${from}" >> "$SKILL_REGISTRY"
    SKILL_COUNT=$((SKILL_COUNT + 1))
    ln -sfn "$source" "${HOME}/.claude/skills/${name}"
}

# Priority 1: Your own skills
for skill in "${REPO}"/config/skills/*/; do
    name=$(basename "$skill")
    [[ "$name" == "learned" || "$name" == "README.md" ]] && continue
    register_skill "$name" "$skill" "config/" || true
done

# Priority 2: ARIS skills
for skill in "${REPO}"/third-party/aris/skills/*/; do
    [[ -d "$skill" ]] || continue
    register_skill "$(basename "$skill")" "$skill" "ARIS" || true
done

# Priority 3: academic-research-skills
for skill in "${REPO}"/third-party/academic-research-skills/*/; do
    [[ -d "$skill" && -f "$skill/SKILL.md" ]] || continue
    register_skill "$(basename "$skill")" "$skill" "academic-research-skills" || true
done

# Priority 4: claude-scientific-skills
for skill in "${REPO}"/third-party/claude-scientific-skills/skills/*/; do
    [[ -d "$skill" ]] || continue
    register_skill "$(basename "$skill")" "$skill" "claude-scientific-skills" || true
done

echo "  ✓ ${SKILL_COUNT} skills installed"

if [[ -s "$CONFLICT_LOG" ]]; then
    echo "  ⚠ Conflicts (resolved by priority):"
    while IFS= read -r c; do echo "    - $c"; done < "$CONFLICT_LOG"
fi

# ════════════════════════════════════════════
# 5. claude-review-loop: commands + hook
# ════════════════════════════════════════════
echo "=== Installing claude-review-loop ==="
REVIEW_LOOP="${REPO}/third-party/claude-review-loop/plugins/review-loop"
if [[ -d "$REVIEW_LOOP/commands" ]]; then
    for cmd in "${REVIEW_LOOP}"/commands/*.md; do
        [[ -f "$cmd" ]] || continue
        ln -sfn "$cmd" "${REPO}/config/commands/$(basename "$cmd")"
    done
    echo "  ✓ commands linked"
fi

# ════════════════════════════════════════════
# 6. ARIS: MCP servers + tools
# ════════════════════════════════════════════
echo "=== Installing ARIS components ==="

# Load .env if exists
if [[ -f "${REPO}/.env" ]]; then
    source "${REPO}/.env" 2>/dev/null || true
fi

# Codex MCP
if [[ -n "$CODEX_BIN" ]] && [[ -n "$CLAUDE_BIN" ]]; then
    "$CLAUDE_BIN" mcp add codex -s user -- "$CODEX_BIN" mcp-server 2>/dev/null && \
        echo "  ✓ Codex MCP" || echo "  △ Codex MCP (may already exist)"
else
    echo "  △ Codex MCP skipped (need codex + claude)"
fi

# LLM-chat MCP
if [[ -n "${LLM_API_KEY:-}" ]] && [[ -n "$CLAUDE_BIN" ]]; then
    "$CLAUDE_BIN" mcp add llm-chat -s user -- \
        python3 "${REPO}/third-party/aris/mcp-servers/llm-chat/server.py" 2>/dev/null && \
        echo "  ✓ LLM-chat MCP" || true
else
    echo "  △ LLM-chat MCP skipped (set LLM_API_KEY in .env)"
fi

# MiniMax MCP
if [[ -n "${MINIMAX_API_KEY:-}" ]] && [[ -n "$CLAUDE_BIN" ]]; then
    "$CLAUDE_BIN" mcp add minimax-chat -s user -- \
        python3 "${REPO}/third-party/aris/mcp-servers/minimax-chat/server.py" 2>/dev/null && \
        echo "  ✓ MiniMax MCP" || true
else
    echo "  △ MiniMax MCP skipped (set MINIMAX_API_KEY in .env)"
fi

# arxiv_fetch.py dependencies
if command -v python3 >/dev/null; then
    python3 -m pip install arxiv requests --quiet 2>/dev/null && \
        echo "  ✓ Python deps (arxiv, requests)" || true
fi

# ════════════════════════════════════════════
# 7. Generate settings.json
# ════════════════════════════════════════════
echo "=== Generating settings.json ==="
sed -e "s|__HOME__|${HOME}|g" \
    -e "s|__REPO__|${REPO}|g" \
    "${REPO}/config/settings.json.template" \
    > "${HOME}/.claude/settings.json"
echo "  ✓ settings.json"

# ════════════════════════════════════════════
# 8. Install plugins
# ════════════════════════════════════════════
echo "=== Installing plugins ==="
if [[ -n "$CLAUDE_BIN" ]]; then
    PLUGINS=(
        "document-skills@anthropic-agent-skills"
        "huggingface-skills@claude-plugins-official"
    )
    for plugin in "${PLUGINS[@]}"; do
        "$CLAUDE_BIN" plugin install "$plugin" 2>/dev/null && \
            echo "  ✓ $plugin" || \
            echo "  △ $plugin (may already be installed)"
    done
else
    echo "  Skipped (Claude CLI not found)"
fi

# ════════════════════════════════════════════
# 9. npm dependencies
# ════════════════════════════════════════════
echo "=== Installing npm dependencies ==="
for pkg in "${HOME}"/.claude/skills/*/package.json; do
    [[ -f "$pkg" ]] || continue
    dir="$(dirname "$pkg")"
    (cd "$dir" && npm ci --silent 2>/dev/null) && \
        echo "  ✓ $(basename "$dir")" || true
done

# ════════════════════════════════════════════
# 10. Done
# ════════════════════════════════════════════
if [[ -d "$BACKUP_DIR" ]]; then
    echo ""
    echo "⚠ Existing config backed up to: $BACKUP_DIR"
fi

echo ""
echo "════════════════════════════════════════════"
echo "  ✓ ResearchMate setup complete! (${OS})"
echo "════════════════════════════════════════════"
echo ""
echo "Start:          claude"
echo "Update:         cd ${REPO} && git pull && ./setup.sh"
echo "Sync upstream:  cd ${REPO} && ./sync-upstream.sh"
echo ""
