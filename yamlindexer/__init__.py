# -*- coding: utf-8 -*-

import os
# import re
import time
import json
import yaml
import tempfile
import hashlib
from glob import iglob
from typing import List, Dict, Set, Optional
import dpath.util


# Class DEFAULTS
DEFAULT_ROOT_PATH = os.getcwd()
DEFAULT_GLOBS = ['**/*.yml', '**/*.yaml']
DEFAULT_LEVEL = 1
DEFAULT_ENCODING = 'utf-8'
DEFAULT_USE_CACHE = False
DEFAULT_CACHE_FILENAME_SUFFIX = '.yamlindex.cache'
DEFAULT_CACHE_TTL = 30


class YamlIndexCacheExpired(Exception):
    pass


class YamlIndex():

    def __init__(self, root_path: str = None, globs: list = None, level: Optional[int] = None,
                 cache: Optional[bool] = None, cache_ttl: Optional[int] = None, encoding: Optional[str] = None):
        self.index = dict()  # type: Dict[str, Dict[str, List[str]]]
        self.root_path = root_path if root_path is not None else DEFAULT_ROOT_PATH
        self.globs = globs if globs is not None else DEFAULT_GLOBS
        self.level = level if level is not None else DEFAULT_LEVEL
        self.use_cache = cache if cache is not None else DEFAULT_USE_CACHE
        self.encoding = encoding if encoding is not None else DEFAULT_ENCODING
        if cache is None:
            self.cache_ttl = None
            self.cache_file = None
        else:
            self.cache_ttl = cache_ttl if cache_ttl is not None else DEFAULT_CACHE_TTL
            self.cache_file = self._generate_cache_filename()

        self.scan()

    def to_dict(self) -> dict:
        return self.__dict__

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.index, **kwargs)

    def __str__(self) -> str:
        # TODO: sorting keys fails when dict has keys of mixed int/str types
        # return self.to_json(indent=4, sort_keys=True)
        return self.to_json(indent=4)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(root_path="{self.root_path}", globs={self.globs}, cache_file="{self.cache_file}", cache_ttl={self.cache_ttl})'

    def scan(self):
        if not self.use_cache:
            self.index = self._index_files()
        # read from cache or scan and refresh cache
        else:
            try:
                if ((time.time() - os.path.getmtime(self.cache_file)) > self.cache_ttl):
                    raise YamlIndexCacheExpired
                else:
                    # load index from cache
                    self._load_cache()
            except (FileNotFoundError, YamlIndexCacheExpired):
                self.index = self._index_files()
                self._save_cache()

    def find_one_of(self, filters: List[dict]) -> list:
        res = set()  # type: Set[str]

        for f in filters:
            res = res.union(set(self.find(**f)))

        return list(res)

    def find(self, **filters: str) -> list:
        res = set()  # type: Set[str]
        for k, v in filters.items():
            res = res.union(set(self.index.get(k, {}).get(v, [])))

        for k, v in filters.items():
            res = res & set(set(self.index.get(k, {}).get(v, [])))

        return list(res)

    def search_xpath(self, query: str) -> list:
        result = list()
        for _, r in dpath.util.search(self.index, query, yielded=True):
            if isinstance(r, dict):
                result.append(r)
            else:
                result += r
        return result

    def _generate_cache_filename(self) -> str:
        hash = hashlib.md5(f'{self.root_path}{sorted(set(self.globs))}{self.level}'.encode("utf-8")).hexdigest()
        return os.path.join(tempfile.gettempdir(), f'{hash}{DEFAULT_CACHE_FILENAME_SUFFIX}')

    def _load_cache(self):
        try:
            with open(self.cache_file) as i:
                self.index = json.load(i)
        except json.decoder.JSONDecodeError:
            self._index_files()
        # TODO: handle IO errors when reading
        except Exception:
            pass

    def _save_cache(self):
        try:
            with open(self.cache_file, 'w') as o:
                json.dump(self.index, o)
        # TODO: handle IO errors when writing
        except Exception:
            pass

    def _index_files(self) -> dict:
        files = list()  # type: List[str]
        for g in self.globs:
            files.extend(iglob(os.path.join(self.root_path, g), recursive=True))
        index = dict()  # type: Dict[str, Dict[str, List[str]]]
        for p in files:
            with open(p, 'r', encoding=DEFAULT_ENCODING) as f:
                # if level == 1, use regex as it's much faster
                # if self.level == 1:
                #     for line in f.readlines():
                #         k = self._extract_key(line.rstrip())
                #         v = self._extract_value(line.rstrip())
                #         if k is not None and v is not None:
                #             index.setdefault(k, {}).setdefault(v, [])
                #             index[k][v] += [p]
                # # we need to yaml load each of the files
                # else:
                #     try:
                #         yamlf = yaml.load(f, Loader=yaml.CSafeLoader)
                #     except AttributeError:
                #         # CSafeLoader only exists if you build yaml with LibYAML
                #         yamlf = yaml.load(f, Loader=yaml.SafeLoader)
                #     index = self._push_to_index(yamlf, p, self.level, index)
                try:
                    yamlf = yaml.load(f, Loader=yaml.CSafeLoader)
                except AttributeError:
                    # CSafeLoader only exists if you build yaml with LibYAML
                    yamlf = yaml.load(f, Loader=yaml.SafeLoader)
                index = self._push_to_index(yamlf, p, self.level, index)
        return index

    def _push_to_index(self, data: dict, path: str, level: int, index=dict()) -> dict:
        if level > 0:
            for k, v in data.items():
                if isinstance(v, list):
                    index.setdefault(k, {})
                    index[k] = self._push_to_index({str(i): v[i] for i in range(len(v))}, path, level - 1, index[k])
                elif isinstance(v, dict):
                    index.setdefault(k, {})
                    index[k] = self._push_to_index(v, path, level - 1, index[k])
                else:
                    index.setdefault(k, {}).setdefault(v, [])
                    index[k][v] += [path]
        return index

    # @staticmethod
    # def _extract_key(yaml_line) -> Optional[str]:
    #     # extract non-quoted key:
    #     m = re.search(r'^(?!<<:)(?=[^\'\"#\s].*[^\'\"]:)\s*([^\s]?.*[^\s])\s*:\s', yaml_line)
    #     if m and m.group(1):
    #         return m.group(1)

    #     # extract double quoted key:
    #     m = re.search(r'^(?=\".*\":)\"(.*)\":\s', yaml_line)
    #     if m and m.group(1):
    #         return m.group(1)

    #     # extract single quoted key:
    #     m = re.search(r'^(?=\'.*\':)\'(.*)\':\s', yaml_line)
    #     if m and m.group(1):
    #         return m.group(1)

    #     return None

    # @staticmethod
    # def _extract_value(yaml_line) -> Optional[str]:
    #     # extract non-quoted value:
    #     m = re.search(r'^[^\s#]*(?!:\s+[\"\'[{|&>]\w*[\"\']?):\s*([^\s]?.*[^\s])\s*$', yaml_line)
    #     if m and m.group(1):
    #         return m.group(1)

    #     # extract double quoted value:
    #     m = re.search(r'(?=:\s+\".*\"):\s+\"(.*)\"\s*$', yaml_line)
    #     if m and m.group(1):
    #         return m.group(1)

    #     # exctact single quoted value:
    #     m = re.search(r'(?=:\s+\'.*\'):\s+\'(.*)\'\s*$', yaml_line)
    #     if m and m.group(1):
    #         return m.group(1)

    #     return None
