from rest_framework.exceptions import APIException
from rest_framework import status


class GenericException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    code = 1000
    summary = 'Error'
    verbose = False

    def __init__(self, message=None, status_code=400):
        if not message:
            message = 'We hit a snag. Please check your internet connection and try'
        if status:
            self.status_code = status_code
        super().__init__(message)

    def serialize(self):
        return {
            'code': self.status_code,
            'message': self.detail,
            'summary': self.summary
        }


class ObjectNotFoundException(GenericException):
    code = 1001

    def __init__(self, message=None, object_id=None):
        if not message:
            message = 'Object not found: [%s] ' % object_id
        super().__init__(message)


class MissingRequiredFieldException(GenericException):
    code = 1002

    def __init__(self, message=None, field_name=None):
        if not message:
            message = 'Missing required field: [%s] ' % field_name
        super().__init__(message)


class InvalidParameterException(GenericException):
    code = 1005

    def __init__(self, message=None):
        super().__init__(message=message)


class InvalidUploadFormException(GenericException):
    code = 1006

    def __init__(self, message=None):
        super().__init__(message=message)


class NameExistsException(GenericException):
    code = 1007
    verbose = True

    def __init__(self, message=None):
        super().__init__(message=message)


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT

    code = 1008
    summary = 'Error'
    verbose = False

    def __init__(self, message=None, status_code=409):
        if not message:
            message = 'We hit a snag. Please check your internet connection and try'
        if status:
            self.status_code = status_code
        super().__init__(message)

    def serialize(self):
        return {
            'code': self.status_code,
            'message': self.detail,
            'summary': self.summary
        }


class ValidateField(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    code = 1009
    summary = 'Error'
    verbose = False

    def __init__(self, message=None, status_code=400):
        if not message:
            message = 'We hit a snag. Please check your internet connection and try'
        if status:
            self.status_code = status_code
        super().__init__(message)

    def serialize(self):
        return {
            'code': self.status_code,
            'message': self.detail,
            'summary': self.summary
        }


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN

    code = 1009
    summary = 'Error'
    verbose = False

    def __init__(self, message=None, status_code=403):
        if not message:
            message = 'We hit a snag. Please check your internet connection and try'
        if status:
            self.status_code = status_code
        super().__init__(message)

    def serialize(self):
        return {
            'code': self.status_code,
            'message': self.detail,
            'summary': self.summary
        }
