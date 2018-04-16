# Copyright 2018 Zegami Ltd

"""Auth commands."""
import sys

from colorama import Fore, Style

from . import (
    config,
    http,
)


def login(log, session, args):
    """Authenticate and retrieve a long lived token."""
    log.warn('Login command coming soon.')
