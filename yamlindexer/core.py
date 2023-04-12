# -*- coding: utf-8 -*-

import os
import json
import dpath
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
    index: Dict[Any, Any] = dict()
    cache = None

    def __init__(self, root_path: Optional[str] = None, globs: Optional[list] = None, cache: Optional[bool] = None,
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
        res: List[Set] = list()
        for f, sep in yiutils.leaf_paths(filter):
            res.append(set(self.search_dpath(f, separator=sep)))

        return list(set.intersection(*res))

    def search_one_of(self, filters: List[dict], separator: Optional[str] = '/') -> list:
        res: Set[str] = set()
        for f in filters:
            res = res.union(set(self.search(f)))
        return list(res)

    def search_kv(self, **filters: str) -> list:
        # TODO: rewrite to avoid loops
        res: Set[str] = set()
        for k, v in filters.items():
            res = res.union(set(self.index.get(k, {}).get(v, [])))

        for k, v in filters.items():
            res = res & set(set(self.index.get(k, {}).get(v, [])))

        return list(res)

    def search_dpath(self, query, **kwargs) -> list:
        res: Set[str] = set()
        dpath.options.ALLOW_EMPTY_STRING_KEYS = True
        search = dpath.values(self.index, query, **kwargs)
        for r in search:
            res = res.union(set([x for _, x in dpath.segments.leaves(r)]))
        return list(res)

    def _index_files(self) -> dict:
        files: List[str] = list()
        for g in self.globs:
            files.extend(iglob(os.path.join(self.root_path, g), recursive=True))
        index: Dict[str, Dict[str, List[str]]] = dict()
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
        if type(data) is list:
            data = {k: v for k, v in enumerate(data)}
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
