
class FixtureIndex():
    globs = ['tests/fixtures/yaml/service.yaml']

    expected_at_level = {
        1: {
            'apiVersion': {
                'v1': globs,
            },
            'kind': {
                'Service': globs,
            },
            'metadata': {},
            'spec': {},
        },
        2: {
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
                'labels': {},
            },
            'spec': {
                'clusterIP': {
                    'None': globs,
                },
                'ports': {},
                'selector': {},
            },
        },
        10: {
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
        },
    }
