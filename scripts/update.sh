#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Pulling latest changes..."
git -C "$REPO_ROOT" pull

bash "$REPO_ROOT/scripts/install.sh" "$@"

echo "Update complete."
