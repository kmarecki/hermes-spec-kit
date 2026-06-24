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

# Remove renamed/obsolete skill directories
OBSOLETE_DIRS="spec-kit-analyze spec-kit-checklist spec-kit-explore spec-kit-compare"
for obsolete in $OBSOLETE_DIRS; do
  if [ -d "$SKILLS_DIR/$obsolete" ]; then
    echo "  Removing obsolete skill directory: $obsolete"
    rm -rf "$SKILLS_DIR/$obsolete"
  fi
done

# Remove obsolete template files
# (TEMPLATES_DIR is defined below; cleanup runs after it's set)

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

# Remove obsolete template files
rm -f "$TEMPLATES_DIR/checklist-template.md"
rm -f "$TEMPLATES_DIR/comparison-template.md"
rm -f "$TEMPLATES_DIR/soul-template.md"

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

# --- MCP Server ---
MCP_SERVER_DIR="$PROJECT_DIR/spec-kit-mcp-server"
MCP_SERVER_DST="$SKILLS_DIR/spec-kit/mcp-server"
if [ -f "$MCP_SERVER_DIR/server.py" ]; then
  mkdir -p "$MCP_SERVER_DST"
  cp "$MCP_SERVER_DIR/server.py" "$MCP_SERVER_DST/server.py"
  cp "$MCP_SERVER_DIR/README.md" "$MCP_SERVER_DST/README.md" 2>/dev/null || true
  chmod +x "$MCP_SERVER_DST/server.py"
  echo "  Installing MCP server: spec-kit-mcp-server/server.py"

  # Determine Python for MCP — prefer venv with mcp SDK, fallback to system
  MCP_PYTHON=""
  if python3 -c "import mcp" 2>/dev/null; then
    MCP_PYTHON="python3"
    echo "  -> mcp SDK found (system python)"
  else
    # Try creating a venv with mcp installed
    MCP_VENV="$HOME/.hermes-venv"
    if [ ! -f "$MCP_VENV/bin/python3" ]; then
      echo "  -> Creating venv at $MCP_VENV..."
      python3 -m venv "$MCP_VENV"
      echo "  -> Installing mcp SDK (pip install mcp)..."
      "$MCP_VENV/bin/pip" install mcp
    fi
    if "$MCP_VENV/bin/python3" -c "import mcp" 2>/dev/null; then
      MCP_PYTHON="$MCP_VENV/bin/python3"
      echo "  -> mcp SDK installed in venv"
    else
      echo "  -> WARNING: Failed to install mcp SDK in venv."
      echo "     Try: $MCP_VENV/bin/pip install mcp"
    fi
  fi

  # Configure MCP server in config.yaml
  #
  # NOTE: We write config.yaml directly instead of using 'hermes mcp add'.
  # 'hermes mcp add' tries to hot-reload into a running Hermes process, which
  # times out when no session is active (typical during installation).
  #
  CONFIG_FILE="$HOME/.hermes/config.yaml"
  if [ -n "$MCP_PYTHON" ]; then
    echo "  -> Configuring MCP server in $CONFIG_FILE..."
    mkdir -p "$(dirname "$CONFIG_FILE")"
    [ -f "$CONFIG_FILE" ] || touch "$CONFIG_FILE"

    # Remove any existing spec-kit block from mcp_servers (3 lines)
    sed -i '/^  spec-kit:/{
      N;N;d
    }' "$CONFIG_FILE" 2>/dev/null || true

    # If mcp_servers section is now empty (no remaining entries), remove it
    sed -i '/^mcp_servers:$/{
      N
      /^mcp_servers:\n$/d
    }' "$CONFIG_FILE" 2>/dev/null || true

    # Append fresh config entry
    cat >> "$CONFIG_FILE" << EOF

mcp_servers:
  spec-kit:
    command: "$MCP_PYTHON"
    args: ["$MCP_SERVER_DST/server.py"]
EOF
    echo "  -> Added spec-kit MCP server entry"
    echo "  -> Activate in Hermes with: /reload-mcp"
  else
    echo "  -> WARNING: mcp Python package not available."
    echo "     Hermes needs it for MCP support. Install manually:"
    echo "     python3 -m venv ~/.hermes-venv && ~/.hermes-venv/bin/pip install mcp"
  fi
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

# Auto-creation: when a spec-kit skill first runs in any project, preflight.md
# creates specs/git-conventions.md from the template automatically.
# No manual copy needed.
echo "---"
echo "git-conventions.md is auto-created per-project when spec-kit skills first run."
echo "No manual copy needed — preflight.md handles it on demand."
