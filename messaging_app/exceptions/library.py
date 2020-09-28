from rest_framework.exceptions import APIException
from rest_framework import status

# Custom API Exception Library
class DateException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'detail' : ['Invalid Date String']}
    default_code = 'invalid'

class OperationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'detail' : ['Operation is not allowed.']}
    default_code = 'not_allowed'

class BlockedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'blocked' : ['This field is required.']}
    default_code = 'required'

class TargetException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'target' : ['This field is required.']}
    default_code = 'required'
