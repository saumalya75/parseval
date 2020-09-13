import pytest
import types
import tempfile
from parseval.parser import Parser
from parseval.parser import (
    StringParser,
    IntegerParser,
    FloatParser,
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
        ('ID', StringParser(1, 2)),
        ('NAME', StringParser(3, 5).change_case('U').not_null('nan', allow_white_space=True)),
        ('GENDER', StringParser(6, 6).value_set(['M', 'F'])),
        ('NOT_NULLABLE_VALUE', StringParser(7, 11).not_null('dummy')),
        ('NULLABLE_VALUE', StringParser(7, 11)),
        ('BIRTH_YEAR', IntegerParser(12, 13).max_value(20)),
        ('BALANCE', FloatParser(14, 17).min_value(10.0))
    ]


@pytest.yield_fixture(name="fixed_width_file_name", scope="session")
def _fixed_width_file_name():
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as sf:
            sf.writelines('d0sauMvalue191000\n')
            sf.writelines('d0pouM     2090.03\n')
            sf.writelines('d0pouX     2090.03')
        yield tf.name


@pytest.yield_fixture(name="fixed_width_bad_file_name", scope="session")
def _fixed_width_bad_file_name():
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as sf:
            sf.writelines('d0sauMvalue191000\n')
            sf.writelines('d0pouY     2090.03\n')
            sf.writelines('d0pouX     2090.03')
        yield tf.name


@pytest.fixture(name="fixed_width_lol", scope="session")
def _fixed_width_lol():
    return [
        'd0sauMvalue191000\n',
        'd0pouM     2090.03\n',
        'd0pouX     2090.03'
    ]


@pytest.fixture(name="fixed_width_bad_lol", scope="session")
def _fixed_width_bad_lol():
    return [
        'd0sauMvalue191000\n',
        'd0pouY     2090.03\n',
        'd0pouX     2090.03'
    ]


def test_fixed_width_input_as_file_object_one_error_allowed(schema, fixed_width_file_name):
    with open(fixed_width_file_name, 'r') as sf:
        p_allow_one_error = Parser(schema=schema, stop_on_error=1, input_row_format='fixed-width')
        parsed_data = p_allow_one_error.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, str)
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 2


def test_fixed_width_input_as_file_object_no_error_allowed(schema, fixed_width_file_name):
    with open(fixed_width_file_name, 'r') as sf:
        p_allow_no_error = Parser(schema=schema, input_row_format='fixed-width')
        with pytest.raises(Exception):
            list(p_allow_no_error.parse(sf))


def test_fixed_width_input_as_file_object_all_error_allowed(schema, fixed_width_bad_file_name):
    with open(fixed_width_bad_file_name, 'r') as sf:
        p_allow_all_error = Parser(schema=schema, stop_on_error=-1, input_row_format='fixed-width')
        parsed_data = p_allow_all_error.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, str)
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 1


def test_fixed_width_input_as_lol_one_error_allowed(schema, fixed_width_lol):
    p_allow_one_error = Parser(schema=schema, stop_on_error=1, input_row_format='fixed-width')
    parsed_data = p_allow_one_error.parse(fixed_width_lol)
    assert isinstance(parsed_data, types.GeneratorType)
    parsed_lines = []
    for parsed_line in parsed_data:  # calling data parsing on file object
        assert isinstance(parsed_line, str)
        parsed_lines.append(parsed_line)
    assert len(parsed_lines) == 2


def test_fixed_width_input_as_lol_no_error_allowed(schema, fixed_width_lol):
    p_allow_no_error = Parser(schema=schema, input_row_format='fixed-width')
    with pytest.raises(Exception):
        list(p_allow_no_error.parse(fixed_width_lol))


def test_delimited_input_as_lol_all_error_allowed(schema, fixed_width_bad_lol):
    p_allow_all_error = Parser(schema=schema, stop_on_error=-1, input_row_format='fixed-width')
    parsed_data = p_allow_all_error.parse(fixed_width_bad_lol)
    assert isinstance(parsed_data, types.GeneratorType)
    parsed_lines = []
    for parsed_line in parsed_data:  # calling data parsing on file object
        assert isinstance(parsed_line, str)
        parsed_lines.append(parsed_line)
    assert len(parsed_lines) == 1
