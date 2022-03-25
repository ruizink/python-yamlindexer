# YAMLIndexer Module Repository

[![example workflow](https://github.com/ruizink/python-yamlindexer/actions/workflows/tests.yaml/badge.svg)](https://github.com/ruizink/python-yamlindexer/actions/workflows/tests.yaml)

Python package to index YAML files for quicker searches

## Installing

You can install this package using pip.

```bash
pip install yamlindexer
```

## Using YAMLIndexer

```python
from yamlindexer.core import YAMLIndex
```

### Indexing files

When you create an instance of YAMLIndex, the indexing process begins straight away.

By default, it searches for `*.yaml` and `*.yml` files in the current working directory.

```python
# this will index all files .yaml and .yaml files in the current working directory
index = YAMLIndex()
```

You can override the indexed directory by passing the `root_path` parameter to the constructor. The same with the filenames, using the `globs` parameter.

```python
# this will index all files .yaml files that start with nginx_, located in /some/other/folder 
index = YAMLIndex(root_path='/some/other/folder', globs=['**/nginx_*.yaml'])
```

### Searching the index

There are 4 ways to search the index:

#### `search_kv`

If you are searching the root level of the YAML files, you can simply use the `search_kv` method:

```python
# this will return a list of files that have both apiVersion='v1' and kind='Pod'
index.search_kv(apiVersion='v1', kind='Pod')
```

#### `search`

Another way is to use `search` and pass it a dict with the criteria:

```python
# this will return a list of files that have both apiVersion='v1' and kind='Pod' (just like the command above)
index.search({'apiVersion': 'v1', 'kind': 'Pod'})
```

#### `search_one_of`

You can also perform a combined search with `search_one_of` method, passing it a list of dicts with the criteria:

```python
# this will return a list of files that have apiVersion='v1' or kind='Pod'
index.search_one_of([
    {'kind': 'Deployment'},
    {'kind': 'Pod'},
])
```

#### `search_dpath`

Lastly, there's also a handier way that allows you to do 'glob' type searches, leveraging the awesome [dpath](https://pypi.org/project/dpath/) project:

```python
# this will return a list of files that a 'port: 80' somewhere in their leaves
index.search_dpath('**/port/80')
```

### Cache

Currently, there's support for a very basic type of cache, that avoids having to re-index the files every time a new `YAMLIndex` is created. This is achieved by saving the index to filesystem. This feature can be used using the `cache` and `cache_ttl` parameters when creating a new instance:

```python
# this will index all files .yaml and .yaml files in the current working directory
# and save the index in filesystem for 60 seconds
index = YAMLIndex(cache=True, cache_ttl=60)
```

### YAML Parser

`YAMLIndexer` requires a YAML parser. By default, it tries to use `ryaml` since it speeds up things quite a bit.
But since `ryaml` might not be available for all platforms, by default it pulls `PyYAML` as a dependency.
If no `ryaml` is available in the system, it tries to use `PyYAML`'s much faster `yaml.CSafeLoader` (if available) and defaults to `yaml.SafeLoader` otherwise.

## Author

Mário Santos

@\_RuiZinK\_
