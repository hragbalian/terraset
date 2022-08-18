#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

__version__ = '0.1.16'

setup(
    author="Hrag Balian",
    author_email='hrag.balian@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Client to manage superset charts and dashboards through code",
    entry_points={
        'console_scripts': [
            'terraset=terraset.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='terraset',
    name='terraset',
    packages=find_packages(include=['terraset', 'terraset.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hragbalian/terraset',
    version=__version__,
    zip_safe=False,
)
