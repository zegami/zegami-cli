# Copyright 2018 Zegami Ltd

"""Collection commands."""
from .log import getLogger


def get(args):
    """Get an image set."""
    log = getLogger(name='cli', verbose=args.verbose)
    log.info('imageset id: {}'.format(args.id))
    log.warn('Get imageset command coming soon.')


def update(args):
    """Update an image set."""
    log = getLogger(name='cli', verbose=args.verbose)
    log.info('imageset id: {}'.format(args.id))
    log.warn('Update imageset command coming soon.')


def delete(args):
    """Delete an image set."""
    log = getLogger(name='cli', verbose=args.verbose)
    log.info('imageset id: {}'.format(args.id))
    log.warn('delete imageset command coming soon.')
