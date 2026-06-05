#!/usr/bin/env bash
# spec-kit installation script for Hermes Agent
# Installs skills and templates from this project to ~/.hermes/skills/

set -e

SKILLS_DIR="$HOME/.hermes/skills"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Installing spec-kit from $PROJECT_DIR to $SKILLS_DIR..."

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Copy each skill file from src/skills/
for skill in "$PROJECT_DIR"/src/skills/*.md; do
  if [ -f "$skill" ]; then
    skill_name=$(basename "$skill")
    echo "  Installing skill: $skill_name"
    cp "$skill" "$SKILLS_DIR/$skill_name"
  fi
done

# Copy templates to spec-kit/templates/
TEMPLATES_DIR="$SKILLS_DIR/spec-kit/templates"
mkdir -p "$TEMPLATES_DIR"

for tmpl in "$PROJECT_DIR"/src/templates/*-template.md; do
  if [ -f "$tmpl" ]; then
    tmpl_name=$(basename "$tmpl")
    echo "  Installing template: $tmpl_name"
    cp "$tmpl" "$TEMPLATES_DIR/$tmpl_name"
  fi
done

echo ""
echo "Done. Installed to $SKILLS_DIR"
echo ""
echo "Skills:"
ls -1 "$SKILLS_DIR"/*.md 2>/dev/null | xargs -I{} basename {} || echo "  (none)"
echo ""
echo "Templates:"
ls -1 "$TEMPLATES_DIR"/*.md 2>/dev/null | xargs -I{} basename {} || echo "  (none)"
echo ""
echo "To use: Load a skill with skill_view(name='...') or mention it in conversation"
