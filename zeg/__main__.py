#!/usr/bin/env python3
#
# Copyright 2018 Zegami Ltd

"""A command line interface for managing Zegami."""
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from textwrap import dedent

import pkg_resources

from . import (
    collections,
    datasets,
    http,
    imagesets,
    log,
)


def main():
    """Zegami command line interface."""
    version = pkg_resources.require('zegami-cli')[0].version
    description = dedent(r'''
         ____                      _
        /_  / ___ ___ ____ ___ _  (_)
         / /_/ -_) _ `/ _ `/  ' \/ /
        /___/\__/\_, /\_,_/_/_/_/_/
                /___/  v{}

        Visual data exploration.

    A command line interface for managing Zegami.
    '''.format(version))

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=description,
    )

    # top level arguments
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(version),
    )

    option_mapper = {
        'get': {
            'help': 'Get a resource',
            'resources': {
                'collections': collections.get,
                'dataset': datasets.get,
                'imageset': imagesets.get,
            }
        },
        'update': {
            'help': 'Update a resource',
            'resources': {
                'collections': collections.update,
                'dataset': datasets.update,
                'imageset': imagesets.update,
            }
        },
        'delete': {
            'help': 'Delete a resource',
            'resources': {
                'collections': collections.delete,
                'dataset': datasets.delete,
                'imageset': imagesets.delete,
            }
        },
    }

    subparsers = parser.add_subparsers()
    for action in option_mapper:
        action_parser = subparsers.add_parser(
            action,
            help=option_mapper[action]['help'],
        )
        # set the action type so we can work out what was chosen
        action_parser.set_defaults(action=action)
        action_parser.add_argument(
            'resource',
            choices=['collections', 'dataset', 'imageset'],
            help='The name of the resource type.'
        )
        action_parser.add_argument(
            'id',
            default=None,
            nargs="?",
            help='Resource identifier.',
        )
        action_parser.add_argument(
            '-c',
            '--config',
            help='Path to command configuration yaml.',
        )
        action_parser.add_argument(
            '-p',
            '--project',
            help='The id of the project.',
        )
        action_parser.add_argument(
            '-t',
            '--token',
            default=None,
            help='Authentication token.',
        )
        action_parser.add_argument(
            '-u',
            '--url',
            default='https://app.zegami.com',
            help='Zegami server address.',
        )
        action_parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='Enable verbose logging.',
        )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    logger = log.Logger(args.verbose)
    session = http.make_session(args.url, args.token)

    try:
        option_mapper[args.action]['resources'][args.resource](
            logger,
            session,
            args,
        )
    except Exception as e:
        # unhandled exceptions
        logger.error('Unhandled exception: {}'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
