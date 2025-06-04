# Scholar MCP Server

A Python Model Context Protocol (MCP) server that adds Google Scholar search, profile, and citation tools to your AI agents

## Overview

`scholar-mcp` exposes read-only Google Scholar scraping utilities through the [Model Context Protocol](https://modelcontextprotocol.io). When paired with your favourite MCP client (Claude Desktop, Cursor, etc.) an LLM can:

* Search scholarly articles (`getScholarData`)
* Find arXiv mirrors of a result (`getArxivData`)
* Retrieve *cited-by* pages with pagination (`getCitedByData`)
* Scrape author listings (`getScholarProfiles`) and detailed author pages (`getAuthorProfileData`)

A minimal Streamlit front-end is included for manual exploration.

## Quick Start

1. Add your api key to `mcp_agent.secrets.yaml`
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run server

```sh
uv run main.py
```

OR Use [docker](https://docs.docker.com/engine/install/)

```sh
docker build -t scholar-mcp:latest .
docker run --rm -it -v ./mcp_agent.secrets.yaml:/app/mcp_agent.secrets.yaml -p 8501:8501 scholar-mcp:latest
```

OR Use [docker compose](https://docs.docker.com/compose/)

```sh
docker compose up
```

## Acknowledgements

* [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) – provides the companion arXiv tooling
* Built with the amazing [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details
