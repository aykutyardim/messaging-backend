# Requirements
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_login_failed

# Serializers
from accounts.serializers import LoginActivitySerializer
# Models
from accounts.models import LoginActivity

# Parse User Agent
def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]

# Parse User IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Save Login Fail
@receiver(user_login_failed)
def log_user_logged_in_failed(signal, sender, **kwargs):
    try:
        data = {}
        request = kwargs.get('request')
        data['login_IP'] = get_client_ip(request)
        data['user_agent'] = get_user_agent(request)
        data['status'] = LoginActivity.FAILED
        data['login_username'] = request.data.get('username','<unknown>')

        serializer = LoginActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
    except:
        pass

# Save Login Success
@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    try:
        data = {}
        data['login_IP'] = get_client_ip(request)
        data['user_agent'] = get_user_agent(request)
        data['login_username'] = user.username
        data['status'] = LoginActivity.SUCCESS

        serializer = LoginActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()

    except:
        pass