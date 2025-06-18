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
