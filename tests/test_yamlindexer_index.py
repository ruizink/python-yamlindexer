# -*- coding: utf-8 -*-

from unittest import mock, TestCase
import pytest

from yamlindexer.core import YamlIndex
from tests.data import IndexTestsData


@pytest.mark.index
@mock.patch('yamlindexer.core.iglob', return_value=IndexTestsData.globs)
def test_index(mock_iglob):
    yi = YamlIndex(globs=IndexTestsData.globs)
    tc = TestCase()
    tc.maxDiff = None
    tc.assertDictEqual(IndexTestsData.expected_index, yi.index)
