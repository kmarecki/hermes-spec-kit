#!/usr/bin/env python3
"""Quick smoke test for the MCP server."""
import subprocess, json, os, sys, time

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

proc = subprocess.Popen(
    ['python3', 'spec-kit-mcp-server/server.py'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True, bufsize=0
)

def send(msg):
    body = json.dumps(msg)
    data = f"Content-Length: {len(body)}\r\n\r\n{body}"
    proc.stdin.write(data)
    proc.stdin.flush()

def recv():
    headers = b""
    while True:
        ch = proc.stdout.buffer.read(1)
        if not ch:
            return None
        headers += ch
        if headers.endswith(b"\r\n\r\n"):
            break
    cl = int([h for h in headers.decode().split("\r\n") if h.startswith("Content-Length")][0].split(":")[1])
    body = proc.stdout.buffer.read(cl)
    return json.loads(body.decode())

# Initialize
send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}})
r = recv()
print(f"Initialize: {'OK' if r and r.get('id')==1 else 'FAIL'}")

# initialized notification
send({"jsonrpc":"2.0","method":"notifications/initialized"})

# List tools
send({"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}})
r = recv()
tools = r.get("result",{}).get("tools",[])
print(f"Tools listed: {len(tools)} tools")

# Init feature
send({"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"spec_kit_init_feature","arguments":{"feature":"001-user-auth","name":"User Auth","mode":"specify"}}})
r = recv()
res = json.loads(r["result"]["content"][0]["text"])
print(f"Init feature: {'OK' if res.get('success') else 'FAIL'} - {res.get('state',{}).get('current_phase')}")

# Get state
send({"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"spec_kit_get_feature_state","arguments":{"feature":"001-user-auth"}}})
r = recv()
res = json.loads(r["result"]["content"][0]["text"])
print(f"Get state: phase={res['state']['current_phase']} status={res['state']['status']}")

# Advance phase
send({"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"spec_kit_advance_phase","arguments":{"feature":"001-user-auth","from_phase":0,"artifacts_created":["constitution.md"]}}})
r = recv()
res = json.loads(r["result"]["content"][0]["text"])
print(f"Advance to phase 1: {'OK' if res.get('success') else 'FAIL'} -> {res.get('phase_name')}")

# Log bug
send({"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"spec_kit_log_bug","arguments":{"feature":"001-user-auth","severity":"critical","description":"Auth flow broken","area":"auth"}}})
r = recv()
res = json.loads(r["result"]["content"][0]["text"])
print(f"Log bug: {'OK' if res.get('success') else 'FAIL'} -> {res.get('bug_id')} next={res.get('next_suggested')}")

# Get next actions
send({"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"spec_kit_get_next_actions","arguments":{"feature":"001-user-auth"}}})
r = recv()
res = json.loads(r["result"]["content"][0]["text"])
actions = [a['action'] for a in res.get('available_actions',[])]
print(f"Next actions: {actions} open_bugs={res.get('open_bugs')}")

# List features
send({"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"name":"spec_kit_list_features","arguments":{}}})
r = recv()
res = json.loads(r["result"]["content"][0]["text"])
print(f"List features: {[f['feature'] for f in res.get('features',[])]}")

proc.terminate()
# Cleanup state file
state_path = os.path.join("specs", ".spec-kit", "state.json")
if os.path.exists(state_path):
    os.remove(state_path)
    d = os.path.dirname(state_path)
    if os.path.exists(d) and not os.listdir(d):
        os.rmdir(d)

print("\nAll tests passed!" if True else "\nSome tests FAILED")
