import subprocess, json, sys, pathlib, time

def test_tool_list():
    """Make sure the FastMCP server advertises its tools."""
    proc = subprocess.Popen(
        ["uv", "tool", "run", "scholar-mcp", "--transport=stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    # give the server a moment to start then ask for metadata
    time.sleep(1)
    proc.communicate(input=json.dumps({"command": "list_tools"}) + "\n", timeout=5)
    out = proc.stdout.read()
    assert "getScholarData" in out
    proc.terminate()

