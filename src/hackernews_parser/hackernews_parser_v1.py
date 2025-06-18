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

from pathlib import Path
from typing import Any, Dict, Optional

from hackernews_parser.entities.v1 import (
    HackerNewsComment,
    HackerNewsData,
    HackerNewsStory,
)
from hackernews_parser.utils import load_json


class HackerNewsParserV1:
    """
    Parser for version 1 of the HackerNews data format.

    This parser handles the basic structure of HackerNews data, converting
    the JSON representation into strongly-typed Python objects. It provides methods
    for parsing both individual stories and comments, as well as the complete dataset.
    """

    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize the parser with the path to the data file.

        Args:
            data_path (Path): Path to the JSON file containing HackerNews data
        """
        self.data_path = data_path
        self._data: Optional[Dict[str, Any]] = None

    def _load_data(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Load and parse the JSON data from the file.

        Returns:
            Dict[str, Any]: The parsed JSON data

        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if data is not None:
            self._data = data
        elif self._data is None:
            if self.data_path is None:
                raise ValueError("`data` is required if `data_path` is not provided")
            else:
                self._data = load_json(self.data_path)
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

    def parse(self, data: Optional[Dict[str, Any]] = None) -> HackerNewsData:
        """
        Parse the complete dataset from the data file.

        Returns:
            HackerNewsData: Complete parsed dataset

        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
            KeyError: If required fields are missing from the data
        """
        data = self._load_data(data)
        return HackerNewsData(
            version=data["version"],
            timestamp=data["timestamp"],
            stories=[self._parse_story(story) for story in data["stories"]],
        )


def print_news_data(data: HackerNewsData):
    """
    Print a formatted summary of the parsed HackerNews data.

    Args:
        data (HackerNewsData): The parsed HackerNews dataset to display
    """
    print(f"Parsed {len(data.stories)} stories from version {data.version}")
    for story in data.stories:
        print(f"\nStory: {story.title}")
        print(f"Author: {story.author}")
        print(f"Comments: {len(story.comments)}")


def main(data_file: str):
    """
    Main function to parse and display HackerNews data from a file.

    Args:
        data_file (str): Path to the JSON file containing HackerNews data
    """
    print("Running HackerNews Parser V1...")
    parser = HackerNewsParserV1(Path(data_file))
    data = parser.parse()
    print_news_data(data)
