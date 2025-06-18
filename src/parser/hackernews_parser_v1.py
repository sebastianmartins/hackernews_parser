"""
Parser for HackerNews data in version 1 format.

This parser handles the basic structure of HackerNews data with stories and comments.
It serves as the base for later versions that add more features and complexity.

Example data structure:
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
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class HackerNewsComment:
    """
    Represents a comment in the HackerNews data structure.

    Attributes:
        id (str): Unique identifier for the comment
        author (str): The username of the comment author
        timestamp (str): ISO format timestamp of when the comment was posted
        text (str): The content of the comment
    """

    id: str
    author: str
    timestamp: str
    text: str


@dataclass
class HackerNewsStory:
    """
    Represents a story in the HackerNews data structure.

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


@dataclass
class HackerNewsData:
    """
    Complete HackerNews dataset in version 1 format.

    Attributes:
        version (str): Version of the data format
        timestamp (str): When the data was scraped
        stories (List[HackerNewsStory]): List of stories
    """

    version: str
    timestamp: str
    stories: List[HackerNewsStory]


class HackerNewsParserV1:
    """
    Parser for version 1 of the HackerNews data format.

    This parser handles the basic structure of HackerNews data, converting
    the JSON representation into strongly-typed Python objects. It provides methods
    for parsing both individual stories and comments, as well as the complete dataset.
    """

    def __init__(self, data_path: Path):
        """
        Initialize the parser with the path to the data file.

        Args:
            data_path (Path): Path to the JSON file containing HackerNews data
        """
        self.data_path = data_path
        self._data: Optional[Dict[str, Any]] = None

    def _load_data(self) -> Dict[str, Any]:
        """
        Load and parse the JSON data from the file.

        Returns:
            Dict[str, Any]: The parsed JSON data

        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if self._data is None:
            with open(self.data_path, "r") as f:
                self._data = json.load(f)
        return self._data

    def _parse_comment(self, comment_data: Dict[str, Any]) -> HackerNewsComment:
        """
        Parse a single comment from the raw data.

        Args:
            comment_data (Dict[str, Any]): Raw comment data from JSON

        Returns:
            HackerNewsComment: Parsed comment object
        """
        return HackerNewsComment(
            id=comment_data["id"],
            author=comment_data["author"],
            timestamp=comment_data["timestamp"],
            text=comment_data["text"],
        )

    def _parse_story(self, story_data: Dict[str, Any]) -> HackerNewsStory:
        """
        Parse a single story from the raw data.

        Args:
            story_data (Dict[str, Any]): Raw story data from JSON

        Returns:
            HackerNewsStory: Parsed story object
        """
        return HackerNewsStory(
            id=story_data["id"],
            title=story_data["title"],
            url=story_data["url"],
            domain=story_data["domain"],
            author=story_data["author"],
            timestamp=story_data["timestamp"],
            points=story_data["points"],
            rank=story_data["rank"],
            comments=[
                self._parse_comment(comment)
                for comment in story_data.get("comments", [])
            ],
        )

    def parse(self) -> HackerNewsData:
        """
        Parse the complete dataset from the data file.

        Returns:
            HackerNewsData: Complete parsed dataset

        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
            KeyError: If required fields are missing from the data
        """
        data = self._load_data()
        return HackerNewsData(
            version=data["version"],
            timestamp=data["timestamp"],
            stories=[self._parse_story(story) for story in data["stories"]],
        )


if __name__ == "__main__":
    # Example usage
    parser = HackerNewsParserV1(Path("data/hackernews_v1.json"))
    data = parser.parse()
    print(f"Parsed {len(data.stories)} stories from version {data.version}")
    for story in data.stories:
        print(f"\nStory: {story.title}")
        print(f"Author: {story.author}")
        print(f"Comments: {len(story.comments)}")
