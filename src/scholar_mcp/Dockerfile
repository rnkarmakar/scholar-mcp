# ── build stage ────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /app
COPY ../../pyproject.toml .
COPY ../../src ./src
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git
RUN pip install --upgrade pip uv && \
    uv pip install . --no-cache-dir

# ── runtime stage ──────────────────────────────────────────────────────────────
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local /usr/local
ENTRYPOINT ["uv", "tool", "run", "scholar-mcp", "--transport=stdio"]
