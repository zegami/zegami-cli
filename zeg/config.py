# Copyright 2018 Zegami Ltd

"""Collection commands."""
import yaml


def parse_config(path):
    """Parse yaml collection configuration."""
    with open(path, 'r') as stream:
        return yaml.load(stream)
    return None
