# -*- coding: utf-8 -*-

import os
import json
import dpath.util
from glob import iglob
from typing import Any, Optional, List, Dict, Set
try:
    import ryaml
    HAS_RYAML = True
except ImportError:
    import yaml
    HAS_RYAML = False

import yamlindexer.cache as yicache
import yamlindexer.utils as yiutils


class YAMLIndex():

    root_path = os.getcwd()
    globs = ['**/*.yml', '**/*.yaml']
    encoding = 'utf-8'
    index = dict()  # type: Any
    cache = None

    def __init__(self, root_path: str = None, globs: list = None, cache: Optional[bool] = None,
                 cache_ttl: Optional[int] = None, encoding: Optional[str] = None):
        if root_path is not None:
            self.root_path = root_path
        if globs is not None:
            self.globs = globs
        if encoding is not None:
            self.encoding = encoding
        if cache is not None:
            self.cache = yicache.YAMLIndexCache(self, cache_ttl=cache_ttl)

        self.scan()

    def to_dict(self) -> dict:
        return self.__dict__

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.index, **kwargs)

    def __str__(self) -> str:
        return self.to_json(indent=4)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(root_path="{self.root_path}", globs={self.globs}, cache="{self.cache}")'

    def scan(self):
        if self.cache is None:
            self.index = self._index_files()
        # read from cache or scan and refresh cache
        else:
            try:
                self.cache.load()
            except (FileNotFoundError, yicache.YAMLIndexCacheExpired):
                self.index = self._index_files()
                self.cache.save()

    def search(self, filter: dict) -> list:
        # TODO: make sure to replace separator if filter_leaf_paths contain /
        res = list()  # type: List[Set]
        for f, sep in yiutils.leaf_paths(filter):
            res.append(set(self.search_dpath(f, separator=sep)))

        return list(set.intersection(*res))

    def search_one_of(self, filters: List[dict], separator: Optional[str] = '/') -> list:
        res = set()  # type: Set[str]
        for f in filters:
            res = res.union(set(self.search(f)))
        return list(res)

    def search_kv(self, **filters: str) -> list:
        # TODO: rewrite to avoid loops
        res = set()  # type: Set[str]
        for k, v in filters.items():
            res = res.union(set(self.index.get(k, {}).get(v, [])))

        for k, v in filters.items():
            res = res & set(set(self.index.get(k, {}).get(v, [])))

        return list(res)

    def search_dpath(self, query, **kwargs) -> list:
        res = set()  # type: Set[str]
        dpath.options.ALLOW_EMPTY_STRING_KEYS = True
        search = dpath.util.values(self.index, query, **kwargs)
        for r in search:
            res = res.union(set([x for _, x in dpath.segments.leaves(r)]))
        return list(res)

    def _index_files(self) -> dict:
        files = list()  # type: List[str]
        for g in self.globs:
            files.extend(iglob(os.path.join(self.root_path, g), recursive=True))
        index = dict()  # type: Dict[str, Dict[str, List[str]]]
        for p in files:
            with open(p, 'r', encoding=self.encoding) as f:
                if HAS_RYAML:
                    yamlf = ryaml.load(f)
                else:
                    try:
                        yamlf = yaml.load(f, Loader=yaml.CSafeLoader)
                    except AttributeError:
                        yamlf = yaml.load(f, Loader=yaml.SafeLoader)
                index = self._push_to_index(yamlf, p, index)

        return index

    def _push_to_index(self, data: dict, path: str, index=dict()) -> dict:
        # TODO: add tests
        for k, v in data.items():
            if isinstance(v, list):
                index.setdefault(k, {})
                index[k] = self._push_to_index({str(i): v[i] for i in range(len(v))}, path, index[k])
            elif isinstance(v, dict):
                index.setdefault(k, {})
                index[k] = self._push_to_index(v, path, index[k])
            else:
                index.setdefault(k, {}).setdefault(v, [])
                index[k][v] += [path]
        return index
