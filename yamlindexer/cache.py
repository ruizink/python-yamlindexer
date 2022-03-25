# -*- coding: utf-8 -*-

import hashlib
import tempfile
import os
import json
import time
from typing import Optional, Any


class YAMLIndexCacheExpired(Exception):
    pass


class YAMLIndexCache():

    cache_filename_suffix = '.yamlindex.cache'
    cache_ttl = 30

    def __init__(self, yamlindex: Any, cache_file: Optional[str] = None, cache_ttl: Optional[int] = None):
        self.yamlindex = yamlindex
        self.cache_file = cache_file if cache_file is not None else self._generate_unique_filename()
        if cache_ttl is not None:
            self.cache_ttl = cache_ttl

    def load(self):
        if ((time.time() - os.path.getmtime(self.cache_file)) > self.cache_ttl):
            raise YAMLIndexCacheExpired(f'The cache file is older than TTL: "{self.cache_file}s" > "{self.cache_ttl}s" ({self.cache_file})')
        try:
            with open(self.cache_file) as i:
                self.yamlindex.index = json.load(i)
        # TODO: handle IO errors decoding
        except json.decoder.JSONDecodeError:
            pass
        # TODO: handle IO errors when reading
        except Exception:
            pass

    def save(self):
        try:
            with open(self.cache_file, 'w') as o:
                json.dump(self.yamlindex.index, o)
        # TODO: handle IO errors encoding
        # TODO: handle IO errors when writing
        except Exception:
            pass

    def _generate_unique_filename(self):
        hash = hashlib.md5(f'{self.yamlindex.root_path}{sorted(set(self.yamlindex.globs))}'.encode("utf-8")).hexdigest()
        return os.path.join(tempfile.gettempdir(), f'{hash}{self.cache_filename_suffix}')
