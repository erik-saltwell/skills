#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
SKILLS_DST="$HOME/.claude/skills"

mkdir -p "$SKILLS_DST"

echo "Installing skills from $SKILLS_SRC → $SKILLS_DST"

installed=0
skipped=0

for category_dir in "$SKILLS_SRC"/*/; do
    [[ -d "$category_dir" ]] || continue
    for skill_dir in "$category_dir"*/; do
        [[ -d "$skill_dir" ]] || continue
        skill_name="$(basename "$skill_dir")"
        target="$SKILLS_DST/$skill_name"

        if [[ -L "$target" ]]; then
            # Overwrite any existing symlink
            ln -sfn "$skill_dir" "$target"
            installed=$((installed + 1))
        elif [[ -e "$target" ]]; then
            # Real directory or file — warn and skip
            echo "  SKIP $skill_name — real directory exists at $target (manual cleanup required)"
            skipped=$((skipped + 1))
        else
            ln -s "$skill_dir" "$target"
            installed=$((installed + 1))
        fi
    done
done

echo "Done. $installed skill(s) installed, $skipped skipped."

# Clean up broken symlinks that point into this repo
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

[[ $broken -gt 0 ]] && echo "Removed $broken broken symlink(s)."

echo "Install complete."
