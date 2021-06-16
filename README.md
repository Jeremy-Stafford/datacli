# Datacli

`datacli` is a library for building simple command line interfaces from
dataclasses. It is built on `argparse` and has no dependencies.

## Usage

A ~~picture~~ code snippet speaks a thousand words:

```python
# person.py

from dataclasses import dataclass, field
from datacli import datacli

@dataclass
class Person:
    name: str
    age: int = 30

args = datacli(Person)
print(args)
```

```shell
$ python person.py --name "Jeremy"
Person(name="Jeremy", age=30)
$ python person.py --name "Jeremy" --age 20
Person(name="Jeremy", age=20)
$ python person.py --help
usage: test.py [-h] --name NAME [--age AGE]

optional arguments:
  -h, --help   show this help message and exit
  --name NAME
  --age AGE
```

## Field names

Short and long field names (`-a` or `--foo-bar`) can be modified through the
[data-class field metadata][field], for example,

```python
# person.py

from dataclasses import dataclass, field
from datacli import datacli

@dataclass
class Person:
    name: str = field(metadata={"short_name": "-n"})
    age: int = field(metadata={"short_name": "-a", "long_name": "--years"})

args = datacli(Person)
print(args)
```

```shell
$ python person.py -n "Jeremy" -a 20
Person(name="Jeremy", age=20)
$ python person.py --name "Jeremy" --years 30
Person(name="Jeremy", age=30)
$ python person.py --help
usage: test.py [-h] --name NAME --age AGE

optional arguments:
  -h, --help   show this help message and exit
  -n, --name NAME
  -a, --age YEARS
```

If you want to use defaults with field names, you should use the [`default` or
`default_factory`][field] arguments to `field()`, for example,

```python
age: int = field(default=20, metadata={"short_name": "-a"})
```

[field]: https://docs.python.org/3/library/dataclasses.html#dataclasses.field

## Help Text

Add custom help messages through `field(metadata={"help": <help text>})`

## Environment variables

Link CLI arguments to environment variables and add defaults via
`field(default_factory=from_env_var(<var_name>, [default=<some_default>]))`.
If `default` is omitted then the value is mandatory and `datacli` will fail with a helpful error message if
neither the parameter nor the environment variable are provided. Setting the `from_env_var` as a default
factory also expands the help text to give the name of the connected environment variable.
