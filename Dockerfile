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

# Set environment variables for Docker deployment
ENV HOST=0.0.0.0
ENV PORT=8000

# Expose the API port
EXPOSE 8000

# Set the default command to run the API server
ENTRYPOINT ["uv", "run", "python", "-m", "hackernews_parser.server"]

# Default arguments
CMD []
