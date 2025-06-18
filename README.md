# Hacker News Parser

A Python-based parser for JSON data obtained from scraping [Hacker News](https://news.ycombinator.com/).
Everything here (including this README) was produced with the assistance of AI.

This project provides two versions of parsers that convert raw JSON data into strongly-typed Python objects, making it easier to work with Hacker News data programmatically.

## Features

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

## Usage

### Basic Usage

```bash
# Parse version 1 data
python -m src.parser.hackernews_parser_v1

# Parse version 2 data
python -m src.parser.hackernews_parser_v2
```

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# How to run the project


# Run locally using UV

*NOTE:* follow this docs to install uv: https://docs.astral.sh/uv/getting-started/installation/

1. Install dependencies

```bash
uv sync --dev
```

2. Install pre-commit hooks

```bash
uv run pre-commit install
```

3. Run the tests

```bash
uv run pytest
```

4. Run the parsers from main point

```bash
uv pip install -e .
```
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



# Run on docker

1. Build the docker image

```bash
docker build -t hackernews-parser .
```

2. Run the docker container (using local file)

* Show help
```bash
docker run --rm hackernews-parser
```

* Run version 1 parser (Mounting directory)
```bash
docker run --rm -v $(pwd)/data/hackernews_v1.json:/data/input.json hackernews-parser --version 1 --data-file /data/input.json
```

* Run version 2 parser (Mounting directory)
```bash
docker run --rm -v $(pwd)/data/hackernews_v2.json:/data/input.json hackernews-parser --version 2 --data-file /data/input.json
```


# Documenting process

# add initial project structure and linting improvements
1. Add package structure (using UV)
2. Adding pre-commit hooks and github actions
3. Fixing linting errors (unused imports, formatting, etc) and add tests folder (with dummy test)


# Working on improving the project
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


# Clarification needed:

* Engagement_score: logic needs clarification. Is average the right implementation?
* Any reason to have timestamps as str and not as timestamp?
* Do we want to allow parser V2 to run on json data with V1? Or should we use each version as an indicator of which parser to use?



# TODO:
1. Refactor project using better versioning pattern: either `Plugin Architecture` or `Feature-Based Parsing`.
3. Add validation between metrics and individual stories. Raising errors if they don't match.
2. Improve error messages for missing fields in the data.
