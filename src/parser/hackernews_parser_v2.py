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

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from .hackernews_parser_v1 import (
    HackerNewsComment as V1Comment,
    HackerNewsStory as V1Story,
    HackerNewsData as V1Data,
    HackerNewsParserV1
)


@dataclass
class SentimentAnalysis:
    """
    Represents sentiment analysis results for a story or comment.
    
    Attributes:
        score (float): Sentiment score between -1.0 (negative) and 1.0 (positive)
        confidence (float): Confidence in the sentiment analysis between 0.0 and 1.0
        aspects (List[str]): List of sentiment aspects identified in the text
    """
    score: float
    confidence: float
    aspects: List[str]


@dataclass
class HackerNewsComment:
    """
    Represents a comment in the HackerNews data structure with sentiment analysis.
    Extends the v1 comment structure with additional sentiment information.
    
    Attributes:
        id (str): Unique identifier for the comment
        author (str): The username of the comment author
        timestamp (str): ISO format timestamp of when the comment was posted
        text (str): The content of the comment
        sentiment (SentimentAnalysis): Sentiment analysis results for the comment
    """
    id: str
    author: str
    timestamp: str
    text: str
    sentiment: SentimentAnalysis

    @classmethod
    def from_v1(cls, v1_comment: V1Comment, sentiment: Optional[SentimentAnalysis] = None) -> 'HackerNewsComment':
        """
        Create a v2 comment from a v1 comment, optionally adding sentiment analysis.
        
        Args:
            v1_comment (V1Comment): The v1 comment to convert
            sentiment (Optional[SentimentAnalysis]): Optional sentiment analysis to add
            
        Returns:
            HackerNewsComment: A new v2 comment with the v1 data and optional sentiment
        """
        return cls(
            id=v1_comment.id,
            author=v1_comment.author,
            timestamp=v1_comment.timestamp,
            text=v1_comment.text,
            sentiment=sentiment or SentimentAnalysis(0.0, 0.0, [])
        )


@dataclass
class StoryRelationships:
    """
    Represents relationships and engagement metrics for a story.
    
    Attributes:
        comment_count (int): Number of comments on the story
        engagement_score (float): Overall engagement score between 0.0 and 1.0
        comment_sentiment_avg (float): Average sentiment score of all comments
    """
    comment_count: int
    engagement_score: float
    comment_sentiment_avg: float


@dataclass
class HackerNewsStory:
    """
    Represents a story in the HackerNews data structure with sentiment analysis
    and relationship metrics. Extends the v1 story structure with additional
    sentiment and relationship information.
    
    Attributes:
        id (str): Unique identifier for the story
        title (str): The title of the story
        url (str): The URL of the story
        domain (str): The domain name of the story URL
        author (str): The username of the story author
        timestamp (str): ISO format timestamp of when the story was posted
        points (int): Number of upvotes
        rank (int): Position on the front page
        comments (List[HackerNewsComment]): List of comments on the story
        sentiment (SentimentAnalysis): Sentiment analysis results for the story
        relationships (StoryRelationships): Relationship and engagement metrics
    """
    id: str
    title: str
    url: str
    domain: str
    author: str
    timestamp: str
    points: int
    rank: int
    comments: List[HackerNewsComment]
    sentiment: SentimentAnalysis
    relationships: StoryRelationships

    @classmethod
    def from_v1(cls, v1_story: V1Story, sentiment: Optional[SentimentAnalysis] = None) -> 'HackerNewsStory':
        """
        Create a v2 story from a v1 story, optionally adding sentiment analysis.
        
        Args:
            v1_story (V1Story): The v1 story to convert
            sentiment (Optional[SentimentAnalysis]): Optional sentiment analysis to add
            
        Returns:
            HackerNewsStory: A new v2 story with the v1 data and optional sentiment
        """
        v2_comments = [HackerNewsComment.from_v1(comment) for comment in v1_story.comments]
        return cls(
            id=v1_story.id,
            title=v1_story.title,
            url=v1_story.url,
            domain=v1_story.domain,
            author=v1_story.author,
            timestamp=v1_story.timestamp,
            points=v1_story.points,
            rank=v1_story.rank,
            comments=v2_comments,
            sentiment=sentiment or SentimentAnalysis(0.0, 0.0, []),
            relationships=StoryRelationships(
                comment_count=len(v2_comments),
                engagement_score=0.0,  # Default value, should be calculated
                comment_sentiment_avg=0.0  # Default value, should be calculated
            )
        )


