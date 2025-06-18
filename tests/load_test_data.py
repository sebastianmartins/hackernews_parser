"""Load test data for testing."""

from pathlib import Path

from hackernews_parser.utils import load_json


def sample_v1_minimal_data():
    """Sample valid V1 data for testing."""
    return {
        "version": "1.0",
        "timestamp": "2024-03-14T12:00:00Z",
        "stories": [
            {
                "id": "123456",
                "title": "Test Story",
                "url": "https://example.com/test",
                "domain": "example.com",
                "author": "test_author",
                "timestamp": "2024-03-14T10:00:00Z",
                "points": 100,
                "rank": 1,
                "comments": [
                    {
                        "id": "c1",
                        "author": "commenter1",
                        "timestamp": "2024-03-14T11:00:00Z",
                        "text": "Great article!",
                    }
                ],
            }
        ],
    }


def sample_v1_minimal_data_no_stories():
    """Sample valid V1 data for testing."""
    data = sample_v1_minimal_data()
    data.pop("stories")
    return data


def sample_v1_minimal_data_without_comments():
    """Sample valid V1 data for testing."""
    data = sample_v1_minimal_data()
    for story in data["stories"]:
        story.pop("comments")
    return data


def sample_v1_example_data():
    """Sample valid V1 data for testing."""
    return load_json(Path("data/hackernews_v1.json"))


def sample_v2_minimal_data():
    """Sample valid V2 data for testing."""
    return {
        "version": "2.0",
        "timestamp": "2024-03-14T12:00:00Z",
        "stories": [
            {
                "id": "123456",
                "title": "Test Story",
                "url": "https://example.com/test",
                "domain": "example.com",
                "author": "test_author",
                "timestamp": "2024-03-14T10:00:00Z",
                "points": 100,
                "rank": 1,
                "sentiment": {
                    "score": 0.8,
                    "confidence": 0.95,
                    "aspects": ["positive", "informative"],
                },
                "comments": [
                    {
                        "id": "c1",
                        "author": "commenter1",
                        "timestamp": "2024-03-14T11:00:00Z",
                        "text": "Great article!",
                        "sentiment": {
                            "score": 0.9,
                            "confidence": 0.85,
                            "aspects": ["positive", "enthusiastic"],
                        },
                    }
                ],
                "relationships": {
                    "comment_count": 1,
                    "engagement_score": 0.85,
                    "comment_sentiment_avg": 0.85,
                },
            }
        ],
        "metrics": {
            "total_stories": 1,
            "total_comments": 1,
            "avg_sentiment": 0.85,
            "engagement_score": 0.85,
        },
    }


def sample_v2_example_data():
    """Sample valid V2 data for testing."""
    return load_json(Path("data/hackernews_v2.json"))
