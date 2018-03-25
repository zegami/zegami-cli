# Copyright 2018 Zegami Ltd

"""
Log helpers.

Based on https://gist.github.com/jonaprieto/a61d9cade3ba19487f98
"""

from logging import (
    DEBUG,
    Formatter,
    StreamHandler,
    WARN,
    getLogger as realGetLogger
)

from colorama import Back, Fore, Style, init


class ColourStreamHandler(StreamHandler):
    """A colorized output SteamHandler."""

    # Some basic colour scheme defaults
    colours = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.WHITE,
        'WARN': Fore.YELLOW,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRIT': Back.RED + Fore.WHITE,
        'CRITICAL': Back.RED + Fore.WHITE
    }

    def emit(self, record):
        """Overridden emit."""
        try:
            message = self.format(record)
            self.stream.write(
                self.colours[record.levelname] + message + Style.RESET_ALL
            )
            self.stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


def getLogger(name=None, fmt='%(message)s', verbose=False):
    """
    Get and initialize a colourised logging instance if the system supports.

    it as defined by the log.has_colour
    :param name: Name of the logger
    :type name: str
    :param fmt: Message format to use
    :type fmt: str
    :return: Logger instance
    :rtype: Logger
    """
    init()
    level = WARN if not verbose else DEBUG
    log = realGetLogger(name)
    # Only enable colour if support was loaded properly
    handler = ColourStreamHandler()
    handler.setLevel(level)
    handler.setFormatter(Formatter(fmt))
    log.addHandler(handler)
    log.setLevel(level)
    log.propagate = 0  # Don't bubble up to the root logger
    return log
