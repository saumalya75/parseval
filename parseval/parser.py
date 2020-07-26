import re
import sys
import typing
import functools
import traceback

try:
    from parseval.exceptions import UnexpectedSystemException, \
        UnexpectedParsingException, \
        SchemaBuildException, \
        NullValueInNotNullFieldException, \
        ValidValueCheckException, \
        MaximumValueConstraintException, \
        MinimumValueConstraintException, \
        RegexMatchException, \
        IntegerParsingException, \
        FloatParsingException
except ImportError:
    from exceptions import UnexpectedSystemException, \
        UnexpectedParsingException, \
        SchemaBuildException, \
        NullValueInNotNullFieldException, \
        ValidValueCheckException, \
        MaximumValueConstraintException, \
        MinimumValueConstraintException, \
        RegexMatchException, \
        IntegerParsingException, \
        FloatParsingException


class FieldParser:
    """
    Base class for all parsers apart from Constant.
    """

    def __init__(self,
                 start: int = 0,
                 end: int = 0,
                 quoted: int = 0
                 ):
        """
        Field parser constructor.
        :param quoted: int
            Quoted code. {0: Not quoted, 1: Double quoted, 2: Single Quoted}
        :param start:
            Use this parameter to specify starting position of the value in the provided data.
            Fixed width files can be parsed using this parameter along with `end` parameter.
            Using this parameter along with `end` parameter data snipping is also possible.
        :param end:
            Use this parameter to specify ending position of the value in the provided data.
            Fixed width files can be parsed using this parameter along with `start` parameter.
            Using this parameter along with `start` parameter data snipping is also possible.
        """
        self._nullable: bool = False
        self._funcs: typing.List = []
        if start and end:
            self.add_func(lambda s: s[start - 1:end])
        if quoted == 1:
            self.add_func(lambda s: s.lstrip('"').rstrip('"'))
        elif quoted == 2:
            self.add_func(lambda s: s.lstrip("'").rstrip("'"))

    def build(self):
        """
        Builder function to accumulate all closures that need to be applied on top of the data.
        :return:
            Master function to be applied on data
        """
        try:
            if self._funcs:
                return functools.reduce(lambda foo, bar: lambda s: bar(foo(s)), self._funcs)
            else:
                return lambda x: x
        except Exception as e:
            print('~' * 100)
            traceback.print_exc(file=sys.stdout)
            print('~' * 100)
            raise UnexpectedSystemException()

    def add_func(self, f: any):
        """
        Add closure to the list of closure.
        :param f: any
            Although this parameter is typed as any, but it accepts a closure
             and adds it to the list of closures for this object.
        :return: bool
            True
        """
        try:
            self._funcs.append(f)
        except Exception as e:
            print('~' * 100)
            traceback.print_exc(file=sys.stdout)
            print('~' * 100)
            raise UnexpectedSystemException()
        return True

    def not_null(self, default_value: any = None):
        """
        Building not null check closure.
        :param default_value: any
            Default value for a column which should be not null.
        :return: FieldParser
            self
        """

        def null_check(data: any):
            """
            Null Check closure.
            :param data: any
                Column data.
            :return: any
                Column value or default value
            """
            try:
                if not data:
                    if default_value is not None:
                        return default_value
                    else:
                        raise NullValueInNotNullFieldException()
                else:
                    return data
            except Exception as e:
                print('~' * 100)
                traceback.print_exc(file=sys.stdout)
                print('~' * 100)
                raise UnexpectedParsingException()

        self.add_func(null_check)
        return self

    def value_set(self, values: typing.List, nullable: bool = True):
        """
        Building valid value check closure.
        :param values: typing.List
            Set of valid values for this column.
        :param nullable: bool
            If set to `True` then empty string and None will be treated as valid value,
             along with the provided value list.
            By default, `True`
        :return: FieldParser
            self
        """
        if nullable:
            values.extend(['', None])

        def valid_value_check(data: any):
            """
            Valid value check closure.
            :param data: any
                Column data.
            :return: any
                Column value
            """
            try:
                if data not in values:
                    raise ValidValueCheckException("Provided value - '{}' is not part of valid value list - {}.".format(data, values))
                else:
                    return data
            except Exception as e:
                print('~' * 100)
                traceback.print_exc(file=sys.stdout)
                print('~' * 100)
                raise UnexpectedParsingException()

        self.add_func(valid_value_check)
        return self

    def max_value(self, val: any):
        """
        Building maximum value check closure.
        :param val: any
            Maximum allowed value for the column.
        :return: FieldParser
            self
        """
        def valid_value_check(data: any):
            """
            Maximum value check closure.
            :param data: any
                Column data.
            :return: any
                Column value
            """
            try:
                if data:
                    if data > val:
                        raise MaximumValueConstraintException(
                            "Provided value - '{}' is higher than maximum allowed value - {}.".format(data, val)
                        )
                return data
            except Exception as e:
                print('~' * 100)
                traceback.print_exc(file=sys.stdout)
                print('~' * 100)
                raise UnexpectedParsingException()

        self.add_func(valid_value_check)
        return self

    def min_value(self, val: any):
        """
        Building minimum value check closure.
        :param val: any
            Maximum allowed value for the column.
        :return: FieldParser
            self
        """
        def valid_value_check(data: any):
            """
            Minimum value check closure.
            :param data: any
                Column data.
            :return: any
                Column value
            """
            try:
                if data:
                    if data < val:
                        raise MinimumValueConstraintException(
                            "Provided value - '{}' is lower than minimum allowed value - {}.".format(data, val)
                        )
                return data
            except Exception as e:
                print('~' * 100)
                traceback.print_exc(file=sys.stdout)
                print('~' * 100)
                raise UnexpectedParsingException()

        self.add_func(valid_value_check)
        return self


