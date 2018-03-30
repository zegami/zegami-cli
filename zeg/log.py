# Copyright 2018 Zegami Ltd

"""Log to the console."""

from colorama import Fore, Style, init


class Logger(object):
    """Simplistic output to a stream with verbosity support."""

    def __init__(self, verbose=False):
        """Initialise logger."""
        init()
        self.verbose = verbose

    def __call__(self, format_string, **kwargs):
        """Log message to stderr."""
        print(format_string.format(**kwargs))

    def debug(self, format_string, **kwargs):
        """Log debug message. Only displays if verbose logging turned on."""
        if self.verbose:
            self.__call__(
                Fore.CYAN + format_string + Style.RESET_ALL,
                **kwargs)

    def warn(self, format_string, **kwargs):
        """Log a warning message."""
        self.__call__(
            Fore.YELLOW + format_string + Style.RESET_ALL,
            **kwargs)

    def error(self, format_string, **kwargs):
        """Log an error message."""
        self.__call__(
            Fore.RED + format_string + Style.RESET_ALL,
            **kwargs)
