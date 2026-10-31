#!/usr/bin/env bash
# spec-kit-log.sh — append one fixed-field entry to specs/<feature>/history.md
# (the no-MCP fallback for mcp_spec_kit_append_history). Stamps the REAL UTC time.
#
# Usage:
#   spec-kit-log.sh <feature> "<Phase label>" <skill> <agent> \
#       [--artifacts "a, b"] [--tests "cmd → N passed"] [--evidence "output:…; ci:…"] \
#       [--commit "message"] [--note "≤ 25 words"]
set -euo pipefail
if [ $# -lt 4 ]; then sed -n '2,9p' "$0"; exit 2; fi
feature="$1"; phase="$2"; skill="$3"; agent="$4"; shift 4
artifacts="" ; tests="none"; evidence="none — unverified"; commit=""; note=""
while [ $# -gt 0 ]; do
  case "$1" in
    --artifacts) artifacts="$2"; shift 2 ;;
    --tests)     tests="$2"; shift 2 ;;
    --evidence)  evidence="$2"; shift 2 ;;
    --commit)    commit="$2"; shift 2 ;;
    --note)      note="$2"; shift 2 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done
file="specs/$feature/history.md"
[ -d "specs/$feature" ] || { echo "specs/$feature does not exist" >&2; exit 1; }
if [ "$(printf '%s' "$note" | wc -w)" -gt 25 ]; then echo "note exceeds 25 words — shorten it (narrative belongs in implementation-summary.md)" >&2; exit 1; fi
[ -f "$file" ] || printf '# Process History: %s\n' "$feature" > "$file"
ts="$(date -u +%Y-%m-%dT%H:%M:%S+00:00)"
{
  printf '\n## %s | %s | %s | %s\n' "$ts" "$phase" "$skill" "$agent"
  printf -- '- Artifacts: %s\n' "${artifacts:-none}"
  printf -- '- Tests: %s\n' "$tests"
  printf -- '- Evidence: %s\n' "$evidence"
  printf -- '- Commit: %s\n' "${commit:-n/a}"
  printf -- '- Note: %s\n' "${note:--}"
} >> "$file"
echo "appended to $file at $ts"
