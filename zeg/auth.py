# Copyright 2018 Zegami Ltd

"""Auth commands."""
import os

from appdirs import user_data_dir

from colorama import Fore, Style

import pkg_resources

from . import (
    config,
    http,
)


def login(log, session, args):
    """Authenticate and retrieve a long lived token."""
    log.warn('Login command coming soon.')
    user_path = _init_conf_location()
    user_data = os.path.join(user_path, '.auth')

    with open(user_data, 'w') as auth:
        auth.write('hello world')


def _init_conf_location():
    """Setup the config file location."""
    app_name = pkg_resources.require('zegami-cli')[0].project_name
    user_data = user_data_dir(app_name, 'zegami')
    
    if not os.path.exists(user_data):
        os.makedirs(user_data)
    return user_data
