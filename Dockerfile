# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Copy source code and README (needed for package metadata)
COPY src/ src/
COPY README.md ./

# Install dependencies and the package
RUN uv sync --frozen --no-dev

# Create data directory for mounted files
RUN mkdir -p /data

# Set the default command to run the parser
ENTRYPOINT ["uv", "run", "hackernews-parser"]

# Default arguments (can be overridden)
CMD ["--help"]
