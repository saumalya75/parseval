class UnexpectedSystemException(BaseException):
    def __init__(self, msg="Unexpected error occurred."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<UnexpectedSystemException({self.msg})>"


class UnexpectedParsingException(BaseException):
    def __init__(self, msg="Unexpected error occurred while parsing the data."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<UnexpectedParsingException({self.msg})>"


class SchemaBuildException(BaseException):
    def __init__(self, msg="Unexpected error occurred while building the schema. Please declare the schema properly."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<SchemaBuildException({self.msg})>"


class NullValueInNotNullFieldException(BaseException):
    def __init__(self, msg="NULL value detected in Not NULL field."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<NullValueInNotNullFieldException({self.msg})>"


class ValidValueCheckException(BaseException):
    def __init__(self, msg="Provided value is not part of valid value list."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<ValidValueCheckException({self.msg})>"


class MaximumValueConstraintException(BaseException):
    def __init__(self, msg="Provided value is higher than maximum allowed value for the column."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<MaximumValueConstraintException({self.msg})>"


class MinimumValueConstraintException(BaseException):
    def __init__(self, msg="Provided value is lower than maximum allowed value for the column."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<MinimumValueConstraintException({self.msg})>"
