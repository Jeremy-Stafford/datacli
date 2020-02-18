# datacli

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
