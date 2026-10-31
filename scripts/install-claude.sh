#!/usr/bin/env bash
# spec-kit installation script for Claude Code
#
# Generates the Claude Code edition of every spec-kit skill from the SAME
# src/skills/*.md sources the Hermes edition is installed from, so both agents
# run the identical workflow and can hand phases to each other on one specs/
# tree (e.g. Claude: specify → plan → tasks, Hermes: implement, Claude: close).
#
# What it does:
#   1. src/skills/<name>.md  ──transform──▶  ~/.claude/skills/<name>/SKILL.md
#      (frontmatter reduced to the fields Claude Code reads; Hermes tool names
#       translated to Claude Code tools; shared-file paths resolved).
#   2. Shares references/, templates/ and mcp-server/ with the installed Hermes
#      tree by SYMLINK (single source of truth — whatever Hermes reads, Claude
#      reads). Falls back to copying from src/ when Hermes is not installed.
#   3. Registers the spec-kit MCP state server for Claude Code at user scope
#      (`claude mcp add -s user spec-kit …`) so specs/.spec-kit/state.json is
#      derived identically for both agents (no state file).
#
# Usage:
#   ./scripts/install-claude.sh            # install / refresh
#   ./scripts/install-claude.sh --no-mcp   # skills only, skip MCP registration
#   ./scripts/install-claude.sh --uninstall

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
HERMES_SKILLS_DIR="${HERMES_SKILLS_DIR:-$HOME/.hermes/skills}"
HERMES_SPEC_KIT="$HERMES_SKILLS_DIR/spec-kit"

DO_MCP=1
DO_UNINSTALL=0
for arg in "$@"; do
  case "$arg" in
    --no-mcp) DO_MCP=0 ;;
    --uninstall) DO_UNINSTALL=1 ;;
    -h|--help) sed -n '2,24p' "$0"; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

# ───────────────────────────── uninstall ─────────────────────────────
if [ "$DO_UNINSTALL" -eq 1 ]; then
  echo "Uninstalling spec-kit (Claude Code edition) from $CLAUDE_SKILLS_DIR..."
  removed=0
  for dir in "$CLAUDE_SKILLS_DIR"/spec-kit-*/ "$CLAUDE_SKILLS_DIR"/spec-kit/; do
    if [ -d "$dir" ] || [ -L "${dir%/}" ]; then
      echo "  Removing: $(basename "$dir")"
      rm -rf "${dir%/}"
      removed=$((removed + 1))
    fi
  done
  echo "  -> Removed $removed skill director(y/ies)"
  if command -v claude >/dev/null 2>&1 && claude mcp get spec-kit >/dev/null 2>&1; then
    claude mcp remove -s user spec-kit >/dev/null 2>&1 && echo "  Removed MCP server 'spec-kit' (user scope)" \
      || echo "  NOTE: could not remove MCP server 'spec-kit' automatically — run: claude mcp remove -s user spec-kit"
  fi
  echo "Done. Restart Claude Code for the change to take effect."
  exit 0
fi

# ───────────────────────────── install ───────────────────────────────
echo "Installing spec-kit (Claude Code edition) from $PROJECT_DIR to $CLAUDE_SKILLS_DIR..."
mkdir -p "$CLAUDE_SKILLS_DIR"

