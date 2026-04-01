#!/usr/bin/env bash
# Commit all changes and push to origin/main. Use when you want a one-step sync.
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "${1:-chore: sync local changes}"
fi
git push origin "$(git branch --show-current)"
