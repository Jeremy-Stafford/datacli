import os
from typing import List, Optional, Tuple

"""A library for building simple CLIs from dataclasses.

DataCLI is based on argparse.
"""

from argparse import ArgumentParser
from contextlib import suppress
from dataclasses import Field, MISSING, fields

__version__ = "0.1.1"

env_var_default_factory_marker = "_datacli_get_env_var"
default_inception_marker = "_datacli_default_inception"


def get_names(field):
    """Return the CLI for a field."""
    with suppress(KeyError):
        yield field.metadata["short_name"]

    try:
        yield field.metadata["long_name"]
    except KeyError:
        yield "--" + field.name.replace("_", "-")


def from_env_var(env_var_name: str, default=None):
    """
    Add a default factory to extract the cli argument from env.
    Returns an anonymous function and passes metadata that can be used for further processing. 
    This solves the following problem:
    A default_factory is a zero parameter function that will be called as a default. As such it has no 
    awareness about the field name that it supposed to fill. The overall intention is to enable error 
    logging that reports both the cli parameter and the corresponding env variable that can be used to 
    fill a required value. Therefore, by raising an error in the default_factory, the application would
    not be able to report the corresponding cli argument without tightly coupling the name of the cli 
    argument and that of the env variable. Hence, by attaching the meta info about the fact that this 
    default factory reads env variables the name of the variable, the subsequent make_parser method can 
    provide more helpful error logging.
    """
    factory_function = lambda: os.getenv(env_var_name, default)

    factory_function.__qualname__ = env_var_default_factory_marker
    factory_function.__name__ = env_var_name
    setattr(factory_function, default_inception_marker, default)

    return factory_function


def has_env_default_factory(field: Field) -> bool:
    """
    Check if a field can be filled with an environment variable. This utilizes the explicit naming of the 
    initially anonymous default factory returned by `from_env_var`
    """
    default_factory = field.default_factory
    return not (default_factory is MISSING) \
        and default_factory.__qualname__ == env_var_default_factory_marker


def get_corresponding_env_var(field: Field) -> Optional[str]:
    """
    Utilize the dyanic name assigned to the initially anonymous default factory returned by `from_env_var`.
    """
    result = None
    if has_env_default_factory(field):
        result = field.default_factory.__name__
    return result


def make_parser(cls):
    """Create an argument parser from a dataclass."""
    parser = ArgumentParser()

    for field in fields(cls):
        default_factory = field.default_factory
        # The default factory called `from_env_var` is used to connect CLI parameters to environment
        # variables. The `from_env_var` factory also enables the distinction between required and
        # optional environment-connected CLI parameters through the passing of a `default` argument on the
        # dataclass.
        default_inception = getattr(default_factory, default_inception_marker, None)
        required = (field.default is MISSING
                    and default_factory is MISSING
                    and default_inception is None)

        help_text = field.metadata.get("help", "")
        env_var_default: Optional[str] = None
        corresponding_env_var = get_corresponding_env_var(field)

        if corresponding_env_var:
            help_text = help_text + \
                (", " if len(help_text) > 0 else "") + \
                f"can also be set with environment variable {corresponding_env_var}"
            env_var_default = os.getenv(corresponding_env_var)

        arg_type = field.metadata.get("arg_type", field.type)

        parser.add_argument(*get_names(field),
                            type=arg_type,  # type: ignore
                            help=help_text,
                            required=required,
                            default=env_var_default)

    return parser


def check_fields_with_env_defaults(instance):
    for field in fields(type(instance)):
        field_content = getattr(instance, field.name)
        corresponding_env_var = get_corresponding_env_var(field)
        if corresponding_env_var and field_content is None:
            raise ValueError(
                f"{field.name} not set, either supply either of the arguments {list(get_names(field))} "
                + f"or set environment variable {corresponding_env_var}"
            )


def datacli(cls, argv=None):
    """Parse command line arguments into a 'cls' object."""
    parser = make_parser(cls)
    data = {key: val for key, val in vars(parser.parse_args(argv)).items()
            if val is not None}
    instance = cls(**data)
    check_fields_with_env_defaults(instance)
    return instance
