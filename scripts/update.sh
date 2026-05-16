#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
SKILLS_DST="$HOME/.claude/skills"

echo "Pulling latest changes..."
git -C "$REPO_ROOT" pull

echo "Cleaning up broken symlinks..."
broken=0
for link in "$SKILLS_DST"/*/; do
    link="${link%/}"
    if [[ -L "$link" ]] && [[ ! -e "$link" ]]; then
        link_target="$(readlink "$link")"
        if [[ "$link_target" == "$SKILLS_SRC"* ]]; then
            echo "  Removing broken symlink: $(basename "$link")"
            rm "$link"
            broken=$((broken + 1))
        fi
    fi
done

[[ $broken -gt 0 ]] && echo "Removed $broken broken symlink(s)." || echo "No broken symlinks."

echo "Update complete."
