import json
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
from parseval.exceptions import UnexpectedSystemException


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


@pytest.fixture(name="fw_schema", scope="session")
def _fw_schema(custom_function):
    return [
        ('ID', StringParser(1, 2)),
        ('NAME', StringParser(3, 5).change_case('U').not_null('nan', allow_white_space=True)),
        ('GENDER', StringParser(6, 6).value_set(['M', 'F'])),
        ('NOT_NULLABLE_VALUE', StringParser(7, 11).not_null('dummy')),
        ('NULLABLE_VALUE', StringParser(7, 11)),
        ('BIRTH_YEAR', IntegerParser(12, 13).max_value(20)),
        ('BALANCE', FloatParser(14, 17).min_value(10.0))
    ]


@pytest.yield_fixture(name="delimited_file_details", scope="session")
def _delimited_file_details():
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as sf:
            sf.writelines('""|Trig2020-23-12|A|20200123|2000|21.0934||10\n')
            sf.writelines('"DEF"||abc|||||34\n')
            sf.writelines('"DEF"|Manual_2020-23-12||2020-01-23 10:20:23|1200|11||')
        yield tf.name, "|"


@pytest.yield_fixture(name="fixed_width_file_name", scope="session")
def _fixed_width_file_name():
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as sf:
            sf.writelines('d0sauMvalue191000\n')
            sf.writelines('d0pouM     2090.03\n')
            sf.writelines('d0pouX     2090.03')
        yield tf.name


@pytest.yield_fixture(name="json_file_name", scope="session")
def _json_file_name():
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as sf:
            sf.writelines(json.dumps({
                'ID': "",
                'RUN_ID': "Trig2020-23-12",
                'CLASS': "A",
                'INITIATED_ON': 20200123,
                'ASKED_AMOUNT': 2000,
                'ADJUSTED_AMOUNT': 21.0934,
                'ROLE_MODEL': "",
                'BLOCK_NUMBER': 10
            }) + '\n')
            sf.writelines(json.dumps({
                'ID': "DEF",
                'RUN_ID': None,
                'CLASS': "abc",
                'INITIATED_ON': None,
                'ASKED_AMOUNT': None,
                'ADJUSTED_AMOUNT': None,
                'ROLE_MODEL': "",
                'BLOCK_NUMBER': 34
            }) + '\n')
            sf.writelines(json.dumps({
                'ID': "DEF",
                'RUN_ID': "Manual_2020-23-12",
                'CLASS': "",
                'INITIATED_ON': "2020-01-23 10:20:23",
                'ASKED_AMOUNT': 1200,
                'ADJUSTED_AMOUNT': 11,
                'ROLE_MODEL': "CR7",
                'BLOCK_NUMBER': None
            }))
        yield tf.name


@pytest.fixture(name="json_lol", scope="session")
def _json_lol():
    return [
            {
                'ID': "",
                'RUN_ID': "Trig2020-23-12",
                'CLASS': "A",
                'INITIATED_ON': 20200123,
                'ASKED_AMOUNT': 2000,
                'ADJUSTED_AMOUNT': 21.0934,
                'ROLE_MODEL': "",
                'BLOCK_NUMBER': 10
            },
            {
                'ID': "DEF",
                'RUN_ID': None,
                'CLASS': "abc",
                'INITIATED_ON': None,
                'ASKED_AMOUNT': None,
                'ADJUSTED_AMOUNT': None,
                'ROLE_MODEL': "",
                'BLOCK_NUMBER': 34
            },
            {
                'ID': "DEF",
                'RUN_ID': "Manual_2020-23-12",
                'CLASS': "",
                'INITIATED_ON': "2020-01-23 10:20:23",
                'ASKED_AMOUNT': 1200,
                'ADJUSTED_AMOUNT': 11,
                'ROLE_MODEL': "CR7",
                'BLOCK_NUMBER': None
            }
    ]


def test_delimited_input_delimited_output(schema, delimited_file_details):
    with open(delimited_file_details[0], 'r') as sf:
        p_delimited_output = Parser(schema=schema, stop_on_error=1, parsed_row_format='delimited', parsed_row_sep=",")
        parsed_data = p_delimited_output.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, str)
            assert len(parsed_line.split(",")) == 8
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 2


