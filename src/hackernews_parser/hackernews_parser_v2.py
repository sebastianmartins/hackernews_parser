"""
Parser for HackerNews data in version 2 format.

This parser extends version 1 by adding sentiment analysis and graph relationships
between stories and comments. It maintains backward compatibility with v1 while
adding new features for more sophisticated analysis.

Example data structure:
{
    "version": "2.0",
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
            "sentiment": {
                "score": 0.8,
                "confidence": 0.95,
                "aspects": ["positive", "informative"]
            },
            "comments": [
                {
                    "id": "c1",
                    "author": "Comment author",
                    "timestamp": "2024-03-14T11:00:00Z",
                    "text": "Comment text",
                    "sentiment": {
                        "score": 0.6,
                        "confidence": 0.85,
                        "aspects": ["neutral", "questioning"]
                    }
                }
            ],
            "relationships": {
                "comment_count": 1,
                "engagement_score": 0.75,
                "comment_sentiment_avg": 0.6
            }
        }
    ],
    "metrics": {
        "total_stories": 1,
        "total_comments": 1,
        "avg_sentiment": 0.7,
        "engagement_score": 0.75
    }
}
"""

from pathlib import Path
from typing import Any, Dict, Optional

from hackernews_parser.entities.v2 import (
    DatasetMetrics,
    HackerNewsComment,
    HackerNewsData,
    HackerNewsStory,
    SentimentAnalysis,
    StoryRelationships,
)
from hackernews_parser.hackernews_parser_v1 import HackerNewsParserV1


class HackerNewsParserV2(HackerNewsParserV1):
    """
    Parser for version 2 of the HackerNews data format.
    Extends the v1 parser to handle sentiment analysis and relationship metrics.
    Maintains backward compatibility with v1 while adding new features.
    """

    def _parse_sentiment(self, sentiment_data: Dict[str, Any]) -> SentimentAnalysis:
        """
        Parse sentiment analysis data from the raw data.

        Args:
            sentiment_data (Dict[str, Any]): Raw sentiment data from JSON

        Returns:
            SentimentAnalysis: Parsed sentiment analysis object
        """
        return SentimentAnalysis(
            score=sentiment_data["score"],
            confidence=sentiment_data["confidence"],
            aspects=sentiment_data["aspects"],
        )

    def _parse_relationships(
        self, relationships_data: Dict[str, Any]
    ) -> StoryRelationships:
        """
        Parse relationship metrics from the raw data.

        Args:
            relationships_data (Dict[str, Any]): Raw relationships data from JSON

        Returns:
            StoryRelationships: Parsed relationships object
        """
        return StoryRelationships(
            comment_count=relationships_data["comment_count"],
            engagement_score=relationships_data["engagement_score"],
            comment_sentiment_avg=relationships_data["comment_sentiment_avg"],
        )

    def _parse_comment(self, comment_data: Dict[str, Any]) -> HackerNewsComment:
        """
        Parse a single comment from the raw data, including sentiment analysis.

        Args:
            comment_data (Dict[str, Any]): Raw comment data from JSON

        Returns:
            HackerNewsComment: Parsed comment object with sentiment
        """
        v1_comment = super()._parse_comment(comment_data)
        sentiment = comment_data.get("sentiment", None)
        if sentiment:
            sentiment = self._parse_sentiment(sentiment)
        else:
            sentiment = None
        return HackerNewsComment.from_v1(v1_comment, sentiment)

    def _parse_story(self, story_data: Dict[str, Any]) -> HackerNewsStory:
        """
        Parse a single story from the raw data, including sentiment and relationships.

        Args:
            story_data (Dict[str, Any]): Raw story data from JSON

        Returns:
            HackerNewsStory: Parsed story object with sentiment and relationships
        """
        v2_comments = [
            self._parse_comment(comment) for comment in story_data.get("comments", [])
        ]
        sentiment = story_data.get("sentiment", None)
        if sentiment:
            sentiment = self._parse_sentiment(sentiment)
        else:
            sentiment = SentimentAnalysis(0.0, 0.0, [])
        relationships = story_data.get("relationships", None)
        if relationships:
            relationships = self._parse_relationships(relationships)
        else:
            relationships = None
        return HackerNewsStory(
            id=story_data["id"],
            title=story_data["title"],
            url=story_data["url"],
            domain=story_data["domain"],
            author=story_data["author"],
            timestamp=story_data["timestamp"],
            points=story_data["points"],
            rank=story_data["rank"],
            comments=v2_comments,
            sentiment=sentiment,
            relationships=relationships,
        )

    def parse(self, data: Optional[Dict[str, Any]] = None) -> HackerNewsData:
        """
        Parse the complete dataset from the data file.

        Returns:
            HackerNewsData: Complete parsed dataset with metrics

        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
            KeyError: If required fields are missing from the data
        """
        data = self._load_data(data)
        stories = [self._parse_story(story) for story in data["stories"]]
        metrics = data.get("metrics", None)
        if metrics:
            metrics = DatasetMetrics(
                total_stories=metrics["total_stories"],
                total_comments=metrics["total_comments"],
                avg_sentiment=metrics["avg_sentiment"],
                engagement_score=metrics["engagement_score"],
            )
        else:
            metrics = None
        return HackerNewsData(
            version=data["version"],
            timestamp=data["timestamp"],
            stories=stories,
            metrics=metrics,
        )


def print_news_data(data: HackerNewsData):
    """
    Print a formatted summary of the parsed HackerNews data with v2 features.

    Displays dataset metrics including sentiment analysis and engagement scores,
    as well as detailed information for each story including sentiment and
    relationships.

    Args:
        data (HackerNewsData): The parsed HackerNews dataset to display
    """
    print(f"Parsed {len(data.stories)} stories from version {data.version}")
    if data.metrics:
        print("Dataset metrics:")
        print(f"- Total stories: {data.metrics.total_stories}")
        print(f"- Total comments: {data.metrics.total_comments}")
        print(f"- Average sentiment: {data.metrics.avg_sentiment:.2f}")
        print(f"- Engagement score: {data.metrics.engagement_score:.2f}")

    for story in data.stories:
        print(f"\nStory: {story.title}")
        print(f"Author: {story.author}")
        if story.sentiment:
            print(
                f"Sentiment: {story.sentiment.score:.2f} "
                f"({', '.join(story.sentiment.aspects)})"
            )
        print(f"Comments: {len(story.comments)}")
        if story.relationships:
            print(f"Engagement: {story.relationships.engagement_score:.2f}")


def main(data_file: str):
    """
    Main function to parse and display HackerNews data from a file using v2 parser.

    Uses the enhanced v2 parser to handle sentiment analysis and relationship metrics.

    Args:
        data_file (str): Path to the JSON file containing HackerNews data
    """
    print("Running HackerNews Parser V2...")
    parser = HackerNewsParserV2(Path(data_file))
    data = parser.parse()
    print_news_data(data)
