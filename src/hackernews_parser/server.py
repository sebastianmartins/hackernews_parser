"""
Server entry point for the HackerNews Parser API.

This module provides a way to run the FastAPI application using uvicorn.
"""

import uvicorn


def run_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    """
    Run the FastAPI server with uvicorn.

    Args:
        host: Host address to bind to
        port: Port to listen on
        reload: Enable auto-reload for development
    """
    uvicorn.run(
        "hackernews_parser.api:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    # Run with reload enabled for development
    run_server(reload=True)
