"""Basic tests for the hackernews parser package."""

from pathlib import Path

from src.parser.hackernews_parser_v1 import HackerNewsParserV1


def test_parser_import():
    """Test that the parser can be imported successfully."""
    parser = HackerNewsParserV1(Path("dummy_path.json"))
    assert parser is not None


def test_parser_initialization():
    """Test that the parser initializes with correct file path."""
    file_path = Path("test_data.json")
    parser = HackerNewsParserV1(file_path)
    assert parser.data_path == file_path


# Add more tests as needed when you have actual data files and functionality to test
