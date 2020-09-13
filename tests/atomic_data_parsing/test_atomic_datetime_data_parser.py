import pytest
import datetime
from parseval.parser import DatetimeParser
from parseval.exceptions import (
    DateTimeParsingException,
    NullValueInNotNullFieldException,
    ValidValueCheckException,
    MaximumValueConstraintException,
    MinimumValueConstraintException,
    UnexpectedParsingException
)


# Type enforce tests
def test_enforce_type():
    func = DatetimeParser(enforce_type=False).build()
    data = "20200101"
    assert func(data) == "20200101"
    func = DatetimeParser(enforce_type=True).build()
    data = "20200101"
    assert func(data) == datetime.datetime.strptime('20200101', '%Y%m%d')


# Data parsing test
@pytest.mark.parametrize("input_data,input_format", [
    ('20200101', ''),
    ('2020010124100', ''),
    ('2020~01~01', '%Y~%m~%d'),
    ('2020 01 01 12:10:10', '%Y %m %d %H:%M:%S'),
    ('2020/01/01T12 10 10Z', '%Y/%m/%dT%H %M %SZ'),
])
def test_valid_data_parsing_type_converted(input_data, input_format):
    if input_format:
        func = DatetimeParser(formats=[input_format]).build()
    else:
        func = DatetimeParser().build()
    if not input_format:
        if len(input_data) == 8:
            input_format = '%Y%m%d'
        else:
            input_format = '%Y%m%d%H%M%S'
    assert func(input_data) == datetime.datetime.strptime(input_data, input_format)


# Data parsing test
@pytest.mark.parametrize("input_data,input_format", [
    ('20200101', ''),
    ('2020010124100', ''),
    ('2020~01~01', '%Y~%m~%d'),
    ('2020 01 01 12:10:10', '%Y %m %d %H:%M:%S'),
    ('2020/01/01T12 10 10Z', '%Y/%m/%dT%H %M %SZ'),
])
def test_valid_data_parsing_type_preserved(input_data, input_format):
    if input_format:
        func = DatetimeParser(formats=[input_format], enforce_type=False).build()
    else:
        func = DatetimeParser(enforce_type=False).build()
    assert func(input_data) == input_data


# Data parsing test
@pytest.mark.parametrize("input_data,input_format", [
    ('20201301', ''),
    ('2020013424100', ''),
    ('2020~02~31', '%Y~%m~%d'),
    ('2020 01 01 12:10:10', '%Y/%m/%d %H:%M:%S')
])
def test_invalid_data_parsing(input_data, input_format):
    if input_format:
        func = DatetimeParser(formats=[input_format], enforce_type=False).build()
    else:
        func = DatetimeParser(enforce_type=False).build()
    with pytest.raises(DateTimeParsingException):
        assert func(input_data)


# Quoted string handling tests
def test_non_quoted_data():
    func = DatetimeParser(enforce_type=False).build()
    data = "20200101"
    assert func(data) == "20200101"
    int_data = 20200101
    assert func(int_data) == 20200101


def test_double_quoted_data():
    func = DatetimeParser(quoted=1).build()
    data = '"20200101"'
    assert func(data) == datetime.datetime.strptime('20200101', '%Y%m%d')


def test_single_quoted_data():
    func = DatetimeParser(quoted=2).build()
    data = "'20200101'"
    assert func(data) == datetime.datetime.strptime('20200101', '%Y%m%d')


# Validators test
def test_not_null_validator():
    func = DatetimeParser(quoted=0, enforce_type=False).not_null().build()
    assert func("20200101") == "20200101"
    with pytest.raises(NullValueInNotNullFieldException):
        assert func(None)
        assert func("") == ""

    # Default value assignment check
    func = DatetimeParser().not_null(default_value="20200101", format='%Y%m%d').build()
    assert func(None) == datetime.datetime.strptime('20200101', '%Y%m%d')
    assert func("") == datetime.datetime.strptime('20200101', '%Y%m%d')


def test_value_set_validator():
    allowed_values = [datetime.datetime.strptime('20200101', '%Y%m%d'), datetime.datetime.strptime('20200102', '%Y%m%d')]
    func = DatetimeParser().value_set(allowed_values).build()
    assert func('20200101') == datetime.datetime.strptime('20200101', '%Y%m%d')
    with pytest.raises(ValidValueCheckException):
        assert func('20200103')


def test_max_value_validator():
    func = DatetimeParser(formats=['%Y-%m-%d']).max_value(value='31/12/2020', format='%d/%m/%Y').build()
    assert func('2020-12-31')
    assert func('1970-01-01')
    with pytest.raises(MaximumValueConstraintException):
        assert func('2021-12-31')

    with pytest.raises(UnexpectedParsingException):
        DatetimeParser().max_value("300").build()


def test_min_value_validator():
    func = DatetimeParser(formats=['%Y-%m-%d']).min_value(value='01/01/2020', format='%d/%m/%Y').build()
    assert func('2020-12-31')
    assert func('2020-01-01')
    with pytest.raises(MinimumValueConstraintException):
        assert func('2019-12-31')

    with pytest.raises(UnexpectedParsingException):
        DatetimeParser().max_value("300").build()


def test_range_validator():
    func = DatetimeParser(formats=['%Y-%m-%d']).range(
        lower_bound='01/01/2020',
        upper_bound=datetime.datetime.strptime('20201231', '%Y%m%d'),
        format='%d/%m/%Y'
    ).build()
    assert func('2020-01-01')
    assert func('2020-12-31')
    assert func('2020-06-30')
    with pytest.raises(MinimumValueConstraintException):
        assert func('2019-12-31')
    with pytest.raises(MaximumValueConstraintException):
        assert func('2021-01-01')


def _get_month_value(data: str):
    if not data:
        return data
    return data.month


def test_add_func_validator():
    func = DatetimeParser().add_func(_get_month_value).build()
    assert func("20200501") == 5


def test_convert():
    func = DatetimeParser().convert('%Y|%m|%d').build()
    assert func("20200501") == "2020|05|01"