class StringParser(FieldParser):
    """
    Parser class for string columns.
    Inherits from `FieldParser` class.
    String specific features:
        - `regex_match`
        - `change_case`
    Overridden features:
        - not_null (to handle prolonged white spaces)
    """
    def __init__(self, *args, **kwargs):
        """
            Handing over object initialization to parent class.
        """
        super().__init__(*args, **kwargs)

    def regex_match(self, pattern: str, nullable: bool = True):
        """
        Building regex match closure.
        :param pattern: str
            Patter to match with the data.
        :param nullable: bool
            If set to `True` then empty string and None will be treated as valid value,
             along with the values that matches provided `pattern`.
            By default, `True`
        :return: StringParser
            any
        """
        def pattern_match(data: str):
            """
            Regex match closure.
            :param data: str
                Column data.
            :return: str
                Parsed column value
            """
            try:
                if not re.match(pattern, data):
                    if not (not data and nullable):
                        print(data)
                        raise RegexMatchException(
                            "Data - '{}' does not match with expected pattern - {}.".format(data, pattern)
                        )
                return data
            except Exception as e:
                print('~' * 100)
                traceback.print_exc(file=sys.stdout)
                print('~' * 100)
                raise UnexpectedParsingException()

        self.add_func(pattern_match)
        return self

    def change_case(self, case_type: str = 'S'):
        """
        Building change case closure.
        :param case_type: str
            Target case: {'U'/'u': UPPERCASE, 'L'/'l': lowercase, 'S'/'s': Sentence Case}
        :return: StringParser
            self
        """
        def change_case(data: str):
            """
            Change case closure.
            :param data: str
                Column data.
            :return: str
                Parsed Column value
            """
            try:
                if case_type.upper() == 'S':
                    return data.capitalize()
                elif case_type.upper() == 'L':
                    return data.lower()
                elif case_type.upper() == 'U':
                    return data.upper()
                else:
                    return data
            except Exception as e:
                print('~' * 100)
                traceback.print_exc(file=sys.stdout)
                print('~' * 100)
                raise UnexpectedParsingException()

        self.add_func(change_case)
        return self

    def not_null(self, default_value: any = None, allow_white_space: bool = False):
        """
        Building not null check closure.
        :param default_value: any
            Default value for a column which should be not null.
        :param allow_white_space: bool
            Decides whether only white spaces should be treated as null or not.
            If white spacesa re allowed, then `not_null('   ')` will return True.
            By default it is set to `False`.
        :return: StringParser
            self
        """

        def null_check(data: any):
            """
            Null Check closure.
            :param data: any
                Column data.
            :return: any
                Column value or default value
            """
            try:
                data = data if allow_white_space else data.strip()
                if not data:
                    if default_value is not None:
                        return default_value
                    else:
                        raise NullValueInNotNullFieldException()
                else:
                    return data
            except Exception as e:
                print('~' * 100)
                traceback.print_exc(file=sys.stdout)
                print('~' * 100)
                raise UnexpectedParsingException()

        self.add_func(null_check)
        return self


