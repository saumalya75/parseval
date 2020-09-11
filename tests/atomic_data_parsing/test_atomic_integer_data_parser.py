import pytest
from parseval.parser import IntegerParser
from parseval.exceptions import (
    UnexpectedParsingException,
    NullValueInNotNullFieldException,
    UnsupportedDatatypeException,
    ValidValueCheckException,
    MaximumValueConstraintException,
    MinimumValueConstraintException
)


# Valid value tests
def test_valid_value():
    func = IntegerParser().build()
    assert func(1) == 1
    assert func("1") == 1
    assert func(1.0) == 1
    with pytest.raises(UnexpectedParsingException):
        assert func("1a")


# Quoted string handling tests
def test_non_quoted_data():
    func = IntegerParser().build()
    data = 1
    assert func(data) == 1


def test_double_quoted_data():
    func = IntegerParser(quoted=1).build()
    data = '"1"'
    assert func(data) == 1


def test_single_quoted_data():
    func = IntegerParser(quoted=2).build()
    data = "'1'"
    assert func(data) == 1


# Type enforce tests
def test_enforce_type():
    func = IntegerParser(enforce_type=False).build()
    data = "1"
    assert func(data) == "1"


# Validators test
def test_not_null_validator():
    func = IntegerParser(quoted=0).not_null().build()
    assert func("123") == 123
    with pytest.raises(NullValueInNotNullFieldException):
        assert func(None)
        assert func("")

    # Default value assignment check
    func = IntegerParser(quoted=0).not_null(default_value=0).build()
    assert func(None) == 0
    assert func("") == 0

    with pytest.raises(UnsupportedDatatypeException):
        IntegerParser(quoted=0).not_null(default_value="0").build()


def test_value_set_validator():
    allowed_values = [100, 200, 300]
    func = IntegerParser(quoted=0).value_set(allowed_values).build()
    assert func(100) == 100
    assert func("300") == 300
    with pytest.raises(ValidValueCheckException):
        assert func('201')

    with pytest.raises(UnsupportedDatatypeException):
        IntegerParser(quoted=0).value_set(["100", "200", "300"]).build()


def test_max_value_validator():
    func = IntegerParser(quoted=0).max_value(100).build()
    assert func('90') == 90
    assert func('80') == 80
    with pytest.raises(MaximumValueConstraintException):
        assert func(101)

    with pytest.raises(UnsupportedDatatypeException):
        IntegerParser(quoted=0).max_value("300").build()


def test_min_value_validator():
    func = IntegerParser(quoted=0).min_value(100).build()
    assert func('190') == 190
    assert func('180') == 180
    with pytest.raises(MinimumValueConstraintException):
        assert func(10)

    with pytest.raises(UnsupportedDatatypeException):
        IntegerParser(quoted=0).min_value("300").build()


def test_range_validator():
    func = IntegerParser(quoted=0).range(lower_bound=100, upper_bound=300).build()
    assert func('190') == 190
    assert func('280') == 280
    with pytest.raises(MaximumValueConstraintException):
        assert func(310)
    with pytest.raises(MinimumValueConstraintException):
        assert func(10)


def _parity_check(data):
    if data:
        i_data = int(data)
        if i_data % 2 != 0:
            raise Exception("The data has to be even!")
    return data


def test_add_func_validator():
    func = IntegerParser().add_func(_parity_check).build()
    assert func(298) == 298
    with pytest.raises(Exception):
        func(299)
