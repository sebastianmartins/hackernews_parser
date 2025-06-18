import pytest

from hackernews_parser.hackernews_parser_v1 import HackerNewsParserV1
from hackernews_parser.hackernews_parser_v2 import HackerNewsParserV2
from tests.load_test_data import (
    sample_v1_example_data,
    sample_v1_minimal_data,
    sample_v2_example_data,
    sample_v2_minimal_data,
)


class TestCompatibility:
    @pytest.mark.parametrize(
        "data",
        [
            sample_v1_minimal_data,
            sample_v1_example_data,
            sample_v2_minimal_data,
            sample_v2_example_data,
        ],
    )
    def test_parsers_on_common_fields(self, data):
        json_data = data()
        v1_parser = HackerNewsParserV1()
        v2_parser = HackerNewsParserV2()
        v1_data = v1_parser.parse(data=json_data)
        v2_data = v2_parser.parse(data=json_data)
        # compare shared fields
        assert v1_data.version == v2_data.version
        assert v1_data.timestamp == v2_data.timestamp
        assert len(v1_data.stories) == len(v2_data.stories)
        # check internal fields for stories.
        for story_v1, story_v2 in zip(v1_data.stories, v2_data.stories):
            assert story_v1.id == story_v2.id
            assert story_v1.title == story_v2.title
            assert story_v1.url == story_v2.url
            assert story_v1.domain == story_v2.domain
            assert story_v1.author == story_v2.author
            assert story_v1.timestamp == story_v2.timestamp
            assert story_v1.points == story_v2.points
            assert story_v1.rank == story_v2.rank
            assert len(story_v1.comments) == len(story_v2.comments)
            for comment_v1, comment_v2 in zip(story_v1.comments, story_v2.comments):
                assert comment_v1.id == comment_v2.id
                assert comment_v1.author == comment_v2.author
                assert comment_v1.timestamp == comment_v2.timestamp
                assert comment_v1.text == comment_v2.text
