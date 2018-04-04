# Copyright 2018 Zegami Ltd

"""Collection commands."""
from colorama import Fore, Style

from . import (
    http,
)


def get(log, session, args):
    """Get a collection."""
    coll_id = args.id if args.id.lower() != "all" else ""
    url = "{}collections/{}".format(
        http.get_api_url(args.url, args.project),
        coll_id)
    log.debug('GET: {}'.format(url))
    response_json = http.get(log, session, url)
    log.print_json(response_json, "collection", "get", shorten=False)


def update(log, args):
    """Update a collection."""
    log('collection id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('Update collection command coming soon.')


def delete(log, session, args):
    """Delete a collection."""
    url = "{}collections/{}".format(
        http.get_api_url(args.url, args.project),
        args.id)
    log.debug('DELETE: {}'.format(url))
    http.delete(log, session, url)
    log('collection {highlight}{id}{reset} deleted',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
