from setuptools import setup

# Package meta-data.
NAME = 'wiki-graph'
DESCRIPTION = 'Graph the connections formed by a single wikipedia page'
URL = 'https://github.com/mvwicky/wiki-graph'
EMAIL = 'mvanwickle@gmail.com'
AUTHOR = 'Michael Van Wickle'

# What packages are required for this module to be executed?
REQUIRED = [
    'attrs',
    'bs4',
    'profilehooks',
    'requests',
    'sqlalchemy',
    'sqlalchemy-utils'
]

setup(
    name=NAME,
    version='0.0.1',
    packages=['wiki-graph'],
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
