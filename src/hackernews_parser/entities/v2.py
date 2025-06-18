from dataclasses import dataclass
from typing import List, Optional

from hackernews_parser.entities.v1 import HackerNewsComment as V1Comment
from hackernews_parser.entities.v1 import HackerNewsData as V1Data
from hackernews_parser.entities.v1 import HackerNewsStory as V1Story


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
class HackerNewsComment(V1Comment):
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

    sentiment: SentimentAnalysis

    @classmethod
    def from_v1(
        cls, v1_comment: V1Comment, sentiment: Optional[SentimentAnalysis] = None
    ) -> "HackerNewsComment":
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
            sentiment=sentiment or SentimentAnalysis(0.0, 0.0, []),
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
class HackerNewsStory(V1Story):
    """HackerNews data structure with sentiment analysis and relationship metrics.

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

    sentiment: SentimentAnalysis
    relationships: StoryRelationships

    @classmethod
    def from_v1(
        cls, v1_story: V1Story, sentiment: Optional[SentimentAnalysis] = None
    ) -> "HackerNewsStory":
        """
        Create a v2 story from a v1 story, optionally adding sentiment analysis.

        Args:
            v1_story (V1Story): The v1 story to convert
            sentiment (Optional[SentimentAnalysis]): Optional sentiment analysis to add

        Returns:
            HackerNewsStory: A new v2 story with the v1 data and optional sentiment
        """
        v2_comments = [
            HackerNewsComment.from_v1(comment) for comment in v1_story.comments
        ]
        comment_count = len(v2_comments)
        if comment_count > 0:
            engagement_score = (
                sum(comment.sentiment.score for comment in v2_comments) / comment_count
            )
            comment_sentiment_avg = (
                sum(comment.sentiment.score for comment in v2_comments) / comment_count
            )
        else:
            engagement_score = 0.0
            comment_sentiment_avg = 0.0

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
                comment_count=comment_count,
                engagement_score=engagement_score,
                comment_sentiment_avg=comment_sentiment_avg,
            ),
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
class HackerNewsData(V1Data):
    """
    Complete HackerNews dataset in version 2 format.
    Extends the v1 data structure with additional metrics.

    Attributes:
        version (str): Version of the data format
        timestamp (str): When the data was scraped
        stories (List[HackerNewsStory]): List of stories
        metrics (DatasetMetrics): Overall dataset metrics
    """

    metrics: DatasetMetrics
