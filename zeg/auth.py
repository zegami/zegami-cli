# Copyright 2018 Zegami Ltd

"""Auth commands."""
import os

from appdirs import user_data_dir

from colorama import Fore, Style

from getpass import getpass

import pkg_resources

from . import (
    config,
    http,
)


def login(log, session, args):
    """Authenticate and retrieve a long lived token."""
    # set up user data location
    user_path = _init_conf_location()
    user_data = os.path.join(user_path, '.auth')
    # get users auth details
    username = input('Username: ')
    password = getpass()
    data = {
        'username': username,
        'password': password,
        'noexpire': True
    }
    # time to authenticate
    url = "{}/oauth/token/".format(args.url)
    log.debug('POST: {}'.format(url))
    response = http.post_json(session, url, data)

    with open(user_data, 'w') as auth:
        auth.write(response['token'])
    
    log('User token saved.')


def get_token(args=None):
    """
    Get the users auth token.
    If specified in the args then will use that over local config
    """
    token = args.token if 'token' in args else None
    if token is None:
        # look in user config
        user_data = os.path.join(_get_user_dir(), '.auth')
        if os.path.exists(user_data):
            # see if something is inside
            with open(user_data) as auth:
                token = auth.read()

    return token


def _get_user_dir():
    """Get the users data directory location."""
    app_name = pkg_resources.require('zegami-cli')[0].project_name
    return user_data_dir(app_name, 'zegami')

def _init_conf_location():
    """Setup the config file location."""
    user_data = _get_user_dir()
    
    if not os.path.exists(user_data):
        os.makedirs(user_data)
    return user_data
