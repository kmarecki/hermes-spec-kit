#!/usr/bin/env bash
# spec-kit installation script for Hermes Agent
# Installs skills and templates from this project to ~/.hermes/skills/

set -e

SKILLS_DIR="$HOME/.hermes/skills"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Installing spec-kit from $PROJECT_DIR to $SKILLS_DIR..."

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Remove old speckit-* directories (pre-rename format) to prevent conflicts
OLD_SPECKIT_COUNT=0
for old_dir in "$SKILLS_DIR"/speckit-*/; do
  if [ -d "$old_dir" ]; then
    echo "  Removing old skill directory: $(basename "$old_dir")"
    rm -rf "$old_dir"
    OLD_SPECKIT_COUNT=$((OLD_SPECKIT_COUNT + 1))
  fi
done
if [ "$OLD_SPECKIT_COUNT" -gt 0 ]; then
  echo "  -> Cleaned up $OLD_SPECKIT_COUNT old speckit-* skill(s)"
fi

# Remove stale flat spec-kit-*.md files (old install format, now replaced by directories)
STALE_COUNT=0
for stale in "$SKILLS_DIR"/spec-kit-*.md; do
  if [ -f "$stale" ]; then
    echo "  Removing stale flat file: $(basename "$stale")"
    rm -f "$stale"
    STALE_COUNT=$((STALE_COUNT + 1))
  fi
done
if [ "$STALE_COUNT" -gt 0 ]; then
  echo "  -> Cleaned up $STALE_COUNT stale flat spec-kit-* file(s)"
fi

# Copy each skill file from src/skills/ — install as <skill-name>/SKILL.md
for skill in "$PROJECT_DIR"/src/skills/*.md; do
  if [ -f "$skill" ]; then
    skill_name=$(basename "$skill" .md)
    skill_dir="$SKILLS_DIR/$skill_name"
    mkdir -p "$skill_dir"
    cp "$skill" "$skill_dir/SKILL.md"
    echo "  Installing skill: $skill_name"
  fi
done

# Copy umbrella SKILL.md to spec-kit/ directory
UMBRELLA_SRC="$PROJECT_DIR/src/skills/spec-kit/SKILL.md"
UMBRELLA_DST="$SKILLS_DIR/spec-kit/SKILL.md"
if [ -f "$UMBRELLA_SRC" ]; then
  mkdir -p "$(dirname "$UMBRELLA_DST")"
  echo "  Installing umbrella SKILL.md"
  cp "$UMBRELLA_SRC" "$UMBRELLA_DST"
fi

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

# Copy references to spec-kit/references/
REFERENCES_DIR="$SKILLS_DIR/spec-kit/references"
mkdir -p "$REFERENCES_DIR"

for ref in "$PROJECT_DIR"/src/references/*.md; do
  if [ -f "$ref" ]; then
    ref_name=$(basename "$ref")
    echo "  Installing reference: $ref_name"
    cp "$ref" "$REFERENCES_DIR/$ref_name"
  fi
done

# --- SOUL.md prompt ---
SOUL_TEMPLATE="$TEMPLATES_DIR/soul-template.md"
if [ -f "$SOUL_TEMPLATE" ]; then
  echo ""
  if [ -f "$HOME/.hermes/SOUL.md" ]; then
    current_soul_size=$(wc -c < "$HOME/.hermes/SOUL.md" 2>/dev/null || echo 0)
    if [ "$current_soul_size" -gt 100 ]; then
      echo "  Note: ~/.hermes/SOUL.md exists and appears to have custom content ($current_soul_size bytes)."
    fi
  fi
  printf "  spec-kit includes a SOUL.md persona template (neutral, multi-mode).\n"
  printf "  Replace ~/.hermes/SOUL.md with the spec-kit version? [y/N] "
  read -r answer
  case "$answer" in
    [yY]|[yY][eE][sS])
      cp "$SOUL_TEMPLATE" "$HOME/.hermes/SOUL.md"
      echo "  -> Installed spec-kit SOUL.md to ~/.hermes/SOUL.md"
      # Also flip display.personality to none if it's currently a non-default value
      if command -v hermes &>/dev/null; then
        current_personality=$(hermes config show display.personality 2>/dev/null || echo "")
        if [ -n "$current_personality" ] && [ "$current_personality" != "none" ] && [ "$current_personality" != "default" ]; then
          printf "  Current display.personality is '%s'. Set it to 'none' to avoid personality overlay conflicts? [Y/n] " "$current_personality"
          read -r p_answer
          case "$p_answer" in
            [nN]|[nN][oO]) echo "  -> Keeping display.personality as '$current_personality'" ;;
            *) hermes config set display.personality none 2>/dev/null && echo "  -> Set display.personality to none" || echo "  -> (could not auto-set display.personality)" ;;
          esac
        fi
      fi
      ;;
    *)
      echo "  -> Skipping SOUL.md (left unchanged)"
      ;;
  esac
fi

echo ""
echo "Done. Installed to $SKILLS_DIR"
echo ""
echo "Skills:"
ls -1 "$SKILLS_DIR"/*.md 2>/dev/null | xargs -I{} basename {} || echo "  (none)"
echo ""
echo "Umbrella SKILL.md:"
if [ -f "$UMBRELLA_DST" ]; then
  echo "  $UMBRELLA_DST"
fi
echo ""
echo "Templates:"
ls -1 "$TEMPLATES_DIR"/*.md 2>/dev/null | xargs -I{} basename {} || echo "  (none)"
echo ""
echo "To use: Load a skill with skill_view(name='...') or mention it in conversation"