class FloatParser(FieldParser):
    """
    Parser class for float columns.
    Inherits from `FieldParser` class.
    Float specific features:
        - float_casting
    Overridden features:
        None
    """
    def __init__(self, *args, **kwargs):
        """
            Handing over object initialization to parent class.
        """
        super().__init__(*args, **kwargs)

        def float_casting(data: str):
            """
            Closure to cast the data to float
            :param data: str
                Column value
            :return: int
                Parsed column value
            """
            try:
                if data:
                    return float(data)
                else:
                    return data
            except Exception:
                print('~' * 100)
                traceback.print_exc(file=sys.stdout)
                print('~' * 100)
                raise FloatParsingException("Column value - {} could not be casted into Float.".format(data))

        self.add_func(float_casting)


class IntegerParser(FieldParser):
    """
    Parser class for integer columns.
    Inherits from `FieldParser` class.
    Integer specific features:
        - integer_casting
    Overridden features:
        None
    """
    def __init__(self, *args, **kwargs):
        """
            Handing over object initialization to parent class.
        """
        super().__init__(*args, **kwargs)

        def integer_casting(data: str):
            """
            Closure to cast the data to integer
            :param data: str
                Column value
            :return: int
                Parsed column value
            """
            try:
                if data:
                    return int(data)
                else:
                    return data
            except Exception:
                print('~' * 100)
                traceback.print_exc(file=sys.stdout)
                print('~' * 100)
                raise IntegerParsingException("Column value - {} could not be casted into Integer.".format(data))

        self.add_func(integer_casting)


class DatetimeParser(FieldParser):
    """
    Parser class for date/datetime columns.
    Inherits from `FieldParser` class.
    Date/Datetime specific features:
        Formatting dates/datetimes
    Overridden features:
        None
    """
    def __init__(self):
        super().__init__()


