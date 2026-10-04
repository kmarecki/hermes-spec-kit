#!/usr/bin/env bash
# spec-kit uninstall script for Hermes Agent
# Removes all skills, templates, references, MCP server, and config entries.

set -e

SKILLS_DIR="$HOME/.hermes/skills"
CONFIG_FILE="$HOME/.hermes/config.yaml"

echo "Uninstalling spec-kit from $SKILLS_DIR..."
echo ""

# --- Remove skill directories ---
REMOVED_SKILLS=0
for dir in "$SKILLS_DIR"/spec-kit-*/; do
  if [ -d "$dir" ]; then
    name=$(basename "$dir")
    echo "  Removing skill: $name"
    rm -rf "$dir"
    REMOVED_SKILLS=$((REMOVED_SKILLS + 1))
  fi
done

# Remove umbrella skill directory
if [ -d "$SKILLS_DIR/spec-kit" ]; then
  echo "  Removing umbrella: spec-kit"
  rm -rf "$SKILLS_DIR/spec-kit"
  REMOVED_SKILLS=$((REMOVED_SKILLS + 1))
fi

echo "  -> Removed $REMOVED_SKILLS skill(s)"

# --- Remove stale flat spec-kit-*.md files (old format) ---
STALE_COUNT=0
for stale in "$SKILLS_DIR"/spec-kit-*.md; do
  if [ -f "$stale" ]; then
    echo "  Removing stale flat file: $(basename "$stale")"
    rm -f "$stale"
    STALE_COUNT=$((STALE_COUNT + 1))
  fi
done
if [ "$STALE_COUNT" -gt 0 ]; then
  echo "  -> Removed $STALE_COUNT stale flat file(s)"
fi

# --- Remove old speckit-* directories (pre-rename format) ---
OLD_COUNT=0
for old_dir in "$SKILLS_DIR"/speckit-*/; do
  if [ -d "$old_dir" ]; then
    echo "  Removing old format: $(basename "$old_dir")"
    rm -rf "$old_dir"
    OLD_COUNT=$((OLD_COUNT + 1))
  fi
done
if [ "$OLD_COUNT" -gt 0 ]; then
  echo "  -> Removed $OLD_COUNT old format skill(s)"
fi

# --- Remove MCP server ---
if [ -d "$SKILLS_DIR/spec-kit/mcp-server" ]; then
  echo "  Removing MCP server: spec-kit/mcp-server"
  rm -rf "$SKILLS_DIR/spec-kit/mcp-server"
fi

# --- Remove spec-kit MCP config from config.yaml ---
if [ -f "$CONFIG_FILE" ]; then
  if grep -q "spec-kit:" "$CONFIG_FILE" 2>/dev/null; then
    cp "$CONFIG_FILE" "$CONFIG_FILE.spec-kit-backup"
    echo "  Backed up config to: $CONFIG_FILE.spec-kit-backup"

    # Remove spec-kit block (3 lines: spec-kit:, command:, args:)
    sed -i '/^  spec-kit:/{
      N;N;d
    }' "$CONFIG_FILE" 2>/dev/null || true

    # Remove empty mcp_servers section (no entries left)
    sed -i '/^mcp_servers:$/{
      N
      /^mcp_servers:\n$/d
    }' "$CONFIG_FILE" 2>/dev/null || true

    echo "  Removed spec-kit entry from ~/.hermes/config.yaml"
  fi
fi

echo ""
echo "Done. spec-kit has been fully uninstalled."
echo "Restart Hermes Agent for changes to take effect."
