from core.exceptions import GenericException
from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework.exceptions import ValidationError as SerializerValidationError


class MissedUsernameOrEmailException(GenericException):
    code = 'missed_username_or_email'
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = 'Username or email is required'
        super().__init__(message=message)


class ValidationError(SerializerValidationError, ModelValidationError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_list = [self]
        self.message = args[0]
        self.params = []
