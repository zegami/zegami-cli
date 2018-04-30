# Copyright 2018 Zegami Ltd

"""Collection commands."""
import os

from jsonschema import validate
import yaml


def parse_config(path):
    """Parse yaml collection configuration."""
    configuration = load_config(path)
    validate_config(configuration)
    return configuration


def load_config(path):
    """Load yaml collection configuration."""
    with open(path, 'r') as stream:
        return yaml.load(stream)
    return None


def validate_config(configuration):
    schema_path = os.path.join(
        os.path.dirname(__file__),
        'schemata',
        'spec.yaml'
    )
    with open(schema_path, 'r') as stream:
        schema = yaml.load(stream)

    validate(configuration, schema)
