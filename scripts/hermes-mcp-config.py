#!/usr/bin/env python3
"""Edit the spec-kit entry under `mcp_servers:` in ~/.hermes/config.yaml — safely.

The old sed-based edit deleted exactly three lines after `  spec-kit:`; a block
written with `args:` as a YAML list is four lines, so the sed left a dangling
`- …server.py` line and the installer then appended a second `mcp_servers:` key
(a corrupt config — the backups named config.yaml.corrupt.* were this).

This script works on indentation, not line counts: it removes the whole
`  spec-kit:` block (every following line indented deeper than two spaces),
keeps other servers, reuses an existing `mcp_servers:` key, and only appends a
new one when none exists. Text-only — no YAML library, comments preserved.

Usage:
    hermes-mcp-config.py add    <config.yaml> <python> <server.py>
    hermes-mcp-config.py remove <config.yaml>
"""
import re
import sys
from pathlib import Path

ENTRY_RE = re.compile(r"^  spec-kit:\s*$")
TOP_RE = re.compile(r"^mcp_servers:\s*$")


def _split(lines):
    """Return (before, servers_body, after) around the top-level mcp_servers: key, or None."""
    for i, line in enumerate(lines):
        if TOP_RE.match(line):
            j = i + 1
            while j < len(lines) and (lines[j].startswith(" ") or lines[j].strip() == ""):
                j += 1
            # trailing blank lines belong to "after", not to the section
            k = j
            while k > i + 1 and lines[k - 1].strip() == "":
                k -= 1
            return lines[:i], lines[i + 1:k], lines[k:]
    return None


def _without_spec_kit(body):
    out, skipping = [], False
    for line in body:
        if ENTRY_RE.match(line):
            skipping = True
            continue
        if skipping and (line.startswith("   ") or line.strip() == ""):
            continue
        skipping = False
        out.append(line)
    return out


def main(argv):
    if len(argv) < 3 or argv[1] not in ("add", "remove"):
        print(__doc__); return 2
    cfg = Path(argv[2])
    text = cfg.read_text() if cfg.exists() else ""
    lines = text.split("\n")
    parts = _split(lines)
    if argv[1] == "remove":
        if parts is None:
            return 0
        before, body, after = parts
        body = _without_spec_kit(body)
        new = before + (["mcp_servers:"] + body if any(l.strip() for l in body) else []) + after
    else:
        if len(argv) != 5:
            print(__doc__); return 2
        python, server = argv[3], argv[4]
        entry = ["  spec-kit:", f'    command: "{python}"', f'    args: ["{server}"]']
        if parts is None:
            base = lines if text.strip() else []
            if base and base[-1].strip():
                base.append("")
            new = base + ["mcp_servers:"] + entry + [""]
        else:
            before, body, after = parts
            body = _without_spec_kit(body)
            while body and body[-1].strip() == "":
                body.pop()
            new = before + ["mcp_servers:"] + body + entry + after
    out = "\n".join(new)
    if not out.endswith("\n"):
        out += "\n"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
