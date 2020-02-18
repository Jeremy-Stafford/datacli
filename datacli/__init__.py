"""A library for building simple CLIs from dataclasses.

DataCLI is based on argparse.
"""

from argparse import ArgumentParser
from contextlib import suppress
from dataclasses import MISSING, fields


def get_names(field):
    """Return the CLI for a field."""
    with suppress(KeyError):
        yield field.metadata["short_name"]

    try:
        yield field.metadata["long_name"]
    except KeyError:
        yield "--" + field.name.replace("_", "-")


def make_parser(cls):
    """Create an argument parser from a dataclass."""
    parser = ArgumentParser()

    for field in fields(cls):
        required = (field.default is MISSING
                    and field.default_factory is MISSING)
        arg_type = field.metadata.get("arg_type", field.type)
        parser.add_argument(*get_names(field),
                            type=arg_type, required=required)

    return parser


def datacli(cls, argv=None):
    """Parse command line arguments into a 'cls' object."""
    parser = make_parser(cls)
    data = {key: val for key, val in vars(parser.parse_args(argv)).items()
            if val is not None}
    return cls(**data)
