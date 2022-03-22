from yamlindexer import YamlIndex
from .fixtures.index import FixtureIndex
from unittest import mock, TestCase
import pytest


@pytest.mark.parametrize("level", [1, 2, 10])
@mock.patch('yamlindexer.iglob', return_value=FixtureIndex.globs)
def test_index_levels(mock_iglob, level):
    yi = YamlIndex(globs=FixtureIndex.globs, level=level)
    tc = TestCase()
    tc.maxDiff = None
    tc.assertDictEqual(FixtureIndex.expected_at_level.get(level), yi.index)
