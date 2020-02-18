from dataclasses import dataclass

from pytest import raises

from datacli import datacli


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
