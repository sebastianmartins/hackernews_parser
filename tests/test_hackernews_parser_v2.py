from typing import Any, Dict, Union

import pytest

from hackernews_parser.entities.v1 import HackerNewsComment as V1Comment
from hackernews_parser.entities.v2 import (
    DatasetMetrics,
    HackerNewsComment,
    HackerNewsData,
    SentimentAnalysis,
    StoryRelationships,
)
from hackernews_parser.hackernews_parser_v2 import HackerNewsParserV2
from hackernews_parser.utils import load_json
from tests.load_test_data import (
    sample_v1_minimal_data,
    sample_v1_minimal_data_no_stories,
    sample_v1_minimal_data_without_comments,
    sample_v2_example_data,
    sample_v2_minimal_data,
)
from tests.test_hackernews_parser_v1 import (
    assert_equal_hackernews_data as assert_equal_hackernews_data_v1,
)


def assert_equal_sentiment(
    sentiment_v2: SentimentAnalysis, sentiment_json: Dict[str, Any]
) -> None:
    assert sentiment_v2.score == sentiment_json["score"]
    assert sentiment_v2.confidence == sentiment_json["confidence"]
    assert sentiment_v2.aspects == sentiment_json["aspects"]


def assert_equal_story_relationships(
    story_relationships_v2: StoryRelationships, story_relationships_json: Dict[str, Any]
) -> None:
    assert (
        story_relationships_v2.comment_count
        == story_relationships_json["comment_count"]
    )
    assert (
        story_relationships_v2.engagement_score
        == story_relationships_json["engagement_score"]
    )
    assert (
        story_relationships_v2.comment_sentiment_avg
        == story_relationships_json["comment_sentiment_avg"]
    )


def assert_equal_comment(
    comment_v2: Union[HackerNewsComment, V1Comment], comment_json: Dict[str, Any]
) -> None:
    assert comment_v2.id == comment_json["id"]
    assert comment_v2.author == comment_json["author"]
    assert comment_v2.timestamp == comment_json["timestamp"]
    assert comment_v2.text == comment_json["text"]
    # Only check sentiment if it's a v2 comment
    if isinstance(comment_v2, HackerNewsComment):
        assert_equal_sentiment(comment_v2.sentiment, comment_json["sentiment"])


def assert_equal_metrics(
    metrics_v2: Union[DatasetMetrics, None], metrics_json: Dict[str, Any]
):
    if metrics_json is None:
        assert metrics_v2 is None
        return
    # At this point, metrics_json is not None, so metrics_v2 should also not be None
    assert metrics_v2 is not None
    assert metrics_v2.total_stories == metrics_json["total_stories"]
    assert metrics_v2.total_comments == metrics_json["total_comments"]
    assert metrics_v2.avg_sentiment == metrics_json["avg_sentiment"]
    assert metrics_v2.engagement_score == metrics_json["engagement_score"]


def assert_equal_hackernews_data(
    hackernews_data: HackerNewsData, json_data: Dict[str, Any]
) -> None:
    assert hackernews_data.version == json_data["version"]
    assert hackernews_data.timestamp == json_data["timestamp"]
    assert len(hackernews_data.stories) == len(json_data["stories"])
    for story_v2, story_json in zip(hackernews_data.stories, json_data["stories"]):
        assert story_v2.id == story_json["id"]
        assert story_v2.title == story_json["title"]
        assert story_v2.url == story_json["url"]
        assert story_v2.domain == story_json["domain"]
        assert story_v2.author == story_json["author"]
        assert story_v2.timestamp == story_json["timestamp"]
        assert story_v2.points == story_json["points"]
        assert story_v2.rank == story_json["rank"]
        assert_equal_sentiment(story_v2.sentiment, story_json["sentiment"])
        assert len(story_v2.comments) == len(story_json.get("comments", []))
        for comment_v2, comment_json in zip(
            story_v2.comments, story_json.get("comments", [])
        ):
            assert_equal_comment(comment_v2, comment_json)
        assert_equal_story_relationships(
            story_v2.relationships, story_json["relationships"]
        )
    assert_equal_metrics(hackernews_data.metrics, json_data["metrics"])


class TestHackerNewsParserV2:
    def test_path_vs_data(self):
        data_path = "data/hackernews_v2.json"
        # parse from path
        v2_parser_path = HackerNewsParserV2(data_path=data_path)
        v2_data_path = v2_parser_path.parse()
        # parse from json data
        data = load_json(data_path)
        v2_parser_data = HackerNewsParserV2()
        v2_data_data = v2_parser_data.parse(data=data)
        assert v2_data_path == v2_data_data

    @pytest.mark.parametrize(
        "data",
        [
            sample_v2_minimal_data,
            sample_v2_example_data,
        ],
    )
    def test_parse_with_stories(self, data):
        json_data = data()
        v2_parser = HackerNewsParserV2()
        v2_data = v2_parser.parse(data=json_data)
        assert_equal_hackernews_data(v2_data, json_data)

    def test_parse_data_no_stories(self):
        data = sample_v1_minimal_data_no_stories()
        assert "stories" not in data
        v2_parser = HackerNewsParserV2()
        with pytest.raises(KeyError):
            v2_parser.parse(data=data)

    @pytest.mark.parametrize(
        "data",
        [
            sample_v1_minimal_data,
            sample_v1_minimal_data_without_comments,
        ],
    )
    def test_parse_v1_news(self, data):
        json_data = data()
        v2_parser = HackerNewsParserV2()
        v2_data = v2_parser.parse(data=json_data)
        assert_equal_hackernews_data_v1(v2_data, json_data)

    def test_parse_no_sentiments(self):
        json_data = sample_v2_minimal_data()
        json_data["stories"][0]["comments"][0]["sentiment"] = None
        json_data["stories"][0]["sentiment"] = None
        v2_parser = HackerNewsParserV2()
        v2_data = v2_parser.parse(data=json_data)
        assert len(v2_data.stories[0].comments) == 1
        assert v2_data.stories[0].sentiment.score == 0.0
        assert v2_data.stories[0].sentiment.confidence == 0.0
        assert v2_data.stories[0].sentiment.aspects == []
        assert v2_data.stories[0].comments[0].sentiment.score == 0.0
        assert v2_data.stories[0].comments[0].sentiment.confidence == 0.0
        assert v2_data.stories[0].comments[0].sentiment.aspects == []

    def test_parse_no_sentiments_no_comments(self):
        json_data = sample_v2_minimal_data()
        json_data["stories"][0]["comments"] = []
        v2_parser = HackerNewsParserV2()
        v2_data = v2_parser.parse(data=json_data)
        assert len(v2_data.stories[0].comments) == 0
        assert_equal_hackernews_data(v2_data, json_data)

    def test_parse_no_metrics(self):
        json_data = sample_v2_minimal_data()
        json_data["metrics"] = None
        v2_parser = HackerNewsParserV2()
        v2_data = v2_parser.parse(data=json_data)
        assert v2_data.metrics is None
        assert_equal_hackernews_data(v2_data, json_data)
