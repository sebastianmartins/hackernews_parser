from dataclasses import dataclass
from typing import List


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
