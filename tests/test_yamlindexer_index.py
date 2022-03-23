from yamlindexer import YamlIndex
from .fixtures.index import FixtureIndex
from unittest import mock, TestCase
import pytest


@pytest.mark.index
@mock.patch('yamlindexer.iglob', return_value=FixtureIndex.globs)
def test_index(mock_iglob):
    yi = YamlIndex(globs=FixtureIndex.globs)
    tc = TestCase()
    tc.maxDiff = None
    tc.assertDictEqual(FixtureIndex.expected, yi.index)
