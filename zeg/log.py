# Copyright 2018 Zegami Ltd

"""Log to the console."""

import copy

from colorama import Fore, Style, init
import yaml


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

    def print_json(self, datadict, typename, verb, shorten=True):
        """Print a JSON file in YAML format."""
        output = copy.deepcopy(datadict)
        dictdata = self._shorten_arrays(output) if shorten else output
        print("=========================================")
        print("{} {} with result:".format(verb, typename))
        print("-----------------------------------------")
        print(yaml.dump(dictdata, default_flow_style=False))
        print("=========================================", flush=True)

    def _shorten_arrays(self, dictdata):
        for key, value in dictdata.items():
            if isinstance(value, list):
                if len(value) > 3:
                    restlable = [
                        "...",
                        "and {} more...".format(len(value) - 2),
                    ]
                    dictdata[key] = value[:2] + restlable + value[-1:]
            if isinstance(value, dict):
                dictdata[key] = self._shorten_arrays(value)
        return dictdata
