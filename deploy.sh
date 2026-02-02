#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v git >/dev/null 2>&1; then
  echo "git not found. Please install git." >&2
  exit 1
fi

if [ -z "$(git status --porcelain)" ]; then
  echo "No changes to deploy."
  exit 0
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
MESSAGE="${1:-deploy: $(date "+%Y-%m-%d %H:%M:%S")}" 

git add -A

git commit -m "$MESSAGE"

git push origin "$BRANCH"

echo "Deployed to origin/$BRANCH"
