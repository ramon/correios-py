class BaseCorreiosError(Exception):
    pass


class ModelError(BaseCorreiosError):
    pass


class InvalidDeclaredValueError(ModelError):
    pass


class MaximumDeclaredValueError(InvalidDeclaredValueError):
    pass


class MinimumDeclaredValueError(InvalidDeclaredValueError):
    pass


class InvalidExtraServiceError(ModelError):
    pass
