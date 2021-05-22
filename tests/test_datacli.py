from dataclasses import dataclass, field

from pytest import raises

from datacli import datacli, from_env_var

import os


def test_no_fields():
    @dataclass
    class Test:
        pass

    args = datacli(Test, [])
    assert args == Test()

    with raises(SystemExit):
        datacli(Test, ["--name", "Jim"])


def test_required_fields():
    @dataclass
    class Test:
        string: str
        integer: int

    args = datacli(Test, ["--string", "abc", "--integer", "10"])
    assert args == Test("abc", 10)

    with raises(SystemExit):
        datacli(Test, ["--string", "abc"])


def test_optional_fields():
    @dataclass
    class Test:
        string: str = "abc"
        integer: int = 10

    args = datacli(Test, [])
    assert args == Test("abc", 10)

    args = datacli(Test, ["--string", "foo"])
    assert args == Test("foo", 10)


def test_environment_variables():
    ENV_VAR_NAME = "STRING_FOR_TEST_CLI"

    @dataclass
    class Test:
        integer: int
        string: str = field(default_factory=from_env_var(ENV_VAR_NAME))

    with raises(ValueError):
        datacli(Test, ["--integer", "10"])

    os.environ[ENV_VAR_NAME] = "abcd"

    args = datacli(Test, ["--integer", "10"])

    assert args == Test(10, "abcd")
