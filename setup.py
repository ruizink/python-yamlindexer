# -*- coding: utf-8 -*-

from distutils.core import setup
import yamlindexer.version
import os


long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.rst'
    )
).read()

if __name__ == "__main__":

    setup(
        name='YamlIndexer',
        version=yamlindexer.version.VERSION,
        description='Python package to index YAML files for quicker searches',
        long_description=long_description,
        author='Mario Santos',
        author_email='mario.rf.santos@gmail.com',
        url='https://github.com/ruizink/python-yamlindexer',
        license="MIT",
        packages=["yamlindexer"],
        install_requires=[
            "PyYAML",
            "dpath"
        ],
        scripts=[],
        data_files=[],
        python_requires=">=3",
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
