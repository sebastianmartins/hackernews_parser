# Hacker News Parser

A Python-based parser for JSON data obtained from scraping [Hacker News](https://news.ycombinator.com/).
Everything here (including this README) was produced with the assistance of AI.

This project provides both a FastAPI REST API and command-line parsers that convert raw JSON data into strongly-typed Python objects, making it easier to work with Hacker News data programmatically.

## Features

- **🚀 FastAPI REST API**: HTTP endpoints for parsing HackerNews data
  - Automatic version-based routing (v1 and v2)
  - Interactive API documentation
  - Health checks and error handling
  - Docker support

- **Version 1 Parser**: Handles basic story and comment data
  - Story metadata (title, URL, domain, author, points, rank)
  - Comment data (author, timestamp, text)
  - Strongly-typed Python objects using dataclasses

- **Version 2 Parser**: Extends V1 with additional features
  - Sentiment analysis
  - Relationship metrics
  - Backward compatible with V1 data format

## Prerequisites

- Python 3.13 or higher
- Docker (optional, for containerized deployment)

## Quick Start

### 🚀 API Usage (Recommended)

Start the API server:
```bash
uv run hackernews-api
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

**Configuration via Environment Variables:**
```bash
# Bind to all interfaces (useful for containers or remote access)
HOST=0.0.0.0 uv run hackernews-api

# Use a different port
PORT=3000 uv run hackernews-api

# Combine multiple settings
HOST=0.0.0.0 PORT=3000 uv run hackernews-api
```

**Alternative direct method:**
```bash
# For direct server startup with custom settings
uv run python -c "from hackernews_parser.server import run_server; run_server(host='0.0.0.0', port=3000)"
```

Send data to parse:
```bash
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d @data/hackernews_v1.json
```

### 📋 CLI Usage



### Data Format

The parsers expect JSON data in the following format:

```json
{
    "version": "1.0",
    "timestamp": "2024-03-14T12:00:00Z",
    "stories": [
        {
            "id": "123",
            "title": "Story title",
            "url": "Story URL",
            "domain": "Domain name",
            "author": "Author name",
            "timestamp": "2024-03-14T10:00:00Z",
            "points": 123,
            "rank": 1,
            "comments": [
                {
                    "id": "c1",
                    "author": "Comment author",
                    "timestamp": "2024-03-14T11:00:00Z",
                    "text": "Comment text"
                }
            ]
        }
    ]
}
```

## Development

Each parser version builds on the previous one, maintaining backward compatibility while adding new features. The parsers use Python dataclasses to ensure type safety and provide a clean interface for working with the data.



# How to run the project


## Run locally using UV

*NOTE:* follow this docs to install uv: https://docs.astral.sh/uv/getting-started/installation/

1. Install dependencies

```bash
uv sync --dev
source .venv/bin/activate
```

2. (Optional) Install pre-commit hooks

```bash
uv run pre-commit install
```
**NOTE:** this will show an error if you are not in a Git repository directory.

3. Run the tests

```bash
uv run pytest
```

4. Run the parsers from main point

Running version 1 parser:
```bash
uv run hackernews-parser --version 1 --data-file data/hackernews_v1.json
```

Running version 2 parser:

```bash
uv run hackernews-parser --version 2 --data-file data/hackernews_v2.json
```


*  Running pre-commit hooks manually

```bash
uv run pre-commit run --all-files
```



## 🐳 Run with Docker

### API Server (Default)

1. Build the docker image
```bash
docker build -t hackernews-parser .
```

2. Run the API server
```bash
# Default: binds to 0.0.0.0:8000 inside container
docker run --rm -p 8000:8000 hackernews-parser

# Custom port mapping (container uses 8000, host uses 3000)
docker run --rm -p 3000:8000 hackernews-parser

# Override container port via environment variables
docker run --rm -p 9000:9000 -e PORT=9000 hackernews-parser
```

3. Test the API
```bash
# Health check
curl http://localhost:8000/health

# Parse v1 data
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d @data/hackernews_v1.json

# Parse v2 data
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d @data/hackernews_v2.json
```

### CLI Parser (Alternative)

Run the CLI parser by overriding the entrypoint:

```bash
# Show help
docker run --rm --entrypoint "uv" hackernews-parser run hackernews-parser --help

# Run version 1 parser
docker run --rm -v $(pwd)/data:/data --entrypoint "uv" \
  hackernews-parser run hackernews-parser --version 1 --data-file /data/hackernews_v1.json

# Run version 2 parser
docker run --rm -v $(pwd)/data:/data --entrypoint "uv" \
  hackernews-parser run hackernews-parser --version 2 --data-file /data/hackernews_v2.json
```


# Documenting Development  Process

## add initial project structure and linting improvements
1. Add package structure (using UV)
2. Adding pre-commit hooks and github actions
3. Fixing linting errors (unused imports, formatting, etc) and add tests folder (with dummy test)


## Working on improving the project
1. Refactor entities out of the parser logic
2. Fix `incompatibility type errors` between v1 and v2 parsers. Using inheritance.
3. Add tests for the parsers: backward compatibility, full functionality v1 and v2.
4. Fix `HackerNewsStory.from_v1`.
* Create v2_comments, rather than using from_v1. Avoiding class incompatibility.
* Calculate missing fields:
WHY: the function recieves an optional parameter that can have scores.
    - engagement score: logic needs to be verified as unclear from code. Is average of all comments correct?
    - comment sentiment avg.
5. Fix `HackerNewsParserV2._parse_story`.
    * Code is parent class is using V2 method, but it's creating an instance of V1.
    * Fix: Create a V2 instance, as V1 has a different behaviour than V2 in comments.
6. Fix `HackerNewsData.stories` type to avoid type incompatibility, by overriding the field in the dataclass.
7. Fix: `HackerNewsParserV2` backward compatibility with V1 data. Adjusting `HackerNewsData.metrics` to be optional.
8. Add central point for running the parsers.


## Clarification needed:

* Engagement_score: logic needs clarification. Is average the right implementation?
* Any reason to have timestamps as str and not as timestamp?
* Do we want to allow parser V2 to run on json data with V1? Or should we use each version as an indicator of which parser to use?
* Do we want to allow parser V1 to run on json data with V2? or should we raise an error indicating that a newer versions should be used instead?



# TODO:
1. Refactor project using better versioning pattern: either `Plugin Architecture` or `Feature-Based Parsing`.
2. Add validation between metrics and individual stories. Raising errors if they don't match.
3. **Inconsistent error handling**: Improve error messages for missing fields in the data.
4. **Missing Input Validation**: Add validation for the input data.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## 🚀 API Reference

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/parse` | Parse HackerNews JSON data (auto-detects version) |
| GET    | `/health` | Health check endpoint |
| GET    | `/` | Root endpoint with API information |
| GET    | `/docs` | Interactive Swagger UI documentation |

### API Usage Examples

**Parse Version 1.0 Data:**
```bash
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "1.0",
    "timestamp": "2024-03-14T12:00:00Z",
    "stories": [...]
  }'
```

**Parse Version 2.0 Data:**
```bash
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "2.0",
    "timestamp": "2024-03-14T12:00:00Z",
    "stories": [...],
    "metrics": {...}
  }'
```

**Using Example Files:**
```bash
# Parse v1 example data
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d @data/hackernews_v1.json

# Parse v2 example data
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d @data/hackernews_v2.json
```

**Run the demo script:**
```bash
uv run python examples/api_usage.py
```

**Access interactive documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Response Format

The API automatically detects the version from your JSON data and routes to the appropriate parser. The response maintains the same structure as the input but with parsed and validated data.
