# -*- coding: utf-8 -*-

def _leaf_paths_tuples(obj, cur=()):
    # TODO: add tests
    if isinstance(obj, dict):
        for k, v in obj.items():
            for path in _leaf_paths_tuples(v, cur + (k,)):
                yield path
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            for path in _leaf_paths_tuples(v, cur + (str(i),)):
                yield path
    else:
        yield cur + (obj,)


def leaf_paths(obj, sep='/'):
    # TODO: add tests
    path_sep_tupples = set()
    for t in _leaf_paths_tuples(obj):
        sep = _find_compatible_separator(''.join(t))
        if sep is not None:
            path = f'{sep}'.join(t)
            path_sep_tupples.add((f'{sep}{path}', sep))
        else:
            raise Exception('Could not find a compatible separator!')
    return path_sep_tupples


def _find_compatible_separator(string):
    # TODO: add tests
    for s in '/~:;,|+-':
        if s not in string:
            return s
    return None
