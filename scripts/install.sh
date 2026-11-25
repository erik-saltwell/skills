#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
INSTALL_ROOT="${SKILLS_INSTALL_ROOT:-$HOME}"
agent=all
category=

usage() {
    echo "Usage: $0 [--agent all|claude|codex|gemini] [--category NAME]"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent|--category)
            [[ $# -ge 2 && -n "$2" ]] || { usage >&2; exit 1; }
            if [[ "$1" == --agent ]]; then agent="$2"; else category="$2"; fi
            shift 2
            ;;
        -h|--help) usage; exit 0 ;;
        *) usage >&2; exit 1 ;;
    esac
done

case "$agent" in
    all) agents=(claude codex gemini) ;;
    claude|codex|gemini) agents=("$agent") ;;
    *) usage >&2; exit 1 ;;
esac
if [[ -n "$category" ]]; then
    [[ "$category" != */* && "$category" != .* && -d "$SKILLS_SRC/$category" ]] || {
        echo "Unknown category: $category" >&2; exit 1;
    }
    categories=("$SKILLS_SRC/$category/")
else
    categories=("$SKILLS_SRC"/*/)
fi

installed=0
skipped=0
shared_installed=false
for selected_agent in "${agents[@]}"; do
    case "$selected_agent" in
        claude) destination="$INSTALL_ROOT/.claude/skills" ;;
        codex|gemini)
            if [[ "$shared_installed" == true ]]; then
                echo "$selected_agent uses the shared skills already installed."
                continue
            fi
            destination="$INSTALL_ROOT/.agents/skills"
            shared_installed=true
            ;;
    esac
    mkdir -p "$destination"
    echo "Installing $selected_agent skills into $destination"
    for category_dir in "${categories[@]}"; do
        for skill_dir in "$category_dir"*/; do
            [[ -f "$skill_dir/SKILL.md" ]] || continue
            skill_dir="${skill_dir%/}"
            skill_name="$(basename "$skill_dir")"
            target="$destination/$skill_name"
            if [[ -L "$target" ]] && [[ "$(readlink "$target")" == "$SKILLS_SRC/"* ]]; then
                ln -sfn "$skill_dir" "$target"
            elif [[ -e "$target" || -L "$target" ]]; then
                echo "  SKIP $skill_name: preserving existing entry at $target"
                skipped=$((skipped + 1))
                continue
            else
                ln -s "$skill_dir" "$target"
            fi
            installed=$((installed + 1))
        done
    done

    # Only remove broken links owned by this repository and selected category.
    cleanup_prefix="$SKILLS_SRC/"
    [[ -z "$category" ]] || cleanup_prefix="$SKILLS_SRC/$category/"
    for link in "$destination"/*; do
        if [[ -L "$link" && ! -e "$link" ]]; then
            link_target="$(readlink "$link")"
            if [[ "$link_target" == "$cleanup_prefix"* ]]; then
                echo "  Removing broken repository link: $link"
                rm "$link"
            fi
        fi
    done
done

echo "Done. $installed link(s) installed, $skipped existing entries preserved."
