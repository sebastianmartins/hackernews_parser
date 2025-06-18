from typing import Any, Dict

import pytest

from hackernews_parser.entities.v1 import HackerNewsData
from hackernews_parser.hackernews_parser_v1 import HackerNewsParserV1
from hackernews_parser.utils import load_json
from tests.load_test_data import (
    sample_v1_minimal_data,
    sample_v1_minimal_data_no_stories,
    sample_v1_minimal_data_without_comments,
    sample_v2_example_data,
    sample_v2_minimal_data,
)


def assert_equal_hackernews_data(
    hackernews_data: HackerNewsData, json_data: Dict[str, Any]
):
    assert hackernews_data.version == json_data["version"]
    assert hackernews_data.timestamp == json_data["timestamp"]
    assert len(hackernews_data.stories) == len(json_data["stories"])
    for story_v1, story_json in zip(hackernews_data.stories, json_data["stories"]):
        assert story_v1.id == story_json["id"]
        assert story_v1.title == story_json["title"]
        assert story_v1.url == story_json["url"]
        assert story_v1.domain == story_json["domain"]
        assert story_v1.author == story_json["author"]
        assert story_v1.timestamp == story_json["timestamp"]
        assert story_v1.points == story_json["points"]
        assert story_v1.rank == story_json["rank"]
        assert len(story_v1.comments) == len(story_json.get("comments", []))
        for comment_v1, comment_json in zip(
            story_v1.comments, story_json.get("comments", [])
        ):
            assert comment_v1.id == comment_json["id"]
            assert comment_v1.author == comment_json["author"]
            assert comment_v1.timestamp == comment_json["timestamp"]
            assert comment_v1.text == comment_json["text"]


class TestHackerNewsParserV1:
    def test_path_vs_data(self):
        data_path = "data/hackernews_v1.json"
        # parse from path
        v1_parser_path = HackerNewsParserV1(data_path=data_path)
        v1_data_path = v1_parser_path.parse()
        # parse from json data
        data = load_json(data_path)
        v1_parser_data = HackerNewsParserV1()
        v1_data_data = v1_parser_data.parse(data=data)
        assert v1_data_path == v1_data_data

    @pytest.mark.parametrize(
        "data",
        [
            sample_v1_minimal_data,
            sample_v1_minimal_data_without_comments,
            sample_v2_minimal_data,
            sample_v2_example_data,
        ],
    )
    def test_parse_with_stories(self, data):
        json_data = data()
        v1_parser = HackerNewsParserV1()
        v1_data = v1_parser.parse(data=json_data)
        assert_equal_hackernews_data(v1_data, json_data)

    def test_parse_data_no_stories(self):
        data = sample_v1_minimal_data_no_stories()
        assert "stories" not in data
        v1_parser = HackerNewsParserV1()
        with pytest.raises(KeyError):
            v1_parser.parse(data=data)
