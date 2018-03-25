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
    imagesets,
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

    # common arguments
    collection_id = ArgumentParser(add_help=False)
    collection_id.add_argument(
        'id',
        help='The unique identifier of the collection',
    )

    dataset_id = ArgumentParser(add_help=False)
    dataset_id.add_argument(
        'id',
        help='The unique identifier of the dataset',
    )

    imageset_id = ArgumentParser(add_help=False)
    imageset_id.add_argument(
        'id',
        help='The unique identifier of the imageset',
    )

    token_arg = ArgumentParser(add_help=False)
    token_arg.add_argument(
        '-t',
        '--token',
        help='Authentication token',
    )

    verbose = ArgumentParser(add_help=False)
    verbose.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enable verbose logging',
    )

    subparsers = parser.add_subparsers()
    parser_get = subparsers.add_parser('get', help='Get a resource')
    subparser_get = parser_get.add_subparsers()

    parser_update = subparsers.add_parser('update', help='Update a resource')
    subparser_update = parser_update.add_subparsers()

    parser_delete = subparsers.add_parser('delete', help='Delete a resource')
    subparser_delete = parser_delete.add_subparsers()

    # Collections
    collection_parents = [collection_id, token_arg, verbose]
    get_collections = subparser_get.add_parser(
        'collections',
        parents=[token_arg, verbose],
    )
    get_collections.set_defaults(func=collections.getAll)

    update_collections = subparser_update.add_parser(
        'collections',
        parents=collection_parents,
    )
    update_collections.set_defaults(func=collections.update)

    delete_collections = subparser_delete.add_parser(
        'collections',
        parents=collection_parents,
    )
    delete_collections.set_defaults(func=collections.delete)

    # Datasets
    dataset_parents = [dataset_id, token_arg, verbose]
    get_dataset = subparser_get.add_parser(
        'dataset',
        parents=dataset_parents,
    )
    get_dataset.set_defaults(func=datasets.get)

    update_dataset = subparser_update.add_parser(
        'dataset',
        parents=dataset_parents,
    )
    update_dataset.set_defaults(func=datasets.update)

    delete_dataset = subparser_delete.add_parser(
        'dataset',
        parents=dataset_parents,
    )
    delete_dataset.set_defaults(func=datasets.delete)

    # Imagesets
    imageset_parents = [imageset_id, token_arg, verbose]
    get_imageset = subparser_get.add_parser(
        'imageset',
        parents=imageset_parents,
    )
    get_imageset.set_defaults(func=imagesets.get)

    update_imageset = subparser_update.add_parser(
        'imageset',
        parents=imageset_parents,
    )
    update_imageset.set_defaults(func=imagesets.update)

    delete_imageset = subparser_delete.add_parser(
        'imageset',
        parents=imageset_parents,
    )
    delete_imageset.set_defaults(func=imagesets.delete)

    args = parser.parse_args()

    # call sub command
    if hasattr(args, "func"):
        args.func(args)


if __name__ == '__main__':
    sys.exit(main())
