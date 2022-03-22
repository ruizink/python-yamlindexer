# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='YamlIndexer',
    version='0.1.0',
    description='Python package to index YAML files for quicker searches',
    long_description=readme,
    author='Mario Santos',
    author_email='mario.rf.santos@gmail.com',
    url='https://github.com/ruizink/yamlindexer',
    license=license,
    packages=find_packages()
)
