#!/usr/bin/env python3
"""Smoke test for the MCP server using the official mcp SDK client."""
import anyio, json, os, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

SERVER_DIR = Path(__file__).resolve().parent
SERVER_SCRIPT = SERVER_DIR / "server.py"

async def test():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            print(f"✓ Initialize: {init.serverInfo.name} v{init.serverInfo.version}")

            tools = await session.list_tools()
            assert len(tools.tools) >= 11, f"Expected 11+ tools, got {len(tools.tools)}"
            print(f"✓ Tools listed: {len(tools.tools)} tools")

            # init_feature
            result = await session.call_tool("spec_kit_init_feature", {
                "feature": "001-user-auth", "name": "User Auth", "mode": "specify"
            })
            data = json.loads(result.content[0].text)
            assert data["success"], f"init_feature failed: {data}"
            print(f"✓ init_feature: phase {data['state']['current_phase']}")

            # get_feature_state
            result = await session.call_tool("spec_kit_get_feature_state", {"feature": "001-user-auth"})
            data = json.loads(result.content[0].text)
            assert data["state"]["current_phase"] == 0
            print(f"✓ get_feature_state: phase {data['state']['current_phase']}")

            # advance_phase
            result = await session.call_tool("spec_kit_advance_phase", {
                "feature": "001-user-auth", "from_phase": 0, "artifacts_created": ["constitution.md"]
            })
            data = json.loads(result.content[0].text)
            assert data["success"]
            print(f"✓ advance_phase: 0 -> 1 ({data['phase_name']})")

            # log_bug
            result = await session.call_tool("spec_kit_log_bug", {
                "feature": "001-user-auth", "severity": "critical",
                "description": "Auth flow broken", "area": "auth"
            })
            data = json.loads(result.content[0].text)
            assert data["success"]
            assert data["next_suggested"] == "bugfix_plan"
            print(f"✓ log_bug: {data['bug_id']} next={data['next_suggested']}")

            # set_bug_status
            result = await session.call_tool("spec_kit_set_bug_status", {
                "feature": "001-user-auth", "bug_id": data["bug_id"], "status": "resolved"
            })
            data2 = json.loads(result.content[0].text)
            assert data2["success"]
            print(f"✓ set_bug_status: {data['bug_id']} -> resolved")

            # set_bug_plan_ref
            result = await session.call_tool("spec_kit_set_bug_plan_ref", {
                "feature": "001-user-auth", "bug_id": data["bug_id"], "plan_ref": "plan.md#bugfix-BUG-001"
            })
            data3 = json.loads(result.content[0].text)
            assert data3["success"]
            print(f"✓ set_bug_plan_ref: {data['bug_id']} -> plan.md#bugfix-BUG-001")

            # get_next_actions
            result = await session.call_tool("spec_kit_get_next_actions", {"feature": "001-user-auth"})
            data4 = json.loads(result.content[0].text)
            print(f"✓ get_next_actions: {len(data4['available_actions'])} actions, {data4['open_bugs']} open bugs")

            # list_features
            result = await session.call_tool("spec_kit_list_features", {})
            data5 = json.loads(result.content[0].text)
            assert len(data5["features"]) == 1
            print(f"✓ list_features: {[f['feature'] for f in data5['features']]}")

            # update_artifact
            result = await session.call_tool("spec_kit_update_artifact", {
                "feature": "001-user-auth", "artifact": "spec.md", "status": "present"
            })
            data6 = json.loads(result.content[0].text)
            assert data6["success"]
            print(f"✓ update_artifact: spec.md -> present")

            return True

def main():
    # Cleanup before
    state_path = Path("specs/.spec-kit/state.json")
    if state_path.exists():
        state_path.unlink()
        parent = state_path.parent
        if parent.exists() and not any(parent.iterdir()):
            parent.rmdir()

    try:
        success = anyio.run(test)
        print(f"\n{'All tests passed!' if success else 'Some tests FAILED'}")
    except Exception as e:
        print(f"\nFAILED: {e}")
        import traceback
        traceback.print_exc()
        success = False
    finally:
        # Cleanup after
        if state_path.exists():
            state_path.unlink()
            parent = state_path.parent
            if parent.exists() and not any(parent.iterdir()):
                parent.rmdir()

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
