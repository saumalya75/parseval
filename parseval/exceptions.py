class UnexpectedSystemException(Exception):
    def __init__(self, msg="Unexpected error occurred."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<UnexpectedSystemException({self.msg})>"


class UnexpectedParsingException(Exception):
    def __init__(self, msg="Unexpected error occurred while parsing the data."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<UnexpectedParsingException({self.msg})>"


class UnsupportedDatatypeException(Exception):
    def __init__(self, msg="Unsupported datatype for column."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<UnsupportedDatatypeException({self.msg})>"


class SchemaBuildException(Exception):
    def __init__(self, msg="Unexpected error occurred while building the schema. Please declare the schema properly."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<SchemaBuildException({self.msg})>"


class NullValueInNotNullFieldException(Exception):
    def __init__(self, msg="NULL value detected in Not NULL field."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<NullValueInNotNullFieldException({self.msg})>"


class ValidValueCheckException(Exception):
    def __init__(self, msg="Provided value is not part of valid value list."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<ValidValueCheckException({self.msg})>"


class MaximumValueConstraintException(Exception):
    def __init__(self, msg="Provided value is higher than maximum allowed value for the column."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<MaximumValueConstraintException({self.msg})>"


class MinimumValueConstraintException(Exception):
    def __init__(self, msg="Provided value is lower than maximum allowed value for the column."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<MinimumValueConstraintException({self.msg})>"


class RegexMatchException(Exception):
    def __init__(self, msg="Provided value does not match with expected pattern."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<RegexMatchException({self.msg})>"


class IntegerParsingException(Exception):
    def __init__(self, msg="Column value could not be casted to Integer."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<IntegerParsingException({self.msg})>"


class FloatParsingException(Exception):
    def __init__(self, msg="Column value could not be casted to Float."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<FloatParsingException({self.msg})>"


class BooleanParsingException(Exception):
    def __init__(self, msg="Column value could not be casted to Boolean."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<BooleanParsingException({self.msg})>"


class DateTimeParsingException(Exception):
    def __init__(self, msg="Column value is not aligned to the provided formats."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<DateTimeParsingException({self.msg})>"