@dataclass
class DatasetMetrics:
    """
    Represents overall metrics for the entire dataset.
    
    Attributes:
        total_stories (int): Total number of stories in the dataset
        total_comments (int): Total number of comments in the dataset
        avg_sentiment (float): Average sentiment score across all stories and comments
        engagement_score (float): Overall engagement score for the dataset
    """
    total_stories: int
    total_comments: int
    avg_sentiment: float
    engagement_score: float


@dataclass
class HackerNewsData:
    """
    Complete HackerNews dataset in version 2 format.
    Extends the v1 data structure with additional metrics.
    
    Attributes:
        version (str): Version of the data format
        timestamp (str): When the data was scraped
        stories (List[HackerNewsStory]): List of stories
        metrics (DatasetMetrics): Overall dataset metrics
    """
    version: str
    timestamp: str
    stories: List[HackerNewsStory]
    metrics: DatasetMetrics


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
            score=sentiment_data['score'],
            confidence=sentiment_data['confidence'],
            aspects=sentiment_data['aspects']
        )

    def _parse_relationships(self, relationships_data: Dict[str, Any]) -> StoryRelationships:
        """
        Parse relationship metrics from the raw data.
        
        Args:
            relationships_data (Dict[str, Any]): Raw relationships data from JSON
            
        Returns:
            StoryRelationships: Parsed relationships object
        """
        return StoryRelationships(
            comment_count=relationships_data['comment_count'],
            engagement_score=relationships_data['engagement_score'],
            comment_sentiment_avg=relationships_data['comment_sentiment_avg']
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
        sentiment = self._parse_sentiment(comment_data['sentiment'])
        return HackerNewsComment.from_v1(v1_comment, sentiment)

    def _parse_story(self, story_data: Dict[str, Any]) -> HackerNewsStory:
        """
        Parse a single story from the raw data, including sentiment and relationships.
        
        Args:
            story_data (Dict[str, Any]): Raw story data from JSON
            
        Returns:
            HackerNewsStory: Parsed story object with sentiment and relationships
        """
        v1_story = super()._parse_story(story_data)
        sentiment = self._parse_sentiment(story_data['sentiment'])
        relationships = self._parse_relationships(story_data['relationships'])
        return HackerNewsStory(
            id=v1_story.id,
            title=v1_story.title,
            url=v1_story.url,
            domain=v1_story.domain,
            author=v1_story.author,
            timestamp=v1_story.timestamp,
            points=v1_story.points,
            rank=v1_story.rank,
            comments=v1_story.comments,
            sentiment=sentiment,
            relationships=relationships
        )

    def parse(self) -> HackerNewsData:
        """
        Parse the complete dataset from the data file.
        
        Returns:
            HackerNewsData: Complete parsed dataset with metrics
            
        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
            KeyError: If required fields are missing from the data
        """
        data = self._load_data()
        stories = [self._parse_story(story) for story in data['stories']]
        metrics = DatasetMetrics(
            total_stories=data['metrics']['total_stories'],
            total_comments=data['metrics']['total_comments'],
            avg_sentiment=data['metrics']['avg_sentiment'],
            engagement_score=data['metrics']['engagement_score']
        )
        return HackerNewsData(
            version=data['version'],
            timestamp=data['timestamp'],
            stories=stories,
            metrics=metrics
        )


if __name__ == "__main__":
    # Example usage
    parser = HackerNewsParserV2(Path("data/hackernews_v2.json"))
    data = parser.parse()
    print(f"Parsed {len(data.stories)} stories from version {data.version}")
    print(f"Dataset metrics:")
    print(f"- Total stories: {data.metrics.total_stories}")
    print(f"- Total comments: {data.metrics.total_comments}")
    print(f"- Average sentiment: {data.metrics.avg_sentiment:.2f}")
    print(f"- Engagement score: {data.metrics.engagement_score:.2f}")
    
    for story in data.stories:
        print(f"\nStory: {story.title}")
        print(f"Author: {story.author}")
        print(f"Sentiment: {story.sentiment.score:.2f} ({', '.join(story.sentiment.aspects)})")
        print(f"Comments: {len(story.comments)}")
        print(f"Engagement: {story.relationships.engagement_score:.2f}") 