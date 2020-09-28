from rest_framework.exceptions import ValidationError, APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from accounts.signals import get_client_ip, get_user_agent
from exceptions.serializers import ExceptionSerializer

# Customized Exception Handler
def custom_exception_handler(exc, context):

    try:
        # Initials
        request = context['request']
        response = exception_handler(exc, context)
        status_code = response.status_code

        # Set error codes
        if isinstance(exc, ValidationError) or isinstance(exc, APIException):
            error_codes = exc.get_codes()
        else:
            error_codes = '<unknown>'
        
        # Set user name
        if request.user.is_anonymous:
            username = '<unknown>'
        else:
            username = request.user.username

        # Set exception data
        data={}
        data['username'] = username
        data['user_IP'] = get_client_ip(request)
        data['user_agent'] = get_user_agent(request)
        data['request_method'] = request.META.get('REQUEST_METHOD', '<unknown>')[:30]
        data['request_path'] = request.META.get('PATH_INFO', '<unknown>')[:255]
        data['status_code'] = status_code
        data['error_codes'] = error_codes
    
        # Serialize and validate exception data
        serializer = ExceptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Save serialized data
        serializer.save()

        # Return response
        return response

    # Return timed out error for DB connection failures 
    except:
        return Response('The server timed out.',
            status=status.HTTP_408_REQUEST_TIMEOUT)