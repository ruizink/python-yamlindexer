from yamlindexer import YamlIndex
from unittest import TestCase
import pytest


t = TestCase()


@pytest.mark.parametrize("level", [1, 2, 10])
def test_find_kv(level):
    yi = YamlIndex(root_path='tests', level=level)
    t.assertCountEqual(yi.find(kind='Deployment'), [
        'tests/fixtures/yaml/deployment.yaml',
    ])
    t.assertCountEqual(yi.find(kind='Pod'), [
        'tests/fixtures/yaml/pod.yaml',
    ])
    t.assertCountEqual(yi.find(apiVersion='v1'), [
        'tests/fixtures/yaml/pod.yaml',
        'tests/fixtures/yaml/service.yaml',
    ])
    t.assertCountEqual(yi.find(kind='Deployment', apiVersion='apps/v1'), [
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.parametrize("level", [1, 2, 10])
def test_find(level):
    yi = YamlIndex(root_path='tests', level=level)

    t.assertCountEqual(yi.find_one_of([
        {'kind': 'Deployment'},
    ]), [
        'tests/fixtures/yaml/deployment.yaml',
    ])
    t.assertCountEqual(yi.find_one_of([
        {'kind': 'Pod'},
    ]), [
        'tests/fixtures/yaml/pod.yaml',
    ])
    t.assertCountEqual(yi.find_one_of([
        {'apiVersion': 'v1'},
    ]), [
        'tests/fixtures/yaml/pod.yaml',
        'tests/fixtures/yaml/service.yaml',
    ])
    t.assertCountEqual(yi.find_one_of([
        {'kind': 'Deployment'},
        {'kind': 'Pod'},
    ]), [
        'tests/fixtures/yaml/pod.yaml',
        'tests/fixtures/yaml/deployment.yaml',
    ])
    t.assertCountEqual(yi.find_one_of([
        {'kind': 'Deployment', 'apiVersion': 'v1'},
    ]), [])
    t.assertCountEqual(yi.find_one_of([
        {'kind': 'Deployment', 'apiVersion': 'apps/v1'},
    ]), [
        'tests/fixtures/yaml/deployment.yaml',
    ])
    t.assertCountEqual(yi.find_one_of([
        {'kind': 'Deployment', 'apiVersion': 'apps/v1'},
    ]), [
        'tests/fixtures/yaml/deployment.yaml',
    ])
    t.assertCountEqual(yi.find_one_of([
        {'kind': 'Deployment', 'apiVersion': 'apps/v1'},
        {'kind': 'Pod'},
    ]), [
        'tests/fixtures/yaml/deployment.yaml',
        'tests/fixtures/yaml/pod.yaml',
    ])


def test_find_dpath():
    yi = YamlIndex(root_path='tests', level=10)

    t.assertCountEqual(yi.search_xpath('/spec/template/spec/containers/*/image/nginx'), [
        'tests/fixtures/yaml/deployment.yaml',
    ])
    t.assertCountEqual(yi.search_xpath('/spec/ports/*/port/80'), [
        'tests/fixtures/yaml/service.yaml',
    ])
    t.assertCountEqual(yi.search_xpath('/metadata/name/nginx'), [
        'tests/fixtures/yaml/service.yaml',
        'tests/fixtures/yaml/deployment.yaml',
        'tests/fixtures/yaml/pod.yaml',
    ])
