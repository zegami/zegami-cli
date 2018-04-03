# Copyright 2018 Zegami Ltd

"""Collection commands."""
import os
import sys

from colorama import Fore, Style

import yaml

from . import (
    http,
)


MIMES = {
    ".tab": "text/tab-separated-values",
    ".tsv": "text/tab-separated-values",
    ".csv": "text/csv",
    ".xlsx": "application/vnd.openxmlformats-officedocument" +
             ".spreadsheetml.sheet",
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
        yargs = yaml.load(stream)

    # get file path
    file_config = yargs['file_config']
    if file_config is None:
        log.error(
            "Missing {highlight}path{reset} or "
            "{highlight}directory{reset} parameter".format(
                highlight=Fore.YELLOW,
                reset=Style.RESET_ALL,
            )
        )
        sys.exit(1)

    if 'path' in file_config:
        file_path = file_config['path']
    elif 'directory' in file_config:
        file_path = _get_most_recent_file(file_config['directory'])

    if file_path is None:
        log.error('Data file not found')
        sys.exit(1)

    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_path)[-1]
    file_mime = MIMES.get(file_ext, MIMES['.csv'])

    log.debug("File path: {}".format(file_path))
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


def _newest_ctime(entry):
    return -entry.stat().st_ctime, entry.name


def _get_most_recent_file(path):
    """Get the most recent file in a directory."""
    allowed_ext = tuple(MIMES.keys())
    files_iter = (
        entry for entry in os.scandir(path)
        if entry.is_file() and entry.name.lower().endswith(allowed_ext)
    )
    for entry in sorted(files_iter, key=_newest_ctime):
        return entry.path
    return None