# The transform: Hermes skill source → Claude Code SKILL.md.
# Kept in one place so a diff of the two editions is ONLY the translation.
transform() {
  local src="$1" dst="$2" skill_name="$3"
  python3 - "$src" "$dst" "$skill_name" <<'PY'
import re, sys
src, dst, skill = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(src, encoding="utf-8").read()

# ── 1. frontmatter: keep only what Claude Code reads ──────────────────────
m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
if not m:
    sys.exit(f"{src}: no YAML frontmatter")
fm, body = m.group(1), text[m.end():]

def field(name):
    """Return the raw YAML value of a top-level scalar field (incl. '>' folds)."""
    mm = re.search(rf"^{name}:(.*?)(?=^\S|\Z)", fm, re.S | re.M)
    return mm.group(1).rstrip("\n") if mm else None

description = field("description")
if description is None:
    sys.exit(f"{src}: frontmatter has no description")
description = description.replace("Hermes Agent", "Claude Code")

arg_hint = {
    "spec-kit": None,
    "spec-kit-constitution": "[project description]",
    "spec-kit-workflow": "[command] [feature]",
}.get(skill, "[feature]")

out = ["---", f"name: {skill}", f"description:{description}"]
if arg_hint:
    out.append(f'argument-hint: "{arg_hint}"')
out.append("---")
frontmatter = "\n".join(out) + "\n"

# ── 2. body: Hermes → Claude Code translation ────────────────────────────
subs = [
    # product names / homes
    (r"Hermes Agent", "Claude Code"),
    (r"~/\.hermes/skills/", "~/.claude/skills/"),
    # shared-file paths (the skills say `spec-kit/references/…` — resolve them)
    (r"(?<![\w/~.])spec-kit/references/", "~/.claude/skills/spec-kit/references/"),
    (r"(?<![\w/~.])spec-kit/templates/", "~/.claude/skills/spec-kit/templates/"),
    # MCP tool prefix: Hermes `mcp_spec_kit_x` → Claude Code `mcp__spec-kit__x`
    (r"mcp_spec_kit_", "mcp__spec-kit__"),
    (r"\(In Hermes the tools appear with the `mcp__spec-kit__` prefix — call them by this full name\.\)",
     "(In Claude Code the tools appear as `mcp__spec-kit__<tool>` — call them by this full name.)"),
    # tool names
    (r"skill_view\(name='([^']+)'\)", r'the `Skill` tool with skill "\1"'),
    (r"`skill_view`", "`Skill`"),
    (r"`read_file`, `search_files`", "`Read`, `Grep`/`Glob`"),
    (r"`read_file`", "`Read`"),
    (r"`search_files`", "`Grep`/`Glob`"),
    (r"`write_file`", "`Write`"),
    (r"\bwrite_file\b", "Write"),
    (r"`patch`", "`Edit`"),
    (r"`terminal`", "`Bash`"),
    (r"\bterminal\(", "Bash("),
    (r"\bterminal \(build/compile/test\)", "Bash (build/compile/test)"),
]
for pat, rep in subs:
    body = re.sub(pat, rep, body)

# Umbrella-only: the Hermes MCP config snippet → the Claude Code command.
if skill == "spec-kit":
    body = re.sub(
        r"Enable by adding to `~/\.hermes/config\.yaml`:\n\n```yaml\n.*?\n```\n",
        "Enable for Claude Code (user scope — once per machine; `scripts/install-claude.sh` does this for you):\n\n"
        "```bash\nclaude mcp add -s user spec-kit -- <python-with-mcp-sdk> ~/.claude/skills/spec-kit/mcp-server/server.py\n```\n",
        body, flags=re.S)
    body = body.replace(
        "regardless of Hermes profile or working directory",
        "regardless of agent (Hermes or Claude Code) or working directory")

# ── 3. the Claude Code notes block, right under the H1 ───────────────────
note = f"""
> Claude Code edition of `src/skills/{skill}.md` (hermes-spec-kit) — generated, do not edit.
> `$ARGUMENTS` = `[feature]` · "load `spec-kit-x`" = the `Skill` tool · ASK / WAIT = `AskUserQuestion`
> · Hermes tool names in references map to `Bash`, `Write`/`Edit`, `Read`, `Grep`/`Glob`; `mcp_spec_kit_x` → `mcp__spec-kit__x`
> · the skills commit their own artifacts (`commits.md`) — standing authorisation; keep the commit attribution rules.
"""
h1 = re.search(r"^# .*\n", body, re.M)
if h1:
    body = body[:h1.end()] + note + body[h1.end():]
else:
    body = note + body

open(dst, "w", encoding="utf-8").write(frontmatter + body)
PY
}

