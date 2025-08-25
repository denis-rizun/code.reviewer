class CodeReviewException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotInitializedException(CodeReviewException):
    pass


class BadResponseException(CodeReviewException):
    pass


class SerializationException(CodeReviewException):
    pass


class DeserializationException(CodeReviewException):
    pass


class NotFoundException(CodeReviewException):
    pass
