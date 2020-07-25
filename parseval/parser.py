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
        MinimumValueConstraintException
except ImportError:
    from exceptions import UnexpectedSystemException, \
        UnexpectedParsingException, \
        SchemaBuildException, \
        NullValueInNotNullFieldException, \
        ValidValueCheckException, \
        MaximumValueConstraintException, \
        MinimumValueConstraintException


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
                    if default_value:
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
            If set to True then empty string and None will be treated as valid value
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
    def __init__(self):
        super().__init__()


class NumericParser(FieldParser):
    def __init__(self):
        super().__init__()


class IntegerParser(FieldParser):
    def __init__(self):
        super().__init__()


class DateParser(FieldParser):
    def __init__(self):
        super().__init__()


class DatetimeParser(FieldParser):
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
            Format of the input data stream, simple delimited/fixed width line or json/dict
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
        if input_row_format not in ["delimited", "json"]:
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
                    pdata.append(self.parsed_row_sep.join(plist))
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
        ('C2', FieldParser().not_null('default')),
        ('C3', FieldParser(start=1, end=1).value_set(['a', 'b', 'A'])),
        ('C4', FieldParser(start=2, end=5).not_null('xnone')),
        ('C5', FieldParser(start=1, end=2).max_value('20')),
        ('C6', FieldParser(start=1, end=2).min_value('AB'))
    ]
    p = Parser(schema=schema)
    parsed_data = p.parse([
        '""|ABC|A|ogoodcbd|2000|ABC',
        '"DEF"||abc|||',
        '"DEF"||||1200|AbF'
    ])
    print(parsed_data)
