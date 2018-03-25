# Copyright 2018 Zegami Ltd

"""Collection commands."""
from .log import getLogger


def get(args):
    """Get a data set."""
    log = getLogger(name='cli', verbose=args.verbose)
    log.info('dataset id: {}'.format(args.id))
    log.warn('Get dataset command coming soon.')


def update(args):
    """Update a data set."""
    log = getLogger(name='cli', verbose=args.verbose)
    log.info('dataset id: {}'.format(args.id))
    log.warn('Update dataset command coming soon.')


def delete(args):
    """Delete an data set."""
    log = getLogger(name='cli', verbose=args.verbose)
    log.info('dataset id: {}'.format(args.id))
    log.warn('delete dataset command coming soon.')
