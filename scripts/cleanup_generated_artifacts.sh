#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Cleaning generated artifacts under: $ROOT_DIR"

remove_dirs=(
  "__pycache__"
  ".pytest_cache"
  "human_agent.egg-info"
  "build"
  "dist"
  "htmlcov"
)

for name in "${remove_dirs[@]}"; do
  find . -type d -name "$name" -prune -print0 | while IFS= read -r -d '' path; do
    rm -rf "$path"
    printf 'removed dir: %s\n' "$path"
  done
done

find . -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '.coverage' -o -name '.DS_Store' \) -print0 | while IFS= read -r -d '' path; do
  rm -f "$path"
  printf 'removed file: %s\n' "$path"
done

echo "Workspace artifact cleanup complete."
