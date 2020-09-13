import json
import re
import typing
import datetime
import functools
import logging

try:
    from parseval.exceptions import (
        UnexpectedSystemException,
        UnexpectedParsingException,
        UnsupportedDatatypeException,
        SchemaBuildException,
        NullValueInNotNullFieldException,
        ValidValueCheckException,
        MaximumValueConstraintException,
        MinimumValueConstraintException,
        RegexMatchException,
        StringParsingException,
        IntegerParsingException,
        FloatParsingException,
        BooleanParsingException,
        DateTimeParsingException
    )
except ImportError:
    from exceptions import (
        UnexpectedSystemException,
        UnexpectedParsingException,
        UnsupportedDatatypeException,
        SchemaBuildException,
        NullValueInNotNullFieldException,
        ValidValueCheckException,
        MaximumValueConstraintException,
        MinimumValueConstraintException,
        RegexMatchException,
        StringParsingException,
        IntegerParsingException,
        FloatParsingException,
        BooleanParsingException,
        DateTimeParsingException
    )

logging.basicConfig(format='%(levelname)s:%(asctime)s:: %(message)s', level=logging.DEBUG)


class FieldParser:
    """
    Base class for all parsers apart from Constant.
    """
    TYPE = str

    def __init__(self,
                 start: int = 0,
                 end: int = 0,
                 quoted: int = 0,
                 enforce_type: bool = True
                 ):
        """
        Field parser constructor.
        :param start:
            Use this parameter to specify starting position of the value in the provided data.
            Fixed width files can be parsed using this parameter along with `end` parameter.
            Using this parameter along with `end` parameter data snipping is also possible.
        :param end:
            Use this parameter to specify ending position of the value in the provided data.
            Fixed width files can be parsed using this parameter along with `start` parameter.
            Using this parameter along with `start` parameter data snipping is also possible.
        :param quoted: int
            Quoted code. {0: Not quoted, 1: Double quoted, 2: Single Quoted}
        :param enforce_type:
            If set to True, the type return value of this parser will be the type of parser,
            e.g. `str` for `StringParser`, `datetime.datetiem` for `DatetiemParser` etc.
            If set to False, type conversion will not happen, whatever type vale was provided,
            will be returned.
            By default this parameter is set to True.
        """
        self._nullable: bool = False
        self._funcs: typing.List = []
        self.enforce_type: bool = enforce_type

        if start and end:
            self.add_func(lambda s: str(s)[start - 1:end])
        if quoted == 1:
            self.add_func(lambda s: s.lstrip('"').rstrip('"'))
        elif quoted == 2:
            self.add_func(lambda s: s.lstrip("'").rstrip("'"))

        def type_casting(data: any):
            """
            Closure to cast the data to respective type
            :param data: any
                Column value
            :return: any
                Parsed column value
            """
            try:
                if data:
                    if self.TYPE and self.TYPE != bool:
                        if self.enforce_type:
                            data = self.TYPE(data)
                        else:
                            self.TYPE(data)
                return data
            except Exception:
                logging.error('~' * 100)
                logging.exception("Datatype casting exception:")
                logging.error('~' * 100)
                raise UnexpectedParsingException("Column value - {} could not be casted into {}.".format(data, self.TYPE))

        self.add_func(type_casting)

    def build(self):
        """
        Builder function to accumulate all closures that need to be applied on top of the data.
        :return:
            Master function to be applied on data
        """
        try:
            if self._funcs:
                return functools.reduce(lambda parser1, parser2: lambda s: parser2(parser1(s)), self._funcs)
            else:
                return lambda x: x
        except Exception as e:
            logging.error('~' * 100)
            logging.exception("Parser functions building exception:")
            logging.error('~' * 100)
            raise UnexpectedSystemException()

    def add_func(self, f: any):
        """
        Add closure to the list of closure.
        :param f: any
            Although this parameter is typed as any, but it accepts a closure
             and adds it to the list of closures for this object.
        :return: FieldParser
            self
        """
        try:
            self._funcs.append(f)
        except Exception as e:
            logging.error('~' * 100)
            logging.exception("Custom function addition exception:")
            logging.error('~' * 100)
            raise UnexpectedSystemException()
        return self

    def not_null(self, default_value: any = None):
        """
        Building not null check closure.
        :param default_value: any
            Default value for a column which should be not null.
        :return: FieldParser
            self
        """
        if default_value and type(default_value) != self.TYPE:
            raise UnsupportedDatatypeException(f"{type(default_value)} type data can not be used as default value of"
                                               f" {self.TYPE} type column. Please provide default value of"
                                               f" {self.TYPE} type.")

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
                        if self.enforce_type:
                            return self.TYPE(default_value)
                        else:
                            return default_value
                    else:
                        raise NullValueInNotNullFieldException()
                else:
                    return data
            except Exception as e:
                logging.error('~' * 100)
                logging.exception("Not null enforcement exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(null_check)

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
        dtypes = set(type(v) for v in values)
        if len(dtypes) > 1 or list(dtypes)[0] != self.TYPE:
            raise UnsupportedDatatypeException(f"Provided valid values are not fit for"
                                               f" {self.TYPE} type column. Please provide valid values of"
                                               f" {self.TYPE} type.")
        if self.enforce_type:
            values = [self.TYPE(value) for value in values]

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
                    raise ValidValueCheckException(
                        "Provided value - '{}' is not part of valid value list - {}.".format(data, values))
                else:
                    return data
            except Exception as e:
                logging.error('~' * 100)
                logging.exception("Value set check exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(valid_value_check)

    def max_value(self, value: any):
        """
        Building maximum value check closure.
        :param value: any
            Maximum allowed value for the column.
        :return: FieldParser
            self
        """
        if type(value) != self.TYPE:
            raise UnsupportedDatatypeException(f"{type(value)} type data can not be used as maximum value of"
                                               f" {self.TYPE} type column. Please provide maximum value of"
                                               f" {self.TYPE} type.")
        if self.enforce_type:
            value = self.TYPE(value)

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
                    if data > value:
                        raise MaximumValueConstraintException(
                            "Provided value - '{}' is higher than maximum allowed value - {}.".format(data, value)
                        )
                return data
            except Exception as e:
                logging.error('~' * 100)
                logging.exception("Max value check exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(valid_value_check)

    def min_value(self, value: any):
        """
        Building minimum value check closure.
        :param value: any
            Maximum allowed value for the column.
        :return: FieldParser
            self
        """
        if type(value) != self.TYPE:
            raise UnsupportedDatatypeException(f"{type(value)} type data can not be used as minimum value of"
                                               f" {self.TYPE} type column. Please provide minimum value of"
                                               f" {self.TYPE} type.")

        if self.enforce_type:
            value = self.TYPE(value)

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
                    if data < value:
                        raise MinimumValueConstraintException(
                            "Provided value - '{}' is lower than minimum allowed value - {}.".format(data, value)
                        )
                return data
            except Exception as e:
                logging.error('\n')
                logging.error('~' * 100)
                logging.exception("Min value check exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(valid_value_check)

    def range(self, lower_bound: any, upper_bound: any):
        """
        Building range check API, max_val and min_val APIs will be used to achieve this.
        :param lower_bound: any
            Minimum allowed value for the column.
        :param upper_bound: any
            Maximum allowed value for the column.
        :return: FieldParser
            self
        """
        self.min_value(lower_bound)
        self.max_value(upper_bound)
        return self

    def __call__(self):
        return self.build()


class StringParser(FieldParser):
    """
    Parser class for string columns.
    Inherits from `FieldParser` class.
    String specific features:
        - regex_match
        - change_case
    Overridden features:
        - not_null (to handle prolonged white spaces)
    """
    TYPE = str

    def __init__(self, *args, **kwargs):
        """
            Handing over object initialization to parent class.
        """
        super().__init__(*args, **kwargs)

        def string_casting(data: any):
            """
            Closure to cast the data to string
            :param data: any
                Column value
            :return: str
                Parsed column value
            """
            try:
                if data:
                    return str(data)
                else:
                    return data
            except Exception:
                logging.error('\n')
                logging.error('~' * 100)
                logging.exception("String casting exception:")
                logging.error('~' * 100)
                raise StringParsingException("Column value - {} could not be casted into String.".format(data))

        self.add_func(string_casting)

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
                        raise RegexMatchException(
                            "Data - '{}' does not match with expected pattern - {}.".format(data, pattern)
                        )
                return data
            except Exception as e:
                logging.error('\n')
                logging.error('~' * 100)
                logging.exception("Pattern match exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(pattern_match)

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
                logging.error('\n')
                logging.error('~' * 100)
                logging.exception("Case change exception:")
                logging.error('~' * 100)
                raise UnexpectedParsingException()

        return self.add_func(change_case)

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
                if data is not None:
                    data = data if allow_white_space else type(data)(str(data).strip())
                if not data:
                    if allow_white_space and data is not None:
                        return data
                    elif default_value is not None:
                        if self.enforce_type:
                            return str(default_value)
                        else:
                            return default_value
                    else:
                        raise NullValueInNotNullFieldException()
                else:
                    return data
            except Exception as e:
                logging.error('\n')
                logging.error('~' * 100)
                logging.exception("Null check exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(null_check)


class FloatParser(FieldParser):
    """
    Parser class for float columns.
    Inherits from `FieldParser` class.
    Float specific features:
        None
    Overridden features:
        None
    """
    TYPE = float

    def __init__(self, *args, **kwargs):
        """
            Handing over object initialization to parent class.
        """
        super().__init__(*args, **kwargs)


class IntegerParser(FieldParser):
    """
    Parser class for integer columns.
    Inherits from `FieldParser` class.
    Integer specific features:
        None
    Overridden features:
        None
    """
    TYPE = int

    def __init__(self, *args, **kwargs):
        """
            Handing over object initialization to parent class.
        """
        super().__init__(*args, **kwargs)


class BooleanParser(FieldParser):
    """
    Parser class for boolean columns.
    Inherits from `FieldParser` class.
    Integer specific features:
        None
    Overridden features:
        None
    """
    TYPE = bool

    def __init__(self, *args, **kwargs):
        """
            Handing over object initialization to parent class.
        """
        super().__init__(*args, **kwargs)

        def boolean_casting(data: any):
            """
            Closure to cast the data to boolean
            :param data: any
                Column value
            :return: any
                Parsed column value
            """
            try:
                if data or data == 0:
                    if type(data) == str and data.strip():
                        if re.match(r'\b[Tt][Rr][Uu][Ee]\b', data.strip()) \
                                or re.match(r'\b[TtyY]\b', data.strip()) \
                                or re.match(r'\b[Yy][eE][sS]\b', data.strip()) \
                                or re.match(r'\-?\d+(\.\d+)?', data.strip()):
                            bool_data = True
                        elif re.match(r'\b[fF][aA][lL][sS][Ee]\b', data.strip()) \
                                or re.match(r'\b[FfnN]\b', data.strip()) \
                                or re.match(r'\b[Nn][Oo]\b', data.strip()) \
                                or re.match(r'0+(\.0+)?', data.strip()):
                            bool_data = False
                        else:
                            raise BooleanParsingException("'{}' is not a valid value for boolean type column."\
                                                          .format(data))
                    else:
                        bool_data = bool(data)
                    if self.enforce_type:
                        data = bool_data
                    else:
                        self.TYPE(data)
                return data
            except Exception as e:
                logging.error('\n')
                logging.error('~' * 100)
                logging.exception("Boolean casting exception:")
                logging.error('~' * 100)
                raise e

        self.add_func(boolean_casting)


class DatetimeParser(FieldParser):
    """
    Parser class for date/datetime columns.
    Inherits from `FieldParser` class.
    Date/Datetime specific features:
        - Format checking
        - convert
    Overridden features:
        - not null check
        - maximum value check
        - minimum value check
    """
    TYPE = False

    def __init__(self,
                 start: int = 0,
                 end: int = 0,
                 formats: typing.List = ['%Y%m%d', '%Y%m%d%H%M%S'],
                 quoted: int = 0,
                 enforce_type: bool = True
                 ):
        """
        Initiating DateTime Parser object with a little help of parents.
        :param start:
            Use this parameter to specify starting position of the value in the provided data.
            Fixed width files can be parsed using this parameter along with `end` parameter.
            Using this parameter along with `end` parameter data snipping is also possible.
        :param end:
            Use this parameter to specify ending position of the value in the provided data.
            Fixed width files can be parsed using this parameter along with `start` parameter.
            Using this parameter along with `start` parameter data snipping is also possible.
        :param formats:
            If input data is of type `str` then this parameter accepts the allowed formats list.
            If inout data is of type `datetime.datetime` then this parameter is obsolete.
        :param quoted: int
            Quoted code. {0: Not quoted, 1: Double quoted, 2: Single Quoted}
        :param enforce_type:
            If set to True, the type return value of this parser will be the type of parser,
            e.g. `str` for `StringParser`, `datetime.datetiem` for `DatetiemParser` etc.
            If set to False, type conversion will not happen, whatever type vale was provided,
            will be returned.
            By default this parameter is set to True.
        """
        self._formats = formats
        super().__init__(start=start, end=end, quoted=quoted, enforce_type=False)
        self.enforce_type: bool = enforce_type

        def format_checker(data: typing.Union[str, datetime.datetime]):
            """
            Closure to read and format date/datetime data. This closure validates the data format,
            as well as returns a datetime object. Please use `convert` closure to reformat data,
            or to store it in string format.
            :param data: typing.Union[str, datetime.datetime]
                Column value
            :return: str
                Column value
            """
            if not data or type(data) == datetime.datetime:
                return data
            for f in self._formats:
                try:
                    if self.enforce_type:
                        data = datetime.datetime.strptime(str(data), f)
                        break
                    else:
                        datetime.datetime.strptime(str(data), f)
                        break
                except:
                    pass
            else:
                raise DateTimeParsingException("Column data - '{}' is not in any of the following formats - {}."
                                               .format(data, self._formats)
                                               )
            return data

        self.add_func(format_checker)

    def not_null(self,
                 default_value: typing.Union[str, datetime.datetime] = None,
                 format: str = '%Y%m%d%H%M%S'):
        """
        Building not null check closure.
        :param default_value: typing.Union[str, datetime.datetime]
            Default value for a column which should be not null.
        :param format: str
            Format in which the default value is provided.
        :return: DatetimeParser
            self
        """
        if default_value:
            if type(default_value) != datetime.datetime:
                try:
                    if self.enforce_type:
                        default_value = datetime.datetime.strptime(str(default_value), format)
                    else:
                        datetime.datetime.strptime(str(default_value), format)
                except Exception:
                    logging.error('\n')
                    logging.error('~' * 100)
                    logging.exception("Null check exception:")
                    logging.error('~' * 100)
                    raise UnexpectedParsingException("Provided default value - '{}' is not of '{}' format."
                                                     .format(default_value, format)
                                                     )
            self._formats += [format]

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
                logging.error('\n')
                logging.error('~' * 100)
                logging.exception("Null check exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(null_check)

    def convert(self, format: str = '%Y%m%d%H%M%S'):
        """
        Closure to convert datetime/date column to desired string format
        :param format: str
            Column value
        :return: DatetimeParser
            self
        """
        self._formats += [format]

        def str_from_date(data: any):
            """
            Format conversion closure.
            :param data: str
                Column data.
            :return: any
                Re-formatted column value
            """
            try:
                if not data:
                    return data
                if type(data) != datetime.datetime:
                    for f in self._formats:
                        try:
                            data = datetime.datetime.strptime(str(data), f)
                            break
                        except:
                            pass
                    else:
                        raise DateTimeParsingException("Column data - '{}' is not in any of the following formats - {}."
                                                       .format(data, self._formats)
                                                       )
                return datetime.datetime.strftime(data, format)
            except Exception as e:
                logging.error('\n')
                logging.error('~' * 100)
                logging.exception("Date format conversion exception:")
                logging.error('~' * 100)
                DateTimeParsingException("It was not possible to convert column data - '{}' to '{}' format."
                                         .format(data, format)
                                         )

        return self.add_func(str_from_date)

    def max_value(self,
                  value: typing.Union[str, datetime.datetime],
                  format: str = '%Y%m%d%H%M%S'):
        """
        Building maximum value check closure.
        :param value: typing.Union[str, datetime.datetime]
            Maximum allowed value for a column.
        :param format: str
            Format in which the default value is provided.
        :return: DatetimeParser
            self
        """
        if type(value) != datetime.datetime:
            try:
                max_val = datetime.datetime.strptime(str(value), format)
            except Exception:
                logging.error('~' * 100)
                logging.exception("Max value check exception:")
                logging.error('~' * 100)
                raise UnexpectedParsingException("Provided maximum allowed value - '{}' is not of '{}' format."
                                                 .format(value, format)
                                                 )
        else:
            max_val = value

        def valid_value_check(data: str):
            """
            Maximum value check closure.
            :param data: str
                Column data.
            :return: any
                Checked column value
            """
            try:
                if not data:
                    return data
                if type(data) != datetime.datetime:
                    for f in self._formats:
                        try:
                            pd = datetime.datetime.strptime(str(data), f)
                            break
                        except Exception:
                            pass
                    else:
                        raise DateTimeParsingException("Column data - '{}' is not in any of the following formats - {}."
                                                       .format(data, self._formats)
                                                       )
                else:
                    pd = data

                if pd > max_val:
                    raise MaximumValueConstraintException(
                        "Column value - '{}' is higher than maximum allowed value - {}.".format(data, value)
                    )
                return data
            except Exception as e:
                logging.error('~' * 100)
                logging.exception("Max value check exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(valid_value_check)

    def min_value(self,
                  value: typing.Union[str, datetime.datetime],
                  format: str = '%Y%m%d%H%M%S'):
        """
        Building minimum value check closure.
        :param value: typing.Union[str, datetime.datetime]
            Minimum allowed value for a column.
        :param format: str
            Format in which the default value is provided.
        :return: DatetimeParser
            self
        """
        if type(value) != datetime.datetime:
            try:
                min_val = datetime.datetime.strptime(str(value), format)
            except Exception:
                logging.error('~' * 100)
                logging.exception("Min value check exception:")
                logging.error('~' * 100)
                raise UnexpectedParsingException("Provided minimum allowed value - '{}' is not of '{}' format."
                                                 .format(value, format)
                                                 )
        else:
            min_val = value

        def valid_value_check(data: str):
            """
            Minimum value check closure.
            :param data: str
                Column data.
            :return: any
                Checked column value
            """
            try:
                if not data:
                    return data
                if type(data) != datetime.datetime:
                    for f in self._formats:
                        try:
                            pd = datetime.datetime.strptime(str(data), f)
                            break
                        except Exception:
                            pass
                    else:
                        raise DateTimeParsingException("Column data - '{}' is not in any of the following formats - {}."
                                                       .format(data, self._formats)
                                                       )
                else:
                    pd = data

                if pd < min_val:
                    raise MinimumValueConstraintException(
                        "Column value - '{}' is lower than minimum allowed value - {}.".format(data, value)
                    )
                return data
            except Exception as e:
                logging.error('~' * 100)
                logging.exception("Min value check exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(valid_value_check)

    def range(self,
              lower_bound: typing.Union[str, datetime.datetime],
              upper_bound: typing.Union[str, datetime.datetime],
              format: str = '%Y%m%d%H%M%S'
              ):
        """
        Building range check API, max_val and min_val APIs will be used to achieve this.
        :param lower_bound: typing.Union[str, datetime.datetime]
            Minimum allowed value for the column.
        :param upper_bound: typing.Union[str, datetime.datetime]
            Maximum allowed value for the column.
        :param format: str
            Format in which the default value is provided.
        :return: FieldParser
            self
        """
        self.min_value(lower_bound, format)
        self.max_value(upper_bound, format)
        return self

    def value_set(self,
                  values: typing.List[typing.Union[str, datetime.datetime]],
                  format: str = '%Y%m%d%H%M%S',
                  nullable: bool = True
                  ):
        """
        Building valid value check closure.
        :param values: typing.List[typing.Union[str, datetime.datetime]]
            Set of valid values for this column.
        :param nullable: bool
            If set to `True` then empty string and None will be treated as valid value,
             along with the provided value list.
            By default, `True`
        :param format: str
            Format in which the allowed values are provided.
        :return: FieldParser
            self
        """
        valid_values = []
        if values:
            for value in values:
                if type(value) != datetime.datetime:
                    try:
                        valid_values.append(datetime.datetime.strptime(str(value), format))
                    except Exception:
                        logging.error('~' * 100)
                        logging.exception("Value set check exception:")
                        logging.error('~' * 100)
                        raise UnexpectedParsingException("Provided allowed value - '{}' is not of '{}' format."
                                                         .format(value, format)
                                                         )
                else:
                    valid_values.append(value)

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
                if not data:
                    return data
                if type(data) != datetime.datetime:
                    for f in self._formats:
                        try:
                            pd = datetime.datetime.strptime(str(data), f)
                            break
                        except:
                            pass
                    else:
                        raise DateTimeParsingException("Column data - '{}' is not in any of the following formats - {}."
                                                       .format(data, self._formats)
                                                       )
                else:
                    pd = data
                if pd not in valid_values:
                    raise ValidValueCheckException(
                        "Provided value - '{}' is not part of valid value list - {}.".format(data, values))
                else:
                    return data
            except Exception as e:
                logging.error('~' * 100)
                logging.exception("Value set check exception:")
                logging.error('~' * 100)
                raise e

        return self.add_func(valid_value_check)


class ConstantParser(FieldParser):
    """
    Parser class for hard coded columns.
    Inherits from `FieldParser` class.
    """

    def __init__(self, value: str):
        """
            Initializing `ConstantParser` with hard coded value.
            It will always return the same value.
        """
        super().__init__()
        self.add_func(lambda x: value)


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
                 parsed_row_sep: str = None,
                 stop_on_error: int = 0):
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
        :param stop_on_error: int
            When `stop_on_error` value is set to **0**, the process will stop on encountering an validation error.
            When `stop_on_error` value is set to `any negative number`, the process will skip all erroneous rows
            and return only valid rows,
            When `stop_on_error` value is set to `any specific positive number`, the process will allow those many
            erroneous rows, if erroneous rows exceeds that number, the process will fail..
        """
        if input_row_format not in ["delimited", "fixed-width", "json"]:
            raise Exception("Only list of lines and list of jsons are supported a input.")
        self.input_row_format: str = input_row_format
        self.input_row_sep: str = input_row_sep
        self.schema: typing.List[typing.Tuple] = schema
        self.parsed_row_format: str = parsed_row_format
        if self.parsed_row_format not in ["delimited", "fixed-width", "json", "dict"]:
            raise UnexpectedSystemException(
                "Unsupported output format. Allowed formats are 'delimited', 'fixed-width' (available only for 'fixed-width' formatted input), 'json' (only available for json formatted input) and 'dict'."
            )
        if self.parsed_row_format == "delimited":
            if not parsed_row_sep:
                if self.input_row_sep:
                    self.parsed_row_sep = self.input_row_sep
                else:
                    raise UnexpectedSystemException(
                        "`parsed_sep` keyword argument is mandatory while `parsed_row_format` argumet is provided as 'delimited'."
                    )
            else:
                self.parsed_row_sep: str = parsed_row_sep
        if self.parsed_row_format == "fixed-width" and self.input_row_format != "fixed-width":
            raise UnexpectedSystemException(
                "`fixed-width` formatted output is only supported for `fixed-width` formatted input."
            )
        if self.input_row_format == "json" and self.parsed_row_format not in ["json", "dict"]:
            raise UnexpectedSystemException(
                "Only `json` and `dict` formatted output are supported for `jaon` formatted input."
            )
        if self.parsed_row_format == "json" and self.input_row_format != "json":
            raise UnexpectedSystemException(
                "Only `json` formatted input can be converted to `jaon` formatted output."
            )
        self.stop_on_error = stop_on_error
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

    def parse(self, data: typing.Union[typing.List[typing.Union[str, typing.Dict]], typing.TextIO]):
        """
        :param data: typing.List[typing.Union[str, typing.Dict, typing.IO]]
            Takes input data as list of string or list of json
        :return(yield): typing.Union[str, typing.Dict]
            Yields parsed line one be one
        """
        try:
            self._build()
        except Exception:
            logging.error('~' * 100)
            logging.exception("Parser function builder exception:")
            logging.error('~' * 100)
            raise SchemaBuildException()
        if self.input_row_format == "delimited":
            line_number = 0
            errornous_line_count = 0
            for d in data:
                try:
                    dlist: typing.List = d.split(self.input_row_sep)
                    if len(dlist) > len(self.schema):
                        raise UnexpectedParsingException(
                            "Number of columns in line - {} is higher that number of declared columns in schema.".format(
                                line_number + 1
                            )
                        )
                    plist: typing.List = []
                    pdict: typing.Dict = {}
                    for i, col in enumerate(self.schema):
                        try:
                            pd = self._parser_funcs[col[0]](dlist[i])
                        except:
                            logging.error("<" * 50, end='')
                            logging.error(">" * 50)
                            logging.error('LINE NUMBER: {}'.format(
                                line_number + 1
                            ))
                            logging.error('COLUMN NAME: {}'.format(
                                col[0]
                            ))
                            logging.error("<" * 50, end='')
                            logging.error(">" * 50)
                            raise
                        if self.parsed_row_format == "delimited":
                            plist.append(pd)
                        else:
                            pdict[col[0]] = pd
                    if self.parsed_row_format == "delimited":
                        yield self.parsed_row_sep.join((str(e) for e in plist))
                    else:
                        yield pdict
                    line_number += 1
                except Exception as e:
                    if self.stop_on_error < 0 or errornous_line_count < self.stop_on_error:
                        logging.error(str(e))
                        logging.error("DATA >>> ")
                        logging.error(d)
                        logging.error("CONTINUING TO PARSE DATA BECAUSE STOP_ON_ERROR CONDITION NOT MET YET!")
                        errornous_line_count += 1
                    else:
                        raise e
        elif self.input_row_format == "fixed-width":
            line_number = 0
            errornous_line_count = 0
            for d in data:
                try:
                    plist: typing.List = []
                    pdict: typing.Dict = {}
                    for i, col in enumerate(self.schema):
                        try:
                            pd = self._parser_funcs[col[0]](d)
                        except:
                            logging.error("<" * 50, end='')
                            logging.error(">" * 50)
                            logging.error('LINE NUMBER: {}'.format(
                                line_number + 1
                            ))
                            logging.error('COLUMN NAME: {}'.format(
                                col[0]
                            ))
                            logging.error("<" * 50, end='')
                            logging.error(">" * 50)
                            raise
                        if self.parsed_row_format == "delimited":
                            plist.append(pd)
                        if self.parsed_row_format == "fixed-width":
                            pass
                        else:
                            pdict[col[0]] = pd
                    if self.parsed_row_format == "delimited":
                        yield self.parsed_row_sep.join((str(e) for e in plist))
                    elif self.parsed_row_format == "fixed-width":
                        yield d
                    else:
                        yield pdict
                    line_number += 1
                except Exception as e:
                    if self.stop_on_error < 0 or errornous_line_count < self.stop_on_error:
                        logging.error(str(e))
                        logging.error("DATA >>> ")
                        logging.error(d)
                        errornous_line_count += 1
                        logging.error("CONTINUING TO PARSE DATA BECAUSE STOP_ON_ERROR CONDITION NOT MET YET!")
                    else:
                        raise e
        else:
            line_number = 0
            errornous_line_count = 0
            json_allowed = None
            for d in data:
                try:
                    if type(d) == str:
                        json_allowed = True
                        d = json.loads(d)
                    if len(list(d.keys())) > len(self.schema):
                        raise UnexpectedParsingException(
                            "Number of columns in line - {} is higher that number of declared columns in schema.".format(
                                line_number + 1
                            )
                        )
                    pdict: typing.Dict = {}
                    for col, _ in self.schema:
                        if col in list(d.keys()):
                            try:
                                pdict[col] = self._parser_funcs[col](d[col])
                            except Exception as e:
                                logging.error("<" * 50, end='')
                                logging.error(">" * 50)
                                logging.error('LINE NUMBER: {}'.format(
                                    line_number + 1
                                ))
                                logging.error('COLUMN NAME: {}'.format(
                                    col
                                ))
                                logging.error("<" * 50, end='')
                                logging.error(">" * 50)
                                raise e
                    if self.parsed_row_format == "json":
                        if not json_allowed:
                            raise UnexpectedSystemException(
                                "`json` formatted output is not supported for `dict` formatted input."
                            )
                        yield json.dumps(d)
                    else:
                        yield pdict
                    line_number += 1
                except Exception as e:
                    if isinstance(e, UnexpectedSystemException):
                        raise e
                    if self.stop_on_error < 0 or errornous_line_count < self.stop_on_error:
                        logging.error(str(e))
                        logging.error("DATA >>> ")
                        logging.error(d)
                        errornous_line_count += 1
                        logging.error("CONTINUING TO PARSE DATA BECAUSE STOP_ON_ERROR CONDITION NOT MET YET!")
                    else:
                        raise e