installed=0
# Phase skills: src/skills/<name>.md → <name>/SKILL.md
for skill in "$PROJECT_DIR"/src/skills/*.md; do
  [ -f "$skill" ] || continue
  name=$(basename "$skill" .md)
  mkdir -p "$CLAUDE_SKILLS_DIR/$name"
  transform "$skill" "$CLAUDE_SKILLS_DIR/$name/SKILL.md" "$name"
  echo "  Installing skill: $name"
  installed=$((installed + 1))
done

# Umbrella skill
UMBRELLA_SRC="$PROJECT_DIR/src/skills/spec-kit/SKILL.md"
if [ -f "$UMBRELLA_SRC" ]; then
  mkdir -p "$CLAUDE_SKILLS_DIR/spec-kit"
  transform "$UMBRELLA_SRC" "$CLAUDE_SKILLS_DIR/spec-kit/SKILL.md" "spec-kit"
  echo "  Installing umbrella skill: spec-kit"
  installed=$((installed + 1))
fi

# Shared files: symlink to the installed Hermes tree (single source of truth),
# else copy from src/. Per-skill references/ directories that exist only in the
# Hermes tree (project-specific notes added over time) are linked too.
link_or_copy() {
  local target="$1" link="$2" fallback_src="$3" label="$4"
  if [ -e "$link" ] && [ ! -L "$link" ]; then
    rm -rf "$link"            # replace an earlier copied directory with the link
  fi
  if [ -d "$target" ]; then
    ln -sfn "$target" "$link"
    echo "  Linking $label -> $target"
  elif [ -n "$fallback_src" ] && [ -d "$fallback_src" ]; then
    rm -f "$link"; mkdir -p "$link"; cp -r "$fallback_src"/. "$link"/
    echo "  Copying $label from $fallback_src (Hermes tree not found)"
  fi
}
link_or_copy "$HERMES_SPEC_KIT/references" "$CLAUDE_SKILLS_DIR/spec-kit/references" "$PROJECT_DIR/src/references" "spec-kit/references"
link_or_copy "$HERMES_SPEC_KIT/templates"  "$CLAUDE_SKILLS_DIR/spec-kit/templates"  "$PROJECT_DIR/src/templates"  "spec-kit/templates"
link_or_copy "$HERMES_SPEC_KIT/mcp-server" "$CLAUDE_SKILLS_DIR/spec-kit/mcp-server" "$PROJECT_DIR/spec-kit-mcp-server" "spec-kit/mcp-server"
link_or_copy "$HERMES_SPEC_KIT/scripts"    "$CLAUDE_SKILLS_DIR/spec-kit/scripts"    "$PROJECT_DIR/src/scripts"            "spec-kit/scripts"
for hdir in "$HERMES_SKILLS_DIR"/spec-kit-*/references; do
  [ -d "$hdir" ] || continue
  sname=$(basename "$(dirname "$hdir")")
  [ -d "$CLAUDE_SKILLS_DIR/$sname" ] || continue
  link_or_copy "$hdir" "$CLAUDE_SKILLS_DIR/$sname/references" "" "$sname/references"
done

# ───────────────────────────── MCP server ────────────────────────────
if [ "$DO_MCP" -eq 1 ]; then
  echo ""
  if ! command -v claude >/dev/null 2>&1; then
    echo "  NOTE: 'claude' CLI not found — skipping MCP registration."
  elif claude mcp get spec-kit >/dev/null 2>&1; then
    echo "  MCP server 'spec-kit' already registered for Claude Code — leaving it as is."
  else
    MCP_PYTHON=""
    for cand in "$HOME/.hermes-venv/bin/python3" "$PROJECT_DIR/.venv/bin/python3" python3; do
      if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import mcp" >/dev/null 2>&1; then
        MCP_PYTHON="$(command -v "$cand")"; break
      fi
    done
    SERVER="$CLAUDE_SKILLS_DIR/spec-kit/mcp-server/server.py"
    if [ -z "$MCP_PYTHON" ]; then
      echo "  WARNING: no Python with the 'mcp' SDK found — MCP server not registered."
      echo "           Install it (see spec-kit-mcp-server/requirements.txt), then run:"
      echo "           claude mcp add -s user spec-kit -- <python3> $SERVER"
    elif [ ! -f "$SERVER" ]; then
      echo "  WARNING: $SERVER not found — MCP server not registered."
    else
      claude mcp add -s user spec-kit -- "$MCP_PYTHON" "$SERVER" >/dev/null
      echo "  Registered MCP server 'spec-kit' (user scope): $MCP_PYTHON $SERVER"
      echo "  -> Claude Code sees its tools as mcp__spec-kit__<tool>; the server keeps no state"
    fi
  fi
fi

echo ""
echo "Done. Installed $installed skill(s) to $CLAUDE_SKILLS_DIR"
echo "Restart Claude Code (or start a new session) to load them. Invoke as /spec-kit-specify, /spec-kit-plan, …"
