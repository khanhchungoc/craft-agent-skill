#!/usr/bin/env bash
#
# Installs craft-agent-skill into target AI agent runtimes at either User (global) or Project level.
#
# Usage:
#   ./scripts/install.sh [--scope user|project] [--runtime all|copilot|claude-code|codex|gemini|kiro] [--mode symlink|copy] [--target-path <path>]
#

set -e

SCOPE="user"
RUNTIME="all"
MODE="symlink"
TARGET_PATH="$(pwd)"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --scope|-s) SCOPE="$2"; shift ;;
        --runtime|-r) RUNTIME="$2"; shift ;;
        --mode|-m) MODE="$2"; shift ;;
        --target-path|-t) TARGET_PATH="$2"; shift ;;
        --help|-h)
            echo "Usage: $0 [--scope user|project] [--runtime all|copilot|claude-code|codex|gemini|kiro] [--mode symlink|copy]"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> Installing craft-agent-skill"
echo "    Source:  $REPO_ROOT"
echo "    Scope:   $SCOPE"
echo "    Mode:    $MODE"
echo "    Target:  $RUNTIME"

declare -A DESTINATIONS

if [[ "$SCOPE" == "user" ]]; then
    DESTINATIONS["copilot"]="$HOME/.copilot/skills/craft-agent-skill"
    DESTINATIONS["claude-code"]="$HOME/.claude/skills/craft-agent-skill"
    DESTINATIONS["codex"]="$HOME/.agents/skills/craft-agent-skill"
    DESTINATIONS["gemini"]="$HOME/.gemini/antigravity/skills/craft-agent-skill"
    DESTINATIONS["kiro"]="$HOME/.kiro/skills/craft-agent-skill"
else
    DESTINATIONS["copilot"]="$TARGET_PATH/.github/skills/craft-agent-skill"
    DESTINATIONS["claude-code"]="$TARGET_PATH/.claude/skills/craft-agent-skill"
    DESTINATIONS["codex"]="$TARGET_PATH/.agents/skills/craft-agent-skill"
    DESTINATIONS["gemini"]="$TARGET_PATH/skills/craft-agent-skill"
    DESTINATIONS["kiro"]="$TARGET_PATH/.kiro/skills/craft-agent-skill"
fi

if [[ "$RUNTIME" == "all" ]]; then
    RUNTIMES=("copilot" "claude-code" "codex" "gemini" "kiro")
else
    RUNTIMES=("$RUNTIME")
fi

for rt in "${RUNTIMES[@]}"; do
    dest="${DESTINATIONS[$rt]}"
    parent_dir="$(dirname "$dest")"
    mkdir -p "$parent_dir"

    if [[ -e "$dest" || -L "$dest" ]]; then
        echo "    Removing existing target at $dest"
        rm -rf "$dest"
    fi

    if [[ "$MODE" == "symlink" ]]; then
        echo "    Linking ($rt) -> $dest"
        ln -s "$REPO_ROOT" "$dest"
    else
        echo "    Copying ($rt) -> $dest"
        cp -R "$REPO_ROOT" "$dest"
        rm -rf "$dest/.git"
    fi
done

echo "==> Installation complete!"