def test_delimited_input_dict_output(schema, delimited_file_details):
    with open(delimited_file_details[0], 'r') as sf:
        p_dict_output = Parser(schema=schema, stop_on_error=1, parsed_row_format='dict')
        parsed_data = p_dict_output.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, dict)
            assert len(parsed_line.keys()) == 8
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 2


def test_delimited_input_wrong_output(schema):
    with pytest.raises(UnexpectedSystemException):
        Parser(schema=schema, parsed_row_format='json')
    with pytest.raises(UnexpectedSystemException):
        Parser(schema=schema, parsed_row_format='fixed_width')


def test_fixed_input_delimited_output(fw_schema, fixed_width_file_name):
    with open(fixed_width_file_name, 'r') as sf:
        p_delimited_output = Parser(
            schema=fw_schema,
            stop_on_error=1,
            input_row_format='fixed-width',
            parsed_row_format='delimited',
            parsed_row_sep=","
        )
        parsed_data = p_delimited_output.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, str)
            assert len(parsed_line.split(",")) == 7
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 2


def test_fixed_input_fixed_width_output(fw_schema, fixed_width_file_name):
    with open(fixed_width_file_name, 'r') as sf:
        p_delimited_output = Parser(
            schema=fw_schema,
            stop_on_error=1,
            input_row_format='fixed-width',
            parsed_row_format='fixed-width'
        )
        parsed_data = p_delimited_output.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, str)
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 2


def test_fixed_width_input_dict_output(fw_schema, fixed_width_file_name):
    with open(fixed_width_file_name, 'r') as sf:
        p_dict_output = Parser(
            schema=fw_schema,
            stop_on_error=1,
            input_row_format='fixed-width',
            parsed_row_format='dict'
        )
        parsed_data = p_dict_output.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, dict)
            assert len(parsed_line.keys()) == 7
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 2


def test_fixed_width_input_wrong_output(fw_schema):
    with pytest.raises(UnexpectedSystemException):
        Parser(schema=fw_schema, parsed_row_format='json')


def test_json_input_json_output(schema, json_file_name):
    with open(json_file_name, 'r') as sf:
        p_json_output = Parser(
            schema=schema,
            stop_on_error=-1,
            input_row_format='json',
            parsed_row_format='json'
        )
        parsed_data = p_json_output.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, str)
            assert len(json.loads(parsed_line).keys()) == 8
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 1


def test_json_input_dict_output(schema, json_file_name):
    with open(json_file_name, 'r') as sf:
        p_dict_output = Parser(
            schema=schema,
            stop_on_error=-1,
            input_row_format='json',
            parsed_row_format='dict'
        )
        parsed_data = p_dict_output.parse(sf)
        assert isinstance(parsed_data, types.GeneratorType)
        parsed_lines = []
        for parsed_line in parsed_data:  # calling data parsing on file object
            assert isinstance(parsed_line, dict)
            assert len(parsed_line.keys()) == 8
            parsed_lines.append(parsed_line)
        assert len(parsed_lines) == 1


def test_dict_input_dict_output(schema, json_lol):
    p_dict_output = Parser(
        schema=schema,
        stop_on_error=-1,
        input_row_format='json',
        parsed_row_format='dict'
    )
    parsed_data = p_dict_output.parse(json_lol)
    assert isinstance(parsed_data, types.GeneratorType)
    parsed_lines = []
    for parsed_line in parsed_data:  # calling data parsing on file object
        assert isinstance(parsed_line, dict)
        assert len(parsed_line.keys()) == 8
        parsed_lines.append(parsed_line)
    assert len(parsed_lines) == 1


def test_json_input_wrong_output(schema, json_lol):
    with pytest.raises(UnexpectedSystemException):
        Parser(
            schema=schema,
            stop_on_error=-1,
            input_row_format='json',
            parsed_row_format='delimited'
        )
        Parser(
            schema=schema,
            stop_on_error=-1,
            input_row_format='json',
            parsed_row_format='fixed-width'
        )
        Parser(
            schema=schema,
            stop_on_error=-1,
            input_row_format='dict',
            parsed_row_format=''
        )
        p_json_output = Parser(
            schema=schema,
            stop_on_error=-1,
            input_row_format='json',
            parsed_row_format='json'
        )
        p_json_output.parse(json_lol)
