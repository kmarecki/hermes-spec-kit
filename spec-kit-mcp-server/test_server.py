#!/usr/bin/env python3
"""Run all MCP server integration tests.

Usage:
    python3 spec-kit-mcp-server/test_server.py
    python3 spec-kit-mcp-server/test_workflow.py
"""
import subprocess, sys, os
script = os.path.join(os.path.dirname(__file__), "test_workflow.py")
sys.exit(subprocess.call([sys.executable, script] + sys.argv[1:]))
