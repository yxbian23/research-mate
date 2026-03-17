#!/usr/bin/env bash
# ResearchMate — Add a new third-party tool via git subtree
# Usage: ./add-tool.sh <name> <git-url> [branch]
set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <name> <git-url> [branch]"
    echo "Example: $0 my-tool https://github.com/user/repo.git main"
    exit 1
fi

NAME="$1"
URL="$2"
BRANCH="${3:-main}"
PREFIX="third-party/${NAME}"

REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"

if [[ -d "$PREFIX" ]]; then
    echo "Error: ${PREFIX} already exists."
    exit 1
fi

echo "Adding ${NAME} from ${URL} (branch: ${BRANCH})..."
git subtree add --prefix="$PREFIX" "$URL" "$BRANCH" --squash

echo ""
echo "Done! Next steps:"
echo "  1. Update sync-upstream.sh to add the new tool's URL"
echo "  2. Update setup.sh if the tool has skills/commands to install"
echo "  3. Run ./setup.sh to activate"