class Parser:
    """
    `Parser` class is the entry point for the utility.
    User must create an object to this class to build the schema and use the parsers.
    """

    def __init__(self,
                 schema: typing.List[typing.Tuple] = [],
                 input_row_format: str = "delimited",
                 input_row_sep: str = "|",
                 parsed_row_format: str = "delimited",
                 parsed_row_sep: str = None):
        """
        :param input_row_format: str
            Format of the input data stream, simple delimited/fixed-width line or json/dict
        :param input_row_sep: str
            If `row_format` is declared as "delimited" while creating perser object,
            then use `sep` to specify column delimiter.
        :param schema: typing.List[typing.Tuple]
            structure of the data, format should be [('column name', field parser object), (...), ...]
        :param parsed_row_format: str
            Format of output rows - "delimited"/"json". Note: "fixed-width" output is not supported.
        :param parsed_row_sep: str
            If `parsed_row_format` is declared as "delimited" while creating perser object,
            then use `parsed_sep` to specify column delimiter of output records.
        """
        if input_row_format not in ["delimited", "fixed-width", "json"]:
            raise Exception("Only list of lines and list of jsons are supported a input.")
        self.input_row_format: str = input_row_format
        self.input_row_sep: str = input_row_sep
        self.schema: typing.List[typing.Tuple] = schema
        self.parsed_row_format: str = parsed_row_format
        if self.parsed_row_format == "delimited":
            if not parsed_row_sep:
                if self.input_row_sep:
                    self.parsed_row_sep = self.input_row_sep
                else:
                    raise Exception(
                        "`parsed_sep` keyword argment is mandatory while `parsed_row_format` argumet is provided as 'delimited'.")
            else:
                self.parsed_row_sep: str = parsed_row_sep
        self._parser_funcs: typing.Dict = {}

    def _build(self):
        """
        To build/compile the schema, this API is used. A schema can be used for parsing only after it is built
        Builds the list of parsable functions.

        :return: bool
            True
        """
        for k, v in self.schema:
            self._parser_funcs[k] = v.build()
        return True

    def parse(self, data: typing.List[typing.Union[str, typing.Dict]]):
        """
        :param data: typing.List[typing.Union[str, typing.Dict]]
            Takes input data as list of string or list of json
        :return: typing.List[typing.Union[str, typing.Dict]]
            Parsed data
        """
        try:
            self._build()
        except Exception:
            print('~' * 100)
            traceback.print_exc(file=sys.stdout)
            print('~' * 100)
            raise SchemaBuildException()

        if self.input_row_format == "delimited":
            pdata: typing.List[typing.Union[str, typing.Dict]] = []
            for d in data:
                dlist: typing.List = d.split(self.input_row_sep)
                plist: typing.List = []
                pdict: typing.Dict = {}
                for i, col in enumerate(self.schema):
                    pd = self._parser_funcs[col[0]](dlist[i])
                    if self.parsed_row_format == "delimited":
                        plist.append(pd)
                    else:
                        pdict[col[0]] = pd
                if self.parsed_row_format == "delimited":
                    pdata.append(self.parsed_row_sep.join((str(e) for e in plist)))
                else:
                    pdata.append(pdict)
        elif self.input_row_format == "fixed-width":
            pdata: typing.List[typing.Union[str, typing.Dict]] = []
            for d in data:
                plist: typing.List = []
                pdict: typing.Dict = {}
                for i, col in enumerate(self.schema):
                    pd = self._parser_funcs[col[0]](d)
                    if self.parsed_row_format == "delimited":
                        plist.append(pd)
                    else:
                        pdict[col[0]] = pd
                if self.parsed_row_format == "delimited":
                    pdata.append(self.parsed_row_sep.join((str(e) for e in plist)))
                else:
                    pdata.append(pdict)
        else:
            pdata: typing.List = []
            for d in data:
                plist: typing.List = []
                pdict: typing.Dict = {}
                for col, _ in self.schema:
                    pd = self._parser_funcs[col](d[col])
                    if self.parsed_row_format == "delimited":
                        plist.append(pd)
                    else:
                        pdict[col[0]] = pd
                if self.parsed_row_format == "delimited":
                    pdata.append(self.parsed_row_sep.join(plist))
                else:
                    pdata.append(pdict)
        return pdata


if __name__ == "__main__":
    schema = [
        ('C1', FieldParser(quoted=1)),
        ('C2', StringParser().regex_match(r'\w+_\d{4}-\d{2}-\d{2}').change_case('u')),
        ('C3', FieldParser(start=1, end=1).value_set(['a', 'b', 'A'])),
        ('C4', FieldParser(start=2, end=5).not_null('xnone')),
        ('C5', IntegerParser().max_value(2000).not_null(default_value=0)),
        ('C6', FloatParser().min_value(10.0).not_null(0))
    ]
    p = Parser(schema=schema)
    parsed_data = p.parse([
        '""|Trig_2020-23-12|A|ogoodcbd|2000|21.0934',
        '"DEF"||abc|||',
        '"DEF"|Manual_2020-23-12|||1200|11'
    ])
    print(parsed_data)
    fw_schema = [
        ('C1', FieldParser(1, 2)),
        ('C2', StringParser(3, 5).change_case('U').not_null('nan', allow_white_space=True)),
        ('C3', FieldParser(6, 6).value_set(['M', 'F'])),
        ('C4', FieldParser(7, 11).not_null('dummy')),
        ('C5', FieldParser(7, 11)),
        ('C6', IntegerParser(12, 13).max_value(20)),
        ('C7', FloatParser(14, 17).min_value(10.0))
    ]
    p = Parser(schema=fw_schema, input_row_format='fixed-width', parsed_row_format='json')
    parsed_data = p.parse([
        'd0sauMvalue191000',
        'd0pouM     2090.03'
    ])
    print(parsed_data)

