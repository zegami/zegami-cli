# Copyright 2018 Zegami Ltd

"""Collection commands."""
from .log import getLogger


def getAll(args):
    """Get all collections."""
    log = getLogger(name='cli')
    log.warn('Get all collections command coming soon.')


def update(args):
    """Update a collection."""
    log = getLogger(name='cli', verbose=args.verbose)
    log.info('collection id: {}'.format(args.id))
    log.warn('Update collection command coming soon.')


def delete(args):
    """Delete a collection."""
    log = getLogger(name='cli', verbose=args.verbose)
    log.info('collection id: {}'.format(args.id))
    log.warn('delete collection command coming soon.')
