# Copyright 2018 Zegami Ltd

"""Collection commands."""
from colorama import Fore, Style


def get(log, args):
    """Get a data set."""
    log('dataset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('Get dataset command coming soon.')


def update(log, args):
    """Update a data set."""
    log('dataset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('Update dataset command coming soon.')


def delete(log, args):
    """Delete an data set."""
    log('dataset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('delete dataset command coming soon.')
