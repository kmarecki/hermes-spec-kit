#!/usr/bin/env bash
# spec-kit installation script for Hermes Agent
# Installs skills from this project to ~/.hermes/skills/

set -e

SKILLS_DIR="$HOME/.hermes/skills"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Installing spec-kit skills from $PROJECT_DIR to $SKILLS_DIR..."

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Copy each skill file
for skill in "$PROJECT_DIR"/src/skills/*.md; do
  if [ -f "$skill" ]; then
    skill_name=$(basename "$skill")
    echo "  Installing: $skill_name"
    cp "$skill" "$SKILLS_DIR/$skill_name"
  fi
done

echo "Done. Installed skills to $SKILLS_DIR"
echo ""
echo "Available skills:"
ls -1 "$SKILLS_DIR"/*.md 2>/dev/null | xargs -I{} basename {} || echo "  (none)"
echo ""
echo "To use: Load a skill with skill_view(name='...') or mention it in conversation"