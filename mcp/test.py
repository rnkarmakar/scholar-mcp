# --- paste everything after the prompt -------------------------------

import subprocess, sys, venv, inspect, pathlib, textwrap, shutil, os, tempfile

tmpdir = pathlib.Path(tempfile.gettempdir()) / "mcp-probe"
if tmpdir.exists():
    shutil.rmtree(tmpdir)
print(f"Creating throw‑away venv at {tmpdir}")
venv.EnvBuilder(with_pip=True).create(tmpdir)

pip = tmpdir / ("Scripts" if os.name == "nt" else "bin") / "pip"
python = tmpdir / ("Scripts" if os.name == "nt" else "bin") / "python"

print("\nInstalling mcp‑agent from GitHub HEAD …")
subprocess.check_call([pip, "install", "--quiet",
                       "git+https://github.com/lastmile-ai/mcp-agent@main"])

code = """
from mcp_agent.mcp.mcp_agent_client_session import MCPAgentClientSession
import inspect, sys
print('Python:', sys.version.split()[0])
print('mcp-agent version:', __import__('importlib.metadata').metadata.version('mcp-agent'))
print('send_request signature:',
      inspect.signature(MCPAgentClientSession.send_request))
"""
print("\nIntrospecting the freshly‑built package …\n")
subprocess.check_call([python, "- <<", code], shell=True)
