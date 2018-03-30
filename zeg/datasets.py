# Copyright 2018 Zegami Ltd

"""Collection commands."""
import os
import sys

import yaml
from colorama import Fore, Style

from . import (
    http,
)


MIMES = {
    ".tab": "text/tab-separated-values",
    ".tsv": "text/tab-separated-values",
    ".csv": "text/csv",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

def get(log, session, args):
    """Get a data set."""
    url = "{}datasets/{}".format(
        http.get_api_url(args.url, args.project),
        args.id)
    log.debug('GET: {}'.format(url))
    response_json = http.get(log, session, url)
    log.print_json(response_json, "dataset", "get")


def update(log, session, args):
    """Update a data set."""
    url = "{}datasets/{}/file/".format(
        http.get_api_url(args.url, args.project),
        args.id)
    log.debug('POST: {}'.format(url))

    # check for config
    if 'config' not in args:
        log.error('Configuration file path missing')
        sys.exit(1)

    # parse yaml collection configuration
    with open(args.config, 'r') as stream:
        try:
            yargs = yaml.load(stream)
        except yaml.YAMLError as exc:
            log.error(str(exc))

    file_path = yargs['file_config']['path']
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_path)[-1]
    file_mime = MIMES.get(file_ext, MIMES['.csv'])

    log.debug("File name: {}".format(file_name))
    log.debug("File mime: {}".format(file_mime))

    with open(file_path) as f:
        response_json = http.post_file(
            log,
            session,
            url,
            file_name,
            f,
            file_mime)
        log.print_json(response_json, "dataset", "update")


def delete(log, args):
    """Delete an data set."""
    log('dataset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('delete dataset command coming soon.')
