from yamlindexer import YamlIndex
from unittest import TestCase
import pytest


t = TestCase()
yi = YamlIndex(root_path='tests/fixtures')


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )


@pytest.mark.search_kv
def test_search_kv_1():
    t.assertCountEqual(yi.search_kv(kind='Deployment'), [
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.search_kv
def test_search_kv_2():
    t.assertCountEqual(yi.search_kv(kind='Pod'), [
        'tests/fixtures/yaml/pod.yaml',
    ])


@pytest.mark.search_kv
def test_search_kv_3():
    t.assertCountEqual(yi.search_kv(apiVersion='v1'), [
        'tests/fixtures/yaml/pod.yaml',
        'tests/fixtures/yaml/service-nginx.yaml',
        'tests/fixtures/yaml/service-haproxy.yaml',
    ])


@pytest.mark.search_kv
def test_search_kv_4():
    t.assertCountEqual(yi.search_kv(apiVersion='v1', kind='Pod'), [
        'tests/fixtures/yaml/pod.yaml',
    ])


@pytest.mark.search_kv
def test_search_kv_5():
    t.assertCountEqual(yi.search_kv(kind='Deployment', apiVersion='apps/v1'), [
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.search
def test_search_1():
    t.assertCountEqual(yi.search({'kind': 'Deployment'}), [
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.search
def test_search_2():
    t.assertCountEqual(yi.search({'kind': 'Pod'}), [
        'tests/fixtures/yaml/pod.yaml',
    ])


@pytest.mark.search
def test_search_3():
    t.assertCountEqual(yi.search({'apiVersion': 'v1'}), [
        'tests/fixtures/yaml/pod.yaml',
        'tests/fixtures/yaml/service-nginx.yaml',
        'tests/fixtures/yaml/service-haproxy.yaml',
    ])


@pytest.mark.search
def test_search_4():
    t.assertCountEqual(yi.search({'apiVersion': 'v1', 'kind': 'Pod'}), [
        'tests/fixtures/yaml/pod.yaml',
    ])


@pytest.mark.search
def test_search_5():
    t.assertCountEqual(yi.search({'kind': 'Deployment', 'apiVersion': 'apps/v1'}), [
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.search_one_of
def test_search_one_of_1():
    t.assertCountEqual(yi.search_one_of([
        {'kind': 'Deployment'},
    ]), [
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.search_one_of
def test_search_one_of_2():
    t.assertCountEqual(yi.search_one_of([
        {'kind': 'Pod'},
    ]), [
        'tests/fixtures/yaml/pod.yaml',
    ])


@pytest.mark.search_one_of
def test_search_one_of_3():
    t.assertCountEqual(yi.search_one_of([
        {'apiVersion': 'v1'},
    ]), [
        'tests/fixtures/yaml/pod.yaml',
        'tests/fixtures/yaml/service-nginx.yaml',
        'tests/fixtures/yaml/service-haproxy.yaml',
    ])


@pytest.mark.search_one_of
def test_search_one_of_4():
    t.assertCountEqual(yi.search_one_of([
        {'kind': 'Deployment'},
        {'kind': 'Pod'},
    ]), [
        'tests/fixtures/yaml/pod.yaml',
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.search_one_of
def test_search_one_of_5():
    t.assertCountEqual(yi.search_one_of([
        {'kind': 'Deployment', 'apiVersion': 'v1'},
    ]), [])


@pytest.mark.search_one_of
def test_search_one_of_6():
    t.assertCountEqual(yi.search_one_of([
        {'kind': 'Deployment'},
        {'apiVersion': 'apps/v1'},
    ]), [
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.search_one_of
def test_search_one_of_7():
    t.assertCountEqual(yi.search_one_of([
        {'kind': 'Deployment'},
        {'apiVersion': 'apps/v1'},
    ]), [
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.search_one_of
def test_search_one_of_8():
    t.assertCountEqual(yi.search_one_of([
        {'kind': 'Deployment', 'apiVersion': 'apps/v1'},
        {'kind': 'Pod'},
    ]), [
        'tests/fixtures/yaml/deployment.yaml',
        'tests/fixtures/yaml/pod.yaml',
    ])


@pytest.mark.search_dpath
def test_search_dpath_1():
    t.assertCountEqual(yi.search_dpath('/spec/template/spec/containers/*/image/nginx'), [
        'tests/fixtures/yaml/deployment.yaml',
    ])


@pytest.mark.search_dpath
def test_search_dpath_2():
    t.assertCountEqual(yi.search_dpath('/spec/ports/*/port/80'), [
        'tests/fixtures/yaml/service-nginx.yaml',
    ])


@pytest.mark.search_dpath
def test_search_dpath_3():
    t.assertCountEqual(yi.search_dpath('**/port/80'), [
        'tests/fixtures/yaml/service-nginx.yaml',
    ])


@pytest.mark.search_dpath
def test_search_dpath_4():
    t.assertCountEqual(yi.search_dpath('/metadata/name/nginx'), [
        'tests/fixtures/yaml/service-nginx.yaml',
        'tests/fixtures/yaml/deployment.yaml',
        'tests/fixtures/yaml/pod.yaml',
    ])


@pytest.mark.search_dpath
def test_search_dpath_5():
    t.assertCountEqual(yi.search_dpath('/spec/ports'), [
        'tests/fixtures/yaml/service-nginx.yaml',
        'tests/fixtures/yaml/service-haproxy.yaml',
    ])


@pytest.mark.search_dpath
def test_search_dpath_6():
    t.assertCountEqual(yi.search_dpath('**/nginx'), [
        'tests/fixtures/yaml/service-nginx.yaml',
        'tests/fixtures/yaml/deployment.yaml',
        'tests/fixtures/yaml/pod.yaml',
    ])
