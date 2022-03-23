# -*- coding: utf-8 -*-

class IndexTestsData:
    globs = ['tests/fixtures/yaml/service-nginx.yaml']

    expected_index = {
        'apiVersion': {
            'v1': globs,
        },
        'kind': {
            'Service': globs,
        },
        'metadata': {
            'name': {
                'nginx': globs,
            },
            'labels': {
                'app': {
                    'nginx': globs,
                },
            },
        },
        'spec': {
            'clusterIP': {
                'None': globs,
            },
            'ports': {
                '0': {
                    'port': {
                        80: globs,
                    },
                    'name': {
                        'web': globs,
                    },
                },
            },
            'selector': {
                'app': {
                    'nginx': globs,
                },
            },
        },
    }
