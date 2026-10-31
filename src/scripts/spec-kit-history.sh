#!/usr/bin/env bash
# spec-kit-history.sh — a feature's timeline from the branch's git log, for the change record
# when history.md is off (history: large / never). Run on the feature branch BEFORE the squash.
# Usage: spec-kit-history.sh <feature> [<base-ref>]   → date | author | subject
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
git log --reverse --date=format:%Y-%m-%d --format='%cd | %an | %s' --grep="$feature" "$range"
