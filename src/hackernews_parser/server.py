"""
Server entry point for the HackerNews Parser API.

This module provides a way to run the FastAPI application using uvicorn.
Host and port can be configured via environment variables.
"""

import os
from typing import Optional

import uvicorn


def run_server(
    host: Optional[str] = None, port: Optional[int] = None, reload: bool = False
):
    """
    Run the FastAPI server with uvicorn.

    Args:
        host: Host address to bind to (defaults to HOST env var or 127.0.0.1)
        port: Port to listen on (defaults to PORT env var or 8000)
        reload: Enable auto-reload for development
    """
    # Use environment variables with sensible defaults
    if host is None:
        host = os.getenv("HOST", "127.0.0.1")
    if port is None:
        port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "hackernews_parser.api:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    # Run with reload enabled for development
    run_server(reload=True)
