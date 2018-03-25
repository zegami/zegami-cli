# Copyright 2018 Zegami Ltd

"""A command line interface for managing Zegami."""

from setuptools import setup
setup(
    name='zegami-cli',
    version='0.1.0',
    packages=['zegcli'],
    install_requires=[
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'zegcli=zegcli.__main__:main'
        ]
    }
)
