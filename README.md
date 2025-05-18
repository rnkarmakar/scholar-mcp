# Scholar MCP Server

> **A Python Model Context Protocol (MCP) server that adds Google Scholar search, profile, and citation tools to your AI agents.**

|         |  Status                                                                           |
| ------- | --------------------------------------------------------------------------------- |
| Build   | ![CI](https://github.com/your‑org/scholar-mcp/actions/workflows/ci.yml/badge.svg) |
| Docker  | `ghcr.io/your‑org/scholar-mcp:latest`                                             |
| License | MIT                                                                               |

---

\## Overview
`scholar-mcp` exposes read‑only Google Scholar scraping utilities through the [Model Context Protocol](https://modelcontextprotocol.io).  When paired with your favourite MCP client (Claude Desktop, Cursor, etc.) an LLM can:

* Search scholarly articles (`getScholarData`)
* Find arXiv mirrors of a result (`getArxivData`)
* Retrieve *cited‑by* pages with pagination (`getCitedByData`)
* Scrape author listings (`getScholarProfiles`) and detailed author pages (`getAuthorProfileData`)

A minimal Streamlit front‑end is included for manual exploration.

---

\## Directory Structure

```text
src/
  scholar_mcp/
    __init__.py           ← package marker
    tool.py               ← FastMCP server (Google Scholar tools)
    ui/
      streamlit_app.py    ← optional Web UI
    Dockerfile            ← container image
mcp_agent.config.yaml     ← example multi‑server config (Scholar + arXiv)
```

---

\## Quick Start
\### 1 Install (editable)

```bash
pip install -e .  # requires Python ≥ 3.10
uv pip install arxiv-mcp-server  # optional companion server
```

\### 2 Run the server

```bash
uv tool run scholar-mcp --transport=stdio
```

\### 3 Docker

```bash
docker build -t scholar-mcp:latest -f src/scholar_mcp/Dockerfile .
docker run --rm scholar-mcp:latest
```

\### 4 Streamlit demo

```bash
streamlit run src/scholar_mcp/ui/streamlit_app.py
```

---

\## Using in an MCP ecosystem
Add the following block to your client‑side *mcp\_agent.config.yaml*:

```yaml
mcp:
  servers:
    scholar-mcp:
      command: uv
      args:
        - tool
        - run
        - scholar-mcp
        - --transport=stdio
    arxiv-mcp-server:
      command: uv
      args:
        - tool
        - run
        - arxiv-mcp-server
        - --storage-path
        - ./data/arxiv_papers
```

Now an agent can call any Scholar or arXiv tool seamlessly.

---

\## Development

```bash
# lint & type‑check
ruff check src/scholar_mcp
mypy src/scholar_mcp

# run unit tests (coming soon)
pytest -q
```

---

\## Acknowledgements

* **[blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server)** – provides the companion arXiv tooling used in our example config.
* Built with the amazing [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).

---

\## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
