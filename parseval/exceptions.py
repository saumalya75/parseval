class UnexpectedSystemException(BaseException):
    def __init__(self, msg="Unexpected error occurred."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<UnexpectedSystemException({self.msg})>"


class NullValueInNotNullFieldException(BaseException):
    def __init__(self, msg="NULL value detected in Not NULL field."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<NullValueInNotNullFieldException({self.msg})>"


class SchemaBuildException(BaseException):
    def __init__(self, msg="Unexpected error occurred while building the schema. Please declare the schema properly."):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<SchemaBuildException({self.msg})>"
