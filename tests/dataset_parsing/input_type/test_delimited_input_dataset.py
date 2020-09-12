import pytest
import types
import tempfile
import datetime
from parseval.parser import Parser
from parseval.parser import (
    StringParser,
    DatetimeParser,
    IntegerParser,
    FloatParser,
    ConstantParser
)


@pytest.fixture(name="custom_function", scope="session")
def _custom_function():
    def _parity_check(data):
        if data:
            try:
                i_data = int(data)
            except:
                pass
            if i_data % 2 != 0:
                raise Exception("The data has to be even!")
        return data

    return _parity_check


@pytest.fixture(name="schema", scope="session")
def _schema(custom_function):
    return [
        ('ID', StringParser(quoted=1)),
        ('RUN_ID', StringParser().regex_match(r'\w+_\d{4}-\d{2}-\d{2}').change_case('u')),
        ('CLASS', StringParser(start=1, end=1).value_set(['a', 'b', 'A'])),
        ('INITIATED_ON', DatetimeParser(formats=['%Y%m%d', '%Y-%m-%d %H:%M:%S'])
         .convert('%Y/%m/%d').max_value(datetime.datetime.now())
         .min_value(value='20000101', format='%Y%m%d')
         .not_null(datetime.datetime.strptime('19001231', '%Y%m%d'))
         ),
        ('ASKED_AMOUNT', IntegerParser().max_value(2000).not_null(default_value=0)),
        ('ADJUSTED_AMOUNT', FloatParser().min_value(10.0).not_null(0.0)),
        ('ROLE_MODEL', ConstantParser('Leo Messi')),
        ('BLOCK_NUMBER', IntegerParser().add_func(custom_function).range(0, 40))
    ]


@pytest.yield_fixture(name="delimited_file_details", scope="session")
def _delimited_file_details():
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as sf:
            sf.writelines('""|Trig2020-23-12|A|20200123|2000|21.0934||10\n')
            sf.writelines('"DEF"||abc|||||34\n')
            sf.writelines('"DEF"|Manual_2020-23-12||2020-01-23 10:20:23|1200|11||')
        yield tf.name, "|"


@pytest.yield_fixture(name="delimited_bad_file_details", scope="session")
def _delimited_bad_file_details():
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as sf:
            sf.writelines('""|Trig2020-23-12|A|20200123|2000|21.0934||10\n')
            sf.writelines('"DEF"||abc|||||34\n')
            sf.writelines('"DEF"|Manual2020-23-12||2020-01-23 10:20:23|1200|11||')
        yield tf.name, "|"


@pytest.fixture(name="delimited_lol_details", scope="session")
def _delimited_lol_details():
    return [
        '"",Trig2020-23-12,A,20200123,2000,21.0934,,10\n',
        '"DEF",,abc,,,,,34\n',
        '"DEF",Manual_2020-23-12,,2020-01-23 10:20:23,1200,11,,'
    ], ","


@pytest.fixture(name="delimited_bad_lol_details", scope="session")
def _delimited_bad_lol_details():
    return [
        '"",Trig2020-23-12,A,20200123,2000,21.0934,,10\n',
        '"DEF",,abc,,,,,34\n',
        '"DEF",Manual2020-23-12,,2020-01-23 10:20:23,1200,11,,'
    ], ","


def test_delimited_input_as_file_object_one_error_allowed(schema, delimited_file_details):
    with open(delimited_file_details[0], 'r') as sf:
        p_allow_one_error = Parser(schema=schema, stop_on_error=1)
        parsed_data = p_allow_one_error.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, str)
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 2


def test_delimited_input_as_file_object_no_error_allowed(schema, delimited_file_details):
    with open(delimited_file_details[0], 'r') as sf:
        p_allow_no_error = Parser(schema=schema)
        with pytest.raises(Exception):
            list(p_allow_no_error.parse(sf))


def test_delimited_input_as_file_object_all_error_allowed(schema, delimited_bad_file_details):
    with open(delimited_bad_file_details[0], 'r') as sf:
        p_allow_all_error = Parser(schema=schema, stop_on_error=-1)
        parsed_data = p_allow_all_error.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, str)
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 1


def test_delimited_input_as_lol_one_error_allowed(schema, delimited_lol_details):
    p_allow_one_error = Parser(schema=schema, stop_on_error=1, input_row_sep=delimited_lol_details[1])
    parsed_data = p_allow_one_error.parse(delimited_lol_details[0])
    assert isinstance(parsed_data, types.GeneratorType)
    parsed_lines = []
    for parsed_line in parsed_data:  # calling data parsing on file object
        assert isinstance(parsed_line, str)
        parsed_lines.append(parsed_line)
    assert len(parsed_lines) == 2


def test_delimited_input_as_lol_no_error_allowed(schema, delimited_lol_details):
    p_allow_no_error = Parser(schema=schema, input_row_sep=delimited_lol_details[1])
    with pytest.raises(Exception):
        list(p_allow_no_error.parse(delimited_lol_details[0]))


def test_delimited_input_as_lol_all_error_allowed(schema, delimited_bad_lol_details):
    p_allow_all_error = Parser(schema=schema, stop_on_error=-1, input_row_sep=delimited_bad_lol_details[1])
    parsed_data = p_allow_all_error.parse(delimited_bad_lol_details[0])
    assert isinstance(parsed_data, types.GeneratorType)
    parsed_lines = []
    for parsed_line in parsed_data:  # calling data parsing on file object
        assert isinstance(parsed_line, str)
        parsed_lines.append(parsed_line)
    assert len(parsed_lines) == 1
