import os
from typing import List, Optional, Tuple

"""A library for building simple CLIs from dataclasses.

DataCLI is based on argparse.
"""

from argparse import ArgumentParser
from contextlib import suppress
from dataclasses import MISSING, fields

__version__ = "0.1.1"


def get_names(field):
    """Return the CLI for a field."""
    with suppress(KeyError):
        yield field.metadata["short_name"]

    try:
        yield field.metadata["long_name"]
    except KeyError:
        yield "--" + field.name.replace("_", "-")


def from_env_var(env_var_name: str):
    """add a default factory to extract the cli argument from env"""
    def _get() -> str:
        return os.getenv(env_var_name, f"")
    return _get


def make_parser(cls):
    """Create an argument parser from a dataclass."""
    parser = ArgumentParser()

    for field in fields(cls):
        corresponding_env_var = field.metadata.get("env_var")

        required = (field.default is MISSING
                    and field.default_factory is MISSING)

        env_var_default: Optional[str] = None
        help_text = field.metadata.get("help")

        if corresponding_env_var:
            required = False
            help_text = help_text + f", can also be set with environment variable {corresponding_env_var}"
            env_var_default = os.getenv(corresponding_env_var, "")

        arg_type = field.metadata.get("arg_type", field.type)

        parser.add_argument(*get_names(field),
                            type=arg_type, # type: ignore
                            help=help_text,
                            required=required,
                            default=env_var_default)

    return parser

def check_fields_with_env_defaults(instance):
    for field in fields(type(instance)):
        corresponding_env_var = field.metadata.get("env_var")
        if corresponding_env_var and getattr(instance, field.name) == "":
            error_message = f"{field.name} not set, either supply arguments {list(get_names(field))} " \
                + f"or set environment variable {corresponding_env_var}"
            raise ValueError(error_message)


def datacli(cls, argv=None):
    """Parse command line arguments into a 'cls' object."""
    parser = make_parser(cls)
    data = {key: val for key, val in vars(parser.parse_args(argv)).items()
            if val is not None}
    instance = cls(**data)
    check_fields_with_env_defaults(instance)
    return instance
