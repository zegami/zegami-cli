# Copyright 2018 Zegami Ltd

"""Collection commands."""
from colorama import Fore, Style


def get(log, args):
    """Get a collection."""
    log('collection id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('Get all collections command coming soon.')


def update(log, args):
    """Update a collection."""
    log('collection id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('Update collection command coming soon.')


def delete(log, args):
    """Delete a collection."""
    log('collection id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('delete collection command coming soon.')
