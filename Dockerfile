FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN uv tool install arxiv-mcp-server

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked

ADD . /app

RUN mv mcp_agent.config.yaml.docker mcp_agent.config.yaml

EXPOSE 8501

CMD ["uv", "run", "main.py"]
