import os
from typing import List, Optional, Tuple

"""A library for building simple CLIs from dataclasses.

DataCLI is based on argparse.
"""

from argparse import ArgumentParser
from contextlib import suppress
from dataclasses import Field, MISSING, fields

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
    def _datacli_get_env_var() -> str:
        val_from_env_var = os.getenv(env_var_name, "")
        return val_from_env_var

    _datacli_get_env_var.__name__ = env_var_name
    return _datacli_get_env_var


def has_env_default_factory(field: Field) -> bool:
    default_factory = field.default_factory
    function_name_len = len("_datacli_get_env_var")
    return not (default_factory is MISSING) and default_factory.__qualname__[-function_name_len:] == "_datacli_get_env_var"


def get_corresponding_env_var(field: Field) -> Optional[str]:
    result = None
    if has_env_default_factory(field):
        result = field.default_factory.__name__
    return result


def make_parser(cls):
    """Create an argument parser from a dataclass."""
    parser = ArgumentParser()

    for field in fields(cls):
        default_factory = field.default_factory

        required = (field.default is MISSING
                    and default_factory is MISSING)


        help_text = field.metadata.get("help", "")
        env_var_default: Optional[str] = None
        corresponding_env_var = get_corresponding_env_var(field)

        if corresponding_env_var:
            help_text = help_text + f", can also be set with environment variable {corresponding_env_var}"
            env_var_default = os.getenv(corresponding_env_var)

        arg_type = field.metadata.get("arg_type", field.type)

        parser.add_argument(*get_names(field),
                            type=arg_type, # type: ignore
                            help=help_text,
                            required=required,
                            default=env_var_default)

    return parser

def check_fields_with_env_defaults(instance):
    for field in fields(type(instance)):
        field_content = getattr(instance, field.name)
        corresponding_env_var = get_corresponding_env_var(field)
        if corresponding_env_var and field_content == "":
            raise ValueError(f"{field.name} not set, either supply either of the arguments {list(get_names(field))} " \
                    + f"or set environment variable {corresponding_env_var}")

def datacli(cls, argv=None):
    """Parse command line arguments into a 'cls' object."""
    parser = make_parser(cls)
    data = {key: val for key, val in vars(parser.parse_args(argv)).items()
            if val is not None}
    instance = cls(**data)
    check_fields_with_env_defaults(instance)
    return instance
