# Copyright 2018 Zegami Ltd

"""A command line interface for managing Zegami."""

from os import path

from setuptools import setup


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zegami-cli',
    version='0.1.0',
    description='Command Line Interface for Zegami',
    long_description=long_description,
    url='https://github.com/zegami/zegami-cli',
    author='Zegami',
    author_email='help@zegami.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=['zeg'],
    install_requires=[
        'colorama==0.3.9',
        'PyYaml==3.12',
        'requests<3.0,>=2.15.0',
    ],
    entry_points={
        'console_scripts': [
            'zeg=zeg.__main__:main'
        ]
    },
    project_urls={
        'Zegami': 'https://zegami.com',
        'Bug Reports': 'https://github.com/zegami/zegami-cli/issues',
    },
)
