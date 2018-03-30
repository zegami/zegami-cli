# Copyright 2018 Zegami Ltd

"""Collection commands."""
from colorama import Fore, Style


def get(log, args):
    """Get an image set."""
    log('imageset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('Get imageset command coming soon.')


def update(log, args):
    """Update an image set."""
    log('imageset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('Update imageset command coming soon.')


def delete(log, args):
    """Delete an image set."""
    log('imageset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('delete imageset command coming soon.')
