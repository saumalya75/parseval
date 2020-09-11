import pytest
from parseval.parser import FloatParser
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
    func = FloatParser().build()
    assert func(1.0) == 1.0
    assert func("1") == 1.0
    assert func(1.0) == 1.0
    with pytest.raises(UnexpectedParsingException):
        assert func("1a")


# Quoted string handling tests
def test_non_quoted_data():
    func = FloatParser().build()
    data = 1.0
    assert func(data) == 1.0


def test_double_quoted_data():
    func = FloatParser(quoted=1).build()
    data = '"1.0"'
    assert func(data) == 1.0


def test_single_quoted_data():
    func = FloatParser(quoted=2).build()
    data = "'1.0'"
    assert func(data) == 1.0


# Type enforce tests
def test_enforce_type():
    func = FloatParser(enforce_type=False).build()
    data = "1.0"
    assert func(data) == "1.0"


# Validators test
def test_not_null_validator():
    func = FloatParser(quoted=0).not_null().build()
    assert func("123.50") == 123.5
    with pytest.raises(NullValueInNotNullFieldException):
        assert func(None)
        assert func("")

    # Default value assignment check
    func = FloatParser(quoted=0).not_null(default_value=0).build()
    assert func(None) == 0
    assert func("") == 0

    with pytest.raises(UnsupportedDatatypeException):
        FloatParser(quoted=0).not_null(default_value="0").build()


def test_value_set_validator():
    allowed_values = [100.50, 200.60, 300.70]
    func = FloatParser(quoted=0).value_set(allowed_values).build()
    assert func(100.50) == 100.50
    assert func("300.70") == 300.70
    with pytest.raises(ValidValueCheckException):
        assert func('201')

    with pytest.raises(UnsupportedDatatypeException):
        FloatParser(quoted=0).value_set(["100", "200", "300"]).build()


def test_max_value_validator():
    func = FloatParser(quoted=0).max_value(100.9).build()
    assert func('100.8') == 100.8
    assert func('100.89') == 100.89
    with pytest.raises(MaximumValueConstraintException):
        assert func(101)

    with pytest.raises(UnsupportedDatatypeException):
        FloatParser(quoted=0).max_value("300").build()


def test_min_value_validator():
    func = FloatParser(quoted=0).min_value(99.99).build()
    assert func('99.99') == 99.99
    assert func('99.991') == 99.991
    with pytest.raises(MinimumValueConstraintException):
        assert func(10)

    with pytest.raises(UnsupportedDatatypeException):
        FloatParser(quoted=0).min_value("300").build()


def test_range_validator():
    func = FloatParser(quoted=0).range(lower_bound=99.99, upper_bound=100.0).build()
    assert func('99.99') == 99.99
    assert func('100') == 100
    assert func('99.999') == 99.999
    with pytest.raises(MaximumValueConstraintException):
        assert func(100.0000000000001)
    with pytest.raises(MinimumValueConstraintException):
        assert func(99.989999999)


def _parity_check(data):
    if data:
        i_data = float(data)
        if i_data % 2 != 0:
            raise Exception("The data has to be even!")
    return data


def test_add_func_validator():
    func = FloatParser().add_func(_parity_check).build()
    assert func(298.0) == 298.0
    with pytest.raises(Exception):
        func(298.1)
