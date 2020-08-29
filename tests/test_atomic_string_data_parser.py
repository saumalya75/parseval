import pytest
from parseval.parser import StringParser
from parseval.exceptions import (
    NullValueInNotNullFieldException,
    ValidValueCheckException,
    RegexMatchException
)


# Quoted string handling tests
def test_non_quoted_data():
    func = StringParser().build()
    data = "ABC"
    assert func(data) == "ABC"


def test_double_quoted_data():
    func = StringParser(quoted=1).build()
    data = '"ABC"'
    assert func(data) == 'ABC'


def test_single_quoted_data():
    func = StringParser(quoted=2).build()
    data = "'ABC'"
    assert func(data) == "ABC"


# Validators test
def test_not_null_validator():
    func = StringParser(quoted=0).not_null().build()
    assert func("SOME_VALUE") == "SOME_VALUE"
    with pytest.raises(NullValueInNotNullFieldException):
        assert func(None)
        assert func("") == ""
    p = StringParser().not_null(allow_white_space=True)
    print(p._funcs)
    func = p.build()
    assert func("") == ""

    # Default value assignment check
    func = StringParser(quoted=0).not_null(default_value="NA").build()
    assert func(None) == "NA"
    assert func("") == "NA"


def test_value_set_validator():
    allowed_values = ['MAEVE', 'OTIS', 'ERIC']
    func = StringParser(quoted=0).value_set(allowed_values).build()
    assert func('OTIS') == "OTIS"
    with pytest.raises(ValidValueCheckException):
        assert func('GRY')


def test_regex_match_validator():
    pattern = r'\w+_\d{4}-\d{2}-\d{2}'
    func = StringParser(quoted=0).regex_match(pattern=pattern).build()
    assert func('Manual_2020-23-12') == "Manual_2020-23-12"
    with pytest.raises(RegexMatchException):
        assert func('Trig2020-23-12')


def test_change_case_validator():
    func = StringParser(quoted=0).change_case(case_type='u').build()
    assert func('Manual_2020-23-12') == "MANUAL_2020-23-12"


def _first_three_char_check(data: str):
    list_of_allowed_value: list = ['ABC', 'DEF']
    if not data:
        return data

    if str(data)[:3].upper() in [word.upper() for word in list_of_allowed_value]:
        return data[3:]
    else:
        raise Exception("Bad prefix in the value.")


def test_add_func_validator():
    func = StringParser(quoted=0).add_func(_first_three_char_check).build()
    assert func("ABC2344") == "2344"
    with pytest.raises(Exception):
        assert func("PQR2344") == "2344"
