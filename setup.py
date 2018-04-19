from setuptools import setup

# Package meta-data.
NAME = 'wiki-graph'
DESCRIPTION = 'Graph the connections formed by a single wikipedia page'
URL = 'https://github.com/mvwicky/wiki-graph'
EMAIL = 'mvanwickle@gmail.com'
AUTHOR = 'Michael Van Wickle'
VERSION = '0.1.2'

# What packages are required for this module to be executed?
REQUIRED = [
    'attrs',
    'bs4',
    'click',
    'profilehooks',
    'requests',
    'requests_html',
    'sqlalchemy',
    'sqlalchemy-utils'
]
PYTHON_REQUIRES = '>=3.6.0'


setup(
    name=NAME,
    version=VERSION,
    install_requires=REQUIRED,
    include_package_data=True,
    python_requires=PYTHON_REQUIRES,
    py_modules=['wiki_graph'],
    entry_points={
        'console_scripts': ['wikigraph=wiki_graph:cli']
    },
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
