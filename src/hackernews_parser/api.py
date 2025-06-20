"""
FastAPI application for HackerNews data parsing.

This API receives JSON data with a version field and routes it to the appropriate
parser (v1 or v2) based on the version, returning the parsed result.
"""

from dataclasses import asdict
from typing import Any, Dict, Union

from fastapi import FastAPI, HTTPException

from hackernews_parser.hackernews_parser_v1 import HackerNewsParserV1
from hackernews_parser.hackernews_parser_v2 import HackerNewsParserV2

app = FastAPI(
    title="HackerNews Parser API",
    description="API for parsing HackerNews JSON data with version-based routing",
    version="1.0.0",
)


def get_parser(version: str) -> Union[HackerNewsParserV1, HackerNewsParserV2]:
    """
    Get the appropriate parser based on version.

    Args:
        version: Version string from the JSON data

    Returns:
        Parser instance for the specified version

    Raises:
        HTTPException: If version is not supported
    """
    if version == "1.0":
        return HackerNewsParserV1()
    elif version == "2.0":
        return HackerNewsParserV2()
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported version: {version}. Supported versions: 1.0, 2.0",
        )


@app.post("/parse")
async def parse_hackernews_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse HackerNews JSON data using the appropriate parser based on version.

    Args:
        data: JSON data containing version field and HackerNews stories

    Returns:
        Parsed HackerNews data structure

    Raises:
        HTTPException: If version is missing, unsupported, or parsing fails
    """
    try:
        # Validate version field exists
        version = data.get("version")
        if not version:
            raise HTTPException(
                status_code=400, detail="Missing 'version' field in request data"
            )

        # Get appropriate parser and parse data
        parser = get_parser(version)
        parsed_data = parser.parse(data)

        # Convert dataclass to dict for JSON response
        result = asdict(parsed_data)
        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle parsing errors and other exceptions
        raise HTTPException(status_code=500, detail=f"Failed to parse data: {str(e)}")


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with API information."""
    return {"message": "HackerNews Parser API", "docs": "/docs", "health": "/health"}
