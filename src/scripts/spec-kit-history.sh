#!/usr/bin/env bash
# spec-kit-history.sh — print a feature's process timeline from git (commit trailers).
# Usage: spec-kit-history.sh <feature> [<base-ref>]
# Output: one line per commit — date | Phase | Implemented-by | subject | Evidence
set -euo pipefail
[ $# -ge 1 ] || { sed -n '2,4p' "$0"; exit 2; }
feature="$1"; base="${2:-}"
[ -d "specs/$feature" ] || { echo "specs/$feature does not exist" >&2; exit 1; }
if [ -z "$base" ]; then
  first="$(git log --reverse --format=%H -- "specs/$feature" | head -1)"
  [ -n "$first" ] || { echo "no commits touch specs/$feature yet" >&2; exit 1; }
  if git rev-parse -q --verify "$first^" >/dev/null 2>&1; then range="$first^..HEAD"; else range="HEAD"; fi
else
  range="$base..HEAD"
fi
# Commits in the range that name the feature in the subject/body (spec(...), feat:, fix:).
git log --reverse --date=format:%Y-%m-%d \
  --format='%cd | %(trailers:key=Phase,valueonly,separator=%x2C) | %(trailers:key=Implemented-by,valueonly,separator=%x2C) | %s | %(trailers:key=Evidence,valueonly,separator=%x3B)' \
  --grep="$feature" "$range" \
| sed -E 's/\| *\|/| — |/g; s/\| *\|/| — |/g; s/\| *$/| —/'
