# Copyright 2018 Zegami Ltd

"""Collection commands."""
import sys

from colorama import Fore, Style

from . import (
    config,
    http,
)


def get(log, session, args):
    """Get a collection."""
    coll_id = args.id if args.id is not None else ""
    url = "{}collections/{}".format(
        http.get_api_url(args.url, args.project),
        coll_id)
    log.debug('GET: {}'.format(url))
    response_json = http.get(session, url)
    log.print_json(response_json, "collection", "get", shorten=False)


def update(log, session, args):
    """Update a collection."""
    log('colection id: {highlight}{id}{reset}',
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
    http.delete(session, url)
    log('collection {highlight}{id}{reset} deleted',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)


def publish(log, session, args):
    """Publish a collection."""
    coll_id = args.id if args.id is not None else ""

    # check for config
    if 'config' not in args:
        log.error('Configuration file path missing')
        sys.exit(1)

    configuration = config.parse_config(args.config)

    # get publish details
    publish_config = configuration['publish_config']
    if publish_config is None:
        log.error(
            "Missing {highlight}publish_config{reset} parameter".format(
                highlight=Fore.YELLOW,
                reset=Style.RESET_ALL,
            )
        )
        sys.exit(1)

    url = "{}collections/{}/{}".format(
        http.get_api_url(args.url, args.project),
        coll_id,
        'publish' if publish_config['publish'] is True else 'unpublish'
    )
    log.debug('POST: {}'.format(url))

    publish_options = {
        "project": publish_config['destination_project'],
    }

    response_json = http.post_json(session, url, publish_options)
    log.print_json(response_json, "collection", "update", shorten=False)
